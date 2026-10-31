"""EXPLORATORY, AFTER THE CONFIRMATORY RUN (new model; not a rescue of the frozen test).

Why: the frozen measure h = extent / pitch uses an extent window of +-0.5 pitch, so part of the extent scales with the
local pitch, and the calibration k (from class differences within lines) was applied to h/pitch although the copper
pitch is not compressed. The drawn III rise in h/pitch combines a pitch rise and a larger letter-height rise.
This script:
 1. decomposes the drawing (fac_h, facsimile pitch) and the frozen copper (extent, pitch) contrasts, III and I, same letters;
 2. re-measures every letter (training, test, control) with a FIXED extent window +-W Lh (W = 0.92, i.e. half the median
    training pitch 1.84 Lh), independent of the local pitch; class table and compression k_fix from training only;
 3. compares the copper fixed-window height contrast with the k_fix-compressed drawing height contrast under two
    hypotheses: (H_claim) true letter height changes as drawn; (H_pitch) letter height scales with the copper pitch only.
Output: out/exploratory/post_run_decomposition.json. Numbers only."""
import sys, os, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from measure import grad_stack, group_mean, extent_from
from measure_set import FINAL, load_placed, BEFORE, AFTER

W = 0.92
SEED = 20261101
rows = load_placed("../out/placed_letters.csv", {2, 3, 4, 6, 7, 8, 11, 16, 17, 18, 21, 22})
conf = {int(r["uid"]): r for r in csv.DictReader(open("../out/letters_measured.csv", encoding="utf-8"))}
trn = {int(r["uid"]): r for r in csv.DictReader(open("../out/exploratory/train_letters.csv", encoding="utf-8"))}
for r in rows:
    src = conf.get(r["uid"]) or trn.get(r["uid"])
    r["pitch"] = float(src["pitch"]) if src and src["pitch"] not in ("", "nan") else np.nan
    r["ext_frozen"] = float(src["ext_ALL"]) if src and src["ext_ALL"] not in ("", "nan") else np.nan
    r["h_rel_cu"] = float(src["h_rel_cu"]) if src and src["h_rel_cu"] not in ("", "nan") else np.nan
    lh = r["lh88"]
    G, lights, _ = grad_stack(r["cut"], r["x88"], r["y88"], max(FINAL["PITCH_HALFW"], FINAL["EXT_HALFW"]) * lh + 4,
                              FINAL["PITCH_HALFH"] * lh, FINAL["SIGMA"])
    img = group_mean(G, lights, "ALL")
    ex = extent_from(img, lh, 2 * W * lh, FINAL) if img is not None else np.nan
    r["hL_fix"] = ex / lh if np.isfinite(ex) else np.nan
    imT, imB = group_mean(G, lights, "T"), group_mean(G, lights, "B")
    r["hL_fix_T"] = extent_from(imT, lh, 2 * W * lh, FINAL) / lh if imT is not None else np.nan
    r["hL_fix_B"] = extent_from(imB, lh, 2 * W * lh, FINAL) / lh if imB is not None else np.nan

TRAIN = {6, 11, 16, 17, 18, 21, 22}
tr = [r for r in rows if r["cut"] in TRAIN and np.isfinite(r["hL_fix"])]
let = np.array([r["letter"] for r in tr]); hv = np.array([r["hL_fix"] for r in tr]); hp = np.array([r["hp_dr"] for r in tr])
tab = {L: float(np.median(hv[let == L])) for L in set(let) if (let == L).sum() >= 5}
allm = float(np.median(hv))
xs = np.array([np.log(np.median(hp[let == L]) / np.median(hp)) for L in tab])
ys = np.array([np.log(tab[L] / allm) for L in tab])
k_fix = float((xs * ys).sum() / (xs * xs).sum())
from scipy.stats import spearmanr
okTB = [r for r in tr if np.isfinite(r["hL_fix_T"]) and np.isfinite(r["hL_fix_B"])]
rho_fix_train = float(spearmanr([r["hL_fix_T"] for r in okTB], [r["hL_fix_B"] for r in okTB]).correlation)
for r in rows:
    r["hL_rel"] = r["hL_fix"] / tab.get(r["letter"], allm) if np.isfinite(r["hL_fix"]) else np.nan

# drawing class medians of fac_h (whole scroll, from placed letters of all columns is enough for ratios within column)
facm = {}
for r in rows:
    facm.setdefault(r["letter"], []).append(float(r["fac_h"]) / float(r["fac_pitch"]))
facm = {k: float(np.median(v)) for k, v in facm.items()}


def ratio(S, key):
    b = np.array([r[key] for r in S if r["l"] in BEFORE and np.isfinite(r[key])])
    a = np.array([r[key] for r in S if r["l"] in AFTER and np.isfinite(r[key])])
    return float(np.median(a) / np.median(b)), b, a


def boot(b, a, n=5000, seed=SEED):
    g = np.random.default_rng(seed)
    v = np.array([np.median(g.choice(a, len(a))) / np.median(g.choice(b, len(b))) for _ in range(n)])
    return [float(np.percentile(v, 5)), float(np.percentile(v, 95))]


out = dict(W_lh=W, k_fix_train=k_fix, n_classes=len(tab), split_half_rho_fix_train=rho_fix_train, columns={})
for col, cuts in (("III", {7, 8}), ("I", {2, 3, 4}), ("II", {6}), ("V", {11}), ("IX", {16}), ("X", {17, 18}), ("XII", {21, 22})):
    S = [r for r in rows if r["col_roman"] == col and r["cut"] in cuts and np.isfinite(r["pitch"])]
    for r in S:
        r["fac_h_rel"] = float(r["fac_h"]) / facm[r["letter"]]   # class-normalised drawn height (facsimile px / class med ratio)
        r["fac_pitch_f"] = float(r["fac_pitch"])
        r["ext_frozen_rel"] = r["h_rel_cu"] * r["pitch"] / r["lh88"] if np.isfinite(r["h_rel_cu"]) else np.nan
    d_pitch, _, _ = ratio(S, "fac_pitch_f")
    d_h, _, _ = ratio(S, "fac_h_rel")
    c_pitch, bp, ap = ratio(S, "pitch")
    c_ext_frozen, _, _ = ratio(S, "ext_frozen_rel")
    c_fix, bf, af = ratio(S, "hL_rel")
    okt = [r for r in S if np.isfinite(r["hL_fix_T"]) and np.isfinite(r["hL_fix_B"])]
    out["columns"][col] = dict(
        role="test" if col == "III" else ("control" if col == "I" else "training"),
        n=len(S), n_before=len(bf), n_after=len(af),
        drawing_pitch_ratio=d_pitch, drawing_height_ratio_classnorm=d_h, drawing_h_over_pitch_ratio=d_h / d_pitch,
        copper_pitch_ratio=c_pitch, copper_pitch_ratio_90=boot(bp, ap),
        copper_frozen_extent_ratio_classnorm=c_ext_frozen,
        copper_fixed_height_ratio=c_fix, copper_fixed_height_ratio_90=boot(bf, af),
        expected_fixed_under_claim=float(d_h ** k_fix), expected_fixed_under_pitch_only=float(c_pitch ** k_fix),
        split_half_rho_fix=float(spearmanr([r["hL_fix_T"] for r in okt], [r["hL_fix_B"] for r in okt]).correlation) if len(okt) > 6 else None)
json.dump(out, open("../out/exploratory/post_run_decomposition.json", "w"), indent=1)
print(json.dumps(out, indent=1))
