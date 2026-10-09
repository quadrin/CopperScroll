"""Structure checks for the reserved recovery batch.

These tests read only the case files and MANIFEST.md in this folder.
They never read the sealed key.
Run from the repository root:
    python3 -I -B -m unittest discover -s research/benchmarks/recovery/reserved -p 'test_*.py'
"""
import glob
import hashlib
import json
import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
CASE_FILES = sorted(glob.glob(os.path.join(HERE, "res-*.json")))
TOP_KEYS = ["case_id", "batch", "instruction", "context", "candidates", "degradations",
            "withheld_question", "withheld_options", "key_sha256"]
DATE_CODES = {"D", "L", "U"}
DEGRADATIONS = {"names_redacted", "direction_word_lost", "distance_missing", "direction_unknown",
                "position_unrecorded", "date_unknown", "reports_conflict",
                "measurement_rounded_to_cubits", "withheld_field_removed", "inventory_partial"}
ANSWER_WORDS = re.compile(r"\b(answer|correct|true feature|target feature)\b", re.IGNORECASE)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class TestCases(unittest.TestCase):
    def test_count(self):
        self.assertGreaterEqual(len(CASE_FILES), 10)
        self.assertLessEqual(len(CASE_FILES), 14)

    def test_schema(self):
        for path in CASE_FILES:
            case = load(path)
            name = os.path.basename(path)[:-5]
            with self.subTest(case=name):
                self.assertEqual(list(case.keys()), TOP_KEYS)
                self.assertEqual(case["case_id"], name)
                self.assertRegex(case["case_id"], r"^res-\d{3}$")
                self.assertEqual(case["batch"], "reserved")
                self.assertTrue(case["instruction"].strip())
                self.assertTrue(case["context"].startswith("Redacted site description:"))
                self.assertRegex(case["key_sha256"], r"^[0-9a-f]{64}$")
                self.assertIn("unknown", case["withheld_options"])
                self.assertEqual(len(set(case["withheld_options"])), len(case["withheld_options"]))
                self.assertTrue(set(case["degradations"]) <= DEGRADATIONS)

    def test_candidates(self):
        for path in CASE_FILES:
            case = load(path)
            with self.subTest(case=case["case_id"]):
                cands = case["candidates"]
                self.assertTrue(3 <= len(cands) <= 6)
                self.assertEqual([c["id"] for c in cands], ["c%d" % i for i in range(1, len(cands) + 1)])
                for c in cands:
                    f = c["features"]
                    for k in ("type", "position", "opening", "date", "notes"):
                        self.assertIn(k, f)
                    self.assertIn(f["date"], DATE_CODES)
                    p = f["position"]
                    self.assertEqual(sorted(p.keys()), ["bearing_deg", "distance_m", "relative_to"])
                    if p["bearing_deg"] is not None:
                        self.assertTrue(0 <= p["bearing_deg"] < 360)
                    if p["distance_m"] is not None:
                        self.assertGreaterEqual(p["distance_m"], 0)

    def test_no_answer_words(self):
        for path in CASE_FILES:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            with self.subTest(case=os.path.basename(path)):
                self.assertIsNone(ANSWER_WORDS.search(text))
                self.assertNotIn("http", text)

    def test_manifest(self):
        with open(os.path.join(HERE, "MANIFEST.md"), encoding="utf-8") as f:
            manifest = f.read()
        self.assertIn("run once, after the harness is frozen", manifest)
        self.assertIn("reported whatever it is", manifest)
        self.assertRegex(manifest, r"Key file SHA-256: `[0-9a-f]{64}`")
        rows = dict(re.findall(r"\| `(res-\d{3})` \| `([0-9a-f]{64})` \|", manifest))
        self.assertEqual(sorted(rows), [os.path.basename(p)[:-5] for p in CASE_FILES])
        for path in CASE_FILES:
            with open(path, "rb") as f:
                digest = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(rows[os.path.basename(path)[:-5]], digest)


if __name__ == "__main__":
    unittest.main()
