#!/usr/bin/env python3
"""Phase 4, part E, reader r1: convert map references and print the frozen phase-2 zone.

  python3 -I zone_refs.py 23543/61067 1712/1315:OIG ...

A suffix :OIG or :NIG forces the grid; otherwise phase-1 geo.parse_ref decides (northing > 400000 = NIG).
Uses the phase-2 helpers unchanged (common.zone_of, geo.parse_ref, geo.to_wgs84, geo.distances).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parents[3]
sys.path.insert(0, str(LANE / "phase2_2026-10-10" / "scripts"))
import common  # noqa: E402
import geo  # noqa: E402


def main(args):
    places = geo.load_places()
    for a in args:
        g = ""
        if ":" in a:
            a, g = a.split(":")
        r = geo.parse_ref(a, g)
        lat, lon = geo.to_wgs84(r["e"], r["n"], r["grid"])
        d = geo.distances(lat, lon, places)[0]
        print(a, r["grid"], "%.5f" % lat, "%.5f" % lon, common.zone_of(lat, lon) or "outside", d)


if __name__ == "__main__":
    main(sys.argv[1:])
