"""blend.py NAME LAT LON HALF ITEM MODEL LAYER:Z dx,dy [dx,dy ...] : HEX (gray) with map ink (dark pixels of LAYER) in red, one tile per shift"""
import sys, os, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reg as R
a = sys.argv
name, lat, lon, half, item, mp = a[1], float(a[2]), float(a[3]), int(a[4]), a[5], a[6]
L, z = a[7].split(":")
m = R.Model(mp)
Ec, Nc = R.utm_inv.transform(lon, lat)
Mp = R.esri_utm(Ec, Nc, half, L, int(z))
ink = Mp < 140
tiles = []
for s in a[8:]:
    dx, dy = map(float, s.split(","))
    H, _ = R.hex_utm(item, m, Ec - dx, Nc + dy, half)
    H = cv2.createCLAHE(2.0, (8, 8)).apply(H)
    o = cv2.cvtColor(H, cv2.COLOR_GRAY2BGR)
    o[ink] = (0, 0, 255)
    o = cv2.resize(o, (700, 700), interpolation=cv2.INTER_AREA)
    cv2.putText(o, s, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    tiles.append(o)
rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
w = max(r.shape[1] for r in rows)
rows = [np.pad(r, ((0, 0), (0, w - r.shape[1]), (0, 0))) for r in rows]
cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pv", f"{name}_blend.png"), np.vstack(rows))
