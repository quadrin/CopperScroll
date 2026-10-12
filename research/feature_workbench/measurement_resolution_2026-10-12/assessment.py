#!/usr/bin/env python3
"""Bounded, exploratory resolution audit. No confidence estimates or new pixels.

Run from any directory: python3 -I .../assessment.py [--check]
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def finite_nonnegative(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError("Expected a finite nonnegative number")
    return float(value)


def length_interval(pixel_distance, scale_pixels, scale_metres, endpoint_radius_px, scale_endpoint_radius_px):
    """Triangle-inequality outer bound; every endpoint has a radial disk.

    Includes ratio uncertainty in both chord and independent scale bar.
    Excludes drafting, datum definition, phase and physical survey error.
    """
    d, p, s, r, e = map(finite_nonnegative, (pixel_distance, scale_pixels, scale_metres, endpoint_radius_px, scale_endpoint_radius_px))
    if p <= 2 * e or not s:
        raise ValueError("Scale interval must be strictly positive")
    return [max(0.0, d - 2 * r) * s / (p + 2 * e), (d + 2 * r) * s / (p - 2 * e)]


def overlap(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    return [lo, hi] if lo <= hi else None


def equal_error_ceiling(a, b):
    """Two exact predictions separate only for each ±error < half their gap."""
    return abs(a - b) / 2


def bounded_same_plan_length(nominal_m, pick_radius_m, scale_fraction, distortion_pair_bound_m, datum_pair_bound_m):
    """Complete bound only when every necessary component is supplied.

    Uniform scale range is [1-f,1+f]. Two radial endpoint disks alter
    source distance by at most 2r. Independent unknowns add by worst case,
    without a probability or covariance assumption. Translation and a common
    rigid rotation cancel for distance; neither cancels all vector geometry.
    """
    if any(x is None for x in (pick_radius_m, scale_fraction, distortion_pair_bound_m, datum_pair_bound_m)):
        return None
    length, pick, scale, distortion, datum = map(finite_nonnegative, (nominal_m, pick_radius_m, scale_fraction, distortion_pair_bound_m, datum_pair_bound_m))
    if scale >= 1:
        raise ValueError("Fractional scale range must remain positive")
    return [max(0.0, (length - 2 * pick) * (1 - scale) - distortion - datum), (length + 2 * pick) * (1 + scale) + distortion + datum]


def apply_similarity(point, scale, rotation_deg, translation):
    a = math.radians(rotation_deg)
    c, s = math.cos(a), math.sin(a)
    return [scale * (c * point[0] - s * point[1]) + translation[0], scale * (s * point[0] + c * point[1]) + translation[1]]


def exposure_audit(template):
    missing = []
    for key in ("coordinator_id", "reviewer_ids", "freeze_commit", "frozen_before_truth_access", "cases"):
        if not template.get(key):
            missing.append(key)
    return {"unused_eligible_case_verified": False, "ready": not missing, "missing": missing,
            "decision": "not identifiable from available evidence: independent field accuracy"}


def calculate(j):
    cubit_lo, cubit_hi = j["cubit_scenarios"]["continuum_m"]
    pilot = []
    for case, reference, saved in zip(j["pilot_measurements"]["cases"], j["pilot_references"]["cases"], j["pilot"]["cases"]):
        scale = case["scale"]
        scale_px = math.dist(*scale["endpoints_px"])
        predictions = []
        for target in case["targets"]:
            if target["endpoints_px"] is None:
                continue
            d = math.dist(*target["endpoints_px"])
            predictions.append({"id": target["id"], "metres": d * scale["metres"] / scale_px,
                                "picking_only_interval_m": length_interval(d, scale_px, scale["metres"], 2, 2)})
        predictions.sort(key=lambda x: x["metres"], reverse=True)
        status = "unmeasurable" if len(predictions) != 2 else "measured_documentary_discrepancy"
        row = {"id": case["id"], "status": status, "chords": predictions,
               "field_accuracy": None, "source_total_error_m": None}
        if status != "unmeasurable":
            primary = predictions[0]["metres"]
            ref = max(reference["dimensions_metres"])
            row["primary_error_percent"] = 100 * abs(primary - ref) / ref
            row["same_as_saved_primary"] = math.isclose(primary, saved["primary"]["predicted_metres"], abs_tol=1e-12)
        pilot.append(row)

    depth = []
    for entry in j["depth_entries"]:
        n = entry["cubits"]
        alternatives = [{"cubit_m": c, "distance_m": n * c} for c in j["cubit_scenarios"]["illustrative_fixed_choices_m"]]
        pairwise = [{"cubits_m": [a["cubit_m"], b["cubit_m"]], "prediction_gap_m": abs(a["distance_m"] - b["distance_m"]),
                     "equal_error_must_be_strictly_less_than_m": equal_error_ceiling(a["distance_m"], b["distance_m"])}
                    for i, a in enumerate(alternatives) for b in alternatives[i + 1:]]
        depth.append({"entry": entry["entry"], "conditional_depth_band_m": [n * cubit_lo, n * cubit_hi],
                      "discrete_alternatives": alternatives, "pairwise_resolution_requirements": pairwise,
                      "one_centimetre_cubit_step_error_ceiling_m": n * .01 / 2,
                      "datum_m": entry["datum_m"], "phase": entry["phase"],
                      "total_target_interval_m": None, "can_discriminate_archaeologically": False,
                      "reason": "Ancient datum/axis/phase and complete metric error remain unavailable"})

    ac = j["ac94"]
    upper = max(b["shortest_distance_outer_envelope_m"][1] for r in ac["rows"] if r["target_set"] == "drawn_terminus_only" for b in r["branches"] if b["envelope"] == "stress")
    bands = [[n * cubit_lo, n * cubit_hi] for n in ac["numerals"]]
    discrepancy = abs(ac["dimension_diagnostic"]["east_inner_trace_m"] - ac["dimension_diagnostic"]["reported_pool_dimensions_m"][0])
    scenarios = {"zero_additional_error": 0.0,
                 "ac94_inner_trace_report_relative_discrepancy": discrepancy / ac["dimension_diagnostic"]["reported_pool_dimensions_m"][0],
                 "Dagesh_primary_documentary_mismatch": pilot[0]["primary_error_percent"] / 100,
                 "Migdal_primary_documentary_mismatch": pilot[1]["primary_error_percent"] / 100}
    acresult = {"stress_envelope_terminus_upper_m": upper, "numeral_bands_m": bands,
                "bands_overlap_m": overlap(*bands), "numeral_discrimination_with_free_unit": "impossible over the overlapping bands even with zero measurement error",
                "additional_source_budget_needed_to_preserve_plan_miss": [{"numeral": n, "additive_must_be_less_than_m": band[0] - upper,
                "multiplicative_must_be_less_than_fraction": band[0] / upper - 1} for n, band in zip(ac["numerals"], bands)],
                "illustrative_stress_only": [{"scenario": name, "fraction": frac, "upper_m": upper * (1 + frac),
                "still_below_band_minimum": [upper * (1 + frac) < band[0] for band in bands]} for name, frac in scenarios.items()],
                "stress_limit": "Documentary mismatch magnitudes are sensitivity scenarios, never calibrated transferred errors or scale corrections",
                "archaeological_decision": "not identifiable from available evidence", "total_archaeological_error_m": None}

    hy = j["hyrcania"]
    narrow = j["cubit_scenarios"]["narrower_exposed_m"]
    hyresult = {"centre_pick_only_m": hy["pool_centre_pick_px"] * hy["scale_m"] / hy["scale_px"],
                "failed_geographic_check_m": hy["geographic_withheld_check_error_m"],
                "shortest_side_m": min(hy["north_pool_sides_m"]),
                "24_cubit_narrow_band_m": [24 * c for c in narrow], "24_cubit_broad_band_m": bands[0],
                "narrow_gap_m": min(hy["north_pool_sides_m"]) - 24 * narrow[1],
                "broad_gap_m": min(hy["north_pool_sides_m"]) - bands[0][1],
                "field_exclusion": False, "reason": "Side datum and survey error unquantified; offset origins undefined; failed geography retained"}
    rg = j["registration"]
    e = math.hypot(rg["anchor_error_proxy_m"], rg["example_feature_error_proxy_m"])
    angle = math.degrees(math.atan2(2 * e, rg["example_distance_m"]))
    return {"schema": 1, "scope": "derived exploratory resolution analysis; no frozen archaeological verdicts changed",
            "pilot_reproduction": pilot, "depth_resolution": depth, "ac94": acresult,
            "iv17": {"observed_proxy_interval_deg": j["iv17"]["proxy_bearing_picking_interval_deg"],
                      "distance_from_central_proxy_to_primary_sector_edge_deg": 135 - j["iv17"]["northern_bearing_deg"],
                      "ancient_aspect_decision": "unknown", "ancient_depth_decision": "unknown",
                      "reason": "Proxy envelope crosses sector edge; north convention and ancient jambs/threshold unresolved; no exposed-plan scoring under frozen rule"},
            "hyrcania": hyresult,
            "siloam": {"entry": 49, "metric_offset_test_permitted": False, "depth_budget_m": None,
                       "reason": "No cubit/depth instruction; main-side underside/floor contact unresolved"},
            "registration": {"north_sector_example_required_margin_deg": angle,
                             "near_due_north_remaining_half_width_deg": 45 - angle,
                             "existing_map_error_m": rg["map_withheld_check_error_m"],
                             "mouth_max_project_proxy_m": rg["mouth_max_registration_proxy_m"],
                             "existing_map_can_test_mouth_relation": False,
                             "same_document_error_requires_differential_model": True,
                             "probabilistic_field_accuracy_estimated": False},
            "benchmark_readiness": exposure_audit(j["benchmark_audit"]["template"])}


def main():
    result = calculate(json.loads((HERE / "inputs.json").read_text()))
    result["inputs_sha256"] = hashlib.sha256((HERE / "inputs.json").read_bytes()).hexdigest()
    expected = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    path = HERE / "results.json"
    if "--check" in sys.argv:
        if not path.exists() or path.read_text() != expected:
            raise SystemExit("Saved resolution results differ from pinned inputs")
        print("Resolution results reproduce exactly")
    else:
        path.write_text(expected)
        print(path)


if __name__ == "__main__":
    main()
