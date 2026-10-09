#!/usr/bin/env python3
"""Map-reference parsing, grid conversion and distances for the HA-ESI feature list.

Conventions (search_plan.json, 'location'):
- Old Israel Grid (OIG) -> WGS84 with EPSG:28191, exactly as W2B scripts/grid_convert.py oig().
- New Israel Grid (NIG) -> WGS84 with EPSG:2039 (Israel 1993 / Israeli TM Grid).
- Grid choice: the report's label if given; else northing (metres) above 400000 = NIG, below 300000 = OIG.
- Digits: 3 = km, 4 = 100 m, 5 = 10 m, 6 = 1 m. Precision = that unit.
- A range such as 222307-35 keeps its first full number.
"""
import csv
import math
import re
from pathlib import Path

from pyproj import Transformer

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PLACES = REPO / "research" / "agent_review_2026-10-07" / "wave2" / "W2B_model_v1" / "inputs_v2" / "places_v2.csv"

_T_OIG = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)
_T_NIG = Transformer.from_crs("EPSG:2039", "EPSG:4326", always_xy=True)
UNIT = {3: 1000, 4: 100, 5: 10, 6: 1}


def km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km (R = 6371.0088 km), as W2B grid_convert.km()."""
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _num(tok):
    """'222307' -> (222307, 1); '2222' -> (222200, 100); '09820' -> (98200, 10)."""
    d = len(tok)
    if d not in UNIT:
        raise ValueError(f"unsupported digit count in {tok!r}")
    return int(tok) * UNIT[d], UNIT[d]


def parse_ref(text, grid_label=""):
    """Parse 'E/N' (ranges allowed). Returns dict(e, n, unit_m, grid, swapped)."""
    m = re.search(r"(\d{3,6})(?:\s*[–-]\s*\d+)?\s*[/.]\s*(\d{3,6})", text)
    if not m:
        raise ValueError(f"no map reference in {text!r}")
    e, ue = _num(m.group(1))
    n, un = _num(m.group(2))
    swapped = False
    if e > 400000 and n < 300000:  # northing written first
        e, n, ue, un = n, e, un, ue
        swapped = True
    grid = grid_label.upper()
    if grid not in ("OIG", "NIG"):
        if n > 400000:
            grid = "NIG"
        elif n < 300000:
            grid = "OIG"
        else:
            raise ValueError(f"cannot tell the grid of {text!r}")
    return dict(e=e, n=n, unit_m=max(ue, un), grid=grid, swapped=swapped)


def to_wgs84(e, n, grid):
    t = _T_OIG if grid == "OIG" else _T_NIG
    lon, lat = t.transform(e, n)
    return lat, lon


def load_places(path=PLACES):
    """Places with a point (mixture rows and transjordan excluded)."""
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not r["lat"] or not r["lon"]:
                continue
            out.append(dict(place_id=r["place_id"], name=r["name"], lat=float(r["lat"]), lon=float(r["lon"]),
                            sigma_km=float(r["sigma_km"]), region=r["model_region"]))
    return out


def distances(lat, lon, places):
    """Sorted list of (km, place_id)."""
    return sorted((round(km(lat, lon, p["lat"], p["lon"]), 3), p["place_id"]) for p in places)
