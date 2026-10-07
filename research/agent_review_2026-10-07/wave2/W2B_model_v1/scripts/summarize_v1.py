#!/usr/bin/env python3
"""Compact tables for REPORT from the analysis outputs.  python3 -I summarize_v1.py ../outputs"""
import csv, collections, json, os, sys
out = sys.argv[1]
rd = lambda f: list(csv.DictReader(open(os.path.join(out, f), encoding='utf-8')))
C = ['tell_es_sultan', 'ein_samiya', 'muhalhil', 'beit_kahil', 'kuhlah', 'carmel_siah', 'mount_zion', 'transjordan',
     'ein_ghuweir', 'ein_feshkha']
SH = dict(tell_es_sultan='Tell', ein_samiya='Samiya', muhalhil='Muhal', beit_kahil='BKahil', kuhlah='Kuhlah', carmel_siah='Carmel',
          mount_zion='Zion', transjordan='TransJ', ein_ghuweir='Ghuweir', ein_feshkha='Feshkha', kh_yanun='Yanun')

# 1. order Bayes factors: tied and entry-60-only, all models
bf = rd('clamp_order_bayes_factors.csv') + [dict(r, kernel='G_uniform_grid') for r in rd('gmodel_order_bayes_factors.csv')]
rows = []
tab = collections.OrderedDict()
for r in bf:
    if r['design'] not in ('tied_all', 'only_60', 'only_19'):
        continue
    k = (r['kernel'], r['excl'], r['order'], r['w_A'], r['w_L'], r['reading'], r['design'])
    tab.setdefault(k, {})[r['candidate']] = float(r['dlog10_vs_tell'])
for k, v in tab.items():
    row = dict(model=k[0], excl=k[1], order=k[2], w_A=k[3], w_L=k[4], reading=k[5], design=k[6])
    for c in C + ['kh_yanun']:
        row[SH[c]] = ('%+.2f' % v[c]) if c in v else ''
    rows.append(row)
w = csv.DictWriter(open(os.path.join(out, 'table_order_BF_summary.csv'), 'w', newline=''), fieldnames=list(rows[0]))
w.writeheader(); w.writerows(rows)

# 2. robustness: range of tied / entry-60 BFs (vs Tell) across density-neutral models (K2, K4, G) and orders
def rng(design, reading, models, excls=('b0_none', 'b2_doc_likely'), orders=('fit', 'weak', 'T06', 'wA0')):
    res = {}
    for c in C + ['kh_yanun']:
        vals = [v[c] for k, v in tab.items() if k[0] in models and k[1] in excls and k[2] in orders and k[5] == reading
                and k[6] == design and c in v]
        if vals:
            res[SH[c]] = (round(min(vals), 2), round(max(vals), 2))
    return res
robust = dict(
    tied_mp_densityneutral=rng('tied_all', 'milik_puech', ('K2_fixed', 'K4_fixed_grid', 'G_uniform_grid')),
    tied_mp_densityneutral_wA0=rng('tied_all', 'milik_puech', ('K2_fixed', 'K4_fixed_grid', 'G_uniform_grid'), orders=('weak', 'wA0')),
    tied_mp_sinkhorn=rng('tied_all', 'milik_puech', ('K1_sinkhorn', 'K3_sinkhorn_grid')),
    e60_mp_densityneutral=rng('only_60', 'milik_puech', ('K2_fixed', 'K4_fixed_grid', 'G_uniform_grid')),
    e60_mp_sinkhorn=rng('only_60', 'milik_puech', ('K1_sinkhorn', 'K3_sinkhorn_grid')),
    e19_mp_densityneutral=rng('only_19', 'milik_puech', ('K2_fixed', 'K4_fixed_grid', 'G_uniform_grid')),
    tied_janoah_densityneutral_wA0=rng('tied_all', 'janoah', ('K2_fixed', 'K4_fixed_grid', 'G_uniform_grid'), orders=('weak', 'wA0')),
)
json.dump(robust, open(os.path.join(out, 'table_order_BF_ranges.json'), 'w'), indent=1)
for k, v in robust.items():
    print(k, v)

# 3. G-model group posteriors, headline configs
gp = rd('gmodel_group_posteriors.csv')
t3 = collections.OrderedDict()
for r in gp:
    k = (r['excl'], r['order'], r['reading'], r['janoah'], r['scheme'])
    t3.setdefault(k, {})[r['candidate']] = float(r['P_group'])
rows = []
for k, v in t3.items():
    rows.append(dict(excl=k[0], order=k[1], reading=k[2], janoah=k[3], scheme=k[4],
                     **{SH.get(c, c): round(v[c], 3) for c in C + ['ELSEWHERE']}))
w = csv.DictWriter(open(os.path.join(out, 'table_G_group_posteriors.csv'), 'w', newline=''), fieldnames=list(rows[0]))
w.writeheader(); w.writerows(rows)

# 4. full-model per-entry posteriors (scheme v1, fitted & weak order, b0/b2), entry 60 and group region
pg = rd('posterior_grid_v1.csv')
rows = []
for r in pg:
    if r['candidate'] not in ('tell_es_sultan', 'ein_samiya', 'kh_yanun', 'carmel_siah', 'mount_zion', 'ein_feshkha', 'muhalhil'):
        continue
    if r['scheme'] not in ('v1', 'equal') or r['excl'] == 'b1_doc':
        continue
    rows.append({k: r.get(k, '') for k in ('kernel', 'excl', 'tie', 'order', 'w_A', 'w_L', 'reading', 'scheme', 'candidate',
                                           'group_P', 'group_P_region', 'e4_P10km', 'e19_P10km', 'e60_P', 'e60_P10km')})
w = csv.DictWriter(open(os.path.join(out, 'table_fullmodel_kohlit.csv'), 'w', newline=''), fieldnames=list(rows[0]))
w.writeheader(); w.writerows(rows)
print('tables written')
