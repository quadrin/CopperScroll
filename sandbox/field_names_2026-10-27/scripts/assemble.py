"""Combine per-source results into one per-unit table, and add 1:20,000 sheet numbers (Palestine grid, EPSG:28191) to every match."""
import sys, csv, json, os
from pyproj import Transformer
O = sys.argv[1]; SRCS = sys.argv[2].split(',')
T = Transformer.from_crs('EPSG:4326', 'EPSG:28191', always_xy=True)
def sheet(lat, lon):
    e, n = T.transform(float(lon), float(lat)); return f'{int(e // 10000)}-{int(n // 10000)}', round(e), round(n)
per = {}
for s in SRCS:
    for r in csv.DictReader(open(f'{O}/{s}_per_unit.csv', encoding='utf-8')):
        u = per.setdefault(r['unit'], dict(unit=r['unit'], label=r['label'], kind=r['kind'], status=r['status'], entries=r['entries']))
        u[f'{s}_match'] = r['match']; u[f'{s}_features'] = r['n_features']; u[f'{s}_c1'] = r['c1']; u[f'{s}_lead'] = r['lead']
    rows = list(csv.DictReader(open(f'{O}/{s}_matches.csv', encoding='utf-8')))
    if rows and 'unit' in rows[0]:
        for r in rows:
            sh, e, n = sheet(r['lat'], r['lon']); r['sheet_1to20k'] = sh; r['pal_grid_E'] = e; r['pal_grid_N'] = n
        with open(f'{O}/{s}_matches_sheets.csv', 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
L = list(per.values())
with open(f'{O}/per_unit_all_sources.csv', 'w', newline='', encoding='utf-8') as f:
    keys = []
    for u in L:
        for k in u:
            if k not in keys: keys.append(k)
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); [w.writerow(u) for u in L]
print('units', len(L))
