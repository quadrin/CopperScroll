"""Tests for HA-ESI phase 3, part C.

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase3_2026-10-11/part_c/tests
"""
import csv
import filecmp
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PART = Path(__file__).resolve().parents[1]
PHASE3 = PART.parent
LANE = PHASE3.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(PART / "scripts"))
import build_part_c  # noqa: E402

PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"
PHASE3_PLAN_SHA256 = "312c27332bbc4d9b9d3405d88cb8d9d40e8e361714cdd5582997467593055cf2"
TIER1_COMMIT = "d431dfd"
OUTPUTS = ["features.csv", "reports.csv", "screen.csv", "candidates_checkoff.csv", "summary.md", "summary.json"]
CLASSES = set(build_part_c.CLASSES)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def coding_records():
    out = []
    for p in sorted((PART / "data").glob("coding_*.json")):
        out.extend(json.loads(p.read_text(encoding="utf-8")))
    return out


class TestPlans(unittest.TestCase):
    def test_phase2_plan_hash(self):
        self.assertEqual(hashlib.sha256((P2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)

    def test_phase3_plan_hash(self):
        self.assertEqual(hashlib.sha256((PHASE3 / "PLAN.md").read_bytes()).hexdigest(), PHASE3_PLAN_SHA256)

    def test_tier1_extraction_committed_alone(self):
        try:
            out = subprocess.run(["git", "-C", str(PART), "show", "--name-only", "--format=", TIER1_COMMIT],
                                 capture_output=True, text=True, check=True).stdout.split()
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("git history not available")
        self.assertEqual(out, ["research/regional/haesi_features/phase3_2026-10-11/part_c/tier1_kh_almit_extraction.md"])


class TestSchema(unittest.TestCase):
    def test_columns_match_phase2(self):
        self.assertEqual(header(PART / "features.csv"), header(P2 / "features.csv"))
        self.assertEqual(header(PART / "reports.csv"), header(P2 / "reports.csv"))

    def test_coding_values(self):
        recs = coding_records()
        ids = [r["report_id"] for r in recs]
        self.assertEqual(len(ids), len(set(ids)))
        for r in recs:
            self.assertRegex(r["report_id"], r"^(ESI\d\d|HAESI1\d\d)-\d{3}-[a-z0-9-]+$")
            for f in r["features"]:
                self.assertIn(f["type"], CLASSES, r["report_id"])
                self.assertIn(f["window"], ("yes", "no", "unknown"), r["report_id"])
                self.assertTrue(f["quote"], r["report_id"])
                self.assertLessEqual(len(f["quote"].split()), 12, (r["report_id"], f["quote"]))

    def test_every_record_has_a_verified_span(self):
        spans = {s["report_id"]: s for s in rows(PART / "data" / "local_spans.csv")}
        for r in coding_records():
            s = spans[r["report_id"]]
            self.assertEqual(s["text_lines"], r["text_lines"], r["report_id"])
            self.assertEqual(s["quotes_not_found"], "", r["report_id"])
            self.assertEqual(int(s["n_quotes"]), sum(1 for f in r["features"] if f.get("quote")), r["report_id"])
            self.assertRegex(s["text_sha256"], r"^[0-9a-f]{64}$")

    def test_sources_cover_all_19_volumes(self):
        src = rows(PART / "data" / "local_sources.csv")
        self.assertEqual(sorted(s["text_file"] for s in src), sorted(build_part_c.VOLS))
        part = {r["local_file"]: r["sha256"] for r in rows(PHASE3 / "partition.csv") if r["part"] == "C"}
        for s in src:
            self.assertEqual(part[s["local_file_name"]], s["pdf_sha256"])


class TestOutputs(unittest.TestCase):
    def test_build_reproduces_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_part_c.main(tmp)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(tmp) / name, PART / name, shallow=False), name)

    def test_screen_accounts_for_every_heading(self):
        sc = rows(PART / "screen.csv")
        for s in sc:
            self.assertTrue(s["final_decision"], (s["vol"], s["heading_line"], s["title"]))
            if s["final_decision"].startswith("in region"):
                self.assertTrue(s["coded_report_ids"], (s["vol"], s["heading_line"], s["title"]))
        held = [s for s in sc if s["status"].startswith("held")]
        self.assertEqual([(s["vol"], s["title"]) for s in held], [("ESI13", "Qumran Caves")])

    def test_held_report_not_in_tables(self):
        held = {r["report_id"] for r in coding_records() if r.get("held")}
        self.assertTrue(held)
        self.assertFalse(held & {r["report_id"] for r in rows(PART / "reports.csv")})
        self.assertFalse(held & {r["report_id"] for r in rows(PART / "features.csv")})

    def test_every_phase1_candidate_accounted_for(self):
        ck = rows(PART / "candidates_checkoff.csv")
        self.assertEqual(len(ck), 202)
        self.assertEqual(len({c["item_key"] for c in ck}), 202)
        for c in ck:
            self.assertNotEqual(c["status"], "not found in the volume", c["item_key"])
            if c["status"] == "read and coded":
                self.assertTrue(c["report_ids"], c["item_key"])

    def test_features_in_region(self):
        for f in rows(PART / "features.csv"):
            self.assertIn(f["region_zone"], build_part_c.ZONES, f["report_id"])


if __name__ == "__main__":
    unittest.main()
