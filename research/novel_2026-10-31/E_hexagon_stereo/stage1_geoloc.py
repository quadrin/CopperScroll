"""Stage 1 (geolocation only): low-resolution (1/8) forward/aft stereo over the whole
area of the zones, registered to GLO-30 by terrain shape (disparity vs height).
Output: affine from forward-mosaic full-res px (stored orientation) to UTM 36N, per pair.
This stage tunes nothing used for precision; it only places the zone windows.
"""
import json
import os
import sys
import time

import cv2
import numpy as np
from scipy import optimize

import common as C
import frames as F
import stereo_local as S

OUT = os.path.join(C.HERE, "stage1_geoloc.json")
TELL = (731228.4, 3528755.2)
REG = (705000.0, 3495000.0, 755000.0, 3545000.0)
AREA = (714000.0, 3504000.0, 740000.0, 3536000.0)  # E0, N0, E1, N1 to cover all zones + margin


def approx_window(orient, tell_X, tell_Y, mpp=1.0):
    E0, N0, E1, N1 = AREA
    if orient == "south_up":
        X0, X1 = tell_X - (E1 - TELL[0]) / mpp, tell_X - (E0 - TELL[0]) / mpp
        Y0, Y1 = tell_Y + (N0 - TELL[1]) / mpp, tell_Y + (N1 - TELL[1]) / mpp
    else:
        X0, X1 = tell_X + (E0 - TELL[0]) / mpp, tell_X + (E1 - TELL[0]) / mpp
        Y0, Y1 = tell_Y - (N1 - TELL[1]) / mpp, tell_Y - (N0 - TELL[1]) / mpp
    return [int(X0), int(max(0, Y0)), int(X1), int(min(25100, Y1))]


def run(pair, fwd, aft, scale=1 / 8):
    t0 = time.time()
    recF = C.hv.index()["items"][C.hv.resolve(fwd[0])]
    recA = C.hv.index()["items"][C.hv.resolve(aft[0])]
    offF, offA = F.measure_offsets(fwd[0]), F.measure_offsets(aft[0])
    # tell in mosaic coords
    TXf, TYf = offF[fwd[1]][0] + fwd[2], offF[fwd[1]][1] + fwd[3]
    TXa, TYa = offA[aft[1]][0] + aft[2], offA[aft[1]][1] + aft[3]
    wF = approx_window("north_up", TXf, TYf)
    wA = approx_window(recA["stored_orientation"], TXa, TYa)
    f = F.read_window(fwd[0], *wF, scale=scale, purpose=f"stage1 geolocation {pair}")
    a = F.read_window(aft[0], *wA, scale=scale, purpose=f"stage1 geolocation {pair}")
    a = S.to_nu(a, recA["stored_orientation"])
    pf, pa = S.tie_points(f, a)
    f_r, a_r, geo = S.rectify(f, a, pf, pa, ransac_px=40.0)
    d, sgp = S.sgm(f_r, a_r, geo["d_tp_range"][0] - 10, geo["d_tp_range"][1] + 10, block=7)
    print(pair, "tie points", geo["n_tp"], geo["n_inl"], "y nmad", geo["y_resid_nmad_px"], "d range", geo["d_tp_range"],
          "valid", float(np.isfinite(d).mean()), f"{time.time() - t0:.0f}s", flush=True)
    # sample points every 4 rectified px (~32 m)
    step = 4
    dd = cv2.medianBlur(np.nan_to_num(d, nan=-9999).astype(np.float32), 5)
    yy, xx = np.mgrid[step // 2:d.shape[0]:step, step // 2:d.shape[1]:step]
    dv = dd[yy, xx]
    ok = np.isfinite(d[yy, xx]) & (dv > -9000)
    xr, yr, dv = xx[ok].astype(float), yy[ok].astype(float), dv[ok].astype(float)
    # rectified -> forward window px -> mosaic full-res px
    Ri = cv2.invertAffineTransform(np.array(geo["Rm"]))
    xw = Ri[0, 0] * xr + Ri[0, 1] * yr + Ri[0, 2]
    yw = Ri[1, 0] * xr + Ri[1, 1] * yr + Ri[1, 2]
    Xm, Ym = wF[0] + xw / scale, wF[1] + yw / scale
    g = S.GloSampler(res=10.0, region=REG)

    def to_utm(p, Xm, Ym):
        # p: tx, ty (m), theta (deg), log-scale, shear terms (2) -> applied to anchor model, forward north_up
        tx, ty, th, ls, s1, s2 = p
        mpp = np.exp(ls)
        t = np.radians(th)
        dX, dY = Xm - TXf, Ym - TYf
        u = dX + s1 * dY
        v = dY + s2 * dX
        E = TELL[0] + mpp * (np.cos(t) * u + np.sin(t) * v) + tx
        N = TELL[1] + mpp * (np.sin(t) * u - np.cos(t) * v) + ty
        return E, N

    xn, yn = (xr - xr.mean()) / 1000.0, (yr - yr.mean()) / 1000.0
    D = S.design(xn, yn, dv, quad=True)
    sub = np.random.default_rng(0).choice(len(dv), min(20000, len(dv)), replace=False)

    def cost(p, idx=sub, robust=False):
        E, N = to_utm(p, Xm[idx], Ym[idx])
        h = g.sample(E, N)
        st = g.sample(E, N, g.stable.astype(np.float32), order=0) > 0.5
        m = np.isfinite(h) & st
        if m.sum() < 500:
            return 1e6
        c, *_ = np.linalg.lstsq(D[idx][m], h[m], rcond=None)
        r = h[m] - D[idx][m] @ c
        return S.nmad(r) if robust else float(np.sqrt(np.mean(r ** 2)))

    best = None
    for th in np.arange(-6, 6.1, 1.0):
        for mpp in (0.92, 0.96, 1.0, 1.04, 1.08, 1.12):
            for tx in np.arange(-2000, 2001, 250):
                for ty in np.arange(-2000, 2001, 250):
                    p = [tx, ty, th, np.log(mpp), 0, 0]
                    c = cost(p, idx=sub[:3000])
                    if best is None or c < best[0]:
                        best = (c, p)
    print(pair, "brute force best", best, f"{time.time() - t0:.0f}s", flush=True)
    r = optimize.minimize(lambda p: cost(p, robust=True), best[1], method="Powell",
                          options=dict(maxiter=4000, xtol=1e-3, ftol=1e-4))
    p = r.x
    print(pair, "refined", p.tolist(), "nmad", r.fun, f"{time.time() - t0:.0f}s", flush=True)
    # forward mosaic px -> UTM as a 2x3 affine (exact for this parametrisation)
    E00, N00 = to_utm(p, np.array([TXf]), np.array([TYf]))
    E10, N10 = to_utm(p, np.array([TXf + 1]), np.array([TYf]))
    E01, N01 = to_utm(p, np.array([TXf]), np.array([TYf + 1]))
    L = np.array([[E10[0] - E00[0], E01[0] - E00[0]], [N10[0] - N00[0], N01[0] - N00[0]]])
    b = np.array([E00[0], N00[0]]) - L @ np.array([TXf, TYf])
    rec = dict(pair=pair, fwd=fwd, aft=aft, wF=wF, wA=wA, scale=scale, geo={k: v for k, v in geo.items() if k not in ("cx", "cy")},
               sgm=sgp, params=p.tolist(), nmad_stage1=float(r.fun), fwd_mosaic_px_to_utm=np.hstack([L, b[:, None]]).tolist(),
               n_points=int(len(dv)))
    allr = json.load(open(OUT)) if os.path.exists(OUT) else {}
    allr[pair] = rec
    json.dump(allr, open(OUT, "w"), indent=1)
    # quick-look products (outside the repo)
    np.save(os.path.join(C.PROD, f"stage1_{pair}_disp.npy"), d)
    v = np.nan_to_num(d, nan=np.nanmin(d))
    v = ((v - np.nanpercentile(d, 1)) / (np.nanpercentile(d, 99) - np.nanpercentile(d, 1)) * 255).clip(0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(C.PROD, f"stage1_{pair}_disp.png"), cv2.resize(v, None, fx=0.5, fy=0.5))
    cv2.imwrite(os.path.join(C.PROD, f"stage1_{pair}_fwd_rect.png"), cv2.resize(f_r, None, fx=0.5, fy=0.5))
    return rec


if __name__ == "__main__":
    PAIRS = {
        "JUN74": (("D3C1208-400636F014", "d", 26404, 7234), ("D3C1208-400636A015", "c", 33458, 21496)),
        "DEC74": (("D3C1209-200214F016", "b", 19406, 20648), ("D3C1209-200214A017", "f", 2876, 14810)),
    }
    for k in sys.argv[1:]:
        run(k, *PAIRS[k])
