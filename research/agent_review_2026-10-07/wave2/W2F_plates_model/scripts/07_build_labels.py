"""Apply by-eye review decisions to the saved Viterbi alignments -> verified letter labels.
Each accepted letter gets: facsimile box, stroke centroid (facsimile), photo coordinates via the
facsimile->photo affine, and flags (T10 candidate_undisputed, target exclusion).
Output: data/labels_verified.csv; prints class x column counts."""
import sys, os, csv, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import importlib.util
spec = importlib.util.spec_from_file_location('al', os.path.join(os.path.dirname(os.path.abspath(__file__)), '05_align_letters.py'))
sys.argv = [sys.argv[0]]
al = importlib.util.module_from_spec(spec); spec.loader.exec_module(al)
reg = json.load(open(os.path.join(BASE,'data','registration.json')))
dec = {}
for line in open(os.path.join(BASE,'data','review_decisions.txt'), encoding='utf-8'):
    line = line.strip()
    if not line or line.startswith('#'): continue
    ref, rest = line.split(':', 1)
    items = {}
    for tok in rest.split():
        if ':' in tok:
            w, qs = tok.split(':'); items[int(w[1:])] = set(int(q) for q in qs.split(','))
        else:
            items[int(tok[1:])] = None
    dec[ref.strip()] = items
rows = []
for col in range(1,13):
    vp = os.path.join(BASE,'data',f'viterbi_col{col:02d}.json')
    if not os.path.exists(vp): continue
    vit = json.load(open(vp, encoding='utf-8'))
    M = np.array(reg[str(col)]['A_fac2photo'])
    f = np.asarray(Image.open(fac_plate_path(col)).convert('L')) > 127
    fc = json.load(open(os.path.join(BASE,'data',f'fac_components_col{col:02d}.json')))
    for ref, v in vit.items():
        if ref not in dec: continue
        units, comps, assign = v['units'], v['comps'], v['assign']
        for j,u in enumerate(units):
            if u['kind'] != 'L': continue
            if u['wi'] not in dec[ref]: continue
            qs = dec[ref][u['wi']]
            if qs is not None and u['q'] not in qs: continue
            cs = assign.get(str(j), [])
            if not cs or not u['clean']: continue
            if (ref, u['wi']) in al.EXCLUDE: continue
            cc = [comps[c] for c in cs]
            bx = [min(c['x0'] for c in cc), min(c['y0'] for c in cc), max(c['x1'] for c in cc), max(c['y1'] for c in cc)]
            ys, xs = [], []
            for c in cc:
                sub = f[c['y0']:c['y1'], c['x0']:c['x1']]; yy, xx = np.nonzero(sub); ys.append(yy+c['y0']); xs.append(xx+c['x0'])
            ys = np.concatenate(ys); xs = np.concatenate(xs)
            p = M @ np.array([xs.mean(), ys.mean(), 1.0]); pb = M @ np.array([(bx[0]+bx[2])/2, (bx[1]+bx[3])/2, 1.0])
            # line centre at the letter (facsimile) -> photo, for vertical centring independent of letter shape
            li = int(ref.split()[1]) - 1
            yl = fc['line_a'][li] + fc['line_b'][li]*((bx[0]+bx[2])/2 - fc['xc'])
            pl = M @ np.array([(bx[0]+bx[2])/2, yl, 1.0])
            ir = al.inv.get((ref, u['wi'], u['ci']))
            rows.append(dict(col=col, ref=ref, word_index=u['wi'], word=u['text'], char_index=u['ci'], pos_in_word=u['q'],
                letter=u['ch'], base=al.FINALS.get(u['ch'], u['ch']),
                t10_candidate=(ir is not None and ir['candidate_undisputed']=='True' and ir['letter']==u['ch']),
                fx0=bx[0], fy0=bx[1], fx1=bx[2], fy1=bx[3], n_parts=len(cc),
                px=round(float(p[0]),1), py=round(float(p[1]),1), pbx=round(float(pb[0]),1), pby=round(float(pb[1]),1),
                plx=round(float(pl[0]),1), ply=round(float(pl[1]),1),
                fac_w=bx[2]-bx[0], fac_h=bx[3]-bx[1], Lh_fac=fc['Lh'],
                scale=float(np.sqrt(abs(np.linalg.det(M[:,:2]))))))
outp = os.path.join(BASE,'data','labels_verified.csv')
with open(outp,'w',newline='',encoding='utf-8') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
cnt = collections.Counter((r['base'], r['col']) for r in rows)
cls = sorted({r['base'] for r in rows}, key=lambda c: -sum(v for (b,_),v in cnt.items() if b==c))
cols = sorted({r['col'] for r in rows})
print('total', len(rows), 'T10-candidate', sum(r['t10_candidate'] for r in rows))
print('cls ' + ' '.join(f'{ROM[c-1]:>4}' for c in cols) + '  tot')
for k in cls:
    print(f'{k:3} ' + ' '.join(f'{cnt[(k,c)]:4d}' for c in cols) + f'  {sum(cnt[(k,c)] for c in cols)}')
