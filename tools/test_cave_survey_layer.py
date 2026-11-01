"""Regression checks for distinct source coordinates and unchanged survey points."""
import csv
import json
import math
import unittest

from build_cave_survey_layer import SOURCE, OUTPUT, build_collection


class CaveSurveyLayerTests(unittest.TestCase):
    def test_original_points_and_confidence_preserved(self):
        collection = build_collection()
        with SOURCE.open(newline="", encoding="utf-8") as file:
            source = {int(row["point"]): row for row in csv.DictReader(file)}
        self.assertEqual(len(collection["features"]), 27)
        for feature in collection["features"]:
            row = source[feature["properties"]["point"]]
            self.assertEqual(feature["geometry"]["coordinates"], [float(row["lon"]), float(row["lat"])])
            self.assertEqual(feature["properties"]["label_confidence"], row["confidence"])

    def test_alternate_coordinates_remain_separate_and_offset_is_geographic(self):
        collection = build_collection()
        self.assertEqual({row["siglum"] for row in collection["comparisons"]}, {"3Q", "1Q"})
        for row in collection["comparisons"]:
            original = next(f for f in collection["features"] if f["properties"]["point"] == row["point"])
            lon, lat = row["coordinates"]
            old_lon, old_lat = original["geometry"]["coordinates"]
            # Independent short-distance check in metres; detects swapped axes,
            # stale crosswalk offsets and accidental kilometre/degree units.
            east = math.radians(lon-old_lon) * 6371000 * math.cos(math.radians((lat+old_lat)/2))
            north = math.radians(lat-old_lat) * 6371000
            self.assertAlmostEqual(row["offset_m"], math.hypot(east, north), delta=1)
            self.assertGreater(row["offset_m"], 200)
            self.assertNotEqual(row["coordinates"], original["geometry"]["coordinates"])
            self.assertIsNone(row["precision_m"], "IAA accuracy must remain unknown")
        three_q = next(r for r in collection["comparisons"] if r["siglum"] == "3Q")
        self.assertEqual(three_q["coordinates"], [35.460174, 31.759102])
        self.assertEqual(three_q["offset_m"], 233)
        self.assertEqual((three_q["itm_e"], three_q["itm_n"]), (243685, 629635))

    def test_checked_in_output_is_current(self):
        self.assertEqual(json.loads(OUTPUT.read_text(encoding="utf-8")), build_collection())


if __name__ == "__main__":
    unittest.main()
