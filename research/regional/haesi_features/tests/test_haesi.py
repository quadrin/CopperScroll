"""Tests for the HA-ESI feature list.

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/tests -t research/regional/haesi_features
"""
import csv
import filecmp
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402
import geo  # noqa: E402

OUTPUTS = ["features.csv", "features_unlocated.csv", "reports.csv", "dropped.csv", "looks_haesi.csv", "summary.md", "summary.json"]


def rows(name):
    with open(ROOT / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


class TestPlan(unittest.TestCase):
    def test_plan_hash_matches_readme(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        m = re.search(r"search_plan\.json SHA-256: `([0-9a-f]{64})`", readme)
        self.assertIsNotNone(m, "README must record the plan hash")
        self.assertEqual(hashlib.sha256((ROOT / "search_plan.json").read_bytes()).hexdigest(), m.group(1))

    def test_plan_is_json(self):
        plan = json.loads((ROOT / "search_plan.json").read_text(encoding="utf-8"))
        self.assertEqual(plan["location"]["primary_radius_km"], 2.0)
        self.assertEqual(plan["location"]["sensitivity_radius_km"], 5.0)


class TestSchema(unittest.TestCase):
    def test_headers(self):
        self.assertEqual(header(ROOT / "features.csv"), build.FEATURE_FIELDS)
        self.assertEqual(header(ROOT / "features_unlocated.csv"), build.FEATURE_FIELDS)
        self.assertEqual(header(ROOT / "reports.csv"), build.REPORT_FIELDS)
        self.assertEqual(header(ROOT / "dropped.csv"), build.DROP_FIELDS)
        self.assertEqual(header(ROOT / "looks_haesi.csv"), header(build.LOOKS_REF))

    def test_values(self):
        for name in ("features.csv", "features_unlocated.csv"):
            for r in rows(name):
                self.assertIn(r["feature_type"], build.TYPES)
                self.assertIn(r["dated_in_window"], ("yes", "no", "unknown"))
                if r["crs_used"]:
                    self.assertIn(r["crs_used"], ("EPSG:28191", "EPSG:2039"))
        for r in rows("looks_haesi.csv"):
            self.assertIn(r["result"], ("reported", "silent"))
            for f in ("coverage", "p_recognise", "p_report", "p_survive"):
                self.assertEqual(r[f], "", "no detection number may be invented")
                self.assertTrue(r[f + "_basis"].startswith("UNKNOWN"))


class TestQuotes(unittest.TestCase):
    def test_quotes_at_most_12_words(self):
        for name in ("features.csv", "features_unlocated.csv"):
            for r in rows(name):
                self.assertTrue(r["quote"].strip(), r["report_id"])
                self.assertLessEqual(len(r["quote"].split()), 12, (r["report_id"], r["quote"]))
        for p in (ROOT / "data").glob("coding_*.json"):
            for rep in json.loads(p.read_text(encoding="utf-8")):
                for f in rep["features"]:
                    self.assertLessEqual(len(f["quote"].split()), 12, (rep["report_id"], f["quote"]))


class TestIds(unittest.TestCase):
    def test_every_row_has_a_known_report_id(self):
        ids = {r["report_id"] for r in rows("reports.csv")}
        self.assertTrue(all(ids))
        for name in ("features.csv", "features_unlocated.csv"):
            for r in rows(name):
                self.assertTrue(r["report_id"])
                self.assertIn(r["report_id"], ids)
        for r in rows("looks_haesi.csv"):
            self.assertIn(r["record_id"], ids)
        for r in rows("reports.csv"):
            self.assertRegex(r["text_sha256"], r"^[0-9a-f]{64}$")


class TestGeo(unittest.TestCase):
    def test_w2b_controls(self):
        # W2B grid_convert.py controls: Kh. Qumran OIG 193620/127720; IV/17 group 19030/14415
        r = geo.parse_ref("193620/127720")
        lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
        self.assertLess(geo.km(lat, lon, 31.74183, 35.45941), 0.01)
        r = geo.parse_ref("19030/14415")
        lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
        self.assertLess(geo.km(lat, lon, 31.89009, 35.42477), 0.01)

    def test_grid_rules(self):
        self.assertEqual(geo.parse_ref("1908/5436")["grid"], "NIG")
        self.assertEqual(geo.parse_ref("1816/1554")["grid"], "OIG")
        self.assertTrue(geo.parse_ref("612342/221662")["swapped"])
        self.assertEqual(geo.parse_ref("2222/6315")["unit_m"], 100)


class TestDeterminism(unittest.TestCase):
    def test_build_is_deterministic_and_matches_files(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            build.main(a)
            build.main(b)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(a) / name, Path(b) / name, shallow=False), name)
                self.assertTrue(filecmp.cmp(Path(a) / name, ROOT / name, shallow=False), name + " differs from the stored file")


class TestLooksJoin(unittest.TestCase):
    def test_validates_with_search_model(self):
        path = REPO / "research" / "models" / "search_effectiveness" / "search_model.py"
        spec = importlib.util.spec_from_file_location("search_model_for_haesi", path)
        sm = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(sm)
        except ImportError as e:  # numpy missing
            self.skipTest(str(e))
        looks = sm.load_looks(ROOT / "looks_haesi.csv")
        entries = {r["entry"] for r in build.read_csv(build.W2B_IN / "entries_v2.csv")}
        places = {r["place_id"] for r in build.read_csv(build.W2B_IN / "places_v2.csv")}
        states = places | {"U_" + r["model_region"] for r in build.read_csv(build.W2B_IN / "places_v2.csv")}
        sm.validate_looks(looks, entries, states)
        # null numbers only: no factor below 1 can arise
        self.assertTrue(all(r[f] is None for r in looks for f in sm.NUM_FIELDS))


if __name__ == "__main__":
    unittest.main()
