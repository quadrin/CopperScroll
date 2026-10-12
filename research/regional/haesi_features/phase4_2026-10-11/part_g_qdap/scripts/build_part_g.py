#!/usr/bin/env python3
"""Build the phase-4 part-G (QDAP) tables from the hand screen and the per-unit coding records.

Reads:  ../data/screen_units.tsv (every screened unit, with decision),
        ../data/units/*.json (one coding record per in-region unit read),
        ../data/held_units.tsv (held / protected units, citation only),
        the phase-2 plan parameters, field lists and place list (through the phase-2 and phase-1 scripts, unchanged).
Writes (part_g_qdap/): reports.csv and features.csv (phase-2 column order exactly), screen.csv, held.csv,
        summary.md, summary.json.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_g_qdap/scripts/build_part_g.py [--out DIR]
Standard library plus pyproj (through the phase-1 geo.py). Deterministic. No OCR text is read here.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
PHASE2 = PART.parent.parent / "phase2_2026-10-10"
sys.path.insert(0, str(PHASE2 / "scripts"))
import build_phase2 as b2  # noqa: E402  (phase-2 build: field lists, fmt, csv helpers; loads common, geo, phase-1 build)

common, geo, p1 = b2.common, b2.geo, b2.p1
DATA = PART / "data"
CLASSES, ZONES = b2.CLASSES, b2.ZONES
IA_URL = "https://archive.org/details/quarterly-department-of-antiquities-palestine_%s"
ACCESS = "archive.org OCR (hocr searchtext with page index; DjVu XML where the searchtext was refused), fetched from the workspace; text not stored"
SCREEN_FIELDS = ["unit_id", "ia_item", "volume", "issue", "year", "kind", "title", "first_page", "title_gazetteer_hits",
                 "zone_by_title", "screen", "decision", "decision_reason", "tier", "order_position_in_tier", "status",
                 "coded_report_id", "n_feature_rows"]
HELD_FIELDS = ["unit_id", "ia_item", "volume", "issue", "year", "pages", "title", "citation", "first_line_seen",
               "hold_reason", "protected_strip", "tier", "order_position_in_tier", "exposure_note"]
DECISIONS = {"IN", "HELD", "OUT_TITLE", "OUT_REGION", "NOT_FIELD", "NO_TEXT"}


def ia_parts(short):
    """'1934_4_1-2' -> (year, volume, issue)."""
    bits = short.split("_")
    year, vol = bits[0], bits[1]
    issue = bits[2] if len(bits) > 2 else ""
    if issue == "supplement":
        issue = "Supplement"
    return year, vol, issue


def slug(title, n=6):
    t = common.norm(title).strip()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    words = [w for w in t.split() if w not in {"the", "of", "a", "an", "in", "at", "and", "on", "from", "by", "to", "for"}]
    return "-".join(words[:n]) or "untitled"


def read_tsv(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        rows.append(line.split("\t"))
    return rows


def sha_order(ids):
    return sorted(ids, key=lambda u: hashlib.sha256(u.encode("utf-8")).hexdigest())


def tier_of(zone, title):
    if zone in ("Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT"):
        return "T1"
    if zone == "Z4_JERUSALEM_HILLS":
        return "T3" if common.norm(title).strip().startswith("jerusalem") else "T2"
    return ""


def load_units():
    recs = {}
    for p in sorted((DATA / "units").glob("*.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        assert p.stem == r["report_id"], p
        assert r["report_id"] not in recs
        recs[r["report_id"]] = r
    return recs


def unit_title_for_tier(r):
    # the tier rule reads the unit's own heading: for round-up paragraphs, the part after the section name
    t = r["title"]
    return t.split(": ", 1)[1] if r["unit_kind"] != "article" and ": " in t else t


def build(out_dir=PART):
    out_dir = Path(out_dir)
    params = common.plan_params()
    pats = common.gazetteer_patterns(params)
    places = geo.load_places(p1.W2B_IN / "places_v2.csv")
    pl_ids = {p["place_id"] for p in places}
    entries_by_place = defaultdict(list)
    for c in b2.read_csv(p1.W2B_IN / "candidates_v2.csv"):
        entries_by_place[c["place_id"]].append(c["entry"])
    for k in entries_by_place:
        entries_by_place[k] = sorted(set(entries_by_place[k]), key=lambda e: (int("".join(ch for ch in e if ch.isdigit())), e))
    plan1 = json.loads((b2.PHASE1 / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)

    units = load_units()
    held = {row[0]: row for row in read_tsv(DATA / "held_units.tsv")}
    screen_in = read_tsv(DATA / "screen_units.tsv")

    # tiers and frozen-rule reading order (ascending sha256 of unit id within tier), in-region units only
    tiers = {}
    for rid, r in units.items():
        t = tier_of(r["name_zone"], unit_title_for_tier(r))
        assert t == r["tier"], (rid, t, r["tier"])
        tiers[rid] = t
    for hid, h in held.items():
        tiers[hid] = h[10]
    order = {}
    for t in ("T1", "T2", "T3"):
        for i, u in enumerate(sha_order([u for u, tt in tiers.items() if tt == t]), 1):
            order[u] = i

    features, reports = [], []
    for rid in sorted(units):
        r = units[rid]
        assert r["name_zone"] in ZONES and not r.get("map_ref"), rid
        url = IA_URL % r["ia_item"].replace("quarterly-department-of-antiquities-palestine_", "")
        name_place = r.get("name_place", "")
        assert not name_place or name_place in pl_ids, (rid, name_place)
        nearest = name_place
        title_norm = common.norm(r["title"]).strip()
        regs = p1.regions_for(None, None, [], title_norm, {"features": r["features"]}, bx)
        status = "name only" if name_place else "name only (zone)"
        csrc = "name only" + (" (%s)" % name_place if name_place else "")
        frows = []
        for f in r["features"]:
            assert f["type"] in CLASSES, (rid, f["type"])
            assert f["window"] in ("yes", "no", "unknown"), (rid, f["window"])
            frows.append(dict(report_id=rid, url=url, series="QDAP", volume=r["volume"], year=r["year"], pages=r["pages"],
                              site_name=r["title"], author=r.get("author", ""), permit="", map_ref_as_given="", map_ref_used="",
                              grid="", crs_used="", easting_m="", northing_m="", precision_m="", lat="", lon="",
                              coordinate_source=csrc, feature_site=f.get("site", ""), nearest_place=nearest, distance_km="",
                              places_within_2km="", places_within_5km="", regions=";".join(regs), feature_type=f["type"],
                              n_features=f.get("n", ""), period_as_given=f["period"], dated_in_window=f["window"],
                              excavated_or_surveyed=r["excavated_or_surveyed"], quote=f["quote"], relevance="",
                              candidate_entries=";".join(entries_by_place.get(name_place, [])) if name_place else "",
                              protected_strip="no", screen=r["screen"], region_zone=r["name_zone"],
                              dist_to_nearest_place_km="", feature_subtype=f.get("subtype", ""),
                              exposure_at_freeze="unexposed at freeze"))
        features.extend(frows)
        reports.append(dict(report_id=rid, url=url, access=ACCESS, series="QDAP", volume=r["volume"], year=r["year"],
                            pages=r["pages"], site_name=r["title"], author=r.get("author", ""), permit="", screen=r["screen"],
                            toc_item="%s span %s (%s)" % (r["ia_item"], r["span"], r["unit_kind"]), map_ref_as_given="",
                            map_ref_used="", grid="", crs_used="", lat="", lon="", coordinate_source=csrc,
                            nearest_place=nearest, distance_km="", places_within_2km="", places_within_5km="",
                            regions=";".join(regs), location_status=status, excavated_or_surveyed=r["excavated_or_surveyed"],
                            area_depth_stated="", n_feature_rows=len(frows),
                            feature_types=";".join(sorted({f["type"] for f in r["features"]})),
                            text_file="archive.org OCR, leaves and OCR lines %s (not stored)" % r["span"], text_lines=r["span"],
                            text_sha256=r["text_sha256"], protected_strip="no",
                            location_note=r.get("location_note", ""),
                            notes=(r.get("notes", "") + " Reading: " + r.get("reading", "") + ".").strip(),
                            region_zone=r["name_zone"], dist_to_nearest_place_km="", exposure_at_freeze="unexposed at freeze",
                            tier=tiers[rid]))
    features.sort(key=lambda x: (x["report_id"], x["feature_type"], x["feature_site"], x["feature_subtype"]))

    # screen table
    srows, seen_ids = [], set()
    nrows = Counter(f["report_id"] for f in features)
    for row in screen_in:
        short, kind, title, page, decision, ref, reason = (row + [""] * 7)[:7]
        assert decision in DECISIONS, row
        year, vol, issue = ia_parts(short)
        hits = common.title_hits(title, pats)
        flat = sorted({t for v in hits.values() for t in v})
        ztitle = ";".join(sorted(z for z in hits if z != "REGION_WIDE"))
        if decision in ("IN", "HELD"):
            uid = ref
        else:
            pg = ("%03d" % int(page)) if page.isdigit() else "x"
            uid = "QDAP%s-%s-%s" % (vol, pg, slug(title.split(": ", 1)[-1]))
        n = 2
        base = uid
        while uid in seen_ids:
            uid = "%s-%d" % (base, n)
            n += 1
        seen_ids.add(uid)
        if decision == "IN":
            assert ref in units, ref
            r = units[ref]
            screen = r["screen"]
            status = "read"
        elif decision == "HELD":
            assert ref in held, ref
            screen = "S-G" if flat else "S-MAN"
            status = "held (citation only)"
        else:
            screen = "S-G" if flat else "none"
            status = ""
        srows.append(dict(unit_id=uid, ia_item="quarterly-department-of-antiquities-palestine_" + short, volume=vol,
                          issue=issue, year=year, kind=kind, title=title, first_page=page,
                          title_gazetteer_hits=";".join(flat), zone_by_title=ztitle, screen=screen, decision=decision,
                          decision_reason=reason, tier=tiers.get(uid, ""), order_position_in_tier=order.get(uid, ""),
                          status=status, coded_report_id=ref if decision == "IN" else "",
                          n_feature_rows=nrows.get(ref, 0) if decision == "IN" else ""))
    in_ids = {r["coded_report_id"] for r in srows if r["decision"] == "IN"}
    assert in_ids == set(units), set(units) ^ in_ids
    assert {r["unit_id"] for r in srows if r["decision"] == "HELD"} == set(held)

    hrows = []
    for hid in sorted(held):
        h = held[hid]
        hrows.append(dict(unit_id=hid, ia_item="quarterly-department-of-antiquities-palestine_" + h[1], volume=h[2], issue=h[3],
                          year=h[4], pages=h[5], title=h[6], citation=h[7], first_line_seen=h[8], hold_reason=h[9],
                          protected_strip=h[11], tier=h[10], order_position_in_tier=order[hid], exposure_note=h[12]))

    b2.write_csv(out_dir / "features.csv", b2.FEATURE_FIELDS, features)
    b2.write_csv(out_dir / "reports.csv", b2.REPORT_FIELDS, reports)
    b2.write_csv(out_dir / "screen.csv", SCREEN_FIELDS, srows)
    b2.write_csv(out_dir / "held.csv", HELD_FIELDS, hrows)
    md, js = summarize(features, reports, srows, hrows)
    (out_dir / "summary.md").write_text(md, encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(js, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("screen rows %d, reports %d, feature rows %d, held %d" % (len(srows), len(reports), len(features), len(hrows)))


def summarize(features, reports, srows, hrows):
    dec = Counter(r["decision"] for r in srows)
    wt = Counter(f["dated_in_window"] for f in features)
    tiers = Counter(r["tier"] for r in reports)
    md = ["# Phase 4, part G (QDAP): summary (generated by scripts/build_part_g.py; do not edit)\n"]
    md.append("Units screened: %d (%s)." % (len(srows), ", ".join("%s %d" % (k, v) for k, v in sorted(dec.items()))))
    md.append("Units read and coded: %d (T1 %d, T2 %d, T3 %d); with no eligible feature: %d. Held or protected: %d.\n" % (
        len(reports), tiers["T1"], tiers["T2"], tiers["T3"], sum(1 for r in reports if r["n_feature_rows"] == 0), len(hrows)))
    md.append("Feature rows in the region: %d (dated in window: yes %d, no %d, unknown %d).\n" % (
        len(features), wt["yes"], wt["no"], wt["unknown"]))
    md.append("## Feature rows by class (yes / no / unknown)\n")
    md.append("| class | rows | yes | no | unknown |")
    md.append("|---|---|---|---|---|")
    by_class = {}
    for c in CLASSES:
        k = Counter(f["dated_in_window"] for f in features if f["feature_type"] == c)
        n = sum(k.values())
        by_class[c] = dict(rows=n, yes=k["yes"], no=k["no"], unknown=k["unknown"])
        md.append("| %s | %d | %d | %d | %d |" % (c, n, k["yes"], k["no"], k["unknown"]))
    md.append("| all | %d | %d | %d | %d |" % (len(features), wt["yes"], wt["no"], wt["unknown"]))
    md.append("\n## Feature rows by zone (yes / no / unknown)\n")
    md.append("| zone | rows | yes | no | unknown |")
    md.append("|---|---|---|---|---|")
    by_zone = {}
    for z in ZONES:
        k = Counter(f["dated_in_window"] for f in features if f["region_zone"] == z)
        n = sum(k.values())
        by_zone[z] = dict(rows=n, yes=k["yes"], no=k["no"], unknown=k["unknown"])
        md.append("| %s | %d | %d | %d | %d |" % (z, n, k["yes"], k["no"], k["unknown"]))
    md.append("\n## Rows dated in the window\n")
    md.append("| report_id | class | subtype | period as given |")
    md.append("|---|---|---|---|")
    for f in features:
        if f["dated_in_window"] == "yes":
            md.append("| %s | %s | %s | %s |" % (f["report_id"], f["feature_type"], f["feature_subtype"].replace("|", "/"),
                                                f["period_as_given"].replace("|", "/")))
    js = dict(units_screened=len(srows), decisions=dict(dec), reports=len(reports), reports_by_tier=dict(tiers),
              reports_without_feature=sum(1 for r in reports if r["n_feature_rows"] == 0), held=len(hrows),
              feature_rows=len(features), window=dict(wt), by_class=by_class, by_zone=by_zone)
    return "\n".join(md) + "\n", js


if __name__ == "__main__":
    out = PART
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    build(out)
