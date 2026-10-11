#!/usr/bin/env python3
"""Test of the exploratory IAA view (PLAN_AMENDMENT_IAA_2026-10-11.md).

Run:  python3 -I -B research/regional/caves_entry25/tests/test_iaa_view.py
Checks: the amendment's hash and that its commit holds only it and precedes the view; that iaa_view.py reproduces
its outputs byte for byte without touching the frozen outputs; that the view's frozen columns equal summary.json; and
that union = frozen + IAA rows.
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
AMEND = "research/regional/caves_entry25/PLAN_AMENDMENT_IAA_2026-10-11.md"
AMEND_SHA = "fc23efe51213b269742f50537e01f76a9816aa21ea66096e71ebedfdb1ef4125"
AMEND_COMMIT = "7e88f3d64a0016c45de092c1db7ea457822952a3"
VIEW_OUT = ["iaa_units.csv", "iaa_excluded.csv", "iaa_scores.csv", "iaa_summary.json", "iaa_view_2026-10-11.csv"]
FROZEN_OUT = ["caves.csv", "scores.csv", "aspect.csv", "summary.json", "excluded.csv", "duplicates.csv"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)


class IAAView(unittest.TestCase):
    def test_amendment_frozen_alone_before_the_view(self):
        self.assertEqual(sha(REPO / AMEND), AMEND_SHA)
        files = git("show", "--name-only", "--format=", AMEND_COMMIT)
        if files.returncode != 0:
            self.skipTest("amendment commit not in this clone")
        self.assertEqual(files.stdout.split(), [AMEND])
        first = git("log", "--diff-filter=A", "--format=%H", "--", "research/regional/caves_entry25/coded/iaa_coding.csv")
        for h in first.stdout.split():
            self.assertEqual(git("merge-base", "--is-ancestor", AMEND_COMMIT, h).returncode, 0)

    def test_view_reproduces_and_frozen_outputs_untouched(self):
        before = {n: sha(LANE / n) for n in VIEW_OUT + FROZEN_OUT}
        tmp = Path(tempfile.mkdtemp())
        try:
            for n in VIEW_OUT:
                shutil.copy(LANE / n, tmp / n)
            subprocess.run([sys.executable, "-I", "-B", str(LANE / "scripts/iaa_view.py")], check=True, capture_output=True)
            self.assertEqual(before, {n: sha(LANE / n) for n in VIEW_OUT + FROZEN_OUT})
        finally:
            for n in VIEW_OUT:
                shutil.copy(tmp / n, LANE / n)
            shutil.rmtree(tmp)

    def test_frozen_columns_equal_summary_and_union_adds_up(self):
        summary = json.load(open(LANE / "summary.json", encoding="utf-8"))["counts"]
        with open(LANE / "iaa_view_2026-10-11.csv", encoding="utf-8") as f:
            view = list(csv.DictReader(f))
        self.assertEqual(len(view), len(summary) * 3)
        for r in view:
            s = summary[f"{r['branch']}|{r['orientation']}|{r['ruleset']}"][r["count"]]
            self.assertEqual([int(r[k]) for k in ("frozen_N", "frozen_k", "frozen_f", "frozen_m")],
                             [s["N"], s["all-match"], s["fail"], s["unknown"]])
            for pre in ("frozen", "iaa", "union"):
                self.assertEqual(int(r[f"{pre}_k"]) + int(r[f"{pre}_f"]) + int(r[f"{pre}_m"]), int(r[f"{pre}_N"]))
            if r["count"] in ("rows", "clusters"):
                self.assertEqual(int(r["union_N"]), int(r["frozen_N"]) + int(r["iaa_N"]))
                for x in ("k", "f", "m"):
                    self.assertEqual(int(r[f"union_{x}"]), int(r[f"frozen_{x}"]) + int(r[f"iaa_{x}"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
