"""Exploratory blind by-eye reference: tiles (photo context 1.6H x 1.4H, centre ticks), NO labels.
For each pair, 8 letters of each class sampled (seed 777) excluding letters shown in audit1.
Key saved separately (work/blind_key.json) and only read after guesses are written."""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
import importlib.util
spec = importlib.util.spec_from_file_location('ex', os.path.join(os.path.dirname(os.path.abspath(__file__)), '08_extract_crops.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
rows = list(csv.DictReader(open(os.path.join(BASE,'data','labels_train.csv'), encoding='utf-8')))
seen = {k['row'] for k in json.load(open(os.path.join(BASE,'work','audit1_key.json')))}
H = ex.column_H(rows); rng = np.random.default_rng(777)
fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
PAIRS = [('ו','ר'), ('ח','ה'), ('ח','ת'), ('ב','כ')]
key = {}; used = set(seen)
plates = {}
for pi,(a,b) in enumerate(PAIRS):
    samp = []
    for ch in (a,b):
        idx = [i for i,r in enumerate(rows) if r['letter']==ch and i not in used]
        s = list(rng.choice(idx, size=8, replace=False)); used.update(s); samp += s
    rng.shuffle(samp)
    TW, TH = 150, 130; tiles = []
    for n,i in enumerate(samp):
        r = rows[i]; col = int(r['col'])
        if col not in plates: plates[col] = np.asarray(Image.open(copy_plate_path(col)).convert('L'))
        g = plates[col]; h = H[col]; cx, cy = float(r['px']), float(r['pby'])
        sub = g[max(0,int(cy-0.7*h)):int(cy+0.7*h), max(0,int(cx-0.8*h)):int(cx+0.8*h)]
        im = Image.fromarray(sub).resize((TW,TH), Image.LANCZOS).convert('RGB'); d = ImageDraw.Draw(im)
        d.line([(TW/2,0),(TW/2,8)], fill=(255,0,0), width=2); d.line([(TW/2,TH-8),(TW/2,TH)], fill=(255,0,0), width=2)
        t = Image.new('RGB',(TW,TH+16),(255,255,255)); t.paste(im,(0,0)); ImageDraw.Draw(t).text((4,TH+1), f"{pi}-{n}", fill=(0,0,0), font=fs)
        tiles.append(t); key[f"{pi}-{n}"] = dict(row=int(i), letter=r['letter'], ref=r['ref'])
    sheet = Image.new('RGB', (8*(TW+4), 2*(TH+20)), (255,255,255))
    for n,t in enumerate(tiles): sheet.paste(t, ((n%8)*(TW+4), (n//8)*(TH+20)))
    sheet.save(os.path.join(BASE,'work',f'blind_pair{pi}.png'))
json.dump(key, open(os.path.join(BASE,'work','blind_key.json'),'w'), ensure_ascii=False, indent=0)
print('ok')
