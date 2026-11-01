"""Validate, merge and compare two readers' keyed files (READER_INSTRUCTIONS.md, "Agreement").

usage: python3 agreement.py <source_id>        e.g. atq41
Reads keyed/<source_id>_<R>_*.csv for R in A, B; writes keyed/<source_id>_<R>.csv (merged),
out/<source_id>_validation.json, out/<source_id>_agreement.json and out/<source_id>_pairs.csv.
"""
import csv
import glob
import json
import re
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
COLS = ["feature_id", "source_id", "page", "figure", "site_name", "grid_printed", "grid_system", "position_basis",
        "feature_class", "class_as_printed", "parent_id", "length_m", "width_m", "height_m", "depth_m", "diameter_m",
        "dims_basis", "n_openings", "opening_dirs", "n_steps", "steps_where", "plaster", "construction", "n_pillars",
        "relations", "rel_distance_m", "rel_bearing_deg", "period", "in_window", "quote", "confidence", "notes"]
CLASSES = set("cave chamber rock_shelter cistern pool reservoir basin ritual_bath conduit outlet dam spring tomb burial "
              "pit steps doorway court building room wall tower pillar columbarium cairn terrace road fissure other".split())
DIMS = ["length_m", "width_m", "height_m", "depth_m", "diameter_m"]
COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def num(v):
    v = (v or "").strip()
    if not v:
        return None
    m = re.match(r"^(\d+(?:\.\d+)?)(?:\s*-\s*(\d+(?:\.\d+)?))?$", v)
    if not m:
        return "bad"
    a = float(m.group(1))
    return (a + float(m.group(2))) / 2 if m.group(2) else a


def load(src, reader):
    rows, problems = [], []
    for f in sorted(glob.glob(str(RUN / f"keyed/{src}_{reader}_g*.csv"))):
        with open(f, encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            if rd.fieldnames != COLS:
                problems.append(f"{Path(f).name}: header differs ({set(COLS) ^ set(rd.fieldnames or [])})")
            for i, r in enumerate(rd):
                r = {c: (r.get(c) or "").strip() for c in COLS}
                r["_file"] = Path(f).name
                if r["feature_class"] not in CLASSES:
                    problems.append(f"{r['_file']} row {i + 2}: class '{r['feature_class']}'")
                for d in DIMS + ["n_openings", "n_steps", "n_pillars"]:
                    if num(r[d]) == "bad":
                        problems.append(f"{r['_file']} row {i + 2}: {d}='{r[d]}'")
                for d in filter(None, r["opening_dirs"].replace(",", ";").split(";")):
                    if d.strip() not in COMPASS:
                        problems.append(f"{r['_file']} row {i + 2}: direction '{d}'")
                if len(r["quote"].split()) > 15:
                    problems.append(f"{r['_file']} row {i + 2}: quote longer than 15 words")
                rows.append(r)
    return rows, problems


def key(fid):
    k = fid.split(":", 1)[-1].upper().replace(" ", "")
    k = re.sub(r"^CAVE", "", k)
    return k


def dirs(v):
    return {d.strip() for d in v.replace(",", ";").split(";") if d.strip() in COMPASS}


def dirs_agree(a, b):
    if not a and not b:
        return None
    if not a or not b:
        return False
    def near(x, y):
        i, j = COMPASS.index(x), COMPASS.index(y)
        return min((i - j) % 8, (j - i) % 8) <= 1
    return all(any(near(x, y) for y in b) for x in a) and all(any(near(y, x) for x in a) for y in b)


def main():
    src = sys.argv[1]
    (RUN / "out").mkdir(exist_ok=True)
    data, val = {}, {}
    for R in ("A", "B"):
        rows, problems = load(src, R)
        data[R] = rows
        val[R] = {"rows": len(rows), "problems": problems[:200], "n_problems": len(problems)}
        with open(RUN / f"keyed/{src}_{R}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
    json.dump(val, open(RUN / f"out/{src}_validation.json", "w"), indent=1)

    A = {}
    for r in data["A"]:
        A.setdefault(key(r["feature_id"]), r)
    B = {}
    for r in data["B"]:
        B.setdefault(key(r["feature_id"]), r)
    both = sorted(set(A) & set(B))
    pairs, stats = [], {"A_rows": len(data["A"]), "B_rows": len(data["B"]), "A_ids": len(A), "B_ids": len(B),
                        "matched": len(both), "A_only": len(set(A) - set(B)), "B_only": len(set(B) - set(A))}
    agg = {"class": [0, 0], "dims": [0, 0], "n_openings": [0, 0], "opening_dirs": [0, 0], "n_steps": [0, 0]}
    for k in both:
        a, b = A[k], B[k]
        p = {"key": k, "class_A": a["feature_class"], "class_B": b["feature_class"]}
        agg["class"][1] += 1
        agg["class"][0] += a["feature_class"] == b["feature_class"]
        for d in DIMS:
            x, y = num(a[d]), num(b[d])
            if isinstance(x, float) and isinstance(y, float):
                agg["dims"][1] += 1
                ok = abs(x - y) <= max(0.2, 0.1 * max(x, y))
                agg["dims"][0] += ok
                p[d] = f"{x}|{y}|{'ok' if ok else 'DIFF'}"
            elif (x is None) != (y is None):
                p[d] = f"{a[d]}|{b[d]}|one_blank"
        for d in ("n_openings", "n_steps"):
            x, y = num(a[d]), num(b[d])
            if isinstance(x, float) or isinstance(y, float):
                agg[d][1] += 1
                agg[d][0] += x == y
                p[d] = f"{a[d]}|{b[d]}"
        da, db = dirs(a["opening_dirs"]), dirs(b["opening_dirs"])
        ag = dirs_agree(da, db)
        if ag is not None:
            agg["opening_dirs"][1] += 1
            agg["opening_dirs"][0] += ag
            p["opening_dirs"] = f"{a['opening_dirs']}|{b['opening_dirs']}|{'ok' if ag else 'DIFF'}"
        pairs.append(p)
    stats["agreement"] = {k: {"agree": v[0], "compared": v[1], "rate": round(v[0] / v[1], 3) if v[1] else None}
                          for k, v in agg.items()}
    stats["A_only_ids"] = sorted(set(A) - set(B))[:300]
    stats["B_only_ids"] = sorted(set(B) - set(A))[:300]
    for R in ("A", "B"):
        rows = data[R]
        stats[f"{R}_attribute_counts"] = {
            "with_any_dimension": sum(any(isinstance(num(r[d]), float) for d in DIMS) for r in rows),
            "with_n_openings": sum(isinstance(num(r["n_openings"]), float) for r in rows),
            "with_opening_dirs": sum(bool(dirs(r["opening_dirs"])) for r in rows),
            "with_n_steps": sum(isinstance(num(r["n_steps"]), float) for r in rows),
            "with_grid": sum(bool(r["grid_printed"]) for r in rows),
            "in_window_yes": sum(r["in_window"] == "yes" for r in rows),
            "classes": {c: sum(r["feature_class"] == c for r in rows) for c in sorted(CLASSES) if any(r["feature_class"] == c for r in rows)},
        }
    json.dump(stats, open(RUN / f"out/{src}_agreement.json", "w"), indent=1)
    cols = sorted({k for p in pairs for k in p}, key=lambda c: (c != "key", c))
    with open(RUN / f"out/{src}_pairs.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(pairs)
    print(json.dumps({k: v for k, v in stats.items() if not k.endswith("_ids")}, indent=1))
    print("validation problems:", {R: val[R]["n_problems"] for R in val})


if __name__ == "__main__":
    main()
