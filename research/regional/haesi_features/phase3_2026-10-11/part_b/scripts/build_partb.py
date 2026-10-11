#!/usr/bin/env python3
"""Build the HA-ESI phase-3 part-B tables (HA Hebrew volumes 1980-1998) from the hand coding and decisions.

Reads (part_b/data): volumes.csv, screen_auto.csv, decisions/*.csv, coding/*.json, spans.csv,
      body_heading_hits.csv, body_heading_review.csv, candidate_overrides.csv (hand matches of phase-1 candidates);
      phase-2 PLAN.md (frozen parameters, through phase-2 common.py), phase-1 and phase-2 reports.csv
      (already-coded crosswalk), phase-1 data/screen_candidates.csv (check-off), W2B places and candidates.
Writes (part_b): reports.csv and features.csv (phase-2 column order), screen.csv, candidates_checkoff.csv,
      already_coded_crosswalk.csv, body_headings.csv, summary.json, summary.md.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase3_2026-10-11/part_b/scripts/build_partb.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic. Needs no PDF or extracted text.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTB = HERE.parent
PHASE3 = PARTB.parent
LANE = PHASE3.parent  # research/regional/haesi_features
PHASE2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(PHASE2 / "scripts"))
import common  # noqa: E402  (phase-2 helpers; puts phase-1 scripts on sys.path)
import geo  # noqa: E402
import build as p1  # noqa: E402

DATA = PARTB / "data"
CLASSES = ["cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"]
ZONES = ["Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"]
FEATURE_FIELDS = p1.FEATURE_FIELDS + ["region_zone", "dist_to_nearest_place_km", "feature_subtype", "exposure_at_freeze"]
REPORT_FIELDS = p1.REPORT_FIELDS + ["region_zone", "dist_to_nearest_place_km", "exposure_at_freeze", "tier"]
SCREEN_FIELDS = ["screen_id", "volume", "year", "url", "source", "group", "title_en", "title_he", "printed_page",
                 "pdf_pages", "title_hits", "zone_by_title", "refs_in_region", "ref_zones", "auto_decision",
                 "decision", "decision_basis", "report_id", "note"]
CHECK_FIELDS = ["item_key", "volume", "year", "pages", "toc_text", "groups", "matched_terms", "screen_id",
                "match_basis", "outcome", "report_id", "note"]
XWALK_FIELDS = ["screen_id", "volume", "decision", "report_id", "phase", "region_zone", "lat", "lon", "n_feature_rows",
                "note"]
BODY_FIELDS = ["volume", "pdf_page", "layout_line", "text", "title_hits", "matches_screen_id", "review", "screen_id", "note"]
DECISIONS = {"read", "already coded in phase 1", "already coded in phase 1 (English version)",
             "already coded in phase 2 (English version)", "opened: outside region", "opened: not a site report",
             "held: cave report in held areas", "not read (pages missing from the copy)", "not read (time limit)"}
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


def vol_label(v):
    """'101-102' / '101–102' -> '101–102' (screen tables use the en dash)."""
    return v.replace("-", "–")


def load_coding():
    reps = []
    for p in sorted((DATA / "coding").glob("*.json")):
        for r in json.loads(p.read_text(encoding="utf-8")):
            r["_file"] = p.name
            reps.append(r)
    reps.sort(key=lambda r: r["report_id"])
    ids = [r["report_id"] for r in reps]
    dup = [k for k, n in Counter(ids).items() if n > 1]
    assert not dup, "duplicate report_id %s" % dup
    return reps


def load_decisions(screen_ids):
    dec = {}
    for p in sorted((DATA / "decisions").glob("*.csv")):
        for r in read_csv(p):
            sid = r["screen_id"]
            assert sid in screen_ids, "%s: unknown screen id %s" % (p.name, sid)
            assert sid not in dec, "duplicate decision for %s" % sid
            assert r["decision"] in DECISIONS, "%s: bad decision %r" % (sid, r["decision"])
            r["_file"] = p.name
            dec[sid] = r
    return dec


def locate_ref(ref, places, params):
    r = geo.parse_ref(ref)
    lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
    d = geo.distances(lat, lon, places)
    return dict(grid=r["grid"], crs="EPSG:28191" if r["grid"] == "OIG" else "EPSG:2039", e=r["e"], n=r["n"],
                unit=r["unit_m"], lat=lat, lon=lon, dists=d, zone=common.zone_of(lat, lon, params) or "outside",
                swapped=r["swapped"])


HE = re.compile(r"[א-ת]{2,}")
STOP = {"ירושלים", "חורבת", "סקר", "מפת", "של", "את", "ועד", "מערת", "מערות", "קבורה", "ח׳", "תל"}


def he_tokens(s):
    return {w for w in HE.findall(s.replace("׳", "").replace("'", "")) if w not in STOP}


def outcome_of(dd):
    """Check-off outcome of a phase-1 candidate from the decision of its screen heading."""
    if dd == "read" or dd.startswith("already coded"):
        return dd
    if dd.startswith(("outside region", "opened: outside")):
        return "outside region"
    if dd.startswith("held"):
        return "held (cave report in held areas)"
    if dd.startswith("opened: not a site"):
        return "not a site report"
    if dd.startswith("group heading"):
        return "group heading (children screened)"
    return dd


def main(out_dir=PARTB):
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

    vols = {r["key"]: r for r in read_csv(DATA / "volumes.csv")}
    vol_by_label = {vol_label(r["label"]): r for r in vols.values()}
    spans = {r["report_id"]: r for r in read_csv(DATA / "spans.csv")}
    screen = read_csv(DATA / "screen_auto.csv")
    sids = {r["screen_id"] for r in screen}
    dec = load_decisions(sids)
    reps = load_coding()
    rep_ids = {r["report_id"] for r in reps}

    # every coded report has exactly one 'read' decision, and every 'read' decision names a coded report
    read_dec = defaultdict(list)
    for sid, d in dec.items():
        if d["decision"] == "read":
            assert d["report_id"] in rep_ids, "%s: read decision names uncoded report %s" % (sid, d["report_id"])
            read_dec[d["report_id"]].append(sid)
    for rid in rep_ids:
        assert len(read_dec[rid]) == 1, "report %s has %d read decisions" % (rid, len(read_dec[rid]))

    features, reports, outside_feats = [], [], []
    for rep in reps:
        v = vols[rep["text_file_id"]]
        url = v["portal_item_url"]
        access = "owner's Mac local PDF '%s' (SHA-256 %s), pdftotext -raw" % (v["local_file"], v["pdf_sha256"])
        sp = spans[rep["report_id"]]
        assert sp["text_lines"] == rep["text_lines"], rep["report_id"]
        assert not sp["quotes_not_found"], rep["report_id"]
        sid = read_dec[rep["report_id"]][0]
        srow = next(r for r in screen if r["screen_id"] == sid)
        assert srow["volume"] == vol_label(rep["volume"]), (rep["report_id"], srow["volume"], rep["volume"])
        text_file = rep["text_file_id"] + ".raw.txt (outside the repository)"
        if rep.get("map_ref"):
            loc = locate_ref(rep["map_ref"], places, params)
            src_txt = "map ref"
        else:
            fref = next((f["map_ref"] for f in rep["features"] if f.get("map_ref")), "")
            if rep.get("name_zone"):
                zone = rep["name_zone"]
                src_txt = "name only (zone)"
            elif fref:
                zone = locate_ref(fref, places, params)["zone"]
                src_txt = "zone from the feature references"
            else:
                zone, src_txt = "unlocated", "unlocated"
            loc = dict(grid="", crs="", e="", n="", unit="", lat=None, lon=None, dists=[], zone=zone, swapped=False)
        d = loc["dists"]
        nearest, dist = (d[0][1], d[0][0]) if d else ("", None)
        w2 = [p for k, p in d if k <= 2.0]
        w5 = [p for k, p in d if k <= 5.0]
        regs = p1.regions_for(loc["lat"], loc["lon"], d, common.norm(rep["title"]).strip(), rep, bx)
        if d:
            status = "within 2 km" if dist <= 2.0 else ("2-5 km" if dist <= 5.0 else "beyond 5 km")
        else:
            status = src_txt
        frows = []
        for f in rep["features"]:
            assert f["type"] in CLASSES, (rep["report_id"], f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (rep["report_id"], f["window"])
            assert f.get("quote") and len(f["quote"].split()) <= 12, (rep["report_id"], f.get("quote"))
            fl, fsrc, fnear, fdist, fw2, fw5 = loc, src_txt, nearest, dist, w2, w5
            if f.get("map_ref"):
                fl = locate_ref(f["map_ref"], places, params)
                fsrc = "feature map ref"
                fd = fl["dists"]
                fnear, fdist = fd[0][1], fd[0][0]
                fw2 = [p for k, p in fd if k <= 2.0]
                fw5 = [p for k, p in fd if k <= 5.0]
            place_for_entries = fnear if (fdist is not None and fdist <= 2.0) else ""
            row = dict(report_id=rep["report_id"], url=url, series=rep["series"], volume=rep["volume"], year=rep["year"],
                       pages=rep.get("pages", ""), site_name=rep["title"], author=rep.get("author", ""),
                       permit=rep.get("permit", ""), map_ref_as_given=f.get("map_ref") or rep.get("map_ref_as_given") or rep.get("map_ref", ""),
                       map_ref_used=f.get("map_ref") or rep.get("map_ref", ""), grid=fl["grid"], crs_used=fl["crs"],
                       easting_m=fl["e"], northing_m=fl["n"], precision_m=fl["unit"], lat=fmt(fl["lat"], 5),
                       lon=fmt(fl["lon"], 5), coordinate_source=fsrc, feature_site=f.get("site", ""),
                       nearest_place=fnear, distance_km=fmt(fdist, 3), places_within_2km=";".join(fw2),
                       places_within_5km=";".join(fw5), regions=";".join(regs), feature_type=f["type"],
                       n_features=f.get("n", ""), period_as_given=f["period"], dated_in_window=f["window"],
                       excavated_or_surveyed=rep["excavated_or_surveyed"], quote=f["quote"], relevance="",
                       candidate_entries=";".join(entries_by_place.get(place_for_entries, [])) if place_for_entries else "",
                       protected_strip=rep.get("protected_strip", "no"), screen="S-LOC",
                       region_zone=fl["zone"], dist_to_nearest_place_km=fmt(fdist, 3),
                       feature_subtype=f.get("subtype", ""), exposure_at_freeze=EXPOSURE)
            (frows if fl["zone"] in ZONES else outside_feats).append(row)
        features.extend(frows)
        reports.append(dict(report_id=rep["report_id"], url=url, access=access, series=rep["series"], volume=rep["volume"],
                            year=rep["year"], pages=rep.get("pages", ""), site_name=rep["title"], author=rep.get("author", ""),
                            permit=rep.get("permit", ""), screen="S-LOC",
                            toc_item="%s: %s" % (sid, srow["title_en"] or srow["title_he"]),
                            map_ref_as_given=rep.get("map_ref_as_given") or rep.get("map_ref", ""),
                            map_ref_used=rep.get("map_ref", ""), grid=loc["grid"], crs_used=loc["crs"],
                            lat=fmt(loc["lat"], 5), lon=fmt(loc["lon"], 5), coordinate_source=src_txt,
                            nearest_place=nearest, distance_km=fmt(dist, 3), places_within_2km=";".join(w2),
                            places_within_5km=";".join(w5), regions=";".join(regs), location_status=status,
                            excavated_or_surveyed=rep["excavated_or_surveyed"], area_depth_stated=rep.get("area_depth", ""),
                            n_feature_rows=len(frows), feature_types=";".join(sorted({f["type"] for f in rep["features"]})),
                            text_file=text_file, text_lines=rep["text_lines"], text_sha256=sp["text_sha256"],
                            protected_strip=rep.get("protected_strip", "no"), location_note=rep.get("location_note", ""),
                            notes=rep.get("notes", ""), region_zone=loc["zone"], dist_to_nearest_place_km=fmt(dist, 3),
                            exposure_at_freeze=EXPOSURE, tier="S-LOC (whole volume)"))

    # screen table: every heading, with its decision
    srows, missing = [], []
    for r in screen:
        v = vol_by_label[r["volume"]]
        d = dec.get(r["screen_id"])
        row = dict(r, url=v["portal_item_url"])
        if d:
            row.update(decision=d["decision"], decision_basis="opened by hand (%s)" % d["_file"],
                       report_id=d["report_id"], note=d["note"])
        elif r["auto_decision"].startswith(("outside region", "group heading")):
            row.update(decision=r["auto_decision"], decision_basis="automatic (frozen screen rules)")
        else:
            missing.append(r["screen_id"])
            row.update(decision="not read (time limit)", decision_basis="flagged; no decision")
        srows.append(row)
    assert not missing, "flagged headings without a decision: %s" % missing

    # already-coded crosswalk (phase 1 / phase 2 reports not re-coded)
    p2rep = {r["report_id"]: r for r in read_csv(PHASE2 / "reports.csv")}
    p1rep = {r["report_id"]: r for r in read_csv(LANE / "reports.csv")}
    p1x = {r["report_id"]: r for r in read_csv(PHASE2 / "phase1_zone_crosswalk.csv") if r["table"] == "reports"}
    xrows = []
    for sid, d in sorted(dec.items()):
        if not d["decision"].startswith("already coded"):
            continue
        rid = d["report_id"]
        if rid in p2rep:
            r, ph = p2rep[rid], "phase 2"
            z = r["region_zone"]
            nrow = r["n_feature_rows"]
            lat, lon = r["lat"], r["lon"]
        else:
            assert rid in p1rep, "%s: unknown already-coded report %s" % (sid, rid)
            r, ph = p1rep[rid], "phase 1"
            z = p1x[rid]["region_zone"] if rid in p1x else ""
            nrow = r["n_feature_rows"]
            lat, lon = r["lat"], r["lon"]
        xrows.append(dict(screen_id=sid, volume=sid.split("-")[0][2:], decision=d["decision"], report_id=rid, phase=ph,
                          region_zone=z, lat=lat, lon=lon, n_feature_rows=nrow, note=d["note"]))

    # body-heading sweep review
    rev = {(r["volume"], r["pdf_page"], r["layout_line"]): r for r in read_csv(DATA / "body_heading_review.csv")}
    brows = []
    auto_re = re.compile(r"(דפוס|התש|סודר)")
    for h in read_csv(DATA / "body_heading_hits.csv"):
        k = (h["volume"], h["pdf_page"], h["layout_line"])
        row = dict(h)
        if h["matches_screen_id"]:
            row.update(review="repeats a screened heading", screen_id=h["matches_screen_id"].split(";")[0])
        elif k in rev:
            row.update(review=rev[k]["review"], screen_id=rev[k]["screen_id"], note=rev[k]["note"])
        elif auto_re.search(h["text"]):
            row.update(review="not a heading (automatic)", note="imprint or printer line")
        elif h["text"].strip().strip(",") == "ירושלים":
            row.update(review="group word 'Jerusalem' (automatic)", note="its reports are screened under their own headings")
        else:
            raise AssertionError("body heading without review: %s" % (k,))
        if row.get("screen_id"):
            assert row["screen_id"] in sids, row
        brows.append(row)

    # phase-1 candidate check-off (HA volumes of part B)
    labels = set(vol_by_label)
    by_vol_page = defaultdict(list)
    for r in srows:
        by_vol_page[r["volume"]].append(r)
    crow = []
    srow_by_id = {r["screen_id"]: r for r in srows}
    overrides = {r["item_key"]: r for r in read_csv(DATA / "candidate_overrides.csv")}
    used_overrides = set()
    for c in read_csv(LANE / "data" / "screen_candidates.csv"):
        if c["series"] != "ha_hebrew_series":
            continue
        m = re.search(r"Arkheologiyot (\d+(?:[–-]\d+)?)", c["volume_title"])
        lab = vol_label(m.group(1))
        if lab not in labels:
            continue
        if c["item_key"] in overrides:
            o = overrides[c["item_key"]]
            used_overrides.add(c["item_key"])
            best = srow_by_id[o["screen_id"]]
            crow.append(dict(c, volume=lab, screen_id=best["screen_id"],
                             match_basis="by hand (data/candidate_overrides.csv): %s" % o["note"],
                             outcome=o["outcome"] or outcome_of(best["decision"]),
                             report_id="" if o["outcome"] else best.get("report_id", ""), note=best.get("note", "")))
            continue
        pg = int(re.match(r"\d+", c["pages"]).group(0)) if re.match(r"\d+", c["pages"]) else None
        ct = he_tokens(c["toc_text"])  # author names after the title rarely occur in screen titles
        best, basis = None, ""
        cands = []
        for r in by_vol_page[lab]:
            try:
                rp = int(r["printed_page"])
            except ValueError:
                rp = None
            ov = len(ct & he_tokens(r["title_he"] + " " + r["group"]))
            near = (rp is not None and pg is not None and abs(rp - pg) <= 1)
            if near or ov >= 2:
                cands.append((near, ov, -abs((rp or 0) - (pg or 0)), r))
        cands.sort(key=lambda t: (t[1] > 0, t[0], t[1], t[2]), reverse=True)
        if cands and (cands[0][1] > 0 or (cands[0][0] and len([t for t in cands if t[0]]) == 1)):
            near, ov, _, best = cands[0]
            basis = "printed page %s and %d title word(s) in common" % (best["printed_page"], ov) if near else \
                "%d title words in common (printed page differs)" % ov
        if best is None:
            crow.append(dict(c, volume=lab, screen_id="", match_basis="no heading on that page with a common title word",
                             outcome="not found in the volume", note="see NOTES.md"))
            continue
        crow.append(dict(c, volume=lab, screen_id=best["screen_id"], match_basis=basis,
                         outcome=outcome_of(best["decision"]), report_id=best.get("report_id", ""),
                         note=best.get("note", "")))
    assert used_overrides == set(overrides), "unused candidate overrides: %s" % (set(overrides) - used_overrides)

    features.sort(key=lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"]))
    reports.sort(key=lambda r: r["report_id"])
    write_csv(out_dir / "features.csv", FEATURE_FIELDS, features)
    write_csv(out_dir / "reports.csv", REPORT_FIELDS, reports)
    write_csv(out_dir / "screen.csv", SCREEN_FIELDS, srows)
    write_csv(out_dir / "candidates_checkoff.csv", CHECK_FIELDS, crow)
    write_csv(out_dir / "already_coded_crosswalk.csv", XWALK_FIELDS, xrows)
    write_csv(out_dir / "body_headings.csv", BODY_FIELDS, brows)
    summ = summarize(features, reports, srows, crow, xrows, outside_feats)
    (out_dir / "summary.json").write_text(json.dumps(summ["json"], ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                          encoding="utf-8")
    (out_dir / "summary.md").write_text(summ["md"], encoding="utf-8")
    print("reports %d, feature rows %d (outside region %d), screen rows %d, candidates %d, crosswalk %d" % (
        len(reports), len(features), len(outside_feats), len(srows), len(crow), len(xrows)))


def summarize(features, reports, srows, crow, xrows, outside_feats):
    md = ["# HA-ESI phase 3 part B summary (generated by scripts/build_partb.py; do not edit)\n"]
    in_reg = [r for r in reports if r["region_zone"] in ZONES]
    md.append("Headings screened: %d in %d volumes. Reports read and coded: %d (in the region %d; with no eligible feature %d)." % (
        len(srows), len({r["volume"] for r in srows}), len(reports), len(in_reg),
        sum(1 for r in in_reg if int(r["n_feature_rows"]) == 0)))
    wt = Counter(f["dated_in_window"] for f in features)
    md.append("Feature rows in the region: %d (dated in window: yes %d, no %d, unknown %d). Feature rows outside the region (feature map ref): %d.\n" % (
        len(features), wt["yes"], wt["no"], wt["unknown"], len(outside_feats)))
    md.append("## Screen decisions\n")
    dc = Counter()
    for r in srows:
        d = r["decision"]
        key = "outside region (automatic)" if d.startswith("outside region") else d
        dc[key] += 1
    md.append("| decision | headings |")
    md.append("|---|---|")
    for k, n in sorted(dc.items()):
        md.append("| %s | %d |" % (k, n))
    md.append("\n## Feature rows by class and zone (rows: yes/no/unknown)\n")
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
    md.append("\n## Reports read by zone\n")
    md.append("| zone | reports | feature rows |")
    md.append("|---|---|---|")
    rz = Counter(r["region_zone"] for r in reports)
    for z in ZONES + sorted(set(rz) - set(ZONES)):
        if rz[z]:
            md.append("| %s | %d | %d |" % (z, rz[z], sum(int(r["n_feature_rows"]) for r in reports if r["region_zone"] == z)))
    md.append("\n## Phase-1 screen candidates in these volumes\n")
    oc = Counter(r["outcome"] for r in crow)
    md.append("| outcome | candidates |")
    md.append("|---|---|")
    for k, n in sorted(oc.items()):
        md.append("| %s | %d |" % (k, n))
    md.append("| all | %d |" % len(crow))
    md.append("\n## Dated-in-window rows\n")
    md.append("| report_id | zone | nearest place (km) | class | subtype | period as given |")
    md.append("|---|---|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s | %s | %s |" % (
                f["report_id"], f["region_zone"],
                ("%s (%s)" % (f["nearest_place"], f["distance_km"])) if f["distance_km"] else "name only",
                f["feature_type"], f["feature_subtype"].replace("|", "/"), f["period_as_given"].replace("|", "/")))
    xz = Counter((r["phase"], r["region_zone"] or "unlocated") for r in xrows)
    md.append("\nAlready coded in phase 1 or 2 (Hebrew counterparts not re-coded): %d headings; by phase and zone: %s.\n" % (
        len(xrows), "; ".join("%s %s %d" % (a, b, n) for (a, b), n in sorted(xz.items()))))
    js = dict(headings=len(srows), decisions=dict(dc), reports=len(reports), reports_in_region=len(in_reg),
              reports_by_zone=dict(rz), feature_rows=len(features), window=dict(wt), class_zone=js_tab,
              rows_by_zone={z: zt[z] for z in ZONES}, outside_feature_rows=len(outside_feats),
              candidates=dict(oc), candidates_total=len(crow), already_coded=len(xrows))
    return dict(md="\n".join(md) + "\n", json=js)


if __name__ == "__main__":
    out = PARTB
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
