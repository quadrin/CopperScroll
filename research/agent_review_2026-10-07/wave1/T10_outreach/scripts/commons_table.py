"""Tabulate Commons imageinfo (licence, author, size, date) for the Copper Scroll images.
Usage: python3 -I commons_table.py OUT_CSV imageinfo.json [imageinfo2.json ...]
"""
import sys, json, csv, re
rows = []
for f in sys.argv[2:]:
    d = json.load(open(f))
    for p in d["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        if not ii.get("url"):
            continue
        em = ii.get("extmetadata", {})
        g = lambda k: re.sub(r"<[^>]+>", "", (em.get(k, {}) or {}).get("value", "")).strip()
        rows.append({"title": p["title"], "width": ii.get("width"), "height": ii.get("height"),
                     "bytes": ii.get("size"), "licence": g("LicenseShortName"), "artist": g("Artist"),
                     "date": g("DateTimeOriginal")[:19], "sha1": ii.get("sha1"),
                     "url": ii["url"].split("?")[0],
                     "page": "https://commons.wikimedia.org/wiki/" + p["title"].replace(" ", "_"),
                     "description": g("ImageDescription")[:200]})
with open(sys.argv[1], "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r["title"][:60], r["width"], r["height"], r["licence"], r["artist"][:40])
