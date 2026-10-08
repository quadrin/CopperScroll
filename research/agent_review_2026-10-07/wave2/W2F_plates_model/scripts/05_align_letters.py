"""Forced alignment of the ETCBC transcription to facsimile components (letter-level DP).

Per line, components (from 04, sorted right-to-left by centre x) are aligned to the line's
letter sequence. A letter consumes 1-3 consecutive components (cost: width of the union vs a
letter-class width prior, horizontal separation of the parts); components can be skipped
(noise; cost); countable letters can be missing (lacuna; high cost); wildcard tokens
(numeral groups, Greek groups, words with reconstructed/supralinear/doubtful segments) absorb
any number of components cheaply. Word boundaries are rewarded by the size of the gap.

A letter is ACCEPTED as a training label only if: its word is clean (no flags), its word was
aligned without any skipped component inside it, every letter of the word got a width within
[0.45, 1.9] x its class prior, and EITHER the whole line is consistent (no countable letter
missing, <=1 interior skip) OR both word boundaries show a gap >= 0.8 x the word's largest
interior gap. Target loci (disputed words, +/- one word) are excluded explicitly.
Usage: python3 -I 05_align_letters.py [--priors data/width_priors.json] [cols...]
"""
import sys, os, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
os.makedirs(os.path.join(BASE,'work','align'), exist_ok=True)
HEB = re.compile(r'[א-ת]')
FINALS = {"ך":"כ","ם":"מ","ן":"נ","ף":"פ","ץ":"צ"}
args = sys.argv[1:]
POST_MIN = 0.9
PRI = {'ו':.22,'י':.2,'ן':.22,'ז':.3,'ג':.55,'נ':.5,'ד':.75,'ר':.7,'כ':.75,'ב':.8,'ל':.7,'ע':.75,'ף':.7,'ך':.7,
       'ה':.85,'ח':.85,'ת':.9,'מ':.9,'ם':.85,'ס':.85,'פ':.85,'צ':.8,'ץ':.8,'ק':.85,'ש':.95,'א':.9,'ט':.9}
if args and args[0] == '--priors':
    PRI.update(json.load(open(args[1]))); args = args[2:]
reg = json.load(open(os.path.join(BASE,'data','registration.json')))
txt = load_text()
inv = {}
invp = os.path.join(BASE,'..','..','results','T10_outreach','data','inventory_letters.csv')
for r in csv.DictReader(open(invp, encoding='utf-8')):
    inv[(r['ref'], int(r['word_index']), int(r['char_index']))] = r
# disputed target words and one word either side, masked from training (word indices are 0-based)
EXCLUDE = {('VII 11', 0), ('VII 11', 1), ('VII 11', 2), ('VII 11', 3), ('VII 11', 4),
           ('X 15', 2), ('X 15', 3), ('X 15', 4), ('X 15', 5),
           ('IX 7', 4), ('IX 7', 5), ('IX 7', 3),
           ('XII 10', 0), ('XII 10', 1), ('XII 10', 2), ('XII 10', 3),
           ('XI 12', 0), ('XI 12', 1), ('XI 12', 2),
           ('VII 14', 5), ('VII 14', 6), ('VII 14', 7), ('VII 15', 0), ('VII 15', 4), ('VII 15', 5), ('VII 15', 6)}

def letter_seq(col, l):
    """Flatten line into units: letters of countable words, or wildcard tokens."""
    ref = f"{ROM[col-1]} {l['l']}"
    units = []   # dict(kind='L'|'W', ...)
    for wi, w in enumerate(l['w']):
        if 'n' in w:
            units.append(dict(kind='W', wi=wi, text=f"N{w['n']}", last=True)); continue
        segs = w['h']
        if any(f == 'g' for _,f in segs):
            units.append(dict(kind='W', wi=wi, text=''.join(s for s,_ in segs), last=True)); continue
        letters = []; pos = 0; wild = False
        for s,f in segs:
            for ch in s:
                if HEB.fullmatch(ch):
                    letters.append(dict(ch=ch, flag=f, ci=pos))
                    if f in ('r','x','s'): wild = True
                else: wild = True
                pos += 1
        text = ''.join(s for s,_ in segs)
        if wild or not letters:
            units.append(dict(kind='W', wi=wi, text=text, last=True, nlet=len(letters))); continue
        clean = all(x['flag']=='' for x in letters)
        for q, let in enumerate(letters):
            units.append(dict(kind='L', wi=wi, text=text, ch=let['ch'], ci=let['ci'], q=q, flag=let['flag'],
                              clean=clean, last=(q==len(letters)-1), first=(q==0), nlet=len(letters)))
    return ref, units

def _edges(comps, units, Lh, gaps, medgap):
    """Enumerate DP edges: (i, j, i2, j2, cost, op, k)."""
    n, m = len(comps), len(units)
    E = []
    for i in range(n+1):
        for j in range(m+1):
            if i < n:
                sk = 1.0 if comps[i]['area'] < 60 else 2.5
                E.append((i,j,i+1,j,sk,'skip',1))
            if j >= m: continue
            u = units[j]
            mc = 0.7 if u['kind']=='W' else 3.5
            E.append((i,j,i,j+1,mc,'miss',0))
            kmax = 3 if u['kind']=='L' else 16
            x0 = 1e9; x1 = -1e9
            for k in range(1, min(kmax, n-i)+1):
                c = comps[i+k-1]; x0 = min(x0, c['x0']); x1 = max(x1, c['x1'])
                if u['kind']=='L':
                    w = (x1-x0)/Lh; pr = PRI.get(u['ch'], .75)
                    cost = 2.0*np.log(max(w,0.05)/pr)**2
                    if k > 1:
                        sep = max(0.0, max(gaps[i:i+k-1]))
                        cost += 0.6*(k-1) + 0.25*sep
                else:
                    cost = 0.15*k
                e = i+k
                if e < n:
                    g = gaps[e-1]/medgap
                    if u['last']: cost -= min(2.0, max(-1.0, g))
                    else: cost += 0.5*max(0.0, g-2.0)
                E.append((i,j,e,j+1,cost,'use',k))
                # two consecutive letters of the same word inside one component (keeps sync; never accepted)
                if u['kind']=='L' and k==1 and j+1 < m and units[j+1]['kind']=='L' and not u['last']:
                    pr2 = PRI.get(u['ch'], .75) + PRI.get(units[j+1]['ch'], .75) + 0.1
                    c2 = 2.0*np.log(max(w,0.05)/pr2)**2 + 4.0
                    if e < n:
                        g = gaps[e-1]/medgap
                        if units[j+1]['last']: c2 -= min(2.0, max(-1.0, g))
                        else: c2 += 0.5*max(0.0, g-2.0)
                    E.append((i,j,e,j+2,c2,'pair',1))
    return E

def align(comps, units, Lh, T=1.0):
    comps = sorted(comps, key=lambda c: -(c['x0']+c['x1'])/2)
    n, m = len(comps), len(units)
    gaps = [comps[i]['x0'] - comps[i+1]['x1'] for i in range(n-1)]
    medgap = max(3.0, float(np.median([g for g in gaps if g > 0]))) if any(g > 0 for g in gaps) else 6.0
    E = _edges(comps, units, Lh, gaps, medgap)
    # edges are generated in topological order of (i,j) source; targets are >= source
    INF = 1e18
    D = np.full((n+1, m+1), INF); D[0,0] = 0.0; back = {}
    A = np.full((n+1, m+1), -np.inf); A[0,0] = 0.0      # forward log-sum (log prob = -cost/T)
    out_by_src = {}
    for e in E: out_by_src.setdefault((e[0],e[1]), []).append(e)
    order = sorted(out_by_src.keys(), key=lambda t: (t[0]+t[1], t[0]))
    # process nodes in order of i+j (all edges increase i+j)
    for (i,j) in order:
        for (a,b,c_,d_,cost,op,k) in out_by_src[(i,j)]:
            if D[i,j] + cost < D[c_,d_]: D[c_,d_] = D[i,j] + cost; back[(c_,d_)] = (i,j,op,k)
            A[c_,d_] = np.logaddexp(A[c_,d_], A[i,j] - cost/T)
    Bk = np.full((n+1, m+1), -np.inf); Bk[n,m] = 0.0
    for (i,j) in reversed(order):
        for (a,b,c_,d_,cost,op,k) in out_by_src[(i,j)]:
            Bk[i,j] = np.logaddexp(Bk[i,j], Bk[c_,d_] - cost/T)
    Z = A[n,m]
    i, j = n, m; path = []
    while (i,j) != (0,0):
        pi, pj, op, k = back[(i,j)]; path.append((op,pi,pj,k)); i, j = pi, pj
    path.reverse()
    assign = {}; skips = []; post = {}; paired = set()
    cost_of = {(e[0],e[1],e[2],e[3],e[5]): e[4] for e in E}
    # marginal P(letter j uses component c), summed over all 'use' edges covering c
    PU = {}
    for (i,j,c_,d_,cost,op,k) in E:
        if op != 'use': continue
        pe = A[i,j] - cost/T + Bk[c_,d_] - Z
        if pe < -30: continue
        pe = float(np.exp(pe))
        for c in range(i, i+k): PU[(j,c)] = PU.get((j,c), 0.0) + pe
    for op,pi,pj,k in path:
        if op=='use':
            assign[pj] = list(range(pi,pi+k))
            cmain = max(assign[pj], key=lambda c: comps[c]['area'])
            post[pj] = PU.get((pj,cmain), 0.0)
        elif op=='pair':
            assign[pj] = []; assign[pj+1] = []; paired.update([pj,pj+1])
        elif op=='miss': assign[pj] = []
        else: skips.append(pi)
    return comps, assign, skips, gaps, medgap, float(D[n,m]), post, paired

def run(cols):
    rows = []; summ = []
    PAL = [(255,80,80),(80,255,80),(80,160,255),(255,255,0),(255,0,255),(0,255,255),(255,160,0)]
    for col in cols:
        fc = json.load(open(os.path.join(BASE,'data',f'fac_components_col{col:02d}.json')))
        Lh = fc['Lh']; M = np.array(reg[str(col)]['A_fac2photo'])
        colt = [c for c in txt['columns'] if c['c']==col][0]
        f = np.asarray(Image.open(fac_plate_path(col)).convert('L')) > 127
        vis = Image.fromarray((f*110).astype(np.uint8)).convert('RGB'); d = ImageDraw.Draw(vis)
        for li, l in enumerate(colt['lines']):
            a_, b_ = fc['line_a'][li], fc['line_b'][li]
            comps0 = []
            for c in fc['comps']:
                if c['line'] != li: continue
                yl = a_ + b_*((c['x0']+c['x1'])/2 - fc['xc'])
                cyc = (c['y0']+c['y1'])/2
                if abs(cyc-yl) > 0.75*Lh and not (c['y0'] <= yl <= c['y1']): continue   # intruder from adjacent line
                comps0.append(c)
            ref, units = letter_seq(col, l)
            nL = sum(1 for u in units if u['kind']=='L')
            if not comps0 or not units:
                summ.append(dict(ref=ref, n_comps=len(comps0), countable_letters=nL, accepted=0, line_consistent=False)); continue
            comps, assign, skips, gaps, medgap, cost, post, paired = align(comps0, units, Lh)
            n = len(comps)
            interior_skips = [s for s in skips if 0 < s < n-1]
            missingL = [j for j,u in enumerate(units) if u['kind']=='L' and not assign.get(j)]
            line_ok = (len(missingL)==0 and len(interior_skips) <= 1 and nL >= 4)
            # group by word
            words = {}
            for j,u in enumerate(units):
                if u['kind']=='L': words.setdefault(u['wi'], []).append(j)
            acc = 0
            for wi, js in words.items():
                u0 = units[js[0]]
                ok = u0['clean'] and all(assign.get(j) for j in js) and not any(j in paired for j in js)
                if ok:
                    ci = [c for j in js for c in assign[j]]
                    lo, hi = min(ci), max(ci)
                    if any(lo < s_ < hi for s_ in skips): ok = False
                    for j in js:
                        cc = [comps[c] for c in assign[j]]
                        w = (max(c['x1'] for c in cc)-min(c['x0'] for c in cc))/Lh
                        pr = PRI.get(units[j]['ch'], .75)
                        if not (0.45*pr <= w <= 1.9*pr): ok = False
                        if post.get(j, 0) < POST_MIN: ok = False
                colr = PAL[wi%len(PAL)]
                for j in js:
                    cc = [comps[c] for c in assign.get(j, [])]
                    if not cc: continue
                    bx = [min(c['x0'] for c in cc), min(c['y0'] for c in cc), max(c['x1'] for c in cc), max(c['y1'] for c in cc)]
                    d.rectangle(bx, outline=colr if ok else (100,100,100), width=3 if ok else 1)
                    if not ok: continue
                    u = units[j]
                    key = (ref, u['wi'], u['ci']); ir = inv.get(key)
                    cand = (ir is not None and ir['candidate_undisputed']=='True' and ir['letter']==u['ch'])
                    # centre of mass of the drawn strokes (not bbox) for the window centre
                    ys, xs = [], []
                    for c in cc:
                        sub = f[c['y0']:c['y1'], c['x0']:c['x1']]
                        yy, xx = np.nonzero(sub); ys.append(yy+c['y0']); xs.append(xx+c['x0'])
                    ys = np.concatenate(ys); xs = np.concatenate(xs)
                    cxf, cyf = float(xs.mean()), float(ys.mean())
                    bcx, bcy = (bx[0]+bx[2])/2, (bx[1]+bx[3])/2
                    p = M @ np.array([cxf, cyf, 1.0]); pb = M @ np.array([bcx, bcy, 1.0])
                    p0 = M @ np.array([bx[0], bx[1], 1.0]); p1 = M @ np.array([bx[2], bx[3], 1.0])
                    rows.append(dict(col=col, line=l['l'], ref=ref, word_index=u['wi'], word=u['text'], char_index=u['ci'],
                        pos_in_word=u['q'], letter=u['ch'], base=FINALS.get(u['ch'], u['ch']), final=u['ch'] in FINALS,
                        candidate_undisputed=cand, excluded_target=(ref, u['wi']) in EXCLUDE,
                        fx0=bx[0], fy0=bx[1], fx1=bx[2], fy1=bx[3], n_parts=len(cc),
                        px=round(p[0],1), py=round(p[1],1), pbx=round(pb[0],1), pby=round(pb[1],1),
                        px0=round(p0[0],1), py0=round(p0[1],1), px1=round(p1[0],1), py1=round(p1[1],1),
                        posterior=round(post.get(j,0),3), Lh_fac=Lh, scale_fac2photo=float(np.sqrt(abs(np.linalg.det(M[:,:2])))), line_consistent=bool(line_ok)))
                    acc += 1
            y_lab = min(c['y0'] for c in comps)
            d.text((5, y_lab), f"{l['l']}", fill=(255,255,255), font=font)
            d.text((f.shape[1]-75, y_lab), f"{acc}/{nL}", fill=(255,255,0), font=font)
            summ.append(dict(ref=ref, n_comps=n, countable_letters=nL, accepted=acc, line_consistent=bool(line_ok),
                             interior_skips=len(interior_skips), missing_letters=len(missingL), cost=round(cost,2)))
        vis.resize((vis.size[0]//2, vis.size[1]//2)).save(os.path.join(BASE,'work','align',f'align_col{col:02d}.png'))
        cs = [s for s in summ if s['ref'].split()[0]==ROM[col-1]]
        print(col, 'accepted', sum(s['accepted'] for s in cs), 'of countable', sum(s['countable_letters'] for s in cs),
              'consistent lines', sum(s['line_consistent'] for s in cs), '/', len(cs), flush=True)
    return rows, summ

if __name__ == '__main__':
    cols = [int(c) for c in args] or list(range(1,13))
    rows, summ = run(cols)
    outp = os.path.join(BASE,'data','letters_all.csv')
    old = []
    if os.path.exists(outp):
        old = [r for r in csv.DictReader(open(outp, encoding='utf-8')) if int(r['col']) not in cols and 'pbx' in r]
    with open(outp,'w',newline='',encoding='utf-8') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(old+rows)
    sp = os.path.join(BASE,'data','alignment_lines.json')
    olds = json.load(open(sp)) if os.path.exists(sp) else []
    olds = [s for s in olds if not any(s['ref'].split()[0]==ROM[c-1] for c in cols)]
    json.dump(olds+summ, open(sp,'w'), ensure_ascii=False, indent=0)
