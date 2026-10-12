"""Conservative recovery of redacted, published archaeological feature records.

This exposed pilot evaluates documentary compatibility. Unknown observations
survive; a high score never eliminates a candidate with missing observations.
Prediction reads reviewer inputs only. Grading reads the separate answer key.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "copper-scroll-feature-recovery-pilot-v1"
ACCEPTED_BASES = {"reported_observation", "published_description"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def compare(observation, predicate):
    """Three-valued matching; source silence and inferred directions stay unknown."""
    if ("equals" in predicate) == ("range" in predicate):
        raise ValueError("Predicate needs exactly one operator")
    if "range" in predicate:
        span = predicate["range"]
        if len(span) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in span) or span[0] > span[1]:
            raise ValueError("Range must have finite ordered numeric bounds")
    if observation is None or observation.get("value") is None:
        return "unknown"
    if predicate.get("requires_observation", True) and observation.get("basis") not in ACCEPTED_BASES:
        return "unknown"
    value = observation["value"]
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Observation must be finite")
    if "equals" in predicate:
        # Prevent Python's bool/int equality from accepting a count of True.
        return "match" if type(value) is type(predicate["equals"]) and value == predicate["equals"] else "contradiction"
    if "range" in predicate:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Numeric predicate applied to nonnumeric observation")
        lo, hi = predicate["range"]
        return "match" if lo <= value <= hi else "contradiction"
    raise ValueError("Predicate needs equals or range")


def predict(packet):
    validate_packet(packet)
    answers = []
    for case in packet["cases"]:
        evaluated = []
        for candidate in case["candidates"]:
            checks = [{"field": p["field"], "outcome": compare(candidate["facts"].get(p["field"]), p)}
                      for p in case["predicates"]]
            contradictions = [c["field"] for c in checks if c["outcome"] == "contradiction"]
            unknowns = [c["field"] for c in checks if c["outcome"] == "unknown"]
            evaluated.append({"candidate_code": candidate["code"], "contradictions": contradictions,
                              "unknown_fields": unknowns, "matched_fields": [c["field"] for c in checks if c["outcome"] == "match"]})
        survivors = [c for c in evaluated if not c["contradictions"]]
        if not survivors:
            decision, selected = "no_compatible_candidate", None
        elif len(survivors) == 1 and not survivors[0]["unknown_fields"]:
            decision, selected = "unique_documentary_match", survivors[0]["candidate_code"]
        else:
            decision, selected = "insufficient_evidence", None
        forecasts = []
        for survivor in survivors:
            model = next(c for c in case["candidates"] if c["code"] == survivor["candidate_code"])
            for field, obs in model.get("model_forecasts", {}).items():
                forecasts.append({"candidate_code": model["code"], "field": field, **obs,
                                  "claim_scope": "exposed_source_expectation_excluded_from_matching"})
        answers.append({"case_code": case["code"], "decision": decision,
                        "selected_candidate_code": selected,
                        "surviving_candidate_codes": [s["candidate_code"] for s in survivors],
                        "candidate_checks": evaluated, "forecasts": forecasts})
    return {"schema": SCHEMA, "reviewer_input_sha256": digest(packet), "responses": answers,
            "evidence_class": "exposed_published_record_recovery",
            "independent_field_accuracy": None, "unseen_confirmation": False}


def validate_packet(packet):
    if packet.get("schema") != SCHEMA:
        raise ValueError("Unknown packet schema")
    case_codes = [c["code"] for c in packet["cases"]]
    if len(set(case_codes)) != len(case_codes):
        raise ValueError("Duplicate case codes")
    forbidden = {"answer", "target", "target_id", "source_url", "source_id", "source_label", "expected", "truth"}
    def walk(value):
        if isinstance(value, dict):
            if forbidden.intersection(value):
                raise ValueError("Coordinator data leaked into reviewer packet")
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(packet)
    for case in packet["cases"]:
        codes = [c["code"] for c in case["candidates"]]
        if len(set(codes)) != len(codes):
            raise ValueError("Duplicate candidate codes")
        if not case["predicates"]:
            raise ValueError("A case requires at least one predicate")
        for predicate in case["predicates"]:
            if ("equals" in predicate) == ("range" in predicate):
                raise ValueError("Predicate needs exactly one operator")
            if "range" in predicate:
                span = predicate["range"]
                if len(span) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in span) or span[0] > span[1]:
                    raise ValueError("Range must have finite ordered numeric bounds")
        forecast_fields = set(case.get("excluded_from_matching", []))
        if forecast_fields.intersection(p["field"] for p in case["predicates"]):
            raise ValueError("Forecast observation reused for matching")
        for candidate in case["candidates"]:
            if forecast_fields.intersection(candidate["facts"]):
                raise ValueError("Forecast observation present in matching facts")


def prepare(dataset, output):
    """Create separate distribution boundaries; same-workspace storage is not access control."""
    output = Path(output)
    models = {m["id"]: m for m in dataset["models"]}
    packet = {"schema": SCHEMA, "exposure": "analyst_exposed; software_separation_only", "cases": []}
    key = {"schema": SCHEMA, "cases": [], "sources": dataset["sources"],
           "exposure": dataset["exposure"], "dataset_sha256": digest(dataset)}
    for i, case in enumerate(dataset["cases"], 1):
        code = f"R{i:03d}"
        excluded = case.get("forecast_fields", [])
        candidates, mappings = [], {}
        for j, model_id in enumerate(case["model_ids"], 1):
            model = models[model_id]
            candidate_code = f"K{j:02d}"
            mappings[candidate_code] = model_id
            candidates.append({"code": candidate_code,
                               "facts": {k: v for k, v in model["facts"].items() if k not in excluded},
                               "model_forecasts": {k: model["facts"].get(k, {"value": None, "basis": "unknown"}) for k in excluded}})
        packet["cases"].append({"code": code, "description": case["redacted_description"],
                                "predicates": case["predicates"], "excluded_from_matching": excluded,
                                "candidates": candidates})
        key["cases"].append({"code": code, **{k: v for k, v in case.items() if k != "model_ids"},
                             "candidate_mapping": mappings})
    validate_packet(packet)
    key["reviewer_input_sha256"] = digest(packet)
    write(output / "reviewer" / "packet.json", packet)
    write(output / "reviewer" / "responses_blank.json", {"schema": SCHEMA, "reviewer_input_sha256": digest(packet),
          "responses": [{"case_code": c["code"], "decision": None, "selected_candidate_code": None,
                          "surviving_candidate_codes": [], "forecasts": []} for c in packet["cases"]]})
    write(output / "coordinator" / "answer_key.json", key)
    write(output / "coordinator" / "freeze_manifest.json", {"schema": SCHEMA, "dataset_sha256": digest(dataset),
          "reviewer_input_sha256": digest(packet), "answer_key_sha256": digest(key),
          "distribution_rule": "Give reviewers reviewer/ only. Keep coordinator/ separately.",
          "seal_scope": "Content-hash integrity; no OS access-control or analyst blindness claim."})
    return packet, key


def grade(packet, predictions, key, freeze):
    validate_packet(packet)
    if digest(key) != freeze.get("answer_key_sha256") or digest(packet) != freeze.get("reviewer_input_sha256"):
        raise ValueError("Answer key or packet differs from coordinator freeze manifest")
    if digest(packet) != predictions.get("reviewer_input_sha256") or digest(packet) != key.get("reviewer_input_sha256"):
        raise ValueError("Packet hash differs from prediction or answer key")
    responses = {r["case_code"]: r for r in predictions["responses"]}
    if len(responses) != len(predictions["responses"]) or set(responses) != {c["code"] for c in key["cases"]}:
        raise ValueError("Missing, duplicate or unexpected response cases")
    results = []
    packet_cases = {c["code"]: c for c in packet["cases"]}
    for case in key["cases"]:
        response = responses[case["code"]]
        mapping = case["candidate_mapping"]
        candidate_codes = response["surviving_candidate_codes"]
        if len(set(candidate_codes)) != len(candidate_codes) or any(c not in mapping for c in candidate_codes):
            raise ValueError("Invalid survivor codes")
        actual_survivors = sorted(mapping[c] for c in candidate_codes)
        selected = response["selected_candidate_code"]
        if selected is not None and (selected not in candidate_codes or selected not in mapping):
            raise ValueError("Selected candidate is not a survivor")
        selected_id = mapping[selected] if selected is not None else None
        decision = response["decision"]
        if decision not in {"unique_documentary_match", "insufficient_evidence", "no_compatible_candidate"}:
            raise ValueError("Invalid decision value")
        if decision == "unique_documentary_match" and (selected is None or candidate_codes != [selected]):
            raise ValueError("Unique match requires exactly one selected survivor")
        if decision != "unique_documentary_match" and selected is not None:
            raise ValueError("Abstention decisions cannot select a winner")
        if decision == "no_compatible_candidate" and candidate_codes:
            raise ValueError("No-compatible-candidate decision has survivors")
        valid_unique = False
        if selected is not None:
            original_case = packet_cases[case["code"]]
            chosen = next(c for c in original_case["candidates"] if c["code"] == selected)
            real_survivors = [c["code"] for c in original_case["candidates"]
                              if all(compare(c["facts"].get(p["field"]), p) != "contradiction" for p in original_case["predicates"])]
            valid_unique = real_survivors == [selected] and all(compare(chosen["facts"].get(p["field"]), p) == "match" for p in original_case["predicates"])
        truth = case["truth"]
        documentary_scorable = truth["validation"] == "published_record_checked" and truth["target_id"] is not None
        recovered = valid_unique and selected_id == truth["target_id"] if documentary_scorable else None
        safety_pass = (response["decision"] == case["expected"]["decision"] and
                       actual_survivors == sorted(case["expected"]["survivor_ids"]))
        forecast_results = []
        for reference in case.get("forecast_references", []):
            relevant = [f for f in response["forecasts"] if f["field"] == reference["field"] and
                        mapping.get(f["candidate_code"]) == truth["target_id"]]
            forecast_results.append({"field": reference["field"], "reference": reference["value"],
                                     "agreement": len(relevant) == 1 and relevant[0]["value"] == reference["value"],
                                     "evidence_class": "same_report_exposed_expectation", "independent_confirmation": False})
        results.append({"case_code": case["code"], "case_kind": case["kind"], "decision": response["decision"],
                        "selected_model_id": selected_id, "surviving_model_ids": actual_survivors,
                        "documentary_identity_recovery": recovered,
                        "decision_and_survivor_check": safety_pass,
                        "field_accuracy_scorable": False, "truth_limit": truth["limit"],
                        "forecast_agreement": forecast_results})
    scored = [r for r in results if r["documentary_identity_recovery"] is not None]
    return {"schema": SCHEMA, "reviewer_input_sha256": digest(packet), "results": results,
            "summary": {"documentary_identity_cases": len(scored),
                        "documentary_identities_recovered": sum(r["documentary_identity_recovery"] for r in scored),
                        "decision_survivor_checks": len(results),
                        "decision_survivor_checks_passed": sum(r["decision_and_survivor_check"] for r in results),
                        "unscorable_ancient_truth_cases": sum(r["case_kind"] == "unscorable_ancient_truth" for r in results),
                        "independent_field_accuracy": None, "unseen_archaeological_confirmation": None},
            "limits": "Convenience tasks authored after source inspection; target descriptors and model facts derive from the same reports. Recovery checks documentary consistency. Null and ambiguity cases audit stopping behavior. Ancient phase, observed entrance and field accuracy require independent truth."}


def audit_reserved(manifest):
    """Fail closed until a future batch documents freeze, roles and independent truth.

    These metadata gates never authenticate a source by themselves; a curator must
    verify each evidence locator and record the validation. Empty placeholders fail.
    """
    issues = []
    if manifest.get("schema") != "copper-scroll-reserved-recovery-batch-v1":
        issues.append("unknown_manifest_schema")
    coordinator = manifest.get("coordinator_id")
    reviewers = manifest.get("reviewer_ids", [])
    if not coordinator or not reviewers or coordinator in reviewers or len(set(reviewers)) != len(reviewers):
        issues.append("separate_coordinator_and_reviewers_required")
    freeze = manifest.get("freeze_commit", "") or ""
    if len(freeze) != 40 or any(c not in "0123456789abcdef" for c in freeze):
        issues.append("real_freeze_commit_required")
    if manifest.get("frozen_before_truth_access") is not True:
        issues.append("freeze_before_truth_access_unverified")
    cases = manifest.get("cases", [])
    if not cases:
        issues.append("reserved_cases_missing")
    for case in cases:
        code = case.get("case_code", "missing_code")
        if case.get("reviewer_exposed_to_truth") is not False:
            issues.append(code + ":reviewer_exposure_not_cleared")
        if case.get("prediction_sha256") is None or len(case.get("prediction_sha256", "")) != 64:
            issues.append(code + ":frozen_prediction_missing")
        truth = case.get("truth", {})
        if truth.get("validation") != "independent_reference_verified" or not truth.get("verified_by"):
            issues.append(code + ":independent_truth_unverified")
        if not truth.get("source_locator") or not truth.get("original_observation_id"):
            issues.append(code + ":truth_source_locator_missing")
        used = set(case.get("selection_observation_ids", []))
        reserved = truth.get("original_observation_id")
        if not used or reserved in used:
            issues.append(code + ":selection_and_truth_observation_independence_unverified")
        if truth.get("lineage_checked") is not True:
            issues.append(code + ":derivative_source_exposure_unchecked")
        if not case.get("surviving_models_registered") or not case.get("failure_rule"):
            issues.append(code + ":decision_rule_or_models_missing")
    return {"eligible_for_reserved_scoring": not issues, "issues": issues,
            "scope": "Metadata readiness only; source truth and freeze chronology need curator verification."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--dataset", type=Path, default=HERE / "source_grounded_cases.json")
    p.add_argument("--output", type=Path, default=HERE / "packets")
    p = sub.add_parser("predict")
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("grade")
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--predictions", type=Path, required=True)
    p.add_argument("--key", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("run")
    p.add_argument("--dataset", type=Path, default=HERE / "source_grounded_cases.json")
    p.add_argument("--output", type=Path, default=HERE / "outputs")
    p = sub.add_parser("audit-reserved")
    p.add_argument("--manifest", type=Path, default=HERE / "reserved_batch_template.json")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(read(args.dataset), args.output)
    elif args.command == "predict":
        write(args.output, predict(read(args.packet)))
    elif args.command == "grade":
        write(args.output, grade(read(args.packet), read(args.predictions), read(args.key),
                                 read(args.key.parent / "freeze_manifest.json")))
    elif args.command == "audit-reserved":
        result = audit_reserved(read(args.manifest))
        print(json.dumps(result, indent=2))
        if not result["eligible_for_reserved_scoring"]:
            raise SystemExit(2)
    else:
        packet, key = prepare(read(args.dataset), args.output / "packets")
        predictions = predict(packet)
        write(args.output / "predictions.json", predictions)
        results = grade(packet, predictions, key, read(args.output / "packets" / "coordinator" / "freeze_manifest.json"))
        write(args.output / "results.json", results)
        print(json.dumps(results["summary"], indent=2))


if __name__ == "__main__":
    main()
