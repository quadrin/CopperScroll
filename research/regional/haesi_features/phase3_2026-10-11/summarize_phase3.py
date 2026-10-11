"""Totals across phase-3 parts A-D (rows as coded; not deduplicated across parts or seasons).
Run: python3 -I summarize_phase3.py  (writes summary_phase3.json)"""
import csv, json, collections, os
csv.field_size_limit(10**9)
HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = ['part_a', 'part_b', 'part_c', 'part_d_online']
out = {'note': 'Feature rows as coded per report and class; repeated seasons and Hebrew/English versions of one report are not yet deduplicated.', 'parts': {}, 'by_class': {}, 'by_zone': {}}
cls = collections.defaultdict(collections.Counter); zone = collections.Counter()
for p in PARTS:
    f = list(csv.DictReader(open(os.path.join(HERE, p, 'features.csv'), encoding='utf-8')))
    r = list(csv.DictReader(open(os.path.join(HERE, p, 'reports.csv'), encoding='utf-8')))
    inreg = [x for x in f if x['region_zone'] and not x['region_zone'].lower().startswith('outside')]
    out['parts'][p] = {'reports': len(r), 'feature_rows_in_region': len(inreg),
                       'dated_in_window': dict(collections.Counter(x['dated_in_window'] for x in inreg))}
    for x in inreg:
        cls[x['feature_type']][x['dated_in_window']] += 1; zone[x['region_zone']] += 1
out['by_class'] = {k: dict(v) for k, v in sorted(cls.items(), key=lambda kv: -sum(kv[1].values()))}
out['by_zone'] = dict(zone)
out['totals'] = {'reports': sum(v['reports'] for v in out['parts'].values()), 'feature_rows_in_region': sum(v['feature_rows_in_region'] for v in out['parts'].values())}
json.dump(out, open(os.path.join(HERE, 'summary_phase3.json'), 'w'), indent=2, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
