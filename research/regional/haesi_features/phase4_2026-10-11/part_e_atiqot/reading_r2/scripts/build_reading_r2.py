#!/usr/bin/env python3
"""Phase 4, part E, reader r2: build the tables from the hand coding of tier T2 positions 61-135.

Reads (reading_r2/data): coding_*.jsonl (one JSON record per unit, hand-coded), page_map.csv (PDF page -> printed
page), mac_text.csv (text SHA-256 per unit, computed on the owner's Mac by verify_on_mac.py), mac_quote_pages.csv
(PDF page on which each quote was found), mac_pdf_sha256.csv (PDF hashes seen on the Mac);
part E pdfs_needed.csv and downloads_2026-10-11.csv; the frozen phase-2 plan (zones) and the phase-1 helpers.
Writes (reading_r2): reports.csv, features.csv (phase-2 columns, same order), held.csv, not_read.csv,
summary.json, summary.md.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/reading_r2/scripts/build_reading_r2.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
DATA = OUT / "data"
PART = OUT.parent
PHASE4 = PART.parent
LANE = PHASE4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
import common  # noqa: E402  (phase-2 helpers; puts the phase-1 scripts on sys.path)
import geo  # noqa: E402
import build as p1  # noqa: E402

CLASSES = ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"]
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]
FEATURE_FIELDS = p1.FEATURE_FIELDS + ["region_zone", "dist_to_nearest_place_km", "feature_subtype", "exposure_at_freeze"]
REPORT_FIELDS = p1.REPORT_FIELDS + ["region_zone", "dist_to_nearest_place_km", "exposure_at_freeze", "tier"]
HELD_FIELDS = ["unit_id", "volume", "year", "first_page", "last_page", "title", "authors", "landing_url",
               "first_line_seen", "held_area", "held", "tier1_kh_almit", "protected_strip", "note"]
NOT_READ_FIELDS = ["unit_id", "tier", "order_position_in_tier", "reason"]
POS_RANGE = (61, 135)
SCREEN = "S-PORTAL (part E screen; PDF read on the owner's Mac)"
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


def load_coding():
    units = []
    for p in sorted(DATA.glob("coding_*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                units.append(json.loads(line))
    ids = [u["unit_id"] for u in units]
    assert len(ids) == len(set(ids)), "duplicate unit_id in coding"
    return units


def assigned_units():
    rows = [r for r in read_csv(PART / "pdfs_needed.csv")
            if r["tier"] == "T2" and POS_RANGE[0] <= int(r["order_position_in_tier"]) <= POS_RANGE[1]]
    rows.sort(key=lambda r: int(r["order_position_in_tier"]))
    return rows


def page_mapper(spec):
    """'2:79' or '2:1:*;16:153:' -> function(pdf_page) -> printed page string."""
    segs = []
    for part in spec.split(";"):
        bits = part.split(":")
        segs.append((int(bits[0]), int(bits[1]), bits[2] if len(bits) > 2 else ""))
    segs.sort()

    def f(pdf):
        s = [x for x in segs if x[0] <= pdf]
        if not s:
            return ""
        a, b, suf = s[-1]
        return "%d%s" % (b + pdf - a, suf)
    return f


def grid_label(ref):
    m = re.match(r"\s*(NIG|OIG)\b", ref)
    return m.group(1) if m else ""


def locate(ref, places, params):
    r = geo.parse_ref(ref, grid_label(ref))
    lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
    d = geo.distances(lat, lon, places)
    return dict(grid=r["grid"], crs="EPSG:28191" if r["grid"] == "OIG" else "EPSG:2039", e=r["e"], n=r["n"],
                unit=r["unit_m"], lat=lat, lon=lon, dists=d, zone=common.zone_of(lat, lon, params) or "outside",
                swapped=r["swapped"])


def build(out_dir=OUT):
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    entries_by_place = defaultdict(list)
    for c in read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    plan1 = json.loads((LANE / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)

    need = {r["unit_id"]: r for r in assigned_units()}
    dl = {r["file"][:-4]: r for r in read_csv(PHASE4 / "downloads_2026-10-11.csv")}
    mac_pdf = {r["unit_id"]: r["pdf_sha256"] for r in read_csv(DATA / "mac_pdf_sha256.csv")}
    text = {r["unit_id"]: r for r in read_csv(DATA / "mac_text.csv")}
    qpages = {(r["unit_id"], int(r["feature_index"])): r for r in read_csv(DATA / "mac_quote_pages.csv")}
    pmap = {r["unit_id"]: r for r in read_csv(DATA / "page_map.csv")}
    coding = {u["unit_id"]: u for u in load_coding()}
    assert set(coding) == set(need), "coding and assigned units differ: %s" % sorted(set(coding) ^ set(need))

    features, reports, outside = [], [], []
    for uid, nd in need.items():
        u = coding[uid]
        t = text[uid]
        assert mac_pdf[uid] == dl[uid]["sha256"], "PDF hash differs from the download manifest: " + uid
        f_page = page_mapper(pmap[uid]["pdf_to_printed"])
        n_pdf = int(t["pdf_pages"])
        url = nd["landing_url"]
        access = ("owner's Mac PDF '%s.pdf' (SHA-256 %s; portal %s), downloaded by the owner 11 Oct 2026; "
                  "pdftotext -raw and -layout" % (uid, mac_pdf[uid], nd["pdf_url"]))
        if u.get("language"):
            access += "; " + u["language"]
        pages = pmap[uid]["printed_pages"]
        year = u.get("year_printed") or nd["year"]
        if u.get("map_ref"):
            loc = locate(u["map_ref"], places, params)
            src = "map ref" + (" (order corrected)" if loc["swapped"] else "")
        else:
            loc = dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[], zone=u["name_zone"], swapped=False)
            src = "name only (%s)" % u["name_place"]
        d = loc["dists"]
        nearest, dist = (d[0][1], d[0][0]) if d else ("", None)
        w2 = [p for k, p in d if k <= 2.0]
        w5 = [p for k, p in d if k <= 5.0]
        regs = p1.regions_for(loc["lat"], loc["lon"], d, common.norm(nd["title"]).strip(),
                              {"features": u["features"]}, bx)
        status = ("within 2 km" if dist <= 2.0 else "2-5 km" if dist <= 5.0 else "beyond 5 km") if d else "name only (zone)"
        frows = []
        for i, f in enumerate(u["features"]):
            assert f["type"] in CLASSES, (uid, f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (uid, f["window"])
            assert 0 < len(f["quote"].split()) <= 12, (uid, f["quote"])
            qp = qpages[(uid, i)]
            fl, fsrc, fnear, fdist, fw2, fw5 = loc, src, nearest, dist, w2, w5
            if f.get("map_ref"):
                fl = locate(f["map_ref"], places, params)
                fsrc = "feature map ref"
                fd = fl["dists"]
                fnear, fdist = fd[0][1], fd[0][0]
                fw2 = [p for k, p in fd if k <= 2.0]
                fw5 = [p for k, p in fd if k <= 5.0]
            place_for_entries = fnear if (fdist is not None and fdist <= 2.0) else ""
            row = dict(report_id=uid, url=url, series="'Atiqot", volume=nd["volume"], year=year,
                       pages=f_page(int(qp["pdf_page"])), site_name=nd["title"], author=u["author"],
                       permit=u.get("permit", ""), map_ref_as_given=f.get("map_ref") or u.get("map_ref_as_given") or u.get("map_ref", ""),
                       map_ref_used=f.get("map_ref") or u.get("map_ref", ""), grid=fl["grid"], crs_used=fl["crs"],
                       easting_m=fl["e"], northing_m=fl["n"], precision_m=fl["unit"], lat=fmt(fl["lat"], 5),
                       lon=fmt(fl["lon"], 5), coordinate_source=fsrc, feature_site=f.get("site", ""), nearest_place=fnear,
                       distance_km=fmt(fdist, 3), places_within_2km=";".join(fw2), places_within_5km=";".join(fw5),
                       regions=";".join(regs), feature_type=f["type"], n_features=f.get("n", ""),
                       period_as_given=f["period"], dated_in_window=f["window"],
                       excavated_or_surveyed=f.get("excavated_or_surveyed") or u["excavated_or_surveyed"],
                       quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else "",
                       protected_strip="no", screen=SCREEN, region_zone=fl["zone"],
                       dist_to_nearest_place_km=fmt(fdist, 3), feature_subtype=f.get("subtype", ""),
                       exposure_at_freeze=EXPOSURE)
            (frows if fl["zone"] in ZONES else outside).append(row)
        features.extend(frows)
        notes = [u.get("notes", ""), "kind: %s (INFERENCE from the article)" % u["kind"]]
        reports.append(dict(report_id=uid, url=url, access=access, series="'Atiqot", volume=nd["volume"], year=year,
                            pages=pages, site_name=nd["title"], author=u["author"], permit=u.get("permit", ""),
                            screen=SCREEN, toc_item=nd["title"],
                            map_ref_as_given=u.get("map_ref_as_given") or u.get("map_ref", ""),
                            map_ref_used=u.get("map_ref", ""), grid=loc["grid"], crs_used=loc["crs"],
                            lat=fmt(loc["lat"], 5), lon=fmt(loc["lon"], 5), coordinate_source=src, nearest_place=nearest,
                            distance_km=fmt(dist, 3), places_within_2km=";".join(w2), places_within_5km=";".join(w5),
                            regions=";".join(regs), location_status=status,
                            excavated_or_surveyed=u["excavated_or_surveyed"], area_depth_stated="",
                            n_feature_rows=len(frows), feature_types=";".join(sorted({f["type"] for f in u["features"]})),
                            text_file="%s.raw.txt and %s.layout.txt (owner's Mac, $HOME/p4text/r2; outside the repository)" % (uid, uid),
                            text_lines="PDF pp. 2-%d (portal cover page 1 excluded); %d characters" % (n_pdf, int(t["text_chars"])),
                            text_sha256=t["text_sha256"], protected_strip="no", location_note=u.get("location_note", ""),
                            notes="; ".join(x for x in notes if x), region_zone=loc["zone"],
                            dist_to_nearest_place_km=fmt(dist, 3), exposure_at_freeze=EXPOSURE,
                            tier="T2 #%s" % nd["order_position_in_tier"]))
    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    reports.sort(key=lambda r: int(r["tier"].split("#")[1]))
    out_dir = Path(out_dir)
    write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    write_csv(out_dir / "held.csv", HELD_FIELDS, [])
    write_csv(out_dir / "not_read.csv", NOT_READ_FIELDS, [])
    summ = summarize(features, reports, outside)
    (out_dir / "summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "summary.md").write_text(summary_md(summ), encoding="utf-8")
    return features, reports, outside, summ


def summarize(features, reports, outside):
    tab = {}
    for c in CLASSES:
        for z in ZONES + ["all"]:
            k = Counter(f["dated_in_window"] for f in features if f["feature_type"] == c and (z == "all" or f["region_zone"] == z))
            tab["%s|%s" % (c, z)] = dict(rows=sum(k.values()), yes=k["yes"], no=k["no"], unknown=k["unknown"])
    wt = Counter(f["dated_in_window"] for f in features)
    return dict(units_assigned=len(reports), units_read=len(reports), units_not_read=0, units_held=0,
                reports_with_features=sum(1 for r in reports if int(r["n_feature_rows"]) > 0),
                reports_without_features=sum(1 for r in reports if int(r["n_feature_rows"]) == 0),
                reports_by_zone=dict(Counter(r["region_zone"] for r in reports)),
                reports_by_location=dict(Counter("map ref" if r["coordinate_source"].startswith("map ref") else "name only" for r in reports)),
                feature_rows=len(features), window=dict(yes=wt["yes"], no=wt["no"], unknown=wt["unknown"]),
                outside_region_rows=len(outside), class_zone=tab)


def summary_md(s):
    md = ["# Phase 4, part E, reader r2: summary tables (generated by scripts/build_reading_r2.py; do not edit)\n",
          "Units assigned and read: %d (T2 positions 61-135). Held: 0. Not read: 0." % s["units_read"],
          "Reports with eligible feature rows: %d; without: %d.\n" % (s["reports_with_features"], s["reports_without_features"]),
          "Feature rows: %d (dated in window: yes %d, no %d, unknown %d). Rows outside the region: %d.\n" % (
              s["feature_rows"], s["window"]["yes"], s["window"]["no"], s["window"]["unknown"], s["outside_region_rows"]),
          "## Feature rows by class and zone (rows: yes / no / unknown)\n",
          "| class | " + " | ".join(ZONES) + " | all |", "|---|" + "---|" * (len(ZONES) + 1)]
    for c in CLASSES:
        cells = []
        for z in ZONES + ["all"]:
            k = s["class_zone"]["%s|%s" % (c, z)]
            cells.append("%d (%d/%d/%d)" % (k["rows"], k["yes"], k["no"], k["unknown"]) if k["rows"] else "0")
        md.append("| %s | %s |" % (c, " | ".join(cells)))
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    out = OUT
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    f, r, o, s = build(out)
    print("reports %d, feature rows %d (yes %d / no %d / unknown %d), outside %d" % (
        len(r), len(f), s["window"]["yes"], s["window"]["no"], s["window"]["unknown"], len(o)))
