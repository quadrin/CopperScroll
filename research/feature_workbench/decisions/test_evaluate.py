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
            recorded = task.get("recorded_outcome")
            for outcome in task["outcomes"]:
                preview = evaluator.preview(task["id"], outcome["id"], REPO)
                self.assertEqual(preview["mode"], "planning_only")
                # A preview never changes current evidence. Only a task with a
                # recorded outcome carries a status other than unknown.
                self.assertEqual(preview["current_evidence"]["status"],
                                 "unknown" if recorded is None else task["current_evidence"]["status"])
                is_recorded = recorded is not None and recorded["outcome_id"] == outcome["id"]
                self.assertIs(preview["possible_outcome"]["recorded"], is_recorded)
                self.assertEqual(preview["label"], "Recorded outcome — observed" if is_recorded else "Possible outcome — not observed")
                self.assertIs(preview["research_state_changed"], False)
                self.assertEqual(preview["request_action"], "none")
                preview["current_evidence"]["status"] = "compatible"
        self.assertEqual(evaluator.build(REPO), originals)
        self.assertEqual((REPO / evaluator.QUEUE_PATH).read_bytes(), source_bytes)
        statuses = {result["id"]: result["status"] for result in originals["results"]}
        self.assertEqual(statuses.pop("decisions-kallai-pool-plan"), "contradicted")
        self.assertTrue(all(status == "unknown" for status in statuses.values()))

    def test_kallai_outcome_is_recorded_with_its_scope(self):
        task = self.tasks["decisions-kallai-pool"]
        recorded = task["recorded_outcome"]
        self.assertEqual(recorded["outcome_id"], "bearing-or-phase-miss")
        self.assertEqual(recorded["row_id"], "bearing-or-phase-miss:not-east+undated")
        self.assertEqual(recorded["excluded_classes"], {"kohlit": ["kohlit-c06", "kohlit-c07", "kohlit-c09", "kohlit-c10"]})
        self.assertEqual(task["current_evidence"]["status"], "contradicted")
        self.assertEqual([o["id"] for o in task["outcomes"] if o["recorded"]], ["bearing-or-phase-miss"])
        for path in recorded["records"]:
            self.assertTrue((REPO / path).is_file(), path)
        # The state before the pages were read is kept verbatim.
        self.assertEqual(task["history"][0]["current_evidence"]["status"], "unknown")
        self.assertIn("remain unread", task["history"][0]["current_evidence"]["detail"])
        sources = {s["id"]: s for s in self.snapshot["sources"]}
        self.assertEqual(sources["decisions-kallai-pages"]["inspection"], "already_inspected")

    def test_validation_rejects_an_unbacked_or_inconsistent_recorded_outcome(self):
        plans = json.loads((HERE / "plans.json").read_text())
        kallai = next(t for t in plans["tasks"] if t["id"] == "decisions-kallai-pool")
        next(o for o in kallai["outcomes"] if o["id"] == "identity-only")["recorded"] = True
        with self.assertRaisesRegex(ValueError, "unrecorded planning branches"):
            evaluator._validate(plans, REPO)
        plans = json.loads((HERE / "plans.json").read_text())
        kallai = next(t for t in plans["tasks"] if t["id"] == "decisions-kallai-pool")
        kallai["current_evidence"]["status"] = "unknown"
        with self.assertRaisesRegex(ValueError, "recorded outcome's status"):
            evaluator._validate(plans, REPO)
        plans = json.loads((HERE / "plans.json").read_text())
        kallai = next(t for t in plans["tasks"] if t["id"] == "decisions-kallai-pool")
        kallai["recorded_outcome"]["records"] = ["research/missing-outcome-record.json"]
        with self.assertRaisesRegex(ValueError, "Missing outcome record"):
            evaluator._validate(plans, REPO)
        plans = json.loads((HERE / "plans.json").read_text())
        kallai = next(t for t in plans["tasks"] if t["id"] == "decisions-kallai-pool")
        del kallai["recorded_outcome"]
        with self.assertRaisesRegex(ValueError, "unrecorded planning branches"):
            evaluator._validate(plans, REPO)

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

    def test_specific_l656_request_preserves_separate_inventory_and_unknown_custody(self):
        task = self.tasks["decisions-iv17-l656"]
        self.assertEqual(task["request"]["status"], "sent_pending")
        self.assertIn("11 October", task["request"]["scope"])
        self.assertIn("separate IAA regional", task["request"]["scope"])
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
