"""Warp an F014 window into an Esri mosaic grid using the E-run affine, then measure the residual
shift by gradient NCC over a grid of large patches; fit a local affine correction.
usage: python3 warp_local.py LAT0 LON0 LAT1 LON1 Z OUTPREFIX
"""
import json, sys, os
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f014 as F, tiles as T

lat0, lon0, lat1, lon1, z, pre = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
E, org = T.mosaic("esri", z, lat0, lon0, lat1, lon1); E = np.array(E)
gy, gx = np.mgrid[0:E.shape[0], 0:E.shape[1]].astype(np.float64)
lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * (org[1] + gy / 256) / 2 ** z))))
lon = (org[0] + gx / 256) / 2 ** z * 360 - 180
Eu, Nu = F.utm_inv.transform(lon, lat)
Mi = np.linalg.inv(F.AFF[:, :2])
dX = Mi[0, 0] * (Eu - F.AFF[0, 2]) + Mi[0, 1] * (Nu - F.AFF[1, 2])
dY = Mi[1, 0] * (Eu - F.AFF[0, 2]) + Mi[1, 1] * (Nu - F.AFF[1, 2])
mpp = 156543.034 / 2 ** z * np.cos(np.radians((lat0 + lat1) / 2))
s = min(1.0, 0.92 / mpp * 1.0)  # read at about the esri pixel size
pad = 3000
X0, X1 = int(dX.min()) - pad, int(dX.max()) + pad
Y0, Y1 = max(0, int(dY.min()) - pad), min(24668, int(dY.max()) + pad)
A = F.read_window(X0, Y0, X1, Y1, s)
mx, my = ((dX - X0) * s).astype(np.float32), ((dY - Y0) * s).astype(np.float32)
Wp = cv2.remap(A, mx, my, cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR, borderValue=0)


def grad(a):
    a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 2.0)
    return np.hypot(cv2.Sobel(a, cv2.CV_32F, 1, 0), cv2.Sobel(a, cv2.CV_32F, 0, 1))


GA, GB = grad(Wp), grad(E)
P, R = 200, 120
pts = []
for cy in range(P // 2 + R, E.shape[0] - P // 2 - R, 100):
    for cx in range(P // 2 + R, E.shape[1] - P // 2 - R, 100):
        tpl = GA[cy - P // 2:cy + P // 2, cx - P // 2:cx + P // 2]
        if (Wp[cy - P // 2:cy + P // 2, cx - P // 2:cx + P // 2] == 0).mean() > 0.02:
            continue
        sr = GB[cy - P // 2 - R:cy + P // 2 + R, cx - P // 2 - R:cx + P // 2 + R]
        r = cv2.matchTemplate(sr, tpl, cv2.TM_CCOEFF_NORMED)
        _, v, _, loc = cv2.minMaxLoc(r)
        pts.append((cx, cy, loc[0] - R, loc[1] - R, v))
pts = np.array(pts)
print("patches", len(pts))
if len(pts):
    good = pts[pts[:, 4] > 0.2]
    print("good", len(good), "median shift px", np.median(good[:, 2:4], 0) if len(good) else None)
    for p in pts:
        print("%d %d %+d %+d %.2f" % tuple(p))
cv2.imwrite(pre + "_hex.png", Wp); cv2.imwrite(pre + "_esri.png", E)
json.dump({"bbox": [lat0, lon0, lat1, lon1], "z": z, "origin": org, "X0Y0": [X0, Y0], "s": s,
           "pts": pts.tolist()}, open(pre + "_warp.json", "w"))
