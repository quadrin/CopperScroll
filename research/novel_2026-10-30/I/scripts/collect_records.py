#!/usr/bin/env python3
"""Collect blind-extractor JSON outputs into data/medieval_records.csv and assign the date of writing.
Usage: python3 -I collect_records.py EXTRACT_DIR SELECTION_MANIFEST OUT_CSV
Layer rule (frozen with the protocol): primary layer = by_editor false AND year of writing in 1100-1600.
Year of writing: speaker_date (first 3-4 digit number, or 'NNth c.' -> century midpoint) when given, else the
segment date (first 4-digit number of date_of_writing; 'NNth' -> midpoint). Le Strange records need a speaker_date.
"""
import sys, os, json, csv, re, glob
EX, MAN, OUT = sys.argv[1:4]
man = {m["seg"]: m for m in json.load(open(MAN))}
def year_of(s):
    s = str(s or "")
    m = re.search(r"\b(1[0-9]{3}|[5-9][0-9]{2})\b", s)
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d{1,2})(?:st|nd|rd|th)\b", s)
    if m:
        return (int(m.group(1)) - 1) * 100 + 50
    return None
rows = []
for f in sorted(glob.glob(os.path.join(EX, "*.json"))):
    chunk = os.path.basename(f)[:-5]
    d = json.load(open(f))
    k = 0
    for l in d.get("result", "").split("\n"):
        l = l.strip()
        if not l.startswith("{"):
            continue
        r = json.loads(l)
        k += 1
        seg = chunk.split("__")[0]
        m = man[seg]
        sd = str(r.get("speaker_date", "") or "")
        y = year_of(sd) if sd.strip() else (None if seg == "lestrange" else year_of(m["date_of_writing"]))
        be = r.get("by_editor")
        be = (be is True) or str(be).lower() == "true"
        prim = (not be) and (y is not None) and (1100 <= y <= 1600)
        if seg == "anon_pilgrims":
            # translator: Pilgrim I "part early, part 11th century" (source lines 60-236); II-VIII 12th century
            try:
                a0 = int(str(r.get("lines", "")).split("-")[0])
            except ValueError:
                a0 = 0
            prim = (not be) and a0 >= 237
        pp = " ".join(str(r.get("position_phrase", "")).split()[:15])
        rows.append(dict(rec_id=f"{chunk}-{k:03d}", seg=seg, chunk=chunk, source_file=m["file"], text=m["text"],
                         lines=r.get("lines", ""), page=r.get("page", ""), name_as_printed=r.get("name_as_printed", ""),
                         name_language=r.get("name_language", ""), other_names=r.get("other_names", ""),
                         feature_type=r.get("feature_type", ""), feature_text=r.get("feature_text", ""),
                         region=r.get("region", ""), anchor_place=r.get("anchor_place", ""), direction=r.get("direction", ""),
                         distance=r.get("distance", ""), position_phrase=pp, by_editor=be, speaker_date=sd,
                         year_used=y if y is not None else "", primary_layer=prim))
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "records;", sum(r["primary_layer"] for r in rows), "in primary layer")
