"""B2 pipeline: template learning on TRAIN lines and candidate scoring.

Modes
  explore  : EXPLORATORY. 2-fold cross-fit on TRAIN lines only (templates learned on one fold, the
             other fold's candidate sets ranked). Used to choose parameters. No held-out line is scored.
  heldout  : CONFIRMATORY (after the freeze). Templates learned on all TRAIN lines; every HELD-OUT line's
             candidate set scored once. Writes calibration_rankings2.csv and heldout_result2.json.
  targets  : only as the frozen protocol allows; writes target_rankings2.csv.
"""
import sys, os, json, time, csv
import numpy as np
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model2 as M

ITEMS = json.load(open(f'{HERE}/calibration_items2.json'))
LINES = json.load(open(f'{HERE}/etcbc_lines.json'))
NLINES = defaultdict(int)
for k in LINES:
    c, l = map(int, k.split(':')); NLINES[c] = max(NLINES[c], l)
_CUT = {}


def frames_of(cut, p):
    if cut not in _CUT:
        d = M.load_cut(cut)
        _CUT[cut] = {code: (M.prep(img, mask, p.LH), img.shape[0]) for code, (img, mask) in d.items()}
    return _CUT[cut]


def nominal(col, line, H, p):
    N = NLINES[col]
    return H * (p.ROWA + p.ROWB * (line - 0.5) / N), H * p.ROWB / N


def rendered_set(lclass, p):
    return {c: M.render(c, lclass, p.LH, p) for c in M.GL}


def learn(train_items, p):
    """Viterbi-style template learning on TRAIN lines, NPASS passes. Pass 0 aligns each TRAIN line's truth
    with the rendered groove templates at its best row (truth alignment, training only); later passes
    realign with the templates of the previous pass. Patches are collected per (col, light class, letter)
    and per ('all', light class, letter); T_col = norm(sum_col + KS * T_all), T_all = norm(sum_all + KS * T_render)."""
    R = {lc: rendered_set(lc, p) for lc in set(M.LCLASS.values())}
    cols = sorted(set(it['col'] for it in ITEMS) | {9, 10, 11, 12})
    cur = {(col, lc): R[lc] for col in cols for lc in R}
    rows, cnt = [], {}
    for ps in range(p.NPASS):
        sums = defaultdict(lambda: None); cnt = defaultdict(int)
        rows = []
        for it in train_items:
            col, line, truth = it['col'], it['line'], it['truth']
            seq = M.letters(truth)
            for cut in it['cuts']:
                for code, (z, H) in frames_of(cut, p).items():
                    lc = M.LCLASS[code]
                    band = band_for(cut, code, col, z, cur[(col, lc)], p, key=f'learn{id(train_items)}p{ps}')
                    yn, pitch = nominal(col, line, H, p)
                    best = (-1, None, None)
                    for y in np.arange(yn - p.WIN * pitch, yn + p.WIN * pitch + 1, p.YSTEP):
                        sc, pl = band.score(y, truth)
                        if sc > best[0]: best = (sc, y, pl)
                    sc, y, pl = best
                    rows.append(dict(col=col, line=line, cut=cut, code=code, H=H, y=None if y is None else float(y), s=sc))
                    if not pl: continue
                    ht = band.ht; dy = int(round(p.DY * p.LH))
                    for i, x in pl:
                        c = seq[i][0]
                        w = band.widths[c]
                        y0 = int(round(y - ht / 2))
                        m = band.maps[c]
                        a, b = max(0, y0 - dy), min(m.shape[0], y0 + dy + 1)
                        yy = a + int(np.argmax(m[a:b, x]))
                        patch = z[yy:yy + ht, x:x + w]
                        if patch.shape != (ht, w): continue
                        patch = M.norm(patch)
                        for key in ((col, lc, c), ('all', lc, c)):
                            sums[key] = patch.copy() if sums[key] is None else sums[key] + patch
                            cnt[key] += 1
        new = {}
        for col in cols:
            for lc in R:
                T = {}
                for c in M.GL:
                    g = R[lc][c]
                    if sums[('all', lc, c)] is not None:
                        g = M.norm(sums[('all', lc, c)] + p.KS * g)
                    if sums[(col, lc, c)] is not None:
                        g = M.norm(sums[(col, lc, c)] + p.KS * g)
                    T[c] = g
                new[(col, lc)] = T
        cur = new
    return cur, rows, dict(cnt)


_BAND = {}


def band_for(cut, code, col, z, temps, p, key):
    k = (cut, code, col, key)
    if _BAND and next(iter(_BAND))[2:] != (col, key):
        _BAND.clear()  # keep only the current column's bands in memory
    if k not in _BAND:
        _BAND[k] = M.Band(z, temps, p.LH, p)
    return _BAND[k]


def score_item(it, temps, p, key, cands=None):
    """returns per-candidate total score; row per (cut, frame) chosen by the mean over candidates"""
    col, line = it['col'], it['line']
    cands = cands or it['candidates']
    tot = np.zeros(len(cands)); detail = []
    for cut in it['cuts']:
        for code, (z, H) in frames_of(cut, p).items():
            lc = M.LCLASS[code]
            band = band_for(cut, code, col, z, temps[(col, lc)], p, key)
            yn, pitch = nominal(col, line, H, p)
            ys = np.arange(yn - p.WIN * pitch, yn + p.WIN * pitch + 1, p.YSTEP)
            sc = np.array([[band.score(y, s)[0] for s in cands] for y in ys])
            j = int(np.argmax(sc.mean(1)))
            tot += sc[j]
            detail.append(dict(cut=cut, code=code, y=float(ys[j]), yn=float(yn)))
    return tot, detail


def score_item_fixed(it, temps, p, key, cands=None):
    """FROZEN SCORING RULE (fixed shared alignment, letter classification at the disputed positions).
    Candidates must have the same letters except at single-letter substitution positions.
    1. Common string: letters shared by all candidates; at each differing position a wildcard whose
       score is 0 and whose width is the mean width of the alternative letters.
    2. In each frame of each cut, the common string is aligned (local alignment) at every row of the
       window; the row with the highest common-string score is used (candidate-symmetric).
    3. For each wildcard position inside the aligned run, each candidate's letter c is scored by its
       pooled letter score (max over +-0.1 Lh, +-DY Lh) at the left edge that centres c on the wildcard.
       Wildcard positions outside the run give no evidence (0 for every candidate).
    4. Candidate score = sum over its letters at wildcard positions, over the column's cuts and frames."""
    col, line = it['col'], it['line']
    cands = cands or it['candidates']
    seqs = [M.letters(c) for c in cands]
    L = len(seqs[0]); assert all(len(q) == L for q in seqs)
    common = []; wild = {}
    for i in range(L):
        ls = [q[i][0] for q in seqs]
        if len(set(ls)) == 1:
            common.append((ls[0], seqs[0][i][1]))
        else:
            k = f'*{i}'; common.append((k, seqs[0][i][1])); wild[i] = ls
    tot = np.zeros(len(cands)); detail = []; observed = {i: 0 for i in wild}
    for cut in it['cuts']:
        for code, (z, H) in frames_of(cut, p).items():
            lc = M.LCLASS[code]
            band = band_for(cut, code, col, z, temps[(col, lc)], p, key)
            yn, pitch = nominal(col, line, H, p)
            letters_needed = {c for c, _ in common if not c.startswith('*')} | {c for ls in wild.values() for c in ls}
            widths = dict(band.widths)
            for i, ls in wild.items():
                widths[f'*{i}'] = int(round(np.mean([band.widths[c] for c in ls])))
            best = (-1e18, None, None, None)
            for y in np.arange(yn - p.WIN * pitch, yn + p.WIN * pitch + 1, p.YSTEP):
                S = band.rowscores(y, letters_needed)
                for i in wild:
                    n = max(len(v) for v in S.values())
                    S[f'*{i}'] = np.zeros(n, np.float32)
                sc, pl = M.align(S, common, widths, p.LH, p)
                if sc > best[0]: best = (sc, y, pl, S)
            sc, y, pl, S = best
            add = np.zeros(len(cands))
            for i, x in (pl or []):
                if i not in wild: continue
                observed[i] += 1
                wst = widths[f'*{i}']
                for j, c in enumerate(wild[i]):
                    x0 = int(round(x + (wst - band.widths[c]) / 2))
                    r = S[c]  # pooled: already the max over +-0.1 Lh around x0
                    add[j] += float(r[x0]) if 0 <= x0 < len(r) else 0.0
            tot += add
            detail.append(dict(cut=cut, code=code, y=None if y is None else float(y), yn=float(yn), common=float(sc)))
    return tot, dict(frames=detail, wild={i: wild[i] for i in wild}, observed=observed)


def line_eval(tot, info):
    """FROZEN EVALUATION (star null). Candidate 0 is the truth; each competitor differs from it at one
    letter position. A competitor is OBSERVED if its position lies inside the shared aligned run in at least
    one frame (decided without the differing letters). Unobserved competitors tie with the truth exactly
    and carry no evidence: they are left out. truth_first = the truth strictly outscores every observed
    competitor. Chance probability under exchangeable letter scores: p0 = product over observed positions
    of 1/(m+1), m = number of competitor letters at that position (competitors at one position are scored
    against the same true-letter score, so they are not independent contests)."""
    wild, obs = info['wild'], info['observed']
    pos_of = {}
    for i, ls in wild.items():
        for j, c in enumerate(ls):
            if j > 0 and c != ls[0]:
                pos_of.setdefault(j, []).append(i)
    obs_c = [j for j in range(1, len(tot)) if pos_of.get(j) and all(obs[i] > 0 for i in pos_of[j])]
    posunits = {}
    for j in obs_c:
        for i in pos_of[j]:
            posunits.setdefault(i, []).append(j)
    if not obs_c:
        return dict(observed=False, n_obs_competitors=0, truth_first=None, p0=None, positions=[])
    first = bool(all(tot[0] > tot[j] for j in obs_c))
    p0 = float(np.prod([1.0 / (len(js) + 1) for js in posunits.values()]))
    positions = [dict(pos=int(i), m=len(js), win=bool(all(tot[0] > tot[j] for j in js)), p0=1.0 / (len(js) + 1))
                 for i, js in posunits.items()]
    return dict(observed=True, n_obs_competitors=len(obs_c), truth_first=first, p0=p0, positions=positions)


def summarise(evals):
    ev = [e for e in evals if e['observed']]
    T = sum(e['truth_first'] for e in ev)
    P = poisson_binomial_tail([e['p0'] for e in ev], T) if ev else None
    pos = [u for e in ev for u in e['positions']]
    W = sum(u['win'] for u in pos)
    PW = poisson_binomial_tail([u['p0'] for u in pos], W) if pos else None
    return dict(n_lines=len(evals), n_observed_lines=len(ev), T=T, expected_T=float(sum(e['p0'] for e in ev)),
                p_T=P, n_positions=len(pos), W=W, expected_W=float(sum(u['p0'] for u in pos)), p_W=PW)


def rank_truth(tot):
    # rank of index 0 (truth); ties count against the truth
    return 1 + int(np.sum(tot[1:] >= tot[0]))


def explore(p, tag):
    tr = [it for it in ITEMS if it['split'].startswith('train')]
    rng = np.random.default_rng(7)
    fold = rng.permutation(len(tr)) % 2
    res = []
    for f in [int(x) for x in os.environ.get('B2_EXPLORE_FOLDS', '0,1').split(',')]:
        A = [it for it, g in zip(tr, fold) if g != f]
        B = [it for it, g in zip(tr, fold) if g == f]
        _BAND.clear()
        temps, rows, cnt = learn(A, p)
        for it in B[:int(os.environ.get('B2_EXPLORE_MAX', '1000'))]:
            tot, info = score_item_fixed(it, temps, p, key=f'learn{f}')
            r = rank_truth(tot); e = line_eval(tot, info)
            res.append(dict(col=it['col'], line=it['line'], split=it['split'], K=len(tot), rank=r,
                            margin=float(tot[0] - np.max(tot[1:])), eval=e))
            print(tag, f, it['col'], it['line'], len(tot), r, round(res[-1]['margin'], 3), e['observed'],
                  e['n_obs_competitors'], e['truth_first'], None if e['p0'] is None else round(e['p0'], 4),
                  [(u['m'], u['win']) for u in e['positions']], flush=True)
    sm = summarise([r['eval'] for r in res])
    print(tag, 'SUMMARY', json.dumps(sm), flush=True)
    return res


def poisson_binomial_tail(ps, t):
    d = np.array([1.0])
    for q in ps:
        d = np.convolve(d, [1 - q, q])
    return float(d[t:].sum())


TPATH = M.SP + '/products/B2/templates_frozen.npz'


def save_temps(temps):
    """private (image-derived) templates: saved outside the repository; only the sha256 is public"""
    import hashlib
    arr = {f'{col}|{lc}|{c}': t for (col, lc), T in temps.items() for c, t in T.items()}
    np.savez_compressed(TPATH, **arr)
    return dict(path=TPATH, sha256=hashlib.sha256(open(TPATH, 'rb').read()).hexdigest())


def load_temps(rec):
    import hashlib
    assert hashlib.sha256(open(rec['path'], 'rb').read()).hexdigest() == rec['sha256']
    d = np.load(rec['path']); temps = defaultdict(dict)
    for k in d.files:
        col, lc, c = k.split('|')
        temps[(int(col), lc)][c] = d[k]
    return dict(temps)


def load_frozen():
    fp = json.load(open(f'{HERE}/frozen_params2.json'))
    for k, v in fp.items():
        setattr(M.P, k, v)
    return fp


def heldout():
    fp = load_frozen()
    p = M.P
    tr = [it for it in ITEMS if it['split'].startswith('train')]
    ho = [it for it in ITEMS if it['split'] == 'heldout']
    t0 = time.time()
    temps, rows, cnt = learn(tr, p)
    tp = save_temps(temps)
    out, res = [], []
    for it in ho:
        tot, info = score_item_fixed(it, temps, p, key='heldout')
        r = rank_truth(tot); K = len(tot); e = line_eval(tot, info)
        for j, s_ in enumerate(it['candidates']):
            out.append(dict(col=it['col'], line=it['line'], K=K, cand=j, is_truth=int(j == 0), string=s_,
                            score=round(float(tot[j]), 4)))
        res.append(dict(col=it['col'], line=it['line'], K=K, rank_ties_against_truth=r,
                        margin=float(tot[0] - np.max(tot[1:])), eval=e,
                        observed_counts={str(k): v for k, v in info['observed'].items()}))
        print('HO', it['col'], it['line'], K, r, round(res[-1]['margin'], 3), e['observed'], e['n_obs_competitors'],
              e['truth_first'], None if e['p0'] is None else round(e['p0'], 4), flush=True)
    with open(f'{HERE}/calibration_rankings2.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    sm = summarise([r['eval'] for r in res])
    PASS = bool(sm['n_observed_lines'] >= 10 and sm['p_T'] is not None and sm['p_T'] < 0.05)
    med_abs_margin = float(np.median([abs(r['margin']) for r in res if r['eval']['observed']] or [0.0]))
    result = dict(summary=sm, PASS=PASS, median_abs_margin_observed=med_abs_margin, lines=res, frozen_params=fp,
                  train_patch_counts_all={f'{k[1]}:{k[2]}': v for k, v in cnt.items() if k[0] == 'all'},
                  templates_private_npz=tp, seconds=round(time.time() - t0))
    json.dump(result, open(f'{HERE}/heldout_result2.json', 'w'), indent=1, ensure_ascii=False)
    print('RESULT', json.dumps(sm), 'PASS', PASS, flush=True)
    return result, temps


def targets():
    import targets2 as TG
    hr = json.load(open(f'{HERE}/heldout_result2.json'))
    rows = []
    if not hr['PASS']:
        for name in TG.ORDER + list(TG.NOT_SCORABLE):
            rows.append(dict(target=name, candidate='NOT RUN', string='', score='', rank='',
                             margin_to_next='', verdict='held-out test failed: targets not scored (frozen rule)'))
    else:
        raise NotImplementedError('held-out PASS: write the protocol section 6 target scorer, commit it with its '
                                  'hash, then run it (frozen rule; the free-alignment score_item is NOT used)')
    with open(f'{HERE}/target_rankings2.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'explore':
        tag = sys.argv[2]
        for kv in sys.argv[3:]:
            k, v = kv.split('=')
            setattr(M.P, k, type(getattr(M.P, k))(v) if not isinstance(getattr(M.P, k), str) else v)
        t0 = time.time()
        res = explore(M.P, tag)
        os.makedirs(f'{HERE}/explore', exist_ok=True)
        json.dump(dict(params={k: getattr(M.P, k) for k in dir(M.P) if not k.startswith('_')}, results=res,
                       seconds=round(time.time() - t0)), open(f'{HERE}/explore/{tag}.json', 'w'), indent=1)
    elif mode == 'heldout':
        heldout()
    elif mode == 'targets':
        targets()
