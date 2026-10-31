"""CONFIRMATORY run (once, as frozen in PROTOCOL_FROZEN.md).
Stage 1: held-out calibration lines -> calibration_rankings.csv, exact one-sided Poisson-binomial test.
Stage 2 (only if Stage 1 passes): targets in ORDER (XII 10 last) -> target_rankings.csv.
Renderings (private) -> /root/novel/private_outputs/B/renderings/."""
import os, sys, json, csv, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model as m, abs_score as A, targets as T
HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = json.load(open(f'{HERE}/frozen_params.json'))
ALPHA = 0.05
def rank_of(tot, key):
    t = tot[key]; return 1 + sum(1 for c in tot if c != key and tot[c] >= t)
def poibin_sf(ps, k):
    d = np.zeros(len(ps) + 1); d[0] = 1
    for q in ps: d = np.concatenate([d * (1 - q), [0]]) + np.concatenate([[0], d * q])
    return float(d[k:].sum())
def stage1(P):
    items = [x for x in json.load(open(f'{HERE}/calibration_items.json')) if x['split'] == 'heldout']
    rows = []; hits = 0; ps = []
    for it in items:
        tot, info = A.score_line(it['col'], it['line'], it['candidates'], P, save=f"cal_{it['col']}_{it['line']}")
        r = rank_of(tot, it['truth']); hits += (r == 1); ps.append(1 / len(it['candidates']))
        other = max(tot[c] for c in tot if c != it['truth'])
        order = sorted(tot, key=lambda c: -tot[c])
        for c in it['candidates']:
            rows.append(dict(run='confirmatory', split='heldout', col=it['col'], line=it['line'],
                n_candidates=len(it['candidates']), candidate=c, is_truth=int(c == it['truth']),
                loglik=round(tot[c], 3), rank=rank_of(tot, c), truth_rank=r,
                margin_truth_minus_best_other=round(tot[it['truth']] - other, 3),
                strips=';'.join(f"{i['cut']}:{i['status']}:o{i.get('orient','')}:y{i.get('y','')}" for i in info)))
        print('heldout', it['col'], it['line'], 'truth rank', r, 'of', len(it['candidates']), flush=True)
    p = poibin_sf(ps, hits)
    return rows, dict(n=len(items), top1=hits, expected_chance=round(sum(ps), 3), p_one_sided=round(p, 5), passed=bool(p < ALPHA))
def stage2(P):
    rows = []
    for name in T.ORDER:
        t = T.TARGETS[name]; labels = list(t['cands']); cands = [t['cands'][k] for k in labels]
        tot, info = A.score_line(t['col'], t['line'], cands, P, save=f"tgt_{name.replace(' ', '')}")
        order = sorted(cands, key=lambda c: -tot[c]); best = tot[order[0]]
        for k, c in zip(labels, cands):
            rows.append(dict(target=name, label=k, candidate=c, loglik=round(tot[c], 3), rank=order.index(c) + 1,
                             delta_from_best=round(tot[c] - best, 3),
                             strips=';'.join(f"{i['cut']}:{i['status']}:o{i.get('orient','')}:y{i.get('y','')}" for i in info)))
        print('target', name, [(labels[cands.index(c)], round(tot[c] - best, 1)) for c in order], flush=True)
    return rows
def write(path, rows):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
if __name__ == '__main__':
    assert not os.path.exists(f'{HERE}/calibration_rankings.csv'), 'confirmatory run already done'
    P = dict(m.DEFAULT); P.update(FROZEN)
    rows, test = stage1(P)
    write(f'{HERE}/calibration_rankings.csv', rows)
    json.dump(test, open(f'{HERE}/heldout_test_result.json', 'w'), indent=1)
    print('HELD-OUT TEST', test, flush=True)
    if test['passed']:
        write(f'{HERE}/target_rankings.csv', stage2(P))
    else:
        write(f'{HERE}/target_rankings.csv', [dict(target='ALL', label='', candidate='', loglik='', rank='',
              delta_from_best='', strips='NOT RUN: held-out calibration failed (frozen rule: targets not scored)')])
