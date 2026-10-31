"""Benchmarks A (fake entries on thinned records) and B (1940s map features), RULE.md.

usage: python3 bench.py A <seed_from> <seed_to> <tag> [cell_km]
       python3 bench.py B <tag> [cell_km]
"""
import json
import sys

import numpy as np
import pandas as pd

from common import sampling_dists
from model import (CI, CLASSES, INP, RUN, WORDS_FOR_CLASS, LANDMARK_CLASS, EntryScorer, Landscape,
                   hps_cover, hps_ncells, merge_clues, zone_of)


def metrics(post, prior, k):
    pt = post[k]
    rank = int((post > pt).sum()) + 1
    return dict(cov50=hps_cover(post, k, 0.5), cov90=hps_cover(post, k, 0.9),
                log10bf=float(np.log10(pt / prior[k])), p_true=float(pt), rank=rank,
                n90=hps_ncells(post, 0.9), n50=hps_ncells(post, 0.5), p_top=float(post.max()))


def fake_entry(L, rng, D):
    c_true = rng.uniform(0.2, 0.8)
    Nt = rng.binomial(L.N, c_true)
    z = rng.choice(len(D["zshare"]), p=D["zshare"])
    cand = np.where((L.zone == z) & (L.N.sum(1) > 0))[0]
    k = int(rng.choice(cand))
    ks, vs = zip(*sorted(D["nclue"].items()))
    n = int(rng.choice(ks, p=np.array(vs) / sum(vs)))
    present = [CLASSES[i] for i in np.where(L.N[k] > 0)[0]]
    words_all, wf = zip(*sorted(D["words"].items()))
    wp = np.array(wf, float) / sum(wf)
    used, sets, kinds = set(), [], []
    for _ in range(n):
        avail = [c for c in present if c not in used and WORDS_FOR_CLASS[c]]
        if avail and rng.random() < 0.8:
            c = avail[rng.integers(len(avail))]
            w = WORDS_FOR_CLASS[c][rng.integers(len(WORDS_FOR_CLASS[c]))]
            kinds.append("true")
        else:
            w = words_all[rng.choice(len(words_all), p=wp)]
            kinds.append("wrong")
        used |= set(LANDMARK_CLASS[w])
        sets.append(set(LANDMARK_CLASS[w]))
    return dict(k=k, zone=int(z), c_true=c_true, Nt=Nt, clues=merge_clues(sets), kinds=kinds)


def run_A(a, b, tag, cell_km=0.3):
    L = Landscape(cell_km)
    D = sampling_dists()
    rows = []
    for seed in range(a, b + 1):
        rng = np.random.default_rng(seed)
        fe = fake_entry(L, rng, D)
        sc = EntryScorer(L, fe["clues"], fe["Nt"])
        for reg in ("R0", "R1"):
            region = None if reg == "R0" else (L.zone == fe["zone"], 0.8)
            post, prior, w, _ = sc.posterior(region)
            m = metrics(post, prior, fe["k"])
            c_post = float((w.sum(0) * np.arange(1, 10) / 10).sum())
            rows.append(dict(seed=seed, region=reg, zone=fe["zone"], c_true=fe["c_true"],
                             nclue=len(fe["clues"]), kinds=";".join(fe["kinds"]),
                             truth_site=bool(sc.site[fe["k"]]), truth_pat=int(sc.pat[fe["k"]]),
                             c_post_mean=c_post, **m))
    df = pd.DataFrame(rows)
    df.to_csv(RUN / f"out/benchA_{tag}.csv", index=False)
    return df


def run_A_v1(a, b, tag, cell_km=0.3, scroll_size=50):
    """Revision 1: fake scrolls of `scroll_size` consecutive seeds; (c, rho) pooled per scroll."""
    from model import RHO_GRID_V1, pooled_theta
    L = Landscape(cell_km)
    D = sampling_dists()
    rows = []
    for s0 in range(a, b + 1, scroll_size):
        seeds = list(range(s0, min(s0 + scroll_size, b + 1)))
        fes, scs = [], []
        for seed in seeds:
            fe = fake_entry(L, np.random.default_rng(seed), D)
            fes.append(fe)
            scs.append(EntryScorer(L, fe["clues"], fe["Nt"]))
        # amendment 1a: the zone named to R1 is right with probability 0.8
        named = []
        for seed, fe in zip(seeds, fes):
            r = np.random.default_rng(10_000_000 + seed)
            if r.random() < 0.8:
                named.append(fe["zone"])
            else:
                p = D["zshare"].copy(); p[fe["zone"]] = 0; p /= p.sum()
                named.append(int(r.choice(len(p), p=p)))
        for reg in ("R0", "R1"):
            regs = [None if reg == "R0" else (L.zone == nz, 0.8) for nz in named]
            Ms = [sc.marginal(rg, RHO_GRID_V1)[1] for sc, rg in zip(scs, regs)]
            W = pooled_theta(Ms)
            c_mean = float((W.sum(0) * np.arange(1, 10) / 10).sum())
            rho_mean = float((W.sum(1) * RHO_GRID_V1).sum())
            for seed, fe, sc, rg, nz in zip(seeds, fes, scs, regs, named):
                post, prior, w, _ = sc.posterior(rg, RHO_GRID_V1, W)
                m = metrics(post, prior, fe["k"])
                rows.append(dict(scroll=s0, seed=seed, region=reg, zone=fe["zone"], c_true=fe["c_true"],
                                 named_zone=nz if reg == "R1" else -1,
                                 nclue=len(fe["clues"]), kinds=";".join(fe["kinds"]),
                                 truth_site=bool(sc.site[fe["k"]]), truth_pat=int(sc.pat[fe["k"]]),
                                 c_post_mean=c_mean, rho_post_mean=rho_mean, **m))
    df = pd.DataFrame(rows)
    df.to_csv(RUN / f"out/benchA_{tag}.csv", index=False)
    return df


def run_B(tag, cell_km=0.3):
    L = Landscape(cell_km)
    m = pd.read_csv(INP / "mandate_features.csv")
    cmap = {"cave": {"cave"}, "aqueduct": {"channel_aqueduct", "dam"}, "tomb": {"tomb"},
            "pool": {"pool_reservoir"}, "cistern": {"cistern"}, "well_or_cistern": {"cistern"}}
    rows = []
    for r in m.itertuples():
        if r.feature_class not in cmap or pd.isna(r.lat):
            continue
        k = int(L.cell_of(r.lat, r.lon)[0])
        if k < 0:
            continue
        sc = EntryScorer(L, [frozenset(cmap[r.feature_class])])
        for reg in ("R0", "R1"):
            region = None if reg == "R0" else (L.zone == L.zone[k], 0.8)
            post, prior, w, _ = sc.posterior(region)
            rows.append(dict(item=r.item_id, window=r.window, cls=r.feature_class, region=reg,
                             zone=int(L.zone[k]), truth_pat=int(sc.pat[k]), truth_site=bool(sc.site[k]),
                             **metrics(post, prior, k)))
    df = pd.DataFrame(rows)
    df.to_csv(RUN / f"out/benchB_{tag}.csv", index=False)
    return df


def summarise(df, by=("region",)):
    g = df.groupby(list(by))
    s = g.agg(n=("cov90", "size"), cov50=("cov50", "mean"), cov90=("cov90", "mean"),
              log10bf=("log10bf", "mean"), med_p_true=("p_true", "median"), med_rank=("rank", "median"),
              top1=("rank", lambda x: (x <= 1).mean()), top10=("rank", lambda x: (x <= 10).mean()),
              top100=("rank", lambda x: (x <= 100).mean()), med_area90_km2=("n90", "median"))
    return s


def boot_ci(x, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    ms = [rng.choice(x, len(x)).mean() for _ in range(n)]
    return float(np.percentile(ms, 2.5)), float(np.percentile(ms, 97.5))


if __name__ == "__main__":
    if sys.argv[1] in ("A", "A1"):
        a, b, tag = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        ck = float(sys.argv[5]) if len(sys.argv) > 5 else 0.3
        df = (run_A if sys.argv[1] == "A" else run_A_v1)(a, b, tag, ck)
    else:
        tag = sys.argv[2]
        ck = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
        df = run_B(tag, ck)
    s = summarise(df)
    s["med_area90_km2"] *= (ck ** 2)
    print(s.round(3).to_string())
    for reg in ("R0", "R1"):
        print(reg, "log10bf 95% CI", np.round(boot_ci(df[df.region == reg].log10bf), 3))
