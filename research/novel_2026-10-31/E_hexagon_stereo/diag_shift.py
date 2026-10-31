"""Exploratory diagnostic: correlation of the 30 m disparity grid with GLO-30 over a wide
shift range (+/-4 km), using the stage-1 geolocation. Prints the best shift and NCC."""
import json
import sys

import cv2
import numpy as np

import common as C
import stereo_local as S

pre = sys.argv[1]  # e.g. explore_JUN74_TRAIN
r = json.load(open(f"{C.HERE}/results/{pre}.json"))
s1 = json.load(open(f"{C.HERE}/stage1_geoloc.json"))[r["pair"]]
M = np.array(s1["fwd_mosaic_px_to_utm"])
h = np.load(f"{C.PROD}/{pre}_h30.npy")
# rebuild cell centres -> UTM (stage-1 mapping only)
bs, sc = r["cell_px"], 0.5
Rm = np.array(r["geo"]["Rm"]); Ri = cv2.invertAffineTransform(Rm)
ny, nx = h.shape
yy, xx = np.mgrid[0:ny, 0:nx]
xr, yr = (xx + 0.5) * bs, (yy + 0.5) * bs
xw = Ri[0, 0] * xr + Ri[0, 1] * yr + Ri[0, 2]
yw = Ri[1, 0] * xr + Ri[1, 1] * yr + Ri[1, 2]
Xm, Ym = r["wF"][0] + xw / sc, r["wF"][1] + yw / sc
E = M[0, 0] * Xm + M[0, 1] * Ym + M[0, 2]
N = M[1, 0] * Xm + M[1, 1] * Ym + M[1, 2]
c = r["coef"]
d = (h - c[0]) / c[1]  # approximately the disparity relief
ok = np.isfinite(d)
g = S.GloSampler(res=30.0, region=(E[ok].min() - 5000, N[ok].min() - 5000, E[ok].max() + 5000, N[ok].max() + 5000))
best = None
for th in np.arange(-6, 6.1, 1.0):
    t = np.radians(th)
    cE, cN = E[ok].mean(), N[ok].mean()
    E2 = cE + np.cos(t) * (E - cE) - np.sin(t) * (N - cN)
    N2 = cN + np.sin(t) * (E - cE) + np.cos(t) * (N - cN)
    for k in (0.92, 0.96, 1.0, 1.04, 1.08):
        E3, N3 = cE + k * (E2 - cE), cN + k * (N2 - cN)
        for tx in np.arange(-4000, 4001, 150):
            for ty in np.arange(-4000, 4001, 150):
                pass
        # vectorised over shifts via matchTemplate on a regular UTM grid
        res = 30.0
        gridE = np.arange(E3[ok].min() - 4000, E3[ok].max() + 4000, res)
        gridN = np.arange(N3[ok].max() + 4000, N3[ok].min() - 4000, -res)
        # rasterise d into a UTM grid
        ci = ((E3 - gridE[0]) / res).round().astype(int)
        ri = ((gridN[0] - N3) / res).round().astype(int)
        T = np.full((len(gridN), len(gridE)), np.nan, np.float32)
        T[ri[ok], ci[ok]] = -d[ok]
        rr, cc = np.where(np.isfinite(T))
        T = T[rr.min():rr.max() + 1, cc.min():cc.max() + 1]
        Mk = np.isfinite(T).astype(np.float32)
        T = np.nan_to_num(T, nan=float(np.nanmean(T)))
        Z = g.sample(*np.meshgrid(gridE, gridN))
        Z = np.nan_to_num(Z, nan=float(np.nanmean(Z))).astype(np.float32)
        m = cv2.matchTemplate(Z, T.astype(np.float32), cv2.TM_CCORR_NORMED, mask=Mk) if False else cv2.matchTemplate(Z, T.astype(np.float32), cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(m)
        sh = ((loc[0] - cc.min()) * res, -(loc[1] - rr.min()) * res)
        if best is None or mx > best[0]:
            best = (mx, th, k, sh)
print("best NCC", best)
