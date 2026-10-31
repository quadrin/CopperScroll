"""EXPLORATORY, after the confirmatory run (not part of the frozen test).

The second drawing change point, XI 7 | XI 8 (h_rel down), measured with the frozen measurement code
on cuts 19 and 20 (column XI; Puech 2006 pls. CCCLIII-CCCLIV). These frames were exposed on 30 Oct.
Column XI has 17 lines: line k centre ~ (k - 0.5)/17 of the strip, so XI 7 ~ 0.38 and XI 8 ~ 0.44.
Split: before r <= 0.38, after r >= 0.44 (no choice was tuned on these frames).
Output: ../out/exploratory_xi.json (numbers only).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copper as C
import run_test as R

CUTS = [19, 20]
RB, RA = (0.0, 0.38), (0.55 * 0 + 0.44, 1.0)
px = C.PX_PER_CM_FULL * R.SCALE
rows = []
for cut in CUTS:
    fr = C.load_cut(cut, R.SCALE, 'EXPLORATORY XI 7-8 check (exposed frames, after confirmatory run)', lights=R.LIGHTS)
    for L, a in fr.items():
        m = C.measure_frame(a, px, inner=R.INNER, q=R.Q)
        if m is None or m['pitch_px'] is None:
            rows.append(dict(cut=cut, light=L, ok=0)); continue
        nB = sum(1 for b in m['bands'] if b['r'] <= RB[1]); nA = sum(1 for b in m['bands'] if b['r'] >= RA[0])
        hB, _ = C.region_h(m, *RB, q=R.Q); hA, _ = C.region_h(m, *RA, q=R.Q)
        rows.append(dict(cut=cut, light=L, ok=int(m['acf'] >= R.MIN_ACF and nB >= 3 and nA >= 3), acf=m['acf'],
                         pitch_cm=m['pitch_px'] / px, n_bands=len(m['bands']), n_before=nB, n_after=nA,
                         h_before=hB, h_after=hA, c_h=(hA - hB) / hB if hB else np.nan))
c_all = [r['c_h'] for r in rows if np.isfinite(r.get('c_h', np.nan))]
c_acc = [r['c_h'] for r in rows if r.get('ok') == 1]
out = dict(note='exploratory; XI 19-20 exposed; drawing XI 1-7 vs 8-17 contrast given for direction',
           frames=rows, median_c_h_all=float(np.median(c_all)) if c_all else None,
           median_c_h_accepted=float(np.median(c_acc)) if c_acc else None, n_accepted=len(c_acc), n_all=len(c_all))
json.dump(out, open(os.path.join(R.OUT, 'exploratory_xi.json'), 'w'), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k != 'frames'}, indent=1, default=float))
for r in rows:
    print(r)
