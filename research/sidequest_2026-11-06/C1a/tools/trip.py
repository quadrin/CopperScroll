"""Triptych for a lat/lon: RAF 1940s (z16) | HEXAGON F014 Jun 1974 | Esri modern (z17).
usage: python3 trip.py NAME LAT LON HALF_M [HEXSCALE] [DX DY]
DX DY: manual pixel correction (full-res) to the 3-point affine.
Writes ../private-view/NAME_trip.png (private: may show unrecorded features)."""
import json, os, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f014 as F, tiles as T
HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, "..", "geo_F014_3pt.json")))
A = np.array(G["aff_px_to_utm36"])


def ll2px(lat, lon):
    E, N = F.utm_inv.transform(lon, lat)
    X, Y = np.linalg.solve(A[:, :2], np.array([E, N]) - A[:, 2])
    return X, Y


def px2ll(X, Y):
    E, N = A[:, :2] @ np.array([X, Y]) + A[:, 2]
    lon, lat = F.utm.transform(E, N)
    return lat, lon


if __name__ == "__main__":
    name, lat, lon, half = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    hs = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
    dx, dy = (float(sys.argv[6]), float(sys.argv[7])) if len(sys.argv) > 7 else (0, 0)
    X, Y = ll2px(lat, lon); X += dx; Y += dy
    hx, hy = half / 1.0, half / 0.84
    h = F.read_window(int(X - hx), int(max(0, Y - hy)), int(X + hx), int(min(24668, Y + hy)), hs)
    dlat = half / 111320; dlon = half / (111320 * np.cos(np.radians(lat)))
    tgt = 700
    h = cv2.resize(h, (tgt, tgt), interpolation=cv2.INTER_AREA)
    ims = []
    for L, z in (("raf", 16), ("esri", 17)):
        im, org = T.mosaic(L, z, lat - dlat, lon - dlon, lat + dlat, lon + dlon)
        ims.append(cv2.resize(np.array(im), (tgt, tgt), interpolation=cv2.INTER_AREA))
    sep = np.full((tgt, 6), 255, np.uint8)
    out = np.hstack([ims[0], sep, h, sep, ims[1]])
    for i, t in enumerate(["RAF 1940s z16", "HEXAGON F014 1974-06-25", "Esri modern z17"]):
        cv2.putText(out, t, (10 + i * 706, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
    d = os.path.join(HERE, "..", "pv"); os.makedirs(d, exist_ok=True)
    cv2.imwrite(os.path.join(d, f"{name}_trip.png"), out)
    print(name, "F014 mosaic px", int(X), int(Y), "window m", 2 * half, "hex scale", hs)
