"""Audit exposed negative notices and geographic-registration eligibility.

No probabilities, geometry, feature observations or reader answers are imputed.
The frozen Koḥlit classifications are imported as documentary results only.
"""
from __future__ import annotations

import argparse
import csv
from copy import deepcopy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
S2 = "research/rarity/kohlit/stage2/addendum_s2"
STANDARD_FIELD = "Cisterns: none"


class Inputs:
    def __init__(self, root: Path):
        self.root = root
        self.paths: set[str] = set()

    def text(self, path: str) -> str:
        self.paths.add(path)
        return (self.root / path).read_text(encoding="utf-8")

    def json(self, path: str):
        return json.loads(self.text(path))

    def csv(self, path: str):
        return list(csv.DictReader(self.text(path).splitlines()))

    def manifest(self):
        return [{"path": path, "sha256": hashlib.sha256((self.root / path).read_bytes()).hexdigest()}
                for path in sorted(self.paths)]


def finite(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def point2(value) -> bool:
    return isinstance(value, list) and len(value) == 2 and all(finite(axis) for axis in value)


def valid_pair(pair: dict, record: dict) -> bool:
    return (point2(pair.get("source_point")) and point2(pair.get("destination_point"))
            and pair.get("source_frame_id") == record.get("native_frame_id")
            and bool(pair.get("source_frame_id"))
            and pair.get("destination_frame_id") == record.get("destination_frame_id")
            and bool(pair.get("destination_frame_id"))
            and pair.get("source_units") == record.get("native_units")
            and pair.get("source_units") in ("px", "m")
            and pair.get("destination_units") == record.get("destination_units") == "m")


def nondegenerate(points: list, model: str) -> bool:
    if model == "similarity":
        return any(math.dist(a, b) > 0 for i, a in enumerate(points) for b in points[i + 1:])
    if model == "affine":
        return any(abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) > 1e-12
                   for i, a in enumerate(points) for j, b in enumerate(points[i + 1:], i + 1) for c in points[j + 1:])
    return False


def transform_matrix(value, model: str) -> bool:
    if not (isinstance(value, list) and len(value) == 2
            and all(isinstance(row, list) and len(row) == 3 and all(finite(item) for item in row) for row in value)):
        return False
    a, b, _ = value[0]
    c, d, _ = value[1]
    if abs(a * d - b * c) <= 1e-12:
        return False
    if model == "similarity":
        return math.isclose(a * a + c * c, b * b + d * d, rel_tol=1e-10) and math.isclose(a * b + c * d, 0.0, abs_tol=1e-10)
    return model == "affine"


def residual_m(matrix: list, pair: dict) -> float:
    x, y = pair["source_point"]
    transformed = [row[0] * x + row[1] * y + row[2] for row in matrix]
    return math.dist(transformed, pair["destination_point"])


def assess_landmark_absence(record: dict) -> dict:
    """A negative field is not a negative search of a specified feature sector.

    This concerns a landmark search, not the separate deposit-target contract.
    Complete evidence would have to name the target predicate and instrument.
    """
    gates = {
        "target_identity_and_boundary": ("target_id", "reference_frame", "boundary", "boundary_verified"),
        "instrument_covers_feature_taxon": ("instrument_id", "covered_feature_types", "covers_predicate_types"),
        "actual_search_reach": ("target_id", "instrument_id", "reference_frame", "searched_geometry", "covers_entire_target"),
        "phase_eligibility": ("target_phase", "searched_feature_phase", "phase_identifiers_explicit", "phase_relation_verified"),
        "preservation_and_visibility": ("preservation_assessed", "negative_interpretable"),
        "detection_limits": ("instrument_id", "method", "limits", "adequate_for_predicted_feature"),
    }
    true_fields = {
        "target_identity_and_boundary": ("boundary_verified",),
        "instrument_covers_feature_taxon": ("covers_predicate_types",),
        "actual_search_reach": ("covers_entire_target",),
        "phase_eligibility": ("phase_relation_verified",),
        "preservation_and_visibility": ("preservation_assessed", "negative_interpretable"),
        "detection_limits": ("adequate_for_predicted_feature",),
    }
    result = []
    supplied = record.get("gate_evidence", {})
    for name, fields in gates.items():
        item = supplied.get(name) or {}
        value = item.get("value")
        refs = item.get("source_refs")
        complete = (isinstance(value, dict) and all(value.get(field) is not None and value.get(field) not in ("", [], {}) for field in fields)
                    and isinstance(refs, list) and bool(refs))
        status = "unknown"
        if complete:
            statuses = [value[field] for field in true_fields[name]]
            if any(flag is False for flag in statuses):
                status = "contradicted"
            elif all(flag is True for flag in statuses):
                status = "compatible"
        result.append({"id": name, "status": status, "source_refs": refs or []})
    by_id = {gate["id"]: gate for gate in result}
    # An unrelated search or another instrument cannot establish target reach.
    boundary = supplied.get("target_identity_and_boundary", {}).get("value") or {}
    reach = supplied.get("actual_search_reach", {}).get("value") or {}
    taxon = supplied.get("instrument_covers_feature_taxon", {}).get("value") or {}
    limits = supplied.get("detection_limits", {}).get("value") or {}
    required_types = record.get("predicate_feature_types")
    if by_id["instrument_covers_feature_taxon"]["status"] == "compatible" and (
        not isinstance(required_types, list) or not required_types
        or not set(required_types).issubset(set(taxon.get("covered_feature_types") or []))
    ):
        by_id["instrument_covers_feature_taxon"]["status"] = "unknown"
    phase = supplied.get("phase_eligibility", {}).get("value") or {}
    equivalence = phase.get("phase_equivalence") or {}
    equivalent = (equivalence.get("target_phase") == phase.get("target_phase")
                  and equivalence.get("searched_feature_phase") == phase.get("searched_feature_phase")
                  and bool(equivalence.get("named_contact")) and bool(equivalence.get("source_refs")))
    if by_id["phase_eligibility"]["status"] == "compatible" and (
        phase.get("phase_identifiers_explicit") is not True
        or (phase.get("target_phase") != phase.get("searched_feature_phase") and not equivalent)
    ):
        by_id["phase_eligibility"]["status"] = "unknown"
    if by_id["actual_search_reach"]["status"] == "compatible" and (
        reach.get("target_id") != record.get("target_id") or reach.get("target_id") != boundary.get("target_id")
        or reach.get("reference_frame") != boundary.get("reference_frame")
        or reach.get("instrument_id") != taxon.get("instrument_id") or reach.get("instrument_id") != limits.get("instrument_id")
    ):
        by_id["actual_search_reach"]["status"] = "unknown"
    negative = record.get("negative_observation") or {}
    reported = (negative.get("reported_absent") is True and bool(negative.get("source_refs"))
                and negative.get("target_id") == record.get("target_id")
                and negative.get("instrument_id") == reach.get("instrument_id"))
    allowed = all(gate["status"] == "compatible" for gate in result) and reported
    return {"gates": result, "archaeological_landmark_exclusion_allowed": allowed,
            "negative_likelihood": None, "likelihood_reason": "No calibrated target-specific detection probability is supplied."}


def assess_registration(record: dict) -> dict:
    """Check a proposed geographic fit; source-local proxies are a separate scope."""
    controls = record.get("controls") or []
    model = record.get("model")
    minimum = {"similarity": 2, "affine": 3}.get(model)
    control_ids = [control.get("observation_id") for control in controls]
    named = bool(controls) and all(
        control.get("identity_verified") is True and control.get("geographic_position_verified") is True
        and control.get("source_refs") and control.get("feature_id") and control.get("observation_id")
        for control in controls)
    independent_controls = named and len(set(control_ids)) == len(controls)
    finite_pairs = bool(controls) and all(valid_pair(control, record) for control in controls)
    nondegenerate_controls = finite_pairs and nondegenerate([control["source_point"] for control in controls], model) and nondegenerate([control["destination_point"] for control in controls], model)
    fit = record.get("frozen_transform") or {}
    matrix = fit.get("matrix")
    valid_transform = (transform_matrix(matrix, model) and fit.get("frozen_before_holdout") is True
                       and bool(fit.get("source_refs")))
    holdout = record.get("holdout") or {}
    limit = record.get("acceptance_bound_m")
    computed_residual = residual_m(matrix, holdout) if valid_transform and valid_pair(holdout, record) else None
    fit_residuals = [residual_m(matrix, pair) for pair in controls] if valid_transform and finite_pairs else None
    held_out = bool(holdout) and (
        holdout.get("reserved_before_inspection") is True
        and holdout.get("identity_verified") is True
        and holdout.get("geographic_position_verified") is True
        and holdout.get("prior_exposure") == "demonstrably_unused_at_freeze"
        and holdout.get("observation_id") not in control_ids
        and bool(holdout.get("observation_id")) and bool(holdout.get("source_refs"))
        and holdout.get("copy_of_exposed_observation") is False
        and finite(computed_residual) and finite(limit) and 0 <= computed_residual <= limit
    )
    uncertainty = record.get("error_budget") or {}
    complete_budget = (uncertainty.get("all_material_errors_bounded") is True
                       and finite(uncertainty.get("total_bound_m")) and uncertainty["total_bound_m"] >= 0
                       and bool(uncertainty.get("source_refs")) and finite(limit) and limit >= 0
                       and uncertainty["total_bound_m"] <= limit)
    checks = {
        "native_frame": record.get("native_frame_verified") is True,
        "geographic_reference_frame": bool(record.get("geographic_crs")),
        "named_control_identity": independent_controls,
        "finite_model_controls": minimum is not None and independent_controls and finite_pairs and nondegenerate_controls and len(controls) >= minimum,
        "control_distribution": record.get("distribution_verified") is True and nondegenerate_controls,
        "frozen_transform": valid_transform,
        "control_residuals_within_bound": bool(fit_residuals) and finite(limit) and all(finite(value) and 0 <= value <= limit for value in fit_residuals),
        "independent_validation": held_out,
        "bounded_error_budget": complete_budget,
    }
    eligible = all(checks.values()) and bool(record.get("source_refs")) and record.get("existing_rejection") is not True
    phase = record.get("historical_phase") or {}
    phase_known = (phase.get("same_landscape_state_verified") is True and bool(phase.get("state_id"))
                   and bool(phase.get("source_refs")))
    return {"id": record["id"], "checks": checks,
            "geographic_registration_eligible": eligible,
            "historical_landscape_reconstruction_eligible": eligible and phase_known,
            "missing_checks": [name for name, passed in checks.items() if not passed],
            "historical_phase_verified": phase_known,
            "source_local_proxies_available": record.get("source_local_proxies_available") is True,
            "existing_rejection_preserved": record.get("existing_rejection") is True,
            "fresh_holdout_available": held_out,
            "computed_holdout_residual_m": computed_residual,
            "computed_control_residuals_m": fit_residuals,
            "reason": record["reason"], "source_refs": record["source_refs"],
            "exposed_diagnostics": deepcopy(record.get("exposed_diagnostics")),
            "next_required_observation": record["next_required_observation"]}


def source_instrument_audit(inputs: Inputs) -> dict:
    rows = inputs.csv(f"{S2}/results/unit_results.csv")
    primary = [row for row in rows if row["variant"] == "primary" and row["nigro"] == "with"]
    if len({row["unit_id"] for row in primary}) != len(primary):
        raise ValueError("Duplicate primary unit result")
    frozen = {row["unit_id"]: row for row in primary}
    metadata = {row["unit_id"]: row for row in inputs.csv(f"{S2}/source2_zertal_units.csv")}
    coding: dict[str, list] = {}
    for coder in ("A", "B"):
        for path in sorted((inputs.root / S2 / "coded_s2" / coder).glob("*.json")):
            relative = path.relative_to(inputs.root).as_posix()
            sheet = inputs.json(relative)
            if sheet["coder"] != coder:
                raise ValueError("Coder directory and sheet disagree")
            for index, absence in enumerate(sheet.get("explicit_absence", [])):
                coding.setdefault(sheet["unit_id"], []).append((coder, relative, index, absence, sheet))
    records = []
    for unit_id, coded in sorted(coding.items()):
        row, meta = frozen[unit_id], metadata[unit_id]
        instrument = "standard_cistern_field" if all(item[3].get("quote") == STANDARD_FIELD for item in coded) else "other_explicit_absence"
        if instrument != "standard_cistern_field":
            raise ValueError("Unreviewed source-2 absence instrument; classify it before rebuilding")
        site = re.search(r"Site\s+(\d+)", meta["citation"])
        if site is None:
            raise ValueError("No exact survey entry identifier")
        refs = [{"path": path, "pointer": f"/explicit_absence/{index}", "coder": coder,
                 "citation": absence["cite"]} for coder, path, index, absence, _ in coded]
        notes = " ".join(sheet.get("notes", "") for _, _, _, _, sheet in coded)
        flags = []
        if re.search(r"not visited|unvisited|minefield", notes, re.I):
            flags.append("site_not_visited")
        if re.search(r"conflict|contradict", notes, re.I):
            flags.append("field_and_narrative_conflict")
        if "no problem found" not in meta["check"]:
            flags.append("source_entry_crosswalk_or_grid_issue")
        target_id = f"kohlit-{unit_id}-C2-northern-sector"
        assessment = assess_landmark_absence({"target_id": target_id,
            "negative_observation": {"reported_absent": True, "source_refs": refs,
                                     "target_id": None, "instrument_id": instrument}})
        records.append({"unit_id": unit_id, "label": row["name"], "main_set": row["main_set"] == "True",
            "source_entry": {"english_volume": meta["english_volume"], "site": site.group(1),
                             "citation": meta["citation"], "pages": meta["pages"], "crosswalk_check": meta["check"]},
            "original_observation_id": f"zertal-vol-{meta['english_volume']}-site-{site.group(1)}-cistern-field",
            "coders": sorted({item[0] for item in coded}), "source_refs": refs,
            "source_instrument": instrument, "reported_absence_scope": "survey entry's site; searched northern sector not established",
            "predicate_scope": "eligible non-tomb pit/cistern within 1 km in the northern sector under the frozen origin rules",
            "frozen_C2": row["C2"], "frozen_A_survey": row["A_survey"], "frozen_coverage_class": row["coverage"],
            "flags": flags, "target_geometry": None, "searched_geometry": None,
            "detection_probability": None, **assessment})
    # The original C3 failure has the same search-footprint limitation, but is a
    # different instrument and source. Preserve it rather than merging C2/C3.
    old_path = "research/rarity/kohlit/stage2/coded/A/S676.json"
    old = inputs.json(old_path)
    old_absences = [{"path": old_path, "pointer": f"/explicit_absence/{index}", "citation": item["cite"]}
                    for index, item in enumerate(old["explicit_absence"]) if item["condition"] == "C3"]
    original_failure = {"unit_id": "S676", "condition": "C3_survey", "frozen_value": frozen["S676"]["C3s"],
        "source_instrument": "SWP_no_tombs_report", "source_refs": old_absences,
        "searched_geometry": None, "negative_likelihood": None, "archaeological_landmark_exclusion_allowed": False}
    main_failures = [item for item in records if item["main_set"] and item["frozen_C2"] == "FAIL"]
    all_failures = [item for item in records if item["frozen_C2"] == "FAIL"]
    if {row["unit_id"] for row in primary if row["C2"] == "FAIL"} != {item["unit_id"] for item in all_failures}:
        raise ValueError("A frozen C2 failure lacks a reviewed source-instrument witness")
    return {"scope": "All coded source-2 absence fields, not a replacement rarity model.",
            "standard_field_text": STANDARD_FIELD,
            "summary": {"source2_units": len(metadata), "source2_main_units": sum(frozen[unit]["main_set"] == "True" for unit in metadata),
                "standard_field_units": len(records), "standard_field_main_units": sum(item["main_set"] for item in records),
                "main_C2_failure_units": len(main_failures), "pre70_C2_failure_units": len(all_failures),
                "independent_observation_warning": "Two coder sheets of one entry are repeated interpretations of that entry, not two field observations.",
                "archaeological_exclusion_units": sum(item["archaeological_landmark_exclusion_allowed"] for item in records)},
            "witnesses": records, "original_C3_failure": original_failure,
            "frozen_results_modified": False}


def registration_audit(inputs: Inputs) -> list[dict]:
    hy_path = "registration/hyrcania_plan_registration_2026-09-30.json"
    qu_path = "registration/qumran_aerial_trial.json"
    up_path = "registration/upstream_similarity.json"
    iv_path = "research/feature_workbench/states/register.json"
    hy, qu, up, iv = (inputs.json(path) for path in (hy_path, qu_path, up_path, iv_path))
    frame = next(item for item in iv["reference_frames"] if item["id"] == "states-iv17-plan5-crop")
    cases = [
        {"id": "hyrcania-regional-fig1", "model": "similarity", "native_frame_verified": True,
         "geographic_crs": hy["transform"]["crs"], "controls": [], "distribution_verified": False,
         "existing_rejection": True, "source_local_proxies_available": True,
         "source_refs": [{"path": hy_path, "pointer": "/source_plan", "citation": "Patrich 1989 p. 243 Fig. 1"},
                         {"path": hy_path, "pointer": "/withheld_check", "citation": "Israel Guide vol. 13 pp. 176–177"}],
         "exposed_diagnostics": {"nominal_controls": hy["transform"]["control_count"],
                                 "old_check_residual_m": hy["withheld_check"]["residual_m"],
                                 "old_check_prior_exposure": "already_inspected", "old_check_identity_verified": False},
         "reason": "One manual summit anchor plus assumed map scale/north; the exposed Guide point has unverified dam identity and error bounds.",
         "next_required_observation": "Surveyed corresponding map features distributed across Fig. 1, a verified Guide-point identity/grid convention, bounded drawing/imagery errors and a different reserved check."},
        {"id": "hyrcania-detailed-fig22", "model": "affine", "native_frame_verified": True,
         "geographic_crs": None, "controls": [], "existing_rejection": True, "source_local_proxies_available": True,
         "source_refs": [{"path": hy_path, "pointer": "/detailed_plan", "citation": "Patrich 1989 p. 256 Fig. 22"}],
         "reason": "Published scale and source-image picks are available; corresponding independently located features and verified north/origin are absent.",
         "next_required_observation": "Native Fig. 22 and independently surveyed identifiable corners/contacts, scan and pick uncertainty, distributed fit controls and a separately reserved landmark."},
        {"id": "qumran-aerial-fig35", "model": "affine", "native_frame_verified": True,
         "geographic_crs": None, "controls": [], "distribution_verified": False,
         "existing_rejection": qu["status"] == "rejected_for_feature_geometry", "source_local_proxies_available": False,
         "source_refs": [{"path": qu_path, "pointer": "", "citation": "Magen–Peleg 2007 Fig. 35; existing aerial-image registration trial"}],
         "exposed_diagnostics": {"RANSAC_inliers": sum(qu["inliers"]), "training_rmse_pixels": qu["training_rmse_pixels"],
                                  "independent_check_points": qu["independent_check_points"],
                                  "leave_one_out_is_independent_holdout": False},
         "reason": "Anonymous SIFT pairs in a western strip are not named surveyed features; post-selection leave-one-out checks are exposed fit diagnostics.",
         "next_required_observation": "Named surveyed geographic anchors spanning the image, dated reference imagery with bounded absolute accuracy, and an independent reserved control."},
        {"id": "qumran-upstream-plan-transfer", "model": "similarity", "native_frame_verified": True,
         "geographic_crs": None, "controls": [], "source_local_proxies_available": True,
         "source_refs": [{"path": up_path, "pointer": "/anchor_order", "citation": "Ilan–Amit 1989 p. 283 Fig. 1; Reeder–Jol 2006 p. 229 Fig. 4"},
                         {"path": up_path, "pointer": "/baseline/validation"}],
         "exposed_diagnostics": {"fitted_plan_anchors": len(up["anchor_order"]), "junction_discrepancy_drawing_m": up["baseline"]["junction_discrepancy_drawing_m"],
                                  "perturbation_is_calibrated_error": False},
         "reason": "Source-to-source similarity uses two approximate tunnel centres; the uncertain junction is already exposed and not a surveyed validation point.",
         "next_required_observation": "Authenticated common landmark identities with bounded source-plan errors, geographic controls and a separately reserved comparison; retain the printed length break."},
        {"id": "iv17-native-plan5", "model": "affine", "native_frame_verified": True,
         "geographic_crs": frame["geographic_registration"], "controls": [], "source_local_proxies_available": True,
         "source_refs": [{"path": iv_path, "pointer": "/reference_frames/0", "citation": "Sion 2002 Plan 5 p. 63; Fig. 12 p. 61"}],
         "exposed_diagnostics": {"native_crop_px": frame["size_px"], "nominal_metres_per_pixel": frame["scale"]["metres_per_pixel"],
                                  "systematic_error_quantified": frame["scale"]["systematic_error_quantified"]},
         "reason": "Native scale/crop/north annotations permit exposed plan proxies; north convention, geographic control, ancient threshold/wall phase and systematic bounds remain unresolved.",
         "next_required_observation": "L-656 threshold section/levels and dated wall contacts tied to surveyed native controls; a new independent field observation reserved before model selection."},
    ]
    return [assess_registration(case) for case in cases]


def build(root: Path = ROOT) -> tuple[dict, list[dict]]:
    inputs = Inputs(root)
    inputs.text("research/feature_workbench/coverage/audit/audit.py")
    module_path = "research/feature_workbench/coverage/evaluate.py"
    inputs.text(module_path)
    spec = importlib.util.spec_from_file_location("existing_coverage", root / module_path)
    coverage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(coverage)
    for path in (coverage.INVENTORY_PATH, coverage.WADI_PATH, coverage.IV17_PHASE_PATH, coverage.IV17_ASSESSMENT_PATH):
        inputs.text(path)
    existing = coverage.build(root)
    data = existing["data"]
    source_audit = source_instrument_audit(inputs)
    plans = registration_audit(inputs)
    result = {"schema_version": 1, "exposure": "exploratory audit of already inspected records",
        "claim": "Available negative notices and plan records supply target-specific exclusion likelihoods or an independently validated ancient landscape registration.",
        "result": "not identifiable from available evidence",
        "source_instrument_audit": source_audit,
        "excavation_targets": [{"id": target["id"], "label": target["label"], "gates": target["gates"],
             "missing_gate_ids": target["missing_gate_ids"], "failed_gate_ids": target["failed_gate_ids"],
             "negative_claim_allowed": target["negative_claim_allowed"], "negative_observation": target["negative_observation"],
             "negative_likelihood": None} for target in data["targets"]],
        "documentary_notices": [{key: deepcopy(notice[key]) for key in ("id", "record_kind", "coverage_detail", "flags", "campaign_ids", "campaign_identity_unknown", "target_id", "source_locators", "reported_datum", "reported_detection_gates", "next_observation")}
             for notice in data["notices"]],
        "physical_coverage_observations": data["coverage_observations"],
        "regional_denominator": data["summary"]["regional_eligible_denominator"],
        "registration_cases": plans,
        "conclusions": {"negative_excavation_eligible_targets": sum(target["negative_claim_allowed"] for target in data["targets"]),
            "geographic_registration_eligible_cases": sum(case["geographic_registration_eligible"] for case in plans),
            "historical_landscape_eligible_cases": sum(case["historical_landscape_reconstruction_eligible"] for case in plans),
            "site_identification_claim_allowed": False, "detection_probabilities": None,
            "frozen_matcher_or_results_modified": False, "closed_questions_reopened": False}}
    return result, inputs.manifest()


def write(result: dict, manifest: list[dict], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "input_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["unit_id", "label", "main_set", "coders", "frozen_C2", "frozen_A_survey", "frozen_coverage_class", "source_instrument", "reported_absence_scope", "flags", "archaeological_landmark_exclusion_allowed"]
    with (output / "absence_witnesses.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for item in result["source_instrument_audit"]["witnesses"]:
            row = {field: item[field] for field in fields}
            row["coders"], row["flags"] = "+".join(row["coders"]), ";".join(row["flags"])
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    result, manifest = build(args.repo_root)
    if args.write:
        write(result, manifest, args.output_dir)
    print(json.dumps({"result": result["result"], **result["source_instrument_audit"]["summary"], **result["conclusions"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
