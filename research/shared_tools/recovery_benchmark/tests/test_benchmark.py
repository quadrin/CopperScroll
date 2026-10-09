"""Failure controls for scientific scope, missing data and answer separation."""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import benchmark as b


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.dataset = b.read(b.HERE / "source_grounded_cases.json")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.packet, self.key = b.prepare(self.dataset, Path(self.temp.name))
        self.freeze = b.read(Path(self.temp.name) / "coordinator" / "freeze_manifest.json")

    def test_source_cases_recover_and_abstain(self):
        result = b.grade(self.packet, b.predict(self.packet), self.key, self.freeze)
        self.assertEqual(result["summary"]["documentary_identities_recovered"], 6)
        self.assertEqual(result["summary"]["decision_survivor_checks_passed"], 13)
        self.assertIsNone(result["summary"]["independent_field_accuracy"])
        self.assertIsNone(result["summary"]["unseen_archaeological_confirmation"])

    def test_complete_match_cannot_eliminate_unmeasured_competitor(self):
        response = b.predict(self.packet)["responses"][-1]
        self.assertEqual(response["decision"], "insufficient_evidence")
        self.assertIsNone(response["selected_candidate_code"])
        self.assertEqual(len(response["surviving_candidate_codes"]), 2)

    def test_lost_entrance_inference_is_not_observed_direction(self):
        result = b.predict(self.packet)["responses"][9]
        self.assertEqual(result["decision"], "insufficient_evidence")
        self.assertEqual(result["candidate_checks"][1]["unknown_fields"], ["entrance_direction"])

    def test_phase_models_cannot_borrow_each_others_facts(self):
        result = b.predict(self.packet)["responses"][11]
        self.assertEqual(result["decision"], "insufficient_evidence")
        self.assertEqual(len(result["surviving_candidate_codes"]), 2)

    def test_only_observed_contradictions_make_null_case(self):
        altered = deepcopy(self.packet)
        null_case = altered["cases"][8]
        null_case["candidates"][0]["facts"]["floor_slope"]["value"] = None
        response = b.predict(altered)["responses"][8]
        self.assertEqual(response["decision"], "insufficient_evidence")
        self.assertEqual(response["surviving_candidate_codes"], ["K01"])

    def test_shuffle_models_preserves_survivors_and_decisions(self):
        altered = deepcopy(self.packet)
        for case in altered["cases"]:
            case["candidates"].reverse()
        before, after = b.predict(self.packet)["responses"], b.predict(altered)["responses"]
        for a, z in zip(before, after):
            self.assertEqual(a["decision"], z["decision"])
            self.assertEqual(set(a["surviving_candidate_codes"]), set(z["surviving_candidate_codes"]))

    def test_answer_data_rejected_in_reviewer_packet(self):
        altered = deepcopy(self.packet)
        altered["cases"][0]["target_id"] = "migdal_1"
        with self.assertRaisesRegex(ValueError, "Coordinator data"):
            b.predict(altered)

    def test_forecast_fields_excluded_across_all_matching_models(self):
        for case in self.packet["cases"]:
            for candidate in case["candidates"]:
                self.assertFalse(set(case["excluded_from_matching"]) & set(candidate["facts"]))
        altered = deepcopy(self.packet)
        altered["cases"][0]["predicates"].append({"field": "sump_corner", "equals": "southwest"})
        with self.assertRaisesRegex(ValueError, "reused for matching"):
            b.predict(altered)

    def test_packet_mutation_invalidates_grading_seal(self):
        predictions = b.predict(self.packet)
        altered = deepcopy(self.packet)
        altered["cases"][0]["description"] += " altered"
        with self.assertRaisesRegex(ValueError, "freeze manifest"):
            b.grade(altered, predictions, self.key, self.freeze)

    def test_wrong_identity_fails_source_scoring(self):
        predictions = b.predict(self.packet)
        predictions["responses"][0]["selected_candidate_code"] = "K02"
        predictions["responses"][0]["surviving_candidate_codes"] = ["K02"]
        result = b.grade(self.packet, predictions, self.key, self.freeze)
        self.assertFalse(result["results"][0]["documentary_identity_recovery"])
        self.assertFalse(result["results"][0]["decision_and_survivor_check"])

    def test_missing_case_cannot_vanish_from_denominator(self):
        predictions = b.predict(self.packet)
        predictions["responses"].pop()
        with self.assertRaisesRegex(ValueError, "Missing, duplicate"):
            b.grade(self.packet, predictions, self.key, self.freeze)

    def test_nonfinite_or_boolean_intervals_rejected(self):
        for span in ([0, float("nan")], [False, 1], [2, 1]):
            altered = deepcopy(self.packet)
            altered["cases"][3]["predicates"][0]["range"] = span
            with self.assertRaisesRegex(ValueError, "finite ordered"):
                b.predict(altered)

    def test_compare_rejects_nonfinite_observation_without_packet_adapter(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            b.compare({"value": float("inf"), "basis": "reported_observation"}, {"field": "distance", "range": [0, 2]})

    def test_injected_unique_decision_without_winner_rejected(self):
        predictions = b.predict(self.packet)
        predictions["responses"][0]["selected_candidate_code"] = None
        with self.assertRaisesRegex(ValueError, "exactly one selected survivor"):
            b.grade(self.packet, predictions, self.key, self.freeze)

    def test_injected_unique_with_multiple_survivors_rejected(self):
        predictions = b.predict(self.packet)
        predictions["responses"][0]["surviving_candidate_codes"].append("K02")
        with self.assertRaisesRegex(ValueError, "exactly one selected survivor"):
            b.grade(self.packet, predictions, self.key, self.freeze)

    def test_changed_answer_key_rejected_by_freeze(self):
        changed = deepcopy(self.key)
        changed["cases"][0]["truth"]["target_id"] = "migdal_3"
        with self.assertRaisesRegex(ValueError, "freeze manifest"):
            b.grade(self.packet, b.predict(self.packet), changed, self.freeze)

    def test_reserved_template_fails_closed(self):
        result = b.audit_reserved(b.read(b.HERE / "reserved_batch_template.json"))
        self.assertFalse(result["eligible_for_reserved_scoring"])
        self.assertIn("real_freeze_commit_required", result["issues"])

    def test_reused_observation_disqualifies_reserved_batch(self):
        manifest = {"schema": "copper-scroll-reserved-recovery-batch-v1", "coordinator_id": "curator",
                    "reviewer_ids": ["reader"], "freeze_commit": "a" * 40,
                    "frozen_before_truth_access": True,
                    "cases": [{"case_code": "C1", "reviewer_exposed_to_truth": False,
                               "prediction_sha256": "b" * 64, "selection_observation_ids": ["same-observation"],
                               "surviving_models_registered": ["M1"], "failure_rule": "wrong direction fails",
                               "truth": {"validation": "independent_reference_verified", "verified_by": "curator",
                                         "source_locator": "record/figure", "original_observation_id": "same-observation",
                                         "lineage_checked": True}}]}
        result = b.audit_reserved(manifest)
        self.assertFalse(result["eligible_for_reserved_scoring"])
        self.assertIn("C1:selection_and_truth_observation_independence_unverified", result["issues"])


if __name__ == "__main__":
    unittest.main()
