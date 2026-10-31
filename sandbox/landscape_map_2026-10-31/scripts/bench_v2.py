"""Revision 2 benchmarks (FORK_LOG entry 4).

usage: python3 bench_v2.py Bitems            # build B items + c priors (all, fold1, fold2)
       python3 bench_v2.py B <tag>            # B cross-fit
       python3 bench_v2.py A <from> <to> <tag>
"""
import json
import sys

import numpy as np
import pandas as pd

from bench import metrics, summarise, boot_ci
from common import sampling_dists
from model import (C_GRID, CLASSES, INP, LANDMARK_CLASS, RUN, WORDS_FOR_CLASS, EntryScorer, Landscape,
                   c_prior_from_items, merge_clues, posterior_v2)

CMAP = {"cave": {"cave"}, "aqueduct": {"channel_aqueduct", "dam"}, "tomb": {"tomb"},
        "pool": {"pool_reservoir"}, "cistern": {"cistern"}, "well_or_cistern": {"cistern"}}
FOLD1 = {"B_buqeia", "B_marsaba", "K_palaces", "S_samiya", "W_choziba"}
FOLD2 = {"B_hyrcania", "J_kidron", "Q_qumran", "T_jericho"}


def b_items(L):
    m = pd.read_csv(INP / "mandate_features.csv")
    out = []
    for r in m.itertuples():
        if r.feature_class not in CMAP or pd.isna(r.lat):
            continue
        k = int(L.cell_of(r.lat, r.lon)[0])
        if k < 0:
            continue
        sc = EntryScorer(L, [frozenset(CMAP[r.feature_class])])
        y = int(sc.pat[k] > 0)
        b = float(sc.p_s[sc.strat[k], 1])
        out.append(dict(r=r, k=k, sc=sc, y=y, b=b, fold=1 if r.window in FOLD1 else 2))
    assert all(it["r"].window in FOLD1 | FOLD2 for it in out)
    return out


def c_priors(items):
    pri = {}
    for name, sel in (("all", lambda it: True), ("fold1", lambda it: it["fold"] == 1),
                      ("fold2", lambda it: it["fold"] == 2)):
        s = [it for it in items if sel(it)]
        pri[name] = c_prior_from_items([it["y"] for it in s], [it["b"] for it in s]).tolist()
    return pri


def run_B(tag):
    L = Landscape()
    items = b_items(L)
    pri = c_priors(items)
    rows = []
    for it in items:
        cp = np.array(pri["fold2" if it["fold"] == 1 else "fold1"])  # prior from the other fold
        for reg in ("R0", "R1"):
            region = None if reg == "R0" else (L.zone == L.zone[it["k"]], 0.8)
            post, prior, w, _ = posterior_v2(it["sc"], region, cp)
            rows.append(dict(item=it["r"].item_id, window=it["r"].window, fold=it["fold"], cls=it["r"].feature_class,
                             region=reg, y=it["y"], b=it["b"], c_post_mean=float((w.sum(0) * C_GRID).sum()),
                             **metrics(post, prior, it["k"])))
    df = pd.DataFrame(rows)
    df.to_csv(RUN / f"out/benchB_{tag}.csv", index=False)
    return df


def fake_entry_v2(L, rng, D, c_prior):
    ci = rng.choice(len(C_GRID), p=c_prior)
    c_true = float(np.clip(C_GRID[ci] + rng.uniform(-0.05, 0.05), 0.01, 0.99))
    keep = rng.random(L.N.shape) < c_true  # cell x class blocks
    Nt = np.where(keep, L.N, 0)
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


def run_A(a, b, tag):
    L = Landscape()
    D = sampling_dists()
    cp = np.array(json.load(open(RUN / "out/c_prior_v2.json"))["all"])
    rows = []
    for seed in range(a, b + 1):
        rng = np.random.default_rng(seed)
        fe = fake_entry_v2(L, rng, D, cp)
        r2 = np.random.default_rng(10_000_000 + seed)  # amendment 1a
        if r2.random() < 0.8:
            nz = fe["zone"]
        else:
            p = D["zshare"].copy(); p[fe["zone"]] = 0; p /= p.sum()
            nz = int(r2.choice(len(p), p=p))
        sc = EntryScorer(L, fe["clues"], fe["Nt"])
        for reg in ("R0", "R1"):
            region = None if reg == "R0" else (L.zone == nz, 0.8)
            post, prior, w, _ = posterior_v2(sc, region, cp)
            rows.append(dict(seed=seed, region=reg, zone=fe["zone"], named_zone=nz if reg == "R1" else -1,
                             c_true=fe["c_true"], nclue=len(fe["clues"]), kinds=";".join(fe["kinds"]),
                             truth_site=bool(sc.site[fe["k"]]), truth_pat=int(sc.pat[fe["k"]]),
                             c_post_mean=float((w.sum(0) * C_GRID).sum()),
                             rho_post_mean=float((w.sum(1) * np.arange(1, 10) / 10).sum()),
                             **metrics(post, prior, fe["k"])))
    df = pd.DataFrame(rows)
    df.to_csv(RUN / f"out/benchA_{tag}.csv", index=False)
    return df


if __name__ == "__main__":
    if sys.argv[1] == "Bitems":
        L = Landscape(); items = b_items(L); pri = c_priors(items)
        json.dump(dict(c_grid=C_GRID.tolist(), **pri,
                       n={f: sum(1 for it in items if f == "all" or it["fold"] == int(f[-1])) for f in pri},
                       matched={f: sum(it["y"] for it in items if f == "all" or it["fold"] == int(f[-1])) for f in pri}),
                  open(RUN / "out/c_prior_v2.json", "w"), indent=1)
        for f, p in pri.items():
            print(f, "mean c", round(float(np.dot(p, C_GRID)), 3), np.round(p, 3))
        sys.exit()
    df = run_B(sys.argv[2]) if sys.argv[1] == "B" else run_A(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    s = summarise(df); s["med_area90_km2"] *= 0.09
    print(s.round(3).to_string())
    for reg in ("R0", "R1"):
        print(reg, "log10bf 95% CI", np.round(boot_ci(df[df.region == reg].log10bf), 3))
