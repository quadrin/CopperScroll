"""Which missing information makes selection impossible, and which single added
observation restores it (development batch only).

For every dev case this script restores each subset of the case's degradations from
dev/restore.json, reruns the procedure and records the output. It also runs two
coding variants that use other facts printed in the same reports (no invented
values). It never reads the reserved batch.

Usage (from the repository root):
    python3 -I research/benchmarks/recovery/ablate.py
writes research/benchmarks/recovery/dev/ablation.json
"""
from __future__ import annotations

import copy
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEV = HERE / "dev"
sys.path.insert(0, str(HERE))
import procedure  # noqa: E402
from harness import load_cases, load_key  # noqa: E402


def set_path(obj, pointer, value):
    parts = [p for p in pointer.split("/") if p]
    cur = obj
    for p in parts[:-1]:
        cur = cur[int(p)] if isinstance(cur, list) else cur[p]
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        cur[last] = value


def restored(case, restore_entry, names):
    c = copy.deepcopy(case)
    for name in names:
        for op in restore_entry["degradations"][name]:
            if op["op"] == "replace":
                set_path(c, op["path"], copy.deepcopy(op["original"]))
            elif op["op"] == "add_candidate":
                c["candidates"].append(copy.deepcopy(op["candidate"]))
            else:
                raise ValueError(op["op"])
    c["degradations"] = [d for d in c["degradations"] if d not in names]
    return c


def label(out, true_id):
    sel = out["selected"]
    if sel == "insufficient_evidence":
        return "insufficient_evidence"
    if sel == "none":
        return "none"
    return "true feature" if sel == true_id else "wrong candidate"


def variants(cases_by_id, restore):
    """Coding variants built only from other facts printed in the same reports."""
    src = json.loads((DEV / "source_records.json").read_text(encoding="utf-8"))
    out = []
    # dev-007: code site 2 from the report's words ("c. 200 m south of the ruin") instead of its map reference.
    c = copy.deepcopy(cases_by_id["dev-007"])
    cid = restore["dev-007"]["true_feature"]
    w = src["zaaq"]["sites"]["2"]["words"]
    for cand in c["candidates"]:
        if cand["id"] == cid:
            cand["features"]["position"] = {"bearing_deg": None, "distance_m": w["distance_m"],
                                            "relative_to": w["relative_to"], "kind": "words",
                                            "direction": w["direction"]}
    r = procedure.run_case(c)
    out.append({"case_id": "dev-007", "variant": "site 2 coded from the report's words (south, c. 200 m) instead of its map reference",
                "selected": r["selected"], "result": label(r, cid)})
    # dev-010: code cave 4 from its printed map reference, which the report says is not marked on its map.
    c = copy.deepcopy(cases_by_id["dev-010"])
    cid = restore["dev-010"]["true_feature"]
    ref = src["dabburiya"]["sites"]["3"]["map_ref"]
    pt = src["dabburiya"]["sites"]["4"]["map_ref"]
    import math
    b = round(math.degrees(math.atan2(pt[0] - ref[0], pt[1] - ref[1])) % 360, 1)
    d = round(math.hypot(pt[0] - ref[0], pt[1] - ref[1]), 1)
    for cand in c["candidates"]:
        if cand["id"] == cid:
            cand["features"]["position"] = {"bearing_deg": b, "distance_m": d, "relative_to": "cave_3",
                                            "kind": "plan", "precision_m": 1}
    r = procedure.run_case(c)
    out.append({"case_id": "dev-010", "variant": f"cave 4 coded from its printed map reference ({b} deg, {d} m)",
                "selected": r["selected"], "result": label(r, cid)})
    return out


# ---------------------------------------------------------------- combination sweep
# Start from each dev case whose fully restored form selects its true feature, remove
# one or two pieces of information, and record whether selection survives. Variants
# with the same instruction and candidate content are run once.

def _drop_instruction(field):
    def adjust(c):
        c[field] = None
        return c
    return adjust


def _true_index(case, true_id):
    return next(i for i, cand in enumerate(case["candidates"]) if cand["id"] == true_id)


def op_dates_unknown(case, true_id):
    for cand in case["candidates"]:
        cand["features"]["date"] = "U"
    return case, true_id


def op_true_bearing(case, true_id):
    pos = case["candidates"][_true_index(case, true_id)]["features"]["position"]
    pos["bearing_deg"] = None
    pos["direction"] = None
    return case, true_id


def op_true_distance(case, true_id):
    case["candidates"][_true_index(case, true_id)]["features"]["position"]["distance_m"] = None
    return case, true_id


def op_true_unrecorded(case, true_id):
    case["candidates"] = [c for c in case["candidates"] if c["id"] != true_id]
    return case, None


OPERATORS = {
    "instruction direction": ("adjust", _drop_instruction("direction")),
    "instruction distance": ("adjust", _drop_instruction("distance")),
    "instruction opening": ("adjust", _drop_instruction("opening")),
    "all dates unknown": ("case", op_dates_unknown),
    "true feature bearing": ("case", op_true_bearing),
    "true feature distance": ("case", op_true_distance),
    "true feature unrecorded": ("case", op_true_unrecorded),
}


def apply_ops(case, true_id, names):
    c = copy.deepcopy(case)
    adjusts = []
    for n in names:
        kind, fn = OPERATORS[n]
        if kind == "adjust":
            adjusts.append(fn)
        else:
            c, true_id = fn(c, true_id)

    def adjust(con):
        for f in adjusts:
            con = f(con)
        return con
    return c, true_id, adjust


def sweep(cases, restore):
    bases, seen = [], set()
    for case in cases:
        r = restore[case["case_id"]]
        full = restored(case, r, list(r["degradations"]))
        out = procedure.run_case(full)
        if out["selected"] != r["true_feature"]:
            continue
        sig = json.dumps([full["instruction"], sorted(json.dumps(c["features"], sort_keys=True)
                                                      for c in full["candidates"])])
        if sig in seen:
            continue
        seen.add(sig)
        bases.append((case["case_id"], full, r["true_feature"]))
    rows = []
    names = list(OPERATORS)
    for k in (1, 2):
        for combo in itertools.combinations(names, k):
            res = {}
            for cid, full, true_id in bases:
                c, tid, adjust = apply_ops(full, true_id, combo)
                out = procedure.run_case(c, adjust=adjust)
                sel = out["selected"]
                if tid is None:
                    res[cid] = "correct none" if sel == "none" else (
                        "insufficient_evidence" if sel == "insufficient_evidence" else "false selection")
                else:
                    res[cid] = "correct" if sel == tid else (
                        "insufficient_evidence" if sel == "insufficient_evidence" else
                        "none" if sel == "none" else "wrong candidate")
            rows.append({"removed": list(combo), "results": res,
                         "selection_survives": sum(v in ("correct", "correct none") for v in res.values()),
                         "bases": len(bases)})
    return {"bases": [b[0] for b in bases], "rows": rows,
            "note": ("Each base is a dev case in its fully restored form that selects its true feature. "
                     "'instruction distance' removal falls back to the 1 km default limit. 'true feature "
                     "unrecorded' makes 'none' the correct output.")}


def main():
    cases = load_cases(DEV)
    key = load_key(DEV / "key.json")
    restore = json.loads((DEV / "restore.json").read_text(encoding="utf-8"))
    by_id = {c["case_id"]: c for c in cases}
    report = {"cases": [], "single_restorations": [], "variants": []}
    for case in cases:
        cid = case["case_id"]
        r = restore[cid]
        names = list(r["degradations"])
        base = procedure.run_case(case)
        entry = {"case_id": cid, "key_answer": key[cid]["answer"], "true_feature": r["true_feature"],
                 "degradations": names, "as_given": base["selected"], "subsets": []}
        for k in range(0, len(names) + 1):
            for subset in itertools.combinations(names, k):
                out = procedure.run_case(restored(case, r, list(subset)))
                entry["subsets"].append({"restored": list(subset),
                                         "still_missing": [n for n in names if n not in subset],
                                         "selected": out["selected"], "result": label(out, r["true_feature"]),
                                         "withheld_prediction": out["withheld_prediction"]})
        report["cases"].append(entry)
        if base["selected"] == "insufficient_evidence":
            singles = [s for s in entry["subsets"] if len(s["restored"]) == 1]
            report["single_restorations"].append({
                "case_id": cid, "degradations": names,
                "restores_selection": [s["restored"][0] for s in singles if s["result"] == "true feature"],
                "outcomes": {s["restored"][0]: s["result"] for s in singles},
                "all_restored": entry["subsets"][-1]["result"] if names else "no degradation to remove"})
    report["variants"] = variants(by_id, restore)
    report["sweep"] = sweep(cases, restore)
    (DEV / "ablation.json").write_text(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                       encoding="utf-8")
    for s in report["single_restorations"]:
        print(s["case_id"], s["degradations"], "->", s["outcomes"], "| all restored:", s["all_restored"])
    for e in report["cases"]:
        for s in e["subsets"]:
            if s["restored"]:
                print("  ", e["case_id"], "restored", s["restored"], "->", s["result"])
    for v in report["variants"]:
        print("variant", v["case_id"], v["variant"], "->", v["result"])
    sw = report["sweep"]
    print("sweep bases:", sw["bases"])
    for row in sw["rows"]:
        print(f"  {' + '.join(row['removed']):55s} {row['selection_survives']}/{row['bases']}  {row['results']}")


if __name__ == "__main__":
    main()
