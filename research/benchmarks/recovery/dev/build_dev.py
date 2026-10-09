"""Build the development batch from source_records.json.

Writes dev-NNN.json (cases), key.json (answers, public for the dev batch only) and
restore.json (the values removed by each degradation, for the ablation run).

Positions: grid bearing in degrees clockwise from ITM grid north and distance in
metres, computed here from the printed map references (the same arithmetic as the
Koh.lit packet `geom`). Where a case uses the survey's own words instead, the
position keeps the words (kind "words") and no bearing.

Run: python3 -I research/benchmarks/recovery/dev/build_dev.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = json.loads((HERE / "source_records.json").read_text(encoding="utf-8"))

ENTRANCE_Q = "Which side of the chosen feature has its entrance?"
ENTRANCE_4 = ["north", "east", "south", "west", "unknown"]
OPENING_8 = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west", "unknown"]
SIDE_4 = ["north", "east", "south", "west", "unknown"]


def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(obj) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def geom(ref, pt):
    dx, dy = pt[0] - ref[0], pt[1] - ref[1]
    return round(math.degrees(math.atan2(dx, dy)) % 360, 1), round(math.hypot(dx, dy), 1)


def grid_candidate(src, site, ref_xy, relative_to, precision=1, date=None, note=None):
    r = SRC[src]["sites"][site]
    b, d = geom(ref_xy, r["map_ref"])
    return {"site": f"{src}:{site}", "features": {
        "type": r["type"],
        "position": {"bearing_deg": b, "distance_m": d, "relative_to": relative_to, "kind": "plan",
                     "precision_m": precision},
        "opening": r.get("opening"),
        "date": date or r.get("date", "U"),
        "notes": note or f"survey site {site}; position computed from its printed map reference"}}


def words_candidate(src, site, direction, distance, relative_to, note):
    r = SRC[src]["sites"][site]
    return {"site": f"{src}:{site}", "features": {
        "type": r["type"],
        "position": {"bearing_deg": None, "distance_m": distance, "relative_to": relative_to, "kind": "words",
                     "direction": direction},
        "opening": r.get("opening"),
        "date": r.get("date", "U"),
        "notes": note}}


QANA_REF = SRC["qana"]["sites"]["29"]["map_ref"]
DUD_REF = SRC["dudaim"]["sites"]["9"]["map_ref"]
ZAAQ_REF = SRC["zaaq"]["reference"]["map_ref"]
AHI_REF = SRC["ahihud"]["sites"]["9"]["map_ref"]
DAB_REF = SRC["dabburiya"]["sites"]["3"]["map_ref"]

CTX = {
    "qana": ("A farmed slope below an ancient village in a fertile valley, with rock-cut burial caves that have hewn "
             "forecourts, cisterns, shafts, quarries and animal pens. Candidate positions are grid bearings (degrees "
             "clockwise from grid north) and distances in metres from a point on the wall remains at the village's "
             "southern edge (relative_to: boundary_wall), computed from the survey's map references. The survey dates "
             "no single feature, so every date is U."),
    "dudaim": ("Low chalk hills cut by seasonal streams in a semi-arid zone, with isolated farms, field watchtowers and "
               "rock-cut cisterns. Candidate positions are grid bearings and distances in metres from a farm "
               "(relative_to: farm), computed from the survey's map references. Target window: the Byzantine period or "
               "earlier. D = dated to the window or earlier (sherds of the window found at the feature, or its building "
               "style); L = securely later; U = undated."),
    "zaaq": ("A ruined village on low chalk hills, with cave dwellings, courtyards, cisterns, wells, an olive press, "
             "hiding refuges and later village buildings. Candidate positions are grid bearings and distances in metres "
             "from the map reference that the report gives for the ruin's survey (relative_to: ruin), computed from "
             "the survey's map references. The features are not dated one by one (U)."),
    "ahihud": ("Two low wooded hills beside a small alluvial valley, with ashlar quarries, winepresses, caves, rock-cut "
               "installations and two limekilns. Candidate positions are grid bearings and distances in metres from one "
               "of the limekilns (relative_to: kiln), computed from the survey's map references. Undated (U)."),
    "dabburiya_cave": ("A quarried limestone spur at the foot of a high mountain, with caves opened by quarrying, terrace "
                       "walls, a winepress and a cistern. Positions are measured from the cave in the quarry whose mouth "
                       "faces north (relative_to: cave_3). Where the report says a cave's map reference is not marked "
                       "on its map, the report's words are used (kind: words); otherwise positions are computed from map "
                       "references. Undated (U)."),
    "dabburiya_area": ("A quarried limestone spur at the foot of a high mountain, with caves opened by quarrying, terrace "
                       "walls, a winepress and a cistern. Positions are the report's own words for where each feature lies "
                       "in the surveyed field (relative_to: survey_area), or relative to another cave where the report "
                       "says so. Undated (U)."),
}

Q = "qana"
INSTR_QANA_W200 = "In the tomb with the hewn forecourt, west of the wall at the edge of the village, at two hundred cubits."
INSTR_QANA_W120 = "In the tomb with the hewn forecourt, west of the wall at the edge of the village, at one hundred and twenty cubits."
INSTR_QANA_E400 = "In the tomb with the hewn forecourt, east of the wall at the edge of the village, at four hundred cubits."
INSTR_DUD_FULL = "In the watchtower east of the farm, at twelve hundred cubits."
INSTR_DUD_NODIR = "In the watchtower of the farm, at twelve hundred cubits."
INSTR_AHI_FULL = "In the cave east of the kiln, at three hundred cubits."
INSTR_AHI_NODIR = "In the cave of the kiln, at three hundred cubits."


def qana(site):
    return grid_candidate(Q, site, QANA_REF, "boundary_wall",
                          note=f"survey site {site}; position from its printed map reference")


def dud(site, date=None):
    return grid_candidate("dudaim", site, DUD_REF, "farm", date=date)


def zaaq(site):
    return grid_candidate("zaaq", site, ZAAQ_REF, "ruin", precision=10)


def ahi(site):
    return grid_candidate("ahihud", site, AHI_REF, "kiln")


def dab(site):
    return grid_candidate("dabburiya", site, DAB_REF, "cave_3")


# Each spec: candidates (as built, before shuffling), true site, degradations as
# (name, kind, details). Degradations are applied to the built case below.
SPECS = [
    {"n": 1, "src": Q, "ctx": "qana", "instruction": INSTR_QANA_W200,
     "cands": [qana("21"), qana("20"), qana("28"), qana("16"), qana("23")], "true": "qana:20",
     "q": ENTRANCE_Q, "opts": ENTRANCE_4, "w": "east", "answer": "true",
     "why": "Site 20 is the only tomb west of the wall remains within 80-120 m (200 cubits at 0.40-0.60 m); its opening is on its eastern side.",
     "degr": []},
    {"n": 2, "src": Q, "ctx": "qana", "instruction": INSTR_QANA_W120,
     "cands": [qana("21"), qana("22"), qana("23"), qana("28"), qana("20")], "true": "qana:22",
     "q": ENTRANCE_Q, "opts": ENTRANCE_4, "w": "north", "answer": "insufficient",
     "why": ("Written from site 22 (58 m, opening north). Without the opening, sites 21, 22 and 28 are all tombs west of "
             "the wall at 48-72 m. Even with it, sites 21 (70 m) and 22 (58 m) both fit: the cubit range cannot separate them."),
     "degr": [("instruction_opening_missing", "instruction",
               INSTR_QANA_W120[:-1] + "; its entrance is on the north.")]},
    {"n": 3, "src": Q, "ctx": "qana", "instruction": INSTR_QANA_E400,
     "cands": [qana("16"), qana("20"), qana("14"), qana("28")], "true": "qana:34",
     "q": ENTRANCE_Q, "opts": ENTRANCE_4, "w": "west", "answer": "none",
     "why": ("Written from site 34 (199 m at 65 deg, opening west), which is left out. Site 16 (191 m at 100 deg) is another "
             "tomb east of the wall at the same distance; it fits the instruction but is not the feature."),
     "degr": [("one_candidate_unrecorded", "add_candidate", qana("34"))]},
    {"n": 4, "src": "dudaim", "ctx": "dudaim", "instruction": INSTR_DUD_NODIR,
     "cands": [dud("12"), dud("14"), dud("15"), dud("17"), dud("21")], "true": "dudaim:14",
     "q": "On which side of the farm does the chosen feature stand?", "opts": SIDE_4, "w": "east", "answer": "true",
     "why": ("Site 14 (554 m at 80 deg) and site 12 (526 m at 113 deg) are the only towers at 480-720 m; site 12 is "
             "attributed to the British Mandate (L). Site 14 lies east of the farm."),
     "degr": [("instruction_direction_missing", "instruction", INSTR_DUD_FULL)]},
    {"n": 5, "src": "dudaim", "ctx": "dudaim", "instruction": INSTR_DUD_NODIR,
     "cands": [dud("12", date="U"), dud("14"), dud("15"), dud("17"), dud("21")], "true": "dudaim:14",
     "q": "On which side of the farm does the chosen feature stand?", "opts": SIDE_4, "w": "east", "answer": "insufficient",
     "why": ("With the Mandate attribution of site 12 removed (U), sites 12 and 14 are both towers east of the farm at "
             "480-720 m, so the instruction cannot choose between them."),
     "degr": [("instruction_direction_missing", "instruction", INSTR_DUD_FULL),
              ("date_unknown", "replace_feature", {"site": "dudaim:12", "field": "date", "original": "L"})]},
    {"n": 6, "src": "dudaim", "ctx": "dudaim", "instruction": INSTR_DUD_NODIR,
     "cands": [dud("12"), dud("15"), dud("17"), dud("21")], "true": "dudaim:14",
     "q": "On which side of the farm does the watchtower of the instruction stand?", "opts": SIDE_4, "w": "east",
     "answer": "none",
     "why": ("Written from site 14, which is left out. The only other tower at 480-720 m is site 12, attributed to "
             "the British Mandate (L); the rest lie outside the distance band."),
     "degr": [("instruction_direction_missing", "instruction", INSTR_DUD_FULL),
              ("one_candidate_unrecorded", "add_candidate", dud("14"))]},
    {"n": 7, "src": "zaaq", "ctx": "zaaq",
     "instruction": "In the building of fieldstones on the slope of the hill, south of the ruin, at five hundred cubits.",
     "cands": [zaaq("2"), zaaq("20"), zaaq("24"), zaaq("28"), zaaq("29")], "true": "zaaq:2",
     "q": ENTRANCE_Q, "opts": ENTRANCE_4, "w": "unknown", "answer": "true",
     "why": ("The report places site 2 'c. 200 m south of the ruin' and the instruction repeats that. Its map reference "
             "lies 283 m at 125 deg from the report's own map reference for the ruin, so the record and the words "
             "disagree; no other building lies south. The report records no entrance side."),
     "degr": []},
    {"n": 8, "src": "zaaq", "ctx": "zaaq", "instruction": "In the cave east of the ruin, at seven hundred cubits.",
     "cands": [zaaq("12"), zaaq("13"), zaaq("15"), zaaq("18"), zaaq("21"), zaaq("23")], "true": "zaaq:21",
     "q": ENTRANCE_Q, "opts": ENTRANCE_4, "w": "unknown", "answer": "insufficient",
     "why": ("Written from site 21 (322 m at 79 deg). Six caves lie east of the ruin at 280-420 m; the instruction names "
             "nothing else that separates them. The report gives no entrance side for site 21's cave."),
     "degr": []},
    {"n": 9, "src": "ahihud", "ctx": "ahihud", "instruction": INSTR_AHI_NODIR,
     "cands": [ahi("7"), ahi("14"), ahi("16"), ahi("20"), ahi("5")], "true": "ahihud:16",
     "q": "Which way does the opening of the chosen feature face?", "opts": OPENING_8, "w": "north-east",
     "answer": "insufficient",
     "why": ("Written from site 16 (150 m at 49 deg). Without the direction, site 7 (177 m, west) also lies at "
             "120-180 m; site 20 has no recorded distance in this case. Its opening faces north-east."),
     "degr": [("instruction_direction_missing", "instruction", INSTR_AHI_FULL),
              ("distance_missing", "replace_feature", {"site": "ahihud:20", "field": "position.distance_m"})]},
    {"n": 10, "src": "dabburiya", "ctx": "dabburiya_cave",
     "instruction": "In the great cave south of the cave in the quarry, at twenty cubits.",
     "cands": [words_candidate("dabburiya", "4", "southeast", 10, "cave_3",
                               "survey site 4; the report places it c. 10 m southeast of the north-facing cave and "
                               "says its map reference is not marked on the map"),
               dab("6"), dab("8"), dab("10")], "true": "dabburiya:4",
     "q": ENTRANCE_Q, "opts": ENTRANCE_4, "w": "east", "answer": "insufficient",
     "why": ("Site 4 is the large cave c. 10 m southeast of cave 3. A cardinal 'south' cannot be tested against a verbal "
             "south-east (quadrant edge), and no plan position exists: the report says site 4 is not marked on its map. "
             "Its opening apparently faces east."),
     "degr": []},
    {"n": 11, "src": "dabburiya", "ctx": "dabburiya_area",
     "instruction": "In the cave in the west of the field, whose mouth opens to the south.",
     "cands": [words_candidate("dabburiya", "3", "northeast", None, "survey_area",
                               "survey site 3; in the northern part of the quarry, which lies in the area's north-east corner"),
               words_candidate("dabburiya", "8", "west", None, "survey_area", "survey site 8"),
               words_candidate("dabburiya", "6", "northeast", None, "survey_area",
                               "survey site 6; in the south-east corner of the quarry, in the area's north-east corner"),
               words_candidate("dabburiya", "4", "southeast", 10, "cave_3", "survey site 4; placed from another cave"),
               {"site": "dabburiya:10", "features": {"type": SRC["dabburiya"]["sites"]["10"]["type"],
                                                     "position": {"bearing_deg": None, "distance_m": None,
                                                                  "relative_to": "survey_area", "kind": "none"},
                                                     "opening": None, "date": "U",
                                                     "notes": "survey site 10; the report gives no words for its place"}}],
     "true": "dabburiya:8",
     "q": ENTRANCE_Q, "opts": ENTRANCE_4, "w": "south", "answer": "true",
     "why": "Site 8 is the cave in the western part of the survey area whose opening faces south; the other caves open north or east.",
     "degr": []},
    {"n": 12, "src": "ahihud", "ctx": "ahihud", "instruction": INSTR_AHI_FULL,
     "cands": [ahi("7"), ahi("13"), ahi("16"), ahi("20"), ahi("23")], "true": "ahihud:16",
     "q": "Which way does the opening of the chosen feature face?", "opts": OPENING_8, "w": "north-east", "answer": "true",
     "why": "Site 16 is the only cave east of the kiln at 120-180 m. Site 7 lies west, so its missing distance does not matter.",
     "degr": [("distance_missing", "replace_feature", {"site": "ahihud:7", "field": "position.distance_m"})]},
]


def get_field(feats, dotted):
    cur = feats
    parts = dotted.split(".")
    for p in parts[:-1]:
        cur = cur[p]
    return cur, parts[-1]


def build():
    cases, keys, restore = [], [], {}
    for spec in SPECS:
        cid = f"dev-{spec['n']:03d}"
        cands = copy.deepcopy(spec["cands"])
        random.Random(1000 + spec["n"]).shuffle(cands)
        id_of = {}
        out_cands = []
        for i, c in enumerate(cands, 1):
            id_of[c["site"]] = f"c{i}"
            out_cands.append({"id": f"c{i}", "features": c["features"]})
        ops, names = {}, []
        for name, kind, detail in spec["degr"]:
            names.append(name)
            if kind == "instruction":
                ops[name] = [{"op": "replace", "path": "/instruction", "degraded": spec["instruction"], "original": detail}]
            elif kind == "add_candidate":
                new_id = f"c{len(out_cands) + 1}"
                id_of[detail["site"]] = new_id
                ops[name] = [{"op": "add_candidate", "candidate": {"id": new_id, "features": detail["features"]}}]
            elif kind == "replace_feature":
                idx = int(id_of[detail["site"]][1:]) - 1
                feats = out_cands[idx]["features"]
                holder, leaf = get_field(feats, detail["field"])
                if "original" in detail:
                    original = detail["original"]
                else:
                    original = holder[leaf]
                    holder[leaf] = None
                path = f"/candidates/{idx}/features/" + detail["field"].replace(".", "/")
                ops[name] = [{"op": "replace", "path": path, "degraded": holder[leaf], "original": original}]
        true_id = id_of.get(spec["true"])
        in_case = true_id is not None and int(true_id[1:]) <= len(out_cands)
        if spec["answer"] == "true":
            answer = true_id
        else:
            answer = spec["answer"]
        key = {"case_id": cid, "answer": answer, "withheld_answer": spec["w"],
               "sources": [SRC[spec["src"]]["citation"],
                           "Site numbers used: " + ", ".join(sorted({c["site"].split(":")[1] for c in spec["cands"]} |
                                                                    {spec["true"].split(":")[1]}, key=int))],
               "why": spec["why"]}
        case = {"case_id": cid, "batch": "development", "instruction": spec["instruction"],
                "context": CTX[spec["ctx"]], "candidates": out_cands, "degradations": names,
                "withheld_question": spec["q"], "withheld_options": spec["opts"], "key_sha256": sha(key)}
        cases.append(case)
        keys.append(key)
        restore[cid] = {"true_feature": true_id, "true_feature_in_case": in_case,
                        "true_site": spec["true"], "degradations": ops,
                        "site_of_candidate": {v: k for k, v in id_of.items()}}
    return cases, keys, restore


def main():
    cases, keys, restore = build()
    for c in cases:
        (HERE / f"{c['case_id']}.json").write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (HERE / "key.json").write_text(json.dumps(keys, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (HERE / "restore.json").write_text(json.dumps(restore, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                       encoding="utf-8")
    print(f"wrote {len(cases)} cases, key.json and restore.json")


if __name__ == "__main__":
    main()
