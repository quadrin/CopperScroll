"""Finite, source-grounded Entry 25 inventory queries; Python standard library only.

The predicate functions also accept another reviewed catalog. A null property or a
measurement in the wrong unit, phase or frame stays unknown. Branches never rank
candidates and the three-cubit instruction never becomes a width requirement.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any


MODULE_DIR = Path(__file__).resolve().parent
TRIVALENT = {"compatible", "contradicted", "unknown"}
UNKNOWN_LABELS = {"unknown", "unestablished", "not established", "not_established", "unspecified", "unresolved", "missing", "n/a", "null", "none"}


def conjunction(statuses: list[str]) -> str:
    """A necessary predicate contradiction fails a branch; missing data never do."""
    if not statuses or not set(statuses) <= TRIVALENT:
        raise ValueError("Conjunction requires nonempty trivalent predicate statuses")
    if "contradicted" in statuses:
        return "contradicted"
    if "unknown" in statuses:
        return "unknown"
    return "compatible"


def branch_summary(statuses: list[str]) -> str:
    """Preserve differing branch outcomes instead of selecting a candidate's best fit."""
    if not statuses or not set(statuses) <= TRIVALENT:
        raise ValueError("Branch summary requires nonempty trivalent statuses")
    values = set(statuses)
    return next(iter(values)) if len(values) == 1 else "mixed"


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _interval(value: Any) -> tuple[float, float] | None:
    if _number(value):
        return float(value), float(value)
    if isinstance(value, list) and len(value) == 2 and all(_number(item) for item in value):
        if value[0] > value[1]:
            raise ValueError("Interval endpoints must be ordered")
        return float(value[0]), float(value[1])
    return None


def _known_label(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value.strip().casefold() not in UNKNOWN_LABELS


def _threshold_binding(candidate: dict, observation: dict) -> str | None:
    """A threshold scalar must identify its feature and a local vertical datum.

    The reference frame can remain local. Its label/ID must match the datum's
    explicit frame binding; no world coordinates follow from that agreement.
    The z-minus-depth model needs heights increasing upward.
    """
    feature_id = candidate.get("reference_features", {}).get("northern_opening")
    if not _known_label(feature_id) or observation.get("feature_id") != feature_id:
        return "Elevation is not explicitly bound to this candidate's northern-opening feature."
    reference_frame = observation.get("reference_frame")
    frame_id = reference_frame.get("id") if isinstance(reference_frame, dict) else reference_frame
    if not _known_label(frame_id) or any(label in frame_id.casefold() for label in ("unestablished", "unspecified", "unresolved", "unknown")):
        return "A registered vertical reference frame is not supplied."
    datum = observation.get("datum")
    if not isinstance(datum, dict) or not _known_label(datum.get("id")) or not _known_label(datum.get("reference_point")):
        return "A named vertical datum and reference point are not supplied."
    if datum.get("reference_frame") != frame_id:
        return "The vertical datum is not bound to the observation's reference frame."
    if datum.get("positive_direction") != "up":
        return "The vertical datum does not establish heights increasing upward for z_target = z_threshold - depth."
    return None


def evaluate_predicate(candidate: dict, predicate: dict) -> dict:
    """Evaluate equals, known, at_least or between on one reviewed property.

    ``between`` requires the whole observed interval to fit. A partial overlap is
    unknown; it cannot certify either a fit or a miss. A requested reference
    frame/phase/unit must be attested, not inferred from the numeric value. A
    known northern-threshold elevation also requires a finite scalar and a
    feature-bound vertical datum. Generic known values may be structured.
    """
    operation = predicate.get("operation", "equals")
    if operation not in {"equals", "known", "at_least", "between"}:
        raise ValueError(f"Unsupported predicate operation: {operation}")
    key = predicate["property"]
    observation = candidate.get("properties", {}).get(key, {})
    value = observation.get("value")
    out = {
        "id": predicate.get("id", key),
        "label": predicate.get("label", key.replace("_", " ")),
        "property": key,
        "status": "unknown",
        "detail": observation.get("note", "No reviewed observation supplies this property."),
        "value": value,
        "source_ids": observation.get("source_ids", []),
        "feature_ids": [observation.get("feature_id", candidate["feature_ids"][0])],
    }
    for qualifier in ("unit", "reference_frame", "phase", "datum"):
        if qualifier in observation:
            out[qualifier] = observation[qualifier]
    if value is None:
        return out
    for qualifier in ("unit", "reference_frame", "phase"):
        expected = predicate.get(qualifier)
        if expected is not None and observation.get(qualifier) != expected:
            out["detail"] = f"Required {qualifier} {expected!r} is not established for this observation."
            return out
    if operation == "known":
        if isinstance(value, str) and (not value.strip() or value.strip().casefold() in UNKNOWN_LABELS):
            out["detail"] = "A placeholder label does not supply a known observation."
            return out
        if predicate.get("value_type") == "finite_number" or key == "northern_threshold_elevation":
            if not _number(value):
                out["detail"] = "A finite scalar quantity is required; booleans, nonfinite values and placeholder labels are not elevations."
                return out
        if key == "northern_threshold_elevation":
            binding_error = _threshold_binding(candidate, observation)
            if binding_error:
                out["detail"] = binding_error
                return out
        out["status"] = "compatible"
        out["detail"] = observation.get("note", "Required observation is supplied.")
        return out
    if operation == "equals":
        expected = predicate["expected"]
        # Python otherwise treats True as equal to 1. Quantities are not booleans.
        same_kind = isinstance(value, bool) == isinstance(expected, bool)
        if not same_kind:
            out["detail"] = "A boolean feature observation cannot substitute for a numeric/categorical quantity, or vice versa."
            return out
        out["status"] = "compatible" if value == expected else "contradicted"
    else:
        observed_range = _interval(value)
        if observed_range is None:
            out["detail"] = "A finite numeric observation is not supplied."
            return out
        low, high = observed_range
        if operation == "at_least":
            expected = predicate["expected"]
            if not _number(expected):
                raise ValueError("at_least requires a finite numeric expected value")
            out["status"] = "compatible" if low >= expected else "contradicted" if high < expected else "unknown"
        else:
            required_range = _interval(predicate["expected"])
            if required_range is None:
                raise ValueError("between requires finite ordered bounds")
            minimum, maximum = required_range
            if low >= minimum and high <= maximum:
                out["status"] = "compatible"
            elif high < minimum or low > maximum:
                out["status"] = "contradicted"
            else:
                out["detail"] = "Observed interval overlaps the query bounds but is not wholly inside or outside them."
                return out
    if "note" not in observation:
        out["detail"] = f"Reviewed value {value!r}; query {operation} {predicate['expected']!r}."
    return out


def expand_branches(query: dict, dimensions: list[dict]) -> list[dict]:
    """One Cartesian branch set is generated before applying it to every control."""
    by_id = {dimension["id"]: dimension for dimension in dimensions}
    ids = query["branch_dimensions"]
    if len(ids) != len(set(ids)) or any(dimension not in by_id for dimension in ids):
        raise ValueError("Query dimensions must be unique and defined")
    branches = []
    for choices in itertools.product(*(by_id[dimension]["options"] for dimension in ids)):
        selection = {dimension: choice["id"] for dimension, choice in zip(ids, choices)}
        branch = {"id": query["id"] + "--" + "--".join(selection.values()), "choices": selection}
        if "unit" in selection:
            cubit = next(option["value"] for option in by_id["unit"]["options"] if option["id"] == selection["unit"])
            branch["depth_metres"] = round(3 * cubit, 8)
            branch["depth_relation"] = (
                "z_target = z_northern_threshold - depth"
                if selection["direction"] == "vertical"
                else "target = northern_origin + distance along declared horizontal path"
            )
        branches.append(branch)
    return branches


def _predicates(query: dict, branch: dict, dimensions: list[dict]) -> list[dict]:
    by_id = {dimension["id"]: dimension for dimension in dimensions}
    choices = branch["choices"]
    selected = {
        dimension: next(option for option in by_id[dimension]["options"] if option["id"] == choice)
        for dimension, choice in choices.items()
    }
    predicates = [
        {"id": "landmark", "label": selected["reading"]["label"] + " association", "property": selected["reading"]["property"], "expected": True},
        {"id": "mouth-pair", "label": "Two exterior openings", "property": "two_exterior_openings", "expected": True},
        {"id": "northern-member", "label": "Northern opening distinguishable", "property": "northern_member", "expected": True},
        {"id": "aspect", "label": selected["orientation"]["label"], "property": selected["orientation"]["property"], "expected": True},
    ]
    if query["kind"] == "reported_form":
        return predicates
    if query["kind"] != "target_prerequisites":
        raise ValueError(f"Unsupported saved query kind: {query['kind']}")
    if choices["phase"] == "ancient":
        predicates.append({
            "id": "phase", "label": "Arrangement established for text-associated ancient phase",
            "property": "ancient_arrangement_phase", "expected": True,
        })
    if choices["direction"] == "vertical":
        predicates.append({
            "id": "threshold-datum", "label": "Northern threshold elevation and datum",
            "property": "northern_threshold_elevation", "operation": "known", "unit": "m",
            "value_type": "finite_number",
            "phase": selected["phase"]["value"],
        })
    else:
        predicates.extend([
            {"id": "horizontal-origin", "label": "Registered origin within northern opening", "property": "northern_horizontal_origin", "operation": "known", "phase": selected["phase"]["value"]},
            {"id": "horizontal-path", "label": "Declared horizontal path/direction", "property": "horizontal_path_direction", "operation": "known", "phase": selected["phase"]["value"]},
        ])
    return predicates


def evaluate_query(query: dict, candidates: list[dict], dimensions: list[dict]) -> dict:
    branches = expand_branches(query, dimensions)
    candidate_results = []
    for candidate in candidates:
        outcomes = []
        for branch in branches:
            checks = [evaluate_predicate(candidate, predicate) for predicate in _predicates(query, branch, dimensions)]
            outcomes.append({
                "branch_id": branch["id"],
                "status": conjunction([check["status"] for check in checks]),
                "checks": checks,
            })
        candidate_results.append({
            "candidate_id": candidate["id"],
            "status": branch_summary([outcome["status"] for outcome in outcomes]),
            "counts": {status: sum(outcome["status"] == status for outcome in outcomes) for status in sorted(TRIVALENT)},
            "branches": outcomes,
        })
    return {**query, "branches": branches, "candidate_results": candidate_results}


def _review_consistency(repo_root: Path, candidates: list[dict]) -> None:
    """Fail if copied reviewed quantities drift from the authoritative local records."""
    by_id = {candidate["id"]: candidate for candidate in candidates}
    registration = json.loads((repo_root / "registration/entry25_abu_saraj_features_2026-10-01.json").read_text())
    iv17 = next(candidate for candidate in registration["candidates"] if candidate["id"] == "Abu_Saraj_IV_17")
    repeat = json.loads((repo_root / "research/measurements/cycle2/iv17_repeat_results.json").read_text())
    north = next(aperture for aperture in repeat["apertures"] if aperture["canonical_id"] == "northern_present_gap")
    expected = {
        "northern_opening_width_reported": iv17["observed"]["northern_mouth_width_metres"],
        "northern_opening_chord_width": north["width_m"],
        "northern_chord_normal_proxy": north["outward_chord_normal_proxy_deg"],
    }
    for key, value in expected.items():
        if by_id["iv17"]["properties"][key]["value"] != value:
            raise ValueError(f"Reviewed inventory {key} differs from its existing source record; review the catalog before rebuilding")
    if by_id["iv17"]["properties"]["published_use_reconstruction"]["value"] != iv17["published_reconstruction"]["use"]:
        raise ValueError("IV/17 use reconstruction differs from the existing source record")
    twin = json.loads((repo_root / "registration/entry25_twin_cave_features_2026-10-01.json").read_text())
    if twin["published_features"]["mouth_dimensions"] is not None:
        raise ValueError("Twin Cave mouth dimensions have changed; review the inventory catalog")


def _candidate_result(candidate: dict, form: dict, target: dict) -> dict:
    form_result = next(item for item in form["candidate_results"] if item["candidate_id"] == candidate["id"])
    target_result = next(item for item in target["candidate_results"] if item["candidate_id"] == candidate["id"])
    checks = []
    for outcome, branch in zip(form_result["branches"], form["branches"]):
        labels = branch["choices"]
        checks.append({
            "id": candidate["id"] + "-form-" + labels["reading"] + "-" + labels["orientation"],
            "label": f"{labels['reading']} / {labels['orientation']}",
            "status": outcome["status"],
            "detail": "; ".join(f"{check['label']}: {check['status']}" for check in outcome["checks"]),
            "source_ids": sorted({source for check in outcome["checks"] for source in check["source_ids"]}),
            "feature_ids": candidate["feature_ids"],
        })
    checks.extend([
        {
            "id": candidate["id"] + "-target", "label": "Target prerequisites across all 96 retained branches",
            "status": target_result["status"],
            "detail": "Missing northern threshold datum or horizontal origin/path leaves every target branch unknown; ancient architectural phase is also unresolved. Unit/deposit alternatives are reported without converting them into entrance-width or deposit-presence predicates.",
            "source_ids": candidate["source_ids"] + ["inventory-puech-entry25", "inventory-entry25-assessment"],
            "feature_ids": candidate["feature_ids"],
        },
        {
            "id": candidate["id"] + "-true-bearings", "label": "True individual-mouth bearings",
            "status": "unknown", "detail": "No surveyed true bearings or edition angular tolerance. Qualitative aspect and source-plan proxies remain distinct.",
            "source_ids": candidate["properties"]["true_individual_mouth_bearings"]["source_ids"],
            "feature_ids": candidate["feature_ids"],
        },
    ])
    unknowns = [
        "Ancient arrangement phase and dated northern threshold contacts are unresolved.",
        "No registered northern threshold elevation or horizontal origin/path supplies a target.",
        "True mouth bearings, geographic mouth coordinates and an unused prediction are unavailable.",
    ]
    if candidate["id"] == "iv11":
        unknowns.insert(0, "An exterior opening pair is not established; missing documentation is not absence.")
    if candidate["id"] == "iv17":
        unknowns.insert(0, "Individual-mouth eastward aspect is not established by eastern-cliff description or chord-normal proxies.")
    return {
        "id": "inventory-" + candidate["id"],
        "title": candidate["name"] + ": form and target prerequisites",
        "claim": "Exploratory reported-form comparison under all retained readings; no complete ancient identification or digging target.",
        "status": "unknown",
        "checks": checks,
        "unknowns": unknowns,
        "source_ids": candidate["source_ids"] + ["inventory-puech-entry25", "inventory-entry25-assessment"],
        "feature_ids": candidate["feature_ids"],
    }


def build(repo_root: Path) -> dict:
    catalog = json.loads((MODULE_DIR / "catalog.json").read_text())
    specification = json.loads((MODULE_DIR / "queries.json").read_text())
    candidates = catalog["candidates"]
    _review_consistency(repo_root, candidates)
    for source in catalog["sources"]:
        if not (repo_root / source["repo_path"]).is_file():
            raise ValueError(f"Missing local source note: {source['repo_path']}")
    queries = [evaluate_query(query, candidates, specification["dimensions"]) for query in specification["queries"]]
    observations = []
    for candidate in candidates:
        for key, property_record in candidate["properties"].items():
            observation = {
                "id": "inventory-" + candidate["id"] + "-" + key.replace("_", "-"),
                "feature_id": property_record.get("feature_id", candidate["feature_ids"][0]),
                "property": key,
                "value": {"amount": property_record["value"], "unit": property_record["unit"]} if property_record.get("unit") and property_record["value"] is not None else property_record["value"],
                "evidence_kind": property_record["evidence_kind"],
                "source_ids": property_record["source_ids"],
                "exposure": "derived" if property_record["evidence_kind"] == "inference" else "already_inspected",
            }
            for key in ("phase", "reference_frame", "datum", "uncertainty", "note"):
                if key in property_record:
                    observation[key] = property_record[key]
            # Keep the units for null quantities too; a null datum is not zero.
            if "unit" in property_record:
                observation["unit"] = property_record["unit"]
            observations.append(observation)
    return {
        "id": "inventory", "number": 3,
        "title": "Inventory queries",
        "summary": "Apply the same saved Entry 25 branches to IV/17, IV/11 and Twin Cave. Reported pillar/two-opening forms overlap; ancient phase and target datums remain unknown.",
        "scope": "Three already examined controls. Four reported-form branches and 96 target-prerequisite branches per control; no regional inventory completeness, rarity, ranking or confirmation claim.",
        "sources": catalog["sources"],
        "features": [],
        "observations": observations,
        "states": [],
        "results": [_candidate_result(candidate, queries[0], queries[1]) for candidate in candidates],
        "data": {
            "schema_version": 1,
            "reviewed_at": catalog["reviewed_at"],
            "catalog": candidates,
            "dimensions": specification["dimensions"],
            "queries": queries,
            "limits": catalog["limits"],
            "semantics": {
                "compatible": "Every required reported predicate in this branch is supplied; exploratory compatibility only.",
                "contradicted": "At least one required predicate has a positive incompatible observation in an eligible frame/phase.",
                "unknown": "At least one required predicate lacks an eligible observation, with no positive contradiction.",
                "mixed": "Retained branches have different outcomes; all remain visible and none is selected as a candidate score.",
                "unit": "Three 0.40/0.50/0.60 m cubit sensitivity samples produce 1.20/1.50/1.80 m conditional distance; they never define mouth size.",
            },
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=MODULE_DIR.parents[2])
    args = parser.parse_args()
    print(json.dumps(build(args.repo_root), indent=2, ensure_ascii=False))
