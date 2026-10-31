"""Confirmatory run (frozen in ../PROTOCOL_FROZEN.md). Run once:  python3 -I run_test.py
Writes ../out/hand_features_by_column.csv, ../out/hand_features_by_line.csv, ../out/photo_frames.csv,
../out/photo_cuts.csv, ../out/results.json and prints a summary."""
import os, sys, csv, json, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import cp, features_drawing, features_text, photo_build

SMOKE = '--smoke' in sys.argv
NPERM = 200 if SMOKE else 10000
SEED = 20261030
os.makedirs(OUT, exist_ok=True)

def wcsv(name, rows):
    if SMOKE: return
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def winsor(Z): return np.clip(Z, -3, 3)

# ---------- features ----------
lines, dcols = features_drawing.run()
tcols = features_text.run()
frames, pcuts, pcols = ([], [], [dict(col=c, p_pitch_cm=None, p_n_pitch=0, p_adv_ratio=None, p_n_ratio=0, p_cuts='') for c in range(1, 13)]) if SMOKE else photo_build.run()
cols = []
for c in range(1, 13):
    r = dict(col=c, col_roman=ROMAN[c - 1]); r.update({k: v for k, v in dcols[c - 1].items() if k != 'col'})
    r.update({k: v for k, v in tcols[c - 1].items() if k != 'col'}); r.update({k: v for k, v in pcols[c - 1].items() if k != 'col'})
    r['exposure_note'] = 'XI-XII: segments 19-23 exposed 30 Oct 2026' if c >= 11 else ''
    cols.append(r)
wcsv('hand_features_by_column.csv', cols); wcsv('hand_features_by_line.csv', lines)
if frames: wcsv('photo_frames.csv', frames); wcsv('photo_cuts.csv', pcuts)

gl = {(c, l): g for c, l, g in line_table()}
G11, G49 = gl[SEAMS['S11']], gl[SEAMS['S49']]
res = dict(seams=dict(S11=dict(col_line='II 13', global_line=G11), S49=dict(col_line='X 15', global_line=G49)))

def num(v): return np.nan if v is None else float(v)

# ---------- T1 (primary): line level, drawing features ----------
F1 = ['h_rel', 'asp_rel', 'gap', 'wgap']
def t1_test(lines_in, seed, tag):
    keep = [r for r in lines_in if r['h_rel'] is not None]
    X = np.array([[num(r[f]) for f in F1] for r in keep]); n = len(keep)
    Z = winsor(cp.zscore(X)); pen1 = (len(F1) + 1) * math.log(n)
    glob = [r['global_line'] for r in keep]; colof = [r['col'] for r in keep]
    def hit(t, gs): return not (glob[t - 1] + 1 > gs + 3 or glob[t] < gs - 3)
    def match_lines(cps): return {'S11': any(hit(t, G11) for t in cps), 'S49': any(hit(t, G49) for t in cps)}
    K1, cps1, g1, crit1 = cp.best_segmentation(Z, 6, 5, pen1)
    m1 = match_lines(cps1); nm1 = sum(m1.values())
    cset = sorted(set(colof)); blocks = [[i for i in range(n) if colof[i] == c] for c in cset]
    rng = np.random.default_rng(seed); Gb = []; Mb = []
    for _ in range(NPERM):
        order = [i for b in rng.permutation(len(blocks)) for i in blocks[b]]
        K, cps, g, _ = cp.best_segmentation(Z[order], 6, 5, pen1); Gb.append(g); Mb.append(sum(match_lines(cps).values()))
    Gb, Mb = np.array(Gb), np.array(Mb)
    rng2 = np.random.default_rng(seed + 1); Gs = []
    for _ in range(NPERM if not SMOKE else 50):
        K, cps, g, _ = cp.best_segmentation(Z[rng2.permutation(n)], 6, 5, pen1); Gs.append(g)
    Gs = np.array(Gs)
    acc11 = {t for t in range(1, n) if hit(t, G11)}; acc49 = {t for t in range(1, n) if hit(t, G49)}
    return dict(tag=tag, n_lines=n, features=F1, penalty=pen1, K=K1,
        change_points=[dict(index=int(t), last_line_old=f'{ROMAN[colof[t-1]-1]} {keep[t-1]["line"]}',
                            first_line_new=f'{ROMAN[colof[t]-1]} {keep[t]["line"]}', global_first_new=glob[t]) for t in cps1],
        gain=g1, crit=crit1, p_block=float((1 + (Gb >= g1).sum()) / (NPERM + 1)) if K1 else None,
        p_shuffle=float((1 + (Gs >= g1).sum()) / (len(Gs) + 1)) if K1 else None,
        matches=m1, n_matched=nm1,
        p_joint_block=float((1 + ((Gb >= g1) & (Mb >= nm1)).sum()) / (NPERM + 1)) if K1 and nm1 else None,
        p_placement=cp.placement_p(n, K1, 5, [acc11, acc49], nm1, 20000, seed + 2) if K1 and nm1 else None,
        segment_means=[dict(zip(F1, np.nanmean(X[a:b], 0).round(4).tolist())) for a, b in zip([0] + cps1, cps1 + [n])])
res['T1'] = t1_test(lines, SEED, 'primary, all columns')
res['T1_without_XII'] = t1_test([r for r in lines if r['col'] != 12], SEED + 5, 'sensitivity, column XII (exposed) removed')
K1, nm1 = res['T1']['K'], res['T1']['n_matched']

# ---------- T2 (secondary): column level, all three sources ----------
F2 = ['d_h_rel', 'd_asp_rel', 'd_gap', 'd_wgap', 't_final_rate', 'p_pitch_cm', 'p_adv_ratio']
def coltest(feats, tag, seed):
    Xc = np.array([[num(r[f]) for f in feats] for r in cols])
    usable = [j for j in range(len(feats)) if np.isfinite(Xc[:, j]).sum() >= 8]
    if not usable: return dict(tag=tag, skipped='fewer than 8 columns measured for every feature')
    Xc = Xc[:, usable]; fz = [feats[j] for j in usable]
    Zc = winsor(cp.zscore(Xc)); pen = (len(fz) + 1) * math.log(12)
    K, cps, g, crit = cp.best_segmentation(Zc, 3, 2, pen)
    acc = [{2, 3}, {10, 11}]   # 1-based column that starts the new segment: boundary on either side of the seam's column
    def mt(c): return {'S11': any(t + 1 in acc[0] for t in c), 'S49': any(t + 1 in acc[1] for t in c)}
    m = mt(cps); nm = sum(m.values())
    r = np.random.default_rng(seed); G = []; M = []
    for _ in range(NPERM):
        Kp, cpp, gp, _ = cp.best_segmentation(Zc[r.permutation(12)], 3, 2, pen); G.append(gp); M.append(sum(mt(cpp).values()))
    G, M = np.array(G), np.array(M)
    return dict(tag=tag, features=fz, penalty=pen, K=K, change_points_new_segment_starts=[ROMAN[t] for t in cps], gain=g, crit=crit,
        p_perm=float((1 + (G >= g).sum()) / (NPERM + 1)) if K else None, matches=m, n_matched=nm,
        p_joint=float((1 + ((G >= g) & (M >= nm)).sum()) / (NPERM + 1)) if K and nm else None,
        p_placement=cp.placement_p(12, K, 2, [{1, 2}, {9, 10}], nm, 20000, seed + 7) if K and nm else None)
res['T2_all'] = coltest(F2, 'all sources', SEED + 10)
res['T2_drawing'] = coltest(F2[:4], 'drawing only', SEED + 11)
res['T2_text'] = coltest(F2[4:5], 'transcription only', SEED + 12)
res['T2_photo'] = coltest(F2[5:], 'photographs only', SEED + 13)

# ---------- T3 (secondary): cut level, photographs ----------
if pcuts:
    kc = [r for r in pcuts if r['p_pitch_cm'] is not None and r['p_adv_ratio'] is not None]
    Xk = np.array([[r['p_pitch_cm'], r['p_adv_ratio']] for r in kc]); nk = len(kc); cutn = [r['cut'] for r in kc]
    Zk = winsor(cp.zscore(Xk)); penk = 3 * math.log(nk)
    K, cps, g, crit = cp.best_segmentation(Zk, 4, 3, penk)
    def mk(c): return {'S11': any(cutn[t] in (5, 6, 7) for t in c), 'S49': any(cutn[t] in (17, 18, 19) for t in c)}
    m = mk(cps); nm = sum(m.values()); r = np.random.default_rng(SEED + 20); G = []; M = []
    for _ in range(NPERM):
        Kp, cpp, gp, _ = cp.best_segmentation(Zk[r.permutation(nk)], 4, 3, penk); G.append(gp); M.append(sum(mk(cpp).values()))
    G, M = np.array(G), np.array(M)
    res['T3_cuts'] = dict(n_cuts=nk, cuts=cutn, K=K, change_points_new_segment_starts_cut=[cutn[t] for t in cps], gain=g, crit=crit,
        p_perm=float((1 + (G >= g).sum()) / (NPERM + 1)) if K else None, matches=m, n_matched=nm,
        p_joint=float((1 + ((G >= g) & (M >= nm)).sum()) / (NPERM + 1)) if K and nm else None)

# ---------- verdict (frozen rule) ----------
def verdict(t):
    if not t['K'] or t['p_block'] >= 0.05: return 'not obtained: no hand change detected above the column-order null'
    if t['n_matched'] == 0: return 'not obtained: hand change detected, at neither seam'
    if t['p_joint_block'] >= 0.05: return 'partly: hand change detected; seam coincidence not above the column-order null'
    if t['n_matched'] == 2: return 'obtained: hand change detected and both seams coincide above the null'
    return 'partly: hand change detected; one seam coincides above the null'
res['verdict_T1'] = verdict(res['T1'])
res['verdict_T1_without_XII'] = verdict(res['T1_without_XII'])
if SMOKE:
    print('SMOKE OK: n_lines', res['T1']['n_lines'], 'n_cols', len(cols), 'T2 keys', list(res['T2_all'].keys())); sys.exit()
json.dump(res, open(os.path.join(OUT, 'results.json'), 'w'), indent=1, default=float, ensure_ascii=False)
print(json.dumps(res, indent=1, default=float, ensure_ascii=False))
