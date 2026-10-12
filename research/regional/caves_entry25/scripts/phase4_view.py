#!/usr/bin/env python3
"""Exploratory view: the phase 1-4 merged inventory folded into the caves_entry25 lane (PLAN_AMENDMENT_PHASE4_2026-10-12.md).

Run from anywhere:  python3 -I -B research/regional/caves_entry25/scripts/phase4_view.py
The IAA-view method (PLAN_AMENDMENT_IAA_2026-10-11.md) rerun unchanged on merged_2026-10-12 (phases 1-4), with the
protected-material screen of the phase-4 amendment (section 5) applied to phase-4 rows before they are read. Reuses
the functions of scripts/iaa_view.py and scores with scripts/score.py, both imported unchanged. Reads committed
tables only. Writes phase4_units.csv, phase4_excluded.csv, phase4_unplaced.csv, phase4_scores.csv, phase4_summary.json
and phase4_view_2026-10-12.csv. Never writes caves.csv, scores.csv, aspect.csv, summary.json or any iaa_* output.

  --scan OUT   write the admitted rows that have no coding line (with their coding fields) to OUT and stop.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
REPO = LANE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(LANE / "scripts"))
import iaa_view as V  # noqa: E402  (IAA-view functions, unchanged)
import score as S  # noqa: E402  (frozen scoring functions, unchanged)
from build_caves import OUT_FIELDS  # noqa: E402

MERGED = REPO / "research/regional/haesi_features/merged_2026-10-12"
PHASE4 = REPO / "research/regional/haesi_features/phase4_2026-10-11"
INPUT_SHA = {  # PLAN_AMENDMENT_PHASE4 section 2
    "features_all.csv": "940e6c04b1ecd18c79a7c88a784a463d69056f70c6e31ad18e5a18c46866d65d",
    "report_groups.csv": "38b67f3c7095993287ac9da80eb229a9752d56ff7c27cb9bb3b1024f47da702f",
    "sites.csv": "5d7458016d7955cced5540d4307570879fbc5b2071d5f644e85d3cec0fcc16db",
}
PLACES_SHA = "315474bd3be8cce3e1776e119417e2444edd99e3f028c7413185302fc7663683"
MAPPED_UTC = "2026-10-12T04:52:30Z"  # first mapping of the in-box rows (scan), after amendment commit 9fad7f4
BOX_ZONES = ("Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT")  # the only zones that meet the box (amendment section 6)

# Amendment section 5.2-5.6
HELD_TERMS = re.compile(
    r"qumr[aâ]n|fe?s[hc]?kh?a|fashkha|qarant[au]l|quruntul|kuruntul|quarantania|temptation|nuwei|nueia?meh|nueima|"
    r"\b(?:duk|doq|dok)\b|\bq[ei]lt\b|\bkelt\b|\bp(?:e)?rat\b|k?h?oziba|st\.? george|"
    r"(?<![א-ת])[בהוכלמש]{0,2}(?:קומראן|קומרן|פשח'ה|צוקים|קרנטל|קלט|פרת)(?![א-ת])", re.I)
STRIP_TERMS = re.compile(r"sultan|סולטאן", re.I)
ALMIT = re.compile(r"almit|עלמית", re.I)
HELD_BOXES = {  # WGS 84 (lat_min, lat_max, lon_min, lon_max), conservative boxes around the places_v2 anchors
    "Qumran cliffs and marl terrace": (31.700, 31.790, 35.420, 35.475),
    "Jericho escarpment": (31.860, 31.915, 35.395, 35.438),
    "Wadi Qelt gorge": (31.825, 31.865, 35.315, 35.432),
}
HELD_PLACES = {"kh_qumran", "wadi_qumran", "ein_feshkha", "doq", "ain_duk", "nuweimeh", "choziba", "iv17_abu_saraj"}
STRIP_CENTRE, STRIP_M = (31.8717, 35.4446), 500.0
CODING_FIELDS = ["row_uid", "action", "target", "n_open", "open_basis", "facings", "facing_basis", "res", "pillar",
                 "pillar_kind", "pillar_pos", "pillar_basis", "terrace", "terrace_basis", "north", "north_basis", "piw",
                 "c1", "notes"]
VIEW_FIELDS = ["branch", "orientation", "ruleset", "count", "frozen_N", "frozen_k", "frozen_f", "frozen_m",
               "iaa1011_N", "iaa1011_k", "iaa1011_f", "iaa1011_m", "union_N", "union_k", "union_f", "union_m",
               "dfrozen_N", "dfrozen_k", "dfrozen_f", "dfrozen_m", "diaa_N", "diaa_k", "diaa_f", "diaa_m",
               "new_all_match_vs_frozen"]
EXCL_FIELDS = ["record_id", "phase", "report_id", "report_group", "feature_type", "site_name", "point_oig",
               "position_basis", "status", "reason"]
UNPLACED_FIELDS = ["row_uid", "phase", "report_id", "series", "volume", "pages", "site_name", "feature_type",
                   "count_zone", "coordinate_source"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def held_unit_ids():
    ids = set()
    for p in sorted(PHASE4.rglob("held.csv")):
        for r in V.read(p):
            for k in ("unit_id", "report_id", "id"):
                if r.get(k):
                    ids.add(r[k].strip())
    return ids


def haversine_m(a, b):
    import math
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


def protected(r, places, held_ids):
    """Amendment section 5, for phase-4 rows only. Returns (status, reason) or None. Uses ids, positions and terms."""
    if r["report_id"] in held_ids:
        return "held", "unit listed in a phase-4 held.csv (5.1)"
    text = " ".join((r["site_name"], r["feature_subtype"], r["quote"], r["coordinate_source"]))
    if ALMIT.search(r["site_name"] + " " + r["report_id"]):
        return "tier1-almit", "Kh. Almit: excluded, compared with nothing (5.5)"
    if re.match(r"ATQ41-", r["report_id"]):
        return "atiqot41", "Atiqot 41 is excluded whole (5.6)"
    if r["protected_strip"] == "yes" or STRIP_TERMS.search(text):
        return "protected-strip", "Tell es-Sultan north strip by flag or term (5.4)"
    if HELD_TERMS.search(text):
        return "held-area", "held cave area by term (5.2)"
    pt = None
    if r["lat"]:
        pt = (float(r["lat"]), float(r["lon"]))
    else:
        m = re.search(r"\(([a-z0-9_]+)\)", r["coordinate_source"])
        if m and m.group(1) in places:
            if m.group(1) in HELD_PLACES:
                return "held-area", f"placed only by held-area place {m.group(1)} (5.3)"
            p = places[m.group(1)]
            pt = (float(p["lat"]), float(p["lon"]))
    if pt:
        for name, (a, b, c, d) in HELD_BOXES.items():
            if a <= pt[0] <= b and c <= pt[1] <= d:
                return "held-area", f"point in the {name} safety box (5.3)"
        if haversine_m(pt, STRIP_CENTRE) <= STRIP_M:
            return "protected-strip", "point within 500 m of Tell es-Sultan (5.4)"
    return None


def in_held_box(u):
    if u.get("lat") in ("", None):
        return ""
    lat, lon = float(u["lat"]), float(u["lon"])
    return ";".join(n for n, (a, b, c, d) in HELD_BOXES.items() if a <= lat <= b and c <= lon <= d)


def load_coding():
    old = {r["row_uid"]: dict(r, _file="iaa_coding.csv") for r in V.read(LANE / "coded/iaa_coding.csv")}
    p = LANE / "coded/phase4_coding.csv"
    new = {r["row_uid"]: dict(r, _file="phase4_coding.csv") for r in V.read(p)} if p.exists() else {}
    both = set(old) & set(new)
    if both:
        raise SystemExit(f"rows coded twice: {sorted(both)}")
    return old, new


def build(scan_out=None):
    for name, h in INPUT_SHA.items():
        if sha(MERGED / name) != h:
            raise SystemExit(f"{name}: hash differs from the amendment's value")
    if sha(V.PLACES) != PLACES_SHA:
        raise SystemExit("places_v2.csv: hash differs")
    places = {r["place_id"]: r for r in V.read(V.PLACES)}
    held_ids = held_unit_ids()
    old_coding, new_coding = load_coding()
    coding = {**old_coding, **new_coding}
    features = V.read(MERGED / "features_all.csv")
    by_uid = {r["row_uid"]: r for r in features}
    # same-campaign carry-over (amendment section 4): (new report group, class) of rows coded same_source/merge on 11 Oct
    carry = {}
    for uid, c in old_coding.items():
        if c["action"] in ("same_source", "merge") and uid in by_uid:
            carry[(by_uid[uid]["report_group"], by_uid[uid]["feature_type"])] = (c["action"], c["target"], uid)
    lane = V.read(LANE / "caves.csv")
    lane_ids = {r["cave_id"] for r in lane}
    units, excluded, unplaced_list, scan = [], [], [], []
    unplaced, outside = Counter(), Counter()
    seen = set()
    for r in V.select_rows(features):
        p4 = r["phase"].startswith("4")
        pos = V.position(r, places)
        if pos is None:
            unplaced[f"{r['feature_type']}@{r['count_zone']}|phase{'4' if p4 else '1-3'}"] += 1
            if p4 and r["count_zone"] in BOX_ZONES:
                prot = protected(r, places, held_ids)
                if prot:
                    excluded.append(dict(record_id=r["row_uid"], phase=r["phase"], report_id=r["report_id"],
                                         report_group=r["report_group"], feature_type=r["feature_type"], site_name="",
                                         point_oig="", position_basis="unplaced", status=prot[0], reason=prot[1]))
                else:
                    unplaced_list.append({k: r[k] for k in UNPLACED_FIELDS if k in r} | {"row_uid": r["row_uid"]})
            continue
        x, y, prec, basis, own = pos
        inside, near = V.in_box(x, y, prec)
        if not (inside or near):
            outside[f"{r['feature_type']}|phase{'4' if p4 else '1-3'}"] += 1
            continue
        base = dict(record_id=r["row_uid"], phase=r["phase"], report_id=r["report_id"], report_group=r["report_group"],
                    feature_type=r["feature_type"], site_name=r["site_name"], point_oig=f"{x:.0f}/{y:.0f}",
                    position_basis=basis)
        if p4:
            prot = protected(r, places, held_ids)
            if prot:
                excluded.append(dict(base, site_name="", status=prot[0], reason=prot[1]))
                continue
        if not V.cave_word(r):
            excluded.append(dict(base, status="not admitted",
                                 reason="the coding does not call the feature a cave (PLAN 4.1(2))"))
            continue
        c = coding.get(r["row_uid"])
        if c is None:
            if scan_out is not None:
                scan.append(r)
                continue
            raise SystemExit(f"in-box row without a coding line: {r['row_uid']}")
        seen.add(r["row_uid"])
        cr = carry.get((r["report_group"], r["feature_type"]))
        if c["_file"] == "phase4_coding.csv" and cr and c["action"] == "add" and "different cave" not in c["notes"]:
            raise SystemExit(f"{r['row_uid']}: same campaign as {cr[2]} ({cr[0]}); code it so or say 'different cave'")
        if c["action"] in ("same_source", "merge"):
            for t in c["target"].split("|"):
                if t not in lane_ids:
                    raise SystemExit(f"{r['row_uid']}: target {t} not in caves.csv")
            excluded.append(dict(base, status="already in the lane" if c["action"] == "same_source" else "merged (stated identity)",
                                 reason=f"{c['action']} -> {c['target']}: {c['notes']}"))
            continue
        u = V.make_unit(r, c, x, y, prec, basis, own, inside, near)
        u["first_read_utc"] = V.MAPPED_UTC if c["_file"] == "iaa_coding.csv" else MAPPED_UTC
        u["phase"] = r["phase"]
        u["held_box_note"] = in_held_box(u) if not p4 else ""
        units.append(u)
    if scan_out is not None:
        with open(scan_out, "w", encoding="utf-8") as f:
            json.dump(scan, f, indent=1, ensure_ascii=False)
        print(f"scan: {len(scan)} admitted rows without a coding line -> {scan_out}")
        sys.exit(0)
    stale_new = set(new_coding) - seen
    if stale_new:
        raise SystemExit(f"phase4_coding lines for rows not admitted: {sorted(stale_new)}")
    V.flag_duplicates(units, lane)
    coverage = dict(unplaced=dict(sorted(unplaced.items())), outside_box=dict(sorted(outside.items())))
    return lane, units, excluded, unplaced_list, coverage, old_coding, seen, by_uid


def iaa1011_view():
    out = {}
    for r in V.read(LANE / "iaa_view_2026-10-11.csv"):
        out[(r["branch"], r["orientation"], r["ruleset"], r["count"])] = r
    return out


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--scan":
        build(scan_out=sys.argv[2])
    lane, units, excluded, unplaced_list, coverage, old_coding, seen, by_uid = build()
    plans = json.load(open(LANE / "coded/plan_measurements.json", encoding="utf-8"))["rows"]
    units_s = V.as_str(units)
    frozen_scores = V.score_all(lane, plans)
    frozen = S.summarise(lane, frozen_scores)
    committed = json.load(open(LANE / "summary.json", encoding="utf-8"))
    if frozen["counts"] != committed["counts"] or frozen["all_match_rows"] != committed["all_match_rows"]:
        raise SystemExit("the frozen scoring does not reproduce summary.json")
    p4_scores = V.score_all(units_s, plans)
    p4 = S.summarise(units_s, p4_scores)
    union = S.summarise(lane + units_s, frozen_scores + p4_scores)
    old = iaa1011_view()
    view = []
    for key in sorted(frozen["counts"]):
        b, o, rs = key.split("|")
        for part in ("rows", "min", "clusters"):
            f, u = frozen["counts"][key][part], union["counts"][key][part]
            i = old[(b, o, rs, part)]
            ik = {x: int(i[f"union_{x}"]) for x in ("N", "k", "f", "m")}
            if int(i["frozen_N"]) != f["N"] or int(i["frozen_k"]) != f["all-match"]:
                raise SystemExit("frozen N differs from iaa_view_2026-10-11.csv")
            new = sorted(set(union["all_match_rows"][key]) - set(frozen["all_match_rows"][key])) if part == "rows" else []
            view.append(dict(branch=b, orientation=o, ruleset=rs, count=part,
                             frozen_N=f["N"], frozen_k=f["all-match"], frozen_f=f["fail"], frozen_m=f["unknown"],
                             iaa1011_N=ik["N"], iaa1011_k=ik["k"], iaa1011_f=ik["f"], iaa1011_m=ik["m"],
                             union_N=u["N"], union_k=u["all-match"], union_f=u["fail"], union_m=u["unknown"],
                             dfrozen_N=u["N"] - f["N"], dfrozen_k=u["all-match"] - f["all-match"],
                             dfrozen_f=u["fail"] - f["fail"], dfrozen_m=u["unknown"] - f["unknown"],
                             diaa_N=u["N"] - ik["N"], diaa_k=u["all-match"] - ik["k"], diaa_f=u["fail"] - ik["f"],
                             diaa_m=u["unknown"] - ik["m"], new_all_match_vs_frozen=";".join(new)))
    # what changed against the 11 October IAA view
    prev_units = {r["cave_id"] for r in V.read(LANE / "iaa_units.csv")}
    prev_excl = {r["record_id"]: r["status"] for r in V.read(LANE / "iaa_excluded.csv")}
    now_units = {u["cave_id"] for u in units_s}
    now_excl = {e["record_id"]: e["status"] for e in excluded}
    changes = dict(
        units_new=sorted(now_units - prev_units),
        units_dropped=sorted(prev_units - now_units),
        excluded_new=sorted(set(now_excl) - set(prev_excl)),
        excluded_dropped=sorted(set(prev_excl) - set(now_excl)),
        dropped_reason={uid: ("version_role now " + by_uid[uid.split(":", 1)[1]]["version_role"]
                              if uid.split(":", 1)[1] in by_uid else "row missing")
                        for uid in sorted((prev_units - now_units) | {"IAA:" + k for k in set(prev_excl) - set(now_excl)})},
    )
    fields = OUT_FIELDS + ["edge", "phase", "held_box_note"]
    V.write(LANE / "phase4_units.csv", fields, units_s)
    V.write(LANE / "phase4_excluded.csv", EXCL_FIELDS, excluded)
    V.write(LANE / "phase4_unplaced.csv", UNPLACED_FIELDS, unplaced_list)
    V.write(LANE / "phase4_scores.csv", list(p4_scores[0].keys()), p4_scores)
    V.write(LANE / "phase4_view_2026-10-12.csv", VIEW_FIELDS, view)
    key = "B-PILLAR|cave|primary"
    p4_only = [u for u in units_s if u["phase"].startswith("4")]
    summary = dict(
        note="Exploratory view (PLAN_AMENDMENT_PHASE4_2026-10-12.md). The frozen counts (summary.json) and the 11 October IAA view are unchanged.",
        inputs=dict(INPUT_SHA, **{"places_v2.csv": PLACES_SHA}),
        rows_added=dict(caves=sum(u["row_kind"] == "cave" for u in units_s), clusters=sum(u["row_kind"] == "cluster" for u in units_s)),
        phase4_rows_added=dict(caves=sum(u["row_kind"] == "cave" for u in p4_only), clusters=sum(u["row_kind"] == "cluster" for u in p4_only)),
        rows_not_added=dict(Counter(e["status"] for e in excluded)),
        phase4_unplaced_in_box_zones=len(unplaced_list),
        changes_vs_iaa_2026_10_11=changes,
        coverage=coverage,
        headline=dict(frozen=frozen["counts"][key]["rows"], union=union["counts"][key]["rows"],
                      frozen_min=frozen["counts"][key]["min"], union_min=union["counts"][key]["min"]),
        union_N_rows=union["N_rows"], union_N_min=union["N_min"], union_cluster_records=union["cluster_records"],
        union_cluster_stated_members=union["cluster_stated_members"],
        added_by_clause=p4["counts"][key]["rows"]["by_clause"],
        union_all_match_rows=union["all_match_rows"],
    )
    with open(LANE / "phase4_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
        f.write("\n")
    h = summary["headline"]
    print(f"rows added: {summary['rows_added']} (phase 4: {summary['phase4_rows_added']}); not added: {summary['rows_not_added']}")
    print(f"B-PILLAR cave primary: frozen {h['frozen']['all-match']}/{h['frozen']['fail']}/{h['frozen']['unknown']} of {h['frozen']['N']}; "
          f"union {h['union']['all-match']}/{h['union']['fail']}/{h['union']['unknown']} of {h['union']['N']}")


if __name__ == "__main__":
    main()
