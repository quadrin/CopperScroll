#!/usr/bin/env python3
"""Fetch CHRE list pages and hoard detail pages into a cache folder (never committed).

Usage:
  python3 -I chre_fetch.py lists <cache_dir>
  python3 -I chre_fetch.py details <cache_dir> <id> [<id> ...]

One request per 1.5 s. Saved HTML is untrusted data; this script only writes bytes to disk.
Every saved file is listed with its URL, size and SHA-256 in <cache_dir>/fetch_log.csv.
"""
import csv
import hashlib
import os
import subprocess
import sys
import time

BASE = "https://chre.ashmus.ox.ac.uk"
Y0, Y1 = -260, 150
LISTS = [("country", "22"), ("country", "103"), ("country", "24"), ("country", "47"),
         ("province", "44"), ("province", "54"), ("province", "31")]


def list_url(kind, val, page):
    key = "ox_hs[hoardCountries][]" if kind == "country" else "ox_hs[hoardProvince]"
    return (f"{BASE}/search/?{key}={val}&ox_hs[hoardTerminalYearRangeStart]={Y0}"
            f"&ox_hs[hoardTerminalYearRangeEnd]={Y1}&page={page}")


def fetch(url, path, log):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return open(path, "rb").read()
    r = subprocess.run(["curl", "-sS", "-m", "120", "-L", "-g", url, "-o", path], capture_output=True)
    time.sleep(1.5)
    if r.returncode != 0 or not os.path.exists(path):
        print("FAIL", url, r.stderr.decode()[:200])
        return b""
    b = open(path, "rb").read()
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["url", "file", "bytes", "sha256", "fetched_utc"])
        w.writerow([url, os.path.basename(path), len(b), hashlib.sha256(b).hexdigest(),
                    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())])
    return b


def main():
    cmd, cache = sys.argv[1], sys.argv[2]
    os.makedirs(cache, exist_ok=True)
    log = os.path.join(cache, "fetch_log.csv")
    if cmd == "lists":
        for kind, val in LISTS:
            page = 1
            while page <= 20:
                path = os.path.join(cache, f"list_{kind}{val}_p{page}.html")
                b = fetch(list_url(kind, val, page), path, log)
                n = b.count(b'class="hoardlistview')
                print(kind, val, page, len(b), n)
                if n == 0 or (b"page=%d" % (page + 1)) not in b:
                    break
                page += 1
    elif cmd == "details":
        for hid in sys.argv[3:]:
            path = os.path.join(cache, f"h{int(hid)}.html")
            b = fetch(f"{BASE}/hoard/{int(hid)}", path, log)
            print(hid, len(b))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
