"""Build the gazetteers (region 31.40-32.55 N, 35.00-35.60 E) BEFORE any matching; write CSVs and a manifest with SHA-256.
S1a  POM place-name layer (palopenmaps.org/api/localities): Palestinian/Mixed localities existing by 1948 (Arabic script; Latin if no Arabic)
S1b  POM 1940s vector overlay (tiler.palopenmaps.org/maps/osm, z14, ODbL): every named feature (Latin, undotted -> branch mode)
S2   repo research/regional/mandate_maps/names.csv (names read off nine 1:20,000 windows; deviation: not an open gazetteer, windows only)
S3   NGA GNS West Bank + Israel + Jordan country files (deviation: not shown to derive from the 1:20,000 sheets)
"""
import sys, os, csv, json, glob, gzip, hashlib, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tileutil import num2deg
from askel import is_english, is_hebrew_roman
D, OUT, REPO = sys.argv[1], sys.argv[2], sys.argv[3]
WANT = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else {'S1a', 'S1b', 'S2', 'S3'}
LAT0, LAT1, LON0, LON1 = 31.40, 32.55, 35.00, 35.60
def inreg(lat, lon): return LAT0 <= lat <= LAT1 and LON0 <= lon <= LON1
FIELDS = ['src', 'gid', 'name', 'script', 'mode', 'lat', 'lon', 'cls', 'note']
def write(fn, rows):
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); [w.writerow(r) for r in rows]
def sha(fn): return hashlib.sha256(open(fn, 'rb').read()).hexdigest()
MF = f'{OUT}/gazetteer_manifest.json'
man = json.load(open(MF)) if os.path.exists(MF) else {'region': [LAT0, LAT1, LON0, LON1], 'sources': {}}
_unused = {'built_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'region': [LAT0, LAT1, LON0, LON1], 'sources': {}}

def build_S1a():
    loc = json.load(open(f'{D}/pom_localities.json'))
    rows = []
    for i, f in enumerate(loc['features']):
        lon, lat = f['geometry']['coordinates'][:2]; p = f['properties']
        if not inreg(lat, lon): continue
        if p['group'] not in ('Palestinian', 'Mixed') or (p['start'] or 0) > 1948: continue
        if p.get('name_ar'):
            rows.append(dict(src='S1a', gid=p['slug'], name=p['name_ar'], script='ar', mode='exact', lat=lat, lon=lon, cls=p['type'], note=p['name_en']))
        else:
            rows.append(dict(src='S1a', gid=p['slug'], name=p['name_en'], script='lat', mode='branch', lat=lat, lon=lon, cls=p['type'], note='no Arabic in layer'))
    write(f'{OUT}/gaz_S1a.csv', rows)
    man['sources']['S1a'] = dict(file='gaz_S1a.csv', raw='dl/pom_localities.json', raw_sha256=sha(f'{D}/pom_localities.json'),
        url='https://palopenmaps.org/api/localities', n_names=len(rows), n_features=len({r['gid'] for r in rows}))

if 'S1a' in WANT: build_S1a()

def build_S1b():
    import mapbox_vector_tile as mvt
    tiles = sorted(glob.glob(f'{D}/pomtiles/14_*.pbf'))
    feat = {}
    NAME_KEYS = ('name', 'name:ar', 'name:en', 'old_name', 'alt_name')
    for fn in tiles:
        _, x, y = os.path.basename(fn)[:-4].split('_'); x, y = int(x), int(y)
        b = open(fn, 'rb').read()
        if not b: continue
        if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
        d = mvt.decode(b)
        for layer, v in d.items():
            ext = v.get('extent', 4096)
            for ft in v['features']:
                p = ft['properties']
                names = [(k, p[k]) for k in NAME_KEYS if p.get(k)]
                if not names: continue
                g = ft['geometry']; coords = []
                def walk(c):
                    if isinstance(c, (list, tuple)) and c and isinstance(c[0], (int, float)): coords.append(c)
                    elif isinstance(c, (list, tuple)): [walk(cc) for cc in c]
                walk(g['coordinates'])
                pts = []
                for cx, cy in coords:
                    lat, lon = num2deg(x + cx / ext, y + (1 - cy / ext), 14)   # mvt decoder default y-up
                    pts.append((lat, lon))
                ins = [q for q in pts if inreg(*q)]
                if not ins: continue
                for k, nm in names:
                    nm = str(nm)
                    if not any('؀' <= ch <= 'ۿ' for ch in nm) and is_english(nm): continue
                    key = (layer, nm, p.get('type', ''), p.get('class', ''))
                    e = feat.setdefault(key, dict(osm_ids=set(), pts=[], key=k))
                    e['osm_ids'].add(p.get('osm_id', '')); e['pts'].extend(ins)
    rows = []
    for (layer, nm, typ, cls), e in sorted(feat.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        lat = sum(q[0] for q in e['pts']) / len(e['pts']); lon = sum(q[1] for q in e['pts']) / len(e['pts'])
        ar = any('؀' <= c <= 'ۿ' for c in nm)
        rows.append(dict(src='S1b', gid=f"{layer}:{'|'.join(sorted(str(i) for i in e['osm_ids']))[:60]}", name=nm, script='ar' if ar else 'lat',
                         mode='exact' if ar else 'branch', lat=round(lat, 6), lon=round(lon, 6), cls=f'{layer}/{cls}/{typ}', note=e['key']))
    write(f'{OUT}/gaz_S1b.csv', rows)
    h = hashlib.sha256()
    for fn in tiles: h.update(os.path.basename(fn).encode()); h.update(open(fn, 'rb').read())
    man['sources']['S1b'] = dict(file='gaz_S1b.csv', raw=f'dl/pomtiles ({len(tiles)} z14 tiles)', raw_sha256_tiles_concat=h.hexdigest(),
        url='https://tiler.palopenmaps.org/maps/osm/14/{x}/{y}.pbf', n_names=len(rows),
        by_layer=dict(collections.Counter(r['cls'].split('/')[0] for r in rows)))

if 'S1b' in WANT: build_S1b()

def build_S2():
    rows = []
    mm = f'{REPO}/research/regional/mandate_maps/names.csv'
    for r in csv.DictReader(open(mm, encoding='utf-8')):
        lat, lon = float(r['lat']), float(r['lon'])
        if not inreg(lat, lon): continue
        nm = r['name_as_printed']
        if r.get('arabic_script_inferred'):
            rows.append(dict(src='S2', gid=r['item_id'], name=r['arabic_script_inferred'], script='ar', mode='exact', lat=lat, lon=lon, cls=r['feature_class'], note=f"{r['sheet']} {nm} (Arabic INFERRED by repo)"))
        import re as _re
        nm = _re.sub(r'\(([^)]*)\)', lambda m: '' if (is_english(m.group(1)) or m.group(1).strip() in ('R.', 'R')) else m.group(0), nm)
        nm = ' / '.join(p_ for p_ in nm.split('/') if p_.strip() and not is_english(p_)).strip()
        if not nm or is_english(nm): continue
        rows.append(dict(src='S2', gid=r['item_id'], name=nm, script='lat', mode='branch', lat=lat, lon=lon, cls=r['feature_class'], note=f"{r['sheet']} grid {r['grid_e']},{r['grid_n']}"))
    write(f'{OUT}/gaz_S2.csv', rows)
    man['sources']['S2'] = dict(file='gaz_S2.csv', raw='research/regional/mandate_maps/names.csv', raw_sha256=sha(mm), n_names=len(rows), n_items=len({r['gid'] for r in rows}))

if 'S2' in WANT: build_S2()

def build_S3():
    rows = []; raw = {}
    allr = []
    for c in ['West%20Bank/West Bank.txt', 'Israel/Israel.txt', 'Jordan/Jordan.txt']:
        fn = f'{D}/gns/{c}'; raw[c] = sha(fn)
        for x in csv.DictReader(open(fn, encoding='utf-8'), delimiter='\t'):
            lat, lon = float(x['lat_dd']), float(x['long_dd'])
            if inreg(lat, lon): allr.append(x)
    hebfeat = {x['ufi'] for x in allr if x['lang_cd'] == 'heb' or x['script_cd'] == 'Hebr'}
    seen = set(); excl = collections.Counter()
    for x in allr:
        key = (x['ufi'], x['full_name'])
        if key in seen: continue
        seen.add(key)
        if x['lang_cd'] in ('heb', 'eng') or x['script_cd'] == 'Hebr' or x['nt'] == 'C': excl['hebrew/english/conventional'] += 1; continue
        if x['desig_cd'] == 'STLMT': excl['Israeli settlement (STLMT)'] += 1; continue
        if is_hebrew_roman(x['full_name']): excl['Hebrew romanization markers'] += 1; continue
        if x['script_cd'] == 'Arab' or any('؀' <= ch <= 'ۿ' for ch in x['full_name']):
            rows.append(dict(src='S3', gid=x['ufi'], name=x['full_name'], script='ar', mode='exact', lat=x['lat_dd'], lon=x['long_dd'], cls=x['desig_cd'], note=f"nt={x['nt']} mgrs={x['mgrs']}")); continue
        if x['lang_cd'] == '' and x['ufi'] in hebfeat: excl['unlabelled romanization on a Hebrew-named feature'] += 1; continue
        if is_english(x['full_name']): excl['English words'] += 1; continue
        rows.append(dict(src='S3', gid=x['ufi'], name=x['full_name'], script='lat', mode='exact', lat=x['lat_dd'], lon=x['long_dd'], cls=x['desig_cd'], note=f"nt={x['nt']} mgrs={x['mgrs']}"))
    write(f'{OUT}/gaz_S3.csv', rows)
    man['sources']['S3'] = dict(file='gaz_S3.csv', raw={k: v for k, v in raw.items()}, url='https://geonames.nga.mil/geonames/GNSData/{West Bank,Israel,Jordan}.zip (files dated 2026-10-21)',
        n_names=len(rows), n_features=len({r['gid'] for r in rows}), n_region_rows=len(allr), excluded=dict(excl))
if 'S3' in WANT: build_S3()

now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
for k in WANT:
    v = man['sources'][k]; v['sha256'] = sha(f"{OUT}/{v['file']}"); v['built_utc'] = now
json.dump(man, open(f'{OUT}/gazetteer_manifest.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(man, indent=1, ensure_ascii=False))
