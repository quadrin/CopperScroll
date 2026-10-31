"""Relief features for a letter window on a per-cut PS product.

Window: square of side 2 x letter height (Lh88) centred on the mapped letter centre, in the PS
reference frame. Inside the window the relief r (high-pass Frankot-Chellappa depth, sigma 6 px) is
normalised by its robust spread (median absolute deviation), so features are scale-free (they do not
depend on the unknown GBR/elevation scale). Groove = -r (engraved strokes are low).

Features (letter-frame coordinates: u = horizontal, toward the LEFT of the letter = reading direction;
v = vertical, down; both in letter heights, letter box = central 1 x 1 Lh square):
  f_base_rext   : groove along the base row (v in [0.35, 0.55]) just right of the right wall
                  (u in [-0.65, -0.45]) minus background - a base projecting right (bet's tail).
  f_br_corner   : groove at the bottom-right corner (u in [-0.5,-0.3], v in [0.3,0.5]) minus background.
  f_base_mean   : mean groove along the base row inside the box.
  f_left_gap    : HH: groove continuity of the left leg (u in [0.3,0.5]) in its upper part
                  (v in [-0.35,-0.05]) relative to the right leg at the same height (ratio of means).
  f_left_top    : HH: groove at the junction roof/left leg (u in [0.3,0.5], v in [-0.5,-0.3]).
  f_foot        : HH: groove below the right leg (taw foot to the left at bottom: u in [0.25,0.55], v in [0.3,0.55]).
  f_left_foot   : HH: groove beyond the left leg at base level (u in [0.50,0.75], v in [0.35,0.55]) minus
                  background - the leftward foot that distinguishes taw from het.
  f_contrast    : robust spread of raw relief in the window divided by the cut-wide spread (quality).
Missing (NaN) if less than 70% of the window lies in the strip mask.
"""
import numpy as np
from scipy import ndimage as ndi

SIGMA = 6.0
BOXES = {
    'f_base_rext': (-0.65, -0.45, 0.35, 0.55),
    'f_br_corner': (-0.50, -0.30, 0.30, 0.50),
    'f_base_mean': (-0.40, 0.40, 0.35, 0.55),
    'f_left_top': (0.30, 0.50, -0.50, -0.30),
    'f_foot': (0.25, 0.55, 0.30, 0.55),
    'f_left_foot': (0.50, 0.75, 0.35, 0.55),
    'left_upper': (0.30, 0.50, -0.35, -0.05),
    'right_upper': (-0.50, -0.30, -0.35, -0.05),
    'bg': None,
}


def window(r, m, cx, cy, lh, rot):
    """Sample a (2Lh x 2Lh) window, 41 x 41 samples, at letter centre; rot=180 flips."""
    n = 41
    t = np.linspace(-1.0, 1.0, n)
    U, V = np.meshgrid(t, t)
    # letter frame: u positive to the image left in an upright frame (reading direction)
    sgn = -1 if rot == 0 else 1
    X = cx + sgn * U * lh * (1)
    Y = cy + (1 if rot == 0 else -1) * V * lh
    rr = ndi.map_coordinates(np.nan_to_num(r, nan=0.0), [Y, X], order=1, cval=0.0)
    mm = ndi.map_coordinates(m.astype(float), [Y, X], order=0, cval=0.0) > 0.5
    return U, V, rr, mm


def feats(r, m, cx, cy, lh, rot, cut_spread):
    U, V, rr, mm = window(r, m, cx, cy, lh, rot)
    if mm.mean() < 0.7:
        return None
    med = np.median(rr[mm]); mad = np.median(np.abs(rr[mm] - med)) + 1e-9
    g = -(rr - med) / (1.4826 * mad)  # groove positive
    def box(b):
        u0, u1, v0, v1 = b
        s = mm & (U >= u0) & (U <= u1) & (V >= v0) & (V <= v1)
        return float(np.mean(g[s])) if s.sum() >= 3 else np.nan
    inner = (np.abs(U) <= 0.5) & (np.abs(V) <= 0.5)
    bg = float(np.mean(g[mm & ~inner])) if (mm & ~inner).sum() > 10 else 0.0
    out = {k: box(b) - bg for k, b in BOXES.items() if b is not None}
    lu, ru = out.pop('left_upper'), out.pop('right_upper')
    out['f_left_gap'] = lu - ru
    out['f_contrast'] = float(1.4826 * mad / (cut_spread + 1e-9))
    out['window_in_mask'] = float(mm.mean())
    return out
