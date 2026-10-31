"""C3 copper measurement at a mapped letter centre (1988 reference-frame coordinates, full resolution).

Inputs per letter: cut, (x88, y88) mapped centre, lh88 = nominal letter height in 1988 px (A2: copy-photo letter
height of the column / placement scale; a per-column scale prior, not a per-letter quantity). Nothing from the
drawing's box size enters.

Signal: Sobel gradient magnitude of each registered light (A2 stack_window, frame-median normalised), Gaussian
pre-blur SIGMA px, divided by its 95th percentile in the window. Gradient magnitude does not change sign when the
lamp moves (as in A2). Group images: T = mean of top-lit lights, B = mean of bottom-lit lights, ALL = mean of all.

Pitch (copper): row profile (mean over |x - x88| <= PITCH_HALFW * lh) over |y - y88| <= PITCH_HALFH * lh, smoothed
(Gaussian 0.06 lh), minus its mean; normalised autocorrelation; pitch = lag of the highest autocorrelation value with
lag in [PITCH_MIN, PITCH_MAX] * lh, refined by a parabola; a maximum on the range boundary gives no pitch (NaN).

Extent (copper letter height): row profile E(y) = mean over |x - x88| <= EXT_HALFW * lh, for |y - y88| <= 0.5 * pitch
(clipping by the neighbouring lines: the window never extends beyond half a pitch from the centre). E' = max(E -
percentile(E, BG_PCT), 0). Extent = y(Q_HI) - y(Q_LO) of the cumulative distribution of E' (linear interpolation).
h = extent / pitch.
"""
import numpy as np, cv2
from scipy.ndimage import gaussian_filter1d
from c3lib import stack_window, usable_lights, reg

TOP = ("RLT", "RCT", "RRT", "RT", "RET", "RTC")
BOT = ("RLB", "RCB", "RRB", "RB", "REB", "RBC")

DEFAULT = dict(SIGMA=3.0, PITCH_HALFW=1.5, PITCH_HALFH=2.8, PITCH_MIN=1.4, PITCH_MAX=3.0,
               EXT_HALFW=0.35, BG_PCT=20.0, Q_LO=0.10, Q_HI=0.90)


def grad_stack(cut, x88, y88, halfw, halfh, sigma):
    R = reg(cut)
    lights = usable_lights(R)
    x0, y0 = int(round(x88 - halfw)), int(round(y88 - halfh))
    w, h = 2 * int(round(halfw)), 2 * int(round(halfh))
    st, lights = stack_window(cut, R, x0, y0, w, h, lights)
    G = []
    for k in range(len(lights)):
        a = st[k]
        ok = np.isfinite(a)
        if ok.mean() < 0.5:
            G.append(np.full(a.shape, np.nan, np.float32)); continue
        a = np.where(ok, a, np.nanmedian(a)).astype(np.float32)
        g = cv2.GaussianBlur(a, (0, 0), sigma)
        gm = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
        okd = cv2.erode(ok.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
        if okd.sum() < 100:
            G.append(np.full(a.shape, np.nan, np.float32)); continue
        gm = gm / (np.percentile(gm[okd], 95) + 1e-6)
        gm[~okd] = np.nan
        G.append(gm)
    return np.stack(G), lights, (x0, y0)


def group_mean(G, lights, group):
    idx = [i for i, L in enumerate(lights) if (group == "ALL" or (group == "T" and L in TOP) or (group == "B" and L in BOT))]
    if not idx:
        return None
    sub = G[idx]
    with np.errstate(all="ignore"):
        m = np.nanmean(sub, axis=0)
    return m


def pitch_from(img, lh, p):
    H, W = img.shape
    cx = W // 2
    hw = int(p["PITCH_HALFW"] * lh)
    prof = np.nanmean(img[:, max(0, cx - hw):cx + hw], axis=1)
    if not np.isfinite(prof).all():
        good = np.isfinite(prof)
        if good.mean() < 0.8:
            return np.nan, np.nan
        prof = np.interp(np.arange(H), np.where(good)[0], prof[good])
    prof = gaussian_filter1d(prof.astype(np.float64), 0.06 * lh)
    prof = prof - prof.mean()
    ac = np.correlate(prof, prof, mode="full")[H - 1:]
    ac = ac / (ac[0] + 1e-9)
    lo, hi = int(p["PITCH_MIN"] * lh), min(int(p["PITCH_MAX"] * lh), H - 2)
    if hi <= lo + 2:
        return np.nan, np.nan
    seg = ac[lo:hi + 1]
    # local maxima inside the range
    k = np.argmax(seg)
    j = lo + k
    if j <= lo or j >= hi:
        return np.nan, float(seg[k])  # peak on the boundary: no periodicity found inside the range
    y1, y2, y3 = ac[j - 1], ac[j], ac[j + 1]
    den = y1 - 2 * y2 + y3
    off = 0.5 * (y1 - y3) / den if den != 0 else 0.0
    return float(j + off), float(y2)


def extent_from(img, lh, pitch, p):
    H, W = img.shape
    cx, cy = W // 2, H // 2
    hw = max(2, int(p["EXT_HALFW"] * lh))
    hh = int(0.5 * pitch)
    sub = img[cy - hh:cy + hh, cx - hw:cx + hw]
    prof = np.nanmean(sub, axis=1)
    if not np.isfinite(prof).all():
        good = np.isfinite(prof)
        if good.mean() < 0.8:
            return np.nan
        prof = np.interp(np.arange(len(prof)), np.where(good)[0], prof[good])
    prof = gaussian_filter1d(prof.astype(np.float64), 0.03 * lh)
    e = np.maximum(prof - np.percentile(prof, p["BG_PCT"]), 0)
    if e.sum() <= 0:
        return np.nan
    c = np.cumsum(e) / e.sum()
    ys = np.arange(len(e)) + 0.5
    ylo = np.interp(p["Q_LO"], c, ys)
    yhi = np.interp(p["Q_HI"], c, ys)
    return float(yhi - ylo)


def extent_mss(img, lh, pitch, p):
    """Alternative extent rule (explored): the contiguous run of rows maximising sum(E - tau),
    tau = percentile(E, MSS_PCT) of the clipped central profile (maximum-sum segment)."""
    H, W = img.shape
    cx, cy = W // 2, H // 2
    hw = max(2, int(p["EXT_HALFW"] * lh))
    hh = int(0.5 * pitch)
    prof = np.nanmean(img[cy - hh:cy + hh, cx - hw:cx + hw], axis=1)
    if not np.isfinite(prof).all():
        good = np.isfinite(prof)
        if good.mean() < 0.8:
            return np.nan
        prof = np.interp(np.arange(len(prof)), np.where(good)[0], prof[good])
    prof = gaussian_filter1d(prof.astype(np.float64), 0.03 * lh)
    d = prof - np.percentile(prof, p["MSS_PCT"])
    best, cur, s0, bs, be = -1e18, 0.0, 0, 0, 0
    for i, v in enumerate(d):
        if cur <= 0:
            cur, s0 = v, i
        else:
            cur += v
        if cur > best:
            best, bs, be = cur, s0, i
    return float(be - bs + 1)


def measure_letter(cut, x88, y88, lh, p=DEFAULT, groups=("ALL", "T", "B")):
    """Pitch from the ALL-light image (required); extent of each light group clipped at half that pitch;
    h_g = extent_g / pitch. T and B are the two independent light halves used for the reliability gate."""
    halfw = max(p["PITCH_HALFW"], p["EXT_HALFW"]) * lh + 4
    halfh = p["PITCH_HALFH"] * lh
    G, lights, _ = grad_stack(cut, x88, y88, halfw, halfh, p["SIGMA"])
    out = {"n_lights": len(lights), "lights": ";".join(lights)}
    imgs = {g: group_mean(G, lights, g) for g in groups}
    pc, pk = pitch_from(imgs["ALL"], lh, p) if imgs.get("ALL") is not None else (np.nan, np.nan)
    out["pitch"] = pc; out["acpk"] = pk
    for g in groups:
        if imgs[g] is None or not np.isfinite(pc):
            out[f"ext_{g}"] = np.nan; out[f"h_{g}"] = np.nan
            continue
        ex = extent_from(imgs[g], lh, pc, p)
        out[f"ext_{g}"] = ex
        out[f"h_{g}"] = ex / pc if np.isfinite(ex) else np.nan
    return out
