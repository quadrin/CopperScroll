"""A2 confirmatory run (run ONCE after the freeze commit): place all controls, compute PS features for training and
held-out items, train the frozen rules on training items only, score the held-out split, write results.

Usage: python3 score_heldout.py OUTDIR [--dryrun]
--dryrun scores a pseudo held-out set drawn from TRAINING items only (code check before the freeze)."""
import sys, json, os
import numpy as np, pandas as pd
from common import HERE, SP
import controls
from rules import RULE_CLASSES, VARIANTS, train_rule, apply_rule

FROZEN = {  # chosen on training LOO only (loo_train_tb.json): best balanced accuracy over 6 variants x S in {0,1,2}
    "BK": {"variant": "tb", "S": 2, "loo_bal_acc": 0.6495},
    "HE_HET": {"variant": "tb", "S": 0, "loo_bal_acc": 0.6611},
    "HET_TAW": {"variant": "ny", "S": 2, "loo_bal_acc": 0.7947},
}
ALPHA = 0.05
QGRID = np.linspace(0, 1, 51)


def _chance_dist(n_a, n_b, q):
    """Distribution of the number correct for a caller that ignores the image and calls class A with prob. q."""
    from math import comb
    pa = np.array([comb(n_a, i) * q ** i * (1 - q) ** (n_a - i) for i in range(n_a + 1)])
    pb = np.array([comb(n_b, j) * (1 - q) ** j * q ** (n_b - j) for j in range(n_b + 1)])
    return np.convolve(pa, pb)


def bias_robust_p(k, n_a, n_b):
    return float(max(_chance_dist(n_a, n_b, q)[k:].sum() for q in np.linspace(0, 1, 1001)))


def pooled_bias_robust_p(k, groups):
    """groups: list of (n_a, n_b), one per rule. P(total correct >= k), maximised over an independent chance bias
    q_r per rule on a 0.02 grid."""
    dists = [[_chance_dist(na, nb, q) for q in QGRID] for na, nb in groups]
    best = 0.0
    import itertools
    for combo in itertools.product(*[range(len(QGRID))] * len(groups)):
        d = np.array([1.0])
        for g, qi in enumerate(combo):
            d = np.convolve(d, dists[g][qi])
        best = max(best, float(d[k:].sum()))
    return best


def main(outdir, dryrun=False):
    os.makedirs(outdir, exist_ok=True)
    pl_csv = f"{outdir}/placements_all.csv"
    npz = f"{SP}/a2work/F_confirm{'_dry' if dryrun else ''}.npz"
    controls.run(pl_csv, npz, include_heldout=not dryrun)
    f = np.load(npz, allow_pickle=True)
    ids, F, lab, split, rule = list(f["ids"]), f["F"], list(f["lab"]), list(f["split"]), list(f["rule"])
    train = [k for k, s in enumerate(split) if s in ("train", "train_w2f")]
    if dryrun:
        rng = np.random.default_rng(1)
        ctrl = [k for k in train if split[k] == "train"]
        test = list(rng.choice(ctrl, size=min(12, len(ctrl)), replace=False))
        train = [k for k in train if k not in test]
    else:
        test = [k for k, s in enumerate(split) if s == "heldout"]
    if dryrun:
        rule = list(rule)
        for k in test:
            rule[k] = {"ב": "BK", "כ": "BK", "ה": "HE_HET", "ת": "HET_TAW"}.get(lab[k], "HE_HET")
    calls, res, unscorable = [], {}, []
    for r, cfg in FROZEN.items():
        a, b = RULE_CLASSES[r]
        ch = VARIANTS[cfg["variant"]]
        ok = lambda k: bool(np.all(np.isfinite(F[k][ch])))
        FA = np.stack([F[k][ch] for k in train if lab[k] == a and ok(k)])
        FB = np.stack([F[k][ch] for k in train if lab[k] == b and ok(k)])
        model = train_rule(FA, FB, cfg["S"])
        for k in test:
            if rule[k] != r:  # each held-out letter is scored once, by the rule fixed in split.csv
                continue
            if not ok(k):
                unscorable.append({"candidate_id": ids[k], "rule": r, "reason": f"channels of {cfg['variant']} unavailable"})
                continue
            s = apply_rule(model, F[k][ch])
            calls.append({"candidate_id": ids[k], "truth": lab[k], "rule": r, "variant": cfg["variant"],
                          "score": round(s, 4), "call": a if s > 0 else b, "correct": (a if s > 0 else b) == lab[k]})
    cdf = pd.DataFrame(calls)
    cdf.to_csv(f"{outdir}/heldout_calls{'_dry' if dryrun else ''}.csv", index=False)
    for r, cfg in FROZEN.items():
        sub = cdf[cdf.rule == r] if len(cdf) else cdf
        a, b = RULE_CLASSES[r]
        n_a, n_b = int((sub.truth == a).sum()), int((sub.truth == b).sum())
        k = int(sub.correct.sum()) if len(sub) else 0
        tpr = float(sub[sub.truth == a].correct.mean()) if n_a else None
        tnr = float(sub[sub.truth == b].correct.mean()) if n_b else None
        p = bias_robust_p(k, n_a, n_b) if (n_a + n_b) else None
        res[r] = {"variant": cfg["variant"], "S": cfg["S"], "n": n_a + n_b,
                  "n_" + a: n_a, "n_" + b: n_b, "correct": k, "accuracy": (k / (n_a + n_b)) if (n_a + n_b) else None,
                  "recall_" + a: tpr, "recall_" + b: tnr, "p_bias_robust": p,
                  }
    groups = [(res[r]["n_" + RULE_CLASSES[r][0]], res[r]["n_" + RULE_CLASSES[r][1]]) for r in FROZEN]
    K = int(cdf.correct.sum()) if len(cdf) else 0
    N = int(len(cdf))
    p_pool = pooled_bias_robust_p(K, groups) if N else None
    out = {"dryrun": dryrun, "alpha": ALPHA, "rules": res,
           "pooled": {"n": N, "correct": K, "accuracy": (K / N) if N else None, "p_bias_robust": p_pool,
                      "passed": bool(p_pool is not None and p_pool < ALPHA)},
           "unscorable_heldout": unscorable,
           "n_train_items_with_features": len(train), "n_test_items_with_features": len(test),
           "targets": "not scored: the frozen placement has no letter-level box for any target (see PROTOCOL_FROZEN.md)"}
    json.dump(out, open(f"{outdir}/confirmatory_result{'_dry' if dryrun else ''}.json", "w"), indent=1,
              ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], dryrun="--dryrun" in sys.argv)
