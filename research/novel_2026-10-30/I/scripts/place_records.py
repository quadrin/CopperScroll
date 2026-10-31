#!/usr/bin/env python3
"""Step 2: place each medieval record from its own description against repo gazetteer anchors.
Usage: python3 -I place_records.py RECORDS_CSV ANCHORS_CSV OUT_CSV
Rule (fixed before any matching):
 1. If the record's own name (name_as_printed or other_names) matches an anchor pattern: place at that anchor;
    radius = anchor sigma. basis = 'own name'.
 2. Else if anchor_place (or, failing that, position_phrase) matches an anchor pattern: place at that anchor;
    radius = anchor sigma + stated distance (km) if parsed, else anchor sigma + 3 km. basis = 'relative'.
 3. Else unplaced: region only.
 Distances: mile 1.5 km (Roman/medieval mile), league/lieue 4.5 km, parasang 5 km, stade/furlong 0.2 km,
 bowshot/stone's throw 0.2 km, 'day' 30 km, 'half a day' 15 km, 'hour' 4 km.
 Anchors are searched in file order (specific features first, cities and the Jordan last).
"""
import sys, csv, re
RC, AC, OUT = sys.argv[1:4]
anchors = list(csv.DictReader(open(AC, encoding="utf-8")))
for a in anchors:
    a["rx"] = re.compile(a["pattern"], re.I)
NUM = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
       "ten": 10, "twelve": 12, "half": 0.5, "half a": 0.5, "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
       "six": 6, "sept": 7, "huit": 8, "dix": 10, "demi": 0.5, "demie": 0.5}
UNIT = [(r"parasang", 5.0), (r"league|lieue", 4.5), (r"mile|mille", 1.5), (r"stad|furlong", 0.2),
        (r"bow.?shot|stone'?s.?(throw|cast)|jet de pierre|portée", 0.2), (r"half a day|demi.?journ", 15.0),
        (r"day|journ[ée]e", 30.0), (r"hour|heure", 4.0)]
def parse_km(s):
    s = (s or "").lower()
    if not s.strip():
        return None
    for u, km in UNIT:
        m = re.search(r"([\d.]+|" + "|".join(sorted(NUM, key=len, reverse=True)) + r")?\s*(?:\w+\s){0,2}?(" + u + r")", s)
        if m:
            q = m.group(1)
            if q is None:
                n = 1.0
            else:
                try:
                    n = float(q)
                except ValueError:
                    n = NUM.get(q, 1)
            if u.startswith("half"):
                n = 1.0
            return n * km
    return None
def find(text):
    for a in anchors:
        if a["rx"].search(text or ""):
            return a
    return None
rows = list(csv.DictReader(open(RC, encoding="utf-8")))
for r in rows:
    own = (r["name_as_printed"] or "") + " | " + (r["other_names"] or "")
    a = find(own)
    lat = lon = rad = ""; basis = "unplaced"; aid = ""
    if a:
        lat, lon, rad, basis, aid = a["lat"], a["lon"], float(a["sigma_km"]), "own name", a["anchor_id"]
    else:
        a = find(r["anchor_place"]) or find(r["position_phrase"])
        if a:
            d = parse_km(r["distance"])
            rad = float(a["sigma_km"]) + (d if d is not None else 3.0)
            lat, lon, basis, aid = a["lat"], a["lon"], "relative" + ("" if d is not None else " (no distance)"), a["anchor_id"]
    r.update(anchor_id=aid, lat=lat, lon=lon, radius_km=(round(rad, 2) if rad != "" else ""), placement_basis=basis)
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
import collections
print(collections.Counter(r["placement_basis"].split(" (")[0] for r in rows))
