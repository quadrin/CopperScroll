"""B2 forward model: letter-template synthesis of a line band in each light frame, scored by local
alignment (analysis by synthesis, new model; not the round-1 model).

Per frame (no cross-frame registration, see prep2.py):
  z = clip((I - G_s(I)) / sqrt(G_s((I - G_s(I))^2)), -3, 3), s = 1.2 Lh; zero outside the strip mask.
Letter templates per (column, light class, letter), Ht = 1.3 Lh high and w_c = glyph width x Lh wide:
  T = normalised mean of the column's aligned TRAINING patches, shrunk toward the scroll-wide mean with
  weight KS, which is shrunk toward the RENDERED template with weight KS.
  Rendered template = groove model: skeleton polylines (glyphs.json: 17 letters from the strip-13 tracing
  of column VII, 10 font fallbacks), V or U cross-section of half-width hw (Lh units), shading
  -(dh/dx lx + dh/dy ly) + gam * h for the light class direction (lx, ly), sign fitted on training.
Line band score for a candidate string in one frame of one cut = best local alignment (free start and end
in the string; the string is read right to left) of letter templates placed left of each other with gaps
in [GMIN, GMAX] Lh inside words and [GMIN, GWORD] Lh across a word space; each placed letter scores
z-score of the pooled NCC (max over +-DY Lh vertically and +-0.1 Lh horizontally)
against that letter's pooled-NCC distribution over the strip interior of the same frame, minus TAU. Line score = sum over the column's cuts and frames, at the
row chosen per cut and frame by the mean over all candidates (candidate-symmetric registration).
"""
import json, os, numpy as np, cv2
SP = '/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
STRIPS = SP + '/products/B2/strips'
TOF = dict(zip('כמנפצ', 'ךםןףץ'))
LCLASS = {'RCT': 'T', 'RT': 'T', 'RCB': 'B', 'RB': 'B', 'RLT': 'LT', 'RRT': 'RT_', 'RLB': 'LB', 'RRB': 'RB_'}
LDIR = {'T': (0, -1), 'B': (0, 1), 'LT': (-.707, -.707), 'RT_': (.707, -.707), 'LB': (-.707, .707), 'RB_': (.707, .707)}
GL = json.load(open(f'{HERE}/glyphs.json'))


class P:  # parameters (defaults; the frozen values are in frozen_params2.json)
    LH = 70.0      # letter height in work px (0.5 of full resolution)
    HT = 1.3       # template height / Lh
    HW = 0.08      # groove half-width / Lh
    PROF = 'V'
    GAM = 0.5
    SIGN = 1.0
    GMIN, GMAX, GWORD = -0.1, 0.6, 1.6
    DY = 0.15
    TAU = 0.0       # in z units of each letter's pooled background NCC distribution
    KS = 3.0
    ROWA, ROWB = 0.05, 0.90   # nominal row: y = H (ROWA + ROWB (l - 0.5) / N)
    WIN = 1.0                 # row search window, +- WIN pitch
    GSTEP = 2
    YSTEP = 6
    NPASS = 2


def load_cut(cut):
    d = np.load(f'{STRIPS}/ct{cut:02d}.npz')
    return {k: (d[k], d[k + '_mask']) for k in d.files if not k.endswith('_mask')}


def prep(img, mask, lh):
    f = img.astype(np.float32)
    s = 1.2 * lh
    hp = f - cv2.GaussianBlur(f, (0, 0), s)
    sd = np.sqrt(cv2.GaussianBlur(hp * hp, (0, 0), s)) + 1.0
    z = np.clip(hp / sd, -3, 3)
    m = cv2.erode(mask.astype(np.uint8), np.ones((9, 9), np.uint8))
    z[m == 0] = 0
    return cv2.GaussianBlur(z, (0, 0), 1.0)


def glyph_w(c, lh):
    return max(6, int(round(GL[c]['w'] * lh)) + 4)


def render(c, lclass, lh, p=P):
    g = GL[c]
    w = glyph_w(c, lh); ht = int(round(p.HT * lh))
    oy = int(round((p.HT - 1.0) / 2 * lh))  # body (0..1) centred in the template
    canvas = np.ones((ht, w), np.uint8)
    for poly in g['polys']:
        pts = np.array([[2 + x * lh, oy + y * lh] for x, y in poly], np.float32)
        pts = np.round(pts).astype(np.int32)
        if len(pts) == 1:  # font fallback glyphs are skeleton point clouds
            cv2.circle(canvas, (int(pts[0, 0]), int(pts[0, 1])), 1, 0, -1)
        else:
            cv2.polylines(canvas, [pts], False, 0, 1)
    d = cv2.distanceTransform(canvas, cv2.DIST_L2, 5) / (p.HW * lh)
    d = np.minimum(d, 10.0)
    if p.PROF == 'V':
        h = -np.clip(1 - d, 0, None)
    else:
        h = -np.sqrt(np.clip(1 - d * d, 0, None))
    hy, hx = np.gradient(h)
    lx, ly = LDIR[lclass]
    t = p.SIGN * (-(hx * lx + hy * ly) * (1.0 / max(p.HW, 1e-3)) + p.GAM * h)
    return norm(t)


def norm(t):
    t = t - t.mean(); s = t.std()
    return (t / s).astype(np.float32) if s > 1e-6 else t.astype(np.float32)


def base(c):
    return {v: k for k, v in TOF.items()}.get(c, c)


def ncc_map(z, t):
    """NCC of template t over image z (valid), returns array (H-ht+1, W-w+1)"""
    if z.shape[0] < t.shape[0] or z.shape[1] < t.shape[1]:
        return None
    return cv2.matchTemplate(z, t, cv2.TM_CCOEFF_NORMED)


def letters(s):
    """reading-order letters with a flag 'word boundary before this letter'"""
    out = []; wb = False
    for ch in s:
        if ch == ' ':
            wb = True; continue
        if 'א' <= ch <= 'ת':
            out.append((ch, wb)); wb = False
    return out


def align(S, seq, widths, lh, p=P):
    """S: dict letter -> score row (len W-w_c+1, NCC-TAU, -inf where invalid) at one band row.
    seq: [(letter, wordbreak_before)], widths: letter -> w. Local alignment, right-to-left.
    Returns best score and the letter placements of the best run."""
    W = max(len(v) + widths[k] - 1 for k, v in S.items())
    NEG = -1e9
    prev = None; best = (0.0, None)
    tb = []
    for i, (c, wb) in enumerate(seq):
        sc = np.full(W, NEG, np.float32)
        r = S[c]; sc[:len(r)] = r
        if prev is None:
            f = sc.copy(); arg = np.full(W, -1, np.int32)
        else:
            gmax = p.GWORD if wb else p.GMAX
            gs = np.arange(int(round(p.GMIN * lh)), int(round(gmax * lh)) + 1, p.GSTEP)
            wi = widths[c]
            bestprev = np.full(W, NEG, np.float32); arg = np.full(W, -1, np.int32)
            for g in gs:
                sh = wi + g  # previous letter's left edge = x + w_i + g
                cand = np.full(W, NEG, np.float32)
                if sh >= 0:
                    if sh < W: cand[:W - sh] = prev[sh:]
                else:
                    cand[-sh:] = prev[:W + sh]
                upd = cand > bestprev
                bestprev[upd] = cand[upd]; arg[upd] = (np.arange(W) + sh)[upd]
            start = bestprev <= 0
            f = sc + np.where(start, 0, bestprev)
            arg[start] = -1
        tb.append(arg)
        m = int(np.argmax(f))
        if f[m] > best[0]: best = (float(f[m]), (i, m))
        prev = f
    if best[1] is None:
        return 0.0, []
    i, x = best[1]; place = []
    while i >= 0 and x >= 0:
        place.append((i, x)); x = int(tb[i][x]); i -= 1
    return best[0], place[::-1]


class Band:
    """precomputed NCC maps of one frame of one cut for a set of templates (one column)"""
    def __init__(self, z, temps, lh, p=P):
        self.z = z; self.lh = lh; self.p = p
        self.maps = {}; self.pmaps = {}; self.mu = {}; self.sd = {}
        valid = None
        dy = int(round(p.DY * lh)); dx = int(round(0.1 * lh))
        ker = np.ones((2 * dy + 1, 2 * dx + 1), np.uint8)
        for c, t in temps.items():
            r = ncc_map(z, t)
            if r is None:
                self.maps[c] = None; continue
            r = np.nan_to_num(r, nan=0.0, posinf=0.0, neginf=0.0)
            # background statistics of this letter's NCC over the strip interior: the score of a placed
            # letter is its z-score against them (removes letter-specific offsets of template sharpness)
            if valid is None or valid.shape != r.shape:
                inside = (np.abs(z) > 1e-3).astype(np.float32)
                cov = cv2.blur(inside, (t.shape[1], t.shape[0]))
                ch, cw = r.shape
                oy, ox = t.shape[0] // 2, t.shape[1] // 2
                valid = cov[oy:oy + ch, ox:ox + cw] > 0.9
            # pooled map = max over the allowed vertical (+-DY Lh) and horizontal (+-0.1 Lh) freedom;
            # its background mean and SD standardise the letter score, so every letter's score has the
            # same null distribution after the max (a sharp template's rougher NCC map gains nothing)
            pm = cv2.dilate(r, ker)
            v = pm[valid] if valid.any() else pm.ravel()
            self.mu[c] = float(v.mean()); self.sd[c] = float(v.std()) + 1e-6
            self.maps[c] = r.astype(np.float16)
            self.pmaps[c] = pm.astype(np.float16)
        self.widths = {c: t.shape[1] for c, t in temps.items()}
        self.ht = next(iter(temps.values())).shape[0]

    def rowscores(self, y, chars):
        """y = band centre row; returns dict letter -> NCC - TAU along x, max over vertical shift"""
        y0 = int(round(y - self.ht / 2))
        out = {}
        for c in chars:
            m = self.pmaps.get(c)
            if m is None:
                out[c] = np.full(1, -1e9, np.float32); continue
            if not (0 <= y0 < m.shape[0]):
                out[c] = np.full(m.shape[1], -1e9, np.float32); continue
            out[c] = (m[y0].astype(np.float32) - self.mu[c]) / self.sd[c] - self.p.TAU
        return out

    def score(self, y, s):
        seq = letters(s)
        if not seq: return 0.0, []
        S = self.rowscores(y, {c for c, _ in seq})
        return align(S, seq, self.widths, self.lh, self.p)
