"""Tests for the Mandate 1:20,000 map regression.

    python3 -I -m unittest discover -s research/regional/mandate_maps -p 'test_*.py'
"""
import csv
import hashlib
import importlib.util
import json
import math
import re
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
KC = REPO / "research/assessments/kohlit_chain"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L = load("mm_lib_t", HERE / "mm_lib.py")
B = load("mm_build_t", HERE / "build.py")
RG = load("kc_registration_t", KC / "registration.py")


def rows(name):
    with open(HERE / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class PlanFreeze(unittest.TestCase):
    def test_plan_hash_matches_readme(self):
        digest = hashlib.sha256((HERE / "plan.json").read_bytes()).hexdigest()
        readme = (HERE / "README.md").read_text(encoding="utf-8")
        m = re.search(r"plan\.json SHA-256 `([0-9a-f]{64})`", readme)
        self.assertIsNotNone(m, "README must record the plan hash")
        self.assertEqual(m.group(1), digest)

    def test_declaration_hash_matches_readme(self):
        readme = (HERE / "README.md").read_text(encoding="utf-8")
        for fname in ("POM-pal20k-z16-19-14.declaration.json", "POM-pal20k-z16-19-14.prepreview.json",
                      "POM-pal20k-z16-19-14.checkpoint.json", "POM-pal20k-z16-19-14.json"):
            digest = hashlib.sha256((KC / "registrations" / fname).read_bytes()).hexdigest()
            self.assertIn(digest, readme, fname)


class Schemas(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((HERE / "plan.json").read_text(encoding="utf-8"))
        self.classes = set(self.plan["legend"]["classes"])
        self.states = set(self.plan["landscape_change"]["states"])

    def test_feature_table(self):
        feats = rows("features.csv")
        self.assertGreater(len(feats), 0)
        for r in feats:
            self.assertIn(r["feature_class"], self.classes, r["item_id"])
            self.assertIn(r["state_2025"], self.states, r["item_id"])
            self.assertEqual("unknown (map)", r["period_in_window"])
            lat, lon = float(r["lat"]), float(r["lon"])
            self.assertTrue(31.6 < lat < 32.3 and 35.2 < lon < 35.6, r["item_id"])
            self.assertGreaterEqual(float(r["position_error_m"]), float(r["pick_error_m"]))
            self.assertTrue(r["evidence_kind"].startswith("EVIDENCE"))

    def test_name_table_and_flags(self):
        names = rows("names.csv")
        self.assertGreater(len(names), 0)
        for r in names:
            self.assertIn(r["feature_class"], self.classes)
            flagged = bool(r["flag_roots"] or r["flag_context"])
            self.assertEqual(flagged, r["flag_label"].startswith("INFERENCE"), r["item_id"])
            self.assertNotIn("(trig)", r["name_as_printed"])

    def test_inputs_are_consistent(self):
        ids = {r["item_id"] for r in rows("items_base.csv")}
        self.assertEqual(len(ids), len(rows("items_base.csv")))
        for r in rows("landscape_change.csv"):
            self.assertIn(r["item_id"], ids)
            self.assertIn(r["state_2025"], self.states)
        for r in rows("g2_controls.csv"):
            self.assertIn(r["item_id"], ids)
        windows = json.loads((HERE / "windows.json").read_text(encoding="utf-8"))
        for r in rows("items_base.csv"):
            self.assertIn(r["window"], windows)
            self.assertIn(r["feature_class"], self.classes)
        for r in rows("g1_picks.csv"):
            self.assertIn(r["status"], {"ok", "ambiguous", "manual", "not_detected"})

    def test_protected_zone_rows_are_marked(self):
        zone = [r for r in rows("features.csv") if r["protected_zone"].startswith("yes")]
        self.assertEqual({"T28", "T32", "T33"}, {r["item_id"] for r in zone})
        for r in zone:
            self.assertIn("after the", r["notes"])


class Residuals(unittest.TestCase):
    def test_known_offset_is_recovered(self):
        E, N = 192000.0, 142000.0
        lat, lon = L.to_wgs(E + 12.0, N - 7.0)
        e, n = L.to_grid(lat, lon)
        de, dn, d = L.residual((e, n), (E, N))
        # the PROJ round trip is good to about 1-2 cm here
        self.assertAlmostEqual(12.0, de, delta=0.05)
        self.assertAlmostEqual(-7.0, dn, delta=0.05)
        self.assertAlmostEqual(math.hypot(12, 7), d, delta=0.05)

    def test_operation_is_pinned(self):
        fwd, inv = L.operation_names()
        self.assertIn(L.OPERATION, fwd)
        self.assertIn(L.OPERATION, inv)

    def test_grid_point_matches_w2b_conversion(self):
        # W2B grid_conversions_v2.csv: OIG 181010/155470 -> 31.99231, 35.32671 with the same operation
        lat, lon = L.to_wgs(181010, 155470)
        self.assertAlmostEqual(31.99231, lat, places=5)
        self.assertAlmostEqual(35.32671, lon, places=5)

    def test_summary_statistics(self):
        s = L.summary([(3.0, 4.0), (-3.0, -4.0), (0.0, 0.0)])
        self.assertEqual(3, s["n"])
        self.assertAlmostEqual(0.0, s["mean_length_m"])
        self.assertAlmostEqual(5.0, s["median_m"])
        self.assertAlmostEqual(5.0, s["max_m"])
        self.assertAlmostEqual(math.sqrt(50 / 3), s["rms_m"])

    def test_similarity_fit_recovers_transform(self):
        c, s_ = 1.01 * math.cos(math.radians(0.3)), 1.01 * math.sin(math.radians(0.3))
        f = lambda p: (c * p[0] - s_ * p[1] + 5.0, s_ * p[0] + c * p[1] - 3.0)  # noqa: E731
        src = [(0, 0), (1000, 0), (0, 1000), (1000, 1000)]
        p = L.fit_similarity(src, [f(q) for q in src])
        self.assertAlmostEqual(1.01, p["scale"], places=9)
        self.assertAlmostEqual(0.3, p["rotation_deg"], places=7)
        for q in [(500, 250), (-200, 900)]:
            for a, b in zip(L.apply_similarity(p, q), f(q)):
                self.assertAlmostEqual(a, b, places=6)

    def test_g1_residuals_from_picks(self):
        g1 = B.g1_residuals(rows("g1_picks.csv"))
        self.assertGreater(len(g1), 40)
        self.assertTrue(all(r["d"] < 25.0 for r in g1), "accepted grid picks lie within 25 m of the nominal grid")
        check = json.loads((HERE / "georef_check.json").read_text(encoding="utf-8"))
        self.assertEqual(16, check["g1_by_sheet"]["19-14"]["n"])


class Names(unittest.TestCase):
    def setUp(self):
        self.roots = json.loads((HERE / "plan.json").read_text(encoding="utf-8"))["toponym_flags"]["roots"]

    def test_root_rule(self):
        self.assertEqual(["k-ḥ-l"], L.root_flags("W. Kuheila", self.roots))
        self.assertEqual(["k-r-m"], L.root_flags("Karm es Samra (El ʿAjaz)", self.roots))
        # documented limits of the frozen patterns
        self.assertEqual([], L.root_flags("ʿEin ed Duyūk", self.roots))
        self.assertEqual(["š-w-h"], L.root_flags("Shawāhid Sayidnā Mūsā", self.roots))

    def test_context_rule_is_window_bound(self):
        self.assertTrue(L.context_flag("Karm es Samra", "B_buqeia"))
        self.assertFalse(L.context_flag("El Mird", "B_hyrcania"))

    def test_translit_expansion(self):
        self.assertEqual("Khirbat Qumrān", L.expand_translit("Kh. Qumrān"))
        self.assertEqual("Wādī Kuheila", L.expand_translit("W. Kuheila"))


class Registration(unittest.TestCase):
    def test_record_passes_validation(self):
        rec = json.loads((KC / "registrations/POM-pal20k-z16-19-14.json").read_text(encoding="utf-8"))
        out = RG.register(rec, RG.load_reference_points())
        self.assertEqual([], out["blocking"])
        self.assertNotEqual("invalid", out["status"])
        saved = json.loads((KC / "registrations/POM-pal20k-z16-19-14.result.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["status"], out["status"])
        self.assertAlmostEqual(saved["check_error_m"], out["check_error_m"], places=6)
        self.assertAlmostEqual(saved["E_total_m"], out["E_total_m"], places=6)

    def test_record_declares_before_fit_and_withholds_spring(self):
        rec = json.loads((KC / "registrations/POM-pal20k-z16-19-14.json").read_text(encoding="utf-8"))
        self.assertTrue(rec["declared_before_fit"])
        self.assertEqual("RP-SPRING", rec["check"]["rp"])
        self.assertNotIn("RP-SPRING", [c["rp"] for c in rec["controls"]])
        decl = json.loads((KC / "registrations/POM-pal20k-z16-19-14.declaration.json").read_text(encoding="utf-8"))
        self.assertEqual("SULTAN-1-precamp-mouth", decl["registered_prediction"]["id"])


class Determinism(unittest.TestCase):
    def test_build_is_deterministic(self):
        outs = ["features.csv", "names.csv", "georef_check.json", "georef_check.csv", "swp_comparison.csv", "summary.json"]
        before = {o: (HERE / o).read_bytes() for o in outs}
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()):
            B.main()
        for o in outs:
            self.assertEqual(before[o], (HERE / o).read_bytes(), o)


if __name__ == "__main__":
    unittest.main()
