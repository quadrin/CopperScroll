"""EXPLORATORY ONLY (training columns II, V, IX, X, XII; cuts 6, 11, 16, 17, 18, 21, 22).
Grid over measurement parameters; reports split-half reliability (top-lit vs bottom-lit lights), spread, class
validity (tall classes and yod against the rest, from the script, not from the drawing's sizes) and letter-level
tracking of the drawing. Never reads cuts 2, 3, 4 (control) or 7, 8 (test)."""
import sys, json, itertools, csv
import numpy as np
from scipy.stats import spearmanr
from measure import grad_stack, group_mean, pitch_from, extent_from, DEFAULT

TRAIN_CUTS = {6, 11, 16, 17, 18, 21, 22}
TALL = set("ךלןקףץ")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad/C3work/explore/explore_grid.json"

rows = [r for r in csv.DictReader(open("../out/placed_letters.csv", encoding="utf-8")) if int(r["cut"]) in TRAIN_CUTS]
for r in rows:
    for k in ("x88", "y88", "lh88", "hp_dr", "h_rel_dr"):
        r[k] = float(r[k])
    r["cut"] = int(r["cut"]); r["l"] = int(r["l"])
print("training letters", len(rows))
assert not any(r["cut"] in (2, 3, 4, 7, 8) for r in rows)

GRID = dict(SIGMA=[2.0, 4.0], EXT_HALFW=[0.25, 0.4], BG_PCT=[10.0, 30.0], Q=[(0.1, 0.9), (0.2, 0.8)])
res = {}
store = {}
for sig in GRID["SIGMA"]:
    p0 = dict(DEFAULT); p0["SIGMA"] = sig
    for i, r in enumerate(rows):
        lh = r["lh88"]
        halfw = 1.5 * lh + 4; halfh = p0["PITCH_HALFH"] * lh
        G, lights, _ = grad_stack(r["cut"], r["x88"], r["y88"], halfw, halfh, sig)
        imgs = {g: group_mean(G, lights, g) for g in ("ALL", "T", "B")}
        pit = {g: (pitch_from(imgs[g], lh, p0) if imgs[g] is not None else (np.nan, np.nan)) for g in imgs}
        store[(sig, i)] = (imgs, pit, lh)
    for ehw, bg, q in itertools.product(GRID["EXT_HALFW"], GRID["BG_PCT"], GRID["Q"]):
        p = dict(p0); p.update(EXT_HALFW=ehw, BG_PCT=bg, Q_LO=q[0], Q_HI=q[1])
        H = {g: [] for g in ("ALL", "T", "B")}
        for i, r in enumerate(rows):
            imgs, pit, lh = store[(sig, i)]
            pc = pit["ALL"][0]
            for g in H:
                if imgs[g] is None or not np.isfinite(pc):
                    H[g].append(np.nan); continue
                ex = extent_from(imgs[g], lh, pc, p)
                H[g].append(ex / pc if np.isfinite(ex) else np.nan)
        hA, hT, hB = (np.array(H[g]) for g in ("ALL", "T", "B"))
        ok = np.isfinite(hT) & np.isfinite(hB)
        rho = spearmanr(hT[ok], hB[ok]).correlation if ok.sum() > 5 else np.nan
        spread = float(np.median(np.abs(hT[ok] - hB[ok]) / ((hT[ok] + hB[ok]) / 2))) if ok.sum() else np.nan
        percut = {}
        for c in sorted(TRAIN_CUTS):
            m = ok & np.array([r["cut"] == c for r in rows])
            percut[c] = round(spearmanr(hT[m], hB[m]).correlation, 3) if m.sum() > 5 else None
        okA = np.isfinite(hA)
        let = np.array([r["letter"] for r in rows])
        tall = okA & np.isin(let, list(TALL)); yod = okA & (let == "י"); rest = okA & ~np.isin(let, list(TALL) + ["י"])
        mr = np.median(hA[rest])
        hp = np.array([r["hp_dr"] for r in rows])
        key = f"s{sig}_w{ehw}_bg{bg}_q{q[0]}"
        res[key] = dict(n=int(okA.sum()), n_TB=int(ok.sum()), rho_TB=round(float(rho), 3), spread_TB=round(spread, 3),
                        rho_TB_percut=percut, median_h=round(float(np.median(hA[okA])), 3),
                        tall_ratio=round(float(np.median(hA[tall]) / mr), 3), n_tall=int(tall.sum()),
                        yod_ratio=round(float(np.median(hA[yod]) / mr), 3), n_yod=int(yod.sum()),
                        rho_drawing=round(float(spearmanr(hA[okA], hp[okA]).correlation), 3))
        print(key, res[key], flush=True)
    pf = np.array([store[(sig, i)][1]["ALL"][0] for i in range(len(rows))])
    pT = np.array([store[(sig, i)][1]["T"][0] for i in range(len(rows))])
    pB = np.array([store[(sig, i)][1]["B"][0] for i in range(len(rows))])
    lhs = np.array([r["lh88"] for r in rows])
    okp = np.isfinite(pT) & np.isfinite(pB)
    res[f"pitch_s{sig}"] = dict(found_ALL=float(np.isfinite(pf).mean()), median_pitch_lh=float(np.nanmedian(pf / lhs)),
                               rel_diff_TB_median=float(np.median(np.abs(pT[okp] - pB[okp]) / ((pT[okp] + pB[okp]) / 2))),
                               rho_TB=float(spearmanr(pT[okp], pB[okp]).correlation))
    print("pitch", sig, res[f"pitch_s{sig}"], flush=True)
    for k in [k for k in store if k[0] == sig]:
        del store[k]
json.dump(res, open(OUT, "w"), indent=1)
