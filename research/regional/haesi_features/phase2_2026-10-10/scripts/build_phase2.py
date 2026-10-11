#!/usr/bin/env python3
"""Build the HA-ESI phase-2 tables from the hand coding in data/coding_*.json.

Reads:  PLAN.md (frozen JSON block), data/coding_local_*.json, data/coding_online.json (if present),
        data/local_spans.csv, data/local_sources.csv, data/online_candidates.csv, data/online_status.csv,
        phase-1 ../reports.csv and ../features.csv (zone crosswalk only), W2B places and candidates (as phase 1).
Writes (lane folder): features.csv, reports.csv, online_screen.csv, phase1_zone_crosswalk.csv,
        looks_haesi_phase2.csv, summary.md, summary.json.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase2_2026-10-10/scripts/build_phase2.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
PHASE1 = LANE.parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402  (also puts phase-1 scripts on sys.path)
import geo  # noqa: E402
import build as p1  # noqa: E402  (phase-1 build: region boxes, W2B paths, field lists)

DATA = LANE / "data"
CLASSES = ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"]
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]
FEATURE_FIELDS = p1.FEATURE_FIELDS + ["region_zone", "dist_to_nearest_place_km", "feature_subtype", "exposure_at_freeze"]
REPORT_FIELDS = p1.REPORT_FIELDS + ["region_zone", "dist_to_nearest_place_km", "exposure_at_freeze", "tier"]
SCREEN_FIELDS = ["report_id", "volume", "year", "title", "url", "screen", "title_hits", "zone_by_title", "tier",
                 "order_position_in_tier", "status", "coded_report_id", "status_note"]
XWALK_FIELDS = ["table", "report_id", "feature_type", "lat", "lon", "coordinate_source", "region_zone",
                "dist_to_nearest_place_km", "dated_in_window", "note"]
LOCAL_FILE = {("ESI", "2"): "ESI02", ("ESI", "3"): "ESI03", ("ESI", "5"): "ESI05", ("ESI", "6"): "ESI06",
              ("ESI", "7–8"): "ESI07-08", ("ESI", "7-8"): "ESI07-08", ("ESI", "9"): "ESI09", ("ESI", "15"): "ESI15"}


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
    reps = []
    for p in sorted(DATA.glob("coding_*.json")):
        for r in json.loads(p.read_text(encoding="utf-8")):
            r["_source"] = "online" if p.name.startswith("coding_online") else "local"
            reps.append(r)
    reps.sort(key=lambda r: r["report_id"])
    ids = [r["report_id"] for r in reps]
    assert len(ids) == len(set(ids)), "duplicate report_id"
    return reps


def locate_ref(ref, places, params):
    r = geo.parse_ref(ref)
    lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
    d = geo.distances(lat, lon, places)
    return dict(grid=r["grid"], crs="EPSG:28191" if r["grid"] == "OIG" else "EPSG:2039", e=r["e"], n=r["n"],
                unit=r["unit_m"], lat=lat, lon=lon, dists=d, zone=common.zone_of(lat, lon, params) or "outside",
                swapped=r["swapped"])


def main(out_dir=LANE):
    out_dir = Path(out_dir)
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    pmeta = {p["place_id"]: p for p in places}
    entries_by_place = defaultdict(list)
    for c in read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    plan1 = json.loads((PHASE1 / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)
    spans = {r["report_id"]: r for r in read_csv(DATA / "local_spans.csv")}
    sources = {r["text_file"]: r for r in read_csv(DATA / "local_sources.csv")}
    cands = {r["report_id"]: r for r in read_csv(DATA / "online_candidates.csv")}
    status_path = DATA / "online_status.csv"
    ostatus = {r["report_id"]: r for r in read_csv(status_path)} if status_path.exists() else {}

    reps = load_coding()
    features, reports, looks, outside_feats = [], [], [], []
    for rep in reps:
        online = rep["_source"] == "online"
        if online:
            hid = rep["report_id"].split("-", 1)[1]
            url = "https://hadashot.iaa.org.il/report_detail_eng.aspx?id=%s" % hid
            access = "hadashot.iaa.org.il report page read in the owner's Chrome (one tab, one page at a time)"
            text_file, text_lines, text_sha = "online page main text (not stored)", "", rep["text_sha256"]
            screen = cands[hid]["screen"] if hid in cands else rep.get("screen", "")
            tier = cands[hid]["tier"] if hid in cands else ""
        else:
            tf = rep.get("text_file_id") or LOCAL_FILE[(rep["series"], rep["volume"])]
            src = sources[tf]
            url = src["portal_item_url"]
            access = "owner's Mac local PDF '%s' (SHA-256 %s), pdftotext -raw" % (src["local_file_name"], src["pdf_sha256"])
            sp = spans[rep["report_id"]]
            assert sp["text_lines"].replace(";", ",") == rep["text_lines"], rep["report_id"]
            text_file, text_lines, text_sha = tf + ".raw.txt (outside the repository)", rep["text_lines"], sp["text_sha256"]
            screen, tier = "S-LOC", "S-LOC (whole volume)"
        exposure = rep.get("exposure") or "unexposed at freeze"
        if rep.get("map_ref"):
            loc = locate_ref(rep["map_ref"], places, params)
            src_txt = "map ref"
        else:
            loc = dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[],
                       zone=rep.get("name_zone") or "unlocated", swapped=False)
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
        in_region = loc["zone"] in ZONES
        frows = []
        for f in rep["features"]:
            assert f["type"] in CLASSES, (rep["report_id"], f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (rep["report_id"], f["window"])
            fl, fsrc, fnear, fdist, fw2, fw5 = loc, src_txt, nearest, dist, w2, w5
            if f.get("map_ref"):
                fl = locate_ref(f["map_ref"], places, params)
                fsrc = "feature map ref"
                fd = fl["dists"]
                fnear, fdist = fd[0][1], fd[0][0]
                fw2 = [p for k, p in fd if k <= 2.0]
                fw5 = [p for k, p in fd if k <= 5.0]
            elif f.get("name_place"):
                fl = dict(loc, lat=None, lon=None, dists=[], e="", n="", unit="", grid="", crs="")
                fsrc, fnear, fdist, fw2, fw5 = "feature site name (%s)" % f["name_place"], f["name_place"], None, [], []
            place_for_entries = fnear if (fdist is not None and fdist <= 2.0) or (fdist is None and fnear) else ""
            row = dict(report_id=rep["report_id"], url=url, series=rep["series"], volume=rep["volume"], year=rep["year"],
                       pages=rep.get("pages", ""), site_name=rep["title"], author=rep.get("author", ""),
                       permit=rep.get("permit", ""), map_ref_as_given=f.get("map_ref") or rep.get("map_ref", ""),
                       map_ref_used="", grid=fl["grid"], crs_used=fl["crs"], easting_m=fl["e"], northing_m=fl["n"],
                       precision_m=fl["unit"], lat=fmt(fl["lat"], 5), lon=fmt(fl["lon"], 5), coordinate_source=fsrc,
                       feature_site=f.get("site", ""), nearest_place=fnear, distance_km=fmt(fdist, 3),
                       places_within_2km=";".join(fw2), places_within_5km=";".join(fw5), regions=";".join(regs),
                       feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                       dated_in_window=f["window"], excavated_or_surveyed=rep["excavated_or_surveyed"],
                       quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else "",
                       protected_strip=rep.get("protected_strip", "no"), screen=screen,
                       region_zone=fl["zone"], dist_to_nearest_place_km=fmt(fdist, 3),
                       feature_subtype=f.get("subtype", ""), exposure_at_freeze=exposure)
            (frows if fl["zone"] in ZONES else outside_feats).append(row)
        features.extend(frows)
        reports.append(dict(report_id=rep["report_id"], url=url, access=access, series=rep["series"], volume=rep["volume"],
                            year=rep["year"], pages=rep.get("pages", ""), site_name=rep["title"], author=rep.get("author", ""),
                            permit=rep.get("permit", ""), screen=screen, toc_item="", map_ref_as_given=rep.get("map_ref", ""),
                            map_ref_used="", grid=loc["grid"], crs_used=loc["crs"], lat=fmt(loc["lat"], 5),
                            lon=fmt(loc["lon"], 5), coordinate_source=src_txt, nearest_place=nearest,
                            distance_km=fmt(dist, 3), places_within_2km=";".join(w2), places_within_5km=";".join(w5),
                            regions=";".join(regs), location_status=status,
                            excavated_or_surveyed=rep["excavated_or_surveyed"], area_depth_stated=rep.get("area_depth", ""),
                            n_feature_rows=len(frows), feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file=text_file, text_lines=text_lines, text_sha256=text_sha,
                            protected_strip=rep.get("protected_strip", "no"),
                            location_note=rep.get("location_note", ""),
                            notes="; ".join(x for x in (rep.get("notes", ""), rep.get("tier1_record", "") and "TIER-1 RECORD: " + rep["tier1_record"]) if x),
                            region_zone=loc["zone"], dist_to_nearest_place_km=fmt(dist, 3), exposure_at_freeze=exposure,
                            tier=tier))
        # looks (phase-1 rule): places covered by the report's map reference or named by it
        if not in_region:
            continue
        covered = []
        if d:
            for k, p in d:
                rad = max(pmeta[p]["sigma_km"], 0.3) + loc["unit"] / 1000.0
                if k <= rad:
                    covered.append((p, "map ref, %s km (cover radius %.2f km)" % (fmt(k, 3), rad)))
        elif rep.get("name_place"):
            covered.append((rep["name_place"], "title names the place; no map reference"))
        for f in rep["features"]:
            if f.get("name_place") and f["name_place"] not in [c[0] for c in covered]:
                covered.append((f["name_place"], "feature site named in the text (%s); no map reference" % f.get("site", "")))
        for p, how in covered:
            here = [f for f in rep["features"] if f.get("name_place") == p or (not f.get("name_place") and not f.get("map_ref") and not how.startswith("feature site"))]
            kinds = ";".join("%s(%s)" % (f["type"], f["window"]) for f in here)
            for e in entries_by_place.get(p, []):
                looks.append(dict(entry_id=e, place_id=p, rep=rep, how=how, result="reported" if here else "silent",
                                  kinds=kinds, record_url=url))

    # online screen table
    order = defaultdict(list)
    for hid, c in cands.items():
        order[c["tier"]].append((c["order_key"], hid))
    pos = {}
    for t, lst in order.items():
        for i, (_, hid) in enumerate(sorted(lst), 1):
            pos[hid] = i
    coded = {r["report_id"].split("-", 1)[1]: r["report_id"] for r in reps if r["_source"] == "online"}
    srows = []
    for hid, c in cands.items():
        st = ostatus.get(hid)
        status = st["status"] if st else ("read" if hid in coded else "not read (time limit)")
        if hid in coded and not status.startswith("read"):
            raise AssertionError("coded report %s has status %s" % (hid, status))
        srows.append(dict(report_id=hid, volume=c["volume"], year=c["year"], title=c["title"], url=c["url"],
                          screen=c["screen"], title_hits=c["title_hits"], zone_by_title=c["zone_by_title"], tier=c["tier"],
                          order_position_in_tier=pos[hid], status=status, coded_report_id=coded.get(hid, ""),
                          status_note=st["note"] if st else ""))
    srows.sort(key=lambda r: (r["tier"], r["order_position_in_tier"]))

    # phase-1 crosswalk (phase-1 rows not re-coded; classes differ, see PLAN §5)
    xrows = []
    for t, path in (("reports", PHASE1 / "reports.csv"), ("features", PHASE1 / "features.csv")):
        for r in read_csv(path):
            if r["lat"]:
                lat, lon = float(r["lat"]), float(r["lon"])
                z = common.zone_of(lat, lon, params) or "outside"
                dd = fmt(geo.distances(lat, lon, places)[0][0], 3)
            else:
                z, dd = "", ""
            xrows.append(dict(table=t, report_id=r["report_id"], feature_type=r.get("feature_type", ""), lat=r["lat"],
                              lon=r["lon"], coordinate_source=r["coordinate_source"], region_zone=z or "unlocated (name only in phase 1)",
                              dist_to_nearest_place_km=dd, dated_in_window=r.get("dated_in_window", ""),
                              note="" if r["lat"] else "phase-1 row without coordinates; zone not assigned here"))

    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    reports.sort(key=lambda r: r["report_id"])
    with open(p1.LOOKS_REF, newline="", encoding="utf-8") as f:
        look_fields = next(csv.reader(f))
    looks.sort(key=lambda x: (x["rep"]["report_id"], x["place_id"], int("".join(ch for ch in x["entry_id"] if ch.isdigit())), x["entry_id"]))
    lrows = []
    for i, lk in enumerate(looks, 1):
        rep = lk["rep"]
        rec = "%s, %s %s (%s)%s, ‘%s’" % (rep.get("author", ""), rep["series"], rep["volume"], rep["year"],
                                         (" p. " + rep["pages"]) if rep.get("pages") else "", rep["title"])
        lrows.append({
            "look_id": "H2-%03d" % i, "entry_id": lk["entry_id"], "place_id": lk["place_id"], "relation_id": "HAESI-COVER",
            "required_feature": "any HA-ESI phase-2 coded feature class at the place (phase2 PLAN.md §5)",
            "reading_condition": "", "placement_relevant": "yes", "record": rec,
            "record_key": "%s %s %s" % (rep["series"], rep["volume"], rep.get("pages", "") or lk["record_url"]),
            "record_id": rep["report_id"], "lineage": "HA-ESI %s%s" % (rep["report_id"], (" (permit %s)" % rep["permit"]) if rep.get("permit") else ""),
            "looked_at": "%s; %s" % (rep["excavated_or_surveyed"], lk["how"]),
            "coverage": "", "coverage_basis": "UNKNOWN: the report gives no target-area fraction",
            "p_recognise": "", "p_recognise_basis": "UNKNOWN: not estimated here",
            "p_report": "", "p_report_basis": "UNKNOWN: not estimated here",
            "p_survive": "", "p_survive_basis": "UNKNOWN: not estimated here",
            "result": lk["result"], "result_basis": "EVIDENCE", "satisfies_requirement": "unknown", "counted_via": "",
            "project_use": "research/regional/haesi_features/phase2_2026-10-10/features.csv",
            "notes": ("coded classes (dated_in_window): " + lk["kinds"]) if lk["kinds"] else "no coded feature class at this place in this report",
        })

    write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    write_csv(out_dir / "online_screen.csv", SCREEN_FIELDS, srows)
    write_csv(out_dir / "phase1_zone_crosswalk.csv", XWALK_FIELDS, xrows)
    write_csv(out_dir / "looks_haesi_phase2.csv", look_fields, lrows)
    summ = summarize(features, reports, srows, xrows, outside_feats, lrows)
    (out_dir / "summary.json").write_text(json.dumps(summ["json"], ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "summary.md").write_text(summ["md"], encoding="utf-8")
    print("reports %d, feature rows %d (outside region %d), screen rows %d, crosswalk %d, looks %d" % (
        len(reports), len(features), len(outside_feats), len(srows), len(xrows), len(lrows)))


def summarize(features, reports, srows, xrows, outside_feats, lrows):
    md = ["# HA-ESI phase 2 summary tables (generated by scripts/build_phase2.py; do not edit)\n"]
    by_src = Counter(("online" if r["series"] == "HA-ESI" else "local") for r in reports)
    in_reg = [r for r in reports if r["region_zone"] in ZONES]
    md.append("Reports read and coded: %d (local PDFs %d, online %d); in the region %d; outside the region or unlocated %d." % (
        len(reports), by_src["local"], by_src["online"], len(in_reg), len(reports) - len(in_reg)))
    md.append("Reports in the region with no eligible feature: %d.\n" % sum(1 for r in in_reg if r["n_feature_rows"] == 0))
    wt = Counter(f["dated_in_window"] for f in features)
    md.append("Feature rows in the region: %d (dated in window: yes %d, no %d, unknown %d). Rows outside the region (feature map ref): %d.\n" % (
        len(features), wt["yes"], wt["no"], wt["unknown"], len(outside_feats)))
    md.append("## Feature rows by class and zone (yes / no / unknown)\n")
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
    md.append("\n## Reports read by zone and source\n")
    md.append("| zone | local PDFs | online | rows |")
    md.append("|---|---|---|---|")
    for z in ZONES + ["outside", "unlocated"]:
        rr = [r for r in reports if r["region_zone"] == z]
        if not rr:
            continue
        md.append("| %s | %d | %d | %d |" % (z, sum(1 for r in rr if r["series"] != "HA-ESI"), sum(1 for r in rr if r["series"] == "HA-ESI"),
                                         sum(int(r["n_feature_rows"]) for r in rr)))
    md.append("\n## Online screen status by tier\n")
    st = defaultdict(Counter)
    for r in srows:
        st[r["tier"]][r["status"].split(":")[0]] += 1
    statuses = sorted({s for c in st.values() for s in c})
    md.append("| tier | candidates | " + " | ".join(statuses) + " |")
    md.append("|---|---|" + "---|" * len(statuses))
    for t in sorted(st):
        md.append("| %s | %d | %s |" % (t, sum(st[t].values()), " | ".join(str(st[t][s]) for s in statuses)))
    md.append("\n## Dated-in-window rows\n")
    md.append("| report_id | zone | nearest place (km) | class | subtype | period as given |")
    md.append("|---|---|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s | %s | %s |" % (f["report_id"], f["region_zone"],
                      ("%s (%s)" % (f["nearest_place"], f["distance_km"])) if f["distance_km"] else (f["nearest_place"] or "name only"),
                      f["feature_type"], f["feature_subtype"].replace("|", "/"), f["period_as_given"].replace("|", "/")))
    xz = Counter((r["table"], r["region_zone"]) for r in xrows)
    md.append("\n## Phase-1 rows by zone (crosswalk; phase-1 classes, not re-coded)\n")
    md.append("| table | " + " | ".join(ZONES + ["outside", "unlocated (name only in phase 1)"]) + " |")
    md.append("|---|" + "---|" * (len(ZONES) + 2))
    for t in ("reports", "features"):
        md.append("| %s | %s |" % (t, " | ".join(str(xz[(t, z)]) for z in ZONES + ["outside", "unlocated (name only in phase 1)"])))
    md.append("\nlooks_haesi_phase2.csv rows: %d (reported %d, silent %d).\n" % (
        len(lrows), sum(1 for r in lrows if r["result"] == "reported"), sum(1 for r in lrows if r["result"] == "silent")))
    js = dict(reports=len(reports), reports_by_source=dict(by_src), reports_in_region=len(in_reg),
              feature_rows=len(features), window=dict(wt), class_zone=js_tab,
              rows_by_zone={z: zt[z] for z in ZONES}, outside_feature_rows=len(outside_feats),
              online_status={t: dict(c) for t, c in st.items()},
              phase1_crosswalk={"%s|%s" % k: v for k, v in sorted(xz.items())}, looks=len(lrows))
    return dict(md="\n".join(md) + "\n", json=js)


if __name__ == "__main__":
    out = LANE
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
