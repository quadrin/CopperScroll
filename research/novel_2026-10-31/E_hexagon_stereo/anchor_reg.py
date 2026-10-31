"""Anchored coarse registration of a 1/32 tile overview to a GLO-30 hillshade (code only).

Anchor: Tell es-Sultan centre (WBADB E334) at the tile pixel listed in SULTAN1.md
(by eye, +/-50 px), or any other pixel->UTM anchor. Search: metres per full-res
pixel, rotation and sun azimuth; translation within +/-1.5 km of the anchor.
Refinement: ECC affine on a 25 m grid. Output: affine A (2x3), UTM -> stored px.
"""
import json
import os
import sys

import cv2
import numpy as np

import common as C
import refgrid as R
from coarse_reg import lcn, ref

OUT = os.path.join(C.HERE, "anchor_reg.json")


def stored_to_map_affine(orient, W, H, anchor_px, anchor_utm, mpp_full, theta_deg):
    """Affine (2x3) from stored full-res px (x, y) to UTM (E, N).
    north-up px (u, v) = (W-1-x, H-1-y) for south_up; image 'up' rotated by theta from north (CCW positive)."""
    if orient == "south_up":
        F = np.array([[-1, 0, W - 1], [0, -1, H - 1]], float)
    else:
        F = np.array([[1, 0, 0], [0, 1, 0]], float)
    t = np.radians(theta_deg)
    # north-up px vector (du, dv) -> map (dE, dN): dE = s(cos t du + sin t dv), dN = s(sin t du - cos t dv)
    Rm = mpp_full * np.array([[np.cos(t), np.sin(t)], [np.sin(t), -np.cos(t)]])
    L = Rm @ F[:, :2]
    a = np.array(anchor_px, float)
    b = np.array(anchor_utm, float) - L @ a
    return np.hstack([L, b[:, None]])


def invert(Aff):
    L = Aff[:, :2]
    Li = np.linalg.inv(L)
    return np.hstack([Li, (-Li @ Aff[:, 2])[:, None]])


def warp_to_ref(ov, valid, Aff_px2utm, scale, res, region=R.REGION, pad_px=0):
    """Resample overview into the reference grid (res m). Returns image, mask, and grid window (r0, c0)."""
    # ref px (c, r) -> UTM -> stored full-res px -> overview px
    E0, N1 = region[0], region[3]
    S = np.array([[res, 0, E0], [0, -res, N1]], float)  # (c, r, 1) -> UTM
    Ainv = invert(Aff_px2utm)  # UTM -> stored px
    M = (Ainv[:, :2] @ S[:, :2]) * scale
    m0 = (Ainv[:, :2] @ S[:, 2] + Ainv[:, 2]) * scale
    Mfull = np.hstack([M, m0[:, None]])  # ref px -> overview px
    # bounding box of the overview in ref px
    H, W = ov.shape
    Minv = invert(Mfull)
    cs = np.array([[0, 0, 1], [W, 0, 1], [0, H, 1], [W, H, 1]], float)
    rc = (Minv @ cs.T).T
    c0, r0 = np.floor(rc.min(0)).astype(int) - pad_px
    c1, r1 = np.ceil(rc.max(0)).astype(int) + pad_px
    M2 = Mfull.copy()
    M2[:, 2] += M2[:, :2] @ np.array([c0, r0], float)
    out = cv2.warpAffine(ov.astype(np.float32), M2, (c1 - c0, r1 - r0), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_AREA)
    mv = cv2.warpAffine(valid.astype(np.uint8), M2, (c1 - c0, r1 - r0), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_NEAREST) > 0
    return out, mv, (r0, c0)


def score_window(img, m, r0, c0, hs_l, shift):
    h, w = img.shape
    R0, C0 = r0 - shift, c0 - shift
    if R0 < 0 or C0 < 0 or R0 + h + 2 * shift > hs_l.shape[0] or C0 + w + 2 * shift > hs_l.shape[1]:
        return -1, (0, 0)
    refw = hs_l[R0:R0 + h + 2 * shift, C0:C0 + w + 2 * shift]
    t = lcn(np.where(m, img, np.nan))
    r = cv2.matchTemplate(refw, t, cv2.TM_CCORR_NORMED, mask=m.astype(np.float32))
    _, mx, _, loc = cv2.minMaxLoc(r)
    return float(mx), (loc[0] - shift, loc[1] - shift)


def anchored(item, tile, anchor_px, anchor_utm, scale=1 / 32, res=50.0, mpps=None, thetas=None, azs=None, shift_m=1500):
    ov, valid, orient, (W, H) = C.read_overview(item, tile, scale=scale, purpose="anchored coarse registration (code only)")
    ov[ov < 5] = 0
    valid &= ov > 5
    mpps = mpps if mpps is not None else np.arange(0.80, 1.201, 0.05)
    thetas = thetas if thetas is not None else np.arange(-12, 12.1, 1.5)
    azs = azs if azs is not None else range(60, 301, 30)
    shift = int(shift_m / res)
    best = None
    for az in azs:
        hs_l = C_cache(res, az)
        for mpp in mpps:
            for th in thetas:
                Aff = stored_to_map_affine(orient, W, H, anchor_px, anchor_utm, mpp, th)
                img, m, (r0, c0) = warp_to_ref(ov, valid, Aff, scale, res)
                sc, (dc, dr) = score_window(img, m, r0, c0, hs_l, shift)
                if best is None or sc > best[0]:
                    best = (sc, az, float(mpp), float(th), dc, dr)
    sc, az, mpp, th, dc, dr = best
    Aff = stored_to_map_affine(orient, W, H, anchor_px, anchor_utm, mpp, th)
    Aff[:, 2] += np.array([dc * res, -dr * res])  # shift found in ref px (template placed at -shift offset)
    # careful: template best location loc means template origin at (C0+loc) = c0 - shift + loc => map shift = (loc-shift)
    return dict(item=item, tile=tile, orient=orient, W=W, H=H, score=sc, az=az, mpp=mpp, theta=th, shift_ref_px=[dc, dr],
                A_px2utm=Aff.tolist()), ov, valid


_hs = {}


def C_cache(res, az):
    k = (res, az)
    if k not in _hs:
        hs = ref(res, az)
        _hs[k] = lcn(hs)
    return _hs[k]


def px2utm(Aff, x, y):
    Aff = np.asarray(Aff)
    return Aff[:, :2] @ np.vstack([x, y]) + Aff[:, 2:3]


if __name__ == "__main__":
    item, tile, ax, ay, E, N = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:7])
    rec, ov, valid = anchored(item, tile, (ax, ay), (E, N))
    allr = json.load(open(OUT)) if os.path.exists(OUT) else {}
    allr[f"{item}:{tile}"] = rec
    json.dump(allr, open(OUT, "w"), indent=1)
    print(json.dumps({k: v for k, v in rec.items() if k != "A_px2utm"}))
