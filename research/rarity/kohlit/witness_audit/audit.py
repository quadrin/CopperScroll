"""Exploratory witness audit of the committed source-2 addendum.

Reads frozen sheets/results; writes only this directory. No packet text is copied.
Run from any directory: python3 -I audit.py [--out OUT_DIR]
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import itertools
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
KOHLIT = HERE.parent
STAGE = KOHLIT / "stage2"
CONDITIONS = ("C1", "C2", "C3s", "C3t")
BRANCHES = {"B": ("C1", "C2"), "A_survey": ("C1", "C2", "C3s"),
            "A_text": ("C1", "C2", "C3t")}
BASE_REF = "897733283606988581155a3c1df0cd235cb7bea9"


def read_json(p):
    return json.loads(p.read_text(encoding="utf-8"))


def rows(p):
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def merge(base, add, source, prefix):
    """Same append/id-renaming policy as the two committed addendum merges."""
    out = copy.deepcopy(base)
    rename = {f["id"]: f["id"] if f["id"].startswith(prefix) else prefix + f["id"]
              for f in add.get("features", [])}
    ids = {f["id"] for f in out["features"]}
    for f in add.get("features", []):
        g = copy.deepcopy(f)
        g["id"], g["source"] = rename[f["id"]], source
        if g.get("mouth") and g["mouth"].get("pit_id") in rename:
            g["mouth"]["pit_id"] = rename[g["mouth"]["pit_id"]]
        if g["id"] in ids:
            raise ValueError(f"duplicate merged id {g['id']}")
        out["features"].append(g)
        ids.add(g["id"])
    out["explicit_absence"] = out.get("explicit_absence", []) + [
        dict(a, source=source) for a in add.get("explicit_absence", [])]
    out["sources"][source] = "read"
    return out


def merged_sheets(coder):
    d = {p.stem: read_json(p) for p in sorted((STAGE / "coded" / coder).glob("*.json"))}
    s4 = STAGE / "addendum_s4"
    s2 = STAGE / "addendum_s2"
    for p in sorted((s4 / "coded_s4" / coder).glob("*.json")):
        # Source 4 is replacement; source 2 is append-only.
        base = copy.deepcopy(d[p.stem])
        base["features"] = [f for f in base["features"] if f["source"] != "4"]
        base["explicit_absence"] = [a for a in base.get("explicit_absence", []) if a["source"] != "4"]
        d[p.stem] = merge(base, read_json(p), "4", "s4_")
    if coder == "B":
        for p in sorted((s4 / "coded_B_full").glob("*.json")):
            d[p.stem] = read_json(p)
    for p in sorted((s2 / "coded_s2" / coder).glob("*.json")):
        d[p.stem] = merge(d[p.stem], read_json(p), "2", "s2z_")
    if coder == "B":
        for p in sorted((s2 / "coded_B_full").glob("*.json")):
            d[p.stem] = read_json(p)
    return d


def precision(x, y):
    for p in (1000, 500, 100, 50, 10):
        if int(round(x)) % p == 0 and int(round(y)) % p == 0:
            return p
    return 1


def geometry(uid, ref, points):
    if uid == ref:
        return None
    if uid not in points or ref not in points:
        return None
    x, y = points[uid]
    fx, fy = points[ref]
    dist = math.hypot(fx - x, fy - y)
    return {"distance_m": round(dist), "bearing_deg": round(math.degrees(math.atan2(fx-x, fy-y)) % 360, 1)
            if dist else None, "bearing_valid": dist >= 3 * max(precision(x,y), precision(fx,fy)),
            "provenance": "reconstructed from committed stage1a points with build_packets.py geometry rule"}


def position_truth(uid, f, condition, points, constants):
    """Tri-valued position; missing packet-only grid rows stay unknown."""
    p = f.get("position") or {}
    kind = p.get("kind")
    sector = constants["sectors_deg"]["C1_east" if condition == "C1" else "C2_north"]
    limit = constants["limits_m"]["C3_survey" if condition == "C3s" else condition]
    def inside(b):
        lo, hi = sector
        return lo <= b <= hi if lo <= hi else b >= lo or b <= hi
    if kind == "grid":
        g = geometry(uid, p.get("ref"), points)
        if not g or not g["bearing_valid"] or g["bearing_deg"] is None:
            return None
        return inside(g["bearing_deg"]) and g["distance_m"] <= limit
    if kind == "plan":
        if p.get("bearing_deg") is None or p.get("distance_m") is None:
            return None
        return inside(float(p["bearing_deg"]) % 360) and float(p["distance_m"]) <= limit
    if kind == "words":
        if p.get("relative_to") != "unit":
            return None
        word = (p.get("direction") or "").strip()
        dist_ok = p.get("distance_m") is None or float(p["distance_m"]) <= limit
        if condition == "C1" and word.lower() in constants["east_part_words"]:
            return dist_ok
        if word.upper() in constants["quadrant_edge_words"]:
            return None
        if word.upper() in constants["compass_deg"]:
            return inside(constants["compass_deg"][word.upper()]) and dist_ok
    return None


def candidate(f, condition):
    if condition == "C1":
        return f["type"] == "pool" and f.get("pool_def") == "yes"
    if condition == "C2":
        return f["type"] == "pit" and not f.get("is_tomb")
    return f["type"] == "grave"


def inferred_hits(uid, sheet, condition, points, constants):
    if condition == "C3t":
        pits, _ = inferred_hits(uid, sheet, "C2", points, constants)
        hits, unknown = [], []
        for f in sheet["features"]:
            m = f.get("mouth") or {}
            if f["type"] != "grave" or f["date"]["code"] == "L" or not m.get("pit_id"):
                continue
            distance = m.get("distance_m")
            ok = (distance is not None and float(distance) <= constants["limits_m"]["C3_text_mouth"]) or any(
                phrase in (m.get("phrase") or "").lower() for phrase in constants["mouth_phrases"])
            if ok and m["pit_id"] in pits:
                hits.append(f["id"])
            elif ok:
                unknown.append(f["id"])
        return hits, unknown
    hits, unresolved = [], []
    for f in sheet["features"]:
        if not candidate(f, condition) or f["date"]["code"] == "L":
            continue
        truth = position_truth(uid, f, condition, points, constants)
        if truth is True:
            hits.append(f["id"])
        elif truth is None:
            unresolved.append(f["id"])
    return hits, unresolved


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def feature_class(f):
    text = norm((f.get("subtype") or "") + " " + (f.get("quote") or ""))
    if f["type"] == "pool":
        return "open-basin-group"
    if f["type"] == "grave":
        return "cemetery" if "cemeter" in text or "necropolis" in text else "burial-group"
    for pat, cls in (("robbing", "robbing-pits"), ("cistern", "cistern-group"),
                     ("cave", "cave-group"), ("well", "well"), ("pit", "pit-group"),
                     ("silo", "silo"), ("shaft", "shaft"), ("chamber", "chamber")):
        if pat in text:
            return cls
    return f["type"] + "-unresolved"


def citation_anchor(f):
    cite = f.get("cite", "")
    if f["source"] == "1":
        m = re.search(r"WBADB\s+([ES]\d+)", cite)
        return "WBADB:" + (m.group(1) if m else "unresolved")
    if f["source"] == "3":
        m = re.search(r"Mem(?:oirs)?\s+(I{1,3})\s+p(?:p)?\.\s*(\d+)", cite)
        if m:
            return f"SWP:{m.group(1)}:{m.group(2)}"
    # Exact normalized citation only: page proximity alone cannot prove identity.
    return "source" + f["source"] + ":" + norm(cite)


def claim_key(uid, f):
    """Exact curated source-feature anchor; uncured citations prove no identity."""
    # Curated pairings are explicit and source-linked in CURATION.json.
    aliases = read_json(HERE / "CURATION.json")["feature_aliases"]
    for a in aliases:
        if a["unit_id"] == uid and f["id"] in a.get("ids", {}).get(f.get("_coder"), []):
            return a["claim_id"]
    return None


def citation_class_key(f):
    """Potential citation/class compatibility only; never feature identity."""
    return "|".join((citation_anchor(f), f["type"], feature_class(f)))


def witness(uid, coder, f, condition, points):
    g = geometry(uid, (f.get("position") or {}).get("ref"), points)
    cur = read_json(HERE / "CURATION.json")
    alias = next((a for a in cur["feature_aliases"] if a["unit_id"] == uid and
                  f["id"] in a.get("ids", {}).get(coder, [])), None)
    key = claim_key(uid, dict(f, _coder=coder))
    lineage = alias.get("lineage") if alias else None
    return {"witness_id": f"{uid}:{coder}:{f['id']}:{condition}", "unit_id": uid,
            "coder": coder, "feature_id": f["id"], "condition": condition,
            "source": f["source"], "cite": f["cite"], "type": f["type"],
            "subtype": f.get("subtype"), "documented_claim_id": key,
            "citation_class_key": citation_class_key(f),
            "identity_scope": "curated source feature group" if alias else "citation/class compatibility only; feature identity unresolved",
            "publication_lineage": citation_anchor(f), "original_observation_lineage": lineage,
            "lineage_status": "curated" if lineage else "not established by coding",
            "directional_witness": f.get("position"), "grid_geometry": g,
            "direction_scope": "row proxy" if (f.get("position") or {}).get("kind") == "grid" else "coded source relation",
            "date_code": f["date"]["code"], "date_basis": f["date"].get("basis"),
            "coexistence_date_established": False, "mouth": f.get("mouth")}


def identity_agreement(a, b):
    ak = {x["documented_claim_id"] for x in a if x["documented_claim_id"] is not None}
    bk = {x["documented_claim_id"] for x in b if x["documented_claim_id"] is not None}
    return sorted(ak & bk)


def citation_compatibility(a, b):
    return sorted({x["citation_class_key"] for x in a} & {x["citation_class_key"] for x in b})


def assignment_sets(witnesses, conditions):
    by = {c: [w for w in witnesses if w["condition"] == c] for c in conditions}
    if any(not by[c] for c in conditions):
        return []
    out = []
    for combo in itertools.product(*(by[c] for c in conditions)):
        # At text level a grave must attach to this same selected C2 feature.
        if "C3t" in conditions:
            pit = combo[conditions.index("C2")]
            grave = combo[conditions.index("C3t")]
            if (grave.get("mouth") or {}).get("pit_id") != pit["feature_id"]:
                continue
        out.append({"condition_features": {c: w["feature_id"] for c, w in zip(conditions, combo)},
                    "condition_claims": {c: w["documented_claim_id"] for c, w in zip(conditions, combo)},
                    "date_codes": {c: w["date_code"] for c, w in zip(conditions, combo)},
                    "survey_compatible": True, "contemporaneity": "UNKNOWN",
                    "text_mouth_relation": "recorded" if "C3t" in conditions else "not tested by this branch"})
    return out


def dump_csv(path, data):
    if not data:
        path.write_text("", encoding="utf-8")
        return
    fields = list(data[0])
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for row in data:
            w.writerow({k: json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict,list)) else v
                        for k,v in row.items()})


def run(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    constants = read_json(STAGE / "protocol_constants.json")
    comparison = rows(STAGE / "addendum_s2/results/coder_comparison.csv")
    primary = {r["unit_id"]: r for r in rows(STAGE / "addendum_s2/results/unit_results.csv")
               if r["variant"] == "primary" and r["nigro"] == "with"}
    points = {r["unit_id"]: (float(r["x"]), float(r["y"])) for r in rows(KOHLIT / "stage1a/stage1a_units.csv")}
    sheets = {"A": merged_sheets("A"), "B": merged_sheets("B")}
    if {r["unit_id"] for r in comparison} != set(sheets["A"]):
        raise ValueError("coder-A snapshot is incomplete or differs from committed comparison")
    for row in comparison:
        uid = row["unit_id"]
        if bool(row["B_C1"]) != (uid in sheets["B"]):
            raise ValueError(f"coder-B snapshot availability differs for {uid}")
        ids = {f["id"] for f in sheets["A"][uid]["features"]}
        recorded = set(itertools.chain.from_iterable(json.loads(row["A_features"]).values()))
        if not recorded <= ids:
            raise ValueError(f"committed A hit ids absent after merge for {uid}: {recorded - ids}")
    frozen_summary = read_json(STAGE / "addendum_s2/results/summary.json")
    exposed = frozen_summary["exposed"]
    windows = {
        "R1_main_Hel_Rom": lambda r: r["main_set"] == "True",
        "R1_pre70": lambda r: True,
        "R2_main_Hel_Rom": lambda r: r["main_set"] == "True" and r["in_R2"] == "True",
        "R2_pre70": lambda r: r["in_R2"] == "True",
    }
    witnesses, conditions, unit_assignments, discrepancies = [], [], [], []
    for row in comparison:
        uid = row["unit_id"]
        ah = json.loads(row["A_features"])
        per_coder = defaultdict(list)
        for condition in CONDITIONS:
            a = [witness(uid, "A", f, condition, points) for f in sheets["A"][uid]["features"]
                 if f["id"] in ah[condition]]
            b, bunresolved = [], []
            b_status = row[f"B_{condition}"]
            if uid in sheets["B"] and b_status == "MATCH":
                hits, bunresolved = inferred_hits(uid, sheets["B"][uid], condition, points, constants)
                b = [witness(uid, "B", f, condition, points) for f in sheets["B"][uid]["features"]
                     if f["id"] in hits]
                if not b:
                    discrepancies.append({"unit_id": uid, "condition": condition,
                                          "status": "B MATCH but exact hit cannot be recovered without packet geometry",
                                          "unresolved_ids": bunresolved})
            witnesses.extend(a + b)
            per_coder["A"].extend(a)
            per_coder["B"].extend(b)
            if row[f"A_{condition}"] == "MATCH" or b_status == "MATCH" or uid in exposed:
                common = identity_agreement(a, b)
                compatible = citation_compatibility(a, b)
                if not b_status:
                    identity = "SINGLE_CODER"
                elif row[f"A_{condition}"] != "MATCH" or b_status != "MATCH":
                    identity = "NO_JOINT_POSITIVE"
                elif common:
                    identity = "CURATED_SAME_SOURCE_FEATURE_GROUP"
                elif compatible:
                    identity = "CITATION_CLASS_COMPATIBLE_IDENTITY_UNRESOLVED"
                elif b:
                    identity = "NO_SHARED_SOURCE_FEATURE_ANCHOR"
                else:
                    identity = "UNKNOWN_PACKET_GEOMETRY"
                conditions.append({"unit_id": uid, "name": row["name"], "condition": condition,
                                   "A_status": row[f"A_{condition}"], "B_status": b_status,
                                   "frozen_final_status": row[f"final_{condition}"],
                                   "A_features": [w["feature_id"] for w in a],
                                   "B_recovered_features": [w["feature_id"] for w in b],
                                   "B_unresolved_candidates": bunresolved,
                                   "witness_agreement": identity, "shared_claim_ids": common,
                                   "citation_class_compatibility": compatible,
                                   "physical_identity": "UNKNOWN"})
        if any(primary[uid][br] == "MATCH" for br in BRANCHES) or uid in exposed or sum(
                primary[uid][c] == "MATCH" for c in ("C1", "C2", "C3s")) >= 2:
            branches = {}
            for branch, cs in BRANCHES.items():
                assign = {coder: assignment_sets(per_coder[coder], cs) for coder in ("A", "B")}
                def key(x):
                    return tuple(x["condition_claims"][c] for c in cs)
                # A tuple of unknown identities never becomes a shared assignment.
                ak = {key(x) for x in assign["A"] if all(key(x))}
                bk = {key(x) for x in assign["B"] if all(key(x))}
                common = sorted(ak & bk)
                branches[branch] = {"frozen_result": primary[uid][branch], "assignments": assign,
                                    "shared_documented_assignments": [dict(zip(cs, x)) for x in common],
                                    "physical_same_assignment": "UNKNOWN", "joint_phase": "UNKNOWN"}
            unit_assignments.append({"unit_id": uid, "name": row["name"], "exposed": uid in exposed,
                                     "branches": branches})
    for uid, data in exposed.items():
        if uid not in sheets["A"]:
            unit_assignments.append({"unit_id": uid, "name": data["label"], "exposed": True,
                                     "reason": "not recorded at Stage 1; no feature sheet; all relations UNKNOWN", "branches": {}})
    candidate_records = []
    for uid in exposed:
        for coder in ("A", "B"):
            if uid not in sheets[coder]:
                continue
            for f in sheets[coder][uid]["features"]:
                possible = [c for c in ("C1", "C2", "C3s") if candidate(f,c)]
                rec = witness(uid, coder, f, "candidate", points)
                rec["primary_position_status"] = {c: position_truth(uid, f, c, points, constants) for c in possible}
                rec["eligible_date_in_primary"] = f["date"]["code"] in ("D", "U")
                candidate_records.append(rec)
    absence_rows = []
    for row in comparison:
        uid = row["unit_id"]
        for c in CONDITIONS:
            if row[f"final_{c}"] != "FAIL":
                continue
            for coder in ("A", "B"):
                if uid not in sheets[coder]:
                    continue
                for absence in sheets[coder][uid].get("explicit_absence", []):
                    if absence["condition"] != ("C3" if c.startswith("C3") else c):
                        continue
                    absence_rows.append({"unit_id": uid, "condition": c, "coder": coder,
                                         "source": absence["source"], "cite": absence.get("cite"),
                                         "statement_hash": hashlib.sha256(absence["quote"].encode()).hexdigest(),
                                         "documentary_status": "explicit class absence under frozen rule",
                                         "physical_sector_coverage": "UNKNOWN", "target_volume_coverage": "UNKNOWN",
                                         "site_entry_mapping": "flagged in addendum" if uid in {"S241","S1080"} else "not independently audited"})
    input_paths = sorted(set([HERE / "audit.py", HERE / "CURATION.json",
                              STAGE / "protocol_constants.json", KOHLIT / "stage1a/stage1a_units.csv",
                              STAGE / "addendum_s2/results/coder_comparison.csv",
                              STAGE / "addendum_s2/results/unit_results.csv",
                              STAGE / "addendum_s2/results/summary.json"] +
                             list((STAGE / "coded").rglob("*.json")) +
                             list((STAGE / "addendum_s4").glob("coded*/*/*.json")) +
                             list((STAGE / "addendum_s4/coded_B_full").glob("*.json")) +
                             list((STAGE / "addendum_s2").glob("coded*/*/*.json")) +
                             list((STAGE / "addendum_s2/coded_B_full").glob("*.json"))))
    summary = {"base_commit": BASE_REF, "analysis": "exploratory; prior evidence exposed",
               "positive_condition_records": sum(r["frozen_final_status"] == "MATCH" for r in conditions),
               "positive_units": len({r["unit_id"] for r in conditions if r["frozen_final_status"] == "MATCH"}),
               "coder_positive_condition_records": sum(r["A_status"] == "MATCH" or r["B_status"] == "MATCH" for r in conditions),
               "witness_records": len(witnesses),
               "positive_condition_agreement": dict(Counter(r["witness_agreement"] for r in conditions
                                                            if r["frozen_final_status"] == "MATCH")),
               "unrecoverable_B_matches": len(discrepancies),
               "frozen_primary_branch_matches_by_window": {
                   window: {branch: [uid for uid,r in primary.items() if select(r) and r[branch] == "MATCH"]
                            for branch in BRANCHES} for window,select in windows.items()},
               "frozen_primary_window_tallies": frozen_summary["headline"],
               "absence_unit_conditions": len({(r["unit_id"],r["condition"]) for r in absence_rows}),
               "physical_coverage_verified": 0,
               "claim": "same feature assignment with a joint ancient phase and text-mouth relation",
               "result": "not identifiable from available evidence",
               "input_hashes": {str(p.relative_to(KOHLIT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths}}
    for name,data in (("witnesses.json",witnesses), ("condition_audit.json",conditions),
                      ("assignments.json",unit_assignments), ("unresolved_B_matches.json",discrepancies),
                      ("absence_audit.json",absence_rows), ("candidate_features.json",candidate_records),
                      ("frozen_primary_units.json",list(primary.values())), ("summary.json",summary)):
        (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",encoding="utf-8")
    dump_csv(out_dir / "condition_audit.csv", conditions)
    print(json.dumps({k:v for k,v in summary.items() if k != "input_hashes"},indent=2))
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=HERE / "outputs")
    run(p.parse_args().out)
