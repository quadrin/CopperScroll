#!/usr/bin/env python3
"""Tests for the caves_entry25 lane.

Run:  python3 -I -B research/regional/caves_entry25/tests/test_lane.py
Checks: the frozen plan's hash and freeze commit; the frozen aspect-rule files' hashes; the schema of the outputs;
that build_caves.py and score.py reproduce the committed caves.csv, scores.csv, aspect.csv and summary.json byte for
byte; and spot checks of the rows the README names.
"""
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
REPO = LANE.parents[2]
PLAN_SHA = "b6bc2cd9fa22df86d4ac8d0c5c723384a17f7c4670c848ac1039a711e6a77193"
FREEZE_COMMIT = "2ff6e5acde5caaea47917dc0fb4269dfc8173609"
RULES = REPO / "research/preregistration/entry25_iv17_rules"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(name):
    with open(LANE / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Freeze(unittest.TestCase):
    def test_plan_hash(self):
        self.assertEqual(sha(LANE / "PLAN.md"), PLAN_SHA)

    def test_plan_matches_freeze_commit(self):
        blob = subprocess.run(["git", "show", f"{FREEZE_COMMIT}:research/regional/caves_entry25/PLAN.md"], cwd=REPO,
                              capture_output=True, check=True).stdout
        self.assertEqual(hashlib.sha256(blob).hexdigest(), PLAN_SHA)

    def test_freeze_commit_holds_only_the_plan(self):
        files = subprocess.run(["git", "show", "--name-only", "--format=", FREEZE_COMMIT], cwd=REPO, capture_output=True,
                               check=True, text=True).stdout.split()
        self.assertEqual(files, ["research/regional/caves_entry25/PLAN.md"])

    def test_frozen_rules_unchanged(self):
        self.assertTrue(sha(RULES / "rules.json").startswith("24a1377d"))
        self.assertTrue(sha(RULES / "RULES.md").startswith("794a4e5e"))


class Schema(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(LANE / "scripts"))
        import build_caves  # noqa: F401
        self.bc = build_caves
        self.rows = read("caves.csv")
        self.scores = read("scores.csv")

    def test_columns(self):
        with open(LANE / "caves.csv", encoding="utf-8") as f:
            header = next(csv.reader(f))
        self.assertEqual(header, self.bc.OUT_FIELDS)
        for col in ("cave_id", "source_records", "name_number", "x_oig", "crs_printed", "precision_m", "n_openings",
                    "opening_facings", "pillar", "published_plan", "period_in_window", "excavation_status", "finds", "exposure"):
            self.assertIn(col, header)

    def test_values(self):
        ids = [r["cave_id"] for r in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.rows:
            self.assertIn(r["exposure"], {"exposed-repo", "page-opened-before", "unexposed-at-freeze", "exposed-this-worker"})
            self.assertIn(r["in_region"], {"yes", "edge"})
            self.assertIn(r["pillar"], {"yes", "no", ""})
            self.assertIn(r["terrace"], {"yes", "no", ""})
            self.assertIn(r["period_in_window"], {"yes", "yes+other", "partly", "no", ""})
            self.assertIn(r["row_kind"], {"cave", "cluster"})
            self.assertIn(r["northern_member"], {"decided", "undetermined", ""})
            if r["n_openings"]:
                self.assertGreaterEqual(int(r["n_openings"]), 1)
            if r["exposure"] == "unexposed-at-freeze" and r["module"] == "a41":
                self.assertGreater(r["first_read_utc"], "2026-10-11T04:07:54Z")

    def test_scores_shape(self):
        self.assertEqual(len(self.scores), len(self.rows) * 2 * 2 * 4)
        for s in self.scores:
            self.assertIn(s["result"], {"all-match", "fail", "unknown"})
            self.assertEqual(int(s["n_match"]) + int(s["n_fail"]) + int(s["n_unknown"]), 5)


class Reproduce(unittest.TestCase):
    def test_rebuild_is_identical(self):
        names = ["caves.csv", "excluded.csv", "duplicates.csv", "scores.csv", "aspect.csv", "summary.json"]
        before = {n: sha(LANE / n) for n in names}
        tmp = Path(tempfile.mkdtemp())
        try:
            for n in names:
                shutil.copy(LANE / n, tmp / n)
            for script in ("build_caves.py", "score.py"):
                subprocess.run([sys.executable, "-I", "-B", str(LANE / "scripts" / script)], check=True, capture_output=True)
            after = {n: sha(LANE / n) for n in names}
            self.assertEqual(before, after)
        finally:
            for n in names:  # restore whatever was there
                shutil.copy(tmp / n, LANE / n)
            shutil.rmtree(tmp)


class SpotChecks(unittest.TestCase):
    def setUp(self):
        self.s = {(r["cave_id"], r["branch"], r["orientation"], r["ruleset"]): r for r in read("scores.csv")}
        with open(LANE / "summary.json", encoding="utf-8") as f:
            self.summary = json.load(f)

    def test_xii53_cave_level(self):
        r = self.s[("A41:XII/53", "B-PILLAR", "cave", "primary")]
        self.assertEqual(r["result"], "all-match")
        self.assertEqual(r["c4_verdict"], "pass")

    def test_twin_cave_both_mouths(self):
        self.assertEqual(self.s[("REPO:TwinCave", "B-PILLAR", "both-mouths", "primary")]["result"], "all-match")
        self.assertEqual(self.s[("REPO:TwinCave", "B-PILLAR", "cave", "primary")]["c4_verdict"], "not-measurable")

    def test_iv17_and_iv11(self):
        self.assertEqual(self.s[("A41:IV/17", "B-PILLAR", "both-mouths", "primary")]["c4_verdict"], "inconclusive")
        self.assertEqual(self.s[("A41:IV/11", "B-PILLAR", "cave", "primary")]["failing"], "C3,C5")

    def test_counts_add_up(self):
        for key, v in self.summary["counts"].items():
            for part in ("rows", "min"):
                c = v[part]
                self.assertEqual(c["all-match"] + c["fail"] + c["unknown"], c["N"], key)


if __name__ == "__main__":
    unittest.main(verbosity=1)
