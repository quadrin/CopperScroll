"""RULE step 2: select the Bar-Adon 1972 sites to key = cited in keyed/concordance.csv, or with a header grid
within 1 km of a positioned inventory feature. Grids are parsed as in bench28.parse_grid.
usage: python3 select_ba72.py -> keyed/ba72_selected.csv
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench28 import inventory, parse_grid  # noqa: E402
from model28 import RUN, read_csv  # noqa: E402

_, _, pos = inventory()
pts = [p for p in pos if p]
cited = {r["describer_ref"] for r in read_csv(RUN / "keyed/concordance.csv") if r["describer"] == "ba72"}
out = []
for r in read_csv(RUN / "keyed/ba72_headers.csv"):
    g = parse_grid(r["grid_printed"])
    d = min(((p[0] - g[0]) ** 2 + (p[1] - g[1]) ** 2) ** 0.5 for p in pts) if g else None
    if r["site"] in cited or (d is not None and d <= 1.0):
        out.append({"site": r["site"], "name": r["name"], "grid_printed": r["grid_printed"], "page": r["page"],
                    "nearest_inventory_km": round(d, 3) if d is not None else "", "reason": "cited" if r["site"] in cited else "within 1 km",
                    "grid_flag": g[3] if g else ""})
with open(RUN / "keyed/ba72_selected.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["site", "name", "grid_printed", "page", "nearest_inventory_km", "reason", "grid_flag"])
    w.writeheader()
    w.writerows(out)
print(len(out), "sites:", [(o["site"], o["nearest_inventory_km"], o["page"]) for o in out])
