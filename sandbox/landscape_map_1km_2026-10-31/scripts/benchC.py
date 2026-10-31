"""Run 27 benchmark C: fresh 1940s features read from 60 windows; supervised (c, rho) on one fold, scored on the other.

usage: python3 benchC.py <reads_dir>
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "sandbox/landscape_map_2026-10-31/scripts"))
from common import sampling_dists  # noqa: E402  (zone shares of the scroll's candidate places)

from model27 import C_GRID, RHO_GRID, RUN, EntryScorer, Landscape, hps_cover, hps_ncells  # noqa: E402

CMAP = {"cave": {"cave"}, "tomb": {"tomb"}, "cistern": {"cistern"}, "well": {"cistern"},
        "pool": {"pool_reservoir"}, "aqueduct": {"channel_aqueduct", "dam"}}
w2g = Transformer.from_crs("EPSG:4326", "EPSG:28191", always_xy=True)


def px_to_latlon(px, py, z):
    n = 256 * 2 ** z
    lon = px / n * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * py / n))))
    return lat, lon


def load_items(L, reads_dir):
    W = {w["id"]: w for w in json.load(open(RUN / "windows.json"))["windows"]}
    G = json.load(open(RUN / "out/mosaic_geometry.json"))
    raw, rows = [], []
    for wid in sorted(W):
        f = Path(reads_dir) / f"{wid}.json"
        if not f.exists():
            raise SystemExit(f"missing reading {f}")
        rd = json.load(open(f))
        g, box = G[wid], W[wid]["box_grid"]
        for it in rd.get("items", []):
            cls = str(it.get("class", "")).lower()
            lat, lon = px_to_latlon(g["px0"] + float(it["x"]), g["py0"] + float(it["y"]), g["z"])
            e, n = w2g.transform(lon, lat)
            inside = box[0] <= e <= box[2] and box[1] <= n <= box[3]
            k = int(L.cell_of(lat, lon)[0])
            raw.append(dict(window=wid, cls=cls, text=it.get("text", ""), confidence=it.get("confidence", ""),
                            x=it["x"], y=it["y"], lat=lat, lon=lon, inside=inside, cell=k))
    raw = pd.DataFrame(raw)
    ok = raw[raw.inside & (raw.cell >= 0) & raw.cls.isin(CMAP)].copy()
    ok["clue"] = ok.cls.map(lambda c: ";".join(sorted(CMAP[c])))
    items = ok.drop_duplicates(["clue", "cell"]).reset_index(drop=True)
    items["item_id"] = np.arange(len(items))
    return raw, items


def folds_of(windows):
    rng = np.random.default_rng(2727)
    order = list(rng.permutation(sorted(windows)))
    return {w: 1 + (i % 2) for i, w in enumerate(order)}


def fit_theta(items, scorers):
    lc = np.zeros(len(C_GRID))
    lr = np.zeros(len(RHO_GRID))
    for r in items.itertuples():
        sc = scorers[r.clue]
        y = sc.pat[r.cell] > 0
        b = sc.p_s[sc.strat[r.cell], 1]
        lc += np.log(np.where(y, C_GRID + b * (1 - C_GRID), (1 - C_GRID) * (1 - b)))
        ns, no = sc.site.sum(), (~sc.site).sum()
        lr += np.log(RHO_GRID / ns if sc.site[r.cell] else (1 - RHO_GRID) / no)
    pc = np.exp(lc - lc.max()); pc /= pc.sum()
    pr = np.exp(lr - lr.max()); pr /= pr.sum()
    return np.outer(pr, pc), pc, pr


def metrics(post, prior, k):
    pt = post[k]
    return dict(cov50=hps_cover(post, k, 0.5), cov90=hps_cover(post, k, 0.9),
                log10bf=float(np.log10(pt / prior[k])), p_true=float(pt), rank=int((post > pt).sum()) + 1,
                n90=hps_ncells(post, 0.9), n50=hps_ncells(post, 0.5))


def named_zone(true_zone, idx, zshare):
    r = np.random.default_rng(10_000_000 + idx)
    if r.random() < 0.8:
        return true_zone
    p = zshare.copy(); p[true_zone] = 0; p /= p.sum()
    return int(r.choice(len(p), p=p))


def score(L, items, scorers, W, zshare):
    rows = []
    for i, r in enumerate(items.itertuples()):
        sc = scorers[r.clue]
        tz = int(L.zone[r.cell])
        for reg in ("R0", "R1"):
            nz = named_zone(tz, int(r.item_id), zshare) if reg == "R1" else -1
            region = None if reg == "R0" else (L.zone == nz, 0.8)
            post, prior, _, _ = sc.posterior(region, RHO_GRID, W)
            rows.append(dict(item=int(r.item_id), window=r.window, fold=r.fold, cls=r.cls, region=reg, zone=tz, named_zone=nz,
                             matched=bool(sc.pat[r.cell] > 0), site=bool(sc.site[r.cell]), **metrics(post, prior, r.cell)))
    return pd.DataFrame(rows)


def cluster_boot(df, col, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    wins = df.window.unique()
    g = {w: df[df.window == w][col].values for w in wins}
    ms = []
    for _ in range(n):
        pick = rng.choice(wins, len(wins))
        v = np.concatenate([g[w] for w in pick])
        ms.append(v.mean())
    return float(np.percentile(ms, 2.5)), float(np.percentile(ms, 97.5))


def main():
    reads = sys.argv[1]
    L = Landscape(1.0)
    zshare = sampling_dists()["zshare"]
    raw, items = load_items(L, reads)
    raw.to_csv(RUN / "out/benchC_raw_reads.csv", index=False)
    fmap = folds_of([w["id"] for w in json.load(open(RUN / "windows.json"))["windows"]])
    items["fold"] = items.window.map(fmap)
    items.to_csv(RUN / "out/benchC_items.csv", index=False)
    print("raw records", len(raw), "| inside & mapped", int((raw.inside & raw.cls.isin(CMAP)).sum()),
          "| items after dedup", len(items), "| by class", items.cls.value_counts().to_dict())
    if len(items) < 80:
        print("UNDERPOWERED: fewer than 80 items; run stops (RULE)")
        json.dump({"n_items": len(items), "verdict": "not identifiable (underpowered)"}, open(RUN / "out/benchC_gate.json", "w"))
        return
    scorers = {c: EntryScorer(L, [frozenset(c.split(";"))]) for c in items.clue.unique()}
    out, thetas = [], {}
    for f in (1, 2):
        W, pc, pr = fit_theta(items[items.fold != f], scorers)
        thetas[f] = dict(c_mean=float(pc @ C_GRID), rho_mean=float(pr @ RHO_GRID), pc=pc.tolist(), pr=pr.tolist())
        out.append(score(L, items[items.fold == f].reset_index(drop=True), scorers, W, zshare))
    df = pd.concat(out, ignore_index=True)
    df.to_csv(RUN / "out/benchC_scores.csv", index=False)
    Wall, pc, pr = fit_theta(items, scorers)
    thetas["all"] = dict(c_mean=float(pc @ C_GRID), rho_mean=float(pr @ RHO_GRID), pc=pc.tolist(), pr=pr.tolist())
    np.save(RUN / "out/theta_all.npy", Wall)
    gate = {"n_items": int(len(items)), "n_windows_with_items": int(items.window.nunique()), "thetas": thetas}
    for reg in ("R0", "R1"):
        d = df[df.region == reg]
        gate[reg] = dict(cov50=float(d.cov50.mean()), cov90=float(d.cov90.mean()), log10bf=float(d.log10bf.mean()),
                         log10bf_ci=cluster_boot(d, "log10bf"), med_rank=float(d["rank"].median()),
                         top1=float((d["rank"] <= 1).mean()), top10=float((d["rank"] <= 10).mean()),
                         med_area90_km2=float(d.n90.median()), matched_share=float(d.matched.mean()),
                         site_share=float(d.site.mean()))
    g1 = all(0.38 <= gate[r]["cov50"] <= 0.62 and 0.82 <= gate[r]["cov90"] <= 0.97 for r in ("R0", "R1"))
    g2 = gate["R1"]["log10bf"] > 0 and gate["R1"]["log10bf_ci"][0] > 0
    gate.update(G1=bool(g1), G2=bool(g2), passes=bool(g1 and g2))
    json.dump(gate, open(RUN / "out/benchC_gate.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in gate.items() if k != "thetas"}, indent=1))
    print("theta means:", {k: (round(v["c_mean"], 3), round(v["rho_mean"], 3)) for k, v in thetas.items()})


if __name__ == "__main__":
    main()
