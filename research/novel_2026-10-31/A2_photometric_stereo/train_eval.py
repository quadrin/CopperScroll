"""A2 exploratory: leave-one-out (LOO) balanced accuracy of each rule and feature variant on the TRAINING split only."""
import sys, json
import numpy as np, pandas as pd
from rules import RULE_CLASSES, VARIANTS, train_rule, apply_rule
from common import HERE


def load(npz, split_csv=None, splits=("train", "train_w2f")):
    f = np.load(npz, allow_pickle=True)
    keep = [k for k, s in enumerate(f["split"]) if s in splits]
    return [f["ids"][k] for k in keep], f["F"][keep], [f["lab"][k] for k in keep]


def loo(ids, F, lab, rule, var, S):
    a, b = RULE_CLASSES[rule]
    ch = VARIANTS[var]
    idx = [k for k, l in enumerate(lab) if l in (a, b) and np.all(np.isfinite(F[k][ch]))]
    calls = []
    for k in idx:
        tr = [j for j in idx if j != k]
        FA = np.stack([F[j][ch] for j in tr if lab[j] == a]) if any(lab[j] == a for j in tr) else None
        FB = np.stack([F[j][ch] for j in tr if lab[j] == b]) if any(lab[j] == b for j in tr) else None
        if FA is None or FB is None:
            continue
        m = train_rule(FA, FB, S)
        s = apply_rule(m, F[k][ch])
        calls.append((lab[k], a if s > 0 else b))
    if not calls:
        return None
    tpr = np.mean([c == t for t, c in calls if t == a]) if any(t == a for t, _ in calls) else np.nan
    tnr = np.mean([c == t for t, c in calls if t == b]) if any(t == b for t, _ in calls) else np.nan
    return {"n": len(calls), "n_a": sum(t == a for t, _ in calls), "n_b": sum(t == b for t, _ in calls),
            "acc": float(np.mean([t == c for t, c in calls])), "bal_acc": float(np.nanmean([tpr, tnr]))}


if __name__ == "__main__":
    ids, F, lab = load(sys.argv[1], f"{HERE}/split.csv")
    out = {}
    for rule in RULE_CLASSES:
        for var in VARIANTS:
            for S in (0, 1, 2):
                r = loo(ids, F, lab, rule, var, S)
                out[f"{rule}|{var}|S{S}"] = r
                print(rule, var, S, r)
    if len(sys.argv) > 2:
        json.dump(out, open(sys.argv[2], "w"), indent=1)
