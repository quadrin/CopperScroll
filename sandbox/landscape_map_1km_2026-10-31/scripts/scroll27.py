"""Run 27 scroll scoring (RULE.md "Scroll outputs"). Refuses to run unless benchmark C's gate passed."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "sandbox/landscape_map_2026-10-31/scripts"))
from common import scroll_entries  # noqa: E402

from model27 import C_GRID, RHO_GRID, RUN, ZNAMES, EntryScorer, Landscape, hav, hps_ncells  # noqa: E402

REPO = RUN.parents[1]


def credible_points(W, level=0.9):
    flat = W.ravel(); order = np.argsort(flat)[::-1]
    cs = np.cumsum(flat[order]); n = int(np.searchsorted(cs, level) + 1)
    return [np.unravel_index(i, W.shape) for i in order[:n]]


def eig_all(sc, post):
    """Expected information gain (bits) of a perfect check of each cell (run 26 definition)."""
    n = sc.nclue; npat = 1 << n
    pv = np.clip(post, 1e-300, 1)
    Ht = -np.sum(pv * np.log2(pv))
    with np.errstate(divide="ignore", invalid="ignore"):
        Hrest = (Ht + pv * np.log2(pv) + (1 - pv) * np.log2(np.clip(1 - pv, 1e-300, 1))) / (1 - pv)

    def h2(p):
        p = np.clip(p, 1e-300, 1 - 1e-16)
        return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    H0 = h2(pv) + (1 - pv) * Hrest
    EH = np.zeros_like(pv)
    pbg = sc.p_s[sc.strat]  # (cells, patterns)
    for t in range(npat):
        k = bin(t).count("1")
        pH = 0.8 ** k * 0.2 ** (n - k)
        pT = pv * pH + (1 - pv) * pbg[:, t]
        pv2 = pv * pH / pT
        EH += pT * (h2(pv2) + (1 - pv2) * Hrest)
    return H0 - EH


def main():
    gate = json.load(open(RUN / "out/benchC_gate.json"))
    if not gate.get("passes"):
        raise SystemExit("benchmark C gate did not pass: the scroll is not scored (RULE.md)")
    L = Landscape(1.0)
    W = np.load(RUN / "out/theta_all.npy")
    cred = credible_points(W)
    pl = L.places.set_index("place_id")
    wb = pd.read_csv(REPO / "sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv")
    samra = wb[wb.site_name.str.contains("Samra", case=False, na=False) & wb.lat.between(31.6, 31.8) & wb.lon.between(35.3, 35.45)]
    special = {"kh_qumran": tuple(pl.loc["kh_qumran", ["lat", "lon"]]), "jericho_palaces": tuple(pl.loc["jericho_palaces", ["lat", "lon"]])}
    if len(samra):
        special["kh_es_samra (WBADB)"] = (float(samra.lat.iloc[0]), float(samra.lon.iloc[0]))
    rows, cand_rows, eig_sum = [], [], np.zeros(L.n)
    eig_special = {k: 0.0 for k in special}
    for e in scroll_entries():
        if not e["clues"]:
            continue
        sc = EntryScorer(L, e["clues"])
        cmask = np.zeros(L.n, bool)
        for p in e["cands"]:
            if p in pl.index:
                cmask |= hav(L.lat, L.lon, pl.loc[p, "lat"], pl.loc[p, "lon"]) <= 2.0
        regions = {"R0": None,
                   "R1": (np.isin(L.zone, e["cand_zones"]), 0.8) if e["cand_zones"] else None,
                   "R2": (cmask, "R2") if cmask.any() else None}
        for reg, region in regions.items():
            post, prior, _, priors = sc.posterior(region, RHO_GRID, W)
            top = np.argsort(post)[::-1][:5]
            same = 0
            for (ri, ci) in cred:
                pr_t = priors[ri] * sc.LR[:, ci]
                same += int(np.argmax(pr_t) == top[0])
            tops = []
            for k in top:
                pid, d = L.nearest_place(k)
                tops.append(f"{L.lat[k]:.4f},{L.lon[k]:.4f} p={post[k]:.4f} near {pid} {d:.1f} km")
            rows.append(dict(entry=e["entry"], title=e["title"], words=";".join(e["words"]), region=reg,
                             p_top=float(post[top[0]]), n_tied_top=int((post == post[top[0]]).sum()),
                             area50_km2=hps_ncells(post, 0.5), area90_km2=hps_ncells(post, 0.9),
                             robust_share=same / len(cred), top5=" | ".join(tops)))
            for p in e["cands"]:
                if p in pl.index:
                    m = hav(L.lat, L.lon, pl.loc[p, "lat"], pl.loc[p, "lon"]) <= 2.0
                    cand_rows.append(dict(entry=e["entry"], region=reg, place=p, post_2km=float(post[m].sum()),
                                          prior_2km=float(prior[m].sum()),
                                          ratio=float(post[m].sum() / prior[m].sum()) if prior[m].sum() > 0 else np.nan))
            if reg == "R1":
                g = eig_all(sc, post)
                eig_sum += np.nan_to_num(g)
                for name, (la, lo) in special.items():
                    k = int(L.cell_of(la, lo)[0])
                    if k >= 0:
                        eig_special[name] += float(np.nan_to_num(g[k]))
    pd.DataFrame(rows).to_csv(RUN / "out/scroll_entries.csv", index=False)
    pd.DataFrame(cand_rows).to_csv(RUN / "out/scroll_candidates.csv", index=False)
    top15 = np.argsort(eig_sum)[::-1][:15]
    voi = [dict(lat=float(L.lat[k]), lon=float(L.lon[k]), zone=ZNAMES[L.zone[k]], eig_bits=float(eig_sum[k]),
                nearest=L.nearest_place(k)[0], dist_km=round(L.nearest_place(k)[1], 2)) for k in top15]
    json.dump({"top15": voi, "special": eig_special, "credible_points": len(cred)}, open(RUN / "out/scroll_voi.json", "w"), indent=1)
    print(pd.DataFrame(rows).groupby("region")[["p_top", "area50_km2", "area90_km2", "robust_share"]].describe().round(3).T)


if __name__ == "__main__":
    main()
