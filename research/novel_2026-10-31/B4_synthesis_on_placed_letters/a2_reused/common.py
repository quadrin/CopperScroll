"""Shared paths and helpers for A2 (photometric stereo on the full-resolution WSRP 1988 frames).

All bucket reads go through hexview.py (SHA-256 56b21cb0...0236, observed 31 Oct 2026).
Image arrays are cached in the scratchpad, never in the repository.
"""
import os, sys
SP = "/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad"
sys.path.insert(0, SP + "/tools/hexview")
import hexview as hv  # noqa: E402
PROD = SP + "/products/A2"
CACHE = SP + "/a2work/cache"
os.makedirs(PROD, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def frames_for_cut(cut):
    ix = hv.index()["items"]
    pre = f"usc:DSS_3Q15_CT{cut}_"
    return sorted(k[len(pre):-2] for k in ix if k.startswith(pre))


def item(cut, light):
    return f"usc:DSS_3Q15_CT{cut}_{light}_T"


def overview_cached(cut, light, scale=0.125):
    import numpy as np
    p = f"{CACHE}/ov_{cut}_{light}_{scale:.4f}.npy"
    if os.path.exists(p):
        return np.load(p)
    a = hv.overview(item(cut, light), "-", scale=scale)
    np.save(p, a)
    return a


def full_cached(cut, light):
    """Full-resolution luminance (uint8, ITU-R 601 weights) of a frame, cached as .npy in the scratchpad."""
    import numpy as np
    p = f"{CACHE}/gray_{cut}_{light}.npy"
    if not os.path.exists(p):
        _, _, t = hv.tile_rec(item(cut, light), "-")
        a = hv.box(item(cut, light), "-", 0, 0, t["width"], t["height"])
        if a.ndim == 3:
            a = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]).round().astype(np.uint8)
        np.save(p, a)
    return np.load(p, mmap_mode="r")


def gridview(img, x0, y0, path, step=100, scale=1.0):
    """Save a crop with a labelled full-res pixel grid (for locating letters by eye). Scratchpad only."""
    import numpy as np, cv2
    a = np.asarray(img, dtype=np.uint8)
    if scale != 1.0:
        a = cv2.resize(a, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    if a.ndim == 2:
        a = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
    a = np.ascontiguousarray(a)
    H, W = a.shape[:2]
    gx0 = (int(x0) // step + 1) * step
    for gx in range(gx0, int(x0 + W / scale), step):
        u = int((gx - x0) * scale)
        cv2.line(a, (u, 0), (u, H - 1), (0, 255, 255), 1)
        cv2.putText(a, str(gx), (u + 2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
    gy0 = (int(y0) // step + 1) * step
    for gy in range(gy0, int(y0 + H / scale), step):
        v = int((gy - y0) * scale)
        cv2.line(a, (0, v), (W - 1, v), (0, 255, 255), 1)
        cv2.putText(a, str(gy), (2, v - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
    cv2.imwrite(path, a)
