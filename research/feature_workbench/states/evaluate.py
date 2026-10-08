"""Evaluate feature-state claims without promoting source plans to world geometry."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Any


MODULE_DIR = Path(__file__).resolve().parent
REPO_ROOT = MODULE_DIR.parents[2]


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_register(register: dict[str, Any]) -> None:
    """Fail closed on geometry, provenance and inconsistent phase sequences."""
    source_ids = {s["id"] for s in register["sources"]}
    frames = {f["id"]: f for f in register["reference_frames"]}
    states = {s["id"]: s for s in register["states"]}
    if len(states) != len(register["states"]):
        raise ValueError("State IDs must be unique")
    for frame in frames.values():
        if frame["kind"] not in {"source_raster", "local_excavation", "descriptive"}:
            raise ValueError("Only native local or descriptive frames are reviewed")
        if frame.get("geographic_registration") is not None:
            raise ValueError("No reviewed geographic registration exists for this pilot")
    for state in states.values():
        if state.get("world_geometry") is not None:
            raise ValueError("Native source geometry cannot become world geometry")
        if not state["source_ids"] or not set(state["source_ids"]).issubset(source_ids):
            raise ValueError("Every state needs reviewed source references")
        frame_id = state.get("reference_frame")
        if frame_id is not None and frame_id not in frames:
            raise ValueError("Unknown reference frame")
        if frame_id is not None:
            frame = frames[frame_id]
            if (frame.get("site") != state.get("site")
                    or state["feature_id"] not in frame.get("feature_ids", [])):
                raise ValueError("Native frame is not bound to this feature and site")
        geometry = state.get("geometry")
        if geometry is not None:
            if geometry["type"] != "source_plan_segment":
                raise ValueError("Only reviewed endpoint segments may be rendered")
            frame = frames[frame_id]
            if frame["kind"] != "source_raster" or geometry["units"] != "px":
                raise ValueError("Source-plan endpoints need their native pixel frame")
            width, height = frame["size_px"]
            if len(geometry["points"]) != 2:
                raise ValueError("An aperture chord has exactly two endpoints")
            for x, y in geometry["points"]:
                if not (0 <= x <= width and 0 <= y <= height):
                    raise ValueError("Endpoint outside its named source crop")
            if not set(geometry["source_ids"]).issubset(source_ids):
                raise ValueError("Geometry provenance is missing")
    for transition in register["transitions"]:
        if transition["from"] not in states or transition["to"] not in states:
            raise ValueError("A transition references an unknown state")
        if not transition["source_ids"] or not set(transition["source_ids"]).issubset(source_ids):
            raise ValueError("Every transition needs source references")
    graph = _chronology(register)
    for start in states:
        if _reachable(graph, start, start):
            raise ValueError("Chronology contains a cycle")


def _chronology(register: dict[str, Any]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {s["id"]: set() for s in register["states"]}
    for transition in register["transitions"]:
        if transition["evidence_kind"] != "observed":
            continue
        relation = transition["relation"]
        if relation == "before":
            graph[transition["from"]].add(transition["to"])
        elif relation in {"cuts", "uses_existing", "extends_existing"}:
            graph[transition["to"]].add(transition["from"])
    return graph


def _reachable(graph: dict[str, set[str]], start: str, target: str) -> bool:
    pending = list(graph.get(start, set()))
    seen: set[str] = set()
    while pending:
        current = pending.pop()
        if current == target:
            return True
        if current not in seen:
            seen.add(current)
            pending.extend(graph.get(current, set()))
    return False


def _finite_interval(value: Any) -> tuple[float, float] | None:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        return None
    if any(not isinstance(endpoint, (int, float)) or isinstance(endpoint, bool)
           or not math.isfinite(endpoint) for endpoint in value):
        return None
    start, end = value
    return (start, end) if start <= end else None


def _known_phase(value: Any) -> bool:
    return (isinstance(value, str) and bool(value.strip())
            and not value.strip().lower().startswith(("unknown", "unresolved", "unestablished", "undated")))


def evaluate_claim(register: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    """Apply a saved claim equally to dated, reconstructed and unknown states.

    A stratigraphic phase is not an accessibility period. Published use dates
    are not sealed construction dates. Overlapping broad date labels are never
    sufficient to certify coexistence.
    """
    states = {s["id"]: s for s in register["states"]}
    selected = [states[state_id] for state_id in query["state_ids"]]
    kind = query["kind"]
    status, detail = "unknown", "The required state observation is unrecorded."
    matched_source_ids: list[str] = []
    if kind in {"same_phase", "before"}:
        first, second = selected
        graph = _chronology(register)
        forward = _reachable(graph, first["id"], second["id"])
        reverse = _reachable(graph, second["id"], first["id"])
        if kind == "before":
            if forward:
                status, detail = "compatible", "The published relative sequence records the first state before the second."
            elif reverse:
                status, detail = "contradicted", "The published sequence runs in the opposite direction."
        elif forward or reverse:
            status, detail = "contradicted", "A published cutting or reuse relation places these states in successive phases."
        else:
            first_key = first.get("phase", {}).get("stratigraphic_key")
            second_key = second.get("phase", {}).get("stratigraphic_key")
            if first_key is not None and first_key == second_key:
                status, detail = "compatible", "Both records belong to the same named local phase; accessibility is a separate claim."
            elif first_key is not None and second_key is not None and first_key[:2] == second_key[:2]:
                status, detail = "contradicted", "The records name different stratigraphic phases in the same local excavation context."
    elif kind == "accessible_together":
        # Accessible old graves beside a later opening need an observation of
        # survival/access, not just an earlier/later ordering or date overlap.
        # A modern observed episode also cannot answer an ancient access claim.
        inspected_sources = {source["id"] for source in register["sources"] if source["inspection"] == "already_inspected"}
        required_phase = query.get("required_access_phase")
        window = _finite_interval(query.get("years"))
        calendar = query.get("calendar")
        supports, excludes = False, False
        if (_known_phase(required_phase)
                and window is not None and calendar == "historical_year"):
            for relation in register.get("access_relations", []):
                if (set(relation.get("state_ids", [])) != set(query["state_ids"])
                        or relation.get("evidence_kind") != "observed"
                        or not relation.get("source_ids")
                        or not set(relation["source_ids"]).issubset(inspected_sources)
                        or relation.get("phase") != required_phase
                        or relation.get("calendar") != calendar
                        or relation.get("dating_basis") != "dated_observed_access_episode"):
                    continue
                interval = _finite_interval(relation.get("dated_accessible_interval"))
                if interval is None:
                    continue
                start, end = interval
                window_start, window_end = window
                if (relation.get("accessible_together") is True
                        and start >= window_start and end <= window_end):
                    supports = True
                    matched_source_ids.extend(relation["source_ids"])
                elif (relation.get("accessible_together") is False
                        and relation.get("exhaustive_for_query") is True
                        and isinstance(query.get("id"), str)
                        and relation.get("query_id") == query.get("id")
                        and start <= window_start and end >= window_end):
                    # A partial/non-overlapping negative episode never excludes
                    # an unobserved ancient episode elsewhere in the window.
                    excludes = True
                    matched_source_ids.extend(relation["source_ids"])
        if supports and excludes:
            status, detail = "mixed", "Reviewed phase-bound accessibility records conflict within the saved window."
        elif supports:
            status, detail = "compatible", "A reviewed, dated access episode is bound to the query's named phase context and lies within its saved window."
        elif excludes:
            status, detail = "contradicted", "A reviewed negative access record explicitly covers the entire saved query phase/window."
        else:
            detail = "No dated observed access episode is bound to the saved ancient phase/window. Relative order, modern access and partial negative episodes leave ancient accessibility unknown."
    elif kind == "construction_window":
        state = selected[0]
        construction = state.get("phase", {}).get("construction")
        if construction is None:
            detail = "Construction is undated; cave-use attribution and survey finds cannot supply a construction contact."
        elif construction["basis"] not in {"documented_construction", "sealed_contact"}:
            detail = "The retained attribution is not an independently dated construction event."
        else:
            start, end = construction["years"]
            window_start, window_end = query["years"]
            if end < window_start or start > window_end:
                status, detail = "contradicted", "The documented construction date lies outside the saved window."
            elif start >= window_start and end <= window_end:
                status, detail = "compatible", "The construction date lies within the saved window; this alone supplies no identity or access relation."
            else:
                detail = "The construction-date bounds cross the saved window."
    elif kind == "target_datum":
        state = selected[0]
        datum = state.get("threshold_elevation")
        inspected_sources = {source["id"] for source in register["sources"] if source["inspection"] == "already_inspected"}
        frames = {frame["id"]: frame for frame in register["reference_frames"]}
        value = datum.get("value") if isinstance(datum, dict) else None
        phase = datum.get("phase") if isinstance(datum, dict) else None
        known_phase = _known_phase(phase)
        if (datum is None or not isinstance(datum, dict)
                or not isinstance(value, (int, float)) or isinstance(value, bool)
                or not math.isfinite(value)
                or datum.get("surface") != "ancient_northern_threshold"
                or not known_phase
                or state["status"] != "observed"
                or datum.get("evidence_kind") != "observed"
                or datum.get("feature_id") != state["feature_id"]
                or datum.get("site") != state.get("site")
                or datum.get("reference_frame") not in frames
                or datum.get("reference_frame") != state.get("level_reference_frame")
                or frames[datum["reference_frame"]]["kind"] != "local_excavation"
                or frames[datum["reference_frame"]].get("site") != state.get("site")
                or state["feature_id"] not in frames[datum["reference_frame"]].get("feature_ids", [])
                or datum.get("unit") != "m"
                or not datum.get("source_ids")
                or not set(datum["source_ids"]).issubset(inspected_sources)
                or not set(datum["source_ids"]).issubset(set(state["source_ids"]))
                or not set(datum["source_ids"]).intersection(frames[datum["reference_frame"]]["source_ids"])):
            detail = "No finite ancient northern threshold elevation with a known phase and local level frame is available, so z_target remains symbolic."
        else:
            status, detail = "compatible", "A named ancient threshold datum is available; the depth branch still needs its own textual and phase justification."
    else:
        raise ValueError(f"Unsupported state query: {kind}")
    return {"status": status, "detail": detail, "source_ids": list(dict.fromkeys(matched_source_ids))}


def build(repo_root: Path) -> dict[str, Any]:
    register = _read(MODULE_DIR / "register.json")
    # Existing reviewed records remain the source of aperture coordinates and
    # dimensions. Do not retype or drift the canonical corrected identities.
    repeat = _read(repo_root / "research/measurements/cycle2/iv17_repeat_results.json")
    feature_record = _read(repo_root / "registration/entry25_abu_saraj_features_2026-10-01.json")
    iv17 = next(c for c in feature_record["candidates"] if c["id"] == "Abu_Saraj_IV_17")
    aperture_state_ids = {
        "northern_present_gap": "states-iv17-north-recorded",
        "southern_remaining_gap": "states-iv17-south-recorded",
    }
    states_by_id = {s["id"]: s for s in register["states"]}
    for aperture in repeat["apertures"]:
        state = states_by_id[aperture_state_ids[aperture["canonical_id"]]]
        state["geometry"] = {
            "type": "source_plan_segment", "units": "px",
            "points": [aperture["endpoint_a_xy"], aperture["endpoint_b_xy"]],
            "source_ids": ["states-iv17-repeat"],
        }
        state["uncertainty"] = {
            "width_m": aperture["independent_corner_sensitivity_width_m"],
            "first_pilot_width_m": aperture["pilot_width_envelope_m"],
            "chord_normal_proxy_degrees": aperture["independent_corner_sensitivity_bearing_deg"],
            "first_pilot_proxy_degrees": aperture["pilot_bearing_envelope_deg"],
            "interpretation": repeat["uncertainty_method"],
            "systematic_error_quantified": False,
        }
    observed = iv17["observed"]
    observations = copy.deepcopy(register["observations"])
    observations.extend([
        {"id": "states-iv17-published-north-width", "feature_id": "iv17-north-mouth", "property": "published_width", "value": {"value": observed["northern_mouth_width_metres"], "unit": "m", "scope": "recorded opening"}, "evidence_kind": "observed", "source_ids": ["states-sion-plan"], "exposure": "already_inspected", "phase": "recorded survey arrangement; ancient date unknown", "reference_frame": "states-iv17-plan5-crop"},
        {"id": "states-iv17-wall-dimensions", "feature_id": "iv17-south-wall", "property": "published_dimensions", "value": {"length": observed["southern_wall"]["length_metres"], "thickness": observed["southern_wall"]["thickness_metres"], "unit": "m"}, "evidence_kind": "observed", "source_ids": ["states-sion-plan"], "exposure": "already_inspected", "phase": "recorded survey arrangement; construction date unknown", "reference_frame": "states-iv17-plan5-crop"},
    ])
    validate_register(register)
    results = []
    for query in register["queries"]:
        outcome = evaluate_claim(register, query)
        selected_states = [states_by_id[state_id] for state_id in query["state_ids"]]
        source_ids = list(dict.fromkeys(query["source_ids"] + outcome["source_ids"] + [source_id for state in selected_states for source_id in state["source_ids"]]))
        feature_ids = list(dict.fromkeys(state["feature_id"] for state in selected_states))
        results.append({
            "id": query["id"], "title": query["title"], "claim": query["claim"],
            "status": outcome["status"],
            "checks": [{"id": query["id"] + "-check", "label": query["predicate_label"], "status": outcome["status"], "detail": outcome["detail"], "source_ids": source_ids, "feature_ids": feature_ids}],
            "unknowns": query["unknowns"], "source_ids": source_ids, "feature_ids": feature_ids,
        })
    return {
        "id": "states", "number": 4, "title": "Historical feature states",
        "summary": "Compare recorded remains with proposed ancient configurations and retain the missing date, datum and access observations.",
        "scope": "Exploratory IV/17 and Tell es-Sultan pilots using already inspected records. Native source geometry has no geographic registration. Relative sequence, contemporaneous accessibility and feature identity are separate claims.",
        "sources": register["sources"], "features": [], "observations": observations,
        "states": register["states"], "results": results,
        "data": {
            "reference_frames": register["reference_frames"],
            "transitions": register["transitions"], "views": register["views"],
            "access_relations": register.get("access_relations", []),
            "saved_queries": register["queries"], "dependencies": register["dependencies"],
            "rendering_policy": {
                "world_geometry": None,
                "source_plan_segments": "Original project endpoint annotations only; no protected source pixels or invented cave-outline tracing.",
                "topology": "Relations and documentary succession; layout spacing is not a metric map.",
                "dates": "Null construction dates stay null; interpretive use/typology dates are labelled separately.",
            },
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(REPO_ROOT), ensure_ascii=False, indent=2))
