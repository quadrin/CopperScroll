"""B4 targets (frozen with the protocol; called by run4.py only if the held-out test passes).

Scorable target rule: the competing readings must align letter by letter with letters that W2F's Viterbi alignment
(viterbi_colNN.json) assigned to facsimile components, and those letters must place on an A2-accepted cut/column pair
(b4lib.place_letters rule, margin 0.45 Lh). Centre = facsimile box centre x and the line centre y at that x, mapped
facsimile -> copy photo (W2F registration.json A_fac2photo), exactly as W2F's plx/ply for training letters.
Status of each target, fixed before any score:
  - X 15: ETCBC/Milik חמים של רחיל תחת vs Puech המים שלוח ולתחת; 13 letters each, aligned one to one; they differ at
    word 2 letter 0 (ח/ה), word 4 letter 0 (ר/ו), word 4 letter 2 (י/ו) of the ETCBC line. Scored if the three
    letters place.
  - IX 10: the disputed words lie beyond the left edge of CT16 on the accepted CT16 -> IX placement (on CT17, whose IX
    placement A2 rejected): not scorable by this model.
  - XII 10: the disputed word is a wildcard in W2F's alignment (no letter units; R1-R7 differ in length): not scorable.
  - I 12: ניקרת (5 letters) against מקרת / נקרת (4 letters); no one-to-one letter alignment: not scorable.
Output: target_rankings4.csv. Every row is a model output on exposed images, not a reading.
"""
import csv, json
import numpy as np
import b4lib as B

X15 = {"ETCBC/Milik": {(2, 0): "ח", (4, 0): "ר", (4, 2): "י"}, "Puech 2006": {(2, 0): "ה", (4, 0): "ו", (4, 2): "ו"}}


def viterbi_letters(col, ref, wanted):
    v = json.load(open(f"{B.W2F}/viterbi_col{col:02d}.json"))[ref]
    M = np.array(json.load(open(f"{B.W2F}/registration.json"))[str(col)]["A_fac2photo"])
    fc = json.load(open(f"{B.W2F}/fac_components_col{col:02d}.json"))
    li = int(ref.split()[1]) - 1
    out = {}
    for j, u in enumerate(v["units"]):
        if u.get("kind") != "L" or (u["wi"], u["ci"]) not in wanted:
            continue
        cs = v["assign"].get(str(j), [])
        if not cs:
            continue
        cc = [v["comps"][c] for c in cs]
        bx = [min(c["x0"] for c in cc), min(c["y0"] for c in cc), max(c["x1"] for c in cc), max(c["y1"] for c in cc)]
        xm = (bx[0] + bx[2]) / 2
        yl = fc["line_a"][li] + fc["line_b"][li] * (xm - fc["xc"])
        p = M @ np.array([xm, yl, 1.0])
        out[(u["wi"], u["ci"])] = dict(col=col, column=B.ROMAN[col - 1], line=li + 1, wi=u["wi"], ci=u["ci"],
                                       letter=u["ch"], cx=float(p[0]), cy=float(p[1]))
    return out


def run(model):
    acc = B.a2_accepted()
    res = json.load(open(f"{B.HERE}/heldout_result4.json"))
    rows = []
    want = set(X15["ETCBC/Milik"])
    vl = viterbi_letters(10, "X 15", want)
    pl = B.place_letters(list(vl.values()), acc)
    placed = {(r["wi"], r["ci"]): r for r in pl if r["placed"]}
    hr = list(csv.DictReader(open(f"{B.HERE}/heldout_rankings4.csv", encoding="utf-8")))
    if set(placed) != want:
        rows.append(["X 15", "not scorable", f"placed {sorted(placed)} of {sorted(want)}", "", "", "", ""])
    else:
        F = B.feature_array([placed[k] for k in sorted(want)])
        tot = {name: 0.0 for name in X15}
        per = []
        for n, k in enumerate(sorted(want)):
            sc = {name: model.score(F[n], placed[k]["cut"], X15[name][k]) for name in X15}
            for name in X15:
                tot[name] += sc[name]
            m = sc["ETCBC/Milik"] - sc["Puech 2006"]
            # held-out positions whose |margin| >= |m|: fraction where the edition letter won
            big = [r for r in hr if abs(float(r["score_truth"]) - max(float(x) for x in r["scores_alts"].split(";"))) >= abs(m)]
            accb = (sum(int(r["truth_wins_position"]) for r in big) / len(big)) if big else None
            per.append((k, placed[k]["cut"], round(sc["ETCBC/Milik"], 3), round(sc["Puech 2006"], 3), round(m, 3),
                        len(big), None if accb is None else round(accb, 3)))
        top = max(tot, key=tot.get); margin = abs(tot["ETCBC/Milik"] - tot["Puech 2006"])
        med = res.get("median_abs_margin_heldout")
        verdict = ("leans " + top) if (med is not None and margin >= 3 * med) else "undecided by this model"
        rows.append(["X 15", "scored", json.dumps({k: round(v, 3) for k, v in tot.items()}, ensure_ascii=False),
                     round(margin, 3), med, verdict, json.dumps(per, ensure_ascii=False)])
    rows += [["IX 10", "not scorable", "disputed words beyond CT16's left edge; CT17->IX placement rejected by A2", "", "", "", ""],
             ["XII 10", "not scorable", "disputed word is a wildcard in W2F alignment; R1-R7 differ in length", "", "", "", ""],
             ["I 12", "not scorable", "no one-to-one letter alignment (5 vs 4 letters)", "", "", "", ""]]
    with open(f"{B.HERE}/target_rankings4.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["target", "status", "scores_or_reason", "margin", "median_abs_position_margin_heldout", "model_output",
                    "per_position(key,cut,s_etcbc,s_puech,diff,n_heldout_at_or_above,heldout_acc_at_or_above)"])
        w.writerows(rows)
