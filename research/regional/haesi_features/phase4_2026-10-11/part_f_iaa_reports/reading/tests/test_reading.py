"""Tests for the phase-4 part F reading pass (reader r4).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_f_iaa_reports/reading/tests
"""
import csv
import filecmp
import hashlib
import json
import re
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

READ = Path(__file__).resolve().parents[1]
PART = READ.parent
PHASE4 = PART.parent
LANE = PHASE4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(READ / "scripts"))
import build_reading  # noqa: E402
import common  # noqa: E402  (phase-2 helpers, put on sys.path by build_reading)

PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"
OUTPUTS = ["features.csv", "reports.csv", "not_read.csv", "summary.json"]


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


class TestReading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.features = rows(READ / "features.csv")
        cls.reports = rows(READ / "reports.csv")
        cls.coding = json.loads((READ / "data" / "coding.json").read_text(encoding="utf-8"))
        cls.needed = rows(PART / "pdfs_needed.csv")
        cls.params = common.plan_params()

    def test_phase2_plan_unchanged(self):
        self.assertEqual(hashlib.sha256((P2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)

    def test_columns_match_phase2(self):
        self.assertEqual(header(READ / "features.csv"), header(P2 / "features.csv"))
        self.assertEqual(header(READ / "reports.csv"), header(P2 / "reports.csv"))
        self.assertEqual(header(READ / "held.csv"), header(PART / "held.csv"))

    def test_unit_ids_and_reading_order(self):
        ids = [r["unit_id"] for r in self.needed]
        self.assertEqual(len(ids), 12)
        self.assertEqual({r["report_id"] for r in self.reports}, set(ids))
        # the coding follows the frozen order (tier, then position in tier)
        order = sorted(self.needed, key=lambda r: (r["tier"], int(r["order_within_tier"])))
        self.assertEqual([r["report_id"] for r in self.coding], [r["unit_id"] for r in order])

    def test_coding_values(self):
        for r in self.features:
            self.assertIn(r["feature_type"], build_reading.CLASSES)
            self.assertIn(r["dated_in_window"], ("yes", "no", "unknown"))
            self.assertLessEqual(len(r["quote"].split()), 12, r["quote"])
            self.assertTrue(r["quote"].strip())
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertEqual(r["protected_strip"], "no")
        for r in self.reports:
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertRegex(r["text_sha256"], r"^[0-9a-f]{64}$")

    def test_spans_verified(self):
        spans = {r["report_id"]: r for r in rows(READ / "data" / "spans.csv")}
        dl = {r["file"]: r["sha256"] for r in rows(PHASE4 / "downloads_2026-10-11.csv")}
        for rep in self.coding:
            sp = spans[rep["report_id"]]
            self.assertEqual(int(sp["quotes_checked"]), len(rep["features"]))
            self.assertEqual(sp["quotes_checked"], sp["quotes_found_verbatim"])
            self.assertEqual(sp["pdf_pages_hashed"], rep["pdf_pages"])
            # the PDF read is the one in the phase-4 download manifest
            self.assertEqual(dl[rep["report_id"] + ".pdf"], sp["pdf_sha256"], rep["report_id"])

    def test_zones_recomputed_from_coordinates(self):
        for r in self.reports + self.features:
            if r["lat"]:
                z = common.zone_of(float(r["lat"]), float(r["lon"]), self.params)
                self.assertEqual(z, r["region_zone"], r["report_id"])
            else:
                self.assertTrue(r["coordinate_source"].startswith("name only"), r["report_id"])
                self.assertIn(r["region_zone"], build_reading.ZONES)

    def test_no_held_unit_coded(self):
        held_ids = {r["unit_id"] for r in rows(PART / "held.csv")} | {r["unit_id"] for r in rows(READ / "held.csv")}
        self.assertTrue(held_ids)  # part F holds IAAR5 (Cave of the Warrior)
        coded = {r["report_id"] for r in self.features} | {r["report_id"] for r in self.reports}
        self.assertFalse(held_ids & coded)

    def test_readme_counts_match_tables(self):
        readme = (READ / "README.md").read_text(encoding="utf-8")
        m = re.search(r"Units read: (\d+)", readme)
        self.assertEqual(int(m.group(1)), len(self.reports))
        m = re.search(r"Feature rows: (\d+) \(yes (\d+) / no (\d+) / unknown (\d+)\)", readme)
        c = Counter(r["dated_in_window"] for r in self.features)
        self.assertEqual([int(x) for x in m.groups()], [len(self.features), c["yes"], c["no"], c["unknown"]])
        by = Counter((r["feature_type"], r["region_zone"], r["dated_in_window"]) for r in self.features)
        for cls, zone, n, y, no, u in re.findall(
                r"^\| (\w+) \| (Z\d_[A-Z_]+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$", readme, re.M):
            self.assertEqual(int(y), by[(cls, zone, "yes")], cls)
            self.assertEqual(int(no), by[(cls, zone, "no")], cls)
            self.assertEqual(int(u), by[(cls, zone, "unknown")], cls)
            self.assertEqual(int(n), int(y) + int(no) + int(u))
        listed = re.findall(r"^\| (\w+) \| (Z\d_[A-Z_]+) \|", readme, re.M)
        self.assertEqual(len(listed), len({(r["feature_type"], r["region_zone"]) for r in self.features}))

    def test_build_reproduces_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            build_reading.main(td)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(td) / name, READ / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
