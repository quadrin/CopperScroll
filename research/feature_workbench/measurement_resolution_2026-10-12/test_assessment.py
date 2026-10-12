"""Numeric counterexamples and preserved-source regressions."""
import importlib.util
import json
import math
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = load("assessment")
P = load("proposed_pair_error")


class ResolutionTests(unittest.TestCase):
    def test_scale_and_chord_bounds_hand_calculated(self):
        self.assertEqual([.9, 1.1], M.length_interval(20, 100, 5, 1, 0))
        low, high = M.length_interval(20, 100, 5, 1, 1)
        self.assertAlmostEqual(90 / 102, low)
        self.assertAlmostEqual(110 / 98, high)

    def test_translation_and_rigid_rotation_preserve_distance(self):
        p, q = [0, 0], [3, 4]
        for rotation in (-90, 0, 37, 180):
            a = M.apply_similarity(p, 1, rotation, [192000, 142000])
            b = M.apply_similarity(q, 1, rotation, [192000, 142000])
            self.assertAlmostEqual(5, math.dist(a, b), places=8)

    def test_common_scale_does_not_cancel(self):
        a = M.apply_similarity([0, 0], 1.1, 40, [10000, -10000])
        b = M.apply_similarity([10, 0], 1.1, 40, [10000, -10000])
        self.assertAlmostEqual(11, math.dist(a, b))
        self.assertEqual([9, 11], M.bounded_same_plan_length(10, 0, .1, 0, 0))

    def test_rotation_can_change_east_west_order(self):
        a = M.apply_similarity([0, 0], 1, 180, [200, 100])
        b = M.apply_similarity([10, 0], 1, 180, [200, 100])
        self.assertLess(b[0], a[0])
        self.assertAlmostEqual(10, math.dist(a, b))

    def test_unknown_datum_and_distortion_remain_unknown(self):
        self.assertIsNone(M.bounded_same_plan_length(10, .1, .05, None, 0))
        self.assertIsNone(M.bounded_same_plan_length(10, .1, .05, 0, None))

    def test_touching_windows_do_not_discriminate(self):
        self.assertEqual([1.575, 1.575], M.overlap([1.215, 1.575], [1.575, 1.935]))
        self.assertIsNone(M.overlap([0, 1], [1.01, 2]))

    def test_invalid_scale_and_error_rejected(self):
        for scale in (0, 3):
            with self.assertRaises(ValueError):
                M.length_interval(20, scale, 5, 1, 2)
        for bad in (float("nan"), float("inf"), -1, True):
            with self.assertRaises(ValueError):
                M.finite_nonnegative(bad)

    def test_documentary_failures_and_etri_abstention_preserved(self):
        result = M.calculate(json.loads((HERE / "inputs.json").read_text()))
        pilot = result["pilot_reproduction"]
        self.assertAlmostEqual(8.7899231199045, pilot[0]["primary_error_percent"])
        self.assertAlmostEqual(7.86955936099254, pilot[1]["primary_error_percent"])
        self.assertEqual("unmeasurable", pilot[2]["status"])
        self.assertNotIn("primary_error_percent", pilot[2])

    def test_numeral_overlap_and_additional_error_slack(self):
        result = M.calculate(json.loads((HERE / "inputs.json").read_text()))
        lo, hi = result["ac94"]["bands_overlap_m"]
        self.assertAlmostEqual(10.8, lo)
        self.assertAlmostEqual(14.4, hi)
        self.assertAlmostEqual(.358547, result["ac94"]["additional_source_budget_needed_to_preserve_plan_miss"][0]["additive_must_be_less_than_m"])
        self.assertFalse(result["ac94"]["illustrative_stress_only"][1]["still_below_band_minimum"][0])

    def test_empty_reserved_template_blocks_accuracy(self):
        result = M.calculate(json.loads((HERE / "inputs.json").read_text()))
        self.assertFalse(result["benchmark_readiness"]["ready"])
        self.assertEqual(5, len(result["benchmark_readiness"]["missing"]))
        self.assertFalse(result["siloam"]["metric_offset_test_permitted"])
        for row in result["depth_resolution"]:
            self.assertIsNone(row["total_target_interval_m"])


class PairErrorCorrectionTests(unittest.TestCase):
    def test_unknown_pair_scale_cannot_be_suppressed(self):
        with self.assertRaises(ValueError):
            P.pair_error(9, 9, same_document=True, pick_error_m=.5)

    def test_complete_explicit_pair_error_is_not_combined_with_global_shift(self):
        # Ten-metre pair with a known ±10% scale bound and zero picks: 1 m.
        # A global 99 m shift cancels and cannot be added to this pair bound.
        self.assertEqual(1, P.pair_error(99, 99, same_document=True, pair_local_error_m=1))
        self.assertEqual(0, P.pair_error(99, 99, same_document=True, pair_local_error_m=0))

    def test_legacy_independent_document_proxy_preserved(self):
        self.assertEqual(5, P.pair_error(3, 4))

    def test_double_count_and_invalid_pair_error_rejected(self):
        with self.assertRaises(ValueError):
            P.pair_error(9, 9, same_document=True, pick_error_m=.5, pair_local_error_m=1)
        for bad in (-1, float("nan"), True):
            with self.assertRaises(ValueError):
                P.pair_error(9, 9, same_document=True, pair_local_error_m=bad)


if __name__ == "__main__":
    unittest.main()
