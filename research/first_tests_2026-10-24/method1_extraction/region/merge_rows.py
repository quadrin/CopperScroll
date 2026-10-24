"""Merge the batch outputs, re-run the mechanical checks, and attach each report's location.

Usage: python3 -I merge_rows.py
Writes online_features.csv (one row per feature, with the report's map-reference point and nearest place)
and merge_report.txt (coverage and verbatim-check counts).
"""
import csv, json, re, glob, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
man = {m['report']: m for m in json.load(open(os.path.join(HERE, 'scope_manifest.json'), encoding='utf-8'))}
screen = {r['id']: r for r in csv.DictReader(open(os.path.join(HERE, 'online_screen_all.csv'), encoding='utf-8'))}
TYPES = {'none', 'cistern', 'pool_reservoir', 'channel_aqueduct', 'ritual_bath', 'rockcut_installation',
         'tomb_burial_cave', 'cave_with_finds', 'wall_tower', 'hoard_cache'}


def norm(s):
    s = (s or '').replace(' ', ' ').replace('­', '')
    return re.sub(r'\s+', ' ', s).strip().lower()


texts = {}


def text(rid):
    if rid not in texts:
        texts[rid] = norm(open(man[rid]['text'], encoding='utf-8', errors='replace').read())
    return texts[rid]


rows, bad, seen, unknown_type = [], Counter(), set(), Counter()
for f in sorted(glob.glob(os.path.join(HERE, 'model_rows', 'b*.csv'))):
    batch = os.path.basename(f)[:-4]
    for r in csv.DictReader(open(f, encoding='utf-8')):
        rid = str(r['report']).strip().lstrip('0') or '0'
        if rid not in man:
            bad['report id not in scope'] += 1
            continue
        seen.add(rid)
        if r['feature_type'] not in TYPES:
            unknown_type[r['feature_type']] += 1
        flags = []
        for fld in ('quote', 'period_as_given', 'size_as_given', 'depth_as_given', 'location_as_given'):
            v = norm(r.get(fld))
            if v and v not in text(rid):
                flags.append(fld); bad[fld] += 1
        s = screen[rid]
        rows.append(dict(batch=batch, report=rid, volume=man[rid]['volume'], date=man[rid]['date'], title=man[rid]['title'],
                         lat=s['lat'], lon=s['lon'], ref=s['ref'], grid=s['grid'], nearest_place=s['nearest'], km=s['km'],
                         within_2km=s['within_2km'], within_5km=s['within_5km'], regions=s['regions'],
                         **{k: r.get(k, '') for k in ('feature_type', 'label', 'count', 'period_as_given', 'dated_in_window',
                                                       'size_as_given', 'depth_as_given', 'location_as_given', 'quote')},
                         not_verbatim=';'.join(flags)))
fields = list(rows[0].keys()) if rows else []
with open(os.path.join(HERE, 'online_features.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
missing = sorted(set(man) - seen, key=int)
feat = [r for r in rows if r['feature_type'] != 'none']
rep = [f'reports in scope: {len(man)}; covered: {len(seen)}; missing: {len(missing)}',
       f'rows: {len(rows)}; feature rows: {len(feat)}',
       'rows per type: ' + ', '.join(f'{k} {v}' for k, v in Counter(r['feature_type'] for r in rows).most_common()),
       'dated in window: ' + ', '.join(f'{k} {v}' for k, v in Counter(r['dated_in_window'] for r in feat).most_common()),
       'not verbatim: ' + ', '.join(f'{k} {v}' for k, v in bad.items()) if bad else 'not verbatim: none',
       'unknown feature types: ' + (', '.join(f'{k} {v}' for k, v in unknown_type.items()) or 'none'),
       'missing reports: ' + ' '.join(missing[:60])]
open(os.path.join(HERE, 'merge_report.txt'), 'w').write('\n'.join(rep) + '\n')
print('\n'.join(rep))
