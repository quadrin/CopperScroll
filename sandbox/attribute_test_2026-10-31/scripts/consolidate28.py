"""Run 28 copy of the attribute-inventory consolidate.py. Same merge rule; it keeps sub-feature rows and parent_id,
because a describer site's caves are keyed as sub-features of the site (bench28.py applies the item definition).

Consolidate the two readers' rows with the third reading.

usage: python3 consolidate.py atq41
Rule: a value both readers keyed identically is kept; where the readers differ (incl. one blank),
the third reading (keyed/<src>_C_adjudication.csv) decides; differences on fields the third reading
did not cover are kept as "A|B". Grids (old Israel grid, EPSG:28191) are converted to WGS84.
Writes out/<src>_consolidated.csv and prints a summary.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

from pyproj import Transformer

RUN = Path(__file__).resolve().parents[1]
FIELDS = ["feature_class", "length_m", "width_m", "height_m", "depth_m", "diameter_m", "n_openings", "opening_dirs",
          "n_steps", "steps_where", "n_pillars", "plaster", "construction", "period", "in_window"]
TO_WGS = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)


def key(fid):
    return re.sub(r"^CAVE", "", fid.split(":", 1)[-1].upper().replace(" ", ""))


def grid_km(g):
    """'18900/14590' (10 m units), '1890/1459' (100 m), ranges 'a-b' -> midpoint; returns (E_km, N_km) or None."""
    parts = g.replace(" ", "").split("/")
    if len(parts) != 2:
        return None
    out = []
    for p in parts:
        m = re.match(r"^(\d+)(?:-(\d+))?$", p)
        if not m:
            return None
        a = m.group(1)
        v = int(a)
        if m.group(2):  # range of trailing digits, e.g. 18900-10
            b = m.group(2)
            v = (v + int(a[: len(a) - len(b)] + b)) / 2
        scale = {4: 0.1, 5: 0.01, 6: 0.001}.get(len(a))
        if scale is None:
            return None
        out.append(v * scale)
    return tuple(out)


def main():
    src = sys.argv[1]
    R = {}
    for rd in ("A", "B"):
        for r in csv.DictReader(open(RUN / f"keyed/{src}_{rd}.csv", encoding="utf-8")):
            k = key(r["feature_id"])
            R.setdefault(k, {}).setdefault(rd, r)
    C = {(r["key"], r["field"]): r for r in csv.DictReader(open(RUN / f"keyed/{src}_C_adjudication.csv", encoding="utf-8"))}
    rows, used_c, unresolved = [], 0, Counter()
    for k in sorted(R):
        a, b = R[k].get("A"), R[k].get("B")
        base = a or b
        row = {"key": k, "region": k.split("/")[0] if "/" in k else "", "readers": "".join(x for x in "AB" if R[k].get(x)),
               "page": base["page"], "site_name": base["site_name"],
               "parent_id": key((a or {}).get("parent_id", "") or (b or {}).get("parent_id", "")) if ((a or {}).get("parent_id") or (b or {}).get("parent_id")) else ""}
        for f in FIELDS:
            va, vb = (a or {}).get(f, "").strip(), (b or {}).get(f, "").strip()
            if a and b and va != vb:
                c = C.get((k, f))
                if c is not None:
                    row[f] = c["C_value"].strip()
                    used_c += 1
                else:
                    row[f] = f"{va}|{vb}"
                    unresolved[f] += 1
            else:
                row[f] = va or vb
        g = (a or {}).get("grid_printed") or (b or {}).get("grid_printed") or ""
        row["grid_printed"] = g
        gk = grid_km(g) if g else None
        if gk:
            lon, lat = TO_WGS.transform(gk[0] * 1000, gk[1] * 1000)
            if 31.5 <= lat <= 32.05 and 35.25 <= lon <= 35.55:  # extent of the 1993 survey map
                row.update(E_km=round(gk[0], 3), N_km=round(gk[1], 3), lat=round(lat, 5), lon=round(lon, 5))
            else:
                row["grid_flag"] = "outside survey extent (misprint?); not converted"
        rows.append(row)
    cols = ["key", "region", "readers", "parent_id", "site_name", "page", "grid_printed", "grid_flag", "E_km", "N_km", "lat", "lon"] + FIELDS
    with open(RUN / f"out/{src}_consolidated.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    # Summary only (31 Oct, before the Qumran third reading existed): sources without survey labels
    # (Qumran group) are summarised over all rows. The merge rule above is unchanged.
    lab = [r for r in rows if re.match(r"^[IVX]+/\d", r["key"])] or rows
    def has(r, f):
        v = str(r.get(f, ""))
        return v not in ("", "unknown") and "|" not in v
    print(f"features {len(rows)}; survey-labelled {len(lab)}; third-reading values used {used_c}; unresolved A|B {dict(unresolved)}")
    for f in ["lat", "length_m", "n_openings", "opening_dirs", "n_steps", "n_pillars", "plaster"]:
        print(f"  {f}: {sum(has(r, f) for r in lab)}")
    print("  in_window yes:", sum(r['in_window'] == 'yes' for r in lab))
    print("  classes:", Counter(r["feature_class"] for r in lab).most_common(8))
    print("  n_openings distribution:", Counter(r["n_openings"] for r in lab if has(r, "n_openings")).most_common(8))
    pos = [r for r in lab if "lat" in r]
    if pos:
        print("  lat/lon range:", min(r["lat"] for r in pos), max(r["lat"] for r in pos),
              min(r["lon"] for r in pos), max(r["lon"] for r in pos))


if __name__ == "__main__":
    main()
