#!/usr/bin/env python3
"""Phase 4, part E, reader r1: build the reading tables from the hand coding.

Reads (reading_r1/data): coding/*.json (one record per unit read), spans.csv (hashes and quote checks made on
the owner's Mac by verify_spans.py), dropped.csv (units located outside the region);
part E pdfs_needed.csv (titles, authors, tiers, order) and the phase-4 downloads manifest (PDF SHA-256);
the frozen phase-2 plan (PLAN.md JSON block) and the phase-1/phase-2 helpers, unchanged.
Writes (reading_r1): reports.csv and features.csv (phase-2 column order), held.csv, not_read.csv,
summary.json and summary.md.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/reading_r1/scripts/build_r1.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
R1 = HERE.parent
DATA = R1 / "data"
PART_E = R1.parent
PHASE4 = PART_E.parent
LANE = PHASE4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
import common  # noqa: E402  (phase-2 helpers; also puts the phase-1 scripts on sys.path)
import geo  # noqa: E402
import build as p1  # noqa: E402  (phase-1 build: region boxes, W2B paths, field lists)

CLASSES = ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"]
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]
FEATURE_FIELDS = p1.FEATURE_FIELDS + ["region_zone", "dist_to_nearest_place_km", "feature_subtype", "exposure_at_freeze"]
REPORT_FIELDS = p1.REPORT_FIELDS + ["region_zone", "dist_to_nearest_place_km", "exposure_at_freeze", "tier"]
HELD_FIELDS = ["unit_id", "volume", "year", "first_page", "last_page", "title", "authors", "landing_url",
               "first_line_seen", "held_area", "held", "tier1_kh_almit", "protected_strip", "note"]
NOT_READ_FIELDS = ["unit_id", "tier", "order_position_in_tier", "reason", "map_ref_as_given", "location_basis"]
TIER_ORDER = {"T1": 0, "U": 1, "T3": 2, "T2": 3}
READER_T2_LIMIT = 60  # this reader's assignment: T1, U and T3 in full, T2 positions 1-60
SCREEN = "S-ATQ (part E title screen; PDF read)"
EXPOSURE = "unexposed at freeze"


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


def assigned_units():
    rows = read_csv(PART_E / "pdfs_needed.csv")
    sel = [r for r in rows if r["tier"] in ("T1", "U", "T3")
           or (r["tier"] == "T2" and int(r["order_position_in_tier"]) <= READER_T2_LIMIT)]
    sel.sort(key=lambda r: (TIER_ORDER[r["tier"]], int(r["order_position_in_tier"])))
    return sel


def load_coding():
    reps = []
    for p in sorted((DATA / "coding").glob("*.json")):
        reps.extend(json.loads(p.read_text(encoding="utf-8")))
    ids = [r["report_id"] for r in reps]
    assert len(ids) == len(set(ids)), "duplicate report_id"
    return reps


def locate_ref(ref, grid, places, params):
    r = geo.parse_ref(ref, grid or "")
    lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
    d = geo.distances(lat, lon, places)
    return dict(grid=r["grid"], crs="EPSG:28191" if r["grid"] == "OIG" else "EPSG:2039", e=r["e"], n=r["n"],
                unit=r["unit_m"], lat=lat, lon=lon, dists=d, zone=common.zone_of(lat, lon, params) or "outside",
                swapped=r["swapped"])


def build(reps, units, params, places, entries_by_place, bx, spans, pdf_sha):
    meta = {u["unit_id"]: u for u in units}
    features, reports, outside_feats = [], [], []
    for rep in reps:
        rid = rep["report_id"]
        m = meta[rid]
        sp = spans[rid]
        assert sp["text_lines"] == rep["text_lines"], rid
        assert not sp["quotes_not_found"], rid
        tf = rep.get("text_file", "raw")
        how = "pdftotext -raw" if tf == "raw" else "pdftotext default reading order (Hebrew text)"
        access = ("owner's Mac PDF 'IAA portal volumes/phase4/%s.pdf' (SHA-256 %s), %s, read on the Mac"
                  % (rid, pdf_sha[rid], how))
        text_file = "%s.%s.txt ($HOME/p4text/r1 on the owner's Mac; outside the repository)" % (rid, tf)
        if rep.get("map_ref") and not rep.get("map_ref_unusable"):
            loc = locate_ref(rep["map_ref"], rep.get("map_ref_grid"), places, params)
            src_txt = "map ref"
        else:
            loc = dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[],
                       zone=rep.get("name_zone") or rep.get("report_zone") or "unlocated", swapped=False)
            src_txt = "name only" + (" (%s)" % rep["name_place"] if rep.get("name_place") else "")
            if rep.get("map_ref_unusable"):
                src_txt += "; printed map reference unusable"
        rzone = rep.get("report_zone") or loc["zone"]
        d = loc["dists"]
        nearest, dist = (d[0][1], d[0][0]) if d else (rep.get("name_place", ""), None)
        w2 = [p for k, p in d if k <= 2.0]
        w5 = [p for k, p in d if k <= 5.0]
        regs = p1.regions_for(loc["lat"], loc["lon"], d, common.norm(m["title"]).strip(), rep, bx)
        if d:
            status = "within 2 km" if dist <= 2.0 else ("2-5 km" if dist <= 5.0 else "beyond 5 km")
        elif rep.get("name_place"):
            status = "name only"
        elif rep.get("name_zone"):
            status = "name only (zone)"
        else:
            status = "unlocated" if not rep.get("report_zone") else rep["report_zone"]
        pages = rep["pages"]
        frows = []
        for f in rep["features"]:
            assert f["type"] in CLASSES, (rid, f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (rid, f["window"])
            assert len(f["quote"].split()) <= 12, (rid, f["quote"])
            fl, fsrc, fnear, fdist, fw2, fw5 = loc, src_txt, nearest, dist, w2, w5
            if f.get("map_ref"):
                fl = locate_ref(f["map_ref"], f.get("map_ref_grid"), places, params)
                fsrc = "feature map ref"
                fd = fl["dists"]
                fnear, fdist = fd[0][1], fd[0][0]
                fw2 = [p for k, p in fd if k <= 2.0]
                fw5 = [p for k, p in fd if k <= 5.0]
            elif f.get("name_zone"):
                # feature without its own map reference, placed by a gazetteer name in the text (plan section 2)
                fl = dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[], zone=f["name_zone"])
                fsrc = "feature name only (%s)" % f["name_basis"]
                fnear, fdist, fw2, fw5 = "", None, [], []
            zone = fl["zone"]
            place_for_entries = fnear if (fdist is not None and fdist <= 2.0) or (fdist is None and fnear) else ""
            row = dict(report_id=rid, url=m["landing_url"], series="Atiqot", volume=m["volume"], year=m["year"],
                       pages=pages, site_name=m["title"], author=m["authors"], permit=rep.get("permit", ""),
                       map_ref_as_given=f.get("map_ref") or rep.get("map_ref", ""), map_ref_used="",
                       grid=fl["grid"], crs_used=fl["crs"], easting_m=fl["e"], northing_m=fl["n"],
                       precision_m=fl["unit"], lat=fmt(fl["lat"], 5), lon=fmt(fl["lon"], 5), coordinate_source=fsrc,
                       feature_site=f.get("site", ""), nearest_place=fnear, distance_km=fmt(fdist, 3),
                       places_within_2km=";".join(fw2), places_within_5km=";".join(fw5), regions=";".join(regs),
                       feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                       dated_in_window=f["window"], excavated_or_surveyed=rep["excavated_or_surveyed"],
                       quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else "",
                       protected_strip=rep.get("protected_strip", "no"), screen=SCREEN, region_zone=zone,
                       dist_to_nearest_place_km=fmt(fdist, 3), feature_subtype=f.get("subtype", ""),
                       exposure_at_freeze=EXPOSURE)
            (frows if zone in ZONES else outside_feats).append(row)
        features.extend(frows)
        reports.append(dict(report_id=rid, url=m["landing_url"], access=access, series="Atiqot", volume=m["volume"],
                            year=m["year"], pages=pages, site_name=m["title"], author=m["authors"],
                            permit=rep.get("permit", ""), screen=SCREEN, toc_item="",
                            map_ref_as_given=rep.get("map_ref", ""), map_ref_used="", grid=loc["grid"],
                            crs_used=loc["crs"], lat=fmt(loc["lat"], 5), lon=fmt(loc["lon"], 5),
                            coordinate_source=src_txt, nearest_place=nearest, distance_km=fmt(dist, 3),
                            places_within_2km=";".join(w2), places_within_5km=";".join(w5), regions=";".join(regs),
                            location_status=status, excavated_or_surveyed=rep["excavated_or_surveyed"],
                            area_depth_stated="", n_feature_rows=len(frows),
                            feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file=text_file, text_lines=rep["text_lines"], text_sha256=sp["text_sha256"],
                            protected_strip=rep.get("protected_strip", "no"),
                            location_note=rep.get("location_note", ""), notes=rep.get("notes", ""),
                            region_zone=rzone, dist_to_nearest_place_km=fmt(dist, 3), exposure_at_freeze=EXPOSURE,
                            tier="%s #%s" % (m["tier"], m["order_position_in_tier"])))
    order = {u["unit_id"]: i for i, u in enumerate(units)}
    reports.sort(key=lambda r: order[r["report_id"]])
    features.sort(key=lambda r: (order[r["report_id"]], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    return features, reports, outside_feats


def summarize(features, reports, outside_feats, not_read, units):
    md = ["# Phase 4, part E, reader r1: summary tables (generated by scripts/build_r1.py; do not edit)\n"]
    tiers = Counter(u["tier"] for u in units)
    read_t = Counter(r["tier"].split()[0] for r in reports)
    md.append("Units assigned: %d (T1 %d, U %d, T3 %d, T2 positions 1-%d: %d). Read and coded: %d. "
              "Dropped as outside the region: %d. Not read: %d.\n" % (
                  len(units), tiers["T1"], tiers["U"], tiers["T3"], READER_T2_LIMIT, tiers["T2"], len(reports),
                  sum(1 for n in not_read if n["reason"].startswith("dropped")),
                  sum(1 for n in not_read if not n["reason"].startswith("dropped"))))
    zr = Counter(r["region_zone"] for r in reports)
    md.append("Reports read by zone: " + "; ".join("%s %d" % (z, zr[z]) for z in sorted(zr)) + ".\n")
    md.append("Reports read with no eligible feature row: %d.\n" % sum(1 for r in reports if int(r["n_feature_rows"]) == 0))
    wt = Counter(f["dated_in_window"] for f in features)
    md.append("Feature rows in the region: %d (dated in window: yes %d, no %d, unknown %d). "
              "Rows outside the region (feature map ref): %d.\n" % (len(features), wt["yes"], wt["no"], wt["unknown"],
                                                                    len(outside_feats)))
    md.append("## Feature rows by class and zone (rows: yes / no / unknown)\n")
    md.append("| class | " + " | ".join(ZONES) + " | all |")
    md.append("|---|" + "---|" * (len(ZONES) + 1))
    tab = defaultdict(Counter)
    for f in features:
        tab[(f["feature_type"], f["region_zone"])][f["dated_in_window"]] += 1
        tab[(f["feature_type"], "all")][f["dated_in_window"]] += 1
    js_tab = {}
    for c in CLASSES:
        cells = []
        for z in ZONES + ["all"]:
            k = tab[(c, z)]
            n = sum(k.values())
            cells.append("%d (%d/%d/%d)" % (n, k["yes"], k["no"], k["unknown"]) if n else "0")
            js_tab["%s|%s" % (c, z)] = dict(rows=n, yes=k["yes"], no=k["no"], unknown=k["unknown"])
        md.append("| %s | %s |" % (c, " | ".join(cells)))
    zt = Counter(f["region_zone"] for f in features)
    md.append("| all classes | " + " | ".join(str(zt[z]) for z in ZONES) + " | %d |" % len(features))
    md.append("\n## Dated-in-window rows\n")
    md.append("| report_id | zone | class | subtype | period as given |")
    md.append("|---|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s | %s |" % (f["report_id"], f["region_zone"], f["feature_type"],
                                                     f["feature_subtype"].replace("|", "/"),
                                                     f["period_as_given"].replace("|", "/")))
    js = dict(units_assigned=len(units), units_by_tier=dict(tiers), reports_read=len(reports),
              reports_read_by_tier=dict(read_t), reports_by_zone=dict(zr),
              reports_without_feature_rows=sum(1 for r in reports if int(r["n_feature_rows"]) == 0),
              not_read=len(not_read), feature_rows=len(features), window=dict(wt), class_zone=js_tab,
              rows_by_zone={z: zt[z] for z in ZONES}, outside_feature_rows=len(outside_feats), held=0)
    return dict(md="\n".join(md) + "\n", json=js)


def main(out_dir=R1):
    out_dir = Path(out_dir)
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    entries_by_place = defaultdict(list)
    for c in read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    plan1 = json.loads((LANE / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)
    units = assigned_units()
    pdf_sha = {r["file"][:-4]: r["sha256"] for r in read_csv(PHASE4 / "downloads_2026-10-11.csv")}
    spans = {r["report_id"]: r for r in read_csv(DATA / "spans.csv")}
    reps = load_coding()
    assert set(spans) == {r["report_id"] for r in reps}, "spans.csv and coding disagree"
    unit_ids = {u["unit_id"] for u in units}
    assert all(r["report_id"] in unit_ids for r in reps), "coded unit outside the assignment"
    features, reports, outside_feats = build(reps, units, params, places, entries_by_place, bx, spans, pdf_sha)
    dropped = {r["unit_id"]: r for r in read_csv(DATA / "dropped.csv")}
    coded = {r["report_id"] for r in reps}
    not_read = []
    for u in units:
        if u["unit_id"] in coded:
            continue
        d = dropped.get(u["unit_id"])
        not_read.append(dict(unit_id=u["unit_id"], tier=u["tier"], order_position_in_tier=u["order_position_in_tier"],
                             reason=d["reason"] if d else "not read (time limit)",
                             map_ref_as_given=d["map_ref_as_given"] if d else "",
                             location_basis=d["location_basis"] if d else ""))
    write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    write_csv(out_dir / "held.csv", HELD_FIELDS, [])
    write_csv(out_dir / "not_read.csv", NOT_READ_FIELDS, not_read)
    summ = summarize(features, reports, outside_feats, not_read, units)
    (out_dir / "summary.json").write_text(json.dumps(summ["json"], ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                          encoding="utf-8")
    (out_dir / "summary.md").write_text(summ["md"], encoding="utf-8")
    print("reports %d, feature rows %d (outside region %d), not read %d" % (
        len(reports), len(features), len(outside_feats), len(not_read)))
    for f in outside_feats:
        print("OUTSIDE:", f["report_id"], f["feature_type"], f["map_ref_as_given"])


if __name__ == "__main__":
    out = R1
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
