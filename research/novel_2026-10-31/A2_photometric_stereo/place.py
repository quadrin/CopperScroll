"""A2 placement: register a 1988 strip (reference frame coordinates, full res) to the Puech 2006 copy photograph
of its column by image-to-image registration of the inscribed text, then map W2F copy-photo letter boxes
(controls_manifest.csv crop_box) into the 1988 frame.

This uses the photograph of the EDF copy (the same letters, photographed), not the drawn facsimile.
Steps (exploratory design, 31 Oct 2026):
1. 1988 edge image: mean over the registered lights of the Sobel gradient magnitude (sigma 2 px, full res),
   inside the strip; this is independent of the light direction and of the shading sign.
2. Copy-photo edge image: the plate itself (it renders letter outlines), contrast-normalised, plus its gradient
   magnitude; both are smoothed to the same stroke scale.
3. Global search: normalised cross-correlation of the strip's central 80% (template) over the copy photo, for
   scales 0.34-0.60 (1988 px -> copy px) and rotations -4..4 deg. The best peak and the ratio to the best peak
   more than 1 letter height away (distinctiveness) are recorded.
4. Refinement: ECC (affine) on the same edge images at the best pose.
5. Local check: for each 3 x 3 letter-height patch on a grid inside the strip, phase correlation between the
   warped copy edge image and the 1988 edge image; residual = median patch shift (1988 px).
"""
import sys, json, time
import numpy as np, cv2
from common import HERE, REPO
from ps import load_reg, stack_window, usable_lights
from copyphoto import copy_photo


def edge88(cut, reg, sigma=2.0):
    x, y, w, h = reg["mask_ref_bbox"]
    st, lights = stack_window(cut, reg, x, y, w, h)
    acc = np.zeros((h, w), np.float32); n = np.zeros((h, w), np.float32)
    for k in range(len(lights)):
        a = st[k]
        ok = np.isfinite(a)
        a = np.where(ok, a, np.nanmedian(a)).astype(np.float32)
        g = cv2.GaussianBlur(a, (0, 0), sigma)
        gm = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
        gm /= (np.percentile(gm[ok], 95) + 1e-6)
        acc += np.where(ok, gm, 0); n += ok
    E = acc / np.maximum(n, 1)
    return E, (x, y)


def prep(a, sigma):
    a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), sigma)
    a = a - cv2.GaussianBlur(a, (0, 0), 8 * sigma)
    return (a - a.mean()) / (a.std() + 1e-6)


def rot_scale(img, s, deg):
    h, w = img.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), deg, s)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * sin + w * cos), int(h * cos + w * sin)
    M[0, 2] += nw / 2 - w / 2; M[1, 2] += nh / 2 - h / 2
    out = cv2.warpAffine(img, M, (nw, nh), flags=cv2.INTER_AREA, borderValue=0)
    return out, M


def place_cut(cut, col, lh88=150.0, verbose=True):
    reg = load_reg(cut)
    E, (x0, y0) = edge88(cut, reg)
    C, page = copy_photo(col)
    C = C.astype(np.float32)
    C = (C - np.percentile(C, 1)) / (np.percentile(C, 99.5) - np.percentile(C, 1) + 1e-6)
    h, w = E.shape
    # template: central 80% in height, central 90% in width
    ty0, ty1 = int(0.1 * h), int(0.9 * h); tx0, tx1 = int(0.05 * w), int(0.95 * w)
    T = E[ty0:ty1, tx0:tx1]
    Cp = prep(C, 2.0)
    best = []
    t0 = time.time()
    for s in np.arange(0.34, 0.605, 0.02):
        for deg in range(-4, 5):
            Ts, M = rot_scale(T, s, deg)
            msk = rot_scale(np.ones_like(T), s, deg)[0] > 0.5
            if Ts.shape[0] >= Cp.shape[0] - 2 or Ts.shape[1] >= Cp.shape[1] - 2:
                continue
            Tp = prep(Ts, 2.0)
            Tp[~msk] = 0
            R = cv2.matchTemplate(Cp, Tp.astype(np.float32), cv2.TM_CCORR_NORMED, mask=msk.astype(np.float32))
            _, mx, _, loc = cv2.minMaxLoc(R)
            # second peak more than one copy letter height away
            lhc = lh88 * s
            R2 = R.copy()
            cv2.circle(R2, loc, int(lhc), -1, -1)
            mx2 = R2.max()
            best.append((mx, mx2, s, deg, loc, M))
    best.sort(key=lambda b: -b[0])
    mx, mx2, s, deg, loc, M = best[0]
    # compose: 1988 ref coords -> template coords -> rotated/scaled -> copy coords
    A1 = np.array([[1, 0, -(x0 + tx0)], [0, 1, -(y0 + ty0)], [0, 0, 1]], float)
    A2 = np.vstack([M, [0, 0, 1]])
    A3 = np.array([[1, 0, loc[0]], [0, 1, loc[1]], [0, 0, 1]], float)
    A_88to_copy = (A3 @ A2 @ A1)[:2]
    # ECC refinement in copy coordinates: warp the 1988 edge image into copy space and refine
    Ef = np.zeros_like(Cp)
    A_e2c = (A3 @ A2 @ np.array([[1, 0, -tx0], [0, 1, -ty0], [0, 0, 1]]) @ np.array([[1, 0, tx0], [0, 1, ty0], [0, 0, 1]]))[:2]
    # simpler: map E (local coords) to copy coords
    A_loc2copy = (A3 @ A2 @ np.array([[1, 0, -tx0], [0, 1, -ty0], [0, 0, 1]], float))[:2]
    Ew = cv2.warpAffine(prep(E, 2.0 / s), A_loc2copy.astype(np.float32), (Cp.shape[1], Cp.shape[0]), flags=cv2.INTER_AREA)
    mk = cv2.warpAffine(np.ones_like(E), A_loc2copy.astype(np.float32), (Cp.shape[1], Cp.shape[0])) > 0.99
    cc = float("nan")
    Aref = np.eye(2, 3, dtype=np.float32)
    try:
        crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
        cc, Aref = cv2.findTransformECC(np.ascontiguousarray(Ew, np.float32), np.ascontiguousarray(Cp, np.float32),
                                        Aref, cv2.MOTION_AFFINE, crit, None, 5)
    except cv2.error as e:
        print("ECC refine failed", str(e)[:100])
    # Aref maps Ew coords (copy space of the initial pose) -> copy coords
    A_final = (np.vstack([Aref, [0, 0, 1]]) @ np.vstack([A_88to_copy, [0, 0, 1]]))[:2]
    out = {"cut": cut, "col": col, "copy_pdf_page_A": page, "ncc_peak": float(mx), "ncc_second": float(mx2),
           "distinctiveness": float(mx / max(mx2, 1e-6)), "scale": float(s), "rot_deg": int(deg),
           "ecc_refine": float(cc), "A_88ref_to_copy": A_final.tolist(), "search_sec": round(time.time() - t0, 1),
           "top5": [[float(b[0]), float(b[2]), int(b[3]), [int(b[4][0]), int(b[4][1])]] for b in best[:5]]}
    # local residual check: phase correlation in 3 Lh patches (copy space), reported in 1988 px
    Ainv = cv2.invertAffineTransform(A_final.astype(np.float32))
    Ew2 = cv2.warpAffine(prep(E, 2.0 / s), (np.vstack([A_final, [0, 0, 1]]) @ np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]], float))[:2].astype(np.float32),
                         (Cp.shape[1], Cp.shape[0]), flags=cv2.INTER_AREA)
    mk2 = cv2.warpAffine(np.ones_like(E), (np.vstack([A_final, [0, 0, 1]]) @ np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]], float))[:2].astype(np.float32),
                         (Cp.shape[1], Cp.shape[0])) > 0.99
    P = int(3 * lh88 * s) // 2 * 2
    win = cv2.createHanningWindow((P, P), cv2.CV_32F)
    sh = []
    ys, xs = np.nonzero(mk2)
    if len(ys):
        for yy in range(ys.min(), ys.max() - P, P // 2):
            for xx in range(xs.min(), xs.max() - P, P // 2):
                if mk2[yy:yy + P, xx:xx + P].mean() < 0.99:
                    continue
                (dx, dy), r = cv2.phaseCorrelate(Ew2[yy:yy + P, xx:xx + P].astype(np.float32), Cp[yy:yy + P, xx:xx + P].astype(np.float32), win)
                sh.append((dx / s, dy / s, r))
    sh = np.array(sh) if sh else np.zeros((0, 3))
    good = sh[sh[:, 2] > 0.08] if len(sh) else sh
    mag = np.hypot(good[:, 0], good[:, 1]) if len(good) else np.array([np.nan])
    out["local"] = {"n_patches": int(len(sh)), "n_resp_gt_0.08": int(len(good)), "median_shift_px88": float(np.median(mag)),
                    "p75_shift_px88": float(np.percentile(mag, 75)) if len(good) else float("nan"),
                    "median_shift_lh": float(np.median(mag) / lh88)}
    if verbose:
        print(json.dumps({k: v for k, v in out.items() if k not in ("A_88ref_to_copy",)}, indent=None)[:900])
    return out


if __name__ == "__main__":
    import os
    cut = int(sys.argv[1]); col = sys.argv[2]
    o = place_cut(cut, col)
    os.makedirs(f"{HERE}/place", exist_ok=True)
    json.dump(o, open(f"{HERE}/place/place_cut{cut:02d}_{col}.json", "w"), indent=1)
