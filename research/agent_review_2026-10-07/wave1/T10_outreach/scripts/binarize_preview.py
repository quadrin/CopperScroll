"""Background-normalise and binarise an engraved-copper photograph; write preview + line profile.
Usage: python3 -I binarize_preview.py IMAGE OUTDIR [x_max]
"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage import filters, morphology

img_path, outdir = sys.argv[1], sys.argv[2]
x_max = int(sys.argv[3]) if len(sys.argv) > 3 else None
os.makedirs(outdir, exist_ok=True)
rgb = np.asarray(Image.open(img_path).convert("RGB")).astype(float) / 255
g = rgb.mean(axis=2)
if x_max:
    g = g[:, :x_max]
bg = ndi.gaussian_filter(g, 25)
norm = g - bg                        # grooves are darker than local background
dark = -norm
t = filters.threshold_otsu(dark)
b = dark > t
b = morphology.remove_small_objects(b, 30)
Image.fromarray((255 * (1 - b)).astype(np.uint8)).save(os.path.join(outdir, "binary.png"))
v = (dark - dark.min()) / (dark.max() - dark.min())
Image.fromarray((255 * (1 - v)).astype(np.uint8)).save(os.path.join(outdir, "norm.png"))
prof = b.sum(axis=1)
np.savetxt(os.path.join(outdir, "row_profile.txt"), prof, fmt="%d")
print("threshold", t, "ink fraction", b.mean())
