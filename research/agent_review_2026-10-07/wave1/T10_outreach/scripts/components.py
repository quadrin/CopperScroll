"""Candidate letter components on an engraved-copper photograph.
Background-normalise, keep the darkest q-fraction of pixels, close small gaps, label components,
and draw numbered boxes for manual labelling.
Usage: python3 -I components.py IMAGE OUTDIR x_max q sigma
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from skimage import morphology, measure

img_path, outdir = sys.argv[1], sys.argv[2]
x_max, q, sigma = int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
os.makedirs(outdir, exist_ok=True)
rgb = np.asarray(Image.open(img_path).convert("RGB")).astype(float) / 255
g = rgb.mean(axis=2)[:, :x_max]
dark = ndi.gaussian_filter(g, sigma) - ndi.gaussian_filter(g, 1.0)   # dark grooves -> positive
t = np.quantile(dark, 1 - q)
b = dark > t
b = morphology.binary_closing(b, morphology.disk(2))
b = morphology.remove_small_objects(b, max_size=60)
lab = measure.label(b)
props = [p for p in measure.regionprops(lab) if 15 <= (p.bbox[2] - p.bbox[0]) <= 90 and 6 <= (p.bbox[3] - p.bbox[1]) <= 90]
vis = Image.fromarray((np.stack([g * 255] * 3, -1)).astype(np.uint8))
d = ImageDraw.Draw(vis)
recs = []
for i, p in enumerate(props):
    y0, x0, y1, x1 = p.bbox
    d.rectangle([x0, y0, x1, y1], outline=(255, 0, 0))
    d.text((x0, y0 - 9), str(i), fill=(255, 255, 0))
    recs.append({"id": i, "bbox": [int(x0), int(y0), int(x1), int(y1)], "area": int(p.area)})
vis.save(os.path.join(outdir, f"components_q{q}_s{sigma}.png"))
Image.fromarray((255 * (1 - b)).astype(np.uint8)).save(os.path.join(outdir, f"binary_q{q}_s{sigma}.png"))
json.dump(recs, open(os.path.join(outdir, f"components_q{q}_s{sigma}.json"), "w"))
print(len(recs), "components")
