"""Render a plate (or crop) with a labelled pixel grid for by-eye coordinate reading.
Usage: python3 -I grid_preview.py in.png out.png scale step [x0 y0 x1 y1]"""
import sys
from PIL import Image, ImageDraw, ImageFont
im = Image.open(sys.argv[1]).convert('RGB')
out, scale, step = sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
x0 = y0 = 0; x1, y1 = im.size
if len(sys.argv) > 5:
    x0, y0, x1, y1 = map(int, sys.argv[5:9])
im = im.crop((x0, y0, x1, y1))
W, H = int(im.size[0]*scale), int(im.size[1]*scale)
im = im.resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
except Exception:
    font = ImageFont.load_default()
for gx in range((x0//step+1)*step, x1, step):
    X = int((gx-x0)*scale); d.line([(X,0),(X,H)], fill=(0,255,255) if gx%(step*5) else (255,255,0), width=1)
    d.text((X+2, 2), str(gx), fill=(255,255,0), font=font)
for gy in range((y0//step+1)*step, y1, step):
    Y = int((gy-y0)*scale); d.line([(0,Y),(W,Y)], fill=(0,255,255) if gy%(step*5) else (255,255,0), width=1)
    d.text((2, Y+2), str(gy), fill=(255,255,0), font=font)
im.save(out)
