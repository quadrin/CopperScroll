"""Tests for the target-volume / excavation-footprint join.

Synthetic fixtures test the join policy only. They are never exported as evidence.
"""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vj = _load("coverage_volume_join_test", HERE / "volume_join.py")
evaluate = _load("coverage_evaluate_volume_test", HERE / "evaluate.py")

FRAMES = {
    "synthetic-up": {"id": "synthetic-up", "units": "m", "metres_per_unit": 1.0, "north_vector": [0, 1], "y_axis": "up"},
    "synthetic-down": {"id": "synthetic-down", "units": "px", "metres_per_unit": 0.5, "north_vector": [0, -1], "y_axis": "down"},
}
SQUARE = [[0, 0], [2, 0], [2, 2], [0, 2]]


def vertical_target(**changes):
    target = {
        "id": "synthetic-target", "label": "Synthetic test only", "horizontal_frame": "synthetic-up",
        "origin": {"point": None},
        "reference_surface": {"elevation_m": 10.0, "vertical_datum_id": "synthetic-datum", "phase_id": "synthetic-A"},
        "region": {"polygon": deepcopy(SQUARE)},
        "measure": {"count": 3, "unit": "cubit"},
        "branch_dimensions": [
            {"id": "direction_model", "options": [{"id": "vertical", "model": "vertical_below_reference"}]},
            {"id": "cubit_length", "options": [{"id": "range", "metres_per_cubit": [0.4, 0.6]}]},
        ],
        "phase": {"id": "synthetic-A"},
        "ancient_accessibility": {"status": "unknown"},
    }
    target.update(changes)
    return target


def horizontal_target(sector=(315, 45), frame="synthetic-up", depth=(0.0, 0.5), origin=(0.0, 0.0)):
    target = vertical_target(horizontal_frame=frame)
    target["origin"] = {"point": list(origin)}
    target["region"] = None
    target["branch_dimensions"][0]["options"] = [{"id": "horizontal", "model": "horizontal_from_origin",
                                                  "sector_deg": list(sector) if sector else None,
                                                  "depth_band_m": list(depth) if depth else None, "radial_tolerance_m": None}]
    return target


def footprint(cuts, frame="synthetic-up", datum="synthetic-datum", **changes):
    record = {
        "id": "synthetic-footprint", "label": "Synthetic footprint", "horizontal_frame": frame,
        "cuts": [dict({"id": f"cut-{i}"}, **cut) for i, cut in enumerate(cuts)],
        "vertical_datum_id": datum, "phase_reached_id": "synthetic-A",
        "disturbance": {"target_zone_assessed": True, "reported": "synthetic"},
        "recording": {"method": "synthetic", "detection_limits": "synthetic"},
        "documented_exclusions": [], "source_ids": ["synthetic-source"],
    }
    record.update(changes)
    return record


def cut(polygon, top=10.5, bottom=8.0):
    return {"polygon": polygon, "top_level_m": top, "bottom_level_m": bottom}


def run(target, record):
    branch = vj.expand_target(target, FRAMES)[0]
    return vj.evaluate_pair(target, branch, record)


class FrameAndDatumTests(unittest.TestCase):
    def test_frame_mismatch_is_rejected(self):
        target = vertical_target()
        branch = vj.expand_target(target, FRAMES)[0]
        record = footprint([cut([[-1, -1], [3, -1], [3, 3], [-1, 3]])], frame="synthetic-down")
        with self.assertRaises(vj.FrameMismatchError):
            vj.join(branch, record)
        result = vj.evaluate_pair(target, branch, record)
        self.assertEqual(result["status"], "undeterminable")
        self.assertEqual(result["frame_check"]["horizontal"], "rejected_mismatch")
        self.assertEqual(result["missing_parameters"], ["frame_registration"])

    def test_datum_mismatch_is_rejected(self):
        target = vertical_target()
        branch = vj.expand_target(target, FRAMES)[0]
        record = footprint([cut([[-1, -1], [3, -1], [3, 3], [-1, 3]])], datum="another-datum")
        with self.assertRaises(vj.DatumMismatchError):
            vj.join(branch, record)
        result = vj.evaluate_pair(target, branch, record)
        self.assertEqual(result["frame_check"]["vertical_datum"], "rejected_mismatch")
        self.assertEqual(result["missing_parameters"], ["vertical_datum_join"])

    def test_unknown_datum_stays_undeterminable(self):
        deep_full_cut = [cut([[-1, -1], [3, -1], [3, 3], [-1, 3]], top=10.5, bottom=0.0)]
        for side in ("target", "footprint"):
            with self.subTest(side=side):
                target = vertical_target()
                record = footprint(deepcopy(deep_full_cut))
                if side == "target":
                    target["reference_surface"]["vertical_datum_id"] = None
                else:
                    record["vertical_datum_id"] = None
                result = run(target, record)
                self.assertEqual(result["status"], "undeterminable")
                self.assertIn(f"{side}{'.reference_surface' if side == 'target' else ''}.vertical_datum_id", result["missing_parameters"])
                self.assertEqual(result["possible_statuses"], ["covered", "partly_covered", "not_covered"])

    def test_unknown_reference_elevation_stays_undeterminable(self):
        target = vertical_target()
        target["reference_surface"]["elevation_m"] = None
        result = run(target, footprint([cut([[-1, -1], [3, -1], [3, 3], [-1, 3]])]))
        self.assertEqual(result["status"], "undeterminable")
        self.assertIn("target.reference_surface.elevation_m", result["missing_parameters"])

    def test_horizontal_disjointness_needs_no_datum(self):
        record = footprint([cut([[10, 10], [12, 10], [12, 12], [10, 12]])], datum=None)
        result = run(vertical_target(), record)
        self.assertEqual(result["status"], "not_covered")
        self.assertEqual(result["missing_parameters"], [])
        # The unknown datum is still carried; it simply was not needed here.
        self.assertIn("footprint.vertical_datum_id", result["open_parameters"])
        self.assertEqual(result["components"]["excavation_reach"]["status"], "undetermined")
        self.assertFalse(result["deposit_absence_inferred"])

    def test_no_recorded_cuts_never_means_not_covered(self):
        result = run(vertical_target(), footprint([]))
        self.assertEqual(result["status"], "undeterminable")
        self.assertIn("footprint.cuts", result["missing_parameters"])

    def test_unknown_values_must_be_explicit(self):
        record = footprint([cut(SQUARE)])
        record.pop("vertical_datum_id")
        with self.assertRaises(vj.RecordError):
            run(vertical_target(), record)
        target = vertical_target()
        target["reference_surface"].pop("phase_id")
        with self.assertRaises(vj.RecordError):
            vj.expand_target(target, FRAMES)

    def test_self_intersecting_polygon_is_rejected(self):
        with self.assertRaises(vj.RecordError):
            run(vertical_target(), footprint([cut([[0, 0], [2, 2], [2, 0], [0, 2]])]))


class CoverageGeometryTests(unittest.TestCase):
    def test_full_cover(self):
        result = run(vertical_target(), footprint([cut([[-1, -1], [3, -1], [3, 3], [-1, 3]])]))
        self.assertEqual(result["status"], "covered")
        self.assertFalse(result["deposit_absence_inferred"])
        self.assertIn("No absence is inferred", result["interpretation"])

    def test_partial_horizontal_overlap(self):
        result = run(vertical_target(), footprint([cut([[1, -1], [3, -1], [3, 3], [1, 3]])]))
        self.assertEqual(result["status"], "partly_covered")

    def test_partial_vertical_reach(self):
        # Target levels are 8.2-8.8 m; the cut stops at 8.5 m.
        result = run(vertical_target(), footprint([cut([[-1, -1], [3, -1], [3, 3], [-1, 3]], bottom=8.5)]))
        self.assertEqual(result["status"], "partly_covered")

    def test_shallow_cut_is_not_covered(self):
        result = run(vertical_target(), footprint([cut([[-1, -1], [3, -1], [3, 3], [-1, 3]], bottom=9.0)]))
        self.assertEqual(result["status"], "not_covered")

    def test_overlapping_cuts_cover_jointly(self):
        cuts = [cut([[-1, -1], [1.5, -1], [1.5, 3], [-1, 3]]), cut([[1, -1], [3, -1], [3, 3], [1, 3]])]
        self.assertEqual(run(vertical_target(), footprint(cuts))["status"], "covered")
        self.assertEqual(run(vertical_target(), footprint(list(reversed(deepcopy(cuts)))))["status"], "covered")

    def test_deep_part_and_shallow_part(self):
        cuts = [cut([[-1, -1], [3, -1], [3, 3], [-1, 3]], bottom=8.6), cut([[-1, -1], [1, -1], [1, 3], [-1, 3]], bottom=8.0)]
        self.assertEqual(run(vertical_target(), footprint(cuts))["status"], "partly_covered")

    def test_non_convex_cut(self):
        l_shape = [[-1, -1], [3, -1], [3, 0.5], [1, 0.5], [1, 3], [-1, 3]]
        self.assertEqual(run(vertical_target(), footprint([cut(l_shape)]))["status"], "partly_covered")

    def test_single_cubit_sample_is_one_level(self):
        target = vertical_target()
        target["branch_dimensions"][1]["options"] = [{"id": "0.50", "metres_per_cubit": [0.5, 0.5]}]
        full = [[-1, -1], [3, -1], [3, 3], [-1, 3]]
        self.assertEqual(run(target, footprint([cut(full, bottom=8.5)]))["status"], "covered")
        self.assertEqual(run(target, footprint([cut(full, bottom=8.6)]))["status"], "not_covered")

    def test_north_centred_sector_wraps_through_north(self):
        target = horizontal_target(sector=(315, 45))
        north_box = [[-2, 0], [2, 0], [2, 2], [-2, 2]]
        east_half = [[0, 0], [2, 0], [2, 2], [0, 2]]
        south_box = [[-2, -2], [2, -2], [2, -0.1], [-2, -0.1]]
        self.assertEqual(run(target, footprint([cut(north_box)]))["status"], "covered")
        self.assertEqual(run(target, footprint([cut(east_half)]))["status"], "partly_covered")
        self.assertEqual(run(target, footprint([cut(south_box)]))["status"], "not_covered")

    def test_y_down_frame_uses_its_own_north_and_scale(self):
        # North is -y and east is +x; 0.5 m per unit puts 1.2-1.8 m at 2.4-3.6 units.
        target = horizontal_target(sector=(80, 100), frame="synthetic-down")
        east_box = [[2, -1], [4, -1], [4, 1], [2, 1]]
        west_box = [[-4, -1], [-2, -1], [-2, 1], [-4, 1]]
        self.assertEqual(run(target, footprint([cut(east_box)], frame="synthetic-down"))["status"], "covered")
        self.assertEqual(run(target, footprint([cut(west_box)], frame="synthetic-down"))["status"], "not_covered")

    def test_horizontal_reading_without_declared_depth_or_sector(self):
        for sector, depth, parameter in (((315, 45), None, "target.direction.depth_band_m"), (None, (0.0, 0.5), "target.direction.sector_deg")):
            with self.subTest(parameter=parameter):
                result = run(horizontal_target(sector=sector, depth=depth), footprint([cut([[-2, 0], [2, 0], [2, 2], [-2, 2]])]))
                self.assertEqual(result["status"], "undeterminable")
                self.assertIn(parameter, result["missing_parameters"])

    def test_known_intersection_excludes_not_covered(self):
        target = vertical_target()
        target["reference_surface"]["phase_id"] = None
        result = run(target, footprint([cut([[1, -1], [3, -1], [3, 3], [1, 3]])]))
        self.assertEqual(result["status"], "undeterminable")
        self.assertEqual(result["possible_statuses"], ["covered", "partly_covered"])


class DeterminismTests(unittest.TestCase):
    def test_join_output_is_deterministic(self):
        target = vertical_target()
        target["branch_dimensions"][1]["options"].append({"id": "0.40", "metres_per_cubit": [0.4, 0.4]})
        record = footprint([cut([[1, -1], [3, -1], [3, 3], [1, 3]])])
        case = {"id": "synthetic-case", "label": "Synthetic", "target_id": target["id"], "footprint_ids": [record["id"]]}
        args = (case, {target["id"]: target}, {record["id"]: record}, FRAMES, [], [])
        first = json.dumps(vj.evaluate_case(*deepcopy(args)), sort_keys=False, ensure_ascii=False, allow_nan=False)
        second = json.dumps(vj.evaluate_case(*deepcopy(args)), sort_keys=False, ensure_ascii=False, allow_nan=False)
        self.assertEqual(first, second)
        self.assertNotIn("probab", first.lower())

    def test_module_build_is_deterministic(self):
        first = json.dumps(evaluate.build(ROOT), ensure_ascii=False, allow_nan=False)
        second = json.dumps(evaluate.build(ROOT), ensure_ascii=False, allow_nan=False)
        self.assertEqual(first, second)


class ImportedCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = evaluate.build(ROOT)
        cls.volume = cls.module["data"]["volume_joins"]
        cls.cases = {case["id"]: case for case in cls.volume["cases"]}

    def test_iv17_chamber_centres_do_not_establish_threshold_coverage(self):
        case = self.cases["coverage-volume-iv17"]
        self.assertEqual(case["summary"]["branches"], 8)
        self.assertEqual(case["summary"]["status_counts"]["undeterminable"], 8)
        for join in case["joins"]:
            with self.subTest(join=join["id"]):
                self.assertNotEqual(join["status"], "covered")
                self.assertIn("footprint.cut.polygon", join["missing_parameters"])
                self.assertIn("target.reference_surface.elevation_m", join["missing_parameters"])
                self.assertFalse(join["deposit_absence_inferred"])
                self.assertEqual(join["frame_check"]["horizontal"], "same")
        result = next(item for item in self.module["results"] if item["id"] == "coverage-volume-iv17")
        self.assertEqual(result["status"], "unknown")

    def test_every_open_parameter_is_mapped_to_a_record_or_declaration(self):
        for case in self.volume["cases"]:
            for row in case["resolution"]:
                with self.subTest(case=case["id"], parameter=row["parameter"]):
                    self.assertTrue(row["mapped"])

    def test_iv17_threshold_records_point_to_the_l656_file(self):
        case = self.cases["coverage-volume-iv17"]
        row = next(item for item in case["resolution"] if item["parameter"] == "target.reference_surface.elevation_m")
        self.assertEqual(row["field_record_ids"], ["coverage-rec-l656-threshold-section"])
        records = {record["id"]: record for record in self.volume["field_records"]}
        self.assertIn("Staff Officer for Judea and Samaria", records["coverage-rec-l656-threshold-section"]["held_by"])
        self.assertEqual(records["coverage-rec-l656-threshold-section"]["inspection"], "not_inspected")

    def test_entry60_distance_band_needs_a_declared_model(self):
        case = self.cases["coverage-volume-tell-es-sultan"]
        self.assertEqual(case["summary"]["status_counts"]["undeterminable"], 4)
        row = next(item for item in case["resolution"] if item["parameter"] == "target.distance_band_m")
        self.assertEqual(row["field_record_ids"], [])
        self.assertEqual(row["requirement_kind"], "model_declaration")
        self.assertTrue(all("target.distance_band_m" in join["missing_parameters"] for join in case["joins"]))

    def test_documented_non_search_stays_a_gap(self):
        footprints = {item["id"]: item for item in self.volume["footprints"]}
        exclusion = footprints["coverage-fp-kenyon-tomb-search"]["documented_exclusions"][0]
        self.assertIsNone(exclusion["polygon"])
        tomb = [join for join in self.cases["coverage-volume-tell-es-sultan"]["joins"] if join["footprint_id"] == "coverage-fp-kenyon-tomb-search"]
        self.assertTrue(all("footprint.cuts" in join["missing_parameters"] for join in tomb))

    def test_no_detection_probability_or_absence_claim(self):
        self.assertFalse(self.volume["summary"]["deposit_absence_inferred"])
        self.assertFalse(self.volume["summary"]["detection_probability_computed"])
        self.assertEqual(self.volume["summary"]["status_counts"]["covered"], 0)
        self.assertFalse(any(target["negative_claim_allowed"] for target in self.module["data"]["targets"]))

    def test_volume_sources_and_features_resolve(self):
        source_ids = {source["id"] for source in self.module["sources"]}
        for collection in ("targets", "footprints", "field_records"):
            for record in self.volume[collection]:
                with self.subTest(record=record["id"]):
                    self.assertTrue(set(record["source_ids"]).issubset(source_ids))
        for source in self.module["sources"]:
            self.assertTrue((ROOT / source["repo_path"]).is_file(), source["id"])
        shared = json.loads((ROOT / "research/feature_workbench/features.json").read_text())["features"]
        feature_ids = {feature["id"] for feature in shared + self.module["features"]}
        for record in self.volume["footprints"]:
            self.assertTrue(set(record["site_feature_ids"]).issubset(feature_ids))

    def test_drift_in_repeated_values_fails(self):
        volume = json.loads((HERE / "volume_inputs.json").read_text())
        register = json.loads((ROOT / evaluate.STATES_REGISTER_PATH).read_text())
        assessment = json.loads((ROOT / evaluate.IV17_ASSESSMENT_PATH).read_text())
        phase = json.loads((ROOT / evaluate.IV17_PHASE_PATH).read_text())
        evaluate._check_volume_imports(ROOT, volume, register, assessment, phase)
        drifted = deepcopy(volume)
        drifted["targets"][0]["reference_surface"]["elevation_m"] = 1.0
        with self.assertRaises(ValueError):
            evaluate._check_volume_imports(ROOT, drifted, register, assessment, phase)
        drifted = deepcopy(volume)
        drifted["targets"][0]["origin"]["present_state_anchor"]["endpoints_px"] = [[548, 386], [500, 400]]
        with self.assertRaises(ValueError):
            evaluate._check_volume_imports(ROOT, drifted, register, assessment, phase)


if __name__ == "__main__":
    unittest.main()
