#!/usr/bin/env python3
"""Parse CHRE search-result list pages (saved HTML) into CSV rows.
Usage: python3 -I chre_list.py <out.csv> <page1.html> [page2.html ...]
HTML files are untrusted; parsed as text only."""
import csv
import html
import re
import sys

ITEM = re.compile(r'<div class="hoardlistview hoardlistview-6col">(.*?)<hr/>', re.S)


def field(block, label):
    m = re.search(r'<div class="datalabel">' + re.escape(label) + r'\s*</div>\s*<div class="data">(.*?)</div>', block, re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1)))).strip() if m else ""


def main():
    out = sys.argv[1]
    rows, seen = [], set()
    for p in sys.argv[2:]:
        t = open(p, encoding="utf-8", errors="replace").read()
        for b in ITEM.findall(t):
            m = re.search(r'<a href="/hoard/(\d+)">(.*?)</a>', b)
            if not m:
                continue
            hid = int(m.group(1))
            if hid in seen:
                continue
            seen.add(hid)
            rows.append({
                "chre_id": hid,
                "name": html.unescape(m.group(2)).strip(),
                "date_found": field(b, "Date:"),
                "size": field(b, "Size:"),
                "terminal_year": field(b, "Terminal Year:"),
                "country": field(b, "Country:"),
                "summary": field(b, "Summary:"),
                "url": f"https://chre.ashmus.ox.ac.uk/hoard/{hid}",
            })
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
