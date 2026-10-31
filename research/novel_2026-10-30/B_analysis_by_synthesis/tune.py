"""EXPLORATORY tuning on TRAIN lines only. Criterion: mean reciprocal rank of the truth, ties -> worst rank."""
import os, sys, json, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model as m, abs_score as A
HERE = os.path.dirname(os.path.abspath(__file__))
items = [x for x in json.load(open(f'{HERE}/calibration_items.json')) if x['split'] == 'train']
grid = json.loads(sys.argv[1])
out = sys.argv[2]
res = []
for vals in itertools.product(*grid.values()):
    P = dict(m.DEFAULT); P.update(dict(zip(grid.keys(), vals)))
    ranks = []
    for it in items:
        tot, info = A.score_line(it['col'], it['line'], it['candidates'], P)
        t = tot[it['truth']]; r = 1 + sum(1 for c in it['candidates'] if c != it['truth'] and tot[c] >= t)
        ranks.append(r)
    mrr = float(np.mean([1 / r for r in ranks])); top1 = sum(r == 1 for r in ranks)
    rec = dict(params=dict(zip(grid.keys(), vals)), ranks=ranks, mrr=round(mrr, 4), top1=top1, n=len(ranks))
    res.append(rec); print(json.dumps(rec), flush=True)
    json.dump(res, open(out, 'w'), indent=1)
