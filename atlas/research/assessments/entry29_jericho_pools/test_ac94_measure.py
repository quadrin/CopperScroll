"""Analytical checks for continuous targets and finite-wall eligibility."""
import math
import unittest

from ac94_measure import finite_distance_range, perpendicular_range


class FiniteGeometryTest(unittest.TestCase):
    def assert_range(self, result, expected):
        for value, exact in zip(result, expected):
            self.assertAlmostEqual(value, exact, places=10)

    def test_crossing_target_has_interior_zero(self):
        self.assert_range(finite_distance_range((-2, 0), (2, 0), (0, -1), (0, 1)), (0, 2))

    def test_endpoint_minimum_can_occur_inside_target(self):
        # The closest target point is (0, 2); testing target endpoints misses it.
        self.assert_range(finite_distance_range((-2, 2), (2, 2), (0, 0), (0, 1)),
                          (1, math.sqrt(5)))

    def test_parallel_overlapping_projections(self):
        self.assert_range(finite_distance_range((0, 2), (4, 2), (0, 0), (4, 0)), (2, 2))

    def test_collinear_overlap_and_point_target(self):
        self.assert_range(finite_distance_range((-1, 0), (1, 0), (0, 0), (2, 0)), (0, 1))
        self.assert_range(finite_distance_range((3, 4), (3, 4), (0, 0), (0, 2)),
                          (math.sqrt(13), math.sqrt(13)))

    def test_perpendicular_clips_whole_target_interval(self):
        result = perpendicular_range((-1, 2), (3, 2), (0, 0), (2, 0))
        self.assert_range(result['permitted_target_parameter'], (0.25, 0.75))
        self.assert_range(result['range_px'], (2, 2))

    def test_short_extension_distance_is_inadmissible(self):
        result = perpendicular_range((-2, 1), (-1, 1), (0, 0), (2, 0))
        self.assertIsNone(result['range_px'])
        self.assertIsNone(result['permitted_target_parameter'])
        self.assert_range(finite_distance_range((-2, 1), (-1, 1), (0, 0), (2, 0)),
                          (math.sqrt(2), math.sqrt(5)))


if __name__ == '__main__':
    unittest.main()
