"""Overview per copy plate: ink map + sparse grid for by-eye column bounds and line mapping."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
os.makedirs(os.path.join(BASE,'work','ov'), exist_ok=True)
for col in range(1,13):
    g = load_gray(copy_plate_path(col)); ink = ink_map(g)
    vis = Image.fromarray(np.clip(255*(1-ink*4),0,255).astype(np.uint8)).convert('RGB')
    d = ImageDraw.Draw(vis); H, W = g.shape
    for x in range(100, W, 100):
        d.line([(x,0),(x,H)], fill=(255,0,0) if x%500==0 else (0,160,255), width=2)
        d.text((x+3,3), str(x), fill=(255,0,0), font=font)
    for y in range(100, H, 100):
        d.line([(0,y),(W,y)], fill=(255,0,0) if y%500==0 else (0,160,255), width=2)
        d.text((3,y+3), str(y), fill=(255,0,0), font=font)
    s = 0.6
    vis.resize((int(W*s), int(H*s)), Image.LANCZOS).save(os.path.join(BASE,'work','ov',f'ov_col{col:02d}.png'))
    print(col, W, H)
