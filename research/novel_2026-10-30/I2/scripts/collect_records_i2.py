#!/usr/bin/env python3
"""Lane I2: collect blind-extractor outputs (Kaftor, Khitrowo, Huetteroth ch. I-V) and the parsed Huetteroth
fiscal-unit gazetteer into one record table.
Usage: python3 -I collect_records_i2.py EXTRACT_DIR SELECTION_MANIFEST HUTT_GAZ_CSV OUT_CSV
Layer rule: lane I rule unchanged (collect_records.py): primary layer = by_editor false AND year of writing 1100-1600
(speaker_date when given, else the segment date).
Gazetteer rows (parse_hutteroth.py output): one record per fiscal unit with a Palestine-grid position inside the
lane I2 region boxes (place_records_i2.py REGION rule); units without a grid position, tribes (type J) and units
outside the boxes are not records. year = 1596 (daftar year); by_editor = false for the name (the daftar name as
transliterated by the authors); the grid position is the authors' modern identification (placement basis 'grid').
feature_type: type N -> town; Q and OCR variants of it -> village; name beginning Mazra'a/Mazra'at -> field;
name beginning Hirbat/Khirbat -> ruin.
"""
import sys, os, json, csv, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from place_records_i2 import grid_region
EX, MAN, GAZ, OUT = sys.argv[1:5]
man = {m["seg"]: m for m in json.load(open(MAN, encoding="utf-8"))}
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
bad = 0
for f in sorted(glob.glob(os.path.join(EX, "*.json"))):
    chunk = os.path.basename(f)[:-5]
    d = json.load(open(f, encoding="utf-8"))
    k = 0
    for l in d.get("result", "").split("\n"):
        l = l.strip()
        if not l.startswith("{"):
            continue
        try:
            r = json.loads(l)
        except json.JSONDecodeError:
            bad += 1
            continue
        k += 1
        seg = chunk.split("__")[0]
        m = man[seg]
        sd = str(r.get("speaker_date", "") or "")
        y = year_of(sd) if sd.strip() else year_of(m["date_of_writing"])
        be = r.get("by_editor")
        be = (be is True) or str(be).lower() == "true"
        prim = (not be) and (y is not None) and (1100 <= y <= 1600)
        pp = " ".join(str(r.get("position_phrase", "")).split()[:15])
        rows.append(dict(rec_id=f"{chunk}-{k:03d}", seg=seg, chunk=chunk, source_file=m["file"], text=m["text"],
                         lines=r.get("lines", ""), page=r.get("page", ""), name_as_printed=r.get("name_as_printed", ""),
                         translit=r.get("translit", ""),
                         name_language=r.get("name_language", ""), other_names=r.get("other_names", ""),
                         feature_type=r.get("feature_type", ""), feature_text=r.get("feature_text", ""),
                         region=r.get("region", ""), anchor_place=r.get("anchor_place", ""), direction=r.get("direction", ""),
                         distance=r.get("distance", ""), position_phrase=pp, by_editor=be, speaker_date=sd,
                         year_used=y if y is not None else "", primary_layer=prim, grid_e="", grid_n=""))
ng = {"no grid": 0, "tribe": 0, "outside regions": 0}
for g in csv.DictReader(open(GAZ, encoding="utf-8")):
    if g["type_raw"].startswith("J"):
        ng["tribe"] += 1; continue
    if g["grid_e"] == "":
        ng["no grid"] += 1; continue
    E, N = int(g["grid_e"]), int(g["grid_n"])
    reg = grid_region(E, N)
    if not reg:
        ng["outside regions"] += 1; continue
    nm = g["name"]
    ft = "town" if g["type_raw"] == "N" else "village"
    if re.match(r"\W*mazra", nm, re.I):
        ft = "field"
    elif re.match(r"\W*(k?h|y)irba", nm, re.I):
        ft = "ruin"
    uid = re.sub(r"[^A-Za-z0-9]", "", g["unit_raw"])
    rows.append(dict(rec_id=f"hutt_gaz-{g['liwa']}-p{g['pdf_page']}-{uid}", seg="hutt_gaz", chunk="", source_file="Huetteroth 1977 ch. VI",
                     text=f"Huetteroth & Abdulfattah 1977, liwa' {g['liwa']}" + (f", nahiya {g['nahiya']}" if g["nahiya"] else ""),
                     lines="", page=g["book_page"], name_as_printed=nm, translit="", name_language="Arabic", other_names="",
                     feature_type=ft, feature_text=f"fiscal unit type {g['type_raw']}", region=reg, anchor_place="", direction="",
                     distance="", position_phrase=f"Palestine grid {E}/{N}", by_editor=False, speaker_date="1596", year_used=1596,
                     primary_layer=True, grid_e=E, grid_n=N))
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
import collections
print(len(rows), "records;", sum(r["primary_layer"] for r in rows), "in primary layer; malformed lines:", bad)
print("gazetteer units not used:", ng)
print(collections.Counter((r["seg"], r["primary_layer"]) for r in rows))
