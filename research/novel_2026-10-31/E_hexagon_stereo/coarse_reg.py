"""Code-only coarse registration of 1/32 overviews to a GLO-30 hillshade.

For each tile: read the 1/32 overview (protected boxes are never read), search
rotation / scale / sun azimuth / translation by normalised cross-correlation
against a 50 m hillshade, then refine an affine map by ECC on a 25 m grid.
Output: affine A (2x3) from UTM (E, N) to stored full-res pixel (x, y), the
correlation score, and the exclusion polygon's bounding box in that tile.
Nothing is displayed or saved as an image here; arrays are dropped after use.
Exclusion pixels are blanked (set to 0, valid=False) immediately after the fit.
"""
import json
import os
import sys
import time

import cv2
import numpy as np
from shapely.geometry import Polygon

import common as C
import refgrid as R
import zones as Z

OUT = os.path.join(C.HERE, "coarse_reg.json")
_cache = {}


def ref(res, az, el=45.0):
    k = (res, az, el)
    if k not in _cache:
        if ("z", res) not in _cache:
            _cache[("z", res)] = R.grid(C.GLO, res)[0]
        z = _cache[("z", res)]
        zf = np.where(np.isnan(z), np.nanmedian(z), z)
        hs = R.hillshade(zf, res, az, el)
        hs[np.isnan(z)] = np.nan
        _cache[k] = hs
    return _cache[k]


def lcn(a, sigma=4.0, valid=None):
    """Local contrast normalisation (NaN-aware)."""
    v = np.isfinite(a) if valid is None else valid & np.isfinite(a)
    x = np.where(v, a, 0).astype(np.float32)
    w = cv2.GaussianBlur(v.astype(np.float32), (0, 0), sigma) + 1e-6
    m = cv2.GaussianBlur(x, (0, 0), sigma) / w
    d = np.where(v, x - m, 0)
    sd = np.sqrt(cv2.GaussianBlur(d * d, (0, 0), sigma) / w) + 1e-3
    out = d / sd
    out[~v] = 0
    return out.astype(np.float32)


def to_north_up(a, orient):
    return a[::-1, ::-1] if orient == "south_up" else a


def search(ov, valid, orient, azs, thetas, mpp_list, res=50.0):
    """Brute-force similarity search. Returns best (score, az, theta, mpp, E_c, N_c) for the overview centre."""
    a = to_north_up(ov.astype(np.float32), orient)
    v = to_north_up(valid, orient)
    a[~v] = np.nan
    best = None
    H, W = a.shape
    for mpp in mpp_list:  # metres per overview px
        f = mpp / res
        for th in thetas:
            # rotate by th about centre and scale by f; image 'up' is north rotated by th
            M = cv2.getRotationMatrix2D((W / 2, H / 2), th, f)
            ow, oh = int(W * f * 1.5), int(H * f * 1.5)
            M[0, 2] += ow / 2 - W / 2
            M[1, 2] += oh / 2 - H / 2
            src = np.nan_to_num(a, nan=0)
            t = cv2.warpAffine(src, M, (ow, oh), flags=cv2.INTER_AREA, borderValue=0)
            t = cv2.GaussianBlur(t, (0, 0), 0.5)
            m = cv2.warpAffine(np.isfinite(a).astype(np.float32), M, (ow, oh), flags=cv2.INTER_NEAREST) > 0.5
            ys, xs = np.where(m)
            if len(ys) < 1000:
                continue
            # central inscribed crop
            cy, cx = oh // 2, ow // 2
            hh, hw = int(H * f * 0.32), int(W * f * 0.32)
            tc = t[cy - hh:cy + hh, cx - hw:cx + hw]
            mc = m[cy - hh:cy + hh, cx - hw:cx + hw]
            if mc.mean() < 0.3:
                continue
            tc = lcn(np.where(mc, tc, np.nan))
            for az in azs:
                hs = ref(res, az)
                img = _cache.get(("lcn", res, az))
                if img is None:
                    img = _cache[("lcn", res, az)] = lcn(hs)
                r = cv2.matchTemplate(img, tc.astype(np.float32), cv2.TM_CCOEFF_NORMED)
                _, mx, _, loc = cv2.minMaxLoc(r)
                if best is None or mx > best[0]:
                    # centre of crop in reference px -> UTM
                    E = R.REGION[0] + (loc[0] + tc.shape[1] / 2) * res
                    N = R.REGION[3] - (loc[1] + tc.shape[0] / 2) * res
                    best = (float(mx), az, th, mpp, E, N)
    return best


def initial_affine(best, orient, Wfull, Hfull, scale=1 / 32):
    """Affine UTM -> stored full-res px from the similarity search result."""
    _, az, th, mpp, Ec, Nc = best
    s = mpp * (1 / scale) / 1.0  # metres per full-res px * ... (mpp is per overview px)
    mfull = mpp * scale  # metres per full-res px
    t = np.radians(th)
    # north-up image coords (u right, v down), centre at (W/2, H/2): rotation th (counter-clockwise image -> map)
    # map vector d = (dE, -dN) relates to image vector by rotation of -th? cv2 rotation by +th rotates image CCW.
    # So the image vector = R(+th) applied... derive numerically below instead.
    return None


def fit_affine_ecc(ov, valid, orient, best, Wfull, Hfull, scale=1 / 32, res=25.0):
    """Refine with ECC: find affine warp from reference px (25 m grid) to stored overview px."""
    score, az, th, mpp, Ec, Nc = best
    hs = ref(res, az)
    # initial: reference px (c, r) -> UTM (E0 + c*res, N1 - r*res) -> north-up overview px -> stored overview px
    Hs, Ws = ov.shape
    t = np.radians(th)
    f = res / mpp  # overview px per reference px
    # In north-up overview coords (u, v): template was rotated by +th (CCW) to align with north.
    # cv2.getRotationMatrix2D(angle=th) maps src->dst with [[cos, sin], [-sin, cos]] * f.
    # Inverse (dst -> src): src = R^T / f ... we build: north-up overview vector = Rinv * map_px_vector * (res/mpp)
    c, s_ = np.cos(t), np.sin(t)
    Rfwd = np.array([[c, s_], [-s_, c]])  # src(nu ovw) -> dst(map-aligned), times scale
    Rinv = Rfwd.T
    # reference px of the search centre
    rc = np.array([(Ec - R.REGION[0]) / res, (R.REGION[3] - Nc) / res])
    nu_c = np.array([Ws / 2, Hs / 2])  # crop centre approximates overview centre
    A_nu = Rinv * f  # map px -> north-up overview px
    b_nu = nu_c - A_nu @ rc
    if orient == "south_up":  # stored = (W-1-u, H-1-v)
        A = -A_nu
        b = np.array([Ws - 1, Hs - 1]) - b_nu
    else:
        A, b = A_nu, b_nu
    warp = np.hstack([A, b[:, None]]).astype(np.float32)
    # region of reference covered by the tile
    corners = np.array([[0, 0], [Ws, 0], [0, Hs], [Ws, Hs]], float)
    Ainv = np.linalg.inv(A)
    rp = (Ainv @ (corners - b).T).T
    c0, r0 = np.floor(rp.min(0)).astype(int) - 10
    c1, r1 = np.ceil(rp.max(0)).astype(int) + 10
    c0, r0 = max(c0, 0), max(r0, 0)
    c1, r1 = min(c1, hs.shape[1]), min(r1, hs.shape[0])
    tmpl = hs[r0:r1, c0:c1]
    tmask = np.isfinite(tmpl).astype(np.uint8)
    tmpl = np.nan_to_num(tmpl, nan=0).astype(np.float32)
    warp[:, 2] += warp[:, :2] @ np.array([c0, r0], np.float32)
    inp = ov.astype(np.float32) / 255.0
    inp[~valid] = 0
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    try:
        cc, warp = cv2.findTransformECC(cv2.GaussianBlur(tmpl, (0, 0), 1), cv2.GaussianBlur(inp, (0, 0), 1 / f),
                                        warp, cv2.MOTION_AFFINE, crit, tmask, 5)
    except cv2.error as e:
        return None, float("nan")
    # warp: (c - c0, r - r0) -> overview px. Convert to UTM -> stored full-res px.
    A2, b2 = warp[:, :2].astype(float), warp[:, 2].astype(float)
    # ref px (c, r) = ((E-E0)/res - c0, (N1-N)/res - r0)
    S = np.array([[1 / res, 0], [0, -1 / res]])
    off = np.array([-R.REGION[0] / res - c0, R.REGION[3] / res - r0])
    A_utm = A2 @ S / scale
    b_utm = (A2 @ off + b2) / scale
    return np.hstack([A_utm, b_utm[:, None]]), float(cc)


def utm_to_px(Aff, E, N):
    return Aff[:, :2] @ np.vstack([E, N]) + Aff[:, 2:3]


def px_to_utm(Aff, x, y):
    return np.linalg.solve(Aff[:, :2], np.vstack([x, y]) - Aff[:, 2:3])


def excl_box(Aff, W, H, extra_px=1500):
    """Bounding box (stored full-res px) of the buffered exclusion polygon, plus extra margin; None if outside tile."""
    _, _, excl, _, _ = Z.build()
    xs, ys = np.array(excl.exterior.coords).T
    px = utm_to_px(Aff, xs, ys)
    x0, y0 = px.min(1) - extra_px
    x1, y1 = px.max(1) + extra_px
    if x1 < 0 or y1 < 0 or x0 > W or y0 > H:
        return None
    return [int(max(0, x0)), int(max(0, y0)), int(min(W, x1)), int(min(H, y1))]


def blank(ov, valid, Aff, scale=1 / 32):
    """Blank the buffered exclusion polygon (in overview px) in place."""
    _, _, excl, _, _ = Z.build()
    xs, ys = np.array(excl.exterior.coords).T
    px = utm_to_px(Aff, xs, ys) * scale
    poly = np.round(px.T).astype(np.int32)
    m = np.zeros(ov.shape, np.uint8)
    cv2.fillPoly(m, [poly], 1)
    m = cv2.dilate(m, np.ones((95, 95), np.uint8))  # +1500 full-res px margin at 1/32
    ov[m > 0] = 0
    valid[m > 0] = False
    return int(m.sum())


def run(items_tiles, azs, thetas, mpps, tag):
    res_all = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for item, tile in items_tiles:
        key = f"{item}:{tile}"
        t0 = time.time()
        ov, valid, orient, (W, H) = C.read_overview(item, tile)
        best = search(ov, valid, orient, azs, thetas, mpps)
        Aff, cc = fit_affine_ecc(ov, valid, orient, best, W, H) if best else (None, float("nan"))
        rec = dict(search=dict(score=best[0], az=best[1], theta=best[2], mpp=best[3], E=best[4], N=best[5]) if best else None,
                   ecc=cc, orient=orient, W=W, H=H, tag=tag)
        if Aff is not None:
            rec["A"] = Aff.tolist()
            ctr = px_to_utm(Aff, np.array([W / 2]), np.array([H / 2]))
            rec["centre_utm"] = [float(ctr[0, 0]), float(ctr[1, 0])]
            gsd = 1 / np.sqrt(abs(np.linalg.det(Aff[:, :2])))
            rec["m_per_px"] = float(gsd)
            rec["excl_box"] = excl_box(Aff, W, H)
            rec["blanked_ov_px"] = blank(ov, valid, Aff)
        del ov
        res_all[key] = rec
        json.dump(res_all, open(OUT, "w"), indent=1)
        print(key, json.dumps({k: rec[k] for k in ("search", "ecc", "centre_utm", "m_per_px", "excl_box") if k in rec}),
              f"{time.time() - t0:.0f}s", flush=True)
    return res_all


if __name__ == "__main__":
    item = sys.argv[1]
    tiles = sys.argv[2].split(",")
    azs = [float(a) for a in sys.argv[3].split(",")]
    thetas = np.arange(-20, 20.1, 2.5)
    run([(item, t) for t in tiles], azs, thetas, [22.0, 25.0, 28.0], sys.argv[4] if len(sys.argv) > 4 else "")
