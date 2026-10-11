"""Tests for HA-ESI phase 3, part D (online tier T3, positions 81-662).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase3_2026-10-11/part_d_online/tests
"""
import csv
import filecmp
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

PART = Path(__file__).resolve().parents[1]
PHASE3 = PART.parent
PHASE2 = PHASE3.parent / "phase2_2026-10-10"
sys.path.insert(0, str(PART / "scripts"))
import build_part_d  # noqa: E402

PHASE3_PLAN_SHA256 = "312c27332bbc4d9b9d3405d88cb8d9d40e8e361714cdd5582997467593055cf2"  # commit 4d8325e
PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"  # commit d0f8c7c
OUTPUTS = ["features.csv", "reports.csv", "screen.csv", "summary.md", "summary.json"]
CLASSES = {"cistern", "pool_reservoir", "channel_aqueduct", "dam", "ritual_bath", "cave_with_finds",
           "tomb_burial_cave", "columbarium_dovecote", "rockcut_installation", "hoard_cache"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def coding():
    return json.loads((PART / "data" / "coding_online_t3.json").read_text(encoding="utf-8"))


class TestPlans(unittest.TestCase):
    def test_frozen_plan_hashes(self):
        self.assertEqual(hashlib.sha256((PHASE3 / "PLAN.md").read_bytes()).hexdigest(), PHASE3_PLAN_SHA256)
        self.assertEqual(hashlib.sha256((PHASE2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)


class TestSchema(unittest.TestCase):
    def test_columns_match_phase2_exactly(self):
        self.assertEqual(header(PART / "features.csv"), header(PHASE2 / "features.csv"))
        self.assertEqual(header(PART / "reports.csv"), header(PHASE2 / "reports.csv"))

    def test_coding_records(self):
        recs = coding()
        self.assertTrue(recs)
        for r in recs:
            self.assertTrue(r["report_id"].startswith("HAESI-"))
            self.assertRegex(r["text_sha256"], r"^[0-9a-f]{64}$")
            self.assertIsInstance(r["text_chars"], int)
            for f in r["features"]:
                self.assertIn(f["type"], CLASSES)
                self.assertIn(f["window"], ("yes", "no", "unknown"))
                self.assertLessEqual(len(f["quote"].split()), 12, (r["report_id"], f["quote"]))
                self.assertTrue(f["period"], r["report_id"])

    def test_features_in_region_and_unexposed(self):
        for r in rows(PART / "features.csv"):
            self.assertIn(r["region_zone"], build_part_d.ZONES)
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertEqual(r["protected_strip"], "no")


class TestOrder(unittest.TestCase):
    def test_reading_follows_frozen_order_without_gaps(self):
        scr = rows(PART / "screen.csv")
        self.assertEqual(len(scr), 582)
        self.assertEqual([int(r["order_position_in_tier"]) for r in scr], list(range(81, 663)))
        frozen = {r["report_id"]: r["order_position_in_tier"] for r in rows(PHASE2 / "online_screen.csv") if r["tier"] == "T3"}
        for r in scr:
            self.assertEqual(frozen[r["report_id"]], r["order_position_in_tier"])
        done = [r["status"] != "not read (time limit)" for r in scr]
        # every handled position comes before every unread one (reading stopped, it did not skip)
        if False in done:
            self.assertNotIn(True, done[done.index(False):])

    def test_phase2_t3_positions_1_to_80_not_recoded(self):
        p2 = {r["report_id"] for r in rows(PHASE2 / "online_screen.csv")
              if r["tier"] == "T3" and int(r["order_position_in_tier"]) <= 80}
        for r in coding():
            self.assertNotIn(r["report_id"].split("-", 1)[1], p2)


class TestReproduce(unittest.TestCase):
    def test_build_reproduces_committed_tables(self):
        with tempfile.TemporaryDirectory() as d:
            build_part_d.main(Path(d))
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(d) / name, PART / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
