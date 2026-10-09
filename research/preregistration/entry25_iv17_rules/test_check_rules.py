"""Tests for check_rules.py. Synthetic geometry and intervals only; no field record."""

import copy
import json
import math
import unittest

import check_rules as c

RULES = c.load_rules()
PRIMARY = c.east_sectors(RULES)["primary"]


class FreezeAndConsistency(unittest.TestCase):
    def test_all_checks_pass(self):
        results = c.run_checks(RULES)
        self.assertEqual({k: v for k, v in results.items() if v}, {})

    def test_freeze_hashes_match(self):
        self.assertEqual(c.check_freeze_record(), [])

    def test_missing_freeze_record_is_reported(self):
        saved = c.README_PATH
        try:
            c.README_PATH = c.RULES_MD_PATH  # a file without the hash table
            self.assertEqual(len(c.check_freeze_record()), 2)
        finally:
            c.README_PATH = saved

    def test_changed_sector_is_caught(self):
        bad = copy.deepcopy(RULES)
        bad["aspect_rule"]["direction_words"][0]["primary_sector_deg"] = [40.0, 140.0]
        self.assertTrue(c.check_aspect(bad))

    def test_changed_branch_is_caught(self):
        bad = copy.deepcopy(RULES)
        bad["iv17_target_declarations"]["branches"][5]["radial_band_m"] = [1.0, 1.4]
        self.assertTrue(c.check_targets(bad))

    def test_changed_class_effect_is_caught(self):
        bad = copy.deepcopy(RULES)
        bad["aspect_rule"]["class_effects"][1]["removes"] = ["entry25-c02"]
        self.assertTrue(c.check_class_effects(bad))
        self.assertTrue(c.check_against_decisions(bad))

    def test_no_changes_to_existing_files(self):
        self.assertEqual(RULES["changes_to_existing_files"], [])

    def test_eight_branches_match_the_join(self):
        self.assertEqual(c.check_against_coverage(RULES), [])
        self.assertEqual(len(RULES["iv17_target_declarations"]["branches"]), 8)


class DecisionRule(unittest.TestCase):
    def v(self, nominal, half, sec=PRIMARY):
        return c.verdict(c.interval(nominal, half), sec)

    def test_inside_outside_straddle(self):
        self.assertEqual(self.v(90, 10), c.PASS)
        self.assertEqual(self.v(160, 10), c.FAIL)
        self.assertEqual(self.v(130, 10), c.INCONCLUSIVE)

    def test_closed_edges(self):
        self.assertEqual(self.v(125, 10), c.PASS)          # ends exactly at 135
        self.assertEqual(self.v(145, 10), c.FAIL)          # touches 135 only
        self.assertEqual(self.v(45, 0), c.PASS)            # zero width on the edge
        self.assertEqual(self.v(30, 0), c.FAIL)

    def test_full_circle_is_inconclusive(self):
        self.assertEqual(self.v(90, math.inf), c.INCONCLUSIVE)
        self.assertEqual(self.v(90, 180), c.INCONCLUSIVE)

    def test_wraparound_sector(self):
        north = c.sector([315, 45])
        self.assertEqual(c.verdict(c.interval(0, 20), north), c.PASS)
        self.assertEqual(c.verdict(c.interval(350, 30), north), c.PASS)          # 320-20 lies inside
        self.assertEqual(c.verdict(c.interval(340, 30), north), c.INCONCLUSIVE)  # 310-10 crosses 315
        self.assertEqual(c.verdict(c.interval(90, 45), north), c.FAIL)
        self.assertEqual(c.verdict(c.interval(180, 10), north), c.FAIL)

    def test_missing_interval_is_not_measurable(self):
        self.assertEqual(c.verdict(None, PRIMARY), c.NOT_MEASURABLE)

    def test_sensitivity_sectors(self):
        secs = c.east_sectors(RULES)
        self.assertEqual(c.verdict(c.interval(125, 10), secs["eight-wind"]), c.FAIL)
        self.assertEqual(c.verdict(c.interval(125, 10), secs["sunrise-arc"]), c.INCONCLUSIVE)
        self.assertEqual(c.verdict(c.interval(125, 10), secs["ne-e-se"]), c.PASS)


class Arcs(unittest.TestCase):
    def test_overlap_wraps(self):
        self.assertAlmostEqual(c.overlap(c.Arc(350, 20), c.Arc(0, 30)), 10.0)
        self.assertAlmostEqual(c.overlap(c.Arc(0, 360), c.Arc(10, 20)), 20.0)

    def test_hull(self):
        h = c.hull(c.Arc(350, 20), c.Arc(0, 30))
        self.assertAlmostEqual(h.start, 350.0)
        self.assertAlmostEqual(h.width, 40.0)
        self.assertTrue(c.hull(c.Arc(0, 10), c.Arc(180, 10)).width <= 190.0)
        self.assertIsNone(c.hull(None, c.Arc(0, 10)))

    def test_mean_interval(self):
        m = c.mean_interval([c.interval(80, 10), c.interval(100, 10)])
        self.assertAlmostEqual(m.start, 80.0)
        self.assertAlmostEqual(m.width, 20.0)
        wrapped = c.mean_interval([c.interval(350, 5), c.interval(20, 5)])
        self.assertAlmostEqual(wrapped.start, 0.0)
        self.assertIsNone(c.mean_interval([c.interval(0, 10), c.interval(175, 10)]))

    def test_cave_interval(self):
        iv = c.cave_interval(c.interval(150, 5), [c.interval(80, 10), c.interval(100, 10)])
        self.assertEqual(c.verdict(iv, PRIMARY), c.INCONCLUSIVE)
        one = c.cave_interval(None, [c.interval(90, 5)])
        self.assertEqual(c.verdict(one, PRIMARY), c.PASS)


class PlanGeometry(unittest.TestCase):
    def test_azimuth_matches_volume_join_convention(self):
        vj = c.load_volume_join()
        for north, y_axis in (([0, -1], "down"), ([0, 1], "up"), ([1, -1], "down"), ([0.3, 1], "up")):
            for theta in (0.0, 45.0, 123.0, 271.0):
                piece = vj.annular_sector_pieces((0.0, 0.0), [theta - 0.5, theta + 0.5], [1.0, 2.0], north, y_axis, outer=False)[0]
                cx = sum(p[0] for p in piece) / len(piece)
                cy = sum(p[1] for p in piece) / len(piece)
                got = c.frame_azimuth([cx, cy], north, y_axis)
                self.assertAlmostEqual((got - theta + 180) % 360 - 180, 0.0, delta=0.6)

    def test_outward_normal_points_away_from_chamber(self):
        n = c.outward_normal([0, 0], [10, 0], [5, -20])     # chamber above the chord (y down = north)
        self.assertEqual(c.frame_azimuth(list(n), [0, -1], "down"), 180.0)
        with self.assertRaises(ValueError):
            c.outward_normal([0, 0], [10, 0], [20, 0])

    def test_half_width(self):
        self.assertAlmostEqual(c.mouth_half_width(1.0, 0.1, None, 0, 0, 0), math.degrees(math.asin(0.2)))
        self.assertTrue(math.isinf(c.mouth_half_width(0.2, 0.1, None, 0, 1, 6)))
        h = c.mouth_half_width(1.0, 0.1, 100.0, 2.0, 1.0, 6.0)
        self.assertAlmostEqual(h, math.degrees(math.asin(0.2)) + math.degrees(math.asin(0.04)) + 7.0)

    def test_allowances_and_radius(self):
        self.assertEqual(c.north_allowance(RULES, "unspecified"), 6.0)
        self.assertEqual(c.north_allowance(RULES, "unspecified", "high"), 10.0)
        self.assertEqual(c.north_allowance(RULES, "true"), 0.0)
        self.assertAlmostEqual(c.endpoint_radius_m(RULES, scale_denominator=500), 0.25)
        self.assertAlmostEqual(c.endpoint_radius_m(RULES, metres_per_px=0.01), 0.10)

    def test_northern_member(self):
        frame = ([0, -1], "down")
        clear = c.northern_member([300, 0], [0, 263], *frame, 0.01, 0.0, 9.0, 0.1)
        self.assertEqual(clear["northern"], "a")
        flipped = c.northern_member([0, 263], [300, 0], *frame, 0.01, 0.0, 9.0, 0.1)
        self.assertEqual(flipped["northern"], "b")
        east_west = c.northern_member([400, 0], [0, 10], *frame, 0.01, 0.0, 9.0, 0.1)
        self.assertEqual(east_west["northern"], "undetermined")

    def test_compass_words(self):
        self.assertEqual(c.verdict(c.word_interval(RULES, "E", 4), PRIMARY), c.PASS)
        self.assertEqual(c.verdict(c.word_interval(RULES, "NE", 8), PRIMARY), c.INCONCLUSIVE)
        self.assertEqual(c.verdict(c.word_interval(RULES, "N", 4), PRIMARY), c.FAIL)
        self.assertEqual(c.verdict(c.word_interval(RULES, "E", 4, add_north_deg=6.0), PRIMARY), c.INCONCLUSIVE)
        self.assertEqual(c.verdict(c.word_interval(RULES, "ESE", 16), PRIMARY), c.PASS)


class Combinations(unittest.TestCase):
    def test_both_mouths(self):
        P, F, I, N, S = c.PASS, c.FAIL, c.INCONCLUSIVE, c.NOT_MEASURABLE, c.SILENT
        self.assertEqual(c.combine_mouths([P, P]), P)
        self.assertEqual(c.combine_mouths([P, F]), F)
        self.assertEqual(c.combine_mouths([N, F]), F)
        self.assertEqual(c.combine_mouths([P, I]), I)
        self.assertEqual(c.combine_mouths([P, N]), I)
        self.assertEqual(c.combine_mouths([N, N]), N)
        self.assertEqual(c.combine_mouths([S, S]), S)
        self.assertEqual(c.combine_mouths([N, S]), I)
        self.assertEqual(c.combine_mouths([P]), N)
        self.assertEqual(c.combine_mouths([]), S)

    def test_records(self):
        self.assertEqual(c.combine_records([c.PASS, c.FAIL]), c.INCONCLUSIVE)
        self.assertEqual(c.combine_records([c.PASS, c.INCONCLUSIVE]), c.PASS)
        self.assertEqual(c.combine_records([c.SILENT, c.NOT_MEASURABLE]), c.NOT_MEASURABLE)
        self.assertEqual(c.combine_records([c.SILENT]), c.SILENT)

    def test_class_effects(self):
        self.assertEqual(c.class_effect(RULES, c.outcome_id("iv17", "mouths", c.FAIL))["removes"],
                         ["entry25-c02", "entry25-c03", "entry25-c05"])
        self.assertEqual(c.class_effect(RULES, c.outcome_id("iv17", "mouths", c.FAIL, True))["removes"], ["entry25-c03"])
        self.assertEqual(c.class_effect(RULES, c.outcome_id("iv17", "mouths", c.PASS))["removes"], [])
        self.assertEqual(c.class_effect(RULES, c.outcome_id("twin", "cave", c.INCONCLUSIVE))["removes"], [])
        self.assertEqual(c.class_effect(RULES, c.outcome_id("iv17", "cave", c.FAIL))["c01_members_removed"], 24)

    def test_dry_run_is_synthetic_and_stable(self):
        result = c.dry_run(RULES)
        self.assertIn("No real record", result["note"])
        rows = {row["case"]: row["verdicts"]["primary"] for row in result["intervals"]}
        self.assertEqual(rows["straddles 135"], c.INCONCLUSIVE)
        self.assertEqual(rows["touches 135 from outside"], c.FAIL)
        self.assertEqual(json.dumps(result, sort_keys=True), json.dumps(c.dry_run(RULES), sort_keys=True))


class CoverageModuleReadsDeclarations(unittest.TestCase):
    """instantiate() on synthetic geometry, fed to the read-only volume_join library."""

    FRAME_ID = "synthetic-plan"
    FRAME = {"metres_per_unit": 0.01, "north_vector": [0, -1], "y_axis": "down"}
    GEOMETRY = {"frame": FRAME, "jambs": [[500, 500], [586, 500]], "interior": [543, 300]}

    @classmethod
    def setUpClass(cls):
        cls.vj = c.load_volume_join()
        volume = c.load_volume_inputs()
        decl = RULES["iv17_target_declarations"]
        cls.target = next(t for t in volume["targets"] if t["id"] == decl["target_id"])
        cls.footprint = next(f for f in volume["footprints"] if f["id"] == decl["footprint_id"])
        cls.values = c.instantiate(RULES, cls.GEOMETRY)

    def patched(self, elevation=None):
        target = c.patch_target(self.target, self.values)
        target["horizontal_frame"] = self.FRAME_ID
        if elevation is not None:
            target["reference_surface"].update({"elevation_m": elevation, "vertical_datum_id": "syn-datum", "phase_id": "syn-phase"})
        return target

    def footprint_with(self, polygon, top, bottom):
        fp = copy.deepcopy(self.footprint)
        fp["horizontal_frame"] = self.FRAME_ID
        fp["vertical_datum_id"] = "syn-datum" if top is not None else None
        fp["cuts"] = [{"id": "syn-cut", "polygon": polygon, "top_level_m": top, "bottom_level_m": bottom}]
        return fp

    def branches(self, elevation=None):
        return self.vj.expand_target(self.patched(elevation), {self.FRAME_ID: {"id": self.FRAME_ID, **self.FRAME}})

    def test_instantiated_values(self):
        v = self.values
        self.assertEqual(v["origin"]["point"], [543.0, 500.0])
        self.assertAlmostEqual(v["diagnostics"]["outward_facing_frame_deg"], 180.0)
        half = 45.0 + math.degrees(math.asin(0.2 / 0.86))
        self.assertAlmostEqual(v["diagnostics"]["sector_half_width_deg"], round(half, 6))
        self.assertAlmostEqual(v["option_horizontal"]["sector_deg"][0], round((-half) % 360, 6))
        self.assertEqual(v["option_horizontal"]["depth_band_m"], [0.0, 1.8])
        self.assertEqual(v["option_range-0.40-0.60"]["distance_band_m"], [1.1, 1.9])
        xs = [p[0] for p in v["region"]["polygon"]]
        ys = [p[1] for p in v["region"]["polygon"]]
        self.assertEqual((min(xs), max(xs)), (490.0, 596.0))   # chord plus r at each end
        self.assertEqual((min(ys), max(ys)), (440.0, 560.0))   # 0.50 + 0.10 m each side

    def test_inner_chord_extends_zone(self):
        geometry = dict(self.GEOMETRY, inner_chord=[[505, 400], [581, 400]])
        ys = [p[1] for p in c.instantiate(RULES, geometry)["region"]["polygon"]]
        self.assertEqual(min(ys), 390.0)                       # 1.00 m inward plus r

    def test_only_record_parameters_remain_missing(self):
        branches = self.branches()
        self.assertEqual(len(branches), 8)
        record_only = {"target.reference_surface.elevation_m", "target.reference_surface.vertical_datum_id",
                       "target.reference_surface.phase_id"}
        for branch in branches:
            self.assertTrue(set(branch["missing_parameters"]) <= record_only, branch["missing_parameters"])
            self.assertTrue(branch["region_constructed"])

    def test_far_cut_is_not_covered_without_levels(self):
        fp = self.footprint_with([[3000, 3000], [3100, 3000], [3100, 3100], [3000, 3100]], None, None)
        statuses = {self.vj.join(b, fp)["status"] for b in self.branches()}
        self.assertEqual(statuses, {"not_covered"})

    def test_whole_area_cut_covers_every_branch(self):
        big = [[-5000, -5000], [5000, -5000], [5000, 5000], [-5000, 5000]]
        fp = self.footprint_with(big, 101.0, 90.0)
        statuses = {self.vj.join(b, fp)["status"] for b in self.branches(elevation=100.0)}
        self.assertEqual(statuses, {"covered"})

    def test_shallow_cut_is_partial_or_not_covered(self):
        big = [[-5000, -5000], [5000, -5000], [5000, 5000], [-5000, 5000]]
        fp = self.footprint_with(big, 101.0, 98.5)
        result = {b["id"].split("/", 1)[1]: self.vj.join(b, fp)["status"] for b in self.branches(elevation=100.0)}
        self.assertEqual(result["vertical/range-0.40-0.60"], "partly_covered")
        self.assertEqual(result["vertical/0.40"], "covered")       # single level 98.8 m
        self.assertEqual(result["vertical/0.60"], "not_covered")   # single level 98.2 m
        self.assertEqual(result["horizontal/0.50"], "partly_covered")

    def test_unregistered_frame_is_refused(self):
        fp = self.footprint_with([[0, 0], [10, 0], [10, 10]], None, None)
        fp["horizontal_frame"] = "another-plan"
        result = self.vj.evaluate_pair(self.patched(), self.branches()[0], fp)
        self.assertEqual(result["status"], "undeterminable")
        self.assertIn("frame_registration", result["missing_parameters"])


if __name__ == "__main__":
    unittest.main()
