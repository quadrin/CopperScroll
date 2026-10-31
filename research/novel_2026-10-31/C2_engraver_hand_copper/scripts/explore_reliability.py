"""EXPLORATORY reliability of per-band letter height across the six frames of a training cut.

python3 -I explore_reliability.py SCALE CUT [CUT ...]     (cuts 7 and 8 are refused)
For each cut: per frame pitch, band count; frame pairs: bands matched by strip position (|dy| <
0.3 pitch after aligning strip tops), Spearman rho of h; and the split contrast (r <= 5/12 vs
r >= 7/12) per frame with its spread across frames.
"""
import sys, os, itertools
import numpy as np
from scipy.stats import spearmanr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copper as C

scale = float(sys.argv[1]); cuts = [int(c) for c in sys.argv[2:]]
assert not set(cuts) & {7, 8}
px = C.PX_PER_CM_FULL * scale
for cut in cuts:
    fr = C.load_cut(cut, scale, f'exploratory reliability training cut {cut}')
    M = {}
    for L, a in fr.items():
        m = C.measure_frame(a, px)
        if m is None or not m['bands']:
            print(cut, L, 'no bands'); continue
        M[L] = m
        hs = np.array([b['h'] for b in m['bands']]); r = np.array([b['r'] for b in m['bands']])
        B = hs[r <= 5 / 12]; A = hs[r >= 7 / 12]
        con = (np.median(A) - np.median(B)) / np.median(B) if len(A) and len(B) else np.nan
        hB, nB = C.region_h(m, 0, 5 / 12); hA, nA = C.region_h(m, 7 / 12, 1)
        hT, nT = C.region_h(m, 0, 1)
        print(f"cut {cut} {L}: pitch {m['pitch_px'] / px:.2f} cm acf {m['acf']:.3f} nb {len(m['bands'])} "
              f"strip {(m['y1'] - m['y0']) / px:.1f} cm  h med {np.median(hs):.3f} split-contrast {con:+.3f} | "
              f"region h all {hT:.3f} upper {hB:.3f}({nB}) lower {hA:.3f}({nA}) rel {(hA - hB) / hB:+.3f}")
    rhos = []
    for L1, L2 in itertools.combinations(sorted(M), 2):
        a, b = M[L1], M[L2]
        pa = a['pitch_px']
        ya = np.array([x['y'] - a['y0'] for x in a['bands']]); yb = np.array([x['y'] - b['y0'] for x in b['bands']])
        # best global offset (strip tops may differ): search +-1 pitch
        best = None
        for off in np.arange(-pa, pa + 1, 2):
            d = np.abs(ya[:, None] - (yb[None, :] + off))
            n = (d.min(1) < 0.3 * pa).sum()
            if best is None or n > best[0]:
                best = (n, off)
        n, off = best
        d = np.abs(ya[:, None] - (yb[None, :] + off))
        ia = np.flatnonzero(d.min(1) < 0.3 * pa); ib = d[ia].argmin(1)
        ha = [a['bands'][i]['h'] for i in ia]; hb = [b['bands'][j]['h'] for j in ib]
        rho = spearmanr(ha, hb).correlation if len(ia) >= 5 else np.nan
        rhos.append(rho)
        print(f"   {L1}-{L2}: matched {len(ia)} rho_h {rho:+.2f}")
    print(f"cut {cut}: median rho_h {np.nanmedian(rhos):+.2f}")
