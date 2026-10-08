"""Evaluate reviewed, finite landmark assignments without filling evidence gaps.

This module reads only local exploratory inputs. A compatible predicate is not an
identification, and an incompatible assignment does not reject its whole site.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

MODULE_DIR = Path(__file__).resolve().parent
STATUSES = {"compatible", "contradicted", "unknown", "mixed", "info"}


def conjunction(statuses: list[str]) -> str:
    """Conjoin required predicates; one miss rejects this assignment only."""
    if "contradicted" in statuses:
        return "contradicted"
    if "mixed" in statuses:
        return "mixed"
    if not statuses or "unknown" in statuses:
        return "unknown"
    return "compatible"


def _resolved(role: str | None, assignment: dict) -> str | None:
    return assignment["roles"].get(role) if role else None


def _facts(model: dict, subject: str, relation: str, target: str | None) -> list[dict]:
    return [
        observation for observation in model["observations"]
        if observation["feature_id"] == subject
        and observation["property"] == relation
        and observation["value"].get("reference_feature_id") == target
    ]


def evaluate_predicate(predicate: dict, assignment: dict, window: dict, model: dict) -> dict:
    """Resolve graph roles, then test only explicitly documented relations.

    Direction facts can be qualitative source statements. They do not imply a
    metric position or tolerance. Phase overlap requires a dated accessible-use
    interval; typological dating and relative phase order alone are insufficient.
    """
    relation = predicate["relation"]
    subject = _resolved(predicate["subject"], assignment)
    target = _resolved(predicate.get("object"), assignment)
    check = {
        "id": predicate["id"],
        "label": predicate["label"],
        "status": "unknown",
        "detail": predicate.get("missing_detail", "This relation is not documented for the selected features."),
        "source_ids": list(predicate["source_ids"]),
        "feature_ids": list(dict.fromkeys(f for f in (subject, target) if f)),
        "value": {
            "predicate_id": predicate["id"], "relation": relation,
            "subject_role": predicate["subject"], "object_role": predicate.get("object"),
            "resolved_subject": subject, "resolved_object": target,
            "observation_ids": [], "required": predicate.get("required", True),
        },
    }
    if subject is None or (predicate.get("object") and target is None):
        check["detail"] = "A required feature role is unassigned; report silence cannot supply or exclude a feature. " + check["detail"]
        return check

    if relation == "exists_during":
        observations = _facts(model, subject, "chronology", None)
        evaluations = []
        for observation in observations:
            value = observation["value"]
            status = "unknown"
            detail = observation["note"]
            earliest = value.get("secure_earliest_construction_year")
            last = value.get("secure_last_accessible_year")
            accessible = value.get("dated_accessible_interval")
            # A securely later construction or sealed earlier last use is a
            # genuine interval miss. Historical observation is not construction.
            if earliest is not None and earliest > window["years"][1]:
                status = "contradicted"
                detail = f"Secure construction in {earliest} CE is after the {window['label']} window. " + detail
            elif last is not None and last < window["years"][0]:
                status = "contradicted"
                detail = "Secure last accessible use precedes the selected window. " + detail
            elif accessible is not None:
                start, end = accessible
                if max(start, window["years"][0]) <= min(end, window["years"][1]):
                    status = "compatible"
                elif value.get("accessible_interval_exhaustive") is True:
                    status = "contradicted"
                else:
                    status = "unknown"
                    detail = "Documented use outside the window does not exclude earlier undocumented use. " + detail
                detail = "The documented accessible-use interval was compared with the selected window. " + detail
            evaluations.append((status, detail, observation))
    elif relation == "coexisted_with":
        # A direct phase-controlled observation can establish joint use. Two
        # separate date ranges or a succession relation cannot establish it.
        observations = _facts(model, subject, relation, target)
        evaluations = []
        for observation in observations:
            value = observation["value"]
            status, detail = "unknown", observation["note"]
            asserted, interval = value.get("asserted"), value.get("dated_joint_accessible_interval")
            if value.get("window_id") == window["id"] and asserted is not None:
                status = "compatible" if asserted else "contradicted"
            elif asserted is True and interval is not None:
                if max(interval[0], window["years"][0]) <= min(interval[1], window["years"][1]):
                    status = "compatible"
                elif value.get("joint_accessible_interval_exhaustive") is True:
                    status = "contradicted"
            elif asserted is not None:
                detail = "The joint-state observation lacks a dated accessible interval or an explicit window-specific exclusion. " + detail
            evaluations.append((status, detail, observation))
    else:
        observations = _facts(model, subject, relation, target)
        evaluations = [
            ("unknown" if o["value"].get("asserted") is None else
             "compatible" if o["value"]["asserted"] else "contradicted", o["note"], o)
            for o in observations
        ]

    if not evaluations:
        return check
    statuses = {status for status, _, _ in evaluations if status != "unknown"}
    check["status"] = "mixed" if len(statuses) > 1 else next(iter(statuses), "unknown")
    check["detail"] = " ".join(dict.fromkeys(detail for _, detail, _ in evaluations))
    check["source_ids"] = list(dict.fromkeys(check["source_ids"] + [source for _, _, o in evaluations for source in o["source_ids"]]))
    check["value"]["observation_ids"] = [o["id"] for _, _, o in evaluations]
    return check


def evaluate_branch(reading: dict, assignment: dict, window: dict, model: dict) -> dict:
    predicates = {p["id"]: p for p in model["predicates"]}
    checks = [evaluate_predicate(predicates[p], assignment, window, model) for p in reading["predicate_ids"]]
    branch_id = f"relationships-{assignment['id']}-{reading['id']}-{window['id']}"
    for check in checks:
        check["id"] = f"{branch_id}-{check['id']}"
    status = conjunction([c["status"] for c in checks if c["value"]["required"]])
    return {
        "id": branch_id,
        "title": f"{assignment['label']} · {reading['label']} · {window['label']}",
        "claim": "The selected physical features satisfy this exploratory Entry 11 / Entry 60 relationship branch within the selected use window.",
        "status": status,
        "checks": checks,
        "unknowns": list(dict.fromkeys(c["detail"] for c in checks if c["status"] in {"unknown", "mixed"})),
        "source_ids": list(dict.fromkeys(s for c in checks for s in c["source_ids"])),
        "feature_ids": list(dict.fromkeys(f for c in checks for f in c["feature_ids"])),
    }


def build(repo_root: Path) -> dict[str, Any]:
    model = json.loads((MODULE_DIR / "model.json").read_text(encoding="utf-8"))
    # Fail stale pointers rather than rendering undocumented evidence.
    for source in model["sources"]:
        if not (repo_root / source["repo_path"]).is_file():
            raise ValueError(f"Missing source pointer: {source['repo_path']}")
    results, branches = [], []
    readings = {r["id"]: r for r in model["readings"]}
    for assignment in model["assignments"]:
        for reading_id in assignment["reading_ids"]:
            for window in model["windows"]:
                result = evaluate_branch(readings[reading_id], assignment, window, model)
                results.append(result)
                branches.append({
                    "id": result["id"], "label": result["title"],
                    "reading_id": reading_id, "assignment_id": assignment["id"],
                    "window_id": window["id"], "result_id": result["id"],
                    "check_ids": [c["id"] for c in result["checks"]],
                })

    # Keep the genuine relative-phase contradiction visible without pretending
    # that construction in successive phases disproves later joint accessibility.
    quarry_assignment = next(a for a in model["assignments"] if a["id"] == "jericho-quarry")
    phase_predicate = next(p for p in model["predicates"] if p["id"] == "same-construction-phase")
    phase_check = evaluate_predicate(phase_predicate, quarry_assignment, model["windows"][0], model)
    phase_check["id"] = "relationships-quarry-phase-check"
    results.append({
        "id": "relationships-quarry-phase-order", "title": "Later quarry pits and earlier north-slope graves",
        "claim": "The phase-lxxvii quarry pits were constructed in the same stratigraphic phase as the phase-lxxvi graves.",
        "status": phase_check["status"], "checks": [phase_check],
        "unknowns": ["Whether later openings and surviving graves were jointly accessible within either early window remains unknown."],
        "source_ids": phase_check["source_ids"], "feature_ids": phase_check["feature_ids"],
    })
    return {
        "id": "relationships", "number": 2, "title": "Landmark relationships",
        "summary": "Compare finite Koḥlit assignments against separate edition-based relations and use windows. Retain each failed and unresolved branch.",
        "scope": "Exploratory Entry 11 / Entry 60 pilot at Jericho, Ein Samiya and the reading-dependent Yanun route. This selected roster cannot establish regional discrimination or identification.",
        "sources": model["sources"], "features": model["features"],
        "observations": model["observations"], "states": [], "results": results,
        "data": {
            "readings": model["readings"], "windows": model["windows"],
            "assignments": model["assignments"], "predicates": model["predicates"],
            "branches": branches, "graph_roles": model["graph_roles"],
            "supplementary_graph": model["supplementary_graph"],
            "limits": model["limits"], "exposure": "already_inspected_exploratory",
            "regional_denominator": None, "unused_prediction": None,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=MODULE_DIR.parents[2])
    args = parser.parse_args()
    print(json.dumps(build(args.repo_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
