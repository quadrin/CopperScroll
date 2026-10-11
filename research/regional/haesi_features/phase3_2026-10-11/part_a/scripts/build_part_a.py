#!/usr/bin/env python3
"""Build the HA-ESI phase-3 part-A tables (HA Hebrew series 1961-1979, local portal PDFs).

Rules: phase-2 frozen plan (../../phase2_2026-10-10/PLAN.md, JSON block) with amendments A1-A4; phase-3 scope freeze
(../PLAN.md). Coordinates, zones, distances and field lists are the phase-2 ones (build_phase2.py, common.py and the
phase-1 geo.py, unchanged). Additions for part A: a report may carry name_zone "MULTI" (a regional survey spanning
zones) with a zone on each feature (feature name_zone), and every screen decision is joined to the portal tables of
contents and to the phase-1 screen candidates.

Reads (part_a/data): coding_*.json, local_spans.csv, local_sources.csv, portal_toc_items.csv, volumes.csv,
  heading_signals.csv, screen_decisions_b*.tsv; ../../data/screen_candidates.csv; W2B places (as phase 1).
Writes (part_a/ or --out DIR): reports.csv, features.csv (phase-2 column order), screen.csv, candidates_checkoff.csv,
  summary.md, summary.json.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase3_2026-10-11/part_a/scripts/build_part_a.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
P3 = PART.parent
LANE = P3.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(P2 / "scripts"))
sys.path.insert(0, str(HERE))
import build_phase2 as p2  # noqa: E402  (phase-2 builder: field lists, locate_ref, csv helpers)
import common  # noqa: E402
import geo  # noqa: E402
import screen_titles  # noqa: E402

p1 = p2.p1
DATA = PART / "data"
ZONES = p2.ZONES
CLASSES = p2.CLASSES
FEATURE_FIELDS = p2.FEATURE_FIELDS
REPORT_FIELDS = p2.REPORT_FIELDS
READ_DECISIONS = {"READ", "READ0", "TIER1"}
DECISIONS = {"READ": "read and coded, features found", "READ0": "read and coded, no eligible feature",
             "TIER1": "Tier-1 record: extraction first, then coded", "COMPOSITE": "several notes under one heading",
             "OUT_TITLE": "outside the region by title or heading", "OUT_REF": "outside the region by map reference",
             "OUT_NAMESAKE": "namesake of a gazetteer place, outside the region", "NONFIELD": "not a field report",
             "HELD": "held cave area (plan section 7): citation and first lines only",
             "STRIP_CHECK": "possible Tell es-Sultan north strip: citation only",
             "BORDER": "on or just beyond a box edge; listed, not coded", "UNLOC": "location not established; listed, not coded"}
SCREEN_FIELDS = ["vol_file", "volume", "year", "item_url", "toc_n", "title", "author", "pages", "heading_pdf_page",
                 "heading_located", "title_hits_strict", "title_hits_prefix", "map_refs_in_item_text",
                 "map_ref_zones", "body_gazetteer_hits_by_zone", "phase1_candidate", "decision", "decision_source",
                 "reason", "report_ids"]
CHECK_FIELDS = ["item_key", "screen", "volume_title", "year", "pages", "toc_text", "groups", "matched_terms", "vol_file",
                "toc_n", "toc_title_part_a", "decision", "outcome", "report_ids", "note"]
NONFIELD_WORDS = ["מפתח", "כנס", "מוסיאון", "מוזיאון", "ספרות", "פרסומים", "נאמני", "הודעה", "הודעות", "הערות",
                  "תיקונים", "ביבליוגרפיה", "חוק", "תערוכה"]


def read_csv(path):
    return p2.read_csv(path)


def vol_file_of(local_file):
    return local_file[len("IAA_"):-len(".pdf")]


def load_decisions():
    dec = {}
    for p in sorted(DATA.glob("screen_decisions_b*.tsv")):
        with open(p, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                assert None not in r, (p.name, r)  # no surplus columns
                r = {k: (v or "").strip() for k, v in r.items()}
                key = (r["vol_file"], r["toc_n"])
                assert key not in dec, ("duplicate decision", key, p.name)
                assert r["decision"] in DECISIONS, (key, r["decision"])
                r["_file"] = p.name
                dec[key] = r
    return dec


def ref_zones(refs, params):
    """Zone each map reference found in an item's text, trying both number orders (raw output often puts N first)."""
    out = []
    for ref in [x for x in refs.split(";") if x]:
        a, b = ref.split("/")
        zs = []
        for e, n in ((a, b), (b, a)):
            try:
                r = geo.parse_ref("%s/%s" % (e, n))
                lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
            except ValueError:
                continue
            zs.append(common.zone_of(lat, lon, params) or "outside")
        out.append("%s:%s" % (ref, "|".join(sorted(set(zs))) or "unparsed"))
    return ";".join(out)


def default_decision(title, has_body_hits):
    if any(w in title for w in NONFIELD_WORDS):
        return "NONFIELD", "default by keyword: not a field report"
    reason = "default: no gazetteer term in the title and no in-region map reference in the item text"
    if has_body_hits:
        reason += "; body gazetteer hits seen in the per-volume signal list and judged incidental (not listed one by one)"
    return "OUT_TITLE", reason


def build_reports(params, places, pmeta, entries_by_place, bx, sources, spans, toc_of_report):
    reps = []
    for p in sorted(DATA.glob("coding_*.json")):
        reps.extend(json.loads(p.read_text(encoding="utf-8")))
    reps.sort(key=lambda r: r["report_id"])
    ids = [r["report_id"] for r in reps]
    assert len(ids) == len(set(ids)), "duplicate report_id"
    features, reports, outside_feats = [], [], []
    for rep in reps:
        tf = rep["text_file_id"]
        src = sources[tf]
        url = src["portal_item_url"]
        access = "owner's Mac local PDF '%s' (SHA-256 %s), pdftotext -raw" % (src["local_file_name"], src["pdf_sha256"])
        sp = spans[rep["report_id"]]
        assert sp["text_lines"] == rep["text_lines"], rep["report_id"]
        assert sp["quotes_not_found"] == "", rep["report_id"]
        text_file, text_lines, text_sha = tf + ".raw.txt (outside the repository)", rep["text_lines"], sp["text_sha256"]
        screen, tier = "S-LOC", "S-LOC (whole volume)"
        exposure = rep.get("exposure") or "unexposed at freeze"
        if rep.get("map_ref"):
            loc = p2.locate_ref(rep["map_ref"], places, params)
            src_txt = "map ref"
        else:
            loc = dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[],
                       zone=rep.get("name_zone") or "unlocated", swapped=False)
            src_txt = "name only" + (" (%s)" % rep["name_place"] if rep.get("name_place") else "")
        d = loc["dists"]
        nearest, dist = (d[0][1], d[0][0]) if d else (rep.get("name_place", ""), None)
        w2 = [pl for k, pl in d if k <= 2.0]
        w5 = [pl for k, pl in d if k <= 5.0]
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
                fl = p2.locate_ref(f["map_ref"], places, params)
                fsrc = "feature map ref"
                fd = fl["dists"]
                fnear, fdist = fd[0][1], fd[0][0]
                fw2 = [pl for k, pl in fd if k <= 2.0]
                fw5 = [pl for k, pl in fd if k <= 5.0]
            elif f.get("name_place"):
                fl = dict(loc, lat=None, lon=None, dists=[], e="", n="", unit="", grid="", crs="")
                fsrc, fnear, fdist, fw2, fw5 = "feature site name (%s)" % f["name_place"], f["name_place"], None, [], []
            if f.get("name_zone"):
                assert not f.get("map_ref"), rep["report_id"]
                fl = dict(fl, zone=f["name_zone"])
                fsrc = "feature zone by name (%s)" % f.get("site", "")
            assert fl["zone"] != "MULTI", ("feature in a MULTI report needs its own zone", rep["report_id"])
            place_for_entries = fnear if (fdist is not None and fdist <= 2.0) or (fdist is None and fnear) else ""
            row = dict(report_id=rep["report_id"], url=url, series=rep["series"], volume=rep["volume"], year=rep["year"],
                       pages=rep.get("pages", ""), site_name=rep["title"], author=rep.get("author", ""),
                       permit=rep.get("permit", ""), map_ref_as_given=f.get("map_ref") or rep.get("map_ref", ""),
                       map_ref_used="", grid=fl["grid"], crs_used=fl["crs"], easting_m=fl["e"], northing_m=fl["n"],
                       precision_m=fl["unit"], lat=p2.fmt(fl["lat"], 5), lon=p2.fmt(fl["lon"], 5), coordinate_source=fsrc,
                       feature_site=f.get("site", ""), nearest_place=fnear, distance_km=p2.fmt(fdist, 3),
                       places_within_2km=";".join(fw2), places_within_5km=";".join(fw5), regions=";".join(regs),
                       feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                       dated_in_window=f["window"], excavated_or_surveyed=rep["excavated_or_surveyed"],
                       quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else "",
                       protected_strip=rep.get("protected_strip", "no"), screen=screen,
                       region_zone=fl["zone"], dist_to_nearest_place_km=p2.fmt(fdist, 3),
                       feature_subtype=f.get("subtype", ""), exposure_at_freeze=exposure)
            (frows if fl["zone"] in ZONES else outside_feats).append(row)
        features.extend(frows)
        notes = "; ".join(x for x in (rep.get("notes", ""), rep.get("screen_note", ""),
                                       rep.get("tier1_record", "") and "TIER-1 RECORD: " + rep["tier1_record"]) if x)
        reports.append(dict(report_id=rep["report_id"], url=url, access=access, series=rep["series"], volume=rep["volume"],
                            year=rep["year"], pages=rep.get("pages", ""), site_name=rep["title"], author=rep.get("author", ""),
                            permit=rep.get("permit", ""), screen=screen, toc_item=toc_of_report.get(rep["report_id"], ""),
                            map_ref_as_given=rep.get("map_ref", ""), map_ref_used="", grid=loc["grid"], crs_used=loc["crs"],
                            lat=p2.fmt(loc["lat"], 5), lon=p2.fmt(loc["lon"], 5), coordinate_source=src_txt,
                            nearest_place=nearest, distance_km=p2.fmt(dist, 3), places_within_2km=";".join(w2),
                            places_within_5km=";".join(w5), regions=";".join(regs), location_status=status,
                            excavated_or_surveyed=rep["excavated_or_surveyed"], area_depth_stated=rep.get("area_depth", ""),
                            n_feature_rows=len(frows), feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file=text_file, text_lines=text_lines, text_sha256=text_sha,
                            protected_strip=rep.get("protected_strip", "no"), location_note=rep.get("location_note", ""),
                            notes=notes, region_zone=loc["zone"], dist_to_nearest_place_km=p2.fmt(dist, 3),
                            exposure_at_freeze=exposure, tier=tier))
    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    return reps, reports, features, outside_feats


def main(out_dir=PART):
    out_dir = Path(out_dir)
    params = common.plan_params()
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    pmeta = {p["place_id"]: p for p in places}
    entries_by_place = defaultdict(list)
    for c in read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    bx = p1.boxes(json.loads((LANE / "search_plan.json").read_text(encoding="utf-8")))
    sources = {r["text_file"]: r for r in read_csv(DATA / "local_sources.csv")}
    spans = {r["report_id"]: r for r in read_csv(DATA / "local_spans.csv")}
    vols = {r["local_file"]: r for r in read_csv(DATA / "volumes.csv")}
    toc = read_csv(DATA / "portal_toc_items.csv")
    sig = {(r["vol_file"], r["toc_n"]): r for r in read_csv(DATA / "heading_signals.csv")}
    dec = load_decisions()
    pats = screen_titles.patterns(params)

    # phase-1 candidates in part-A volumes: item_key '<series>_<portal item no>#<toc n, 3 digits>'
    url_to_vol = {v["item_url"]: vol_file_of(k) for k, v in vols.items()}
    cands = defaultdict(list)
    for c in read_csv(LANE / "data" / "screen_candidates.csv"):
        if c["series"] != "ha_hebrew_series":
            continue
        url = "https://publications.iaa.org.il/ha_hebrew_series/%s" % c["item_no"]
        if url in url_to_vol:
            cands[(url_to_vol[url], str(int(c["item_key"].split("#")[1])))].append(c)

    # report -> TOC item(s)
    toc_of_report = defaultdict(list)
    for (vf, n), r in sorted(dec.items()):
        for rid in [x for x in r["report_id"].split(";") if x]:
            toc_of_report[rid].append("%s TOC %s" % (vf, n))
    toc_of_report = {k: "; ".join(v) for k, v in toc_of_report.items()}

    reps, reports, features, outside_feats = build_reports(params, places, pmeta, entries_by_place, bx, sources, spans,
                                                           toc_of_report)
    rep_ids = {r["report_id"] for r in reps}
    zone_of_rep = {r["report_id"]: r["region_zone"] for r in reports}

    # screen table: every portal TOC item, plus decision rows for headings not in the portal TOC (x.., n.1)
    srows, seen = [], set()
    for t in toc:
        vf = vol_file_of(t["local_file"])
        key = (vf, t["n"])
        seen.add(key)
        s, p = screen_titles.hits(t["title"], pats)
        sg = sig.get(key, {})
        refs = sg.get("map_refs_in_item_text", "")
        rz = ref_zones(refs, params) if refs else ""
        body = sg.get("body_gazetteer_hits_by_zone", "")
        d = dec.get(key)
        if d:
            decision, source, reason, rids = d["decision"], "explicit (%s)" % d["_file"], d["reason"], d["report_id"]
        else:
            decision, reason = default_decision(t["title"], bool(body))
            source, rids = "default", ""
        srows.append(dict(vol_file=vf, volume=t["volume"], year=t["year"], item_url=t["item_url"], toc_n=t["n"],
                          title=t["title"], author=t["author"], pages=t["pages"],
                          heading_pdf_page=sg.get("heading_pdf_page", ""), heading_located=sg.get("heading_located", ""),
                          title_hits_strict=";".join("%s:%s" % x for x in s), title_hits_prefix=";".join("%s:%s" % x for x in p),
                          map_refs_in_item_text=refs, map_ref_zones=rz, body_gazetteer_hits_by_zone=body,
                          phase1_candidate=";".join(c["item_key"] for c in cands.get(key, [])),
                          decision=decision, decision_source=source, reason=reason, report_ids=rids))
    for key, d in sorted(dec.items()):
        if key in seen:
            continue
        vf, n = key
        v = vols["IAA_%s.pdf" % vf]
        srows.append(dict(vol_file=vf, volume=v["volume"], year=v["year"], item_url=v["item_url"], toc_n=n,
                          title=d["extra_title"], author="", pages=d["printed"], heading_pdf_page=d["pdf_page"],
                          heading_located="heading in the text (not in the portal table of contents)",
                          title_hits_strict="", title_hits_prefix="", map_refs_in_item_text="", map_ref_zones="",
                          body_gazetteer_hits_by_zone="", phase1_candidate="", decision=d["decision"],
                          decision_source="explicit (%s)" % d["_file"], reason=d["reason"], report_ids=d["report_id"]))

    def nkey(n):
        m = re.match(r"(x?)(\d+)(?:\.(\d+))?$", n)
        return (1 if m.group(1) else 0, int(m.group(2)), int(m.group(3) or 0))
    srows.sort(key=lambda r: (r["vol_file"], nkey(r["toc_n"])))
    for r in srows:
        for rid in [x for x in r["report_ids"].split(";") if x]:
            assert rid in rep_ids, ("decision names an uncoded report", rid)
    coded_by_dec = {rid for r in srows for rid in r["report_ids"].split(";") if rid}
    assert coded_by_dec == rep_ids, ("coded reports without a screen decision", sorted(rep_ids - coded_by_dec))

    # phase-1 candidate checkoff
    toc_title = {(vol_file_of(t["local_file"]), t["n"]): t["title"] for t in toc}
    scr = {(r["vol_file"], r["toc_n"]): r for r in srows}
    crows = []
    for key in sorted(cands, key=lambda k: (k[0], int(k[1]))):
        for c in cands[key]:
            r = scr.get(key)
            if not r:
                outcome, note, decision, rids = "not found in the volume", "no portal TOC item with this number", "", ""
            else:
                decision, rids = r["decision"], r["report_ids"]
                if decision in READ_DECISIONS or (decision == "COMPOSITE" and rids):
                    zs = sorted({zone_of_rep[x] for x in rids.split(";") if x})
                    outcome = "read (%s)" % ";".join(zs)
                elif decision == "HELD":
                    outcome = "held (plan section 7)"
                elif decision == "STRIP_CHECK":
                    outcome = "protected strip check: citation only"
                elif decision in ("BORDER", "UNLOC"):
                    outcome = "listed, not coded (%s)" % DECISIONS[decision]
                elif decision == "NONFIELD":
                    outcome = "not a field report"
                else:
                    outcome = "outside region"
                note = r["reason"]
            crows.append(dict(item_key=c["item_key"], screen=c["screen"], volume_title=c["volume_title"], year=c["year"],
                              pages=c["pages"], toc_text=c["toc_text"], groups=c["groups"], matched_terms=c["matched_terms"],
                              vol_file=key[0], toc_n=key[1], toc_title_part_a=toc_title.get(key, ""), decision=decision,
                              outcome=outcome, report_ids=rids, note=note))
    # phase-1 candidates whose portal item is a part-A volume but which did not join (should be none)
    p1_part_a = sum(len(v) for v in cands.values())

    p2.write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    p2.write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    p2.write_csv(out_dir / "screen.csv", SCREEN_FIELDS, srows)
    p2.write_csv(out_dir / "candidates_checkoff.csv", CHECK_FIELDS, crows)
    summ = summarize(features, reports, srows, crows, outside_feats, vols)
    (out_dir / "summary.json").write_text(json.dumps(summ["json"], ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                          encoding="utf-8")
    (out_dir / "summary.md").write_text(summ["md"], encoding="utf-8")
    print("volumes %d, screen rows %d, reports %d, feature rows %d (outside region %d), phase-1 candidates %d" % (
        len(vols), len(srows), len(reports), len(features), len(outside_feats), p1_part_a))


def summarize(features, reports, srows, crows, outside_feats, vols):
    md = ["# HA-ESI phase 3 part A: summary tables (generated by scripts/build_part_a.py; do not edit)\n"]
    md.append("Volumes screened: %d files (HA 1961-1979). Screen rows: %d (portal table-of-contents items plus headings "
              "found only in the text)." % (len(vols), len(srows)))
    dc = Counter(r["decision"] for r in srows)
    ds = Counter(r["decision_source"].split(" ")[0] for r in srows)
    md.append("Decisions: " + ", ".join("%s %d" % (k, dc[k]) for k in DECISIONS if dc[k]) +
              ". Explicit %d, default %d.\n" % (ds["explicit"], ds["default"]))
    in_reg = [r for r in reports if r["region_zone"] in ZONES or r["region_zone"] == "MULTI"]
    md.append("Reports read and coded: %d; in the region %d (MULTI-zone surveys %d); outside the region by map reference %d." % (
        len(reports), len(in_reg), sum(1 for r in reports if r["region_zone"] == "MULTI"), len(reports) - len(in_reg)))
    md.append("Reports in the region with no eligible feature: %d.\n" % sum(1 for r in in_reg if int(r["n_feature_rows"]) == 0))
    wt = Counter(f["dated_in_window"] for f in features)
    md.append("Feature rows in the region: %d (dated in window: yes %d, no %d, unknown %d). Rows outside the region: %d.\n" % (
        len(features), wt["yes"], wt["no"], wt["unknown"], len(outside_feats)))
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
    md.append("\n## Reports by zone\n")
    md.append("| zone | reports | with features | feature rows |")
    md.append("|---|---|---|---|")
    for z in ZONES + ["MULTI", "outside", "unlocated"]:
        rr = [r for r in reports if r["region_zone"] == z]
        if rr:
            md.append("| %s | %d | %d | %d |" % (z, len(rr), sum(1 for r in rr if int(r["n_feature_rows"])),
                                               sum(int(r["n_feature_rows"]) for r in rr)))
    oc = Counter(r["outcome"].split(" (")[0] for r in crows)
    md.append("\n## Phase-1 screen candidates in part-A volumes\n")
    md.append("Candidates: %d. " % len(crows) + ", ".join("%s %d" % kv for kv in sorted(oc.items())) + ".\n")
    md.append("## Dated-in-window rows\n")
    md.append("| report_id | zone | nearest place (km) | class | subtype | period as given |")
    md.append("|---|---|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s | %s | %s |" % (
                f["report_id"], f["region_zone"],
                ("%s (%s)" % (f["nearest_place"], f["distance_km"])) if f["distance_km"] else (f["nearest_place"] or "name only"),
                f["feature_type"], f["feature_subtype"].replace("|", "/"), f["period_as_given"].replace("|", "/")))
    js = dict(volumes=len(vols), screen_rows=len(srows), decisions=dict(dc), decision_source=dict(ds),
              reports=len(reports), reports_in_region=len(in_reg), feature_rows=len(features), window=dict(wt),
              class_zone=js_tab, rows_by_zone={z: zt[z] for z in ZONES}, outside_feature_rows=len(outside_feats),
              phase1_candidates=len(crows), phase1_outcomes=dict(oc))
    return dict(md="\n".join(md) + "\n", json=js)


if __name__ == "__main__":
    out = PART
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
