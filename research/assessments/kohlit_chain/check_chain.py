"""Check chain.json: every landmark prediction must use an unused relation.

Standard library only. Run from the repository root:

    python3 -I research/assessments/kohlit_chain/check_chain.py
    python3 -I research/assessments/kohlit_chain/check_chain.py --deps
    python3 -I research/assessments/kohlit_chain/check_chain.py --write-ranking research/assessments/kohlit_chain/next_links.md

Errors (exit status 1):
- a prediction uses a relation that selected its model;
- a rarity MATCH condition is missing from the model's selection relations;
- a chain step marked as used is not a selection relation, or the reverse;
- unknown relation, record or reading-dependency IDs;
- a prediction lacks what, where, record, success or contradiction;
- stored rarity values differ from the registered unit_results.csv;
- a two-of-three rarity unit has no model;
- a workbench assignment is missing or listed twice.

Warnings: shared evidence lineage among selection steps, and predictions whose
records are all already inspected (exploratory only, not unseen tests).
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # the read-only workbench import must not write caches
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CHAIN = HERE / "chain.json"
RARITY_CSV = REPO / "research/rarity/kohlit/stage2/addendum_s2/results/unit_results.csv"
WORKBENCH = REPO / "research/feature_workbench/relationships/evaluate.py"

TIER = {"supplied_unread": 1, "open_access_unread": 1, "requested_pending": 2,
        "library": 3, "archive_order": 4, "fieldwork": 4, "inspected": 5}
STRENGTH = {"two-sided": 0, "absence-statement only": 1, "one-sided": 2}
COND_REL = {"C1": "R-E11-POOL-EAST", "C2": "R-E60-PIT-N", "C3s": "R-E60-GRAVES-N-SECTOR"}
REQUIRED_LINK_FIELDS = ("expect", "where", "success", "contradiction")


def load(path: Path = CHAIN) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _reading_rank(text: str) -> int:
    text = (text or "").lower()
    if "restored" in text:
        return 2
    if "disputed" in text:
        return 1
    return 0


def link_tier(link: dict, records: dict) -> int:
    tiers = [TIER.get(records[r]["access"], 5) for r in link["record_ids"] if r in records]
    return min(tiers) if tiers else 5


def link_key(link: dict, doc: dict) -> tuple:
    records = {r["id"]: r for r in doc["records"]}
    relations = {r["id"]: r for r in doc["relations"]}
    reading = max([_reading_rank(relations[r]["reading"]) for r in link["relations"] if r in relations] or [0])
    return (link_tier(link, records), STRENGTH.get(link["contradiction_strength"], 3), reading, link["priority"])


def validate(doc: dict, rarity_csv: Path | None = None, workbench: dict | None = None) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    relations = {r["id"]: r for r in doc["relations"]}
    deps = {d["id"] for d in doc["reading_dependencies"]}
    records = {r["id"]: r for r in doc["records"]}
    for r in doc["relations"]:
        for d in r["dependencies"]:
            if d not in deps:
                errors.append(f"relation {r['id']}: unknown dependency {d}")
    for r in doc["records"]:
        if r["access"] not in TIER:
            errors.append(f"record {r['id']}: unknown access class {r['access']}")
        if r["access"] == "requested_pending" and not r.get("pending_request"):
            errors.append(f"record {r['id']}: requested_pending without the ACTIVE_TEST request line")
        if r.get("pending_request") and r["access"] != "requested_pending":
            errors.append(f"record {r['id']}: pending request but access {r['access']}")
    seen_models, seen_links = set(), set()
    for m in doc["models"]:
        mid = m["id"]
        if mid in seen_models:
            errors.append(f"duplicate model {mid}")
        seen_models.add(mid)
        selection = set(m["selection_relations"])
        for rel in selection:
            if rel not in relations:
                errors.append(f"{mid}: unknown selection relation {rel}")
        used_steps = set()
        lineages: dict[str, int] = {}
        for s in m["chain"]:
            if s["relation"] not in relations:
                errors.append(f"{mid} step {s['step']}: unknown relation {s['relation']}")
            if s["used_for_selection"]:
                used_steps.add(s["relation"])
                for lin in {e.get("lineage") for e in s["evidence"] if e.get("lineage")}:
                    if lin in lineages and lineages[lin] != s["step"]:
                        warnings.append(f"{mid}: steps {lineages[lin]} and {s['step']} share lineage '{lin}' (not independent)")
                    lineages.setdefault(lin, s["step"])
            elif s["relation"] in selection:
                errors.append(f"{mid} step {s['step']}: {s['relation']} is a selection relation but the step is marked unused")
            for e in s["evidence"]:
                if e.get("record") and e["record"] not in records:
                    errors.append(f"{mid} step {s['step']}: unknown record {e['record']}")
                if not e.get("record") and not e.get("citation"):
                    errors.append(f"{mid} step {s['step']}: evidence needs a record or a citation")
        if used_steps != selection:
            errors.append(f"{mid}: selection relations {sorted(selection)} differ from used chain steps {sorted(used_steps)}")
        rar = m.get("rarity")
        if rar:
            for cond, rel in COND_REL.items():
                if rar.get(cond) == "MATCH" and rel not in selection:
                    errors.append(f"{mid}: rarity {cond} MATCH but {rel} is not listed as a selection relation")
        if not m["next_links"]:
            errors.append(f"{mid}: no next link")
        for link in m["next_links"]:
            lid = link["id"]
            if lid in seen_links:
                errors.append(f"duplicate link {lid}")
            seen_links.add(lid)
            for f in REQUIRED_LINK_FIELDS:
                if not str(link.get(f) or "").strip():
                    errors.append(f"{mid} {lid}: missing {f}")
            if not link["record_ids"]:
                errors.append(f"{mid} {lid}: no record")
            for r in link["record_ids"]:
                if r not in records:
                    errors.append(f"{mid} {lid}: unknown record {r}")
            for d in link.get("reading_dependencies", []):
                if d not in deps:
                    errors.append(f"{mid} {lid}: unknown dependency {d}")
            if link["contradiction_strength"] not in STRENGTH:
                errors.append(f"{mid} {lid}: unknown contradiction strength")
            if link.get("kind", "landmark") == "reading_gate":
                if link["relations"] or not link.get("reading_dependencies"):
                    errors.append(f"{mid} {lid}: a reading gate names no relation and at least one reading dependency")
                continue
            if not link["relations"]:
                errors.append(f"{mid} {lid}: a landmark prediction needs a relation")
            for rel in link["relations"]:
                if rel not in relations:
                    errors.append(f"{mid} {lid}: unknown relation {rel}")
                elif rel in selection:
                    errors.append(f"{mid} {lid}: uses {rel}, which selected the model")
            if link_tier(link, records) == 5:
                warnings.append(f"{mid} {lid}: every record is already inspected; exploratory only, not an unseen test")
    if rarity_csv and Path(rarity_csv).is_file():
        _check_rarity(doc, rarity_csv, errors)
    if workbench is not None:
        _check_workbench(doc, workbench, errors)
    return errors, warnings


def _check_rarity(doc: dict, path: Path, errors: list[str]) -> None:
    with open(path, newline="", encoding="utf-8") as f:
        rows = {r["unit_id"]: r for r in csv.DictReader(f) if r["variant"] == "primary" and r["nigro"] == "with"}
    modelled = {}
    for m in doc["models"]:
        rar = m.get("rarity")
        if not rar:
            continue
        row = rows.get(rar["unit"])
        if row is None:
            errors.append(f"{m['id']}: rarity unit {rar['unit']} not in {path.name}")
            continue
        modelled[rar["unit"]] = m["id"]
        for k in ("C1", "C2", "C3s", "C3t", "A_survey", "B"):
            if rar.get(k) != row[k]:
                errors.append(f"{m['id']}: rarity {k} {rar.get(k)} differs from registered {row[k]}")
    for uid, row in rows.items():
        if [row[c] for c in ("C1", "C2", "C3s")].count("MATCH") >= 2 and uid not in modelled:
            errors.append(f"two-of-three unit {uid} ({row['name']}) has no model")


def workbench_branches(repo: Path = REPO) -> dict:
    """Run the relationships evaluator read-only and group its branches by assignment."""
    spec = importlib.util.spec_from_file_location("kc_relationships_evaluate", repo / "research/feature_workbench/relationships/evaluate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    built = module.build(repo)
    status = {r["id"]: r["status"] for r in built["results"]}
    out: dict[str, list[str]] = {}
    for b in built["data"]["branches"]:
        out.setdefault(b["assignment_id"], []).append(status[b["result_id"]])
    return out


def _check_workbench(doc: dict, branches: dict, errors: list[str]) -> None:
    listed: dict[str, str] = {}
    for m in doc["models"]:
        wb = m.get("workbench") or {}
        for kind in ("surviving_assignments", "contradicted_assignments"):
            for a in wb.get(kind, []):
                if a in listed:
                    errors.append(f"workbench assignment {a} listed twice ({listed[a]}, {m['id']})")
                listed[a] = m["id"]
                statuses = branches.get(a)
                if statuses is None:
                    errors.append(f"{m['id']}: unknown workbench assignment {a}")
                    continue
                all_contradicted = all(s == "contradicted" for s in statuses)
                if kind == "contradicted_assignments" and not all_contradicted:
                    errors.append(f"{m['id']}: {a} listed as contradicted but has non-contradicted branches")
                if kind == "surviving_assignments" and all_contradicted:
                    errors.append(f"{m['id']}: {a} listed as surviving but every branch is contradicted")
    for a in branches:
        if a not in listed:
            errors.append(f"workbench assignment {a} has no model")


def dependencies(doc: dict) -> dict:
    """Per model: reading dependencies of selection and prediction relations, and records needed."""
    relations = {r["id"]: r for r in doc["relations"]}
    out = {}
    for m in doc["models"]:
        sel_deps = sorted({d for r in m["selection_relations"] for d in relations[r]["dependencies"]})
        pred = {}
        for link in m["next_links"]:
            ds = set(link.get("reading_dependencies", []))
            for r in link["relations"]:
                ds.update(relations[r]["dependencies"])
            flags = sorted({relations[r]["reading"] for r in link["relations"] if _reading_rank(relations[r]["reading"])})
            pred[link["id"]] = {"reading_dependencies": sorted(ds), "restored_or_disputed": flags, "records": link["record_ids"]}
        gates = [g["dependency"] for g in m.get("gates", [])]
        out[m["id"]] = {"label": m["label"], "selection_dependencies": sel_deps, "gates": gates, "predictions": pred}
    return out


def ranking(doc: dict) -> list[dict]:
    """The most findable next link of each model, ordered across models."""
    records = {r["id"]: r for r in doc["records"]}
    order = {m["id"]: i for i, m in enumerate(doc["models"])}
    rows = []
    for m in doc["models"]:
        best = min(m["next_links"], key=lambda l: link_key(l, doc))
        key = link_key(best, doc)
        pending = [records[r]["pending_request"] for r in best["record_ids"] if records[r].get("pending_request")]
        rows.append({"model": m["id"], "label": m["label"], "link": best["id"], "relations": best["relations"],
                     "tier": key[0], "strength": best["contradiction_strength"],
                     "records": [records[r]["title"] for r in best["record_ids"]],
                     "requested": bool(pending), "request_lines": pending, "_key": key + (order[m["id"]],)})
    rows.sort(key=lambda r: r["_key"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        del r["_key"]
    return rows


def ranking_markdown(doc: dict) -> str:
    rows = ranking(doc)
    lines = [
        "# Next findable link for each Koḥlit model",
        "",
        "Generated by `check_chain.py --write-ranking` from `chain.json`. Do not edit by hand.",
        "",
        "Order: tier, then contradiction strength (two-sided, absence statement only, one-sided), then reading (agreed before disputed before restored), then the model's place in `chain.json`. Tiers: " +
        "; ".join(f"{k} = {v}" for k, v in doc["method"]["tiers"].items()) + ".",
        "",
        "| Rank | Model | Link | Relations tested | Tier | Can contradict? | Record | Already requested? |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        req = "yes" if r["requested"] else "no"
        lines.append(f"| {r['rank']} | {r['label']} | `{r['link']}` | {', '.join(r['relations']) or 'reading gate'} | {r['tier']} | {r['strength']} | {'; '.join(r['records'])} | {req} |")
    lines += ["", "Full predictions, success and contradiction criteria, and every further link per model are in `chain.json`.", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chain", type=Path, default=CHAIN)
    ap.add_argument("--rarity", type=Path, default=RARITY_CSV)
    ap.add_argument("--no-workbench", action="store_true", help="skip the read-only relationships evaluator check")
    ap.add_argument("--deps", action="store_true", help="print the dependency listing as JSON")
    ap.add_argument("--write-ranking", type=Path)
    ap.add_argument("--check-ranking", type=Path)
    args = ap.parse_args(argv)
    doc = load(args.chain)
    wb = None if args.no_workbench else workbench_branches()
    errors, warnings = validate(doc, args.rarity, wb)
    for w in warnings:
        print("WARNING", w)
    for e in errors:
        print("ERROR", e)
    if args.deps:
        print(json.dumps(dependencies(doc), ensure_ascii=False, indent=1))
    text = ranking_markdown(doc)
    if args.write_ranking:
        args.write_ranking.write_text(text, encoding="utf-8")
    if args.check_ranking and Path(args.check_ranking).read_text(encoding="utf-8") != text:
        print("ERROR ranking file is out of date")
        errors.append("ranking")
    n_links = sum(len(m["next_links"]) for m in doc["models"])
    print(f"{len(doc['models'])} models, {n_links} next links, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
