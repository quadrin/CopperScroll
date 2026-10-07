"""Random audit of label->photo transfer: tiles of the copy photograph around each sampled
letter centre (1.6 H x 1.4 H, centre marked by ticks), label printed under each tile.
Sample: up to K letters per class from the 7 pair classes, RNG seed given.
Usage: python3 -I 09_audit_sheet.py labels.csv seed K out.png"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
import importlib.util
spec = importlib.util.spec_from_file_location('ex', os.path.join(os.path.dirname(os.path.abspath(__file__)), '08_extract_crops.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
lab, seed, K, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rows = list(csv.DictReader(open(lab, encoding='utf-8')))
H = ex.column_H(rows)
rng = np.random.default_rng(seed)
samp = []
for ch in 'ורחהתבכ':
    idx = [i for i,r in enumerate(rows) if r['letter']==ch]
    samp += list(rng.choice(idx, size=min(K,len(idx)), replace=False))
rng.shuffle(samp)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
TW, TH = 128, 112
tiles = []; key = []
plates = {}
for n,i in enumerate(samp):
    r = rows[i]; col = int(r['col'])
    if col not in plates: plates[col] = np.asarray(Image.open(copy_plate_path(col)).convert('L'))
    g = plates[col]; h = H[col]
    cx, cy = float(r['px']), float(r['pby'])
    x0, x1 = int(cx-0.8*h), int(cx+0.8*h); y0, y1 = int(cy-0.7*h), int(cy+0.7*h)
    sub = g[max(0,y0):y1, max(0,x0):x1]
    im = Image.fromarray(sub).resize((TW, TH), Image.LANCZOS).convert('RGB')
    d = ImageDraw.Draw(im)
    d.line([(TW/2,0),(TW/2,8)], fill=(255,0,0), width=2); d.line([(TW/2,TH-8),(TW/2,TH)], fill=(255,0,0), width=2)
    t = Image.new('RGB', (TW, TH+20), (255,255,255)); t.paste(im, (0,0))
    dt = ImageDraw.Draw(t); dt.text((4, TH+1), f"#{n}", fill=(0,0,0), font=fs); dt.text((TW-22, TH), r['letter'], fill=(200,0,0), font=font)
    tiles.append(t); key.append(dict(n=n, row=int(i), ref=r['ref'], word=r['word'], letter=r['letter']))
C = 8; R = (len(tiles)+C-1)//C
sheet = Image.new('RGB', (C*(TW+4), R*(TH+24)), (255,255,255))
for n,t in enumerate(tiles): sheet.paste(t, ((n%C)*(TW+4), (n//C)*(TH+24)))
sheet.save(outp)
json.dump(key, open(outp.replace('.png','_key.json'),'w'), ensure_ascii=False, indent=0)
print(len(tiles))
