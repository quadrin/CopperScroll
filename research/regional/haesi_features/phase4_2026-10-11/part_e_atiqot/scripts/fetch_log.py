#!/usr/bin/env python3
"""Merge the shell fetch logs (scratch folder) into data/fetch_log.csv: UTC time, URL, HTTP status, bytes.

  python3 -I fetch_log.py VOL_LOG LANDING_LOG
"""
import csv
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "fetch_log.csv"
BASE = "https://publications.iaa.org.il/atiqot/"


def main(vol_log, land_log):
    out = [
        {"utc": "2026-10-12T00:39Z (not logged)", "url": "https://publications.iaa.org.il/robots.txt", "http": "200", "bytes": "",
         "note": "robots.txt: volume pages, landing pages and images.kml are not disallowed for user agent *"},
        {"utc": "2026-10-12T00:40Z (not logged)", "url": BASE + "vol42/iss1/", "http": "200", "bytes": "59004",
         "note": "fetched twice, 3 s apart: first with user agent 'Mozilla/5.0', then with curl's default agent; the second copy was used; every later request used curl's default agent"},
    ]
    for line in open(vol_log, encoding="utf-8"):
        p = line.split()
        if not p or p[0] == "DONE":
            continue
        out.append({"utc": p[1], "url": p[3], "http": p[2], "bytes": p[4], "note": "volume page"})
    for line in open(land_log, encoding="utf-8"):
        p = line.split()
        if not p or p[0] == "DONE":
            continue
        if p[0] == "images.kml":
            out.append({"utc": p[1], "url": BASE + "images.kml", "http": "200", "bytes": "298997",
                        "note": "portal location map (KML); placemarks of vol. 41 dropped unread by script"})
            continue
        v, i = p[0].split("/")
        out.append({"utc": p[1], "url": BASE + "vol%s/iss1/%s" % (v, i), "http": p[2] if len(p) > 2 else "200",
                    "bytes": p[3] if len(p) > 3 else "", "note": "landing page"})
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["utc", "url", "http", "bytes", "note"], lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(len(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
