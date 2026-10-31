"""Run 27: copy of run 26 model.py with the run 27 changes (inventory v2, grids 0.05-0.95).

Run 26 docstring follows.
Run 26: calibrated landscape map of the scroll's landmark words.

Implements RULE.md. Cells are hypotheses; records enter through a recording-gap mixture
likelihood stratified by zone and other-class richness; (c, rho) are marginalised.
"""
from __future__ import annotations

import itertools
import math
from pathlib import Path

import numpy as np
import pandas as pd

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]
INP = REPO / "sandbox/landscape_map_2026-10-31/inputs"  # places_v2, entry_features (run 26 copies)
FEATURES = REPO / "sandbox/west_bank_inventory_2026-10-31/data/features_unified_v2.csv"  # inventory v2

KX = math.cos(math.radians(31.8)) * 111.32  # km per degree of longitude
KY = 110.57  # km per degree of latitude
LAT0, LON0, LAT1, LON1 = 31.20, 35.10, 32.27, 35.60

ZONES = [  # lane J / HA-ESI phase-2 plan boxes, first match wins
    ("Z1_GERIZIM", [(32.14, 32.26, 35.19, 35.37)]),
    ("Z2_JORDAN_VALLEY", [(31.76, 32.06, 35.40, 35.60)]),
    ("Z4_JERUSALEM_HILLS", [(31.62, 31.90, 35.10, 35.27)]),
    ("Z3_JUDEAN_DESERT", [(31.20, 31.92, 35.27, 35.60), (31.92, 32.06, 35.30, 35.60)]),
]
ZNAMES = [z for z, _ in ZONES]
DS_LINE = np.array([(31.20, 35.40), (31.46, 35.40), (31.60, 35.43), (31.714, 35.462), (31.77, 35.50)])

CLASSES = ["rockcut", "cave", "tomb", "cistern", "channel_aqueduct", "pool_reservoir", "dovecote",
           "steps_ritual_bath", "fortress", "dam"]
CI = {c: i for i, c in enumerate(CLASSES)}
LANDMARK_CLASS = {  # lane J build_features.py, unchanged
    "cistern": ["cistern"], "pool": ["pool_reservoir"], "reservoir": ["pool_reservoir"],
    "basin": ["pool_reservoir"], "conduit": ["channel_aqueduct", "dam"], "outlet": ["channel_aqueduct", "dam"],
    "tomb": ["tomb"], "monument": ["tomb"], "cave": ["cave"], "dovecote": ["dovecote"],
    "steps": ["steps_ritual_bath"], "pit": ["cistern", "rockcut"], "chamber": ["rockcut"],
    "fortress": ["fortress"]}
WORDS_FOR_CLASS = {c: sorted(w for w, cs in LANDMARK_CLASS.items() if c in cs) for c in CLASSES}

C_GRID = np.round(np.arange(0.05, 0.951, 0.05), 2)
RHO_GRID = np.round(np.arange(0.05, 0.951, 0.05), 2)
RICH_EDGES = [0, 1, 2, 5, 16]  # bins 0, 1, 2-4, 5-15, 16+
SMOOTH = 5.0


def zone_of(lat, lon):
    for zi, (_, boxes) in enumerate(ZONES):
        for a, b, c, d in boxes:
            if a <= lat <= b and c <= lon <= d:
                return zi
    return -1


def in_dead_sea(lat, lon):
    if lat >= 31.77:
        return False
    return lon > np.interp(lat, DS_LINE[:, 0], DS_LINE[:, 1])


def hav(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp, dl = p2 - p1, np.radians(np.asarray(lon2) - np.asarray(lon1))
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * 6371.0088 * np.arcsin(np.sqrt(a))


def merge_clues(sets):
    """Merge class sets that overlap (transitively)."""
    out = [set(s) for s in sets if s]
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            for j in range(i + 1, len(out)):
                if out[i] & out[j]:
                    out[i] |= out.pop(j)
                    changed = True
                    break
            if changed:
                break
    return [frozenset(s) for s in out]


def words_to_clues(words):
    return merge_clues([set(LANDMARK_CLASS[w]) for w in words if w in LANDMARK_CLASS])


class Landscape:
    def __init__(self, cell_km=0.3, include_unlocated=False):
        self.cell_km = cell_km
        dy, dx = cell_km / KY, cell_km / KX
        ni, nj = int(math.ceil((LAT1 - LAT0) / dy)), int(math.ceil((LON1 - LON0) / dx))
        lat = LAT0 + (np.arange(ni) + 0.5) * dy
        lon = LON0 + (np.arange(nj) + 0.5) * dx
        LA, LO = np.meshgrid(lat, lon, indexing="ij")
        LA, LO = LA.ravel(), LO.ravel()
        z = np.array([zone_of(a, b) for a, b in zip(LA, LO)])
        keep = (z >= 0) & ~np.array([in_dead_sea(a, b) for a, b in zip(LA, LO)])
        self.idx = -np.ones(ni * nj, int)
        self.idx[np.where(keep)[0]] = np.arange(keep.sum())
        self.ni, self.nj, self.dy, self.dx = ni, nj, dy, dx
        self.lat, self.lon, self.zone = LA[keep], LO[keep], z[keep]
        self.n = int(keep.sum())

        f = pd.read_csv(FEATURES)
        self.places = pd.read_csv(INP / "places_v2.csv").dropna(subset=["lat"])
        pl = {r.place_id: (r.lat, r.lon) for r in self.places.itertuples()}
        if include_unlocated:
            m = f.lat.isna() & f.name_place.isin(pl.keys())
            f.loc[m, "lat"] = [pl[p][0] for p in f.loc[m, "name_place"]]
            f.loc[m, "lon"] = [pl[p][1] for p in f.loc[m, "name_place"]]
        f = f.dropna(subset=["lat"])
        k = self.cell_of(f.lat.values, f.lon.values)
        f = f[k >= 0].assign(cell=k[k >= 0])
        self.records = f
        N = np.zeros((self.n, len(CLASSES)), np.int64)
        np.add.at(N, (f.cell.values, f["cls"].map(CI).values), 1)
        self.N = N

    def cell_of(self, lat, lon):
        lat, lon = np.atleast_1d(lat), np.atleast_1d(lon)
        i = np.floor((lat - LAT0) / self.dy).astype(int)
        j = np.floor((lon - LON0) / self.dx).astype(int)
        ok = (i >= 0) & (i < self.ni) & (j >= 0) & (j < self.nj)
        out = -np.ones(len(lat), int)
        out[ok] = self.idx[i[ok] * self.nj + j[ok]]
        return out

    def nearest_place(self, k):
        d = hav(self.lat[k], self.lon[k], self.places.lat.values, self.places.lon.values)
        a = int(np.argmin(d))
        return self.places.place_id.values[a], float(d[a])


def rich_bin(x):
    return np.digitize(x, RICH_EDGES[1:])  # 0..4


class EntryScorer:
    """Scores one entry (a list of clue class sets) on a count matrix N."""

    def __init__(self, L: Landscape, clues, N=None):
        self.L, self.clues = L, clues
        N = L.N if N is None else N
        n = len(clues)
        self.nclue = n
        pres = np.zeros((L.n, n), bool)
        used = set()
        for j, cs in enumerate(clues):
            cols = [CI[c] for c in cs]
            used |= set(cols)
            pres[:, j] = N[:, cols].sum(1) > 0
        other = [i for i in range(len(CLASSES)) if i not in used]
        self.other_rich = N[:, other].sum(1)
        self.pat = (pres * (1 << np.arange(n))).sum(1) if n else np.zeros(L.n, int)
        self.site = self.other_rich >= 1
        nz = len(ZNAMES)
        self.strat = L.zone * 5 + rich_bin(self.other_rich)
        self.npat = 1 << n
        # background P_bg(T | s), hierarchical smoothing
        cnt_all = np.bincount(self.pat, minlength=self.npat).astype(float)
        p_all = (cnt_all + 0.5) / (cnt_all.sum() + 0.5 * self.npat)
        p_s = np.zeros((nz * 5, self.npat))
        for zi in range(nz):
            mz = L.zone == zi
            cz = np.bincount(self.pat[mz], minlength=self.npat).astype(float)
            p_z = (cz + SMOOTH * p_all) / (cz.sum() + SMOOTH)
            for b in range(5):
                ms = mz & (rich_bin(self.other_rich) == b)
                cs_ = np.bincount(self.pat[ms], minlength=self.npat).astype(float)
                p_s[zi * 5 + b] = (cs_ + SMOOTH * p_z) / (cs_.sum() + SMOOTH)
        self.p_s = p_s
        # LR table [stratum, pattern, c]
        popc = np.array([bin(t).count("1") for t in range(self.npat)])
        lr = np.zeros((nz * 5, self.npat, len(C_GRID)))
        for t in range(self.npat):
            subs = [b for b in range(self.npat) if b & ~t == 0]
            for ci, c in enumerate(C_GRID):
                ptrue = sum(p_s[:, b] * c ** (popc[t] - popc[b]) for b in subs) * (1 - c) ** (n - popc[t])
                lr[:, t, ci] = ptrue / p_s[:, t]
        self.lr_table = lr
        self.LR = lr[self.strat, self.pat, :]  # (cells, c)

    def prior(self, rho, region=None):
        """region: None, or (mask_in, weight_in)."""
        L = self.L

        def base(mask):
            p = np.zeros(L.n)
            s, o = mask & self.site, mask & ~self.site
            if s.sum() and o.sum():
                p[s], p[o] = rho / s.sum(), (1 - rho) / o.sum()
            elif mask.sum():
                p[mask] = 1.0 / mask.sum()
            return p

        allm = np.ones(L.n, bool)
        if region is None:
            return base(allm)
        m_in, w = region
        if m_in.all() or not m_in.any():
            return base(allm)
        if w == "R2":
            return 0.5 * base(m_in) + 0.5 * base(allm)
        return w * base(m_in) + (1 - w) * base(~m_in)

    def marginal(self, region=None, rho_grid=RHO_GRID):
        """Prior stack (rho, cells) and marginal likelihood matrix M (rho, c)."""
        priors = np.stack([self.prior(r, region) for r in rho_grid])
        return priors, priors @ self.LR

    def posterior(self, region=None, rho_grid=RHO_GRID, theta_w=None):
        """theta_w: shared posterior over (rho, c) from the whole scroll (revision 1);
        None = this entry alone with a uniform prior over pairs (RULE.md)."""
        priors, M = self.marginal(region, rho_grid)
        w = M / M.sum() if theta_w is None else theta_w
        post = np.zeros(self.L.n)
        for ri in range(len(rho_grid)):
            for ci in range(len(C_GRID)):
                if w[ri, ci] > 0:
                    post += w[ri, ci] * priors[ri] * self.LR[:, ci] / M[ri, ci]
        if theta_w is None:
            prior_mix = priors.mean(0)
        else:  # prior of a cell under the shared parameter posterior
            prior_mix = (w.sum(1)[:, None] * priors).sum(0)
        return post, prior_mix, w, priors


RHO_GRID_V1 = RHO_GRID  # run 27: same grid


def pooled_theta(Ms):
    """Posterior over (rho, c) from the product of entries' marginal likelihoods (uniform prior)."""
    lw = sum(np.log(M) for M in Ms)
    lw -= lw.max()
    w = np.exp(lw)
    return w / w.sum()


def hps_cover(post, k_true, level):
    """Fractional coverage of the highest-posterior set at `level` (ties shared)."""
    pt = post[k_true]
    above = post > pt
    m_above = post[above].sum()
    tie = post == pt
    n_tie = tie.sum()
    if m_above >= level:
        return 0.0
    need = math.ceil((level - m_above) / pt - 1e-12)
    return min(1.0, need / n_tie)


def hps_ncells(post, level):
    s = np.sort(post)[::-1]
    cs = np.cumsum(s)
    return int(np.searchsorted(cs, level) + 1)


# ---- revision 2 (FORK_LOG entry 4) ----
def c_prior_from_items(y, b):
    """Grid likelihood of independent-describer items: y_i match in cell, b_i background match rate."""
    y, b = np.asarray(y, float), np.asarray(b, float)
    ll = np.array([np.sum(y * np.log(1 - (1 - c) * (1 - b)) + (1 - y) * np.log((1 - c) * (1 - b)))
                   for c in C_GRID])
    w = np.exp(ll - ll.max())
    return w / w.sum()


def posterior_v2(sc, region, c_prior, rho_grid=RHO_GRID_V1):
    """Per-entry posterior with prior over (rho, c) = uniform(rho) x c_prior; no pooling."""
    priors, M = sc.marginal(region, rho_grid)
    tp = np.outer(np.full(len(rho_grid), 1 / len(rho_grid)), c_prior)
    w = tp * M
    w /= w.sum()
    post = np.zeros(sc.L.n)
    for ri in range(len(rho_grid)):
        for ci in range(len(C_GRID)):
            if w[ri, ci] > 0:
                post += w[ri, ci] * priors[ri] * sc.LR[:, ci] / M[ri, ci]
    prior_mix = priors.mean(0)
    return post, prior_mix, w, priors
