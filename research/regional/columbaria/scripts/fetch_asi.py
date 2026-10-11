#!/usr/bin/env python3
"""Fetch the ASI online records that PLAN.md §4 (S1) selects, into a cache outside the repository.

Run:  python3 -I scripts/fetch_asi.py CACHE_DIR            # phase 1: map list, grid, en+he GeoJSON
      python3 -I scripts/fetch_asi.py CACHE_DIR --records  # phase 2: GetSiteDesc2 of every screened hit

At most one request per 1.2 s, header Content-Type: application/json (as the site's own calls send).
CACHE_DIR/manifest.csv lists URL, HTTP status, size, SHA-256 and fetch time of every response.
No images are fetched.
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
import colcommon as C  # noqa: E402

BASE = 'https://survey.iaa.org.il/aspxService/'
MIN_GAP = 1.2
_last = [0.0]
MANIFEST = {}
CACHE = ['']


def utc(ts=None):
    t = dt.datetime.fromtimestamp(ts, dt.timezone.utc) if ts else dt.datetime.now(dt.timezone.utc)
    return t.strftime('%Y-%m-%dT%H:%M:%SZ')


def load_manifest():
    path = os.path.join(CACHE[0], 'manifest.csv')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            MANIFEST.update({r['cache_file']: r for r in csv.DictReader(f)})


def write_manifest():
    path = os.path.join(CACHE[0], 'manifest.csv')
    cols = ['cache_file', 'url', 'http_status', 'bytes', 'sha256', 'fetched_utc']
    with open(path + '.tmp', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for k in sorted(MANIFEST):
            w.writerow(MANIFEST[k])
    os.replace(path + '.tmp', path)


def fetch(url, name):
    path = os.path.join(CACHE[0], name)
    if os.path.exists(path):
        if name not in MANIFEST:
            st = os.stat(path)
            MANIFEST[name] = dict(cache_file=name, url=url, http_status='200', bytes=str(st.st_size),
                                  sha256=C.sha256_file(path), fetched_utc=utc(st.st_mtime))
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
            with urllib.request.urlopen(req, timeout=240) as r:
                status, body = r.status, r.read()
            break
        except urllib.error.HTTPError as e:
            status, body = e.code, e.read()
            break
        except Exception as e:  # network hiccup
            print('retry', url, type(e).__name__, file=sys.stderr, flush=True)
            time.sleep(5 * (attempt + 1))
    _last[0] = time.time()
    if status != 200:
        MANIFEST['ERR_' + name] = dict(cache_file='ERR_' + name, url=url, http_status=str(status),
                                       bytes=str(len(body)), sha256='', fetched_utc=utc())
        write_manifest()
        print('HTTP', status, url, file=sys.stderr, flush=True)
        return None
    with open(path, 'wb') as f:
        f.write(body)
    MANIFEST[name] = dict(cache_file=name, url=url, http_status='200', bytes=str(len(body)),
                          sha256=C.sha256_file(path), fetched_utc=utc())
    write_manifest()
    print(f'{utc()} {time.time() - t0:5.1f}s {name}', flush=True)
    return json.loads(body.decode('utf-8'))


def api(endpoint, **params):
    q = '&'.join(f'{k}={v}' for k, v in params.items())
    return fetch(BASE + endpoint + ('?' + q if q else ''), C.cache_name(endpoint, **params))


def phase1():
    maps = api('Service_Eng.aspx/GetMaps')['d']
    grid = fetch(BASE + 'GetIsraelGrid.aspx', 'GetIsraelGrid.json')
    online = {str(m['id']): m for m in maps}
    sel = C.sheets_in_region(grid, online)
    print(len(sel), 'online maps touch the polygon:', ', '.join(n for _, n in sel), flush=True)
    for mid, _ in sel:
        api('Service_Eng.aspx/GetPolygonsSites', MapId=mid, sitesId='null')
        api('Service.aspx/GetPolygonsSites', MapId=mid, sitesId='null')
    return sel


def phase2():
    import build_inventory as B  # noqa: E402  (screen only; reads the cache)
    hits = B.asi_screen(CACHE[0])
    ids = sorted({h['site_id'] for h in hits if h['in_region']}, key=int)
    print(len(ids), 'records to fetch', flush=True)
    for sid in ids:
        api('Service_Eng.aspx/GetSiteDesc2', Id=sid)


def main():
    CACHE[0] = os.path.abspath(sys.argv[1])
    os.makedirs(CACHE[0], exist_ok=True)
    load_manifest()
    if '--records' in sys.argv:
        phase2()
    else:
        phase1()
    write_manifest()


if __name__ == '__main__':
    main()
