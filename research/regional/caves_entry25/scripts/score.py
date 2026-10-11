#!/usr/bin/env python3
"""Score every row of caves.csv against the clauses of entry 25 (PLAN.md sections 1, 4.3, 5, 6).

Run from anywhere:  python3 -I -B research/regional/caves_entry25/scripts/score.py
Reads caves.csv and coded/plan_measurements.json; uses the frozen aspect rule's functions read-only
(research/preregistration/entry25_iv17_rules/check_rules.py with rules.json). Writes scores.csv, aspect.csv and
summary.json. B-GATE (Allegro's Temple reading) is not a cave and is not scored.
"""
import csv
import importlib.util
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
REPO = LANE.parents[2]
RULES_DIR = REPO / "research/preregistration/entry25_iv17_rules"
spec = importlib.util.spec_from_file_location("check_rules", RULES_DIR / "check_rules.py")
CR = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CR)
RULES = CR.load_rules(RULES_DIR / "rules.json")
SECTORS = CR.east_sectors(RULES)  # primary, eight-wind, sunrise-arc, ne-e-se

BRANCHES = ["B-PILLAR", "B-TERRACE"]
ORIENTATIONS = ["cave", "both-mouths"]
RULESETS = ["primary", "s_open_ge2", "s_singular_unknown", "s_pillar_between"]
M, F, U = "match", "fail", "unknown"

# s_pillar_between (PLAN 5): the pillar's recorded position, classified by hand for every row with pillar = yes.
PILLAR_BETWEEN = {
    "A41:III/3": F,          # at the entrance of the upper level (the openings are on two levels)
    "A41:III/11": M,         # between the two openings
    "A41:IV/11": F,          # south-west end of the hall
    "A41:IV/17": M,          # between the northern and southern spaces and openings
    "A41:V/49": U,           # position not tied to the openings in the record
    "A41:V/50": F,           # interior rock pillar, not between the openings
    "A41:VI/46": F,          # seven pillars inside dividing sub-spaces (one mouth)
    "A41:XII/53": M,         # in the opening, dividing it into two parts
    "REPO:TwinCave": M,      # separating the northern and southern units
    "ASI:83/12-70": U,       # position not stated
    "WB:E253": U,            # position not stated
    "ASI:109/4-107-burial": F,  # in the facade between the entrance vault and a small inner chamber
    "ASI:109/7-98-C27": F,   # in the later blocking wall at the single entrance
    "ASI:109/7-98-C48": M,   # at the opening, between the entry passage and the walled part
}


def word_arc(word, res):
    return CR.word_interval(RULES, word, int(res or 4))


def verdicts(arc):
    return {k: CR.verdict(arc, sec) for k, sec in SECTORS.items()}


def plan_mouth_arc(pm, mouth):
    import math as _m
    north = [pm["north_tip_px"][0] - pm["north_tail_px"][0], pm["north_tip_px"][1] - pm["north_tail_px"][1]]
    mpp = pm["metres_per_px"]
    p1, p2, inner = mouth["p1_px"], mouth["p2_px"], mouth["interior_px"]
    normal = CR.outward_normal(p1, p2, inner)
    az = CR.frame_azimuth(list(normal), north, pm["y_axis"])
    chord_m = _m.hypot(p2[0] - p1[0], p2[1] - p1[1]) * mpp
    r = CR.endpoint_radius_m(RULES, metres_per_px=mpp)
    n = CR.north_allowance(RULES, pm["north_case"])
    unc = RULES["aspect_rule"]["uncertainty"]
    d = unc["distortion_deg"]["scanned_or_printed"]
    e = unc["north_arrow_endpoint"]["raster_px"]
    arrow_len = _m.hypot(*north)
    h = CR.mouth_half_width(chord_m, r, arrow_len, e, d, n)
    return CR.interval(az, h), dict(azimuth=round(az, 1), chord_m=round(chord_m, 2), half_width=round(h, 1) if math.isfinite(h) else "full")


def aspect(row, plans):
    """Return {level: (arc or None, verdict-by-sector, basis)} for levels 'cave' and 'both-mouths'."""
    cid = row["cave_id"]
    fac = row["opening_facings"].strip()
    res = row["facing_resolution"] or 4
    n_open = int(row["n_openings"]) if row["n_openings"] not in ("", None) else None
    out = {}
    if cid in plans:
        pm = plans[cid]
        mouths = pm.get("mouths", {})
        mouth_v, extra = [], {}
        for key, m in mouths.items():
            if key == "whole_opening":
                arc, info = plan_mouth_arc(pm, m)
                extra["facade (whole opening)"] = (arc, info)
                continue
            if m.get("measurable") is False:
                mouth_v.append(CR.NOT_MEASURABLE)
            else:
                arc, info = plan_mouth_arc(pm, m)
                extra[key] = (arc, info)
                mouth_v.append(CR.verdict(arc, SECTORS["primary"]))
        both = CR.combine_mouths(mouth_v)
        out["both-mouths"] = (None, {k: both for k in SECTORS} if both in (CR.NOT_MEASURABLE, CR.SILENT) else
                              {k: CR.combine_mouths([CR.verdict(extra[m][0], SECTORS[k]) if m in extra else CR.NOT_MEASURABLE
                                                     for m in mouths if m != "whole_opening"]) for k in SECTORS},
                              "plan (" + "; ".join(f"{k}: az {v[1]['azimuth']}, h {v[1]['half_width']}" for k, v in extra.items() if k != "facade (whole opening)") + ")")
        # cave level: a record word wins (used directly); otherwise hull(facade, mean of mouths) needs every mouth
        if fac.startswith("cave:"):
            arc = word_arc(fac.split(":")[1], res)
            out["cave"] = (arc, verdicts(arc), f"word '{fac.split(':')[1]}' at {res}-point")
        else:
            out["cave"] = (None, {k: CR.NOT_MEASURABLE for k in SECTORS}, "plan: not every mouth measurable, so the cave level is not measurable")
        out["plan_extra"] = extra
        return out
    if not fac or fac == "plan":
        nm = CR.NOT_MEASURABLE if (n_open is not None and n_open < 2) else CR.SILENT
        out["both-mouths"] = (None, {k: nm for k in SECTORS}, "no mouth facing" if nm == CR.SILENT else "fewer than two mouths")
        out["cave"] = (None, {k: CR.SILENT for k in SECTORS}, "no facing in the record")
        return out
    parts = [p.split(":") for p in fac.split(";")]
    if len(parts) == 1 and parts[0][0] == "cave":
        arc = word_arc(parts[0][1], res)
        out["cave"] = (arc, verdicts(arc), f"word '{parts[0][1]}' at {res}-point")
        nm = CR.NOT_MEASURABLE if (n_open is not None and n_open < 2) else CR.SILENT
        out["both-mouths"] = (None, {k: nm for k in SECTORS}, "a cave-level word gives no mouth facing" if nm == CR.SILENT else "fewer than two mouths")
        return out
    centres = RULES["aspect_rule"]["uncertainty"]["compass_word"]["centres_deg"]
    # a mouth whose record word is not a compass word (e.g. 'up' for a roof opening) has no horizontal facing: silent
    arcs = [word_arc(w, res) if w in centres else None for _, w in parts]
    known = len(arcs)
    total = max(known, n_open or 0)
    mouth_verdicts = {k: [CR.verdict(a, sec) if a is not None else CR.SILENT for a in arcs] + [CR.SILENT] * (total - known)
                      for k, sec in SECTORS.items()}
    out["both-mouths"] = (None, {k: CR.combine_mouths(v) for k, v in mouth_verdicts.items()},
                          "mouth words: " + ", ".join(w for _, w in parts) + (f" (+{total - known} silent)" if total > known else ""))
    if total == 1 and arcs[0] is not None:
        out["cave"] = (arcs[0], verdicts(arcs[0]), "single mouth word")
    elif total == 1:
        out["cave"] = (None, {k: CR.SILENT for k in SECTORS}, "the only mouth word is not a compass word")
    else:
        out["cave"] = (None, {k: CR.NOT_MEASURABLE for k in SECTORS}, "two or more mouths without positions: facade normal unknown")
    return out


def c4_from(v):
    return {CR.PASS: M, CR.FAIL: F}.get(v, U)


def score_row(row, asp, branch, orient, rs):
    c1 = U if row["c1_override"] == "unknown" else M
    if branch == "B-PILLAR":
        p = row["pillar"]
        c2 = M if p == "yes" else F if p == "no" else U
        if rs == "s_pillar_between" and p == "yes":
            c2 = PILLAR_BETWEEN.get(row["cave_id"], U)
    else:
        t = row["terrace"]
        c2 = M if t == "yes" else F if t == "no" else U
    n = int(row["n_openings"]) if row["n_openings"] != "" else None
    singular = row["openings_basis"].startswith("singular description")
    if rs == "s_singular_unknown" and singular:
        n = None
    if n is None:
        c3 = U
    elif rs == "s_open_ge2":
        c3 = M if n >= 2 else F
    else:
        c3 = M if n == 2 else F
    vd = asp[orient][1]["primary"]
    c4 = c4_from(vd)
    if row["northern_member"] == "decided" and (n is None or n >= 2):
        c5 = M
    elif n is not None and n < 2:
        c5 = F
    else:
        c5 = U
    clauses = [c1, c2, c3, c4, c5]
    result = "fail" if F in clauses else "all-match" if all(c == M for c in clauses) else "unknown"
    failing = ",".join(f"C{i + 1}" for i, c in enumerate(clauses) if c == F)
    return dict(c1=c1, c2=c2, c3=c3, c4=c4, c4_verdict=vd, c5=c5, result=result, n_match=clauses.count(M),
                n_fail=clauses.count(F), n_unknown=clauses.count(U), failing=failing)


def components(rows):
    parent = {r["cave_id"]: r["cave_id"] for r in rows}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for r in rows:
        for o in filter(None, (s.strip() for s in r["possible_duplicate_of"].split(";"))):
            if o in parent:
                parent[find(r["cave_id"])] = find(o)
    groups = defaultdict(list)
    for r in rows:
        groups[find(r["cave_id"])].append(r["cave_id"])
    return list(groups.values())


def main():
    rows = list(csv.DictReader(open(LANE / "caves.csv", encoding="utf-8")))
    plans = json.load(open(LANE / "coded/plan_measurements.json", encoding="utf-8"))["rows"]
    scores, aspects = [], []
    for row in rows:
        asp = aspect(row, plans)
        for lvl in ORIENTATIONS:
            arc, vs, basis = asp[lvl]
            aspects.append(dict(cave_id=row["cave_id"], level=lvl, interval=(arc.as_list() if arc else ""), basis=basis,
                                primary=vs["primary"], eight_wind=vs["eight-wind"], sunrise_arc=vs["sunrise-arc"], ne_e_se=vs["ne-e-se"]))
        for key, (arc, info) in asp.get("plan_extra", {}).items():
            vs = verdicts(arc)
            aspects.append(dict(cave_id=row["cave_id"], level=f"plan sensitivity: {key}", interval=arc.as_list(), basis=json.dumps(info),
                                primary=vs["primary"], eight_wind=vs["eight-wind"], sunrise_arc=vs["sunrise-arc"], ne_e_se=vs["ne-e-se"]))
        for b in BRANCHES:
            for o in ORIENTATIONS:
                for rs in RULESETS:
                    s = score_row(row, asp, b, o, rs)
                    scores.append(dict(cave_id=row["cave_id"], row_kind=row["row_kind"], branch=b, orientation=o, ruleset=rs, **s))
    with open(LANE / "scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(scores[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(scores)
    with open(LANE / "aspect.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(aspects[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(aspects)
    summary = summarise(rows, scores)
    json.dump(summary, open(LANE / "summary.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    p = summary["counts"]["B-PILLAR|cave|primary"]
    print(f"scores.csv {len(scores)} rows; B-PILLAR cave primary: k={p['rows']['all-match']} f={p['rows']['fail']} m={p['rows']['unknown']} of {p['rows']['N']}")


RANK = {"all-match": 0, "unknown": 1, "fail": 2}


def summarise(rows, scores):
    caves = [r for r in rows if r["row_kind"] == "cave"]
    clusters = [r for r in rows if r["row_kind"] == "cluster"]
    comps = components(caves)
    by = defaultdict(dict)
    for s in scores:
        by[(s["branch"], s["orientation"], s["ruleset"])][s["cave_id"]] = s
    out = {"N_rows": len(caves), "N_min": len(comps), "cluster_records": len(clusters),
           "cluster_stated_members": sum(int(r["cluster_count"]) for r in clusters if r["cluster_count"] not in ("", None)),
           "cluster_records_without_count": sum(1 for r in clusters if r["cluster_count"] in ("", None)),
           "N_min_rule": "a merged group of possible duplicates counts once; its result is the best of its members (all-match > unknown > fail) and its clause value per clause the best of its members (match > unknown > fail) (AMENDMENT_1, item 6)",
           "counts": {}, "all_match_rows": {}}
    for (b, o, rs), d in sorted(by.items()):
        key = f"{b}|{o}|{rs}"
        rc = Counter(d[r["cave_id"]]["result"] for r in caves)
        clause = {c: dict(Counter(d[r["cave_id"]][c] for r in caves)) for c in ("c1", "c2", "c3", "c4", "c5")}
        mc = Counter()
        mclause = {c: Counter() for c in ("c1", "c2", "c3", "c4", "c5")}
        for g in comps:
            best = min((d[i]["result"] for i in g), key=RANK.get)
            mc[best] += 1
            for c in mclause:
                vals = [d[i][c] for i in g]
                mclause[c][M if M in vals else U if U in vals else F] += 1
        cl = Counter(d[r["cave_id"]]["result"] for r in clusters)
        out["counts"][key] = {
            "rows": {"N": len(caves), "all-match": rc["all-match"], "fail": rc["fail"], "unknown": rc["unknown"], "by_clause": clause},
            "min": {"N": len(comps), "all-match": mc["all-match"], "fail": mc["fail"], "unknown": mc["unknown"],
                    "by_clause": {c: dict(v) for c, v in mclause.items()}},
            "clusters": {"N": len(clusters), "all-match": cl["all-match"], "fail": cl["fail"], "unknown": cl["unknown"]},
        }
        out["all_match_rows"][key] = sorted(r["cave_id"] for r in caves if d[r["cave_id"]]["result"] == "all-match")
    return out


if __name__ == "__main__":
    main()
