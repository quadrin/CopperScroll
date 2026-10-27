"""Recorded site points used to screen control tiles: WBADB (surveyed + excavations) and Mar Saba map (Patrich 1994) IAA points."""
import json, pathlib, openpyxl, pyproj

SCR = pathlib.Path('/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad')
OUT = pathlib.Path(__file__).parent.parent / 'out'
t = pyproj.Transformer.from_crs('EPSG:28191', 'EPSG:4326', always_xy=True)
pts = []
wb = openpyxl.load_workbook(SCR / 'kohlit_south_of_yanun_2026-10-27/dl/WBADB_data1.xlsx', read_only=True)
for sheet in ('Surveyed', 'Excavations'):
    ws = wb[sheet]
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i == 0 or r[1] is None: continue
        try: x, y = float(r[1]), float(r[2])
        except (TypeError, ValueError): continue
        lon, lat = t.transform(x, y)
        pts.append({'src': 'WBADB-' + sheet, 'id': r[0], 'name': r[3], 'lat': lat, 'lon': lon, 'what': str(r[9] if sheet == 'Surveyed' else r[8])[:200]})
for s in json.load(open('/home/claude/copperscroll/sandbox/samra_hyrcania_valley_2026-10-27/out/marsaba_sites_dist.json')):
    pts.append({'src': 'MarSaba', 'id': s['n'], 'name': s['name'], 'lat': s['lat'], 'lon': s['lon'], 'what': s['finds']})
json.dump(pts, open(OUT / 'site_points.json', 'w'), ensure_ascii=False)
print(len(pts))
near = [p for p in pts if 31.70 < p['lat'] < 31.79 and 35.43 < p['lon'] < 35.48]
for p in near: print(p['src'], p['id'], p['name'], round(p['lat'], 5), round(p['lon'], 5), p['what'][:80])
