"""Facsimile with coordinate grid (full-res px) for by-eye line anchoring.
Usage: python3 -I fac_grid.py col scale [y0 y1]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
col = int(sys.argv[1]); sc = float(sys.argv[2])
f = Image.open(fac_plate_path(col)).convert('L')
W,H = f.size
y0,y1 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv)>4 else (0,H)
f = f.crop((0,y0,W,y1))
im = f.resize((int(W*sc), int((y1-y0)*sc)), Image.LANCZOS).convert('RGB')
d = ImageDraw.Draw(im)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
for y in range((y0//25+1)*25, y1, 25):
    Y = (y-y0)*sc
    col_ = (255,60,60) if y%100==0 else (70,70,140)
    d.line([(0,Y),(im.size[0],Y)], fill=col_, width=1)
    if y%50==0:
        d.text((2,Y-14), str(y), fill=(255,120,120), font=font)
        d.text((im.size[0]-38,Y-14), str(y), fill=(255,120,120), font=font)
for x in range(100, W, 100):
    X = x*sc
    d.line([(X,0),(X,im.size[1])], fill=(60,160,60), width=1)
    d.text((X+2,2), str(x), fill=(120,255,120), font=font)
im.save(os.path.join(BASE,'work','fac',f'grid_col{col:02d}_{y0}.png'))
