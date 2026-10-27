"""Step 2: cave inventory for run 10 (cave_entries_2026-10-27).

Reads (read-only) the entry-25 lane tables: caves.csv, iaa_units.csv, phase4_units.csv, excluded.csv
(crevice / cleft / fissure records only) and the ASI-Jerusalem lane tables (sites.csv, features.csv)
for the two candidate places outside the lane's box (jer_temple, natuf).
Writes out/inventory.csv: one row per (cave, entry) membership, with distances.
"""
import csv, json, math, os, sys
from pyproj import Transformer

REPO = "/home/claude/copperscroll/research/regional"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
OIG2WGS = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)

PLACES = {
    "jer_temple": (31.77825, 35.23534, 150),
    "kh_qumran": (31.74183, 35.45941, 100),
    "abu_saraj_iv17": (31.89009, 35.42477, 300),
    "jericho_area": (31.85611, 35.46306, 3000),
    "tell_el_qos": (31.8551, 35.4656, 200),
    "natuf": (31.64436, 35.23543, 700),
}
ENTRY_PLACES = {
    "7": ["jer_temple"], "22": ["kh_qumran"], "25": ["kh_qumran", "abu_saraj_iv17"],
    "26": ["kh_qumran"], "30": ["jericho_area", "tell_el_qos"], "38": ["natuf"],
}
BAND_ENTRIES = {"22", "25", "26"}
BAND = (31.700, 31.790, 35.420, 35.475)
RADIUS = 5000.0


def dist_m(a, b):
    la1, lo1 = map(math.radians, a); la2, lo2 = map(math.radians, b)
    x = (lo2 - lo1) * math.cos((la1 + la2) / 2); y = la2 - la1
    return 6371000.0 * math.hypot(x, y)


def bearing(a, b):
    la1, lo1 = map(math.radians, a); la2, lo2 = map(math.radians, b)
    x = (lo2 - lo1) * math.cos((la1 + la2) / 2); y = la2 - la1
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def lane_rows():
    rows = []
    for fn, src in (("caves.csv", "lane"), ("iaa_units.csv", "lane-iaa"), ("phase4_units.csv", "lane-phase4")):
        for r in csv.DictReader(open(os.path.join(REPO, "caves_entry25", fn), encoding="utf-8")):
            r["_src"] = src
            r["_kind"] = "cave" if r["row_kind"] == "cave" else r["row_kind"]
            rows.append(r)
    # fissure / crevice / cleft records from excluded.csv
    for r in csv.DictReader(open(os.path.join(REPO, "caves_entry25", "excluded.csv"), encoding="utf-8")):
        t = (r["feature_type_source"] + " " + r["reason"]).lower()
        if not any(w in t for w in ("crev", "cleft", "fiss", "crack")):
            continue
        if not r["coord_printed"] or r["crs_printed"] != "OIG":
            rows.append({"cave_id": r["record_id"], "name_number": r["name_number"], "source_records": r["source_records"],
                         "feature_type_source": r["feature_type_source"], "lat": "", "lon": "", "precision_m": "",
                         "_src": "lane-excluded-fissure", "_kind": "fissure", "notes": "no printed coordinates"})
            continue
        x, y = r["coord_printed"].split("/")
        x = float(x); y = float(y)
        if x < 100000:  # 10 m unit (e.g. 19348/12872)
            x *= 10; y *= 10; prec = 5.0
        else:
            prec = 5.0
        lon, lat = OIG2WGS.transform(x, y)
        rows.append({"cave_id": r["record_id"], "name_number": r["name_number"], "source_records": r["source_records"],
                     "feature_type_source": r["feature_type_source"], "lat": f"{lat:.6f}", "lon": f"{lon:.6f}",
                     "precision_m": str(prec), "_src": "lane-excluded-fissure", "_kind": "fissure", "notes": ""})
    return rows


def asi_rows():
    """ASI-Jerusalem lane: records within 3 km of a place that have a 'cave' feature class."""
    feats = list(csv.DictReader(open(os.path.join(REPO, "asi_jerusalem", "features.csv"), encoding="utf-8")))
    sites = {r["record_id"]: r for r in csv.DictReader(open(os.path.join(REPO, "asi_jerusalem", "sites.csv"), encoding="utf-8"))}
    by = {}
    for f in feats:
        by.setdefault(f["record_id"], []).append(f)
    out = []
    for rid, fl in by.items():
        classes = sorted({f["feature_class"] for f in fl})
        if "cave" not in classes:
            continue
        s = sites[rid]
        cave_f = [f for f in fl if f["feature_class"] == "cave"]
        dated = sorted({f["dated_in_window"] for f in cave_f})
        out.append({"cave_id": f"ASI:{s['map_num']}/{s['site_num']}", "name_number": s["name"], "source_records": s["citation"],
                    "feature_type_source": "ASI record with cave feature", "lat": s["lat"], "lon": s["lon"], "precision_m": "50",
                    "_src": "asi_jerusalem", "_kind": "cave", "asi_classes": ";".join(classes),
                    "asi_cave_dated_in_window": ";".join(dated), "asi_site_finds_in_window": s["site_finds_in_window"],
                    "asi_periods": s["periods_as_given"], "asi_url": s["url"], "notes": s.get("quote", "")})
    return out


# Rows the lane placed "by description" (no point). Placement fixed before any clause was coded
# (INFERENCE from the lane's where_described text): (lat, lon, sigma_m, basis).
QUMRAN_MARL = (31.74183, 35.45941, 300, "description: marl terrace by Kh. Qumran (Qumran point, sigma 300 m)")
QUMRAN_CLIFF = (31.745, 35.445, 3000, "description: Qumran cliff band (band centre, sigma 3 km)")
DESC = {
    "DJD3:4Q": QUMRAN_MARL, "DJD3:5Q": QUMRAN_MARL, "DJD3:7Q": QUMRAN_MARL, "DJD3:8Q": QUMRAN_MARL,
    "DJD3:9Q": QUMRAN_MARL, "DJD3:10Q": QUMRAN_MARL, "DJD3:oval": QUMRAN_MARL,
    "A41:XIV/marl-2": QUMRAN_MARL, "A41:XIV/marl-3": QUMRAN_MARL,
    "A41:XI/7": (31.74183, 35.45941, 1000, "description: lower cliff above Horbat Qumran (sigma 1 km)"),
}
for k in ("DJD3:5", "DJD3:6", "DJD3:11", "DJD3:13", "DJD3:20", "DJD3:23", "DJD3:25", "DJD3:33", "DJD3:34",
          "DJD3:36", "DJD3:38", "DJD3:11Q", "DJD3:A", "DJD3:B", "REPO:JonesNorth"):
    DESC[k] = QUMRAN_CLIFF
NJ = (31.888, 35.424, 1800, "description: Na'aran-Jericho cliff, Wadi Makkuk to Qarantal (segment centre, sigma 1.8 km)")
LMAK = (31.905, 35.405, 1000, "description: lower Wadi el-Makkuk (sigma 1 km)")
UMAK = (31.905, 35.385, 1500, "description: upper/eastern Wadi Makkuk (sigma 1.5 km)")
DESC["Z23:KetefJericho"] = (31.850, 35.435, 1500, "description: cliff west of Jericho, Ketef Jericho (Zissu p. 205; sigma 1.5 km)")
DESC["Z23:JerichoRidge"] = (31.860, 35.430, 2500, "description: Jericho ridge (Zissu p. 207; sigma 2.5 km)")
QILT = (31.846, 35.425, 1000, "description: Wadi Qilt within 2 km E of St George's (sigma 1 km)")


def place_desc(r):
    cid = r["cave_id"]
    if cid in DESC:
        return DESC[cid]
    if cid.startswith("PAT:NJ-"):
        return NJ
    if cid.startswith("PAT:LMakkuk-") or cid in ("A41:III/12", "A41:III/13"):
        return LMAK
    if cid.startswith("PAT:UMakkuk-"):
        return UMAK
    if cid.startswith("PAT:Qilt-"):
        return QILT
    return None


# Eshel & Porat source lane (Porat 2023, Drive 1F1CVv2LfnbMSKmB-mTTMKHa8zxAwNB9t): caves of Wadi Khureitun.
# Positions are by description only (INFERENCE); sigma large.
PORAT = [
    {"cave_id": "PORAT23:HaNer", "name_number": "Ha-Ner Cave, Nahal Teqo'a shelter", "lat": "31.655", "lon": "35.240", "precision_m": "1500",
     "source_records": "Porat 2023 pp. 222, 229, 234, Fig. 12", "feature_type_source": "cave (refuge-cave shelter)",
     "period_stated": "used as a shelter in the Jewish revolts (Porat 2023 pp. 222, 229)", "period_in_window": "yes",
     "excavation_status": "surveyed (Porat)", "notes": "'at the foot of Herodium on the south'; entrances concealed (p. 234)",
     "_src": "porat2023", "_kind": "cave", "_placement": "description: Nahal Teqo'a at the foot of Herodium on the south (sigma 1.5 km)"},
    {"cave_id": "PORAT23:HaPitriya", "name_number": "Ha-Pitriya Cave, Nahal Teqo'a shelter", "lat": "31.655", "lon": "35.240", "precision_m": "1500",
     "source_records": "Porat 2023 pp. 222, 229, 234, Fig. 12", "feature_type_source": "cave (refuge-cave shelter)",
     "period_stated": "used as a shelter in the Jewish revolts (Porat 2023 pp. 222, 229)", "period_in_window": "yes",
     "excavation_status": "surveyed (Porat)", "notes": "'at the foot of Herodium on the south'; entrances concealed (p. 234)",
     "_src": "porat2023", "_kind": "cave", "_placement": "description: Nahal Teqo'a at the foot of Herodium on the south (sigma 1.5 km)"},
    {"cave_id": "PORAT23:Chariton", "name_number": "the large Chariton Cave", "lat": "31.64436", "lon": "35.23543", "precision_m": "1000",
     "source_records": "Porat 2023 p. 234 n. 16", "feature_type_source": "cave", "period_stated": "pottery 'from the period under discussion' (revolts)",
     "period_in_window": "yes", "excavation_status": "surveyed (Ulman)", "notes": "no ASI crosswalk stated",
     "_src": "porat2023", "_kind": "cave", "_placement": "description: Wadi Khureitun near the Chariton laura (sigma 1 km)"},
]


def main():
    rows = lane_rows() + asi_rows() + PORAT
    inv = []
    for r in rows:
        if not r.get("lat"):
            pd = place_desc(r)
            if pd is None:
                continue
            r["lat"], r["lon"], r["precision_m"] = str(pd[0]), str(pd[1]), str(pd[2])
            r["_placement"] = pd[3]
        p = (float(r["lat"]), float(r["lon"]))
        prec = float(r["precision_m"] or 100)
        in_band = BAND[0] <= p[0] <= BAND[1] and BAND[2] <= p[1] <= BAND[3]
        for e, pl in ENTRY_PLACES.items():
            ds = {k: dist_m(p, PLACES[k][:2]) for k in pl}
            near = min(ds, key=ds.get)
            member = ds[near] <= RADIUS
            basis = "5km" if member else ""
            if not member and e in BAND_ENTRIES and in_band:
                member, basis = True, "band"
            if not member:
                continue
            # ASI rows only count for the two places outside the lane's box (avoid double counting)
            if r["_src"] == "asi_jerusalem" and near not in ("jer_temple", "natuf"):
                continue
            inv.append({"entry": e, "cave_id": r["cave_id"], "src": r["_src"], "kind": r["_kind"], "basis": basis,
                        "near_place": near, "dist_m": round(ds[near]), "bearing_from_place": round(bearing(PLACES[near][:2], p), 1),
                        "lat": r["lat"], "lon": r["lon"], "precision_m": prec, "placement": r.get("_placement", "point")})
    with open(os.path.join(OUT, "inventory.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(inv[0].keys()))
        w.writeheader(); w.writerows(inv)
    with open(os.path.join(OUT, "all_rows.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False)
    from collections import Counter
    print(Counter((x["entry"], x["src"]) for x in inv))
    print("no-coord rows:", [r["cave_id"] for r in rows if not r.get("lat")][:50])


if __name__ == "__main__":
    main()
