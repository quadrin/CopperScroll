"""F014 (June 1974 forward, north-up stored) mosaic reader + approximate georef from the E run,
refined against Esri by patch NCC. usage:
  python3 f014.py refine         -> geo_F014.json (polynomial mosaic px -> lat/lon)
  python3 f014.py crop LAT LON SIZE_M SCALE OUT.png [ITEM]   (ITEM default F014)
"""
import json, os, sys
import numpy as np, cv2, pyproj
sys.path.insert(0, "/home/claude/swarm")
import hexview as hv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tiles as T

HERE = os.path.dirname(os.path.abspath(__file__))
OFFS = {'a': [0.0, 0.0], 'b': [34992.0, 24.0], 'c': [70256.0, 32.0], 'd': [105120.0, 40.0], 'e': [140320.0, 48.0], 'f': [175368.0, 32.0], 'g': [210560.0, 24.0]}
AFF = np.array([[0.9194395608501509, -0.03210753691382706, 610283.581422256], [-0.032107537146657705, -0.9194395607337356, 3540166.1150804544]])
utm = pyproj.Transformer.from_crs(32636, 4326, always_xy=True)
utm_inv = pyproj.Transformer.from_crs(4326, 32636, always_xy=True)
ITEM = "D3C1208-400636F014"
W, H = 37280, 24668


def read_window(X0, Y0, X1, Y1, scale):
    oh, ow = int(round((Y1 - Y0) * scale)), int(round((X1 - X0) * scale))
    out = np.zeros((oh, ow), np.uint8)
    stem = hv.resolve(ITEM)
    for t, (ox, oy) in OFFS.items():
        x0, x1 = max(0, X0 - ox), min(W, X1 - ox)
        y0, y1 = max(0, Y0 - oy), min(H, Y1 - oy)
        if x1 - x0 < 64 or y1 - y0 < 64:
            continue
        a = hv.box(stem, t, int(x0), int(y0), int(x1), int(y1), scale=scale)
        px, py = int(round((x0 + ox - X0) * scale)), int(round((y0 + oy - Y0) * scale))
        hh, ww = min(a.shape[0], oh - py), min(a.shape[1], ow - px)
        reg = out[py:py + hh, px:px + ww]
        m = reg == 0
        reg[m] = a[:hh, :ww][m]
    return out


def aff_px2ll(X, Y):
    E = AFF[0, 0] * X + AFF[0, 1] * Y + AFF[0, 2]
    N = AFF[1, 0] * X + AFF[1, 1] * Y + AFF[1, 2]
    lon, lat = utm.transform(E, N)
    return lat, lon


def poly_terms(X, Y):
    x, y = (X - 110000) / 10000.0, (Y - 12000) / 10000.0
    return np.stack([np.ones_like(x), x, y, x * x, x * y, y * y], -1)


def refine():
    s = 1 / 16
    X0, X1, Y0, Y1 = 90000, 135000, 0, 24700
    A = read_window(X0, Y0, X1, Y1, s)
    lat0, lon0, lat1, lon1 = 31.62, 35.02, 32.02, 35.48
    z = 13
    E, org = T.mosaic("esri", z, lat0, lon0, lat1, lon1)
    E = np.array(E)
    # warp HEXAGON into the Esri grid using the E-run affine
    gy, gx = np.mgrid[0:E.shape[0], 0:E.shape[1]].astype(np.float64)
    lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * (org[1] + gy / 256) / 2 ** z))))
    lon = (org[0] + gx / 256) / 2 ** z * 360 - 180
    Eu, Nu = utm_inv.transform(lon, lat)
    M = np.array([[AFF[0, 0], AFF[0, 1]], [AFF[1, 0], AFF[1, 1]]])
    Mi = np.linalg.inv(M)
    dX = Mi[0, 0] * (Eu - AFF[0, 2]) + Mi[0, 1] * (Nu - AFF[1, 2])
    dY = Mi[1, 0] * (Eu - AFF[0, 2]) + Mi[1, 1] * (Nu - AFF[1, 2])
    mx, my = ((dX - X0) * s).astype(np.float32), ((dY - Y0) * s).astype(np.float32)
    Wp = cv2.remap(A, mx, my, cv2.INTER_LINEAR, borderValue=0)
    cv2.imwrite(os.path.join(HERE, "..", "f014_warp_esri13.png"), Wp)
    cv2.imwrite(os.path.join(HERE, "..", "esri13_big.png"), E)

    def grad(a):
        a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.5)
        gx_ = cv2.Sobel(a, cv2.CV_32F, 1, 0); gy_ = cv2.Sobel(a, cv2.CV_32F, 0, 1)
        return np.sqrt(gx_ ** 2 + gy_ ** 2)
    GA, GB = grad(Wp), grad(E)
    pts = []
    P, R = 96, 40
    for cy in range(P, E.shape[0] - P, 64):
        for cx in range(P, E.shape[1] - P, 64):
            if (Wp[cy - P // 2:cy + P // 2, cx - P // 2:cx + P // 2] == 0).mean() > 0.05:
                continue
            tpl = GA[cy - P // 2:cy + P // 2, cx - P // 2:cx + P // 2]
            srch = GB[cy - P // 2 - R:cy + P // 2 + R, cx - P // 2 - R:cx + P // 2 + R]
            if srch.shape != (P + 2 * R, P + 2 * R):
                continue
            r = cv2.matchTemplate(srch, tpl, cv2.TM_CCOEFF_NORMED)
            _, mxv, _, loc = cv2.minMaxLoc(r)
            r2 = r.copy(); cv2.circle(r2, loc, 6, -1, -1)
            second = r2.max()
            if mxv > 0.35 and mxv - second > 0.05:
                pts.append((cx, cy, loc[0] - R, loc[1] - R, mxv))
    pts = np.array(pts)
    print("patches", len(pts))
    # hexagon mosaic px of patch centre and the true esri pos
    cx, cy, dx, dy = pts[:, 0], pts[:, 1], pts[:, 2], pts[:, 3]
    Xh = mx[cy.astype(int), cx.astype(int)] / s + X0
    Yh = my[cy.astype(int), cx.astype(int)] / s + Y0
    ex, ey = cx + dx, cy + dy
    lat_t = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * (org[1] + ey / 256) / 2 ** z))))
    lon_t = (org[0] + ex / 256) / 2 ** z * 360 - 180
    Et, Nt = utm_inv.transform(lon_t, lat_t)
    D = poly_terms(Xh, Yh)
    keep = np.ones(len(D), bool)
    for it in range(5):
        cE, *_ = np.linalg.lstsq(D[keep], Et[keep], rcond=None)
        cN, *_ = np.linalg.lstsq(D[keep], Nt[keep], rcond=None)
        rr = np.hypot(D @ cE - Et, D @ cN - Nt)
        thr = max(3 * np.median(rr[keep]), 25)
        keep = rr < thr
        print(it, keep.sum(), "median resid m", float(np.median(rr[keep])), "p90", float(np.percentile(rr[keep], 90)))
    json.dump({"item": ITEM, "offsets": OFFS, "cE": cE.tolist(), "cN": cN.tolist(), "n": int(keep.sum()),
               "median_resid_m": float(np.median(rr[keep])), "p90_resid_m": float(np.percentile(rr[keep], 90)),
               "method": "E-run affine (stage1_geoloc fwd_mosaic_px_to_utm) as start; Esri z13 gradient patch NCC; quadratic poly mosaic px -> UTM36N",
               "pts": np.c_[Xh, Yh, Et, Nt][keep].tolist()}, open(os.path.join(HERE, "..", "geo_F014.json"), "w"))


def px2utm(X, Y, g):
    D = poly_terms(np.asarray(X, float), np.asarray(Y, float))
    return D @ np.array(g["cE"]), D @ np.array(g["cN"])


def utm2px(E, N, g):
    # invert by Newton from affine guess
    M = np.array([[AFF[0, 0], AFF[0, 1]], [AFF[1, 0], AFF[1, 1]]]); Mi = np.linalg.inv(M)
    X, Y = Mi @ (np.array([E, N]) - AFF[:, 2])
    for _ in range(20):
        e, n = px2utm(X, Y, g)
        h = 1.0
        e1, n1 = px2utm(X + h, Y, g); e2, n2 = px2utm(X, Y + h, g)
        J = np.array([[e1 - e, e2 - e], [n1 - n, n2 - n]])
        d = np.linalg.solve(J, np.array([E - e, N - n]))
        X, Y = X + d[0], Y + d[1]
    return float(X), float(Y)


if __name__ == "__main__":
    if sys.argv[1] == "refine":
        refine()
