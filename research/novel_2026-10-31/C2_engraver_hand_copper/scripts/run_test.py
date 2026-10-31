"""C2 confirmatory run (frozen; see ../PROTOCOL_FROZEN.md). Run once:  python3 -I run_test.py

Test cuts 7 and 8 (column III) and control cuts 10 and 16, six standard recto frames each
(RLT RCT RRT RLB RCB RRB), read at 0.5 of full resolution through hexview.py. Numbers only are
written to ../out/. Image products (overlays) go to SP/products/C2/.
"""
import sys, os, json, csv, time
import numpy as np, cv2
from scipy.stats import mannwhitneyu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copper as C, fetch

# ---------------- frozen parameters ----------------
SCALE = 0.5
TEST_CUTS = [7, 8]          # column III (Puech 2006 pls. CCCXXXVII 8G 8D, CCCXXXVIII 7G 7C)
CONTROL_CUTS = [10, 16]     # column IV (+ start of V) and column IX
LIGHTS = ['RLT', 'RCT', 'RRT', 'RLB', 'RCB', 'RRB']
R_BEFORE = (0.0, 0.45)      # strip-position range of 'before' bands (III 1-6 equivalent)
R_AFTER = (0.55, 1.0)       # strip-position range of 'after' bands (III 8-13 equivalent)
Q = (0.15, 0.85)            # inter-quantile range for the letter extent
INNER = 0.6                 # inner fraction of the strip width analysed
MIN_ACF = 0.10              # frame accepted if pitch acf >= MIN_ACF and >= 3 bands in each region
MIN_FRAMES = 4              # per cut
GATE_SD = 0.25              # pooled within-cut robust SD of frame contrasts must be <= GATE_SD
THR = 0.086                 # half the drawing's within-column III relative effect (+0.172)
N_BOOT = 10000
SEED = 20261031
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
os.makedirs(OUT, exist_ok=True)


def med_region(bands, key, lo, hi):
    v = [b[key] for b in bands if lo <= b['r'] <= hi and np.isfinite(b.get(key, np.nan))]
    return float(np.median(v)) if v else np.nan


def rel(a, b):
    return (a - b) / b if np.isfinite(a) and np.isfinite(b) and b != 0 else np.nan


def overlay(a, m, path):
    g = C.gray(a); vis = (np.dstack([g] * 3) * 255).astype(np.uint8).copy()
    x0, x1, y0, y1 = m['win']
    for b in m['bands']:
        col = (0, 200, 0) if b['r'] <= R_BEFORE[1] else ((255, 0, 0) if b['r'] >= R_AFTER[0] else (200, 200, 0))
        cv2.line(vis, (x0, b['y_ext0']), (x1, b['y_ext0']), col, 1)
        cv2.line(vis, (x0, b['y_ext1']), (x1, b['y_ext1']), col, 1)
    cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 0, 255), 1)
    cv2.imwrite(path, vis[:, max(0, x0 - 40):x1 + 40, ::-1])


def main():
    t0 = time.time()
    px = C.PX_PER_CM_FULL * SCALE
    frames, bands_rows = [], []
    for group, cuts in (('test', TEST_CUTS), ('control', CONTROL_CUTS)):
        for cut in cuts:
            fr = C.load_cut(cut, SCALE, f'CONFIRMATORY run C2 ({group})', lights=LIGHTS)
            for L in LIGHTS:
                if L not in fr:
                    frames.append(dict(group=group, cut=cut, light=L, accepted=0, why='frame absent')); continue
                a = fr[L]
                rp, racf = C.ruler_px_per_cm(a, px)
                m = C.measure_frame(a, px, inner=INNER, q=Q)
                row = dict(group=group, cut=cut, light=L, ruler_px_per_cm_fullres=rp / SCALE if np.isfinite(rp) else np.nan,
                           ruler_acf=racf)
                if m is None or m['pitch_px'] is None:
                    row.update(accepted=0, why='no strip or no pitch'); frames.append(row); continue
                bl = m['bands']
                nB = sum(1 for b in bl if R_BEFORE[0] <= b['r'] <= R_BEFORE[1])
                nA = sum(1 for b in bl if R_AFTER[0] <= b['r'] <= R_AFTER[1])
                hB, _ = C.region_h(m, *R_BEFORE, q=Q); hA, _ = C.region_h(m, *R_AFTER, q=Q)
                ok = m['acf'] >= MIN_ACF and nB >= 3 and nA >= 3
                row.update(accepted=int(ok), why='' if ok else 'acf or band count', pitch_cm=m['pitch_px'] / px,
                           acf=m['acf'], n_bands=len(bl), n_before=nB, n_after=nA,
                           strip_h_cm=(m['y1'] - m['y0']) / px,
                           h_before=hB, h_after=hA, c_h=rel(hA, hB))
                for key in ('ploc_px', 'asp', 'gapr', 'wgapr', 'fill'):
                    b_ = med_region(bl, key, *R_BEFORE); a_ = med_region(bl, key, *R_AFTER)
                    row[f'{key}_before'] = b_; row[f'{key}_after'] = a_; row[f'c_{key}'] = rel(a_, b_)
                frames.append(row)
                for i, b in enumerate(bl):
                    bands_rows.append(dict(group=group, cut=cut, light=L, band=i, r=round(b['r'], 4),
                                           region='before' if b['r'] <= R_BEFORE[1] else ('after' if b['r'] >= R_AFTER[0] else 'boundary'),
                                           h=b['h'], hloc=b['hloc'], ext_cm=b['ext_px'] / px,
                                           ploc_cm=b['ploc_px'] / px if np.isfinite(b['ploc_px']) else np.nan,
                                           asp=b['asp'], gapr=b['gapr'], wgapr=b['wgapr'], fill=b['fill'], prom=b['prom']))
                overlay(a, m, os.path.join(fetch.PROD, f'confirm_cut{cut}_{L}_overlay.jpg'))
            print(group, cut, 'done', round(time.time() - t0), 's', flush=True)

    # ---------------- outputs ----------------
    keys = sorted({k for r in frames for k in r}, key=lambda k: (k not in ('group', 'cut', 'light', 'accepted', 'why'), k))
    with open(os.path.join(OUT, 'copper_frames.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(frames)
    bkeys = list(bands_rows[0].keys()) if bands_rows else []
    with open(os.path.join(OUT, 'copper_bands.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=bkeys); w.writeheader(); w.writerows(bands_rows)

    acc = [r for r in frames if r.get('accepted') == 1 and np.isfinite(r.get('c_h', np.nan))]
    per_cut = {}
    for cut in TEST_CUTS + CONTROL_CUTS:
        cs = [r['c_h'] for r in acc if r['cut'] == cut]
        per_cut[cut] = dict(n_frames=len(cs), median_c_h=float(np.median(cs)) if cs else None,
                            robust_sd=float(1.4826 * np.median(np.abs(np.array(cs) - np.median(cs)))) if len(cs) >= 2 else None)
    # gate
    g1 = all(per_cut[c]['n_frames'] >= MIN_FRAMES for c in per_cut)
    dev = []
    for cut in per_cut:
        cs = np.array([r['c_h'] for r in acc if r['cut'] == cut])
        if len(cs) >= 2:
            dev += list(np.abs(cs - np.median(cs)))
    pooled_sd = float(1.4826 * np.median(dev)) if dev else np.nan
    g2 = bool(np.isfinite(pooled_sd) and pooled_sd <= GATE_SD)
    T = np.array([r['c_h'] for r in acc if r['group'] == 'test'])
    K = np.array([r['c_h'] for r in acc if r['group'] == 'control'])
    res = dict(parameters=dict(SCALE=SCALE, TEST_CUTS=TEST_CUTS, CONTROL_CUTS=CONTROL_CUTS, LIGHTS=LIGHTS,
                               R_BEFORE=R_BEFORE, R_AFTER=R_AFTER, Q=Q, INNER=INNER, MIN_ACF=MIN_ACF,
                               MIN_FRAMES=MIN_FRAMES, GATE_SD=GATE_SD, THR=THR, N_BOOT=N_BOOT, SEED=SEED),
               per_cut=per_cut, gate=dict(G1_min_frames=g1, pooled_within_cut_robust_sd=pooled_sd, G2_sd_ok=g2,
                                          passed=bool(g1 and g2)))
    if len(T) and len(K):
        D_T, D_K = float(np.median(T)), float(np.median(K))
        p = float(mannwhitneyu(T, K, alternative='greater').pvalue)
        rng = np.random.default_rng(SEED)
        boots = np.array([np.median(rng.choice(T, len(T))) - np.median(rng.choice(K, len(K))) for _ in range(N_BOOT)])
        lo95, hi95 = float(np.percentile(boots, 5)), float(np.percentile(boots, 95))
        res['primary'] = dict(D_test=D_T, D_control=D_K, diff=D_T - D_K, mwu_p_greater=p,
                              boot_diff_one_sided_95=[lo95, hi95], n_test=len(T), n_control=len(K))
        if not res['gate']['passed']:
            verdict = 'not identifiable from available evidence (measurement gate failed)'
            label = 'not obtained'
        elif D_T >= THR and (D_T - D_K) >= THR and p < 0.05:
            verdict = 'supported relative to the registered alternatives'
            label = 'obtained'
        elif hi95 < THR:
            verdict = 'rejected (copper excludes a III-specific rise of half the drawing effect)'
            label = 'not obtained'
        else:
            verdict = 'not identifiable from available evidence (gate passed, effect unresolved)'
            label = 'partly'
        res['verdict'] = verdict; res['label'] = label
    else:
        res['verdict'] = 'not identifiable from available evidence (no accepted frames)'; res['label'] = 'not obtained'
    # secondary features (reported only)
    sec = {}
    for key in ('c_ploc_px', 'c_asp', 'c_gapr', 'c_wgapr', 'c_fill'):
        t = [r[key] for r in acc if r['group'] == 'test' and np.isfinite(r.get(key, np.nan))]
        k = [r[key] for r in acc if r['group'] == 'control' and np.isfinite(r.get(key, np.nan))]
        sec[key] = dict(median_test=float(np.median(t)) if t else None, median_control=float(np.median(k)) if k else None,
                        n_test=len(t), n_control=len(k),
                        mwu_p_two_sided=float(mannwhitneyu(t, k).pvalue) if len(t) >= 3 and len(k) >= 3 else None)
    res['secondary'] = sec
    res['runtime_s'] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(OUT, 'results.json'), 'w'), indent=1, default=float)
    print(json.dumps({k: res[k] for k in ('per_cut', 'gate', 'primary', 'verdict', 'label') if k in res}, indent=1, default=float))


if __name__ == '__main__':
    main()
