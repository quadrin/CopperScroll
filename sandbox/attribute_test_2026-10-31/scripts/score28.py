"""Run 28 scroll scoring (RULE.md, "Scroll outputs"). Runs only if out/gate.json says PASS.
Written 31 Oct 2026 before any consolidated describer file existed.

usage: python3 score28.py
Inputs: keyed/scroll_coding_A.csv and keyed/scroll_coding_B.csv, columns
        entry, class_group, n_openings, opening_dir, pillar (yes/no/blank), steps (yes/no/blank), notes
        out/alpha.json ("all_items"), the inventory as in bench28.py.
A field is used only where both coders give the same value; otherwise it is blank. An entry is scored only if
both coders give the same class group, that group occurs in the inventory, and at least one attribute is left.
Outputs: out/scroll_scores.csv (one row per scored entry), out/scroll_top5.csv.
The posterior is conditional on the entry's place being one of the inventory's features.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model28 import ATTRS, NONCLASS, RUN, Model, dir_list, match, read_csv, set_size  # noqa: E402
from bench28 import inventory  # noqa: E402


def coded(r):
    def yn(v):
        v = (v or "").strip().lower()
        return True if v == "yes" else False if v == "no" else None
    n = (r.get("n_openings") or "").strip()
    return {"cls": (r.get("class_group") or "").strip() or None,
            "n_open": int(n) if n.isdigit() else None,
            "dirs": dir_list(r.get("opening_dir")),
            "pillar": yn(r.get("pillar")), "steps": yn(r.get("steps"))}


def main():
    gate = json.load(open(RUN / "out/gate.json"))
    if gate.get("status") != "PASS":
        print("gate did not pass; the scroll is not scored:", gate.get("status"))
        return
    alpha = json.load(open(RUN / "out/alpha.json"))["all_items"]
    inv_rows, cands, _ = inventory()
    model = Model(cands)
    present = {c["cls"] for c in cands}
    A = {r["entry"]: coded(r) for r in read_csv(RUN / "keyed/scroll_coding_A.csv")}
    B = {r["entry"]: coded(r) for r in read_csv(RUN / "keyed/scroll_coding_B.csv")}
    scores, top = [], []
    for e in sorted(set(A) & set(B), key=lambda x: (len(x), x)):
        a, b = A[e], B[e]
        clue = {k: (a[k] if a[k] == b[k] else None) for k in ATTRS}
        if clue["cls"] is None or clue["cls"] not in present or all(clue[k] is None for k in NONCLASS):
            continue
        post = model.posterior(clue, alpha, ATTRS)
        order = np.argsort(-post)
        n_all = sum(all(c[k] is not None and match(k, clue[k], c[k]) for k in ATTRS if clue[k] is not None) for c in cands)
        scores.append({"entry": e, "clue": json.dumps({k: (sorted("/".join(sorted(s)) for s in v) if k == "dirs" and v else v)
                                                       for k, v in clue.items()}),
                       "n_match_all_known": n_all, "size50": set_size(post, 0.5), "size90": set_size(post, 0.9),
                       "top_post": float(post[order[0]]), "top_bf": float(post[order[0]] * model.N)})
        for rank, j in enumerate(order[:5], 1):
            top.append({"entry": e, "rank": rank, "key": inv_rows[j]["key"], "posterior": float(post[j]),
                        "bayes_factor": float(post[j] * model.N)})
    for name, rows in (("scroll_scores", scores), ("scroll_top5", top)):
        if rows:
            with open(RUN / f"out/{name}.csv", "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
    print(f"scored entries: {len(scores)} (conditional on the place being an inventory feature)")


if __name__ == "__main__":
    main()
