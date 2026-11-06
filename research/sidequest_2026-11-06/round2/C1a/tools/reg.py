"""Hand-control registration helper for HEXAGON frames (round 2, C1a).
Model: mosaic px (X, Y) of a frame -> UTM 36N (E, N). Prior = affine in a JSON file.
panel NAME LAT LON [HALF_M] [ITEM] [MODEL.json] : writes pv/NAME.png with
   [HEX warped to a north-up UTM grid at 1 m/px | Esri z17 on the same grid | HEX at NCC best shift]
   grid every 100 m, labels in metres from the centre (x east, y south). Prints NCC best shift.
Control = feature seen at panel pixel (u, v) in HEX and (u', v') in Esri.
"""
import json, os, sys
import numpy as np, cv2, pyproj
sys.path.insert(0, "/home/claude/swarm")
import hexview as hv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tiles as T

utm = pyproj.Transformer.from_crs(32636, 4326, always_xy=True)
utm_inv = pyproj.Transformer.from_crs(4326, 32636, always_xy=True)
OFFS_ALL = json.load(open("/home/claude/swarm/branch_only/claude__novel-2026-10-31-E/research/novel_2026-10-31/E_hexagon_stereo/tile_offsets.json"))


def offsets(item):
    stem = hv.resolve(item)
    if stem in OFFS_ALL:
        return {k: v[:2] for k, v in OFFS_ALL[stem].items()}
    # fallback: nominal (tile width - overlap unknown) -> measure crudely: width spacing
    rec = hv.index()["items"][stem]
    o, X = {}, 0.0
    for t in rec["tiles"]:
        o[t["tile"]] = [X, 0.0]
        X += t["width"]
    return o


def read_window(item, X0, Y0, X1, Y1, scale=1.0):
    stem = hv.resolve(item)
    rec = hv.index()["items"][stem]
    OF = offsets(stem)
    oh, ow = int(round((Y1 - Y0) * scale)), int(round((X1 - X0) * scale))
    out = np.zeros((oh, ow), np.uint8)
    for t in rec["tiles"]:
        ox, oy = OF[t["tile"]]
        W, H = t["width"], t["height"]
        x0, x1 = max(0, X0 - ox), min(W, X1 - ox)
        y0, y1 = max(0, Y0 - oy), min(H, Y1 - oy)
        if x1 - x0 < 32 or y1 - y0 < 32:
            continue
        a = hv.box(stem, t["tile"], int(x0), int(y0), int(x1), int(y1), scale=scale, allow_protected=True)
        if a.ndim == 3:
            a = a[..., 0]
        px, py = int(round((x0 + ox - X0) * scale)), int(round((y0 + oy - Y0) * scale))
        hh, ww = min(a.shape[0], oh - py), min(a.shape[1], ow - px)
        reg = out[py:py + hh, px:px + ww]
        m = reg == 0
        reg[m] = a[:hh, :ww][m]
    return out


class Model:
    def __init__(self, path):
        g = json.load(open(path))
        self.g = g
        self.kind = g.get("kind", "affine")
        if self.kind == "affine":
            self.A = np.array(g["aff_px_to_utm36"])
        else:
            self.cE, self.cN = np.array(g["cE"]), np.array(g["cN"])
            self.x0, self.y0, self.s = g["norm"]
            self.deg = g["deg"]

    def terms(self, X, Y):
        x, y = (np.asarray(X, float) - self.x0) / self.s, (np.asarray(Y, float) - self.y0) / self.s
        cols = []
        for d in range(self.deg + 1):
            for i in range(d + 1):
                cols.append(x ** (d - i) * y ** i)
        return np.stack(cols, -1)

    def px2utm(self, X, Y):
        if self.kind == "affine":
            return self.A[0, 0] * X + self.A[0, 1] * Y + self.A[0, 2], self.A[1, 0] * X + self.A[1, 1] * Y + self.A[1, 2]
        D = self.terms(X, Y)
        return D @ self.cE, D @ self.cN

    def utm2px(self, E, N):
        if self.kind == "affine":
            M = self.A[:, :2]
            v = np.linalg.solve(M, np.stack([np.asarray(E, float) - self.A[0, 2], np.asarray(N, float) - self.A[1, 2]]).reshape(2, -1))
            return v[0].reshape(np.shape(E)), v[1].reshape(np.shape(E))
        A0 = np.array(self.g["affine_start"])
        M = A0[:, :2]
        E = np.asarray(E, float); N = np.asarray(N, float)
        v = np.linalg.solve(M, np.stack([E.ravel() - A0[0, 2], N.ravel() - A0[1, 2]]))
        X, Y = v[0], v[1]
        for _ in range(8):
            e, n = self.px2utm(X, Y)
            e1, n1 = self.px2utm(X + 1, Y); e2, n2 = self.px2utm(X, Y + 1)
            a, b, c, d = e1 - e, e2 - e, n1 - n, n2 - n
            det = a * d - b * c
            rx, ry = E.ravel() - e, N.ravel() - n
            X = X + (d * rx - b * ry) / det
            Y = Y + (-c * rx + a * ry) / det
        return X.reshape(E.shape), Y.reshape(E.shape)


def esri_utm(Ec, Nc, half, layer="esri", z=17):
    lon0, lat0 = utm.transform(Ec - half - 50, Nc - half - 50)
    lon1, lat1 = utm.transform(Ec + half + 50, Nc + half + 50)
    im, org = T.mosaic(layer, z, lat0, lon0, lat1, lon1)
    im = np.array(im)
    gy, gx = np.mgrid[0:2 * half, 0:2 * half].astype(np.float64)
    E = Ec - half + gx + 0.5
    N = Nc + half - gy - 0.5
    lon, lat = utm.transform(E, N)
    n = 2 ** z
    px = ((lon + 180) / 360 * n - org[0]) * 256
    py = ((1 - np.arcsinh(np.tan(np.radians(lat))) / np.pi) / 2 * n - org[1]) * 256
    return cv2.remap(im, px.astype(np.float32), py.astype(np.float32), cv2.INTER_LINEAR, borderValue=0)


def hex_utm(item, model, Ec, Nc, half):
    gy, gx = np.mgrid[0:2 * half, 0:2 * half].astype(np.float64)
    E = Ec - half + gx + 0.5
    N = Nc + half - gy - 0.5
    X, Y = model.utm2px(E, N)
    X0, X1 = int(np.floor(X.min())) - 4, int(np.ceil(X.max())) + 4
    Y0, Y1 = int(np.floor(Y.min())) - 4, int(np.ceil(Y.max())) + 4
    Y0c, X0c = max(0, Y0), max(0, X0)
    win = read_window(item, X0c, Y0c, X1, Y1, 1.0)
    return cv2.remap(win, (X - X0c).astype(np.float32), (Y - Y0c).astype(np.float32), cv2.INTER_LINEAR, borderValue=0), (X, Y)


def grad(a):
    a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 2.0)
    return np.hypot(cv2.Sobel(a, cv2.CV_32F, 1, 0), cv2.Sobel(a, cv2.CV_32F, 0, 1))


def ncc_shift(H, Ei, tpl_half, search):
    c = H.shape[0] // 2
    t = grad(H)[c - tpl_half:c + tpl_half, c - tpl_half:c + tpl_half]
    s = grad(Ei)[c - tpl_half - search:c + tpl_half + search, c - tpl_half - search:c + tpl_half + search]
    r = cv2.matchTemplate(s, t, cv2.TM_CCOEFF_NORMED)
    _, mx, _, loc = cv2.minMaxLoc(r)
    r2 = r.copy(); cv2.circle(r2, loc, 15, -1, -1)
    return loc[0] - search, loc[1] - search, float(mx), float(r2.max())


def draw_grid(a, half, step=50):
    a = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
    n = a.shape[0]
    for k in range(-half, half + 1, step):
        p = half + k
        col = (0, 0, 255) if k == 0 else (0, 200, 255)
        cv2.line(a, (p, 0), (p, n - 1), col, 1)
        cv2.line(a, (0, p), (n - 1, p), col, 1)
        cv2.putText(a, str(k), (p + 2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1) if k % 100 == 0 else None
        cv2.putText(a, str(k), (2, p - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1) if k % 100 == 0 else None
    return a


def panel(name, lat, lon, half=400, item="D3C1208-400636F014", mpath=None, tpl=150, search=None, outdir=None, clahe=True):
    model = Model(mpath or os.path.join(HERE, "..", "F014_3point_affine.json"))
    Ec, Nc = utm_inv.transform(lon, lat)
    H, (X, Y) = hex_utm(item, model, Ec, Nc, half)
    Ei = esri_utm(Ec, Nc, half)
    if clahe:
        cl = cv2.createCLAHE(2.0, (8, 8))
        H = cl.apply(H); Ei = cl.apply(Ei)
    search = search or min(half - tpl - 5, 250)
    dx, dy, pk, sec = ncc_shift(H, Ei, tpl, search)
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    Hs = cv2.warpAffine(H, M, H.shape[::-1])
    sep = np.full((2 * half, 6, 3), 255, np.uint8)
    out = np.hstack([draw_grid(H, half), sep, draw_grid(Ei, half)])
    cv2.putText(out, f"{item[:20]} prior", (5, 2 * half - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(out, f"NCC shift {dx},{dy} pk {pk:.2f}/{sec:.2f}", ((2 * half + 6) + 5, 2 * half - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    d = outdir or os.path.join(HERE, "..", "pv"); os.makedirs(d, exist_ok=True)
    cv2.imwrite(os.path.join(d, f"{name}.png"), out)
    cX, cY = model.utm2px(np.array([Ec]), np.array([Nc]))
    print(f"{name}: centre px ({float(cX[0]):.0f},{float(cY[0]):.0f}); NCC shift (m, x east / y south) {dx},{dy} peak {pk:.2f} second {sec:.2f}")
    return dict(name=name, lat=lat, lon=lon, E=Ec, N=Nc, X=float(cX[0]), Y=float(cY[0]), dx=dx, dy=dy, pk=pk, sec=sec)


def control_from_panel(model, Ec, Nc, half, u_hex, v_hex, u_esri, v_esri):
    """feature at (u_hex, v_hex) in HEX panel and (u_esri, v_esri) in Esri panel -> (X, Y, E, N)."""
    Eh, Nh = Ec - half + u_hex, Nc + half - v_hex
    X, Y = model.utm2px(np.array([Eh]), np.array([Nh]))
    Et, Nt = Ec - half + u_esri, Nc + half - v_esri
    return float(X[0]), float(Y[0]), Et, Nt


if __name__ == "__main__":
    a = sys.argv
    if a[1] == "panel":
        half = int(a[5]) if len(a) > 5 else 400
        item = a[6] if len(a) > 6 else "D3C1208-400636F014"
        mp = a[7] if len(a) > 7 else None
        panel(a[2], float(a[3]), float(a[4]), half, item, mp)
