#!/usr/bin/env python3
"""Build the part-H tables (SWP Memoirs and Guerin) from the committed screen and hand coding.

Reads:  data/screen_<src>.csv (every site entry screened), data/coding_<src>.jsonl (hand coding of read units),
        data/held_records.jsonl (held / protected / Tier-1 units), data/missed_headings.csv,
        the phase-2 column order and helpers (build_phase2.py, common.py) and the phase-1 region helper.
Writes: reports.csv, features.csv (phase-2 columns, single zone), features_zone_unresolved.csv (same columns;
        in-region rows whose SWP square straddles two zones), screen.csv, held.csv, summary.json, summary.md.

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_h_surveys/scripts/build_part_h.py [--out DIR]
Deterministic. Standard library plus pyproj (through the phase-2 / phase-1 helpers).
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
DATA = PART / "data"
PHASE2 = PART.parents[1] / "phase2_2026-10-10"
sys.path.insert(0, str(PHASE2 / "scripts"))
sys.path.insert(0, str(HERE))
import build_phase2 as b2  # noqa: E402
import names  # noqa: E402

common, p1 = b2.common, b2.p1
ZONES, CLASSES = b2.ZONES, b2.CLASSES
SOURCES = {
    "swp3": dict(series="SWP Memoirs", volume="III", year="1883", author="C. R. Conder and H. H. Kitchener",
                 url="https://archive.org/details/surveyofwesternp03conduoft",
                 access="archive.org OCR (hOCR search text with its page index, surveyofwesternp03conduoft), fetched in the workspace; text kept outside the repository"),
    "swp2": dict(series="SWP Memoirs", volume="II", year="1882", author="C. R. Conder and H. H. Kitchener",
                 url="https://archive.org/details/surveyofwesternp02conduoft",
                 access="archive.org OCR (hOCR search text with its page index, surveyofwesternp02conduoft), fetched in the workspace; text kept outside the repository"),
    "gue_j1": dict(series="Guerin, Description geographique, historique et archeologique de la Palestine, Judee",
                   volume="I", year="1868", author="V. Guerin",
                   url="https://archive.org/details/descriptiongeogr01guer",
                   access="archive.org OCR (hOCR search text with its page index, descriptiongeogr01guer), fetched in the workspace; text kept outside the repository"),
}
SCREEN_FIELDS = ["unit_id", "source", "sheet_or_part", "name", "name_as_printed", "square", "page_first", "page_last",
                 "square_status", "zones_seen", "gazetteer_hits", "zone", "location_basis", "decision", "tier",
                 "order_position_in_tier", "status", "n_feature_rows", "note"]
HELD_FIELDS = ["unit_id", "source", "pages", "hold_type", "scope", "area", "protected_strip", "first_words", "note"]


def read_jsonl(p):
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def load():
    screens, coding = {}, {}
    for src in SOURCES:
        sp = DATA / ("screen_%s.csv" % src)
        if sp.exists():
            screens[src] = b2.read_csv(sp)
            coding[src] = {r["unit_id"]: r for r in read_jsonl(DATA / ("coding_%s.jsonl" % src))}
    held = read_jsonl(DATA / "held_records.jsonl")
    return screens, coding, held


def location_text(s):
    if s["location_basis"] == "SWP square":
        return "SWP square (zone only; swp_grid calibration)"
    if s["location_basis"] == "SWP square (zone split)":
        return "SWP square (zone split; region certain, zone not)"
    if s["location_basis"].startswith("name"):
        return "name only (gazetteer: %s)" % s["gazetteer_hits"]
    return s["location_basis"]


def build_rows(screens, coding, held):
    plan1 = json.loads((b2.PHASE1 / "search_plan.json").read_text(encoding="utf-8"))
    bx = p1.boxes(plan1)
    whole_held = {h["unit_id"] for h in held if h["scope"].startswith("whole")}
    feats, unresolved, reports, srows = [], [], [], []
    for src, rows in screens.items():
        meta = SOURCES[src]
        for s in rows:
            s = dict(s, sheet_or_part=s.get("sheet", s.get("sheet_or_part", "")))
            uid = s["unit_id"]
            rec = coding[src].get(uid)
            assert not (rec and uid in whole_held), uid
            zone = s["zone"]
            single = zone in ZONES
            if rec:
                status = "read" if single else "read (zone unresolved)"
            elif uid in whole_held:
                status = "held or protected (citation only)" if not any(
                    h["unit_id"] == uid and h["hold_type"].startswith("Tier-1") for h in held) else "Tier-1 extraction only"
            elif s["decision"].startswith("candidate"):
                status = "not read (time limit)"
            else:
                status = "not read (%s)" % s["decision"].split(":")[0].split(" (")[0]
            nrows = 0
            if rec:
                title_norm = common.norm(rec["name"]).strip()
                regs = p1.regions_for(None, None, [], title_norm, {"features": [{"type": f["type"]} for f in rec["features"]]}, bx)
                maptxt = ("Sheet %s, square %s" % (s["sheet_or_part"], s["square"])) if s["square"] else ""
                for f in rec["features"]:
                    assert f["type"] in CLASSES
                    row = dict(report_id=uid, url=meta["url"], series=meta["series"], volume=meta["volume"], year=meta["year"],
                               pages=rec["pages"], site_name=rec["name"], author=meta["author"], permit="",
                               map_ref_as_given=maptxt, map_ref_used="", grid="SWP reference square" if s["square"] else "",
                               crs_used="", easting_m="", northing_m="", precision_m="", lat="", lon="",
                               coordinate_source=location_text(s), feature_site=f.get("site", ""), nearest_place="",
                               distance_km="", places_within_2km="", places_within_5km="", regions=";".join(regs),
                               feature_type=f["type"], n_features=f.get("n", ""), period_as_given=f["period"],
                               dated_in_window=f["window"], excavated_or_surveyed=rec["excavated_or_surveyed"],
                               quote=f["quote"], relevance="", candidate_entries="", protected_strip="no",
                               screen="%s (%s)" % (s["decision"], s["location_basis"]), region_zone=zone,
                               dist_to_nearest_place_km="", feature_subtype="%s [%s]" % (f["subtype"], f["label"]),
                               exposure_at_freeze="unexposed at freeze")
                    (feats if single else unresolved).append(row)
                    nrows += 1
                reports.append(dict(report_id=uid, url=meta["url"], access=meta["access"], series=meta["series"],
                                    volume=meta["volume"], year=meta["year"], pages=rec["pages"], site_name=rec["name"],
                                    author=meta["author"], permit="", screen="%s (%s)" % (s["decision"], s["location_basis"]),
                                    toc_item=("Sheet %s, Section B" % s["sheet_or_part"]) if src.startswith("swp") else ("Judee %s" % meta["volume"]),
                                    map_ref_as_given=maptxt, map_ref_used="", grid="SWP reference square" if s["square"] else "",
                                    crs_used="", lat="", lon="", coordinate_source=location_text(s), nearest_place="",
                                    distance_km="", places_within_2km="", places_within_5km="", regions=";".join(regs),
                                    location_status=location_text(s), excavated_or_surveyed=rec["excavated_or_surveyed"],
                                    area_depth_stated="", n_feature_rows=nrows,
                                    feature_types=";".join(sorted({f["type"] for f in rec["features"]})),
                                    text_file="archive.org OCR (not stored)", text_lines=rec["read_scope"],
                                    text_sha256=rec["text_sha256"], protected_strip="no", location_note=s["note"],
                                    notes=rec["notes"], region_zone=zone, dist_to_nearest_place_km="",
                                    exposure_at_freeze="unexposed at freeze", tier=s["tier"]))
            srows.append(dict(unit_id=uid, source=src, sheet_or_part=s["sheet_or_part"], name=s["name"],
                              name_as_printed=s["name_as_printed"], square=s["square"], page_first=s["page_first"],
                              page_last=s["page_last"], square_status=s["square_status"], zones_seen=s["zones_seen"],
                              gazetteer_hits=s["gazetteer_hits"], zone=zone, location_basis=s["location_basis"],
                              decision=s["decision"], tier=s["tier"], order_position_in_tier=s["order_position_in_tier"],
                              status=status, n_feature_rows=nrows if rec else "", note=s["note"]))
    key = lambda r: (r["report_id"], r["feature_type"], r["feature_site"], r["feature_subtype"])
    feats.sort(key=key)
    unresolved.sort(key=key)
    reports.sort(key=lambda r: r["report_id"])
    return feats, unresolved, reports, srows


def summarize(feats, unresolved, reports, srows, held):
    js = {}
    st = Counter(r["status"] for r in srows)
    js["units_screened"] = len(srows)
    js["status"] = dict(sorted(st.items()))
    js["by_source"] = {src: dict(sorted(Counter(r["status"] for r in srows if r["source"] == src).items()))
                       for src in sorted({r["source"] for r in srows})}
    js["units_read"] = len(reports)
    js["feature_rows"] = len(feats)
    js["feature_rows_zone_unresolved"] = len(unresolved)
    js["held_records"] = len(held)

    def tab(rows):
        out = {}
        for c in CLASSES:
            k = Counter(r["dated_in_window"] for r in rows if r["feature_type"] == c)
            out[c] = dict(rows=sum(k.values()), yes=k["yes"], no=k["no"], unknown=k["unknown"])
        return out
    js["by_class"] = tab(feats)
    js["by_class_zone_unresolved"] = tab(unresolved)
    js["by_zone"] = {z: dict(rows=sum(1 for r in feats if r["region_zone"] == z),
                             yes=sum(1 for r in feats if r["region_zone"] == z and r["dated_in_window"] == "yes"),
                             no=sum(1 for r in feats if r["region_zone"] == z and r["dated_in_window"] == "no"),
                             unknown=sum(1 for r in feats if r["region_zone"] == z and r["dated_in_window"] == "unknown"))
                     for z in ZONES}
    js["by_zone_unresolved"] = dict(sorted(Counter(r["region_zone"] for r in unresolved).items()))
    js["by_class_and_zone"] = {c: {z: sum(1 for r in feats if r["feature_type"] == c and r["region_zone"] == z) for z in ZONES}
                               for c in CLASSES}
    w = Counter(r["dated_in_window"] for r in feats)
    wu = Counter(r["dated_in_window"] for r in unresolved)
    js["window"] = dict(yes=w["yes"], no=w["no"], unknown=w["unknown"])
    js["window_zone_unresolved"] = dict(yes=wu["yes"], no=wu["no"], unknown=wu["unknown"])
    md = ["# Part H summary (generated by scripts/build_part_h.py; do not edit)\n",
          "Units screened: %d. Status: %s.\n" % (len(srows), ", ".join("%s %d" % kv for kv in sorted(st.items()))),
          "Units read and coded: %d. Feature rows with one zone: %d (yes %d, no %d, unknown %d). "
          "Rows in the region whose zone is split: %d (yes %d, no %d, unknown %d).\n" % (
              len(reports), len(feats), w["yes"], w["no"], w["unknown"], len(unresolved), wu["yes"], wu["no"], wu["unknown"]),
          "## Rows by class (one zone | zone split)\n", "| class | rows | yes | no | unknown | split rows | split yes | split no | split unknown |",
          "|---|---|---|---|---|---|---|---|---|"]
    for c in CLASSES:
        a, b = js["by_class"][c], js["by_class_zone_unresolved"][c]
        md.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d |" % (c, a["rows"], a["yes"], a["no"], a["unknown"],
                                                                    b["rows"], b["yes"], b["no"], b["unknown"]))
    md.append("\n## Rows by zone (one zone)\n")
    md.append("| zone | rows | yes | no | unknown |")
    md.append("|---|---|---|---|---|")
    for z in ZONES:
        a = js["by_zone"][z]
        md.append("| %s | %d | %d | %d | %d |" % (z, a["rows"], a["yes"], a["no"], a["unknown"]))
    md.append("\nZone-split rows by zone pair: " + ", ".join("%s %d" % kv for kv in js["by_zone_unresolved"].items()) + ".\n")
    return "\n".join(md) + "\n", js


def main(out_dir=PART):
    out_dir = Path(out_dir)
    screens, coding, held = load()
    feats, unresolved, reports, srows = build_rows(screens, coding, held)
    b2.write_csv(out_dir / "features.csv", b2.FEATURE_FIELDS, feats)
    b2.write_csv(out_dir / "features_zone_unresolved.csv", b2.FEATURE_FIELDS, unresolved)
    b2.write_csv(out_dir / "reports.csv", b2.REPORT_FIELDS, reports)
    b2.write_csv(out_dir / "screen.csv", SCREEN_FIELDS, srows)
    b2.write_csv(out_dir / "held.csv", HELD_FIELDS, held)
    md, js = summarize(feats, unresolved, reports, srows, held)
    (out_dir / "summary.md").write_text(md, encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(js, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("screened %d, read %d, feature rows %d (+%d zone split), held %d" % (
        len(srows), len(reports), len(feats), len(unresolved), len(held)))


if __name__ == "__main__":
    out = PART
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
    main(out)
