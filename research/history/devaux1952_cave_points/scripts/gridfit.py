"""Detect the 1-km grid lines on pl. XX (two halves), fit lines, intersect, fit affine.

Usage: python3 -I gridfit.py <workdir>
Writes <workdir>/grid_intersections.json
"""
import sys, json, os
import numpy as np
from PIL import Image

W = sys.argv[1]

HALVES = {
    'north': dict(img='img_p23-001.jpg',
                  vx={192: 208, 193: 804, 194: 1404},
                  hy={131: 525, 130: 1117, 129: 1715, 128: 2310}),
    'south': dict(img='img_p24-001.jpg',
                  vx={192: 210, 193: 805, 194: 1401},
                  hy={127: 728, 126: 1321, 125: 1912, 124: 2503}),
}
THR = 120  # dark threshold (paper ~190, ink ~60)


def trace(a, nominal, axis, span, half=14, step=4):
    """Return list of (t, c): along-line coordinate t, across-line centroid c of the
    dark run nearest the nominal position, rejecting runs wider than 9 px."""
    pts = []
    for t in range(span[0], span[1], step):
        if axis == 'v':
            prof = a[t, nominal - half:nominal + half + 1]
        else:
            prof = a[nominal - half:nominal + half + 1, t]
        dark = prof < THR
        if not dark.any():
            continue
        # find runs
        idx = np.where(dark)[0]
        runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
        best = None
        for r in runs:
            if len(r) > 9 or len(r) < 2:
                continue
            w = (255 - prof[r]).astype(float)
            c = (r * w).sum() / w.sum()
            if best is None or abs(c - half) < abs(best - half):
                best = c
        if best is not None:
            pts.append((t, nominal - half + best))
    return np.array(pts)


def robust_line(pts, iters=5, k=2.5):
    t, c = pts[:, 0], pts[:, 1]
    m = np.ones(len(t), bool)
    for _ in range(iters):
        A = np.vstack([np.ones(m.sum()), t[m]]).T
        coef, *_ = np.linalg.lstsq(A, c[m], rcond=None)
        r = c - (coef[0] + coef[1] * t)
        s = 1.4826 * np.median(np.abs(r[m])) + 0.3
        m = np.abs(r) < k * s
    A = np.vstack([np.ones(m.sum()), t[m]]).T
    coef, *_ = np.linalg.lstsq(A, c[m], rcond=None)
    r = c[m] - (coef[0] + coef[1] * t[m])
    return coef, m.sum(), len(t), float(np.sqrt(np.mean(r ** 2)))


out = {}
for name, H in HALVES.items():
    a = np.asarray(Image.open(os.path.join(W, H['img'])).convert('L')).astype(float)
    h, w = a.shape
    ys = sorted(H['hy'].values()); xs = sorted(H['vx'].values())
    vlines, hlines = {}, {}
    for E, x0 in H['vx'].items():
        pts = trace(a, x0, 'v', (min(ys) - 40, max(ys) + 40))
        coef, nin, ntot, rms = robust_line(pts)
        vlines[E] = dict(a=float(coef[0]), b=float(coef[1]), n_in=int(nin), n=int(ntot), rms_px=rms,
                         t_range=[int(pts[:, 0].min()), int(pts[:, 0].max())])
    for N, y0 in H['hy'].items():
        pts = trace(a, y0, 'h', (min(xs) - 40, max(xs) + 40))
        coef, nin, ntot, rms = robust_line(pts)
        hlines[N] = dict(a=float(coef[0]), b=float(coef[1]), n_in=int(nin), n=int(ntot), rms_px=rms,
                         t_range=[int(pts[:, 0].min()), int(pts[:, 0].max())])
    # intersections: vertical x = av + bv*y ; horizontal y = ah + bh*x
    inter = []
    for E, v in vlines.items():
        for N, hh in hlines.items():
            # solve x = av + bv*y, y = ah + bh*x
            y = (hh['a'] + hh['b'] * v['a']) / (1 - hh['b'] * v['b'])
            x = v['a'] + v['b'] * y
            inter.append(dict(E=E, N=N, x=x, y=y))
    out[name] = dict(vlines=vlines, hlines=hlines, intersections=inter)
    print(name)
    for E, v in vlines.items():
        print(f"  V E{E}: x = {v['a']:.2f} + {v['b']:.5f}*y  in {v['n_in']}/{v['n']} rms {v['rms_px']:.2f}px tilt {np.degrees(np.arctan(v['b'])):.3f} deg")
    for N, v in hlines.items():
        print(f"  H N{N}: y = {v['a']:.2f} + {v['b']:.5f}*x  in {v['n_in']}/{v['n']} rms {v['rms_px']:.2f}px tilt {np.degrees(np.arctan(v['b'])):.3f} deg")

json.dump(out, open(os.path.join(W, 'grid_intersections.json'), 'w'), indent=1)
