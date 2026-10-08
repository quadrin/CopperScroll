"""Regression checks for coverage inference, source precedence and de-duplication."""

from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("evaluate.py")
SPEC = importlib.util.spec_from_file_location("coverage_evaluate", MODULE_PATH)
assert SPEC and SPEC.loader
evaluate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluate)
ROOT = MODULE_PATH.parents[3]


def complete_synthetic_target():
    """Synthetic fixtures test policy only; they are never exported as evidence."""
    values = {
        "ancient_target_volume": {"geometry": {"type": "bounded_volume", "bounds": [[0, 0, -2], [1, 1, -1]], "unit": "m"}, "reference_frame": "synthetic-local"},
        "ancient_datum": {"datum_id": "synthetic-threshold", "datum_kind": "ancient_surface", "surface": "synthetic-contemporary-surface", "surface_id": "synthetic-threshold", "surface_phase": "synthetic-A", "ancient_surface_verified": True, "ancient_surface_source_ids": ["synthetic-surface-source"], "reference_frame": "synthetic-local"},
        "actual_reach": {"covers_entire_target": True, "reference_frame": "synthetic-local", "target_id": "synthetic-target", "datum_id": "synthetic-threshold"},
        "phase_alignment": {"target_phase": "synthetic-A", "exposed_phase": "synthetic-A", "phase_identifiers_explicit": True, "coexistence_verified": True},
        "disturbance_assessment": {"target_preservation_assessed": True, "negative_observation_interpretable": True, "unexplained_removal_used_as_rescue": False},
        "detection_method": {"method": "synthetic documented excavation", "limits": "synthetic adequate recovery limits", "adequate_for_predicted_material": True},
    }
    return {"id": "synthetic-target", "label": "Synthetic test only", "geometry": None,
            "gate_evidence": {gate_id: {"state": "established", "value": value, "source_ids": ["synthetic-source"]} for gate_id, value in values.items()},
            "negative_observation": {"target_id": "synthetic-target", "no_predicted_material": True, "source_ids": ["synthetic-source"]}}


class NegativeCoverageGateTests(unittest.TestCase):
    def test_every_gate_is_required(self):
        for missing_gate in evaluate.GATE_LABELS:
            with self.subTest(gate=missing_gate):
                target = complete_synthetic_target()
                target["gate_evidence"].pop(missing_gate)
                result = evaluate.evaluate_target(target)
                self.assertFalse(result["negative_claim_allowed"])
                self.assertIn(missing_gate, result["missing_gate_ids"])
                self.assertEqual(result["negative_deposit_status"], "unknown")

    def test_verified_complete_negative_can_pass_the_gate(self):
        result = evaluate.evaluate_target(complete_synthetic_target())
        self.assertTrue(result["negative_excavation_eligible"])
        self.assertTrue(result["negative_claim_allowed"])
        self.assertEqual(result["missing_gate_ids"], [])

    def test_full_coverage_without_negative_observation_is_not_a_negative(self):
        target = complete_synthetic_target()
        target["negative_observation"] = None
        result = evaluate.evaluate_target(target)
        self.assertTrue(result["negative_excavation_eligible"])
        self.assertFalse(result["negative_claim_allowed"])
        self.assertEqual(result["negative_deposit_status"], "unknown")

    def test_negative_observation_for_another_target_cannot_transfer(self):
        target = complete_synthetic_target()
        target["negative_observation"]["target_id"] = "another-target"
        result = evaluate.evaluate_target(target)
        self.assertTrue(result["negative_excavation_eligible"])
        self.assertFalse(result["negative_claim_allowed"])

    def test_period_heading_and_numeric_depth_cannot_supply_a_target(self):
        target = complete_synthetic_target()
        target["gate_evidence"]["ancient_datum"]["value"] = 1.3
        target["gate_evidence"]["phase_alignment"]["value"] = {"period_heading": "Persian to Herodian"}
        result = evaluate.evaluate_target(target)
        self.assertFalse(result["negative_claim_allowed"])
        self.assertIn("ancient_datum", result["missing_gate_ids"])
        self.assertIn("phase_alignment", result["missing_gate_ids"])

    def test_different_phase_id_cannot_pass_on_a_coexistence_flag(self):
        target = complete_synthetic_target()
        target["gate_evidence"]["phase_alignment"]["value"]["exposed_phase"] = "synthetic-B"
        result = evaluate.evaluate_target(target)
        self.assertFalse(result["negative_claim_allowed"])
        self.assertIn("phase_alignment", result["missing_gate_ids"])

    def test_same_period_label_or_broad_date_range_is_not_a_phase_identity(self):
        for value in (
            {"target_phase": "Hellenistic", "exposed_phase": "Hellenistic", "phase_identifiers_explicit": False, "coexistence_verified": True},
            {"target_phase": {"date_range_bce": [200, 50]}, "exposed_phase": {"date_range_bce": [200, 50]}, "phase_identifiers_explicit": True, "coexistence_verified": True},
        ):
            with self.subTest(value=value):
                target = complete_synthetic_target()
                target["gate_evidence"]["phase_alignment"]["value"] = value
                result = evaluate.evaluate_target(target)
                self.assertFalse(result["negative_claim_allowed"])
                self.assertIn("phase_alignment", result["missing_gate_ids"])

    def test_different_phase_ids_need_a_sourced_same_state_contact(self):
        target = complete_synthetic_target()
        value = target["gate_evidence"]["phase_alignment"]["value"]
        value["exposed_phase"] = "synthetic-B"
        value["phase_equivalence"] = {
            "target_phase": "synthetic-A", "exposed_phase": "synthetic-B",
            "relation": "same_archaeological_state", "named_contact": "synthetic shared wall/floor contact",
            "source_ids": ["synthetic-contact-source"],
        }
        self.assertTrue(evaluate.evaluate_target(target)["negative_claim_allowed"])
        value["phase_equivalence"]["source_ids"] = []
        self.assertFalse(evaluate.evaluate_target(target)["negative_claim_allowed"])

    def test_equivalence_for_another_phase_pair_does_not_transfer(self):
        target = complete_synthetic_target()
        value = target["gate_evidence"]["phase_alignment"]["value"]
        value["exposed_phase"] = "synthetic-B"
        value["phase_equivalence"] = {
            "target_phase": "synthetic-A", "exposed_phase": "synthetic-C",
            "relation": "same_archaeological_state", "named_contact": "synthetic contact",
            "source_ids": ["synthetic-source"],
        }
        self.assertFalse(evaluate.evaluate_target(target)["negative_claim_allowed"])

    def test_explicit_incompatible_phase_relation_fails_eligibility(self):
        target = complete_synthetic_target()
        value = target["gate_evidence"]["phase_alignment"]["value"]
        value["exposed_phase"] = "synthetic-B"
        value["phase_relation"] = "incompatible"
        result = evaluate.evaluate_target(target)
        self.assertFalse(result["negative_claim_allowed"])
        self.assertIn("phase_alignment", result["failed_gate_ids"])

    def test_modern_only_surface_cannot_supply_an_ancient_datum(self):
        target = complete_synthetic_target()
        value = target["gate_evidence"]["ancient_datum"]["value"]
        value.update({"surface": "documented present-day concrete survey pad", "surface_phase": "modern", "ancient_surface_verified": False})
        result = evaluate.evaluate_target(target)
        self.assertFalse(result["negative_claim_allowed"])
        self.assertIn("ancient_datum", result["missing_gate_ids"])

    def test_ancient_surface_requires_specific_identity_phase_and_sources(self):
        for missing_field in ("surface_id", "surface_phase", "ancient_surface_source_ids", "ancient_surface_verified"):
            with self.subTest(field=missing_field):
                target = complete_synthetic_target()
                target["gate_evidence"]["ancient_datum"]["value"].pop(missing_field)
                result = evaluate.evaluate_target(target)
                self.assertFalse(result["negative_claim_allowed"])
                self.assertIn("ancient_datum", result["missing_gate_ids"])

    def test_ancient_surface_phase_must_match_accepted_target_state(self):
        target = complete_synthetic_target()
        target["gate_evidence"]["ancient_datum"]["value"]["surface_phase"] = "synthetic-C"
        result = evaluate.evaluate_target(target)
        self.assertFalse(result["negative_claim_allowed"])
        self.assertIn("ancient_datum", result["missing_gate_ids"])

    def test_surface_in_documented_equivalent_exposed_state_can_pass(self):
        target = complete_synthetic_target()
        phase = target["gate_evidence"]["phase_alignment"]["value"]
        phase["exposed_phase"] = "synthetic-B"
        phase["phase_equivalence"] = {"target_phase": "synthetic-A", "exposed_phase": "synthetic-B", "relation": "same_archaeological_state", "named_contact": "synthetic shared wall/floor contact", "source_ids": ["synthetic-contact-source"]}
        target["gate_evidence"]["ancient_datum"]["value"]["surface_phase"] = "synthetic-B"
        self.assertTrue(evaluate.evaluate_target(target)["negative_claim_allowed"])
        phase["phase_equivalence"].pop("source_ids")
        self.assertFalse(evaluate.evaluate_target(target)["negative_claim_allowed"])

    def test_modern_benchmark_needs_measured_ancient_surface_join(self):
        target = complete_synthetic_target()
        value = target["gate_evidence"]["ancient_datum"]["value"]
        value.update({"datum_id": "synthetic-modern-benchmark", "datum_kind": "modern_benchmark"})
        target["gate_evidence"]["actual_reach"]["value"]["datum_id"] = "synthetic-modern-benchmark"
        self.assertFalse(evaluate.evaluate_target(target)["negative_claim_allowed"])
        value["modern_benchmark_join"] = {
            "benchmark_id": "synthetic-modern-benchmark", "ancient_surface_id": "synthetic-threshold",
            "surface_phase": "synthetic-A", "reference_frame": "synthetic-local",
            "measured_offset": {"value": -1.2, "unit": "m", "convention": "ancient_surface_minus_benchmark"},
            "uncertainty_m": 0.02, "source_ids": ["synthetic-measured-join-source"],
        }
        self.assertTrue(evaluate.evaluate_target(target)["negative_claim_allowed"])
        for field, bad_value in (("ancient_surface_id", "another-surface"), ("surface_phase", "synthetic-C"), ("benchmark_id", "another-benchmark"), ("reference_frame", "another-frame"), ("source_ids", []), ("uncertainty_m", None)):
            with self.subTest(field=field):
                invalid = deepcopy(target)
                invalid["gate_evidence"]["ancient_datum"]["value"]["modern_benchmark_join"][field] = bad_value
                result = evaluate.evaluate_target(invalid)
                self.assertFalse(result["negative_claim_allowed"])
                self.assertIn("ancient_datum", result["missing_gate_ids"])

    def test_modern_benchmark_offset_needs_metric_convention_and_finite_value(self):
        target = complete_synthetic_target()
        value = target["gate_evidence"]["ancient_datum"]["value"]
        value.update({"datum_id": "synthetic-modern-benchmark", "datum_kind": "modern_benchmark"})
        target["gate_evidence"]["actual_reach"]["value"]["datum_id"] = "synthetic-modern-benchmark"
        value["modern_benchmark_join"] = {
            "benchmark_id": "synthetic-modern-benchmark", "ancient_surface_id": "synthetic-threshold",
            "surface_phase": "synthetic-A", "reference_frame": "synthetic-local",
            "measured_offset": {"value": -1.2, "unit": "m", "convention": "ancient_surface_minus_benchmark"},
            "uncertainty_m": 0.02, "source_ids": ["synthetic-measured-join-source"],
        }
        for field, bad_value in (("value", float("nan")), ("unit", "unknown units"), ("convention", "unreported")):
            with self.subTest(field=field):
                invalid = deepcopy(target)
                invalid["gate_evidence"]["ancient_datum"]["value"]["modern_benchmark_join"]["measured_offset"][field] = bad_value
                self.assertFalse(evaluate.evaluate_target(invalid)["negative_claim_allowed"])

    def test_unsupported_established_assertion_does_not_pass(self):
        target = complete_synthetic_target()
        target["gate_evidence"]["detection_method"]["source_ids"] = []
        result = evaluate.evaluate_target(target)
        self.assertIn("detection_method", result["missing_gate_ids"])
        self.assertFalse(result["negative_excavation_eligible"])

    def test_unmatched_datum_or_reference_frame_is_unknown(self):
        for field, value in (("reference_frame", "another-frame"), ("datum_id", "another-surface"), ("target_id", "another-target")):
            with self.subTest(field=field):
                target = complete_synthetic_target()
                target["gate_evidence"]["actual_reach"]["value"][field] = value
                result = evaluate.evaluate_target(target)
                self.assertFalse(result["negative_claim_allowed"])
                self.assertIn("actual_reach", result["missing_gate_ids"])

    def test_partial_reach_and_uninterpretable_loss_fail_eligibility(self):
        for gate, field in (("actual_reach", "covers_entire_target"), ("disturbance_assessment", "negative_observation_interpretable")):
            with self.subTest(gate=gate):
                target = complete_synthetic_target()
                target["gate_evidence"][gate]["value"][field] = False
                result = evaluate.evaluate_target(target)
                self.assertFalse(result["negative_claim_allowed"])
                self.assertIn(gate, result["failed_gate_ids"])

    def test_unexplained_removal_cannot_rescue_negative(self):
        target = complete_synthetic_target()
        target["gate_evidence"]["disturbance_assessment"]["value"]["unexplained_removal_used_as_rescue"] = True
        result = evaluate.evaluate_target(target)
        self.assertFalse(result["negative_claim_allowed"])
        self.assertIn("disturbance_assessment", result["failed_gate_ids"])


class ImportedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = evaluate.build(ROOT)

    def test_documentary_counts_do_not_become_physical_denominators(self):
        data = self.module["data"]
        self.assertEqual(len(data["notices"]), 28)
        self.assertEqual(len(data["sectors"]), 12)
        self.assertEqual(len(data["obligations"]), 21)
        self.assertEqual(data["summary"]["record_kind_counts"], {"phase_state": 3, "physical_feature": 13, "aggregate_notice": 10, "unresolved_feature_identity": 2})
        for field in ("distinct_eligible_basins", "regional_eligible_denominator", "inventory_detection_rate"):
            self.assertIsNone(data["summary"][field])
        self.assertIsNone(data["regional_boundary"]["polygon"])
        self.assertTrue(all(notice["geometry"] is None for notice in data["notices"]))

    def test_every_notice_has_the_same_coverage_gates(self):
        data = self.module["data"]
        for notice in data["notices"]:
            with self.subTest(notice=notice["id"]):
                self.assertEqual(notice["gate_ids"], list(evaluate.GATE_LABELS))
                self.assertEqual(notice["missing_gate_ids"], list(evaluate.GATE_LABELS))
        self.assertFalse(any(target["negative_claim_allowed"] for target in data["targets"]))

    def test_current_wadi_original_supersedes_historical_pending_dependency(self):
        notice = next(item for item in self.module["data"]["notices"] if item["id"] == "J23")
        self.assertEqual(notice["current_original_status"], "already_inspected")
        self.assertTrue(notice["original_scope_complete"])
        self.assertTrue(notice["historical_source_dependency_superseded"])
        self.assertEqual(notice["record_kind"], "aggregate_notice")
        self.assertEqual(notice["explicit_baths_described"], 1)
        self.assertIsNone(notice["complete_site_bath_count"])
        self.assertEqual(notice["reported_depth_m"], 1.3)
        self.assertIsNone(notice["bath_footprint_dimensions_m"])
        self.assertIsNone(notice["bath_construction_date"])
        self.assertTrue(notice["western_rectangle_dimensions_not_bath_dimensions"])
        self.assertIn("field record", notice["next_observation"])
        self.assertIn("Dinur", notice["historical_record"]["next_observation"])

    def test_duplicate_lower_cypros_notices_count_each_observation_once(self):
        observations = self.module["data"]["coverage_observations"]
        cypros = [item for item in observations if item["physical_notice_id"] in ("CY_LOWER_CISTERN_1", "CY_LOWER_CISTERN_2")]
        self.assertEqual(len(cypros), 2)
        self.assertTrue(all(item["related_notice_ids"] == ["J14", "J18"] for item in cypros))
        sources = {"S": {"observation_lineage_id": "shared-lineage"}}
        first = {"id": "A", "status": "destroyed", "normalization_notice_id": "cistern-1", "original_ids": ["J14"], "citation": {"source_id": "S", "printed_pages": [1]}}
        duplicate = deepcopy(first)
        duplicate.update({"id": "B", "original_ids": ["J18"]})
        deduplicated = evaluate._deduplicate_coverage_observations([first, duplicate], sources)
        self.assertEqual(len(deduplicated), 1)
        self.assertEqual(deduplicated[0]["related_notice_ids"], ["J14", "J18"])
        # Without an explicit same-feature ID, similar notices must not collapse.
        first.pop("normalization_notice_id")
        duplicate.pop("normalization_notice_id")
        self.assertEqual(len(evaluate._deduplicate_coverage_observations([first, duplicate], sources)), 2)

    def test_netzer_derivative_publications_share_one_lineage(self):
        campaign = next(item for item in self.module["data"]["campaigns"] if item["id"] == "netzer_jericho_excavation_lineage")
        self.assertTrue(set(("coverage-netzer1983", "coverage-netzer1989", "coverage-netzer2001", "coverage-trumper2018")).issubset(campaign["source_ids"]))
        self.assertEqual(campaign["independent_campaign_increment"], 0)
        unknown = next(item for item in self.module["data"]["notices"] if item["id"] == "J13")
        self.assertTrue(unknown["campaign_identity_unknown"])
        self.assertEqual(unknown["campaign_ids"], [])

    def test_state_merger_does_not_collapse_distinct_early_basins(self):
        relations = self.module["data"]["identity_relations"]
        merger = next(item for item in relations if item["id"] == "REL_MERGER")
        self.assertEqual(merger["earlier_members"], ["J01", "J02"])
        self.assertEqual(merger["later_member"], "J03")
        distinct = next(item for item in relations if item["id"] == "REL_EARLY_PAIR_DISTINCT")
        self.assertEqual(distinct["members"], ["J01", "J02"])

    def test_iv17_central_excavation_does_not_prove_threshold_reach(self):
        target = next(item for item in self.module["data"]["targets"] if item["id"] == "coverage-target-iv17")
        self.assertFalse(target["negative_excavation_eligible"])
        self.assertFalse(target["field_file_inspected"])
        self.assertIsNone(target["excavation_footprint"])
        self.assertIsNone(target["maximum_reached_depth_m"])
        self.assertIsNone(target["ancient_threshold_elevation"])
        self.assertIsNone(target["depth_branch"]["deposit_geometry"])
        self.assertFalse(target["local_plan_is_excavation_footprint"])
        self.assertEqual(target["field_record"]["permit"], "L-656")
        self.assertTrue(target["repeated_coin_evidence_deduplicated"])

    def test_bounded_coverage_facts_do_not_become_whole_basin_claims(self):
        by_id = {item["id"]: item for item in self.module["data"]["coverage_observations"]}
        ac90 = by_id["coverage-unexcavated-ac90-bottom"]
        ac44 = by_id["coverage-destroyed-ac44-east"]
        self.assertIsNone(ac90["whole_basin_unexcavated"])
        self.assertFalse(ac44["whole_basin_destroyed"])
        self.assertIsNone(ac44["target_volume_relation"])

    def test_all_source_and_feature_references_resolve(self):
        source_ids = {source["id"] for source in self.module["sources"]}
        shared = evaluate._load(ROOT, "research/feature_workbench/features.json")["features"]
        feature_ids = {feature["id"] for feature in shared + self.module["features"]}
        for observation in self.module["observations"]:
            self.assertIn(observation["feature_id"], feature_ids)
            self.assertTrue(set(observation["source_ids"]).issubset(source_ids))
        for result in self.module["results"]:
            self.assertTrue(set(result["source_ids"]).issubset(source_ids))
            self.assertTrue(set(result["feature_ids"]).issubset(feature_ids))
            for check in result["checks"]:
                self.assertTrue(set(check["source_ids"]).issubset(source_ids))
        self.assertFalse(self.module["data"]["parked_tests_reopened"])


if __name__ == "__main__":
    unittest.main()
