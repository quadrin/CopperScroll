#!/usr/bin/env python3
"""Build the reviewed feature register and atlas workbench from five evaluators."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MODULES = ("relationships", "inventory", "states", "coverage", "decisions")
STATUSES = {"compatible", "contradicted", "unknown", "mixed", "info"}
EXPOSURES = {"already_inspected", "not_inspected", "derived"}
EVIDENCE_KINDS = {"observed", "published_reconstruction", "excavator_label", "textual_constraint", "inference"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def index(records: list[dict], label: str) -> dict[str, dict]:
    found = {}
    for record in records:
        identifier = record.get("id")
        require(isinstance(identifier, str) and bool(identifier), f"{label}: missing id")
        require(identifier not in found, f"{label}: duplicate id {identifier}")
        found[identifier] = record
    return found


def refs(record: dict, key: str, known: dict, label: str) -> None:
    values = record.get(key, [])
    require(isinstance(values, list), f"{label}: {key} must be a list")
    require(all(isinstance(value, str) and value in known for value in values), f"{label}: unknown {key} {values}")


def validate_register(register: dict, repo_root: Path) -> None:
    features = index(register["features"], "features")
    sources = index(register["sources"], "sources")
    for feature in features.values():
        for key in ("name", "kind", "site"):
            require(isinstance(feature.get(key), str) and bool(feature[key]), f"{feature['id']}: missing {key}")
        require("geometry" in feature, f"{feature['id']}: geometry must be explicit, including null")
        if feature["geometry"] is not None:
            require(bool(feature.get("reference_frame")), f"{feature['id']}: geometry without reference frame")
    for source in sources.values():
        require(source.get("inspection") in EXPOSURES, f"{source['id']}: invalid inspection")
        for key in ("title", "citation", "repo_path"):
            require(isinstance(source.get(key), str) and bool(source[key]), f"{source['id']}: missing {key}")
        path = (repo_root / source["repo_path"]).resolve()
        require(path.is_relative_to(repo_root.resolve()) and path.is_file(), f"{source['id']}: missing or unsafe source file")
    for observation in index(register["observations"], "observations").values():
        require(observation.get("feature_id") in features, f"{observation['id']}: unknown feature")
        require(observation.get("evidence_kind") in EVIDENCE_KINDS, f"{observation['id']}: invalid evidence kind")
        require(observation.get("exposure") in EXPOSURES, f"{observation['id']}: invalid exposure")
        require(bool(observation.get("property")) and "value" in observation, f"{observation['id']}: property/value required")
        refs(observation, "source_ids", sources, observation["id"])
        require(bool(observation["source_ids"]), f"{observation['id']}: source required")
    for state in index(register["states"], "states").values():
        require(state.get("feature_id") in features, f"{state['id']}: unknown feature")
        require(state.get("status") in {"observed", "reconstructed", "unknown"}, f"{state['id']}: invalid state status")
        require(bool(state.get("label")), f"{state['id']}: state label required")
        refs(state, "source_ids", sources, state["id"])
        if state.get("geometry") is not None:
            require(bool(state.get("reference_frame")), f"{state['id']}: geometry without reference frame")


def validate_modules(modules: list[dict], register: dict) -> None:
    features, sources = index(register["features"], "features"), index(register["sources"], "sources")
    all_results = {}
    for module in modules:
        for key in ("title", "summary", "scope"):
            require(isinstance(module.get(key), str) and bool(module[key]), f"{module['id']}: missing {key}")
        require(bool(module.get("results")), f"{module['id']}: no evaluated results")
        for result in module["results"]:
            require(result["id"] not in all_results, f"duplicate result {result['id']}")
            all_results[result["id"]] = result
            require(result.get("status") in STATUSES, f"{result['id']}: invalid status")
            require(bool(result.get("title")) and bool(result.get("claim")), f"{result['id']}: title/claim required")
            require(isinstance(result.get("unknowns"), list), f"{result['id']}: unknowns must be explicit")
            refs(result, "source_ids", sources, result["id"])
            refs(result, "feature_ids", features, result["id"])
            for check in index(result.get("checks", []), result["id"] + " checks").values():
                require(check.get("status") in STATUSES, f"{check['id']}: invalid check status")
                require(bool(check.get("label")) and isinstance(check.get("detail"), str), f"{check['id']}: missing label/detail")
                refs(check, "source_ids", sources, check["id"])
                refs(check, "feature_ids", features, check["id"])


def build(repo_root: Path = ROOT) -> dict:
    here = repo_root / "research/feature_workbench"
    features = json.loads((here / "features.json").read_text())["features"]
    register = {"schema_version": 1, "features": features, "sources": [], "observations": [], "states": []}
    modules = []
    for number, name in enumerate(MODULES, start=2):
        path = here / name / "evaluate.py"
        spec = importlib.util.spec_from_file_location(f"feature_workbench_{name}", path)
        require(spec is not None and spec.loader is not None, f"Cannot load {path}")
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)
        result = evaluator.build(repo_root)
        require(result.get("id") == name and result.get("number") == number, f"Wrong module identity: {name}")
        module = dict(result)
        for key in ("features", "sources", "observations", "states"):
            records = module.pop(key, [])
            require(isinstance(records, list), f"{name}: {key} must be a list")
            register[key].extend(records)
            module[key[:-1] + "_ids" if key != "features" else "feature_ids"] = [record["id"] for record in records]
        modules.append(module)
    validate_register(register, repo_root)
    validate_modules(modules, register)
    payload = {
        "schema_version": 1,
        "reviewed": "2026-10-08",
        "method": "Exploratory evaluations of already inspected records. Compatibility does not establish identification. Missing observations remain unknown; source notices and publications are not counted as independent physical features or confirmation.",
        "limits": {"confirmatory": False, "unused_observation_certified": False, "regional_eligible_denominator": None, "new_source_inspections": 0, "new_outcomes": 0},
        "register": register,
        "modules": modules,
    }
    # Reject non-finite numeric JSON; reproducible snapshots do not depend on run time.
    json.dumps(payload, ensure_ascii=False, allow_nan=False)
    return payload


def rendered(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated snapshots differ")
    args = parser.parse_args()
    payload = build()
    outputs = {
        HERE / "register.json": rendered(payload["register"]),
        HERE / "results.json": rendered(payload),
        ROOT / "atlas/app/atlas-workbench.json": rendered(payload),
    }
    for path, content in outputs.items():
        if args.check:
            require(path.is_file() and path.read_text() == content, f"Stale generated snapshot: {path.relative_to(ROOT)}")
        else:
            path.write_text(content)
    print(f"{'Checked' if args.check else 'Built'} {len(payload['modules'])} modules; {len(payload['register']['features'])} feature records; {sum(len(m['results']) for m in payload['modules'])} exploratory result records.")


if __name__ == "__main__":
    main()
