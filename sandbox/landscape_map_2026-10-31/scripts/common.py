"""Scroll entry clues and the benchmark's sampling distributions (RULE.md)."""
from collections import Counter

import numpy as np
import pandas as pd

from model import INP, LANDMARK_CLASS, ZNAMES, words_to_clues, zone_of


def scroll_entries():
    e = pd.read_csv(INP / "entry_features.csv", dtype=str)
    pl = pd.read_csv(INP / "places_v2.csv").dropna(subset=["lat"])
    plz = {r.place_id: zone_of(r.lat, r.lon) for r in pl.itertuples()}
    rows = []
    for r in e.itertuples():
        words = [w for w in str(r.landmarks).split(";") if w in LANDMARK_CLASS]
        clues = words_to_clues(words)
        cands = [p for p in str(r.candidate_places).split(";") if p in plz]
        rows.append(dict(entry=r.entry, title=r.title, words=words, clues=clues, cands=cands,
                         cand_zones=sorted({plz[p] for p in cands if plz[p] >= 0})))
    return rows


def sampling_dists():
    ents = [x for x in scroll_entries() if x["clues"]]
    # zone shares: candidate-place mentions by zone (in-zone places only)
    pl = pd.read_csv(INP / "places_v2.csv").dropna(subset=["lat"])
    plz = {r.place_id: zone_of(r.lat, r.lon) for r in pl.itertuples()}
    zc = Counter(plz[p] for x in ents for p in x["cands"] if plz[p] >= 0)
    zshare = np.array([zc.get(i, 0) for i in range(len(ZNAMES))], float)
    zshare /= zshare.sum()
    ncl = Counter(len(x["clues"]) for x in ents)
    wf = Counter(w for x in ents for w in x["words"])
    return dict(zshare=zshare, nclue=ncl, words=wf, n_entries=len(ents))
