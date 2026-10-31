"""C3 shared library: letter-level copper measurement at A2-placed positions (31 Oct 2026).

Reuses A2's registration and placement code (branch claude/novel-2026-10-31-A2, commit 6a309e75) unchanged.
The A2 files are read from an extraction of that commit in the scratchpad; their SHA-256 are checked on import
against the values A2 recorded in its sha256_inputs.txt. Image arrays come from A2's scratchpad cache (read only);
nothing image-like is written to the repository.

W2F letter boxes (research/agent_review_2026-10-07/wave2/W2F_plates_model/data/labels_verified.csv):
  px, py   = letter centre on the Puech 2006 copy photograph (copy-photo pixels; the frame A2 registered to).
  fx0..fy1, fac_w, fac_h = box on Puech's facsimile drawing (used ONLY for the drawing features and the paired
             analysis, never for the copper measurement).
Only the box CENTRES (px, py) are mapped into the 1988 frames.
"""
import os, sys, json, hashlib, csv
import numpy as np

SP = "/tmp/claude-0/-home-user-CopperScroll/a9f5167d-29f8-59e4-bea0-35def87251ce/scratchpad"
A2DIR = SP + "/C3work/ref/research/novel_2026-10-31/A2_photometric_stereo"
HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
W2F = REPO + "/research/agent_review_2026-10-07/wave2/W2F_plates_model/data"
PROD = SP + "/products/C3"
os.makedirs(PROD, exist_ok=True)

# SHA-256 of the A2 files used (values from A2's sha256_inputs.txt, commit 6a309e75); checked on import.
A2_SHA = {
    "common.py": "97f6e952f3045c327eecd3fc012adf3d220e316853f0a961947275e470b85a10",
    "register.py": "f48ec4f671489da39bc58959693f4e2fc662ec3d56ce6bc59a4aafbf74f61b99",
    "ps.py": "9a7cf1346d97c3a0732cdc0958ca55fad208a3e9bafd70627db7356f6cb2ff0d",
    "copyphoto.py": "0e7a0278a7ffec29c2861e33c239bcfe189f6cbcf745205881679fb7cb00b25a",
    "place.py": "af0b6480fba0d79276d4c52e379cd86e11f978e973ce548ccc591922f1362059",
    "controls.py": "40e93babe98c71bac3a520d387ee5a46802180f334a71f342ef2458b52fac9cf",
}
ACCEPTED = {  # A2 accepted cut/column placements (distinctiveness >= 1.8, local median <= 0.15 Lh)
    (2, "I"): "place_cut02_I_narrow.json", (3, "I"): "place_cut03_I.json", (4, "I"): "place_cut04_I.json",
    (6, "II"): "place_cut06_II.json", (7, "III"): "place_cut07_III.json", (8, "III"): "place_cut08_III.json",
    (11, "V"): "place_cut11_V.json", (16, "IX"): "place_cut16_IX.json", (17, "X"): "place_cut17_X.json",
    (18, "X"): "place_cut18_X.json", (21, "XII"): "place_cut21_XII.json", (22, "XII"): "place_cut22_XII.json",
}
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def check_a2():
    out = {}
    for f, h in A2_SHA.items():
        got = sha(f"{A2DIR}/{f}")
        if got != h:
            raise RuntimeError(f"A2 file {f} hash mismatch {got}")
        out[f] = got
    for (c, col), f in ACCEPTED.items():
        out[f"place/{f}"] = sha(f"{A2DIR}/place/{f}")
        out[f"reg/reg_cut{c:02d}.json"] = sha(f"{A2DIR}/reg/reg_cut{c:02d}.json")
    return out


check_a2()
sys.path.insert(0, A2DIR)
import cv2  # noqa: E402
from ps import load_reg, usable_lights, stack_window  # noqa: E402  (A2)
from controls import strip_mask_ref, COPY_LH, MARGIN_LH  # noqa: E402  (A2)


def place_json(cut, col):
    return json.load(open(f"{A2DIR}/place/{ACCEPTED[(cut, col)]}"))


# ---------------------------------------------------------------- W2F letters and drawing features (round-1 C defs)
def w2f_letters():
    L = list(csv.DictReader(open(f"{W2F}/labels_verified.csv", encoding="utf-8")))
    pitch = {}
    for c in range(1, 13):
        fc = json.load(open(f"{W2F}/fac_components_col{c:02d}.json"))
        a = sorted(fc["line_a"])
        n = len(a)
        for k in range(n):
            d = [a[j + 1] - a[j] for j in (k - 1, k) if 0 <= j and j + 1 < n]
            pitch[(c, k + 1)] = float(np.mean(d))
    for i, r in enumerate(L):
        r["uid"] = i
        r["c"] = int(r["col"]); r["col_roman"] = ROMAN[r["c"] - 1]; r["l"] = int(r["ref"].split()[1])
        for k in ("fx0", "fx1", "fy0", "fy1", "fac_w", "fac_h", "px", "py"):
            r[k] = float(r[k])
        r["fac_pitch"] = pitch[(r["c"], r["l"])]
        r["hp_dr"] = r["fac_h"] / r["fac_pitch"]
        r["asp_dr"] = r["fac_w"] / r["fac_h"]
    med = {}
    for r in L:
        med.setdefault(r["letter"], []).append(r)
    med = {k: dict(hp=float(np.median([x["hp_dr"] for x in v]))) for k, v in med.items()}
    for r in L:
        r["h_rel_dr"] = r["hp_dr"] / med[r["letter"]]["hp"]
    return L


# ---------------------------------------------------------------- placement (A2 global fit, A2 margin rule)
_MASK = {}
_REG = {}


def reg(cut):
    if cut not in _REG:
        _REG[cut] = load_reg(cut)
    return _REG[cut]


def mask(cut):
    if cut not in _MASK:
        _MASK[cut] = strip_mask_ref(reg(cut), cut)
    return _MASK[cut]


def place_letters(L, cuts_by_col):
    """Map W2F copy-photo centres (px, py) into the reference frame of each accepted cut of the letter's column.
    A letter is placed on a cut if a square of half-size MARGIN_LH * Lh88 (A2's rule, 0.4 Lh) around the mapped
    centre lies inside A2's strip mask. If two cuts qualify, the one with the larger distance to the mask edge
    is used. No local refinement (A2's never passed its threshold). Returns list of dicts."""
    out = []
    for r in L:
        col = r["col_roman"]
        best = None
        for c in cuts_by_col.get(col, []):
            P = place_json(c, col)
            A = np.vstack([np.asarray(P["A_88ref_to_copy"]), [0, 0, 1]])
            x88, y88 = (np.linalg.inv(A) @ [r["px"], r["py"], 1])[:2]
            lh = COPY_LH[col] / P["scale"]
            m = mask(c)
            xi, yi = int(round(x88)), int(round(y88))
            if not (0 <= xi < m.shape[1] and 0 <= yi < m.shape[0]) or not m[yi, xi]:
                continue
            rr = int(MARGIN_LH * lh)
            sub = m[max(0, yi - rr):yi + rr + 1, max(0, xi - rr):xi + rr + 1]
            if sub.size == 0 or sub.mean() < 0.999:
                continue
            # horizontal distance to the mask edge (for tie-breaking only)
            row = m[yi, :]
            left = xi - np.max(np.where(row[:xi] == 0)[0]) if (row[:xi] == 0).any() else xi
            right = np.min(np.where(row[xi:] == 0)[0]) if (row[xi:] == 0).any() else m.shape[1] - xi
            dist = min(left, right)
            cand = dict(cut=c, x88=float(x88), y88=float(y88), lh88=float(lh), edge_dist=float(dist),
                        place_scale=float(P["scale"]))
            if best is None or cand["edge_dist"] > best["edge_dist"]:
                best = cand
        if best is not None:
            d = {k: r[k] for k in ("uid", "col_roman", "c", "l", "ref", "word_index", "char_index", "letter", "px", "py",
                                   "hp_dr", "h_rel_dr", "fac_h", "fac_w", "fac_pitch")}
            d.update(best)
            out.append(d)
    return out
