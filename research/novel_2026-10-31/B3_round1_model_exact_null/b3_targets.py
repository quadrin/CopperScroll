"""B3 targets: run ONLY after a PASS of the frozen decision rule (called by b3_run.py confirm_merge).

Uses round-1 targets.py (verbatim: XII 10 R1-R7, IX 10, I 12, VII 11, X 15, in round-1 ORDER with XII 10 last)
and round-1 confirm.stage2 (verbatim), with the frozen parameters, once. Renderings go to SP/products/B3/renderings.
Round-1 'lean / undecided' rule: a target leans to its top candidate only if the margin to the runner-up is at
least the median absolute truth-minus-best-other margin on the held-out lines (here: the 76 new lines' truth
sets at their own line, from confirm_result.json); otherwise it is undecided by this model.
These are model outputs from exposed images, not readings."""
import os, sys, csv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import b3_score as S          # sets the private paths before confirm imports abs_score
import confirm as CF          # round-1 confirm.py, verbatim


def run(res):
    os.makedirs(S.A.REND, exist_ok=True)
    rows = CF.stage2(S.P)
    thr = res['median_abs_truth_margin']
    by = {}
    for r in rows: by.setdefault(r['target'], []).append(r)
    for name, rr in by.items():
        rr.sort(key=lambda r: r['rank'])
        margin = rr[0]['loglik'] - rr[1]['loglik'] if len(rr) > 1 else float('inf')
        for r in rr:
            r['top_margin_to_runner_up'] = round(margin, 3); r['lean_threshold'] = thr
            r['lean'] = ('leans to ' + rr[0]['label']) if margin >= thr else 'undecided by this model'
    with open(f'{HERE}/target_rankings_b3.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
