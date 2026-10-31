"""Locate each 1988 cut frame inside its column, by template matching the PS groove map of the cut
against a synthetic 'letter-box' image built from the W2F facsimile components (Puech 2006 facsimile,
transformed into Puech copy-photo pixels with the W2F affine). The result is a transform
copy-photo px -> 1988 reference-frame px for each (cut, film). No image is read by eye; numbers only.

Search: column candidates from the radiograph captions (data/plate_index.csv); vertical scale
s in [0.40, 0.66]; horizontal/vertical aspect a in [0.55, 1.05] (curvature foreshortening);
rotation 0 or 180 deg plus small tilt in {-3, -1.5, 0, 1.5, 3} deg; translation exhaustive (NCC).
Quality: peak NCC and its margin over the best peak with a translation differing by more than
0.6 line spacings (line-shift ambiguity), recorded per cut.

Usage: python3 -I map_cuts.py
"""
import os, sys, json, glob
import numpy as np, cv2
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ps_lib as P

W2F = os.path.join(P.REPO, 'research/agent_review_2026-10-07/wave2/W2F_plates_model/data')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ps_runs')
REG = json.load(open(os.path.join(W2F, 'registration.json')))
DS = 0.5
EDGE_ERODE = 12
CUT_COLS = {2: [1], 3: [1], 5: [2], 6: [2], 7: [3], 8: [3], 9: [4], 10: [4, 5], 12: [6], 15: [8],
            16: [9], 18: [10]}
# Cuts 19-23 (columns XI-XII) are excluded: exposed series and XII 10 is applied last, never used for calibration.
# Column XI from cut 16 dropped for the same reason.


def col_template(col):
    d = json.load(open(os.path.join(W2F, f'fac_components_col{col:02d}.json')))
    A = np.array(REG[str(col)]['A_fac2photo'])
    boxes = []
    for c in d['comps']:
        p0 = A @ [c['x0'], c['y0'], 1]; p1 = A @ [c['x1'], c['y1'], 1]
        boxes.append((p0[0], p0[1], p1[0], p1[1]))
    b = np.array(boxes)
    Wd = int(b[:, 2].max() + 80); Hd = int(b[:, 3].max() + 80)
    return b, (Hd, Wd), d['Lh'], d


def render(boxes, shape, M, out_shape):
    """Fill boxes transformed by 2x3 M into an image of out_shape."""
    img = np.zeros(out_shape, np.float32)
    for x0, y0, x1, y1 in boxes:
        pts = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], np.float32)
        q = pts @ M[:, :2].T + M[:, 2]
        cv2.fillConvexPoly(img, np.round(q).astype(np.int32), 1.0)
    return img


def groove_map(npz):
    d = np.load(npz)
    N, m, z = d['N'], d['mask'], d['z']
    r = P.relief(z, m, 6.0)
    g = np.clip(-np.nan_to_num(r, nan=0.0), 0, None)
    g = ndi.gaussian_filter(g, 1.0)
    m = ndi.binary_erosion(m, iterations=EDGE_ERODE)  # strip edges carry curl/shadow artefacts
    g[~m] = 0
    return g, m


def match(cut, film):
    npz = os.path.join(P.PRIVATE, f'ps_cut{cut:02d}_{film}.npz')
    if not os.path.exists(npz):
        return None
    g, m = groove_map(npz)
    ys, xs = np.nonzero(m); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    T = g[y0:y1, x0:x1]; Tm = m[y0:y1, x0:x1]
    T = np.where(Tm, (T - T[Tm].mean()) / (T[Tm].std() + 1e-9), 0).astype(np.float32)
    Td = cv2.resize(T, None, fx=DS, fy=DS, interpolation=cv2.INTER_AREA)
    best = []
    for col in CUT_COLS.get(cut, []):
        boxes, (Hd, Wd), Lh, d = col_template(col)
        # vertical scale constrained by line spacing: autocorrelation of the row profile of the
        # groove map, first peak in [35, 75] px, divided by the column's copy-photo line spacing
        prof = np.array([g[y][m[y]].mean() if m[y].sum() > 10 else np.nan for y in range(y0, y1)])
        prof = np.nan_to_num(prof - np.nanmean(prof))
        ac = np.correlate(prof, prof, 'full')[len(prof) - 1:]; ac /= ac[0]
        lag = 35 + int(np.argmax(ac[35:76]))
        sp = float(np.median(np.diff(d['line_a']))) * float(np.array(REG[str(col)]['A_fac2photo'])[1][1])
        s0 = lag / sp
        S_GRID = s0 * np.array([0.9, 0.95, 1.0, 1.05, 1.1])
        for rot in (0, 180):
            for tilt in (-2, 0, 2):
                for s in S_GRID:
                    for a in np.arange(0.30, 0.801, 0.05):
                        th = np.deg2rad(rot + tilt)
                        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
                        S = np.diag([s * a, s])
                        Mlin = R @ S
                        # place transformed column in a canvas
                        corners = np.array([[0, 0], [Wd, 0], [Wd, Hd], [0, Hd]], float) @ Mlin.T
                        off = -corners.min(0) + T.shape[::-1]
                        M = np.hstack([Mlin, off[:, None]])
                        cs = (int(np.ptp(corners[:, 1]) + 2 * T.shape[0]), int(np.ptp(corners[:, 0]) + 2 * T.shape[1]))
                        F = render(boxes, None, M, cs)
                        F = cv2.GaussianBlur(F, (0, 0), 1.0)
                        Fd = cv2.resize(F, None, fx=DS, fy=DS, interpolation=cv2.INTER_AREA)
                        R_ = cv2.matchTemplate(Fd, Td, cv2.TM_CCOEFF_NORMED)
                        cover = cv2.matchTemplate(Fd, np.ones_like(Td), cv2.TM_CCORR) / Td.size
                        R_ = np.where((cover > 0.04) & np.isfinite(R_) & (R_ <= 1.0), R_, -1)
                        iy, ix = np.unravel_index(np.argmax(R_), R_.shape)
                        pk = R_[iy, ix]
                        iy, ix = int(round(iy / DS)), int(round(ix / DS))
                        # line-shift ambiguity: best peak further than 0.6 line spacing (~1.9 Lh*s)
                        rad = int(max(4, 0.6 * 2.0 * Lh * s))
                        ry, rx, rr = int(iy * DS), int(ix * DS), int(rad * DS) + 1
                        R2 = R_.copy(); R2[max(0, ry - rr):ry + rr + 1, max(0, rx - rr):rx + rr + 1] = -1
                        second = R2.max()
                        best.append((float(pk), float(second), col, rot, tilt, float(s), float(a), int(ix), int(iy), M.tolist(), (int(x0), int(y0))))
    best.sort(key=lambda b: -b[0])
    return best


def to_frame(best_row):
    """Return 2x3 transform copy-photo px -> 1988 reference frame px."""
    pk, second, col, rot, tilt, s, a, ix, iy, M, (x0, y0) = best_row
    M = np.array(M)
    # canvas px = M @ photo; template top-left in canvas = (ix, iy) corresponds to frame (x0, y0)
    M2 = M.copy(); M2[:, 2] += np.array([x0 - ix, y0 - iy])
    return M2


if __name__ == '__main__':
    res = {}
    cuts = [int(c) for c in sys.argv[1:]] or sorted(CUT_COLS)
    for cut in cuts:
        for film in ('bla', 'col'):
            b = match(cut, film)
            if not b:
                continue
            top = b[0]
            # best alternative with different column or rotation
            alt = next((x for x in b if (x[2], x[3]) != (top[2], top[3])), None)
            res[f'{cut}_{film}'] = dict(cut=cut, film=film, ncc=round(top[0], 4), ncc_second_shift=round(top[1], 4),
                                        ncc_alt_col_or_rot=None if alt is None else round(alt[0], 4),
                                        col=top[2], rot=top[3], tilt=top[4], s=round(top[5], 3), aspect=top[6],
                                        photo_to_frame=to_frame(top).tolist())
            print(cut, film, {k: v for k, v in res[f'{cut}_{film}'].items() if k != 'photo_to_frame'}, flush=True)
            json.dump(res, open(os.path.join(OUT, 'cut_mapping' + ('_' + '_'.join(sys.argv[1:]) if sys.argv[1:] else '') + '.json'), 'w'), indent=1)
