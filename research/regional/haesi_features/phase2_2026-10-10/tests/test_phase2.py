"""Tests for HA-ESI phase 2.

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase2_2026-10-10/tests
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

LANE = Path(__file__).resolve().parents[1]
PHASE1 = LANE.parent
sys.path.insert(0, str(LANE / "scripts"))
import build_phase2  # noqa: E402
import common  # noqa: E402

FROZEN_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"
OUTPUTS = ["features.csv", "reports.csv", "online_screen.csv", "phase1_zone_crosswalk.csv", "looks_haesi_phase2.csv",
           "summary.md", "summary.json"]


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def coding_records():
    out = []
    for p in sorted((LANE / "data").glob("coding_*.json")):
        out.extend(json.loads(p.read_text(encoding="utf-8")))
    return out


class TestPlan(unittest.TestCase):
    def test_plan_hash_is_frozen_value_and_in_readme(self):
        h = hashlib.sha256((LANE / "PLAN.md").read_bytes()).hexdigest()
        self.assertEqual(h, FROZEN_PLAN_SHA256)
        readme = (LANE / "README.md").read_text(encoding="utf-8")
        self.assertIn(FROZEN_PLAN_SHA256, readme)

    def test_plan_parameters_parse(self):
        p = common.plan_params()
        self.assertEqual(p["zones_order"][0], "Z1_GERIZIM")
        self.assertEqual(set(p["zones"]), {"Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"})


class TestSchema(unittest.TestCase):
    def test_features_columns(self):
        self.assertEqual(header(LANE / "features.csv"),
                         header(PHASE1 / "features.csv") + ["region_zone", "dist_to_nearest_place_km", "feature_subtype",
                                                            "exposure_at_freeze"])

    def test_reports_columns(self):
        self.assertEqual(header(LANE / "reports.csv"),
                         header(PHASE1 / "reports.csv") + ["region_zone", "dist_to_nearest_place_km", "exposure_at_freeze",
                                                           "tier"])

    def test_looks_columns(self):
        self.assertEqual(header(LANE / "looks_haesi_phase2.csv"), header(PHASE1 / "looks_haesi.csv"))

    def test_feature_values(self):
        for r in rows(LANE / "features.csv"):
            self.assertIn(r["feature_type"], build_phase2.CLASSES)
            self.assertIn(r["dated_in_window"], ("yes", "no", "unknown"))
            self.assertIn(r["region_zone"], build_phase2.ZONES)
            self.assertLessEqual(len(r["quote"].split()), 12, r["quote"])

    def test_feature_reports_exist(self):
        rids = {r["report_id"] for r in rows(LANE / "reports.csv")}
        for r in rows(LANE / "features.csv"):
            self.assertIn(r["report_id"], rids)


class TestCoding(unittest.TestCase):
    def test_unique_ids_and_quotes(self):
        recs = coding_records()
        ids = [r["report_id"] for r in recs]
        self.assertEqual(len(ids), len(set(ids)))
        for r in recs:
            for f in r["features"]:
                self.assertLessEqual(len(f["quote"].split()), 12, (r["report_id"], f["quote"]))
                self.assertTrue(f["quote"].strip())

    def test_local_spans_cover_local_records(self):
        spans = {r["report_id"]: r for r in rows(LANE / "data" / "local_spans.csv")}
        for r in coding_records():
            if r["report_id"].startswith("HAESI-"):
                self.assertRegex(r["text_sha256"], r"^[0-9a-f]{64}$")
                continue
            self.assertIn(r["report_id"], spans)
            self.assertEqual(spans[r["report_id"]]["quotes_not_found"], "")
            self.assertRegex(spans[r["report_id"]]["text_sha256"], r"^[0-9a-f]{64}$")

    def test_online_records_are_candidates(self):
        cands = {r["report_id"] for r in rows(LANE / "data" / "online_candidates.csv")}
        for r in coding_records():
            if r["report_id"].startswith("HAESI-"):
                self.assertIn(r["report_id"].split("-", 1)[1], cands)

    def test_status_rows_are_candidates(self):
        cands = {r["report_id"] for r in rows(LANE / "data" / "online_candidates.csv")}
        for r in rows(LANE / "data" / "online_status.csv"):
            self.assertIn(r["report_id"], cands)


class TestScreen(unittest.TestCase):
    def test_online_list_counts(self):
        lists = rows(LANE / "data" / "online_lists.csv")
        titles = rows(LANE / "data" / "online_titles.csv")
        self.assertEqual(sum(int(r["n_reports"]) for r in lists), len(titles))
        self.assertEqual(len(titles), 4667)

    def test_screen_rows(self):
        srows = rows(LANE / "online_screen.csv")
        self.assertEqual(len(srows), len(rows(LANE / "data" / "online_candidates.csv")))
        for t in ("T1", "T2", "T3"):
            pos = sorted(int(r["order_position_in_tier"]) for r in srows if r["tier"] == t)
            self.assertEqual(pos, list(range(1, len(pos) + 1)))

    def test_reading_order_is_hash_order(self):
        srows = rows(LANE / "online_screen.csv")
        for t in ("T1", "T2", "T3"):
            tier = sorted((r for r in srows if r["tier"] == t), key=lambda r: int(r["order_position_in_tier"]))
            keys = [hashlib.sha256(r["report_id"].encode()).hexdigest() for r in tier]
            self.assertEqual(keys, sorted(keys))

    def test_no_unread_before_read_in_tier(self):
        """Within a tier, reading stopped at one position: nothing is 'not read' before a read item."""
        srows = rows(LANE / "online_screen.csv")
        for t in ("T1", "T2", "T3"):
            tier = sorted((r for r in srows if r["tier"] == t), key=lambda r: int(r["order_position_in_tier"]))
            seen_unread = False
            for r in tier:
                if r["status"].startswith("not read"):
                    seen_unread = True
                elif seen_unread:
                    self.fail("tier %s: %s handled after an unread item" % (t, r["report_id"]))


class TestReproduce(unittest.TestCase):
    def test_build_reproduces_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            build_phase2.main(d)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(d) / name, LANE / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
