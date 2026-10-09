"""Tests for the Peraea gazetteer and the W2B v3 model variant.

    python3 -I -B -m unittest discover -s research/regional/peraea/tests -t research/regional/peraea/tests

Checks: frozen plan hashes; gazetteer, feature and source schemas; builders reproduce the committed files;
the switched-off v3 build equals inputs_v2 and the runner reproduces v2; the v3 run is deterministic.
"""
import csv
import hashlib
import importlib.util
import io
import json
import re
import sys
import unittest
from pathlib import Path

PERAEA = Path(__file__).resolve().parents[1]
REPO = PERAEA.parents[2]
W2B = REPO / "research/agent_review_2026-10-07/wave2/W2B_model_v1"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    keep = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = keep
    return mod


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


BG = load("peraea_build_gazetteer", PERAEA / "scripts/build_gazetteer.py")
BV3 = load("peraea_build_inputs_v3", W2B / "inputs_v3/build_inputs_v3.py")
RUN = load("peraea_run_v3", PERAEA / "scripts/run_v3.py")
LABELS = {"EVIDENCE", "INFERENCE", "TRADITION", "CLAIM"}


class PlanHashes(unittest.TestCase):
    def test_plan_json_hash_recorded(self):
        readme = (PERAEA / "README.md").read_text(encoding="utf-8")
        self.assertIn(sha(PERAEA / "plan.json"), readme)
        self.assertEqual(sha(PERAEA / "plan.json"), "010fa981cd2967b8443a1a30566547332758276c96ff596c820f09138393e707")

    def test_plan_v3_hash_recorded(self):
        readme = (PERAEA / "README.md").read_text(encoding="utf-8")
        self.assertIn(sha(PERAEA / "PLAN_v3.md"), readme)

    def test_plan_v3_frozen_inputs_unchanged(self):
        plan = RUN.load_plan()
        for rel, h in plan["frozen_inputs_sha256"].items():
            self.assertEqual(sha(REPO / rel), h, rel)


class Schema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gaz = rows(PERAEA / "gazetteer.csv")
        cls.feat = rows(PERAEA / "features.csv")
        cls.src = rows(PERAEA / "sources.csv")

    def test_columns(self):
        self.assertEqual(list(self.gaz[0]), BG.GAZ_FIELDS)
        self.assertEqual(list(self.feat[0]), BG.FEAT_FIELDS)
        self.assertEqual(list(self.src[0]), BG.SRC_FIELDS)

    def test_gazetteer_values(self):
        ids = [g["site_id"] for g in self.gaz]
        self.assertEqual(len(ids), len(set(ids)))
        for g in self.gaz:
            self.assertIn(g["status"], {"documented", "partial", "excluded"})
            self.assertIn(g["peraea_proper"], {"yes", "no"})
            self.assertIn(g["occupation_dated_in_window"], {"yes", "overlaps", "no", "undated", "unknown"})
            for k in ("occupation_label", "marker_text_label", "marker_arch_label"):
                self.assertIn(g[k], LABELS | {""}, (g["site_id"], k))
            self.assertIn(g["identification_label"], LABELS | {"n.a."})
            if g["lat"]:
                self.assertTrue(31.0 < float(g["lat"]) < 33.0 and 35.0 < float(g["lon"]) < 36.5)
                self.assertGreater(float(g["sigma_km"]), 0)
            if g["status"] == "documented":
                self.assertEqual(g["occupation_label"], "EVIDENCE")
                self.assertEqual(g["occupation_dated_in_window"], "yes")
                self.assertTrue("EVIDENCE" in (g["marker_text_label"], g["marker_arch_label"]), g["site_id"])
                self.assertTrue(g["lat"] and g["in_area"] == "yes", g["site_id"])
            if g["w2b_place_id"]:
                self.assertEqual((g["w2b_place_id"], g["status"], g["peraea_proper"]), ("transjordan", "documented", "yes"))

    def test_features(self):
        sites = {g["site_id"] for g in self.gaz}
        srcs = {s["source_id"] for s in self.src}
        ids = [f["feature_id"] for f in self.feat]
        self.assertEqual(len(ids), len(set(ids)))
        for f in self.feat:
            self.assertIn(f["site_id"], sites)
            self.assertIn(f["feature_type"], BG.FEATURE_TYPES)
            self.assertIn(f["dated_in_window"], BG.WINDOW_VALUES)
            self.assertIn(f["evidence_label"], LABELS)
            self.assertLessEqual(len(f["quote"].split()), 12, f["feature_id"])
            self.assertGreater(len(f["quote"].split()), 0)
            self.assertIn(f["citation"].split()[0].rstrip(";,"), srcs, f["feature_id"])
            self.assertTrue(f["source_url"].startswith("https://"), f["feature_id"])

    def test_sources(self):
        for s in self.src:
            if s["source_id"] != "wikidata":
                self.assertRegex(s["sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(s["url"].startswith("https://"))

    def test_builders_reproduce_files(self):
        out = BG.build()
        for name, b in out.items():
            self.assertEqual((PERAEA / name).read_bytes(), b, name)
        v3 = BV3.build()
        for name, b in v3.items():
            self.assertEqual((W2B / "inputs_v3" / name).read_bytes(), b, name)


class V2Reproduction(unittest.TestCase):
    def test_switch_off_equals_inputs_v2(self):
        off = BV3.build(off=True)
        self.assertEqual(len(off), 6)
        for name, b in off.items():
            self.assertEqual(b, (W2B / "inputs_v2" / name.replace("_v3.csv", "_v2.csv")).read_bytes(), name)

    def test_v3_changes_only_transjordan_components(self):
        def parse(p):
            return list(csv.reader(io.StringIO(Path(p).read_text(encoding="utf-8"), newline="")))
        a, b = parse(W2B / "inputs_v2/places_v2.csv"), parse(W2B / "inputs_v3/places_v3.csv")
        self.assertEqual(len(a), len(b))
        diff = [(x[0], [h for h, u, v in zip(a[0], x, y) if u != v]) for x, y in zip(a, b) if x != y]
        self.assertEqual(diff, [("transjordan", ["precision_string", "coord_note", "components"])])
        tj = [r for r in rows(W2B / "inputs_v3/places_v3.csv") if r["place_id"] == "transjordan"][0]
        doc = [g for g in rows(PERAEA / "gazetteer.csv") if g["w2b_place_id"] == "transjordan"]
        self.assertEqual(len(tj["components"].split("|")), len(doc))

    def test_runner_reproduces_v2(self):
        v2 = RUN.run(RUN.load_data(W2B / "inputs_v2", "v2"))
        chk = RUN.reproduce_v2(v2)
        self.assertTrue(RUN.r0_ok(chk, 1e-8), chk)


class Determinism(unittest.TestCase):
    def test_two_runs_identical_and_match_results(self):
        plan = RUN.load_plan()
        a = RUN.analyse(plan, with_kernel=False)
        b = RUN.analyse(plan, with_kernel=False)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        stored = json.loads((W2B / "outputs_v3/results_v3.json").read_text(encoding="utf-8"))
        stored.pop("kernel_grid", None)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(stored, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
