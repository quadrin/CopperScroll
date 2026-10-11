#!/usr/bin/env python3
"""Fetch the ASI map list, sheet grid and the site GeoJSON of every online sheet that intersects the box (PLAN.md S9).

Run: python3 -I fetch_asi_box.py CACHE_DIR
Method of research/regional/asi_jerusalem/access.md: public JSON services of survey.iaa.org.il, header
Content-Type: application/json, at most one request per 1.2 s, each response cached once (by name) in CACHE_DIR,
which stays outside the repository. CACHE_DIR/manifest.csv records URL, status, bytes, SHA-256 and fetch time.
"""
import csv
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.request

BASE = "https://survey.iaa.org.il/aspxService/"
GAP = 1.2
_last = [0.0]


def utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(cache, url, name, manifest):
    path = os.path.join(cache, name)
    if not os.path.exists(path):
        wait = GAP - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"Content-Type": "application/json",
                                                   "User-Agent": "copper-scroll-research (read-only; 1 req/s)"})
        with urllib.request.urlopen(req, timeout=180) as r:
            body, status = r.read(), r.status
        _last[0] = time.time()
        with open(path, "wb") as f:
            f.write(body)
        manifest.append(dict(cache_file=name, url=url, http_status=status, bytes=len(body),
                             sha256=hashlib.sha256(body).hexdigest(), fetched_utc=utc()))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(cache):
    os.makedirs(cache, exist_ok=True)
    manifest = []
    maps = fetch(cache, BASE + "Service_Eng.aspx/GetMaps", "maps_eng.json", manifest)
    grid = fetch(cache, BASE + "GetIsraelGrid.aspx", "israel_grid.json", manifest)
    json.dump({"maps": maps, "grid": grid}, open(os.path.join(cache, "_peek.json"), "w"))
    mpath = os.path.join(cache, "manifest.csv")
    old = list(csv.DictReader(open(mpath))) if os.path.exists(mpath) else []
    with open(mpath, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["cache_file", "url", "http_status", "bytes", "sha256", "fetched_utc"])
        w.writeheader()
        w.writerows(old + manifest)


def fetch_maps(cache, ids):
    manifest = []
    for mid in ids:
        fetch(cache, BASE + f"Service_Eng.aspx/GetPolygonsSites?MapId={mid}&sitesId=null", f"sites_eng_{mid}.json", manifest)
        fetch(cache, BASE + f"Service.aspx/GetPolygonsSites?MapId={mid}&sitesId=null", f"sites_heb_{mid}.json", manifest)
    mpath = os.path.join(cache, "manifest.csv")
    old = list(csv.DictReader(open(mpath))) if os.path.exists(mpath) else []
    with open(mpath, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["cache_file", "url", "http_status", "bytes", "sha256", "fetched_utc"])
        w.writeheader()
        w.writerows(old + manifest)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        fetch_maps(sys.argv[1], [int(x) for x in sys.argv[2:]])
    else:
        main(sys.argv[1])
