"""Align the ETCBC transcription to glyphs segmented from Puech's facsimile.

For each column/line: components (from 04) -> glyphs (merge horizontally overlapping parts)
-> DP segmentation of the glyph sequence (right-to-left) into the line's tokens (words,
numeral groups, Greek groups), rewarding large gaps at word boundaries and penalising
glyph-count deviations. A word is ACCEPTED for labelling only if its glyph count equals its
letter count exactly, all its letters are unflagged in the transcription, and it is not a
disputed word (T10 inventory rule + an explicit exclusion list for the target loci).
Output: data/letters_all.csv (one row per accepted letter, facsimile + photo boxes),
        data/alignment_lines.json (per-line summary), work/align/align_colNN.png overlays.
"""
import sys, os, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import ImageDraw, ImageFont
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
os.makedirs(os.path.join(BASE,'work','align'), exist_ok=True)
HEB = re.compile(r'[א-ת]')
FINALS = {"ך":"כ","ם":"מ","ן":"נ","ף":"פ","ץ":"צ"}
reg = json.load(open(os.path.join(BASE,'data','registration.json')))
txt = load_text()
# candidate-undisputed flags from the wave-1 inventory (T10 letter_inventory.py rule)
inv = {}
invp = os.path.join(BASE,'..','..','results','T10_outreach','data','inventory_letters.csv')
for r in csv.DictReader(open(invp, encoding='utf-8')):
    inv[(r['ref'], int(r['word_index']), int(r['char_index']))] = r
# Explicit exclusions: the disputed target words and their immediate neighbours (masked)
EXCLUDE = {('VII 11', 1), ('VII 11', 2), ('VII 11', 3), ('VII 11', 4),   # Doq landmark word area
           ('X 15', 3), ('X 15', 4), ('X 15', 5),                     # של רחיל / שלוח
           ('IX 7', 5), ('IX 7', 4),                                  # direction word
           ('XII 10', 1), ('XII 10', 2), ('XII 10', 0),              # word before (ב)צפון
           ('XI 12', 1), ('XI 12', 2), ('XI 12', 0),                   # Bethesda word
           ('VII 14', 6), ('VII 14', 7), ('VII 15', 0), ('VII 15', 5), ('VII 15', 6)}
def tokens_for_line(col, l):
    toks = []
    ref = f"{ROM[col-1]} {l['l']}"
    for wi, w in enumerate(l['w']):
        if 'n' in w:
            ns = w.get('ns','')
            toks.append(dict(kind='num', wi=wi, exp=None, n_signs=len(ns.split('+')) if ns else None, text=f"N{w['n']}"))
            continue
        segs = w['h']
        if any(f == 'g' for _,f in segs):
            toks.append(dict(kind='greek', wi=wi, exp=None, text=''.join(s for s,_ in segs))); continue
        letters = []; pos = 0; wild = False
        for s,f in segs:
            for ch in s:
                if HEB.fullmatch(ch):
                    letters.append(dict(ch=ch, flag=f, ci=pos))
                    if f in ('r','x','s'): wild = True
                else:
                    wild = True   # ◦, … etc.
                pos += 1
        text = ''.join(s for s,_ in segs)
        exp = None if wild else len(letters)
        toks.append(dict(kind='word', wi=wi, exp=exp, nlet=len(letters), letters=letters, text=text, ref=ref,
                         clean=all(x['flag']=='' for x in letters)))
    return ref, toks

def make_glyphs(comps, Lh):
    comps = sorted(comps, key=lambda c: -(c['x0']+c['x1'])/2)
    glyphs = []
    med_area = np.median([c['area'] for c in comps]) if comps else 1
    for c in comps:
        merged = False
        for g in glyphs[-3:]:
            ov = min(g['x1'], c['x1']) - max(g['x0'], c['x0'])
            wmin = min(g['x1']-g['x0'], c['x1']-c['x0'])
            if ov >= 0.5*wmin or (c['area'] < 0.12*med_area and ov > -2):
                g['x0']=min(g['x0'],c['x0']); g['x1']=max(g['x1'],c['x1']); g['y0']=min(g['y0'],c['y0']); g['y1']=max(g['y1'],c['y1'])
                g['area']+=c['area']; g['parts'].append(c['id']); merged=True; break
        if not merged:
            glyphs.append(dict(x0=c['x0'],x1=c['x1'],y0=c['y0'],y1=c['y1'],area=c['area'],parts=[c['id']]))
        glyphs.sort(key=lambda g: -(g['x0']+g['x1'])/2)
    # drop tiny isolated specks
    glyphs = [g for g in glyphs if g['area'] >= 0.08*med_area]
    return glyphs

def dp_align(glyphs, toks, Lh):
    n, m = len(glyphs), len(toks)
    gaps = [glyphs[i]['x0'] - glyphs[i+1]['x1'] for i in range(n-1)]   # RTL: right glyph x0 - left glyph x1
    medgap = max(2.0, float(np.median(gaps))) if gaps else 5.0
    INF = 1e9
    D = np.full((n+1, m+1), INF); D[0,0] = 0; back = {}
    SKIP = 2.0
    for i in range(n+1):
        for j in range(m+1):
            if D[i,j] >= INF: continue
            # skip a glyph (noise / neighbour column / unknown)
            if i < n:
                c = D[i,j] + SKIP
                if c < D[i+1,j]: D[i+1,j] = c; back[(i+1,j)] = (i,j,'skip',1)
            if j < m:
                t = toks[j]
                # token absent (lacuna)
                c = D[i,j] + (0.8 if t['exp'] is None else 3.0 + 0.5*t.get('nlet',1))
                if c < D[i,j+1]: D[i,j+1] = c; back[(i,j+1)] = (i,j,'miss',0)
                kmax = (t['exp']+2) if t['exp'] is not None else (t.get('nlet',0)+4 if t['kind']=='word' else 14)
                for k in range(1, min(kmax, n-i)+1):
                    if t['exp'] is not None:
                        pen = 4.0*abs(k - t['exp'])
                    elif t['kind']=='word':
                        pen = 0.6*abs(k - t['nlet'])
                    else:
                        pen = 0.1*k
                    # boundary reward: gap after this token (if not last glyph)
                    e = i+k
                    rew = 0.0
                    if e < n: rew -= min(2.5, max(-1.0, gaps[e-1]/medgap))
                    # within-token large gaps penalised
                    inner = gaps[i:e-1]
                    pin = sum(max(0, g/medgap - 2.0) for g in inner)*0.7
                    c = D[i,j] + pen + rew + pin
                    if c < D[e,j+1]: D[e,j+1] = c; back[(e,j+1)] = (i,j,'tok',k)
    # end: allow trailing skipped glyphs already covered by skip moves; must consume all tokens
    i, j = n, m
    path = []
    while (i,j) != (0,0):
        pi, pj, op, k = back[(i,j)]
        path.append((op, pi, pj, k)); i, j = pi, pj
    path.reverse()
    assign = {}
    nskip_mid = sum(1 for op,pi,pj,k in path if op=='skip' and 0 < pi < n-1)
    for op, pi, pj, k in path:
        if op == 'tok': assign[pj] = list(range(pi, pi+k))
        elif op == 'miss': assign[pj] = []
    return assign, gaps, medgap, float(D[n,m]), nskip_mid

rows = []; summ = []
lettc = 0
PAL = [(255,80,80),(80,255,80),(80,160,255),(255,255,0),(255,0,255),(0,255,255),(255,160,0)]
cols = [int(c) for c in sys.argv[1:]] or list(range(1,13))
for col in cols:
    fc = json.load(open(os.path.join(BASE,'data',f'fac_components_col{col:02d}.json')))
    Lh = fc['Lh']
    M = np.array(reg[str(col)]['A_fac2photo'])
    colt = [c for c in txt['columns'] if c['c']==col][0]
    f = np.asarray(Image.open(fac_plate_path(col)).convert('L')) > 127
    vis = Image.fromarray((f*110).astype(np.uint8)).convert('RGB'); d = ImageDraw.Draw(vis)
    for li, l in enumerate(colt['lines']):
        comps = [c for c in fc['comps'] if c['line']==li]
        glyphs = make_glyphs(comps, Lh)
        ref, toks = tokens_for_line(col, l)
        if not glyphs:
            summ.append(dict(ref=ref, n_glyphs=0, n_tokens=len(toks), accepted_words=0, accepted_letters=0)); continue
        assign, gaps, medgap, cost, nskip_mid = dp_align(glyphs, toks, Lh)
        acc_w = acc_l = 0; exp_l = sum(t.get('nlet',0) for t in toks if t['kind']=='word')
        # line-level consistency: every countable token got exactly its letter count,
        # no countable token missing, at most one glyph skipped inside the line
        line_ok = nskip_mid <= 1 and all((t['exp'] is None) or (len(assign.get(j,[]))==t['exp']) for j,t in enumerate(toks)) \
                  and sum(1 for t in toks if t['exp'] is not None) >= 2
        for j,t in enumerate(toks):
            gi = assign.get(j, [])
            ok = (t['kind']=='word' and t['exp'] is not None and len(gi)==t['exp'] and t['clean'])
            # boundary check (only when the line is not fully consistent):
            # both outer gaps larger than 0.8 x the largest inner gap
            if ok and not line_ok and len(gi) > 1:
                inner = max(gaps[gi[0]:gi[-1]]) if gi[-1] > gi[0] else 0
                outer = []
                if gi[0] > 0: outer.append(gaps[gi[0]-1])
                if gi[-1] < len(glyphs)-1: outer.append(gaps[gi[-1]])
                if outer and min(outer) < 0.8*inner: ok = False
            colr = PAL[j%len(PAL)]
            for q,g in enumerate(gi):
                G = glyphs[g]
                d.rectangle([G['x0'],G['y0'],G['x1'],G['y1']], outline=colr if ok else (110,110,110), width=3 if ok else 1)
                if ok:
                    let = t['letters'][q]
                    excluded = (ref, t['wi']) in EXCLUDE
                    key = (ref, t['wi'], let['ci'])
                    ir = inv.get(key)
                    cand = (ir is not None and ir['candidate_undisputed']=='True' and ir['letter']==let['ch'])
                    cxf, cyf = (G['x0']+G['x1'])/2, (G['y0']+G['y1'])/2
                    px = M @ np.array([cxf, cyf, 1.0])
                    p0 = M @ np.array([G['x0'], G['y0'], 1.0]); p1 = M @ np.array([G['x1'], G['y1'], 1.0])
                    rows.append(dict(col=col, line=l['l'], ref=ref, word_index=t['wi'], word=t['text'], char_index=let['ci'],
                        pos_in_word=q, letter=let['ch'], base=FINALS.get(let['ch'], let['ch']), final=let['ch'] in FINALS,
                        candidate_undisputed=cand, excluded_target=excluded,
                        fx0=G['x0'], fy0=G['y0'], fx1=G['x1'], fy1=G['y1'],
                        px=round(px[0],1), py=round(px[1],1), px0=round(p0[0],1), py0=round(p0[1],1), px1=round(p1[0],1), py1=round(p1[1],1),
                        Lh_fac=Lh, line_consistent=bool(line_ok)))
            if ok: acc_w += 1; acc_l += len(gi)
        d.text((5, glyphs[0]['y0'] if glyphs else 0), f"{l['l']}", fill=(255,255,255), font=font)
        d.text((f.shape[1]-60, glyphs[0]['y0']), f"{acc_l}/{exp_l}", fill=(255,255,0), font=font)
        summ.append(dict(ref=ref, n_glyphs=len(glyphs), n_tokens=len(toks), expected_letters=exp_l, accepted_words=acc_w, accepted_letters=acc_l, dp_cost=cost, line_consistent=bool(line_ok)))
    vis.resize((vis.size[0]//2, vis.size[1]//2)).save(os.path.join(BASE,'work','align',f'align_col{col:02d}.png'))
    tot = sum(s['accepted_letters'] for s in summ if s['ref'].split()[0]==ROM[col-1])
    exp = sum(s.get('expected_letters',0) for s in summ if s['ref'].split()[0]==ROM[col-1])
    print(col, 'accepted letters', tot, 'of', exp)
outp = os.path.join(BASE,'data','letters_all.csv')
if len(cols) < 12 and os.path.exists(outp):
    old = [r for r in csv.DictReader(open(outp, encoding='utf-8')) if int(r['col']) not in cols]
else: old = []
allrows = old + rows
with open(outp,'w',newline='',encoding='utf-8') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(allrows)
json.dump(summ, open(os.path.join(BASE,'data',f'alignment_lines_{"_".join(map(str,cols))}.json'),'w'), ensure_ascii=False, indent=0)
