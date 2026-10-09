"""Check the frozen Entry 25 aspect rule and IV/17 target declarations.

The checker tests the schema and internal consistency of rules.json. It also
dry-runs the decision rule on synthetic intervals. It never reads a field
record, and it scores no real cave. Repository modules are read, never changed.

Commands (run from anywhere):
    python3 -I -B check_rules.py              # check, then print "rules: ok"
    python3 -I -B check_rules.py dry-run      # decision rule on synthetic intervals
    python3 -I -B check_rules.py instantiate GEOMETRY.json
        # turn rules plus plan geometry into volume_join field values (for later use)

Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys
from itertools import product
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True  # never leave __pycache__ in modules we only read

HERE = Path(__file__).resolve().parent
RULES_PATH = HERE / "rules.json"
RULES_MD_PATH = HERE / "RULES.md"
README_PATH = HERE / "README.md"
REPO_ROOT = HERE.parents[2]
VOLUME_INPUTS = REPO_ROOT / "research/feature_workbench/coverage/volume_inputs.json"
VOLUME_JOIN = REPO_ROOT / "research/feature_workbench/coverage/volume_join.py"
DISCRIMINATE = REPO_ROOT / "research/feature_workbench/decisions/discriminate.py"

PASS, FAIL, INCONCLUSIVE = "pass", "fail", "inconclusive"
NOT_MEASURABLE, SILENT = "not-measurable", "silent"
VERDICTS = (PASS, FAIL, INCONCLUSIVE, NOT_MEASURABLE, SILENT)
EPS = 1e-9
FULL = 360.0
LABELS = ("EVIDENCE", "INFERENCE", "ASSUMPTION")
DECISIONS_BEARING_VALUES = ("both-east", "not-both-east", "undetermined")


# --------------------------------------------------------------------- arcs

class Arc:
    """A clockwise arc on the compass: start in [0, 360), width in [0, 360]."""

    __slots__ = ("start", "width")

    def __init__(self, start: float, width: float):
        if width >= FULL - EPS:
            self.start, self.width = 0.0, FULL
        else:
            if width < 0:
                raise ValueError("Arc width must be non-negative.")
            self.start, self.width = start % FULL, float(width)

    @property
    def full(self) -> bool:
        return self.width >= FULL

    @property
    def end(self) -> float:
        return self.start + self.width

    def as_list(self) -> list[float]:
        return [round(self.start, 6), round(self.end % FULL if not self.full else self.start + FULL, 6)]

    def __repr__(self) -> str:
        return f"Arc({self.start:.3f}, {self.width:.3f})"


def sector(bounds: list[float]) -> Arc:
    """A closed sector [from, to], clockwise. [a, a + 360] is the full circle."""
    lo, hi = float(bounds[0]), float(bounds[1])
    if hi - lo >= FULL:
        return Arc(0.0, FULL)
    width = (hi - lo) % FULL
    if width == 0:
        raise ValueError("A sector needs positive width.")
    return Arc(lo, width)


def interval(nominal: float, half_width: float) -> Arc:
    """nominal ± half_width; the full circle when the half-width reaches 180°."""
    if not math.isfinite(half_width) or half_width >= 180.0:
        return Arc(0.0, FULL)
    if half_width < 0:
        raise ValueError("Half-width must be non-negative.")
    return Arc(nominal - half_width, 2.0 * half_width)


def contains(outer: Arc, inner: Arc) -> bool:
    if outer.full:
        return True
    if inner.full:
        return False
    offset = (inner.start - outer.start) % FULL
    if offset > FULL - EPS:
        offset -= FULL
    return offset >= -EPS and offset + inner.width <= outer.width + EPS


def overlap(a: Arc, b: Arc) -> float:
    """Length of the shared arc."""
    if a.full:
        return b.width
    if b.full:
        return a.width
    total = 0.0
    for k in (-1, 0, 1):
        b0 = b.start + FULL * k
        total += max(0.0, min(a.end, b0 + b.width) - max(a.start, b0))
    return total


def verdict(iv: Arc | None, sec: Arc) -> str:
    """PASS only if the interval lies inside the sector; FAIL only if they share no arc."""
    if iv is None:
        return NOT_MEASURABLE
    if contains(sec, iv):
        return PASS
    if overlap(iv, sec) <= EPS:
        return FAIL
    return INCONCLUSIVE


def hull(a: Arc | None, b: Arc | None) -> Arc | None:
    """Smallest arc containing two arcs."""
    if a is None or b is None:
        return None
    if a.full or b.full:
        return Arc(0.0, FULL)
    width_a = max(a.width, (b.start - a.start) % FULL + b.width)
    width_b = max(b.width, (a.start - b.start) % FULL + a.width)
    if min(width_a, width_b) >= FULL:
        return Arc(0.0, FULL)
    return Arc(a.start, width_a) if width_a <= width_b else Arc(b.start, width_b)


def mean_interval(arcs: list[Arc | None]) -> Arc | None:
    """Mean of the lower ends to mean of the upper ends, after unwrapping.

    None (not measurable) if any arc is missing or full, or if two facings
    could lie 180° or more apart.
    """
    if not arcs or any(arc is None or arc.full for arc in arcs):
        return None
    ref = arcs[0].start
    lows, highs = [], []
    for arc in arcs:
        shift = ((arc.start - ref + 180.0) % FULL) - 180.0
        lows.append(ref + shift)
        highs.append(ref + shift + arc.width)
    if max(highs) - min(lows) >= 180.0:
        return None
    low, high = sum(lows) / len(lows), sum(highs) / len(highs)
    return Arc(low, high - low)


# ------------------------------------------------------------ plan geometry

def _unit(vector: list[float]) -> tuple[float, float]:
    norm = math.hypot(vector[0], vector[1])
    if norm == 0:
        raise ValueError("Zero-length vector.")
    return vector[0] / norm, vector[1] / norm


def east_vector(north_vector: list[float], y_axis: str) -> tuple[float, float]:
    """Same convention as volume_join.annular_sector_pieces."""
    nx, ny = _unit(north_vector)
    if y_axis == "down":
        return -ny, nx
    if y_axis == "up":
        return ny, -nx
    raise ValueError("y_axis must be 'up' or 'down'.")


def frame_azimuth(vector: list[float], north_vector: list[float], y_axis: str) -> float:
    """Azimuth of a frame vector, clockwise from the frame's drawn north."""
    nx, ny = _unit(north_vector)
    ex, ey = east_vector(north_vector, y_axis)
    return math.degrees(math.atan2(vector[0] * ex + vector[1] * ey, vector[0] * nx + vector[1] * ny)) % FULL


def outward_normal(p1, p2, interior) -> tuple[float, float]:
    """Unit normal of chord p1-p2 pointing away from an interior (chamber) point."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    mid = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
    candidate = (dy, -dx)
    side = candidate[0] * (mid[0] - interior[0]) + candidate[1] * (mid[1] - interior[1])
    if side == 0:
        raise ValueError("The interior point lies on the chord line; outward side undefined.")
    if side < 0:
        candidate = (-dy, dx)
    return _unit(list(candidate))


def asin_term(twice_uncertainty: float, length: float) -> float:
    """asin(min(1, 2u/L)) in degrees; inf when 2u >= L (full circle)."""
    if length <= 0 or twice_uncertainty >= length:
        return math.inf
    return math.degrees(math.asin(twice_uncertainty / length))


# ------------------------------------------------------------- rule access

def load_rules(path: Path = RULES_PATH) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def north_allowance(rules: dict, case_id: str, choice: str = "primary") -> float:
    case = next(item for item in rules["aspect_rule"]["north_reference"]["cases"] if item["id"] == case_id)
    if choice == "primary":
        return case["allowance_deg"]
    low, high = case.get("sensitivity_allowance_deg", [case["allowance_deg"]] * 2)
    return {"low": low, "high": high}[choice]


def endpoint_radius_m(rules: dict, choice: str = "primary", stated_precision_m: float | None = None,
                      scale_denominator: float | None = None, metres_per_px: float | None = None) -> float:
    spec = rules["aspect_rule"]["uncertainty"]["endpoint_radius_m"]
    base = spec["primary"] if choice == "primary" else {"low": spec["sensitivity"][0], "high": spec["sensitivity"][1]}[choice]
    floors = [base]
    if stated_precision_m is not None:
        floors.append(stated_precision_m)
    if scale_denominator is not None:
        floors.append(0.0005 * scale_denominator)
    if metres_per_px is not None:
        floors.append(2.0 * metres_per_px)
    return max(floors)


def mouth_half_width(chord_m: float, r_m: float, arrow_len: float | None, arrow_e: float,
                     distortion_deg: float, north_deg: float) -> float:
    """h = asin(min(1,2r/L)) + asin(min(1,2e/La)) + d + n; inf means the full circle."""
    arrow = 0.0 if (arrow_len is None or arrow_e == 0) else asin_term(2.0 * arrow_e, arrow_len)
    return asin_term(2.0 * r_m, chord_m) + arrow + distortion_deg + north_deg


def word_interval(rules: dict, word: str, resolution: int, add_north_deg: float = 0.0) -> Arc:
    spec = rules["aspect_rule"]["uncertainty"]["compass_word"]
    return interval(spec["centres_deg"][word], spec["half_width_deg"][str(resolution)] + add_north_deg)


def east_sectors(rules: dict) -> dict[str, Arc]:
    word = next(item for item in rules["aspect_rule"]["direction_words"] if item["word"] == "east")
    out = {"primary": sector(word["primary_sector_deg"])}
    for item in word["sensitivity_sectors"]:
        out[item["id"]] = sector(item["deg"])
    return out


def northern_member(ma, mb, north_vector, y_axis, metres_per_unit: float, correction_deg: float,
                    alpha_deg: float, r_m: float) -> dict[str, Any]:
    """A6: which midpoint is northern, under north rotations within ±alpha and ±2r."""
    v = [(ma[0] - mb[0]) * metres_per_unit, (ma[1] - mb[1]) * metres_per_unit]
    length = math.hypot(*v)
    psi = frame_azimuth(v, north_vector, y_axis) + correction_deg if length else 0.0
    if alpha_deg >= 180.0:
        low, high = -length, length
    else:
        values = [length * math.cos(math.radians(psi + t)) for t in (-alpha_deg, alpha_deg)]
        for target, value in ((0.0, length), (180.0, -length)):
            t = ((target - psi + 180.0) % FULL) - 180.0
            if -alpha_deg <= t <= alpha_deg:
                values.append(value)
        low, high = min(values), max(values)
    low, high = low - 2.0 * r_m, high + 2.0 * r_m
    decision = "a" if low > 0 else "b" if high < 0 else "undetermined"
    return {"delta_m": [low, high], "northern": decision}


def combine_mouths(verdicts: list[str]) -> str:
    """A8, individual mouths."""
    if not verdicts:
        return SILENT
    if len(verdicts) < 2:
        return NOT_MEASURABLE
    if FAIL in verdicts:
        return FAIL
    if all(v == PASS for v in verdicts):
        return PASS
    if all(v == NOT_MEASURABLE for v in verdicts):
        return NOT_MEASURABLE
    if all(v == SILENT for v in verdicts):
        return SILENT
    return INCONCLUSIVE


def cave_interval(facade: Arc | None, mouth_arcs: list[Arc | None]) -> Arc | None:
    """A8, cave level: hull of the facade normal and the mean mouth facing."""
    if len(mouth_arcs) == 1:
        return mouth_arcs[0]
    return hull(facade, mean_interval(mouth_arcs))


def combine_records(verdicts: list[str]) -> str:
    """A10: several new records for one cave and level."""
    decisive = {v for v in verdicts if v in (PASS, FAIL)}
    if decisive == {PASS, FAIL}:
        return INCONCLUSIVE
    if decisive:
        return decisive.pop()
    for value in (INCONCLUSIVE, NOT_MEASURABLE):
        if value in verdicts:
            return value
    return SILENT


def outcome_id(cave: str, level: str, result: str, reported_only: bool = False) -> str:
    return f"e25aspect:{cave}:{level}:{result}" + (":reported-only" if reported_only else "")


def class_effect(rules: dict, outcome: str) -> dict[str, Any]:
    for row in rules["aspect_rule"]["class_effects"]:
        if row["outcome"] == outcome:
            return row
    return {"outcome": outcome, "effect": None, "removes": [], "c01_members_removed": 0}


# ------------------------------------------------- class bookkeeping (rules)

def _composition_members(rules: dict, part: dict, where: dict | None = None, candidate: str | None = None) -> int:
    fixed = rules["aspect_rule"]["entry25_classes"]["dimensions_all_values"]
    base = 1
    for values in fixed.values():
        base *= len(values)
    count = base
    for dim in ("candidate", "reading", "orientation", "phase"):
        values = list(part[dim])
        if dim == "candidate" and candidate is not None:
            values = [v for v in values if v == candidate]
        if where and dim in where:
            values = [v for v in values if v == where[dim]]
        count *= len(values)
    return count


def effect_footprint(rules: dict, effect: dict | None) -> dict[str, dict[str, int]]:
    """Members per class matched by an effect, and class sizes."""
    out = {}
    for cls in rules["aspect_rule"]["entry25_classes"]["classes"]:
        size = sum(_composition_members(rules, part) for part in cls["composition"])
        matched = 0
        if effect is not None:
            matched = sum(_composition_members(rules, part, effect.get("where", {}), effect["candidate"]) for part in cls["composition"])
        out[cls["id"]] = {"size": size, "matched": matched}
    return out


# ------------------------------------------------------ instantiate (later)

def instantiate(rules: dict, geometry: dict, *, zone: str = "primary", sector_choice: str = "primary") -> dict[str, Any]:
    """Rules plus plan geometry -> volume_join field values.

    geometry = {"frame": {"metres_per_unit", "north_vector", "y_axis"},
                "jambs": [[x, y], [x, y]], "interior": [x, y],
                "inner_chord": [[x, y], [x, y]] (optional), "endpoint_radius_m": optional}
    Coordinates are in frame units. Nothing here reads a record.
    """
    decl = rules["iv17_target_declarations"]
    frame = geometry["frame"]
    mpu = float(frame["metres_per_unit"])
    p1, p2 = [float(v) for v in geometry["jambs"][0]], [float(v) for v in geometry["jambs"][1]]
    r_m = float(geometry.get("endpoint_radius_m", decl["zone_outline"]["r_m"]))
    out_n = outward_normal(p1, p2, geometry["interior"])
    along = _unit([p2[0] - p1[0], p2[1] - p1[1]])
    chord_m = math.hypot(p2[0] - p1[0], p2[1] - p1[1]) * mpu

    zone_spec = decl["zone_outline"]
    if zone != "primary":
        zone_spec = {**zone_spec, **next(item for item in zone_spec["sensitivity"] if item["id"] == zone)}
    d_out, d_in = zone_spec["d_out_m"], zone_spec["d_in_m"]
    if geometry.get("inner_chord"):
        mid = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
        depth_in = max(-((q[0] - mid[0]) * out_n[0] + (q[1] - mid[1]) * out_n[1]) * mpu for q in geometry["inner_chord"])
        d_in = max(d_in, depth_in)
    ext, out_u, in_u = r_m / mpu, (d_out + r_m) / mpu, (d_in + r_m) / mpu
    a = (p1[0] - along[0] * ext, p1[1] - along[1] * ext)
    b = (p2[0] + along[0] * ext, p2[1] + along[1] * ext)
    polygon = [
        [a[0] + out_n[0] * out_u, a[1] + out_n[1] * out_u],
        [b[0] + out_n[0] * out_u, b[1] + out_n[1] * out_u],
        [b[0] - out_n[0] * in_u, b[1] - out_n[1] * in_u],
        [a[0] - out_n[0] * in_u, a[1] - out_n[1] * in_u],
    ]
    origin = [(p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0]

    sec_spec = {"half_width_base_deg": decl["sector"]["half_width_base_deg"], "centre": "inward"}
    if sector_choice != "primary":
        sec_spec = next(item for item in decl["sector"]["sensitivity"] if item["id"] == sector_choice)
    facing_out = frame_azimuth(list(out_n), frame["north_vector"], frame["y_axis"])
    centre = facing_out + (180.0 if sec_spec["centre"] == "inward" else 0.0)
    half = sec_spec["half_width_base_deg"] + asin_term(2.0 * r_m, chord_m) if chord_m > 2.0 * r_m else sec_spec["half_width_base_deg"] + 90.0
    if half >= 180.0:
        start = (centre - 180.0) % FULL
        sector_deg = [round(start, 6), round(start, 6)]
    else:
        sector_deg = [round((centre - half) % FULL, 6), round((centre + half) % FULL, 6)]

    fields = decl["volume_join_fields"]
    return {
        "origin": {"point": [round(v, 6) for v in origin]},
        "region": {"polygon": [[round(x, 6), round(y, 6)] for x, y in polygon]},
        "option_horizontal": {"sector_deg": sector_deg, "depth_band_m": list(fields["option_horizontal"]["depth_band_m"]),
                              "radial_tolerance_m": fields["option_horizontal"]["radial_tolerance_m"]},
        "option_range-0.40-0.60": {"distance_band_m": list(fields["option_range-0.40-0.60"]["distance_band_m"])},
        "diagnostics": {"chord_m": round(chord_m, 6), "outward_facing_frame_deg": round(facing_out, 6),
                        "sector_half_width_deg": round(half, 6), "zone": zone, "sector_choice": sector_choice},
    }


def patch_target(target: dict, values: dict) -> dict:
    """Apply instantiate() output to a copy of the volume_inputs target record."""
    patched = json.loads(json.dumps(target))
    patched["origin"]["point"] = values["origin"]["point"]
    patched["region"] = {**(patched.get("region") or {}), "polygon": values["region"]["polygon"]}
    for dim in patched["branch_dimensions"]:
        for option in dim["options"]:
            if option.get("model") == "horizontal_from_origin":
                option.update(values["option_horizontal"])
            if option["id"] == "range-0.40-0.60":
                option.update(values["option_range-0.40-0.60"])
    return patched


# ----------------------------------------------------- repository modules

def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_volume_join():
    return _load_module("e25rules_volume_join_readonly", VOLUME_JOIN)


def load_volume_inputs() -> dict:
    with open(VOLUME_INPUTS, encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ------------------------------------------------------------------ checks

def _walk_labels(node, path="$"):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("label", "primary_label") and isinstance(value, str):
                yield path + "." + key, value
            yield from _walk_labels(value, path + "." + key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk_labels(value, f"{path}[{index}]")


def check_schema(rules: dict) -> list[str]:
    errors = []
    for key in ("schema_version", "id", "version", "status", "labels", "exposure", "aspect_rule",
                "iv17_target_declarations", "sits_beside", "changes_to_existing_files"):
        if key not in rules:
            errors.append(f"missing top-level key {key}")
    if errors:
        return errors
    if rules["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if rules["changes_to_existing_files"] != []:
        errors.append("changes_to_existing_files must be empty")
    if sorted(rules["labels"]) != sorted(LABELS):
        errors.append("labels must be EVIDENCE, INFERENCE, ASSUMPTION")
    for path, value in _walk_labels(rules):
        if not value.startswith(LABELS):
            errors.append(f"{path}: label {value!r} is not EVIDENCE, INFERENCE or ASSUMPTION")
    aspect = rules["aspect_rule"]
    for key in ("candidates", "azimuth", "north_reference", "mouth_measure", "uncertainty", "direction_words",
                "northern_member_rule", "decision_rule", "levels", "phase_rule", "record_combination",
                "outcome_id_format", "outcome_parts", "entry25_classes", "class_effects"):
        if key not in aspect:
            errors.append(f"aspect_rule missing {key}")
    decl = rules["iv17_target_declarations"]
    for key in ("target_id", "case_id", "footprint_id", "frame", "threshold_chord", "origin_point", "zone_outline",
                "sector", "distance", "depth", "reference_surface", "footprint_reading", "volume_join_fields",
                "requirements", "status_rules", "branches"):
        if key not in decl:
            errors.append(f"iv17_target_declarations missing {key}")
    return errors


def check_aspect(rules: dict) -> list[str]:
    errors = []
    aspect = rules["aspect_rule"]
    if sorted(aspect["candidates"]) != ["iv11", "iv17", "twin"]:
        errors.append("candidates must be iv17, iv11 and twin")
    cases = {case["id"]: case for case in aspect["north_reference"]["cases"]}
    if set(cases) != {"true", "grid", "magnetic_stated", "magnetic_year", "unspecified"}:
        errors.append("north cases must be true, grid, magnetic_stated, magnetic_year, unspecified")
    for case in cases.values():
        if case["allowance_deg"] < 0:
            errors.append(f"north case {case['id']} has a negative allowance")
    low, high = cases["unspecified"]["sensitivity_allowance_deg"]
    if not low < cases["unspecified"]["allowance_deg"] < high:
        errors.append("unspecified north allowance must lie between its sensitivity values")
    unc = aspect["uncertainty"]
    for key in ("endpoint_radius_m", "reported_azimuth_precision_deg"):
        spec = unc[key]
        if not spec["sensitivity"][0] < spec["primary"] < spec["sensitivity"][1]:
            errors.append(f"{key}: primary must lie between its sensitivity values")
    dist = unc["distortion_deg"]
    if not dist["sensitivity"][0] <= dist["scanned_or_printed"] <= dist["sensitivity"][1]:
        errors.append("distortion: primary must lie within its sensitivity values")
    words = unc["compass_word"]
    for res, half in words["half_width_deg"].items():
        if abs(half - 180.0 / int(res)) > EPS:
            errors.append(f"compass resolution {res}: half-width must be {180.0 / int(res)}")
    names = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    if [words["centres_deg"].get(name) for name in names] != [22.5 * i for i in range(16)]:
        errors.append("compass centres must be the 16 winds at 22.5° steps")

    east = next((w for w in aspect["direction_words"] if w["word"] == "east"), None)
    northern = next((w for w in aspect["direction_words"] if w["word"] == "northern"), None)
    if east is None or northern is None:
        return errors + ["direction words east and northern are required"]
    if east["primary_sector_deg"] != [90.0 - words["half_width_deg"]["4"], 90.0 + words["half_width_deg"]["4"]]:
        errors.append("primary east sector must be the four-wind east bin")
    sens = {item["id"]: item for item in east["sensitivity_sectors"]}
    if sens["eight-wind"]["deg"] != [90.0 - words["half_width_deg"]["8"], 90.0 + words["half_width_deg"]["8"]]:
        errors.append("eight-wind sector must be the eight-wind east bin")
    if sens["ne-e-se"]["deg"] != [45.0 - words["half_width_deg"]["8"], 135.0 + words["half_width_deg"]["8"]]:
        errors.append("ne-e-se sector must be the union of the NE, E and SE eight-wind bins")
    arc = sens["sunrise-arc"]
    for obliquity in arc["obliquity_deg"]:
        azimuth = math.degrees(math.acos(math.sin(math.radians(obliquity)) / math.cos(math.radians(arc["latitude_deg"]))))
        if abs(azimuth - arc["deg"][0]) > 1.0 or abs((180.0 - azimuth) - arc["deg"][1]) > 1.0:
            errors.append(f"sunrise arc does not match the solstice azimuth {azimuth:.2f}° for obliquity {obliquity}")
    for name, sec in [("primary", east["primary_sector_deg"])] + [(k, v["deg"]) for k, v in sens.items()]:
        if not contains(sector(sec), Arc(90.0, 0.0)):
            errors.append(f"east sector {name} must contain due east")
    if northern["primary_sector_deg"] is not None:
        errors.append("the designation word northern has no facing sector")
    if not 0 < aspect["decision_rule"]["epsilon_deg"] < 1e-6:
        errors.append("decision epsilon must be tiny and positive")

    parts = aspect["outcome_parts"]
    pattern = re.compile(r"^e25aspect:(\w+):(\w+):([\w-]+)(:reported-only)?$")
    classes = {cls["id"] for cls in aspect["entry25_classes"]["classes"]}
    for row in aspect["class_effects"]:
        match = pattern.match(row["outcome"])
        if not match or match.group(1) not in parts["cave"] or match.group(2) not in parts["level"] or match.group(3) not in parts["verdict"]:
            errors.append(f"bad outcome id {row['outcome']}")
        if row.get("registered_row") and row["decisions_value"] not in DECISIONS_BEARING_VALUES:
            errors.append(f"{row['outcome']}: registered rows must use a decisions bearing value")
        if any(cid not in classes for cid in row["removes"]):
            errors.append(f"{row['outcome']}: unknown class id")
    errors.extend(check_class_effects(rules))
    return errors


def check_class_effects(rules: dict) -> list[str]:
    errors = []
    aspect = rules["aspect_rule"]
    sizes = effect_footprint(rules, None)
    declared = {cls["id"]: cls["members"] for cls in aspect["entry25_classes"]["classes"]}
    for cid, info in sizes.items():
        if info["size"] != declared[cid]:
            errors.append(f"{cid}: composition gives {info['size']} members, declared {declared[cid]}")
    if sum(declared.values()) != 288:
        errors.append("Entry 25 classes must hold 288 branches")
    for row in aspect["class_effects"]:
        effect = row["effect"]
        if effect is None or effect["status"] != "contradicted":
            if row["removes"] or row["c01_members_removed"]:
                errors.append(f"{row['outcome']}: a non-contradicting outcome removes nothing")
            continue
        footprint = effect_footprint(rules, effect)
        removes = sorted(cid for cid, info in footprint.items() if info["matched"] and info["matched"] == info["size"])
        partial = {cid: info["matched"] for cid, info in footprint.items() if 0 < info["matched"] < info["size"]}
        if removes != sorted(row["removes"]):
            errors.append(f"{row['outcome']}: removes {removes}, declared {row['removes']}")
        if partial.get("entry25-c01", 0) != row["c01_members_removed"]:
            errors.append(f"{row['outcome']}: c01 members removed {partial.get('entry25-c01', 0)}, declared {row['c01_members_removed']}")
        if set(partial) - {"entry25-c01"}:
            errors.append(f"{row['outcome']}: splits a class other than c01")
    return errors


def check_targets(rules: dict) -> list[str]:
    errors = []
    decl = rules["iv17_target_declarations"]
    dist = decl["distance"]
    r = dist["origin_uncertainty_m"]
    if abs(dist["single_radial_tolerance_m"]["primary"] - (dist["instruction_tolerance_m"]["primary"] + r)) > EPS:
        errors.append("single-cubit tolerance must equal instruction tolerance plus origin uncertainty")
    for value, base in zip(dist["single_radial_tolerance_m"]["sensitivity"], dist["instruction_tolerance_m"]["sensitivity"]):
        if abs(value - (base + r)) > EPS:
            errors.append("single-cubit tolerance sensitivity must follow the instruction tolerance sensitivity")
    if abs(decl["zone_outline"]["r_m"] - r) > EPS or abs(rules["aspect_rule"]["uncertainty"]["endpoint_radius_m"]["primary"] - r) > EPS:
        errors.append("zone r, origin uncertainty and endpoint radius must agree")
    alt = dist["unit_alternative"]
    if [round(3 * u, 6) for u in alt["metres_per_cubit"]] != alt["three_cubits_m"]:
        errors.append("unit alternative: three cubits must be 3 x unit")
    fields = decl["volume_join_fields"]
    branches = decl["branches"]
    if len(branches) != 8 or len({b["branch_id"] for b in branches}) != 8:
        errors.append("there must be eight distinct branches")
    for branch in branches:
        bid, opts = branch["branch_id"], branch["options"]
        if bid != f"{decl['target_id']}/{opts['direction_model']}/{opts['cubit_length']}":
            errors.append(f"{bid}: id does not match its options")
        three = [round(3 * u, 6) for u in branch["metres_per_cubit"]]
        if three != branch["three_cubits_m"]:
            errors.append(f"{bid}: three cubits must be 3 x unit")
        single = branch["metres_per_cubit"][0] == branch["metres_per_cubit"][1]
        if opts["direction_model"] == "vertical":
            if branch["model"] != "vertical_below_reference" or branch["depth_below_threshold_m"] != three:
                errors.append(f"{bid}: vertical depth must be the three-cubit band")
            if branch["radial_band_m"] is not None or branch["radial_tolerance_m"] is not None:
                errors.append(f"{bid}: vertical branches take no radial band")
        else:
            if branch["model"] != "horizontal_from_origin":
                errors.append(f"{bid}: wrong model")
            if branch["depth_band_m"] != fields["option_horizontal"]["depth_band_m"] or branch["depth_band_m"] != decl["depth"]["horizontal"]["primary"]:
                errors.append(f"{bid}: depth band must match the declared horizontal band")
            if single:
                tol = dist["single_radial_tolerance_m"]["primary"]
                expected = [round(three[0] - tol, 6), round(three[1] + tol, 6)]
                if branch["radial_tolerance_m"] != tol or branch["radial_tolerance_m"] != fields["option_horizontal"]["radial_tolerance_m"]:
                    errors.append(f"{bid}: tolerance must be the declared single-cubit tolerance")
            else:
                expected = [round(three[0] - r, 6), round(three[1] + r, 6)]
                if branch["radial_tolerance_m"] is not None:
                    errors.append(f"{bid}: the range branch takes no tolerance")
                if expected != dist["range_distance_band_m"] or expected != fields["option_range-0.40-0.60"]["distance_band_m"]:
                    errors.append(f"{bid}: range distance band must be the three-cubit band widened by r")
            if [round(v, 6) for v in branch["radial_band_m"]] != expected:
                errors.append(f"{bid}: radial band {branch['radial_band_m']} != {expected}")
    req_ids = [item["id"] for item in decl["requirements"]]
    if len(req_ids) != len(set(req_ids)):
        errors.append("requirement ids must be unique")
    for status, rule in decl["status_rules"].items():
        refs = rule.get("requires", []) + [x for group in rule.get("requires_any_of", []) for x in group]
        for ref in refs:
            if ref not in req_ids:
                errors.append(f"status {status}: unknown requirement {ref}")
    if set(decl["status_rules"]) != {"covered", "partly_covered", "not_covered", "undeterminable"}:
        errors.append("status rules must cover the four join statuses")
    return errors


def check_against_coverage(rules: dict) -> list[str]:
    """Branch ids, options and declaration parameters against the coverage module."""
    errors = []
    decl = rules["iv17_target_declarations"]
    volume = load_volume_inputs()
    target = next((t for t in volume["targets"] if t["id"] == decl["target_id"]), None)
    if target is None:
        return [f"target {decl['target_id']} not in volume_inputs.json"]
    if decl["case_id"] not in {c["id"] for c in volume["cases"]} or decl["footprint_id"] not in {f["id"] for f in volume["footprints"]}:
        errors.append("case or footprint id not in volume_inputs.json")
    dims = target["branch_dimensions"]
    if [d["id"] for d in dims] != decl["branch_dimension_order"]:
        errors.append("branch dimension order differs from volume_inputs.json")
    expected = {}
    for combo in product(*[d["options"] for d in dims]):
        bid = target["id"] + "/" + "/".join(option["id"] for option in combo)
        expected[bid] = {d["id"]: option for d, option in zip(dims, combo)}
    declared = {b["branch_id"]: b for b in decl["branches"]}
    if set(expected) != set(declared):
        errors.append(f"branch ids differ from the join's expansion: {sorted(set(expected) ^ set(declared))}")
    for bid, options in expected.items():
        if bid in declared and options["cubit_length"]["metres_per_cubit"] != declared[bid]["metres_per_cubit"]:
            errors.append(f"{bid}: metres_per_cubit differs from volume_inputs.json")
    addressed = {"target.region.polygon": decl["zone_outline"], "target.origin.point": decl["origin_point"],
                 "target.direction.sector_deg": decl["sector"], "target.direction.depth_band_m": decl["depth"]["horizontal"],
                 "target.direction.radial_tolerance_m": decl["distance"]["single_radial_tolerance_m"]}
    for item in volume["declarations"]:
        if decl["target_id"] in item["applies_to"] and item["parameter"] not in addressed:
            errors.append(f"declaration {item['parameter']} is not addressed")
    try:
        labels = load_volume_join().PARAMETER_LABELS
    except Exception as error:  # pragma: no cover - only when the module is missing
        return errors + [f"volume_join.py could not be loaded: {error}"]
    for item in decl["requirements"]:
        for name in item["volume_join_parameters"]:
            if name not in labels:
                errors.append(f"{item['id']}: {name} is not a volume_join parameter")
    return errors


def check_against_decisions(rules: dict) -> list[str]:
    """Class sizes and every effect against the decisions module's own semantics (read-only)."""
    errors = []
    module = _load_module("e25rules_discriminate_readonly", DISCRIMINATE)
    result = module.analyse(REPO_ROOT)
    family = next(f for f in result["families"] if f["id"] == "entry25")
    inventory = module._load_evaluator(REPO_ROOT, "inventory").build(REPO_ROOT)
    models, _ = module._entry25_models(inventory, "inventory-entry25-target-prerequisites")
    by_id = {m["id"]: m for m in models}
    members = {cls["id"]: cls.get("members") for cls in family["classes"]}
    declared = {cls["id"]: cls["members"] for cls in rules["aspect_rule"]["entry25_classes"]["classes"]}
    for cid, count in declared.items():
        if cid not in members:
            errors.append(f"{cid} not found in the decisions module")
            continue
        size = len(members[cid]) if members[cid] is not None else next(c["member_count"] for c in family["classes"] if c["id"] == cid)
        if size != count:
            errors.append(f"{cid}: decisions module has {size} members, rules declare {count}")
    # Membership lists may be omitted for large classes; rebuild them from compositions.
    for cid in declared:
        if members.get(cid) is None:
            cls = next(c for c in rules["aspect_rule"]["entry25_classes"]["classes"] if c["id"] == cid)
            members[cid] = [m["id"] for m in models if any(all(m["dims"][d] in part[d] for d in ("candidate", "reading", "orientation", "phase")) for part in cls["composition"])]
            if len(members[cid]) != declared[cid]:
                errors.append(f"{cid}: composition matches {len(members[cid])} decisions models, rules declare {declared[cid]}")
    for row in rules["aspect_rule"]["class_effects"]:
        effect = row["effect"]
        if effect is None:
            continue
        removed, partial = [], {}
        for cid, ids in members.items():
            dead = sum(not module.survives(by_id[mid], [effect]) for mid in ids)
            if dead and dead == len(ids):
                removed.append(cid)
            elif dead:
                partial[cid] = dead
        if sorted(removed) != sorted(row["removes"]) or partial.get("entry25-c01", 0) != row["c01_members_removed"] or set(partial) - {"entry25-c01"}:
            errors.append(f"{row['outcome']}: decisions module gives removes={sorted(removed)} partial={partial}")
    return errors


def check_rules_md(rules: dict) -> list[str]:
    """Key numbers of rules.json must appear in RULES.md."""
    text = RULES_MD_PATH.read_text(encoding="utf-8")
    needles = ["45°–135°", "67.5°–112.5°", "62°–118°", "22.5°–157.5°", "0.10 m", "**6°**", "3° and 10°",
               "[1.10, 1.90]", "0.30 m", "[0.00, 1.80]", "d_out = d_in = 0.50 m", "45° + asin(min(1, 2r / L))",
               "**c02, c03, c05**", "**c04, c06**", "**c03**", "0.445–0.525", "1.335–1.575"]
    return [f"RULES.md lacks {needle!r}" for needle in needles if needle not in text]


def check_freeze_record() -> list[str]:
    """The hashes in README.md must match RULES.md and rules.json."""
    text = README_PATH.read_text(encoding="utf-8")
    errors = []
    for name, path in (("RULES.md", RULES_MD_PATH), ("rules.json", RULES_PATH)):
        match = re.search(r"\|\s*`" + re.escape(name) + r"`\s*\|\s*`([0-9a-f]{64})`", text)
        if not match:
            errors.append(f"README.md has no freeze hash for {name}")
        elif match.group(1) != sha256(path):
            errors.append(f"{name} changed after the freeze (README hash {match.group(1)[:12]}…)")
    return errors


def sits_beside_status(rules: dict) -> list[dict[str, Any]]:
    """Informational: has a neighbouring document changed since the freeze?"""
    out = []
    for item in rules["sits_beside"]:
        path = REPO_ROOT / item["path"]
        current = sha256(path) if path.exists() else None
        out.append({"path": item["path"], "unchanged": current == item["sha256"], "exists": current is not None})
    return out


def run_checks(rules: dict | None = None, with_modules: bool = True) -> dict[str, list[str]]:
    rules = rules if rules is not None else load_rules()
    results = {"schema": check_schema(rules)}
    if results["schema"]:
        return results
    results["aspect"] = check_aspect(rules)
    results["targets"] = check_targets(rules)
    results["rules_md"] = check_rules_md(rules)
    results["freeze"] = check_freeze_record()
    missing = [item["path"] for item in sits_beside_status(rules) if not item["exists"]]
    results["sits_beside"] = [f"missing neighbour {path}" for path in missing]
    if with_modules:
        results["coverage_module"] = check_against_coverage(rules)
        results["decisions_module"] = check_against_decisions(rules)
    return results


# ----------------------------------------------------------------- dry run

SYNTHETIC_INTERVALS = [
    ("well inside", 90.0, 10.0),
    ("edge, inside", 125.0, 10.0),
    ("straddles 135", 130.0, 10.0),
    ("touches 135 from outside", 145.0, 10.0),
    ("wholly south-east", 160.0, 10.0),
    ("wraps north", 0.0, 20.0),
    ("wide", 90.0, 60.0),
    ("full circle", 90.0, math.inf),
    ("zero width on edge", 45.0, 0.0),
]


def dry_run(rules: dict | None = None) -> dict[str, Any]:
    """Decision rule on synthetic intervals only. No real record is used."""
    rules = rules if rules is not None else load_rules()
    secs = east_sectors(rules)
    rows = []
    for label, nominal, half in SYNTHETIC_INTERVALS:
        iv = interval(nominal, half)
        rows.append({"case": label, "interval": iv.as_list(),
                     "verdicts": {name: verdict(iv, sec) for name, sec in secs.items()}})
    primary = secs["primary"]
    pairs = [
        ("both inside", [interval(80, 10), interval(100, 10)]),
        ("one straddles", [interval(80, 10), interval(130, 10)]),
        ("one outside", [interval(80, 10), interval(170, 10)]),
        ("one not measurable", [interval(80, 10), None]),
    ]
    mouths = []
    for label, arcs in pairs:
        per = [verdict(arc, primary) for arc in arcs]
        mouths.append({"case": label, "per_mouth": per, "both_mouths": combine_mouths(per)})
    caves = []
    for label, facade, arcs in [
        ("frontage and mouths east", interval(95, 5), [interval(80, 10), interval(100, 10)]),
        ("frontage south-east, mouths east", interval(150, 5), [interval(80, 10), interval(100, 10)]),
        ("both senses south", interval(180, 5), [interval(170, 5), interval(190, 5)]),
    ]:
        iv = cave_interval(facade, arcs)
        caves.append({"case": label, "interval": iv.as_list() if iv else None, "cave": verdict(iv, primary)})
    effects = {oid: class_effect(rules, oid)["removes"] for oid in
               (outcome_id("iv17", "mouths", PASS), outcome_id("iv17", "mouths", FAIL),
                outcome_id("iv17", "mouths", FAIL, True), outcome_id("iv17", "mouths", INCONCLUSIVE),
                outcome_id("iv17", "cave", FAIL))}
    return {"note": "Synthetic intervals only. No real record was scored.", "intervals": rows,
            "both_mouths": mouths, "cave_level": caves, "class_effects": effects}


def _print_dry_run(result: dict) -> None:
    print(result["note"])
    names = list(result["intervals"][0]["verdicts"])
    print("case".ljust(26) + "interval".ljust(20) + "".join(name.ljust(14) for name in names))
    for row in result["intervals"]:
        print(row["case"].ljust(26) + str(row["interval"]).ljust(20) + "".join(row["verdicts"][n].ljust(14) for n in names))
    print("\nindividual mouths (primary sector)")
    for row in result["both_mouths"]:
        print(f"  {row['case']}: {row['per_mouth']} -> {row['both_mouths']}")
    print("\ncave level (primary sector)")
    for row in result["cave_level"]:
        print(f"  {row['case']}: {row['interval']} -> {row['cave']}")
    print("\nclass effects")
    for oid, removed in result["class_effects"].items():
        print(f"  {oid}: removes {removed or 'none'}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="check", choices=("check", "dry-run", "instantiate"))
    parser.add_argument("geometry", nargs="?", help="geometry JSON for instantiate")
    parser.add_argument("--json", action="store_true", help="print machine-readable output")
    parser.add_argument("--no-modules", action="store_true", help="skip the coverage and decisions module cross-checks")
    args = parser.parse_args(argv)
    rules = load_rules()
    if args.command == "dry-run":
        result = dry_run(rules)
        print(json.dumps(result, ensure_ascii=False, indent=1)) if args.json else _print_dry_run(result)
        return 0
    if args.command == "instantiate":
        if not args.geometry:
            parser.error("instantiate needs a geometry JSON file")
        with open(args.geometry, encoding="utf-8") as handle:
            geometry = json.load(handle)
        print(json.dumps(instantiate(rules, geometry), ensure_ascii=False, indent=1))
        return 0
    results = run_checks(rules, with_modules=not args.no_modules)
    failed = {k: v for k, v in results.items() if v}
    neighbours = sits_beside_status(rules)
    if args.json:
        print(json.dumps({"ok": not failed, "errors": results, "sits_beside": neighbours}, ensure_ascii=False, indent=1))
    else:
        for section, errors in results.items():
            print(f"{section}: {'ok' if not errors else 'FAILED'}")
            for error in errors:
                print(f"  - {error}")
        changed = [n["path"] for n in neighbours if n["exists"] and not n["unchanged"]]
        print(f"neighbours unchanged since freeze: {len(neighbours) - len(changed)}/{len(neighbours)}")
        for path in changed:
            print(f"  changed since freeze (informational): {path}")
        print("rules: ok" if not failed else "rules: FAILED")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
