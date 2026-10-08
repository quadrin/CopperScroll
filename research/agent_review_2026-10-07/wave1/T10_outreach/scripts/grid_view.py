"""Render a crop of an image with edge rulers (ticks every `step` px, labels every 5*step),
for manual letter-box annotation. Optionally overlay boxes from a JSON list.
Usage: python3 -I grid_view.py IMAGE OUT.png x0 y0 x1 y1 [scale] [step] [boxes.json]
"""
import sys, json
from PIL import Image, ImageDraw

img_path, out = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(int, sys.argv[3:7])
scale = float(sys.argv[7]) if len(sys.argv) > 7 else 2.0
step = int(sys.argv[8]) if len(sys.argv) > 8 else 10
boxes = json.load(open(sys.argv[9])) if len(sys.argv) > 9 else []
im = Image.open(img_path).convert("RGB").crop((x0, y0, x1, y1))
im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
pad = 28
canvas = Image.new("RGB", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0))
canvas.paste(im, (pad, pad))
d = ImageDraw.Draw(canvas)
for x in range((x0 // step + 1) * step, x1, step):
    X = pad + (x - x0) * scale
    L = 10 if x % (5 * step) == 0 else 4
    for yy in (pad, pad + im.height):
        d.line([(X, yy - L if yy == pad else yy), (X, yy if yy == pad else yy + L)], fill=(0, 255, 255))
    if x % (5 * step) == 0:
        d.text((X - 8, 2), str(x), fill=(255, 255, 0))
        d.text((X - 8, pad + im.height + 12), str(x), fill=(255, 255, 0))
for y in range((y0 // step + 1) * step, y1, step):
    Y = pad + (y - y0) * scale
    L = 10 if y % (5 * step) == 0 else 4
    d.line([(pad - L, Y), (pad, Y)], fill=(0, 255, 255))
    d.line([(pad + im.width, Y), (pad + im.width + L, Y)], fill=(0, 255, 255))
    if y % (5 * step) == 0:
        d.text((0, Y - 12), str(y), fill=(255, 255, 0))
        d.text((pad + im.width + 2, Y - 12), str(y), fill=(255, 255, 0))
for b in boxes:
    bx0, by0, bx1, by1 = b["bbox"]
    d.rectangle([pad + (bx0 - x0) * scale, pad + (by0 - y0) * scale, pad + (bx1 - x0) * scale, pad + (by1 - y0) * scale], outline=(0, 255, 0))
    d.text((pad + (bx0 - x0) * scale + 2, pad + (by0 - y0) * scale + 1), b.get("label", ""), fill=(0, 255, 0))
canvas.save(out)
print(out, canvas.size)
