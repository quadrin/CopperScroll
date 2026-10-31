"""B4 confirmatory run (frozen; run once). Usage: python3 run4.py confirm

1. Rebuild placements and items (deterministic; must equal items4.json).
2. Templates and calibration from all TRAIN letters (model4 frozen parameters).
3. Held-out letter patches computed here for the first time (stored in SP/products/B4, never in the repo).
4. Primary: T = held-out lines whose edition reading strictly outscores every competitor; exact Poisson-binomial
   null with p0 = product over varied positions of 1/(a+1); ties count against the truth.
5. Decoy-truth bias control: per line a seeded competitor V; set at V's position = V's letter, the edition letter and
   the other competitor letters there; V first iff strictly above all; null 1/(a+1); Poisson-binomial.
6. Secondary: W (per-position wins), label-permutation null of T (TRAIN labels permuted within cut, NPERM times),
   per-letter accuracy for the pairs bet/kaf and he/het on TRAIN (leave-one-line-out) and held-out placed letters.
7. Targets: only on PASS (targets4.py); otherwise NOT RUN.
Outputs (numbers only): heldout_result4.json, heldout_rankings4.csv, letter_pairs4.csv, target_rankings4.csv.
"""
import sys, os, json, csv, time, collections
import numpy as np
import b4lib as B, items4 as I, model4 as M

DECOY_SEED = 4_202_610
PERM_SEED = 31_104
NPERM = 200
ALPHA = 0.05
MIN_LINES = 10


def poibin_sf(ps, t):
    """P(T >= t) for T = sum of independent Bernoulli(ps) (exact, by convolution)."""
    pmf = np.array([1.0])
    for p in ps:
        pmf = np.convolve(pmf, [1 - p, p])
    return float(pmf[t:].sum()), pmf


def build():
    acc = B.a2_accepted()
    B.check_cache(sorted({c for c, _ in acc}))
    rows, _ = B.w2f_letters()
    pl = B.place_letters(rows, acc)
    items, dropped, modelled, cnt, tr = I.build(pl)
    ref = json.load(open(f"{B.HERE}/items4.json"))
    assert json.dumps(ref["items"], ensure_ascii=False, sort_keys=True) == json.dumps(items, ensure_ascii=False, sort_keys=True)
    return pl, items, tr


def train_model(tr):
    fp = f"{B.PROD}/train_patches.npz"
    ids = [B.letter_id(r) for r in tr]
    d = np.load(fp) if os.path.exists(fp) else None
    if d is not None and list(d["ids"]) == ids and d["F"].shape[1] == len(B.CHANNELS):
        F = d["F"]
    else:
        F = B.feature_array(tr); np.savez_compressed(fp, F=F, ids=np.array(ids))
    forms = np.array([r["letter"] for r in tr]); cuts = np.array([r["cut"] for r in tr])
    return F, forms, cuts


def score_items(model, items, HF, hidx):
    """Per held-out line: positions, letter scores, truth-first, p0."""
    out = []
    for it in items:
        if it["split"] != "heldout":
            continue
        bypos = collections.OrderedDict()
        for c in it["competitors"]:
            bypos.setdefault((c["wi"], c["ci"], c["truth"], c["pos"]), []).append(c["alt"])
        pos = []
        for (wi, ci, t, p), alts in bypos.items():
            j = hidx[(it["col"], it["line"], wi, ci)]
            alts = sorted(set(alts))
            sc = {c: model.score(HF[j][0], HF[j][1], c) for c in [t] + alts}
            pos.append(dict(wi=wi, ci=ci, pos=p, truth=t, alts=alts, scores=sc))
        ok = [p for p in pos if all(np.isfinite(v) for v in p["scores"].values())]
        first = bool(ok) and all(all(p["scores"][p["truth"]] > p["scores"][a] for a in p["alts"]) for p in ok)
        ties = sum(any(p["scores"][p["truth"]] == p["scores"][a] for a in p["alts"]) for p in ok)
        p0 = float(np.prod([1.0 / (len(p["alts"]) + 1) for p in ok])) if ok else None
        out.append(dict(col=it["col"], line=it["line"], positions=pos, n_scored_pos=len(ok), truth_first=first,
                        ties=int(ties), p0=p0, competitors=it["competitors"]))
    return out


def decoy(res):
    T, ps, rows = 0, [], []
    for r in res:
        if not r["n_scored_pos"]:
            continue
        rng = np.random.default_rng(DECOY_SEED + 100 * r["col"] + r["line"])
        V = r["competitors"][int(rng.integers(len(r["competitors"])))]
        p = next(q for q in r["positions"] if q["pos"] == V["pos"])
        others = [p["truth"]] + [a for a in p["alts"] if a != V["alt"]]
        first = all(p["scores"][V["alt"]] > p["scores"][o] for o in others)
        T += first; ps.append(1.0 / (len(others) + 1))
        rows.append(dict(col=r["col"], line=r["line"], decoy_letter=V["alt"], pos=V["pos"], n_alternatives=len(others),
                         decoy_first=bool(first)))
    return T, ps, rows


def stats(res):
    lines = [r for r in res if r["n_scored_pos"]]
    T = sum(r["truth_first"] for r in lines)
    sf, _ = poibin_sf([r["p0"] for r in lines], T)
    W, wps = 0, []
    for r in lines:
        for p in r["positions"]:
            W += all(p["scores"][p["truth"]] > p["scores"][a] for a in p["alts"]); wps.append(1.0 / (len(p["alts"]) + 1))
    wsf, _ = poibin_sf(wps, W)
    return dict(n_lines=len(lines), T=int(T), E_T=float(sum(r["p0"] for r in lines)), P_T=sf, W=int(W), n_pos=len(wps),
                E_W=float(sum(wps)), P_W=wsf)


PAIRS = {"ב": ["כ"], "כ": ["ב"], "ה": ["ח"], "ח": ["ה"], "ך": ["ב"]}  # word-final kaf vs bet (final form kept)


def pair_acc(model_for, F, forms, cuts, idx):
    """Per-letter accuracy for bet/kaf and he/het: truth form vs its partner, for letters idx."""
    c = collections.defaultdict(lambda: [0, 0])
    for i in idx:
        t = forms[i]
        if t not in PAIRS:
            continue
        m = model_for(i)
        for v in PAIRS[t]:
            if v not in m.T.forms or t not in m.T.forms:
                continue
            win = m.score(F[i], cuts[i], t) > m.score(F[i], cuts[i], v)
            c[f"{t}>{v}"][0] += int(win); c[f"{t}>{v}"][1] += 1
    return {k: v for k, v in sorted(c.items())}


def main():
    t0 = time.time()
    pl, items, tr = build()
    F, forms, cuts = train_model(tr)
    model = M.Model(F, forms, cuts)
    held = {(i["col"], i["line"]) for i in items if i["split"] == "heldout"}
    hl = [r for r in pl if r["placed"] and (r["col"], r["line"]) in held]
    HFa = B.feature_array(hl)
    np.savez_compressed(f"{B.PROD}/heldout_patches.npz", F=HFa, ids=np.array([B.letter_id(r) for r in hl]))
    hidx = {(r["col"], r["line"], r["wi"], r["ci"]): j for j, r in enumerate(hl)}
    HF = [(HFa[j], hl[j]["cut"]) for j in range(len(hl))]
    res = score_items(model, items, HF, hidx)
    S = stats(res)
    Td, dps, drows = decoy(res)
    Pd, _ = poibin_sf(dps, Td)
    passed = bool(S["n_lines"] >= MIN_LINES and S["P_T"] < ALPHA and Pd >= ALPHA)
    # label-permutation null of T (secondary)
    rng = np.random.default_rng(PERM_SEED)
    Tperm = []
    for k in range(NPERM):
        f2 = forms.copy()
        for cc in sorted(set(cuts)):
            ix = np.nonzero(cuts == cc)[0]
            f2[ix] = f2[rng.permutation(ix)]
        mk = M.Model(F, f2, cuts)
        rk = score_items(mk, items, HF, hidx)
        Tperm.append(sum(r["truth_first"] for r in rk if r["n_scored_pos"]))
    Tperm = np.array(Tperm)
    P_perm = float((1 + np.sum(Tperm >= S["T"])) / (NPERM + 1))
    # per-letter accuracy, bet/kaf and he/het
    lines = np.array([f"{r['col']}:{r['line']}" for r in tr])
    loo = {}
    for ln in sorted(set(lines)):
        tst = np.nonzero(lines == ln)[0]
        if not any(forms[i] in PAIRS for i in tst):
            continue
        mm = M.Model(F[lines != ln], forms[lines != ln], cuts[lines != ln])
        for i in tst:
            loo[i] = mm
    acc_train = pair_acc(lambda i: loo[i], F, forms, cuts, sorted(loo))
    hforms = np.array([r["letter"] for r in hl]); hcuts = np.array([r["cut"] for r in hl])
    acc_held = pair_acc(lambda i: model, HFa, hforms, hcuts, range(len(hl)))
    out = dict(protocol="PROTOCOL_FROZEN.md", pass_rule=f"n_lines >= {MIN_LINES} and P(T>=t) < {ALPHA} and decoy P >= {ALPHA}",
               PASS=passed, primary=S, decoy=dict(T_decoy=int(Td), E_decoy=float(sum(dps)), P_decoy=Pd, n=len(dps)),
               permutation=dict(NPERM=NPERM, T_perm_mean=float(Tperm.mean()), T_perm_q95=float(np.quantile(Tperm, 0.95)),
                                P_perm=P_perm, T_perm_counts=dict(collections.Counter(int(x) for x in Tperm))),
               letter_accuracy=dict(train_loo=acc_train, heldout=acc_held),
               ties_total=int(sum(r["ties"] for r in res)), n_heldout_letters_featurised=len(hl),
               runtime_s=round(time.time() - t0, 1))
    margins = []
    with open(f"{B.HERE}/heldout_rankings4.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["col", "line", "word_index", "char_index", "pos", "truth_letter", "alt_letters", "score_truth",
                    "scores_alts", "truth_wins_position", "line_truth_first", "line_p0"])
        for r in res:
            for p in r["positions"]:
                st = p["scores"][p["truth"]]; sa = [p["scores"][a] for a in p["alts"]]
                margins.append(abs(st - max(sa)))
                w.writerow([r["col"], r["line"], p["wi"], p["ci"], p["pos"], p["truth"], "".join(p["alts"]), round(st, 4),
                            ";".join(f"{x:.4f}" for x in sa), int(all(st > x for x in sa)), int(r["truth_first"]),
                            round(r["p0"], 5) if r["p0"] else ""])
    out["median_abs_margin_heldout"] = float(np.median(margins)) if margins else None
    out["decoy_rows"] = drows
    json.dump(out, open(f"{B.HERE}/heldout_result4.json", "w"), ensure_ascii=False, indent=1)
    with open(f"{B.HERE}/letter_pairs4.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["set", "truth>partner", "truth_wins", "n"])
        for s, d in (("train_loo", acc_train), ("heldout", acc_held)):
            for k, v in d.items():
                w.writerow([s, k, v[0], v[1]])
    if passed:
        import targets4
        targets4.run(model)
    else:
        with open(f"{B.HERE}/target_rankings4.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh); w.writerow(["target", "status"])
            for t in ("XII 10", "IX 10", "X 15", "I 12"):
                w.writerow([t, "NOT RUN (held-out test did not pass)"])
    print(json.dumps({k: v for k, v in out.items() if k not in ("decoy_rows",)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if sys.argv[1:] != ["confirm"]:
        raise SystemExit("usage: run4.py confirm")
    main()
