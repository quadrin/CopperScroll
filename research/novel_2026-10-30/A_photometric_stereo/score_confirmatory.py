"""Confirmatory scoring, run ONCE after PROTOCOL_FROZEN.md is committed and pushed.
Computes relief features for every keyed control (BK, HH) whose column maps to a cut whose mapping
passed the frozen cross-film agreement gate (ps_runs/mapping_agreement.json, accepted == true),
writes relief_features_controls.csv (numbers only) and scores the frozen het/taw rule."""
import sys, os, json, csv
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ps_lib as P, features as FE
D = os.path.dirname(os.path.abspath(__file__))
mp = json.load(open(os.path.join(D, 'ps_runs', 'cut_mapping.json')))
ag = json.load(open(os.path.join(D, 'ps_runs', 'mapping_agreement.json')))
W2F = os.path.join(P.REPO, 'research/agent_review_2026-10-07/wave2/W2F_plates_model/data')
L = {(x['ref'], x['word_index'], x['char_index']): x for x in csv.DictReader(open(os.path.join(W2F, 'labels_verified.csv')))}
C = [x for x in csv.DictReader(open(os.path.join(P.REPO, 'research/text/letter_controls/controls_manifest.csv')))
     if x['use'] == 'control' and x['question'] in ('BK', 'HH')]
rows = []
for cut, a in sorted(ag.items(), key=lambda kv: int(kv[0])):
    if not a.get('accepted'):
        continue
    for film in ('bla', 'col'):
        c = mp[f'{cut}_{film}']; M = np.array(c['photo_to_frame'])
        d = np.load(os.path.join(P.PRIVATE, f'ps_cut{int(cut):02d}_{film}.npz'))
        m = d['mask']; r = P.relief(d['z'], m, FE.SIGMA)
        spread = 1.4826 * np.nanmedian(np.abs(r[m] - np.nanmedian(r[m])))
        Lh = json.load(open(os.path.join(W2F, f"fac_components_col{c['col']:02d}.json")))['Lh']
        lh88 = Lh * c['s']
        for x in C:
            k = (x['ref'], x['word_index'], x['char_index'])
            if k not in L or int(L[k]['col']) != c['col']:
                continue
            p = M @ [float(L[k]['px']), float(L[k]['py']), 1]
            if not (0 <= p[0] < m.shape[1] and 0 <= p[1] < m.shape[0] and m[int(p[1]), int(p[0])]):
                continue
            f = FE.feats(r, m, p[0], p[1], lh88, c['rot'], spread)
            row = dict(candidate_id=x['candidate_id'], question=x['question'], secure_answer=x['secure_answer'], ref=x['ref'],
                       cut=int(cut), film=film, x_px=round(float(p[0]), 1), y_px=round(float(p[1]), 1), lh_px=round(lh88, 1),
                       valid=f is not None)
            if f:
                row.update({kk: round(v, 4) for kk, v in f.items()})
            rows.append(row)
keys = ['candidate_id', 'question', 'secure_answer', 'ref', 'cut', 'film', 'x_px', 'y_px', 'lh_px', 'valid',
        'f_base_rext', 'f_br_corner', 'f_base_mean', 'f_left_top', 'f_foot', 'f_left_foot', 'f_left_gap', 'f_contrast', 'window_in_mask']
with open(os.path.join(D, 'relief_features_controls.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, keys); w.writeheader()
    for r_ in rows:
        w.writerow({k: r_.get(k, '') for k in keys})
# frozen rule: het/taw controls; per letter mean f_left_foot over valid films; taw if > 0; invalid in both films = error
items = {}
for r_ in rows:
    if r_['question'] == 'HH' and r_['secure_answer'] in ('ח', 'ת'):
        items.setdefault(r_['candidate_id'], dict(ans=r_['secure_answer'], v=[]))
        if r_['valid'] and np.isfinite(r_['f_left_foot']):
            items[r_['candidate_id']]['v'].append(r_['f_left_foot'])
res = []
for cid, it in sorted(items.items()):
    if it['v']:
        val = float(np.mean(it['v'])); pred = 'ת' if val > 0 else 'ח'
    else:
        val, pred = None, 'invalid'
    res.append(dict(candidate_id=cid, truth=it['ans'], f_left_foot_mean=val, pred=pred, correct=pred == it['ans']))
n = len(res); kc = sum(r_['correct'] for r_ in res)
p = float(stats.binomtest(kc, n, 0.5, alternative='greater').pvalue) if n else None
ci = stats.binomtest(kc, n).proportion_ci(0.95, method='exact') if n else None
cls = {c: [r_ for r_ in res if r_['truth'] == c] for c in ('ח', 'ת')}
bal = float(np.mean([np.mean([r_['correct'] for r_ in v]) for v in cls.values() if v])) if n else None
out = dict(n=n, correct=kc, accuracy=None if not n else kc / n, ci95_clopper_pearson=None if ci is None else [ci.low, ci.high],
           balanced_accuracy=bal, binomial_one_sided_p=p, passed=bool(p is not None and p < 0.05), items=res,
           n_rows_csv=len(rows))
json.dump(out, open(os.path.join(D, 'confirmatory_result.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in out.items() if k != 'items'}, ensure_ascii=False))
