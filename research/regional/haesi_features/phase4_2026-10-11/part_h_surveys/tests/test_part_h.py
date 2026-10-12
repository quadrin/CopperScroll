#!/usr/bin/env python3
"""Checks for part H (SWP Memoirs III and II, Guerin Judee I).

Run from the repository root:
  python3 -I research/regional/haesi_features/phase4_2026-10-11/part_h_surveys/tests/test_part_h.py

Checks: column order equals phase 2; zones recomputed from the SWP square calibration or the gazetteer;
feature rows carry their unit's screened zone; no held unit has a feature row; the build reproduces the
committed tables byte for byte; README counts match the tables; quotes are at most 12 words.
"""
import csv
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
PHASE2 = PART.parents[1] / "phase2_2026-10-10"
sys.path.insert(0, str(PART / "scripts"))
sys.path.insert(0, str(PHASE2 / "scripts"))

import build_part_h  # noqa: E402
import names  # noqa: E402
import swp_grid  # noqa: E402

SCREENS = {"swp3": "screen_swp3.csv", "swp2": "screen_swp2.csv", "gue_j1": "screen_gue_j1.csv"}


def header(p):
    with open(p, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def rows(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def jsonl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


class ColumnOrder(unittest.TestCase):
    def test_features_columns(self):
        ref = header(PHASE2 / "features.csv")
        self.assertEqual(header(PART / "features.csv"), ref)
        self.assertEqual(header(PART / "features_zone_unresolved.csv"), ref)

    def test_reports_columns(self):
        self.assertEqual(header(PART / "reports.csv"), header(PHASE2 / "reports.csv"))


class Zones(unittest.TestCase):
    def setUp(self):
        self.coef = {"3": swp_grid.fit(group="III"), "2": swp_grid.fit(group="II")}

    def gaz(self, name, seen=None):
        hz = sorted(z for z in names.gaz_hits(name) if z != "REGION_WIDE")
        if seen is not None:
            hz = [z for z in hz if z in seen]
        return hz

    def test_swp_zones_recomputed(self):
        n = 0
        for src in ("swp3", "swp2"):
            for r in rows(PART / "data" / SCREENS[src]):
                b = r["location_basis"]
                if b in ("SWP square", "SWP square (zone split)"):
                    z, status, seen = swp_grid.square_zone(r["square"], self.coef[r["vol"]])
                    if b == "SWP square":
                        self.assertEqual(status, "clear", r["unit_id"])
                        self.assertEqual(z or "OUTSIDE", r["zone"], r["unit_id"])
                    else:
                        self.assertEqual(status, "mixed", r["unit_id"])
                        self.assertNotIn("OUTSIDE", seen, r["unit_id"])
                        self.assertEqual("|".join(seen), r["zone"], r["unit_id"])
                    n += 1
                elif b == "name (gazetteer)":
                    seen = r["zones_seen"].split("|") if r["square_status"] == "mixed" else None
                    self.assertEqual(self.gaz(r["name"], seen), [r["zone"]], r["unit_id"])
                    n += 1
        self.assertGreater(n, 1000)

    def test_guerin_zones_recomputed(self):
        for r in rows(PART / "data" / SCREENS["gue_j1"]):
            if r["location_basis"]:
                self.assertEqual(self.gaz(r["name"]), [r["zone"]], r["unit_id"])
            elif r["decision"].startswith("unlocated: no gazetteer"):
                self.assertEqual(self.gaz(r["name"]), [], r["unit_id"])

    def test_feature_rows_carry_screen_zone(self):
        zone = {}
        for f in SCREENS.values():
            for r in rows(PART / "data" / f):
                zone[r["unit_id"]] = r["zone"]
        for r in rows(PART / "features.csv"):
            self.assertEqual(r["region_zone"], zone[r["report_id"]])
            self.assertTrue(r["region_zone"].startswith("Z") and "|" not in r["region_zone"])
        for r in rows(PART / "features_zone_unresolved.csv"):
            self.assertEqual(r["region_zone"], zone[r["report_id"]])
            self.assertIn("|", r["region_zone"])

    def test_only_candidates_read(self):
        dec = {}
        for f in SCREENS.values():
            for r in rows(PART / "data" / f):
                dec[r["unit_id"]] = r["decision"]
        for r in rows(PART / "reports.csv"):
            self.assertTrue(dec[r["report_id"]].startswith("candidate"), r["report_id"])


class Held(unittest.TestCase):
    def test_no_feature_rows_for_held_units(self):
        held = jsonl(PART / "data" / "held_records.jsonl")
        whole = {h["unit_id"] for h in held if h["scope"].startswith("whole")}
        self.assertTrue(whole)
        fr = {r["report_id"] for r in rows(PART / "features.csv") + rows(PART / "features_zone_unresolved.csv")}
        rep = {r["report_id"] for r in rows(PART / "reports.csv")}
        self.assertFalse(whole & fr)
        self.assertFalse(whole & rep)
        for h in held:
            self.assertLessEqual(len(h["first_words"].split()), 12, h["unit_id"])

    def test_protected_strip_rows(self):
        held = jsonl(PART / "data" / "held_records.jsonl")
        self.assertTrue(any(h["protected_strip"] == "yes" for h in held))
        for r in rows(PART / "features.csv") + rows(PART / "features_zone_unresolved.csv"):
            self.assertEqual(r["protected_strip"], "no")


class Content(unittest.TestCase):
    def test_quotes_short(self):
        for r in rows(PART / "features.csv") + rows(PART / "features_zone_unresolved.csv"):
            self.assertLessEqual(len(r["quote"].split()), 12, r["report_id"])
            self.assertIn(r["dated_in_window"], ("yes", "no", "unknown"))
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertEqual(r["coordinate_source"].split(" ")[0] in ("SWP", "name"), True)
            self.assertEqual(r["lat"], "")

    def test_build_reproduces_tables(self):
        with tempfile.TemporaryDirectory() as d:
            build_part_h.main(d)
            for name in ("features.csv", "features_zone_unresolved.csv", "reports.csv", "screen.csv", "held.csv",
                         "summary.json", "summary.md"):
                self.assertEqual((Path(d) / name).read_bytes(), (PART / name).read_bytes(), name)


class Readme(unittest.TestCase):
    def test_counts_match(self):
        js = json.loads((PART / "summary.json").read_text(encoding="utf-8"))
        text = (PART / "README.md").read_text(encoding="utf-8")
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("**What it is.**"))
        self.assertTrue(lines[1].startswith("**Main result.**"))
        self.assertTrue(lines[2].startswith("**What stays unknown.**"))
        must = ["%d units screened" % js["units_screened"], "%d units read" % js["units_read"],
                "%d feature rows" % js["feature_rows"], "%d further rows" % js["feature_rows_zone_unresolved"]]
        for m in must:
            self.assertIn(m, text)
        for k, v in js["status"].items():
            self.assertIn("| %s | %d |" % (k, v), text)
        summary_rows = [l for l in (PART / "summary.md").read_text(encoding="utf-8").splitlines() if l.startswith("| ")]
        for l in summary_rows:
            self.assertIn(l, lines, l)
        n_feat = len(rows(PART / "features.csv"))
        n_unres = len(rows(PART / "features_zone_unresolved.csv"))
        self.assertEqual(n_feat, js["feature_rows"])
        self.assertEqual(n_unres, js["feature_rows_zone_unresolved"])
        self.assertEqual(len(rows(PART / "reports.csv")), js["units_read"])
        self.assertEqual(len(rows(PART / "screen.csv")), js["units_screened"])
        self.assertEqual(len(rows(PART / "held.csv")), js["held_records"])
        self.assertTrue(re.search(r"\b%d held records\b" % js["held_records"], text))


if __name__ == "__main__":
    unittest.main(verbosity=1)
