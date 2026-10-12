"""Tests for the exploratory phase-4 inventory view (PLAN_AMENDMENT_PHASE4_2026-10-12.md).

From the repository root:
  python3 -I -B -m unittest discover -s research/comparanda/hoards_full/tests -t research/comparanda/hoards_full
"""
import csv
import hashlib
import importlib.util
import json
import os
import re
import unittest

LANE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load():
    spec = importlib.util.spec_from_file_location("phase4_view", os.path.join(LANE, "scripts", "phase4_view.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = load()


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestFreeze(unittest.TestCase):
    def test_amendment_hash(self):
        self.assertEqual(sha(V.AMENDMENT), V.AMENDMENT_SHA256)
        self.assertEqual(V.AMENDMENT_SHA256, "ba1f690c9a556290895b119f23464201f0ac736ddee4f98bb42c5daca98b5f2d")

    def test_readme_records_amendment(self):
        with open(os.path.join(LANE, "README.md"), encoding="utf-8") as f:
            txt = f.read()
        self.assertIn(V.AMENDMENT_SHA256, txt)
        self.assertIn(V.AMENDMENT_COMMIT, txt)

    def test_frozen_lane_files_unchanged(self):
        for name, h in V.FROZEN_LANE_SHA256.items():
            self.assertEqual(sha(os.path.join(LANE, name)), h, name)
        V.H.check_frozen()

    def test_inventory_input_pinned(self):
        self.assertEqual(sha(os.path.join(V.MERGED, "features_all.csv")), V.FEATURES_ALL_SHA256)


class TestView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view = rows(V.OUT_VIEW)
        cls.scores = rows(V.OUT_SCORES)
        with open(V.OUT_SUMMARY, encoding="utf-8") as f:
            cls.summary = json.load(f)

    def test_frozen_counts_unchanged(self):
        self.assertTrue(self.summary["frozen_reproduced"])
        with open(os.path.join(LANE, "results.json"), encoding="utf-8") as f:
            frozen = json.load(f)
        got = {r["run"]: r for r in self.scores if r["view"] == "frozen"}
        for k, run in frozen["runs"].items():
            self.assertEqual(int(got[k]["comparanda_known"]), run["n_b"], k)
            self.assertEqual(int(got[k]["comparanda_unknown"]), run["n_comparanda_unknown"], k)
            self.assertAlmostEqual(float(got[k]["D"]), run["D"], places=12)
            self.assertEqual(got[k]["verdict"], run["verdict"])

    def test_every_counted_hoard_row_listed(self):
        inv = V.hoard_rows()
        self.assertEqual(sorted(r["row_uid"] for r in inv), sorted(r["row_uid"] for r in self.view))

    def test_no_protected_or_held_row_in_a_view(self):
        for r in self.view:
            text = (r["site_name"] + " " + r["feature_subtype"] + " " + r["quote"]).lower()
            protected = bool(r["protected"]) or "sultan" in text or "almit" in text or (
                re.search(V.CAVE_WORD, text) and re.search(V.HELD_AREA, text))
            if protected:
                for k in ("in_view_A", "in_view_B", "in_view_B_undetermined"):
                    self.assertNotEqual(r.get(k), "yes", r["row_uid"])

    def test_view_membership(self):
        for r in self.view:
            if r["in_view_A"] == "yes":
                self.assertEqual(r["in_view_B"], "yes")
                self.assertFalse(r["phase"].startswith("4"))
            if r["in_view_B"] == "yes":
                self.assertEqual(r["include"], "1")
                self.assertEqual(r["duplicate_of"], "")
                self.assertEqual(r["undetermined_with"], "")
                self.assertEqual(r["in_view_B_undetermined"], "yes")

    def test_checks_never_add_a_code(self):
        for r in self.view:
            if not r.get("id"):
                continue
            proposed = [x for x in r["proposed_setting"].split(";") if x]
            self.assertIn(r["setting"], proposed + ["unknown"], r["row_uid"])
            props = [x for x in r["proposed_landmark"].split(";") if x]
            for c in r["landmark"].split(";"):
                if c and c != "none_stated":
                    self.assertIn(c, props, r["row_uid"])

    def test_every_review_item_decided(self):
        b = V.build(strict=True)  # raises if a check or a candidate pair is undecided
        self.assertFalse(b["missing_checks"])
        self.assertFalse(b["missing_pairs"])

    def test_reproducible(self):
        for path, data in V.outputs().items():
            with open(path, "rb") as f:
                self.assertEqual(f.read(), data, os.path.basename(path))


if __name__ == "__main__":
    unittest.main()
