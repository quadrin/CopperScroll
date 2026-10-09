"""Schema and sourcing tests for research/history/salvage_records.

Run: python3 -I -m unittest discover -s research/history/salvage_records -t research/history/salvage_records
"""
import csv
import importlib.util
import json
import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)


def load_summarize():
    spec = importlib.util.spec_from_file_location("summarize", os.path.join(FOLDER, "summarize.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = load_summarize()


def rows(name):
    with open(os.path.join(FOLDER, name), encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


class TestSchemas(unittest.TestCase):
    def test_columns(self):
        self.assertEqual(rows("catalogue.csv")[0], S.CATALOGUE_COLS)
        self.assertEqual(rows("searches.csv")[0], S.SEARCH_COLS)
        self.assertEqual(rows("sources.csv")[0], S.SOURCE_COLS)
        self.assertEqual(rows("source_files.csv")[0], S.FILE_COLS)

    def test_join_columns_for_search_effectiveness(self):
        cols = rows("searches.csv")[0]
        for c in ("place_id", "record", "looked_at", "result", "notes"):
            self.assertIn(c, cols)

    def test_unique_ids(self):
        for name, key, pat in (("catalogue.csv", "cat_id", r"C\d{2}"), ("searches.csv", "search_id", r"S\d{2}"),
                               ("sources.csv", "source_id", r"SRC-[A-Z0-9-]+")):
            ids = [r[key] for r in rows(name)[1]]
            self.assertEqual(len(ids), len(set(ids)), name)
            for i in ids:
                self.assertRegex(i, "^" + pat + "$")

    def test_validator_passes(self):
        errors = S.validate()[0]
        self.assertEqual(errors, [])

    def test_controlled_vocabularies(self):
        for r in rows("catalogue.csv")[1]:
            self.assertIn(r["kind"], S.KINDS, r["cat_id"])
            for c in ("s_removed", "s_unrecovered", "s_literary"):
                self.assertIn(r[c], S.SCEN, r["cat_id"])
            self.assertTrue(r["scenario_reason"].strip(), r["cat_id"])
            self.assertTrue(r["dependency_group"].strip(), r["cat_id"])
        for r in rows("searches.csv")[1]:
            self.assertIn(r["result"], S.RESULTS, r["search_id"])
            self.assertIn(r["purpose"], S.PURPOSES, r["search_id"])
            self.assertIn(r["kind"], S.KINDS, r["search_id"])
            self.assertIn(r["place_match"], S.MATCH, r["search_id"])

    def test_place_ids_exist_in_places_v1(self):
        places = S.place_ids()
        self.assertEqual(len(places), 49)
        for name in ("catalogue.csv", "searches.csv"):
            for r in rows(name)[1]:
                if r["place_id"]:
                    self.assertIn(r["place_id"], places, r)

    def test_entry_ids_format(self):
        for r in rows("searches.csv")[1]:
            if r["entry_ids"]:
                self.assertRegex(r["entry_ids"], r"^\d+[a-z]?(;\d+[a-z]?)*$", r["search_id"])


class TestSourcing(unittest.TestCase):
    def setUp(self):
        self.sources = {r["source_id"]: r for r in rows("sources.csv")[1]}
        self.files = rows("source_files.csv")[1]

    def test_every_row_has_a_resolving_source(self):
        for name, key in (("catalogue.csv", "cat_id"), ("searches.csv", "search_id")):
            for r in rows(name)[1]:
                ids = [x for x in r["source_ids"].split(";") if x]
                self.assertTrue(ids, r[key])
                for x in ids:
                    self.assertIn(x, self.sources, r[key])
                    self.assertNotIn(self.sources[x]["access"], ("not_accessed", "failed"), r[key])

    def test_catalogue_rows_have_locators(self):
        for r in rows("catalogue.csv")[1]:
            self.assertTrue(r["reference"].strip())
            if r["quote"]:
                self.assertTrue(r["quote_locator"].strip(), r["cat_id"])

    def test_downloaded_sources_have_hashes(self):
        with_files = {f["source_id"] for f in self.files}
        for sid, s in self.sources.items():
            if s["access"] == "read" and s["url"].startswith("http") and "no content hash" not in s["notes"]:
                self.assertIn(sid, with_files, sid)
        for f in self.files:
            self.assertRegex(f["sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(f["url"])
            self.assertGreater(int(f["bytes"]), 0)


class TestQuotes(unittest.TestCase):
    def test_quotes_at_most_12_words(self):
        for name in ("catalogue.csv",):
            for r in rows(name)[1]:
                self.assertLessEqual(len(r["quote"].split()), 12, (r["cat_id"], r["quote"]))

    def test_no_long_quoted_spans_in_text_fields(self):
        # Any span in straight or curly double quotes inside the tables stays within 12 words.
        pat = re.compile(r"[\"“]([^\"”]{1,400})[\"”]")
        # Bibliographic titles in sources.csv (the citation column) are not quotes.
        for name, skip in (("catalogue.csv", None), ("searches.csv", None), ("sources.csv", "citation")):
            with open(os.path.join(FOLDER, name), encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    for col, cell in row.items():
                        if col == skip:
                            continue
                        for m in pat.finditer(cell):
                            self.assertLessEqual(len(m.group(1).split()), 12, (name, m.group(1)))
                        for m in re.finditer(r"(?:^|[\s(])'([^']{1,400})'(?=[\s,.;:)]|$)", cell):
                            span = m.group(1)
                            if " " in span:
                                self.assertLessEqual(len(span.split()), 12, (name, span))

    def test_readme_quotes_short(self):
        path = os.path.join(FOLDER, "README.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for m in re.finditer(r"[\"“]([^\"”\n]{1,400})[\"”]", text):
            self.assertLessEqual(len(m.group(1).split()), 12, m.group(1))


class TestSummary(unittest.TestCase):
    def test_summary_deterministic_and_current(self):
        errors, _, _, cat, srch = S.validate()
        self.assertEqual(errors, [])
        a = json.dumps(S.summary(cat, srch), sort_keys=True)
        b = json.dumps(S.summary(cat, srch), sort_keys=True)
        self.assertEqual(a, b)
        with open(os.path.join(FOLDER, "summary.json"), encoding="utf-8") as f:
            stored = json.load(f)
        self.assertEqual(json.loads(a), stored)

    def test_plan_hash_recorded(self):
        import hashlib
        with open(os.path.join(FOLDER, "PLAN.md"), "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        with open(os.path.join(FOLDER, "README.md"), encoding="utf-8") as f:
            readme = f.read()
        self.assertIn(h, readme)


if __name__ == "__main__":
    unittest.main()
