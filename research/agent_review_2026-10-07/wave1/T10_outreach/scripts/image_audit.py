"""Basic quality audit of downloaded images: size, near-saturated (glare) fraction, sha256.
Usage: python3 -I image_audit.py OUT_CSV IMAGE [IMAGE ...]
"""
import sys, csv, hashlib, os
import numpy as np
from PIL import Image
out = sys.argv[1]
rows = []
for p in sys.argv[2:]:
    im = Image.open(p).convert("RGB")
    a = np.asarray(im)
    sat = (a.min(axis=2) >= 245).mean()
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    rows.append({"file": os.path.basename(p), "width": im.width, "height": im.height,
                 "near_saturated_fraction": round(float(sat), 4), "sha256": h})
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r["file"][:70], r["width"], r["height"], r["near_saturated_fraction"])
