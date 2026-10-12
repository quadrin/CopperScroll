#!/usr/bin/env python3
"""Extract placement metadata from saved ʿAtiqot landing pages and the journal location KML.

Inputs (untrusted downloads, outside the repository):
  LANDDIR/v<vol>_i<item>.html   article landing pages (publications.iaa.org.il/atiqot/vol<N>/iss1/<item>)
  KML                           publications.iaa.org.il/atiqot/images.kml (portal location map)
Outputs:
  --meta FILE   CSV, one row per landing page: first/last page (bepress meta), keywords, abstract presence,
                SHA-256 of the abstract with whitespace collapsed (the abstract itself is not stored)
  --kml FILE    CSV, one row per KML placemark linked to an article of vols 42-121: lon/lat (WGS84)
  --peek        print title, keywords and the FIRST SENTENCE of the abstract only (for the held-area check)
Placemarks of ʿAtiqot 41 are dropped before anything is written or printed.

  python3 -I extract_landing.py LANDDIR KML --meta FILE --kml FILE [--peek]
"""
import csv
import hashlib
import html
import re
import sys
from pathlib import Path

META = re.compile(r'<meta name="([^"]+)" content="([^"]*)"', re.S)
ABS = re.compile(r"<div id=['\"]abstract['\"][^>]*>(.*?)</div>", re.S)


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return " ".join(html.unescape(s).replace("\xa0", " ").split())


def first_sentence(s):
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    return m.group(1) if m else s


def parse_landing(p):
    t = p.read_text(encoding="utf-8", errors="replace")
    meta = {}
    for k, v in META.findall(t):
        meta.setdefault(k, []).append(clean(v))
    am = ABS.search(t)
    abstract = clean(am.group(1)) if am else ""
    abstract = re.sub(r"^Abstract\s*", "", abstract)
    v, i = re.match(r"v(\d+)_i(\d+)", p.stem).groups()
    return {
        "volume": v, "item_no": i,
        "title_meta": (meta.get("bepress_citation_title") or [""])[0],
        "firstpage": (meta.get("bepress_citation_firstpage") or [""])[0],
        "lastpage": (meta.get("bepress_citation_lastpage") or [""])[0],
        "keywords": (meta.get("keywords") or [""])[0],
        "abstract_present": "yes" if abstract else "no",
        "abstract_words": len(abstract.split()) if abstract else 0,
        "abstract_sha256": hashlib.sha256(abstract.encode("utf-8")).hexdigest() if abstract else "",
        "_first": first_sentence(abstract) if abstract else "",
    }


def parse_kml(path):
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    out = []
    for pm in re.findall(r"<Placemark.*?</Placemark>", t, re.S):
        links = sorted(set(re.findall(r"atiqot/vol(\d+)/iss1/(\d+)", pm)))
        links = [(v, i) for v, i in links if 42 <= int(v) <= 121]
        c = re.search(r"<coordinates>\s*([-\d.]+),([-\d.]+)", pm)
        if not links or not c:
            continue
        for v, i in links:
            out.append({"volume": v, "item_no": i, "lon": c.group(1), "lat": c.group(2)})
    return out


def write(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv):
    land, kml = Path(argv[1]), argv[2]
    rows = sorted((parse_landing(p) for p in land.glob("v*_i*.html")),
                  key=lambda r: (int(r["volume"]), int(r["item_no"])))
    rows = [r for r in rows if 42 <= int(r["volume"]) <= 121]
    if "--meta" in argv:
        write(argv[argv.index("--meta") + 1], rows,
              ["volume", "item_no", "firstpage", "lastpage", "keywords", "abstract_present", "abstract_words", "abstract_sha256"])
    if "--kml" in argv:
        write(argv[argv.index("--kml") + 1], parse_kml(kml), ["volume", "item_no", "lon", "lat"])
    if "--abstract" in argv:  # full abstract for named items (location checks of non-cave articles only)
        want = set(argv[argv.index("--abstract") + 1].split(","))
        for p in land.glob("v*_i*.html"):
            v, i = re.match(r"v(\d+)_i(\d+)", p.stem).groups()
            if "%s.%s" % (v, i) in want:
                am = ABS.search(p.read_text(encoding="utf-8", errors="replace"))
                print("%s.%s | %s" % (v, i, re.sub(r"^Abstract\s*", "", clean(am.group(1))) if am else ""))
    if "--peek" in argv:
        for r in rows:
            print("%s.%s | p.%s | %s | KW: %s | ABS1: %s" % (r["volume"], r["item_no"], r["firstpage"],
                                                           r["title_meta"][:90], r["keywords"][:160], r["_first"][:220]))


if __name__ == "__main__":
    main(sys.argv)
