"""A2 registration of all frames of one cut to a reference frame, without using the shading sign.

Method (exploratory design, 31 Oct 2026):
1. Strip mask at 1/8 scale from colour (copper patina: hue 55-105 on OpenCV's 0-180 scale, saturation 12-110,
   value > 35), largest component. The charts and ruler move between frames, so only the strip is used.
2. Coarse pose: mask moments (centroid, principal axis); both 0 and 180 degree flips are tried.
3. ECC (affine) on the Gaussian-blurred strip mask at 1/8 scale (outline only: independent of shading).
4. ECC (affine) on the gradient magnitude of the luminance at 1/2 scale, inside the eroded strip mask.
   Gradient magnitude does not change sign when the light moves from top to bottom.
5. Residual check, independent of step 4's objective: phase correlation of Sobel gradient magnitude
   (sigma 2 px) between the warped frame and the reference in 256 x 256 full-res patches on a grid
   inside the strip; the residual is the median and 90th percentile patch shift (full-res px).
Outputs: affine matrices (frame full-res px -> reference full-res px) in a JSON, numbers only.
"""
import sys, json, time
import numpy as np, cv2
from common import overview_cached, full_cached, frames_for_cut, CACHE, HERE

S0 = 0.125


def strip_mask(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    m = ((h >= 55) & (h <= 105) & (s >= 12) & (s <= 110) & (v > 35)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2:
        return m
    # largest component that is tall
    best = max(range(1, n), key=lambda i: st[i, cv2.CC_STAT_AREA] * (st[i, cv2.CC_STAT_HEIGHT] > 0.4 * m.shape[0]))
    m = (lab == best).astype(np.uint8)
    # fill holes
    ff = m.copy()
    cv2.floodFill(ff, np.zeros((m.shape[0] + 2, m.shape[1] + 2), np.uint8), (0, 0), 1)
    holes = (ff == 0)
    m[holes] = 1
    return m


def moments_pose(m):
    ys, xs = np.nonzero(m)
    c = np.array([xs.mean(), ys.mean()])
    cov = np.cov(np.vstack([xs - c[0], ys - c[1]]))
    w, V = np.linalg.eigh(cov)
    ax = V[:, np.argmax(w)]
    if ax[1] < 0:
        ax = -ax
    return c, np.arctan2(ax[1], ax[0])


def to3(A):
    return np.vstack([A, [0, 0, 1]])


def ecc(tmpl, img, A, mask=None, iters=200, eps=1e-6):
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, iters, eps)
    A = np.ascontiguousarray(A, dtype=np.float32)
    cc, A = cv2.findTransformECC(np.ascontiguousarray(tmpl, np.float32), np.ascontiguousarray(img, np.float32), A, cv2.MOTION_AFFINE, crit,
                                 mask, 5)
    return cc, A


def gradmag(g, sigma):
    g = cv2.GaussianBlur(g.astype(np.float32), (0, 0), sigma)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    return np.sqrt(gx * gx + gy * gy)


def sift_affine(cut, La, Lb, ma_full, mb_full, lev=0.5, nfeat=20000):
    """Within-group registration (same top/bottom side): SIFT + RANSAC affine. Returns A mapping La full-res -> Lb full-res,
    number of inliers and the median inlier residual in full-res px."""
    ga = cv2.resize(np.asarray(full_cached(cut, La)), None, fx=lev, fy=lev, interpolation=cv2.INTER_AREA)
    gb = cv2.resize(np.asarray(full_cached(cut, Lb)), None, fx=lev, fy=lev, interpolation=cv2.INTER_AREA)
    cl = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    ga, gb = cl.apply(ga), cl.apply(gb)
    ma = cv2.resize(ma_full, (ga.shape[1], ga.shape[0]), interpolation=cv2.INTER_NEAREST)
    mb = cv2.resize(mb_full, (gb.shape[1], gb.shape[0]), interpolation=cv2.INTER_NEAREST)
    sift = cv2.SIFT_create(nfeatures=nfeat)
    ka, da = sift.detectAndCompute(ga, ma)
    kb, db = sift.detectAndCompute(gb, mb)
    if da is None or db is None or len(ka) < 10 or len(kb) < 10:
        return None, 0, float("nan")
    bf = cv2.BFMatcher(cv2.NORM_L2)
    mt = bf.knnMatch(da, db, k=2)
    good = [m for m, n in (p for p in mt if len(p) == 2) if m.distance < 0.8 * n.distance]
    if len(good) < 6:
        return None, len(good), float("nan")
    pa = np.float32([ka[m.queryIdx].pt for m in good]) / lev
    pb = np.float32([kb[m.trainIdx].pt for m in good]) / lev
    A, inl = cv2.estimateAffine2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=6.0, maxIters=5000, confidence=0.999)
    if A is None:
        return None, 0, float("nan")
    inl = inl.ravel().astype(bool)
    pr = (A[:, :2] @ pa[inl].T).T + A[:, 2]
    res = np.hypot(*(pr - pb[inl]).T)
    return A, int(inl.sum()), float(np.median(res))


def compose(A_bc, A_ab):
    """A_ab maps a->b, A_bc maps b->c; return a->c."""
    return (to3(np.asarray(A_bc)) @ to3(np.asarray(A_ab)))[:2]


def cross_register(cut, ref, L, masks, gref_full, mref_full):
    """Register frame L to ref without the shading sign: strip-outline ECC at 1/8, then gradient-magnitude ECC
    at 1/4 and 1/2. Returns (A ref->L full-res, flip, ecc_mask, ecc_grad)."""
    cr, ar = moments_pose(masks[ref])
    tm = cv2.GaussianBlur(masks[ref].astype(np.float32), (0, 0), 2.0)
    c, a = moments_pose(masks[L])
    im = cv2.GaussianBlur(masks[L].astype(np.float32), (0, 0), 2.0)
    best = None
    for flip in (0, 1):
        ang = ar - a + (np.pi if flip else 0.0)
        R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        Rinv = R.T
        t = c - Rinv @ cr
        A0 = np.hstack([Rinv, t[:, None]])
        try:
            cc, A = ecc(tm, im, A0, iters=300)
        except cv2.error:
            continue
        if best is None or cc > best[0]:
            best = (cc, A, flip)
    cc_m, A8, flip = best
    gL = np.asarray(full_cached(cut, L)).astype(np.float32)
    mL_full = cv2.resize(masks[L], (gL.shape[1], gL.shape[0]), interpolation=cv2.INTER_NEAREST)
    A = A8.astype(float).copy()
    cur = S0
    cc_g = float("nan")
    for lev in (0.25, 0.5):
        A[:, 2] *= lev / cur
        cur = lev
        Gr = gradmag(cv2.resize(gref_full, None, fx=lev, fy=lev, interpolation=cv2.INTER_AREA), 2.0)
        mr = cv2.resize(mref_full, (Gr.shape[1], Gr.shape[0]), interpolation=cv2.INTER_NEAREST)
        Gr /= (np.percentile(Gr[mr > 0], 99) + 1e-6)
        Gl = gradmag(cv2.resize(gL, None, fx=lev, fy=lev, interpolation=cv2.INTER_AREA), 2.0)
        ml = cv2.resize(mL_full, (Gl.shape[1], Gl.shape[0]), interpolation=cv2.INTER_NEAREST)
        Gl /= (np.percentile(Gl[ml > 0], 99) + 1e-6)
        ml = cv2.erode(ml, np.ones((int(80 * lev) | 1, int(80 * lev) | 1), np.uint8))
        try:
            cc_g, A2 = ecc(np.clip(Gr, 0, 1.5), np.clip(Gl, 0, 1.5), A, mask=ml, iters=200)
            A = A2.astype(float)
        except cv2.error as e:
            print("ECC-grad failed", L, lev, str(e)[:120])
    A[:, 2] /= cur
    return A, int(flip), float(cc_m), float(cc_g)


def side_of(L):
    if L in ("RLT", "RCT", "RRT", "RT", "RET", "RTC"):
        return "T"
    if L in ("RLB", "RCB", "RRB", "RB", "REB", "RBC"):
        return "B"
    return "O"


def register_cut(cut, ref=None, verbose=True):
    """Top group: SIFT to the top-centre reference. Bottom group: the bottom-centre frame is registered to the
    reference by cross_register (sign-free); the other bottom frames by SIFT to the bottom-centre frame.
    Frames of other light codes: cross_register to the reference."""
    frames = frames_for_cut(cut)
    if ref is None:
        ref = next(L for L in ("RCT", "RT", "RTC", "RET", "RLT", "RRT") if L in frames)
    pref_b = {"RLT": ("RLB",), "RRT": ("RRB",)}.get(ref, ("RCB", "RB", "RBC", "REB"))
    banc = next((L for L in pref_b if L in frames), None)
    ov = {L: overview_cached(cut, L, S0) for L in frames}
    masks = {L: strip_mask(ov[L]) for L in frames}
    gref_full = np.asarray(full_cached(cut, ref)).astype(np.float32)
    H, W = gref_full.shape
    mfull = {}
    for L in frames:
        g = full_cached(cut, L)
        mfull[L] = cv2.dilate(cv2.resize(masks[L], (g.shape[1], g.shape[0]), interpolation=cv2.INTER_NEAREST),
                              np.ones((41, 41), np.uint8))
    mref_full = cv2.resize(masks[ref], (W, H), interpolation=cv2.INTER_NEAREST)
    out = {"cut": cut, "ref": ref, "bottom_anchor": banc, "frames": {}}
    out["frames"][ref] = {"method": "reference", "A_ref2frame": [[1, 0, 0], [0, 1, 0]]}
    A_banc = None
    if banc:
        t0 = time.time()
        A_banc, flip, ccm, ccg = cross_register(cut, ref, banc, masks, gref_full, mref_full)
        out["frames"][banc] = {"method": "sign-free cross-group: outline ECC + gradient-magnitude ECC",
                               "flip": flip, "ecc_mask": ccm, "ecc_grad": ccg, "A_ref2frame": A_banc.tolist(),
                               "sec": round(time.time() - t0, 1)}
    for L in frames:
        if L in out["frames"]:
            continue
        t0 = time.time()
        sd = side_of(L)
        if sd == "T" or (sd == "B" and banc):
            parent = ref if sd == "T" else banc
            A_pl, n, r = sift_affine(cut, parent, L, mfull[parent], mfull[L])
            if A_pl is not None and n >= 30:
                A = A_pl if parent == ref else compose(A_pl, A_banc)
                out["frames"][L] = {"method": f"SIFT+RANSAC affine to {parent} (same side)", "sift_inliers": n,
                                    "sift_median_resid_px": r, "A_ref2frame": np.asarray(A).tolist(),
                                    "sec": round(time.time() - t0, 1)}
                continue
        A, flip, ccm, ccg = cross_register(cut, ref, L, masks, gref_full, mref_full)
        out["frames"][L] = {"method": "sign-free cross-group: outline ECC + gradient-magnitude ECC", "flip": flip,
                            "ecc_mask": ccm, "ecc_grad": ccg, "A_ref2frame": A.tolist(), "sec": round(time.time() - t0, 1)}
    if verbose:
        for L, r in out["frames"].items():
            print(cut, L, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items() if k != "A_ref2frame"},
                  flush=True)
    out["mask_ref_bbox"] = [int(v) for v in cv2.boundingRect(mref_full)]
    return out


def warp_to_ref(cut, L, A_ref2frame, shape):
    g = np.asarray(full_cached(cut, L)).astype(np.float32)
    return cv2.warpAffine(g, np.asarray(A_ref2frame, np.float32), (shape[1], shape[0]),
                          flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)


def residuals(cut, reg, patch=256, stride=384):
    ref = reg["ref"]
    gref = np.asarray(full_cached(cut, ref)).astype(np.float32)
    H, W = gref.shape
    x, y, w, h = reg["mask_ref_bbox"]
    Gr = gradmag(gref, 2.0)
    win = cv2.createHanningWindow((patch, patch), cv2.CV_32F)
    res = {}
    ov = overview_cached(cut, ref, S0)
    m = cv2.resize(strip_mask(ov), (W, H), interpolation=cv2.INTER_NEAREST)
    m = cv2.erode(m, np.ones((61, 61), np.uint8))
    for L, rec in reg["frames"].items():
        if L == ref or not rec["method"].startswith("sign-free"):
            continue
        gw = warp_to_ref(cut, L, rec["A_ref2frame"], (H, W))
        Gw = gradmag(gw, 2.0)
        sh = []
        for yy in range(y, y + h - patch, stride):
            for xx in range(x, x + w - patch, patch // 2):
                if m[yy:yy + patch, xx:xx + patch].mean() < 0.98:
                    continue
                a = Gr[yy:yy + patch, xx:xx + patch]; b = Gw[yy:yy + patch, xx:xx + patch]
                (dx, dy), resp = cv2.phaseCorrelate(a, b, win)
                if resp > 0.05:
                    sh.append((dx, dy, resp))
        sh = np.array(sh) if sh else np.zeros((0, 3))
        mag = np.hypot(sh[:, 0], sh[:, 1]) if len(sh) else np.array([np.nan])
        res[L] = {"n_patches": int(len(sh)), "median_px": float(np.median(mag)),
                  "p90_px": float(np.percentile(mag, 90)) if len(sh) else float("nan"),
                  "median_dx": float(np.median(sh[:, 0])) if len(sh) else float("nan"),
                  "median_dy": float(np.median(sh[:, 1])) if len(sh) else float("nan")}
        print(cut, L, res[L], flush=True)
    return res


if __name__ == "__main__":
    import os
    cut = int(sys.argv[1])
    reg = register_cut(cut)
    reg["residual"] = residuals(cut, reg)
    os.makedirs(f"{HERE}/reg", exist_ok=True)
    json.dump(reg, open(f"{HERE}/reg/reg_cut{cut:02d}.json", "w"), indent=1)
