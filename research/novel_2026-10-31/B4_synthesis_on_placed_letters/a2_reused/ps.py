"""A2 photometric stereo on registered full-resolution WSRP 1988 frames (semi-calibrated, titled azimuths).

Light model (exploratory design, carried over from round 1 as a NEW implementation):
- Azimuths from the frame titles, in image coordinates with x to the right and y UP:
  L/C/R x T: 135, 90, 45 deg; L/C/R x B: 225, 270, 315 deg; RT 90; RB 270; RET/RTC 90; REB/RBC 270.
  Other codes (FRS, RFR, RCS) are not used.
- One fixed elevation for all lights (ELEV_DEG). Each frame is divided by its median luminance inside the strip
  (equalises lamp power and exposure). Lambertian least squares gives g = albedo * n.
- Depth: Frankot-Chellappa integration of p = -nx/nz, q = -ny/nz inside the window; relief = depth minus its
  Gaussian low-pass (sigma = RELIEF_SIGMA_LH x letter height).
"""
import json
import numpy as np, cv2
from common import full_cached, HERE

AZ = {"RLT": 135, "RCT": 90, "RRT": 45, "RLB": 225, "RCB": 270, "RRB": 315,
      "RT": 90, "RB": 270, "RET": 90, "REB": 270, "RTC": 90, "RBC": 270}
ELEV_DEG = 30.0


def load_reg(cut):
    return json.load(open(f"{HERE}/reg/reg_cut{cut:02d}.json"))


MAX_CROSS_RESID_PX = 3.0  # a sign-free cross-group registration is accepted if its median patch residual is <= this


def usable_lights(reg):
    """Lights with a titled azimuth whose registration is accepted. A frame registered by the sign-free method is
    accepted only if its phase-correlation residual median is <= MAX_CROSS_RESID_PX with >= 20 patches; frames
    chained through a rejected anchor are dropped with it."""
    res = reg.get("residual", {})
    bad = set()
    for L, r in reg["frames"].items():
        if r.get("method", "").startswith("sign-free"):
            q = res.get(L, {})
            if not (q.get("median_px", 99) <= MAX_CROSS_RESID_PX and q.get("n_patches", 0) >= 20):
                bad.add(L)
    for L, r in reg["frames"].items():
        m = r.get("method", "")
        if any(f"to {b} " in m for b in bad):
            bad.add(L)
    return [L for L in reg["frames"] if L in AZ and L not in bad]


def light_vecs(lights, elev=ELEV_DEG):
    e = np.radians(elev)
    out = []
    for L in lights:
        a = np.radians(AZ[L])
        # image coords: x right, y DOWN -> flip the y component
        out.append([np.cos(e) * np.cos(a), -np.cos(e) * np.sin(a), np.sin(e)])
    return np.array(out)


_NORM = {}


def frame_norm(cut, L, reg):
    k = (cut, L)
    if k not in _NORM:
        g = np.asarray(full_cached(cut, L))
        x, y, w, h = reg["mask_ref_bbox"]
        A = np.asarray(reg["frames"][L]["A_ref2frame"])
        # sample the central 60% of the reference strip box, mapped into this frame
        xs = np.linspace(x + 0.2 * w, x + 0.8 * w, 40)
        ys = np.linspace(y + 0.2 * h, y + 0.8 * h, 120)
        X, Y = np.meshgrid(xs, ys)
        u = A[0, 0] * X + A[0, 1] * Y + A[0, 2]
        v = A[1, 0] * X + A[1, 1] * Y + A[1, 2]
        ok = (u >= 0) & (v >= 0) & (u < g.shape[1] - 1) & (v < g.shape[0] - 1)
        _NORM[k] = float(np.median(g[v[ok].astype(int), u[ok].astype(int)]))
    return _NORM[k]


def stack_window(cut, reg, x0, y0, w, h, lights=None):
    """Warp each frame's window into reference full-res coords [x0,x0+w) x [y0,y0+h)."""
    if lights is None:
        lights = usable_lights(reg)
    out = []
    for L in lights:
        A = np.asarray(reg["frames"][L]["A_ref2frame"], float)
        T = A.copy()
        T[:, 2] = A[:, 2] + A[:, 0] * x0 + A[:, 1] * y0  # window-local ref coords -> frame coords
        g = full_cached(cut, L)
        # read only the needed frame region
        cx = np.array([0, w, 0, w]); cy = np.array([0, 0, h, h])
        u = T[0, 0] * cx + T[0, 1] * cy + T[0, 2]; v = T[1, 0] * cx + T[1, 1] * cy + T[1, 2]
        ux0, uy0 = int(max(0, np.floor(u.min()) - 4)), int(max(0, np.floor(v.min()) - 4))
        ux1, uy1 = int(min(g.shape[1], np.ceil(u.max()) + 4)), int(min(g.shape[0], np.ceil(v.max()) + 4))
        if ux1 <= ux0 + 2 or uy1 <= uy0 + 2:
            out.append(np.full((h, w), np.nan, np.float32)); continue
        sub = np.asarray(g[uy0:uy1, ux0:ux1]).astype(np.float32)
        T2 = T.copy(); T2[0, 2] -= ux0; T2[1, 2] -= uy0
        wimg = cv2.warpAffine(sub, T2.astype(np.float32), (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                              borderMode=cv2.BORDER_CONSTANT, borderValue=np.nan)
        out.append(wimg / frame_norm(cut, L, reg))
    return np.stack(out), lights


SHADOW_FRAC = 0.25  # a light is dropped at a pixel where its normalised intensity is below this fraction
SAT_FRAC = 2.5      # ... or above this (specular / saturation)


def ps_normals(stack, lights, elev=ELEV_DEG):
    """Lambertian least squares per pixel, using only the lights that are neither in shadow nor saturated there.
    Pixels with fewer than 3 usable lights (or fewer than 2 azimuth sides) get NaN."""
    Lm = light_vecs(lights, elev)  # K x 3
    K, h, w = stack.shape
    I = stack.reshape(K, -1)
    use = np.isfinite(I) & (I > SHADOW_FRAC) & (I < SAT_FRAC)
    G = np.full((3, h * w), np.nan, np.float32)
    codes = np.zeros(h * w, np.int64)
    for k in range(K):
        codes |= (use[k].astype(np.int64) << k)
    for c in np.unique(codes):
        ks = [k for k in range(K) if (c >> k) & 1]
        if len(ks) < 3:
            continue
        sub = Lm[ks]
        if np.linalg.matrix_rank(sub, tol=1e-3) < 3:
            continue
        px = codes == c
        G[:, px] = np.linalg.pinv(sub) @ I[ks][:, px]
    rho = np.linalg.norm(G, axis=0)
    N = G / np.maximum(rho, 1e-6)
    N[2] = np.maximum(N[2], 0.05)
    return N.reshape(3, h, w), rho.reshape(h, w)


def frankot(p, q):
    h, w = p.shape
    wx = np.fft.fftfreq(w) * 2 * np.pi
    wy = np.fft.fftfreq(h) * 2 * np.pi
    WX, WY = np.meshgrid(wx, wy)
    P, Q = np.fft.fft2(p), np.fft.fft2(q)
    den = WX ** 2 + WY ** 2
    den[0, 0] = 1
    Z = (-1j * WX * P - 1j * WY * Q) / den
    Z[0, 0] = 0
    return np.real(np.fft.ifft2(Z))


def relief_window(cut, reg, cx, cy, half, lh, relief_sigma_lh=0.5, lights=None):
    """Return dict with normals, albedo, relief (high-passed depth, groove positive = deeper) for a square window
    of half-size `half` px centred at reference coords (cx, cy)."""
    x0, y0 = int(round(cx - half)), int(round(cy - half))
    w = h = 2 * half
    st, lights = stack_window(cut, reg, x0, y0, w, h, lights)
    N, rho = ps_normals(st, lights)
    valid = np.isfinite(N[0])
    p = -N[0] / N[2]
    q = N[1] / N[2]  # image y is down; q = dz/dy_up -> flip sign so depth is consistent in image coordinates
    p = np.clip(np.nan_to_num(p), -3, 3); q = np.clip(np.nan_to_num(q), -3, 3)
    # window: taper edges to reduce FFT wrap
    z = frankot(p, -q)
    zs = cv2.GaussianBlur(z.astype(np.float32), (0, 0), relief_sigma_lh * lh)
    relief = z - zs
    return {"N": N, "rho": rho, "relief": relief, "valid": valid, "lights": lights, "x0": x0, "y0": y0}
