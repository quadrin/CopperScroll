"""C3 confirmatory run (frozen; see PROTOCOL_FROZEN.md). One run.

  python3 -I run_test.py            -> confirmatory: test column III (cuts 7, 8), control column I (cuts 2, 3, 4)
  python3 -I run_test.py smoke      -> code check on TRAINING cuts only: "test" X (17, 18), "control" II (6); writes to SP

Steps: measure every placed W2F letter of the test and control cuts (measure_set.FINAL, pitch fallback);
class-normalise with the frozen training table (out/class_medians.json); gate; primary statistic; decision;
secondary and paired analyses. Numbers only are written to the repository.
"""
import sys, os, json, csv, hashlib, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python3 -I drops the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr
from measure_set import (FINAL, load_placed, measure_rows, normalise, split_half, class_validity, region_contrast,
                         line_contrast, BEFORE, AFTER)
from c3lib import SP, check_a2

SMOKE = len(sys.argv) > 1 and sys.argv[1] == "smoke"
if SMOKE:
    TEST_COL, TEST_CUTS, CTRL_COL, CTRL_CUTS = "X", {17, 18}, "II", {6}
    OUTD = SP + "/C3work/smoke_out"
else:
    TEST_COL, TEST_CUTS, CTRL_COL, CTRL_CUTS = "III", {7, 8}, "I", {2, 3, 4}
    OUTD = os.path.abspath("../out")
os.makedirs(OUTD, exist_ok=True)

# ---- frozen parameters
THR = 0.038            # half the calibrated expected copper effect: 0.5 * k(0.527) * drawing effect(0.146)
THR_UNCAL = 0.073      # half the uncalibrated drawing effect (sensitivity only; does not decide)
G1_RHO_ALL = 0.50      # split-half Spearman, all measured test + control letters
G1_RHO_TEST = 0.40     # split-half Spearman, test-column letters only
G2_SPREAD = 0.15       # median relative |h_T - h_B|
G3_MIN_BEFORE, G3_MIN_AFTER = 30, 10   # measured letters per region, test and control columns
NBOOT, SEED = 10000, 20261031

t0 = time.time()
a2 = check_a2()
tab = json.load(open("../out/class_medians.json", encoding="utf-8"))
rows = load_placed("../out/placed_letters.csv", TEST_CUTS | CTRL_CUTS)
rows = [r for r in rows if r["col_roman"] in (TEST_COL, CTRL_COL)]
meas = measure_rows(rows)
normalise(meas, tab["class_medians"], tab["overall_median"])
T = [d for d in meas if d["col_roman"] == TEST_COL and np.isfinite(d["h_rel_cu"])]
C = [d for d in meas if d["col_roman"] == CTRL_COL and np.isfinite(d["h_rel_cu"])]
ALLM = T + C

# ---- gate (direction-blind)
sh_all, sh_test = split_half(ALLM), split_half(T)
cv = class_validity(ALLM)
cnt = {f"{col}_{reg}": sum(1 for d in S if d["l"] in rng) for col, S in ((TEST_COL, T), (CTRL_COL, C))
       for reg, rng in (("before", BEFORE), ("after", AFTER))}
gate = dict(G1_all=bool(sh_all["rho"] >= G1_RHO_ALL), G1_test=bool(sh_test["rho"] >= G1_RHO_TEST),
            G2=bool(sh_all["spread"] <= G2_SPREAD),
            G3=bool(all(cnt[f"{c}_before"] >= G3_MIN_BEFORE and cnt[f"{c}_after"] >= G3_MIN_AFTER for c in (TEST_COL, CTRL_COL))),
            G4=bool(cv["tall_ratio"] > 1.0 and cv["yod_ratio"] < 1.0))
gate_pass = all(gate.values())

# ---- primary statistic
cT, bT, aT = region_contrast(T, "h_rel_cu")
cC, bC, aC = region_contrast(C, "h_rel_cu")
delta = cT - cC
rng = np.random.default_rng(SEED)
bs = np.empty(NBOOT); bsT = np.empty(NBOOT)
for i in range(NBOOT):
    t = np.median(rng.choice(aT, len(aT))) / np.median(rng.choice(bT, len(bT))) - 1
    c = np.median(rng.choice(aC, len(aC))) / np.median(rng.choice(bC, len(bC))) - 1
    bs[i] = t - c; bsT[i] = t
p_boot = float(np.mean(bs <= 0))
lo5, hi95 = float(np.percentile(bs, 5)), float(np.percentile(bs, 95))
mw = mannwhitneyu(aT, bT, alternative="greater")
mwC = mannwhitneyu(aC, bC, alternative="greater")

if not gate_pass:
    verdict, label = "not identifiable from available evidence (measurement gate failed)", "not obtained"
elif cT >= THR and delta >= THR and p_boot < 0.05:
    verdict, label = "supported relative to the registered alternatives", "obtained"
elif hi95 < THR:
    verdict, label = "rejected", "not obtained"
else:
    verdict, label = "not identifiable from available evidence (gate passed)", "partly"

# ---- secondary: drawing on the same measured letters; line-level; uncalibrated threshold
dT, _, _ = region_contrast(T, "h_rel_dr"); dC, _, _ = region_contrast(C, "h_rel_dr")
sec = dict(drawing_contrast_test_same_letters=dT, drawing_contrast_control_same_letters=dC,
           line_level_copper_test=line_contrast(T, "h_rel_cu"), line_level_copper_control=line_contrast(C, "h_rel_cu"),
           line_level_drawing_test=line_contrast(T, "h_rel_dr"), line_level_drawing_control=line_contrast(C, "h_rel_dr"),
           uncalibrated_threshold=THR_UNCAL, delta_ge_uncal=bool(delta >= THR_UNCAL), hi95_lt_uncal=bool(hi95 < THR_UNCAL),
           own_pitch_only=None)
own = [d for d in ALLM if d["pitch_src"] == "own"]
cTo, _, _ = region_contrast([d for d in own if d["col_roman"] == TEST_COL], "h_rel_cu")
cCo, _, _ = region_contrast([d for d in own if d["col_roman"] == CTRL_COL], "h_rel_cu")
sec["own_pitch_only"] = dict(c_test=cTo, c_control=cCo, delta=(cTo - cCo) if (cTo is not None and cCo is not None) else None)
sec["by_cut"] = {}
for c in sorted(TEST_CUTS | CTRL_CUTS):
    S = [d for d in ALLM if d["cut"] == c]
    cc, b, a = region_contrast(S, "h_rel_cu")
    sec["by_cut"][str(c)] = dict(c_copper=cc, n_before=len(b), n_after=len(a), split_half=split_half(S))
sec["pitch_test_before_after_median"] = [float(np.median([d["pitch"] for d in T if d["l"] in BEFORE])),
                                         float(np.median([d["pitch"] for d in T if d["l"] in AFTER]))]
sec["extent_test_before_after_median"] = [float(np.median([d["ext_ALL"] for d in T if d["l"] in BEFORE])),
                                          float(np.median([d["ext_ALL"] for d in T if d["l"] in AFTER]))]

# ---- paired analysis (secondary, descriptive)
def ols(y, X):
    X = np.column_stack([np.ones(len(y))] + X)
    return np.linalg.lstsq(X, y, rcond=None)[0]


def paired(S, label):
    S = [d for d in S if (d["l"] in BEFORE or d["l"] in AFTER) and np.isfinite(d["h_rel_dr"])]
    cu = np.array([d["h_rel_cu"] for d in S]); dr = np.array([d["h_rel_dr"] for d in S])
    after = np.array([1.0 if d["l"] in AFTER else 0.0 for d in S])
    raw_cu = np.array([d["h_ALL"] for d in S]); raw_dr = np.array([d["hp_dr"] for d in S])
    out = dict(n=len(S), rho_rel=float(spearmanr(cu, dr).correlation), rho_raw=float(spearmanr(raw_cu, raw_dr).correlation))
    b = ols(cu, [dr, after]); out["copper_on_drawing_plus_after"] = dict(slope_drawing=float(b[1]), step_after=float(b[2]))
    g0 = ols(dr, [after])[1]; g = ols(dr, [cu, after])[2]
    out["drawing_step_g0"] = float(g0); out["drawing_step_given_copper_g"] = float(g)
    out["share_of_drawing_step_explained_by_copper"] = float(1 - g / g0) if g0 != 0 else None
    r2 = np.random.default_rng(SEED + 1); bb = []
    idx_b = np.where(after == 0)[0]; idx_a = np.where(after == 1)[0]
    for _ in range(2000):
        ii = np.concatenate([r2.choice(idx_b, len(idx_b)), r2.choice(idx_a, len(idx_a))])
        bb.append(ols(cu[ii], [dr[ii], after[ii]])[1:])
    bb = np.array(bb)
    out["copper_on_drawing_plus_after_90ci"] = dict(slope=[float(np.percentile(bb[:, 0], 5)), float(np.percentile(bb[:, 0], 95))],
                                                    step=[float(np.percentile(bb[:, 1], 5)), float(np.percentile(bb[:, 1], 95))])
    return out


paired_res = {TEST_COL: paired(T, TEST_COL), CTRL_COL: paired(C, CTRL_COL)}

res = dict(mode="smoke (training cuts; not a test)" if SMOKE else "confirmatory", test_col=TEST_COL, test_cuts=sorted(TEST_CUTS),
           control_col=CTRL_COL, control_cuts=sorted(CTRL_CUTS), params=FINAL, THR=THR,
           n_placed=len(rows), n_measured=len(ALLM), n_pitch_fallback=sum(1 for d in ALLM if d["pitch_src"] == "fallback"),
           counts=cnt, split_half_all=sh_all, split_half_test=sh_test, class_validity=cv, gate=gate, gate_pass=gate_pass,
           c_test=cT, c_control=cC, delta=delta, p_boot=p_boot, delta_boot_5=lo5, delta_boot_95=hi95,
           c_test_boot_5_95=[float(np.percentile(bsT, 5)), float(np.percentile(bsT, 95))],
           median_before_after_test=[float(np.median(bT)), float(np.median(aT))],
           median_before_after_control=[float(np.median(bC)), float(np.median(aC))],
           mannwhitney_test_after_gt_before_p=float(mw.pvalue), mannwhitney_control_after_gt_before_p=float(mwC.pvalue),
           verdict=verdict, label=label, secondary=sec, paired=paired_res, a2_sha256=a2,
           class_medians_sha256=hashlib.sha256(open("../out/class_medians.json", "rb").read()).hexdigest(),
           runtime_s=round(time.time() - t0, 1))
json.dump(res, open(f"{OUTD}/results.json", "w"), indent=1, default=float, ensure_ascii=False)
keys = ["uid", "col_roman", "cut", "l", "ref", "word_index", "char_index", "letter", "x88", "y88", "lh88", "n_lights",
        "lights", "pitch", "pitch_src", "acpk", "ext_ALL", "ext_T", "ext_B", "h_ALL", "h_T", "h_B", "h_rel_cu", "hp_dr", "h_rel_dr"]
with open(f"{OUTD}/letters_measured.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
    for d in meas:
        w.writerow({k: (round(d[k], 4) if isinstance(d[k], float) else d[k]) for k in keys})
print(json.dumps({k: v for k, v in res.items() if k not in ("params", "a2_sha256", "secondary", "paired")}, indent=1, default=float, ensure_ascii=False))
print(json.dumps(sec, indent=1, default=float))
print(json.dumps(paired_res, indent=1, default=float))
