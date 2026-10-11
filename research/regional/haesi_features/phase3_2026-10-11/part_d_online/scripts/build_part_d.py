#!/usr/bin/env python3
"""Build the phase-3 part-D tables (online tier T3, positions 81-662) from the hand coding.

Reads:  ../data/coding_online_t3.json (hand coding, phase-2 coding_online.json format),
        ../data/online_status_t3.csv (non-coded statuses, optional),
        phase-2 online_screen.csv (frozen T3 order and positions) and data/online_candidates.csv,
        the phase-2 plan parameters, grid conversion and places (through the phase-2 and phase-1 scripts, unchanged).
Writes (part_d_online/): features.csv, reports.csv (phase-2 column order exactly), screen.csv, summary.md, summary.json.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase3_2026-10-11/part_d_online/scripts/build_part_d.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
PHASE2 = PART.parent.parent / "phase2_2026-10-10"
sys.path.insert(0, str(PHASE2 / "scripts"))
import build_phase2 as b2  # noqa: E402  (phase-2 build: fields, locate_ref, fmt; also loads common, geo, phase-1 build)

common, geo, p1 = b2.common, b2.geo, b2.p1
DATA = PART / "data"
FIRST, LAST = 81, 662
CLASSES, ZONES = b2.CLASSES, b2.ZONES
SCREEN_FIELDS = ["report_id", "volume", "year", "title", "url", "tier", "order_position_in_tier", "status",
                 "coded_report_id", "n_feature_rows", "status_note"]


def t3_queue():
    rows = [r for r in b2.read_csv(PHASE2 / "online_screen.csv") if r["tier"] == "T3"]
    rows.sort(key=lambda r: int(r["order_position_in_tier"]))
    return [r for r in rows if FIRST <= int(r["order_position_in_tier"]) <= LAST]


def load_coding():
    p = DATA / "coding_online_t3.json"
    reps = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    ids = [r["report_id"] for r in reps]
    assert len(ids) == len(set(ids)), "duplicate report_id"
    return reps


def build_rows(reps, places, params):
    """Phase-2 row logic (build_phase2.main), online branch only; no looks rows."""
    cands = {r["report_id"]: r for r in b2.read_csv(PHASE2 / "data" / "online_candidates.csv")}
    plan1 = json.loads((b2.PHASE1 / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)
    entries_by_place = defaultdict(list)
    for c in b2.read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    features, reports, outside = [], [], []
    for rep in reps:
        hid = rep["report_id"].split("-", 1)[1]
        url = "https://hadashot.iaa.org.il/report_detail_eng.aspx?id=%s" % hid
        access = "hadashot.iaa.org.il report page read in the owner's Chrome (one tab, one page at a time)"
        screen, tier = cands[hid]["screen"], cands[hid]["tier"]
        assert tier == "T3", rep["report_id"]
        exposure = rep.get("exposure") or "unexposed at freeze"
        if rep.get("map_ref"):
            loc = b2.locate_ref(rep["map_ref"], places, params)
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
        frows = []
        for f in rep["features"]:
            assert f["type"] in CLASSES, (rep["report_id"], f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (rep["report_id"], f["window"])
            fl, fsrc, fnear, fdist, fw2, fw5 = loc, src_txt, nearest, dist, w2, w5
            if f.get("map_ref"):
                fl = b2.locate_ref(f["map_ref"], places, params)
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
                       precision_m=fl["unit"], lat=b2.fmt(fl["lat"], 5), lon=b2.fmt(fl["lon"], 5), coordinate_source=fsrc,
                       feature_site=f.get("site", ""), nearest_place=fnear, distance_km=b2.fmt(fdist, 3),
                       places_within_2km=";".join(fw2), places_within_5km=";".join(fw5), regions=";".join(regs),
                       feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                       dated_in_window=f["window"], excavated_or_surveyed=rep["excavated_or_surveyed"],
                       quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else "",
                       protected_strip=rep.get("protected_strip", "no"), screen=screen,
                       region_zone=fl["zone"], dist_to_nearest_place_km=b2.fmt(fdist, 3),
                       feature_subtype=f.get("subtype", ""), exposure_at_freeze=exposure)
            (frows if fl["zone"] in ZONES else outside).append(row)
        features.extend(frows)
        reports.append(dict(report_id=rep["report_id"], url=url, access=access, series=rep["series"], volume=rep["volume"],
                            year=rep["year"], pages=rep.get("pages", ""), site_name=rep["title"], author=rep.get("author", ""),
                            permit=rep.get("permit", ""), screen=screen, toc_item="", map_ref_as_given=rep.get("map_ref", ""),
                            map_ref_used="", grid=loc["grid"], crs_used=loc["crs"], lat=b2.fmt(loc["lat"], 5),
                            lon=b2.fmt(loc["lon"], 5), coordinate_source=src_txt, nearest_place=nearest,
                            distance_km=b2.fmt(dist, 3), places_within_2km=";".join(w2), places_within_5km=";".join(w5),
                            regions=";".join(regs), location_status=status,
                            excavated_or_surveyed=rep["excavated_or_surveyed"], area_depth_stated=rep.get("area_depth", ""),
                            n_feature_rows=len(frows), feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file="online page main text (not stored)", text_lines="", text_sha256=rep["text_sha256"],
                            protected_strip=rep.get("protected_strip", "no"),
                            location_note=rep.get("location_note", ""), notes=rep.get("notes", ""),
                            region_zone=loc["zone"], dist_to_nearest_place_km=b2.fmt(dist, 3), exposure_at_freeze=exposure,
                            tier=tier))
    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    reports.sort(key=lambda r: r["report_id"])
    return features, reports, outside


def screen_rows(queue, reps, reports):
    coded = {r["report_id"].split("-", 1)[1]: r["report_id"] for r in reps}
    zone = {r["report_id"]: r["region_zone"] for r in reports}
    nrows = {r["report_id"]: r["n_feature_rows"] for r in reports}
    sp = DATA / "online_status_t3.csv"
    st = {r["report_id"]: r for r in b2.read_csv(sp)} if sp.exists() else {}
    out = []
    for q in queue:
        hid = q["report_id"]
        if hid in st:
            assert hid not in coded, hid
            status, note = st[hid]["status"], st[hid]["note"]
        elif hid in coded:
            status = "read" if zone[coded[hid]] in ZONES else "read: map ref outside region"
            note = ""
        else:
            status, note = "not read (time limit)", ""
        out.append(dict(report_id=hid, volume=q["volume"], year=q["year"], title=q["title"], url=q["url"], tier="T3",
                        order_position_in_tier=q["order_position_in_tier"], status=status,
                        coded_report_id=coded.get(hid, ""), n_feature_rows=nrows.get(coded.get(hid), ""), status_note=note))
    return out


def summarize(features, reports, srows, outside):
    md = ["# HA-ESI phase 3, part D (online T3, positions 81-662): summary (generated by scripts/build_part_d.py; do not edit)\n"]
    stc = Counter(r["status"] for r in srows)
    read_pos = [int(r["order_position_in_tier"]) for r in srows if r["status"].startswith("read")]
    md.append("T3 positions in scope: %d. Status: %s." % (len(srows), ", ".join("%s %d" % (k, v) for k, v in sorted(stc.items()))))
    if read_pos:
        md.append("Positions read: %d to %d (contiguous: %s)." % (min(read_pos), max(read_pos),
                  "yes" if sorted(read_pos) == list(range(min(read_pos), max(read_pos) + 1)) else "no"))
    in_reg = [r for r in reports if r["region_zone"] in ZONES]
    md.append("Reports coded: %d; in the region %d; with no eligible feature %d.\n" % (
        len(reports), len(in_reg), sum(1 for r in in_reg if r["n_feature_rows"] == 0)))
    wt = Counter(f["dated_in_window"] for f in features)
    md.append("Feature rows in the region: %d (dated in window: yes %d, no %d, unknown %d). Rows outside the region: %d.\n" % (
        len(features), wt["yes"], wt["no"], wt["unknown"], len(outside)))
    md.append("## Feature rows by class (yes / no / unknown)\n")
    md.append("| class | rows | yes | no | unknown |")
    md.append("|---|---|---|---|---|")
    js_tab = {}
    for c in CLASSES:
        k = Counter(f["dated_in_window"] for f in features if f["feature_type"] == c)
        n = sum(k.values())
        js_tab[c] = dict(rows=n, yes=k["yes"], no=k["no"], unknown=k["unknown"])
        md.append("| %s | %d | %d | %d | %d |" % (c, n, k["yes"], k["no"], k["unknown"]))
    md.append("| all | %d | %d | %d | %d |" % (len(features), wt["yes"], wt["no"], wt["unknown"]))
    zt = Counter(f["region_zone"] for f in features)
    md.append("\nRows by zone: " + ", ".join("%s %d" % (z, zt[z]) for z in ZONES) + ".\n")
    md.append("## Dated-in-window rows\n")
    md.append("| report_id | nearest place (km) | class | subtype | period as given |")
    md.append("|---|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s | %s |" % (f["report_id"],
                      ("%s (%s)" % (f["nearest_place"], f["distance_km"])) if f["distance_km"] else (f["nearest_place"] or "name only"),
                      f["feature_type"], f["feature_subtype"].replace("|", "/"), f["period_as_given"].replace("|", "/")))
    js = dict(positions_in_scope=len(srows), status=dict(stc), reports=len(reports), reports_in_region=len(in_reg),
              feature_rows=len(features), window=dict(wt), by_class=js_tab, rows_by_zone={z: zt[z] for z in ZONES},
              outside_feature_rows=len(outside),
              positions_read=[min(read_pos), max(read_pos)] if read_pos else None)
    return "\n".join(md) + "\n", js


def main(out_dir=PART):
    out_dir = Path(out_dir)
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    queue = t3_queue()
    assert len(queue) == LAST - FIRST + 1
    reps = load_coding()
    qids = {q["report_id"] for q in queue}
    for r in reps:
        assert r["report_id"].split("-", 1)[1] in qids, r["report_id"]
    features, reports, outside = build_rows(reps, places, params)
    srows = screen_rows(queue, reps, reports)
    b2.write_csv(out_dir / "features.csv", b2.FEATURE_FIELDS, features)
    b2.write_csv(out_dir / "reports.csv", b2.REPORT_FIELDS, reports)
    b2.write_csv(out_dir / "screen.csv", SCREEN_FIELDS, srows)
    md, js = summarize(features, reports, srows, outside)
    (out_dir / "summary.md").write_text(md, encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(js, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("reports %d, feature rows %d (outside region %d), screen rows %d" % (len(reports), len(features), len(outside), len(srows)))


if __name__ == "__main__":
    out = PART
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
