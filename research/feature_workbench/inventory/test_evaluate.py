"""Tests of evidence semantics and equal treatment, not snapshot output."""

import copy
import importlib.util
import json
from pathlib import Path
import unittest


MODULE_DIR = Path(__file__).resolve().parent
REPO_ROOT = MODULE_DIR.parents[2]
SPEC = importlib.util.spec_from_file_location("inventory_evaluate", MODULE_DIR / "evaluate.py")
evaluate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluate)


def candidate_with(value, **metadata):
    return {"feature_ids": ["example-feature"], "properties": {"feature": {"value": value, "source_ids": [], **metadata}}}


def threshold_candidate(value=10):
    return {
        "feature_ids": ["example-cave", "example-north-mouth", "example-south-mouth"],
        "reference_features": {"northern_opening": "example-north-mouth"},
        "properties": {
            "northern_threshold_elevation": {
                "value": value, "unit": "m", "phase": "ancient_arrangement",
                "feature_id": "example-north-mouth", "source_ids": [],
                "reference_frame": "example local level survey",
                "datum": {
                    "id": "example benchmark 1", "reference_point": "surveyed local benchmark 1",
                    "reference_frame": "example local level survey", "positive_direction": "up",
                },
            }
        },
    }


class PredicateSemantics(unittest.TestCase):
    def test_missing_observation_is_unknown(self):
        self.assertEqual(evaluate.evaluate_predicate(candidate_with(None), {"property": "feature", "expected": True})["status"], "unknown")

    def test_positive_absence_can_contradict(self):
        self.assertEqual(evaluate.evaluate_predicate(candidate_with(False), {"property": "feature", "expected": True})["status"], "contradicted")

    def test_bool_cannot_supply_numeric_quantity(self):
        outcome = evaluate.evaluate_predicate(candidate_with(True), {"property": "feature", "operation": "at_least", "expected": 1})
        self.assertEqual(outcome["status"], "unknown")
        equality = evaluate.evaluate_predicate(candidate_with(True), {"property": "feature", "expected": 1})
        self.assertEqual(equality["status"], "unknown")

    def test_unit_mismatch_is_unknown_not_numerical_miss(self):
        outcome = evaluate.evaluate_predicate(candidate_with(80, unit="cm"), {"property": "feature", "operation": "between", "expected": [0.7, 0.9], "unit": "m"})
        self.assertEqual(outcome["status"], "unknown")

    def test_source_plan_proxy_cannot_be_true_bearing(self):
        outcome = evaluate.evaluate_predicate(candidate_with(123, unit="deg", reference_frame="source-plan chord normal"), {"property": "feature", "operation": "between", "expected": [80, 100], "unit": "deg", "reference_frame": "true geographic bearing"})
        self.assertEqual(outcome["status"], "unknown")

    def test_observed_phase_cannot_supply_ancient_datum(self):
        outcome = evaluate.evaluate_predicate(candidate_with(10, unit="m", phase="reported_state"), {"property": "feature", "operation": "known", "unit": "m", "phase": "ancient_arrangement"})
        self.assertEqual(outcome["status"], "unknown")

    def test_interval_partial_overlap_is_unknown(self):
        predicate = {"property": "feature", "operation": "between", "expected": [0.7, 0.9], "unit": "m"}
        self.assertEqual(evaluate.evaluate_predicate(candidate_with([0.6, 0.85], unit="m"), predicate)["status"], "unknown")
        self.assertEqual(evaluate.evaluate_predicate(candidate_with([0.75, 0.85], unit="m"), predicate)["status"], "compatible")
        self.assertEqual(evaluate.evaluate_predicate(candidate_with([1.0, 1.2], unit="m"), predicate)["status"], "contradicted")

    def test_nonfinite_quantity_is_unknown(self):
        outcome = evaluate.evaluate_predicate(candidate_with(float("nan")), {"property": "feature", "operation": "at_least", "expected": 1})
        self.assertEqual(outcome["status"], "unknown")

    def test_known_threshold_requires_finite_scalar_quantity(self):
        predicate = {"property": "northern_threshold_elevation", "operation": "known", "unit": "m", "phase": "ancient_arrangement"}
        for value in (True, False, float("nan"), float("inf"), -float("inf"), "unknown", "10", [9, 11], {"amount": 10, "unit": "m"}):
            with self.subTest(value=value):
                self.assertEqual(evaluate.evaluate_predicate(threshold_candidate(value), predicate)["status"], "unknown")
        # Zero is a valid finite elevation if it has an explicit local datum.
        self.assertEqual(evaluate.evaluate_predicate(threshold_candidate(0), predicate)["status"], "compatible")

    def test_known_threshold_requires_its_northern_feature(self):
        predicate = {"property": "northern_threshold_elevation", "operation": "known", "unit": "m", "phase": "ancient_arrangement"}
        candidate = threshold_candidate()
        candidate["properties"]["northern_threshold_elevation"]["feature_id"] = "example-south-mouth"
        self.assertEqual(evaluate.evaluate_predicate(candidate, predicate)["status"], "unknown")
        candidate = threshold_candidate()
        candidate["reference_features"]["northern_opening"] = None
        self.assertEqual(evaluate.evaluate_predicate(candidate, predicate)["status"], "unknown")

    def test_known_threshold_requires_frame_bound_vertical_datum(self):
        predicate = {"property": "northern_threshold_elevation", "operation": "known", "unit": "m", "phase": "ancient_arrangement"}
        for change in (
            {"datum": None},
            {"reference_frame": "threshold elevation datum unestablished"},
            {"datum": {"id": "benchmark", "reference_point": "benchmark 1", "reference_frame": "different level survey", "positive_direction": "up"}},
            {"datum": {"id": "benchmark", "reference_point": "benchmark 1", "reference_frame": "example local level survey", "positive_direction": "down"}},
        ):
            with self.subTest(change=change):
                candidate = threshold_candidate()
                candidate["properties"]["northern_threshold_elevation"].update(change)
                self.assertEqual(evaluate.evaluate_predicate(candidate, predicate)["status"], "unknown")
        candidate = threshold_candidate()
        candidate["properties"]["northern_threshold_elevation"]["reference_frame"] = {"id": "example local level survey", "kind": "local level survey"}
        self.assertEqual(evaluate.evaluate_predicate(candidate, predicate)["status"], "compatible")

    def test_generic_known_supports_structured_origins_and_paths(self):
        predicate = {"property": "feature", "operation": "known", "phase": "reported_state"}
        for value in ({"x": 1, "y": 2}, {"start": [1, 2], "direction": [0, 1]}):
            self.assertEqual(evaluate.evaluate_predicate(candidate_with(value, phase="reported_state"), predicate)["status"], "compatible")
        for value in ("unknown", "Unestablished", " "):
            self.assertEqual(evaluate.evaluate_predicate(candidate_with(value, phase="reported_state"), predicate)["status"], "unknown")

    def test_conjunction_preserves_contradiction_despite_other_missing_data(self):
        self.assertEqual(evaluate.conjunction(["compatible", "unknown"]), "unknown")
        self.assertEqual(evaluate.conjunction(["contradicted", "unknown"]), "contradicted")
        self.assertEqual(evaluate.branch_summary(["compatible", "unknown"]), "mixed")

    def test_bad_query_configuration_fails(self):
        with self.assertRaises(ValueError):
            evaluate.evaluate_predicate(candidate_with(1), {"property": "feature", "operation": "between", "expected": [2, 1]})
        with self.assertRaises(ValueError):
            evaluate.conjunction([])


class Entry25Inventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = evaluate.build(REPO_ROOT)
        cls.catalog = cls.module["data"]["catalog"]
        cls.dimensions = cls.module["data"]["dimensions"]
        cls.queries = cls.module["data"]["queries"]

    def test_every_control_receives_identical_full_branch_set(self):
        for query, expected in zip(self.queries, [4, 96]):
            canonical = [branch["id"] for branch in query["branches"]]
            self.assertEqual(len(canonical), expected)
            self.assertEqual(len(query["candidate_results"]), 3)
            for candidate in query["candidate_results"]:
                self.assertEqual([branch["branch_id"] for branch in candidate["branches"]], canonical)

    def test_three_cubits_is_distance_not_mouth_width(self):
        altered = copy.deepcopy(self.catalog)
        altered[0]["properties"]["northern_opening_width_reported"]["value"] = 200
        for query in self.queries:
            original = evaluate.evaluate_query(query, self.catalog, self.dimensions)
            changed = evaluate.evaluate_query(query, altered, self.dimensions)
            self.assertEqual(original["candidate_results"], changed["candidate_results"])
        target = self.queries[1]
        self.assertEqual({branch["depth_metres"] for branch in target["branches"]}, {1.2, 1.5, 1.8})

    def test_iv11_unestablished_pair_never_becomes_absence(self):
        iv11 = next(candidate for candidate in self.catalog if candidate["id"] == "iv11")
        self.assertIsNone(iv11["properties"]["two_exterior_openings"]["value"])
        for query in self.queries:
            candidate = next(result for result in query["candidate_results"] if result["candidate_id"] == "iv11")
            self.assertEqual(candidate["counts"]["contradicted"], 0)
            self.assertEqual(candidate["status"], "unknown")

    def test_connectivity_is_not_a_mandatory_predicate(self):
        altered = copy.deepcopy(self.catalog)
        for candidate in altered:
            candidate["properties"]["ancient_traversable_connection"]["value"] = False
        for query in self.queries:
            original = evaluate.evaluate_query(query, self.catalog, self.dimensions)
            changed = evaluate.evaluate_query(query, altered, self.dimensions)
            self.assertEqual(original["candidate_results"], changed["candidate_results"])

    def test_phased_target_never_claims_a_location(self):
        for candidate in self.queries[1]["candidate_results"]:
            self.assertEqual(candidate["counts"], {"compatible": 0, "contradicted": 0, "unknown": 96})
        self.assertTrue(all(result["status"] == "unknown" for result in self.module["results"]))
        self.assertIsNone(self.module["data"]["limits"]["eligible_denominator"])
        self.assertFalse(self.module["data"]["limits"]["coverage_complete"])

    def test_saved_target_query_rejects_false_threshold_quantities(self):
        for value in (True, float("nan"), "unknown"):
            with self.subTest(value=value):
                altered = copy.deepcopy(self.catalog)
                record = altered[0]["properties"]["northern_threshold_elevation"]
                record.update(threshold_candidate(value)["properties"]["northern_threshold_elevation"])
                record["feature_id"] = "iv17-north-mouth"
                query = evaluate.evaluate_query(self.queries[1], altered, self.dimensions)
                iv17 = next(result for result in query["candidate_results"] if result["candidate_id"] == "iv17")
                for branch in iv17["branches"]:
                    for check in branch["checks"]:
                        if check["id"] == "threshold-datum":
                            self.assertEqual(check["status"], "unknown")

    def test_retained_reading_misses_remain_visible(self):
        altered = copy.deepcopy(self.catalog)
        altered[0]["properties"]["pillar"]["value"] = False
        query = evaluate.evaluate_query(self.queries[0], altered, self.dimensions)
        iv17 = next(result for result in query["candidate_results"] if result["candidate_id"] == "iv17")
        self.assertEqual(iv17["counts"]["contradicted"], 2)
        self.assertEqual(iv17["counts"]["unknown"], 2)
        self.assertEqual(iv17["status"], "mixed")

    def test_known_form_overlap_does_not_rank_candidates(self):
        form = {candidate["candidate_id"]: candidate for candidate in self.queries[0]["candidate_results"]}
        self.assertEqual(form["iv17"]["counts"]["compatible"], 1)
        self.assertEqual(form["twin"]["counts"]["compatible"], 2)
        self.assertEqual(form["iv11"]["counts"]["compatible"], 0)
        self.assertNotIn("rank", self.module["data"])
        self.assertNotIn("confidence", self.module["data"])

    def test_catalog_quantity_drift_is_detected(self):
        altered = copy.deepcopy(self.catalog)
        altered[0]["properties"]["northern_opening_width_reported"]["value"] = 1.8
        with self.assertRaisesRegex(ValueError, "differs"):
            evaluate._review_consistency(REPO_ROOT, altered)

    def test_source_references_and_feature_ids_are_resolved(self):
        sources = {source["id"] for source in self.module["sources"]}
        features = {feature["id"] for feature in json.loads((REPO_ROOT / "research/feature_workbench/features.json").read_text())["features"]}
        for observation in self.module["observations"]:
            self.assertTrue(set(observation["source_ids"]) <= sources)
            self.assertIn(observation["feature_id"], features)
        for result in self.module["results"]:
            self.assertTrue(set(result["source_ids"]) <= sources)
            self.assertTrue(set(result["feature_ids"]) <= features)


if __name__ == "__main__":
    unittest.main()
