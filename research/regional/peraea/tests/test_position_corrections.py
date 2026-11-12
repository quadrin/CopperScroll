#!/usr/bin/env python3
"""Tests for the position corrections of 2026-11-11 (exploratory; the frozen gazetteer is not changed).

    python3 -I -B research/regional/peraea/tests/test_position_corrections.py
"""
import csv
import math
import subprocess
import sys
import unittest
from pathlib import Path

PERAEA = Path(__file__).resolve().parents[1]
REPO = PERAEA.parents[2]


def rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def metres(lat1, lon1, lat2, lon2):
    k = 111320.0
    return math.hypot((lat1 - lat2) * k, (lon1 - lon2) * k * math.cos(math.radians(lat1)))


class Corrections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cor = rows(PERAEA / "gazetteer_position_corrections_2026-11-11.csv")
        cls.gaz = {r["site_id"]: r for r in rows(PERAEA / "gazetteer.csv")}

    def test_frozen_values_are_the_gazetteer_values(self):
        for c in self.cor:
            g = self.gaz[c["site_id"]]
            self.assertEqual((float(c["frozen_lat"]), float(c["frozen_lon"])), (float(g["lat"]), float(g["lon"])))

    def test_distances(self):
        for c in self.cor:
            d = metres(float(c["frozen_lat"]), float(c["frozen_lon"]), float(c["corrected_lat"]), float(c["corrected_lon"]))
            self.assertLess(abs(d - float(c["distance_frozen_to_corrected_m"])), 15, c["site_id"])

    def test_corrected_points_are_in_the_site_table(self):
        sites = rows(REPO / "research/sources/hexagon_registration_2026-11-11/sites.csv")
        for c in self.cor:
            near = min(metres(float(c["corrected_lat"]), float(c["corrected_lon"]), float(s["lat"]), float(s["lon"])) for s in sites)
            self.assertLess(near, 1.0, c["site_id"])

    def test_exploratory_output_matches_a_fresh_run(self):
        r = subprocess.run([sys.executable, "-I", "-B", str(PERAEA / "scripts/run_s2_corrected_positions.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
