"""Tests for HA-ESI phase 3, part A (HA Hebrew series 1961-1979).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/haesi_features/phase3_2026-10-11/part_a/tests
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
P3 = PART.parent
LANE = P3.parent
P2 = LANE / "phase2_2026-10-10"
sys.path.insert(0, str(PART / "scripts"))
import build_part_a  # noqa: E402

PHASE2_PLAN_SHA256 = "5b1a5c082b41333a472a1d676066a5d377a24de72bd03c837025baf45eb7b3be"
PHASE3_PLAN_SHA256 = "312c27332bbc4d9b9d3405d88cb8d9d40e8e361714cdd5582997467593055cf2"
OUTPUTS = ["features.csv", "reports.csv", "screen.csv", "candidates_checkoff.csv", "summary.md", "summary.json"]
ZONES = {"Z1_GERIZIM", "Z2_JORDAN_VALLEY", "Z3_JUDEAN_DESERT", "Z4_JERUSALEM_HILLS"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def coding():
    out = []
    for p in sorted((PART / "data").glob("coding_*.json")):
        out.extend(json.loads(p.read_text(encoding="utf-8")))
    return out


class TestFrozenInputs(unittest.TestCase):
    def test_plans_unchanged(self):
        self.assertEqual(hashlib.sha256((P2 / "PLAN.md").read_bytes()).hexdigest(), PHASE2_PLAN_SHA256)
        self.assertEqual(hashlib.sha256((P3 / "PLAN.md").read_bytes()).hexdigest(), PHASE3_PLAN_SHA256)

    def test_sources_are_the_part_a_partition(self):
        part = {r["local_file"]: r["sha256"] for r in rows(P3 / "partition.csv") if r["part"] == "A"}
        src = {r["local_file_name"]: r["pdf_sha256"] for r in rows(PART / "data" / "local_sources.csv")}
        self.assertEqual(src, part)
        self.assertEqual(len(part), 50)


class TestSchema(unittest.TestCase):
    def test_columns_equal_phase2(self):
        self.assertEqual(header(PART / "features.csv"), header(P2 / "features.csv"))
        self.assertEqual(header(PART / "reports.csv"), header(P2 / "reports.csv"))


class TestCoding(unittest.TestCase):
    def test_ids_unique_and_named_by_volume_and_page(self):
        recs = coding()
        ids = [r["report_id"] for r in recs]
        self.assertEqual(len(ids), len(set(ids)))
        for r in recs:
            self.assertRegex(r["report_id"], r"^HA\d{2}-\d{3}-[a-z0-9-]+$")

    def test_quotes_short_and_found(self):
        spans = {r["report_id"]: r for r in rows(PART / "data" / "local_spans.csv")}
        for r in coding():
            sp = spans[r["report_id"]]
            self.assertEqual(sp["text_lines"], r["text_lines"])
            self.assertEqual(int(sp["n_quotes"]), len(r["features"]))
            self.assertEqual(sp["quotes_not_found"], "", r["report_id"])
            self.assertNotIn("N", sp["quote_check"], r["report_id"])
            for f in r["features"]:
                self.assertTrue(f["quote"].strip(), r["report_id"])
                self.assertLessEqual(len(f["quote"].split()), 12, (r["report_id"], f["quote"]))

    def test_quotes_unchanged_since_text_check(self):
        """The quotes were checked against the text on the Mac by hash; any later edit of a quote must be re-checked."""
        import span_jobs  # noqa: E402
        spans = {r["report_id"]: r for r in rows(PART / "data" / "local_spans.csv")}
        for r in coding():
            got = ",".join(span_jobs.qh(f["quote"]) for f in r["features"])
            self.assertEqual(got, spans[r["report_id"]]["quote_hashes"], r["report_id"])

    def test_classes_and_window_values(self):
        for r in coding():
            for f in r["features"]:
                self.assertIn(f["type"], build_part_a.CLASSES)
                self.assertIn(f["window"], ("yes", "no", "unknown"))

    def test_name_place_ids_exist(self):
        places = {p["place_id"] for p in build_part_a.geo.load_places(build_part_a.p1.W2B_IN / "places_v2.csv")}
        for r in coding():
            for x in [r] + r["features"]:
                if x.get("name_place"):
                    self.assertIn(x["name_place"], places, r["report_id"])


class TestOutputs(unittest.TestCase):
    def test_rebuild_is_identical(self):
        with tempfile.TemporaryDirectory() as d:
            build_part_a.main(d)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(Path(d) / name, PART / name, shallow=False), name)

    def test_every_report_in_region_and_screened(self):
        reps = rows(PART / "reports.csv")
        self.assertEqual({r["report_id"] for r in reps}, {r["report_id"] for r in coding()})
        for r in reps:
            self.assertIn(r["region_zone"], ZONES | {"MULTI"}, r["report_id"])
        for f in rows(PART / "features.csv"):
            self.assertIn(f["region_zone"], ZONES, f["report_id"])

    def test_screen_covers_every_toc_item(self):
        toc = {(build_part_a.vol_file_of(t["local_file"]), t["n"]) for t in rows(PART / "data" / "portal_toc_items.csv")}
        scr = {(r["vol_file"], r["toc_n"]) for r in rows(PART / "screen.csv")}
        self.assertTrue(toc <= scr)

    def test_defaults_only_without_signals(self):
        """A default (unlisted) decision is allowed only where the title has no gazetteer term and no map reference in
        the item text falls in a zone under either number order."""
        for r in rows(PART / "screen.csv"):
            if r["decision_source"] != "default":
                continue
            self.assertEqual(r["title_hits_strict"] + r["title_hits_prefix"], "", (r["vol_file"], r["toc_n"]))
            for z in ZONES:
                self.assertNotIn(z, r["map_ref_zones"], (r["vol_file"], r["toc_n"]))
            self.assertNotEqual(r["heading_located"], "not found", (r["vol_file"], r["toc_n"]))

    def test_candidates_all_accounted(self):
        ck = rows(PART / "candidates_checkoff.csv")
        vols = rows(PART / "data" / "volumes.csv")
        self.assertEqual(len(ck), sum(int(v["p1_cands"]) for v in vols))
        for c in ck:
            self.assertTrue(c["outcome"], c["item_key"])
            if c["outcome"].startswith("read"):
                self.assertTrue(c["report_ids"], c["item_key"])

    def test_protected_items_not_coded(self):
        for r in rows(PART / "screen.csv"):
            if r["decision"] in ("HELD", "STRIP_CHECK", "BORDER", "UNLOC"):
                self.assertEqual(r["report_ids"], "", (r["vol_file"], r["toc_n"]))


if __name__ == "__main__":
    unittest.main()
