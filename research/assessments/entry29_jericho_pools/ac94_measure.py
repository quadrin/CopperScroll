"""Explore finite Plan13 traces. Outputs are source-plan sensitivity, not a survey."""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def length(a):
    return math.hypot(*a)


def at(a, b, t):
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def point_distance(q, a, b):
    v = sub(b, a)
    t = max(0.0, min(1.0, dot(sub(q, a), v) / dot(v, v)))
    return length(sub(q, at(a, b, t)))


def finite_distance_range(p, q, a, b):
    """Exact range over target segment p–q; distance to a convex set is convex."""
    v, w = sub(q, p), sub(b, a)
    denom = cross(v, w)
    if abs(denom) > 1e-12:
        t = cross(sub(a, p), w) / denom
        u = cross(sub(a, p), v) / denom
        intersects = 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0
    else:
        intersects = False
    distances = [point_distance(p, a, b), point_distance(q, a, b),
                 point_distance(a, p, q) if p != q else length(sub(a, p)),
                 point_distance(b, p, q) if p != q else length(sub(b, p))]
    minimum = 0.0 if intersects else min(distances)
    maximum = max(point_distance(p, a, b), point_distance(q, a, b))
    return (minimum, maximum)


def perpendicular_range(p, q, a, b):
    """Clip the complete target parameter interval by finite-foot eligibility."""
    v = sub(b, a)
    size = length(v)
    projections = [dot(sub(x, a), v) / size for x in (p, q)]
    t0, t1 = (projections[0] / size, projections[1] / size)
    if abs(t1 - t0) < 1e-12:
        permitted = (0.0, 1.0) if 0.0 <= t0 <= 1.0 else None
    else:
        bounds = sorted((-t0 / (t1 - t0), (1.0 - t0) / (t1 - t0)))
        lo, hi = max(0.0, bounds[0]), min(1.0, bounds[1])
        permitted = (lo, hi) if lo <= hi else None
    signed = [cross(v, sub(x, a)) / size for x in (p, q)]
    if permitted is None:
        return {"permitted_target_parameter": None, "range_px": None,
                "signed_projection_from_north_endpoint_px": projections,
                "status": "no nominal target projects onto the finite trace"}
    ds = [signed[0] + s * (signed[1] - signed[0]) for s in permitted]
    minimum = 0.0 if min(ds) <= 0.0 <= max(ds) else min(map(abs, ds))
    return {"permitted_target_parameter": permitted,
            "range_px": (minimum, max(map(abs, ds))),
            "signed_projection_from_north_endpoint_px": projections,
            "status": "nominal finite projection available"}


def round_tree(value):
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, dict):
        return {k: round_tree(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [round_tree(v) for v in value]
    return value


def recompute(inputs):
    scale = inputs["coordinates"]["scale"]
    bar = length(sub(*scale["endpoints_px"]))
    mpp = scale["metres"] / bar
    terminal, upstream = inputs["pipe"]["endpoints_px"]
    rows = []
    for target_id in inputs["target_sets"]:
        target_end = terminal if target_id == "drawn_terminus_only" else upstream
        for wall in inputs["wall_traces"]:
            a, b = wall["endpoints_px"]
            distance = finite_distance_range(terminal, target_end, a, b)
            perp = perpendicular_range(terminal, target_end, a, b)
            envelopes = []
            for envelope in inputs["uncertainty_envelopes"]:
                # A target endpoint and wall endpoint can each move by e.
                # Their segment sets move at most e in Hausdorff distance;
                # shortest-distance extrema therefore change by at most 2e.
                e = envelope["point_disk_radius_px"]
                se = envelope["scale_endpoint_disk_radius_px"]
                lower = max(0.0, distance[0] - 2.0 * e) * scale["metres"] / (bar + 2.0 * se)
                upper = (distance[1] + 2.0 * e) * scale["metres"] / (bar - 2.0 * se)
                for n in inputs["reading_models"]["numerals_cubits"]:
                    units = inputs["reading_models"]["cubit_range_m"]
                    band = (n * units[0], n * units[1])
                    overlap = lower <= band[1] and upper >= band[0]
                    nominal_overlap = distance[0] * mpp <= band[1] and distance[1] * mpp >= band[0]
                    permitted_units = (max(units[0], distance[0] * mpp / n),
                                       min(units[1], distance[1] * mpp / n)) if nominal_overlap else None
                    envelopes.append({
                        "envelope": envelope["id"], "numeral_cubits": n,
                        "cubit_band_m": band, "shortest_distance_outer_envelope_m": (lower, upper),
                        "shortest_distance_nominal_overlap": nominal_overlap,
                        "shortest_distance_nominal_attainable_cubit_m": permitted_units,
                        "shortest_distance_band_status": "possible overlap of conservative bounds" if overlap else "disjoint",
                        "perpendicular_band_status": (
                            "disjoint even if a perturbed finite projection becomes eligible" if not overlap
                            else "no nominal eligible projection; perturbed eligibility/fit not established"
                            if perp["range_px"] is None else "requires separate constrained uncertainty analysis"),
                        "archaeological_status": "unknown: aperture/face/surface/phase gates unresolved"
                    })
            rows.append({"target_set": target_id, "wall_trace": wall["id"],
                         "shortest_distance_nominal_range_m": [x * mpp for x in distance],
                         "perpendicular_nominal": perp, "branches": envelopes,
                         "conduit_chainage_status": "unknown: no justified connection to either long side",
                         "other_axes_status": "unknown: ancient origin and surface unspecified"})
    return round_tree({
        "scope": inputs["claim"], "source_sha256": inputs["source"]["sha256"],
        "scale_bar_pixels": bar, "metres_per_pixel": mpp,
        "drawn_pipe_length_m": length(sub(terminal, upstream)) * mpp,
        "reported_pipe_length_m": inputs["pipe"]["reported_preserved_length_m"],
        "dimension_diagnostic": {
            "north_inner_span_m": length(sub(*inputs["dimension_diagnostic"]["north_inner_span_px"])) * mpp,
            "east_inner_trace_m": length(sub(*next(w["endpoints_px"] for w in inputs["wall_traces"] if w["id"] == "east_inner"))) * mpp,
            "east_outer_trace_m": length(sub(*next(w["endpoints_px"] for w in inputs["wall_traces"] if w["id"] == "east_outer"))) * mpp,
            "reported_pool_dimensions_m": inputs["dimension_diagnostic"]["reported_pool_dimensions_m"],
            "total_archaeological_error_bound_m": None,
            "rule": inputs["dimension_diagnostic"]["rule"]
        },
        "target_parameter": "0 = drawn terminus; 1 = target-set end",
        "method": "Exact continuous target-segment extrema; no point sampling or wall extension. Conservative picking envelopes are bounds, not proof that every distance is attainable.",
        "rows": rows, "controls": inputs["controls"],
        "missing_control_data_is_failure": False,
        "regional_denominator": None, "unused_prediction": None,
        "decision": "not identifiable from available evidence",
        "formal_outcome_increment": 0
    })


def tracing(inputs):
    """Project vector tracing in the original full-page pixel coordinate space."""
    walls = inputs["wall_traces"]
    p, q = inputs["pipe"]["endpoints_px"]
    a, b = next(w["endpoints_px"] for w in walls if w["id"] == "east_inner")
    v = sub(b, a)
    foot = at(a, b, dot(sub(p, a), v) / dot(v, v))
    lines = []
    for w in walls:
        start, end = w["endpoints_px"]
        dash = ' stroke-dasharray="4 3"' if w["face_model"] == "outer" else ""
        lines.append(f'<line x1="{start[0]}" y1="{start[1]}" x2="{end[0]}" y2="{end[1]}" stroke="#394d63" stroke-width="2"{dash}/>' )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="390 800 415 580" width="620" height="865" role="img" aria-labelledby="title desc">
<title id="title">A(C)94 finite-wall sensitivity tracing</title>
<desc id="desc">Original project tracing of selected Netzer2001 Plan13 contours. The pipe's perpendicular foot falls north of the finite east inner trace. Dashed contours are uncertified outer-face hypotheses. No survey or deposit coordinate.</desc>
<rect x="390" y="800" width="415" height="580" fill="#ffffff"/>
<g font-family="sans-serif" fill="#263545">
<text x="410" y="826" font-size="14">A(C)94: pipe and finite wall traces</text>
<text x="410" y="848" font-size="10">Project tracing · Netzer2001 p52 / Plan13</text>
{''.join(lines)}
<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="#187965" stroke-width="4"/>
<circle cx="{p[0]}" cy="{p[1]}" r="4" fill="#187965"/>
<line x1="{p[0]}" y1="{p[1]}" x2="{foot[0]}" y2="{foot[1]}" stroke="#b55032" stroke-width="1.5" stroke-dasharray="3 3"/>
<circle cx="{foot[0]}" cy="{foot[1]}" r="4" fill="#b55032"/>
<text x="474" y="882" font-size="11">3.3m approach</text>
<text x="509" y="936" font-size="10">drawn terminus</text>
<text x="624" y="950" font-size="10" fill="#b55032">foot beyond wall end</text>
<text x="503" y="1077" font-size="12">A(C)94</text>
<text x="412" y="1050" font-size="10">west stub</text>
<text x="704" y="1110" font-size="10">east side</text>
<text x="410" y="1269" font-size="10">Solid: inner-outline model</text>
<text x="410" y="1287" font-size="10">Dashed: uncertified outer-outline model</text>
<line x1="410" y1="1315" x2="545" y2="1315" stroke="#263545" stroke-width="2"/>
<text x="410" y="1331" font-size="10">0</text><text x="529" y="1331" font-size="10">5m</text>
<text x="410" y="1354" font-size="9">Source-plan scale only; no geographic CRS or ancient elevation.</text>
</g></svg>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify saved outputs and source hash without rewriting")
    args = parser.parse_args()
    inputs = json.loads((ROOT / "ac94_inputs.json").read_text())
    source = ROOT / inputs["source"]["asset"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == inputs["source"]["sha256"]
    outputs = {"ac94_results.json": json.dumps(recompute(inputs), ensure_ascii=False, indent=2) + "\n",
               "ac94_tracing.svg": tracing(inputs)}
    for name, expected in outputs.items():
        path = ROOT / name
        if args.check:
            assert path.read_text() == expected, f"stale output: {name}"
        else:
            path.write_text(expected)
    data = json.loads(outputs["ac94_results.json"])
    print(f"Plan13: {data['scale_bar_pixels']}px =5m; drawn pipe {data['drawn_pipe_length_m']:.2f}m")
    for row in data["rows"]:
        print(row["target_set"], row["wall_trace"], row["shortest_distance_nominal_range_m"],
              row["perpendicular_nominal"]["status"])
    print("Controls J05/J09 unknown; entry29/A(C)94 not identifiable; no outcome increment.")


if __name__ == "__main__":
    main()
