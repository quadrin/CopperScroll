"""Finite research decisions, with hypothetical outcomes kept apart from evidence.

This module is a planning aid. Selecting an outcome never records a finding,
changes a request's status, reopens a test, or updates the historical queue.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_REPO = MODULE_DIR.parents[2]
QUEUE_PATH = "research/measurements/queue.json"
DISCRIMINATE_PATH = MODULE_DIR / "discriminate.py"
STATUSES = {"compatible", "contradicted", "unknown", "mixed", "info"}
REQUEST_STATES = {"sent_pending", "related_request_pending", "not_requested"}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _discriminate():
    """Load the logical discrimination search beside this evaluator.

    build.py loads this file by path, so a package-relative import is unavailable.
    """
    spec = importlib.util.spec_from_file_location("decisions_discriminate", DISCRIMINATE_PATH)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load {DISCRIMINATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validate(plans: dict, repo_root: Path) -> None:
    """Fail on ambiguous references or a future outcome presented as evidence."""
    if plans.get("mode") != "planning_only":
        raise ValueError("Decision outcomes must be planning_only")
    source_ids = [source["id"] for source in plans["sources"]]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Duplicate decision source ID")
    source_set = set(source_ids)
    feature_set = {
        feature["id"]
        for feature in _read_json(repo_root / "research/feature_workbench/features.json")["features"]
    }
    for source in plans["sources"]:
        if not source["id"].startswith("decisions-"):
            raise ValueError("Decision source ID must be module-prefixed")
        if not (repo_root / source["repo_path"]).is_file():
            raise ValueError(f"Missing source record: {source['repo_path']}")
        if source["inspection"] not in {"already_inspected", "not_inspected", "derived"}:
            raise ValueError("Unknown source inspection state")

    task_ids: set[str] = set()
    for task in plans["tasks"]:
        task_id = task["id"]
        if task_id in task_ids or not task_id.startswith("decisions-"):
            raise ValueError("Duplicate or unprefixed decision task ID")
        task_ids.add(task_id)
        if task["current_evidence"]["status"] not in STATUSES:
            raise ValueError("Invalid current evidence status")
        if task["request"]["status"] not in REQUEST_STATES:
            raise ValueError("Invalid request state")
        if task["freeze"]["unused_status"] != "unverified":
            raise ValueError("This queue cannot certify an unused observation")
        if not set(task["source_ids"]) <= source_set:
            raise ValueError(f"Unknown task source in {task_id}")
        if not set(task["feature_ids"]) <= feature_set:
            raise ValueError(f"Unknown feature in {task_id}")
        if not set(task["request"]["source_ids"]) <= source_set:
            raise ValueError(f"Unknown request source in {task_id}")
        outcome_ids: set[str] = set()
        has_inconclusive = False
        for outcome in task["outcomes"]:
            if outcome["id"] in outcome_ids:
                raise ValueError(f"Duplicate outcome in {task_id}")
            outcome_ids.add(outcome["id"])
            if outcome["status"] not in STATUSES or outcome["recorded"] is not False:
                raise ValueError("Possible outcomes are unrecorded planning branches")
            if not outcome["condition"] or not outcome["claim_scope"]:
                raise ValueError("Outcome must name its condition and claim scope")
            if not outcome["consequences"] or not outcome["remaining_unknowns"]:
                raise ValueError("Outcome must retain consequences and remaining limits")
            has_inconclusive |= outcome["status"] == "unknown"
        if not has_inconclusive:
            raise ValueError(f"Task {task_id} needs an inconclusive outcome")


def build(repo_root: Path) -> dict:
    repo_root = Path(repo_root).resolve()
    plans = _read_json(MODULE_DIR / "plans.json")
    _validate(plans, repo_root)
    discrimination_spec = _read_json(MODULE_DIR / "discrimination.json")
    # Logical separation of the surviving models. It reads plans.json and the
    # relationships/inventory evaluators without changing any status.
    discrimination = _discriminate().analyse(repo_root, copy.deepcopy(plans), discrimination_spec)
    queue_bytes = (repo_root / QUEUE_PATH).read_bytes()
    queue = json.loads(queue_bytes)
    # Import the historical source verbatim; its execution states are not current
    # readiness estimates and its activity totals are not incremented here.
    historical = {
        "repo_path": QUEUE_PATH,
        "sha256": hashlib.sha256(queue_bytes).hexdigest(),
        "interpretation": "Historical tracks as recorded; no execution status rewritten. Their next_action fields are reference material: ACTIVE_TEST and the contemporary record dependencies govern new work.",
        "tracks": copy.deepcopy(queue["tracks"]),
        "created_utc": queue["created_utc"],
        "last_update_utc": queue["last_update_utc"],
        "counts_as_recorded": copy.deepcopy(queue["counts"]),
        "execution_policy_as_recorded": copy.deepcopy(queue["execution_policy"]),
    }

    results = []
    for task in plans["tasks"]:
        # Actual evidence status supplies every result. Outcome selection supplies
        # none of these fields; it is only a preview of a conditional next step.
        results.append({
            "id": task["result_id"],
            "title": task["title"],
            "claim": task["claim"],
            "status": task["current_evidence"]["status"],
            "checks": [
                {
                    "id": task["id"] + "-current-evidence",
                    "label": "Recorded evidence",
                    "status": task["current_evidence"]["status"],
                    "detail": task["current_evidence"]["detail"],
                    "source_ids": task["source_ids"],
                    "feature_ids": task["feature_ids"],
                },
                {
                    "id": task["id"] + "-request",
                    "label": "Record access",
                    "status": "unknown",
                    "detail": task["request"]["scope"],
                    "source_ids": task["request"]["source_ids"],
                    "feature_ids": task["feature_ids"],
                    "value": {"status": task["request"]["status"], "delivery": task["request"]["delivery"], "reply": task["request"]["reply"]},
                },
                {
                    "id": task["id"] + "-specification",
                    "label": "Test specification and exposure",
                    "status": "info",
                    "detail": task["freeze"]["detail"],
                    "source_ids": task["source_ids"],
                    "feature_ids": task["feature_ids"],
                    "value": {"freeze": task["freeze"]["status"], "unused_status": task["freeze"]["unused_status"]},
                },
            ],
            "unknowns": task["record_needed"],
            "source_ids": task["source_ids"],
            "feature_ids": task["feature_ids"],
        })

    return {
        "id": "decisions",
        "number": 6,
        "title": "Decision queue",
        "summary": "Seven bounded record dependencies with finite possible outcomes, their branch consequences and an exact search for the records that separate the surviving models.",
        "scope": "Planning from the reviewed records as of 8 October 2026; six historical tracks remain as recorded. No outcome selection constitutes an observation or a research result. Discrimination is logical only: no probability or information gain.",
        "sources": plans["sources"] + discrimination_spec["sources"],
        "features": [],
        "observations": [],
        "states": [],
        "results": results,
        "data": {
            "schema_version": 1,
            "mode": "planning_only",
            "as_of_utc": plans["as_of_utc"],
            "historical_queue": historical,
            "priority_scale": plans["priority_scale"],
            "tasks": plans["tasks"],
            "selection_policy": plans["selection_policy"],
            "discrimination": discrimination,
        },
    }


def preview(task_id: str, outcome_id: str, repo_root: Path = DEFAULT_REPO) -> dict:
    """Return a labelled counterfactual without changing the evidence snapshot."""
    snapshot = build(repo_root)
    task = next((item for item in snapshot["data"]["tasks"] if item["id"] == task_id), None)
    if task is None:
        raise ValueError(f"Unknown decision task: {task_id}")
    outcome = next((item for item in task["outcomes"] if item["id"] == outcome_id), None)
    if outcome is None:
        raise ValueError(f"Unknown outcome {outcome_id} for {task_id}")
    return {
        "mode": "planning_only",
        "task_id": task_id,
        "result_id": task["result_id"],
        "label": "Possible outcome — not observed",
        "current_evidence": copy.deepcopy(task["current_evidence"]),
        "possible_outcome": copy.deepcopy(outcome),
        "source_ids": task["source_ids"],
        "research_state_changed": False,
        "request_action": "none",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--task")
    parser.add_argument("--outcome")
    args = parser.parse_args()
    if bool(args.task) != bool(args.outcome):
        parser.error("--task and --outcome must be supplied together")
    result = preview(args.task, args.outcome, args.repo_root) if args.task else build(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
