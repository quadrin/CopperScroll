#!/usr/bin/env python3
"""Fetch a list of URLs into a cache folder, one request per 1.5 s, skipping cached files.

Usage: python3 -I fetch_cached.py <cache_dir> <url_list_file>

Only for hosts whose robots.txt allows the paths (checked by hand and recorded in README.md).
Saved files are untrusted data and are never committed. Each fetch is logged with its SHA-256
in <cache_dir>/fetch_log.csv.
"""
import csv
import hashlib
import os
import re
import subprocess
import sys
import time


def fname(url):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", url.split("://", 1)[-1]).strip("_")[:180] + ".html"


def main():
    cache, lst = sys.argv[1], sys.argv[2]
    os.makedirs(cache, exist_ok=True)
    log = os.path.join(cache, "fetch_log.csv")
    urls = [u.strip() for u in open(lst) if u.strip() and not u.startswith("#")]
    for url in urls:
        path = os.path.join(cache, fname(url))
        if os.path.exists(path) and os.path.getsize(path) > 0:
            continue
        r = subprocess.run(["curl", "-sS", "-m", "120", "-L", "-g", "-A",
                            "Mozilla/5.0 (research; copper-scroll hoards lane)", url, "-o", path],
                           capture_output=True)
        time.sleep(1.5)
        if r.returncode != 0 or not os.path.exists(path):
            print("FAIL", url, r.stderr.decode()[:200])
            continue
        b = open(path, "rb").read()
        new = not os.path.exists(log)
        with open(log, "a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["url", "file", "bytes", "sha256", "fetched_utc"])
            w.writerow([url, os.path.basename(path), len(b), hashlib.sha256(b).hexdigest(),
                        time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())])
        print(len(b), url)


if __name__ == "__main__":
    main()
