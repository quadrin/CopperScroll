"""C2 copper measurement library (31 Oct 2026). Numbers only leave this module; images stay in SP.

Pipeline for one cut (all steps automatic, no hand placement):
 1. Read the six standard recto lights (RLT RCT RRT RLB RCB RRB) at scale S of full resolution.
 2. Strip mask per frame: largest bright-enough, tall connected component that is not a colour chart
    (copper patina: saturation and hue band; the black background is dark).
 3. Register each light to RCT by ECC (Euclidean) on the blurred strip silhouette, then refined on
    high-passed luminance inside the eroded mask.
 4. Relief-slope maps from opposite lights (photometric differences; albedo cancels):
      gy = (T - B)/(T + B), T = mean(RLT, RCT, RRT), B = mean(RLB, RCB, RRB)
      gx = (L - R)/(L + R), L = mean(RLT, RLB),      R = mean(RRT, RRB)
    high-passed (minus a Gaussian of sigma HP_CM) to remove wrinkles; E = sqrt(gx^2 + gy^2) is the
    'engraving energy' (strong local slope).
 5. Strip axis: the strip is near vertical; the analysis window is the inner INNER fraction of the
    mask width, row by row.
 6. Row profile of E over the window, smoothed; line bands = peaks separated by >= 0.6 pitch, where
    pitch = autocorrelation peak in [1.4, 2.8] cm.
 7. Per band (between the troughs on either side):
      h      = FWHM of the band peak above the mean of its two troughs / local pitch (mean distance to
               neighbouring peaks)   [letter height against line pitch]
      adv    = horizontal autocorrelation period of the band's column profile of |gx| (letter advance), cm
      asp    = adv / FWHM            [aspect proxy: letter advance against letter height]
      fill   = share of window columns whose band column-profile exceeds the band's threshold
               (mid-point between the 20th and 90th percentiles)   [ink/space proxy]
      gapr   = mean length of below-threshold runs shorter than 1.5 adv, / FWHM   [inter-letter gap]
      wgapr  = mean length of below-threshold runs >= 1.5 adv and < 6 adv, / FWHM   [inter-word gap]
"""
import os, sys, json
import numpy as np, cv2
from scipy import ndimage as ndi
from scipy.signal import find_peaks

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch  # noqa: E402

LIGHTS = ['RLT', 'RCT', 'RRT', 'RLB', 'RCB', 'RRB']
PX_PER_CM_FULL = 155.0  # nominal; replaced per frame by the ruler measurement when found


def load_cut(cut, scale, purpose, lights=LIGHTS):
    out = {}
    for L in lights:
        item = fetch.item_name(cut, L)
        try:
            a = fetch.get_overview(item, scale, purpose)
        except KeyError:
            continue
        out[L] = a
    return out


def gray(a):
    return cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0


def strip_window(a, px_cm):
    """Strip location without hand placement. Returns (x0, x1, y0, y1) of the copper strip:
    columns = the run of high fine-texture columns nearest the image centre (width >= 1.5 cm);
    rows = rows whose mean brightness inside that run exceeds 40 % of the run's median brightness."""
    v = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)[..., 2].astype(np.float32)
    vb = cv2.GaussianBlur(v, (0, 0), 1.5)
    lap = np.abs(cv2.Laplacian(vb, cv2.CV_32F))
    H, W = v.shape
    r0, r1 = int(0.15 * H), int(0.85 * H)
    t = np.median(lap[r0:r1], 0) * (np.median(vb[r0:r1], 0) > 25)
    t = ndi.gaussian_filter1d(t, max(2, 0.1 * px_cm))
    thr = 0.5 * (np.percentile(t, 10) + np.percentile(t, 90))
    on = t > thr
    runs, s0 = [], None
    for x in range(W + 1):
        if x < W and on[x]:
            s0 = x if s0 is None else s0
        elif s0 is not None:
            runs.append((s0, x)); s0 = None
    runs = [(x0, x1) for x0, x1 in runs if x1 - x0 >= 1.5 * px_cm and 0.2 * W <= (x0 + x1) / 2 <= 0.8 * W]
    if not runs:
        return None
    x0, x1 = max(runs, key=lambda r: t[r[0]:r[1]].sum())
    rowv = vb[:, x0:x1].mean(1)
    med = np.median(rowv[r0:r1])
    rows = np.flatnonzero(rowv > 0.4 * med)
    if len(rows) < 10:
        return None
    return int(x0), int(x1), int(rows[0]), int(rows[-1]) + 1


def strip_mask(a, px_cm):
    w = strip_window(a, px_cm)
    if w is None:
        return None
    m = np.zeros(a.shape[:2], bool)
    x0, x1, y0, y1 = w
    m[y0:y1, x0:x1] = True
    return m


def hp(img, sigma):
    return img - cv2.GaussianBlur(img, (0, 0), sigma)


def register_tb(T, B, win):
    """Translation of B onto T (same view, light changed) by phase correlation of high-passed
    luminance inside the strip window of T. Returns (dx, dy, response)."""
    x0, x1, y0, y1 = win
    gT = hp(gray(T), 3.0); gB = hp(gray(B), 3.0)
    H = min(gT.shape[0], gB.shape[0]); W = min(gT.shape[1], gB.shape[1])
    gT, gB = gT[:H, :W], gB[:H, :W]
    pad = 0.1
    xa, xb = max(0, x0 - int(pad * (x1 - x0))), min(W, x1 + int(pad * (x1 - x0)))
    ya, yb = max(0, y0), min(H, y1)
    win2 = cv2.createHanningWindow((xb - xa, yb - ya), cv2.CV_32F)
    (dx, dy), resp = cv2.phaseCorrelate(np.ascontiguousarray(gT[ya:yb, xa:xb]), np.ascontiguousarray(gB[ya:yb, xa:xb]), win2)
    return float(dx), float(dy), float(resp)


def shift(img, dx, dy, shape):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, M, (shape[1], shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_REFLECT)


def relief_view(T, B, scale):
    """One view (L, C or R): T = top-lit, B = bottom-lit frame. Returns dict with the albedo-free
    vertical-slope image S = hp((T-B)/(T+B)), the energy E = |S|, a single-light horizontal-gradient
    image GX (from T+B), the strip window and registration diagnostics."""
    px_cm = PX_PER_CM_FULL * scale
    win = strip_window(T, px_cm)
    if win is None:
        return None
    dx, dy, resp = register_tb(T, B, win)
    gT = gray(T)
    gB = shift(gray(B), dx, dy, gT.shape)
    eps = 0.02
    S = hp((gT - gB) / (gT + gB + eps), 0.5 * px_cm)
    S = cv2.GaussianBlur(S, (0, 0), max(0.6, 0.02 * px_cm))
    A = cv2.GaussianBlur(gT + gB, (0, 0), max(0.6, 0.02 * px_cm))
    GX = hp(np.abs(cv2.Sobel(A, cv2.CV_32F, 1, 0)), 0.5 * px_cm)
    m = np.zeros(gT.shape, bool)
    x0, x1, y0, y1 = win
    m[y0:y1, x0:x1] = True
    return dict(S=S, E=np.abs(S), GX=GX, mask=m, win=win, px_cm=px_cm,
                reg=dict(dx=round(dx, 2), dy=round(dy, 2), resp=round(resp, 3)))


def window(mask, inner):
    """Per-row [x0, x1) of the inner fraction of the mask width; rows with too little mask -> None."""
    H, W = mask.shape
    xs0 = np.full(H, -1); xs1 = np.full(H, -1)
    for y in range(H):
        r = np.flatnonzero(mask[y])
        if len(r) < 10:
            continue
        a, b = r[0], r[-1] + 1
        m = int((1 - inner) / 2 * (b - a))
        xs0[y], xs1[y] = a + m, b - m
    return xs0, xs1


def row_profile(E, xs0, xs1):
    H = E.shape[0]
    p = np.full(H, np.nan)
    for y in range(H):
        if xs0[y] >= 0 and xs1[y] - xs0[y] > 5:
            p[y] = E[y, xs0[y]:xs1[y]].mean()
    return p


def acf(x):
    x = np.asarray(x, float); x = x - x.mean()
    a = np.correlate(x, x, 'full')[len(x) - 1:]
    return a / a[0] if a[0] > 0 else a


def peak_in(a, lo, hi):
    lo = max(1, int(lo)); hi = min(len(a) - 1, int(hi))
    if hi <= lo + 2:
        return None, None
    pk, _ = find_peaks(a[lo:hi])
    if len(pk) == 0:
        return None, None
    k = pk[np.argmax(a[lo:hi][pk])] + lo
    return int(k), float(a[k])


def bands(E, mask, px_cm, inner=0.7, smooth_cm=0.12):
    """Detect line bands and measure them. Returns (pitch_px, acf_pitch, list of band dicts, profile)."""
    xs0, xs1 = window(mask, inner)
    prof = row_profile(E, xs0, xs1)
    valid = np.isfinite(prof)
    ys = np.flatnonzero(valid)
    if len(ys) < 50:
        return None, None, [], prof
    y_lo, y_hi = ys[0], ys[-1] + 1
    p = prof[y_lo:y_hi].copy()
    p[~np.isfinite(p)] = np.nanmedian(p)
    p = ndi.gaussian_filter1d(p, smooth_cm * px_cm)
    pd_ = p - ndi.uniform_filter1d(p, int(4 * px_cm))
    kp, ap = peak_in(acf(pd_), 1.4 * px_cm, 2.8 * px_cm)
    if kp is None:
        return None, None, [], prof
    pk, _ = find_peaks(pd_, distance=max(3, int(0.6 * kp)), prominence=0.15 * np.std(pd_))
    tr, _ = find_peaks(-pd_, distance=max(3, int(0.4 * kp)))
    res = []
    for i, y in enumerate(pk):
        above = tr[tr < y]; below = tr[tr > y]
        if len(above) == 0 or len(below) == 0:
            continue
        ta, tb = above[-1], below[0]
        base = 0.5 * (p[ta] + p[tb]); top = p[y]
        if top <= base:
            continue
        half = base + 0.5 * (top - base)
        seg = np.flatnonzero(p[ta:tb + 1] >= half)
        # extent = outermost rows above half height between the two troughs (handles roof/base
        # double peaks of the square script)
        l, r = int(seg[0]), int(seg[-1])
        fwhm = (r - l + 1)
        nb = []
        if i > 0:
            nb.append(y - pk[i - 1])
        if i < len(pk) - 1:
            nb.append(pk[i + 1] - y)
        nb = [d for d in nb if 0.6 * kp <= d <= 1.6 * kp]
        pitch_loc = float(np.mean(nb)) if nb else float(kp)
        yy = y + y_lo
        res.append(dict(y=int(yy), y_top=int(ta + y_lo), y_bot=int(tb + y_lo), y_ext0=int(ta + l + y_lo), y_ext1=int(ta + r + y_lo), fwhm_px=float(fwhm),
                        pitch_px=pitch_loc, h=float(fwhm) / pitch_loc, contrast=float((top - base) / (np.std(pd_) + 1e-9))))
    return kp, ap, res, prof


def band_columns(Emap, gx, mask, band, px_cm, inner=0.7):
    """Column-level measures inside one band: adv (cm), asp, fill, gapr, wgapr."""
    y0 = band['y_ext0']; y1 = band['y_ext1'] + 1
    y0 = max(0, y0); y1 = min(mask.shape[0], y1)
    if y1 - y0 < 3:
        return {}
    xs0, xs1 = window(mask[y0:y1], inner)
    ok = xs0 >= 0
    if ok.sum() < 3:
        return {}
    x0, x1 = int(np.median(xs0[ok])), int(np.median(xs1[ok]))
    if x1 - x0 < 1.5 * px_cm:
        return {}
    cp = Emap[y0:y1, x0:x1].mean(0)
    cp = ndi.gaussian_filter1d(cp, 0.05 * px_cm)
    cpx = np.abs(gx[y0:y1, x0:x1]).mean(0) if gx is not None else cp
    cpx = cpx - ndi.uniform_filter1d(cpx, int(2 * px_cm))
    ka, aa = peak_in(acf(cpx), 0.35 * px_cm, 1.6 * px_cm)
    adv = ka if ka else np.nan
    lo, hi = np.percentile(cp, 20), np.percentile(cp, 90)
    thr = 0.5 * (lo + hi)
    on = cp >= thr
    fill = float(on.mean())
    runs = []
    s = None
    for x in range(len(on) + 1):
        if x < len(on) and not on[x]:
            s = x if s is None else s
        elif s is not None:
            if s > 0 and x < len(on):  # interior runs only
                runs.append(x - s)
            s = None
    runs = np.array(runs, float)
    fw = band['fwhm_px']
    out = dict(adv_cm=float(adv / px_cm) if np.isfinite(adv) else np.nan, acf_adv=float(aa) if aa else np.nan,
               asp=float(adv / fw) if np.isfinite(adv) else np.nan, fill=fill, width_cm=float((x1 - x0) / px_cm))
    if np.isfinite(adv) and len(runs):
        short = runs[runs < 1.5 * adv]; long_ = runs[(runs >= 1.5 * adv) & (runs < 6 * adv)]
        out['gapr'] = float(short.mean() / fw) if len(short) else np.nan
        out['wgapr'] = float(long_.mean() / fw) if len(long_) else np.nan
    else:
        out['gapr'] = np.nan; out['wgapr'] = np.nan
    return out


# ---------------------------------------------------------------------------------------------
# Single-frame horizontal-stroke energy (no cross-light registration needed)
# ---------------------------------------------------------------------------------------------
def stroke_energy(a, px_cm):
    """|d/dy| of luminance, band-passed to stroke scale (DoG 0.04 cm / 0.25 cm) and smoothed along x
    (0.25 cm) so that horizontal strokes (roofs and bases of the square script) dominate over
    randomly oriented crumple relief. Ex is the same for vertical strokes (smoothed along y)."""
    g = gray(a)
    s1, s2 = max(0.6, 0.04 * px_cm), 0.25 * px_cm
    bp = cv2.GaussianBlur(g, (0, 0), s1) - cv2.GaussianBlur(g, (0, 0), s2)
    dy = np.abs(cv2.Sobel(bp, cv2.CV_32F, 0, 1, ksize=3))
    dx = np.abs(cv2.Sobel(bp, cv2.CV_32F, 1, 0, ksize=3))
    Ey = cv2.GaussianBlur(dy, (0, 0), sigmaX=0.25 * px_cm, sigmaY=max(0.6, 0.03 * px_cm))
    Ex = cv2.GaussianBlur(dx, (0, 0), sigmaX=max(0.6, 0.03 * px_cm), sigmaY=0.25 * px_cm)
    return Ey, Ex


def frame_profile(a, px_cm, inner=0.6):
    win = strip_window(a, px_cm)
    if win is None:
        return None
    Ey, Ex = stroke_energy(a, px_cm)
    x0, x1, y0, y1 = win
    m = int((1 - inner) / 2 * (x1 - x0))
    xa, xb = x0 + m, x1 - m
    # holes and dark patina blotches: luminance below 0.5 x the window median (blurred 0.1 cm);
    # their edges are dilated by 0.1 cm and excluded from the row profile.
    g = cv2.GaussianBlur(gray(a), (0, 0), max(0.6, 0.1 * px_cm))
    sub = g[y0:y1, xa:xb]
    dark = g < 0.5 * np.median(sub)
    dark = ndi.binary_dilation(dark, iterations=max(1, int(0.1 * px_cm)))
    W = (~dark).astype(np.float32)
    num = (Ey * W)[:, xa:xb].sum(1); den = W[:, xa:xb].sum(1)
    prof = np.where(den > 0.3 * (xb - xa), num / np.maximum(den, 1), np.nan)
    prof[:y0] = np.nan; prof[y1:] = np.nan
    return dict(win=win, xa=xa, xb=xb, prof=prof, Ey=Ey, Ex=Ex, valid=W)


def measure_frame(a, px_cm, inner=0.6, smooth_cm=0.06, q=(0.15, 0.85)):
    """Bands from the masked stroke-energy row profile of one frame.
    Letter extent per band = energy-weighted inter-quantile range (q) of rows between the two
    troughs, after subtracting the trough baseline; h = extent / frame pitch (acf).
    Returns dict(pitch_px, acf, y0, y1, bands=[dict(y, r, ext_px, h, hloc, adv_px, asp, fill, gapr, wgapr)])."""
    F = frame_profile(a, px_cm, inner)
    if F is None:
        return None
    x0, x1, y0, y1 = F['win']
    p = F['prof'].copy()
    seg = np.arange(y0, y1)
    pp = p[y0:y1]
    pp[~np.isfinite(pp)] = np.nanmedian(pp)
    pp = ndi.gaussian_filter1d(pp, smooth_cm * px_cm)
    pd_ = pp - ndi.uniform_filter1d(pp, int(4 * px_cm))
    kp, ap = peak_in(acf(pd_), 1.4 * px_cm, 2.8 * px_cm)
    if kp is None:
        return dict(pitch_px=None, acf=None, y0=y0, y1=y1, bands=[])
    pk, _ = find_peaks(pd_, distance=max(3, int(0.6 * kp)), prominence=0.15 * np.std(pd_))
    tr, _ = find_peaks(-pd_, distance=max(3, int(0.4 * kp)))
    out = []
    for i, y in enumerate(pk):
        above = tr[tr < y]; below = tr[tr > y]
        if len(above) == 0 or len(below) == 0:
            continue
        ta, tb = above[-1], below[0]
        if tb - ta > 1.6 * kp:
            continue
        base = min(pd_[ta], pd_[tb])
        w = np.clip(pd_[ta:tb + 1] - base, 0, None)
        if w.sum() <= 0:
            continue
        c = np.cumsum(w) / w.sum()
        lo = ta + int(np.searchsorted(c, q[0])); hi = ta + int(np.searchsorted(c, q[1]))
        ext = hi - lo + 1
        nb = []
        if i > 0:
            nb.append(y - pk[i - 1])
        if i < len(pk) - 1:
            nb.append(pk[i + 1] - y)
        nb = [d for d in nb if 0.6 * kp <= d <= 1.6 * kp]
        ploc = float(np.mean(nb)) if nb else np.nan
        Y = int(y + y0)
        b = dict(y=Y, r=(Y - y0) / max(1, (y1 - y0)), ext_px=float(ext), h=float(ext) / kp,
                 hloc=float(ext) / ploc if np.isfinite(ploc) else np.nan, ploc_px=ploc,
                 y_ext0=int(lo + y0), y_ext1=int(hi + y0), fwhm_px=float(ext),
                 prom=float((pd_[y] - base) / (np.std(pd_) + 1e-9)))
        # horizontal measures inside the band (C-view centre only is used for decisions)
        ya, yb = b['y_ext0'], b['y_ext1'] + 1
        xa, xb = F['xa'], F['xb']
        cpx = F['Ex'][ya:yb, xa:xb].mean(0)
        cpx = cpx - ndi.uniform_filter1d(cpx, int(2 * px_cm))
        ka, aa = peak_in(acf(cpx), 0.35 * px_cm, 1.6 * px_cm)
        b['adv_px'] = float(ka) if ka else np.nan
        b['asp'] = b['adv_px'] / ext if ka else np.nan
        cp = (F['Ex'][ya:yb, xa:xb] + F['Ey'][ya:yb, xa:xb]).mean(0)
        loq, hiq = np.percentile(cp, 20), np.percentile(cp, 90)
        on = cp >= 0.5 * (loq + hiq)
        b['fill'] = float(on.mean())
        runs, s0 = [], None
        for x in range(len(on) + 1):
            if x < len(on) and not on[x]:
                s0 = x if s0 is None else s0
            elif s0 is not None:
                if s0 > 0 and x < len(on):
                    runs.append(x - s0)
                s0 = None
        runs = np.array(runs, float)
        if ka and len(runs):
            sh = runs[runs < 1.5 * ka]; lg = runs[(runs >= 1.5 * ka) & (runs < 6 * ka)]
            b['gapr'] = float(sh.mean() / ext) if len(sh) else np.nan
            b['wgapr'] = float(lg.mean() / ext) if len(lg) else np.nan
        else:
            b['gapr'] = b['wgapr'] = np.nan
        out.append(b)
    return dict(pitch_px=float(kp), acf=float(ap), y0=int(y0), y1=int(y1), win=F['win'], bands=out,
                pd=pd_, peaks=[int(v) for v in pk])


def ruler_px_per_cm(a, px_cm_nominal):
    """Ruler period (alternating 1 cm black/white blocks): the 5-px column whose vertical profile is
    black-and-white (>= 20 % of rows < 60 and >= 20 % > 190 grey) with the strongest autocorrelation
    peak at 0.65-1.35 x the nominal 2 cm period. Returns (px_per_cm, acf) or (nan, nan)."""
    g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float32)
    H, W = g.shape
    r0, r1 = int(0.1 * H), int(0.9 * H)
    best = (0.0, None)
    for x in range(2, W - 2, 2):
        col = g[r0:r1, x - 2:x + 3].mean(1)
        if (col < 60).mean() < 0.2 or (col > 190).mean() < 0.2:
            continue
        k, ac = peak_in(acf(col), 0.65 * 2 * px_cm_nominal, 1.35 * 2 * px_cm_nominal)
        if k and ac > best[0]:
            best = (ac, k)
    if best[1] is None:
        return np.nan, np.nan
    return best[1] / 2.0, best[0]


def region_h(m, r_lo, r_hi, q=(0.15, 0.85)):
    """Region-level letter height against pitch: the band windows (peak +- 0.5 pitch) of all bands
    whose strip position r lies in [r_lo, r_hi] are baseline-subtracted (window minimum), normalised
    to unit sum and averaged; the extent is the inter-quantile (q) range of the mean window, / pitch.
    Returns (h, n_bands)."""
    if m is None or not m.get('peaks'):
        return np.nan, 0
    pd_ = m['pd']; kp = m['pitch_px']; half = int(round(0.5 * kp))
    L = m['y1'] - m['y0']
    acc, n = np.zeros(2 * half + 1), 0
    for y in m['peaks']:
        r = y / max(1, L)
        if not (r_lo <= r <= r_hi):
            continue
        if y - half < 0 or y + half >= len(pd_):
            continue
        w = pd_[y - half:y + half + 1].copy()
        w = w - w.min()
        if w.sum() <= 0:
            continue
        acc += w / w.sum(); n += 1
    if n == 0:
        return np.nan, 0
    acc = acc - acc.min()
    c = np.cumsum(acc) / acc.sum()
    lo = int(np.searchsorted(c, q[0])); hi = int(np.searchsorted(c, q[1]))
    return float((hi - lo + 1) / kp), n
