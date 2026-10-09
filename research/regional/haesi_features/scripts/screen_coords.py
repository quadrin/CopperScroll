#!/usr/bin/env python3
"""Supplementary coordinate screen (S3, post-freeze, additive): find every map reference in the
readable full texts, convert it and list those within 5 km of a place or inside a region box.

Run: python3 -I screen_coords.py <out_csv> <label>=<text_file> [<label>=<text_file> ...]
Text files are the volume texts as read (Hebrew already in logical order). Standard library + pyproj.
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import geo  # noqa: E402

PLAN = Path(__file__).resolve().parent.parent / "search_plan.json"
REF = re.compile(r"(?:map\s*ref[s]?\.?|נ[\"״]צ|נ\.צ\.)\s*(?:(NIG|OIG|New Israel Grid|Old Israel Grid)\s*)?\(?\s*"
                 r"(\d{3,6}(?:\s*[–-]\s*\d+)?\s*/\s*\d{3,6}(?:\s*[–-]\s*\d+)?)", re.I)


def boxes():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    out = {}
    for k, v in plan["regions"].items():
        if isinstance(v, dict) and "lat" in v:
            out[k] = (v["lat"], v["lon"])
    return out


def in_boxes(lat, lon, bx):
    return [k for k, (la, lo) in sorted(bx.items()) if la[0] <= lat <= la[1] and lo[0] <= lon <= lo[1]]


def main(out_csv, pairs):
    places = geo.load_places()
    bx = boxes()
    rows = []
    for pair in pairs:
        label, path = pair.split("=", 1)
        text = Path(path).read_text(encoding="utf-8")
        for m in REF.finditer(text):
            i = text.count("\n", 0, m.start()) + 1
            lab = (m.group(1) or "").upper()
            lab = "NIG" if lab.startswith("NEW") or lab == "NIG" else ("OIG" if lab.startswith("OLD") or lab == "OIG" else "")
            try:
                r = geo.parse_ref(m.group(2), lab)
            except ValueError:
                continue
            lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
            d = geo.distances(lat, lon, places)
            regs = in_boxes(lat, lon, bx)
            if d[0][0] <= 5.0 or regs:
                rows.append(dict(volume=label, line=i, ref=m.group(2), grid=r["grid"], lat=round(lat, 5),
                                 lon=round(lon, 5), nearest=d[0][1], km=d[0][0],
                                 within_2km=";".join(p for k, p in d if k <= 2.0),
                                 within_5km=";".join(p for k, p in d if k <= 5.0), regions=";".join(regs)))
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["volume"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} map references within 5 km of a place or inside a region box")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
