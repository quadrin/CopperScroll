"""Register an incoming photograph or plan with a withheld check point.

Standard library only. The affine fit is the shared tools' least-squares fit
(research/shared_tools/benchmarks.py); this file adds a similarity fit, the
acceptance thresholds of registration_protocol.md and the verdict rules.

    python3 -I research/assessments/kohlit_chain/registration.py RECORD.json

A record names its document, the transform and target relations chosen before
fitting, three or more controls, and one check point declared before fitting.
Coordinates: target frame in metres (east, north). Source points in a
right-handed frame, or raster pixels with "source_axes": "pixel_y_down".
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SHARED = REPO / "research" / "shared_tools"

# Acceptance: the registration error must be at most a quarter of the target
# relation's size, so that a 2E margin still leaves half of the relation.
K_MARGIN = 2.0
RELATIONS = {
    "mouth_10m": {"size_m": 10.0, "max_error_m": 2.5,
                  "basis": "Entry 60 tombs at the mouth: 10 m, pre-registration §4 (C3 text level)"},
    "north_sector": {"size_m": None, "max_error_m": 10.0,
                     "basis": "Entry 60 pit north: 315°–45° within 1 km (C2); the bearing margin rule decides each feature"},
    "east_west_order": {"size_m": None, "max_error_m": None,
                        "basis": "Entry 19 eastern pit: E_pair at most a quarter of the east–west separation"},
}
MIN_CONTROLS = {"similarity": 3, "affine": 4}
REFERENCE_POINTS = HERE / "reference_points.json"
CONTROL_ROLES = {"control", "check", "tie"}
CHECK_ROLES = {"check", "control"}


def load_reference_points(path: Path = REFERENCE_POINTS) -> dict:
    return {c["id"]: c for c in json.loads(Path(path).read_text(encoding="utf-8"))["candidates"]}


def role_problems(record: dict, candidates: dict) -> list[str]:
    """Controls and the check point must be listed candidates with a fitting role."""
    out = []
    for c in record["controls"]:
        cand = candidates.get(c["rp"])
        if cand is None:
            out.append(f"control {c['rp']} is not in reference_points.json (add it before fitting)")
        elif not CONTROL_ROLES & set(cand["roles"]):
            out.append(f"control {c['rp']} has role {cand['roles']} and cannot enter the fit")
        elif "tie" in cand["roles"] and "control" not in cand["roles"] and not record.get("historical_tie"):
            out.append(f"control {c['rp']} is a tie point: use it only between two historical documents")
    cand = candidates.get(record["check"]["rp"])
    if cand is None:
        out.append(f"check point {record['check']['rp']} is not in reference_points.json")
    elif not CHECK_ROLES & set(cand["roles"]):
        out.append(f"check point {record['check']['rp']} has role {cand['roles']}")
    return out


def _shared_affine():
    """Import the shared tools' affine fit without changing that module."""
    sys.path.insert(0, str(SHARED))
    try:
        spec = importlib.util.spec_from_file_location("kc_shared_benchmarks", SHARED / "benchmarks.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(SHARED))
    return module.fit_affine, module.transform


FIT_AFFINE, TRANSFORM_AFFINE = _shared_affine()


def _finite_pairs(points):
    for p in points:
        if len(p) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in p):
            raise ValueError("Points must be finite coordinate pairs")


def fit_similarity(source, destination):
    """Least-squares 2D similarity (scale, rotation, shift; no reflection)."""
    if len(source) != len(destination) or len(source) < 2:
        raise ValueError("At least two paired controls required")
    _finite_pairs(source + destination)
    n = len(source)
    sx = sum(p[0] for p in source) / n
    sy = sum(p[1] for p in source) / n
    dx = sum(p[0] for p in destination) / n
    dy = sum(p[1] for p in destination) / n
    num_a = num_b = den = 0.0
    for (x, y), (u, v) in zip(source, destination):
        x, y, u, v = x - sx, y - sy, u - dx, v - dy
        num_a += x * u + y * v
        num_b += x * v - y * u
        den += x * x + y * y
    if den < 1e-12:
        raise ValueError("Degenerate control geometry")
    a, b = num_a / den, num_b / den
    return {"a": a, "b": b, "tx": dx - (a * sx - b * sy), "ty": dy - (b * sx + a * sy),
            "scale": math.hypot(a, b), "rotation_deg": math.degrees(math.atan2(b, a))}


def apply_similarity(p, point):
    x, y = point
    return [p["a"] * x - p["b"] * y + p["tx"], p["b"] * x + p["a"] * y + p["ty"]]


def _collinear(points, tol=1e-9):
    if len(points) < 3:
        return True
    (x0, y0) = points[0]
    span = max(math.dist(points[0], q) for q in points) or 1.0
    for i in range(1, len(points)):
        for j in range(i + 1, len(points)):
            (x1, y1), (x2, y2) = points[i], points[j]
            if abs((x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)) > tol * span * span:
                return False
    return True


def _inside_hull(points, q):
    """True if q lies inside or on the convex hull of points (monotone chain)."""
    pts = sorted(set(map(tuple, points)))
    if len(pts) < 3:
        return False

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    return all(cross(hull[i], hull[(i + 1) % len(hull)], q) >= -1e-9 for i in range(len(hull)))


def register(record: dict, candidates: dict | None = None) -> dict:
    """Fit on controls only; measure residuals and the withheld check error.

    Blocking problems give status 'invalid' and no acceptance. Warnings keep
    the measured error but are reported with it.
    """
    transform = record.get("transform")
    if transform not in MIN_CONTROLS:
        raise ValueError("transform must be 'similarity' or 'affine'")
    flip = record.get("source_axes") == "pixel_y_down"

    def src(p):
        return [p[0], -p[1]] if flip else list(p)
    controls, check = record["controls"], record["check"]
    blocking, warnings = [], []
    if not record.get("declared_before_fit"):
        blocking.append("check point, transform and target relations were not declared before fitting")
    if not record.get("target_relations"):
        blocking.append("no target relation declared")
    unknown = [r for r in record.get("target_relations", []) if r not in RELATIONS]
    if unknown:
        blocking.append(f"unknown target relation(s): {unknown}")
    if check["rp"] in {c["rp"] for c in controls}:
        blocking.append("the check point is also a control")
    if candidates is not None:
        blocking.extend(role_problems(record, candidates))
    if len(controls) < MIN_CONTROLS[transform]:
        blocking.append(f"{transform} needs at least {MIN_CONTROLS[transform]} controls plus one check point")
    source = [src(c["source_xy"]) for c in controls]
    dest = [list(c["target_xy"]) for c in controls]
    _finite_pairs(source + dest + [src(check["source_xy"]), list(check["target_xy"])])
    if _collinear(dest):
        blocking.append("controls are collinear")
    out = {"document": record.get("document", {}).get("id"), "transform": transform}
    if any("needs at least" in b or "collinear" in b for b in blocking):
        out.update({"status": "invalid", "blocking": blocking, "warnings": warnings, "accepted_for": []})
        return out
    if transform == "similarity":
        params = fit_similarity(source, dest)
        fwd = lambda q: apply_similarity(params, q)  # noqa: E731
        out["parameters"] = {k: params[k] for k in ("scale", "rotation_deg", "tx", "ty")}
    else:
        matrix = FIT_AFFINE(source, dest)
        fwd = lambda q: TRANSFORM_AFFINE(matrix, q)  # noqa: E731
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        out["parameters"] = {"matrix": matrix, "determinant": det}
        if det < 0:
            warnings.append("affine fit reflects the source: check for a mirrored print or the pixel axis convention")
    residuals = [{"rp": c["rp"], "residual_m": math.dist(fwd(s), d)} for c, s, d in zip(controls, source, dest)]
    rms = math.sqrt(sum(r["residual_m"] ** 2 for r in residuals) / len(residuals))
    predicted = fwd(src(check["source_xy"]))
    check_error = math.dist(predicted, check["target_xy"])
    reference_error = float(record.get("target_frame", {}).get("reference_error_m", 0.0))
    e_fit = max(check_error, rms)
    e_total = math.hypot(e_fit, reference_error)
    if not _inside_hull(dest, check["target_xy"]):
        warnings.append("check point lies outside the control hull: its error understates extrapolation")
    accepted = [] if blocking else [
        name for name in record.get("target_relations", [])
        if name in RELATIONS and RELATIONS[name]["max_error_m"] is not None and e_total <= RELATIONS[name]["max_error_m"]]
    status = "invalid" if blocking else ("accepted" if accepted and not warnings else
                                         "accepted_with_warnings" if accepted else "rejected")
    out.update({"status": status, "blocking": blocking, "warnings": warnings, "residuals": residuals,
                "rms_residual_m": rms, "check_rp": check["rp"], "check_predicted": predicted,
                "check_error_m": check_error, "reference_error_m": reference_error,
                "E_fit_m": e_fit, "E_total_m": e_total, "accepted_for": accepted})
    return out


def pair_error(e1: float, e2: float, same_document: bool = False, pick_error_m: float = 0.0) -> float:
    """Error of a distance between two mapped features.

    Two features drawn in one registered document share its transform, so the
    pair error is their picking error, not the registration error.
    """
    if same_document:
        return math.hypot(pick_error_m, pick_error_m)
    return math.hypot(e1, e2)


def classify_distance(d: float, threshold: float, e_pair: float, k: float = K_MARGIN) -> str:
    if d + k * e_pair <= threshold:
        return "inside"
    if d - k * e_pair > threshold:
        return "outside"
    return "indeterminate"


def bearing(anchor, point) -> float:
    return math.degrees(math.atan2(point[0] - anchor[0], point[1] - anchor[1])) % 360.0


def classify_sector(anchor, point, e_point: float, e_anchor: float, sector=(315.0, 45.0),
                    limit_m: float = 1000.0, k: float = K_MARGIN) -> dict:
    """Is the point in the sector from the anchor, given both position errors?"""
    d = math.dist(anchor, point)
    b = bearing(anchor, point)
    e = math.hypot(e_point, e_anchor)
    lo, hi = sector
    inside = lo <= b <= hi if lo <= hi else (b >= lo or b <= hi)
    margin = min(abs((b - lo + 180) % 360 - 180), abs((b - hi + 180) % 360 - 180))
    need = math.degrees(math.atan2(k * e, d)) if d > 0 else 180.0
    if d - k * e > limit_m:
        verdict = "outside"
    elif margin < need or d + k * e > limit_m:
        verdict = "indeterminate"
    else:
        verdict = "inside" if inside else "outside"
    return {"distance_m": d, "bearing_deg": b, "edge_margin_deg": margin, "needed_margin_deg": need, "verdict": verdict}


def classify_order(east_a: float, east_b: float, e_pair: float, k: float = K_MARGIN) -> str:
    """Which of two openings is the eastern one (Entry 19)?"""
    sep = east_a - east_b
    if abs(sep) <= k * e_pair:
        return "indeterminate"
    return "a_east" if sep > 0 else "b_east"


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print(__doc__)
        return 2
    record = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    print(json.dumps(register(record, load_reference_points()), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
