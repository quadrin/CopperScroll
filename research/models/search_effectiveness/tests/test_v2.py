#!/usr/bin/env python3
"""Tests for the v2 candidates run (two new W2B candidates: entry 60 at kh_qumran, entry 25 at IV/17).

Run from the repository root (about one minute):
    python3 -I -B -m unittest discover -s research/models/search_effectiveness -t research/models/search_effectiveness -p 'test_v2.py'
"""
import csv
import importlib.util
import io
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
sys.dont_write_bytecode = True
import run_v2 as rv  # noqa: E402
import build_looks_v2 as bl  # noqa: E402
import search_model as sm  # noqa: E402

JM = rv.JM


def load_build():
    spec = importlib.util.spec_from_file_location("build_inputs_v2", str(rv.IN_V2 / "build_inputs_v2.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BUILD = load_build()
ADDITIONS = json.loads((rv.IN_V2 / "additions_v2.json").read_text(encoding="utf-8"))
RESULTS_V2 = json.loads(rv.RESULTS_V2.read_text(encoding="utf-8")) if rv.RESULTS_V2.exists() else None


def rows_of(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))


def has_pyproj():
    try:
        import pyproj  # noqa: F401
        return True
    except ImportError:
        return False


class InputsV2Tests(unittest.TestCase):
    """v2 inputs = v1 inputs plus exactly the declared rows."""

    PAIRS = {"entries_v2.csv": "entries_v1.csv", "name_groups_v2.csv": "name_groups_v1.csv",
             "kohlit_proposals_v2.csv": "kohlit_proposals_v1.csv", "places_v2.csv": "places_v1.csv",
             "candidates_v2.csv": "candidates_v1.csv", "grid_conversions_v2.csv": "grid_conversions.csv"}

    def test_v2_is_v1_bytes_plus_declared_rows(self):
        declared = ADDITIONS["declared_rows"]
        for v2, v1 in self.PAIRS.items():
            a = (rv.IN_V1 / v1).read_bytes()
            b = (rv.IN_V2 / v2).read_bytes()
            self.assertTrue(b.startswith(a), f"{v2} does not start with the bytes of {v1}")
            ra_, rb = rows_of(a), rows_of(b)
            self.assertEqual(rb[:len(ra_)], ra_)
            self.assertEqual(rb[len(ra_):], declared.get(v2, []), f"{v2}: extra rows differ from the declared rows")
        self.assertEqual(sorted(declared), ["candidates_v2.csv", "grid_conversions_v2.csv", "places_v2.csv"])
        self.assertEqual(len(declared["candidates_v2.csv"]), 2)
        self.assertEqual(len(declared["places_v2.csv"]), 1)

    def test_declared_rows_are_the_frozen_choices(self):
        cands = {(r["entry"], r["place_id"]): r for r in ADDITIONS["declared_rows"]["candidates_v2.csv"]}
        self.assertEqual(set(cands), {("60", "kh_qumran"), ("25", "iv17_abu_saraj")})
        plan = rv.load_plan_v2()
        for key_s, steps in plan["label_steps"].items():
            e, p = key_s.split("|")
            self.assertEqual([cands[(e, p)]["status"], cands[(e, p)]["confidence"]], steps["main"])
        q, c = cands[("60", "kh_qumran")], cands[("25", "iv17_abu_saraj")]
        self.assertEqual((q["order_derived"], q["conditional_on_reading"], q["kohlit_proposal"]), ("no", "xii10!=janoah", "no"))
        self.assertEqual((c["order_derived"], c["conditional_on_reading"], c["kohlit_proposal"]), ("no", "", "no"))
        self.assertIn("not a published Kohlit proposal", q["source"])
        place = ADDITIONS["declared_rows"]["places_v2.csv"][0]
        self.assertEqual((place["place_id"], place["model_region"], float(place["sigma_km"])),
                         ("iv17_abu_saraj", "JERICHO", plan["sigma_km"]["main"]))
        self.assertEqual(ADDITIONS["conversion"]["iv17_group_oig"], [190300, 144150])
        self.assertLess(ADDITIONS["conversion"]["controls"][0]["difference_km"], 0.2)
        self.assertTrue(all(r["equal"] for r in ADDITIONS["conversion"]["reproduces_w2b_grid_conversions"]))

    def test_additions_record_matches_files(self):
        for v2, info in ADDITIONS["files"].items():
            self.assertEqual(rv.sha256(rv.IN_V2 / v2), info["v2_sha256"], v2)
            self.assertEqual(rv.sha256(rv.IN_V1 / info["from_v1"]), info["v1_sha256"], info["from_v1"])

    @unittest.skipUnless(has_pyproj(), "pyproj (W2B grid_convert.py dependency) not installed")
    def test_fresh_build_matches_files(self):
        for name, b in BUILD.build().items():
            self.assertEqual((rv.IN_V2 / name).read_bytes(), b, name)

    def test_looks_v2_changes_only_the_iv17_place(self):
        a = sm.load_csv(sm.LOOKS)
        b = sm.load_csv(rv.LOOKS_V2)
        self.assertEqual(len(a), len(b))
        self.assertEqual(rv.LOOKS_V2.read_bytes(), bl.build())
        for r, s in zip(a, b):
            diff = {k for k in r if r[k] != s[k]}
            if r["look_id"] in ("L43", "L44"):
                self.assertEqual(diff, {"place_id"})
                self.assertEqual((r["place_id"], s["place_id"]), ("U_JERICHO", "iv17_abu_saraj"))
            else:
                self.assertEqual(diff, set(), r["look_id"])

    def test_plan_v2_freeze(self):
        plan = rv.load_plan_v2()
        rv.check_frozen_v2(plan)  # raises on any change
        readme = (PKG / "README_v2.md").read_text(encoding="utf-8")
        m = re.search(r"PLAN_v2\.md SHA-256: `([0-9a-f]{64})`", readme)
        self.assertIsNotNone(m, "README_v2 must record the PLAN_v2.md hash")
        self.assertEqual(m.group(1), rv.sha256(rv.PLAN_V2))

    def test_loader_uses_the_rows_as_declared(self):
        d = rv.load_data(rv.IN_V2, "v2")
        m = JM.Model(d, JM.cfg_with())
        ev = m.evidence(d.order)
        P0 = {e: ev[e][1] for e in ("25", "60")}
        # entry 60: eleven candidates with equal odds 1/9 -> each 0.05 a priori
        self.assertAlmostEqual(P0["60"][m.idx["kh_qumran"]], P0["60"][m.idx["tell_es_sultan"]], places=15)
        self.assertAlmostEqual(P0["60"][m.idx["kh_qumran"]], (1 / 9) / (1 + 11 / 9), places=12)
        # entry 25: two candidates with equal odds 3/7
        self.assertAlmostEqual(P0["25"][m.idx["iv17_abu_saraj"]], P0["25"][m.idx["kh_qumran"]], places=15)
        # Janoah reading switches the entry-60 Qumran row off with the ten proposals
        mj = JM.Model(d, JM.cfg_with(readings=dict(kohlit15=True, solomon23=True, xii10="janoah")))
        evj = mj.evidence(d.order)
        self.assertEqual([mj.states[k] for k in evj["60"][2]], ["kh_yanun"])
        # kohlit_proposal = no: a Kohlit odds scheme without kh_qumran does not drop the row
        mk = JM.Model(d, JM.cfg_with(kohlit_scheme={"tell_es_sultan": 0.3 / 0.7}))
        self.assertIn(mk.idx["kh_qumran"], mk.evidence(d.order)["60"][2])
        # order_derived = no: excluding documented and likely rows keeps both new rows
        mx = JM.Model(d, JM.cfg_with(exclude_order_derived=("documented", "likely")))
        evx = mx.evidence(d.order)
        self.assertIn(mx.idx["iv17_abu_saraj"], evx["25"][2])
        self.assertNotIn(mx.idx["kh_qumran"], evx["25"][2])
        self.assertIn(mx.idx["kh_qumran"], evx["60"][2])


class ReproductionTests(unittest.TestCase):
    """The v2 runner, fed the unchanged v1 inputs, reproduces outputs_fixed/ and results.json."""

    def test_kernel_rows_reproduce_outputs_fixed(self):
        rows = rv.kernel_rows(rv.IN_V1, "v0") + rv.kernel_rows(rv.IN_V1, "v1")
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "kernel_sensitivity.csv"
            JM.write_csv(p, rows)
            cmp = rv.compare_kernel_csv(rv.OUT_FIXED / "kernel_sensitivity.csv", p)
            committed = (rv.OUT_V2 / "repro_v1" / "kernel_sensitivity.csv").read_bytes()
            same_as_committed = p.read_bytes() == committed
        self.assertTrue(cmp["structure_equal"])
        self.assertEqual(cmp["rows"], 30)
        self.assertLessEqual(cmp["max_abs_diff"], 1e-12)  # round-off only (see README_v2, R0)
        if not same_as_committed:  # another BLAS may round differently; then only the tolerance applies
            print("note: kernel_sensitivity bytes differ from outputs_v2/repro_v1 on this machine", file=sys.stderr)

    def test_v0_check_is_byte_equal(self):
        self.assertEqual(rv.v0_check_text(rv.IN_V1), (rv.OUT_FIXED / "v0_reproduction_check.json").read_text())

    def test_layer_wrapper_reproduces_results_json(self):
        a = rv.layer_analyse(rv.IN_V1, "v1", sm.LOOKS)
        b = json.loads((PKG / "results.json").read_text(encoding="utf-8"))
        self.assertEqual(json.loads(json.dumps(a)), b)

    def test_w2b_and_layer_code_unchanged_since_the_run(self):
        if RESULTS_V2 is None:
            self.skipTest("results_v2.json not written yet")
        meta = RESULTS_V2["meta"]
        self.assertEqual(meta["model_code_sha256"], rv.sha256(sm.MODEL_PATH))
        for n, h in meta["layer_code_sha256"].items():
            self.assertEqual(h, rv.sha256(PKG / n), n)


class DeterminismTests(unittest.TestCase):
    def test_model_runs_are_deterministic_and_match_results_v2(self):
        plan = rv.load_plan_v2()
        a = rv.analyse(plan, with_kernel=False, with_layer=False)
        b = rv.analyse(plan, with_kernel=False, with_layer=False)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        if RESULTS_V2 is not None:
            self.assertEqual(json.loads(json.dumps(a["model"])), RESULTS_V2["model"])
            self.assertEqual(json.loads(json.dumps(a["meta"])), RESULTS_V2["meta"])

    def test_layer_runs_match_results_v2(self):
        if RESULTS_V2 is None:
            self.skipTest("results_v2.json not written yet")
        lay = json.loads(json.dumps(rv.rnd(rv.layer_runs())))
        self.assertEqual(lay, RESULTS_V2["layer"])

    def test_tv_and_variants(self):
        self.assertEqual(rv.tv({"a": 1.0}, {"b": 1.0}), 1.0)
        self.assertEqual(rv.tv({"a": 0.5, "b": 0.5}, {"a": 0.5, "b": 0.5}), 0.0)
        d = rv.load_data(rv.IN_V2, "v2")
        v = rv.variant(d, drop=rv.NEW_ROWS, sigma=0.5, relabel=None)
        self.assertEqual(len(v.cands), len(d.cands) - 2)
        self.assertEqual(v.place["iv17_abu_saraj"]["sigma_km"], "0.5")
        self.assertEqual(d.place["iv17_abu_saraj"]["sigma_km"], "0.3")  # the original is untouched
        np.testing.assert_equal(len(rv.load_data(rv.IN_V1, "v1").cands), len(v.cands))


if __name__ == "__main__":
    unittest.main()
