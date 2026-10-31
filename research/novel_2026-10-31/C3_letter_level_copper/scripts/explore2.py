"""EXPLORATORY ONLY (training cuts 6, 11, 16, 17, 18, 21, 22). Second pass: the inter-quantile extent rule against
an alternative (maximum-sum segment), at SIGMA 2 px and EXT_HALFW 0.4 Lh; per-cut split-half reliability; within-region
robust SD of the class-normalised copper height; compression k of the copper measure relative to drawn class
heights (slope through the origin of log class medians, copper on drawing, classes with >= 5 training letters)."""
import sys, csv, json
import numpy as np
from scipy.stats import spearmanr
from measure import grad_stack, group_mean, pitch_from, extent_from, extent_mss, DEFAULT

TRAIN = {6, 11, 16, 17, 18, 21, 22}
TALL = set("ךלןקףץ")
OUT = sys.argv[1]
rows = [r for r in csv.DictReader(open("../out/placed_letters.csv", encoding="utf-8")) if int(r["cut"]) in TRAIN]
for r in rows:
    for k in ("x88", "y88", "lh88", "hp_dr", "h_rel_dr"):
        r[k] = float(r[k])
    r["cut"] = int(r["cut"]); r["l"] = int(r["l"])
p0 = dict(DEFAULT); p0.update(SIGMA=2.0, EXT_HALFW=0.4)
imgs_all = []
for r in rows:
    lh = r["lh88"]
    G, lights, _ = grad_stack(r["cut"], r["x88"], r["y88"], 1.5 * lh + 4, p0["PITCH_HALFH"] * lh, 2.0)
    imgs = {g: group_mean(G, lights, g) for g in ("ALL", "T", "B")}
    imgs_all.append((imgs, pitch_from(imgs["ALL"], lh, p0)[0], lh))
variants = {"iqr_bg10_q0.2": ("iqr", dict(BG_PCT=10.0, Q_LO=0.2, Q_HI=0.8)),
            "iqr_bg10_q0.1": ("iqr", dict(BG_PCT=10.0, Q_LO=0.1, Q_HI=0.9)),
            "mss40": ("mss", dict(MSS_PCT=40.0)), "mss60": ("mss", dict(MSS_PCT=60.0))}
out = {}
let = np.array([r["letter"] for r in rows]); cuts = np.array([r["cut"] for r in rows]); hp = np.array([r["hp_dr"] for r in rows])
cols = np.array([r["col_roman"] for r in rows]); lines = np.array([r["l"] for r in rows])
for name, (kind, pp) in variants.items():
    p = dict(p0); p.update(pp)
    H = {g: np.full(len(rows), np.nan) for g in ("ALL", "T", "B")}
    for i, (imgs, pc, lh) in enumerate(imgs_all):
        if not np.isfinite(pc):
            continue
        for g in H:
            if imgs[g] is None:
                continue
            ex = (extent_from if kind == "iqr" else extent_mss)(imgs[g], lh, pc, p)
            H[g][i] = ex / pc if np.isfinite(ex) else np.nan
    hA, hT, hB = H["ALL"], H["T"], H["B"]
    ok = np.isfinite(hT) & np.isfinite(hB); okA = np.isfinite(hA)
    percut = {int(c): round(float(spearmanr(hT[ok & (cuts == c)], hB[ok & (cuts == c)]).correlation), 3)
              for c in sorted(TRAIN) if (ok & (cuts == c)).sum() > 8}
    cls = {L: float(np.median(hA[okA & (let == L)])) for L in set(let[okA]) if (okA & (let == L)).sum() >= 5}
    allmed = float(np.median(hA[okA]))
    hrel = np.array([hA[i] / cls.get(let[i], allmed) if okA[i] else np.nan for i in range(len(rows))])
    sds = []
    for c in set(cols):
        for rng in (range(1, 7), range(8, 14)):
            m = okA & (cols == c) & np.isin(lines, list(rng))
            if m.sum() >= 8:
                v = hrel[m]; sds.append(1.4826 * np.median(np.abs(v - np.median(v))) / np.median(v))
    dcls = {L: float(np.median(hp[okA & (let == L)])) for L in cls}
    dall = float(np.median(hp[okA]))
    xs = np.array([np.log(dcls[L] / dall) for L in cls]); ys = np.array([np.log(cls[L] / allmed) for L in cls])
    k = float((xs * ys).sum() / (xs * xs).sum())
    tall = okA & np.isin(let, list(TALL)); yod = okA & (let == "י"); rest = okA & ~np.isin(let, list(TALL) + ["י"])
    out[name] = dict(n=int(okA.sum()), rho_TB=round(float(spearmanr(hT[ok], hB[ok]).correlation), 3), rho_TB_percut=percut,
                     rho_TB_percut_median=float(np.median(list(percut.values()))),
                     spread_TB=round(float(np.median(np.abs(hT[ok] - hB[ok]) / ((hT[ok] + hB[ok]) / 2))), 3),
                     tall_ratio=round(float(np.median(hA[tall]) / np.median(hA[rest])), 3),
                     yod_ratio=round(float(np.median(hA[yod]) / np.median(hA[rest])), 3),
                     rho_drawing_raw=round(float(spearmanr(hA[okA], hp[okA]).correlation), 3),
                     n_classes=len(cls), compression_k=round(k, 3), class_rho=round(float(spearmanr(xs, ys).correlation), 3),
                     robust_sd_rel_median=round(float(np.median(sds)), 3), n_region_sds=len(sds))
    print(name, out[name], flush=True)
json.dump(out, open(OUT, "w"), indent=1)
