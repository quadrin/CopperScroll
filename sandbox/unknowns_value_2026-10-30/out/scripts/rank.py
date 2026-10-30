"""Run 25: rank missing records by the verdict units they could change.

Reads out/units.csv, out/records.csv, out/links.csv. Writes out/ranking_evidence.csv,
out/ranking_all.csv, out/ranking_variants.json and prints a summary.
Run from anywhere: python3 -I sandbox/unknowns_value_2026-10-30/out/scripts/rank.py

Rule (RULE.md, commit 8c6c2de): primary key = EVIDENCE-linked units; ties: more runs
touched, then easier access. Second table: EVIDENCE + INFERENCE links.
Records already read for a unit are not linked (linking criterion 2), so a record whose
access state is 'read' appears only where it was not read for that unit.
"""
import csv
import json
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(OUT, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


units = {u["unit_id"]: u for u in load("units.csv")}
records = {r["record_id"]: r for r in load("records.csv")}
links = load("links.csv")

for x in links:
    assert x["unit_id"] in units, x
    assert x["record_id"] in records, x
    assert x["link_type"] in ("EVIDENCE", "INFERENCE"), x

STRICT_EVIDENCE_KINDS = {"RESULT-unit", "other-source"}


def rank(types, unit_filter=lambda u: True, evidence_kinds=None, access_rank=None):
    rows = []
    for rid, rec in records.items():
        ev = set()
        inf = set()
        for x in links:
            if x["record_id"] != rid or not unit_filter(units[x["unit_id"]]):
                continue
            if x["link_type"] == "EVIDENCE" and (evidence_kinds is None or x["basis_kind"] in evidence_kinds):
                ev.add(x["unit_id"])
            elif x["link_type"] == "INFERENCE" or x["link_type"] == "EVIDENCE":
                inf.add(x["unit_id"])
        inf -= ev
        counted = set(ev) | (inf if "INFERENCE" in types else set())
        if not counted:
            continue
        runs = sorted({int(units[u]["run"]) for u in counted}, key=int)
        rows.append({
            "record_id": rid,
            "units": len(counted),
            "evidence_units": len(ev),
            "inference_only_units": len(inf),
            "runs_touched": len(runs),
            "runs": " ".join(str(r) for r in runs),
            "access_state": rec["access_state"],
            "access_rank": int(rec["access_rank"]) if access_rank is None else access_rank[rec["access_state"]],
            "unit_ids": " ".join(sorted(counted)),
        })
    rows.sort(key=lambda r: (-r["units"], -r["runs_touched"], r["access_rank"], r["record_id"]))
    # dense rank on the full key (ties share a rank)
    prev, rk = None, 0
    for i, r in enumerate(rows):
        key = (r["units"], r["runs_touched"], r["access_rank"])
        if key != prev:
            rk = i + 1
            prev = key
        r["rank"] = rk
    return rows


def write(rows, name):
    f = ["rank", "record_id", "units", "evidence_units", "inference_only_units", "runs_touched",
         "runs", "access_state", "access_rank", "unit_ids"]
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=f)
        w.writeheader()
        w.writerows(rows)


r1 = rank({"EVIDENCE"})
r2 = rank({"EVIDENCE", "INFERENCE"})
write(r1, "ranking_evidence.csv")
write(r2, "ranking_all.csv")

variants = {
    "V1_literal_units_only": rank({"EVIDENCE"}, unit_filter=lambda u: u["literal"] == "yes"),
    "V2_strict_evidence_named_for_unit_or_other_source": rank({"EVIDENCE"}, evidence_kinds=STRICT_EVIDENCE_KINDS),
    "V3_both": rank({"EVIDENCE"}, unit_filter=lambda u: u["literal"] == "yes", evidence_kinds=STRICT_EVIDENCE_KINDS),
    # Access order is not fixed by the rule. Main order: read 1, Drive <=10 MB 2, Mac online-only 3,
    # Drive >10 MB 3, not in library 4, held by person 5. V4 puts a pending request before a purchase.
    "V4_access_held_before_library": rank({"EVIDENCE"}, access_rank={
        "read": 1, "Drive <=10 MB, not opened": 2, "Mac online-only": 3, "Drive >10 MB": 3,
        "held by person, request pending": 4, "not in library": 5}),
}
summ = {k: [{kk: r[kk] for kk in ("rank", "record_id", "units", "runs_touched", "access_state")} for r in v[:10]]
        for k, v in variants.items()}

# Units with no link at all, and per-run coverage
linked_units = {x["unit_id"] for x in links}
ev_units = {x["unit_id"] for x in links if x["link_type"] == "EVIDENCE"}
summ["counts"] = {
    "units": len(units),
    "units_literal": sum(u["literal"] == "yes" for u in units.values()),
    "records": len(records),
    "records_with_evidence_link": len(r1),
    "records_with_any_link": len(r2),
    "links": len(links),
    "evidence_links": sum(x["link_type"] == "EVIDENCE" for x in links),
    "inference_links": sum(x["link_type"] == "INFERENCE" for x in links),
    "units_with_evidence_link": len(ev_units),
    "units_with_any_link": len(linked_units),
    "units_without_link": sorted(set(units) - linked_units),
    "units_inference_only": sorted(linked_units - ev_units),
}
# Per-run coverage: units, units with an EVIDENCE link, units with no link
per_run = {}
for uid, u in units.items():
    pr = per_run.setdefault(int(u["run"]), {"units": 0, "with_evidence": 0, "no_link": []})
    pr["units"] += 1
    if uid in ev_units:
        pr["with_evidence"] += 1
    if uid not in linked_units:
        pr["no_link"].append(uid)
summ["per_run"] = {str(k): per_run[k] for k in sorted(per_run)}

# Comparison with method 6 (research/feature_workbench/decisions): its queue rank is
# recomputed by its own script; sandbox counts are joined by shared_id.
import subprocess
REPO = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
m6 = None
try:
    p = subprocess.run(["python3", "-I", "research/feature_workbench/decisions/discriminate.py", "--summary"],
                       cwd=REPO, capture_output=True, text=True, timeout=300, check=True)
    m6 = json.loads(p.stdout)["queue_rank"]
except Exception as e:  # report, do not guess
    summ["method6_error"] = repr(e)
if m6:
    r1_by = {r["record_id"]: r for r in r1}
    r2_by = {r["record_id"]: r for r in r2}
    comp = []
    for q in m6:
        tid = q["task_id"]
        shared = [rid for rid, rec in records.items() if rec["shared_id"] == tid]
        ev = sum(r1_by[s]["units"] for s in shared if s in r1_by)
        al = sum(r2_by[s]["units"] for s in shared if s in r2_by)
        comp.append({"method6_rank": q["rank"], "task_id": tid, "rank_key": q["rank_key"],
                     "sandbox_records": shared, "sandbox_evidence_units": ev, "sandbox_all_units": al,
                     "sandbox_rank1": [r1_by[s]["rank"] for s in shared if s in r1_by],
                     "sandbox_access": [records[s]["access_state"] for s in shared]})
    summ["method6_comparison"] = comp
    print("Method 6 comparison")
    for c in comp:
        print(f"  m6 #{c['method6_rank']} {c['task_id']:<30} sandbox ev units={c['sandbox_evidence_units']} all={c['sandbox_all_units']} "
              f"records={c['sandbox_records']} access={c['sandbox_access']}")

with open(os.path.join(OUT, "ranking_variants.json"), "w", encoding="utf-8") as fh:
    json.dump(summ, fh, ensure_ascii=False, indent=1)


def show(title, rows, n=12):
    print(title)
    for r in rows[:n]:
        print(f"  {r['rank']:>2}  {r['record_id']:<38} units={r['units']:<2} (ev {r['evidence_units']}, inf {r['inference_only_units']})"
              f"  runs={r['runs_touched']} [{r['runs']}]  {r['access_state']}")


show("Ranking 1 (EVIDENCE)", r1)
show("Ranking 2 (EVIDENCE + INFERENCE)", r2)
for k, v in variants.items():
    show(k, v, 6)
print(json.dumps(summ["counts"], ensure_ascii=False, indent=1))
