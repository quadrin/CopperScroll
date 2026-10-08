"""Check shared provenance/reference contracts and unchanged research claims."""
import copy
import json
from pathlib import Path
import unittest

import build


class SharedRegisterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = build.build()

    def test_modules_share_resolved_features_and_sources(self):
        self.assertEqual([module["number"] for module in self.payload["modules"]], [2, 3, 4, 5, 6])
        build.validate_register(self.payload["register"], build.ROOT)
        build.validate_modules(self.payload["modules"], self.payload["register"])

    def test_feature_redefinitions_cannot_silently_merge(self):
        register = copy.deepcopy(self.payload["register"])
        register["features"].append(dict(register["features"][0], name="A different physical feature"))
        with self.assertRaisesRegex(ValueError, "duplicate id"):
            build.validate_register(register, build.ROOT)

    def test_missing_and_outside_repo_sources_fail(self):
        for path in ("missing-observation.json", "../../outside-evidence.json"):
            register = copy.deepcopy(self.payload["register"])
            register["sources"][0]["repo_path"] = path
            with self.assertRaisesRegex(ValueError, "missing or unsafe source"):
                build.validate_register(register, build.ROOT)

    def test_orphan_observation_and_result_fail(self):
        register = copy.deepcopy(self.payload["register"])
        register["observations"][0]["feature_id"] = "unknown-physical-feature"
        with self.assertRaisesRegex(ValueError, "unknown feature"):
            build.validate_register(register, build.ROOT)
        modules = copy.deepcopy(self.payload["modules"])
        modules[0]["results"][0]["source_ids"] = ["missing-source"]
        with self.assertRaisesRegex(ValueError, "unknown source_ids"):
            build.validate_modules(modules, self.payload["register"])

    def test_geometry_requires_reference_frame(self):
        register = copy.deepcopy(self.payload["register"])
        register["features"][0]["geometry"] = {"type": "Point", "coordinates": [0, 0]}
        with self.assertRaisesRegex(ValueError, "geometry without reference frame"):
            build.validate_register(register, build.ROOT)

    def test_no_confirmatory_or_negative_deposit_claim_added(self):
        limits = self.payload["limits"]
        self.assertIsNone(limits["regional_eligible_denominator"])
        self.assertFalse(limits["confirmatory"])
        self.assertFalse(limits["unused_observation_certified"])
        self.assertEqual(limits["new_source_inspections"], 0)
        self.assertEqual(limits["new_outcomes"], 0)
        coverage = next(module for module in self.payload["modules"] if module["id"] == "coverage")
        self.assertTrue(all(not target["negative_claim_allowed"] for target in coverage["data"]["targets"]))

    def test_original_queue_is_preserved_and_outcomes_are_hypothetical(self):
        decisions = next(module for module in self.payload["modules"] if module["id"] == "decisions")
        queue = json.loads((build.ROOT / "research/measurements/queue.json").read_text())
        self.assertEqual(decisions["data"]["historical_queue"]["tracks"], queue["tracks"])
        self.assertTrue(all(outcome["recorded"] is False for task in decisions["data"]["tasks"] for outcome in task["outcomes"]))

    def test_native_geometry_is_not_promoted_to_world_coordinates(self):
        self.assertTrue(all(feature["geometry"] is None for feature in self.payload["register"]["features"]))
        self.assertTrue(all(state.get("world_geometry") is None for state in self.payload["register"]["states"]))
        self.assertNotEqual(next(feature for feature in self.payload["register"]["features"] if feature["id"] == "jericho-historical-basin"), next(feature for feature in self.payload["register"]["features"] if feature["id"] == "jericho-reservoir-1898"))


if __name__ == "__main__":
    unittest.main()
