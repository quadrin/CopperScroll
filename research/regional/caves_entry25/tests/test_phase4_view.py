#!/usr/bin/env python3
"""Test of the exploratory phase 1-4 view (PLAN_AMENDMENT_PHASE4_2026-10-12.md).

Run:  python3 -I -B research/regional/caves_entry25/tests/test_phase4_view.py
Checks: the amendment's hash, that its commit holds only it and precedes the phase-4 coding and script; that
phase4_view.py reproduces its outputs byte for byte without touching the frozen or IAA-view outputs; that the frozen
columns equal summary.json and the IAA columns equal iaa_view_2026-10-11.csv; union arithmetic; that no held,
strip or Kh. Almit row is scored; and that the README states the headline.
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
AMEND = "research/regional/caves_entry25/PLAN_AMENDMENT_PHASE4_2026-10-12.md"
AMEND_SHA = "50e7a8762cc08e065251dde9e7bb248225ff1ef43a4a4d5ea0cec61885a6d8c1"
AMEND_COMMIT = "9fad7f4f2250a6fb9da19f1a0eed1686539a76f1"
VIEW_OUT = ["phase4_units.csv", "phase4_excluded.csv", "phase4_unplaced.csv", "phase4_scores.csv",
            "phase4_summary.json", "phase4_view_2026-10-12.csv"]
OTHER_OUT = ["caves.csv", "scores.csv", "aspect.csv", "summary.json", "excluded.csv", "duplicates.csv",
             "iaa_units.csv", "iaa_excluded.csv", "iaa_scores.csv", "iaa_summary.json", "iaa_view_2026-10-11.csv"]
PROTECTED = {"held", "held-area", "protected-strip", "tier1-almit", "atiqot41"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)


def rows(name):
    with open(LANE / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Phase4View(unittest.TestCase):
    def test_amendment_frozen_alone_before_the_view(self):
        self.assertEqual(sha(REPO / AMEND), AMEND_SHA)
        files = git("show", "--name-only", "--format=", AMEND_COMMIT)
        if files.returncode != 0:
            self.skipTest("amendment commit not in this clone")
        self.assertEqual(files.stdout.split(), [AMEND])
        for path in ("research/regional/caves_entry25/coded/phase4_coding.csv",
                     "research/regional/caves_entry25/scripts/phase4_view.py"):
            for h in git("log", "--diff-filter=A", "--format=%H", "--", path).stdout.split():
                self.assertEqual(git("merge-base", "--is-ancestor", AMEND_COMMIT, h).returncode, 0)
                self.assertNotEqual(h, AMEND_COMMIT)

    def test_view_reproduces_and_other_outputs_untouched(self):
        before = {n: sha(LANE / n) for n in VIEW_OUT + OTHER_OUT}
        tmp = Path(tempfile.mkdtemp())
        try:
            for n in VIEW_OUT:
                shutil.copy(LANE / n, tmp / n)
            subprocess.run([sys.executable, "-I", "-B", str(LANE / "scripts/phase4_view.py")], check=True, capture_output=True)
            self.assertEqual(before, {n: sha(LANE / n) for n in VIEW_OUT + OTHER_OUT})
        finally:
            for n in VIEW_OUT:
                shutil.copy(tmp / n, LANE / n)
            shutil.rmtree(tmp)

    def test_frozen_and_iaa_columns_unchanged_and_union_adds_up(self):
        summary = json.load(open(LANE / "summary.json", encoding="utf-8"))["counts"]
        iaa = {(r["branch"], r["orientation"], r["ruleset"], r["count"]): r for r in rows("iaa_view_2026-10-11.csv")}
        view = rows("phase4_view_2026-10-12.csv")
        added = json.load(open(LANE / "phase4_summary.json", encoding="utf-8"))["rows_added"]
        self.assertEqual(len(view), len(summary) * 3)
        for r in view:
            s = summary[f"{r['branch']}|{r['orientation']}|{r['ruleset']}"][r["count"]]
            self.assertEqual([int(r[k]) for k in ("frozen_N", "frozen_k", "frozen_f", "frozen_m")],
                             [s["N"], s["all-match"], s["fail"], s["unknown"]])
            i = iaa[(r["branch"], r["orientation"], r["ruleset"], r["count"])]
            self.assertEqual([int(r[f"iaa1011_{x}"]) for x in "Nkfm"], [int(i[f"union_{x}"]) for x in "Nkfm"])
            for pre in ("frozen", "iaa1011", "union"):
                self.assertEqual(int(r[f"{pre}_k"]) + int(r[f"{pre}_f"]) + int(r[f"{pre}_m"]), int(r[f"{pre}_N"]))
            if r["count"] == "rows":
                self.assertEqual(int(r["union_N"]), int(r["frozen_N"]) + added["caves"])
            if r["count"] == "clusters":
                self.assertEqual(int(r["union_N"]), int(r["frozen_N"]) + added["clusters"])

    def test_no_protected_row_scored(self):
        excl = {r["record_id"] for r in rows("phase4_excluded.csv") if r["status"] in PROTECTED}
        unit_ids = {r["cave_id"].split(":", 1)[1] for r in rows("phase4_units.csv")}
        scored = {r["cave_id"].split(":", 1)[1] for r in rows("phase4_scores.csv")}
        unplaced = {r["row_uid"] for r in rows("phase4_unplaced.csv")}
        self.assertFalse(excl & (unit_ids | scored | unplaced))
        for r in rows("phase4_excluded.csv"):
            if r["status"] in PROTECTED:
                self.assertEqual(r["site_name"], "")  # held rows are listed by id only
        for r in rows("phase4_units.csv"):
            self.assertNotRegex(r["name_number"], r"(?i)qumr|sultan|almit|qelt|qilt|kelt|qarantal|quruntul")

    def test_readme_headline(self):
        text = (LANE / "README.md").read_text(encoding="utf-8")
        h = json.load(open(LANE / "phase4_summary.json", encoding="utf-8"))["headline"]["union"]
        self.assertIn(f"{h['all-match']} / {h['fail']} / {h['unknown']} of {h['N']}", text)


if __name__ == "__main__":
    unittest.main(verbosity=1)
