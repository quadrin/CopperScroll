"""Photometric stereo on the USC public previews of the WSRP 1988 multi-light frames.

Library used by run_ps.py. No image is written to the repository; all image products go to
PRIVATE (outside the repo). Numbers only are returned to callers.
"""
import csv, os, json, hashlib
import numpy as np, cv2
from scipy import ndimage as ndi

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
PRIVATE = '/root/novel/private_outputs/A'
INDEX = os.path.join(REPO, 'research/sources/usc_copper_scroll_images/index.csv')
MM_PER_PX = 10 / 29.5  # 1988 ruler on the previews (method 8, UC15246880)
ECC_SIL_MIN = 0.85  # silhouette ECC to accept a frame
ECC_TEX_MIN = 0.25  # relief-edge ECC to accept a frame

TITLE_AZ = {  # azimuth prior in frame coords (x right, y UP), degrees
    'lft top light': 135, 'ctr top light': 90, 'rt top light': 45,
    'lft bot light': 225, 'ctr bot light': 270, 'rt bot light': 315,
    'top light': 90, 'bot light': 270,
}


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def frame_path(u):
    for d in ('images/previews/cuts-01-10', 'images/previews/original-scroll-remaining'):
        p = os.path.join(REPO, d, u + '.jpg')
        if os.path.exists(p):
            return p
    return None


def frames_for(cut, film):
    """Recto multi-light frames of one cut and film ('col' or 'bla')."""
    out = []
    for r in csv.DictReader(open(INDEX)):
        if r['cut'] == str(cut) and r['side'] == 'Recto' and r['film'][:3] == film \
                and r['lighting_as_titled'] in TITLE_AZ:
            out.append((r['uc_identifier'], r['lighting_as_titled']))
    # deduplicate titles (cut 19 has two ctr top); keep all, distinct ids
    return sorted(out, key=lambda x: x[1])


def load_gray(u):
    im = cv2.imread(frame_path(u), cv2.IMREAD_COLOR)
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return g


def strip_mask(g):
    """Largest bright, tall component nearest the frame centre (the copper strip)."""
    b = cv2.GaussianBlur(g, (0, 0), 3)
    t, _ = cv2.threshold(b, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    m = (b > max(25, 0.6 * t)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    H, W = g.shape
    best, bs = None, -1
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if h < 0.45 * H:
            continue
        # cards are rectangles at the sides: penalise distance from centre
        score = a / (1 + abs(cen[i][0] - W / 2) / (0.1 * W))
        if score > bs:
            best, bs = i, score
    if best is None:
        return np.zeros_like(g, bool)
    mm = lab == best
    mm = ndi.binary_fill_holes(mm)
    return mm


_cl = cv2.createCLAHE(3.0, (8, 8))
_sift = cv2.SIFT_create(nfeatures=8000, contrastThreshold=0.01)


def register(gref, mref, g, m):
    """SIFT + RANSAC homography from frame g to reference; tries 0 and 180 degree rotation.
    Returns H (maps g pixels to ref pixels), rotation, inliers, 5-fold CV residual (px)."""
    kr, dr = _sift.detectAndCompute(_cl.apply(gref), (mref * 255).astype(np.uint8))
    best = None
    for rot in (0, 2):
        gi = np.ascontiguousarray(np.rot90(g, rot)); mi = np.ascontiguousarray(np.rot90(m, rot))
        k, d = _sift.detectAndCompute(_cl.apply(gi), (mi * 255).astype(np.uint8))
        if d is None or len(k) < 10:
            continue
        mt = cv2.BFMatcher().knnMatch(d, dr, k=2)
        good = [a for a, b in (x for x in mt if len(x) == 2) if a.distance < 0.75 * b.distance]
        if len(good) < 12:
            continue
        p1 = np.float32([k[a.queryIdx].pt for a in good]); p2 = np.float32([kr[a.trainIdx].pt for a in good])
        Hm, inl = cv2.findHomography(p1, p2, cv2.RANSAC, 3.0)
        if Hm is None:
            continue
        inl = inl.ravel().astype(bool)
        if best is None or inl.sum() > best[2]:
            best = (Hm, rot, int(inl.sum()), p1[inl], p2[inl], gi.shape)
    if best is None:
        return None
    Hm, rot, n, P1, P2, shp = best
    rng = np.random.default_rng(0); idx = rng.permutation(len(P1)); folds = np.array_split(idx, 5); errs = []
    for f in folds:
        tr = np.setdiff1d(idx, f)
        Hf, _ = cv2.findHomography(P1[tr], P2[tr], 0)
        pr = cv2.perspectiveTransform(P1[f].reshape(-1, 1, 2), Hf).reshape(-1, 2)
        errs += list(np.linalg.norm(pr - P2[f], axis=1))
    errs = np.array(errs)
    # compose rotation: H acts on the rotated image; build full transform from original g coords
    h0, w0 = g.shape
    if rot == 2:
        R = np.array([[-1, 0, w0 - 1], [0, -1, h0 - 1], [0, 0, 1]], float)
    else:
        R = np.eye(3)
    Hfull = Hm @ R
    return dict(H=Hfull, rot=rot * 90, inliers=n, cv_med_px=float(np.median(errs)),
                cv_p90_px=float(np.percentile(errs, 90)))


def phase_check(a, b, mask):
    """Residual translation between two warped frames using phase correlation on gradient magnitude."""
    def gm(x):
        x = x.astype(np.float32)
        gx = cv2.Sobel(x, cv2.CV_32F, 1, 0); gy = cv2.Sobel(x, cv2.CV_32F, 0, 1)
        g = np.sqrt(gx * gx + gy * gy) * mask
        return g
    win = cv2.createHanningWindow(a.shape[::-1], cv2.CV_32F)
    (dx, dy), resp = cv2.phaseCorrelate(gm(a), gm(b), win)
    return float(dx), float(dy), float(resp)


def to_linear(g):
    return (g.astype(np.float64) / 255.0) ** 2.2


def uncalibrated_ps(Is, mask, title_az, rots, seed=0):
    """Is: list of k registered linear images. Returns normals (H,W,3), albedo, lights (k,3), diagnostics.

    1. SVD rank-3 factorisation  I = B~ L~.
    2. Constant-albedo constraint (Hayakawa 1994) fixes B = B~ Q up to an orthogonal matrix.
    3. Mean normal of the strip -> camera axis (+z).
    4. In-plane rotation psi and mirror chosen by integrability (minimum curl of the gradient field).
    5. The remaining concave/convex (psi+180) flip is chosen by the titled light positions
       (weak prior): maximise sum cos(estimated azimuth - titled azimuth).
    """
    k = len(Is)
    H, W = mask.shape
    er = ndi.binary_erosion(mask, iterations=6)
    X = np.stack([I[er] for I in Is], 1)  # P x k
    ok = np.all((X > 0.003) & (X < 0.97), 1)
    rng = np.random.default_rng(seed)
    sel = np.flatnonzero(ok)
    sel = rng.choice(sel, min(len(sel), 60000), replace=False)
    Xs = X[sel]
    U, S, Vt = np.linalg.svd(Xs, full_matrices=False)
    sv = S / S[0]
    Lt = np.diag(np.sqrt(S[:3])) @ Vt[:3]  # 3 x k
    # pseudo-normals for all pixels in mask (weighted LS excluding shadow/saturation)
    Xall = np.stack([I[mask] for I in Is], 1)
    Wt = ((Xall > 0.003) & (Xall < 0.97)).astype(float)
    Bt = np.zeros((Xall.shape[0], 3))
    # solve per pixel with weights: group by weight pattern
    pats, inv = np.unique(Wt.astype(np.uint8), axis=0, return_inverse=True)
    inv = inv.ravel()
    for pi, pat in enumerate(pats):
        cols = pat.astype(bool)
        rows = inv == pi
        if cols.sum() < 3:
            Bt[rows] = np.nan
            continue
        Lp = Lt[:, cols]
        Bt[rows] = np.linalg.lstsq(Lp.T, Xall[rows][:, cols].T, rcond=None)[0].T
    # constant albedo: b~^T M b~ = 1
    bs = Bt[np.isfinite(Bt).all(1)]
    bs = bs[rng.choice(len(bs), min(len(bs), 40000), replace=False)]
    A = np.stack([bs[:, 0]**2, bs[:, 1]**2, bs[:, 2]**2, 2*bs[:, 0]*bs[:, 1], 2*bs[:, 0]*bs[:, 2], 2*bs[:, 1]*bs[:, 2]], 1)
    m = np.linalg.lstsq(A, np.ones(len(bs)), rcond=None)[0]
    M = np.array([[m[0], m[3], m[4]], [m[3], m[1], m[5]], [m[4], m[5], m[2]]])
    ev, evec = np.linalg.eigh(M)
    pd_ok = bool(ev.min() > 0)
    ev = np.clip(ev, 1e-6 * ev.max(), None)
    Q = evec @ np.diag(np.sqrt(ev))  # Q Q^T = M
    B = Bt @ Q
    L = np.linalg.inv(Q) @ Lt  # 3 x k
    # 3. mean normal -> +z
    nb = B / np.linalg.norm(B, axis=1, keepdims=True)
    mn = np.nanmean(nb, 0); mn /= np.linalg.norm(mn)
    z = np.array([0, 0, 1.0])
    v = np.cross(mn, z); s = np.linalg.norm(v); c = mn @ z
    if s < 1e-9:
        R1 = np.eye(3) if c > 0 else np.diag([1, -1, -1.0])
    else:
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        R1 = np.eye(3) + vx + vx @ vx * ((1 - c) / s**2)
    B = B @ R1.T
    L = R1 @ L
    # image-coordinate convention for normals: x right, y UP, z toward camera
    Bimg = np.full((H, W, 3), np.nan); Bimg[mask] = B

    def curl_energy(Bi):
        n = Bi / np.linalg.norm(Bi, axis=2, keepdims=True)
        nz = np.clip(n[..., 2], 0.2, None)
        p = -n[..., 0] / nz; q = -n[..., 1] / nz  # dz/dx, dz/dy(up)
        p = np.where(er, p, 0); q = np.where(er, q, 0)
        p = ndi.gaussian_filter(np.nan_to_num(p), 1.0); q = ndi.gaussian_filter(np.nan_to_num(q), 1.0)
        # y up: d/dy_up = -d/drow
        dp_dy = -np.gradient(p, axis=0); dq_dx = np.gradient(q, axis=1)
        cu = (dp_dy - dq_dx)[er]
        gr = np.sqrt(np.gradient(p, axis=1)**2 + np.gradient(q, axis=0)**2)[er]
        return float(np.mean(cu**2) / (np.mean(gr**2) + 1e-12))

    res = []
    for mirror in (1, -1):
        for psi in range(0, 180, 3):
            a = np.deg2rad(psi)
            Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]]) @ np.diag([mirror, 1, 1])
            Bi = Bimg @ Rz.T
            res.append((curl_energy(Bi), psi, mirror))
    res.sort()
    ce, psi, mirror = res[0]
    best_d = 0.0
    for d in np.arange(-3, 3.01, 0.5):
        a = np.deg2rad(psi + d)
        Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]]) @ np.diag([mirror, 1, 1])
        e = curl_energy(Bimg @ Rz.T)
        if e < ce:
            ce, best_d = e, d
    psi_best = psi + best_d
    curl_other_mirror = min(r[0] for r in res if r[2] != mirror)
    # 5. concave/convex flip by titled light azimuths
    out = []
    for extra in (0, 180):
        a = np.deg2rad(psi_best + extra)
        Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]]) @ np.diag([mirror, 1, 1])
        Lr = Rz @ L
        az = np.degrees(np.arctan2(Lr[1], Lr[0]))
        prior = np.array([(t + r) % 360 for t, r in zip(title_az, rots)])
        sc = float(np.sum(np.cos(np.deg2rad(az - prior))))
        out.append((sc, extra, Rz, Lr, az, prior))
    out.sort(key=lambda x: -x[0])
    sc, extra, Rz, Lr, az, prior = out[0]
    Bf = Bimg @ Rz.T
    alb = np.linalg.norm(Bf, axis=2)
    N = Bf / alb[..., None]
    N[N[..., 2] < 0.05] = np.nan
    el = np.degrees(np.arcsin(np.clip(Lr[2] / np.linalg.norm(Lr, axis=0), -1, 1)))
    diag = dict(k=k, sv_ratio=[float(x) for x in sv[:min(k, 6)]], albedo_M_posdef=pd_ok,
                curl_ratio=ce, curl_ratio_other_mirror=float(curl_other_mirror), psi=float(psi_best), mirror=int(mirror),
                flip_score_chosen=sc, flip_score_other=float(out[1][0]),
                light_az_est=[float(x) for x in az], light_az_title=[float(x) for x in prior],
                light_elev_est=[float(x) for x in el],
                az_err_deg=[float(((a - p + 180) % 360) - 180) for a, p in zip(az, prior)])
    return N, alb, Lr.T, diag


def frankot_chellappa(N, mask):
    nz = np.clip(N[..., 2], 0.15, None)
    p = -N[..., 0] / nz; q = -N[..., 1] / nz  # dz/dx (x right), dz/dy (y up)
    p = np.where(mask & np.isfinite(p), p, 0); q = np.where(mask & np.isfinite(q), q, 0)
    q_row = -q  # dz/drow
    H, W = p.shape
    wx = np.fft.fftfreq(W) * 2 * np.pi; wy = np.fft.fftfreq(H) * 2 * np.pi
    WX, WY = np.meshgrid(wx, wy)
    P = np.fft.fft2(p); Qf = np.fft.fft2(q_row)
    den = WX**2 + WY**2; den[0, 0] = 1
    Z = (-1j * WX * P - 1j * WY * Qf) / den
    Z[0, 0] = 0
    z = np.real(np.fft.ifft2(Z))
    return z  # in pixel units (same unit as x,y)


def relief(z, mask, sigma):
    """High-pass relative depth: z minus a masked Gaussian (removes strip curvature)."""
    m = mask.astype(float)
    num = ndi.gaussian_filter(np.where(mask, z, 0), sigma); den = ndi.gaussian_filter(m, sigma)
    base = num / np.maximum(den, 1e-6)
    r = np.where(mask, z - base, np.nan)
    return r


def strip_mask2(g):
    """Silhouette of the copper strip: low threshold over the near-black background, component
    nearest the frame centre that is taller than 45% of the frame; holes kept (through-holes are
    lighting-invariant landmarks), outer outline closed."""
    b = cv2.GaussianBlur(g, (0, 0), 2)
    H, W = g.shape
    bgv = np.percentile(b[:, :int(0.04 * W)], 50)
    thr = max(bgv + 12, 22)
    m = (b > thr).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    best, bs = None, -1
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if h < 0.45 * H or w > 0.6 * W:
            continue
        # reject calibration cards: very rectangular and near the frame side
        score = a / (1 + abs(cen[i][0] - W / 2) / (0.1 * W))
        if score > bs:
            best, bs = i, score
    if best is None:
        return np.zeros_like(g, bool)
    mm = (lab == best).astype(np.uint8)
    mm = cv2.morphologyEx(mm, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    return mm.astype(bool)


def _lapmag(g, s):
    x = cv2.GaussianBlur(g.astype(np.float32), (0, 0), s)
    L = np.abs(cv2.Laplacian(x, cv2.CV_32F))
    return L


def register_sil(gref, mref, g, m):
    """Similarity init from silhouettes (0/180), ECC affine on blurred silhouette, then ECC affine
    on Laplacian magnitude (relief edges; polarity-free) at sigma 3 and 1.5 inside the eroded strip.
    Returns g->ref 3x3, rot, silhouette ECC, texture ECC."""
    cr, ar, lr, wr = _mask_pose(mref); c, a, l, w = _mask_pose(m)
    Hc = max(gref.shape[0], g.shape[0]); Wc = max(gref.shape[1], g.shape[1])
    def pad(x):
        o = np.zeros((Hc, Wc), np.float32); o[:x.shape[0], :x.shape[1]] = x; return o
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-6)
    Sr = pad(cv2.GaussianBlur(mref.astype(np.float32), (0, 0), 3)); Sm = pad(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 3))
    tm = pad(ndi.binary_erosion(mref, iterations=10).astype(np.float32)).astype(np.uint8)
    best = None
    for rot in (0, 180):
        aa = a if rot == 0 else -a
        ang = np.arctan2(ar[1], ar[0]) - np.arctan2(aa[1], aa[0]); sc = lr / l
        R = sc * np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]]); tt = cr - R @ c
        Af = np.vstack([np.hstack([R, tt[:, None]]), [0, 0, 1]])
        A = np.linalg.inv(Af)[:2].astype(np.float32)
        try:
            csil, A = cv2.findTransformECC(Sr, Sm, A, cv2.MOTION_AFFINE, crit, None, 1)
        except cv2.error:
            csil = -1
        ctex = -1
        A2 = A.copy()
        try:
            for sig in (3.0, 1.5):
                Fr = pad(_lapmag(gref, sig)); Fm = pad(_lapmag(g, sig))
                ctex, A2 = cv2.findTransformECC(Fr, Fm, A2, cv2.MOTION_AFFINE, crit, tm, 1)
        except cv2.error:
            ctex = -1; A2 = A.copy()
        # guard: texture refinement may not move far from the silhouette solution
        Hs_ = np.vstack([A, [0, 0, 1]]); Ht_ = np.vstack([A2, [0, 0, 1]])
        ys, xs = np.nonzero(mref)
        pts = np.stack([xs[::200], ys[::200], np.ones_like(xs[::200])]).astype(float)
        drift = float(np.median(np.linalg.norm((Hs_ @ pts - Ht_ @ pts)[:2], axis=0)))
        key = ctex if ctex > 0 else csil - 1
        if best is None or key > best[0]:
            best = (key, rot, A, A2, csil, ctex, drift)
    _, rot, A, A2, csil, ctex, drift = best
    use = A2 if (ctex > 0 and drift < 15) else A
    H = np.linalg.inv(np.vstack([use, [0, 0, 1]]))
    return dict(H=H, rot=rot, ecc_sil=float(csil), ecc_tex=float(ctex), tex_drift_px=drift,
                scale=float(np.sqrt(abs(np.linalg.det(use[:, :2])))))


def tile_residuals(a, b, mask, n=4):
    """Phase-correlation shift between Laplacian-magnitude images in n tiles along the strip."""
    ys, xs = np.nonzero(mask)
    y0, y1 = ys.min(), ys.max(); x0, x1 = xs.min(), xs.max()
    out = []
    for i in range(n):
        ya = int(y0 + (y1 - y0) * i / n); yb = int(y0 + (y1 - y0) * (i + 1) / n)
        A = _lapmag(a[ya:yb, x0:x1], 1.5) * mask[ya:yb, x0:x1]
        B = _lapmag(b[ya:yb, x0:x1], 1.5) * mask[ya:yb, x0:x1]
        win = cv2.createHanningWindow((A.shape[1], A.shape[0]), cv2.CV_32F)
        (dx, dy), r = cv2.phaseCorrelate(A.astype(np.float32), B.astype(np.float32), win)
        out.append((float(dx), float(dy), float(r)))
    return out


def _grad(g, s=2.0):
    x = cv2.GaussianBlur(g.astype(np.float32), (0, 0), s)
    gx = cv2.Sobel(x, cv2.CV_32F, 1, 0); gy = cv2.Sobel(x, cv2.CV_32F, 0, 1)
    m = np.sqrt(gx * gx + gy * gy)
    return m


def _mask_pose(m):
    ys, xs = np.nonzero(m)
    c = np.array([xs.mean(), ys.mean()])
    cov = np.cov(np.stack([xs - c[0], ys - c[1]]))
    ev, evec = np.linalg.eigh(cov)
    ax = evec[:, 1]
    if ax[1] < 0: ax = -ax
    return c, ax, np.sqrt(ev[1]), np.sqrt(ev[0])


def register_ecc(gref, mref, g, m):
    """Initial similarity from strip masks (centroid, long axis, length), tried at 0 and 180 deg;
    refined by ECC (affine) on blurred gradient magnitude inside the strip at two scales.
    Returns H (3x3, g -> ref), rot (0/180), ecc correlation, and a held-out check: ECC correlation
    and residual phase-correlation shift computed after warping."""
    cr, ar, lr, wr = _mask_pose(mref); c, a, l, w = _mask_pose(m)
    s = lr / l
    best = None
    for rot in (0, 180):
        aa = a if rot == 0 else -a
        ang = np.arctan2(ar[1], ar[0]) - np.arctan2(aa[1], aa[0])
        R = s * np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        t = cr - R @ c
        A0 = np.hstack([R, t[:, None]]).astype(np.float32)
        Hc = max(gref.shape[0], g.shape[0]); Wc = max(gref.shape[1], g.shape[1])
        def pad(x):
            o = np.zeros((Hc, Wc), x.dtype); o[:x.shape[0], :x.shape[1]] = x; return o
        Gr = pad(_grad(gref)); Gm = pad(_grad(g)); mref_p = pad(mref); m_p = pad(m)
        Gr = Gr / (np.percentile(Gr[mref_p], 99) + 1e-6); Gm = Gm / (np.percentile(Gm[m_p], 99) + 1e-6)
        tmpl_mask = ndi.binary_erosion(mref_p, iterations=8).astype(np.uint8)
        A = A0.copy(); cc = -1
        try:
            for sc, sig in ((0.5, 4.0), (1.0, 2.0)):
                Gr_ = cv2.GaussianBlur(Gr, (0, 0), sig); Gm_ = cv2.GaussianBlur(Gm, (0, 0), sig)
                if sc != 1.0:
                    Gr_s = cv2.resize(Gr_, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
                    Gm_s = cv2.resize(Gm_, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
                    ms = cv2.resize(tmpl_mask, (Gr_s.shape[1], Gr_s.shape[0]), interpolation=cv2.INTER_NEAREST)
                    As = A.copy(); As[:, 2] *= sc
                    cc, As = cv2.findTransformECC(Gr_s, Gm_s, As, cv2.MOTION_AFFINE,
                                                  (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), ms, 5)
                    A = As.copy(); A[:, 2] /= sc
                else:
                    cc, A = cv2.findTransformECC(Gr_, Gm_, A, cv2.MOTION_AFFINE,
                                                 (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), tmpl_mask, 5)
        except cv2.error as e:
            print('ECC error', str(e)[:120]); cc = -1
        # findTransformECC returns warp mapping template coords -> input coords (ref -> g)
        if best is None or cc > best[0]:
            best = (cc, rot, A.copy())
    cc, rot, A = best
    Hinv = np.vstack([A, [0, 0, 1]])  # ref -> g
    H = np.linalg.inv(Hinv)            # g -> ref
    return dict(H=H, rot=rot, ecc=float(cc), scale=float(np.sqrt(abs(np.linalg.det(A[:, :2])))))


_sift2 = cv2.SIFT_create(nfeatures=10000, contrastThreshold=0.005)


def sift_affine(gref, mref, g, m, min_inl=30):
    """Full affine g->ref from SIFT matches inside dilated strip masks; 5-fold CV residual."""
    kr, dr = _sift2.detectAndCompute(_cl.apply(gref), (ndi.binary_dilation(mref, iterations=5) * 255).astype(np.uint8))
    k, d = _sift2.detectAndCompute(_cl.apply(g), (ndi.binary_dilation(m, iterations=5) * 255).astype(np.uint8))
    if d is None or dr is None:
        return None
    mt = cv2.BFMatcher().knnMatch(d, dr, k=2)
    good = [a for a, b in (x for x in mt if len(x) == 2) if a.distance < 0.8 * b.distance]
    if len(good) < 8:
        return None
    p1 = np.float32([k[a.queryIdx].pt for a in good]); p2 = np.float32([kr[a.trainIdx].pt for a in good])
    A, inl = cv2.estimateAffine2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=3.0, maxIters=10000)
    if A is None or inl.sum() < min_inl:
        return dict(ok=False, inliers=0 if inl is None else int(inl.sum()))
    inl = inl.ravel().astype(bool); P1, P2 = p1[inl], p2[inl]
    rng = np.random.default_rng(0); idx = rng.permutation(len(P1)); errs = []
    for f in np.array_split(idx, 5):
        tr = np.setdiff1d(idx, f)
        Af, _ = cv2.estimateAffine2D(P1[tr], P2[tr], method=cv2.LMEDS)
        pr = P1[f] @ Af[:, :2].T + Af[:, 2]
        errs += list(np.linalg.norm(pr - P2[f], axis=1))
    errs = np.array(errs)
    return dict(ok=True, H=np.vstack([A, [0, 0, 1]]), inliers=int(inl.sum()),
                cv_med_px=float(np.median(errs)), cv_p90_px=float(np.percentile(errs, 90)))


def titled_ps(Is, mask, title_az, el_grid=range(10, 81, 5), iters=6, seed=0):
    """Semi-calibrated Lambertian PS: light azimuths fixed to the titled positions (frame coords,
    y up), one common unknown elevation (grid, chosen by least residual), one unknown intensity
    scale per frame (alternating least squares). Shadowed/saturated samples are excluded.
    Note: under the generalized bas-relief ambiguity, elevation mostly rescales relief; features
    used downstream are scale-free."""
    k = len(Is)
    X = np.stack([I[mask] for I in Is], 1)
    Wt = ((X > 0.003) & (X < 0.97)).astype(float)
    rng = np.random.default_rng(seed)
    sub = rng.choice(len(X), min(len(X), 30000), replace=False)

    def solve_B(L, Xs, Ws):
        B = np.zeros((len(Xs), 3))
        pats, inv = np.unique(Ws.astype(np.uint8), axis=0, return_inverse=True); inv = inv.ravel()
        for pi, pat in enumerate(pats):
            c = pat.astype(bool); rows = inv == pi
            if c.sum() < 3:
                B[rows] = np.nan; continue
            B[rows] = np.linalg.lstsq(L[c], Xs[rows][:, c].T, rcond=None)[0].T
        return B

    best = None
    for el in el_grid:
        e = np.deg2rad(el)
        D = np.array([[np.cos(e) * np.cos(np.deg2rad(a)), np.cos(e) * np.sin(np.deg2rad(a)), np.sin(e)] for a in title_az])
        s = np.ones(k)
        Xs, Ws = X[sub], Wt[sub]
        for _ in range(iters):
            L = D * s[:, None]
            B = solve_B(L, Xs, Ws)
            ok = np.isfinite(B).all(1)
            pred = np.clip(B[ok] @ D.T, 1e-6, None)
            for i in range(k):
                w = Ws[ok, i] > 0
                s[i] = np.sum(pred[w, i] * Xs[ok][w, i]) / np.sum(pred[w, i] ** 2)
            s /= np.exp(np.mean(np.log(s)))
        L = D * s[:, None]
        B = solve_B(L, Xs, Ws); ok = np.isfinite(B).all(1)
        r = np.sum(Ws[ok] * (Xs[ok] - np.clip(B[ok] @ L.T, 0, None)) ** 2) / np.sum(Ws[ok] * Xs[ok] ** 2)
        if best is None or r < best[0]:
            best = (r, el, L, s)
    r, el, L, s = best
    B = solve_B(L, X, Wt)
    H, W = mask.shape
    Bi = np.full((H, W, 3), np.nan); Bi[mask] = B
    alb = np.linalg.norm(Bi, axis=2)
    N = Bi / alb[..., None]
    N[~(N[..., 2] > 0.05)] = np.nan
    return N, alb, L, dict(el_fit=float(el), rel_resid=float(r), frame_scale=[float(x) for x in s])
