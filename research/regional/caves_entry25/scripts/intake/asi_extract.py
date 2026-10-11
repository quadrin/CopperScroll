#!/usr/bin/env python3
"""Flatten the cached ASI GeoJSON (fetch_asi_box.py) into one JSON list of site records with plain text.

Run: python3 -I asi_extract.py CACHE_DIR OUT_JSON
Each record: map number, map id, site id, site number, name, WGS84 point, kind of site, plain-text description,
finds and bibliography, and a cave-word flag (PLAN.md 4.1: cave / caves / grotto / cavern / מערה / מערות / מערת).
"""
import html
import json
import os
import re
import sys

MAPS = {78: "109/5 Kalia", 33: "147 'Ein Gedi", 68: "109/4 Wadi Qelt", 73: "83/12 Wadi el-Makokh", 62: "109/7 Deir Mar Saba"}
CAVE = re.compile(r"\bcaves?\b|\bgrott|\bcavern|מער", re.I)


def plain(s):
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>|</p>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"[ \t]+", " ", html.unescape(s)).strip()


def main(cache, out):
    recs = []
    for mid, mname in MAPS.items():
        for lang in ("eng", "heb"):
            d = json.load(open(os.path.join(cache, f"sites_{lang}_{mid}.json"), encoding="utf-8"))["d"]
            for f in d["features"]:
                p = {kv["key"]: kv["value"] for kv in f["properties"]}
                lon, lat = f["geometry"]["coordinates"][:2]
                desc = plain(p.get("description_heb"))
                m = re.search(r"Kind of site:\s*([^|\n]+)", desc) or re.search(r"סוג האתר:\s*([^|\n]+)", desc)
                recs.append(dict(lang=lang, map=mname, map_id=mid, site_id=p.get("id"), site_num=p.get("site_num"),
                                 name=plain(p.get("name_heb")), lon=lon, lat=lat, kind=(m.group(1).strip() if m else ""),
                                 description=desc, finds=plain(p.get("finding_heb")), bibliography=plain(p.get("bibliography_heb"))))
    for r in recs:
        r["cave_word"] = bool(CAVE.search(" ".join([r["name"], r["kind"], r["description"]])))
    json.dump(recs, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(recs), sum(r["cave_word"] for r in recs if r["lang"] == "eng"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
