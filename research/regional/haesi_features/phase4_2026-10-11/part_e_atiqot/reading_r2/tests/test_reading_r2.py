"""Tests for phase 4, part E, reader r2 (T2 positions 61-135).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/reading_r2/tests
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

R2 = Path(__file__).resolve().parents[1]
PART = R2.parent
PHASE4 = PART.parent
PHASE2 = PHASE4.parent / "phase2_2026-10-10"
sys.path.insert(0, str(R2 / "scripts"))
import build_reading_r2 as b  # noqa: E402

PHASE4_PLAN_SHA256 = "5428c4ccadd6dae0b0df3f4a4030bba9f3626a628377f931ed949fb752e9b2da"  # commit b002e03
PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"  # commit d0f8c7c
OUTPUTS = ["features.csv", "reports.csv", "held.csv", "not_read.csv", "summary.json", "summary.md"]


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


class TestPlans(unittest.TestCase):
    def test_frozen_plan_hashes(self):
        self.assertEqual(hashlib.sha256((PHASE4 / "PLAN.md").read_bytes()).hexdigest(), PHASE4_PLAN_SHA256)
        self.assertEqual(hashlib.sha256((PHASE2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)


class TestSchema(unittest.TestCase):
    def test_columns_match_phase2_exactly(self):
        self.assertEqual(header(R2 / "features.csv"), header(PHASE2 / "features.csv"))
        self.assertEqual(header(R2 / "reports.csv"), header(PHASE2 / "reports.csv"))

    def test_held_columns_match_part_e(self):
        self.assertEqual(header(R2 / "held.csv"), header(PART / "held.csv"))


class TestCoverage(unittest.TestCase):
    def test_every_assigned_unit_is_read_or_listed(self):
        need = [r["unit_id"] for r in b.assigned_units()]
        self.assertEqual(len(need), 75)
        read = {r["report_id"] for r in rows(R2 / "reports.csv")}
        held = {r["unit_id"] for r in rows(R2 / "held.csv")}
        not_read = {r["unit_id"] for r in rows(R2 / "not_read.csv")}
        self.assertEqual(read | held | not_read, set(need))
        self.assertFalse(read & held or read & not_read or held & not_read)

    def test_pdf_hashes_match_the_download_manifest(self):
        dl = {r["file"][:-4]: r["sha256"] for r in rows(PHASE4 / "downloads_2026-10-11.csv")}
        for r in rows(R2 / "data" / "mac_pdf_sha256.csv"):
            self.assertEqual(r["pdf_sha256"], dl[r["unit_id"]], r["unit_id"])

    def test_every_quote_was_located_on_a_pdf_page(self):
        qp = {(r["unit_id"], int(r["feature_index"])): r for r in rows(R2 / "data" / "mac_quote_pages.csv")}
        for u in b.load_coding():
            for i, f in enumerate(u["features"]):
                self.assertIn((u["unit_id"], i), qp)
                self.assertTrue(qp[(u["unit_id"], i)]["pdf_page"].isdigit())
                self.assertLessEqual(len(f["quote"].split()), 12, (u["unit_id"], f["quote"]))


class TestRows(unittest.TestCase):
    def test_values(self):
        for f in rows(R2 / "features.csv"):
            self.assertIn(f["feature_type"], b.CLASSES)
            self.assertIn(f["dated_in_window"], ("yes", "no", "unknown"))
            self.assertEqual(f["exposure_at_freeze"], "unexposed at freeze")
            self.assertEqual(f["protected_strip"], "no")
            self.assertTrue(f["pages"])
        for r in rows(R2 / "reports.csv"):
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertRegex(r["text_sha256"], r"^[0-9a-f]{64}$")

    def test_zones_recomputed_from_coordinates(self):
        params = b.common.plan_params()
        for path in ("features.csv", "reports.csv"):
            for r in rows(R2 / path):
                if r["lat"]:
                    self.assertEqual(b.common.zone_of(float(r["lat"]), float(r["lon"]), params), r["region_zone"],
                                     (path, r["report_id"]))
                else:
                    self.assertTrue(r["coordinate_source"].startswith("name only"))
                    self.assertIn(r["region_zone"], b.ZONES)
                    self.assertEqual(r["distance_km"], "")

    def test_no_held_unit_has_a_feature_row(self):
        held = {r["unit_id"] for r in rows(R2 / "held.csv")}
        for f in rows(R2 / "features.csv"):
            self.assertNotIn(f["report_id"], held)

    def test_n_feature_rows_match(self):
        feats = rows(R2 / "features.csv")
        for r in rows(R2 / "reports.csv"):
            self.assertEqual(int(r["n_feature_rows"]), sum(1 for f in feats if f["report_id"] == r["report_id"]))


class TestReadme(unittest.TestCase):
    def test_readme_counts_match_tables(self):
        text = (R2 / "README.md").read_text(encoding="utf-8")
        feats = rows(R2 / "features.csv")
        reps = rows(R2 / "reports.csv")
        m = re.search(r"Units read: (\d+)\. Held: (\d+)\. Not read: (\d+)\.", text)
        self.assertEqual(tuple(int(x) for x in m.groups()),
                         (len(reps), len(rows(R2 / "held.csv")), len(rows(R2 / "not_read.csv"))))
        m = re.search(r"Feature rows: (\d+) \(yes (\d+) / no (\d+) / unknown (\d+)\)", text)
        w = [f["dated_in_window"] for f in feats]
        self.assertEqual(tuple(int(x) for x in m.groups()), (len(feats), w.count("yes"), w.count("no"), w.count("unknown")))
        for c in b.CLASSES:
            m = re.search(r"\| %s \| (\d+) \| (\d+) / (\d+) / (\d+) \|" % c, text)
            self.assertIsNotNone(m, c)
            sel = [f["dated_in_window"] for f in feats if f["feature_type"] == c and f["region_zone"] == "Z4_JERUSALEM_HILLS"]
            self.assertEqual(tuple(int(x) for x in m.groups()),
                             (len(sel), sel.count("yes"), sel.count("no"), sel.count("unknown")), c)


class TestDeterministic(unittest.TestCase):
    def test_rebuild_identical(self):
        with tempfile.TemporaryDirectory() as d:
            b.build(d)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(d) / name, R2 / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
