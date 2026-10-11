#!/usr/bin/env python3
"""Fetch the English GeoJSON of the ASI maps named in PLAN.md §3 into a cache outside the repo.

Run:  python3 -I scripts/fetch_asi.py CACHE_DIR
One request per 1.2 s, header Content-Type: application/json (as the site's own page sends).
CACHE_DIR/manifest.csv lists URL, HTTP status, size, SHA-256 and UTC fetch time of each response.
"""
import csv
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = 'https://survey.iaa.org.il/aspxService/'
MAP_NUMS = ['101', '102', '105', '106', '83/1', '83/2', '83/12', '108/2', '109/4', '109/5', '109/7']
GAP = 1.2


def utc():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def get(url, path, manifest, last):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            body = f.read()
        manifest.setdefault(os.path.basename(path), dict(file=os.path.basename(path), url=url, http_status='200',
                                                         bytes=str(len(body)), sha256=sha(body), fetched_utc=''))
        return json.loads(body.decode('utf-8'))
    wait = GAP - (time.time() - last[0])
    if wait > 0:
        time.sleep(wait)
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
        except Exception as e:  # network hiccup
            print('retry', url, type(e).__name__, file=sys.stderr, flush=True)
            time.sleep(5 * (attempt + 1))
    last[0] = time.time()
    manifest[os.path.basename(path)] = dict(file=os.path.basename(path), url=url, http_status=str(status),
                                            bytes=str(len(body)), sha256=sha(body) if status == 200 else '',
                                            fetched_utc=utc())
    if status != 200:
        print('HTTP', status, url, file=sys.stderr, flush=True)
        return None
    with open(path, 'wb') as f:
        f.write(body)
    print(utc(), os.path.basename(path), len(body), flush=True)
    return json.loads(body.decode('utf-8'))


def main(cache):
    os.makedirs(cache, exist_ok=True)
    manifest, last = {}, [0.0]
    maps = get(BASE + 'Service_Eng.aspx/GetMaps', os.path.join(cache, 'Service_Eng_GetMaps.json'), manifest, last)['d']
    if isinstance(maps, str):
        maps = json.loads(maps)
    by_num = {str(m['map_num']).strip(): m for m in maps}
    for num in MAP_NUMS:
        m = by_num[num]
        mid = m['id']
        get(f'{BASE}Service_Eng.aspx/GetPolygonsSites?MapId={mid}&sitesId=null',
            os.path.join(cache, f'GetPolygonsSites_en_map{mid}.json'), manifest, last)
    with open(os.path.join(cache, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['file', 'url', 'http_status', 'bytes', 'sha256', 'fetched_utc'],
                           lineterminator='\n')
        w.writeheader()
        for k in sorted(manifest):
            w.writerow(manifest[k])


if __name__ == '__main__':
    main(sys.argv[1])
