#!/usr/bin/env python3
"""Build the arrival register: register.json, items/<id>.md and RANKING.md.

Reads repository files read-only. Runs the decisions discriminator and the
coverage evaluator as subprocesses and parses their JSON. Writes only inside
its own folder (or --out). Standard library only; deterministic output.

    python3 -I research/preregistration/arrivals/build_register.py
    python3 -I research/preregistration/arrivals/build_register.py --out /tmp/x
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.dont_write_bytecode = True

DECISIVE_SHARES = (0.25, 0.5, 0.75)
MAIN_SHARE = 0.5
OUTCOME_SUFFIXES = ("confirm", "contradict", "inconclusive", "silent")


def load_specs():
    spec = importlib.util.spec_from_file_location("arrival_specs", HERE / "specs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def run_json(args: list[str], repo: Path) -> dict:
    out = subprocess.run([sys.executable, "-I", *args], cwd=repo, check=True,
                         capture_output=True, text=True)
    return json.loads(out.stdout)


def load_inputs(repo: Path) -> dict:
    chain = json.loads((repo / "research/assessments/kohlit_chain/chain.json").read_text(encoding="utf-8"))
    disc = run_json(["research/feature_workbench/decisions/discriminate.py", "--repo-root", str(repo)], repo)
    cov = run_json(["research/feature_workbench/coverage/evaluate.py", "--repo-root", str(repo)], repo)
    reg = json.loads((repo / "research/agent_review_2026-10-07/wave2/W2B_model_v1/registry_v2_entry60.json").read_text(encoding="utf-8"))
    return {"chain": chain, "disc": disc, "cov": cov, "registry": reg}


# ---------------------------------------------------------------- classes

def decision_classes(disc: dict) -> dict:
    fams = {}
    for fam in disc["families"]:
        fams[fam["id"]] = [{"id": c["id"], "label": c["label"], "members": c["member_count"]}
                           for c in fam["classes"]]
    return fams


def chain_models(chain: dict, roster: set) -> list[dict]:
    return [{"id": m["id"], "label": m["label"], "in_decision_roster": m["id"] in roster}
            for m in chain["models"]]


# ---------------------------------------------------------------- per item

def link_coverage(item: dict, link_id: str) -> float:
    cov = item.get("chain_coverage", {"default": 0.5})
    value = cov.get("default", 0.5)
    for key, val in cov.items():
        if key != "default" and key in link_id:
            value = val
    return value


ALL_BRANCHES = ["RB-M", "RB-P", "RB-B"]


def link_branches(text: str | None) -> list[str]:
    """Koḥlit-anchored reading branches named in a chain link's branch field."""
    text = text or ""
    if "all branches" in text:
        return list(ALL_BRANCHES)
    found = set(re.findall(r"RB-[MPB]", text))
    return [b for b in ALL_BRANCHES if b in found]


def item_links(item: dict, chain: dict) -> list[dict]:
    wanted = set(item.get("chain_record_ids", []))
    extra = {(e["model"], e["link"]): e for e in item.get("extra_links", [])}
    links = []
    for model in chain["models"]:
        for link in model["next_links"]:
            key = (model["id"], link["id"])
            hit = sorted(wanted & set(link.get("record_ids", [])))
            if not hit and key not in extra:
                continue
            strength = link.get("contradiction_strength")
            coverage = extra[key]["coverage"] if key in extra else link_coverage(item, link["id"])
            links.append({
                "model": model["id"],
                "model_label": model["label"],
                "link": link["id"],
                "relations": link.get("relations", []),
                "branch": link.get("branch"),
                "branches_named": link_branches(link.get("branch")),
                "branches_excludable": link_branches(link.get("branch")) if strength != "one-sided" else [],
                "predicts": link.get("expect"),
                "where": link.get("where"),
                "confirm_if": link.get("success"),
                "contradict_if": link.get("contradiction"),
                "contradiction_strength": strength,
                "reading_dependencies": link.get("reading_dependencies", []),
                "records_matched": hit,
                "coverage": coverage,
                "coverage_note": extra[key]["note"] if key in extra else None,
                "inconclusive_if": "The record covers the place but meets neither the confirm nor the contradict criterion.",
                "silent_if": "The record does not cover this place or relation. Silence is never a FAIL.",
            })
    return links


def decision_rows(item: dict, disc: dict) -> list[dict]:
    task = item.get("decision_task")
    if not task:
        return []
    table = {t["task_id"]: t for t in disc["observation_table"]}
    rows = []
    for row in table[task]["outcomes"]:
        comps = row.get("components") or {}
        if item.get("decision_row_filter") == "bearing_undetermined":
            if comps.get("bearing") not in (None, "undetermined"):
                continue
        excluded = {f: sorted(v) for f, v in sorted(row["excluded_classes"].items()) if v}
        rows.append({
            "id": row["id"],
            "plans_outcome_id": row["plans_outcome_id"],
            "kind": row["row_kind"],
            "basis": row["basis"],
            "label": row["label"],
            "components": comps or None,
            "surviving": {f: sorted(v) for f, v in sorted(row["surviving_classes"].items())},
            "excluded": excluded,
            "n_excluded": sum(len(v) for v in excluded.values()),
        })
    return rows


def registry_entries(item: dict, registry: dict) -> list[dict]:
    recs = {r["id"]: r for r in registry["records"]}
    out = []
    for entry in item.get("registry", []):
        rec = recs[entry["record"]]
        out.append({
            "record": entry["record"],
            "site": rec["site_name"],
            "reading_assumed": rec["reading_assumed"],
            "record_sha256": rec["record_sha256"],
            "next_desk_test": rec.get("next_desk_test"),
            "prediction": entry["prediction"],
        })
    return out


def coverage_entries(item: dict, cov: dict) -> list[dict]:
    cases = {c["id"]: c for c in cov["data"]["volume_joins"]["cases"]}
    out = []
    for entry in item.get("coverage_cases", []):
        case = cases[entry["case"]]
        joins = [{"branch": j.get("branch_id"), "footprint": j.get("footprint_id"),
                  "status_now": j.get("status"), "missing": sorted(j.get("missing_parameters") or [])}
                 for j in case.get("joins", [])]
        out.append({"case": entry["case"], "label": case.get("label"), "joins_now": joins,
                    "prediction": entry["prediction"]})
    return out


def outcome_ids(item: dict, links: list, rows: list, preds: list, regs: list, covs: list) -> list[str]:
    ids = ["item:silent", "item:partial", "item:unregistered-observation"]
    ids += [f"dec:{r['id']}" for r in rows]
    for link in links:
        for suffix in OUTCOME_SUFFIXES:
            if suffix == "contradict" and link["contradiction_strength"] == "one-sided":
                continue
            ids.append(f"chain:{link['link']}:{suffix}")
    for i, _ in enumerate(preds, 1):
        ids += [f"pred{i}:{s}" for s in OUTCOME_SUFFIXES]
    for reg in regs:
        ids += [f"reg:{reg['record']}:{s}" for s in ("as-predicted", "not-as-predicted", "silent")]
    for c in covs:
        ids += [f"cov:{c['case']}:{s}" for s in ("as-predicted", "not-as-predicted")]
    for i, _ in enumerate(item.get("closed_results", []), 1):
        ids += [f"closed{i}:{s}" for s in ("reopen-triggered", "not-triggered")]
    return ids


# ---------------------------------------------------------------- ranking

def e_dec_by_family(rows: list, c: float, share: float) -> dict[str, float]:
    """Descriptive split of E_dec by model family (same formula, one family at a time)."""
    fams = sorted({f for r in rows for f in r["surviving"]})
    out = {}
    for f in fams:
        sub = [{"kind": r["kind"], "n_excluded": len(r["excluded"].get(f, []))} for r in rows]
        out[f] = round(e_dec(sub, c, share)[0], 3)
    return out


def e_dec(rows: list, c: float, share: float) -> tuple[float, int]:
    if c == 0 or not rows:
        return 0.0, 0
    dec = [r["n_excluded"] for r in rows if r["kind"] == "decisive"]
    non = [r["n_excluded"] for r in rows if r["kind"] != "decisive"]
    mean_d = sum(dec) / len(dec) if dec else 0.0
    mean_n = sum(non) / len(non) if non else 0.0
    best = max(r["n_excluded"] for r in rows)
    return c * ((1 - share) * mean_n + share * mean_d), best


def e_chain(links: list, roster: set, share: float) -> tuple[float, float]:
    per_model: dict[str, dict[str, list[float]]] = {}
    for link in links:
        if link["model"] in roster or not link["branches_excludable"]:
            continue
        p = link["coverage"] * share * 0.5
        for b in link["branches_excludable"]:
            per_model.setdefault(link["model"], {}).setdefault(b, []).append(p)
    expected = 0.0
    best = 0.0
    for branches in per_model.values():
        for ps in branches.values():
            keep = 1.0
            for p in ps:
                keep *= (1 - p)
            expected += (1 - keep) / 3
        best += len(branches) / 3
    return expected, best


def rank_items(entries: list[dict], share: float) -> list[dict]:
    rows = []
    for e in entries:
        if e.get("unranked"):
            continue
        ed, best_d = e_dec(e["decision_rows"], e["decision_coverage"], share)
        ec, best_c = e_chain(e["chain_links"], e["_roster"], share)
        rows.append({
            "item": e["id"],
            "E_dec": round(ed, 3),
            "E_dec_by_family": e_dec_by_family(e["decision_rows"], e["decision_coverage"], share),
            "E_chain": round(ec, 3),
            "E_total": round(ed + ec, 3),
            "best_dec": best_d if e["decision_coverage"] > 0 else 0,
            "best_chain": round(best_c, 3),
            "decisive_rows": sum(1 for r in e["decision_rows"] if r["kind"] == "decisive"),
            "non_decisive_rows": sum(1 for r in e["decision_rows"] if r["kind"] != "decisive"),
            "contradictable_links": sum(1 for l in e["chain_links"] if l["branches_excludable"] and l["model"] not in e["_roster"]),
            "reopenable_closed_results": sum(1 for c in e.get("closed_results", []) if c["can_satisfy"] in ("yes", "partly")),
        })
    rows.sort(key=lambda r: (-r["E_total"], -(r["best_dec"] + r["best_chain"]), -r["reopenable_closed_results"], r["item"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


# ---------------------------------------------------------------- build

def build(repo: Path = REPO) -> dict:
    specs = load_specs()
    inputs = load_inputs(repo)
    roster = set(specs.ROSTER_MODELS)
    classes = decision_classes(inputs["disc"])
    models = chain_models(inputs["chain"], roster)
    items = []
    for spec in specs.ITEMS:
        links = item_links(spec, inputs["chain"])
        rows = decision_rows(spec, inputs["disc"])
        regs = registry_entries(spec, inputs["registry"])
        covs = coverage_entries(spec, inputs["cov"])
        preds = spec.get("other_predictions", [])
        entry = {k: v for k, v in spec.items() if k not in ("chain_coverage", "extra_links", "registry", "coverage_cases")}
        entry["decision_coverage"] = spec.get("decision_coverage", 0.0) if spec.get("decision_task") else 0.0
        entry["decision_rows"] = rows
        entry["chain_links"] = links
        linked = {l["model"] for l in links}
        entry["chain_models_without_prediction"] = [m["id"] for m in models if m["id"] not in linked]
        entry["registry"] = regs
        entry["coverage_cases"] = covs
        entry["registered_outcome_ids"] = outcome_ids(spec, links, rows, preds, regs, covs)
        entry["_roster"] = roster
        items.append(entry)
    ranking = {f"decisive_share_{s}": rank_items(items, s) for s in DECISIVE_SHARES}
    for entry in items:
        entry.pop("_roster")
    sources = [{"path": p, "sha256": sha256_file(repo / p)} for p in specs.SOURCE_FILES]
    register = {
        "schema_version": 1,
        "id": "arrival-register",
        "registered_utc": specs.REGISTERED_UTC,
        "status": ("Exploratory pre-registration. A prediction counts only if this file was committed "
                   "and pushed before the item arrived. As of " + specs.AS_OF + " no listed item has arrived; "
                   "parts that arrived earlier are marked 'arrived before registration: not a test'. "
                   "No identification, deposit or outcome-ledger count follows from any entry."),
        "rules": [
            "Silence is never a FAIL. An item that does not cover a relation is recorded as silent.",
            "No letter prediction is made for XII 10 or the 21/22 cut; those items carry only the mapping from frozen-protocol outcomes to model classes.",
            "Predictions restate existing repository models; where a model makes no prediction, the item says so.",
            "A changed prediction after arrival is a new exploratory model, never a rescue.",
        ],
        "sources": sources,
        "ranking_plan": {"path": "research/preregistration/arrivals/RANKING_PLAN.md",
                         "sha256": sha256_file(HERE / "RANKING_PLAN.md")},
        "coverage_levels": {str(k): v for k, v in specs.COVERAGE_LEVELS.items()},
        "class_universe": {
            "decision_classes": classes,
            "decision_class_count": sum(len(v) for v in classes.values()),
            "chain_models": models,
            "chain_models_outside_roster": sum(1 for m in models if not m["in_decision_roster"]),
            "chain_branches": ["RB-M", "RB-P", "RB-B"],
        },
        "items": items,
        "ranking": ranking,
    }
    return register


# ---------------------------------------------------------------- render

def class_legend(register: dict) -> dict:
    out = {}
    for fam, cls in register["class_universe"]["decision_classes"].items():
        for c in cls:
            out[c["id"]] = c["label"]
    return out


def fmt_excl(excl: dict) -> str:
    if not excl:
        return "none"
    return "; ".join(f"{f}: {', '.join(v)}" for f, v in excl.items())


def short(cid: str) -> str:
    if cid.startswith("xii10-c"):
        return "R" + str(int(cid[len("xii10-c"):]))
    return cid.replace("kohlit-", "").replace("entry25-", "e25-")


def per_class_lines(rows: list, register: dict) -> list[str]:
    """For each class in the affected families: which outcomes exclude it."""
    out = []
    fams = sorted({f for r in rows for f in r["surviving"]})
    for f in fams:
        if f == "xii10":
            out.append("- XII 10 strings R1–R7: these are the protocol's own alternatives; the protocol scores them. No further prediction is added.")
            continue
        for c in register["class_universe"]["decision_classes"][f]:
            exc = [r["id"] for r in rows if c["id"] in r["excluded"].get(f, [])]
            ok = [r["id"] for r in rows if r["kind"] == "decisive" and c["id"] not in r["excluded"].get(f, [])]
            if not exc:
                out.append(f"- `{short(c['id'])}` ({f}): no prediction about this item. It survives every registered outcome.")
            else:
                out.append(f"- `{short(c['id'])}` ({f}): compatible decisive outcomes: "
                           + (", ".join(f"`dec:{e}`" for e in ok) or "none")
                           + ". Excluded by: " + ", ".join(f"`dec:{e}`" for e in exc)
                           + ". Survives every other outcome, including silence.")
    return out


def render_item(item: dict, register: dict) -> str:
    legend = class_legend(register)
    L = []
    L.append(f"# {item['title']}")
    L.append("")
    L.append(f"Item `{item['id']}`. Registered {register['registered_utc']} by the arrival register. Exploratory; no identification or ledger count follows.")
    L.append("")
    L.append(f"- **Holder:** {item['holder']}")
    L.append(f"- **Requested:** {item['requested']} ({item['request_source']})")
    if item.get("request_detail"):
        L.append(f"- **Asked for:** {item['request_detail']}")
    L.append(f"- **Status on 9 October 2026:** {item['status']}. {item['status_note']}")
    if item["arrived_before_registration"]:
        for a in item["arrived_before_registration"]:
            L.append(f"- **Arrived before registration: not a test.** {a['what']} ({a['when']}; {a['source']}). {a['consequence']}")
    else:
        L.append("- **Arrived before registration:** nothing.")
    for e in item.get("exposure", []):
        L.append(f"- **Exposure:** {e}")
    L.append("")
    L.append("## What it bears on")
    L.append("")
    L.append(f"- Open questions: {', '.join(item['questions']) or 'none'}")
    L.append(f"- Active questions (ACTIVE_TEST): {', '.join(str(q) for q in item['active_questions']) or 'none'}")
    L.append(f"- Entries: {', '.join(item['entries']) or 'none'}")
    L.append(f"- Reserved observation: {'yes' if item['reserved'] else 'no'}")
    L.append("")
    L.append("## Handling on arrival")
    L.append("")
    L.append(item["handling"])
    L.append("")
    L.append("## Predictions by model family")
    L.append("")
    L.append("Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).")
    L.append("")
    # decision classes
    L.append("### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)")
    L.append("")
    rows = item["decision_rows"]
    if item.get("decision_task") and rows:
        L.append(f"Source: `discriminate.py` task `{item['decision_task']}`, read-only. Coverage factor c = {item['decision_coverage']}: {item.get('decision_coverage_reason', '')}")
        L.append("")
        if item["decision_task"] == "decisions-xii10":
            L.append("**Mapping only: no letter prediction.** Each row is a possible outcome of the frozen protocol. "
                     "Rule from the protocol's components: if R4 (שבינח) is rejected, the three Janoaḥ classes "
                     "(c08–c10, reading RB-L) are excluded; if R4 survives, all 10 Koḥlit classes survive, "
                     "because R4 support needs a separate linguistic and geographic argument. "
                     "Chain model M-JANOAH and registry record P60-T8 follow c08–c10.")
            L.append("")
            L.append("| Outcome id | Protocol outcome | Kind | Surviving strings | Surviving Koḥlit classes | Excluded Koḥlit classes |")
            L.append("|---|---|---|---|---|---|")
            for r in rows:
                s_str = ", ".join(short(x) for x in r["surviving"].get("xii10", [])) or "none"
                s_k = ", ".join(short(x) for x in r["surviving"].get("kohlit", [])) or "none"
                e_k = ", ".join(short(x) for x in r["excluded"].get("kohlit", [])) or "none"
                L.append(f"| `dec:{r['id']}` | {r['plans_outcome_id']} | {r['kind']} | {s_str} | {s_k} | {e_k} |")
            if item["decision_coverage"] == 0:
                L.append("")
                L.append("For this item the coverage factor is 0: its result maps to `dec:reading-gate-fails` (not identifiable). The table is shown for reference only.")
        else:
            L.append("| Outcome id | Kind | Basis | Outcome | Excluded classes |")
            L.append("|---|---|---|---|---|")
            for r in rows:
                L.append(f"| `dec:{r['id']}` | {r['kind']} | {r['basis']} | {r['label']} | {fmt_excl({f: [short(x) for x in v] for f, v in r['excluded'].items()})} |")
        L.append("")
        fams = sorted({f for r in rows for f in r["surviving"]})
        L.append("Class legend:")
        for f in fams:
            for c in register["class_universe"]["decision_classes"][f]:
                L.append(f"- `{short(c['id'])}` ({f}): {c['label']}")
        L.append("")
        L.append("What each class predicts for this item:")
        L.extend(per_class_lines(rows, register))
    else:
        L.append(f"No decision class depends on this item. Reason: {item.get('decision_none_reason', 'no decision task.')}")
    L.append("")
    # chain
    L.append("### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)")
    L.append("")
    if item["chain_links"]:
        L.append("Inconclusive if the record covers the place but meets neither criterion. Silent if it does not cover the place or relation; silence is never a FAIL.")
        L.append("")
        for l in item["chain_links"]:
            roster = " (model held by the decision classes; not counted again in the chain metric)" if l["model"] in ("M-SULTAN", "M-MARJAMA", "M-JANOAH") else ""
            L.append(f"**{l['model_label']}**, link `{l['link']}`{roster}")
            L.append("")
            L.append(f"- Branches: {l['branch']}. Relations: {', '.join(l['relations']) or 'reading gate'}. Reading dependencies: {', '.join(l['reading_dependencies']) or 'none'}.")
            if not l["relations"]:
                L.append("- Predicts: reading gate only. No letter expectation is restated here; the outcome follows the mapping table above (R4 rejected: contradicted; R4 surviving: not contradicted).")
            else:
                L.append(f"- Predicts: {l['predicts']}")
            missing = [b for b in ALL_BRANCHES if b not in l["branches_named"]]
            if l["relations"] and missing:
                L.append(f"- No prediction from this link under: {', '.join(missing)}.")
            if l.get("where"):
                L.append(f"- Where: {l['where']}")
            L.append(f"- Confirm if: {l['confirm_if']}")
            if l["contradiction_strength"] == "one-sided":
                L.append(f"- Contradict if: cannot contradict (one-sided). {l['contradict_if']}")
            else:
                L.append(f"- Contradict if ({l['contradiction_strength']}): {l['contradict_if']}")
            if roster:
                L.append("- Coverage factor: not used (the decision classes carry this model).")
            else:
                L.append(f"- Coverage factor c = {l['coverage']}." + (f" {l['coverage_note']}" if l.get("coverage_note") else ""))
            L.append(f"- Outcome ids: " + ", ".join(f"`chain:{l['link']}:{s}`" for s in OUTCOME_SUFFIXES if not (s == "contradict" and l["contradiction_strength"] == "one-sided")))
            L.append("")
    no_pred = item["chain_models_without_prediction"]
    labels = {m["id"]: m["label"] for m in register["class_universe"]["chain_models"]}
    L.append(f"No prediction from the other {len(no_pred)} chain models (no link of theirs uses this record): " + "; ".join(labels[m] for m in no_pred) + ".")
    L.append("")
    # registry
    L.append("### Entry 60 registry v2 (W2B registry_v2_entry60.json)")
    L.append("")
    if item["registry"]:
        for r in item["registry"]:
            L.append(f"- `{r['record']}` ({r['site']}; record SHA-256 {r['record_sha256'][:12]}…): {r['prediction']} Outcome ids: `reg:{r['record']}:as-predicted`, `…:not-as-predicted`, `…:silent`.")
    else:
        L.append("No registry record uses this item.")
    L.append("")
    # coverage
    if item["coverage_cases"]:
        L.append("### Coverage joins (feature_workbench/coverage)")
        L.append("")
        for c in item["coverage_cases"]:
            now = sorted({j["status_now"] for j in c["joins_now"]})
            L.append(f"- `{c['case']}`: {len(c['joins_now'])} joins, now {', '.join(now)}. Prediction: {c['prediction']} Outcome ids: `cov:{c['case']}:as-predicted`, `…:not-as-predicted`.")
        L.append("")
    # closed results
    L.append("### Closed results and their reopening criteria (ACTIVE_TEST)")
    L.append("")
    if item.get("closed_results"):
        for i, c in enumerate(item["closed_results"], 1):
            L.append(f"- {c['result']}. Reopen for: {c['reopen']} Can this item satisfy it: **{c['can_satisfy']}**. {c['reason']} Outcome ids: `closed{i}:reopen-triggered`, `closed{i}:not-triggered`.")
    else:
        L.append("None.")
    L.append("")
    # other predictions
    if item.get("other_predictions"):
        L.append("### Other registered predictions")
        L.append("")
        for i, p in enumerate(item["other_predictions"], 1):
            L.append(f"**pred{i}. {p['family']}: {p['model']}** ({p['label']})")
            L.append("")
            L.append(f"- Predicts: {p['predicts']}")
            L.append(f"- Confirm if: {p['confirm_if']}")
            L.append(f"- Contradict if: {p['contradict_if']}")
            L.append(f"- Inconclusive if: {p['inconclusive_if']}")
            L.append(f"- Silent if: {p['silent_if']}")
            L.append("")
    if item.get("rarity"):
        L.append("### Rarity units")
        L.append("")
        for k, v in item["rarity"].items():
            L.append(f"- {k}: {', '.join(v) if isinstance(v, list) else v}")
        L.append("")
    L.append("### Families with no prediction")
    L.append("")
    for n in item.get("no_prediction", []):
        L.append(f"- {n['family']}: {n['reason']}")
    L.append("")
    L.append("## Registered outcome ids")
    L.append("")
    L.append(", ".join(f"`{o}`" for o in item["registered_outcome_ids"]))
    L.append("")
    return "\n".join(L)


def render_ranking(register: dict) -> str:
    main = register["ranking"][f"decisive_share_{MAIN_SHARE}"]
    by_item = {s: {r["item"]: r["rank"] for r in register["ranking"][f"decisive_share_{s}"]} for s in DECISIVE_SHARES}
    L = ["# Ranking of pending items by expected separations", ""]
    L.append(f"Generated by `build_register.py` under the frozen plan `RANKING_PLAN.md` (SHA-256 `{register['ranking_plan']['sha256']}`). Descriptive only.")
    L.append("")
    L.append(f"Universe: {register['class_universe']['decision_class_count']} decision classes and {register['class_universe']['chain_models_outside_roster']} chain models outside the decision roster (counted in model equivalents). All values are conditional on the item arriving. Coverage factors and the equal-halves convention are declared in the plan; they are not probability estimates.")
    L.append("")
    L.append("| Rank | Item | E_dec (by family) | E_chain | E_total | Best case (dec + chain) | Decisive / non-decisive decision rows | Contradictable chain links | Closed results it can reopen |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for r in main:
        fam = ", ".join(f"{k} {v:.2f}" for k, v in r["E_dec_by_family"].items() if v) or "–"
        L.append(f"| {r['rank']} | `{r['item']}` | {r['E_dec']:.3f} ({fam}) | {r['E_chain']:.3f} | {r['E_total']:.3f} | {r['best_dec']} + {r['best_chain']:.2f} | {r['decisive_rows']} / {r['non_decisive_rows']} | {r['contradictable_links']} | {r['reopenable_closed_results']} |")
    L.append("")
    L.append("## Sensitivity to the decisive share")
    L.append("")
    L.append("| Item | Rank at ¼ | Rank at ½ | Rank at ¾ |")
    L.append("|---|---|---|---|")
    moved = []
    for r in main:
        ranks = [by_item[s][r["item"]] for s in DECISIVE_SHARES]
        if len(set(ranks)) > 1:
            moved.append(r["item"])
        L.append(f"| `{r['item']}` | {ranks[0]} | {ranks[1]} | {ranks[2]} |")
    L.append("")
    L.append("Ranks that move: " + (", ".join(f"`{m}`" for m in moved) if moved else "none") + ".")
    L.append("")
    return "\n".join(L)


def write_all(register: dict, out: Path) -> None:
    (out / "items").mkdir(parents=True, exist_ok=True)
    (out / "register.json").write_text(json.dumps(register, ensure_ascii=False, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    for item in register["items"]:
        (out / "items" / f"{item['id']}.md").write_text(render_item(item, register), encoding="utf-8")
    (out / "RANKING.md").write_text(render_ranking(register), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=HERE, help="output folder (default: this folder)")
    ap.add_argument("--repo-root", type=Path, default=REPO)
    args = ap.parse_args()
    register = build(args.repo_root.resolve())
    write_all(register, args.out)
    print(f"wrote {len(register['items'])} items, register.json and RANKING.md to {args.out}")


if __name__ == "__main__":
    main()
