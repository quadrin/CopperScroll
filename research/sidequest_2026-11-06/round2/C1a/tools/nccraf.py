"""nccraf.py LAT LON HALF ITEM MODEL LAYER:Z TPL SEARCH SIGMA -> best shift of HEX vs layer (m, x east, y south), with peak table"""
import sys, os, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reg as R
a = sys.argv
lat, lon, half, item, mp = float(a[1]), float(a[2]), int(a[3]), a[4], a[5]
L, z = a[6].split(":"); tpl, search, sig = int(a[7]), int(a[8]), float(a[9])
m = R.Model(mp)
Ec, Nc = R.utm_inv.transform(lon, lat)
H, _ = R.hex_utm(item, m, Ec, Nc, half)
E = R.esri_utm(Ec, Nc, half, L, int(z))
def prep(x, mode):
    x = cv2.GaussianBlur(x.astype(np.float32), (0, 0), sig)
    if mode == "g":
        return np.hypot(cv2.Sobel(x, cv2.CV_32F, 1, 0), cv2.Sobel(x, cv2.CV_32F, 0, 1))
    return x - cv2.GaussianBlur(x, (0, 0), 40)
c = half
for mode in ("g", "i"):
    h, e = prep(H, mode), prep(E, mode)
    t = h[c - tpl:c + tpl, c - tpl:c + tpl]
    s = e[c - tpl - search:c + tpl + search, c - tpl - search:c + tpl + search]
    for sign, tt in (("+", t), ("-", -t)):
        r = cv2.matchTemplate(s, tt, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(r)
        r2 = r.copy(); cv2.circle(r2, loc, 25, -1, -1)
        print(mode, sign, "shift", loc[0] - search, loc[1] - search, "peak %.3f second %.3f" % (mx, r2.max()))
        if mode == "g": break
