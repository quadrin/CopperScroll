"""Logical observation planning; pair counts are never probabilities or confidence.

Predictions are conservative sets of compatible decisive outcomes. None means
the model makes no prediction; this expands to the complete outcome universe.
An unresolved empirical outcome never excludes a model. All plans are conditional
on their acquisition and observation gates, which are not asserted completed.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]
BASE_COMMIT = "897733283606988581155a3c1df0cd235cb7bea9"


def outcome_set(prediction, universe):
    """Unknown permits every decisive outcome, rather than acting as a category."""
    if prediction is None:
        return frozenset(universe)
    values = frozenset(prediction)
    if not values or not values <= frozenset(universe):
        raise ValueError("A prediction must be unknown or a nonempty subset of outcomes")
    return values


def collapse_hypotheses(hypotheses, observations):
    """Union nuisance branches first, then collapse identical observable signatures.

    The union preserves a family's best permitted alternative. Adding an identical
    branch cannot multiply its influence; adding a different branch can only make
    that family harder to exclude. Preserve correlations recorded in the explicit
    nuisance branches. Inside each branch, unrecorded correlations remain unknown:
    every combination of its marginal compatible outcomes is permitted.
    """
    families = defaultdict(list)
    for hypothesis in hypotheses:
        families[hypothesis.get("family_id", hypothesis["id"])].append(hypothesis)
    grouped = defaultdict(list)
    for family_id, branches in sorted(families.items()):
        if math.prod(len(o["outcomes"]) for o in observations) > 200000:
            raise ValueError("Joint outcome universe exceeds the exact planner's bound")
        boxes = {
            tuple(tuple(sorted(outcome_set(b.get("predictions", {}).get(o["id"]), o["outcomes"])))
                  for o in observations)
            for b in branches
        }
        # Full joint outcome signatures prevent correlated nuisance alternatives
        # from being broadened into combinations that no branch permits.
        signature = tuple(sorted(set().union(*[
            set(itertools.product(*box)) for box in boxes
        ])))
        grouped[signature].append({
            "family_id": family_id,
            "branch_ids": sorted(set(b["id"] for b in branches)),
            "labels": sorted(set(b.get("label", b["id"]) for b in branches)),
        })
    return [{
        "id": f"C{index:02d}",
        "families": groups,
        "predictions": {o["id"]: sorted({v[i] for v in signature})
                        for i, o in enumerate(observations)},
        "_joint_vectors": frozenset(signature),
    } for index, (signature, groups) in enumerate(sorted(grouped.items()), 1)]


def dependency_closure(ids, dependencies):
    index = {d["id"]: d for d in dependencies}
    if len(index) != len(dependencies):
        raise ValueError("Duplicate dependency IDs")
    closed, active = set(), set()

    def visit(node):
        if node in active:
            raise ValueError(f"Dependency cycle at {node}")
        if node in closed:
            return
        if node not in index:
            raise ValueError(f"Missing dependency {node}")
        active.add(node)
        for parent in index[node].get("requires", []):
            visit(parent)
        active.remove(node)
        closed.add(node)

    for node in ids:
        visit(node)
    return sorted(closed)


def admissible(observation, dependencies, scenario):
    nodes = dependency_closure(observation.get("dependencies", []), dependencies)
    states = {d["id"]: d["status"] for d in dependencies}
    if scenario == "available_now":
        return all(states[n] == "ready" for n in nodes)
    if scenario == "named_dependencies":
        return all(states[n] in {"ready", "pending", "future_gate"} for n in nodes)
    if scenario == "all_planning":
        return True
    raise ValueError(f"Unknown scenario {scenario}")


def separating_pairs(classes, observation):
    return frozenset(
        (a["id"], b["id"]) for a, b in itertools.combinations(classes, 2)
        if set(a["predictions"][observation["id"]]).isdisjoint(
            b["predictions"][observation["id"]])
    )


def joint_separating_pairs(classes, selected, observations):
    """Disjoint projections separate even when each marginal set overlaps."""
    indices = [i for i, o in enumerate(observations) if o["id"] in selected]
    projected = {
        c["id"]: {tuple(v[i] for i in indices) for v in c["_joint_vectors"]}
        for c in classes
    }
    return frozenset((a["id"], b["id"]) for a, b in itertools.combinations(classes, 2)
                     if projected[a["id"]].isdisjoint(projected[b["id"]]))


def directional_opportunities(classes, observation):
    """Outcomes retaining one class and excluding another; no chance is assigned."""
    opportunities = []
    for a, b in itertools.permutations(classes, 2):
        a_set = set(a["predictions"][observation["id"]])
        b_set = set(b["predictions"][observation["id"]])
        outcomes = sorted(a_set - b_set)
        if outcomes:
            opportunities.append({"retained": a["id"], "excluded": b["id"], "outcomes": outcomes})
    return opportunities


def minimal_covers(coverage, target, observations, dependencies, classes=None, all_observations=None):
    """Exact minimum-cardinality cover; every tied minimum is retained.

    A dependency is an acquisition/gate cost, not another observation. Report
    its distinct closure without attaching an invented numerical effort value.
    Empty target means no separating observation is attainable, not success at
    identifying the models. Enumeration is bounded to this small planning roster.
    """
    if not target:
        return []
    usable = observations if classes is not None else [o for o in observations if coverage[o["id"]]]
    if len(usable) > 24:
        raise ValueError("Exact enumeration supports at most 24 nonempty observations")
    for count in range(1, len(usable) + 1):
        answers = []
        for chosen in itertools.combinations(usable, count):
            reached = (joint_separating_pairs(classes, {o["id"] for o in chosen}, all_observations)
                       if classes is not None else set().union(*(coverage[o["id"]] for o in chosen)))
            if target <= reached:
                dep_ids = dependency_closure(
                    [d for o in chosen for d in o.get("dependencies", [])], dependencies)
                answers.append({
                    "observations": [o["id"] for o in chosen],
                    "dependency_ids": dep_ids,
                    "acquisition_ids": [d["id"] for d in dependencies
                                        if d["id"] in dep_ids and d.get("kind") == "acquisition"],
                })
        if answers:
            return answers
    return []


def analyze(domain, dependencies, scenario):
    observations = domain["observations"]
    classes = collapse_hypotheses(domain["hypotheses"], observations)
    selected = [o for o in observations if admissible(o, dependencies, scenario)]
    coverage = {o["id"]: separating_pairs(classes, o) for o in selected}
    attained = joint_separating_pairs(classes, {o["id"] for o in selected}, observations)
    all_pairs = set(itertools.combinations([c["id"] for c in classes], 2))
    ranks = []
    for observation in selected:
        directional = directional_opportunities(classes, observation)
        ranks.append({
            "observation_id": observation["id"],
            "separated_pairs": sorted(map(list, coverage[observation["id"]])),
            "separated_pair_count": len(coverage[observation["id"]]),
            "directional_opportunities": directional,
            "directional_pair_count": len(directional),
            "dependency_ids": dependency_closure(observation.get("dependencies", []), dependencies),
        })
    # These tiers order logical capability. A tie does not justify a scientific
    # priority; timing, source availability and project value remain qualitative.
    ranks.sort(key=lambda r: (-r["separated_pair_count"], -r["directional_pair_count"], r["observation_id"]))
    return {
        "scenario": scenario,
        "class_count": len(classes),
        "class_pair_count": len(all_pairs),
        "classes": [{k: v for k, v in c.items() if k != "_joint_vectors"} for c in classes],
        "attainable_pair_count": len(attained),
        "attainable_pairs": sorted(map(list, attained)),
        "unseparable_pairs": sorted(map(list, all_pairs - attained)),
        "perfect_separation_conditional_on_decisive_results": bool(all_pairs) and attained == all_pairs,
        "minimum_sets_for_all_attainable_pairs": minimal_covers(
            coverage, attained, selected, dependencies, classes, observations),
        "capability_order": ranks,
    }


def survivors(domain, observation_id, outcome):
    """Return original branches compatible with one previewed empirical outcome."""
    observation = next(o for o in domain["observations"] if o["id"] == observation_id)
    observed = {outcome} if isinstance(outcome, str) else set(outcome)
    if "unresolved" in observed:
        return [h["id"] for h in domain["hypotheses"]]
    if not observed or not observed <= set(observation["outcomes"]):
        raise ValueError(f"Outcome {outcome} is outside this observation's universe")
    return [h["id"] for h in domain["hypotheses"]
            if observed & outcome_set(h.get("predictions", {}).get(observation_id), observation["outcomes"])]


def source_record(root, relative, baseline=True):
    data = (root / relative).read_bytes()
    result = {"repo_path": relative, "sha256": hashlib.sha256(data).hexdigest(),
              "provenance": "pinned_exposed_source" if baseline else "new_local_derived_artifact"}
    if baseline:
        result["url"] = f"https://github.com/quadrin/CopperScroll/blob/{BASE_COMMIT}/{relative}"
    return result


def load_relationship_evaluator(root):
    path = root / "research/feature_workbench/relationships/evaluate.py"
    spec = importlib.util.spec_from_file_location("relationship_evaluator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_inputs(root):
    """Derive sets from the exposed registry; do not turn gate outcomes into sites."""
    config = json.loads((HERE / "specification.json").read_text())
    plans_path = "research/feature_workbench/decisions/plans.json"
    model_path = "research/feature_workbench/relationships/model.json"
    protocol_path = "research/agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md"
    plans = json.loads((root / plans_path).read_text())
    model = json.loads((root / model_path).read_text())
    protocol = (root / protocol_path).read_text()
    evaluator = load_relationship_evaluator(root)
    reading_task = next(t for t in plans["tasks"] if t["id"] == "decisions-xii10")
    readings = reading_task["registered_readings"]
    expected_strings = {"R1": "שכנה", "R2": "שבנה", "R3": "שבצח", "R4": "שבינח",
                        "R5": "שכינה", "R6": "שכונה", "R7": "שבצהב"}
    if {r["id"]: r["sequence"] for r in readings} != expected_strings:
        raise ValueError("The registered reading set changed; revise exploratory segmentation explicitly")
    if any(f"{r['id']} `" not in protocol for r in readings):
        raise ValueError("A registered reading is absent from the source protocol")
    reading_hypotheses = []
    for reading in readings:
        sequence = reading["sequence"]
        # Components follow the registered stage-2 box, medial and tail/extra-sign
        # questions. Tail is an ordered suffix, not an asserted saw-cut location.
        if sequence == expected_strings["R7"]:
            medial, tail = "צ", "הב"
        else:
            medial, tail = sequence[2:-1], sequence[-1]
        reading_hypotheses.append({
            "id": reading["id"], "label": sequence,
            "predictions": {"xii10-box": [sequence[1]], "xii10-medial": [medial], "xii10-tail": [tail]},
            "source_task": reading_task["id"], "source_path": protocol_path,
        })
    reading_domain = {"id": "xii10-letters", "claim": reading_task["claim"],
                      "hypotheses": reading_hypotheses, "observations": config["reading_observations"]}
    archaeological, excluded = [], []
    readings_by_id = {r["id"]: r for r in model["readings"]}
    predicates = {p["id"]: p for p in model["predicates"]}
    for observation in config["relationship_observations"]:
        observation["source_ids"] = list(predicates[observation["predicate_id"]]["source_ids"])
    for observation in config["reading_observations"]:
        observation["source_ids"] = list(reading_task["source_ids"])
    for assignment in model["assignments"]:
        for reading_id in assignment["reading_ids"]:
            reading = readings_by_id[reading_id]
            for window in model["windows"]:
                result = evaluator.evaluate_branch(reading, assignment, window, model)
                branch = {
                    "id": result["id"], "family_id": f"{assignment['id']}:{reading_id}",
                    "label": result["title"], "assignment_id": assignment["id"],
                    "reading_id": reading_id, "window_id": window["id"],
                    "existing_status": result["status"], "source_ids": result["source_ids"],
                    "predictions": {},
                }
                if result["status"] == "contradicted":
                    branch["reason"] = [c for c in result["checks"] if c["status"] == "contradicted"]
                    excluded.append(branch)
                    continue
                for observation in config["relationship_observations"]:
                    p = predicates[observation["predicate_id"]]
                    required = p["id"] in reading["predicate_ids"]
                    subject = assignment["roles"].get(p["subject"])
                    target = assignment["roles"].get(p.get("object")) if p.get("object") else None
                    matches = subject is not None and subject == observation["subject_feature_id"]
                    matches = matches and target == observation.get("object_feature_id")
                    # An assignment to another site does not predict absence of
                    # this feature. An optional textual constraint also predicts
                    # no absence. Only a required, exactly matched role yields a
                    # positive conditional prediction.
                    if required and matches:
                        if observation.get("window_sensitive"):
                            values = ["early"] if window["id"] == "early" else ["early", "extended-only"]
                        else:
                            values = ["satisfied"]
                        branch["predictions"][observation["id"]] = values
                    else:
                        branch["predictions"][observation["id"]] = None
                archaeological.append(branch)
    relationship_domain = {
        "id": "kohlit-relationships",
        "claim": "Conservative observable consequences of retained exposed Entry 11/60 assignments; no regional identification claim.",
        "hypotheses": archaeological, "excluded_by_existing_evidence": excluded,
        "observations": config["relationship_observations"],
    }
    imported_queue = [{
        "task_id": t["id"], "claim": t["claim"], "priority": t["priority"],
        "priority_reason": t["priority_reason"], "current_evidence": t["current_evidence"],
        "request": t["request"], "access": t["access"], "effort": t["effort"],
        "freeze": t["freeze"], "outcomes": t["outcomes"], "source_ids": t["source_ids"],
        "pair_ranking": "Not pooled across independent claims or translated into mutually exclusive site predictions.",
    } for t in plans["tasks"]]
    return {
        "schema_version": 1, "mode": "exploratory_conditional_planning", "base_commit": BASE_COMMIT,
        "input_sources": [source_record(root, p) for p in [plans_path, model_path, protocol_path,
                           "research/feature_workbench/relationships/evaluate.py"]] +
                         [source_record(root, "research/feature_workbench/decisions/separation/" + name, baseline=False)
                          for name in ["specification.json", "planner.py"]],
        "dependencies": config["dependencies"], "domains": [reading_domain, relationship_domain],
        "source_catalogue": deepcopy(plans["sources"] + model["sources"]),
        "imported_queue": imported_queue,
        "limits": config["limits"],
    }


def run(root):
    inputs = build_inputs(root)
    return {"schema_version": 1, "mode": inputs["mode"], "base_commit": BASE_COMMIT,
            "input_sources": inputs["input_sources"], "domains": {
                d["id"]: {scenario: analyze(d, inputs["dependencies"], scenario)
                          for scenario in ["available_now", "named_dependencies", "all_planning"]}
                for d in inputs["domains"]}, "limits": inputs["limits"]}, inputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--write", action="store_true", help="Write only this module's inputs/results JSON")
    parser.add_argument("--domain", choices=["xii10-letters", "kohlit-relationships"])
    parser.add_argument("--observation")
    parser.add_argument("--outcome")
    args = parser.parse_args()
    output, inputs = run(args.repo_root)
    if args.observation or args.outcome:
        if not (args.domain and args.observation and args.outcome):
            parser.error("A preview requires --domain, --observation and --outcome")
        domain = next(d for d in inputs["domains"] if d["id"] == args.domain)
        output = {"label": "Possible outcome — not observed", "domain": args.domain,
                  "observation": args.observation, "outcome": args.outcome,
                  "surviving_branches": survivors(domain, args.observation, args.outcome.split(",")),
                  "scope": domain["claim"]}
    elif args.write:
        (HERE / "prediction_sets.json").write_text(json.dumps(inputs, ensure_ascii=False, indent=2) + "\n")
        (HERE / "results.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
