"""Tests target false ancient configurations, alias joins and geometry promotion."""

import copy
import importlib.util
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("feature_states_evaluator", HERE / "evaluate.py")
EVALUATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVALUATOR)


class StateSafetyTests(unittest.TestCase):
    def setUp(self):
        self.register = json.loads((HERE / "register.json").read_text(encoding="utf-8"))
        self.states = {state["id"]: state for state in self.register["states"]}
        self.queries = {query["id"]: query for query in self.register["queries"]}

    def outcome(self, query_id):
        return EVALUATOR.evaluate_claim(self.register, self.queries[query_id])["status"]

    def add_reviewed_iv17_level_fixture(self):
        # Entirely synthetic validation fixture, never added to production data.
        source_id, frame_id = "states-fixture-field-record", "states-fixture-iv17-levels"
        self.register["sources"].append({"id": source_id, "inspection": "already_inspected"})
        self.register["reference_frames"].append({"id": frame_id, "kind": "local_excavation", "site": "Abu Saraj", "feature_ids": ["iv17-north-mouth"], "source_ids": [source_id], "geographic_registration": None})
        threshold = self.states["states-iv17-north-ancient-threshold"]
        threshold["status"] = "observed"
        threshold["source_ids"].append(source_id)
        threshold["level_reference_frame"] = frame_id
        datum = {"value": 2.0, "unit": "m", "surface": "ancient_northern_threshold", "phase": "fixture-observed-phase", "evidence_kind": "observed", "feature_id": "iv17-north-mouth", "site": "Abu Saraj", "reference_frame": frame_id, "source_ids": [source_id]}
        threshold["threshold_elevation"] = datum
        return datum

    def add_reviewed_access_fixture(self, query_id):
        # Synthetic dated observation; this fixture never enters the register.
        query = self.queries[query_id]
        source_id = "states-fixture-access-record"
        if not any(source["id"] == source_id for source in self.register["sources"]):
            self.register["sources"].append({"id": source_id, "inspection": "already_inspected"})
        relation = {"state_ids": query["state_ids"], "evidence_kind": "observed", "accessible_together": True, "source_ids": [source_id], "phase": query["required_access_phase"], "dated_accessible_interval": [25, 50], "calendar": "historical_year", "dating_basis": "dated_observed_access_episode"}
        self.register.setdefault("access_relations", []).append(relation)
        return relation

    def test_successive_graves_and_pits_are_not_same_phase(self):
        self.assertEqual(self.outcome("states-jericho-same-phase"), "contradicted")
        self.assertEqual(self.outcome("states-jericho-access"), "unknown")

    def test_sequence_is_directional_and_reconstruction_cannot_create_it(self):
        query = copy.deepcopy(self.queries["states-d9-sequence"])
        self.assertEqual(EVALUATOR.evaluate_claim(self.register, query)["status"], "compatible")
        query["state_ids"].reverse()
        self.assertEqual(EVALUATOR.evaluate_claim(self.register, query)["status"], "contradicted")
        next(t for t in self.register["transitions"] if t["id"] == "states-d9-reuse")["evidence_kind"] = "inference"
        self.assertEqual(EVALUATOR.evaluate_claim(self.register, query)["status"], "unknown")

    def test_relative_order_and_typology_cannot_date_pit_opening(self):
        pit = self.states["states-jericho-quarries-recorded"]
        query = {"kind": "construction_window", "state_ids": [pit["id"]], "years": [-100, 100]}
        self.assertEqual(EVALUATOR.evaluate_claim(self.register, query)["status"], "unknown")
        pit["phase"]["construction"] = {"basis": "published_reconstruction", "years": [1, 100]}
        self.assertEqual(EVALUATOR.evaluate_claim(self.register, query)["status"], "unknown")

    def test_construction_window_keeps_modern_and_historical_basins_distinct(self):
        self.assertEqual(self.outcome("states-jericho-modern-early"), "contradicted")
        self.assertEqual(self.outcome("states-jericho-historical-early"), "unknown")
        self.assertNotEqual(self.states["states-spring-historical-basin"]["feature_id"],
                            self.states["states-spring-reservoir-1898"]["feature_id"])

    def test_hellenistic_use_does_not_date_the_blocking_wall(self):
        self.assertEqual(self.outcome("states-iv17-ancient-wall"), "unknown")
        use = self.states["states-iv17-hellenistic-use"]
        self.assertEqual(use["status"], "reconstructed")
        self.assertIsNone(use["phase"]["construction"])

    def test_northern_threshold_is_required_and_modern_datum_cannot_replace_it(self):
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
        threshold = self.states["states-iv17-north-ancient-threshold"]
        threshold["threshold_elevation"] = {"value": 8.17, "unit": "m", "surface": "present_surface", "phase": "unknown", "reference_frame": "states-kenyon-trench-II", "source_ids": ["states-kenyon-III"]}
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")

    def test_null_nonfinite_boolean_and_unknown_datum_metadata_cannot_make_a_target(self):
        datum = self.add_reviewed_iv17_level_fixture()
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "compatible")
        for bad_value in [None, True, float("nan"), float("inf"), "8.17"]:
            with self.subTest(value=bad_value):
                datum["value"] = bad_value
                self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
        datum.pop("value")
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
        datum["value"] = 8.17
        for phase in [None, "", "unknown", "unknown phase", "undated phase"]:
            with self.subTest(phase=phase):
                datum["phase"] = phase
                self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
        datum["phase"] = "fixture-observed-phase"
        datum["reference_frame"] = "unknown"
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
        datum["reference_frame"] = "states-iv17-plan5-crop"
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
        datum["reference_frame"] = "states-kenyon-trench-II"
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
        datum["source_ids"] = ["states-kenyon-III"]
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")

    def test_datum_needs_explicit_feature_site_and_level_frame_binding(self):
        datum = self.add_reviewed_iv17_level_fixture()
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "compatible")
        for field in ["feature_id", "site"]:
            old_value = datum.pop(field)
            self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
            datum[field] = old_value
        self.states["states-iv17-north-ancient-threshold"]["level_reference_frame"] = None
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")
        self.states["states-iv17-north-ancient-threshold"]["level_reference_frame"] = "states-kenyon-trench-II"
        datum["reference_frame"] = "states-kenyon-trench-II"
        # Even a nominally inspected source and local level cannot cross sites.
        datum["source_ids"] = ["states-kenyon-III"]
        self.states["states-iv17-north-ancient-threshold"]["source_ids"].append("states-kenyon-III")
        self.assertEqual(self.outcome("states-iv17-depth-datum"), "unknown")

    def test_unsourced_access_assertion_cannot_override_unknown(self):
        query = self.queries["states-jericho-ns1-join"]
        query["observed_access_relation"] = True
        self.assertEqual(self.outcome(query["id"]), "unknown")
        relation = self.add_reviewed_access_fixture(query["id"])
        relation["source_ids"] = ["states-kenyon-III-plates"]
        self.assertEqual(self.outcome(query["id"]), "unknown")

    def test_modern_access_does_not_prove_or_exclude_ancient_access(self):
        for query_id in ["states-iv17-ancient-aperture", "states-jericho-access", "states-jericho-ns1-join"]:
            with self.subTest(query=query_id):
                relation = self.add_reviewed_access_fixture(query_id)
                relation["phase"] = "2002 survey arrangement"
                relation["dated_accessible_interval"] = [2002, 2002]
                self.assertEqual(self.outcome(query_id), "unknown")
                # Relabelling the episode still cannot change its modern date.
                relation["phase"] = self.queries[query_id]["required_access_phase"]
                self.assertEqual(self.outcome(query_id), "unknown")
                relation["accessible_together"] = False
                relation["exhaustive_for_query"] = True
                relation["query_id"] = query_id
                self.assertEqual(self.outcome(query_id), "unknown")

    def test_phase_bound_dated_access_can_support_the_specific_window(self):
        for query_id in ["states-iv17-ancient-aperture", "states-jericho-access", "states-jericho-ns1-join"]:
            with self.subTest(query=query_id):
                modern = self.add_reviewed_access_fixture(query_id)
                modern["dated_accessible_interval"] = [2002, 2002]
                self.add_reviewed_access_fixture(query_id)
                self.assertEqual(self.outcome(query_id), "compatible")

    def test_partial_disjoint_or_uncertain_access_episode_is_not_an_ancient_failure(self):
        query_id = "states-jericho-access"
        relation = self.add_reviewed_access_fixture(query_id)
        for interval, accessible in [([-200, -150], True), ([-200, -150], False), ([25, 50], False), ([75, 125], True)]:
            with self.subTest(interval=interval, accessible=accessible):
                relation["dated_accessible_interval"] = interval
                relation["accessible_together"] = accessible
                self.assertEqual(self.outcome(query_id), "unknown")

    def test_access_observation_requires_phase_window_and_dated_observation(self):
        query_id = "states-iv17-ancient-aperture"
        relation = self.add_reviewed_access_fixture(query_id)
        self.assertEqual(self.outcome(query_id), "compatible")
        for key in ["phase", "calendar", "dated_accessible_interval", "dating_basis"]:
            with self.subTest(missing=key):
                old_value = relation.pop(key)
                self.assertEqual(self.outcome(query_id), "unknown")
                relation[key] = old_value
        for interval in [[None, 50], [True, 50], [float("nan"), 50], [25, float("inf")], [50, 25]]:
            with self.subTest(interval=interval):
                relation["dated_accessible_interval"] = interval
                self.assertEqual(self.outcome(query_id), "unknown")
        relation["dated_accessible_interval"] = [25, 50]
        self.queries[query_id]["required_access_phase"] = "unknown phase"
        self.assertEqual(self.outcome(query_id), "unknown")
        self.queries[query_id]["required_access_phase"] = relation["phase"]
        self.queries[query_id]["years"] = None
        self.assertEqual(self.outcome(query_id), "unknown")

    def test_negative_access_requires_explicit_complete_query_coverage(self):
        query_id = "states-jericho-access"
        relation = self.add_reviewed_access_fixture(query_id)
        relation["accessible_together"] = False
        relation["dated_accessible_interval"] = [-100, 100]
        self.assertEqual(self.outcome(query_id), "unknown")
        relation["exhaustive_for_query"] = True
        relation["query_id"] = "states-other-query"
        self.assertEqual(self.outcome(query_id), "unknown")
        relation["query_id"] = query_id
        self.assertEqual(self.outcome(query_id), "contradicted")
        self.add_reviewed_access_fixture(query_id)
        self.assertEqual(self.outcome(query_id), "mixed")

    def test_native_frames_fail_closed_on_world_coordinates(self):
        self.register["reference_frames"][0]["geographic_registration"] = {"crs": "EPSG:4326"}
        with self.assertRaisesRegex(ValueError, "geographic registration"):
            EVALUATOR.validate_register(self.register)
        self.register["reference_frames"][0]["geographic_registration"] = None
        self.states["states-iv17-north-recorded"]["world_geometry"] = {"type": "Point", "coordinates": [35.4, 31.8]}
        with self.assertRaisesRegex(ValueError, "world geometry"):
            EVALUATOR.validate_register(self.register)

    def test_native_segment_needs_exact_named_crop_and_provenance(self):
        north = self.states["states-iv17-north-recorded"]
        north["geometry"] = {"type": "source_plan_segment", "units": "px", "points": [[548, 386], [627, 400]], "source_ids": ["states-iv17-repeat"]}
        with self.assertRaisesRegex(ValueError, "outside"):
            EVALUATOR.validate_register(self.register)
        north["geometry"]["points"][1] = [502, 400]
        north["reference_frame"] = "states-kenyon-trench-II"
        with self.assertRaisesRegex(ValueError, "bound to this feature and site"):
            EVALUATOR.validate_register(self.register)
        self.register["reference_frames"].append({"id": "states-fixture-wrong-plane", "kind": "local_excavation", "site": "Abu Saraj", "feature_ids": ["iv17-north-mouth"], "source_ids": ["states-sion-plan"], "geographic_registration": None})
        north["reference_frame"] = "states-fixture-wrong-plane"
        with self.assertRaisesRegex(ValueError, "native pixel frame"):
            EVALUATOR.validate_register(self.register)

    def test_phase_cycles_are_rejected(self):
        self.register["transitions"].append({"id": "states-bad-reverse", "from": "states-jericho-d9-roman", "to": "states-jericho-d9-mb", "relation": "before", "evidence_kind": "observed", "source_ids": ["states-kenyon-II"]})
        with self.assertRaisesRegex(ValueError, "cycle"):
            EVALUATOR.validate_register(self.register)

    def test_build_imports_corrected_chords_and_retains_unknowns(self):
        result = EVALUATOR.build(HERE.parents[2])
        states = {state["id"]: state for state in result["states"]}
        self.assertEqual(states["states-iv17-north-recorded"]["geometry"]["points"], [[548, 386], [502, 400]])
        self.assertEqual(states["states-iv17-south-recorded"]["geometry"]["points"], [[258, 398], [319, 375]])
        self.assertTrue(all(state["world_geometry"] is None for state in result["states"]))
        self.assertIsNone(states["states-iv17-north-ancient-threshold"]["depth_branch"]["target_geometry"])
        self.assertTrue(all((HERE.parents[2] / source["repo_path"]).is_file() for source in result["sources"]))
        results = {row["id"]: row for row in result["results"]}
        self.assertEqual(results["states-jericho-same-phase"]["status"], "contradicted")
        self.assertEqual(results["states-jericho-access"]["status"], "unknown")


if __name__ == "__main__":
    unittest.main()
