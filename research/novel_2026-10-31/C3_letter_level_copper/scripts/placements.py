"""C3 step 1 (before any copper letter measurement): place all W2F verified letters of the columns with accepted
A2 cut/column pairs into the 1988 reference frames, and compute the drawing contrast (lines 1-6 against 8-13,
line 7 excluded; round-1 definition: mean of line medians of h_rel over lines with >= 3 letters) for every column,
on all verified letters and on the placed subset. Uses the drawing, A2's affine placements and A2's strip masks
(1/8-scale strip outline) only. Output: out/placed_letters.csv, out/drawing_contrasts.json."""
import json, csv
import numpy as np
from c3lib import w2f_letters, place_letters, ACCEPTED, FOLDER, ROMAN

CUTS_BY_COL = {}
for (c, col) in ACCEPTED:
    CUTS_BY_COL.setdefault(col, []).append(c)


def contrast(rows, key="h_rel_dr", before=range(1, 7), after=range(8, 14), min_n=3):
    by = {}
    for r in rows:
        by.setdefault(r["l"], []).append(r[key])
    lm = {l: float(np.median(v)) for l, v in by.items() if len(v) >= min_n}
    b = [lm[l] for l in before if l in lm]
    a = [lm[l] for l in after if l in lm]
    if not b or not a:
        return None
    mb, ma = float(np.mean(b)), float(np.mean(a))
    return dict(before=mb, after=ma, rel=(ma - mb) / mb, n_lines_before=len(b), n_lines_after=len(a),
                n_letters_before=sum(len(by[l]) for l in before if l in by),
                n_letters_after=sum(len(by[l]) for l in after if l in by))


def letter_contrast(rows, key="h_rel_dr", before=range(1, 7), after=range(8, 14)):
    b = [r[key] for r in rows if r["l"] in before]
    a = [r[key] for r in rows if r["l"] in after]
    if len(b) < 3 or len(a) < 3:
        return None
    mb, ma = float(np.median(b)), float(np.median(a))
    return dict(before=mb, after=ma, rel=(ma - mb) / mb, n_before=len(b), n_after=len(a))


if __name__ == "__main__":
    L = w2f_letters()
    P = place_letters(L, CUTS_BY_COL)
    with open(f"{FOLDER}/out/placed_letters.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(P[0].keys()))
        w.writeheader()
        for r in P:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    res = {}
    for col in ROMAN:
        allc = [r for r in L if r["col_roman"] == col]
        pl = [r for r in P if r["col_roman"] == col]
        res[col] = dict(n_verified=len(allc), n_placed=len(pl),
                        placed_by_cut={str(c): sum(1 for r in pl if r["cut"] == c) for c in CUTS_BY_COL.get(col, [])},
                        drawing_all=contrast(allc), drawing_placed=contrast(pl),
                        drawing_placed_letterlevel=letter_contrast(pl),
                        drawing_all_letterlevel=letter_contrast(allc),
                        n_lines=max([r["l"] for r in allc]) if allc else None)
        if col == "III":
            res[col]["placed_by_line"] = {str(l): {str(c): sum(1 for r in pl if r["l"] == l and r["cut"] == c)
                                                   for c in CUTS_BY_COL[col]} for l in range(1, 14)}
            res[col]["verified_by_line"] = {str(l): sum(1 for r in allc if r["l"] == l) for l in range(1, 14)}
    json.dump(res, open(f"{FOLDER}/out/drawing_contrasts.json", "w"), indent=1)
    for col, v in res.items():
        print(col, v["n_verified"], v["n_placed"], v["placed_by_cut"],
              {k: (round(v[k]["rel"], 3) if v[k] else None) for k in ("drawing_all", "drawing_placed", "drawing_placed_letterlevel")})
    print(json.dumps(res["III"]["placed_by_line"]))
