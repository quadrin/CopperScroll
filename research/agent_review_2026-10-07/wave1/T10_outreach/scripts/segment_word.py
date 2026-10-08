"""Split a word region into letter boxes from the vertical darkness profile.
Prints candidate cut positions (local minima of groove darkness between letters).
Usage: python3 -I segment_word.py IMAGE x0 y0 x1 y1 n_letters OUT.png
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.signal import find_peaks

img = sys.argv[1]
x0, y0, x1, y1, n = map(int, sys.argv[2:7])
out = sys.argv[7]
g = np.asarray(Image.open(img).convert("L")).astype(float)
reg = g[y0:y1, x0:x1]
dark = ndi.gaussian_filter(reg, 6) - ndi.gaussian_filter(reg, 1)
dark[dark < 0] = 0
prof = ndi.gaussian_filter1d(dark.sum(0), 2.5)
# choose the n-1 deepest minima separated by >= 12 px
mins, _ = find_peaks(-prof, distance=12)
order = mins[np.argsort(prof[mins])][: n - 1]
cuts = sorted(int(c) for c in order)
edges = [0] + cuts + [x1 - x0]
boxes = [(x0 + edges[i], y0, x0 + edges[i + 1], y1) for i in range(len(edges) - 1)]
boxes = boxes[::-1]          # right-to-left reading order
im = Image.open(img).convert("RGB").crop((x0 - 10, y0 - 10, x1 + 10, y1 + 10))
im = im.resize((im.width * 3, im.height * 3))
d = ImageDraw.Draw(im)
for i, b in enumerate(boxes):
    d.rectangle([(b[0] - x0 + 10) * 3, 3, (b[2] - x0 + 10) * 3, im.height - 3], outline=(0, 255, 0))
    d.text(((b[0] - x0 + 10) * 3 + 3, 5), str(i), fill=(255, 255, 0))
im.save(out)
print([list(b) for b in boxes])
