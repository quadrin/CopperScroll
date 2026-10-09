"""Join an excavation footprint to a text-defined ancient target volume.

A target-volume record holds what a textual instruction defines: origin
feature, ancient reference surface and datum, direction model and sector,
distance band, depth band from the stated cubits, and phase. A footprint
record holds what an excavation reached: cut outlines in a stated frame, top
and bottom levels, datum, phase reached, disturbance and recording method.

The join reports spatial coverage only: covered, partly_covered, not_covered
or undeterminable. Undeterminable results name the missing parameters. The
join computes no detection probability. It never infers that a deposit is
absent, whatever the coverage status.

Standard library only. Records are plain JSON objects.
"""

from __future__ import annotations

from copy import deepcopy
from itertools import combinations, product
import math
from typing import Any

STATUSES = ("covered", "partly_covered", "not_covered", "undeterminable")
ARC_STEP_DEG = 1.0
REL_TOL = 1e-9

PARAMETER_LABELS = {
    "target.horizontal_frame": "Frame in which the target is drawn",
    "target.region.polygon": "Horizontal outline of the target zone",
    "target.origin.point": "Origin point of the measurement",
    "target.direction.sector_deg": "Direction sector",
    "target.distance_band_m": "Distance band from the origin",
    "target.direction.depth_band_m": "Depth band for a horizontal reading",
    "target.direction.radial_tolerance_m": "Tolerance around a single distance",
    "target.reference_surface.elevation_m": "Elevation of the ancient reference surface",
    "target.reference_surface.vertical_datum_id": "Vertical datum of the ancient reference surface",
    "target.reference_surface.phase_id": "Phase of the ancient reference surface",
    "target.measure": "Stated measure",
    "frame.metres_per_unit": "Scale of the target frame",
    "frame.north_vector": "North direction of the target frame",
    "footprint.horizontal_frame": "Frame of the excavated area",
    "footprint.cuts": "Recorded excavation cuts",
    "footprint.cut.polygon": "Outline of an excavated cut",
    "footprint.cut.top_level_m": "Top level of an excavated cut",
    "footprint.cut.bottom_level_m": "Lowest level reached in an excavated cut",
    "footprint.vertical_datum_id": "Vertical datum of the excavation levels",
    "frame_registration": "Registration between the target and footprint frames",
    "vertical_datum_join": "Measured join between the target and footprint vertical datums",
    # Carried components. They qualify interpretation, not spatial coverage.
    "target.ancient_accessibility": "Ancient accessibility of the target",
    "footprint.phase_reached_id": "Phase of the surface the excavation reached",
    "footprint.disturbance.target_zone_assessed": "Preservation assessed in the target zone",
    "footprint.recording.detection_limits": "Detection limits of the recording method",
}

TARGET_KEYS = ("id", "label", "horizontal_frame", "origin", "reference_surface", "region", "measure",
               "branch_dimensions", "phase", "ancient_accessibility")
FOOTPRINT_KEYS = ("id", "label", "horizontal_frame", "cuts", "vertical_datum_id", "phase_reached_id",
                  "disturbance", "recording", "documented_exclusions", "source_ids")
CUT_KEYS = ("id", "polygon", "top_level_m", "bottom_level_m")
MODELS = ("vertical_below_reference", "horizontal_from_origin")


class RecordError(ValueError):
    """A record is malformed. Unknown values must be explicit nulls."""


class FrameMismatchError(ValueError):
    """Target and footprint name different frames and no registration exists."""


class DatumMismatchError(FrameMismatchError):
    """Target and footprint levels use different vertical datums."""


# ---------------------------------------------------------------- geometry

def _finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _cross(o, a, b) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _signed_area(poly) -> float:
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                     for i in range(len(poly)))


def _area(poly) -> float:
    return abs(_signed_area(poly)) if len(poly) >= 3 else 0.0


def _segments_touch(p1, p2, q1, q2) -> bool:
    def on(a, b, c):
        return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
    d1, d2 = _cross(q1, q2, p1), _cross(q1, q2, p2)
    d3, d4 = _cross(p1, p2, q1), _cross(p1, p2, q2)
    if ((d1 > 0) != (d2 > 0)) and d1 != 0 and d2 != 0 and ((d3 > 0) != (d4 > 0)) and d3 != 0 and d4 != 0:
        return True
    return (d1 == 0 and on(q1, q2, p1)) or (d2 == 0 and on(q1, q2, p2)) or (d3 == 0 and on(p1, p2, q1)) or (d4 == 0 and on(p1, p2, q2))


def normalize_polygon(polygon: Any) -> list[tuple[float, float]]:
    """Validate a simple polygon and return it counter-clockwise, without collinear vertices."""
    if not isinstance(polygon, list) or len(polygon) < 3:
        raise RecordError("A polygon needs at least three vertices.")
    points = []
    for vertex in polygon:
        if not (isinstance(vertex, (list, tuple)) and len(vertex) == 2 and all(_finite(v) for v in vertex)):
            raise RecordError("Polygon vertices must be finite [x, y] pairs.")
        point = (float(vertex[0]), float(vertex[1]))
        if not points or point != points[-1]:
            points.append(point)
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    changed = True
    while changed and len(points) >= 3:
        changed = False
        for i in range(len(points)):
            if _cross(points[i - 1], points[i], points[(i + 1) % len(points)]) == 0:
                points.pop(i)
                changed = True
                break
    if len(points) < 3 or _area(points) == 0:
        raise RecordError("A polygon must enclose a positive area.")
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if _segments_touch(points[i], points[(i + 1) % n], points[j], points[(j + 1) % n]):
                raise RecordError("A polygon must be simple (no self-intersection).")
    if _signed_area(points) < 0:
        points.reverse()
    return points


def _in_triangle(p, a, b, c) -> bool:
    return _cross(a, b, p) >= 0 and _cross(b, c, p) >= 0 and _cross(c, a, p) >= 0


def convex_pieces(polygon: Any) -> list[list[tuple[float, float]]]:
    """Split a simple polygon into convex pieces (ear clipping when needed)."""
    points = normalize_polygon(polygon)
    if all(_cross(points[i - 1], points[i], points[(i + 1) % len(points)]) > 0 for i in range(len(points))):
        return [points]
    remaining, pieces = list(range(len(points))), []
    while len(remaining) > 3:
        for k in range(len(remaining)):
            i0, i1, i2 = remaining[k - 1], remaining[k], remaining[(k + 1) % len(remaining)]
            a, b, c = points[i0], points[i1], points[i2]
            if _cross(a, b, c) <= 0:
                continue
            if any(_in_triangle(points[j], a, b, c) for j in remaining if j not in (i0, i1, i2)):
                continue
            pieces.append([a, b, c])
            remaining.pop(k)
            break
        else:
            raise RecordError("The polygon could not be split into convex pieces.")
    pieces.append([points[i] for i in remaining])
    return pieces


def _clip(subject, clip):
    """Sutherland-Hodgman clip of a convex subject by a convex counter-clockwise polygon."""
    output = list(subject)
    for i in range(len(clip)):
        a, b = clip[i], clip[(i + 1) % len(clip)]
        source, output = output, []
        if not source:
            break
        start = source[-1]
        for end in source:
            end_in, start_in = _cross(a, b, end) >= 0, _cross(a, b, start) >= 0
            if end_in != start_in:
                d1, d2 = _cross(a, b, start), _cross(a, b, end)
                t = d1 / (d1 - d2)
                output.append((start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1])))
            if end_in:
                output.append(end)
            start = end
    return output


def _union_area_within(target_pieces, cut_piece_lists) -> float:
    """Area of target ∩ (union of cuts), by inclusion-exclusion over cuts."""
    total = 0.0
    for size in range(1, len(cut_piece_lists) + 1):
        sign = 1.0 if size % 2 else -1.0
        for chosen in combinations(cut_piece_lists, size):
            for piece in target_pieces:
                for clips in product(*chosen):
                    clipped = piece
                    for clip in clips:
                        clipped = _clip(clipped, clip)
                        if len(clipped) < 3:
                            break
                    total += sign * _area(clipped)
    return max(total, 0.0)


def annular_sector_pieces(origin, sector_deg, radial_band, north_vector, y_axis, *, outer: bool):
    """Convex pieces approximating an annular sector in frame units.

    Azimuths run clockwise from frame north. The outer approximation contains
    the true sector; the inner approximation lies inside it.
    """
    nx, ny = north_vector
    norm = math.hypot(nx, ny)
    nx, ny = nx / norm, ny / norm
    ex, ey = (-ny, nx) if y_axis == "down" else (ny, -nx)
    start, end = sector_deg
    width = (end - start) % 360.0 or 360.0
    steps = max(1, math.ceil(width / ARC_STEP_DEG))
    delta = width / steps
    r_min, r_max = radial_band
    widen = 1.0 / math.cos(math.radians(delta) / 2.0)
    r_in = r_min if outer else r_min * widen
    r_out = r_max * widen if outer else r_max
    if r_in >= r_out:
        return []

    def point(azimuth, radius):
        theta = math.radians(azimuth)
        return (origin[0] + radius * (math.cos(theta) * nx + math.sin(theta) * ex),
                origin[1] + radius * (math.cos(theta) * ny + math.sin(theta) * ey))

    pieces = []
    for k in range(steps):
        a0, a1 = start + k * delta, start + (k + 1) * delta
        quad = [point(a0, r_in), point(a0, r_out), point(a1, r_out), point(a1, r_in)]
        if r_in == 0:
            quad = [quad[0], quad[1], quad[2]]
        if _signed_area(quad) < 0:
            quad.reverse()
        pieces.append(quad)
    return pieces


def _measure(target_pieces, interval, cuts_geo):
    """Return (covered, total) target measure. A degenerate interval is one level."""
    low, high = interval
    area_target = sum(_area(piece) for piece in target_pieces)
    if high == low:
        slabs = [(low, high, 1.0)]
    else:
        levels = sorted({low, high} | {v for _, bottom, top in cuts_geo for v in (bottom, top) if low < v < high})
        slabs = [(a, b, b - a) for a, b in zip(levels, levels[1:])]
    covered = total = 0.0
    for a, b, weight in slabs:
        active = [pieces for pieces, bottom, top in cuts_geo if bottom <= a and top >= b]
        covered += weight * (_union_area_within(target_pieces, active) if active else 0.0)
        total += weight * area_target
    return covered, total


def _status(covered: float, total: float) -> str:
    if total <= 0:
        return "undeterminable"
    if covered >= total * (1 - REL_TOL):
        return "covered"
    if covered <= total * REL_TOL:
        return "not_covered"
    return "partly_covered"


# ------------------------------------------------------------- validation

def validate_target(target: dict[str, Any]) -> None:
    for key in TARGET_KEYS:
        if key not in target:
            raise RecordError(f"{target.get('id', 'target')}: '{key}' must be present (use null when unknown).")
    for key in ("elevation_m", "vertical_datum_id", "phase_id"):
        if key not in target["reference_surface"]:
            raise RecordError(f"{target['id']}: reference_surface.{key} must be present (use null when unknown).")
    if "point" not in target["origin"]:
        raise RecordError(f"{target['id']}: origin.point must be present (use null when unknown).")
    if not target["branch_dimensions"]:
        raise RecordError(f"{target['id']}: at least one branch dimension is required.")
    models = [option.get("model") for dim in target["branch_dimensions"] for option in dim["options"] if "model" in option]
    if not models or any(model not in MODELS for model in models):
        raise RecordError(f"{target['id']}: every direction-model option must name a known model.")


def validate_footprint(footprint: dict[str, Any]) -> None:
    for key in FOOTPRINT_KEYS:
        if key not in footprint:
            raise RecordError(f"{footprint.get('id', 'footprint')}: '{key}' must be present (use null when unknown).")
    for cut in footprint["cuts"]:
        for key in CUT_KEYS:
            if key not in cut:
                raise RecordError(f"{footprint['id']}: cut.{key} must be present (use null when unknown).")
        if cut["polygon"] is not None:
            normalize_polygon(cut["polygon"])
        for key in ("top_level_m", "bottom_level_m"):
            if cut[key] is not None and not _finite(cut[key]):
                raise RecordError(f"{footprint['id']}: cut.{key} must be a finite number or null.")
        if _finite(cut["top_level_m"]) and _finite(cut["bottom_level_m"]) and cut["bottom_level_m"] > cut["top_level_m"]:
            raise RecordError(f"{footprint['id']}: cut {cut['id']} bottom lies above its top.")
    for key in ("target_zone_assessed",):
        if key not in footprint["disturbance"]:
            raise RecordError(f"{footprint['id']}: disturbance.{key} must be present.")
    if "detection_limits" not in footprint["recording"]:
        raise RecordError(f"{footprint['id']}: recording.detection_limits must be present (use null when unknown).")


# ------------------------------------------------------- target branches

def _band(value: Any, name: str):
    if value is None:
        return None
    if not (isinstance(value, list) and len(value) == 2 and all(_finite(v) for v in value) and 0 <= value[0] <= value[1]):
        raise RecordError(f"{name} must be [low, high] with 0 <= low <= high, or null.")
    return [float(value[0]), float(value[1])]


def expand_target(target: dict[str, Any], frames: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Expand every combination of branch options into a target branch."""
    validate_target(target)
    branches = []
    dimensions = target["branch_dimensions"]
    for combo in product(*[dimension["options"] for dimension in dimensions]):
        params: dict[str, Any] = {}
        for option in combo:
            params.update({key: value for key, value in option.items() if key not in ("id", "label", "basis", "note")})
        options = {dimension["id"]: option["id"] for dimension, option in zip(dimensions, combo)}
        branch_id = target["id"] + "/" + "/".join(option["id"] for option in combo)
        branches.append(_build_branch(target, branch_id, options, params, frames))
    return branches


def _build_branch(target, branch_id, options, params, frames):
    missing: list[str] = []
    model = params.get("model")
    frame_id = target["horizontal_frame"]
    frame = None
    if frame_id is None:
        missing.append("target.horizontal_frame")
    elif frame_id not in frames:
        raise RecordError(f"{target['id']}: unknown frame {frame_id}.")
    else:
        frame = frames[frame_id]
    surface = target["reference_surface"]
    if surface["elevation_m"] is None:
        missing.append("target.reference_surface.elevation_m")
    elif not _finite(surface["elevation_m"]):
        raise RecordError(f"{target['id']}: reference_surface.elevation_m must be finite or null.")
    if surface["vertical_datum_id"] is None:
        missing.append("target.reference_surface.vertical_datum_id")
    if surface["phase_id"] is None:
        missing.append("target.reference_surface.phase_id")

    measure_band = None
    measure = target["measure"]
    if "metres_per_cubit" in params:
        if measure is None or not _finite(measure.get("count")):
            raise RecordError(f"{target['id']}: a cubit branch needs a stated measure count.")
        unit = _band(params["metres_per_cubit"], "metres_per_cubit")
        measure_band = [measure["count"] * unit[0], measure["count"] * unit[1]]

    outer = inner = None
    interval = None
    if model == "vertical_below_reference":
        region = target["region"] or {}
        polygon = region.get("polygon")
        if polygon is None:
            missing.append("target.region.polygon")
        elif frame is not None:
            outer = inner = convex_pieces(polygon)
        if measure_band is None:
            missing.append("target.measure")
        if _finite(surface["elevation_m"]) and measure_band is not None:
            interval = [surface["elevation_m"] - measure_band[1], surface["elevation_m"] - measure_band[0]]
    elif model == "horizontal_from_origin":
        origin = target["origin"]["point"]
        if origin is None:
            missing.append("target.origin.point")
        elif not (isinstance(origin, list) and len(origin) == 2 and all(_finite(v) for v in origin)):
            raise RecordError(f"{target['id']}: origin.point must be a finite [x, y] pair or null.")
        sector = params.get("sector_deg")
        if sector is None:
            missing.append("target.direction.sector_deg")
        elif not (isinstance(sector, list) and len(sector) == 2 and all(_finite(v) for v in sector)):
            raise RecordError(f"{target['id']}: sector_deg must be [from, to] clockwise from north, or null.")
        radial = _band(params.get("distance_band_m"), "distance_band_m") if params.get("distance_band_m") is not None else measure_band
        if radial is None:
            missing.append("target.distance_band_m")
        elif radial[0] == radial[1]:
            tolerance = params.get("radial_tolerance_m")
            if tolerance is None:
                missing.append("target.direction.radial_tolerance_m")
                radial = None
            elif not _finite(tolerance) or tolerance <= 0:
                raise RecordError(f"{target['id']}: radial_tolerance_m must be positive or null.")
            else:
                radial = [max(0.0, radial[0] - tolerance), radial[1] + tolerance]
        depth = _band(params.get("depth_band_m"), "depth_band_m")
        if depth is None:
            missing.append("target.direction.depth_band_m")
        elif _finite(surface["elevation_m"]):
            interval = [surface["elevation_m"] - depth[1], surface["elevation_m"] - depth[0]]
        frame_ready = frame is not None
        if frame is not None:
            if not _finite(frame.get("metres_per_unit")) or frame["metres_per_unit"] <= 0:
                missing.append("frame.metres_per_unit")
                frame_ready = False
            if frame.get("north_vector") is None or frame.get("y_axis") not in ("up", "down"):
                missing.append("frame.north_vector")
                frame_ready = False
        # The horizontal outline needs only origin, sector, distance and frame;
        # unknown levels still leave a usable outline for disjointness checks.
        if frame_ready and origin is not None and sector is not None and radial is not None:
            scale = frame["metres_per_unit"]
            band_units = [radial[0] / scale, radial[1] / scale]
            outer = annular_sector_pieces(origin, sector, band_units, frame["north_vector"], frame["y_axis"], outer=True)
            inner = annular_sector_pieces(origin, sector, band_units, frame["north_vector"], frame["y_axis"], outer=False)
            if not outer or not inner:
                raise RecordError(f"{target['id']}: the distance band encloses no usable area.")
    else:
        raise RecordError(f"{target['id']}: unknown model {model}.")

    return {
        "id": branch_id, "target_id": target["id"], "options": options, "model": model,
        "horizontal_frame": frame_id, "vertical_datum_id": surface["vertical_datum_id"],
        "reference_surface_phase_id": surface["phase_id"],
        "measure_band_m": measure_band, "interval_m": interval,
        "region_constructed": outer is not None,
        "missing_parameters": sorted(set(missing)),
        "_outer": outer, "_inner": inner,
    }


# ------------------------------------------------------------------- join

def _vertical_known(branch, footprint, cut):
    return (branch["interval_m"] is not None and branch["vertical_datum_id"] is not None
            and footprint["vertical_datum_id"] is not None
            and _finite(cut["top_level_m"]) and _finite(cut["bottom_level_m"]))


def _vertical_disjoint(interval, cut) -> bool:
    low, high = interval
    if low == high:
        return low < cut["bottom_level_m"] or low > cut["top_level_m"]
    return cut["bottom_level_m"] >= high or cut["top_level_m"] <= low


def join(branch: dict[str, Any], footprint: dict[str, Any]) -> dict[str, Any]:
    """Join one target branch to one footprint.

    Raises FrameMismatchError when both name different horizontal frames, and
    DatumMismatchError when both name different vertical datums. The join never
    compares coordinates across frames; transform the footprint first.
    """
    validate_footprint(footprint)
    target_frame, footprint_frame = branch["horizontal_frame"], footprint["horizontal_frame"]
    if target_frame is not None and footprint_frame is not None and target_frame != footprint_frame:
        raise FrameMismatchError(f"Target frame {target_frame} differs from footprint frame {footprint_frame}; no registration is recorded.")
    target_datum, footprint_datum = branch["vertical_datum_id"], footprint["vertical_datum_id"]
    if target_datum is not None and footprint_datum is not None and target_datum != footprint_datum:
        raise DatumMismatchError(f"Target datum {target_datum} differs from footprint datum {footprint_datum}; no measured datum join is recorded.")

    missing = list(branch["missing_parameters"])
    if footprint_frame is None:
        missing.append("footprint.horizontal_frame")
    if footprint_datum is None:
        missing.append("footprint.vertical_datum_id")
    cuts = footprint["cuts"]
    if not cuts:
        missing.append("footprint.cuts")
    for cut in cuts:
        if cut["polygon"] is None:
            missing.append("footprint.cut.polygon")
        if cut["top_level_m"] is None:
            missing.append("footprint.cut.top_level_m")
        if cut["bottom_level_m"] is None:
            missing.append("footprint.cut.bottom_level_m")
    missing = sorted(set(missing))

    same_frame = target_frame is not None and target_frame == footprint_frame
    reasons, disjoint_flags, intersect_known = [], [], False
    for cut in cuts:
        horizontal_known = same_frame and branch["_outer"] is not None and cut["polygon"] is not None
        vertical_known = _vertical_known(branch, footprint, cut)
        h_disjoint = horizontal_known and _union_area_within(branch["_outer"], [convex_pieces(cut["polygon"])]) == 0.0
        v_disjoint = vertical_known and _vertical_disjoint(branch["interval_m"], cut)
        disjoint_flags.append(h_disjoint or v_disjoint)
        if h_disjoint:
            reasons.append(f"Cut {cut['id']} lies outside the target outline.")
        if v_disjoint:
            reasons.append(f"Cut {cut['id']} does not reach the target levels.")
        if horizontal_known and vertical_known and not h_disjoint and not v_disjoint:
            if _union_area_within(branch["_inner"], [convex_pieces(cut["polygon"])]) > 0:
                intersect_known = True

    if cuts and all(disjoint_flags):
        status, possible = "not_covered", ["not_covered"]
    elif missing:
        status = "undeterminable"
        possible = ["covered", "partly_covered"] if intersect_known else ["covered", "partly_covered", "not_covered"]
        reasons.append("Coverage cannot be computed while the listed parameters are missing.")
    else:
        cuts_geo = [(convex_pieces(cut["polygon"]), cut["bottom_level_m"], cut["top_level_m"]) for cut in cuts]
        outer_status = _status(*_measure(branch["_outer"], branch["interval_m"], cuts_geo))
        inner_status = _status(*_measure(branch["_inner"], branch["interval_m"], cuts_geo))
        if outer_status in ("covered", "not_covered"):
            status = outer_status
        elif inner_status == "partly_covered":
            status = "partly_covered"
        else:
            status = "undeterminable"
            reasons.append("The result lies within the arc approximation margin; refine ARC_STEP_DEG.")
        possible = [status] if status != "undeterminable" else ["covered", "partly_covered", "not_covered"]
    return {
        "id": branch["id"] + "@" + footprint["id"],
        "branch_id": branch["id"], "target_id": branch["target_id"], "footprint_id": footprint["id"],
        "options": deepcopy(branch["options"]), "model": branch["model"],
        "status": status, "possible_statuses": possible,
        "missing_parameters": missing if status == "undeterminable" else [],
        "open_parameters": missing,
        "frame_check": {
            "horizontal": "same" if same_frame else "unknown",
            "vertical_datum": "same" if target_datum is not None and target_datum == footprint_datum else "unknown",
        },
        "reasons": reasons,
    }


def _components(target, branch, footprint, result):
    # Open parameters are listed even when a disjoint cut settles "not covered".
    target_missing = [item for item in result["open_parameters"] if item.startswith(("target.", "frame."))]
    footprint_missing = [item for item in result["open_parameters"]
                         if item.startswith("footprint.") or item in ("frame_registration", "vertical_datum_join")]
    accessibility = target["ancient_accessibility"]
    disturbance = footprint["disturbance"]
    recording = footprint["recording"]
    target_phase, reached_phase = branch["reference_surface_phase_id"], footprint["phase_reached_id"]
    carried = []
    if accessibility.get("status") != "established":
        carried.append("target.ancient_accessibility")
    if reached_phase is None:
        carried.append("footprint.phase_reached_id")
    if disturbance["target_zone_assessed"] is not True:
        carried.append("footprint.disturbance.target_zone_assessed")
    if recording["detection_limits"] is None:
        carried.append("footprint.recording.detection_limits")
    return {
        "target_position": {"status": "determined" if not target_missing else "undetermined", "missing_count": len(target_missing)},
        "excavation_reach": {"status": "determined" if not footprint_missing else "undetermined", "missing_count": len(footprint_missing),
                             "cuts": len(footprint["cuts"]), "coverage_status": result["status"]},
        "ancient_accessibility": {"status": accessibility.get("status", "unknown")},
        "preservation": {"status": "assessed" if disturbance["target_zone_assessed"] is True else "unknown"},
        "recording_capability": {"status": "documented" if recording["detection_limits"] is not None else "unknown"},
        "phase": {"target_reference_surface_phase_id": target_phase, "footprint_phase_reached_id": reached_phase,
                  "status": "unknown" if target_phase is None or reached_phase is None else ("same" if target_phase == reached_phase else "different")},
    }, carried


INTERPRETATION = {
    "undeterminable": "Coverage of this branch cannot be determined. An unsuccessful excavation here says nothing about the deposit.",
    "not_covered": "The excavation did not reach this branch. Its results cannot bear on a deposit in this branch.",
    "partly_covered": "The excavation reached only part of this branch. The rest remains untested.",
    "covered": "The excavation reached the whole branch volume. No absence is inferred: accessibility, preservation, phase and recording must still be established, and the negative-excavation gates still apply.",
}


def evaluate_pair(target: dict[str, Any], branch: dict[str, Any], footprint: dict[str, Any]) -> dict[str, Any]:
    """Join with frame/datum rejection recorded instead of raised, plus carried components."""
    try:
        result = join(branch, footprint)
    except FrameMismatchError as error:
        datum_error = isinstance(error, DatumMismatchError)
        result = {
            "id": branch["id"] + "@" + footprint["id"], "branch_id": branch["id"], "target_id": branch["target_id"],
            "footprint_id": footprint["id"], "options": deepcopy(branch["options"]), "model": branch["model"],
            "status": "undeterminable", "possible_statuses": ["covered", "partly_covered", "not_covered"],
            "missing_parameters": ["vertical_datum_join" if datum_error else "frame_registration"],
            "open_parameters": ["vertical_datum_join" if datum_error else "frame_registration"],
            "frame_check": {"horizontal": "same" if datum_error else "rejected_mismatch",
                            "vertical_datum": "rejected_mismatch" if datum_error else "not_evaluated"},
            "reasons": [str(error) + " The join was refused."],
        }
    components, carried = _components(target, branch, footprint, result)
    result["components"] = components
    result["carried_unknowns"] = carried
    result["interpretation"] = INTERPRETATION[result["status"]]
    result["deposit_absence_inferred"] = False
    return result


def resolve_parameters(parameters: list[str], scope_ids: set[str], field_records: list[dict[str, Any]],
                       declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Map each open parameter to field records or required model declarations."""
    resolution = []
    for parameter in sorted(set(parameters)):
        records = [record for record in field_records
                   if parameter in record["resolves"] and scope_ids & set(record["applies_to"])]
        declaration = next((item for item in declarations
                            if item["parameter"] == parameter and scope_ids & set(item["applies_to"])), None)
        resolution.append({
            "parameter": parameter, "label": PARAMETER_LABELS.get(parameter, parameter),
            "field_record_ids": [record["id"] for record in records],
            "field_records_apply_to": sorted({item for record in records for item in record["applies_to"] if item in scope_ids}),
            "requirement_kind": declaration["requirement_kind"] if declaration else None,
            "requirement": declaration["requirement"] if declaration else None,
            "requirement_applies_to": sorted(set(declaration["applies_to"]) & scope_ids) if declaration else [],
            "mapped": bool(records) or declaration is not None,
        })
    return resolution


def evaluate_case(case: dict[str, Any], targets: dict[str, dict[str, Any]], footprints: dict[str, dict[str, Any]],
                  frames: dict[str, dict[str, Any]], field_records: list[dict[str, Any]],
                  declarations: list[dict[str, Any]]) -> dict[str, Any]:
    target = targets[case["target_id"]]
    branches = expand_target(target, frames)
    case_footprints = [footprints[footprint_id] for footprint_id in case["footprint_ids"]]
    joins = [evaluate_pair(target, branch, footprint) for branch in branches for footprint in case_footprints]
    status_counts = {status: sum(item["status"] == status for item in joins) for status in STATUSES}
    spatial, carried = {}, {}
    for item in joins:
        for parameter in item["missing_parameters"]:
            spatial.setdefault(parameter, []).append(item["id"])
        for parameter in item["carried_unknowns"]:
            carried.setdefault(parameter, []).append(item["id"])
    scope = {target["id"], *case["footprint_ids"]}
    resolution = resolve_parameters(list(spatial) + list(carried), scope, field_records, declarations)
    for row in resolution:
        row["kind"] = "spatial" if row["parameter"] in spatial else "carried"
        row["join_count"] = len(spatial.get(row["parameter"], carried.get(row["parameter"], [])))
    public_branches = [{key: value for key, value in branch.items() if not key.startswith("_") and key != "missing_parameters"}
                       for branch in branches]
    return {
        "id": case["id"], "label": case["label"], "target_id": target["id"], "footprint_ids": list(case["footprint_ids"]),
        "branches": public_branches, "joins": joins,
        "summary": {"branches": len(branches), "joins": len(joins), "status_counts": status_counts,
                    "deposit_absence_inferred": False},
        "resolution": resolution,
    }
