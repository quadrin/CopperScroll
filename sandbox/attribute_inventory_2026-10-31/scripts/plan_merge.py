"""Plan pass (PLAN_PASS.md): agreement between plan readers, third-reading list, and merge into the consolidated table.

usage: python3 plan_merge.py agree     -> out/atq41plans_agreement.json, out/atq41plans_to_adjudicate.csv
       python3 plan_merge.py merge     -> out/atq41_consolidated_v2.csv (needs keyed/atq41plans_C_adjudication.csv)
"""
import csv
import glob
import json
import re
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
VALS = ["n_openings_plan", "opening_dirs_plan", "max_length_m", "max_width_m", "n_pillars_plan", "n_steps_plan"]


def norm_key(k):
    k = (k or "").upper().replace(" ", "")
    k = re.sub(r"^(CAVE|ATQ41:)", "", k)
    # Hebrew-order labels such as "49/V" -> "V/49" (fix added 31 Oct before agreement was run:
    # a plan reader keyed labels in the caption's order)
    m = re.match(r"^(\d+[A-Z]?)/([IVX]+)$", k)
    if m:
        k = f"{m.group(2)}/{m.group(1)}"
    return k


def num(v):
    v = (v or "").strip()
    m = re.match(r"^(\d+(?:\.\d+)?)$", v)
    return float(m.group(1)) if m else None


def dir_sets(v):
    """'E;N/NE' -> [{'E'}, {'N','NE'}]"""
    out = []
    for part in filter(None, (v or "").replace(",", ";").split(";")):
        s = {p.strip() for p in part.split("/") if p.strip() in COMPASS}
        if s:
            out.append(s)
    return out


def near(a, b):
    i, j = COMPASS.index(a), COMPASS.index(b)
    return min((i - j) % 8, (j - i) % 8) <= 1


def dirs_agree(va, vb):
    A, B = dir_sets(va), dir_sets(vb)
    if not A and not B:
        return None
    if not A or not B or len(A) != len(B):
        return False
    used = set()
    for sa in A:
        hit = next((k for k, sb in enumerate(B) if k not in used and any(near(x, y) for x in sa for y in sb)), None)
        if hit is None:
            return False
        used.add(hit)
    return True


def load(reader):
    best = {}
    for f in sorted(glob.glob(str(RUN / f"keyed/atq41plans_{reader}_g*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            k = norm_key(r.get("key"))
            if not k:
                continue
            if (r.get("plan_ref") or "").replace(" ", "") == "2561:1":
                # Both readers flagged it: captioned 57/X like Plan 3, but placed in and cited by the 35/X entry.
                # Excluded rather than guessed (decided before agreement was computed).
                continue
            score = (r.get("north_arrow", "").strip().lower() == "yes", {"high": 2, "medium": 1}.get(r.get("confidence", "").strip(), 0))
            if k not in best or score > best[k][0]:
                best[k] = (score, {c: (r.get(c) or "").strip() for c in r})
    return {k: v[1] for k, v in best.items()}


def agree():
    A, B = load("A"), load("B")
    keys = sorted(set(A) | set(B))
    stats = {"A_keys": len(A), "B_keys": len(B), "matched": len(set(A) & set(B)), "A_only": sorted(set(A) - set(B)), "B_only": sorted(set(B) - set(A))}
    agg = {"n_openings": [0, 0], "dirs": [0, 0], "size": [0, 0], "one_blank": 0}
    todo = []
    for k in keys:
        a, b = A.get(k), B.get(k)
        if not (a and b):
            continue
        for f in VALS:
            va, vb = a.get(f, ""), b.get(f, "")
            if not va and not vb:
                continue
            if bool(va) != bool(vb):
                agg["one_blank"] += 1
                todo.append(dict(key=k, field=f, A=va, B=vb, plan_A=a.get("plan_ref", ""), plan_B=b.get("plan_ref", ""), page_A=a.get("pdf_page", ""), page_B=b.get("pdf_page", "")))
                continue
            if f == "opening_dirs_plan":
                ok = dirs_agree(va, vb)
                agg["dirs"][1] += 1
                agg["dirs"][0] += bool(ok)
            elif f in ("max_length_m", "max_width_m"):
                x, y = num(va), num(vb)
                ok = x is not None and y is not None and abs(x - y) <= max(0.5, 0.1 * max(x, y))
                agg["size"][1] += 1
                agg["size"][0] += ok
            else:
                ok = va == vb
                if f == "n_openings_plan":
                    agg["n_openings"][1] += 1
                    agg["n_openings"][0] += ok
            if not ok:
                todo.append(dict(key=k, field=f, A=va, B=vb, plan_A=a.get("plan_ref", ""), plan_B=b.get("plan_ref", ""), page_A=a.get("pdf_page", ""), page_B=b.get("pdf_page", "")))
    stats["agreement"] = {k: ({"agree": v[0], "compared": v[1], "rate": round(v[0] / v[1], 3) if v[1] else None} if isinstance(v, list) else v) for k, v in agg.items()}
    stats["with_north_arrow"] = {R: sum(r.get("north_arrow", "").lower() == "yes" for r in D.values()) for R, D in (("A", A), ("B", B))}
    stats["with_dirs"] = {R: sum(bool(dir_sets(r.get("opening_dirs_plan"))) for r in D.values()) for R, D in (("A", A), ("B", B))}
    (RUN / "out").mkdir(exist_ok=True)
    json.dump(stats, open(RUN / "out/atq41plans_agreement.json", "w"), indent=1)
    with open(RUN / "out/atq41plans_to_adjudicate.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["key", "field", "A", "B", "plan_A", "plan_B", "page_A", "page_B"])
        w.writeheader()
        w.writerows(todo)
    print(json.dumps({k: v for k, v in stats.items() if k not in ("A_only", "B_only")}, indent=1))
    print("to adjudicate:", len(todo), "| A_only", len(stats["A_only"]), "| B_only", len(stats["B_only"]))


def first_dir(v):
    """Plan direction value -> schema value: keep one point per opening; a 'X/Y' boundary value keeps both as 'X/Y'."""
    return ";".join("/".join(sorted(s, key=COMPASS.index)) for s in dir_sets(v))


def merge():
    A, B = load("A"), load("B")
    C = {(r["key"], r["field"]): r["C_value"].strip() for r in csv.DictReader(open(RUN / "keyed/atq41plans_C_adjudication.csv", encoding="utf-8"))}
    plan = {}
    for k in set(A) | set(B):
        a, b = A.get(k, {}), B.get(k, {})
        vals = {}
        for f in VALS:
            va, vb = a.get(f, ""), b.get(f, "")
            if (k, f) in C:
                vals[f] = C[(k, f)]
            elif va and vb and (va == vb or (f == "opening_dirs_plan" and dirs_agree(va, vb)) or
                                (f in ("max_length_m", "max_width_m") and num(va) is not None and num(vb) is not None and abs(num(va) - num(vb)) <= max(0.5, 0.1 * max(num(va), num(vb))))):
                vals[f] = va
            elif a and b:
                vals[f] = ""  # unresolved disagreement: leave blank
            else:
                vals[f] = va or vb  # only one reader saw this plan: keep, flagged single-reader
        vals["plan_readers"] = "".join(x for x, D in (("A", A), ("B", B)) if k in D)
        vals["plan_ref"] = a.get("plan_ref") or b.get("plan_ref", "")
        plan[k] = vals
    rows = list(csv.DictReader(open(RUN / "out/atq41_consolidated.csv", encoding="utf-8")))
    fill = {"n_openings": "n_openings_plan", "opening_dirs": "opening_dirs_plan", "length_m": "max_length_m",
            "width_m": "max_width_m", "n_pillars": "n_pillars_plan", "n_steps": "n_steps_plan"}
    filled = {f: 0 for f in fill}
    conflicts = 0
    for r in rows:
        p = plan.get(r["key"])
        r["plan_ref"] = p["plan_ref"] if p else ""
        r["plan_readers"] = p["plan_readers"] if p else ""
        conf = []
        for f, pf in fill.items():
            r[f + "_src"] = "text" if r.get(f) not in ("", None) else ""
            if not p:
                continue
            pv = p.get(pf, "")
            if f == "opening_dirs" and pv:
                pv = first_dir(pv)
            if not pv or pv.lower() == "unknown":
                continue
            if r.get(f) in ("", None):
                r[f] = pv
                r[f + "_src"] = "plan" + ("" if p["plan_readers"] == "AB" else "_single")
                filled[f] += 1
            elif r[f] != pv:
                conf.append(f"{f}: text {r[f]} / plan {pv}")
        r["plan_conflict"] = "; ".join(conf)
        conflicts += bool(conf)
    cols = list(rows[0].keys())
    with open(RUN / "out/atq41_consolidated_v2.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    lab = [r for r in rows if "/" in r["key"]]
    def has(r, f):
        v = str(r.get(f, ""))
        return v not in ("", "unknown") and "|" not in v
    print("filled from plans:", filled, "| rows with a text/plan conflict:", conflicts)
    for f in ["n_openings", "opening_dirs", "length_m", "n_pillars", "n_steps"]:
        print(f"  {f}: {sum(has(r, f) for r in lab)} of {len(lab)}")
    print("  plan keys not in the text table:", sorted(set(plan) - {r['key'] for r in rows})[:40])


if __name__ == "__main__":
    {"agree": agree, "merge": merge}[sys.argv[1]]()
