"""Forward model + frozen-form likelihood for analysis by synthesis on 3Q15 (direction B).

Physical model (per strip = one registered multi-light stack of the 1988 WSRP USC previews):
  surface z(x,y) = s(x,y) [smooth curvature, removed by high-pass] - depth * P(d(x,y)/hw)  [engraved grooves]
                   + corrosion texture (treated as i.i.d. Gaussian residual after high-pass)
  d = distance to the glyph skeleton of the candidate string; P = V profile (1-u) or U profile sqrt(1-u^2).
  Lambertian shading, small-slope: I_f = alb*(l_z - l_x z_x - l_y z_y) + ambient-occlusion/dirt term in the
  groove (c_f * groove) + offset. After high-pass, frame f is linear in the regressors [1, z_x, z_y, groove]
  with unknown per-frame coefficients = the frame's light vector (fitted by least squares, the SAME freedom
  for every candidate). Specular term: not used (option off; see PROTOCOL).
Likelihood: per frame Gaussian residual with fitted variance -> log L = -(n/2) log(RSS_f / SST_f) summed over
frames; maximised over a horizontal text offset t (any position of the line on the strip) and a small
vertical offset dy. Same search for every candidate.
Saw kerf (0.15 mm) = 0.44 px at 0.34 mm/px: below one preview pixel; not modelled except that a strip's
visible text is a contiguous window of the line.
"""
import json, os, numpy as np, cv2
from scipy.signal import correlate
HERE = os.path.dirname(os.path.abspath(__file__))
PRIV = '/root/novel/private_outputs/B/stacks'
GLY = json.load(open(os.path.join(HERE, 'glyphs.json')))
FINAL = {'ך': 'כ', 'ם': 'מ', 'ן': 'ן', 'ף': 'פ', 'ץ': 'ץ'}
DEFAULT = dict(rho=0.52, hw=0.09, prof='V', hp=1.6, gap=0.22, space=0.45, dys=(-0.12, 0.0, 0.12), band=0.62)

def clean(s):
    return ''.join(ch for ch in s if ch in GLY or ch == ' ' or ch in FINAL)

def load_stack(cut, flip, P):
    d = np.load(f'{PRIV}/cut{cut:02d}.npz')
    S = d['stack'].astype(np.float32); M = d['mask'].astype(np.uint8)
    if flip: S = S[:, ::-1, ::-1].copy(); M = M[::-1, ::-1].copy()
    M = cv2.erode(M, np.ones((7, 7), np.uint8)).astype(bool)
    return S, M, list(d['labels'])

def highpass(img, sigma):
    return img - cv2.GaussianBlur(img, (0, 0), sigma)

def prep_obs(S, M, sp, P):
    """high-pass every frame at sigma = hp * letter height, normalise by in-mask std"""
    h = P['rho'] * sp; out = []
    for f in S:
        f2 = np.where(M, f, f[M].mean())
        g = highpass(f2, P['hp'] * h)
        g = g / (g[M].std() + 1e-6)
        out.append(g * M)
    return np.array(out, np.float32)

def render_line(text, h, P):
    """height map of the whole line (RTL). returns regressors (gx, gy, groove) and canvas width"""
    text = clean(text)
    ss = 4  # supersampling
    H = h * ss
    widths = []
    for ch in text:
        if ch == ' ': widths.append(None); continue
        g = GLY.get(ch) or GLY.get(FINAL.get(ch, ch))
        widths.append(g['w'])
    total = sum((w + P['gap']) if w is not None else P['space'] for w in widths)
    Wc = int(np.ceil(total * H)) + 4 * ss
    top_pad = int(0.6 * H); Hc = int(2.0 * H) + top_pad
    sk = np.zeros((Hc, Wc), np.uint8)
    cur = Wc - 2 * ss
    for ch, w in zip(text, widths):
        if w is None: cur -= P['space'] * H; continue
        g = GLY.get(ch) or GLY.get(FINAL.get(ch, ch))
        x0 = cur - w * H
        for poly in g['polys']:
            pts = np.array([[x0 + x * H, top_pad + y * H] for x, y in poly])
            if len(pts) == 1:
                cv2.circle(sk, tuple(np.round(pts[0]).astype(int)), ss // 2, 255, -1)
            else:
                cv2.polylines(sk, [np.round(pts).astype(np.int32)], False, 255, 1)
        cur -= (w + P['gap']) * H
    dist = cv2.distanceTransform((sk == 0).astype(np.uint8), cv2.DIST_L2, 5) / ss  # in native px
    hw = max(P['hw'] * h, 0.6)
    u = np.clip(dist / hw, 0, 1)
    prof = (1 - u) if P['prof'] == 'V' else np.sqrt(np.clip(1 - u * u, 0, 1))
    depth = cv2.resize(prof.astype(np.float32), (Wc // ss, Hc // ss), interpolation=cv2.INTER_AREA)
    z = -depth
    zx = cv2.Sobel(z, cv2.CV_32F, 1, 0, ksize=3) / 8; zy = cv2.Sobel(z, cv2.CV_32F, 0, 1, ksize=3) / 8
    sig = P['hp'] * h
    regs = [highpass(zx, sig), highpass(zy, sig), highpass(depth, sig)]
    # vertical reference: body centre row in native px
    yc = (top_pad + 0.5 * H) / ss
    return regs, yc

def fit_scores(obs, M, regs, yc, ycen, sp, P):
    """sliding least-squares fit. obs: F x H x W high-passed frames. returns best score, (dy, t)."""
    F, Hs, Ws = obs.shape
    best = (-np.inf, None)
    half = int(round(P['band'] * sp))
    for dyf in P['dys']:
        y = int(round(ycen + dyf * sp))
        y0, y1 = y - half, y + half
        if y0 < 0 or y1 > Hs: 
            y0c, y1c = max(y0, 0), min(y1, Hs)
        else: y0c, y1c = y0, y1
        if y1c - y0c < half: continue
        O = obs[:, y0c:y1c, :]; Mb = M[y0c:y1c, :].astype(np.float32)
        n = Mb.sum()
        if n < 50: continue
        # rendered rows aligned: canvas row r corresponds to strip row y0c + (r - (yc - (y - y0c)))...
        ry0 = int(round(yc - (y - y0c))); ry1 = ry0 + (y1c - y0c)
        R = []
        for g in regs:
            pad_top = max(0, -ry0); pad_bot = max(0, ry1 - g.shape[0])
            gg = np.pad(g, ((pad_top, pad_bot), (0, 0)))[ry0 + pad_top: ry1 + pad_top]
            # pad horizontally so that the window can slide fully off both ends
            gg = np.pad(gg, ((0, 0), (Ws, Ws)))
            R.append(gg.astype(np.float32))
        def xc(a, b):  # sum over rows of 1D correlation: out[t] = sum a * b[:, t:t+Ws]
            return correlate(b, a, mode='valid', method='fft')[0]
        k = 3
        # Gram components
        S1 = n
        Sj = [xc(Mb, R[j]) for j in range(k)]
        Sjk = {}
        for i in range(k):
            for j in range(i, k):
                Sjk[(i, j)] = xc(Mb, R[i] * R[j])
        T = len(Sj[0])
        G = np.zeros((T, k + 1, k + 1), np.float64)
        G[:, 0, 0] = S1
        for j in range(k): G[:, 0, j + 1] = G[:, j + 1, 0] = Sj[j]
        for (i, j), v in Sjk.items(): G[:, i + 1, j + 1] = G[:, j + 1, i + 1] = v
        G += np.eye(k + 1)[None] * 1e-3 * n
        Ginv = np.linalg.inv(G)
        tot = np.zeros(T)
        for f in range(F):
            Of = O[f] * Mb
            b = np.zeros((T, k + 1)); b[:, 0] = Of.sum()
            for j in range(k): b[:, j + 1] = xc(Of, R[j])
            sso = (Of * O[f]).sum()
            sst = sso - Of.sum() ** 2 / n
            expl = np.einsum('ti,tij,tj->t', b, Ginv, b)
            rss = np.maximum(sso - expl, 1e-6 * sst)
            tot += -(n / 2) * np.log(rss / sst)
        tmax = int(np.argmax(tot))
        if tot[tmax] > best[0]: best = (float(tot[tmax]), (dyf, tmax - Ws))
    return best

def row_profile(obs, M):
    e = np.abs(obs).mean(0)
    # groove energy minus horizontal-edge-free baseline
    num = (e * M).sum(1); den = M.sum(1) + 1e-6
    return num / den

def comb_fit(prof, N, sp_range):
    """text-agnostic: periodic comb with N teeth maximising mean energy. returns (y_first, sp)"""
    best = (-1, None)
    L = len(prof); p = (prof - prof.mean()) / (prof.std() + 1e-6)
    for sp in np.arange(sp_range[0], sp_range[1], 0.5):
        for y0 in np.arange(0, L - (N - 1) * sp * 0.5, 1.0):
            ys = y0 + sp * np.arange(N)
            ys = ys[ys < L - 1]
            if len(ys) < 0.6 * N: break
            v = np.interp(ys, np.arange(L), p).mean()
            if v > best[0]: best = (v, (float(y0), float(sp)))
    return best[1]

from scipy.signal import fftconvolve
def _xc2(A, R):
    """2-D valid cross-correlation: out[y,t] = sum A[y+r, t+c] * R[r,c]"""
    return fftconvolve(A, R[::-1, ::-1], mode='valid')

def fit_map(obs, M, regs, yc, sp, P):
    """Whole-strip version of fit_scores: for every row y (centre of the band) the log-likelihood maximised
    over the horizontal offset t. Same model and freedom as fit_scores (per-frame least squares on
    [1, gx, gy, groove]; band half-height = band * sp). Returns (score[y], t_best[y])."""
    F, Hs, Ws = obs.shape
    half = int(round(P['band'] * sp)); bh = 2 * half + 1
    r0 = int(round(yc)) - half
    R = []
    for g in regs:
        pt, pb = max(0, -r0), max(0, r0 + bh - g.shape[0])
        gg = np.pad(g, ((pt, pb), (0, 0)))[r0 + pt: r0 + pt + bh]
        R.append(gg.astype(np.float64))
    Wc = R[0].shape[1]
    pad = ((half, half), (Wc, Wc))
    Mp = np.pad(M.astype(np.float64), pad)
    ones = np.ones((bh, Ws + 2 * Wc - (Ws + Wc) + 0))[:, :1]
    k = 3
    n2 = _xc2(Mp, np.ones((bh, Wc)))          # band pixel count per (y,t) under canvas footprint? use full band
    nfull = _xc2(np.pad(M.astype(np.float64), ((half, half), (0, 0))), np.ones((bh, Ws)))[:, 0]  # (Hs,)
    shape = _xc2(Mp, R[0]).shape
    G = np.zeros(shape + (k + 1, k + 1))
    G[..., 0, 0] = nfull[:, None]
    for j in range(k):
        v = _xc2(Mp, R[j]); G[..., 0, j + 1] = G[..., j + 1, 0] = v
    for i in range(k):
        for j in range(i, k):
            v = _xc2(Mp, R[i] * R[j]); G[..., i + 1, j + 1] = G[..., j + 1, i + 1] = v
    G += np.eye(k + 1) * 1e-3 * np.maximum(nfull, 1)[:, None, None, None]
    Ginv = np.linalg.inv(G)
    tot = np.zeros(shape)
    Mb = np.pad(M.astype(np.float64), ((half, half), (0, 0)))
    for f in range(F):
        Ob = np.pad(obs[f].astype(np.float64), ((half, half), (0, 0))) * Mb
        s1 = _xc2(Ob, np.ones((bh, Ws)))[:, 0]; s2 = _xc2(Ob * Ob, np.ones((bh, Ws)))[:, 0]
        Of = np.pad(Ob, ((0, 0), (Wc, Wc)))
        b = np.zeros(shape + (k + 1,)); b[..., 0] = s1[:, None]
        for j in range(k): b[..., j + 1] = _xc2(Of, R[j])
        nn = np.maximum(nfull, 1)[:, None]
        sst = np.maximum(s2[:, None] - s1[:, None] ** 2 / nn, 1e-9)
        expl = np.einsum('yti,ytij,ytj->yt', b, Ginv, b) - s1[:, None] ** 2 / nn
        rss = np.maximum(sst - expl, 1e-6 * sst)
        tot += -(nn / 2) * np.log(rss / sst)
    valid = nfull >= 0.25 * bh * M.sum(1).max()
    tb = np.argmax(tot, 1)
    sc = tot[np.arange(tot.shape[0]), tb]
    sc[~valid] = -np.inf
    return sc, tb - Wc
