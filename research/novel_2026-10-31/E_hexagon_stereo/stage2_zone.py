"""Stage 2: per-zone stereo elevation model at 1/2 scale (about 2 m/px), registered and
height-calibrated against GLO-30 on stable terrain (checkerboard blocks 'A'), evaluated
on held-out stable blocks 'B'; then change detection against GLO-30.

Usage: python3 stage2_zone.py PAIR ZONE [ZONE ...]   (ZONE in TRAIN, QUMRAN, QELT, KIDRON, JERICHO_OUT)
"""
import json
import os
import sys
import time

import cv2
import numpy as np
from scipy import ndimage, optimize
from shapely.geometry import Point
from shapely.prepared import prep

import common as C
import frames as F
import stereo_local as S
import zones as Z

SCALE = float(os.environ.get("E_SCALE", "0.5"))
P = dict(  # parameters (frozen in PROTOCOL_FROZEN.md before the confirmatory run)
    scale=SCALE,         # read scale (1/2 overview, ~2 m/px)
    margin_m=800.0,      # window margin around the zone bounding box
    aft_extra_m=600.0,   # extra aft margin for parallax
    block=5,             # SGBM block size (px)
    cell_m=30.0,         # sampling cell (matches GLO-30)
    chk_m=600.0,         # checkerboard block size (m) for fit (A) / evaluation (B)
    min_valid_frac=0.5,  # a cell needs >= 50 % valid disparities
    target_nmad_m=2.5,   # frozen vertical precision target
    k_sigma=3.0, min_dh_m=5.0, min_cells=3,  # change detection
)
OUT_DIR = os.path.join(C.HERE, "results")
S1 = os.path.join(C.HERE, "stage1_geoloc.json")


def inv(M):
    M = np.asarray(M, float)
    Li = np.linalg.inv(M[:, :2])
    return np.hstack([Li, (-Li @ M[:, 2])[:, None]])


def app(M, x, y):
    M = np.asarray(M, float)
    return M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2]


def aft_mosaic_to_fwd_mosaic(s1, Wa_nu, Ha_nu):
    """Affine: aft mosaic px (stored) -> forward mosaic px, from stage 1 (at 1/8)."""
    sc = s1["scale"]
    wF, wA = s1["wF"], s1["wA"]
    A = np.array(s1["geo"]["A"])  # aft window(nu, scaled) -> fwd window(scaled)
    south = True  # aft frames are stored south_up
    # aft mosaic (X, Y) -> aft window scaled px (stored) -> north-up flip
    # stored window px: xs = (X - wA0)*sc ; north-up: xn = Wn-1-xs
    Wn, Hn = Wa_nu, Ha_nu
    M1 = np.array([[-sc, 0, Wn - 1 + wA[0] * sc], [0, -sc, Hn - 1 + wA[1] * sc]]) if south else \
        np.array([[sc, 0, -wA[0] * sc], [0, sc, -wA[1] * sc]])
    M2 = np.vstack([A, [0, 0, 1]]) @ np.vstack([M1, [0, 0, 1]])
    M3 = np.array([[1 / sc, 0, wF[0]], [0, 1 / sc, wF[1]], [0, 0, 1]]) @ M2
    return M3[:2]


def run_zone(pair, zone, tag):
    t0 = time.time()
    s1 = json.load(open(S1))[pair]
    fwd, aft = s1["fwd"], s1["aft"]
    M_fu = np.array(s1["fwd_mosaic_px_to_utm"])  # forward mosaic px -> UTM
    M_uf = inv(M_fu)
    tell, core, excl, zones, train = Z.build()
    poly = train if zone == "TRAIN" else zones[zone]
    E0, N0, E1, N1 = poly.bounds
    m = P["margin_m"]
    cs = np.array([[E0 - m, N0 - m], [E1 + m, N0 - m], [E0 - m, N1 + m], [E1 + m, N1 + m]])
    fx, fy = app(M_uf, cs[:, 0], cs[:, 1])
    wF = [int(fx.min()), int(max(0, fy.min())), int(fx.max()), int(min(25100, fy.max()))]
    # aft window: aft mosaic px -> fwd mosaic px affine, inverted
    wA1 = s1["wA"]
    Wn = int(round((wA1[2] - wA1[0]) * s1["scale"]))
    Hn = int(round((wA1[3] - wA1[1]) * s1["scale"]))
    M_af = aft_mosaic_to_fwd_mosaic(s1, Wn, Hn)
    M_fa = inv(M_af)
    ma = (m + P["aft_extra_m"]) / m
    csa = np.array([[E0 - m * ma, N0 - m * ma], [E1 + m * ma, N0 - m * ma], [E0 - m * ma, N1 + m * ma], [E1 + m * ma, N1 + m * ma]])
    gx_, gy_ = app(M_uf, csa[:, 0], csa[:, 1])
    ax_, ay_ = app(M_fa, gx_, gy_)
    wA = [int(ax_.min()), int(max(0, ay_.min())), int(ax_.max()), int(min(25100, ay_.max()))]
    sc = P["scale"]
    f = F.read_window(fwd[0], *wF, scale=sc, purpose=f"stage2 {tag} {zone}")
    a = F.read_window(aft[0], *wA, scale=sc, purpose=f"stage2 {tag} {zone}")
    a = S.to_nu(a, "south_up")
    cov = float((f > 0).mean())
    pf, pa = S.tie_points(f, a, max_side=4000)
    f_r, a_r, geo = S.rectify(f, a, pf, pa, ransac_px=80.0)
    d, sgp = S.sgm(f_r, a_r, geo["d_tp_range"][0] - 6, geo["d_tp_range"][1] + 6, block=P["block"])
    print(zone, "tp", geo["n_tp"], geo["n_inl"], "ynmad", round(geo["y_resid_nmad_px"], 2), "drange", geo["d_tp_range"],
          "valid", round(float(np.isfinite(d).mean()), 3), f"{time.time() - t0:.0f}s", flush=True)
    # 30 m cells: block median in rectified space; rectified px size ~ 1/sc * mpp
    mpp = float(np.sqrt(abs(np.linalg.det(M_fu[:, :2]))))
    bs = max(3, int(round(P["cell_m"] / (mpp / sc))))
    Hh, Ww = d.shape
    nb_y, nb_x = Hh // bs, Ww // bs
    blk = d[:nb_y * bs, :nb_x * bs].reshape(nb_y, bs, nb_x, bs).transpose(0, 2, 1, 3).reshape(nb_y, nb_x, bs * bs)
    vf = np.isfinite(blk).mean(-1)
    dmed = np.nanmedian(np.where(vf[..., None] >= P["min_valid_frac"], blk, np.nan), axis=-1)
    yy, xx = np.mgrid[0:nb_y, 0:nb_x]
    xr, yr = (xx + 0.5) * bs, (yy + 0.5) * bs
    Ri = cv2.invertAffineTransform(np.array(geo["Rm"]))
    xw = Ri[0, 0] * xr + Ri[0, 1] * yr + Ri[0, 2]
    yw = Ri[1, 0] * xr + Ri[1, 1] * yr + Ri[1, 2]
    Xm, Ym = wF[0] + xw / sc, wF[1] + yw / sc
    ok = np.isfinite(dmed)
    g = S.GloSampler(res=10.0, region=(E0 - 3000, N0 - 3000, E1 + 3000, N1 + 3000))
    pp = prep(poly)
    Xc, Yc = Xm[ok], Ym[ok]
    dv = dmed[ok]
    xn, yn = (Xc - Xc.mean()) / 2000.0, (Yc - Yc.mean()) / 2000.0
    D = S.design(xn, yn, dv, quad=True)
    E00, N00 = app(M_fu, Xc, Yc)
    cE, cN = E00.mean(), N00.mean()

    dc = dv - np.median(dv)

    def utm(p):
        # p: shift (m), rotation (deg), log scale, two shears, and the relief displacement
        # (m of horizontal shift per px of disparity, E and N): the images are not orthorectified
        tx, ty, th, ls, s1_, s2_ = p[:6]
        uE, uN = (p[6], p[7]) if len(p) > 6 else (0.0, 0.0)
        t = np.radians(th)
        u, v = E00 - cE, N00 - cN
        u2, v2 = u + s1_ * v, v + s2_ * u
        k = np.exp(ls)
        return (cE + k * (np.cos(t) * u2 - np.sin(t) * v2) + tx + uE * dc,
                cN + k * (np.sin(t) * u2 + np.cos(t) * v2) + ty + uN * dc)

    def chk(E, N):
        return ((np.floor(E / P["chk_m"]) + np.floor(N / P["chk_m"])) % 2 == 0)

    def sample(p):
        E, N = utm(p)
        h = g.sample(E, N)
        st = g.sample(E, N, g.stable.astype(np.float32), order=0) > 0.5
        return E, N, h, st

    def cost(p):
        E, N, h, st = sample(p)
        mA = np.isfinite(h) & st & chk(E, N)
        if mA.sum() < 200:
            return 1e6
        c, *_ = np.linalg.lstsq(D[mA], h[mA], rcond=None)
        return S.nmad(h[mA] - D[mA] @ c)

    best = None
    for th in (-2.0, -1.0, 0.0, 1.0, 2.0):
        for tx in np.arange(-1500, 1501, 100):
            for ty in np.arange(-1500, 1501, 100):
                c_ = cost([tx, ty, th, 0, 0, 0])
                if best is None or c_ < best[0]:
                    best = (c_, [tx, ty, th, 0, 0, 0])
    for tx in np.arange(best[1][0] - 100, best[1][0] + 101, 20):
        for ty in np.arange(best[1][1] - 100, best[1][1] + 101, 20):
            c_ = cost([tx, ty, best[1][2], 0, 0, 0])
            if c_ < best[0]:
                best = (c_, [tx, ty, best[1][2], 0, 0, 0])
    bnds = [(best[1][0] - 100, best[1][0] + 100), (best[1][1] - 100, best[1][1] + 100), (best[1][2] - 1.5, best[1][2] + 1.5), (-0.05, 0.05), (-0.03, 0.03), (-0.03, 0.03),
            (-4.0, 4.0), (-4.0, 4.0)]
    # relief displacement: coarse grid first
    b2 = None
    for uE in np.arange(-4, 4.01, 0.5):
        for uN in np.arange(-4, 4.01, 0.5):
            c_ = cost(best[1][:6] + [uE, uN])
            if b2 is None or c_ < b2[0]:
                b2 = (c_, best[1][:6] + [uE, uN])
    r = optimize.minimize(cost, b2[1], method="Powell", bounds=bnds, options=dict(maxiter=4000, xtol=1e-3, ftol=1e-5))
    p = r.x
    E, N, h, st = sample(p)
    inzone = np.array([pp.contains(Point(e, n)) for e, n in zip(E, N)])
    mA = np.isfinite(h) & st & chk(E, N)
    c, *_ = np.linalg.lstsq(D[mA], h[mA], rcond=None)
    hh = D @ c
    res = hh - h
    mB = np.isfinite(h) & st & ~chk(E, N) & inzone
    mB_all = np.isfinite(h) & st & ~chk(E, N)
    out = dict(pair=pair, zone=zone, tag=tag, wF=wF, wA=wA, fwd_coverage_frac=cov, mpp_full=mpp, cell_px=bs,
               n_cells=int(len(dv)), n_cells_in_zone=int(inzone.sum()), zone_cells_expected=int(round(poly.area / P["cell_m"] ** 2)),
               n_fit_A=int(mA.sum()), n_eval_B=int(mB.sum()), params=p.tolist(), coef=c.tolist(),
               m_per_disp_px=float(c[1]), nmad_B_zone=S.nmad(res[mB]), median_B_zone=float(np.nanmedian(res[mB])) if mB.any() else None,
               rmse_B_zone=float(np.sqrt(np.nanmean(res[mB] ** 2))) if mB.any() else None, nmad_A_fit=S.nmad(res[mA]),
               nmad_B_window=S.nmad(res[mB_all]), geo={k: v for k, v in geo.items() if k not in ("cx", "cy")}, sgm=sgp,
               seconds=round(time.time() - t0))
    out["pass_precision"] = bool(out["nmad_B_zone"] <= P["target_nmad_m"]) if np.isfinite(out["nmad_B_zone"]) else None
    # change detection inside the zone (all valid cells, stable or not)
    thr = max(P["k_sigma"] * out["nmad_B_zone"], P["min_dh_m"]) if np.isfinite(out["nmad_B_zone"]) else None
    grid_r = np.full(dmed.shape, np.nan, np.float32)
    grid_r[ok] = np.where(inzone, res, np.nan)
    clusters = []
    if thr is not None:
        slope = g.sample(E, N, g.slope)
        surf = g.sample(E, N, g.surface_obj.astype(np.float32), order=0) > 0.5
        sl_g = np.full(dmed.shape, np.nan, np.float32); sl_g[ok] = slope
        sf_g = np.zeros(dmed.shape, bool); sf_g[ok] = surf
        E_g = np.full(dmed.shape, np.nan); E_g[ok] = E
        N_g = np.full(dmed.shape, np.nan); N_g[ok] = N
        for sign in (-1, 1):
            cand = np.nan_to_num(sign * grid_r, nan=0) >= thr
            lab, n = ndimage.label(cand, structure=np.ones((3, 3)))
            for i in range(1, n + 1):
                mm = lab == i
                if mm.sum() < P["min_cells"]:
                    continue
                edge = mm[0].any() or mm[-1].any() or mm[:, 0].any() or mm[:, -1].any()
                cls = ("surface object in GLO-30 (WorldCover tree/crop/built-up)" if sf_g[mm].mean() >= 0.5 else
                       "steep-slope artefact likely" if np.nanmedian(sl_g[mm]) > 25 else
                       ("1974 lower than 2011-15: candidate infill / loss of a depression, cut or pool" if sign < 0 else
                        "1974 higher than 2011-15: candidate removal since 1974 (quarry, cut, erosion, new pool)"))
                clusters.append(dict(sign=sign, n_cells=int(mm.sum()), area_m2=float(mm.sum() * P["cell_m"] ** 2),
                                     dh_median_m=float(np.nanmedian(grid_r[mm])), dh_extreme_m=float(grid_r[mm][np.nanargmax(np.abs(grid_r[mm]))]),
                                     E=float(np.nanmean(E_g[mm])), N=float(np.nanmean(N_g[mm])), touches_edge=bool(edge),
                                     slope_median_deg=float(np.nanmedian(sl_g[mm])), surface_obj_frac=float(sf_g[mm].mean()), cls=cls))
    out["change_threshold_m"] = thr
    out["clusters"] = clusters
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, f"{tag}_{pair}_{zone}.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    # image products outside the repo
    pre = os.path.join(C.PROD, f"{tag}_{pair}_{zone}")
    hgrid = np.full(dmed.shape, np.nan, np.float32); hgrid[ok] = hh
    np.save(pre + "_h30.npy", hgrid)
    diag = np.stack([E, N, h, hh, dv, st.astype(float), g.sample(E, N, g.slope), inzone.astype(float), chk(E, N).astype(float)], -1)
    np.save(pre + "_cells.npy", diag)
    sl_ = diag[:, 6]
    out["nmad_B_zone_by_slope"] = {f"{a}-{b}": S.nmad(res[mB & (sl_ >= a) & (sl_ < b)]) for a, b in ((0, 5), (5, 10), (10, 15), (15, 20), (20, 25))}
    out["n_B_zone_by_slope"] = {f"{a}-{b}": int((mB & (sl_ >= a) & (sl_ < b)).sum()) for a, b in ((0, 5), (5, 10), (10, 15), (15, 20), (20, 25))}
    np.save(pre + "_resid30.npy", grid_r)
    hfull = c[0] + c[1] * d  # disparity-scaled relief at full window resolution (plane/quad terms omitted)
    v = np.nan_to_num(hfull, nan=np.nanmedian(hfull))
    gyv, gxv = np.gradient(cv2.GaussianBlur(v, (0, 0), 1.0))
    hs = np.clip(128 + 60 * (gxv - gyv) / (np.nanstd(gxv) + 1e-6), 0, 255).astype(np.uint8)
    hs[~np.isfinite(d)] = 0
    cv2.imwrite(pre + "_relief_hillshade.png", cv2.resize(hs, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))
    rv = np.clip(128 + 12 * np.nan_to_num(grid_r, nan=0), 0, 255).astype(np.uint8)
    cv2.imwrite(pre + "_resid30.png", cv2.resize(rv, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST))
    print(json.dumps({k: out[k] for k in ("zone", "fwd_coverage_frac", "n_cells_in_zone", "zone_cells_expected", "n_fit_A", "n_eval_B",
                                          "m_per_disp_px", "nmad_A_fit", "nmad_B_zone", "median_B_zone", "nmad_B_window",
                                          "pass_precision", "change_threshold_m", "seconds", "nmad_B_zone_by_slope", "n_B_zone_by_slope")}), len(clusters), "clusters", flush=True)
    return out


if __name__ == "__main__":
    pair, tag = sys.argv[1], sys.argv[2]
    for zn in sys.argv[3:]:
        run_zone(pair, zn, tag)
