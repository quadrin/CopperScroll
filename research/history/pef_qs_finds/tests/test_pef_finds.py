"""Tests for the PEF Quarterly Statement find index. Standard library only.

    python3 -I -m unittest discover -s research/history/pef_qs_finds/tests
"""
import csv
import hashlib
import importlib.util
import json
import os
import re
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACES = os.path.join(HERE, "..", "..", "agent_review_2026-10-07", "wave2", "W2B_model_v1", "inputs", "places_v1.csv")
FROZEN_SHA256 = "bfeed9a1324e4ac73f68dc184953358c1e308a17876aa2d96f1fc55300c7f28c"

FIND_COLUMNS = [
    "find_id", "hit_seq", "hit_id", "volume", "year", "issue", "printed_page", "page_source", "find_page",
    "ia_identifier", "leaf", "matched_key", "author_or_reporter", "place_as_written", "place_id",
    "distance_direction", "find_type", "report_kind", "date_period", "finder", "disposition", "quote",
    "georef_confidence", "relevance", "ocr_flag", "same_find_as",
]
HIT_COLUMNS = [
    "seq", "tier", "status", "drop_reason", "hit_id", "ia_identifier", "year", "issue", "leaf", "printed_page",
    "page_source", "key", "region", "hit_class", "matched_text", "strong_terms", "feature_terms",
    "discovery_terms", "occurrences_on_page", "text_version",
]
POST_COLUMNS = [
    "pf_id", "found_by", "why_missed", "volume", "year", "find_page", "ia_identifier", "leaf",
    "author_or_reporter", "place_as_written", "place_id", "distance_direction", "find_type", "report_kind",
    "date_period", "finder", "disposition", "quote", "georef_confidence", "relevance", "ocr_flag",
]
FIND_TYPES = {"coin", "coin_hoard", "treasure", "cistern", "tomb", "cave", "jar_vessel", "inscription",
              "ossuary", "sarcophagus", "lamp", "metal_object", "manuscript", "structure", "other"}
REPORT_KINDS = {"chance", "excavation", "survey", "purchase"}
GEOREF = {"high", "medium", "low", "none"}
OCR = {"good", "fair", "poor"}
EXTRA_PLACES = {"x_qarn_sartaba", "x_khan_el_ahmar", "x_tell_es_samarat", "unresolved"}


def rows(name):
    with open(os.path.join(HERE, name), newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def words(s):
    return len(s.split())


def text(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


class FrozenTerms(unittest.TestCase):
    def test_hash_matches_freeze_record(self):
        with open(os.path.join(HERE, "search_terms.json"), "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(h, FROZEN_SHA256)
        readme = text("README.md")
        self.assertIn(FROZEN_SHA256, readme)

    def test_terms_parse(self):
        t = json.loads(text("search_terms.json"))
        for k in ("places", "groups", "find_terms", "hit_rule", "drop_reasons", "coding_fields"):
            self.assertIn(k, t)


class Schemas(unittest.TestCase):
    def test_finds_columns(self):
        cols, _ = rows("finds.csv")
        self.assertEqual(cols, FIND_COLUMNS)

    def test_hits_columns(self):
        cols, _ = rows("hits.csv")
        self.assertEqual(cols, HIT_COLUMNS)

    def test_post_freeze_columns(self):
        cols, _ = rows("post_freeze_finds.csv")
        self.assertEqual(cols, POST_COLUMNS)

    def test_find_ids_unique(self):
        _, fr = rows("finds.csv")
        ids = [r["find_id"] for r in fr]
        self.assertEqual(len(ids), len(set(ids)))


class Content(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.finds = rows("finds.csv")
        _, cls.hits = rows("hits.csv")
        _, cls.post = rows("post_freeze_finds.csv")

    def test_quotes_at_most_12_words(self):
        for r in self.finds + self.post:
            self.assertTrue(r["quote"].strip(), r)
            self.assertLessEqual(words(r["quote"]), 12, r["quote"])
        _, ir = rows("index_recall.csv")
        for r in ir:
            self.assertLessEqual(words(r["index_entry_ocr"]), 12)

    def test_every_row_has_volume_and_page(self):
        for r in self.finds + self.post:
            self.assertTrue(r["volume"].startswith("QS "), r)
            self.assertRegex(r["find_page"], r"\d", r)
        for r in self.finds:
            self.assertTrue(r["printed_page"] or r["find_page"], r)

    def test_kept_hits_have_rows_and_rows_have_kept_hits(self):
        kept = {h["seq"] for h in self.hits if h["status"] == "kept"}
        with_rows = {r["hit_seq"] for r in self.finds}
        self.assertEqual(kept, with_rows)

    def test_hit_status_and_reasons(self):
        t = json.loads(text("search_terms.json"))
        reasons = set(t["drop_reasons"])
        for h in self.hits:
            self.assertIn(h["status"], {"kept", "dropped", "uncoded"})
            if h["status"] == "dropped":
                self.assertIn(h["drop_reason"], reasons)
            else:
                self.assertEqual(h["drop_reason"], "")

    def test_place_ids_valid(self):
        if not os.path.exists(PLACES):
            self.skipTest("places_v1.csv not found")
        with open(PLACES, newline="", encoding="utf-8") as f:
            ids = {r["place_id"] for r in csv.DictReader(f)} | EXTRA_PLACES
        for r in self.finds + self.post:
            self.assertIn(r["place_id"], ids, r["place_id"])

    def test_vocabularies(self):
        for r in self.finds + self.post:
            for t in r["find_type"].split(";"):
                self.assertIn(t.strip(), FIND_TYPES, r)
            self.assertIn(r["report_kind"], REPORT_KINDS, r)
            self.assertIn(r["georef_confidence"], GEOREF, r)
            self.assertIn(r["ocr_flag"], OCR, r)

    def test_same_find_as_points_to_a_find(self):
        ids = {r["find_id"] for r in self.finds}
        for r in self.finds:
            if r["same_find_as"]:
                self.assertIn(r["same_find_as"], ids)
                self.assertNotEqual(r["same_find_as"], r["find_id"])

    def test_post_freeze_rows_are_not_search_hits(self):
        for r in self.post:
            self.assertTrue(r["pf_id"].startswith("PF"))
            self.assertTrue(r["found_by"].startswith("post-freeze"), r)


class Housekeeping(unittest.TestCase):
    def test_summary_is_current(self):
        spec = importlib.util.spec_from_file_location("summarize", os.path.join(HERE, "scripts", "summarize.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        out = json.dumps(mod.build(), indent=1, ensure_ascii=False, sort_keys=False) + "\n"
        self.assertEqual(text("summary.json"), out)

    def test_no_ocr_dumps_in_folder(self):
        for root, _, files in os.walk(HERE):
            for fn in files:
                p = os.path.join(root, fn)
                self.assertFalse(fn.endswith((".gz", "_djvu.txt", ".pdf", ".jsonl")), p)
                self.assertLess(os.path.getsize(p), 3_000_000, p)

    def test_volumes_have_url_and_hash(self):
        _, vr = rows("volumes.csv")
        searched = [v for v in vr if v["role"] == "searched"]
        self.assertEqual(len(searched), 111)
        for v in vr:
            self.assertTrue(v["djvu_txt_url"].startswith("https://archive.org/download/"))
            self.assertTrue(v["djvu_txt_sha256"] or v["searchtext_sha256"], v["ia_identifier"])


if __name__ == "__main__":
    unittest.main()
