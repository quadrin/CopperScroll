"""Frame-level helpers: tile offsets along x (tiles lie side by side) and windows that
may straddle two tiles. Offsets are measured by phase correlation of tile edges at 1/8."""
import json
import os

import cv2
import numpy as np

import common as C

OFFS = os.path.join(C.HERE, "tile_offsets.json")


def tiles_of(item):
    return [t["tile"] for t in C.hv.index()["items"][C.hv.resolve(item)]["tiles"]]


def _edge(item, tile, side, width, scale):
    stem, rec, t = C.hv.tile_rec(item, tile)
    W, H = t["width"], t["height"]
    x0, x1 = (W - width, W) if side == "right" else (0, width)
    a = C.hv.box(stem, tile, x0, 0, x1, H, scale=scale)
    C.log_read(stem, tile, x0, 0, x1, H, scale, "tile overlap measurement (code only)")
    return a.astype(np.float32), W, H


def measure_offsets(item, scale=1 / 8, width=8000):
    """Offset of each tile's x origin in a frame mosaic (stored orientation), plus dy."""
    stem = C.hv.resolve(item)
    allo = json.load(open(OFFS)) if os.path.exists(OFFS) else {}
    if stem in allo:
        return allo[stem]
    tl = tiles_of(stem)
    res = {tl[0]: [0.0, 0.0]}
    X = 0.0
    Y = 0.0
    for a, b in zip(tl[:-1], tl[1:]):
        ra, Wa, Ha = _edge(stem, a, "right", width, scale)
        lb, Wb, Hb = _edge(stem, b, "left", width, scale)
        h = min(ra.shape[0], lb.shape[0])
        # search: template = central part of lb's left strip within ra
        tw = lb[:, : int(lb.shape[1] * 0.25)]
        tw = tw[int(h * 0.1):int(h * 0.9)]
        r = cv2.matchTemplate(ra[:h], tw, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(r)
        # tile b x=0 corresponds to tile a x = (Wa - width) + loc_x/scale ; dy = loc_y/scale - 0.1h/scale
        ox = (Wa - width) + loc[0] / scale
        oy = (loc[1] - int(h * 0.1)) / scale
        X += ox
        Y += oy
        res[b] = [X, Y, float(mx)]
    allo[stem] = res
    json.dump(allo, open(OFFS, "w"), indent=1)
    return res


def read_window(item, X0, Y0, X1, Y1, scale=1.0, purpose="stereo window"):
    """Window in frame-mosaic coordinates (stored orientation). Returns uint8 array at `scale`."""
    stem = C.hv.resolve(item)
    offs = measure_offsets(stem)
    oh, ow = int(round((Y1 - Y0) * scale)), int(round((X1 - X0) * scale))
    out = np.zeros((oh, ow), np.uint8)
    filled = np.zeros((oh, ow), bool)
    for tile in tiles_of(stem):
        ox, oy = offs[tile][0], offs[tile][1]
        _, rec, t = C.hv.tile_rec(stem, tile)
        x0, x1 = max(0, X0 - ox), min(t["width"], X1 - ox)
        y0, y1 = max(0, Y0 - oy), min(t["height"], Y1 - oy)
        if x1 - x0 < 64 or y1 - y0 < 64:
            continue
        a = C.hv.box(stem, tile, int(x0), int(y0), int(x1), int(y1), scale=scale)
        C.log_read(stem, tile, int(x0), int(y0), int(x1), int(y1), scale, purpose)
        px, py = int(round((x0 + ox - X0) * scale)), int(round((y0 + oy - Y0) * scale))
        hh, ww = min(a.shape[0], oh - py), min(a.shape[1], ow - px)
        sel = ~filled[py:py + hh, px:px + ww]  # first tile wins in the overlap
        out[py:py + hh, px:px + ww][sel] = a[:hh, :ww][sel]
        filled[py:py + hh, px:px + ww] |= a[:hh, :ww] > 0
    return out
