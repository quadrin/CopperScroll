"""Exploratory follow-ups (outside the rule): brute-force check of the DP, feature-drop variants, fixed-K p values,
cost of the project's earlier blocks (19|20, 35|36, 56|57) and a chance baseline for the geographic match."""
import csv, json, math, os, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'out')
rows = list(csv.DictReader(open(os.path.join(OUT, 'feature_matrix.csv'), encoding='utf-8')))
N = len(rows); ENT = [r['entry'] for r in rows]; POS = {e: i for i, e in enumerate(ENT)}
ALLBIN = ['depth', 'vessels', 'direction', 'named', 'greek']
ALLCAT = {'unit': ['none', 'kk', 'kkrin', 'kkr', 'kk+kkrin'], 'metal': ['none', 'silver', 'gold', 'both'], 'digform': ['none', 'חפור', 'חפר']}
MINLEN, KMAX = 3, 5; LN = math.log(N)
ii, jj = np.meshgrid(np.arange(N + 1), np.arange(N + 1), indexing='ij')
VALID = (jj - ii) >= MINLEN; NSEG = np.where(jj > ii, jj - ii, 1).astype(float)
y = np.log(np.array([float(r['nwords']) for r in rows])); SIG2 = y.var()

def make(bin_, cat, use_len=True):
    blocks = {f: np.array([[1 - int(r[f]), int(r[f])] for r in rows], float) for f in bin_}
    blocks.update({f: np.array([[float(r[f] == l) for l in ALLCAT[f]] for r in rows]) for f in cat})
    p = len(bin_) + sum(len(ALLCAT[f]) - 1 for f in cat) + int(use_len)
    def cf(order):
        out = {}
        for f, X in blocks.items():
            X = X[order]; P = np.vstack([np.zeros(X.shape[1]), np.cumsum(X, 0)]); c = P[None] - P[:, None]
            with np.errstate(divide='ignore', invalid='ignore'):
                out[f] = -2 * np.where(c > 0, c * np.log(c / NSEG[:, :, None]), 0).sum(-1)
        if use_len:
            yy = y[order]; S1 = np.r_[0, np.cumsum(yy)]; S2 = np.r_[0, np.cumsum(yy ** 2)]
            s1 = S1[None] - S1[:, None]; s2 = S2[None] - S2[:, None]
            out['nwords'] = (s2 - s1 ** 2 / NSEG) / SIG2 + NSEG * math.log(2 * math.pi * SIG2)
        return out
    return cf, p

def dp(C):
    F = C[0].copy(); res = [F[N]]; args = []
    for k in range(1, KMAX + 1):
        M = F[:, None] + C; a = M.argmin(0); F = M[a, np.arange(N + 1)]; res.append(F[N]); args.append(a)
    segs = {}
    for K in range(KMAX + 1):
        b, j = [], N
        for k in range(K, 0, -1): j = args[k - 1][j]; b.append(int(j))
        segs[K] = sorted(b)
    return np.array(res), segs

def run(bin_, cat, use_len=True, nperm=2000, seed=1):
    cf, p = make(bin_, cat, use_len)
    def stat(order, back=False):
        C = np.where(VALID, sum(cf(order).values()), np.inf); costs, segs = dp(C)
        K = np.arange(KMAX + 1); bic = costs + ((K + 1) * p + K) * LN; ks = 1 + int(np.argmin(bic[1:]))
        return bic[0] - bic[ks], ks, segs, costs
    G, ks, segs, costs = stat(np.arange(N))
    rng = np.random.default_rng(seed); null = np.array([stat(rng.permutation(N))[0] for _ in range(nperm)])
    return dict(G=round(float(G), 2), K=ks, seams=[ENT[t] for t in segs[ks]], all_K={K: [ENT[t] for t in b] for K, b in segs.items()},
                p=round(float((null >= G - 1e-9).mean()), 4), nperm=nperm), costs, segs

out = {}
# 1. brute-force check of the DP for K = 1, 2 (full feature set)
cf, p = make(ALLBIN, list(ALLCAT)); C = np.where(VALID, sum(cf(np.arange(N)).values()), np.inf)
costs, segs = dp(C)
bf1 = min((C[0, t] + C[t, N], t) for t in range(1, N))
bf2 = min((C[0, a] + C[a, b] + C[b, N], a, b) for a in range(1, N) for b in range(a + 1, N))
out['bruteforce'] = dict(dp_K1=[float(costs[1]), [ENT[t] for t in segs[1]]], bf_K1=[float(bf1[0]), ENT[bf1[1]]],
                         dp_K2=[float(costs[2]), [ENT[t] for t in segs[2]]], bf_K2=[float(bf2[0]), ENT[bf2[1]], ENT[bf2[2]]])
# 2. the project's earlier blocks A/B/C/D (seams before 20, 36, 57) under the M1 cost, vs the optimum at K = 3
t3 = [POS['20'], POS['36'], POS['57']]; e = [0] + t3 + [N]
out['earlier_blocks_K3_cost'] = float(sum(C[e[i], e[i + 1]] for i in range(4))); out['optimal_K3_cost'] = float(costs[3])
out['optimal_K3_seams'] = [ENT[t] for t in segs[3]]
# 3. feature-drop variants (2,000 permutations each)
variants = {
  'full (check)': (ALLBIN, list(ALLCAT), True),
  'drop digform (redundant with depth)': (ALLBIN, ['unit', 'metal'], True),
  'drop depth and digform': ([f for f in ALLBIN if f != 'depth'], ['unit', 'metal'], True),
  'drop greek': ([f for f in ALLBIN if f != 'greek'], list(ALLCAT), True),
  'drop unit': (ALLBIN, ['metal', 'digform'], True),
  'drop nwords': (ALLBIN, list(ALLCAT), False),
}
out['variants'] = {k: run(*v)[0] for k, v in variants.items()}
# 4. entries 11-48 only (inside the dig zone): any seam?
json.dump(out, open(os.path.join(OUT, 'explore.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
