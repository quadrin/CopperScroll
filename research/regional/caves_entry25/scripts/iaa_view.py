#!/usr/bin/env python3
"""Exploratory view: the merged IAA inventory folded into the caves_entry25 lane (PLAN_AMENDMENT_IAA_2026-10-11.md).

Run from anywhere:  python3 -I -B research/regional/caves_entry25/scripts/iaa_view.py
Reads the committed caves.csv, summary.json and coded/plan_measurements.json, the merged IAA inventory
(research/regional/haesi_features/merged_2026-10-11/) and the hand coding coded/iaa_coding.csv. Scores with the
functions of scripts/score.py, imported unchanged. Writes iaa_units.csv, iaa_excluded.csv, iaa_scores.csv,
iaa_summary.json and iaa_view_2026-10-11.csv. Never writes caves.csv, scores.csv, aspect.csv or summary.json.
"""
import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from pyproj import Transformer

LANE = Path(__file__).resolve().parents[1]
REPO = LANE.parents[2]
MERGED = REPO / "research/regional/haesi_features/merged_2026-10-11"
PLACES = REPO / "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv"
sys.dont_write_bytecode = True
sys.path.insert(0, str(LANE / "scripts"))
import score as S  # noqa: E402  (frozen scoring functions, unchanged)
from build_caves import OUT_FIELDS  # noqa: E402

INPUT_SHA = {  # PLAN_AMENDMENT_IAA §2
    "features_all.csv": "2170f7fb15b097621e07648c128719f25e50e3550d5ec8756c08fca6267e455b",
    "report_groups.csv": "06085467541339b097fcd29a55a5d7e8d49ade829b7f8329a00f981e9624b89c",
    "sites.csv": "7e89ddce959869e8a960103e63417870d621edb5f7f1b0376b3d12f54450e87b",
}
CLASSES = ("cave_with_finds", "tomb_burial_cave")
BOX = (180000.0, 197000.0, 91000.0, 150000.0)  # PLAN §2, EPSG:28191
DUP_M = 50.0  # PLAN 4.2
CAVE = re.compile(r"\bcaves?\b|\bcaverns?\b|\bgrott(?:o|oes|os)\b|(?<![א-ת])[בהוכלמש]{0,2}מער(?:ה|ות|ת)(?![א-ת])", re.I)
SHELTER = re.compile(r"cave or (?:a )?rock[\s-]?shelter|rock[\s-]?shelter or (?:a )?cave", re.I)
W2O = Transformer.from_crs("EPSG:4326", "EPSG:28191", always_xy=True)
W2I = Transformer.from_crs("EPSG:4326", "EPSG:2039", always_xy=True)
MAPPED_UTC = "2026-10-11T17:55:40Z"  # first look at the in-box rows (scratch scan), after amendment commit 7e88f3d
VIEW_FIELDS = ["branch", "orientation", "ruleset", "count", "frozen_N", "frozen_k", "frozen_f", "frozen_m",
               "iaa_N", "iaa_k", "iaa_f", "iaa_m", "union_N", "union_k", "union_f", "union_m",
               "delta_N", "delta_k", "delta_f", "delta_m", "new_all_match"]


def sha(p):
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tier1(r):
    return bool(re.match(r"HA(28|29)-", r["report_id"])) or bool(re.search(r"almit|עלמית", r["site_name"], re.I))


def select_rows(rows):
    """Version rule (amendment §5): preferred or single version; an alternate only for a class the preferred lacks."""
    by = defaultdict(list)
    for r in rows:
        if r["counted"] == "yes" and r["feature_type"] in CLASSES:
            by[(r["report_group"], r["feature_type"])].append(r)
    out = []
    for key in sorted(by):
        rs = by[key]
        pref = [r for r in rs if r["version_role"] in ("single", "preferred")]
        out += pref if pref else rs
    return out


def position(r, places):
    """(x, y, precision_m, basis, own_point) in EPSG:28191, or None (amendment §4)."""
    if r["lat"]:
        x, y = W2O.transform(float(r["lon"]), float(r["lat"]))
        return x, y, float(r["precision_m"] or 0), "point", True
    m = re.search(r"\(([a-z0-9_]+)\)", r["coordinate_source"])
    if m and m.group(1) in places:
        p = places[m.group(1)]
        x, y = W2O.transform(float(p["lon"]), float(p["lat"]))
        return x, y, float(p["sigma_km"] or 0) * 1000.0, f"reader place {m.group(1)} (places_v2)", False
    return None


def in_box(x, y, prec):
    inside = BOX[0] <= x <= BOX[1] and BOX[2] <= y <= BOX[3]
    near = min(abs(x - BOX[0]), abs(x - BOX[1]), abs(y - BOX[2]), abs(y - BOX[3])) <= prec
    return inside, near


def cave_word(r):
    text = r["feature_subtype"] + " " + r["quote"]
    if r["feature_type"] == "cave_with_finds":
        text += " " + r["site_name"]
    return bool(CAVE.search(text))


def build():
    for name, h in INPUT_SHA.items():
        if sha(MERGED / name) != h:
            raise SystemExit(f"{name}: hash differs from the amendment's value")
    places = {r["place_id"]: r for r in read(PLACES)}
    coding = {r["row_uid"]: r for r in read(LANE / "coded/iaa_coding.csv")}
    lane = read(LANE / "caves.csv")
    lane_ids = {r["cave_id"] for r in lane}
    units, excluded, seen_uids = [], [], set()
    unplaced, outside = Counter(), Counter()
    for r in select_rows(read(MERGED / "features_all.csv")):
        pos = position(r, places)
        if pos is None:
            unplaced[f"{r['feature_type']}@{r['count_zone']}"] += 1
            continue
        x, y, prec, basis, own = pos
        inside, near = in_box(x, y, prec)
        if not (inside or near):
            outside[r["feature_type"]] += 1
            continue
        base = dict(record_id=r["row_uid"], report_id=r["report_id"], report_group=r["report_group"],
                    feature_type=r["feature_type"], site_name=r["site_name"],
                    point_oig=f"{x:.0f}/{y:.0f}", position_basis=basis)
        if not cave_word(r):
            excluded.append(dict(base, status="not admitted",
                                 reason="the IAA coding does not call the feature a cave (PLAN 4.1(2))"))
            continue
        c = coding.get(r["row_uid"])
        if c is None:
            raise SystemExit(f"in-box row without a hand-coding line: {r['row_uid']}")
        seen_uids.add(r["row_uid"])
        if c["action"] in ("same_source", "merge"):
            for t in c["target"].split("|"):
                if t not in lane_ids:
                    raise SystemExit(f"{r['row_uid']}: target {t} not in caves.csv")
            excluded.append(dict(base, status="already in the lane" if c["action"] == "same_source" else "merged (stated identity)",
                                 reason=f"{c['action']} -> {c['target']}: {c['notes']}"))
            continue
        units.append(make_unit(r, c, x, y, prec, basis, own, inside, near))
    missing = set(coding) - seen_uids
    if missing:
        raise SystemExit(f"coding lines for rows not in the box: {sorted(missing)}")
    flag_duplicates(units, lane)
    return lane, units, excluded, dict(unplaced=dict(sorted(unplaced.items())), outside_box=dict(sorted(outside.items())))


def make_unit(r, c, x, y, prec, basis, own, inside, near):
    n = r["n_features"].strip()
    plural = bool(re.search(r"\bcaves\b|\bcaverns\b|\bgrott(?:oes|os)\b|מערות", r["feature_subtype"] + " " + r["quote"], re.I))
    if n.isdigit() and int(n) >= 2:
        kind, count = "cluster", int(n)
    elif not n.isdigit() and plural:
        kind, count = "cluster", ""
    else:
        kind, count = "cave", ""
    c1 = "unknown" if (c["c1"] == "unknown" or SHELTER.search(r["feature_subtype"] + " " + r["quote"])) else ""
    lon, lat = float(r["lon"]) if r["lon"] else None, float(r["lat"]) if r["lat"] else None
    u = {k: "" for k in OUT_FIELDS}
    u.update(
        cave_id=f"IAA:{r['row_uid']}", name_number=f"{r['site_name']} ({r['feature_type']})",
        source_records=f"{r['series']} {r['volume']} ({r['year']}) p. {r['pages']}, {r['author']}; merged IAA inventory row {r['row_uid']}",
        other_ids=f"report group {r['report_group']}; site {r['site_id']}", lineage=f"IAA report {r['report_group']}",
        feature_type_source=r["feature_type"], row_kind=kind, cluster_count=count,
        coord_printed=r["map_ref_as_given"], crs_printed=r["grid"],
        precision_m=f"{prec:g}", coord_basis=basis, coord_ok="yes" if own else "",
        in_region="yes" if inside else "edge", region_basis="point" if own else "by description",
        n_openings=c["n_open"], openings_basis=c["open_basis"], opening_facings=c["facings"],
        facing_basis=c["facing_basis"], facing_resolution=c["res"], pillar=c["pillar"], pillar_kind=c["pillar_kind"],
        pillar_position=c["pillar_pos"], pillar_basis=c["pillar_basis"], terrace=c["terrace"],
        terrace_basis=c["terrace_basis"], northern_member=c["north"], northern_basis=c["north_basis"],
        published_plan="not opened (IAA coding only)", period_stated=r["period_as_given"], period_in_window=c["piw"],
        excavation_status=r["excavated_or_surveyed"], finds="", c1_override=c1,
        exposure="exposed-repo", first_read_utc=MAPPED_UTC, module="iaa",
        notes=("tier1_related; " if tier1(r) else "") + c["notes"])
    if own:
        ix, iy = W2I.transform(lon, lat)
        u.update(x_oig=round(x, 1), y_oig=round(y, 1), lat=round(lat, 6), lon=round(lon, 6), itm_x=round(ix, 1), itm_y=round(iy, 1))
    u["edge"] = "" if inside else "edge"
    u["_report_group"] = r["report_group"]
    return u


def flag_duplicates(units, lane):
    """PLAN 4.2: points within 50 m across field campaigns (lane rows with coord_ok; IAA rows of other report groups)."""
    lane_pts = [(r["cave_id"], float(r["x_oig"]), float(r["y_oig"])) for r in lane if r["x_oig"] and r["coord_ok"] == "yes"]
    flags = defaultdict(set)
    own = [u for u in units if u["x_oig"] != ""]
    for u in own:
        for cid, x, y in lane_pts:
            if math.hypot(u["x_oig"] - x, u["y_oig"] - y) <= DUP_M:
                flags[u["cave_id"]].add(cid)
    for i, a in enumerate(own):
        for b in own[i + 1:]:
            if a["_report_group"] != b["_report_group"] and math.hypot(a["x_oig"] - b["x_oig"], a["y_oig"] - b["y_oig"]) <= DUP_M:
                flags[a["cave_id"]].add(b["cave_id"])
                flags[b["cave_id"]].add(a["cave_id"])
    for u in units:
        u["possible_duplicate_of"] = "; ".join(sorted(flags.get(u["cave_id"], [])))


def score_all(rows, plans):
    out = []
    for row in rows:
        asp = S.aspect(row, plans)
        for b in S.BRANCHES:
            for o in S.ORIENTATIONS:
                for rs in S.RULESETS:
                    out.append(dict(cave_id=row["cave_id"], row_kind=row["row_kind"], branch=b, orientation=o, ruleset=rs,
                                    **S.score_row(row, asp, b, o, rs)))
    return out


def as_str(rows):
    return [{k: ("" if v is None else str(v)) for k, v in r.items()} for r in rows]


def main():
    lane, units, excluded, coverage = build()
    plans = json.load(open(LANE / "coded/plan_measurements.json", encoding="utf-8"))["rows"]
    units_s = as_str(units)
    frozen_scores = score_all(lane, plans)
    frozen = S.summarise(lane, frozen_scores)
    committed = json.load(open(LANE / "summary.json", encoding="utf-8"))
    if frozen["counts"] != committed["counts"] or frozen["all_match_rows"] != committed["all_match_rows"]:
        raise SystemExit("the frozen scoring does not reproduce summary.json")
    iaa_scores = score_all(units_s, plans)
    iaa = S.summarise(units_s, iaa_scores)
    union = S.summarise(lane + units_s, frozen_scores + iaa_scores)
    view = []
    for key in sorted(frozen["counts"]):
        b, o, rs = key.split("|")
        for part in ("rows", "min", "clusters"):
            f, i, u = frozen["counts"][key][part], iaa["counts"][key][part], union["counts"][key][part]
            new = sorted(set(union["all_match_rows"][key]) - set(frozen["all_match_rows"][key])) if part == "rows" else []
            view.append(dict(branch=b, orientation=o, ruleset=rs, count=part,
                             frozen_N=f["N"], frozen_k=f["all-match"], frozen_f=f["fail"], frozen_m=f["unknown"],
                             iaa_N=i["N"], iaa_k=i["all-match"], iaa_f=i["fail"], iaa_m=i["unknown"],
                             union_N=u["N"], union_k=u["all-match"], union_f=u["fail"], union_m=u["unknown"],
                             delta_N=u["N"] - f["N"], delta_k=u["all-match"] - f["all-match"], delta_f=u["fail"] - f["fail"],
                             delta_m=u["unknown"] - f["unknown"], new_all_match=";".join(new)))
    write(LANE / "iaa_units.csv", OUT_FIELDS + ["edge"], units_s)
    write(LANE / "iaa_excluded.csv", ["record_id", "report_id", "report_group", "feature_type", "site_name", "point_oig",
                                       "position_basis", "status", "reason"], excluded)
    write(LANE / "iaa_scores.csv", list(iaa_scores[0].keys()), iaa_scores)
    write(LANE / "iaa_view_2026-10-11.csv", VIEW_FIELDS, view)
    key = "B-PILLAR|cave|primary"
    summary = dict(
        note="Exploratory view (PLAN_AMENDMENT_IAA_2026-10-11.md). The frozen counts (summary.json) are unchanged.",
        inputs={k: v for k, v in INPUT_SHA.items()},
        iaa_rows_added=dict(caves=sum(u["row_kind"] == "cave" for u in units), clusters=sum(u["row_kind"] == "cluster" for u in units)),
        iaa_rows_not_added=dict(Counter(e["status"] for e in excluded)),
        coverage=coverage,
        headline=dict(frozen=frozen["counts"][key]["rows"], union=union["counts"][key]["rows"],
                      frozen_min=frozen["counts"][key]["min"], union_min=union["counts"][key]["min"]),
        union_N_rows=union["N_rows"], union_N_min=union["N_min"], union_cluster_records=union["cluster_records"],
        union_cluster_stated_members=union["cluster_stated_members"],
        iaa_by_clause=iaa["counts"][key]["rows"]["by_clause"],
        union_all_match_rows=union["all_match_rows"],
    )
    with open(LANE / "iaa_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
        f.write("\n")
    h = summary["headline"]
    print(f"IAA rows added: {summary['iaa_rows_added']}; not added: {summary['iaa_rows_not_added']}")
    print(f"B-PILLAR cave primary: frozen {h['frozen']['all-match']}/{h['frozen']['fail']}/{h['frozen']['unknown']} of {h['frozen']['N']}; "
          f"union {h['union']['all-match']}/{h['union']['fail']}/{h['union']['unknown']} of {h['union']['N']}")


def write(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
