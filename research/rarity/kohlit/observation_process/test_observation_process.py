"""Tests for the observation-process audit. Synthetic data, plus consistency checks on the
committed CSV files. Run: python3 -I test_observation_process.py"""
import csv
import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import observation as O  # noqa: E402

M = O.M


def sheet(absences, features, uid="S1"):
    return {"unit_id": uid, "coder": "A", "sources": {k: "read" for k in "12345"},
            "explicit_absence": absences, "features": features}


def pit(fid, pos):
    return {"id": fid, "source": "1", "cite": "x", "quote": "cistern", "type": "pit", "is_tomb": False,
            "position": pos, "date": {"code": "U", "basis": "test"}}


ZERTAL = {"condition": "C2", "source": "2", "cite": "Zertal test p. 1", "quote": "Cisterns: none"}
REFS = {"S2": {"bearing_deg": 180.0, "distance_m": 500, "bearing_valid": True}, "S1": None}


class ScopeRules(unittest.TestCase):
    def test_classify_known_forms(self):
        self.assertEqual(O.classify("2", "Cisterns: none")["spatial_scope"], "site only")
        self.assertEqual(O.classify("3", "There are wells and cisterns, but no tombs were found")["rule"],
                         "swp_no_tombs_sentence")

    def test_unknown_form_stops(self):
        with self.assertRaises(ValueError):
            O.classify("4", "no water installation")

    def test_registered_forms_do_not_reach_sector(self):
        for r in O.RULES:
            for c in ("C2", "C3"):
                self.assertFalse(O.reaches_sector(r, c))

    def test_stated_radius_rule_reaches_only_if_class_covered(self):
        r = {"spatial_scope": "stated radius", "stated_radius_m": 1000, "class_covers_condition": True}
        self.assertTrue(O.reaches_sector(r, "C2"))
        self.assertFalse(O.reaches_sector(dict(r, stated_radius_m=500), "C2"))
        self.assertFalse(O.reaches_sector(dict(r, class_covers_condition=False), "C2"))

    def test_area_and_share(self):
        self.assertEqual(O.area_m2("1 dunam (1000 sq. m)"), 1000)
        self.assertEqual(O.area_m2("7.5 dunams (7500 sq. m)"), 7500)
        self.assertEqual(O.area_m2("0.5 dunam (0.13 acre)"), 500)
        self.assertIsNone(O.area_m2(""))
        self.assertAlmostEqual(O.site_share_pct(1000), 0.032, places=3)
        self.assertAlmostEqual(O.site_share_pct(3141593), 100.0, places=1)

    def test_grid_geometry_and_rule_2(self):
        g = O.grid_geom(189300, 184900, 188900, 185800)
        self.assertEqual(g["distance_m"], 985)
        self.assertAlmostEqual(g["bearing_deg"], 336.0, places=0)
        self.assertTrue(g["bearing_valid"])
        self.assertFalse(O.grid_geom(193900, 194600, 193900, 194800)["bearing_valid"])


class Models(unittest.TestCase):
    def test_registered_rule_fails_and_scope_rule_does_not(self):
        s = sheet([ZERTAL], [pit("f1", {"kind": "grid", "ref": "S2"})])
        self.assertEqual(M.evaluate(s, REFS, {})["C2"][0], "FAIL")
        table = {("A", "S1", "C2", "2", "Cisterns: none"): False}
        self.assertEqual(M.evaluate(O.scoped_sheet(s, "A", table), REFS, {})["C2"][0], "UNKNOWN")

    def test_reaching_absence_keeps_fail(self):
        s = sheet([ZERTAL], [])
        table = {("A", "S1", "C2", "2", "Cisterns: none"): True}
        self.assertEqual(M.evaluate(O.scoped_sheet(s, "A", table), REFS, {})["C2"][0], "FAIL")

    def test_missing_absence_row_stops(self):
        with self.assertRaises(KeyError):
            O.scoped_sheet(sheet([ZERTAL], []), "A", {})

    def test_scope_rule_never_creates_a_match(self):
        s = sheet([ZERTAL], [pit("f1", {"kind": "grid", "ref": "S3"})])
        refs = dict(REFS, S3={"bearing_deg": 10.0, "distance_m": 400, "bearing_valid": True})
        table = {("A", "S1", "C2", "2", "Cisterns: none"): False}
        self.assertEqual(M.evaluate(s, refs, {})["C2"][0], "MATCH")
        self.assertEqual(M.evaluate(O.scoped_sheet(s, "A", table), refs, {})["C2"][0], "MATCH")

    def test_sector_record_positions(self):
        packet = {"unit": {"x": 189300, "y": 184900, "precision_m": 100}}
        far = {"record_id": "r1", "protocol_source": "2", "cite": "c", "quote": "q", "subtype": "cistern",
               "ref": "", "x": "188900", "y": "185800", "precision_m": "100"}
        f = O.record_feature(far, packet)
        self.assertEqual(f["position"]["kind"], "plan")
        self.assertEqual(f["position"]["distance_m"], 985)
        near = dict(far, x="189300", y="185100")
        self.assertEqual(O.record_feature(near, packet)["position"], {"kind": "none"})
        self.assertEqual(O.record_feature(dict(far, ref="S9"), packet)["position"], {"kind": "grid", "ref": "S9"})
        s = sheet([ZERTAL], [f])
        self.assertEqual(M.evaluate(s, REFS, {})["C2"][0], "MATCH")
        s = sheet([ZERTAL], [O.record_feature(near, packet)])
        self.assertEqual(M.evaluate(s, REFS, {})["C2"][0], "UNKNOWN")


class CommittedFiles(unittest.TestCase):
    def rows(self, name):
        with open(HERE / name, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_absences_table(self):
        rows = self.rows("absences.csv")
        self.assertEqual(len(rows), 63)
        self.assertEqual({r["reaches_1km_sector"] for r in rows}, {"no"})
        self.assertEqual(sum(r["quote"] == "Cisterns: none" for r in rows), 61)
        for r in rows:
            self.assertLessEqual(len(r["quote"].split()), 12, r["absence_id"])
            O.classify(r["source"], r["quote"])

    def test_sector_records(self):
        for r in self.rows("sector_records.csv"):
            self.assertLessEqual(len(r["quote"].split()), 12)
            m = re.search(r"(\d+) m at (\d+(?:\.\d+)?) deg from the unit point", r["note"])
            if m and not r["ref"]:
                g = O.grid_geom(int(r["unit_x"]), int(r["unit_y"]), int(r["x"]), int(r["y"]))
                self.assertEqual(g["distance_m"], int(m.group(1)))
                self.assertAlmostEqual(g["bearing_deg"], float(m.group(2)), delta=0.6)

    def test_comparison_registered_columns_equal_committed_result(self):
        committed = json.loads((O.REGISTERED_DIR / "summary.json").read_text(encoding="utf-8"))
        for r in self.rows("results/comparison.csv"):
            key = f"{r['set']}|{r['branch']}" + (f"|{r['variant']}" if r["table"] == "sensitivity" else "")
            t = committed[r["table"]][key]
            self.assertEqual((int(r["registered_k"]), int(r["registered_f"]), int(r["registered_m"])),
                             (t["k"], t["f"], t["m"]), key)
            self.assertEqual(int(r["scoped_f"]), 0)
            self.assertEqual(int(r["scoped_k"]), t["k"])
            self.assertEqual(int(r["scoped_m"]), t["m"] + t["f"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
