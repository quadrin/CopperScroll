"""B4 letter model: multi-light templates learned at placed TRAIN letters, scored at a placed letter position.

Template of letter form c on cut k, channel h (patch side WIN_LH * RES, template side TPL_LH * RES, centred):
  T_all[c,h]   = mean over all TRAIN letters of form c (any cut having channel h) of the standardised central patch;
  T_cut[k,c,h] = (sum over TRAIN letters of form c on cut k + KAPPA * T_all[c,h]) / (n_k,c + KAPPA), re-standardised.
Raw score of form c at a placed letter on cut k: mean over the channels present on cut k (and in CHANNEL_SET) of the
NCC map (OpenCV TM_CCOEFF_NORMED) of T_cut[k,c,h] over the patch, then the maximum over the shift window
|dx| <= SHIFT_X_LH * Lh, |dy| <= SHIFT_Y_LH * Lh around the mapped centre (the frozen local search; every candidate
form takes its own maximum over the same window).
Calibrated score (CALIB = "z"): z = (raw - mu_c) / sd_c, mu_c and sd_c = mean and SD of the raw score of form c over
the TRAIN letters of every OTHER form (all cuts). This removes differences in the general response level of
templates built from different numbers of letters.
"""
import numpy as np, cv2
import b4lib as B

KAPPA = 5.0
SHIFT_X_LH = 0.2
SHIFT_Y_LH = 0.15
CHANNEL_SET = ("CT", "CB", "LT", "LB", "RT", "RB", "TB", "LR")  # frozen (exploratory choice V12)
CALIB = "z"

NP = int(round(B.WIN_LH * B.RES))
NT = int(round(B.TPL_LH * B.RES))
O = (NP - NT) // 2  # offset of the template window inside the patch at zero shift
SX = int(round(SHIFT_X_LH * B.RES)); SY = int(round(SHIFT_Y_LH * B.RES))
CH_IDX = [B.CHANNELS.index(h) for h in CHANNEL_SET]


def std(a):
    a = a - a.mean()
    return a / (a.std() + 1e-6)


def centre(p):
    return std(p[O:O + NT, O:O + NT])


ALIGN_ITERS = 2   # template congealing: re-centre each TRAIN patch on its form's template, re-average (frozen, V12)


def crop_at(p, dy, dx):
    return std(p[O + dy:O + dy + NT, O + dx:O + dx + NT])


class Templates:
    def __init__(self, F, forms, cuts):
        """F: (n, C, NP, NP) TRAIN patches; forms: letter forms; cuts: cut numbers."""
        self.all, self.cut = {}, {}
        forms = np.asarray(forms); cuts = np.asarray(cuts)
        shift = {i: (0, 0) for i in range(len(F))}
        for c in sorted(set(forms)):
            idx = np.nonzero(forms == c)[0]
            for it in range(ALIGN_ITERS + 1):
                for h in CH_IDX:
                    sel = [i for i in idx if np.isfinite(F[i, h, 0, 0])]
                    if sel:
                        self.all[(c, h)] = std(np.mean([crop_at(F[i, h], *shift[i]) for i in sel], axis=0))
                if it == ALIGN_ITERS:
                    break
                for i in idx:  # best shift of each TRAIN patch against the current scroll-wide template
                    acc, n = None, 0
                    for h in CH_IDX:
                        if (c, h) in self.all and np.isfinite(F[i, h, 0, 0]):
                            sub = F[i, h, O - SY:O + NT + SY, O - SX:O + NT + SX].astype(np.float32)
                            m = cv2.matchTemplate(sub, self.all[(c, h)].astype(np.float32), cv2.TM_CCOEFF_NORMED)
                            acc = m if acc is None else acc + m; n += 1
                    if n:
                        iy, ix = np.unravel_index(int(np.argmax(acc)), acc.shape)
                        shift[i] = (iy - SY, ix - SX)
            for k in sorted(set(cuts)):
                for h in CH_IDX:
                    if (c, h) not in self.all:
                        continue
                    sel = [i for i in np.nonzero((forms == c) & (cuts == k))[0] if np.isfinite(F[i, h, 0, 0])]
                    s = np.sum([crop_at(F[i, h], *shift[i]) for i in sel], axis=0) if sel else 0.0
                    self.cut[(k, c, h)] = std(s + KAPPA * self.all[(c, h)])
        self.forms = sorted(set(forms))

    def get(self, k, c, h):
        if (k, c, h) in self.cut:
            return self.cut[(k, c, h)]
        return self.all.get((c, h))


def raw_score(T, patch, k, c):
    """patch: (C, NP, NP) for a letter on cut k. Returns max over the shift window of the channel-mean NCC."""
    acc, n = None, 0
    for h in CH_IDX:
        if not np.isfinite(patch[h, 0, 0]):
            continue
        t = T.get(k, c, h)
        if t is None:
            continue
        sub = patch[h, O - SY:O + NT + SY, O - SX:O + NT + SX].astype(np.float32)
        m = cv2.matchTemplate(sub, t.astype(np.float32), cv2.TM_CCOEFF_NORMED)
        acc = m if acc is None else acc + m
        n += 1
    if n == 0:
        return np.nan
    return float((acc / n).max())


class Model:
    def __init__(self, F, forms, cuts):
        self.T = Templates(F, forms, cuts)
        forms = np.asarray(forms)
        self.mu, self.sd = {}, {}
        if CALIB == "z":
            for c in self.T.forms:
                v = [raw_score(self.T, F[i], cuts[i], c) for i in range(len(F)) if forms[i] != c]
                v = np.array([x for x in v if np.isfinite(x)])
                self.mu[c], self.sd[c] = float(v.mean()), float(v.std() + 1e-6)

    def score(self, patch, k, c):
        r = raw_score(self.T, patch, k, c)
        if CALIB == "z":
            return (r - self.mu[c]) / self.sd[c]
        return r


SHIFT_MODE = "own"   # "own": each form takes its own maximum over the shift window; "shared": one shift per position


def ncc_maps(T, patch, k, c):
    """Channel-mean NCC map over the shift window, or None."""
    acc, n = None, 0
    for h in CH_IDX:
        if not np.isfinite(patch[h, 0, 0]):
            continue
        t = T.get(k, c, h)
        if t is None:
            continue
        sub = patch[h, O - SY:O + NT + SY, O - SX:O + NT + SX].astype(np.float32)
        m = cv2.matchTemplate(sub, t.astype(np.float32), cv2.TM_CCOEFF_NORMED)
        acc = m if acc is None else acc + m
        n += 1
    return None if n == 0 else acc / n


def scores_at(model, patch, k, forms_set):
    """Scores of every form in forms_set at one placed letter.
    "own": model.score per form (each form takes its own maximum over the shift window; CALIB applies).
    "shared": one shift for the position = argmax of the mean of the forms' NCC maps (symmetric in the forms, so it
    does not depend on which form is the edition reading); each form is then scored by its NCC at that shift."""
    if SHIFT_MODE == "own":
        return {c: model.score(patch, k, c) for c in forms_set}
    maps = {c: ncc_maps(model.T, patch, k, c) for c in forms_set}
    mean = np.mean([m for m in maps.values()], axis=0)
    iy, ix = np.unravel_index(int(np.argmax(mean)), mean.shape)
    return {c: float(m[iy, ix]) for c, m in maps.items()}
