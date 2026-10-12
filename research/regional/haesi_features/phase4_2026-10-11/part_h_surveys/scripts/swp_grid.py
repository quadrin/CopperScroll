#!/usr/bin/env python3
"""SWP reference squares -> phase-2 zone (INFERENCE; exploratory choice, see NOTES.md).

The Survey of Western Palestine gives each site a square: a capital letter (column, west to east)
and a small letter (row, north to south), one grid across all sheets. The squares are about 9 km.
We fit an affine map from (row, column) to WGS84 (EPSG:4326) on calibration points whose square
is printed in the memoir heading and whose coordinates are already in the repository
(data/swp_grid_calibration.csv). A square is given a zone only when the whole square, widened by
MARGIN square units on every side, falls in one phase-2 zone (or wholly outside the region).
Otherwise the square is 'mixed' and the entry is placed by name or left unlocated (plan section 2).
No coordinate is written for an entry from its square: the square fixes a zone, not a point.

Standard library only (plus the phase-2 common.py for the frozen zone boxes).
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = HERE.parent
PHASE2 = PART.parents[1] / "phase2_2026-10-10"
sys.path.insert(0, str(PHASE2 / "scripts"))
import common  # noqa: E402  (frozen plan parameters and zone_of)

CALIB = PART / "data" / "swp_grid_calibration.csv"
PLACES = PART.parents[3] / "agent_review_2026-10-07" / "wave2" / "W2B_model_v1" / "inputs_v2" / "places_v2.csv"
MARGIN = 0.25   # square units added on each side before testing the zone (about 2.3 km)
SAMPLES = 9     # sample points per side of the widened square


def idx(square):
    """'Os' -> (col, row) as integers (A=0, a=0)."""
    return ord(square[0]) - ord('A'), ord(square[1]) - ord('a')


# Fit groups: the Memoirs III screen was frozen with the volume-III points only; Memoirs II uses all points
# (the Samaria points were added before any volume-II entry was read).
FIT_GROUPS = {"III": ("III",), "II": ("II", "III")}


def load_calibration(path=CALIB, vols=None):
    places = {}
    with open(PLACES, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["lat"] and r["lon"]:
                places[r["place_id"]] = (float(r["lat"]), float(r["lon"]))
    pts = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["lat"]:
                lat, lon = float(r["lat"]), float(r["lon"])
            else:
                pid = r["coord_source"].split()[1]
                lat, lon = places[pid]
            if vols is None or r["swp_vol"] in vols:
                pts.append(dict(r, lat=lat, lon=lon))
    return pts


def _lsq(X, y):
    n = len(X[0])
    A = [[sum(x[i] * x[j] for x in X) for j in range(n)] for i in range(n)]
    B = [sum(x[i] * v for x, v in zip(X, y)) for i in range(n)]
    M = [A[i] + [B[i]] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                M[r] = [a - f * b for a, b in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


def fit(pts=None, group="III"):
    """Affine fit lat, lon = a + b*row + c*col on square centres. Returns (lat_coef, lon_coef)."""
    pts = pts or load_calibration(vols=FIT_GROUPS[group])
    X = [[1.0, idx(p["swp_square"])[1], idx(p["swp_square"])[0]] for p in pts]
    return _lsq(X, [p["lat"] for p in pts]), _lsq(X, [p["lon"] for p in pts])


def to_latlon(row, col, coef):
    la, lo = coef
    return la[0] + la[1] * row + la[2] * col, lo[0] + lo[1] * row + lo[2] * col


def to_rowcol(lat, lon, coef):
    """Inverse of the affine map (fractional row, col)."""
    la, lo = coef
    a, b, c = la[1], la[2], lat - la[0]
    d, e, f = lo[1], lo[2], lon - lo[0]
    det = a * e - b * d
    return (c * e - b * f) / det, (a * f - c * d) / det


def residuals(pts=None, coef=None, group="III"):
    """Offset of each calibration point from its square centre, in square units (row, col)."""
    pts = pts or load_calibration(vols=FIT_GROUPS[group])
    coef = coef or fit(pts)
    out = []
    for p in pts:
        r, c = to_rowcol(p["lat"], p["lon"], coef)
        c0, r0 = idx(p["swp_square"])
        out.append((p["point"], p["swp_square"], r - r0, c - c0))
    return out


def square_zone(square, coef=None, params=None, margin=MARGIN):
    """Zone of a whole square widened by margin: (zone or None for outside, 'clear'|'mixed', zones seen)."""
    coef = coef or fit()
    params = params or common.plan_params()
    c0, r0 = idx(square)
    seen = set()
    h = 0.5 + margin
    for i in range(SAMPLES):
        for j in range(SAMPLES):
            r = r0 - h + 2 * h * i / (SAMPLES - 1)
            c = c0 - h + 2 * h * j / (SAMPLES - 1)
            lat, lon = to_latlon(r, c, coef)
            seen.add(common.zone_of(lat, lon, params) or "OUTSIDE")
    if len(seen) == 1:
        z = seen.pop()
        return (None if z == "OUTSIDE" else z), "clear", [z]
    return None, "mixed", sorted(seen)


if __name__ == "__main__":
    group = "III"
    if sys.argv[1:2] in (["II"], ["III"]):
        group = sys.argv.pop(1)
    coef = fit(group=group)
    print("lat = %.5f %+.5f*row %+.5f*col" % tuple(coef[0]))
    print("lon = %.5f %+.5f*row %+.5f*col" % tuple(coef[1]))
    for name, sq, dr, dc in residuals(coef=coef, group=group):
        print("%-28s %s  row %+.2f  col %+.2f" % (name, sq, dr, dc))
    for sq in sys.argv[1:]:
        print(sq, square_zone(sq, coef))
