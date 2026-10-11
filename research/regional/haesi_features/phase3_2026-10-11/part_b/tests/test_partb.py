"""Tests for HA-ESI phase 3, part B (HA Hebrew volumes 1980-1998).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase3_2026-10-11/part_b/tests
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

PARTB = Path(__file__).resolve().parents[1]
PHASE3 = PARTB.parent
LANE = PHASE3.parent
PHASE2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(PARTB / "scripts"))
import build_partb  # noqa: E402

PHASE3_PLAN_SHA256 = "312c27332bbc4d9b9d3405d88cb8d9d40e8e361714cdd5582997467593055cf2"  # commit 4d8325e
PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"
OUTPUTS = ["features.csv", "reports.csv", "screen.csv", "candidates_checkoff.csv", "already_coded_crosswalk.csv",
           "body_headings.csv", "summary.md", "summary.json"]


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def coding_records():
    out = []
    for p in sorted((PARTB / "data" / "coding").glob("*.json")):
        out.extend(json.loads(p.read_text(encoding="utf-8")))
    return out


def decisions():
    out = []
    for p in sorted((PARTB / "data" / "decisions").glob("*.csv")):
        for r in rows(p):
            assert len(r) == 4 and None not in r, (p.name, r)
            out.append(r)
    return out


class TestPlans(unittest.TestCase):
    def test_plan_hashes(self):
        self.assertEqual(hashlib.sha256((PHASE3 / "PLAN.md").read_bytes()).hexdigest(), PHASE3_PLAN_SHA256)
        self.assertEqual(hashlib.sha256((PHASE2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)

    def test_part_b_volumes_match_partition(self):
        part = {(r["local_file"], r["sha256"]) for r in rows(PHASE3 / "partition.csv") if r["part"] == "B"}
        vols = {(r["local_file"], r["pdf_sha256"]) for r in rows(PARTB / "data" / "volumes.csv")}
        self.assertEqual(len(part), 32)
        self.assertEqual(vols, part)


class TestSchema(unittest.TestCase):
    def test_features_columns_match_phase2(self):
        self.assertEqual(header(PARTB / "features.csv"), header(PHASE2 / "features.csv"))

    def test_reports_columns_match_phase2(self):
        self.assertEqual(header(PARTB / "reports.csv"), header(PHASE2 / "reports.csv"))

    def test_feature_values(self):
        rids = {r["report_id"] for r in rows(PARTB / "reports.csv")}
        for r in rows(PARTB / "features.csv"):
            self.assertIn(r["report_id"], rids)
            self.assertIn(r["feature_type"], build_partb.CLASSES)
            self.assertIn(r["dated_in_window"], ("yes", "no", "unknown"))
            self.assertIn(r["region_zone"], build_partb.ZONES)
            self.assertLessEqual(len(r["quote"].split()), 12, r["quote"])
            if r["lat"]:
                self.assertIn(r["crs_used"], ("EPSG:28191", "EPSG:2039"))


class TestCodingAndDecisions(unittest.TestCase):
    def test_decisions_reference_screen_ids(self):
        sids = {r["screen_id"] for r in rows(PARTB / "data" / "screen_auto.csv")}
        seen = set()
        for r in decisions():
            self.assertIn(r["screen_id"], sids)
            self.assertNotIn(r["screen_id"], seen)
            seen.add(r["screen_id"])
            self.assertIn(r["decision"], build_partb.DECISIONS)

    def test_one_read_decision_per_coded_report(self):
        recs = coding_records()
        ids = [r["report_id"] for r in recs]
        self.assertEqual(len(ids), len(set(ids)))
        read = [r["report_id"] for r in decisions() if r["decision"] == "read"]
        self.assertEqual(sorted(read), sorted(ids))

    def test_quotes_short_and_found(self):
        spans = {r["report_id"]: r for r in rows(PARTB / "data" / "spans.csv")}
        for r in coding_records():
            for f in r["features"]:
                self.assertTrue(f["quote"].strip())
                self.assertLessEqual(len(f["quote"].split()), 12, (r["report_id"], f["quote"]))
            for q in r.get("extra_quotes", []):
                self.assertLessEqual(len(q.split()), 12, (r["report_id"], q))
            sp = spans[r["report_id"]]
            self.assertEqual(sp["quotes_not_found"], "", r["report_id"])
            self.assertRegex(sp["text_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(sp["text_lines"], r["text_lines"])

    def test_held_and_protected(self):
        """Held cave reports are not coded; Tier-1 Kh. 'Almit stays in its extraction file only."""
        held = [r for r in decisions() if r["decision"].startswith("held")]
        self.assertTrue(held)
        for r in held:
            self.assertEqual(r["report_id"], "")
        for r in coding_records():
            self.assertNotRegex(r["title"], r"(?i)almit|עלמית")
        self.assertTrue((PARTB / "tier1_kh_almit_extraction.md").exists())

    def test_no_full_text_in_repository(self):
        for p in PARTB.rglob("*"):
            if p.is_file():
                self.assertNotRegex(p.name, r"\.(pdf|txt|png|jpe?g|tiff?)$", p)
                self.assertLess(p.stat().st_size, 2_000_000, p)
        for r in rows(PARTB / "data" / "volumes.csv"):
            self.assertRegex(r["local_file"], r"^IAA_HA_[0-9-]+_\d{4}\.pdf$")
            self.assertRegex(r["pdf_sha256"], r"^[0-9a-f]{64}$")


class TestScreen(unittest.TestCase):
    def test_every_heading_has_a_decision(self):
        for r in rows(PARTB / "screen.csv"):
            self.assertTrue(r["decision"], r["screen_id"])
            self.assertNotEqual(r["decision_basis"], "flagged; no decision", r["screen_id"])

    def test_every_candidate_accounted_for(self):
        sids = {r["screen_id"] for r in rows(PARTB / "screen.csv")}
        for r in rows(PARTB / "candidates_checkoff.csv"):
            self.assertIn(r["screen_id"], sids, r["item_key"])
            self.assertNotEqual(r["outcome"], "not found in the volume", r["item_key"])

    def test_screen_ids_well_formed(self):
        for r in rows(PARTB / "screen.csv"):
            self.assertRegex(r["screen_id"], r"^HA\d{2,3}-p?\d{3}-\d+$")


class TestReproduce(unittest.TestCase):
    def test_build_reproduces_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            build_partb.main(d)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(d) / name, PARTB / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
