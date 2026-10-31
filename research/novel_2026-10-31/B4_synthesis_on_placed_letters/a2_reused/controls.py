"""A2: place letter controls on the 1988 frames and compute photometric-stereo feature vectors.

Placement (logged to placements.csv): the W2F locator box (copy-photo pixels, controls_manifest.csv crop_box) is
mapped into the 1988 reference frame through the accepted text registration of that cut (place/*.json), then
refined locally by phase correlation of a 3-letter-height patch of the registered copy edge image against the
1988 multi-light edge image. No facsimile drawing is used.
Features: PS on a 2.5 Lh window; high-passed n_x, n_y and log-albedo; central 1.4 Lh box resampled to G x G.
"""
import json, os, sys, glob
import numpy as np, cv2, pandas as pd
from common import HERE, REPO
from ps import load_reg, usable_lights, stack_window, ps_normals
from place import edge88, prep
from copyphoto import copy_photo

GATE_DIST = 1.8        # placement gate: NCC distinctiveness of the global text registration
GATE_LOCAL_LH = 0.15   # ... and median local patch shift in letter heights
MARGIN_LH = 0.4        # control centre at least this far inside the strip mask
REFINE_MAX_LH = 0.4    # local refinement accepted if |shift| <= this and response >= REFINE_MIN_RESP
REFINE_MIN_RESP = 0.10
G = 16
COPY_LH = {"I": 62.1, "II": 61.1, "III": 67.6, "IV": 72.8, "V": 74.2, "VI": 73.6, "VII": 71.3, "VIII": 66.6,
           "IX": 52.4, "X": 56.2, "XI": 55.3, "XII": 41.8}  # W2F plate_index.csv letter_height_px (copy photo)


def accepted_placements():
    """Wide-search placement if it passes the gate; otherwise the narrow-scale retry if that passes."""
    acc = {}
    for f in sorted(glob.glob(f"{HERE}/place/place_cut*_*.json")):
        P = json.load(open(f))
        lm = P["local"]["median_shift_lh"]
        ok = bool(P["distinctiveness"] >= GATE_DIST and np.isfinite(lm) and lm <= GATE_LOCAL_LH)
        k = (P["cut"], P["col"])
        if k not in acc or (ok and not acc[k][0]):
            acc[k] = (ok, P)
    return acc


_E = {}


def e88(cut):
    if cut not in _E:
        reg = load_reg(cut)
        _E[cut] = (edge88(cut, reg), reg)
    return _E[cut]


def strip_mask_ref(reg, cut):
    from register import strip_mask
    from common import overview_cached, full_cached
    g = full_cached(cut, reg["ref"])
    m = strip_mask(overview_cached(cut, reg["ref"], 0.125))
    return cv2.resize(m, (g.shape[1], g.shape[0]), interpolation=cv2.INTER_NEAREST)


_M = {}


def place_control(row, acc):
    col = row["column"]
    if "cxc" in row and pd.notna(row.get("cxc")):
        cxc, cyc = float(row["cxc"]), float(row["cyc"])
    else:
        bx = [float(v) for v in row["crop_box"].split(",")]
        cxc, cyc = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
    best = None
    for c in [int(v) for v in str(row["cuts_present"]).split(";") if v]:
        if (c, col) not in acc:
            continue
        ok, P = acc[(c, col)]
        if not ok:
            continue
        A = np.vstack([np.asarray(P["A_88ref_to_copy"]), [0, 0, 1]])
        Ai = np.linalg.inv(A)
        x88, y88 = (Ai @ [cxc, cyc, 1])[:2]
        lh = COPY_LH[col] / P["scale"]
        reg = load_reg(c)
        if c not in _M:
            _M[c] = strip_mask_ref(reg, c)
        m = _M[c]
        xi, yi = int(round(x88)), int(round(y88))
        if not (0 <= xi < m.shape[1] and 0 <= yi < m.shape[0]) or not m[yi, xi]:
            continue
        dist = cv2.distanceTransform(m, cv2.DIST_L2, 5)[yi, xi] if False else None
        # margin: check the square of half-size MARGIN_LH * lh is inside the mask
        r = int(MARGIN_LH * lh)
        sub = m[max(0, yi - r):yi + r + 1, max(0, xi - r):xi + r + 1]
        frac = float(sub.mean()) if sub.size else 0.0
        if frac < 0.999:
            continue
        cand = {"cut": c, "x88": x88, "y88": y88, "lh88": lh, "P": P, "reg": reg}
        if best is None:
            best = cand
    if best is None:
        return None
    # local refinement
    c = best["cut"]; P = best["P"]; lh = best["lh88"]
    (E, (ex0, ey0)), reg = e88(c)
    C, _ = copy_photo(P["col"])
    Cf = prep(C.astype(np.float32), 2.0)
    A = np.vstack([np.asarray(P["A_88ref_to_copy"]), [0, 0, 1]])
    half = int(1.5 * lh)
    X0, Y0 = int(best["x88"]) - half, int(best["y88"]) - half
    T = (A @ np.array([[1, 0, X0], [0, 1, Y0], [0, 0, 1]], float))[:2]
    Cw = cv2.warpAffine(Cf, T.astype(np.float32), (2 * half, 2 * half), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
    Ew = E[Y0 - ey0:Y0 - ey0 + 2 * half, X0 - ex0:X0 - ex0 + 2 * half]
    dx = dy = 0.0; resp = 0.0; applied = False
    if Ew.shape == Cw.shape:
        Ewp = prep(Ew, 2.0)
        win = cv2.createHanningWindow((2 * half, 2 * half), cv2.CV_32F)
        (sx, sy), resp = cv2.phaseCorrelate(Cw.astype(np.float32), Ewp.astype(np.float32), win)
        if resp >= REFINE_MIN_RESP and np.hypot(sx, sy) <= REFINE_MAX_LH * lh:
            dx, dy, applied = sx, sy, True
    best.update(x_ref=best["x88"] + dx, y_ref=best["y88"] + dy, refine_dx=dx, refine_dy=dy, refine_resp=float(resp),
                refine_applied=applied)
    return best


TB_PAIRS = [("RCT", "RCB"), ("RT", "RB"), ("RLT", "RLB"), ("RRT", "RRB")]


def _prep_map(a, lh, half):
    a = np.where(np.isfinite(a), a, np.nanmedian(a) if np.isfinite(a).any() else 0).astype(np.float32)
    a = a - cv2.GaussianBlur(a, (0, 0), 0.6 * lh)
    a = cv2.GaussianBlur(a, (0, 0), 0.04 * lh)
    k = int(round(0.7 * lh))
    a = a[half - k:half + k, half - k:half + k]
    a = cv2.resize(a, (G, G), interpolation=cv2.INTER_AREA)
    med = np.median(a); mad = np.median(np.abs(a - med)) + 1e-6
    return ((a - med) / (1.4826 * mad)).astype(np.float32)


def features(cut, reg, cx, cy, lh, lights=None):
    """Channels: 0 n_x, 1 n_y, 2 log albedo (PS, needs >= 3 lights; NaN otherwise);
    3 'tb' = (I_top - I_bottom) / (I_top + I_bottom) of the first available mirrored top/bottom pair
    (two-light vertical photometric gradient, a proxy for n_y; available on 2-light cuts)."""
    half = int(round(1.25 * lh))
    x0, y0 = int(round(cx)) - half, int(round(cy)) - half
    st, lights = stack_window(cut, reg, x0, y0, 2 * half, 2 * half, lights)
    maps = []
    vf = 0.0
    if len(lights) >= 3:
        N, rho = ps_normals(st, lights)
        vf = float(np.isfinite(N[0]).mean())
        for a in (N[0], N[1], np.log(np.maximum(rho, 1e-3))):
            maps.append(_prep_map(a, lh, half))
    else:
        maps += [np.full((G, G), np.nan, np.float32)] * 3
    tb = None
    for t, b in TB_PAIRS:
        if t in lights and b in lights:
            It, Ib = st[lights.index(t)], st[lights.index(b)]
            tb = (It - Ib) / np.maximum(It + Ib, 1e-3)
            break
    maps.append(_prep_map(tb, lh, half) if tb is not None else np.full((G, G), np.nan, np.float32))
    return np.stack(maps), vf, lights


ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
COL_CUTS = {"I": "2;3;4", "II": "5;6", "III": "7;8", "IV": "10", "V": "10;11", "VI": "11", "IX": "16;17", "X": "17;18"}


def w2f_training_letters(sp):
    """W2F verified letters (labels_verified.csv) of the five letters in columns I-X with a present cut, excluding any
    letter within 0.5 copy letter heights of a held-out control centre (the same letter instance) and duplicates
    of training controls (within 0.5 Lh). Used for training only."""
    d = pd.read_csv(f"{REPO}/research/agent_review_2026-10-07/wave2/W2F_plates_model/data/labels_verified.csv")
    d = d[d.letter.isin(list("בכהחת")) & (d.col <= 10)].copy()
    d["column"] = d.col.apply(lambda c: ROMAN[c - 1])
    d = d[d.column.isin(COL_CUTS)]
    cen = {}
    for _, r in sp.iterrows():
        bx = [float(v) for v in r["crop_box"].split(",")]
        cen.setdefault(r["column"], []).append(((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2))
    rows = []
    for _, r in d.iterrows():
        lh = COPY_LH[r["column"]]
        if any(np.hypot(r["px"] - x, r["py"] - y) < 0.5 * lh for x, y in cen.get(r["column"], [])):
            continue
        rows.append({"candidate_id": f"W2F-{r['ref'].replace(' ', '')}-{int(r['word_index'])}-{int(r['char_index'])}",
                     "split": "train_w2f", "rule": "", "column": r["column"], "secure_answer": r["letter"],
                     "cxc": r["px"], "cyc": r["py"], "cuts_present": COL_CUTS[r["column"]]})
    return pd.DataFrame(rows)


def run(out_csv, out_npz, include_heldout=False):
    sp = pd.read_csv(f"{HERE}/split.csv")
    sp = pd.concat([sp, w2f_training_letters(sp)], ignore_index=True)
    acc = accepted_placements()
    rows, feats = [], []
    for _, r in sp.iterrows():
        b = place_control(r, acc)
        rec = {"candidate_id": r["candidate_id"], "split": r["split"], "rule": r["rule"], "column": r["column"],
               "secure_answer": r["secure_answer"]}
        if b is None:
            rec.update(placed=False, method="no accepted cut / outside strip margin")
            rows.append(rec); continue
        lights = usable_lights(b["reg"])
        rec.update(placed=True, cut=b["cut"], frame=b["reg"]["ref"],
                   box_x0=round(b["x_ref"] - 0.5 * b["lh88"], 1), box_y0=round(b["y_ref"] - 0.5 * b["lh88"], 1),
                   box_x1=round(b["x_ref"] + 0.5 * b["lh88"], 1), box_y1=round(b["y_ref"] + 0.5 * b["lh88"], 1),
                   x_ref=round(b["x_ref"], 1), y_ref=round(b["y_ref"], 1), lh88=round(b["lh88"], 1),
                   method="copy-photo text registration (place.py) + local phase-correlation refinement",
                   reg_distinctiveness=round(b["P"]["distinctiveness"], 3),
                   reg_local_median_lh=round(b["P"]["local"]["median_shift_lh"], 3),
                   refine_dx=round(b["refine_dx"], 1), refine_dy=round(b["refine_dy"], 1),
                   refine_resp=round(b["refine_resp"], 3), refine_applied=b["refine_applied"],
                   n_lights=len(lights), lights=";".join(lights))
        conf = "high" if (b["P"]["distinctiveness"] >= 2.4 and b["refine_applied"]) else (
            "medium" if b["refine_applied"] or b["P"]["distinctiveness"] >= 2.4 else "low")
        rec["confidence"] = conf
        has_tb = any(t in lights and b in lights for t, b in TB_PAIRS)
        if (len(lights) >= 3 or has_tb) and (rec["split"] != "heldout" or include_heldout):
            F, vf, _ = features(b["cut"], b["reg"], b["x_ref"], b["y_ref"], b["lh88"], lights)
            rec["ps_valid_frac"] = round(vf, 3)
            feats.append((r["candidate_id"], F, r["secure_answer"], rec["split"], rec["rule"]))
        rows.append(rec)
        pass
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    if feats:
        np.savez(out_npz, ids=np.array([f[0] for f in feats]), F=np.stack([f[1] for f in feats]),
                 lab=np.array([f[2] for f in feats]), split=np.array([f[3] for f in feats]),
                 rule=np.array([str(f[4]) for f in feats]))


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], include_heldout=(len(sys.argv) > 3 and sys.argv[3] == "heldout"))
