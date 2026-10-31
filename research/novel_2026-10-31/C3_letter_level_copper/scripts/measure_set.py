"""C3: measure a set of placed letters with the final (frozen) parameters, including the pitch fallback, and the
shared statistics helpers. Used by train_table.py (training, exploratory) and run_test.py (confirmatory)."""
import csv
import numpy as np
from measure import measure_letter, DEFAULT

FINAL = dict(DEFAULT)
FINAL.update(SIGMA=2.0, EXT_HALFW=0.4, BG_PCT=10.0, Q_LO=0.2, Q_HI=0.8,
             PITCH_HALFW=1.5, PITCH_HALFH=2.8, PITCH_MIN=1.4, PITCH_MAX=3.0)
TALL = set("ךלןקףץ")


def load_placed(path, cuts):
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8")) if int(r["cut"]) in cuts]
    for r in rows:
        for k in ("x88", "y88", "lh88", "hp_dr", "h_rel_dr", "px", "py"):
            r[k] = float(r[k])
        r["cut"] = int(r["cut"]); r["l"] = int(r["l"]); r["uid"] = int(r["uid"])
    return rows


def measure_rows(rows, p=FINAL):
    """Pass 1: own pitch. Pass 2 (fallback): letters whose own pitch failed take the median own pitch of the
    measured letters of the same cut on lines l-1..l+1 (copper values only); their extents are then measured
    with that pitch. pitch_src records 'own' or 'fallback'."""
    from measure import grad_stack, group_mean, extent_from
    out = []
    for r in rows:
        m = measure_letter(r["cut"], r["x88"], r["y88"], r["lh88"], p)
        d = dict(r); d.update(m); d["pitch_src"] = "own" if np.isfinite(m["pitch"]) else "none"
        out.append(d)
    for d in out:
        if d["pitch_src"] != "none":
            continue
        nb = [e["pitch"] for e in out if e["cut"] == d["cut"] and abs(e["l"] - d["l"]) <= 1 and e["pitch_src"] == "own"]
        if not nb:
            continue
        pc = float(np.median(nb))
        lh = d["lh88"]
        G, lights, _ = grad_stack(d["cut"], d["x88"], d["y88"], max(p["PITCH_HALFW"], p["EXT_HALFW"]) * lh + 4,
                                  p["PITCH_HALFH"] * lh, p["SIGMA"])
        for g in ("ALL", "T", "B"):
            img = group_mean(G, lights, g)
            ex = extent_from(img, lh, pc, p) if img is not None else np.nan
            d[f"ext_{g}"] = ex
            d[f"h_{g}"] = ex / pc if np.isfinite(ex) else np.nan
        d["pitch"] = pc; d["pitch_src"] = "fallback"
    return out


def class_table(meas, min_n=5):
    h = np.array([d["h_ALL"] for d in meas]); let = np.array([d["letter"] for d in meas]); ok = np.isfinite(h)
    tab = {L: float(np.median(h[ok & (let == L)])) for L in sorted(set(let[ok])) if (ok & (let == L)).sum() >= min_n}
    return tab, float(np.median(h[ok]))


def normalise(meas, tab, allmed):
    for d in meas:
        d["h_rel_cu"] = d["h_ALL"] / tab.get(d["letter"], allmed) if np.isfinite(d["h_ALL"]) else np.nan
    return meas


def split_half(meas):
    from scipy.stats import spearmanr
    hT = np.array([d["h_T"] for d in meas]); hB = np.array([d["h_B"] for d in meas])
    ok = np.isfinite(hT) & np.isfinite(hB)
    if ok.sum() < 6:
        return dict(n=int(ok.sum()), rho=np.nan, spread=np.nan)
    return dict(n=int(ok.sum()), rho=float(spearmanr(hT[ok], hB[ok]).correlation),
                spread=float(np.median(np.abs(hT[ok] - hB[ok]) / ((hT[ok] + hB[ok]) / 2))))


def class_validity(meas):
    h = np.array([d["h_ALL"] for d in meas]); let = np.array([d["letter"] for d in meas]); ok = np.isfinite(h)
    tall = ok & np.isin(let, list(TALL)); yod = ok & (let == "י"); rest = ok & ~np.isin(let, list(TALL) + ["י"])
    mr = float(np.median(h[rest])) if rest.any() else np.nan
    return dict(n_tall=int(tall.sum()), n_yod=int(yod.sum()), n_rest=int(rest.sum()),
                tall_ratio=float(np.median(h[tall]) / mr) if tall.any() else np.nan,
                yod_ratio=float(np.median(h[yod]) / mr) if yod.any() else np.nan)


def compression_k(meas, tab, allmed, min_n=5):
    """Slope through the origin of log copper class medians on log drawing class medians (both relative to their
    overall medians over the same letters)."""
    h = np.array([d["h_ALL"] for d in meas]); hp = np.array([d["hp_dr"] for d in meas])
    let = np.array([d["letter"] for d in meas]); ok = np.isfinite(h)
    cls = [L for L in tab if (ok & (let == L)).sum() >= min_n]
    dall = float(np.median(hp[ok]))
    xs = np.array([np.log(np.median(hp[ok & (let == L)]) / dall) for L in cls])
    ys = np.array([np.log(np.median(h[ok & (let == L)]) / allmed) for L in cls])
    return float((xs * ys).sum() / (xs * xs).sum()), len(cls)


BEFORE, AFTER = range(1, 7), range(8, 14)


def region_contrast(meas, key):
    b = np.array([d[key] for d in meas if d["l"] in BEFORE and np.isfinite(d[key])])
    a = np.array([d[key] for d in meas if d["l"] in AFTER and np.isfinite(d[key])])
    if len(b) < 3 or len(a) < 3:
        return None, b, a
    return float(np.median(a) / np.median(b) - 1), b, a


def line_contrast(meas, key, min_n=3):
    by = {}
    for d in meas:
        if np.isfinite(d[key]):
            by.setdefault(d["l"], []).append(d[key])
    lm = {l: float(np.median(v)) for l, v in by.items() if len(v) >= min_n}
    b = [lm[l] for l in BEFORE if l in lm]; a = [lm[l] for l in AFTER if l in lm]
    if not b or not a:
        return None
    return dict(rel=float(np.mean(a) / np.mean(b) - 1), n_lines_before=len(b), n_lines_after=len(a))
