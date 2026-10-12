#!/usr/bin/env python3
"""List the landing pages to fetch: gazetteer title candidates (not dropped by title) plus manual adds/checks.

Duplicate portal listings of one article (same unit id) are fetched once, for the first listing.
  python3 -I landing_list.py OUTFILE
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import screen_lib as L  # noqa: E402

DATA = L.PART / "data"


def candidates():
    pats = L.patterns()
    man = {(r["volume"], r["item_no"]): r for r in csv.DictReader(open(DATA / "screen_manual.csv", encoding="utf-8"))}
    seen, out = set(), []
    for x in csv.DictReader(open(DATA / "atiqot_articles.csv", encoding="utf-8")):
        t, note, fp, lp, lang = L.split_title(x["title"])
        uid = L.unit_id(x["volume"], fp, x["item_no"], t)
        if uid in seen:
            continue
        seen.add(uid)
        m = man.get((x["volume"], x["item_no"]))
        if m and m["action"] == "drop_title":
            continue
        if L.hits(x["title"], pats) or m:
            out.append(x)
    return out


if __name__ == "__main__":
    rows = candidates()
    Path(sys.argv[1]).write_text("".join(r["landing_url"] + "\n" for r in rows), encoding="utf-8")
    print(len(rows))
