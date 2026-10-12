#!/usr/bin/env python3
"""Phase 4 part I (ADAJ): build the part-I tables from the screen inputs and the hand coding.

Reads (part_i_adaj/data):
  portal_toc.csv        every table-of-contents title on the DoA portal for ADAJ 1-62 (English and Arabic parts)
  portal_chapters.csv   portal chapter metadata (pages, authors, chapter PDF) for ADAJ 1-17 and the later candidates
  early_headings.csv    site headings and news paragraphs inside the news and round-up sections of ADAJ 1-12/13
  screen_decisions.csv  the decision for every gazetteer hit and every hand addition (with reason)
  coding.json           the coded units (phase-2 coding format)
  spans.csv             for each coded unit: PDF, PDF pages, printed pages, SHA-256 of the whitespace-collapsed
                        OCR text read, quotes checked (made in the scratch folder by verify_spans.py)
  held.csv              held and protected units (citation and first line only)
  pdf_sources.csv       the PDFs fetched, with SHA-256
Writes (part_i_adaj): reports.csv, features.csv (phase-2 column order), screen.csv, summary.md, summary.json.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_i_adaj/scripts/build_part_i.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
DATA = PART / "data"
LANE = PART.parent.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
sys.path.insert(0, str(HERE))
import build_phase2 as b2  # noqa: E402  (phase-2 fields, locate_ref, fmt; loads common, geo and phase-1 build)
import screen_titles  # noqa: E402

common, geo, p1 = b2.common, b2.geo, b2.p1
CLASSES, ZONES = b2.CLASSES, b2.ZONES
SERIES = "ADAJ"
PORTAL = "https://publication.doa.gov.jo"
SCREEN_FIELDS = ["screen_key", "source", "volume", "year", "chapter_id", "printed_pages", "title", "author",
                 "title_hits", "decision", "zone", "unit_id", "tier", "order_position_in_tier", "status",
                 "n_feature_rows", "note"]
HELD_FIELDS = ["unit_id", "volume", "year", "printed_pages", "title", "author", "area", "kind", "first_line",
               "citation", "note"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def unit_sha(uid):
    return hashlib.sha256(uid.encode("utf-8")).hexdigest()


def tier_of(zone, title, decided_tier=""):
    if decided_tier:
        return decided_tier
    if zone in ("Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT"):
        return "T1"
    if zone == "Z4_JERUSALEM_HILLS":
        return "T3" if common.norm(title).strip().startswith("jerusalem") else "T2"
    return ""


def load_coding():
    p = DATA / "coding.json"
    reps = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    ids = [r["report_id"] for r in reps]
    assert len(ids) == len(set(ids)), "duplicate report_id"
    return reps


def screen_rows():
    pats = screen_titles.patterns()
    dec = {(d["source"], d["key"]): d for d in read_csv(DATA / "screen_decisions.csv")}
    chap = {c["chapter_id"]: c for c in read_csv(DATA / "portal_chapters.csv")}
    rows = []
    for r in read_csv(DATA / "portal_toc.csv"):
        rows.append(dict(screen_key="toc:%s" % r["chapter_id"], source="portal TOC (%s)" % r["lang"], volume=r["volume"],
                         year=r["year"], chapter_id=r["chapter_id"],
                         printed_pages="", title=r["title"], author=chap.get(r["chapter_id"], {}).get("authors", ""),
                         _dkey=("toc", r["chapter_id"])))
    for r in read_csv(DATA / "early_headings.csv"):
        rows.append(dict(screen_key="head:%s" % r["heading_id"], source="%s heading" % r["section"], volume=r["volume"],
                         year=r["year"], chapter_id=r["chapter_id"], printed_pages=r["printed_page"], title=r["title"],
                         author=r.get("author", ""), _dkey=("head", r["heading_id"])))
    out = []
    for r in rows:
        h = screen_titles.hits_for(r["title"], pats)
        r["title_hits"] = ";".join("%s:%s" % (z, "|".join(v)) for z, v in sorted(h.items()))
        d = dec.get(r["_dkey"])
        if d:
            r["decision"], r["zone"], r["unit_id"], r["note"] = d["decision"], d["zone"], d["unit_id"], d["reason"]
            r["_tier"] = d.get("tier", "")
        else:
            assert not h, ("gazetteer hit without a decision", r["_dkey"], r["title"])
            r["decision"], r["zone"], r["unit_id"], r["note"], r["_tier"] = (
                "outside region (title names no region place)", "", "", "", "")
        out.append(r)
    return out


def assign_order(srows):
    """Tier and position (ascending SHA-256 of unit id) for every in-region candidate unit."""
    units = {}
    for r in srows:
        if r["decision"].startswith(("candidate", "held", "protected")) and r["unit_id"]:
            units.setdefault(r["unit_id"], tier_of(r["zone"], r["title"], r.get("_tier", "")))
    pos = {}
    for t in ("T1", "T2", "T3"):
        ids = sorted((u for u, tt in units.items() if tt == t), key=unit_sha)
        for i, u in enumerate(ids, 1):
            pos[u] = (t, i)
    return pos


def build(reps, places, params):
    spans = {s["report_id"]: s for s in read_csv(DATA / "spans.csv")}
    srcs = {s["pdf_file"]: s for s in read_csv(DATA / "pdf_sources.csv")}
    plan1 = json.loads((b2.PHASE1 / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)
    entries_by_place = defaultdict(list)
    for c in b2.read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]),
                                     key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    features, reports, outside = [], [], []
    for rep in reps:
        sp = spans[rep["report_id"]]
        src = srcs[sp["pdf_file"]]
        url = PORTAL + src["url_path"]
        access = ("DoA portal PDF fetched from the workspace (SHA-256 %s); no text layer: tesseract 5 OCR (eng, 250 dpi), "
                  "PDF pages %s" % (src["sha256"], sp["pdf_pages"]))
        exposure = rep.get("exposure") or "unexposed at freeze"
        if rep.get("map_ref"):
            loc = b2.locate_ref(rep["map_ref"], places, params)
            src_txt = "map ref (Palestine Grid, EPSG:28191)"
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
                fsrc = "feature map ref (Palestine Grid, EPSG:28191)"
                fd = fl["dists"]
                fnear, fdist = fd[0][1], fd[0][0]
                fw2 = [p for k, p in fd if k <= 2.0]
                fw5 = [p for k, p in fd if k <= 5.0]
            elif f.get("name_zone"):
                fl = dict(loc, lat=None, lon=None, dists=[], e="", n="", unit="", grid="", crs="", zone=f["name_zone"])
                fsrc, fnear, fdist, fw2, fw5 = "feature site name only", f.get("name_place", ""), None, [], []
            place_for_entries = fnear if (fdist is not None and fdist <= 2.0) or (fdist is None and fnear) else ""
            row = dict(report_id=rep["report_id"], url=url, series=SERIES, volume=rep["volume"], year=rep["year"],
                       pages=rep["pages"], site_name=rep["title"], author=rep.get("author", ""), permit="",
                       map_ref_as_given=f.get("map_ref") or rep.get("map_ref", ""), map_ref_used="",
                       grid=fl["grid"], crs_used=fl["crs"], easting_m=fl["e"], northing_m=fl["n"], precision_m=fl["unit"],
                       lat=b2.fmt(fl["lat"], 5), lon=b2.fmt(fl["lon"], 5), coordinate_source=fsrc,
                       feature_site=f.get("site", ""), nearest_place=fnear, distance_km=b2.fmt(fdist, 3),
                       places_within_2km=";".join(fw2), places_within_5km=";".join(fw5), regions=";".join(regs),
                       feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                       dated_in_window=f["window"], excavated_or_surveyed=rep["excavated_or_surveyed"],
                       quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else "",
                       protected_strip=rep.get("protected_strip", "no"), screen=rep["screen"],
                       region_zone=fl["zone"], dist_to_nearest_place_km=b2.fmt(fdist, 3),
                       feature_subtype=f.get("subtype", ""), exposure_at_freeze=exposure)
            (frows if fl["zone"] in ZONES else outside).append(row)
        features.extend(frows)
        reports.append(dict(report_id=rep["report_id"], url=url, access=access, series=SERIES, volume=rep["volume"],
                            year=rep["year"], pages=rep["pages"], site_name=rep["title"], author=rep.get("author", ""),
                            permit="", screen=rep["screen"], toc_item=rep.get("toc_item", ""),
                            map_ref_as_given=rep.get("map_ref", ""), map_ref_used="", grid=loc["grid"],
                            crs_used=loc["crs"], lat=b2.fmt(loc["lat"], 5), lon=b2.fmt(loc["lon"], 5),
                            coordinate_source=src_txt, nearest_place=nearest, distance_km=b2.fmt(dist, 3),
                            places_within_2km=";".join(w2), places_within_5km=";".join(w5), regions=";".join(regs),
                            location_status=status, excavated_or_surveyed=rep["excavated_or_surveyed"],
                            area_depth_stated=rep.get("area_depth", ""), n_feature_rows=len(frows),
                            feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file="OCR of %s (outside the repository)" % sp["pdf_file"],
                            text_lines="PDF pp. %s" % sp["pdf_pages"], text_sha256=sp["text_sha256"],
                            protected_strip=rep.get("protected_strip", "no"),
                            location_note=rep.get("location_note", ""), notes=rep.get("notes", ""),
                            region_zone=loc["zone"], dist_to_nearest_place_km=b2.fmt(dist, 3),
                            exposure_at_freeze=exposure, tier=rep["tier"]))
    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    reports.sort(key=lambda r: r["report_id"])
    return features, reports, outside


def finish_screen(srows, pos, reps, reports, held):
    coded = {r["report_id"] for r in reps}
    nrows = {r["report_id"]: r["n_feature_rows"] for r in reports}
    held_ids = {h["unit_id"] for h in held}
    for r in srows:
        u = r["unit_id"]
        t, i = pos.get(u, ("", ""))
        r["tier"], r["order_position_in_tier"] = t, i
        if r["decision"].startswith("candidate"):
            if u in coded:
                r["status"] = "read and coded"
                r["n_feature_rows"] = nrows[u]
            elif u in held_ids:
                r["status"] = "held (citation and first line only)"
            else:
                r["status"] = "not read (time limit)"
        elif r["decision"].startswith(("held", "protected")):
            assert u in held_ids, u
            r["status"] = r["decision"].split(":")[0]
        else:
            r["status"] = "not coded"
    srows.sort(key=lambda r: (r["screen_key"].split(":")[0], int(r["chapter_id"] or 0), r["screen_key"]))
    return srows


def summarize(features, reports, srows, outside, held):
    md = ["# Phase 4 part I (ADAJ): summary (generated by scripts/build_part_i.py; do not edit)\n"]
    stc = Counter(r["status"] for r in srows)
    md.append("Screen rows: %d. Status: %s." % (len(srows), ", ".join("%s %d" % (k, v) for k, v in sorted(stc.items()))))
    cand = [r for r in srows if r["decision"].startswith("candidate")]
    units = sorted({r["unit_id"] for r in cand})
    md.append("Candidate units: %d. Held or protected units: %d." % (len(units), len(held)))
    in_reg = [r for r in reports if r["region_zone"] in ZONES]
    md.append("Units coded: %d; in the region %d; with no eligible feature %d.\n" % (
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
    md.append("\n## Feature rows by zone (yes / no / unknown)\n")
    md.append("| zone | rows | yes | no | unknown |")
    md.append("|---|---|---|---|---|")
    js_zone = {}
    for z in ZONES:
        k = Counter(f["dated_in_window"] for f in features if f["region_zone"] == z)
        n = sum(k.values())
        js_zone[z] = dict(rows=n, yes=k["yes"], no=k["no"], unknown=k["unknown"])
        md.append("| %s | %d | %d | %d | %d |" % (z, n, k["yes"], k["no"], k["unknown"]))
    md.append("\n## Dated-in-window rows\n")
    md.append("| report_id | class | subtype | period as given |")
    md.append("|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s |" % (f["report_id"], f["feature_type"], f["feature_subtype"].replace("|", "/"),
                                              f["period_as_given"].replace("|", "/")))
    js = dict(screen_rows=len(srows), status=dict(sorted(stc.items())), candidate_units=len(units),
              held_units=len(held), units_coded=len(reports), units_in_region=len(in_reg),
              feature_rows=len(features), window=dict(sorted(wt.items())), by_class=js_tab, by_zone=js_zone,
              outside_feature_rows=len(outside))
    return "\n".join(md) + "\n", js


def main(out_dir=PART):
    out_dir = Path(out_dir)
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    srows = screen_rows()
    pos = assign_order(srows)
    reps = load_coding()
    for r in reps:
        assert r["report_id"] in pos, r["report_id"]
        r["tier"] = pos[r["report_id"]][0]
    held = read_csv(DATA / "held.csv")
    features, reports, outside = build(reps, places, params)
    srows = finish_screen(srows, pos, reps, reports, held)
    b2.write_csv(out_dir / "features.csv", b2.FEATURE_FIELDS, features)
    b2.write_csv(out_dir / "reports.csv", b2.REPORT_FIELDS, reports)
    b2.write_csv(out_dir / "screen.csv", SCREEN_FIELDS, srows)
    b2.write_csv(out_dir / "held.csv", HELD_FIELDS, sorted(held, key=lambda h: h["unit_id"]))
    md, js = summarize(features, reports, srows, outside, held)
    (out_dir / "summary.md").write_text(md, encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(js, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                          encoding="utf-8")
    print("screen rows %d, units coded %d, feature rows %d (outside region %d), held %d" % (
        len(srows), len(reports), len(features), len(outside), len(held)))


if __name__ == "__main__":
    out = PART
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
