"""Synthetic contract failures and real source-lineage regressions."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("coverage_notice_audit", Path(__file__).with_name("audit.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def synthetic_absence():
    values = {
        "target_identity_and_boundary": {"target_id": "synthetic-T", "reference_frame": "synthetic-frame", "boundary": [0, 1, 0, 1], "boundary_verified": True},
        "instrument_covers_feature_taxon": {"instrument_id": "synthetic-I", "covered_feature_types": ["pit", "cistern"], "covers_predicate_types": True},
        "actual_search_reach": {"target_id": "synthetic-T", "instrument_id": "synthetic-I", "reference_frame": "synthetic-frame", "searched_geometry": [0, 1, 0, 1], "covers_entire_target": True},
        "phase_eligibility": {"target_phase": "synthetic-phase", "searched_feature_phase": "synthetic-phase", "phase_identifiers_explicit": True, "phase_relation_verified": True},
        "preservation_and_visibility": {"preservation_assessed": True, "negative_interpretable": True},
        "detection_limits": {"instrument_id": "synthetic-I", "method": "synthetic-method", "limits": {"synthetic": True}, "adequate_for_predicted_feature": True},
    }
    return {"target_id": "synthetic-T", "predicate_feature_types": ["pit", "cistern"],
            "gate_evidence": {key: {"value": value, "source_refs": ["synthetic-fixture-only"]} for key, value in values.items()},
            "negative_observation": {"reported_absent": True, "target_id": "synthetic-T", "instrument_id": "synthetic-I", "source_refs": ["synthetic-fixture-only"]}}


def synthetic_registration():
    controls = [{"feature_id": f"synthetic-{i}", "observation_id": f"synthetic-obs-{i}", "identity_verified": True,
                 "geographic_position_verified": True, "source_refs": ["synthetic-fixture-only"],
                 "source_point": point, "destination_point": [point[0] + 10, point[1] + 20],
                 "source_frame_id": "synthetic-native", "destination_frame_id": "synthetic-destination",
                 "source_units": "px", "destination_units": "m"}
                for i, point in enumerate([[0, 0], [10, 0], [0, 10]])]
    return {"id": "synthetic-registration", "model": "affine", "native_frame_verified": True,
            "native_frame_id": "synthetic-native", "destination_frame_id": "synthetic-destination",
            "native_units": "px", "destination_units": "m",
            "geographic_crs": "synthetic-frame-only", "controls": controls, "distribution_verified": True,
            "frozen_transform": {"matrix": [[1, 0, 10], [0, 1, 20]], "frozen_before_holdout": True, "source_refs": ["synthetic-fixture-only"]},
            "acceptance_bound_m": 2.0, "error_budget": {"all_material_errors_bounded": True, "total_bound_m": 1.5, "source_refs": ["synthetic-fixture-only"]},
            "holdout": {"observation_id": "synthetic-independent-check", "reserved_before_inspection": True,
                "prior_exposure": "demonstrably_unused_at_freeze", "copy_of_exposed_observation": False,
                "identity_verified": True, "geographic_position_verified": True, "source_refs": ["synthetic-fixture-only"],
                "source_point": [3, 3], "destination_point": [13, 23], "source_frame_id": "synthetic-native",
                "destination_frame_id": "synthetic-destination", "source_units": "px", "destination_units": "m"},
            "historical_phase": {"state_id": "synthetic-phase", "same_landscape_state_verified": True, "source_refs": ["synthetic-fixture-only"]},
            "source_refs": ["synthetic-fixture-only"], "reason": "synthetic fixture", "next_required_observation": "synthetic fixture"}


class AbsenceContractTests(unittest.TestCase):
    def test_complete_synthetic_contract_passes_without_probability(self):
        result = audit.assess_landmark_absence(synthetic_absence())
        self.assertTrue(result["archaeological_landmark_exclusion_allowed"])
        self.assertIsNone(result["negative_likelihood"])

    def test_report_silence_or_standard_field_has_no_search_gates(self):
        result = audit.assess_landmark_absence({"target_id": "T", "negative_observation": {"reported_absent": True, "source_refs": ["synthetic"]}})
        self.assertFalse(result["archaeological_landmark_exclusion_allowed"])
        self.assertTrue(all(item["status"] == "unknown" for item in result["gates"]))

    def test_every_missing_gate_blocks_exclusion(self):
        for gate in synthetic_absence()["gate_evidence"]:
            with self.subTest(gate=gate):
                record = synthetic_absence()
                del record["gate_evidence"][gate]
                self.assertFalse(audit.assess_landmark_absence(record)["archaeological_landmark_exclusion_allowed"])

    def test_missing_provenance_blocks_every_gate(self):
        for gate in synthetic_absence()["gate_evidence"]:
            with self.subTest(gate=gate):
                record = synthetic_absence()
                record["gate_evidence"][gate]["source_refs"] = []
                self.assertFalse(audit.assess_landmark_absence(record)["archaeological_landmark_exclusion_allowed"])

    def test_unrelated_target_instrument_or_frame_does_not_join(self):
        for field in ("target_id", "instrument_id", "reference_frame"):
            with self.subTest(field=field):
                record = synthetic_absence()
                record["gate_evidence"]["actual_search_reach"]["value"][field] = "different-synthetic"
                self.assertFalse(audit.assess_landmark_absence(record)["archaeological_landmark_exclusion_allowed"])

    def test_cistern_only_instrument_cannot_exclude_all_pits(self):
        record = synthetic_absence()
        record["gate_evidence"]["instrument_covers_feature_taxon"]["value"]["covered_feature_types"] = ["cistern"]
        self.assertFalse(audit.assess_landmark_absence(record)["archaeological_landmark_exclusion_allowed"])

    def test_broad_period_or_unmatched_phases_are_unknown(self):
        for field, value in (("phase_identifiers_explicit", False), ("searched_feature_phase", "different-synthetic-phase")):
            with self.subTest(field=field):
                record = synthetic_absence()
                record["gate_evidence"]["phase_eligibility"]["value"][field] = value
                self.assertFalse(audit.assess_landmark_absence(record)["archaeological_landmark_exclusion_allowed"])

    def test_partial_reach_or_disturbance_failure_cannot_pass(self):
        for gate, field in (("actual_search_reach", "covers_entire_target"), ("preservation_and_visibility", "negative_interpretable")):
            with self.subTest(gate=gate):
                record = synthetic_absence()
                record["gate_evidence"][gate]["value"][field] = False
                result = audit.assess_landmark_absence(record)
                self.assertFalse(result["archaeological_landmark_exclusion_allowed"])
                self.assertIn("contradicted", [item["status"] for item in result["gates"]])

    def test_missing_actual_negative_observation_blocks_claim(self):
        record = synthetic_absence()
        record.pop("negative_observation")
        self.assertFalse(audit.assess_landmark_absence(record)["archaeological_landmark_exclusion_allowed"])


class RegistrationContractTests(unittest.TestCase):
    def test_complete_synthetic_contract_passes(self):
        result = audit.assess_registration(synthetic_registration())
        self.assertTrue(result["geographic_registration_eligible"])
        self.assertTrue(result["historical_landscape_reconstruction_eligible"])

    def test_exposed_check_copy_and_postselection_leave_one_out_fail(self):
        for changes in ({"prior_exposure": "already_inspected"}, {"copy_of_exposed_observation": True}, {"reserved_before_inspection": False}, {"observation_id": "synthetic-obs-0"}):
            with self.subTest(changes=changes):
                record = synthetic_registration()
                record["holdout"].update(changes)
                self.assertFalse(audit.assess_registration(record)["geographic_registration_eligible"])

    def test_duplicate_controls_and_too_few_affine_points_fail(self):
        for duplicate in (True, False):
            record = synthetic_registration()
            if duplicate:
                record["controls"][2] = deepcopy(record["controls"][1])
            else:
                record["controls"].pop()
            self.assertFalse(audit.assess_registration(record)["geographic_registration_eligible"])

    def test_low_fit_error_cannot_replace_named_geographic_identity(self):
        record = synthetic_registration()
        record["controls"][0]["identity_verified"] = False
        self.assertFalse(audit.assess_registration(record)["geographic_registration_eligible"])

    def test_unbounded_error_or_invalid_holdout_points_fail(self):
        for coordinate in (float("nan"), float("inf"), True, 200):
            with self.subTest(coordinate=coordinate):
                record = synthetic_registration()
                record["holdout"]["destination_point"][0] = coordinate
                self.assertFalse(audit.assess_registration(record)["geographic_registration_eligible"])
        record = synthetic_registration()
        record["error_budget"]["all_material_errors_bounded"] = False
        self.assertFalse(audit.assess_registration(record)["geographic_registration_eligible"])

    def test_truthy_metadata_without_numeric_coordinates_does_not_pass(self):
        record = synthetic_registration()
        for control in record["controls"]:
            control.pop("source_point")
            control.pop("destination_point")
        result = audit.assess_registration(record)
        self.assertFalse(result["checks"]["finite_model_controls"])
        self.assertFalse(result["geographic_registration_eligible"])

    def test_collinear_boolean_or_mismatched_control_frames_fail(self):
        for mode in ("collinear", "boolean", "wrong-frame", "wrong-units"):
            with self.subTest(mode=mode):
                record = synthetic_registration()
                if mode == "collinear":
                    record["controls"][2]["source_point"] = [20, 0]
                    record["controls"][2]["destination_point"] = [30, 20]
                elif mode == "boolean":
                    record["controls"][0]["source_point"] = [False, True]
                elif mode == "wrong-frame":
                    record["controls"][0]["destination_frame_id"] = "different-frame"
                else:
                    record["controls"][0]["destination_units"] = "degrees"
                self.assertFalse(audit.assess_registration(record)["geographic_registration_eligible"])

    def test_asserted_residual_cannot_override_computed_point_error(self):
        record = synthetic_registration()
        record["holdout"]["destination_point"] = [100, 100]
        record["holdout"]["residual_m"] = 0
        result = audit.assess_registration(record)
        self.assertFalse(result["geographic_registration_eligible"])
        self.assertGreater(result["computed_holdout_residual_m"], 2)

    def test_transform_must_be_frozen_finite_and_nondegenerate(self):
        for mode in ("not-frozen", "singular", "nonfinite"):
            with self.subTest(mode=mode):
                record = synthetic_registration()
                if mode == "not-frozen":
                    record["frozen_transform"]["frozen_before_holdout"] = False
                elif mode == "singular":
                    record["frozen_transform"]["matrix"] = [[0, 0, 0], [0, 0, 0]]
                else:
                    record["frozen_transform"]["matrix"][0][0] = float("nan")
                self.assertFalse(audit.assess_registration(record)["geographic_registration_eligible"])

    def test_existing_rejection_is_not_reopened_by_old_metrics(self):
        record = synthetic_registration()
        record["existing_rejection"] = True
        self.assertFalse(audit.assess_registration(record)["geographic_registration_eligible"])

    def test_ancient_landscape_requires_a_separate_phase_join(self):
        record = synthetic_registration()
        record.pop("historical_phase")
        result = audit.assess_registration(record)
        self.assertTrue(result["geographic_registration_eligible"])
        self.assertFalse(result["historical_landscape_reconstruction_eligible"])


class ActualEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result, cls.manifest = audit.build()

    def test_all_standard_fields_and_frozen_failure_units_retained(self):
        data = self.result["source_instrument_audit"]
        self.assertEqual(data["summary"]["standard_field_units"], 50)
        self.assertEqual(data["summary"]["main_C2_failure_units"], 19)
        self.assertEqual(data["summary"]["pre70_C2_failure_units"], 30)
        self.assertFalse(data["frozen_results_modified"])
        self.assertTrue(all(not item["archaeological_landmark_exclusion_allowed"] for item in data["witnesses"]))

    def test_unvisited_and_conflicted_entries_are_not_hidden(self):
        by_id = {item["unit_id"]: item for item in self.result["source_instrument_audit"]["witnesses"]}
        self.assertIn("site_not_visited", by_id["S845"]["flags"])
        self.assertEqual(by_id["S845"]["frozen_C2"], "MATCH")
        for unit in ("S1173", "S503", "S1116"):
            self.assertIn("field_and_narrative_conflict", by_id[unit]["flags"])
        for unit in ("S241", "S1080"):
            self.assertIn("source_entry_crosswalk_or_grid_issue", by_id[unit]["flags"])

    def test_documentary_and_physical_counts_do_not_become_search_denominator(self):
        self.assertEqual(len(self.result["documentary_notices"]), 28)
        self.assertEqual(len(self.result["excavation_targets"]), 29)
        self.assertEqual(len(self.result["physical_coverage_observations"]), 6)
        self.assertIsNone(self.result["regional_denominator"])
        self.assertTrue(all(not item["negative_claim_allowed"] for item in self.result["excavation_targets"]))

    def test_old_checks_remain_exposed_and_registration_denied(self):
        by_id = {item["id"]: item for item in self.result["registration_cases"]}
        self.assertEqual(len(by_id), 5)
        self.assertAlmostEqual(by_id["hyrcania-regional-fig1"]["exposed_diagnostics"]["old_check_residual_m"], 244.37106137762902)
        self.assertFalse(by_id["qumran-aerial-fig35"]["exposed_diagnostics"]["leave_one_out_is_independent_holdout"])
        self.assertTrue(all(not item["geographic_registration_eligible"] and not item["fresh_holdout_available"] for item in by_id.values()))

    def test_deterministic_outputs_and_input_hashes(self):
        other, manifest = audit.build()
        self.assertEqual(other, self.result)
        self.assertEqual(manifest, self.manifest)
        with tempfile.TemporaryDirectory() as directory:
            audit.write(other, manifest, Path(directory))
            self.assertEqual(json.loads((Path(directory) / "results.json").read_text()), other)
        self.assertEqual(len({item["path"] for item in manifest}), len(manifest))
        self.assertTrue(all(len(item["sha256"]) == 64 for item in manifest))


if __name__ == "__main__":
    unittest.main()
