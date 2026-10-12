"""Tests for phase 4, part G (QDAP).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_g_qdap/tests
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
PHASE2 = PHASE4.parent / "phase2_2026-10-10"
sys.path.insert(0, str(PART / "scripts"))
import build_part_g  # noqa: E402

common = build_part_g.common
PHASE4_PLAN_SHA256 = "5428c4ccadd6dae0b0df3f4a4030bba9f3626a628377f931ed949fb752e9b2da"  # commit b002e03
PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"  # commit d0f8c7c
OUTPUTS = ["features.csv", "reports.csv", "screen.csv", "held.csv", "summary.md", "summary.json"]
ZONES = set(build_part_g.ZONES)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def units():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((PART / "data" / "units").glob("*.json"))}


class TestPlans(unittest.TestCase):
    def test_frozen_plan_hashes(self):
        self.assertEqual(hashlib.sha256((PHASE4 / "PLAN.md").read_bytes()).hexdigest(), PHASE4_PLAN_SHA256)
        self.assertEqual(hashlib.sha256((PHASE2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)


class TestSchema(unittest.TestCase):
    def test_columns_match_phase2_exactly(self):
        self.assertEqual(header(PART / "features.csv"), header(PHASE2 / "features.csv"))
        self.assertEqual(header(PART / "reports.csv"), header(PHASE2 / "reports.csv"))

    def test_coding_records(self):
        for uid, r in units().items():
            self.assertRegex(uid, r"^QDAP\d{1,2}-\d{3}-[a-z0-9-]+$")
            self.assertRegex(r["text_sha256"], r"^[0-9a-f]{64}$")
            self.assertIsInstance(r["text_chars"], int)
            self.assertEqual(r.get("map_ref", ""), "")
            for f in r["features"]:
                self.assertIn(f["type"], build_part_g.CLASSES)
                self.assertIn(f["window"], ("yes", "no", "unknown"))
                self.assertLessEqual(len(f["quote"].split()), 12, (uid, f["quote"]))
                self.assertTrue(f["period"], uid)

    def test_feature_rows(self):
        for r in rows(PART / "features.csv"):
            self.assertIn(r["region_zone"], ZONES)
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertEqual(r["protected_strip"], "no")
            self.assertLessEqual(len(r["quote"].split()), 12)
        for r in rows(PART / "reports.csv"):
            self.assertEqual(r["exposure_at_freeze"], "unexposed at freeze")
            self.assertIn(r["tier"], ("T1", "T2", "T3"))


class TestZones(unittest.TestCase):
    def test_zone_recomputed_from_coordinates(self):
        """Any row with coordinates must sit in the zone the frozen boxes give (QDAP rows are name-only)."""
        params = common.plan_params()
        for r in rows(PART / "features.csv") + rows(PART / "reports.csv"):
            if r["lat"] and r["lon"]:
                self.assertEqual(common.zone_of(float(r["lat"]), float(r["lon"]), params), r["region_zone"])
            else:
                self.assertTrue(r["coordinate_source"].startswith("name only"))

    def test_gazetteer_screen_units_take_a_zone_their_title_names(self):
        pats = common.gazetteer_patterns()
        for uid, r in units().items():
            if r["screen"] == "S-G":
                hits = common.title_hits(r["title"], pats)
                self.assertIn(r["name_zone"], hits, uid)

    def test_tier_rule(self):
        for uid, r in units().items():
            title = build_part_g.unit_title_for_tier(r)
            self.assertEqual(build_part_g.tier_of(r["name_zone"], title), r["tier"], uid)


class TestHeld(unittest.TestCase):
    def test_no_held_unit_has_a_feature_or_report_row(self):
        held = {r["unit_id"] for r in rows(PART / "held.csv")}
        self.assertTrue(held)
        self.assertFalse(held & {r["report_id"] for r in rows(PART / "features.csv")})
        self.assertFalse(held & {r["report_id"] for r in rows(PART / "reports.csv")})
        self.assertFalse(held & set(units()))
        for r in rows(PART / "held.csv"):
            self.assertLessEqual(len(r["first_line_seen"].split()), 12)

    def test_screen_accounts_for_every_unit(self):
        scr = rows(PART / "screen.csv")
        ids = [r["unit_id"] for r in scr]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual({r["coded_report_id"] for r in scr if r["decision"] == "IN"}, set(units()))
        self.assertEqual({r["unit_id"] for r in scr if r["decision"] == "HELD"},
                         {r["unit_id"] for r in rows(PART / "held.csv")})
        for r in scr:
            if r["decision"] == "IN":
                self.assertEqual(r["status"], "read")


class TestOrder(unittest.TestCase):
    def test_reading_order_is_sha256_within_tier(self):
        scr = [r for r in rows(PART / "screen.csv") if r["tier"]]
        for t in ("T1", "T2", "T3"):
            tier = sorted((r for r in scr if r["tier"] == t), key=lambda r: int(r["order_position_in_tier"]))
            ids = [r["unit_id"] for r in tier]
            self.assertEqual(ids, sorted(ids, key=lambda u: hashlib.sha256(u.encode()).hexdigest()))
            self.assertEqual([int(r["order_position_in_tier"]) for r in tier], list(range(1, len(tier) + 1)))
        self.assertFalse([r for r in scr if r["status"].startswith("not read")])


class TestReadme(unittest.TestCase):
    def test_readme_counts_match_tables(self):
        text = (PART / "README.md").read_text(encoding="utf-8")
        js = json.loads((PART / "summary.json").read_text(encoding="utf-8"))
        feats = rows(PART / "features.csv")
        reps = rows(PART / "reports.csv")
        held = rows(PART / "held.csv")
        scr = rows(PART / "screen.csv")
        m = re.search(r"Units screened: (\d+)", text)
        self.assertEqual(int(m.group(1)), len(scr))
        m = re.search(r"Units read and coded: (\d+)", text)
        self.assertEqual(int(m.group(1)), len(reps))
        m = re.search(r"Feature rows: (\d+) \(yes (\d+), no (\d+), unknown (\d+)\)", text)
        self.assertEqual(int(m.group(1)), len(feats))
        for k, g in (("yes", 2), ("no", 3), ("unknown", 4)):
            self.assertEqual(int(m.group(g)), sum(1 for f in feats if f["dated_in_window"] == k))
        m = re.search(r"Held or protected: (\d+)", text)
        self.assertEqual(int(m.group(1)), len(held))
        for c, v in js["by_class"].items():
            mm = re.search(r"\| %s \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|" % c, text)
            self.assertIsNotNone(mm, c)
            self.assertEqual([int(x) for x in mm.groups()], [v["rows"], v["yes"], v["no"], v["unknown"]], c)
        for z, v in js["by_zone"].items():
            mm = re.search(r"\| %s \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|" % z, text)
            self.assertIsNotNone(mm, z)
            self.assertEqual([int(x) for x in mm.groups()], [v["rows"], v["yes"], v["no"], v["unknown"]], z)


class TestReproduce(unittest.TestCase):
    def test_build_reproduces_committed_tables(self):
        with tempfile.TemporaryDirectory() as d:
            build_part_g.build(Path(d))
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(d) / name, PART / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
