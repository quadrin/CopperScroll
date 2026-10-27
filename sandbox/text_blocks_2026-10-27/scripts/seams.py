"""Steps 2-4 as fixed in out/METHOD_LOCK.md (SHA-256 9b049714...ca38)."""
import csv, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'out')
rows = list(csv.DictReader(open(os.path.join(OUT, 'feature_matrix.csv'), encoding='utf-8')))
N = len(rows); ENT = [r['entry'] for r in rows]; POS = {e: i for i, e in enumerate(ENT)}
BIN = ['depth', 'vessels', 'direction', 'named', 'greek']
CAT = {'unit': ['none', 'kk', 'kkrin', 'kkr', 'kk+kkrin'], 'metal': ['none', 'silver', 'gold', 'both'], 'digform': ['none', 'חפור', 'חפר']}
FEATS = BIN + list(CAT) + ['nwords']
MINLEN, KMAX, NPERM, SEED = 3, 5, 10000, 20261027
LN = math.log(N)

# one-hot blocks per feature (binary = 2 levels)
blocks = {}
for f in BIN: blocks[f] = np.array([[1 - int(r[f]), int(r[f])] for r in rows], float)
for f, lev in CAT.items():
    assert all(r[f] in lev for r in rows), f
    blocks[f] = np.array([[float(r[f] == l) for l in lev] for r in rows])
y = np.log(np.array([float(r['nwords']) for r in rows])); SIG2 = y.var()
P_SEG = len(BIN) + sum(len(v) - 1 for v in CAT.values()) + 1
assert P_SEG == 15

ii, jj = np.meshgrid(np.arange(N + 1), np.arange(N + 1), indexing='ij')
VALID = (jj - ii) >= MINLEN
NSEG = np.where(jj > ii, jj - ii, 1).astype(float)

def xlogx(c, n):
    with np.errstate(divide='ignore', invalid='ignore'):
        v = np.where(c > 0, c * np.log(c / n), 0.0)
    return v

def cost_by_feature(order):
    """dict feature -> (N+1,N+1) matrix of -2LL for segment [i,j) (inf where too short)."""
    out = {}
    for f in BIN + list(CAT):
        X = blocks[f][order]; P = np.vstack([np.zeros(X.shape[1]), np.cumsum(X, 0)])
        c = P[None, :, :] - P[:, None, :]                     # counts in [i,j)
        out[f] = -2 * xlogx(c, NSEG[:, :, None]).sum(-1)
    yy = y[order]; S1 = np.concatenate([[0], np.cumsum(yy)]); S2 = np.concatenate([[0], np.cumsum(yy ** 2)])
    s1 = S1[None, :] - S1[:, None]; s2 = S2[None, :] - S2[:, None]
    rss = s2 - s1 ** 2 / NSEG
    out['nwords'] = rss / SIG2 + NSEG * math.log(2 * math.pi * SIG2)
    return out

def total(cf):
    C = sum(cf.values()); return np.where(VALID, C, np.inf)

GOW = None
def gower_D():
    n = N; D = np.zeros((n, n))
    for f in BIN + list(CAT):
        v = np.array([r[f] for r in rows]); D += (v[:, None] != v[None, :])
    rng_ = y.max() - y.min(); D += np.abs(y[:, None] - y[None, :]) / rng_
    return D / len(FEATS)
GOW = gower_D()

def gower_cost(order):
    U = np.triu(GOW[np.ix_(order, order)], 1)
    Q = np.zeros((N + 1, N + 1)); Q[1:, 1:] = U.cumsum(0).cumsum(1)
    S = Q[jj, jj] - Q[ii, jj] - Q[jj, ii] + Q[ii, ii]
    return np.where(VALID, S / NSEG, np.inf)

def dp(C, kmax=KMAX, back=False):
    """F[k] = optimal cost with k seams for the whole sequence; optional backtrack."""
    F = C[0].copy(); res = [F[N]]; args = []
    for k in range(1, kmax + 1):
        M = F[:, None] + C; a = M.argmin(0); F = M[a, np.arange(N + 1)]
        res.append(F[N]); args.append(a)
    if not back: return np.array(res)
    segs = {}
    for K in range(kmax + 1):
        b, j = [], N
        for k in range(K, 0, -1):
            j = args[k - 1][j]; b.append(int(j))
        segs[K] = sorted(b)
    return np.array(res), segs

def m1_stats(order, back=False):
    cf = cost_by_feature(order); C = total(cf)
    r = dp(C, back=back); costs = r[0] if back else r
    K = np.arange(KMAX + 1); bic = costs + ((K + 1) * P_SEG + K) * LN
    ks = 1 + int(np.argmin(bic[1:]))
    out = dict(G=float(bic[0] - bic[ks]), K=ks, bic=bic.tolist(), cost=costs.tolist())
    if back: out['segs'] = r[1]; out['cf'] = cf
    return out

def m2_stats(order, back=False):
    C = gower_cost(order); r = dp(C, back=back); W = r[0] if back else r
    K = np.arange(KMAX + 1); crit = N * np.log(W / N) + K * (len(FEATS) + 1) * LN
    ks = 1 + int(np.argmin(crit[1:]))
    out = dict(G=float(crit[0] - crit[ks]), K=ks, crit=crit.tolist(), W=W.tolist())
    if back: out['segs'] = r[1]
    return out

# ---------------------------------------------------------------- observed
ident = np.arange(N)
o1 = m1_stats(ident, back=True); o2 = m2_stats(ident, back=True)

def seg_label(b):
    edges = [0] + b + [N]; return [f'{ENT[edges[s]]}–{ENT[edges[s+1]-1]}' for s in range(len(edges) - 1)]

# per-feature contribution at each seam of the chosen M1 segmentation: cost(merged) - cost(left) - cost(right)
def seam_feature_change(b, cf):
    edges = [0] + b + [N]; rep = []
    for s in range(1, len(edges) - 1):
        a, t, c = edges[s - 1], edges[s], edges[s + 1]
        contrib = {f: float(cf[f][a, c] - cf[f][a, t] - cf[f][t, c]) for f in FEATS}
        def summ(lo, hi):
            d = {}
            for f in BIN: d[f] = round(float(np.mean([int(rows[i][f]) for i in range(lo, hi)])), 2)
            for f in CAT:
                from collections import Counter
                d[f] = dict(Counter(rows[i][f] for i in range(lo, hi)).most_common())
            d['nwords_median'] = float(np.median([int(rows[i]['nwords']) for i in range(lo, hi)]))
            return d
        rep.append(dict(seam_before=ENT[t], left=f'{ENT[a]}–{ENT[t-1]}', right=f'{ENT[t]}–{ENT[c-1]}',
                        contrib=dict(sorted(contrib.items(), key=lambda kv: -kv[1])), left_profile=summ(a, t), right_profile=summ(t, c)))
    return rep

# ---------------------------------------------------------------- permutations
rng = np.random.default_rng(SEED)
G1, G2, K1, K2 = [], [], [], []
for p in range(NPERM):
    perm = rng.permutation(N)
    a = m1_stats(perm); b = m2_stats(perm)
    G1.append(a['G']); K1.append(a['K']); G2.append(b['G']); K2.append(b['K'])
G1, G2 = np.array(G1), np.array(G2)
def pval(G, g): c = int((G >= g - 1e-9).sum()); return c, c / len(G), (c + 1) / (len(G) + 1)

# per-K permutation p for M1 (exploratory: gain at fixed K, no BIC choice)
# ---------------------------------------------------------------- geography
REG = {
 'P':  {'9': 'J', '10': 'J', '35': 'J', '49': 'J', '51': 'J', '57': 'G', '58': 'B'},
}
REG['D1'] = dict(REG['P'], **{'31': 'Jer', '32': 'Jer', '55': 'J'})
REG['D2'] = dict(REG['D1'], **{'17': 'Jer', '20': 'S', '21': 'S', '22': 'S', '46': 'J'})
def changes(reg):
    an = sorted(reg, key=lambda e: POS[e]); ch = []
    for a, b in zip(an, an[1:]):
        if reg[a] != reg[b]: ch.append((a, b, reg[a], reg[b], POS[a], POS[b]))
    return ch
def match(t, ch, strict=False):
    hits = []
    for a, b, ra, rb, pa, pb in ch:
        ok = (abs(t - pb) <= 2 or abs(t - (pa + 1)) <= 2) if strict else (pa - 1 <= t <= pb + 2)
        if ok: hits.append(f'{a}({ra})→{b}({rb})')
    return hits
def geo(b):
    out = {}
    for name, reg in REG.items():
        ch = changes(reg)
        ms = [match(t, ch) for t in b]; mss = [match(t, ch, True) for t in b]
        win = set(t for t in range(1, N) if match(t, ch)); wins = set(t for t in range(1, N) if match(t, ch, True))
        out[name] = dict(changes=[f'{a}({ra})→{b_}({rb})' for a, b_, ra, rb, _, _ in ch],
                         seams=[dict(seam_before=ENT[t], match=m, match_strict=s) for t, m, s in zip(b, ms, mss)],
                         n_match=sum(bool(m) for m in ms), n_match_strict=sum(bool(m) for m in mss), n_seams=len(b),
                         chance_share_of_boundaries=round(len(win) / (N - 1), 3), chance_share_strict=round(len(wins) / (N - 1), 3))
    return out

res = dict(
  N=N, method_lock_sha256='9b049714b54920ed99d5b5f4bc784e3291226844a307197eb3f1329324e4ca38',
  M1=dict(G=o1['G'], K=o1['K'], bic=o1['bic'], cost=o1['cost'],
          segs={K: dict(seams_before=[ENT[t] for t in b], segments=seg_label(b)) for K, b in o1['segs'].items()},
          p=pval(G1, o1['G']), null_G_quantiles=np.quantile(G1, [0.5, 0.9, 0.95, 0.99]).tolist(), null_K_counts=np.bincount(K1, minlength=6).tolist(),
          seam_features=seam_feature_change(o1['segs'][o1['K']], o1['cf']), geography=geo(o1['segs'][o1['K']]),
          geography_all_K={K: geo(b) for K, b in o1['segs'].items() if K > 0}),
  M2=dict(G=o2['G'], K=o2['K'], crit=o2['crit'],
          segs={K: dict(seams_before=[ENT[t] for t in b], segments=seg_label(b)) for K, b in o2['segs'].items()},
          p=pval(G2, o2['G']), null_G_quantiles=np.quantile(G2, [0.5, 0.9, 0.95, 0.99]).tolist(), null_K_counts=np.bincount(K2, minlength=6).tolist(),
          geography=geo(o2['segs'][o2['K']])),
)
# entry -> block (M1 chosen segmentation)
edges = [0] + o1['segs'][o1['K']] + [N]
res['M1']['block_of_entry'] = {ENT[i]: s + 1 for s in range(len(edges) - 1) for i in range(edges[s], edges[s + 1])}
json.dump(res, open(os.path.join(OUT, 'results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
np.save(os.path.join(OUT, 'null_G_M1.npy'), G1); np.save(os.path.join(OUT, 'null_G_M2.npy'), G2)
print(json.dumps({k: (v if k not in ('M1', 'M2') else {kk: vv for kk, vv in v.items() if kk not in ('geography_all_K',)}) for k, v in res.items()}, ensure_ascii=False, indent=1, default=str))
