#!/usr/bin/env python3
"""Lane I2 step 2: place each record. Lane I rule (I/scripts/place_records.py) unchanged, with these additions,
fixed before any matching:
 G. Huetteroth gazetteer records carry a Palestine-grid position (km E/N, as printed, 1 km resolution).
    Conversion: E*1000, N*1000 = EPSG:28191 (Palestine 1923 / Palestine Grid, Cassini) -> EPSG:4326 with pyproj
    (repo convention, research/history/devaux1952_cave_points/scripts/build.py). radius = 1.0 km
    (0.5 km reading resolution + 0.5 km for the authors' modern identification; datum error < 0.01 km).
    basis = 'grid'. Region code from grid_region() (boxes below).
 H. Anchor patterns: lane I data/anchors.csv (unchanged) + I2 data/anchors_hebrew.csv (Hebrew-script forms of the
    same 29 anchors, same coordinates and sigma) + I2 data/anchors_extra_latin.csv (French/Russian-pilgrim spellings
    of the same 29 anchors). Patterns are tried on the text as given, on the text with
    diacritics stripped (DMG macrons), and, for Khitrowo (seg kh_*), on the text with the OCR long-s 'f' -> 's'.
 U. Extra distance units: verst/verste 1.07 km; Hebrew mil (מיל) 1.5 km, parsa (פרסה/פרסאות) 5 km, day (יום) 30 km,
    hour (שעה/שעות) 4 km, half day (חצי יום) 15 km; extra number words (French 15-100; Hebrew 1-10, half).
 Lane I rules 1-3 (own name -> anchor sigma; relative -> sigma + distance or + 3 km; else region only) unchanged.
 C. Copyright: after placement, position_phrase and feature_text of records from Huetteroth's running text
    (seg hutt_txt) are replaced by '[omitted: in copyright]' in the output (they are not used by the matcher).
    The unredacted input table is kept outside the repository; its SHA-256 is in the protocol.
Region boxes for gazetteer rows (Palestine grid km), from lane I's five region definitions:
 JER: within 6 km of 172.5/131.5 (Haram); JJV: 187<=E<=210, 110<=N<=155; DES: 166<=E<187, 95<=N<=128 (desert and
 its western edge, Bethlehem-Tekoa line, as lane I's DES definition) or 187<=E<=200, 85<=N<110 (west Dead Sea shore); GER: within 10 km of 175/180 (Nablus); PER: 210<E<=240, 110<=N<=160.
Usage: python3 -I place_records_i2.py RECORDS_CSV LANE_I_ANCHORS_CSV HEBREW_ANCHORS_CSV EXTRA_LATIN_CSV OUT_CSV
"""
import sys, csv, re, math, unicodedata
def grid_region(E, N):
    if math.hypot(E - 172.5, N - 131.5) <= 6:
        return "JER"
    if 187 <= E <= 210 and 110 <= N <= 155:
        return "JJV"
    if (166 <= E < 187 and 95 <= N <= 128) or (187 <= E <= 200 and 85 <= N < 110):
        return "DES"
    if math.hypot(E - 175, N - 180) <= 10:
        return "GER"
    if 210 < E <= 240 and 110 <= N <= 160:
        return "PER"
    return ""
if __name__ == "__main__":
    RC, AC, HC, XC, OUT = sys.argv[1:6]
    from pyproj import Transformer
    T = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)
    anchors = list(csv.DictReader(open(AC, encoding="utf-8")))
    heb = {r["anchor_id"]: r["hebrew_pattern"] for r in csv.DictReader(open(HC, encoding="utf-8"))}
    xla = {r["anchor_id"]: r["extra_pattern"] for r in csv.DictReader(open(XC, encoding="utf-8"))}
    for a in anchors:
        a["rx"] = re.compile(a["pattern"] + "|" + heb[a["anchor_id"]] + "|" + xla[a["anchor_id"]], re.I)
    NUM = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
           "ten": 10, "twelve": 12, "half": 0.5, "half a": 0.5, "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
           "sept": 7, "huit": 8, "dix": 10, "demi": 0.5, "demie": 0.5,
           "quinze": 15, "vingt": 20, "trente": 30, "quarante": 40, "cinquante": 50, "soixante": 60, "cent": 100, "douze": 12,
           "אחד": 1, "אחת": 1, "שני": 2, "שתי": 2, "שנים": 2, "שלש": 3, "שלשה": 3, "שלוש": 3, "ארבע": 4, "ארבעה": 4, "חמש": 5,
           "חמשה": 5, "שש": 6, "ששה": 6, "שבע": 7, "שבעה": 7, "שמונה": 8, "תשע": 9, "עשר": 10, "עשרה": 10, "חצי": 0.5}
    UNIT = [(r"parasang|פרס", 5.0), (r"league|lieue", 4.5), (r"verst", 1.07), (r"mile|mille|מיל", 1.5), (r"stad|furlong", 0.2),
            (r"bow.?shot|stone'?s.?(throw|cast)|jet de pierre|portée|מטחוי", 0.2), (r"half a day|demi.?journ|חצי יום", 15.0),
            (r"day|journ[ée]e|יום|ימים", 30.0), (r"hour|heure|שע", 4.0)]
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
                if u.startswith("half") or u.startswith("חצי"):
                    n = 1.0
                return n * km
        return None
    def forms(text, seg):
        t = text or ""
        out = [t, "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))]
        if seg.startswith("kh_"):
            out.append(re.sub(r"f(?=[a-zéèêàâîôûç])", "s", t))
        return out
    def find(text, seg):
        for a in anchors:
            if any(a["rx"].search(f) for f in forms(text, seg)):
                return a
        return None
    rows = list(csv.DictReader(open(RC, encoding="utf-8")))
    for r in rows:
        lat = lon = rad = ""; basis = "unplaced"; aid = ""
        if r["grid_e"]:
            lon_, lat_ = T.transform(float(r["grid_e"]) * 1000, float(r["grid_n"]) * 1000)
            lat, lon, rad, basis = round(lat_, 6), round(lon_, 6), 1.0, "grid"
        else:
            own = (r["name_as_printed"] or "") + " | " + (r["other_names"] or "")
            a = find(own, r["seg"])
            if a:
                lat, lon, rad, basis, aid = a["lat"], a["lon"], float(a["sigma_km"]), "own name", a["anchor_id"]
            else:
                a = find(r["anchor_place"], r["seg"]) or find(r["position_phrase"], r["seg"])
                if a:
                    d = parse_km(r["distance"])
                    rad = float(a["sigma_km"]) + (d if d is not None else 3.0)
                    lat, lon, basis, aid = a["lat"], a["lon"], "relative" + ("" if d is not None else " (no distance)"), a["anchor_id"]
        r.update(anchor_id=aid, lat=lat, lon=lon, radius_km=(round(rad, 2) if rad != "" else ""), placement_basis=basis)
        if r["seg"] == "hutt_txt":
            r["position_phrase"] = r["feature_text"] = "[omitted: in copyright]"
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    import collections
    print(collections.Counter((r["seg"].split("_")[0], r["placement_basis"].split(" (")[0]) for r in rows if r["primary_layer"] == "True"))
