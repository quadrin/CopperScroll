"""Gazetteers for the frozen test (built BEFORE any matching).
 S2  repo research/regional/mandate_maps/names.csv, rebuilt with run 19's build_S2 code verbatim (must reproduce run 19 SHA-256
     95130cea...8d); Mandate 1:20,000 window readings.
 S4  run 19 addendum A1 direct reading of sheets 18-12, 18-13, 19-14 (478 names), copied verbatim from origin/sandbox/methods
     sandbox/field_names_2026-10-27/out/A1/gaz_S4.csv (SHA-256 5378499b...2cff).
 ASI research/regional/asi_jerusalem/sites.csv (IAA Archaeological Survey of Israel site names), region box of run 19,
     romanized 'name' column only, run 19 S3 exclusions applied (Hebrew romanization markers; English words), mode 'branch'.
usage: python3 -I build_gazetteers.py REPO OUTDIR
"""
import sys, os, csv, json, hashlib, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from askel import is_english, is_hebrew_roman
REPO, OUT = sys.argv[1], sys.argv[2]
LAT0, LAT1, LON0, LON1 = 31.40, 32.55, 35.00, 35.60
def inreg(lat, lon): return LAT0 <= lat <= LAT1 and LON0 <= lon <= LON1
FIELDS = ['src', 'gid', 'name', 'script', 'mode', 'lat', 'lon', 'cls', 'note']
def write(fn, rows):
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); [w.writerow(r) for r in rows]
def sha(fn): return hashlib.sha256(open(fn, 'rb').read()).hexdigest()
man = {}
# S2: run 19 build_S2, verbatim logic
rows = []
mm = f'{REPO}/research/regional/mandate_maps/names.csv'
for r in csv.DictReader(open(mm, encoding='utf-8')):
    lat, lon = float(r['lat']), float(r['lon'])
    if not inreg(lat, lon): continue
    nm = r['name_as_printed']
    if r.get('arabic_script_inferred'):
        rows.append(dict(src='S2', gid=r['item_id'], name=r['arabic_script_inferred'], script='ar', mode='exact', lat=lat, lon=lon, cls=r['feature_class'], note=f"{r['sheet']} {nm} (Arabic INFERRED by repo)"))
    nm = re.sub(r'\(([^)]*)\)', lambda m: '' if (is_english(m.group(1)) or m.group(1).strip() in ('R.', 'R')) else m.group(0), nm)
    nm = ' / '.join(p_ for p_ in nm.split('/') if p_.strip() and not is_english(p_)).strip()
    if not nm or is_english(nm): continue
    rows.append(dict(src='S2', gid=r['item_id'], name=nm, script='lat', mode='branch', lat=lat, lon=lon, cls=r['feature_class'], note=f"{r['sheet']} grid {r['grid_e']},{r['grid_n']}"))
write(f'{OUT}/gaz_S2.csv', rows)
man['S2'] = dict(file='gaz_S2.csv', raw=mm, raw_sha256=sha(mm), n_names=len(rows), sha256=sha(f'{OUT}/gaz_S2.csv'),
                 run19_sha256='95130ceda475ca2223052747f66a18eafd2cc87189223035e13b8ab050255f8d')
man['S2']['reproduces_run19'] = man['S2']['sha256'] == man['S2']['run19_sha256']
# S4: copy already in inputs/
s4 = os.path.join(os.path.dirname(OUT), 'inputs', 'gaz_S4.csv')
man['S4'] = dict(file='inputs/gaz_S4.csv', source='origin/sandbox/methods:sandbox/field_names_2026-10-27/out/A1/gaz_S4.csv (commit eb0ef639)',
                 n_names=sum(1 for _ in csv.DictReader(open(s4, encoding='utf-8'))), sha256=sha(s4))
# ASI
asi = f'{REPO}/research/regional/asi_jerusalem/sites.csv'
rows = []; excl = {'outside region or no coordinates': 0, 'Hebrew romanization markers': 0, 'English words': 0, 'empty name': 0}
for r in csv.DictReader(open(asi, encoding='utf-8')):
    try: lat, lon = float(r['lat']), float(r['lon'])
    except ValueError: excl['outside region or no coordinates'] += 1; continue
    if not inreg(lat, lon): excl['outside region or no coordinates'] += 1; continue
    nm = r['name'].strip()
    nm = re.sub(r'\[[^\]]*\]|\(\d+\)|\((?:M|north|south|east|west|centre|center)\)', ' ', nm).strip()
    if not nm: excl['empty name'] += 1; continue
    if is_hebrew_roman(nm): excl['Hebrew romanization markers'] += 1; continue
    if is_english(nm): excl['English words'] += 1; continue
    rows.append(dict(src='ASI', gid=f"{r['map_num']}/{r['site_num']}/{r['record_id']}", name=nm, script='lat', mode='branch', lat=lat, lon=lon,
                     cls=r['feature_classes'], note=f"ASI map {r['map_num']} {r['map_name']} site {r['site_num']}; he: {r['name_he']}"))
write(f'{OUT}/gaz_ASI.csv', rows)
man['ASI'] = dict(file='gaz_ASI.csv', raw=asi, raw_sha256=sha(asi), n_names=len(rows), excluded=excl, sha256=sha(f'{OUT}/gaz_ASI.csv'))
json.dump(man, open(f'{OUT}/gazetteer_manifest.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(man, indent=1, ensure_ascii=False))
