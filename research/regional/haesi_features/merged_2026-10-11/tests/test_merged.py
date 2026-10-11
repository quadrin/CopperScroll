#!/usr/bin/env python3
"""Tests for the merged HA-ESI inventory (standard library only).

Run from the repository root:
    python3 -I -B -m unittest discover -s research/regional/haesi_features/merged_2026-10-11/tests
"""
import csv
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
HAESI = LANE.parent
REPO = LANE.parents[3]
PLAN_SHA256 = "ff13b357ae37c558bf5cebba0db01541cc0d17db0d2b12e1c7b8fe0710be676f"
FREEZE_COMMIT = "bf4320f"
OUTPUTS = ["features_all.csv", "report_groups.csv", "sites.csv", "conflicts.csv", "pair_candidates.csv", "site_review.csv",
           "ha_esi_volume_map.csv", "summary.json", "summary.md"]

_spec = importlib.util.spec_from_file_location("build_merged", LANE / "scripts" / "build_merged.py")
bm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bm)


def rows(name):
    with open(LANE / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def src_rows(rel):
    with open(HAESI / rel, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestPlan(unittest.TestCase):
    def test_plan_hash(self):
        h = hashlib.sha256((LANE / "DEDUPE_PLAN.md").read_bytes()).hexdigest()
        self.assertEqual(h, PLAN_SHA256)
        self.assertIn(PLAN_SHA256, (LANE / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(json.loads((LANE / "summary.json").read_text(encoding="utf-8"))["plan"]["sha256"], PLAN_SHA256)

    def test_freeze_commit_holds_only_the_plan(self):
        try:
            out = subprocess.run(["git", "-C", str(REPO), "show", "--name-only", "--format=", FREEZE_COMMIT],
                                 capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            self.skipTest("git not available")
        if out.returncode != 0:
            self.skipTest("freeze commit not in this clone")
        files = [x for x in out.stdout.split("\n") if x.strip()]
        self.assertEqual(files, ["research/regional/haesi_features/merged_2026-10-11/DEDUPE_PLAN.md"])


class TestHelpers(unittest.TestCase):
    def test_name_keys(self):
        self.assertEqual(bm.name_keys("Jerusalem, Pisgat Ze’ev (East A)")[0], "pisgat zeev")
        self.assertEqual(bm.name_keys("ירושלים - פסגת זאב (מזרח א׳) (Jerusalem, Pisgat Ze'ev East A)")[0], "pisgat zeev")
        self.assertEqual(bm.name_keys("Jerusalem, the Lower Aqueduct")[0], "lower aqueduct")
        self.assertEqual(bm.name_keys("Judean Desert, Survey (Map 106)")[0], "")  # region-wide term is not a site
        self.assertEqual(bm.name_keys("Jerusalem")[0], "")
        self.assertTrue(bm.name_keys("ירושלים, הר הזיתים")[1])

    def test_author_skeletons(self):
        self.assertTrue(bm.author_skeletons("J. Seligman") & bm.author_skeletons("Jon Seligman"))
        self.assertTrue(bm.author_skeletons("Y. Billig") & bm.author_skeletons("Ya‘aqov Billig"))
        self.assertFalse(bm.author_skeletons("Z. Greenhut, G. Solimany") & bm.author_skeletons("Ya‘akov Billig"))
        self.assertEqual(bm.author_skeletons("W. Zeidan (Ramallah district inspector)"), {"zdn"})

    def test_permits_amendment_a1(self):
        self.assertEqual(bm.permits("A-5185"), bm.permits("A- 5185"))
        self.assertEqual(bm.permits("S-123/2005"), {"S1232005"})
        self.assertEqual(bm.permits("License No. G-12/2010"), bm.permits("G-12/2010"))
        self.assertEqual(bm.permits("A-9317, A-9796"), {"A9317", "A9796"})
        self.assertEqual(bm.permits(""), set())

    def test_tolerance(self):
        self.assertAlmostEqual(bm.tol_m(1, 1), 250 + 2 * 2 ** 0.5)
        self.assertAlmostEqual(bm.tol_m(100, 10), 250 + 110 * 2 ** 0.5)


class TestBuild(unittest.TestCase):
    def test_rebuild_is_identical(self):
        with tempfile.TemporaryDirectory() as d:
            bm.main(d)
            for name in OUTPUTS:
                self.assertEqual(Path(d, name).read_bytes(), (LANE / name).read_bytes(), name)

    def test_inputs_match_summary_hashes(self):
        s = json.loads((LANE / "summary.json").read_text(encoding="utf-8"))
        for rel, info in list(s["inputs"].items()) + list(s["report_inputs"].items()):
            self.assertEqual(hashlib.sha256((HAESI / rel).read_bytes()).hexdigest(), info["sha256"], rel)


class TestTables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fa = rows("features_all.csv")
        cls.rg = rows("report_groups.csv")
        cls.sites = rows("sites.csv")
        cls.summary = json.loads((LANE / "summary.json").read_text(encoding="utf-8"))

    def test_every_source_row_once_in_order(self):
        i = 0
        for _, rel in bm.FEATURE_SOURCES:
            for k, r in enumerate(src_rows(rel), 1):
                m = self.fa[i]
                self.assertEqual(m["row_uid"], "%s#%d" % (rel, k))
                for col in ("report_id", "feature_type", "dated_in_window", "quote", "lat", "lon"):
                    self.assertEqual(m[col], r[col], (rel, k, col))
                i += 1
        self.assertEqual(i, len(self.fa))
        self.assertEqual(len(set(m["row_uid"] for m in self.fa)), len(self.fa))

    def test_columns(self):
        with open(HAESI / "phase2_2026-10-10/features.csv", newline="", encoding="utf-8") as f:
            p2 = next(csv.reader(f))
        with open(LANE / "features_all.csv", newline="", encoding="utf-8") as f:
            hdr = next(csv.reader(f))
        self.assertEqual(hdr[:len(p2) + 4], p2 + ["phase", "source_file", "report_group", "site_id"])

    def test_groups_partition_reports(self):
        allids = []
        for _, rel in bm.REPORT_SOURCES:
            allids += [r["report_id"] for r in src_rows(rel)]
        members = [m for g in self.rg for m in g["member_report_ids"].split(";")]
        self.assertEqual(sorted(members), sorted(allids))
        self.assertEqual(len(members), len(set(members)))
        gid = {m: g["report_group"] for g in self.rg for m in g["member_report_ids"].split(";")}
        for r in self.fa:
            self.assertEqual(r["report_group"], gid[r["report_id"]])
            self.assertTrue(r["site_id"])

    def test_counted_rows(self):
        for r in self.fa:
            ok = r["feature_type"] in bm.CLASSES and r["count_zone"] in bm.ZONES
            self.assertEqual(r["counted"] == "yes", ok)
            if r["phase"] != "1":
                self.assertEqual(r["zone_source"], "source row")

    def test_phase1_zones_agree_with_crosswalk(self):
        xw = [r for r in src_rows("phase2_2026-10-10/phase1_zone_crosswalk.csv") if r["table"] == "features"]
        p1 = [r for r in self.fa if r["source_file"] == "features.csv"]
        self.assertEqual(len(xw), len(p1))
        for a, b in zip(xw, p1):
            self.assertEqual(a["report_id"], b["report_id"])
            if a["region_zone"] in bm.ZONES + ["outside"]:
                self.assertEqual(a["region_zone"], b["count_zone"])

    def test_level_arithmetic(self):
        c = self.summary["counts"]
        for cl in bm.CLASSES:
            for z in bm.ZONES:
                for d in bm.DATING:
                    self.assertLessEqual(c["reports"][cl][z][d], c["rows"][cl][z][d], (cl, z, d))
        tot_rows = sum(c["rows"][cl][z][d] for cl in bm.CLASSES for z in bm.ZONES for d in bm.DATING)
        self.assertEqual(tot_rows, sum(1 for r in self.fa if r["counted"] == "yes"))
        units = Counter()
        for g in self.rg:
            for u in filter(None, g["units"].split("; ")):
                units[u.rsplit("=", 1)[1]] += 1
        for d in bm.DATING:
            self.assertEqual(units[d], self.summary["totals"]["reports"]["all_classes"][d])
        sunits = Counter()
        for s in self.sites:
            for u in filter(None, s["classes"].split("; ")):
                sunits[u.rsplit("=", 1)[1]] += 1
        for d in bm.DATING:
            self.assertEqual(sunits[d], self.summary["totals"]["sites"]["all_classes"][d])

    def test_manual_decisions_hold(self):
        man = rows("data/manual_decisions.csv")
        gid = {m: g["report_group"] for g in self.rg for m in g["member_report_ids"].split(";")}
        sites_of = defaultdict(set)
        for r in self.fa:
            sites_of[(r["report_id"], r["feature_type"])].add(r["site_id"])
            sites_of[(r["report_id"], "")].add(r["site_id"])
        for m in man:
            self.assertTrue(m["reason"].strip() and m["basis"].strip(), m)
            if m["kind"] == "report":
                same = gid[m["id_a"]] == gid[m["id_b"]]
                self.assertEqual(same, m["decision"] == "same", m)
            else:
                a, b = sites_of[(m["id_a"], m["class"])], sites_of[(m["id_b"], m["class"])]
                self.assertTrue(a and b, m)
                if m["decision"] == "same":
                    self.assertEqual(len(a | b), 1, m)

    def test_no_open_review(self):
        for r in rows("pair_candidates.csv"):
            self.assertNotIn("REVIEW:", r["note"], r)

    def test_readme_tables_match_generated(self):
        readme = (LANE / "README.md").read_text(encoding="utf-8")
        for line in (LANE / "summary.md").read_text(encoding="utf-8").split("\n"):
            if line.startswith("| ") and "/" in line:
                self.assertIn(line, readme)


if __name__ == "__main__":
    unittest.main()
