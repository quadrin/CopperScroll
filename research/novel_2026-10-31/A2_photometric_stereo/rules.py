"""A2 letter rules: class-mean template (difference of class means) on PS feature maps.

For a rule (A vs B) trained on items X_A, X_B (feature vectors from features() in controls.py, restricted to the
channels of the chosen VARIANT): w = mean(X_A) - mean(X_B); t = 0.5 * (mean(X_A) + mean(X_B)) . w;
call A if x . w > t, else B. Shift tolerance: x is taken at the integer shift (dx, dy) in [-S, S]^2 grid cells that
maximises the correlation with the pooled class mean (class-agnostic alignment).
Rules: BK (ב vs כ), HE_HET (ה vs ח), HET_TAW (ח vs ת). Training hets serve both het rules.
"""
import numpy as np

RULE_CLASSES = {"BK": ("ב", "כ"), "HE_HET": ("ה", "ח"), "HET_TAW": ("ח", "ת")}
VARIANTS = {"nx_ny_alb": [0, 1, 2], "nx_ny": [0, 1], "ny": [1], "nx": [0], "alb": [2], "tb": [3]}


def align(F, ref, S):
    """F: C x G x G; ref: C x G x G pooled mean. Return the shifted F (zero-padded) with the best correlation."""
    best, bv = F, -np.inf
    C, Gh, Gw = F.shape
    for dy in range(-S, S + 1):
        for dx in range(-S, S + 1):
            Fs = np.roll(np.roll(F, dy, axis=1), dx, axis=2)
            v = float((Fs * ref).sum())
            if v > bv:
                bv, best = v, Fs
    return best


def train_rule(FA, FB, S=1):
    ref = np.concatenate([FA, FB]).mean(axis=0)
    FA = np.stack([align(f, ref, S) for f in FA]); FB = np.stack([align(f, ref, S) for f in FB])
    mA, mB = FA.mean(axis=0), FB.mean(axis=0)
    w = (mA - mB).ravel()
    t = 0.5 * float(((mA + mB).ravel() * w).sum())
    return {"ref": ref, "w": w, "t": t, "S": S}


def apply_rule(model, F):
    x = align(F, model["ref"], model["S"]).ravel()
    return float(x @ model["w"] - model["t"])
