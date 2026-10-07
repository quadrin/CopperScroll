"""Render review sheets of the automatic (Viterbi) alignment for by-eye verification.
Each line: facsimile strip; every letter's component box in its word colour, the assigned
transcription letter printed above it, the word index printed below. Grey boxes = components
not assigned to a countable letter. Margin text lists letters left unassigned.
Output: work/review/colNN_sheetK.png (3 lines per sheet) and data/viterbi_colNN.json."""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
spec = importlib.util.spec_from_file_location('al', os.path.join(os.path.dirname(os.path.abspath(__file__)), '05_align_letters.py'))
argv = sys.argv[1:]; sys.argv = [sys.argv[0]]
al = importlib.util.module_from_spec(spec); spec.loader.exec_module(al)
if os.path.exists(os.path.join(BASE,'data','width_priors.json')):
    al.PRI.update(json.load(open(os.path.join(BASE,'data','width_priors.json'))))
fH = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
fS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
PAL = [(255,70,70),(60,230,60),(80,170,255),(255,230,0),(255,60,255),(0,240,240),(255,150,0)]
os.makedirs(os.path.join(BASE,'work','review'), exist_ok=True)
cols = [int(c) for c in argv] or list(range(1,13))
for col in cols:
    fc = json.load(open(os.path.join(BASE,'data',f'fac_components_col{col:02d}.json')))
    Lh = fc['Lh']
    colt = [c for c in al.txt['columns'] if c['c']==col][0]
    f = np.asarray(Image.open(fac_plate_path(col)).convert('L')) > 127
    strips = []; vit = {}
    for li, l in enumerate(colt['lines']):
        a_, b_ = fc['line_a'][li], fc['line_b'][li]
        comps0 = [c for c in fc['comps'] if c['line']==li and (abs((c['y0']+c['y1'])/2-(a_+b_*((c['x0']+c['x1'])/2-fc['xc'])))<=0.75*Lh or c['y0']<=a_+b_*((c['x0']+c['x1'])/2-fc['xc'])<=c['y1'])]
        ref, units = al.letter_seq(col, l)
        if not comps0:
            continue
        comps, assign, skips, gaps, medgap, cost, post, paired = al.align(comps0, units, Lh)
        vit[ref] = dict(units=[{k:v for k,v in u.items()} for u in units], comps=comps, assign={str(k):v for k,v in assign.items()},
                        post={str(k):v for k,v in post.items()}, paired=sorted(paired))
        y0 = max(0, min(c['y0'] for c in comps)-34); y1 = min(f.shape[0], max(c['y1'] for c in comps)+22)
        x0 = max(0, min(c['x0'] for c in comps)-10); x1 = min(f.shape[1], max(c['x1'] for c in comps)+10)
        im = Image.fromarray((f[y0:y1, x0:x1]*170).astype(np.uint8)).convert('RGB'); d = ImageDraw.Draw(im)
        used = set()
        missing = []
        for j,u in enumerate(units):
            cs = assign.get(j, [])
            if u['kind'] != 'L':
                for c in cs:
                    C = comps[c]; used.add(c)
                    d.rectangle([C['x0']-x0,C['y0']-y0,C['x1']-x0,C['y1']-y0], outline=(150,150,150), width=1)
                if cs:
                    C = comps[cs[0]]; d.text((C['x0']-x0, 2), '[%s]' % u['text'][:6], fill=(200,200,200), font=fS)
                continue
            colr = PAL[u['wi'] % len(PAL)]
            if not cs:
                missing.append(f"{u['ch']}(w{u['wi']})"); continue
            cc = [comps[c] for c in cs]; used.update(cs)
            bx = [min(c['x0'] for c in cc)-x0, min(c['y0'] for c in cc)-y0, max(c['x1'] for c in cc)-x0, max(c['y1'] for c in cc)-y0]
            d.rectangle(bx, outline=colr, width=2)
            d.text(((bx[0]+bx[2])/2-8, 2), u['ch'], fill=colr, font=fH)
            if u['q'] == u['nlet']-1 or True:
                pass
        # word index below the word (centre of its letters)
        for wi in sorted({u['wi'] for u in units if u['kind']=='L'}):
            xs = [ (comps[c]['x0']+comps[c]['x1'])/2 for j,u in enumerate(units) if u['kind']=='L' and u['wi']==wi for c in assign.get(j,[])]
            if xs: d.text((np.mean(xs)-x0-10, im.size[1]-18), f"w{wi}", fill=PAL[wi%len(PAL)], font=fS)
        for ci,C in enumerate(comps):
            if ci not in used:
                d.rectangle([C['x0']-x0,C['y0']-y0,C['x1']-x0,C['y1']-y0], outline=(110,110,110), width=1)
        hdr = Image.new('RGB', (im.size[0], 20), (40,40,40)); dh = ImageDraw.Draw(hdr)
        dh.text((4,2), f"{ref}   missing: {' '.join(missing) if missing else '-'}   paired: {len(paired)}", fill=(255,255,255), font=fS)
        strips.append((ref, hdr, im))
    json.dump(vit, open(os.path.join(BASE,'data',f'viterbi_col{col:02d}.json'),'w'), ensure_ascii=False)
    for k in range(0, len(strips), 3):
        grp = strips[k:k+3]
        W = max(s[2].size[0] for s in grp); H = sum(s[1].size[1]+s[2].size[1]+6 for s in grp)
        out = Image.new('RGB', (W, H), (0,0,0)); y = 0
        for ref, hdr, im in grp:
            out.paste(hdr, (W-hdr.size[0], y)); y += hdr.size[1]
            out.paste(im, (W-im.size[0], y)); y += im.size[1]+6
        out.save(os.path.join(BASE,'work','review',f'col{col:02d}_sheet{k//3+1}.png'))
    print(col, len(strips), 'lines', flush=True)
