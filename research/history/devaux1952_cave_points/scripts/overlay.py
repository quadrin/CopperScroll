"""Overlay of measured points on pl. XX (stitched halves) -> pl_XX_points_overlay.png

Usage: python3 -I overlay.py <workdir>
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = sys.argv[1]
T = json.load(open(os.path.join(W, 'transforms.json')))
S = json.load(open(os.path.join(W, 'build_summary.json')))
PP = json.load(open(os.path.join(W, 'points_px.json')))
OFF = T['south_row_offset_px']
A = T['combined']['affine']
M = np.array([[A['E'][1], A['E'][2]], [A['N'][1], A['N'][2]]]); c0 = np.array([A['E'][0], A['N'][0]])
Minv = np.linalg.inv(M)


def pal2px(E, N):
    x, y = Minv @ (np.array([E, N]) - c0); return float(x), float(y)


def fnt(name, size):
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


north = Image.open(os.path.join(W, 'img_p23-001.jpg')).convert('RGB')
south = Image.open(os.path.join(W, 'img_p24-001.jpg')).convert('RGB')
canvas = Image.new('RGB', (1950, OFF + 3000), 'white')
canvas.paste(south, (0, OFF))
canvas.paste(north.crop((0, 0, 1950, 2440)), (0, 0))   # north rows 2440-2735 == south rows 264-559 (identical)

pts = {r['point']: (r['x'], r['y'] + (OFF if r['half'] == 'south' else 0), r['dot_conf']) for r in PP['points']}
COL = {'sure': (220, 0, 0), 'probable': (235, 130, 0), 'uncertain': (225, 0, 225)}
LAB = (0, 70, 230)
INSETS = [('A  3Q cluster (8 = 3Q)', (830, 940, 1160, 1360)),
          ('B  1Q (14) / 2Q (19) cluster', (880, 1580, 1080, 2010)),
          ('C  Wadi Qumran outlet', (700, 2470, 1010, 2930))]
# annotation offsets (source px) with leader lines; chosen to avoid the printed labels
OFFS = {1: (40, -22), 2: (-15, 35), 3: (-60, -28), 4: (32, -58), 7: (14, 24), 8: (22, 26), 9: (-58, 6), 10: (0, 30),
        12: (-50, 22), 14: (-55, -12), 15: (-55, 2), 19: (-45, 32), 18: (62, -4), 17: (56, 12), 21: (-40, 26),
        22: (-50, -15), 26: (-52, 12), 27: (16, -32), 28: (-52, 36), 29: (12, -46), 30: (-8, 32), 31: (-52, 12), 32: (0, 32),
        35: (0, 30), 37: (30, 20), 39: (-10, 30), 40: (-45, 10)}

big = canvas.copy(); d = ImageDraw.Draw(big)
f_in = fnt('DejaVuSans-Bold.ttf', 17)
for n, (x, y, conf) in pts.items():
    r = 13
    d.ellipse([x - r, y - r, x + r, y + r], outline=COL[conf], width=3)
    d.line([x - 4, y, x + 4, y], fill=COL[conf], width=1); d.line([x, y - 4, x, y + 4], fill=COL[conf], width=1)
    dx, dy = OFFS.get(n, (20, 20))
    tx, ty = x + dx, y + dy
    v = np.array([dx, dy], float); v /= np.linalg.norm(v)
    d.line([x + v[0] * (r + 1), y + v[1] * (r + 1), tx - v[0] * 9, ty - v[1] * 9], fill=LAB, width=1)
    d.text((tx, ty), str(n), fill=LAB, font=f_in, anchor='mm', stroke_width=3, stroke_fill=(255, 255, 255))
refs = {'trig_-72': (192.831, 126.829, 'trig 639'), 'trig_-388': (194.247, 126.976, 'trig 636'),
        'khq_square': (S['esri_khq_pal'][0], S['esri_khq_pal'][1], 'Kh. Qumran')}
for cid, (E, N) in S['ctrl_plate'].items():
    if cid not in refs:
        continue
    x, y = pal2px(E, N)
    d.ellipse([x - 12, y - 12, x + 12, y + 12], outline=(0, 150, 0), width=3)
    rx, ry = pal2px(refs[cid][0], refs[cid][1])
    d.line([rx - 8, ry - 8, rx + 8, ry + 8], fill=(0, 150, 0), width=3); d.line([rx - 8, ry + 8, rx + 8, ry - 8], fill=(0, 150, 0), width=3)

# full-map panel: downscale, then draw inset boxes and a few labels at readable size
X0, Y0, X1, Y1 = 40, 380, 1910, OFF + 2665
sc = 640 / (X1 - X0)
full = big.crop((X0, Y0, X1, Y1)).resize((640, int((Y1 - Y0) * sc)), Image.LANCZOS)
df = ImageDraw.Draw(full); f_sm = fnt('DejaVuSans-Bold.ttf', 13); f_tx = fnt('DejaVuSans.ttf', 15)
for title, (a, b, c, e) in INSETS:
    df.rectangle([(a - X0) * sc, (b - Y0) * sc, (c - X0) * sc, (e - Y0) * sc], outline=(0, 70, 230), width=2)
    df.text(((c - X0) * sc + 3, (b - Y0) * sc), title[0], fill=(0, 70, 230), font=f_sm, stroke_width=2, stroke_fill=(255, 255, 255))
for n in (35, 37, 39, 40):
    x, y, _ = pts[n]
    df.text(((x - X0) * sc + 9, (y - Y0) * sc - 4), str(n), fill=LAB, font=f_sm, stroke_width=2, stroke_fill=(255, 255, 255))
for cid, (E, N) in S['ctrl_plate'].items():
    if cid in refs:
        x, y = pal2px(E, N)
        df.text(((x - X0) * sc + 8, (y - Y0) * sc + 4), refs[cid][2], fill=(0, 120, 0), font=f_sm, stroke_width=2, stroke_fill=(255, 255, 255))

ims = []
for title, box in INSETS:
    im = big.crop(box)
    im = im.resize((int(im.size[0] * 1.4), int(im.size[1] * 1.4)), Image.LANCZOS)
    dd = ImageDraw.Draw(im); dd.rectangle([0, 0, im.size[0], 24], fill=(255, 255, 255)); dd.text((6, 3), title, fill=(0, 0, 0), font=f_tx)
    ims.append(im)
A_, B_, C_ = ims
colw = max(A_.size[0], C_.size[0])
Wd = 640 + 10 + colw + 10 + B_.size[0]
H = max(full.size[1], A_.size[1] + 10 + C_.size[1], B_.size[1])
out = Image.new('RGB', (Wd, H + 70), 'white')
out.paste(full, (0, 70)); out.paste(A_, (650, 70)); out.paste(C_, (650, 70 + A_.size[1] + 10)); out.paste(B_, (650 + colw + 10, 70))
dd = ImageDraw.Draw(out)
dd.text((6, 4), 'R. de Vaux, RB 60 (1953) pl. XX: measured dot centres. Circle colour = dot-position confidence (red sure, orange probable, magenta uncertain).', fill=(0, 0, 0), font=f_tx)
dd.text((6, 26), 'Blue = point number (leader line to its dot). Green circle = control symbol on the plate; green x = repo/modern position of the same feature.', fill=(0, 0, 0), font=f_tx)
dd.text((6, 48), 'Halves stitched on their pixel-identical overlap (south row 0 = north row 2176). Grid labels are Palestine-grid km. For checking only.', fill=(0, 0, 0), font=f_tx)
out = out.quantize(colors=160, method=Image.MEDIANCUT)
out.save(os.path.join(W, 'pl_XX_points_overlay.png'), optimize=True)
print(out.size, os.path.getsize(os.path.join(W, 'pl_XX_points_overlay.png')))
