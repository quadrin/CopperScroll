#!/usr/bin/env python3
"""Tests for the merged regional inventory, phases 1-4 (standard library only).

Run from the repository root:
    python3 -I -B -m unittest discover -s research/regional/haesi_features/merged_2026-10-12/tests
"""
import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
HAESI = LANE.parent
OLD = HAESI / "merged_2026-10-11"
REPO = LANE.parents[3]
EXT_SHA256 = "bedae3bf7ead121f84790d6346723c5e42bcf8e2aa9e00d833234a781803c3cf"
EXT_FREEZE_COMMIT = "f596618"
PLAN_SHA256 = "ff13b357ae37c558bf5cebba0db01541cc0d17db0d2b12e1c7b8fe0710be676f"
OUTPUTS = ["features_all.csv", "report_groups.csv", "sites.csv", "conflicts.csv", "pair_candidates.csv", "site_review.csv",
           "ha_esi_volume_map.csv", "summary.json", "summary.md"]

_spec = importlib.util.spec_from_file_location("build_merged_p4", LANE / "scripts" / "build_merged.py")
bm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bm)


def rows(name, base=LANE):
    with open(base / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def src_rows(rel):
    with open(HAESI / rel, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def git(*args):
    try:
        out = subprocess.run(["git", "-C", str(REPO)] + list(args), capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return out if out.returncode == 0 else None


class TestPlan(unittest.TestCase):
    def test_extension_hash(self):
        h = hashlib.sha256((LANE / "PLAN_EXTENSION.md").read_bytes()).hexdigest()
        self.assertEqual(h, EXT_SHA256)
        self.assertIn(EXT_SHA256, (LANE / "README.md").read_text(encoding="utf-8"))
        s = json.loads((LANE / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(s["plan"]["extension"]["sha256"], EXT_SHA256)
        self.assertEqual(s["plan"]["sha256"], PLAN_SHA256)
        self.assertEqual(hashlib.sha256((OLD / "DEDUPE_PLAN.md").read_bytes()).hexdigest(), PLAN_SHA256)

    def test_freeze_commit_holds_only_the_extension(self):
        out = git("show", "--name-only", "--format=", EXT_FREEZE_COMMIT)
        if out is None:
            self.skipTest("git or freeze commit not available")
        files = [x for x in out.stdout.split("\n") if x.strip()]
        self.assertEqual(files, ["research/regional/haesi_features/merged_2026-10-12/PLAN_EXTENSION.md"])

    def test_extension_unchanged_since_freeze(self):
        out = git("show", "%s:research/regional/haesi_features/merged_2026-10-12/PLAN_EXTENSION.md" % EXT_FREEZE_COMMIT)
        if out is None:
            self.skipTest("git or freeze commit not available")
        self.assertEqual(hashlib.sha256(out.stdout.encode("utf-8")).hexdigest(), EXT_SHA256)


class TestNoPhaseFileChanged(unittest.TestCase):
    def test_inputs_match_summary_hashes(self):
        s = json.loads((LANE / "summary.json").read_text(encoding="utf-8"))
        for rel, info in list(s["inputs"].items()) + list(s["report_inputs"].items()):
            self.assertEqual(hashlib.sha256((HAESI / rel).read_bytes()).hexdigest(), info["sha256"], rel)
        for rel, h in s["phase4"]["old_inputs"].items():
            self.assertEqual(hashlib.sha256((LANE / rel).read_bytes()).hexdigest(), h, rel)

    def test_git_changes_only_this_lane(self):
        out = git("diff", "--name-only", EXT_FREEZE_COMMIT + "^", "HEAD", "--", "research/regional/haesi_features")
        if out is None:
            self.skipTest("git or freeze commit not available")
        changed = [x for x in out.stdout.split("\n") if x.strip()]
        # B3: phase READMEs and addenda may change; the frozen inputs may not.
        frozen = set("research/regional/haesi_features/" + rel for rel in
                     json.loads((LANE / "summary.json").read_text(encoding="utf-8"))["inputs"])
        frozen.discard("research/regional/haesi_features/phase4_2026-10-11/part_f_iaa_reports/reading_addendum_2026-10-12/features.csv")
        for f in changed:
            self.assertTrue(f.startswith("research/regional/haesi_features/merged_2026-10-12/") or f not in frozen, f)


class TestHelpers(unittest.TestCase):
    def test_permits_extension(self):
        self.assertEqual(bm.permits("A-4604/2005; A-4710/2006"), {"A4604", "A4710"})
        self.assertEqual(bm.permits("A-4604"), {"A4604"})
        self.assertEqual(bm.permits("S-123/2005"), {"S1232005"})  # A1 kept for other prefixes
        self.assertEqual(bm.permits("A-2900 (northern area), A-3130 (southern area)"), {"A2900", "A3130"})
        self.assertEqual(bm.permits("License No. G-12/2010"), bm.permits("G-12/2010"))

    def test_phase4_keys(self):
        self.assertEqual(bm.name_keys("Coins from the Excavation near Warren’s Gate, Jerusalem", True)[0], "warrens")
        self.assertEqual(bm.name_keys("Excavations near Warren's Gate, Jerusalem", True)[0], "warrens")
        # phase 1-3 keys are the frozen ones
        self.assertEqual(bm.name_keys("Jerusalem, Pisgat Ze’ev (East A)")[0], "pisgat zeev")
        self.assertEqual(bm.name_keys("Coins, Warren's Gate")[0], "coins")

    def test_n4(self):
        a = dict(keys=bm.name_keys("Jerusalem, Giv‘ati Parking Lot"), toks=bm.all_tokens("Jerusalem, Giv‘ati Parking Lot"))
        b = dict(keys=bm.name_keys("Coins from Givʻati Parking Lot, Jerusalem", True), toks=bm.all_tokens("Coins from Givʻati Parking Lot, Jerusalem", True))
        self.assertTrue(bm.n4_test(a, b))


class TestPhases13(unittest.TestCase):
    def test_phases13_reproduce_merged_2026_10_11(self):
        with tempfile.TemporaryDirectory() as d:
            bm.main(d, phases13=True)
            for name in OUTPUTS:
                self.assertEqual(Path(d, name).read_bytes(), (OLD / name).read_bytes(), name)

    def test_frozen_decisions_carried_over(self):
        old = (OLD / "data" / "manual_decisions.csv").read_bytes()
        new = (LANE / "data" / "manual_decisions.csv").read_bytes()
        self.assertTrue(new.startswith(old))
        self.assertEqual(len(rows("data/manual_decisions.csv", OLD)), 88)


class TestBuild(unittest.TestCase):
    def test_rebuild_is_identical(self):
        with tempfile.TemporaryDirectory() as d:
            bm.main(d)
            for name in OUTPUTS:
                self.assertEqual(Path(d, name).read_bytes(), (LANE / name).read_bytes(), name)


class TestTables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fa = rows("features_all.csv")
        cls.rg = rows("report_groups.csv")
        cls.sites = rows("sites.csv")
        cls.summary = json.loads((LANE / "summary.json").read_text(encoding="utf-8"))
        cls.sources = list(bm.FEATURE_SOURCES13) + bm.FEATURE_SOURCES4
        cls.rsources = list(bm.REPORT_SOURCES13) + bm.REPORT_SOURCES4

    def test_every_source_row_once_in_order(self):
        i = 0
        for _, rel in self.sources:
            for k, r in enumerate(src_rows(rel), 1):
                m = self.fa[i]
                self.assertEqual(m["row_uid"], "%s#%d" % (rel, k))
                for col in ("report_id", "feature_type", "dated_in_window", "quote", "lat", "lon"):
                    self.assertEqual(m[col], r[col], (rel, k, col))
                i += 1
        self.assertEqual(i, len(self.fa))

    def test_columns(self):
        with open(HAESI / "phase2_2026-10-10/features.csv", newline="", encoding="utf-8") as f:
            p2 = next(csv.reader(f))
        with open(LANE / "features_all.csv", newline="", encoding="utf-8") as f:
            hdr = next(csv.reader(f))
        self.assertEqual(hdr[:len(p2) + 4], p2 + ["phase", "source_file", "report_group", "site_id"])
        for _, rel in bm.FEATURE_SOURCES4 + bm.REPORT_SOURCES4:
            with open(HAESI / rel, newline="", encoding="utf-8") as f:
                h = next(csv.reader(f))
            ref = "features.csv" if rel.endswith("features.csv") or "features_" in rel else "reports.csv"
            with open(HAESI / "phase2_2026-10-10" / ref, newline="", encoding="utf-8") as f:
                self.assertEqual(h, next(csv.reader(f)), rel)

    def test_groups_partition_reports(self):
        allids = []
        for _, rel in self.rsources:
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
            if r["source_file"] in bm.NEVER_COUNTED:
                self.assertEqual(r["counted"], "no")
                self.assertIn("|", r["count_zone"])
                continue
            ok = r["feature_type"] in bm.CLASSES and r["count_zone"] in bm.ZONES
            self.assertEqual(r["counted"] == "yes", ok)
            if r["phase"] != "1":
                self.assertEqual(r["zone_source"], "source row")

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

    def test_phase4_split_adds_up(self):
        p = self.summary["phase4"]["levels"]
        n4 = sum(1 for r in self.fa if r["counted"] == "yes" and r["phase"].startswith("4"))
        self.assertEqual(p["rows"]["phase4"]["all_classes"]["all"], n4)
        for lv in ("reports", "sites"):
            for d in bm.DATING + ["all"]:
                parts = sum(p[lv][k]["all_classes"][d] for k in ("phase4_only", "shared", "phase13_only"))
                self.assertEqual(parts, self.summary["totals"][lv]["all_classes"][d], (lv, d))
        # phase-4-only report units: every row of the unit is a phase-4 row
        rows_of = defaultdict(list)
        for r in self.fa:
            if r["counted"] == "yes":
                rows_of[(r["report_group"], r["feature_type"], r["level2_zone"])].append(r["phase"])
        only4 = sum(1 for v in rows_of.values() if all(x.startswith("4") for x in v))
        self.assertEqual(only4, p["reports"]["phase4_only"]["all_classes"]["all"])

    def test_manual_decisions_hold(self):
        man = rows("data/manual_decisions.csv")
        gid = {m: g["report_group"] for g in self.rg for m in g["member_report_ids"].split(";")}
        sites_of = defaultdict(set)
        for r in self.fa:
            sites_of[(r["report_id"], r["feature_type"])].add(r["site_id"])
            sites_of[(r["report_id"], "")].add(r["site_id"])
        for i, m in enumerate(man):
            self.assertTrue(m["reason"].strip() and m["basis"].strip(), m)
            self.assertIn(m["decision"], ("same", "different", "undetermined"))
            if i >= 88:
                self.assertTrue(m["reason"].startswith("INFERENCE"), m)
            if m["kind"] == "report":
                if m["decision"] == "same":
                    self.assertEqual(gid[m["id_a"]], gid[m["id_b"]], m)
                elif m["decision"] == "different":
                    self.assertNotEqual(gid[m["id_a"]], gid[m["id_b"]], m)
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

    def test_readme_counts(self):
        readme = (LANE / "README.md").read_text(encoding="utf-8")
        d = self.summary["distinct"]
        p = self.summary["phase4"]

        def n(x):
            return "{:,}".format(x)
        for x in (d["rows_all"], d["reports_coded"], d["rows_counted"], d["sites_with_counted_rows"], d["report_groups"], d["sites"],
                  self.summary["totals"]["reports"]["all_classes"]["all"], self.summary["totals"]["sites"]["all_classes"]["all"],
                  p["levels"]["rows"]["phase4"]["all_classes"]["all"], p["levels"]["reports"]["phase4_only"]["all_classes"]["all"],
                  p["levels"]["sites"]["phase4_only"]["all_classes"]["all"], p["levels"]["reports"]["shared"]["all_classes"]["all"],
                  p["levels"]["sites"]["shared"]["all_classes"]["all"], p["report_groups_joined_to_phase13"],
                  p["phase4_reports_joined_to_phase13"], p["report_groups_with_phase4"], p["report_groups_phase4_only"],
                  self.summary["sensitivity_sites_without_S2"]["sites_with_counted_rows"], sum(self.summary["conflicts_by_type"].values())):
            self.assertIn(n(x), readme, x)
        man = rows("data/manual_decisions.csv")
        self.assertIn(n(len(man)), readme)
        new = Counter(m["decision"] for m in man[88:] if m["kind"] == "report")
        self.assertIn("%d same, %d different, %d undetermined" % (new["same"], new["different"], new["undetermined"]), readme)
        listed = sum(1 for r in rows("pair_candidates.csv") if "LISTED:" in r["note"])
        self.assertIn("%d R6 pairs listed but not reviewed" % listed, readme)


if __name__ == "__main__":
    unittest.main()
