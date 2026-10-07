#!/usr/bin/env python3
"""Extra tables for the v0 report: candidate-level probabilities across models, LOO without order-derived
candidates, and region posteriors for the Kohlit group under w_A / rho choices.
Run after joint_model.py:  python3 -I extra_tables.py ../inputs ../outputs"""
import csv, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import joint_model as jm

ind, out = sys.argv[1], sys.argv[2]
data = jm.Data(ind)
S = json.load(open(os.path.join(out, 'summary.json')))
runs = {k: v['cfg'] for k, v in S['runs'].items()}

# 1. candidate-level probabilities across models
rows = []
models = {}
for name, kw in runs.items():
    m = jm.Model(data, jm.cfg_with(**kw))
    r = m.run()
    models[name] = (m, r)
m0, r0 = models['M0_prior']
for i, e in enumerate(r0['order']):
    for s in r0['ev'][e][2]:
        row = dict(entry=e, block=data.block[e], entry_conf=data.econf[e], candidate=m0.states[s],
                   region=m0.region_of[m0.states[s]],
                   order_derived=[c['order_derived'] for c in data.cands if c['entry'] == e and c['place_id'] == m0.states[s]][0])
        for name, (m, r) in models.items():
            row[name] = round(float(r['post'][i][s]), 3)
        rows.append(row)
jm.write_csv(os.path.join(out, 'candidate_probabilities_by_model.csv'), rows)

# 2. LOO with order-derived candidates removed (itinerary only, fitted weights)
kw = dict(runs['M1_itinerary_fitted'])
for lab, excl in [('no_documented', ('documented',)), ('no_documented_or_likely', ('documented', 'likely'))]:
    loo = jm.loo_all(data, jm.cfg_with(**{**kw, 'exclude_order_derived': excl}))
    jm.write_csv(os.path.join(out, f'loo_all_itinerary_fitted_{lab}.csv'), loo)
    res = {'all': round(float(np.mean([x['expected_log_lift'] for x in loo])), 3), 'n': len(loo)}
    for bl in 'ABCD':
        v = [x['expected_log_lift'] for x in loo if x['block'] == bl]
        res[bl] = (round(float(np.mean(v)), 3), len(v)) if v else None
    print('LOO', lab, res)
    S[f'loo_itinerary_fitted_{lab}'] = res

# 3. Kohlit / entry 60 grid over w_A and rho (w_L, lam at fitted values)
grid = []
for wa in (0.0, 0.2, 0.4, 0.6, 0.995):
    for rho in (0.0, 0.5, 0.9):
        for temper in (True, False):
            if rho == 0 and not temper:
                continue
            m = jm.Model(data, jm.cfg_with(**{**kw, 'w_A': wa, 'rho': rho, 'temper': temper}))
            r = m.run()
            pos = {e: i for i, e in enumerate(r['order'])}
            row = dict(w_A=wa, rho=rho, temper=temper, logml=round(r['logml'], 3))
            for e in ('4', '11', '15', '19', '60'):
                rp = m.region_probs(r['post'][pos[e]])
                row[f'e{e}_JERICHO'] = round(rp['JERICHO'], 2)
                row[f'e{e}_JER'] = round(rp['JER'], 2)
                row[f'e{e}_NORTH'] = round(rp['NORTH'], 2)
                row[f'e{e}_QUMRAN'] = round(rp['QUMRAN'], 2)
            grid.append(row)
jm.write_csv(os.path.join(out, 'kohlit_grid.csv'), grid)
json.dump(S, open(os.path.join(out, 'summary.json'), 'w'), indent=1, default=str)
print('ok')
