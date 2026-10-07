#!/usr/bin/env python3
"""Filter Sefaria hits to ancient corpora (Tanakh, Targum, Mishnah, Tosefta,
Talmuds, tannaitic/amoraic midrash) and print them grouped by query.

Usage: python3 -I scripts/filter_ancient.py <outdir> [term_id ...]
"""
import csv
import os
import re
import sys

OUT = sys.argv[1]
want = set(sys.argv[2:])
ANCIENT = (
    "Tanakh/", "Mishnah/", "Tosefta/", "Talmud/Bavli/", "Talmud/Yerushalmi/",
    "Midrash/Halakhic Midrash/", "Midrash/Aggadah/Midrash Rabbah/",
    "Targum/", "Midrash/Aggadah/Pesikta", "Midrash/Aggadah/Tanchuma",
    "Second Temple/", "Midrash/Aggadah/Seder Olam",
    "Midrash/Aggadah/Avot DeRabbi Natan", "Talmud/Bavli/Minor Tractates",
)
EXCLUDE = ("Commentary", "Rishonim", "Acharonim", "Modern", "Quoting")

rows = []
with open(os.path.join(OUT, "data", "sefaria_hits_raw.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        p = r["path"]
        if not p.startswith(ANCIENT):
            continue
        if any(x in p for x in EXCLUDE):
            continue
        if r["lang"] != "he":
            continue
        if want and r["term_id"] not in want:
            continue
        rows.append(r)

with open(os.path.join(OUT, "data", "sefaria_hits_ancient.csv"), "w",
          newline="", encoding="utf-8") as f:
    if rows:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

cur = None
for r in rows:
    k = (r["term_id"], r["query"])
    if k != cur:
        cur = k
        print(f"\n### {r['term_id']}  {r['query']}  (total reported {r['total_hits_reported']})")
    snip = re.sub(r"</?b>", "**", r["snippet"])[:260]
    print(f"- {r['ref']} [{r['path'].split('/')[0]}]: {snip}")
