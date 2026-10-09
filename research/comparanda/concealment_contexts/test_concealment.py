"""Tests: plan hash, schema, category mapping, determinism.
Run: python3 -I -B -m unittest discover -s research/comparanda/concealment_contexts -t research/comparanda/concealment_contexts
"""
import csv
import hashlib
import os
import re
import unittest

import concealment as cc

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def words(q):
    return len(q.replace("...", " ").split())


class TestPlanHash(unittest.TestCase):
    def test_plan_hash_matches_frozen_value(self):
        with open(os.path.join(HERE, "PLAN.md"), "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, cc.PLAN_SHA256)

    def test_readme_records_hash_and_time(self):
        with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn(cc.PLAN_SHA256, text)
        self.assertRegex(text, r"Frozen: 2026-10-09T\d\d:\d\d:\d\dZ")


class TestSchema(unittest.TestCase):
    def setUp(self):
        self.comp = cc.read_csv("comparanda.csv")
        self.scr = cc.read_csv("scroll_contexts.csv")

    def test_comparanda_header(self):
        with open(os.path.join(HERE, "comparanda.csv"), encoding="utf-8") as f:
            header = next(csv.reader(f))
        self.assertEqual(header, cc.COMP_INPUT + cc.COMP_DERIVED)

    def test_comparanda_rows(self):
        ids = [r["id"] for r in self.comp]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.comp:
            self.assertIn(r["setting"], cc.SETTINGS, r["id"])
            self.assertNotEqual(r["setting"], "water_pit", r["id"])  # scroll-only setting
            self.assertIn(r["placement"], cc.PLACEMENTS, r["id"])
            self.assertIn(r["how_found"], cc.HOW_FOUND, r["id"])
            self.assertIn(r["include"], ("0", "1"), r["id"])
            self.assertTrue(r["source"], r["id"])
            self.assertTrue(r["cluster_id"], r["id"])
            self.assertLessEqual(words(r["context_reported"]), 12, r["id"])
            if r["include"] == "0":
                self.assertTrue(r["exclusion_reason"], r["id"])
            else:
                self.assertIsNotNone(cc.midpoint(r), r["id"])

    def test_scroll_header_and_entries(self):
        with open(os.path.join(HERE, "scroll_contexts.csv"), encoding="utf-8") as f:
            header = next(csv.reader(f))
        self.assertEqual(header, cc.SCROLL_INPUT + cc.SCROLL_DERIVED)
        with open(os.path.join(REPO, "tables", "entry_concordance.csv"), encoding="utf-8-sig") as f:
            canon = [r["entry_puech"] for r in csv.DictReader(f)]
        self.assertEqual([r["entry"] for r in self.scr], canon)
        self.assertEqual(len(self.scr), 61)
        for r in self.scr:
            for b in cc.BRANCHES:
                self.assertIn(r[f"setting_{b}"], cc.SETTINGS, (r["entry"], b))
                self.assertIn(r[f"placement_{b}"], cc.PLACEMENTS, (r["entry"], b))
                if b != "P" and (r[f"setting_{b}"], r[f"placement_{b}"]) != (r["setting_P"], r["placement_P"]):
                    self.assertTrue(r[f"ref_{b}"], (r["entry"], b))  # every branch change cites readings.json

    def test_branch_refs_exist_in_readings(self):
        import json
        with open(os.path.join(REPO, "text", "readings.json"), encoding="utf-8") as f:
            ids = {x["id"] for x in json.load(f)}
        for r in self.scr:
            for b in ("Pu", "M", "L"):
                for ref in filter(None, (s.strip() for s in r[f"ref_{b}"].split(";"))):
                    self.assertIn(ref, ids, (r["entry"], b, ref))


class TestMapping(unittest.TestCase):
    def test_every_combination_maps(self):
        for s in cc.SETTINGS:
            for p in cc.PLACEMENTS:
                for pit in (False, True):
                    f = cc.fine_category(s, p, pit)
                    self.assertIn(f, cc.FINE_LABELS)
                    g = cc.coarse_group(s, pit)
                    self.assertTrue(g is None or g in cc.COARSE_LABELS)
                    self.assertEqual(f == "UNK", g is None, (s, p, pit))

    def test_named_categories_present(self):
        named = ["cistern", "pool/reservoir", "channel/aqueduct/conduit", "tomb or burial cave",
                 "natural cave or shelter", "wall cavity", "under floor", "under a stone or threshold",
                 "jar buried in ground", "near a column/pillar", "field or open ground", "ruin or heap"]
        labels = set(cc.FINE_LABELS.values())
        for n in named:
            self.assertIn(n, labels)

    def test_examples(self):
        self.assertEqual(cc.fine_category("structure", "under_floor"), "C07")
        self.assertEqual(cc.fine_category("structure", "wall_cavity"), "C06")
        self.assertEqual(cc.fine_category("open_ground", "container_buried"), "C09")
        self.assertEqual(cc.fine_category("ruin_heap", "under_stone_threshold"), "C08")
        self.assertEqual(cc.fine_category("cave", "under_stone_threshold"), "C05")
        self.assertEqual(cc.fine_category("water_pit", "not_stated"), "C01")
        self.assertEqual(cc.fine_category("water_pit", "not_stated", pit_unknown=True), "UNK")
        self.assertEqual(cc.coarse_group("ruin_heap"), "G5")

    def test_stored_derived_columns_match(self):
        for r in cc.read_csv("comparanda.csv"):
            self.assertEqual(r["context_category"], cc.fine_category(r["setting"], r["placement"]), r["id"])
            self.assertEqual(r["coarse_group"], cc.coarse_group(r["setting"]) or "", r["id"])
        for r in cc.read_csv("scroll_contexts.csv"):
            for b in cc.BRANCHES:
                self.assertEqual(r[f"fine_{b}"], cc.fine_category(r[f"setting_{b}"], r[f"placement_{b}"]))

    def test_window_and_region_rules(self):
        row = {"date_from": "-64", "date_to": "-62", "lat": "31.7", "lon": "35.2", "judaea_by_name": "",
               "country": "Israel"}
        self.assertTrue(cc.in_window(row, cc.WINDOW_SENS))
        self.assertTrue(cc.in_region_judaea(row))
        row2 = dict(row, lat="", lon="", judaea_by_name="")
        self.assertFalse(cc.in_region_judaea(row2))


class TestStatistics(unittest.TestCase):
    def test_dissimilarity_and_verdict(self):
        self.assertAlmostEqual(cc.dissimilarity(["G1", "G1"], ["G4", "G4"], ["G1", "G4"]), 1.0)
        self.assertAlmostEqual(cc.dissimilarity(["G1", "G4"], ["G4", "G1"], ["G1", "G4"]), 0.0)
        self.assertEqual(cc.verdict({"p": 0.01, "D": 0.3}, 40), "DIFFERENT")
        self.assertEqual(cc.verdict({"p": 0.2, "D": 0.1}, 40), "SIMILAR")
        self.assertEqual(cc.verdict({"p": 0.01, "D": 0.1}, 40), "INCONCLUSIVE")
        self.assertEqual(cc.verdict({"p": 0.01, "D": 0.9}, 29), "NOT TESTABLE")


class TestDeterminism(unittest.TestCase):
    def test_build_is_idempotent(self):
        cb, sb = cc.built_bytes()
        with open(os.path.join(HERE, "comparanda.csv"), "rb") as f:
            self.assertEqual(f.read(), cb)
        with open(os.path.join(HERE, "scroll_contexts.csv"), "rb") as f:
            self.assertEqual(f.read(), sb)

    def test_compare_repeats(self):
        a = ["G1"] * 10 + ["G4"] * 3
        b = ["G4"] * 12 + ["G3"] * 5
        self.assertEqual(cc.compare(a, b, cc.COARSE_ORDER), cc.compare(a, b, cc.COARSE_ORDER))

    def test_results_file_matches_fresh_run(self):
        with open(os.path.join(HERE, "results.json"), "rb") as f:
            self.assertEqual(f.read(), cc.results_bytes(cc.analyse()))


if __name__ == "__main__":
    unittest.main()
