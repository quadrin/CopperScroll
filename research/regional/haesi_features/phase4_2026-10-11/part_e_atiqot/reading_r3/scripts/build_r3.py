#!/usr/bin/env python3
"""Phase 4, part E (ʿAtiqot), reader r3: build the coded tables for tier T2 order positions 136-208.

Reads (reading_r3/data): units/<unit_id>.json (hand coding, one file per unit), spans_r3.jsonl (span hashes and
quote checks made on the owner's Mac by verify_spans.py); ../pdfs_needed.csv (unit list, titles, authors, pages,
URLs); ../../downloads_2026-10-11.csv (PDF SHA-256); the frozen phase-2 plan (zones) and the phase-1 helpers
(grid conversion, places, region tags), unchanged.
Writes (reading_r3): reports.csv and features.csv (phase-2 column order), held.csv (part-E header),
not_read.csv, summary.json.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/reading_r3/scripts/build_r3.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
R3 = HERE.parent
DATA = R3 / "data"
PART = R3.parent
PHASE4 = PART.parent
LANE = PHASE4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
import common  # noqa: E402  (phase-2 helpers; also puts the phase-1 scripts on sys.path)
import geo  # noqa: E402
import build as p1  # noqa: E402

TIER = "T2"
POS_FIRST, POS_LAST = 136, 208
CLASSES = ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"]
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]
FEATURE_FIELDS = p1.FEATURE_FIELDS + ["region_zone", "dist_to_nearest_place_km", "feature_subtype", "exposure_at_freeze"]
REPORT_FIELDS = p1.REPORT_FIELDS + ["region_zone", "dist_to_nearest_place_km", "exposure_at_freeze", "tier"]
HELD_FIELDS = ["unit_id", "volume", "year", "first_page", "last_page", "title", "authors", "landing_url",
               "first_line_seen", "held_area", "held", "tier1_kh_almit", "protected_strip", "note"]
NOT_READ_FIELDS = ["unit_id", "tier", "order_position_in_tier", "reason"]
EXPOSURE = "unexposed at freeze"
SCREEN = "phase-4 part-E screen (pdfs_needed.csv)"


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
    rows = [r for r in read_csv(PART / "pdfs_needed.csv")
            if r["tier"] == TIER and POS_FIRST <= int(r["order_position_in_tier"]) <= POS_LAST]
    rows.sort(key=lambda r: int(r["order_position_in_tier"]))
    return rows


def load_units():
    out = {}
    for p in sorted((DATA / "units").glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        assert p.stem == d["unit_id"], p.name
        out[d["unit_id"]] = d
    return out


def load_spans():
    out = {}
    for line in (DATA / "spans_r3.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            out[d["unit"]] = d
    return out


def locate_ref(ref, places, params):
    r = geo.parse_ref(ref)
    lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
    d = geo.distances(lat, lon, places)
    return dict(grid=r["grid"], crs="EPSG:28191" if r["grid"] == "OIG" else "EPSG:2039", e=r["e"], n=r["n"],
                unit=r["unit_m"], lat=lat, lon=lon, dists=d, zone=common.zone_of(lat, lon, params) or "outside")


def no_loc(zone):
    return dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[], zone=zone or "unlocated")


def build(out_dir):
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    entries_by_place = defaultdict(list)
    for c in read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    plan1 = json.loads((LANE / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)
    pdf_sha = {r["file"][:-4]: r["sha256"] for r in read_csv(PHASE4 / "downloads_2026-10-11.csv")}

    assigned = assigned_units()
    units = load_units()
    spans = load_spans()
    ids = [r["unit_id"] for r in assigned]
    assert set(units) == set(ids), ("coding and assignment differ", set(units) ^ set(ids))
    assert set(spans) == set(ids), "spans_r3.jsonl and assignment differ"

    reports, features, outside = [], [], []
    for meta in assigned:
        uid = meta["unit_id"]
        u, sp = units[uid], spans[uid]
        assert u["status"] == "read", uid
        assert not any(q.startswith("NOT FOUND") for q in sp["quotes"]), uid
        assert len(sp["quotes"]) == len(u["features"]), uid
        pages = ("%s-%s" % (meta["first_page"], meta["last_page"])) if meta["first_page"] else ""
        access = ("owner's Mac PDF '%s.pdf' in ~/Downloads/IAA portal volumes/phase4 (SHA-256 %s), pdftotext -raw"
                  % (uid, pdf_sha[uid]))
        if u.get("map_ref") and not u.get("map_ref_unusable"):
            loc = locate_ref(u["map_ref"], places, params)
            src = "map ref (%s)" % u.get("grid", loc["grid"])
            assert loc["grid"] == u.get("grid", loc["grid"]), (uid, loc["grid"], u.get("grid"))
        else:
            loc = no_loc(u.get("name_zone"))
            src = "name only"
            if u.get("map_ref_unusable"):
                src += "; printed map reference unusable"
        d = loc["dists"]
        nearest, dist = (d[0][1], d[0][0]) if d else ("", None)
        w2 = [p for k, p in d if k <= 2.0]
        w5 = [p for k, p in d if k <= 5.0]
        regs = p1.regions_for(loc["lat"], loc["lon"], d, common.norm(meta["title"]).strip(), u, bx)
        if d:
            status = "within 2 km" if dist <= 2.0 else ("2-5 km" if dist <= 5.0 else "beyond 5 km")
        else:
            status = "name only (zone)" if u.get("name_zone") else "unlocated"
        frows = []
        for f, qres in zip(u["features"], sp["quotes"]):
            assert f["type"] in CLASSES, (uid, f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (uid, f["window"])
            assert len(f["quote"].split()) <= 12, (uid, f["quote"])
            fl, fsrc, fnear, fdist, fw2, fw5 = loc, src, nearest, dist, w2, w5
            if f.get("map_ref"):
                fl = locate_ref(f["map_ref"], places, params)
                fsrc = "feature map ref (%s)" % fl["grid"]
                fd = fl["dists"]
                fnear, fdist = fd[0][1], fd[0][0]
                fw2 = [p for k, p in fd if k <= 2.0]
                fw5 = [p for k, p in fd if k <= 5.0]
            pe = fnear if (fdist is not None and fdist <= 2.0) else ""
            row = dict(report_id=uid, url=meta["landing_url"], series="Atiqot", volume=meta["volume"],
                       year=meta["year"], pages=pages or u.get("pages", ""), site_name=meta["title"],
                       author=meta["authors"], permit=u.get("permit", ""),
                       map_ref_as_given=f.get("map_ref") or u.get("map_ref", ""), map_ref_used="",
                       grid=fl["grid"], crs_used=fl["crs"], easting_m=fl["e"], northing_m=fl["n"],
                       precision_m=fl["unit"], lat=fmt(fl["lat"], 5), lon=fmt(fl["lon"], 5), coordinate_source=fsrc,
                       feature_site=f.get("site", ""), nearest_place=fnear, distance_km=fmt(fdist, 3),
                       places_within_2km=";".join(fw2), places_within_5km=";".join(fw5), regions=";".join(regs),
                       feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                       dated_in_window=f["window"], excavated_or_surveyed=f.get("eos") or u["excavated_or_surveyed"],
                       quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(pe, [])) if pe else "",
                       protected_strip="no", screen=SCREEN, region_zone=fl["zone"],
                       dist_to_nearest_place_km=fmt(fdist, 3), feature_subtype=f.get("subtype", ""),
                       exposure_at_freeze=EXPOSURE)
            (frows if fl["zone"] in ZONES else outside).append(row)
        features.extend(frows)
        notes = ["language: %s" % u.get("lang", ""), "printed pages seen: %s" % u.get("pages", ""),
                 "quote checks: %s" % (",".join(sp["quotes"]) or "none"), u.get("notes", "")]
        reports.append(dict(report_id=uid, url=meta["landing_url"], access=access, series="Atiqot",
                            volume=meta["volume"], year=meta["year"], pages=pages or u.get("pages", ""),
                            site_name=meta["title"], author=meta["authors"], permit=u.get("permit", ""),
                            screen=SCREEN, toc_item="", map_ref_as_given=u.get("map_ref", ""), map_ref_used="",
                            grid=loc["grid"], crs_used=loc["crs"], lat=fmt(loc["lat"], 5), lon=fmt(loc["lon"], 5),
                            coordinate_source=src, nearest_place=nearest, distance_km=fmt(dist, 3),
                            places_within_2km=";".join(w2), places_within_5km=";".join(w5), regions=";".join(regs),
                            location_status=status, excavated_or_surveyed=u["excavated_or_surveyed"],
                            area_depth_stated="", n_feature_rows=len(frows),
                            feature_types=";".join(sorted({f["type"] for f in u["features"]})),
                            text_file="%s.raw.txt (outside the repository)" % uid, text_lines=u["text_lines"],
                            text_sha256=sp["sha256"], protected_strip="no",
                            location_note=u.get("location_note", ""), notes="; ".join(x for x in notes if x),
                            region_zone=loc["zone"], dist_to_nearest_place_km=fmt(dist, 3),
                            exposure_at_freeze=EXPOSURE,
                            tier="%s #%s" % (meta["tier"], meta["order_position_in_tier"])))
    assert not outside, ("feature outside the region", [r["report_id"] for r in outside])
    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    reports.sort(key=lambda r: r["report_id"])

    out_dir = Path(out_dir)
    write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    write_csv(out_dir / "held.csv", HELD_FIELDS, [])
    write_csv(out_dir / "not_read.csv", NOT_READ_FIELDS, [])

    by = defaultdict(Counter)
    for r in features:
        by[(r["feature_type"], r["region_zone"])][r["dated_in_window"]] += 1
    summary = {
        "reader": "r3", "tier": TIER, "positions": [POS_FIRST, POS_LAST],
        "units_assigned": len(assigned), "units_read": len(reports), "units_not_read": 0, "units_held": 0,
        "units_with_feature_rows": sum(1 for r in reports if r["n_feature_rows"]),
        "feature_rows": len(features),
        "report_zones": dict(sorted(Counter(r["region_zone"] for r in reports).items())),
        "rows_by_class_zone": {"%s|%s" % k: {w: v[w] for w in ("yes", "no", "unknown")}
                               for k, v in sorted(by.items())},
        "rows_by_window": dict(sorted(Counter(r["dated_in_window"] for r in features).items())),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    out = R3
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
    print(json.dumps(build(out), indent=1, ensure_ascii=False))
