"""Tests for registration.py: fits, withheld check, thresholds and verdicts."""
import importlib.util
import json
import math
import re
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("kc_registration", HERE / "registration.py")
RG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RG)
SHARED = HERE.parents[2] / "research" / "shared_tools"


def similarity_map(scale, rot_deg, tx, ty):
    c, s = scale * math.cos(math.radians(rot_deg)), scale * math.sin(math.radians(rot_deg))
    return lambda p: [c * p[0] - s * p[1] + tx, s * p[0] + c * p[1] + ty]


def record(controls_src, f, check_src, transform="similarity", rps=None, check_rp="RP-SPRING", noise=None, **extra):
    rps = rps or ["RP-TELL-FOOT-E", "RP-TELL-FOOT-W", "RP-TELL-FOOT-S", "RP-MEFJAR", "RP-SAMARAT", "RP-TAWAHIN"]
    noise = noise or [[0, 0]] * len(controls_src)
    controls = [{"rp": rp, "source_xy": p, "target_xy": [f(p)[0] + n[0], f(p)[1] + n[1]]}
                for rp, p, n in zip(rps, controls_src, noise)]
    r = {"document": {"id": "synthetic"}, "transform": transform, "target_relations": ["mouth_10m", "north_sector"],
         "declared_before_fit": "synthetic fixture", "controls": controls,
         "check": {"rp": check_rp, "source_xy": check_src, "target_xy": f(check_src)}}
    r.update(extra)
    return r


SRC = [[0, 0], [400, 0], [0, 300], [420, 310]]
CHECK = [200, 140]


class FitTests(unittest.TestCase):
    def test_similarity_recovers_known_transform(self):
        f = similarity_map(0.95, 12.0, 192000.0, 142000.0)
        out = RG.register(record(SRC, f, CHECK))
        self.assertEqual("accepted", out["status"])
        self.assertAlmostEqual(0.95, out["parameters"]["scale"], places=9)
        self.assertAlmostEqual(12.0, out["parameters"]["rotation_deg"], places=7)
        self.assertLess(out["check_error_m"], 1e-6)
        self.assertEqual(["mouth_10m", "north_sector"], out["accepted_for"])

    def test_pixel_rows_down_are_flipped_before_fitting(self):
        f = similarity_map(0.5, -9.4, 192000.0, 142000.0)  # map from a right-handed frame
        to_px = lambda p: [p[0], -p[1]]  # noqa: E731
        r = record([to_px(p) for p in SRC], lambda q: f(to_px(q)), to_px(CHECK), source_axes="pixel_y_down")
        out = RG.register(r)
        self.assertLess(out["check_error_m"], 1e-6)
        self.assertAlmostEqual(-9.4, out["parameters"]["rotation_deg"], places=7)

    def test_affine_uses_the_shared_fit(self):
        cases = json.loads((SHARED / "calibration_cases.json").read_text(encoding="utf-8"))
        results = {r["id"]: r for r in json.loads((SHARED / "results.json").read_text(encoding="utf-8"))["synthetic_calibration"]}
        for case in cases:
            m = RG.FIT_AFFINE(case["source"], case["destination"])
            pred = RG.TRANSFORM_AFFINE(m, case["heldout"])
            for a, b in zip(pred, results[case["id"]]["predicted"]):
                self.assertAlmostEqual(a, b, places=9)

    def test_affine_record_with_shear(self):
        f = lambda p: [1.1 * p[0] + 0.2 * p[1] + 5, 0.05 * p[0] + 0.9 * p[1] - 3]  # noqa: E731
        out = RG.register(record(SRC, f, CHECK, transform="affine"))
        self.assertEqual("accepted", out["status"])
        self.assertLess(out["check_error_m"], 1e-6)

    def test_noise_sets_acceptance_by_relation_size(self):
        f = similarity_map(1.0, 0.0, 0.0, 0.0)
        for amp, expected in ((1.0, ["mouth_10m", "north_sector"]), (5.0, ["north_sector"]), (20.0, [])):
            noise = [[amp, 0], [-amp, 0], [0, amp], [0, -amp]]
            out = RG.register(record(SRC, f, CHECK, noise=noise))
            self.assertEqual(expected, out["accepted_for"], (amp, out["E_total_m"]))
        out = RG.register(record(SRC, f, CHECK, target_frame={"reference_error_m": 3.0}))
        self.assertEqual(["north_sector"], out["accepted_for"])

    def test_check_error_counts_even_when_residuals_are_zero(self):
        f = similarity_map(1.0, 0.0, 0.0, 0.0)
        r = record(SRC, f, CHECK)
        r["check"]["target_xy"] = [CHECK[0] + 4.0, CHECK[1]]
        out = RG.register(r)
        self.assertAlmostEqual(4.0, out["check_error_m"], places=9)
        self.assertEqual(["north_sector"], out["accepted_for"])


class BlockingTests(unittest.TestCase):
    f = staticmethod(similarity_map(1.0, 0.0, 0.0, 0.0))

    def test_undeclared_check_is_invalid(self):
        r = record(SRC, self.f, CHECK)
        r["declared_before_fit"] = None
        out = RG.register(r)
        self.assertEqual("invalid", out["status"])
        self.assertEqual([], out["accepted_for"])

    def test_check_point_cannot_be_a_control(self):
        out = RG.register(record(SRC, self.f, CHECK, check_rp="RP-TELL-FOOT-E"))
        self.assertEqual("invalid", out["status"])

    def test_too_few_controls(self):
        out = RG.register(record(SRC[:2], self.f, CHECK))
        self.assertEqual("invalid", out["status"])
        out = RG.register(record(SRC[:3], self.f, CHECK, transform="affine"))
        self.assertEqual("invalid", out["status"])

    def test_collinear_controls(self):
        out = RG.register(record([[0, 0], [100, 0], [200, 0], [300, 0]], self.f, CHECK))
        self.assertEqual("invalid", out["status"])

    def test_roles_from_reference_points(self):
        cands = RG.load_reference_points()
        r = record(SRC, self.f, CHECK, rps=["RP-TELL-FOOT-E", "RP-QARANTAL", "RP-TELL-FOOT-S", "RP-MEFJAR"])
        out = RG.register(r, cands)
        self.assertEqual("invalid", out["status"])
        self.assertTrue(any("RP-QARANTAL" in b for b in out["blocking"]))
        r = record(SRC, self.f, CHECK, rps=["RP-TELL-FOOT-E", "RP-NEW", "RP-TELL-FOOT-S", "RP-MEFJAR"])
        self.assertTrue(any("not in reference_points.json" in b for b in RG.register(r, cands)["blocking"]))
        self.assertEqual("accepted", RG.register(record(SRC, self.f, CHECK), cands)["status"])

    def test_extrapolated_check_point_warns(self):
        out = RG.register(record(SRC, self.f, [900, 900]))
        self.assertEqual("accepted_with_warnings", out["status"])


class VerdictTests(unittest.TestCase):
    def test_distance_verdicts(self):
        self.assertEqual("inside", RG.classify_distance(4.0, 10.0, 2.5))
        self.assertEqual("indeterminate", RG.classify_distance(7.0, 10.0, 2.5))
        self.assertEqual("outside", RG.classify_distance(16.0, 10.0, 2.5))

    def test_same_document_pair_uses_picking_error(self):
        self.assertAlmostEqual(math.hypot(0.5, 0.5), RG.pair_error(9.0, 9.0, same_document=True, pick_error_m=0.5))
        self.assertAlmostEqual(math.hypot(3.0, 4.0), RG.pair_error(3.0, 4.0))

    def test_sector_verdict_depends_on_anchor_error(self):
        a = [0.0, 0.0]
        self.assertEqual("inside", RG.classify_sector(a, [0.0, 200.0], 5.0, 0.0)["verdict"])
        self.assertEqual("indeterminate", RG.classify_sector(a, [150.0, 160.0], 5.0, 50.0)["verdict"])
        self.assertEqual("outside", RG.classify_sector(a, [200.0, 0.0], 5.0, 0.0)["verdict"])
        self.assertEqual("outside", RG.classify_sector(a, [0.0, 1300.0], 5.0, 0.0)["verdict"])
        self.assertEqual("indeterminate", RG.classify_sector(a, [0.0, 995.0], 5.0, 0.0)["verdict"])

    def test_bearing_convention(self):
        self.assertAlmostEqual(90.0, RG.bearing([0, 0], [10, 0]))
        self.assertAlmostEqual(0.0, RG.bearing([0, 0], [0, 10]))

    def test_east_west_order(self):
        self.assertEqual("a_east", RG.classify_order(20.0, 0.0, 5.0))
        self.assertEqual("indeterminate", RG.classify_order(8.0, 0.0, 5.0))


class ProtocolTableTests(unittest.TestCase):
    def test_table_ids_match_reference_points(self):
        text = (HERE / "registration_protocol.md").read_text(encoding="utf-8")
        table_ids = set(re.findall(r"^\| (RP-[A-Z0-9-]+) \|", text, flags=re.M))
        self.assertEqual(set(RG.load_reference_points()), table_ids)

    def test_one_default_check(self):
        defaults = [c["id"] for c in RG.load_reference_points().values() if c.get("default_check")]
        self.assertEqual(["RP-SPRING"], defaults)

    def test_thresholds_are_a_quarter_of_the_relation(self):
        self.assertEqual(RG.RELATIONS["mouth_10m"]["size_m"] / 4, RG.RELATIONS["mouth_10m"]["max_error_m"])


if __name__ == "__main__":
    unittest.main()
