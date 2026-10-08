import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('al', os.path.join(os.path.dirname(os.path.abspath(__file__)), '05_align_letters.py'))
sys.argv = [sys.argv[0]] + sys.argv[1:]
argv = sys.argv[1:]
sys.argv = [sys.argv[0]]
al = importlib.util.module_from_spec(spec); spec.loader.exec_module(al)
from common import *
from PIL import ImageDraw, ImageFont
col = int(argv[0]); lines = [int(x) for x in argv[1:]]
fc = json.load(open(os.path.join(BASE,'data',f'fac_components_col{col:02d}.json')))
colt = [c for c in al.txt['columns'] if c['c']==col][0]
f = np.asarray(Image.open(fac_plate_path(col)).convert('L')) > 127
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
strips = []
for ln in lines:
    li = ln-1; l = colt['lines'][li]
    a_, b_ = fc['line_a'][li], fc['line_b'][li]; Lh = fc['Lh']
    comps0 = [c for c in fc['comps'] if c['line']==li and (abs((c['y0']+c['y1'])/2-(a_+b_*((c['x0']+c['x1'])/2-fc['xc'])))<=0.75*Lh or c['y0']<=a_+b_*((c['x0']+c['x1'])/2-fc['xc'])<=c['y1'])]
    ref, units = al.letter_seq(col, l)
    comps, assign, skips, gaps, medgap, cost, post, paired = al.align(comps0, units, fc['Lh'])
    print(ref, ''.join(u.get('ch','[%s]'%u['text']) + ('|' if u['last'] else '') for u in units))
    print(' gaps', [int(g) for g in gaps], 'skips', skips, 'paired', sorted(paired))
    print(' assign', {j:(units[j].get('ch','*'),cs,round(post.get(j,0),2)) for j,cs in assign.items()})
    lab = {}
    for j, cs in assign.items():
        for c in cs: lab[c] = (j, units[j].get('ch', '*'))
    y0 = max(0,min(c['y0'] for c in comps)-22); y1 = max(c['y1'] for c in comps)+3
    x0 = max(0,min(c['x0'] for c in comps)-5); x1 = max(c['x1'] for c in comps)+5
    im = Image.fromarray((f[y0:y1, x0:x1]*200).astype(np.uint8)).convert('RGB'); d = ImageDraw.Draw(im)
    for ci,c in enumerate(comps):
        j = lab.get(ci, (-1,'-'))[0]
        d.rectangle([c['x0']-x0,c['y0']-y0,c['x1']-x0,c['y1']-y0], outline=[(255,0,0),(0,200,255),(0,255,0)][j%3] if j>=0 else (90,90,90))
        d.text((c['x0']-x0+1, 1 + 10*(ci%2)), f"{ci}:{lab.get(ci,(-1,'-'))[1]}", fill=(255,255,0), font=font)
    strips.append(im)
W = max(s.size[0] for s in strips); H = sum(s.size[1] for s in strips)
out = Image.new('RGB',(W,H)); y=0
for s in strips: out.paste(s,(W-s.size[0],y)); y+=s.size[1]
out.save(os.path.join(BASE,'work','align','debug2.png'))
