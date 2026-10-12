#!/usr/bin/env python3
"""Parse the saved ʿAtiqot volume pages (publications.iaa.org.il/atiqot/vol<N>/iss1/) into one row per article.

Input: a directory of saved volume pages vol<N>.html (untrusted downloads, kept outside the repository).
Output: CSV (stdout or --out) with volume, year, item number, title, authors, landing URL, PDF URL, PDF size.
Standard library only. Run with python3 -I.

  python3 -I parse_volumes.py <vol_dir> [--out FILE]
"""
import csv
import html
import re
import sys
from pathlib import Path

DOC = re.compile(r'<div class="doc">(.*?)</div>', re.S)
PDF = re.compile(r'<p class="pdf"><a href="([^"]+)"[^>]*title="Download PDF of (.*?)"', re.S)
LAND = re.compile(r'<p><a href="(https://publications\.iaa\.org\.il/atiqot/vol(\d+)/iss1/(\d+))"\s*>(.*?)</a>(.*?)</p>', re.S)
AUTH = re.compile(r'<span class="auth">(.*?)</span>', re.S)
H1 = re.compile(r'<h1>\s*Volume\s+(\d+)\s*\((\d{4})\)', re.S)
SIZE = re.compile(r'\(([\d.,]+\s*(?:KB|MB|GB))\)\s*$')
FIELDS = ["volume", "year", "item_no", "title", "authors", "landing_url", "pdf_url", "pdf_size"]


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).replace("\xa0", " ")
    return " ".join(s.split())


def parse(path):
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    m = H1.search(t)
    vol, year = (m.group(1), clean(m.group(2))) if m else ("", "")
    out = []
    for block in DOC.findall(t):
        lm = LAND.search(block)
        if not lm:
            continue
        pm = PDF.search(block)
        am = AUTH.search(lm.group(5)) or AUTH.search(block)
        size = ""
        if pm:
            sm = SIZE.search(clean(pm.group(2)))
            size = sm.group(1) if sm else ""
        out.append({
            "volume": lm.group(2), "year": year, "item_no": lm.group(3),
            "title": clean(lm.group(4)), "authors": clean(am.group(1)) if am else "",
            "landing_url": lm.group(1), "pdf_url": html.unescape(pm.group(1)) if pm else "",
            "pdf_size": size,
        })
        if vol and lm.group(2) != vol:
            raise SystemExit("volume mismatch in %s" % path)
    return out


def main(argv):
    d = Path(argv[1])
    rows = []
    for p in sorted(d.glob("vol*.html"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0)):
        rows.extend(parse(p))
    fo = open(argv[argv.index("--out") + 1], "w", newline="", encoding="utf-8") if "--out" in argv else sys.stdout
    w = csv.DictWriter(fo, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return rows


if __name__ == "__main__":
    main(sys.argv)
