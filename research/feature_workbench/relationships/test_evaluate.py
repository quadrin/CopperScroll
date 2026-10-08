"""Regression checks for archaeological unknowns and finite branch accounting."""
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("relationships_evaluate", HERE / "evaluate.py")
EVAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVAL)


class RelationshipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = json.loads((HERE / "model.json").read_text(encoding="utf-8"))
        cls.module = EVAL.build(HERE.parents[2])
        cls.results = {r["id"]: r for r in cls.module["results"]}

    def predicate(self, id):
        return next(p for p in self.model["predicates"] if p["id"] == id)

    def assignment(self, id):
        return next(a for a in self.model["assignments"] if a["id"] == id)

    def check(self, assignment, predicate, window=0):
        return EVAL.evaluate_predicate(self.predicate(predicate), self.assignment(assignment), self.model["windows"][window], self.model)

    def test_every_permitted_combination_is_returned(self):
        expected = {
            (a["id"], reading, w["id"])
            for a in self.model["assignments"]
            for reading in a["reading_ids"] for w in self.model["windows"]
        }
        actual = {(b["assignment_id"], b["reading_id"], b["window_id"]) for b in self.module["data"]["branches"]}
        self.assertEqual(expected, actual)
        self.assertEqual(40, len(actual))
        self.assertEqual(len(expected), len(self.module["data"]["branches"]))

    def test_modern_reservoir_fails_both_early_windows(self):
        for window in (0, 1):
            check = self.check("jericho-modern-ns1", "pool-period", window)
            self.assertEqual("contradicted", check["status"])
            self.assertIn("1898", check["detail"])

    def test_historical_basin_is_not_backdated(self):
        self.assertEqual("compatible", self.check("jericho-historical-ns1", "pool-east")["status"])
        self.assertEqual("unknown", self.check("jericho-historical-ns1", "pool-period")["status"])
        self.assertEqual("unknown", self.check("jericho-historical-ns1", "pool-north-corner")["status"])

    def test_unlocated_pool_is_unknown_not_miss(self):
        for predicate in ("pool-east", "pool-period"):
            self.assertEqual("unknown", self.check("samiya-kallai", predicate)["status"])

    def test_southwest_crypt_assignment_is_retained_as_miss(self):
        check = self.check("samiya-crypt", "pool-east")
        self.assertEqual("contradicted", check["status"])
        self.assertIn("separate pool", check["detail"])
        self.assertEqual("unknown", self.check("samiya-crypt", "pool-period")["status"])

    def test_graves_in_northern_sector_do_not_supply_mouth_join(self):
        for assignment in ("jericho-historical-ns1", "jericho-d9", "jericho-quarry"):
            self.assertEqual("compatible", self.check(assignment, "pit-north")["status"])
            self.assertEqual("unknown", self.check(assignment, "graves-at-mouth")["status"])

    def test_later_phase_does_not_imply_later_than_135(self):
        for window in (0, 1):
            self.assertEqual("unknown", self.check("jericho-quarry", "pit-period", window)["status"])
            self.assertEqual("unknown", self.check("jericho-quarry", "joint-accessibility", window)["status"])
        self.assertEqual("contradicted", self.check("jericho-quarry", "same-construction-phase")["status"])

    def test_reading_branches_do_not_exchange_opening_requirements(self):
        readings = {r["id"]: set(r["predicate_ids"]) for r in self.model["readings"]}
        self.assertIn("opening-north", readings["RB-M"])
        self.assertNotIn("opening-concealed", readings["RB-M"])
        self.assertIn("opening-concealed", readings["RB-P"])
        self.assertNotIn("opening-north", readings["RB-P"])
        self.assertNotIn("graves-at-mouth", readings["RB-B"])
        self.assertNotIn("joint-accessibility", readings["RB-B"])

    def test_yanun_keeps_missing_pit_separate_from_kohlit_anchor(self):
        for assignment in ("yanun-jericho-anchor", "yanun-marjama-anchor"):
            self.assertEqual(["RB-L"], self.assignment(assignment)["reading_ids"])
            check = self.check(assignment, "pit-at-yanun")
            self.assertEqual("unknown", check["status"])
            self.assertIsNone(check["value"]["resolved_subject"])
            self.assertEqual("yanun-site", check["value"]["resolved_object"])

    def test_no_complete_branch_claims_a_match(self):
        statuses = [self.results[b["result_id"]]["status"] for b in self.module["data"]["branches"]]
        self.assertEqual(12, statuses.count("contradicted"))
        self.assertEqual(28, statuses.count("unknown"))
        self.assertNotIn("compatible", statuses)
        self.assertIsNone(self.module["data"]["regional_denominator"])
        self.assertIsNone(self.module["data"]["unused_prediction"])

    def test_conflicting_source_facts_are_visible(self):
        model = json.loads(json.dumps(self.model))
        observed = next(o for o in model["observations"] if o["id"] == "relationships-historical-east")
        conflicting = json.loads(json.dumps(observed))
        conflicting["id"] = "relationships-conflict-fixture"
        conflicting["value"]["asserted"] = False
        conflicting["note"] = "Synthetic contrary observation for this test only."
        model["observations"].append(conflicting)
        check = EVAL.evaluate_predicate(self.predicate("pool-east"), self.assignment("jericho-historical-ns1"), model["windows"][0], model)
        self.assertEqual("mixed", check["status"])
        self.assertIn("relationships-conflict-fixture", check["value"]["observation_ids"])

    def test_actual_dated_accessible_interval_can_resolve_phase(self):
        model = json.loads(json.dumps(self.model))
        chronology = next(o for o in model["observations"] if o["id"] == "relationships-historical-basin-chronology")
        chronology["value"]["dated_accessible_interval"] = [-10, 30]
        chronology["note"] = "Synthetic dated-use fixture; not project evidence."
        check = EVAL.evaluate_predicate(self.predicate("pool-period"), self.assignment("jericho-historical-ns1"), model["windows"][0], model)
        self.assertEqual("compatible", check["status"])
        chronology["value"]["dated_accessible_interval"] = [200, 250]
        check = EVAL.evaluate_predicate(self.predicate("pool-period"), self.assignment("jericho-historical-ns1"), model["windows"][0], model)
        self.assertEqual("unknown", check["status"])
        chronology["value"]["accessible_interval_exhaustive"] = True
        check = EVAL.evaluate_predicate(self.predicate("pool-period"), self.assignment("jericho-historical-ns1"), model["windows"][0], model)
        self.assertEqual("contradicted", check["status"])

    def test_undated_coexistence_cannot_supply_early_joint_use(self):
        model = json.loads(json.dumps(self.model))
        relation = next(o for o in model["observations"] if o["id"] == "relationships-quarries-co-use")
        relation["value"]["asserted"] = True
        check = EVAL.evaluate_predicate(self.predicate("joint-accessibility"), self.assignment("jericho-quarry"), model["windows"][0], model)
        self.assertEqual("unknown", check["status"])
        relation["value"]["dated_joint_accessible_interval"] = [30, 50]
        check = EVAL.evaluate_predicate(self.predicate("joint-accessibility"), self.assignment("jericho-quarry"), model["windows"][0], model)
        self.assertEqual("compatible", check["status"])

    def test_result_pointers_and_evidence_lineages_are_not_confidence(self):
        sources = {s["id"] for s in self.module["sources"]}
        observations = {o["id"] for o in self.module["observations"]}
        campaigns = {s["id"]: s.get("original_campaign") for s in self.module["sources"]}
        self.assertEqual(campaigns["relationships-kenyon-II"], campaigns["relationships-kenyon-III"])
        for result in self.module["results"]:
            self.assertNotIn("confidence", result)
            self.assertTrue(set(result["source_ids"]) <= sources)
            for check in result["checks"]:
                self.assertIn(check["status"], EVAL.STATUSES)
                self.assertTrue(set(check["value"]["observation_ids"]) <= observations)
        for branch in self.module["data"]["branches"]:
            self.assertEqual(set(branch["check_ids"]), {c["id"] for c in self.results[branch["result_id"]]["checks"]})


if __name__ == "__main__":
    unittest.main()
