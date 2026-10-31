"""Local forward/aft stereo for HEXAGON (KH-9) panoramic frames without a camera model.

Steps (all in code; no manual point picking):
 1. Read forward and aft windows (frames.read_window); aft is turned 180 deg when
    stored south_up, so both are roughly north-up.
 2. SIFT tie points, robust affine aft->forward, epipolar direction = principal
    direction of the affine residuals (the along-track parallax).
 3. Rectify: rotate so the epipolar direction is x; fit the cross-epipolar (y)
    residual with a cubic polynomial and the along-epipolar (x) residual with a plane;
    warp the aft image into the rotated forward frame.
 4. Semi-global matching (OpenCV StereoSGBM) -> disparity d (pixels, along-track parallax).
 5. Geolocation + height: affine from rectified forward px to UTM 36N and
    h = a + b d + c x + e y + quadratic(x, y), fitted against GLO-30 on stable terrain.
The KH-9 optical-bar (panoramic) camera model is NOT used.
"""
import cv2
import numpy as np
from scipy import ndimage, optimize

import common as C
import refgrid as R

SIFT_N = 30000


def to_nu(a, orient):
    return a[::-1, ::-1].copy() if orient == "south_up" else a


def tie_points(f, a, ratio=0.8, max_side=3000):
    s = min(1.0, max_side / max(f.shape))
    fs = cv2.resize(f, None, fx=s, fy=s, interpolation=cv2.INTER_AREA) if s < 1 else f
    as_ = cv2.resize(a, None, fx=s, fy=s, interpolation=cv2.INTER_AREA) if s < 1 else a
    clahe = cv2.createCLAHE(2.0, (8, 8))
    sift = cv2.SIFT_create(nfeatures=SIFT_N)
    k1, d1 = sift.detectAndCompute(clahe.apply(fs), None)
    k2, d2 = sift.detectAndCompute(clahe.apply(as_), None)
    m = cv2.BFMatcher(cv2.NORM_L2).knnMatch(d1, d2, k=2)
    good = [p[0] for p in m if len(p) == 2 and p[0].distance < ratio * p[1].distance]
    pf = np.float32([k1[g.queryIdx].pt for g in good]) / s
    pa = np.float32([k2[g.trainIdx].pt for g in good]) / s
    return pf, pa


def poly_terms(x, y, deg):
    t = [np.ones_like(x)]
    for d in range(1, deg + 1):
        for i in range(d + 1):
            t.append(x ** (d - i) * y ** i)
    return np.stack(t, -1)


def poly_eval(x, y, c, deg):
    out = np.full(x.shape, c[0], np.float32)
    k = 1
    for d in range(1, deg + 1):
        for i in range(d + 1):
            out += np.float32(c[k]) * x ** (d - i) * y ** i
            k += 1
    return out


def robust_lsq(Aterm, b, iters=5, k=3.0, floor=0.5):
    w = np.ones(len(b), bool)
    for _ in range(iters):
        c, *_ = np.linalg.lstsq(Aterm[w], b[w], rcond=None)
        r = b - Aterm @ c
        s = max(1.4826 * np.median(np.abs(r[w] - np.median(r[w]))), floor)
        w = np.abs(r) < k * s
    return c, w, s


def rectify(f, a, pf, pa, ransac_px=60.0):
    """Returns rectified forward, rectified aft, and the geometry dict."""
    A, inl = cv2.estimateAffine2D(pa, pf, ransacReprojThreshold=ransac_px, maxIters=5000, confidence=0.999)
    inl = inl.ravel().astype(bool)
    pa_f = (A[:, :2] @ pa.T).T + A[:, 2]
    res = (pf - pa_f)[inl]
    res = res - np.median(res, 0)
    # principal direction of residuals
    u, s_, vt = np.linalg.svd(res - res.mean(0), full_matrices=False)
    ex = vt[0] / np.linalg.norm(vt[0])
    if abs(ex[1]) > abs(ex[0]):  # keep orientation close to image axes; the sign is irrelevant
        pass
    ang = np.degrees(np.arctan2(ex[1], ex[0]))
    H, W = f.shape
    # rotation about the window centre so that ex -> +x
    Rm = cv2.getRotationMatrix2D((W / 2, H / 2), ang, 1.0)
    # output canvas big enough
    cos, sin = abs(Rm[0, 0]), abs(Rm[0, 1])
    nW, nH = int(H * sin + W * cos), int(H * cos + W * sin)
    Rm[0, 2] += nW / 2 - W / 2
    Rm[1, 2] += nH / 2 - H / 2
    pf_r = (Rm[:, :2] @ pf[inl].T).T + Rm[:, 2]
    pa_r = (Rm[:, :2] @ pa_f[inl].T).T + Rm[:, 2]
    sc = max(nW, nH) / 2.0
    xn, yn = (pf_r[:, 0] - nW / 2) / sc, (pf_r[:, 1] - nH / 2) / sc
    dy = pf_r[:, 1] - pa_r[:, 1]
    dx = pf_r[:, 0] - pa_r[:, 0]
    cy, wy, sy = robust_lsq(poly_terms(xn, yn, 3), dy, floor=0.3)
    cx, wx, sx = robust_lsq(poly_terms(xn, yn, 1), dx, k=4.0, floor=2.0)
    good = wy
    # warp aft: for rectified px (X, Y): aft-in-forward-rotated coords = (X - plane_x, Y - poly_y)
    gy, gx = np.mgrid[0:nH, 0:nW].astype(np.float32)
    Xn, Yn = (gx - nW / 2) / sc, (gy - nH / 2) / sc
    sx_map = gx - poly_eval(Xn, Yn, cx, 1)
    sy_map = gy - poly_eval(Xn, Yn, cy, 3)
    del Xn, Yn
    # back through rotation and affine to aft original px
    Ri = cv2.invertAffineTransform(Rm)
    fx = Ri[0, 0] * sx_map + Ri[0, 1] * sy_map + Ri[0, 2]
    fy = Ri[1, 0] * sx_map + Ri[1, 1] * sy_map + Ri[1, 2]
    Ai = cv2.invertAffineTransform(A)
    ax = (Ai[0, 0] * fx + Ai[0, 1] * fy + Ai[0, 2]).astype(np.float32)
    ay = (Ai[1, 0] * fx + Ai[1, 1] * fy + Ai[1, 2]).astype(np.float32)
    a_r = cv2.remap(a, ax, ay, cv2.INTER_CUBIC, borderValue=0)
    f_r = cv2.warpAffine(f, Rm, (nW, nH), flags=cv2.INTER_CUBIC, borderValue=0)
    d_tp = dx - poly_terms(xn, yn, 1) @ cx  # tie-point disparities after plane removal
    geo = dict(A=A.tolist(), Rm=Rm.tolist(), angle_deg=float(ang), n_tp=int(len(pf)), n_inl=int(inl.sum()),
               y_resid_nmad_px=float(sy), n_y_good=int(good.sum()), d_tp_range=[float(np.percentile(d_tp[good], 0.5)),
                                                                                  float(np.percentile(d_tp[good], 99.5))],
               cx=cx.tolist(), cy=cy.tolist(), sc=float(sc), nW=nW, nH=nH)
    return f_r, a_r, geo


def sgm(f_r, a_r, dmin, dmax, block=5):
    mind = int(np.floor(dmin)) - 8
    nd = int(np.ceil((dmax - mind + 8) / 16.0)) * 16
    clahe = cv2.createCLAHE(2.0, (8, 8))
    L, Rr = clahe.apply(f_r), clahe.apply(a_r)
    sg = cv2.StereoSGBM_create(minDisparity=mind, numDisparities=nd, blockSize=block, P1=8 * block * block,
                               P2=32 * block * block, disp12MaxDiff=1, uniquenessRatio=5, speckleWindowSize=100,
                               speckleRange=2, preFilterCap=31, mode=cv2.STEREO_SGBM_MODE_SGBM)
    d = sg.compute(L, Rr).astype(np.float32) / 16.0
    bad = (d < mind) | (f_r == 0) | (a_r == 0)
    d[bad] = np.nan
    return d, dict(minDisparity=mind, numDisparities=nd, block=block)


class GloSampler:
    """GLO-30 heights (bilinear) and the stable-terrain mask on a UTM grid.
    Stable = WorldCover 2021 class 20, 30 or 60 (shrub, grass, bare/sparse) and no class
    10/40/50/80/90 (tree, crop, built-up, water, wetland) within 60 m; GLO-30 slope <= 25 deg
    (computed at 30 m); GLO-30 height >= -390 m (below that: the 1974 Dead Sea and its shore)."""

    def __init__(self, res=10.0, region=None, slope_max=25.0, zmin=-390.0, buf_m=60.0):
        from rasterio.warp import Resampling
        self.res = res
        self.region = region or R.REGION
        self.z, _ = R.grid(C.GLO, res, region=self.region)
        z30, _ = R.grid(C.GLO, 30.0, region=self.region)
        s30 = R.slope_deg(np.nan_to_num(z30, nan=0), 30.0)
        self.slope = cv2.resize(s30, (self.z.shape[1], self.z.shape[0]), interpolation=cv2.INTER_LINEAR)
        wc, _ = R.grid(C.WC, res, region=self.region, resampling=Resampling.nearest, dtype=np.uint8, nodata=0)
        self.wc = wc
        ok_cls = np.isin(wc, (20, 30, 60))
        bad = np.isin(wc, (10, 40, 50, 80, 90, 95))
        k = int(round(buf_m / res)) * 2 + 1
        bad_b = cv2.dilate(bad.astype(np.uint8), np.ones((k, k), np.uint8)) > 0
        self.stable = ok_cls & ~bad_b & (self.slope <= slope_max) & (self.z >= zmin) & np.isfinite(self.z)
        self.surface_obj = cv2.dilate(np.isin(wc, (10, 40, 50)).astype(np.uint8), np.ones((k, k), np.uint8)) > 0

    def sample(self, E, N, arr=None, order=1):
        arr = self.z if arr is None else arr
        c = (E - self.region[0]) / self.res
        r = (self.region[3] - N) / self.res
        return ndimage.map_coordinates(arr, [r, c], order=order, mode="constant", cval=np.nan)


def design(x, y, d, quad=True):
    cols = [np.ones_like(x), d, x, y]
    if quad:
        cols += [x * x, x * y, y * y]
    return np.stack(cols, -1)


def nmad(r):
    r = r[np.isfinite(r)]
    return float(1.4826 * np.median(np.abs(r - np.median(r)))) if len(r) else float("nan")
