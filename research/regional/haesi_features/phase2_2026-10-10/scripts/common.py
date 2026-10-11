#!/usr/bin/env python3
"""Shared helpers for HA-ESI phase 2: the frozen plan parameters, title normalisation, zones, distances.

The plan parameters are read from the JSON block in PLAN.md (frozen; SHA-256 in README.md).
Grid conversion and distances reuse phase 1 (../../scripts/geo.py), unchanged.
Standard library plus pyproj (through geo.py).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
PLAN_MD = LANE / "PLAN.md"
PHASE1 = LANE.parent
sys.path.insert(0, str(PHASE1 / "scripts"))
import geo  # noqa: E402  (phase-1 grid conversion, EPSG:28191 / EPSG:2039)

DROP_CHARS = "ʿʾ‘’'`´׳ʽʻ’"
SPACE_CHARS = "-–—,.;:()[]/\"״“”"


def norm(s):
    """Phase-1 normalisation (NFKD, marks removed, lower case, apostrophes dropped, punctuation to spaces)."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    for c in DROP_CHARS:
        s = s.replace(c, "")
    for c in SPACE_CHARS:
        s = s.replace(c, " ")
    return " " + " ".join(s.split()) + " "


def plan_params(path=PLAN_MD):
    t = Path(path).read_text(encoding="utf-8")
    m = re.search(r"```json\n(.*?)\n```", t, re.S)
    return json.loads(m.group(1))


def zone_of(lat, lon, params=None):
    """First zone (in the frozen order) whose box contains the point, else None."""
    params = params or plan_params()
    for z in params["zones_order"]:
        for la0, la1, lo0, lo1 in params["zones"][z]:
            if la0 <= lat <= la1 and lo0 <= lon <= lo1:
                if z == "Z3_JUDEAN_DESERT":
                    # Z3 boxes exclude Z2 (already tested first in the order).
                    pass
                return z
    return None


def gazetteer_patterns(params=None):
    params = params or plan_params()
    pats = {}
    for z, g in params["gazetteer"].items():
        pats[z] = sorted(set(norm(p).strip() for p in g["en"] + g["he"] if norm(p).strip()))
    rw = params["region_wide_terms"]
    pats["REGION_WIDE"] = sorted(set(norm(p).strip() for p in rw["en"] + rw["he"]))
    return pats


def title_hits(title, pats):
    nt = norm(title)
    out = {}
    for z, ps in pats.items():
        h = [p for p in ps if (" " + p + " ") in nt]
        if h:
            out[z] = h
    return out


def nearest_place(lat, lon):
    places = geo.load_places()
    d = geo.distances(lat, lon, places)
    return d[0] if d else (None, None)
