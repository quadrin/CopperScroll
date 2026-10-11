"""Tests for the hoards_full lane. Standard library only.

From the repository root:
  python3 -I -B -m unittest discover -s research/comparanda/hoards_full/tests -t research/comparanda/hoards_full
"""
import csv
import hashlib
import importlib.util
import os
import re
import unittest

LANE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREC = os.path.join(os.path.dirname(LANE), "concealment_contexts")


def load():
    spec = importlib.util.spec_from_file_location("hoards_full", os.path.join(LANE, "hoards_full.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = load()


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestFreeze(unittest.TestCase):
    def test_plan_hash(self):
        with open(os.path.join(LANE, "PLAN.md"), "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), H.PLAN_SHA256)

    def test_readme_records_plan_hash(self):
        with open(os.path.join(LANE, "README.md"), encoding="utf-8") as f:
            self.assertIn(H.PLAN_SHA256, f.read())

    def test_frozen_inputs(self):
        H.check_frozen()  # raises SystemExit if any precedent input changed

    def test_statistic_is_the_precedents(self):
        self.assertTrue(H.C.__file__.endswith(os.path.join("concealment_contexts", "concealment.py")))
        self.assertEqual((H.C.SEED, H.C.N_PERM, H.C.N_BOOT, H.C.D_THRESHOLD, H.C.MIN_KNOWN),
                         (20261009, 20000, 2000, 0.25, 30))


class TestSchema(unittest.TestCase):
    def setUp(self):
        self.rows = rows(os.path.join(LANE, "hoards.csv"))

    def test_header(self):
        with open(os.path.join(LANE, "hoards.csv"), encoding="utf-8") as f:
            self.assertEqual(f.readline().strip().split(","), H.FIELDS)

    def test_validate(self):
        self.assertTrue(H.validate(self.rows))

    def test_precedent_rows_unchanged_except_documented_recodes(self):
        prec = {r["id"]: r for r in rows(os.path.join(PREC, "comparanda.csv"))}
        mine = [r for r in self.rows if r["origin"] == "precedent"]
        self.assertEqual(len(mine), len(prec))
        for r in mine:
            p = prec[r["id"]]
            for k in H.PREC_INPUT:
                if k == "flags":
                    self.assertTrue(r[k].startswith(p[k]), r["id"])
                elif r["recode_reason"] and k in ("setting", "placement", "include", "date_from", "date_to"):
                    continue
                else:
                    self.assertEqual(r[k], p[k], f"{r['id']} {k}")
            if r["recode_reason"]:
                self.assertEqual(r["prec_setting"], p["setting"])
                self.assertEqual(r["prec_placement"], p["placement"])
                self.assertEqual(r["prec_include"], p["include"])

    def test_new_rows(self):
        prec_ids = {r["id"] for r in rows(os.path.join(PREC, "comparanda.csv"))}
        for r in self.rows:
            if r["origin"] == "new":
                self.assertNotIn(r["id"], prec_ids)
                self.assertEqual(r["first_read"], "after_freeze")
                self.assertTrue(r["source"], r["id"])

    def test_unknown_is_null(self):
        for r in self.rows:
            if r["setting"] == "unknown" and r["include"] == "1":
                self.assertEqual(r["landmark"], "", r["id"])

    def test_mapping_examples(self):
        self.assertEqual(H.C.fine_category("structure", "wall_cavity"), "C06")
        self.assertEqual(H.C.coarse_group("cave"), "G3")
        self.assertEqual(H.window_status({"date_from": "-225", "date_to": "-175"}), "partial")
        self.assertEqual(H.window_status({"date_from": "68", "date_to": "68"}), "inside")
        self.assertEqual(H.landmark_strict({"landmark": "threshold", "landmark_text": "at the entrance to x"}),
                         "none_stated")
        self.assertEqual(H.landmark_strict({"landmark": "threshold", "landmark_text": "under the doorway"}),
                         "threshold")


class TestDescriptive(unittest.TestCase):
    def test_scroll_digs(self):
        digs, cub = H.scroll_digs()
        self.assertEqual(len(digs), 26)
        self.assertEqual(cub, {"short": 0.445, "working": 0.5, "royal": 0.525})

    def test_scroll_regex(self):
        self.assertEqual(H.scroll_landmarks("in the reservoir, as you go in, on its left"), ["threshold"])
        self.assertEqual(H.scroll_landmarks("in the reservoir, as you go in", strict=True), [])
        self.assertEqual(H.scroll_landmarks("in the cistern opposite the East Gate"), ["gate"])


class TestReproduce(unittest.TestCase):
    def test_check(self):
        cwd = os.getcwd()
        try:
            H.main(["hoards_full.py", "check"])
        finally:
            os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
