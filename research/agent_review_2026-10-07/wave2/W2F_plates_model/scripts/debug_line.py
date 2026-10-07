import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('al', os.path.join(os.path.dirname(os.path.abspath(__file__)), '05_align_words.py'))
from common import *
from PIL import ImageDraw, ImageFont
# re-use functions by exec of the module top (without running main loop): quick hack
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '05_align_words.py')).read()
src = src.split('rows = []; summ = []')[0]
exec(src)
col = int(sys.argv[1]); lines = [int(x) for x in sys.argv[2:]]
fc = json.load(open(os.path.join(BASE,'data',f'fac_components_col{col:02d}.json')))
colt = [c for c in txt['columns'] if c['c']==col][0]
f = np.asarray(Image.open(fac_plate_path(col)).convert('L')) > 127
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
strips = []
for ln in lines:
    li = ln-1; l = colt['lines'][li]
    comps = [c for c in fc['comps'] if c['line']==li]
    glyphs = make_glyphs(comps, fc['Lh'])
    ref, toks = tokens_for_line(col, l)
    assign, gaps, medgap, cost, nsk = dp_align(glyphs, toks, fc['Lh'])
    print(ref, [ (t['text'], t['exp']) for t in toks])
    print(' gaps', [int(g) for g in gaps], 'med', medgap)
    print(' assign', assign)
    y0 = min(g['y0'] for g in glyphs)-25; y1 = max(g['y1'] for g in glyphs)+5
    x0 = min(g['x0'] for g in glyphs)-5; x1 = max(g['x1'] for g in glyphs)+5
    im = Image.fromarray((f[y0:y1, x0:x1]*200).astype(np.uint8)).convert('RGB'); d = ImageDraw.Draw(im)
    tokof = {g:j for j,gl in assign.items() for g in gl}
    for gi,g in enumerate(glyphs):
        d.rectangle([g['x0']-x0,g['y0']-y0,g['x1']-x0,g['y1']-y0], outline=(255,0,0) if tokof.get(gi,-1)%2==0 else (0,200,255))
        d.text((g['x0']-x0+2, 2), f"{gi}:{tokof.get(gi,'-')}", fill=(255,255,0), font=font)
    strips.append(im)
W = max(s.size[0] for s in strips); H = sum(s.size[1] for s in strips)
out = Image.new('RGB',(W,H)); y=0
for s in strips: out.paste(s,(W-s.size[0],y)); y+=s.size[1]
out.save(os.path.join(BASE,'work','align','debug.png'))
