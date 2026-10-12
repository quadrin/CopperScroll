"""Tests for phase 4, part E (ʿAtiqot 42-121): screen, held list and PDF list.

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_e_atiqot/tests
"""
import csv
import filecmp
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PART = Path(__file__).resolve().parents[1]
P4 = PART.parent
P2 = P4.parent / "phase2_2026-10-10"
sys.path.insert(0, str(PART / "scripts"))
import build_part_e  # noqa: E402
import screen_lib as L  # noqa: E402

PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"  # commit d0f8c7c
PHASE4_PLAN_SHA256 = "5428c4ccadd6dae0b0df3f4a4030bba9f3626a628377f931ed949fb752e9b2da"  # commit b002e03
ZONES = {"Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


class TestFrozen(unittest.TestCase):
    def test_plan_hashes(self):
        self.assertEqual(hashlib.sha256((P2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)
        self.assertEqual(hashlib.sha256((P4 / "PLAN.md").read_bytes()).hexdigest(), PHASE4_PLAN_SHA256)


class TestSchema(unittest.TestCase):
    def test_columns_equal_phase2(self):
        self.assertEqual(header(PART / "features.csv"), header(P2 / "features.csv"))
        self.assertEqual(header(PART / "reports.csv"), header(P2 / "reports.csv"))

    def test_no_article_body_coded(self):
        self.assertEqual(rows(PART / "features.csv"), [])
        self.assertEqual(rows(PART / "reports.csv"), [])


class TestScreen(unittest.TestCase):
    def setUp(self):
        self.screen = rows(PART / "screen.csv")
        self.articles = rows(PART / "data" / "atiqot_articles.csv")

    def test_every_listing_screened_vol41_excluded(self):
        self.assertEqual(len(self.screen), len(self.articles))
        vols = {int(r["volume"]) for r in self.screen}
        self.assertEqual(vols, set(range(42, 122)))
        self.assertNotIn(41, vols)

    def test_every_row_has_decision_and_reason(self):
        for r in self.screen:
            self.assertTrue(r["decision"], r["unit_id"])
            self.assertTrue(r["reason"], r["unit_id"])

    def test_unit_ids_unique_and_formed(self):
        ids = [r["unit_id"] for r in self.screen]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.screen:
            self.assertRegex(r["unit_id"], r"^ATQ\d{2,3}-(\d{3}s?|i\d{2})-[a-z0-9-]+(~i\d+)?$")

    def test_gazetteer_hits_recomputed(self):
        pats = L.patterns()
        for r in self.screen:
            self.assertEqual(r["title_hits"], L.fmt_hits(L.hits(r["title"], pats)), r["unit_id"])

    def test_tiers_follow_zone_rule(self):
        for r in self.screen:
            t, z = r["tier"], r["zone"]
            if t == "T1":
                self.assertTrue(z in {"Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT"} or "REGION_WIDE" in r["title_hits"], r["unit_id"])
            elif t in ("T2", "T3"):
                self.assertEqual(z, "Z4_JERUSALEM_HILLS", r["unit_id"])
                starts = L.common.norm(r["title"]).strip().startswith("jerusalem")
                self.assertEqual(t == "T3", starts, r["unit_id"])

    def test_order_is_sha256_of_unit_id(self):
        for t in ("T1", "T2", "T3", "U"):
            ts = sorted((r for r in self.screen if r["tier"] == t), key=lambda r: int(r["order_position_in_tier"]))
            hs = [hashlib.sha256(r["unit_id"].encode()).hexdigest() for r in ts]
            self.assertEqual(hs, sorted(hs), t)

    def test_kml_zones_recomputed(self):
        params = L.common.plan_params()
        for r in self.screen:
            if r["kml_lat"]:
                z = L.common.zone_of(float(r["kml_lat"]), float(r["kml_lon"]), params) or "outside"
                self.assertEqual(r["kml_zone"], z, r["unit_id"])

    def test_zone_from_kml_when_that_is_the_basis(self):
        for r in self.screen:
            if r["zone_basis"].startswith("portal location map"):
                self.assertEqual(r["zone"], r["kml_zone"], r["unit_id"])

    def test_landing_firstpage_is_item_number(self):
        meta = rows(PART / "data" / "landing_meta.csv")
        self.assertTrue(meta)
        for m in meta:
            if m["firstpage"]:
                self.assertEqual(m["firstpage"], m["item_no"])


class TestHeldAndPdfs(unittest.TestCase):
    def setUp(self):
        self.screen = rows(PART / "screen.csv")
        self.held = rows(PART / "held.csv")
        self.pdfs = rows(PART / "pdfs_needed.csv")

    def test_no_held_unit_coded(self):
        held_ids = {r["unit_id"] for r in self.held if r["held"] == "yes" or r["protected_strip"] == "yes"}
        coded = {r["report_id"] for r in rows(PART / "features.csv")} | {r["report_id"] for r in rows(PART / "reports.csv")}
        self.assertFalse(held_ids & coded)
        for p in self.pdfs:
            self.assertNotIn(p["unit_id"], {r["unit_id"] for r in self.held if r["held"] == "yes"})

    def test_pdf_urls_are_portal_viewcontent(self):
        for p in self.pdfs:
            self.assertRegex(p["pdf_url"], r"^https://publications\.iaa\.org\.il/cgi/viewcontent\.cgi\?article=\d+&context=atiqot$")
            self.assertRegex(p["landing_url"], r"^https://publications\.iaa\.org\.il/atiqot/vol\d+/iss1/\d+$")

    def test_pdf_list_matches_screen(self):
        need = {r["unit_id"] for r in self.screen if r["tier"]}
        self.assertEqual(need, {p["unit_id"] for p in self.pdfs})
        order = {"T1": 0, "T2": 1, "T3": 2, "U": 3}
        keys = [(order[p["tier"]], int(p["order_position_in_tier"])) for p in self.pdfs]
        self.assertEqual(keys, sorted(keys))
        for p in self.pdfs:
            self.assertEqual(p["sha256_unit_id"], hashlib.sha256(p["unit_id"].encode()).hexdigest())

    def test_readme_counts_match_tables(self):
        s = json.loads((PART / "summary.json").read_text(encoding="utf-8"))
        readme = (PART / "README.md").read_text(encoding="utf-8")
        self.assertEqual(s["listings_screened"], len(self.screen))
        self.assertEqual(s["pdfs_needed"], len(self.pdfs))
        for t, v in s["pdfs_by_tier"].items():
            self.assertEqual(v["pdfs"], sum(1 for p in self.pdfs if p["tier"] == t))
            self.assertIn("| %s | %d |" % (t, v["pdfs"]), readme)
        self.assertIn("%d listings" % s["listings_screened"], readme)
        self.assertIn("%d PDFs" % s["pdfs_needed"], readme)
        self.assertIn("%d held" % s["held"], readme)


class TestDeterministic(unittest.TestCase):
    def test_rebuild_identical(self):
        outs = ["screen.csv", "held.csv", "pdfs_needed.csv", "summary.json"]
        with tempfile.TemporaryDirectory() as d:
            for o in outs:
                shutil.copy(PART / o, Path(d) / o)
            build_part_e.main()
            for o in outs:
                self.assertTrue(filecmp.cmp(PART / o, Path(d) / o, shallow=False), o)


if __name__ == "__main__":
    unittest.main()
