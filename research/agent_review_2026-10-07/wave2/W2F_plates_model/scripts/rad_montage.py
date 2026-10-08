"""Low-res montage of radiograph images with a y-grid (every 100 px, labelled) for locating lines."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
files = sys.argv[2:]; out = sys.argv[1]; sc = 0.45
ims = []
for fn in files:
    im = Image.open(os.path.join(BASE,'plates','png',fn)).convert('RGB'); d = ImageDraw.Draw(im)
    for y in range(100, im.size[1], 100):
        d.line([(0,y),(im.size[0],y)], fill=(255,0,0) if y%500==0 else (0,200,255), width=2); d.text((3,y-24), str(y), fill=(255,255,0), font=font)
    for x in range(100, im.size[0], 100):
        d.line([(x,0),(x,12)], fill=(0,255,0), width=3); d.text((x+2,14), str(x), fill=(0,255,0), font=font)
    d.text((5, 40), fn.split('_')[0]+' '+fn.split('_')[-1][:3], fill=(255,0,255), font=font)
    ims.append(im.resize((int(im.size[0]*sc), int(im.size[1]*sc))))
W = sum(i.size[0] for i in ims)+10*len(ims); H = max(i.size[1] for i in ims)
M = Image.new('RGB', (W,H), (255,255,255)); x = 0
for i in ims: M.paste(i, (x,0)); x += i.size[0]+10
M.save(out)
