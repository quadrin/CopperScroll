"""B4: analysis by synthesis on letters placed by A2's copy-photo registration (31 Oct 2026). NEW MODEL.

Shared library: paths, A2 reuse (read-only), W2F letter table, placement of every W2F verified letter into the
1988 reference frame of an accepted cut/column pair, and multi-light feature patches.

A2 code and outputs are copied unchanged into ./a2_reused (from origin/claude/novel-2026-10-31-A2 at 6a309e75;
SHA-256 in sha256_inputs.txt). A2's image cache (SP/a2work/cache) is read only; this module refuses to run if a
needed cache file is missing, so it never writes there. Image products of B4 go to SP/products/B4 only.
"""
import os, sys, json, csv, glob
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
A2 = os.path.join(HERE, "a2_reused")
SP = "/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad"
PROD = SP + "/products/B4"
A2CACHE = SP + "/a2work/cache"
os.makedirs(PROD, exist_ok=True)
sys.path.insert(0, A2)

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
ROM = {r: i + 1 for i, r in enumerate(ROMAN)}
W2F = REPO + "/research/agent_review_2026-10-07/wave2/W2F_plates_model/data"
COPY_LH = {"I": 62.1, "II": 61.1, "III": 67.6, "IV": 72.8, "V": 74.2, "VI": 73.6, "VII": 71.3, "VIII": 66.6,
           "IX": 52.4, "X": 56.2, "XI": 55.3, "XII": 41.8}  # A2 controls.py (W2F plate_index letter_height_px)
GATE_DIST = 1.8          # A2 placement gate (frozen in A2's protocol)
GATE_LOCAL_LH = 0.15
MARGIN_LH = 0.45         # B4: letter centre at least this far inside the strip mask (letter heights)
TOF = dict(zip("כמנפצ", "ךםןףץ")); FROMF = {v: k for k, v in TOF.items()}


def a2_accepted():
    """A2's accepted cut/column placements: (cut, col) -> placement dict. Same rule as A2 controls.accepted_placements."""
    acc = {}
    for f in sorted(glob.glob(f"{A2}/place/place_cut*_*.json")):
        P = json.load(open(f))
        lm = P["local"]["median_shift_lh"]
        ok = bool(P["distinctiveness"] >= GATE_DIST and np.isfinite(lm) and lm <= GATE_LOCAL_LH)
        k = (P["cut"], P["col"])
        if ok and k not in acc:
            P["_file"] = os.path.basename(f)
            acc[k] = P
    return acc


def check_cache(cuts):
    import ps
    miss = []
    for c in cuts:
        reg = ps.load_reg(c)
        for L in ps.usable_lights(reg):
            if not os.path.exists(f"{A2CACHE}/gray_{c}_{L}.npy"):
                miss.append(f"gray_{c}_{L}.npy")
        if not os.path.exists(f"{A2CACHE}/ov_{c}_{reg['ref']}_0.1250.npy"):
            miss.append(f"ov_{c}_{reg['ref']}")
    if miss:
        raise SystemExit(f"A2 cache files missing (would be written by A2 code): {miss}")


_MASK = {}


def strip_mask_ref(cut):
    if cut not in _MASK:
        import ps
        from common import overview_cached, full_cached
        from register import strip_mask
        reg = ps.load_reg(cut)
        g = full_cached(cut, reg["ref"])
        m = strip_mask(overview_cached(cut, reg["ref"], 0.125))
        _MASK[cut] = cv2.resize(m, (g.shape[1], g.shape[0]), interpolation=cv2.INTER_NEAREST)
    return _MASK[cut]


def etcbc_lines():
    return json.load(open(f"{HERE}/etcbc_lines.json"))


def w2f_letters():
    """W2F verified letters (labels_verified.csv), each checked against the ETCBC text of its line.
    Centre used by B4: x = box centre (plx), y = line centre at the letter (ply), copy-photo pixels.
    The box size is not used (it would import Puech's drawing)."""
    L = etcbc_lines()
    rows = []
    bad = 0
    for r in csv.DictReader(open(f"{W2F}/labels_verified.csv", encoding="utf-8")):
        col = int(r["col"]); line = int(r["ref"].split()[1]); wi = int(r["word_index"]); ci = int(r["char_index"])
        ws = L.get(f"{col}:{line}")
        ok = ws is not None and wi < len(ws) and ci < len(ws[wi]["t"]) and ws[wi]["t"][ci] == r["letter"]
        if not ok:
            bad += 1
            continue
        rows.append(dict(col=col, column=ROMAN[col - 1], line=line, wi=wi, ci=ci, letter=r["letter"],
                         cx=float(r["plx"]), cy=float(r["ply"])))
    return rows, bad


def place_letters(rows, acc):
    """Map each letter's copy-photo centre into the 1988 reference frame of the first accepted cut of its column
    (cut order ascending) in whose strip mask a square of half-size MARGIN_LH * Lh around it lies entirely."""
    out = []
    bycol = {}
    for (c, col), P in acc.items():
        bycol.setdefault(col, []).append(c)
    for r in rows:
        r = dict(r)
        r["placed"] = False
        for c in sorted(bycol.get(r["column"], [])):
            P = acc[(c, r["column"])]
            A = np.vstack([np.asarray(P["A_88ref_to_copy"]), [0, 0, 1]])
            x88, y88 = (np.linalg.inv(A) @ [r["cx"], r["cy"], 1])[:2]
            lh = COPY_LH[r["column"]] / P["scale"]
            m = strip_mask_ref(c)
            rr = int(MARGIN_LH * lh)
            xi, yi = int(round(x88)), int(round(y88))
            if not (rr <= xi < m.shape[1] - rr and rr <= yi < m.shape[0] - rr):
                continue
            if m[yi - rr:yi + rr + 1, xi - rr:xi + rr + 1].mean() < 0.999:
                continue
            r.update(placed=True, cut=c, x88=float(x88), y88=float(y88), lh88=float(lh),
                     place_file=P["_file"], dist=float(P["distinctiveness"]),
                     local_lh=float(P["local"]["median_shift_lh"]),
                     conf=("high" if P["distinctiveness"] >= 2.4 else "medium"))
            break
        out.append(r)
    return out


# ---------------------------------------------------------------- features
RES = 20            # work pixels per letter height
WIN_LH = 2.0        # patch side (letter heights): template 1.2 Lh plus +-0.4 Lh of search room
TPL_LH = 1.2        # template side (letter heights)
HP_SIGMA_LH = 0.5   # high-pass: subtract Gaussian of this sigma
CHANNEL_OF = {"RCT": "CT", "RT": "CT", "RCB": "CB", "RB": "CB", "RLT": "LT", "RLB": "LB", "RRT": "RT", "RRB": "RB"}
CHANNELS = ["CT", "CB", "LT", "LB", "RT", "RB", "E", "TB", "LR"]


def _norm(a):
    a = a - a.mean()
    s = a.std()
    return a / (s + 1e-6)


def letter_patches(cut, x, y, lh):
    """Registered multi-light window around (x, y) (1988 reference px), returned as a dict channel -> RES-scaled
    patch (side round(WIN_LH * RES)). Light channels: intensity / frame median, high-passed. Channel E: mean over
    lights of the gradient magnitude (light-direction independent), high-passed."""
    import ps
    reg = ps.load_reg(cut)
    lights = ps.usable_lights(reg)
    half = int(round(0.5 * WIN_LH * lh)) + int(round(0.5 * lh))  # extra margin for the high-pass
    x0, y0 = int(round(x)) - half, int(round(y)) - half
    st, lights = ps.stack_window(cut, reg, x0, y0, 2 * half, 2 * half, lights)
    n = int(round(WIN_LH * RES))
    k = int(round(0.5 * WIN_LH * lh))
    out = {}
    gacc = None
    for i, L in enumerate(lights):
        a = st[i]
        a = np.where(np.isfinite(a), a, np.nanmedian(a) if np.isfinite(a).any() else 0).astype(np.float32)
        g = cv2.GaussianBlur(a, (0, 0), 0.03 * lh)
        gm = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
        gm /= (np.percentile(gm, 95) + 1e-6)
        gacc = gm if gacc is None else gacc + gm
        if L in CHANNEL_OF:
            hp = a - cv2.GaussianBlur(a, (0, 0), HP_SIGMA_LH * lh)
            c = hp[half - k:half + k, half - k:half + k]
            out[CHANNEL_OF[L]] = cv2.resize(c, (n, n), interpolation=cv2.INTER_AREA)
    # photometric ratio channels (albedo-normalised, light-direction contrasts):
    # TB = (top - bottom) / (top + bottom); LR = (left - right) / (left + right), from the lights present.
    def grp(names):
        sel = [st[i] for i, L in enumerate(lights) if L in names]
        return np.nanmean(np.stack(sel), axis=0) if sel else None
    top, bot = grp({"RCT", "RT"}), grp({"RCB", "RB"})
    if top is None or bot is None:
        top, bot = grp({"RLT", "RRT"}), grp({"RLB", "RRB"})
    lef, rig = grp({"RLT", "RLB"}), grp({"RRT", "RRB"})
    for name, (u, v) in (("TB", (top, bot)), ("LR", (lef, rig))):
        if u is None or v is None:
            continue
        r = (u - v) / np.maximum(u + v, 1e-3)
        r = np.where(np.isfinite(r), r, 0).astype(np.float32)
        r = cv2.GaussianBlur(r, (0, 0), 0.03 * lh)
        r = r - cv2.GaussianBlur(r, (0, 0), HP_SIGMA_LH * lh)
        out[name] = cv2.resize(r[half - k:half + k, half - k:half + k], (n, n), interpolation=cv2.INTER_AREA)
    gacc /= len(lights)
    hp = gacc - cv2.GaussianBlur(gacc, (0, 0), HP_SIGMA_LH * lh)
    c = hp[half - k:half + k, half - k:half + k]
    out["E"] = cv2.resize(c, (n, n), interpolation=cv2.INTER_AREA)
    return out, lights


def letter_id(r):
    return f"{r['col']}:{r['line']}:{r['wi']}:{r['ci']}"


def feature_array(placed):
    """Patches for a list of placed letters: array (n, len(CHANNELS), side, side), NaN where a channel is absent.
    Image-derived: callers store it in PROD (scratchpad) only, never in the repository."""
    n = int(round(WIN_LH * RES))
    F = np.full((len(placed), len(CHANNELS), n, n), np.nan, np.float32)
    for i, r in enumerate(placed):
        pt, _ = letter_patches(r["cut"], r["x88"], r["y88"], r["lh88"])
        for j, ch in enumerate(CHANNELS):
            if ch in pt:
                F[i, j] = pt[ch]
    return F
