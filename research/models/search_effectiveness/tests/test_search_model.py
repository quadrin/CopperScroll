#!/usr/bin/env python3
"""Tests for the search-effectiveness layer.

Run from the repository root:
    python3 -I -m unittest discover -s research/models/search_effectiveness -t research/models/search_effectiveness
"""
import csv
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
sys.path.insert(0, str(PKG))
import search_model as sm  # noqa: E402
import run_analysis as ra  # noqa: E402

JM = sm.load_jm()


def row(**kw):
    r = dict(look_id="T", entry_id="e1", place_id="A", relation_id="R", reading_condition="",
             placement_relevant="yes", result="silent", lineage="lin", satisfies_requirement="",
             record="toy", record_key="", coverage=None, p_recognise=None, p_report=None, p_survive=None)
    r.update(kw)
    return r


S0 = {"caps": {}}


def toy_data(tmp):
    """Two entries, three places in two regions; written in the W2B input format."""
    d = Path(tmp)
    with open(d / "entries_toy.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["order", "entry", "block", "entry_confidence", "status", "title"])
        w.writerow([0, "e1", "A", "low", "possible only", "toy one"])
        w.writerow([1, "e2", "A", "low", "possible only", "toy two"])
    with open(d / "places_toy.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["place_id", "name", "lat", "lon", "sigma_km", "mixture_of", "model_region",
                    "coords_in_places_json", "precision_string", "coord_note", "components", "kind"])
        w.writerow(["A", "A", 31.80, 35.40, 0.2, "", "R1", "yes", "", "", "", "toy"])
        w.writerow(["B", "B", 31.90, 35.50, 0.2, "", "R1", "yes", "", "", "", "toy"])
        w.writerow(["C", "C", 32.00, 35.30, 0.2, "", "R2", "yes", "", "", "", "toy"])
    with open(d / "candidates_toy.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["entry", "place_id", "status", "confidence", "order_derived", "prior_override", "source",
                    "conditional_on_reading", "kohlit_proposal"])
        w.writerow(["e1", "A", "preferred", "medium", "no", "", "toy", "", "no"])
        w.writerow(["e1", "B", "possible", "low", "no", "", "toy", "", "no"])
        w.writerow(["e2", "C", "possible", "low", "no", "", "toy", "", "no"])
    with open(d / "name_groups_toy.csv", "w", newline="") as f:
        csv.writer(f).writerow(["group", "entry", "conditional_on_reading", "source"])
    return JM.Data(str(d), "toy")


class FactorTests(unittest.TestCase):
    def test_pd_formula_and_nulls(self):
        self.assertAlmostEqual(sm.row_pd(row(coverage=0.5, p_recognise=0.5, p_report=1.0, p_survive=0.8), S0), 0.2)
        # any null -> no factor
        for f in sm.NUM_FIELDS:
            r = row(coverage=1.0, p_recognise=1.0, p_report=1.0, p_survive=1.0)
            r[f] = None
            self.assertIsNone(sm.row_pd(r, S0))
        # reported rows and non-placement rows never give a factor
        self.assertIsNone(sm.row_pd(row(result="reported", coverage=1.0, p_recognise=1.0, p_report=1.0, p_survive=1.0), S0))
        self.assertIsNone(sm.row_pd(row(placement_relevant="no", coverage=1.0, p_recognise=1.0, p_report=1.0, p_survive=1.0), S0))

    def test_nulls_are_inert(self):
        rows = [row(look_id="a", coverage=None, p_recognise=1.0, p_report=1.0, p_survive=1.0),
                row(look_id="b", lineage="other", coverage=1.0, p_recognise=None, p_report=None, p_survive=None)]
        t = sm.target_factors(rows, S0, {})
        self.assertEqual(t[("e1", "A", "R")]["factor"], 1.0)
        self.assertEqual(t[("e1", "A", "R")]["used"], [])

    def test_lineage_max_and_product(self):
        same = [row(look_id="a", coverage=0.5, p_recognise=1.0, p_report=1.0, p_survive=1.0),
                row(look_id="b", coverage=0.8, p_recognise=1.0, p_report=1.0, p_survive=1.0)]
        self.assertAlmostEqual(sm.target_factors(same, S0, {})[("e1", "A", "R")]["factor"], 0.2)
        diff = [same[0], dict(same[1], lineage="other")]
        self.assertAlmostEqual(sm.target_factors(diff, S0, {})[("e1", "A", "R")]["factor"], 0.5 * 0.2)

    def test_reported_requirement_dominates_silence(self):
        rows = [row(look_id="a", coverage=1.0, p_recognise=1.0, p_report=1.0, p_survive=1.0),
                row(look_id="b", result="reported", satisfies_requirement="yes", lineage="x")]
        self.assertEqual(sm.target_factors(rows, S0, {})[("e1", "A", "R")]["factor"], 1.0)
        rows[1]["satisfies_requirement"] = "partly"
        self.assertEqual(sm.target_factors(rows, S0, {})[("e1", "A", "R")]["factor"], 0.0)

    def test_reading_gate(self):
        rows = [row(reading_condition="tel=mound", coverage=1.0, p_recognise=0.9, p_report=1.0, p_survive=1.0)]
        self.assertAlmostEqual(sm.target_factors(rows, S0, {"tel": "mound"})[("e1", "A", "R")]["factor"], 0.1)
        self.assertEqual(sm.target_factors(rows, S0, {"tel": "ruins"}), {})

    def test_scenario_caps(self):
        plan = sm.load_plan()
        sc = plan["scenarios"]
        r = row(coverage=1.0, p_recognise=0.9, p_report=1.0, p_survive=0.9)
        self.assertAlmostEqual(sm.row_pd(r, sc["S0"]), 0.81)
        self.assertAlmostEqual(sm.row_pd(r, sc["S1"]), 0.9 * sc["S1"]["caps"]["p_survive"]["value"])
        self.assertAlmostEqual(sm.row_pd(r, sc["S2"]), 0.9 * sc["S2"]["caps"]["p_recognise"]["value"])
        self.assertAlmostEqual(sm.row_pd(r, sc["S3"]), 0.81 * sc["S3"]["caps"]["p_report"]["value"])
        self.assertAlmostEqual(sm.row_pd(dict(r, result="explicit_absence"), sc["S3"]), 0.81)  # S3 is for silences
        self.assertEqual(sm.row_pd(r, sc["S4"]), 0.0)


class ToyModelTests(unittest.TestCase):
    def test_pd_09_cuts_single_place_odds_tenfold(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = toy_data(tmp)
            m = JM.Model(data, JM.cfg_with(w_A=0.0, w_L=0.0, rho=0.0))
            base = m.run()["post"][0]
            rows = [row(coverage=0.9, p_recognise=1.0, p_report=1.0, p_survive=1.0)]
            t = sm.target_factors(rows, S0, {})
            post = sm.run(m, sm.entry_vectors(m, t))["post"]
            k = m.idx["A"]
            odds = lambda p: p[k] / (1 - p[k])
            self.assertAlmostEqual(odds(post[0]) / odds(base), 0.1, places=12)
            # the other, independent entry is untouched
            np.testing.assert_allclose(post[1], m.run()["post"][1], rtol=0, atol=1e-15)


class W2BReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = JM.Data(str(sm.INPUTS), "v1")
        cls.model = JM.Model(cls.data, JM.cfg_with())
        cls.ref = cls.model.run()

    def assert_same(self, res):
        self.assertTrue(np.array_equal(res["post"], self.ref["post"]))
        self.assertEqual(res["logml"], self.ref["logml"])

    def test_default_is_K2(self):
        self.assertEqual(self.model.c["transition"], "fixed")

    def test_factor_one_reproduces_model_exactly(self):
        ones = {e: np.ones(self.model.S) for e in self.data.order}
        self.assert_same(sm.run(self.model, ones, force_override=True))
        self.assert_same(sm.run(self.model, {}, force_override=True))

    def test_S4_and_null_looks_reproduce_model(self):
        plan = sm.load_plan()
        looks = sm.load_looks()
        rset = plan["reading_sets"][plan["main_reading_set"]]
        t = sm.target_factors(looks, plan["scenarios"]["S4"], rset)
        self.assertTrue(all(v["factor"] == 1.0 for v in t.values()))
        self.assert_same(sm.run(self.model, sm.entry_vectors(self.model, t), force_override=True))
        nulled = [dict(r, coverage=None) for r in looks]
        t2 = sm.target_factors(nulled, plan["scenarios"]["S0"], rset)
        self.assertEqual(sm.entry_vectors(self.model, t2), {})
        self.assert_same(sm.run(self.model, sm.entry_vectors(self.model, t2)))

    def test_matches_recorded_W2B_K2_run(self):
        # outputs_fixed/kernel_sensitivity.csv: v1 inputs, fixed, no grid, rho .9, w_A .4, w_L .995
        rows = sm.load_csv(sm.W2B / "outputs_fixed" / "kernel_sensitivity.csv")
        ref = [r for r in rows if r["inputs"] == "v1" and r["transition"] == "fixed" and r["grid_km"] == "0"
               and float(r["rho"]) == 0.9 and float(r["w_A"]) == 0.4 and float(r["w_L"]) == 0.995
               and r["excluded"] == ""]
        self.assertEqual(len(ref), 1)
        res = sm.run(self.model, {}, force_override=True)
        p60 = res["post"][self.data.order.index("60")][self.model.idx["tell_es_sultan"]]
        self.assertAlmostEqual(p60, float(ref[0]["P_tell_es_sultan"]), places=12)
        self.assertAlmostEqual(res["logml"], float(ref[0]["logml"]), places=10)

    def test_looks_table_is_valid(self):
        sm.validate_looks(sm.load_looks(), set(self.data.order), set(self.model.states))
        for n in sm.load_csv(sm.NEXT):
            self.assertIn(n["entry_id"], self.data.order)
            self.assertIn(n["place_id"], self.model.states)


class FreezeTests(unittest.TestCase):
    def test_frozen_hashes(self):
        plan = sm.load_plan()
        self.assertEqual(plan["frozen_inputs_sha256"]["looks.csv"], sm.sha256(sm.LOOKS))
        self.assertEqual(plan["frozen_inputs_sha256"]["next_records.csv"], sm.sha256(sm.NEXT))
        readme = (PKG / "README.md").read_text(encoding="utf-8")
        m = re.search(r"PLAN\.md SHA-256: `([0-9a-f]{64})`", readme)
        self.assertIsNotNone(m, "README must record the PLAN.md hash")
        self.assertEqual(m.group(1), sm.sha256(sm.PLAN))


class DeterminismTests(unittest.TestCase):
    def test_analysis_is_deterministic_and_matches_results_json(self):
        plan = sm.load_plan()
        a = json.dumps(ra.analyse(plan), sort_keys=True, ensure_ascii=False)
        b = json.dumps(ra.analyse(plan), sort_keys=True, ensure_ascii=False)
        self.assertEqual(a, b)
        stored = PKG / "results.json"
        if stored.exists():
            self.assertEqual(json.loads(a), json.loads(stored.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
