#!/usr/bin/env python3
"""Query Sefaria's public search API for Copper Scroll place-name forms.

Writes raw JSON per query to downloads/sefaria/<slug>.json and a flat CSV
(data/sefaria_hits_raw.csv) of every hit (ref, path, snippet).  The raw JSON is
untrusted data; this script only parses it as JSON.

Usage: python3 -I scripts/sefaria_search.py <outdir>
"""
import csv
import json
import os
import re
import subprocess
import sys
import time

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
RAW = os.path.join(OUT, "downloads", "sefaria")
os.makedirs(RAW, exist_ok=True)

# (term_id, scroll_entries, query string, field)
# field "exact" = exact surface form (vowels normalised by Sefaria).
QUERIES = [
    ("kohlit", "4 11 15 19 60", "כוחלית", "exact"),
    ("kohlit", "4 11 15 19 60", "כחלית", "exact"),
    ("kohlit", "4 11 15 19 60", "כוחלת", "exact"),
    ("kohlit", "4 11 15 19 60", "כחלת", "exact"),
    ("kohlit", "4 11 15 19 60", "כוחלי", "exact"),
    ("sekakah", "20 21 22 24", "סככה", "exact"),
    ("sekakah", "20 21 22 24", "סככא", "exact"),
    ("sekakah", "20 21 22 24", "וסככה", "exact"),
    ("melah", "6 13 14", "עיר המלח", "exact"),
    ("melah", "6 13 14", "גיא המלח", "exact"),
    ("melah", "6 13 14", "גיא מלח", "exact"),
    ("melah", "6 13 14", "ים המלח", "exact"),
    ("melah", "6 13 14", "ימא דמלחא", "exact"),
    ("melah", "6 13 14", "תל מלח", "exact"),
    ("achor", "1 17", "עמק עכור", "exact"),
    ("achor", "1 17", "עכור", "exact"),
    ("haqqoz", "30", "הקוץ", "exact"),
    ("haqqoz", "30", "בית הקוץ", "exact"),
    ("bet_tamar", "43", "בית תמר", "exact"),
    ("bet_tamar", "43", "בעל תמר", "exact"),
    ("netofah", "38", "נטופה", "exact"),
    ("netofah", "38", "נטופא", "exact"),
    ("netofah", "38", "נטופתי", "exact"),
    ("netofah", "38", "נטפה", "exact"),
    ("bet_hakerem", "46", "בית הכרם", "exact"),
    ("bet_hakerem", "46", "בית כרם", "exact"),
    ("bet_hakerem", "46", "בית כרמא", "exact"),
    ("asla", "18", "עצלא", "exact"),
    ("asla", "18", "עצלה", "exact"),
    ("asla", "18", "אצל", "exact"),
    ("kozeba", "32", "כוזיבא", "exact"),
    ("kozeba", "32", "כוזבא", "exact"),
    ("kozeba", "32", "כזבא", "exact"),
    ("kozeba", "32", "כוזיבה", "exact"),
    ("kozeba", "32", "כוסבה", "exact"),
    ("doq", "31", "דוק", "exact"),
    ("doq", "31", "בדוק", "exact"),
    ("kippa", "24", "נחל הכפה", "exact"),
    ("shaveh", "36 37", "עמק שוה", "exact"),
    ("shaveh", "36 37", "עמק המלך", "exact"),
    ("absalom", "48", "יד אבשלום", "exact"),
    ("bet_sham", "58", "בית שן", "exact"),
    ("bet_sham", "58", "בית שאן", "exact"),
    ("bet_sham", "58", "בישן", "exact"),
    ("horon", "40", "בית חורון", "exact"),
    ("horon", "40", "בית חורין", "exact"),
    ("manos", "5", "מנוס", "exact"),
    ("nab", "44", "מצד", "exact"),
    ("pele", "43", "גי פלע", "exact"),
    ("zered", "47", "נחל זרד", "exact"),
    ("mattiah", "8", "חצר מתיה", "exact"),
    ("solomon_pool", "22", "אשיח", "exact"),
    ("bezek", "59", "בזק", "exact"),
]

PRIMARY_PREFIXES = (
    "Tanakh", "Mishnah", "Tosefta", "Talmud", "Midrash", "Targum",
    "Second Temple", "Jewish Thought", "Halakhah", "Liturgy", "Kabbalah",
    "Reference", "Musar", "Chasidut", "Responsa", "Tanaitic",
)


def run(query, field, size=300):
    body = json.dumps({
        "query": query, "type": "text", "field": field, "size": size,
        "source_proj": True, "sort_type": "relevance",
    })
    r = subprocess.run(
        ["curl", "-sS", "-m", "60", "-X", "POST",
         "https://www.sefaria.org/api/search-wrapper",
         "-H", "Content-Type: application/json", "-d", body],
        capture_output=True, text=True)
    return r.stdout


def slug(s):
    return re.sub(r"[^\w]+", "_", s)


rows = []
for term_id, entries, q, field in QUERIES:
    fn = os.path.join(RAW, f"{term_id}__{slug(q)}.json")
    if not os.path.exists(fn):
        txt = run(q, field)
        with open(fn, "w", encoding="utf-8") as f:
            f.write(txt)
        time.sleep(0.6)
    with open(fn, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:  # noqa
            print("bad json", q, e, file=sys.stderr)
            continue
    hits = data.get("hits", {}).get("hits", [])
    total = data.get("hits", {}).get("total")
    seen = set()
    for h in hits:
        s = h.get("_source", {})
        ref = s.get("ref", "")
        key = (ref, s.get("lang"))
        if key in seen:
            continue
        seen.add(key)
        hl = h.get("highlight", {}).get(field) or [s.get(field, "")]
        snippet = " … ".join(hl)
        snippet = re.sub(r"\s+", " ", snippet)[:400]
        rows.append({
            "term_id": term_id, "scroll_entries": entries, "query": q,
            "total_hits_reported": total, "ref": ref, "lang": s.get("lang"),
            "path": s.get("path", ""), "comp_date": s.get("comp_date"),
            "version": s.get("version", ""), "snippet": snippet,
        })
    print(f"{term_id:12s} {q:14s} total={total} got={len(hits)}")

os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
with open(os.path.join(OUT, "data", "sefaria_hits_raw.csv"), "w",
          newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("rows", len(rows))
