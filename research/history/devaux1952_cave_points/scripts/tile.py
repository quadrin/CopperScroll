"""Render a zoomed crop with pixel ticks and detected blobs.

Usage: python3 -I tile.py <workdir> <half> <x0> <y0> <x1> <y1> <scale> <name> [marks]
marks: optional 'x,y;x,y' list of extra crosses (source px)
"""
import sys, os, json
from PIL import Image, ImageDraw

W, half = sys.argv[1], sys.argv[2]
x0, y0, x1, y1, sc = map(int, sys.argv[3:8])
name = sys.argv[8]
marks = sys.argv[9] if len(sys.argv) > 9 else ''
fn = {'north': 'img_p23-001.jpg', 'south': 'img_p24-001.jpg'}[half]
im = Image.open(os.path.join(W, fn)).convert('RGB').crop((x0, y0, x1, y1))
im = im.resize((im.size[0] * sc, im.size[1] * sc), Image.LANCZOS)
d = ImageDraw.Draw(im)
step = 25 if sc >= 3 else 50
for x in range((x0 // step + 1) * step, x1, step):
    X = (x - x0) * sc; d.line([(X, 0), (X, 10)], fill=(255, 0, 0), width=2); d.text((X + 2, 10), str(x), fill=(255, 0, 0))
for y in range((y0 // step + 1) * step, y1, step):
    Y = (y - y0) * sc; d.line([(0, Y), (10, Y)], fill=(255, 0, 0), width=2); d.text((12, Y - 5), str(y), fill=(255, 0, 0))
B = json.load(open(os.path.join(W, 'blobs.json')))[half]
for b in B:
    if x0 <= b['x'] < x1 and y0 <= b['y'] < y1:
        X, Y = (b['x'] - x0) * sc, (b['y'] - y0) * sc
        d.line([(X - 4, Y), (X + 4, Y)], fill=(0, 120, 255), width=1)
        d.line([(X, Y - 4), (X, Y + 4)], fill=(0, 120, 255), width=1)
        d.text((X + 6, Y + 6), b['id'], fill=(0, 90, 255))
if marks:
    for m in marks.split(';'):
        mx, my = map(float, m.split(','))
        X, Y = (mx - x0) * sc, (my - y0) * sc
        d.ellipse([X - 14 * sc / 2, Y - 14 * sc / 2, X + 14 * sc / 2, Y + 14 * sc / 2], outline=(0, 160, 0), width=2)
im.save(os.path.join(W, 'tiles', name + '.png'))
