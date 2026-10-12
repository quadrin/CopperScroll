"""Synthetic fixtures test arithmetic/gates; they supply no manuscript evidence."""
import copy
import tempfile
import unittest
from pathlib import Path

from letter_controls import eligibility, native_roi_valid, packet, score, load


def fixture_item(code="F01", label="ב"):
    return {"code": code, "kind": "control", "synthetic": True,
            "substrate": "original", "source_bytes_verified": True,
            "original_locus_authenticated": True, "neighboring_original_hebrew": "synthetic anchor",
            "native_roi": [1, 1, 5, 5], "width_px": 10, "height_px": 10,
            "glyph_id": "synthetic-glyph-" + code, "observation_lineage": "synthetic-capture",
            "reuse_authorized": True, "damage_comparability_reviewed": True,
            "local_comparator_inventory_complete": True, "project_exposure_status": "exposed",
            "truth": {"value": label, "basis": "independent_original_reading", "certain": True,
                      "original_anchor": "synthetic anchor, no real metal", "established_before_scoring": True,
                      "independent_of_scoring_readers": True}}


def fixture_reader(reader_id="SYNTHETIC_A", independent_of=None):
    return {"reader_id": reader_id, "synthetic": True, "independent_human": True,
            "epigraphic_experience_recorded": True, "independent_of": independent_of or []}


def fixture_response(code, reader_id="SYNTHETIC_A", decision="read", label="ב"):
    return {"code": code, "reader_id": reader_id, "synthetic": True,
            "decision": decision, "label": label if decision == "read" else None,
            "grade": "certain" if decision == "read" else "illegible", "stage": 1,
            "locked_before_stage2": True, "locked_at_utc": "synthetic-time",
            "recognized": False, "prior_exposure": False, "prior_exposure_audited": True}


def pilot():
    items = [fixture_item("F01", "ב"), fixture_item("F02", "כ"),
             fixture_item("F03", "ה"), fixture_item("F04", "ח"), fixture_item("F05", "ת")]
    a = "SYNTHETIC_A"; b = "SYNTHETIC_B"
    readers = [fixture_reader(a, [b]), fixture_reader(b, [a])]
    responses = [fixture_response("F01", a, label="ב"), fixture_response("F02", a, label="ב"),
                 fixture_response("F03", a, decision="abstain"), fixture_response("F04", a, decision="unknown"),
                 fixture_response("F01", b, label="כ"), fixture_response("F02", b, label="כ"),
                 fixture_response("F03", b, label="ה"), fixture_response("F04", b, decision="unknown")]
    data = {"mode": "synthetic_software_pilot", "items": items, "readers": readers, "responses": responses,
            "notice": "Fabricated software fixtures. All authentication/human flags simulate inputs; no real source or human supplied them."}
    return data, score(items, responses, readers, data["mode"])


class Tests(unittest.TestCase):
    def test_absent_anchor_and_edition_truth_fail(self):
        item = fixture_item()
        item["neighboring_original_hebrew"] = None
        item["truth"]["basis"] = "edition_transcription"
        q = eligibility(item)
        self.assertFalse(q["eligible_for_empirical_accuracy"])
        self.assertIn("neighboring original Hebrew anchors", q["gaps"])
        self.assertIn("independently established certain truth with original anchor", q["gaps"])

    def test_replica_and_uncertain_truth_fail(self):
        item = fixture_item(); item["substrate"] = "replica"; item["truth"]["certain"] = False
        self.assertFalse(eligibility(item)["eligible_for_empirical_accuracy"])

    def test_rescan_exposed_scope(self):
        item = fixture_item()
        q = eligibility(item)
        self.assertTrue(q["eligible_for_empirical_accuracy"])
        self.assertFalse(q["eligible_for_confirmatory_accuracy"])
        item["project_exposure_status"] = "unused_status_unverified"
        self.assertFalse(eligibility(item)["eligible_for_empirical_accuracy"])

    def test_roi_rejects_nan_bool_outside(self):
        for roi in ([0, 0, float("nan"), 4], [False, 0, 4, 4], [0, 0, 11, 4], [5, 0, 4, 4]):
            self.assertFalse(native_roi_valid(roi, 10, 10))

    def test_abstentions_unknowns_missing_and_confusion(self):
        _, result = pilot(); a, b = result["reader_results"]
        self.assertFalse(result["empirical_accuracy_obtained"])
        self.assertEqual(a["correct"], 1)
        self.assertEqual(a["scorable_locked_responses"], 4)
        self.assertEqual(a["accuracy_including_abstentions"], .25)
        self.assertEqual(a["accuracy_when_answered"], .5)
        self.assertEqual(a["response_completeness"], .8)
        self.assertEqual(a["missing_responses"], ["F05"])
        self.assertEqual(a["abstentions"], 1); self.assertEqual(a["unknown_answers"], 1)
        self.assertIn({"truth": "כ", "answer": "ב", "count": 1}, a["confusion_matrix"])
        self.assertEqual(b["correct"], 2)
        self.assertEqual(sum(not x["same_answer"] for x in result["independent_reader_comparisons"]), 3)

    def test_synthetic_cannot_be_empirical(self):
        data, _ = pilot()
        with self.assertRaisesRegex(ValueError, "Synthetic"):
            score(data["items"], data["responses"], data["readers"])

    def test_unknown_truth_excluded_with_response_preserved(self):
        item = fixture_item(); item["truth"] = None
        result = score([item], [fixture_response("F01")], [fixture_reader()], "synthetic_software_pilot")
        r = result["reader_results"][0]
        self.assertIsNone(r["accuracy_including_abstentions"])
        self.assertEqual(len(r["excluded_control_responses"]), 1)

    def test_recognition_excluded_exposure_unknown_excluded(self):
        responses = [fixture_response("F01"), fixture_response("F02")]
        responses[0]["recognized"] = True; responses[1]["prior_exposure"] = None
        result = score([fixture_item("F01"), fixture_item("F02")], responses, [fixture_reader()], "synthetic_software_pilot")
        r = result["reader_results"][0]
        self.assertEqual(r["scorable_locked_responses"], 0)
        self.assertEqual(r["response_completeness"], 1)
        self.assertEqual(len(r["excluded_control_responses"]), 2)

    def test_model_reader_cannot_supply_human_accuracy(self):
        reader = fixture_reader(); reader["independent_human"] = False
        result = score([fixture_item()], [fixture_response("F01")], [reader], "synthetic_software_pilot")
        r = result["reader_results"][0]
        self.assertEqual(r["scorable_locked_responses"], 0)
        self.assertIn("independent qualified human reader", r["excluded_control_responses"][0]["reasons"])

    def test_duplicate_glyph_and_response_rejected(self):
        a, b = fixture_item("F01"), fixture_item("F02")
        b["glyph_id"] = a["glyph_id"]
        with self.assertRaisesRegex(ValueError, "same physical glyph"):
            score([a, b], [], [], "synthetic_software_pilot")
        r = fixture_response("F01")
        with self.assertRaisesRegex(ValueError, "Duplicate initial"):
            score([a], [r, r], [fixture_reader()], "synthetic_software_pilot")

    def test_stage_two_or_unlocked_answer_rejected(self):
        for update in ({"stage": 2}, {"locked_before_stage2": False}, {"locked_at_utc": None}):
            r = fixture_response("F01"); r.update(update)
            with self.assertRaisesRegex(ValueError, "Stage 1"):
                score([fixture_item()], [r], [fixture_reader()], "synthetic_software_pilot")

    def test_grade_decision_and_hidden_label_rejected(self):
        for update in ({"grade": "confident"}, {"decision": "guess"}, {"decision": "abstain", "label": "ב"}):
            r = fixture_response("F01"); r.update(update)
            with self.assertRaises(ValueError):
                score([fixture_item()], [r], [fixture_reader()], "synthetic_software_pilot")

    def test_targets_have_no_accuracy(self):
        item = fixture_item(); item["kind"] = "target"
        result = score([item], [fixture_response("F01")], [fixture_reader()], "synthetic_software_pilot")
        self.assertEqual(len(result["reader_results"][0]["unscored_target_responses"]), 1)
        self.assertIsNone(result["reader_results"][0]["accuracy_including_abstentions"])

    def test_packet_separation_determinism_and_no_overwrite(self):
        data = {"inputs": {}, "original_frame_candidates": [],
                "locus_records": [{"locus": x, "status": "unregistered"} for x in ["VII 11", "IX 7", "X 15", "X 16", "XII 10"]]}
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a", Path(d) / "b"
            packet(data, a); packet(data, b)
            self.assertEqual((a / "coordinator/source_key.json").read_bytes(), (b / "coordinator/source_key.json").read_bytes())
            self.assertFalse(load(a / "coordinator/readiness.json")["ready"])
            public = (a / "reviewer/items.json").read_text()
            self.assertNotIn("XII", public); self.assertNotIn("truth", public); self.assertNotIn("target_loci", public)
            with self.assertRaises(ValueError):
                packet(data, a)


if __name__ == "__main__":
    unittest.main()
