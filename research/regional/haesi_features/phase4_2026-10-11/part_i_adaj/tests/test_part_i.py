"""Tests for phase 4, part I (ADAJ).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_i_adaj/tests
"""
import csv
import filecmp
import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

PART = Path(__file__).resolve().parents[1]
PHASE4 = PART.parent
LANE = PHASE4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(PART / "scripts"))
sys.path.insert(0, str(P2 / "scripts"))
import build_part_i  # noqa: E402
import common  # noqa: E402

PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"
OUTPUTS = ["features.csv", "reports.csv", "screen.csv", "held.csv", "summary.md", "summary.json"]
ZONES = build_part_i.ZONES


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def coding():
    return json.loads((PART / "data" / "coding.json").read_text(encoding="utf-8"))


class TestPlan(unittest.TestCase):
    def test_phase2_plan_hash(self):
        self.assertEqual(hashlib.sha256((P2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)


class TestSchema(unittest.TestCase):
    def test_columns_match_phase2(self):
        self.assertEqual(header(PART / "features.csv"), header(P2 / "features.csv"))
        self.assertEqual(header(PART / "reports.csv"), header(P2 / "reports.csv"))

    def test_coding_values(self):
        recs = coding()
        ids = [r["report_id"] for r in recs]
        self.assertEqual(len(ids), len(set(ids)))
        for r in recs:
            self.assertRegex(r["report_id"], r"^ADAJ\d+(_\d+)?(ar)?-\d{3}-[a-z0-9-]+$")
            self.assertEqual(r.get("exposure", "unexposed at freeze"), "unexposed at freeze")
            for f in r["features"]:
                self.assertIn(f["type"], build_part_i.CLASSES, r["report_id"])
                self.assertIn(f["window"], ("yes", "no", "unknown"), r["report_id"])
                self.assertTrue(f["quote"], r["report_id"])
                self.assertLessEqual(len(f["quote"].split()), 12, (r["report_id"], f["quote"]))

    def test_every_record_has_a_verified_span(self):
        spans = {s["report_id"]: s for s in rows(PART / "data" / "spans.csv")}
        for r in coding():
            s = spans[r["report_id"]]
            self.assertEqual(s["pdf_file"], r["span"]["pdf"], r["report_id"])
            self.assertEqual(s["pdf_pages"], r["span"]["pages"], r["report_id"])
            self.assertEqual(s["quotes_not_found"], "", r["report_id"])
            self.assertEqual(int(s["n_quotes"]), sum(1 for f in r["features"] if f.get("quote")), r["report_id"])
            self.assertRegex(s["text_sha256"], r"^[0-9a-f]{64}$")


class TestZones(unittest.TestCase):
    def test_zone_recomputed_from_coordinates(self):
        params = common.plan_params()
        n = 0
        for f in rows(PART / "features.csv") + rows(PART / "reports.csv"):
            if f["lat"] and f["lon"]:
                n += 1
                self.assertEqual(common.zone_of(float(f["lat"]), float(f["lon"]), params) or "outside",
                                 f["region_zone"], f["report_id"])
        for f in rows(PART / "features.csv"):
            self.assertIn(f["region_zone"], ZONES, f["report_id"])

    def test_tier_follows_zone_and_title(self):
        for r in rows(PART / "screen.csv"):
            if r["decision"].startswith("candidate"):
                self.assertIn(r["zone"], ZONES, r["screen_key"])
                self.assertIn(r["tier"], ("T1", "T2", "T3"), r["screen_key"])


class TestHeld(unittest.TestCase):
    def test_no_held_unit_coded(self):
        held = {h["unit_id"] for h in rows(PART / "held.csv")}
        self.assertTrue(held)
        self.assertFalse(held & {r["report_id"] for r in rows(PART / "reports.csv")})
        self.assertFalse(held & {r["report_id"] for r in rows(PART / "features.csv")})
        self.assertFalse(held & {r["report_id"] for r in coding()})

    def test_held_first_lines_short(self):
        for h in rows(PART / "held.csv"):
            self.assertLessEqual(len(h["first_line"].split()), 12, h["unit_id"])

    def test_no_strip_feature_rows(self):
        for f in rows(PART / "features.csv"):
            self.assertEqual(f["protected_strip"], "no", f["report_id"])


class TestOutputs(unittest.TestCase):
    def test_build_reproduces_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_part_i.main(tmp)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(tmp) / name, PART / name, shallow=False), name)

    def test_every_candidate_has_a_status(self):
        for r in rows(PART / "screen.csv"):
            if r["decision"].startswith("candidate"):
                self.assertIn(r["status"], ("read and coded", "not read (time limit)"), r["screen_key"])

    def test_readme_counts_match_tables(self):
        readme = (PART / "README.md").read_text(encoding="utf-8")
        js = json.loads((PART / "summary.json").read_text(encoding="utf-8"))
        feats = rows(PART / "features.csv")
        reps = rows(PART / "reports.csv")
        self.assertEqual(js["feature_rows"], len(feats))
        self.assertEqual(js["units_coded"], len(reps))
        m = re.search(r"README counts: units coded (\d+); feature rows (\d+) \(yes (\d+) / no (\d+) / unknown (\d+)\); "
                      r"held or protected (\d+); screen rows (\d+)", readme)
        self.assertIsNotNone(m, "README counts line missing")
        w = js["window"]
        self.assertEqual([int(x) for x in m.groups()],
                         [len(reps), len(feats), w.get("yes", 0), w.get("no", 0), w.get("unknown", 0),
                          len(rows(PART / "held.csv")), js["screen_rows"]])


if __name__ == "__main__":
    unittest.main()
