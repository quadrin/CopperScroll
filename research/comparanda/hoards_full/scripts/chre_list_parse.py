#!/usr/bin/env python3
"""Parse saved CHRE list pages into one CSV (adapted from T02 scripts/chre_list.py).

Usage: python3 -I chre_list_parse.py <cache_dir> <out.csv>
HTML is untrusted data; it is parsed as text only.
"""
import csv
import glob
import html
import os
import re
import sys

ITEM = re.compile(r'<div class="hoardlistview hoardlistview-6col">(.*?)<hr/>', re.S)


def field(block, label):
    m = re.search(r'<div class="datalabel">' + re.escape(label) + r'\s*</div>\s*<div class="data">(.*?)</div>',
                  block, re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1)))).strip() if m else ""


def main():
    cache, out = sys.argv[1], sys.argv[2]
    rows = {}
    for p in sorted(glob.glob(os.path.join(cache, "list_*.html"))):
        src = os.path.basename(p).split("_p")[0].replace("list_", "")
        t = open(p, encoding="utf-8", errors="replace").read()
        for b in ITEM.findall(t):
            m = re.search(r'<a href="/hoard/(\d+)">(.*?)</a>', b)
            if not m:
                continue
            hid = int(m.group(1))
            if hid in rows:
                rows[hid]["lists"] += ";" + src
                continue
            rows[hid] = {"chre_id": hid, "name": html.unescape(m.group(2)).strip(),
                         "date_found": field(b, "Date:"), "size": field(b, "Size:"),
                         "terminal_year": field(b, "Terminal Year:"), "country": field(b, "Country:"),
                         "summary": field(b, "Summary:"), "lists": src,
                         "url": f"https://chre.ashmus.ox.ac.uk/hoard/{hid}"}
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(next(iter(rows.values())).keys()), lineterminator="\n")
        w.writeheader()
        for k in sorted(rows):
            w.writerow(rows[k])
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
