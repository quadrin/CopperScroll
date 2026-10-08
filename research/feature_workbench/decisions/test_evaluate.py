"""Check that planning branches cannot turn into findings or outreach."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SPEC = importlib.util.spec_from_file_location("decision_evaluator", HERE / "evaluate.py")
evaluator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(evaluator)


class DecisionQueueTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = evaluator.build(REPO)
        self.tasks = {task["id"]: task for task in self.snapshot["data"]["tasks"]}

    def test_all_six_historical_tracks_imported_without_status_changes(self):
        original_bytes = (REPO / evaluator.QUEUE_PATH).read_bytes()
        original = json.loads(original_bytes)
        imported = self.snapshot["data"]["historical_queue"]
        self.assertEqual(imported["tracks"], original["tracks"])
        self.assertEqual(len(imported["tracks"]), 6)
        self.assertEqual(imported["sha256"], hashlib.sha256(original_bytes).hexdigest())
        self.assertEqual(imported["counts_as_recorded"], original["counts"])
        self.assertIn("parked", imported["tracks"][2]["next_action"])
        self.assertIn("parked", imported["tracks"][4]["next_action"])

    def test_possible_support_does_not_replace_unknown_evidence(self):
        originals = copy.deepcopy(self.snapshot)
        source_bytes = (REPO / evaluator.QUEUE_PATH).read_bytes()
        for task in self.tasks.values():
            for outcome in task["outcomes"]:
                preview = evaluator.preview(task["id"], outcome["id"], REPO)
                self.assertEqual(preview["mode"], "planning_only")
                self.assertEqual(preview["current_evidence"]["status"], "unknown")
                self.assertIs(preview["possible_outcome"]["recorded"], False)
                self.assertIs(preview["research_state_changed"], False)
                self.assertEqual(preview["request_action"], "none")
                preview["current_evidence"]["status"] = "compatible"
        self.assertEqual(evaluator.build(REPO), originals)
        self.assertEqual((REPO / evaluator.QUEUE_PATH).read_bytes(), source_bytes)
        self.assertTrue(all(result["status"] == "unknown" for result in originals["results"]))

    def test_each_task_retains_inconclusive_and_claim_scoped_outcomes(self):
        self.assertEqual(len(self.tasks), 7)
        self.assertEqual(sum(len(t["outcomes"]) for t in self.tasks.values()), 28)
        for task in self.tasks.values():
            self.assertTrue(any(o["status"] == "unknown" for o in task["outcomes"]))
            for outcome in task["outcomes"]:
                self.assertTrue(outcome["condition"])
                self.assertTrue(outcome["claim_scope"])
                self.assertTrue(outcome["remaining_unknowns"])
            self.assertEqual(task["freeze"]["unused_status"], "unverified")

    def test_exact_reading_freeze_does_not_certify_an_unused_image(self):
        task = self.tasks["decisions-xii10"]
        self.assertEqual(task["freeze"]["commit"], "fd3f334ea2a40c0f8e99921ef663f8b126112fe1")
        self.assertEqual([r["id"] for r in task["registered_readings"]], [f"R{i}" for i in range(1, 8)])
        self.assertEqual([r["sequence"] for r in task["registered_readings"]],
                         ["שכנה", "שבנה", "שבצח", "שבינח", "שכינה", "שכונה", "שבצהב"])
        self.assertEqual(task["cut_letter_candidates"], ["ה", "ח", "ת", "unresolved"])
        self.assertEqual(task["freeze"]["unused_status"], "unverified")
        self.assertEqual(task["request"]["status"], "sent_pending")

    def test_generic_iaa_request_not_relabelled_as_l656_request(self):
        task = self.tasks["decisions-iv17-l656"]
        self.assertEqual(task["request"]["status"], "related_request_pending")
        self.assertIn("not a verified request", task["request"]["scope"])
        self.assertIs(task["access"]["custody_verified"], False)
        sources = {s["id"]: s for s in self.snapshot["sources"]}
        self.assertEqual(sources["decisions-iv17-unread-file"]["inspection"], "not_inspected")
        self.assertEqual(sources["decisions-kallai-unread"]["inspection"], "not_inspected")
        self.assertEqual(sources["decisions-kenyon-unread-plates"]["inspection"], "not_inspected")

    def test_sent_request_status_matches_current_structured_source(self):
        siloam = json.loads((REPO / "research/measurements/cycle15/siloam_bathing.json").read_text())
        wadi = json.loads((REPO / "research/assessments/entry29_jericho_pools/wadi_en_nueima_original_2026-10-06.json").read_text())
        self.assertTrue(siloam["survey_request_sending"]["sent"])
        self.assertEqual(siloam["survey_request_sending"]["status"], "sent")
        self.assertIsNone(siloam["survey_request_sending"]["delivery"])
        self.assertIsNone(siloam["survey_request_sending"]["reply"])
        self.assertTrue(wadi["archive_referral_sent_2026_10_06"]["stored_message_recipient_subject_body_verified"])
        self.assertFalse(wadi["archive_referral_sent_2026_10_06"]["delivery_verified"])
        self.assertIsNone(wadi["archive_referral_sent_2026_10_06"]["reply_received"])
        for task_id in ("decisions-siloam-main-side", "decisions-wadi-bath-contact"):
            self.assertEqual(self.tasks[task_id]["request"]["status"], "sent_pending")
            self.assertEqual(self.tasks[task_id]["request"]["delivery"], "unverified")
            self.assertEqual(self.tasks[task_id]["request"]["reply"], "unverified")

    def test_validation_rejects_promoting_a_possible_outcome(self):
        plans = json.loads((HERE / "plans.json").read_text())
        plans["tasks"][0]["outcomes"][0]["recorded"] = True
        with self.assertRaisesRegex(ValueError, "unrecorded planning branches"):
            evaluator._validate(plans, REPO)

    def test_validation_requires_inconclusive_and_valid_feature_refs(self):
        plans = json.loads((HERE / "plans.json").read_text())
        plans["tasks"][0]["outcomes"] = [o for o in plans["tasks"][0]["outcomes"] if o["status"] != "unknown"]
        with self.assertRaisesRegex(ValueError, "inconclusive"):
            evaluator._validate(plans, REPO)
        plans = json.loads((HERE / "plans.json").read_text())
        plans["tasks"][0]["feature_ids"] = ["invented-mouth"]
        with self.assertRaisesRegex(ValueError, "Unknown feature"):
            evaluator._validate(plans, REPO)

    def test_unknown_task_or_outcome_is_not_silently_defaulted(self):
        with self.assertRaisesRegex(ValueError, "Unknown decision task"):
            evaluator.preview("missing-task", "one-sequence", REPO)
        with self.assertRaisesRegex(ValueError, "Unknown outcome"):
            evaluator.preview("decisions-xii10", "missing-outcome", REPO)


if __name__ == "__main__":
    unittest.main()
