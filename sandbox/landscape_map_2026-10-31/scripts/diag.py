"""Dev-only diagnostics: where does the posterior mass go, compared with where the truth is."""
import sys
import numpy as np, pandas as pd
from common import sampling_dists
from model import Landscape, EntryScorer
from bench import fake_entry
L = Landscape(); D = sampling_dists()
rows = []
for seed in range(1, 201):
    rng = np.random.default_rng(seed); fe = fake_entry(L, rng, D)
    sc = EntryScorer(L, fe["clues"], fe["Nt"]); k = fe["k"]
    post, prior, w, _ = sc.posterior(None)
    matched = sc.pat > 0; site = sc.site; rec = fe["Nt"].sum(1) > 0
    rows.append(dict(seed=seed, c_true=fe["c_true"], t_matched=matched[k], t_site=site[k], t_rec=rec[k],
                     m_matched=post[matched].sum(), m_site=post[site].sum(), m_rec=post[rec].sum(),
                     m_site_matched=post[site & matched].sum(), m_nonsite_matched=post[~site & matched].sum(),
                     m_nonsite_unmatched_rec=post[~site & ~matched & rec].sum(),
                     m_never=post[~rec].sum()))
d = pd.DataFrame(rows)
print("truth matched", d.t_matched.mean().round(3), "| post mass on matched", d.m_matched.mean().round(3))
print("truth site", d.t_site.mean().round(3), "| post mass on sites", d.m_site.mean().round(3))
print("truth in a cell with any kept record", d.t_rec.mean().round(3), "| post mass there", d.m_rec.mean().round(3))
print("cells: site&matched truth", (d.t_site & d.t_matched).mean().round(3), "mass", d.m_site_matched.mean().round(3))
print("cells: nonsite&matched truth", (~d.t_site & d.t_matched).mean().round(3), "mass", d.m_nonsite_matched.mean().round(3))
print("cells: never-recorded (after thinning) truth", (~d.t_rec).mean().round(3), "mass", d.m_never.mean().round(3))
d["cb"] = pd.cut(d.c_true, [0.2, 0.4, 0.6, 0.8])
print(d.groupby("cb")[["t_matched", "m_matched", "t_rec", "m_rec"]].mean().round(3))
