#!/usr/bin/env python3
"""Fetch the ASI map list, the sheet grid and the English GeoJSON of every online map whose sheet
intersects Region A or Region B (PLAN §2-3), into a cache outside the repository.

Run from the repository root:
    python3 -I research/regional/tombs/scripts/fetch_asi_maps.py CACHE_DIR
At most one request per second; each response is fetched once. CACHE_DIR/manifest.csv lists URL,
HTTP status, size, SHA-256 and fetch time. Same services and headers as research/regional/asi_jerusalem.
No image is fetched.
"""
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tombs_common as T  # noqa: E402

BASE = 'https://survey.iaa.org.il/aspxService/'
MIN_GAP = 1.2
_last = [0.0]


def utc():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def fetch(cache, url, name, manifest):
    path = os.path.join(cache, name)
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    gap = time.time() - _last[0]
    if gap < MIN_GAP:
        time.sleep(MIN_GAP - gap)
    req = urllib.request.Request(url, headers={'Content-Type': 'application/json',
                                               'User-Agent': 'copper-scroll-research (read-only; 1 req/s)'})
    status, body = None, b''
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                status, body = r.status, r.read()
            break
        except urllib.error.HTTPError as e:
            status, body = e.code, e.read()
            break
        except Exception as e:  # noqa: BLE001
            print('retry', url, type(e).__name__, file=sys.stderr, flush=True)
            time.sleep(5 * (attempt + 1))
    _last[0] = time.time()
    manifest.append(dict(cache_file=name, url=url, http_status=str(status), bytes=str(len(body)),
                         sha256=T.hashlib.sha256(body).hexdigest() if status == 200 else '',
                         fetched_utc=utc()))
    if status != 200:
        print('HTTP', status, url, file=sys.stderr, flush=True)
        return None
    with open(path, 'wb') as f:
        f.write(body)
    print(utc(), name, len(body), flush=True)
    return json.loads(body.decode('utf-8'))


def sheets_from_grid(grid):
    out = {}
    for ft in grid['features']:
        props = ft.get('properties') or {}
        mid = str(props.get('itemid', '')).strip()
        geom = ft.get('geometry') or {}
        if not mid or geom.get('type') != 'Polygon':
            continue
        pts = geom['coordinates'][0]
        lons = [p[0] for p in pts]
        lats = [p[1] for p in pts]
        out[mid] = dict(lat_lo=min(lats), lat_hi=max(lats), lon_lo=min(lons), lon_hi=max(lons),
                        map_num=str(props.get('name', '')).strip())
    return out


def sheet_hits_region(plan, sh):
    """A sheet intersects a region if its nearest point to the region's defining geometry is within
    the region's distance (5 km corridor used for B2, as the plan's sensitivity bound)."""
    P, R = plan['points'], plan['regions']
    a = T.rect_km(*P['jer_temple'], sh['lat_lo'], sh['lat_hi'], sh['lon_lo'], sh['lon_hi'])
    b1 = min(T.rect_km(*P[k], sh['lat_lo'], sh['lat_hi'], sh['lon_lo'], sh['lon_hi'])
             for k in ('tell_es_sultan', 'jericho_palaces'))
    # corridor: sample the segment every 100 m
    (la1, lo1), (la2, lo2) = P['jericho_palaces'], P['kh_qumran']
    n = 150
    b2 = min(T.rect_km(la1 + (la2 - la1) * i / n, lo1 + (lo2 - lo1) * i / n,
                       sh['lat_lo'], sh['lat_hi'], sh['lon_lo'], sh['lon_hi']) for i in range(n + 1))
    return a <= R['A_radius_km'], b1 <= R['B1_radius_km'], b2 <= R['B2_sensitivity_halfwidth_km']


def main(cache):
    os.makedirs(cache, exist_ok=True)
    plan = T.load_plan()
    manifest = []
    maps = fetch(cache, BASE + 'Service_Eng.aspx/GetMaps', 'GetMaps.json', manifest)['d']
    grid = fetch(cache, BASE + 'GetIsraelGrid.aspx', 'GetIsraelGrid.json', manifest)
    sheets = sheets_from_grid(grid)
    online = {str(m['id']): m for m in maps}
    sel = []
    for mid, sh in sorted(sheets.items(), key=lambda kv: int(kv[0])):
        if mid not in online:
            continue
        a, b1, b2 = sheet_hits_region(plan, sh)
        if a or b1 or b2:
            sel.append(dict(map_id=mid, map_num=online[mid].get('mapNum') or sh['map_num'],
                            name=online[mid].get('name', ''), author=online[mid].get('author', ''),
                            hits_A=a, hits_B1=b1, hits_B2_5km=b2, **{k: sh[k] for k in ('lat_lo', 'lat_hi', 'lon_lo', 'lon_hi')}))
    for s in sel:
        fetch(cache, f"{BASE}Service_Eng.aspx/GetPolygonsSites?MapId={s['map_id']}&sitesId=null",
              f"GetPolygonsSites_Eng__MapId-{s['map_id']}.json", manifest)
        fetch(cache, f"{BASE}Service_Eng.aspx/GetMapIntro?mapId={s['map_id']}",
              f"GetMapIntro_Eng__mapId-{s['map_id']}.json", manifest)
    with open(os.path.join(cache, 'selected_maps.json'), 'w', encoding='utf-8') as f:
        json.dump(sel, f, ensure_ascii=False, indent=1)
    path = os.path.join(cache, 'manifest.csv')
    old = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            old = list(csv.DictReader(f))
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['cache_file', 'url', 'http_status', 'bytes', 'sha256', 'fetched_utc'],
                           lineterminator='\n')
        w.writeheader()
        for r in old + manifest:
            w.writerow(r)
    print('selected maps:', [(s['map_id'], s['map_num'], s['name']) for s in sel])


if __name__ == '__main__':
    main(sys.argv[1])
