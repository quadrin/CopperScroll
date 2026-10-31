"""Shape similarity of Hebrew letter pairs in a traced Herodian formal book hand.

Font: 'Hebrew Square Habakkuk' (Yoram Gnat, Culmus Ancient Semitic Fonts 0.06-1, GPL-2; README: modelled on the
Habakkuk Commentary 1QpHab, Qumran, ~0 CE = Herodian formal hand). Source tarball:
https://sourceforge.net/projects/culmus/files/ancient_fonts/AncientSemiticFonts-0.06-1/AncientSemiticFonts-0.06-1.TTF.tgz/download
Method (fixed before any gazetteer was touched): render the 22 base letters at 96 px on a common baseline/origin
(relative size and position kept), Gaussian blur sigma 3 px, then similarity = max over shifts (-8..8 px, step 2) of the
cosine similarity of the blurred images. Final forms are not used (Delitzsch 1920 p. 119 n. 1: leave finals aside).
usage: python3 -I build_shape.py FONT.ttf OUT.csv
"""
import sys, csv, itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter, shift as nd_shift
FONT, OUT = sys.argv[1], sys.argv[2]
LET = 'אבגדהוזחטיכלמנסעפצקרשת'
f = ImageFont.truetype(FONT, 96)
def render(c):
    im = Image.new('L', (160, 200), 0); d = ImageDraw.Draw(im)
    d.text((30, 40), c, font=f, fill=255)
    a = np.asarray(im, dtype=float) / 255.0
    return gaussian_filter(a, 3.0)
R = {c: render(c) for c in LET}
def sim(a, b):
    best = -1
    for dx in range(-8, 9, 2):
        for dy in range(-8, 9, 2):
            bb = np.roll(np.roll(b, dy, 0), dx, 1)
            s = float((a * bb).sum() / (np.sqrt((a * a).sum() * (bb * bb).sum()) + 1e-12))
            best = max(best, s)
    return best
rows = []
for x, y in itertools.combinations(LET, 2):
    rows.append(dict(pair=f'{x}–{y}', letter_1=x, letter_2=y, shape_sim=round(sim(R[x], R[y]), 5)))
with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
rows.sort(key=lambda r: -r['shape_sim'])
for r in rows[:25]: print(r['pair'], r['shape_sim'])
