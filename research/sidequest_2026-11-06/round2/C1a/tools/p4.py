"""p4.py NAME LAT LON HALF ITEM MODEL [DXm DYm] [layers...] : HEX (prior, + manual shift DX east, DY south in m) | layers, all on one UTM grid, 50 m grid"""
import sys, os, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reg as R
a = sys.argv
name, lat, lon, half, item, mp = a[1], float(a[2]), float(a[3]), int(a[4]), a[5], a[6]
dx, dy = float(a[7]), float(a[8])
layers = a[9:] or ["pal20k:16", "esri:17"]
m = R.Model(mp)
Ec, Nc = R.utm_inv.transform(lon, lat)
H, _ = R.hex_utm(item, m, Ec - dx, Nc + dy, half)   # feature at true (Ec,Nc) appears at panel centre when shift is right
H = cv2.createCLAHE(2.0, (8, 8)).apply(H)
P = [R.draw_grid(H, half, 100)]
for s in layers:
    L, z = s.split(":")
    E = R.esri_utm(Ec, Nc, half, L, int(z))
    P += [np.full((2 * half, 6, 3), 255, np.uint8), R.draw_grid(E, half, 100)]
out = np.hstack(P)
if out.shape[1] > 2400:
    f = 2400 / out.shape[1]; out = cv2.resize(out, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pv", f"{name}_p4.png"), out)
X, Y = m.utm2px(np.array([Ec - dx]), np.array([Nc + dy]))
print(name, "HEX px at centre", float(X[0]), float(Y[0]))
