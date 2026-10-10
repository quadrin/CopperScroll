"""Fit pixel -> Palestine grid (km) transforms for each half from grid intersections.

Usage: python3 -I affine.py <workdir>
Writes <workdir>/transforms.json
"""
import sys, json, os
import numpy as np

W = sys.argv[1]
g = json.load(open(os.path.join(W, 'grid_intersections.json')))


def fit(X, Y, kind):
    x, y = X[:, 0], X[:, 1]
    if kind == 'affine':
        A = np.vstack([np.ones_like(x), x, y]).T
    elif kind == 'similarity':
        # E = a + c*x - d*y ; N = b + d*x + c*y  (y down -> handle by flipping sign of y)
        n = len(x)
        A = np.zeros((2 * n, 4)); rhs = np.zeros(2 * n)
        A[:n, 0] = 1; A[:n, 2] = x; A[:n, 3] = -(-y)
        A[n:, 1] = 1; A[n:, 2] = -y; A[n:, 3] = x
        rhs[:n] = Y[:, 0]; rhs[n:] = Y[:, 1]
        p, *_ = np.linalg.lstsq(A, rhs, rcond=None)
        pred = A @ p
        res = rhs - pred
        return p, np.vstack([res[:n], res[n:]]).T
    elif kind == 'poly2':
        A = np.vstack([np.ones_like(x), x, y, x * x, x * y, y * y]).T
    pE, *_ = np.linalg.lstsq(A, Y[:, 0], rcond=None)
    pN, *_ = np.linalg.lstsq(A, Y[:, 1], rcond=None)
    res = np.vstack([Y[:, 0] - A @ pE, Y[:, 1] - A @ pN]).T
    return (pE, pN), res


OFF = 2176  # south image row 0 == north image row 2176 (pixel-identical overlap rows 2440-2735)
g['combined'] = dict(intersections=[dict(i) for i in g['north']['intersections']] +
                     [dict(i, y=i['y'] + OFF) for i in g['south']['intersections']])
out = {'south_row_offset_px': OFF}
for half, d in g.items():
    P = np.array([[i['x'], i['y']] for i in d['intersections']])
    G = np.array([[i['E'], i['N']] for i in d['intersections']], float)
    res_all = {}
    for kind in ['similarity', 'affine', 'poly2']:
        p, res = fit(P, G, kind)
        r_m = np.hypot(res[:, 0], res[:, 1]) * 1000
        res_all[kind] = dict(rms_m=float(np.sqrt(np.mean(r_m ** 2))), max_m=float(r_m.max()),
                             rms_E_m=float(np.sqrt(np.mean((res[:, 0] * 1000) ** 2))),
                             rms_N_m=float(np.sqrt(np.mean((res[:, 1] * 1000) ** 2))))
        if kind == 'affine':
            pE, pN = p
            aff = dict(E=list(map(float, pE)), N=list(map(float, pN)))
            per_pt = [dict(E=int(G[i, 0]), N=int(G[i, 1]), x=float(P[i, 0]), y=float(P[i, 1]),
                           dE_m=float(res[i, 0] * 1000), dN_m=float(res[i, 1] * 1000), d_m=float(r_m[i]))
                      for i in range(len(P))]
            # leave-one-out
            loo = []
            for i in range(len(P)):
                m = np.ones(len(P), bool); m[i] = False
                (qE, qN), _ = fit(P[m], G[m], 'affine')
                A = np.array([1, P[i, 0], P[i, 1]])
                loo.append(float(np.hypot(A @ qE - G[i, 0], A @ qN - G[i, 1]) * 1000))
            # scale and shear diagnostics
            J = np.array([[pE[1], pE[2]], [pN[1], pN[2]]])  # km per px
            sx = np.hypot(J[0, 0], J[1, 0]); sy = np.hypot(J[0, 1], J[1, 1])
            ang_x = np.degrees(np.arctan2(J[1, 0], J[0, 0]))
            ang_y = np.degrees(np.arctan2(-J[0, 1], -J[1, 1]))
            diag = dict(m_per_px_x=sx * 1000, m_per_px_y=sy * 1000, px_per_km_x=1 / sx, px_per_km_y=1 / sy,
                        rot_x_deg=float(ang_x), rot_y_deg=float(ang_y), shear_deg=float(ang_x - ang_y))
    out[half] = dict(affine=aff, residuals=per_pt, loo_m=loo, fits=res_all, diag=diag)
    print(half)
    for k, v in res_all.items():
        print(f"  {k:10s} RMS {v['rms_m']:.1f} m  max {v['max_m']:.1f} m  (E {v['rms_E_m']:.1f}, N {v['rms_N_m']:.1f})")
    print('  diag', {k: round(v, 4) for k, v in diag.items()})
    for r, l in zip(per_pt, loo):
        print(f"   E{r['E']} N{r['N']} px ({r['x']:.1f},{r['y']:.1f}) res dE {r['dE_m']:+.1f} dN {r['dN_m']:+.1f} |{r['d_m']:.1f}| m  LOO {l:.1f} m")

json.dump(out, open(os.path.join(W, 'transforms.json'), 'w'), indent=1)
