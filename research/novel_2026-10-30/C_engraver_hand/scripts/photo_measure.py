"""Automatic per-frame measurement on USC public previews of the 1988 WSRP photographs (original cut segments, recto).
Outputs numbers only. No image is written to the repository.
Per frame:
  scale   : ruler period. The ruler is the 5-px column whose vertical grey profile is black-and-white (>=20 % of rows
            < 60 and >=20 % > 190 grey) and has the strongest autocorrelation peak at lag 40-120 px; the peak lag = 2 cm (alternating 1 cm black/white blocks) -> px_per_cm.
  strip   : the widest contiguous run of image columns whose mean grey (rows 10-90 %) is in [20, 170] and whose
            vertical-gradient energy exceeds the frame median, excluding +-25 px around the ruler column.
            Inner 70 % of that run is analysed.
  pitch_cm: line pitch = lag of the strongest autocorrelation peak of the detrended row profile of |d/dy| (Sobel,
            Gaussian sigma 1) over the inner strip, searched in 0.9-2.6 cm; acf_pitch = its height.
  adv_cm  : horizontal letter advance = lag of the strongest autocorrelation peak of the detrended column profile of
            |d/dx|, computed per text band (rows within +-0.35 pitch of each row-profile maximum) and averaged,
            searched in 0.35-1.6 cm; acf_adv = its height.
"""
import sys, csv, numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.signal import find_peaks

def acf(x):
    x = np.asarray(x, float); x = x - x.mean(); a = np.correlate(x, x, 'full')[len(x) - 1:]
    return a / a[0] if a[0] > 0 else a

def peak_in(a, lo, hi):
    lo = max(1, int(lo)); hi = min(len(a) - 1, int(hi))
    if hi <= lo + 2: return None, None
    pk, _ = find_peaks(a[lo:hi])
    if len(pk) == 0: return None, None
    k = pk[np.argmax(a[lo:hi][pk])] + lo
    return int(k), float(a[k])

def measure(path):
    g = np.asarray(Image.open(path).convert('L'), float); H, W = g.shape
    r0, r1 = int(0.1 * H), int(0.9 * H)
    cm = g[r0:r1].mean(0)
    # ruler
    best = (0, None, None)
    for x in range(2, W - 2):
        col = g[r0:r1, x - 2:x + 3].mean(1)
        if col.std() < 30: continue
        # ruler blocks are black and white: require >=20 % of rows below 60 and >=20 % above 190
        if (col < 60).mean() < 0.2 or (col > 190).mean() < 0.2: continue
        k, a = peak_in(acf(col), 40, 120)
        if k and a > best[0]: best = (a, x, k)
    acf_r, rx, k = best
    if rx is None: return dict(ok=0, why='no ruler')
    pxcm = k / 2.0
    # strip
    gy = np.abs(ndi.sobel(ndi.gaussian_filter(g, 1.0), axis=0))
    en = gy[r0:r1].mean(0)
    good = (cm > 20) & (cm < 170) & (en > np.median(en))
    good[max(0, rx - 25):rx + 25] = False
    runs = []; s = None
    for x in range(W + 1):
        if x < W and good[x]:
            s = x if s is None else s
        elif s is not None:
            runs.append((x - s, s, x)); s = None
    if not runs: return dict(ok=0, why='no strip')
    w, a0, a1 = max(runs)
    if w < 1.5 * pxcm: return dict(ok=0, why='strip too narrow', px_per_cm=pxcm)
    m = int(0.15 * w); x0, x1 = a0 + m, a1 - m
    S = ndi.gaussian_filter(g[:, x0:x1], 1.0)
    prof = np.abs(ndi.sobel(S, axis=0)).mean(1)[r0:r1]
    prof = prof - ndi.uniform_filter1d(prof, int(3 * pxcm))
    kp, ap = peak_in(acf(prof), 0.9 * pxcm, 2.6 * pxcm)
    if kp is None: return dict(ok=0, why='no pitch peak', px_per_cm=pxcm)
    # horizontal advance within text bands
    gx = np.abs(ndi.sobel(S, axis=1))
    maxima, _ = find_peaks(prof, distance=max(3, int(0.7 * kp)))
    advs = []
    for y in maxima:
        y = y + r0; b0, b1 = max(0, y - int(0.35 * kp)), min(H, y + int(0.35 * kp))
        cp = gx[b0:b1].mean(0); cp = cp - ndi.uniform_filter1d(cp, int(2 * pxcm))
        ka, aa = peak_in(acf(cp), 0.35 * pxcm, 1.6 * pxcm)
        if ka: advs.append((ka, aa))
    adv = np.median([a for a, _ in advs]) / pxcm if advs else np.nan
    aadv = np.median([b for _, b in advs]) if advs else np.nan
    return dict(ok=1, why='', px_per_cm=pxcm, acf_ruler=acf_r, ruler_x=rx, strip_x0=a0, strip_x1=a1,
                strip_w_cm=w / pxcm, pitch_cm=kp / pxcm, acf_pitch=ap, adv_cm=adv, acf_adv=aadv, n_bands=len(advs))

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p.split('/')[-1], {k: (round(v, 3) if isinstance(v, float) else v) for k, v in measure(p).items()})
