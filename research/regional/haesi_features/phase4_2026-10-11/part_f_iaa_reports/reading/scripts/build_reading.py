#!/usr/bin/env python3
"""Phase 4, part F reading pass (reader r4): build reports.csv and features.csv from the hand coding.

Reads (reading/data): coding.json (one record per IAA Reports unit), spans.csv (text span hashes and
quote checks made on the owner's Mac); ../pdfs_needed.csv (unit ids, URLs, tier, order); the frozen
phase-2 plan (PLAN.md JSON block) and the phase-1/phase-2 helpers, unchanged.
Writes (reading): reports.csv, features.csv (phase-2 column order), not_read.csv, summary.json.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_f_iaa_reports/reading/scripts/build_reading.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
READ = HERE.parent
DATA = READ / "data"
PART = READ.parent
PHASE4 = PART.parent
LANE = PHASE4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
import common  # noqa: E402  (phase-2 helpers; also puts the phase-1 scripts on sys.path)
import geo  # noqa: E402
import build as p1  # noqa: E402

CLASSES = ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"]
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]
FEATURE_FIELDS = p1.FEATURE_FIELDS + ["region_zone", "dist_to_nearest_place_km", "feature_subtype", "exposure_at_freeze"]
REPORT_FIELDS = p1.REPORT_FIELDS + ["region_zone", "dist_to_nearest_place_km", "exposure_at_freeze", "tier"]
NOT_READ_FIELDS = ["unit_id", "tier", "order_within_tier", "reason", "parts_not_read"]
SCREEN = "S-F (portal title screen, phase 4)"


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def fmt(x, nd):
    return "" if x is None or x == "" else ("%.*f" % (nd, x))


def locate_ref(ref, places, params):
    r = geo.parse_ref(ref)
    lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
    d = geo.distances(lat, lon, places)
    return dict(grid=r["grid"], crs="EPSG:28191" if r["grid"] == "OIG" else "EPSG:2039", e=r["e"], n=r["n"],
                unit=r["unit_m"], lat=lat, lon=lon, dists=d, zone=common.zone_of(lat, lon, params) or "outside")


def load_coding():
    reps = json.loads((DATA / "coding.json").read_text(encoding="utf-8"))
    ids = [r["report_id"] for r in reps]
    assert len(ids) == len(set(ids)), "duplicate report_id"
    return reps


def build(reps, needed, spans, params, places, entries_by_place, bx):
    features, reports, outside = [], [], []
    for rep in reps:
        rid = rep["report_id"]
        nd = needed[rid]
        sp = spans[rid]
        assert sp["quotes_checked"] == sp["quotes_found_verbatim"] == str(len(rep["features"])), rid
        assert sp["pdf_pages_hashed"] == rep["pdf_pages"], rid
        ref = rep.get("map_ref_used") or rep.get("map_ref")
        if ref:
            loc = locate_ref(ref, places, params)
            src_txt = "map ref (p. %s)" % rep["map_ref_page"]
        else:
            loc = dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[],
                       zone=rep.get("name_zone") or "unlocated")
            src_txt = "name only" + (" (%s)" % rep["name_place"] if rep.get("name_place") else "")
        d = loc["dists"]
        nearest, dist = (d[0][1], d[0][0]) if d else (rep.get("name_place", ""), None)
        w2 = [p for k, p in d if k <= 2.0]
        w5 = [p for k, p in d if k <= 5.0]
        regs = p1.regions_for(loc["lat"], loc["lon"], d, common.norm(rep["title"]).strip(), rep, bx)
        if d:
            status = "within 2 km" if dist <= 2.0 else ("2-5 km" if dist <= 5.0 else "beyond 5 km")
        elif rep.get("name_place"):
            status = "name only"
        else:
            status = "name only (zone)" if rep.get("name_zone") else "unlocated"
        place_for_entries = nearest if (dist is not None and dist <= 2.0) or (dist is None and nearest) else ""
        cand = ";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else ""
        frows = []
        for f in rep["features"]:
            assert f["type"] in CLASSES, (rid, f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (rid, f["window"])
            assert len(f["quote"].split()) <= 12, (rid, f["quote"])
            row = dict(report_id=rid, url=nd["landing_url"], series="IAA Reports", volume=rep["volume"],
                       year=rep["year"], pages=f["pages"], site_name=rep["title"], author=rep["author"],
                       permit=rep.get("permit", ""), map_ref_as_given=rep.get("map_ref", ""),
                       map_ref_used=rep.get("map_ref_used", ""), grid=loc["grid"], crs_used=loc["crs"],
                       easting_m=loc["e"], northing_m=loc["n"], precision_m=loc["unit"], lat=fmt(loc["lat"], 5),
                       lon=fmt(loc["lon"], 5), coordinate_source=src_txt, feature_site=f.get("site", ""),
                       nearest_place=nearest, distance_km=fmt(dist, 3), places_within_2km=";".join(w2),
                       places_within_5km=";".join(w5), regions=";".join(regs), feature_type=f["type"],
                       n_features=f.get("n", ""), period_as_given=f["period"], dated_in_window=f["window"],
                       excavated_or_surveyed=rep["excavated_or_surveyed"], quote=f["quote"], relevance="",
                       candidate_entries=cand, protected_strip="no", screen=SCREEN, region_zone=loc["zone"],
                       dist_to_nearest_place_km=fmt(dist, 3), feature_subtype=f.get("subtype", ""),
                       exposure_at_freeze="unexposed at freeze")
            (frows if loc["zone"] in ZONES else outside).append(row)
        features.extend(frows)
        access = ("owner's Mac PDF '%s' (SHA-256 %s; downloaded under the phase-4 plan, approved by the owner), %s"
                  % (sp["pdf_file"], sp["pdf_sha256"], sp["text_source"]))
        reports.append(dict(report_id=rid, url=nd["landing_url"], access=access, series="IAA Reports",
                            volume=rep["volume"], year=rep["year"], pages=rep["pages_read"], site_name=rep["title"],
                            author=rep["author"], permit=rep.get("permit", ""), screen=SCREEN, toc_item="",
                            map_ref_as_given=rep.get("map_ref", ""), map_ref_used=rep.get("map_ref_used", ""),
                            grid=loc["grid"], crs_used=loc["crs"], lat=fmt(loc["lat"], 5), lon=fmt(loc["lon"], 5),
                            coordinate_source=src_txt, nearest_place=nearest, distance_km=fmt(dist, 3),
                            places_within_2km=";".join(w2), places_within_5km=";".join(w5), regions=";".join(regs),
                            location_status=status, excavated_or_surveyed=rep["excavated_or_surveyed"],
                            area_depth_stated="", n_feature_rows=len(frows),
                            feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file="%s text, PDF pages %s (outside the repository)" % (rid, rep["pdf_pages"]),
                            text_lines="PDF pages %s" % rep["pdf_pages"], text_sha256=sp["text_sha256"],
                            protected_strip="no", location_note=rep.get("location_note", ""),
                            notes=rep.get("notes", ""), region_zone=loc["zone"],
                            dist_to_nearest_place_km=fmt(dist, 3), exposure_at_freeze="unexposed at freeze",
                            tier="%s position %s" % (nd["tier"], nd["order_within_tier"])))
    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["dated_in_window"], r["feature_site"]))
    reports.sort(key=lambda r: r["report_id"])
    return features, reports, outside


def not_read(reps, needed):
    """Units read only in part: chapters absent from the portal PDF or not opened (finds catalogues)."""
    out = []
    for rep in reps:
        nd = needed[rep["report_id"]]
        if rep.get("parts_not_read"):
            out.append(dict(unit_id=rep["report_id"], tier=nd["tier"], order_within_tier=nd["order_within_tier"],
                            reason="read in part", parts_not_read=rep["parts_not_read"]))
    for uid, nd in needed.items():
        if uid not in {r["report_id"] for r in reps}:
            out.append(dict(unit_id=uid, tier=nd["tier"], order_within_tier=nd["order_within_tier"],
                            reason="not read (time limit)", parts_not_read="whole unit"))
    return out


def summarize(features, reports, outside):
    by = defaultdict(Counter)
    for f in features:
        by[(f["feature_type"], f["region_zone"])][f["dated_in_window"]] += 1
    cls = {"%s|%s" % k: dict(rows=sum(v.values()), yes=v["yes"], no=v["no"], unknown=v["unknown"])
           for k, v in sorted(by.items())}
    return dict(units_read=len(reports), feature_rows=len(features), outside_region_rows=len(outside),
                rows_by_class_zone=cls,
                rows_by_window=dict(Counter(f["dated_in_window"] for f in features)),
                units_with_features=sum(1 for r in reports if int(r["n_feature_rows"]) > 0))


def main(out_dir=READ):
    out_dir = Path(out_dir)
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    entries_by_place = defaultdict(list)
    for c in read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]),
                                     key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    plan1 = json.loads((LANE / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)
    needed = {r["unit_id"]: r for r in read_csv(PART / "pdfs_needed.csv")}
    spans = {r["report_id"]: r for r in read_csv(DATA / "spans.csv")}
    reps = load_coding()
    assert set(spans) == {r["report_id"] for r in reps}, "spans.csv and coding disagree"
    assert set(r["report_id"] for r in reps) <= set(needed), "unit id not in pdfs_needed.csv"
    features, reports, outside = build(reps, needed, spans, params, places, entries_by_place, bx)
    assert not outside, "feature rows outside the region: %r" % [r["report_id"] for r in outside]
    write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    write_csv(out_dir / "not_read.csv", NOT_READ_FIELDS, not_read(reps, needed))
    summ = summarize(features, reports, outside)
    (out_dir / "summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                          encoding="utf-8")
    print("units read %d, feature rows %d" % (len(reports), len(features)))


if __name__ == "__main__":
    out = READ
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
    main(out)
