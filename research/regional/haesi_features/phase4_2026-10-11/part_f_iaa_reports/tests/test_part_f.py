"""Tests for phase 4, part F (IAA Reports nos. 2-6 and 8-78): screen, held list and PDF list.

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_f_iaa_reports/tests
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
P4 = PART.parent
LANE = P4.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(PART / "scripts"))
import build_part_f  # noqa: E402
import common_f  # noqa: E402

PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"
PHASE4_PLAN_SHA256 = "5428c4ccadd6dae0b0df3f4a4030bba9f3626a628377f931ed949fb752e9b2da"
OUTPUTS = ["screen.csv", "held.csv", "pdfs_needed.csv", "reports.csv", "features.csv", "summary.json"]
ZONES = {"Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


class TestFrozenInputs(unittest.TestCase):
    def test_plans_unchanged(self):
        self.assertEqual(hashlib.sha256((P2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)
        self.assertEqual(hashlib.sha256((P4 / "PLAN.md").read_bytes()).hexdigest(), PHASE4_PLAN_SHA256)


class TestSchema(unittest.TestCase):
    def test_columns_equal_phase2(self):
        self.assertEqual(header(PART / "features.csv"), header(P2 / "features.csv"))
        self.assertEqual(header(PART / "reports.csv"), header(P2 / "reports.csv"))

    def test_reports_and_features_empty_in_this_pass(self):
        self.assertEqual(rows(PART / "reports.csv"), [])
        self.assertEqual(rows(PART / "features.csv"), [])


class TestScreen(unittest.TestCase):
    def test_every_number_screened_once(self):
        scr = rows(PART / "screen.csv")
        nos = [r["no_label"] for r in scr]
        self.assertEqual(len(nos), len(set(nos)))
        self.assertEqual({int(n.split("/")[0]) for n in nos}, set(range(1, 79)))
        self.assertEqual(len({r["unit_id"] for r in scr}), len(scr))
        for r in scr:
            self.assertRegex(r["unit_id"], r"^IAAR\d{1,2}(p\d)?-[a-z0-9-]+$")
            self.assertTrue(r["decision"], r["unit_id"])

    def test_1_and_7_already_read_not_rescreened(self):
        scr = {r["no_label"]: r for r in rows(PART / "screen.csv")}
        for n in ("1", "7"):
            self.assertTrue(scr[n]["decision"].startswith("ALREADY_READ"))
            self.assertEqual(scr[n]["pdf_url"], "")

    def test_title_hits_recomputed(self):
        pats = common_f.patterns()
        for r in rows(PART / "screen.csv"):
            self.assertEqual(r["title_hits"], common_f.fmt_hits(common_f.hits(r["title"], pats)), r["unit_id"])
            if r["decision"] == "OUT_TITLE":
                self.assertEqual(r["title_hits"], "", r["unit_id"])
                self.assertEqual(r["chapter_title_hits"], "", r["unit_id"])

    def test_zone_by_name_and_tier(self):
        """No landing page gives a map reference: zones come from the title's gazetteer terms (plan section 2)."""
        pats = common_f.patterns()
        for r in rows(PART / "screen.csv"):
            if not r["decision"].startswith("CANDIDATE"):
                continue
            self.assertEqual(r["coordinate_source"], "name only")
            zones = {z for z, _, _ in common_f.hits(r["title"], pats)} - {"REGION_WIDE"}
            self.assertEqual(zones, {r["region_zone"]}, r["unit_id"])
            self.assertIn(r["region_zone"], ZONES)
            self.assertEqual(r["tier"], build_part_f.tier_of(r["region_zone"], r["title"]))

    def test_no_coordinates_invented(self):
        for r in rows(PART / "screen.csv"):
            self.assertEqual(r["pages"], "")
        for r in rows(PART / "pdfs_needed.csv"):
            self.assertEqual(r["pages"], "")


class TestHeldAndPdfs(unittest.TestCase):
    def test_no_held_unit_coded_or_requested(self):
        held = {r["unit_id"] for r in rows(PART / "held.csv")}
        self.assertTrue(held)
        self.assertFalse(held & {r["report_id"] for r in rows(PART / "features.csv")})
        self.assertFalse(held & {r["report_id"] for r in rows(PART / "reports.csv")})
        self.assertFalse(held & {r["unit_id"] for r in rows(PART / "pdfs_needed.csv")})
        for r in rows(PART / "held.csv"):
            self.assertEqual(r["protected_strip"], "no")

    def test_pdfs_needed_are_the_candidates_in_frozen_order(self):
        scr = rows(PART / "screen.csv")
        cands = {r["unit_id"]: r for r in scr if r["decision"].startswith("CANDIDATE")}
        need = rows(PART / "pdfs_needed.csv")
        self.assertEqual({r["unit_id"] for r in need}, set(cands))
        key = [(r["tier"], hashlib.sha256(r["unit_id"].encode()).hexdigest()) for r in need]
        self.assertEqual(key, sorted(key))
        for r in need:
            self.assertEqual(r["sha256_unit_id"], hashlib.sha256(r["unit_id"].encode()).hexdigest())
            self.assertRegex(r["pdf_url"], r"^https://publications\.iaa\.org\.il/cgi/viewcontent\.cgi\?article=\d+&context=iaareports$")
            self.assertEqual(r["pdf_url"], cands[r["unit_id"]]["pdf_url"])

    def test_no_tier1_extraction_without_almit(self):
        for r in rows(PART / "screen.csv"):
            self.assertNotIn("almit", common_f.norm(r["title"]))
        self.assertFalse((PART / "tier1_kh_almit_extraction.md").exists())


class TestOutputs(unittest.TestCase):
    def test_rebuild_is_identical(self):
        with tempfile.TemporaryDirectory() as d:
            build_part_f.main(d)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(d) / name, PART / name, shallow=False), name)

    def test_readme_counts_match_tables(self):
        s = json.loads((PART / "summary.json").read_text(encoding="utf-8"))
        t = (PART / "README.md").read_text(encoding="utf-8")
        need = rows(PART / "pdfs_needed.csv")
        scr = rows(PART / "screen.csv")
        held = rows(PART / "held.csv")
        self.assertEqual(s["portal_items"], len(scr))
        self.assertIn("Portal items screened: %d" % len(scr), t)
        self.assertIn("Candidates in the region: %d" % len(need), t)
        for tier in ("T1", "T2", "T3"):
            n = sum(1 for r in need if r["tier"] == tier)
            self.assertIn("%s: %d PDF" % (tier, n), t)
        self.assertIn("Held: %d" % len(held), t)
        self.assertIn("Units read: 0", t)
        self.assertIn("Feature rows: 0", t)
        out = sum(1 for r in scr if r["decision"] == "OUT_TITLE")
        self.assertIn("Out of region by title: %d" % out, t)
        self.assertIn("Chapter files listed: %d" % s["chapter_files_listed"], t)
        mb = sum(float(re.match(r"([\d.]+) MB", r["pdf_size"]).group(1)) for r in need)
        self.assertIn("%.1f MB" % mb, t)


if __name__ == "__main__":
    unittest.main()
