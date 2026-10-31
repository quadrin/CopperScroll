"""Run 27 reported checks: leave-one-source-out (LOSO) and benchmark A (machinery). Uses the benchmark-C posterior.

usage: python3 checks27.py loso | benchA
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "sandbox/landscape_map_2026-10-31/scripts"))
from common import sampling_dists  # noqa: E402

from benchC import cluster_boot, metrics, named_zone  # noqa: E402
from model27 import (C_GRID, CI, CLASSES, LANDMARK_CLASS, RHO_GRID, RUN, WORDS_FOR_CLASS, EntryScorer,  # noqa: E402
                     Landscape, merge_clues)


def clue_for(c):
    return frozenset({"channel_aqueduct", "dam"}) if c in ("channel_aqueduct", "dam") else frozenset({c})


def run_loso(L, W, zshare):
    r = L.records.copy()
    r["site_key"] = np.where(r.inventory.str.startswith("WBADB"), r.fid.str.rsplit(":", n=1).str[0], r.fid)
    out = []
    for src, sel, seed in (("WBADB", r.inventory.str.startswith("WBADB"), 2728), ("ASI", r.inventory == "ASI", 2728)):
        keys = r[sel].site_key.unique()
        rng = np.random.default_rng(seed)
        pick = rng.choice(keys, size=min(500, len(keys)), replace=False)
        rng2 = np.random.default_rng(2729)
        for j, key in enumerate(pick):
            own = r[r.site_key == key]
            k = int(own.cell.iloc[0])
            cls = own["cls"].values[rng2.integers(len(own))]
            N = L.N.copy()
            np.subtract.at(N, (own.cell.values, own["cls"].map(CI).values), 1)
            sc = EntryScorer(L, [clue_for(cls)], N)
            still = bool(sc.pat[k] > 0)
            for reg in ("R0", "R1"):
                nz = named_zone(int(L.zone[k]), 20_000_000 + j + (0 if src == "WBADB" else 100_000), zshare) if reg == "R1" else -1
                region = None if reg == "R0" else (L.zone == nz, 0.8)
                post, prior, _, _ = sc.posterior(region, RHO_GRID, W)
                out.append(dict(source=src, key=key, cls=cls, region=reg, zone=int(L.zone[k]),
                                still_matched=still, window=key, **metrics(post, prior, k)))
    df = pd.DataFrame(out)
    df.to_csv(RUN / "out/loso_scores.csv", index=False)
    s = df.groupby(["source", "region"]).agg(n=("cov90", "size"), cov50=("cov50", "mean"), cov90=("cov90", "mean"),
                                              log10bf=("log10bf", "mean"), still_matched=("still_matched", "mean"),
                                              med_rank=("rank", "median"), med_area90=("n90", "median"))
    print(s.round(3).to_string())
    return s


def fake_entry(L, rng, D, pc):
    ci = rng.choice(len(C_GRID), p=pc)
    c_true = float(np.clip(C_GRID[ci] + rng.uniform(-0.025, 0.025), 0.01, 0.99))
    Nt = np.where(rng.random(L.N.shape) < c_true, L.N, 0)
    z = rng.choice(len(D["zshare"]), p=D["zshare"])
    cand = np.where((L.zone == z) & (L.N.sum(1) > 0))[0]
    k = int(rng.choice(cand))
    ks, vs = zip(*sorted(D["nclue"].items()))
    n = int(rng.choice(ks, p=np.array(vs) / sum(vs)))
    present = [CLASSES[i] for i in np.where(L.N[k] > 0)[0]]
    words_all, wf = zip(*sorted(D["words"].items()))
    wp = np.array(wf, float) / sum(wf)
    used, sets = set(), []
    for _ in range(n):
        avail = [c for c in present if c not in used and WORDS_FOR_CLASS[c]]
        if avail and rng.random() < 0.8:
            c = avail[rng.integers(len(avail))]
            w = WORDS_FOR_CLASS[c][rng.integers(len(WORDS_FOR_CLASS[c]))]
        else:
            w = words_all[rng.choice(len(words_all), p=wp)]
        used |= set(LANDMARK_CLASS[w]); sets.append(set(LANDMARK_CLASS[w]))
    return k, int(z), c_true, Nt, merge_clues(sets)


def run_benchA(L, W, pc, zshare):
    D = sampling_dists()
    rows = []
    for seed in range(5001, 6001):
        k, z, c_true, Nt, clues = fake_entry(L, np.random.default_rng(seed), D, pc)
        sc = EntryScorer(L, clues, Nt)
        for reg in ("R0", "R1"):
            nz = named_zone(z, seed, zshare) if reg == "R1" else -1
            region = None if reg == "R0" else (L.zone == nz, 0.8)
            post, prior, _, _ = sc.posterior(region, RHO_GRID, W)
            rows.append(dict(seed=seed, region=reg, zone=z, c_true=c_true, window=seed, site=bool(sc.site[k]),
                             **metrics(post, prior, k)))
    df = pd.DataFrame(rows)
    df.to_csv(RUN / "out/benchA27.csv", index=False)
    s = df.groupby("region").agg(n=("cov90", "size"), cov50=("cov50", "mean"), cov90=("cov90", "mean"),
                                 log10bf=("log10bf", "mean"), site=("site", "mean"), med_rank=("rank", "median"))
    print(s.round(3).to_string())
    return s


if __name__ == "__main__":
    L = Landscape(1.0)
    W = np.load(RUN / "out/theta_all.npy")
    zshare = sampling_dists()["zshare"]
    if sys.argv[1] == "loso":
        run_loso(L, W, zshare)
    else:
        g = json.load(open(RUN / "out/benchC_gate.json"))
        run_benchA(L, W, np.array(g["thetas"]["all"]["pc"]), zshare)
