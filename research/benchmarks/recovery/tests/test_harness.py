"""Tests for the harness, the key check, scoring, and reproducibility of the dev batch.

These tests read only research/benchmarks/recovery/dev and temporary folders.
They never open the reserved batch.
"""
import contextlib
import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "dev"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(DEV))
import harness as H  # noqa: E402
import procedure as P  # noqa: E402
import build_dev as B  # noqa: E402


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


class KeyCheck(unittest.TestCase):
    def test_canonical_hash_follows_schema(self):
        e = {"case_id": "x", "answer": "c1", "withheld_answer": "west", "sources": ["s"], "why": "w é"}
        expect = hashlib.sha256(json.dumps(e, ensure_ascii=False, sort_keys=True,
                                           separators=(",", ":")).encode("utf-8")).hexdigest()
        self.assertEqual(H.canonical_sha256(e), expect)

    def test_dev_key_verifies(self):
        self.assertEqual(quiet(H.main, [str(DEV), "--key", str(DEV / "key.json"), "--verify-key"]), 0)

    def test_tampered_key_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = json.loads((DEV / "key.json").read_text(encoding="utf-8"))
            key[0]["answer"] = "c9"
            kp = Path(tmp) / "key.json"
            kp.write_text(json.dumps(key), encoding="utf-8")
            self.assertEqual(quiet(H.main, [str(DEV), "--key", str(kp), "--verify-key"]), 1)
            report = H.verify_key(H.load_cases(DEV), H.load_key(kp))
            self.assertEqual(report["cases"][0]["status"], "hash_mismatch")

    def test_key_formats(self):
        key = json.loads((DEV / "key.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            jl = Path(tmp) / "key.jsonl"
            jl.write_text("\n".join(json.dumps(e) for e in key), encoding="utf-8")
            mp = Path(tmp) / "key_map.json"
            mp.write_text(json.dumps({e["case_id"]: e for e in key}), encoding="utf-8")
            self.assertEqual(H.load_key(jl), H.load_key(DEV / "key.json"))
            self.assertEqual(H.load_key(mp), H.load_key(DEV / "key.json"))

    def test_only_case_files_are_loaded(self):
        ids = [c["case_id"] for c in H.load_cases(DEV)]
        self.assertEqual(ids, [f"dev-{i:03d}" for i in range(1, 13)])


class Scoring(unittest.TestCase):
    def test_rules(self):
        key = {"a": {"answer": "insufficient", "withheld_answer": "north"},
               "b": {"answer": "c1", "withheld_answer": "east"},
               "c": {"answer": "none", "withheld_answer": "west"},
               "d": {"answer": "c2", "withheld_answer": "south"}}
        outs = [{"case_id": "a", "selected": "insufficient_evidence", "withheld_prediction": "unknown"},
                {"case_id": "b", "selected": "insufficient_evidence", "withheld_prediction": "unknown"},
                {"case_id": "c", "selected": "c3", "withheld_prediction": "west"},
                {"case_id": "d", "selected": "c2", "withheld_prediction": "unknown"}]
        s = H.score(outs, key)
        self.assertEqual(s["summary"], {"cases": 4, "selection_correct": 2, "wrong_selections": 1,
                                        "abstentions_on_decidable": 1, "correct_abstentions": 1})
        self.assertEqual(s["withheld_among_non_abstentions"],
                         {"non_abstentions": 2, "correct": 1, "wrong": 0, "unknown_when_answer_known": 1})


class Reproducibility(unittest.TestCase):
    def test_build_matches_stored_files(self):
        cases, keys, restore = B.build()
        for c in cases:
            stored = json.loads((DEV / f"{c['case_id']}.json").read_text(encoding="utf-8"))
            self.assertEqual(stored, c)
        self.assertEqual(json.loads((DEV / "key.json").read_text(encoding="utf-8")), keys)
        self.assertEqual(json.loads((DEV / "restore.json").read_text(encoding="utf-8")), restore)

    def test_saved_outputs_and_score_reproduce(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(quiet(H.main, [str(DEV), "--out", tmp, "--key", str(DEV / "key.json")]), 0)
            for p in sorted((DEV / "outputs").glob("*.json")):
                self.assertEqual(json.loads(p.read_text(encoding="utf-8")),
                                 json.loads((Path(tmp) / p.name).read_text(encoding="utf-8")), p.name)

    def test_cases_follow_schema(self):
        for c in H.load_cases(DEV):
            self.assertEqual(c["batch"], "development")
            self.assertTrue(3 <= len(c["candidates"]) <= 6, c["case_id"])
            self.assertIn("unknown", c["withheld_options"])
            for cand in c["candidates"]:
                self.assertIn(cand["features"]["date"], ("D", "L", "U"))

    def test_case_dir_copy_runs_without_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            for p in DEV.glob("dev-*.json"):
                shutil.copy(p, tmp)
            out = Path(tmp) / "out"
            self.assertEqual(quiet(H.main, [tmp, "--out", str(out)]), 0)
            self.assertFalse((out / "score.json").exists())
            self.assertEqual(len(list(out.glob("dev-*.json"))), 12)


if __name__ == "__main__":
    unittest.main()
