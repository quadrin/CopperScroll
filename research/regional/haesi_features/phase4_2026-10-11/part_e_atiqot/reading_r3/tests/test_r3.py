"""Tests for phase 4, part E, reader r3 (ʿAtiqot T2 positions 136-208).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/reading_r3/tests
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

R3 = Path(__file__).resolve().parents[1]
PART = R3.parent
PHASE4 = PART.parent
LANE = PHASE4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(R3 / "scripts"))
import build_r3  # noqa: E402
import common  # noqa: E402  (put on sys.path by build_r3)
import geo  # noqa: E402

PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"
OUTPUTS = ["reports.csv", "features.csv", "held.csv", "not_read.csv", "summary.json"]


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


class TestR3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reports = rows(R3 / "reports.csv")
        cls.features = rows(R3 / "features.csv")
        cls.held = rows(R3 / "held.csv")
        cls.not_read = rows(R3 / "not_read.csv")
        cls.summary = json.loads((R3 / "summary.json").read_text(encoding="utf-8"))
        cls.params = common.plan_params()

    def test_phase2_plan_unchanged(self):
        self.assertEqual(hashlib.sha256((P2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)

    def test_column_order_matches_phase2(self):
        self.assertEqual(header(R3 / "features.csv"), header(P2 / "features.csv"))
        self.assertEqual(header(R3 / "reports.csv"), header(P2 / "reports.csv"))
        self.assertEqual(header(R3 / "held.csv"), header(PART / "held.csv"))

    def test_all_assigned_units_accounted_for(self):
        assigned = [r["unit_id"] for r in build_r3.assigned_units()]
        self.assertEqual(len(assigned), 73)
        done = {r["report_id"] for r in self.reports} | {r["unit_id"] for r in self.not_read} | \
               {r["unit_id"] for r in self.held}
        self.assertEqual(set(assigned), done)
        self.assertTrue(all(r["tier"].startswith("T2 #") for r in self.reports))

    def test_zones_recomputed_from_coordinates(self):
        for r in self.features + self.reports:
            if r["lat"]:
                z = common.zone_of(float(r["lat"]), float(r["lon"]), self.params)
                self.assertEqual(z, r["region_zone"], r["report_id"])
                ref = geo.parse_ref(r["map_ref_as_given"])
                lat, lon = geo.to_wgs84(ref["e"], ref["n"], ref["grid"])
                self.assertAlmostEqual(lat, float(r["lat"]), places=4)
                self.assertAlmostEqual(lon, float(r["lon"]), places=4)
            else:
                self.assertIn(r["region_zone"], build_r3.ZONES, r["report_id"])
                self.assertTrue(r["coordinate_source"].startswith("name only"), r["report_id"])

    def test_no_held_unit_has_feature_rows(self):
        held = {r["unit_id"] for r in self.held}
        self.assertFalse(held & {r["report_id"] for r in self.features})
        self.assertFalse(held & {r["report_id"] for r in self.reports})

    def test_coding_rules(self):
        for r in self.features:
            self.assertIn(r["feature_type"], build_r3.CLASSES)
            self.assertIn(r["dated_in_window"], ("yes", "no", "unknown"))
            self.assertLessEqual(len(r["quote"].split()), 12, r["quote"])
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertEqual(r["protected_strip"], "no")
        for r in self.reports:
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertRegex(r["text_sha256"], r"^[0-9a-f]{64}$")
            n = sum(1 for f in self.features if f["report_id"] == r["report_id"])
            self.assertEqual(int(r["n_feature_rows"]), n, r["report_id"])

    def test_quotes_verified_on_source_text(self):
        for line in (R3 / "data" / "spans_r3.jsonl").read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            for q in d["quotes"]:
                self.assertIn(q, ("exact", "dehyph", "nospace", "tokens"), d["unit"])

    def test_readme_counts_match_tables(self):
        text = (R3 / "README.md").read_text(encoding="utf-8")
        m = re.search(r"Units read: (\d+) of (\d+)\. Feature rows: (\d+)\.", text)
        self.assertIsNotNone(m, "README count line missing")
        self.assertEqual(int(m.group(1)), len(self.reports))
        self.assertEqual(int(m.group(2)), 73)
        self.assertEqual(int(m.group(3)), len(self.features))
        by = {}
        for r in self.features:
            by.setdefault(r["feature_type"], Counter())[r["dated_in_window"]] += 1
        for cls, c in by.items():
            pat = r"\| %s \| Z4 \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|" % re.escape(cls)
            mm = re.search(pat, text)
            self.assertIsNotNone(mm, cls)
            self.assertEqual([int(x) for x in mm.groups()],
                             [sum(c.values()), c["yes"], c["no"], c["unknown"]], cls)
        self.assertEqual(self.summary["feature_rows"], len(self.features))

    def test_rebuild_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            build_r3.build(tmp)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(tmp) / name, R3 / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
