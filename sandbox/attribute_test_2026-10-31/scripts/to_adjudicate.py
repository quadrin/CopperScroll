"""List every field where the two describer readers differ (run 28 step 3), for the third reading.
Fields: class, sizes, openings, directions, steps, pillars, plaster (the same set as the Qumran third reading).
usage: python3 to_adjudicate.py <src>   -> out/<src>_to_adjudicate.csv
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agreement import key  # noqa: E402
from model28 import RUN, read_csv  # noqa: E402

FIELDS = ["feature_class", "length_m", "width_m", "height_m", "depth_m", "diameter_m", "n_openings", "opening_dirs",
          "n_steps", "n_pillars", "plaster"]
src = sys.argv[1]
R = {}
for rd in "AB":
    for r in read_csv(RUN / f"keyed/{src}_{rd}.csv"):
        R.setdefault(key(r["feature_id"]), {})[rd] = r
out = []
for k in sorted(R):
    a, b = R[k].get("A"), R[k].get("B")
    if not (a and b):
        continue
    for f in FIELDS:
        va, vb = (a.get(f) or "").strip(), (b.get(f) or "").strip()
        if va != vb:
            out.append({"source": src, "key": k, "field": f, "A": va, "B": vb, "page_A": a.get("page", ""), "page_B": b.get("page", "")})
with open(RUN / f"out/{src}_to_adjudicate.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["source", "key", "field", "A", "B", "page_A", "page_B"])
    w.writeheader()
    w.writerows(out)
from collections import Counter
print(len(out), Counter(r["field"] for r in out))
