#!/usr/bin/env python3
"""Fetch the ASI records that plan.json (with plan_amendment_1.json) selects, into a local cache.

Run:  python3 -I scripts/fetch_asi.py CACHE_DIR [MAX_MINUTES] [--skip-records]
The cache stays outside the repository. Each response is fetched once (cached by endpoint and
parameters), at most one request per second, with the header Content-Type: application/json
(the site's own AngularJS calls send the same). No images are fetched.
CACHE_DIR/manifest.csv lists URL, HTTP status, size, SHA-256 and fetch time of every response.
Phase 1: map list, sheet grid, English and Hebrew GeoJSON and introductions of selected maps.
Phase 2: GetSiteDesc2 records in the amendment's tier order, until MAX_MINUTES (default 600).
Phase 3: the GetSiteRemains probe. --skip-records skips phase 2 (used to run the probe after
phase 2 was stopped by hand).
"""
import csv
import datetime as dt
import json
import os
import signal
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import asi_common as C  # noqa: E402

BASE = 'https://survey.iaa.org.il/aspxService/'
MIN_GAP = 1.2
FOCUS = {'JER', 'DESERT', 'SOUTH', 'QUMRAN', 'JERICHO'}
_last = [0.0]
MANIFEST = {}
CACHE = ['']


def utc(ts=None):
    t = dt.datetime.fromtimestamp(ts, dt.timezone.utc) if ts else dt.datetime.now(dt.timezone.utc)
    return t.strftime('%Y-%m-%dT%H:%M:%SZ')


def load_manifest(cache):
    path = os.path.join(cache, 'manifest.csv')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            MANIFEST.update({r['cache_file']: r for r in csv.DictReader(f)})


def write_manifest(*_):
    path = os.path.join(CACHE[0], 'manifest.csv')
    cols = ['cache_file', 'url', 'http_status', 'bytes', 'sha256', 'fetched_utc']
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for k in sorted(MANIFEST):
            w.writerow(MANIFEST[k])
    os.replace(tmp, path)


def _record_existing(name, path, url):
    if name not in MANIFEST:
        st = os.stat(path)
        MANIFEST[name] = dict(cache_file=name, url=url, http_status='200', bytes=str(st.st_size),
                              sha256=C.sha256_file(path), fetched_utc=utc(st.st_mtime))


def fetch(url, name):
    path = os.path.join(CACHE[0], name)
    if os.path.exists(path):
        _record_existing(name, path, url)
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    gap = time.time() - _last[0]
    if gap < MIN_GAP:
        time.sleep(MIN_GAP - gap)
    req = urllib.request.Request(url, headers={'Content-Type': 'application/json',
                                               'User-Agent': 'copper-scroll-research (read-only; 1 req/s)'})
    status, body = None, b''
    t0 = time.time()
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                status, body = r.status, r.read()
            break
        except urllib.error.HTTPError as e:
            status, body = e.code, e.read()
            break
        except Exception as e:  # network hiccup: wait and retry
            print('retry', url, type(e).__name__, file=sys.stderr, flush=True)
            time.sleep(5 * (attempt + 1))
    _last[0] = time.time()
    if status != 200:
        MANIFEST['ERR_' + name] = dict(cache_file='ERR_' + name, url=url, http_status=str(status),
                                       bytes=str(len(body)), sha256='', fetched_utc=utc())
        print('HTTP', status, url, file=sys.stderr, flush=True)
        return None
    with open(path, 'wb') as f:
        f.write(body)
    MANIFEST[name] = dict(cache_file=name, url=url, http_status='200', bytes=str(len(body)),
                          sha256=C.sha256_file(path), fetched_utc=utc())
    print(f'{utc()} {time.time() - t0:5.1f}s {name}', flush=True)
    return json.loads(body.decode('utf-8'))


def api(endpoint, query=''):
    params = dict(p.split('=', 1) for p in query.split('&') if p) if query else {}
    return fetch(BASE + endpoint + ('?' + query if query else ''), C.cache_name(endpoint, **params))


def selected_maps(plan, places, cache_get):
    maps = cache_get('Service_Eng.aspx/GetMaps')['d']
    grid = fetch(BASE + 'GetIsraelGrid.aspx', 'GetIsraelGrid.json')
    sheets = C.sheets_from_grid(grid)
    online = {str(m['id']): m for m in maps}
    out = []
    for mid, sh in sorted(sheets.items(), key=lambda kv: int(kv[0])):
        if mid not in online:
            continue
        dmin = min(C.rect_km(p['lat_f'], p['lon_f'], sh['lat_lo'], sh['lat_hi'], sh['lon_lo'], sh['lon_hi'])
                   for p in places)
        if dmin <= 3.0:
            out.append(mid)
    return out, online, sheets


def site_tiers(places, en_by_map):
    """Return list of (tier, dist, site_id, map_id, site_num) for sites within 3.5 km."""
    rows = []
    for mid, en in en_by_map.items():
        for ft in en['d']['features']:
            lon, lat = ft['geometry']['coordinates'][:2]
            best = None
            best_focus = None
            for p in places:
                d = C.km(lat, lon, p['lat_f'], p['lon_f'])
                if best is None or d < best:
                    best = d
                if p['model_region'] in FOCUS and (best_focus is None or d < best_focus):
                    best_focus = d
            if best > 3.5:
                continue
            pr = C.geojson_props(ft)
            sid = int(pr['id'])
            if best_focus is not None and best_focus <= 1.0:
                tier = 1
            elif best <= 1.0:
                tier = 2
            elif best_focus is not None and best_focus <= 3.5:
                tier = 3
            else:
                tier = 4
            rows.append((tier, round(best, 6), sid, mid, int(pr.get('site_num') or 0)))
    rows.sort()
    return rows


def main(cache, max_minutes, skip_records=False):
    CACHE[0] = cache
    os.makedirs(cache, exist_ok=True)
    load_manifest(cache)
    signal.signal(signal.SIGTERM, lambda *a: (write_manifest(), sys.exit(1)))
    t_end = time.time() + 60 * max_minutes
    plan = C.load_plan()
    places, _ = C.load_places(plan)
    try:
        mids, online, _ = selected_maps(plan, places, api)
        print('selected maps:', ', '.join(f"{m}={online[m]['map_num']}" for m in mids), flush=True)
        en_by_map = {}
        for mid in mids:  # phase 1
            en_by_map[mid] = api('Service_Eng.aspx/GetPolygonsSites', f'MapId={mid}&sitesId=null')
            api('Service.aspx/GetPolygonsSites', f'MapId={mid}&sitesId=null')
            api('Service_Eng.aspx/GetMapIntro', f'mapId={mid}')
            api('Service.aspx/GetMapIntro', f'mapId={mid}')
        write_manifest()
        tiers = site_tiers(places, en_by_map)
        counts = {}
        for t in tiers:
            counts[t[0]] = counts.get(t[0], 0) + 1
        print('sites per tier:', counts, flush=True)
        n = 0
        for tier, _, sid, mid, _ in tiers:  # phase 2
            if skip_records:
                break
            if time.time() > t_end:
                print('time limit reached', flush=True)
                break
            api('Service_Eng.aspx/GetSiteDesc2', f'Id={sid}')
            n += 1
            if n % 20 == 0:
                write_manifest()
        write_manifest()
        by_map = {}
        for tier, _, sid, mid, snum in tiers:  # phase 3
            if tier == 1:
                by_map.setdefault(mid, []).append((snum, sid))
        for mid in sorted(by_map, key=int):
            for snum, sid in sorted(by_map[mid])[:10]:
                if time.time() > t_end:
                    break
                r = api('Service_Eng.aspx/GetSiteRemains', f'Id={sid}')
                d = (r or {}).get('d')
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except ValueError:
                        pass
                if d:
                    print('NON-EMPTY remains', mid, sid, flush=True)
    finally:
        write_manifest()


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3, 4):
        sys.exit(__doc__)
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) >= 3 else 600.0,
         skip_records=(len(sys.argv) == 4 and sys.argv[3] == '--skip-records'))
