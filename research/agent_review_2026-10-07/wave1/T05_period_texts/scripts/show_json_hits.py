#!/usr/bin/env python3
"""Print Sefaria search hits from a folder of raw JSON files (untrusted data,
parsed as JSON only). Shows ancient-corpus Hebrew hits by default; pass --all
to show everything.

Usage: python3 -I scripts/show_json_hits.py <folder> [--all]
"""
import glob
import json
import os
import re
import sys

folder = sys.argv[1]
show_all = "--all" in sys.argv
ANCIENT = ("Tanakh/", "Mishnah/", "Tosefta/", "Talmud/Bavli/", "Talmud/Yerushalmi/",
           "Midrash/", "Targum/", "Second Temple/")
EXCL = ("Commentary", "Rishonim", "Acharonim", "Modern")
for fn in sorted(glob.glob(os.path.join(folder, "*.json"))):
    try:
        d = json.load(open(fn, encoding="utf-8"))
    except Exception:
        print("##", os.path.basename(fn), "BAD JSON")
        continue
    hits = d.get("hits", {}).get("hits", [])
    print(f"\n## {os.path.basename(fn)[:-5]}  total={d.get('hits', {}).get('total')}")
    for h in hits:
        s = h["_source"]
        p = s.get("path", "")
        if not show_all and (not p.startswith(ANCIENT) or any(x in p for x in EXCL)):
            continue
        hl = " … ".join(h.get("highlight", {}).get("exact", [s.get("exact", "")]))
        hl = re.sub(r"\s+", " ", re.sub(r"</?b>", "**", hl))[:300]
        print(f"- {s.get('ref')} [{s.get('lang')}|{p.split('/')[0]}]: {hl}")
