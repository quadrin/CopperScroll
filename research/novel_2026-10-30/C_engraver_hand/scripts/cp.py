"""Exact optimal multiple change-point segmentation (mean shift, Gaussian cost on z-scored features)
and a column-order permutation null. Shared by all tests (frozen in PROTOCOL_FROZEN.md)."""
import numpy as np

def zscore(X):
    X = np.asarray(X, float)
    mu = np.nanmean(X, 0); sd = np.nanstd(X, 0); sd[sd == 0] = 1
    Z = (X - mu) / sd
    Z[np.isnan(Z)] = 0.0          # missing value -> sequence mean
    return Z

def seg_costs(Z):
    """C[i, j] = SSE of rows i..j-1 around their mean, summed over features (j > i)."""
    n = len(Z)
    S1 = np.vstack([np.zeros(Z.shape[1]), np.cumsum(Z, 0)])
    S2 = np.concatenate([[0.0], np.cumsum((Z ** 2).sum(1))])
    C = np.full((n + 1, n + 1), np.inf)
    for i in range(n):
        j = np.arange(i + 1, n + 1); m = (j - i)[:, None]
        s1 = S1[j] - S1[i]; C[i, j] = (S2[j] - S2[i]) - (s1 ** 2 / m).sum(1)
    return C

def best_segmentation(Z, kmax, minlen, pen):
    """Return (K*, change points list [start index of each new segment], gain G = cost0 - min_K(cost_K + K*pen))."""
    n = len(Z); C = seg_costs(Z)
    I, J = np.indices(C.shape); C[(J - I) < minlen] = np.inf
    INF = np.inf
    D = np.full((kmax + 1, n + 1), INF); B = np.zeros((kmax + 1, n + 1), int)
    D[0, :] = C[0, :]
    for k in range(1, kmax + 1):
        for j in range(n + 1):
            v = D[k - 1, :j] + C[:j, j]
            if len(v) == 0: continue
            i = int(np.argmin(v)); D[k, j] = v[i]; B[k, j] = i
    cost0 = D[0, n]
    crit = [D[k, n] + k * pen for k in range(kmax + 1)]
    K = int(np.argmin(crit))
    cps = []; j = n
    for k in range(K, 0, -1):
        i = B[k, j]; cps.append(i); j = i
    return K, sorted(cps), float(cost0 - crit[K]), [float(c) for c in crit]

def permutation_null(Z, kmax, minlen, pen, nperm, seed, match_fn=None):
    rng = np.random.default_rng(seed); G = []; M = []
    for _ in range(nperm):
        Zp = Z[rng.permutation(len(Z))]
        K, cps, g, _ = best_segmentation(Zp, kmax, minlen, pen)
        G.append(g); M.append(match_fn(cps) if match_fn else 0)
    return np.array(G), np.array(M)

def placement_p(n, K, minlen, accept_sets, m_obs, nsim, seed):
    """Chance that K change points placed uniformly at random among admissible segmentations of n items
    (all segments >= minlen) hit >= m_obs seams. accept_sets: list of sets of change indices (start index of new segment)."""
    if K == 0: return None
    rng = np.random.default_rng(seed); hit = 0; tot = 0
    while tot < nsim:
        cps = np.sort(rng.choice(np.arange(1, n), K, replace=False))
        b = np.r_[0, cps, n]
        if np.any(np.diff(b) < minlen): continue
        tot += 1
        m = sum(any(c in A for c in cps) for A in accept_sets)
        hit += m >= m_obs
    return hit / tot
