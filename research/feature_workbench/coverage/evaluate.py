"""Source-grounded coverage and negative-excavation gates (method 5).

J01-J28 are documentary records, not a list of distinct eligible basins.
The evaluator imports reviewed evidence without changing its historical files.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
import math
from pathlib import Path
from typing import Any


INVENTORY_PATH = "research/assessments/entry29_jericho_pools/regional_inventory_2026-10-06.json"
WADI_PATH = "research/assessments/entry29_jericho_pools/wadi_en_nueima_original_2026-10-06.json"
IV17_PHASE_PATH = "research/measurements/cycle3/iv17_phase.json"
IV17_ASSESSMENT_PATH = "research/assessments/entry25_iv17/assessment.json"
IV17_REVIEW_PATH = "research/sources/atiqot41_iv11_iv17_review_2026-10-01.md"

GATE_LABELS = {
    "ancient_target_volume": "Bounded ancient target volume",
    "ancient_datum": "Ancient surface and survey datum",
    "actual_reach": "Actual excavation reach through the target",
    "phase_alignment": "Target and exposed state in the same phase",
    "disturbance_assessment": "Target preservation and disturbance assessed",
    "detection_method": "Documented method and detection limits",
}

# Presence of a published depth, an object or a period heading does not meet
# these predicates. Each established gate also requires source provenance.
REQUIRED_VALUE_FIELDS = {
    "ancient_target_volume": ("geometry", "reference_frame"),
    "ancient_datum": ("datum_id", "datum_kind", "surface", "surface_id", "surface_phase", "ancient_surface_verified", "ancient_surface_source_ids", "reference_frame"),
    "actual_reach": ("covers_entire_target", "reference_frame", "target_id", "datum_id"),
    "phase_alignment": ("target_phase", "exposed_phase", "phase_identifiers_explicit", "coexistence_verified"),
    "disturbance_assessment": ("target_preservation_assessed", "negative_observation_interpretable", "unexplained_removal_used_as_rescue"),
    "detection_method": ("method", "limits", "adequate_for_predicted_material"),
}


def _load(repo_root: Path, relative_path: str) -> dict[str, Any]:
    return json.loads((repo_root / relative_path).read_text(encoding="utf-8"))


def _sid(source_id: str) -> str:
    return "coverage-" + source_id.lower().replace("_", "-")


def _unique(values: list[Any]) -> list[Any]:
    """Stable de-duplication that accepts JSON objects as well as scalars."""
    result, seen = [], set()
    for value in values:
        key = json.dumps(value, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            result.append(value)
            seen.add(key)
    return result


def _locators(value: Any) -> list[dict[str, Any]]:
    """Find the actual source/page/figure locators in the reviewed input."""
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if "source_id" in value and ("printed_pages" in value or "figures" in value):
            found.append(value)
        for child in value.values():
            found.extend(_locators(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_locators(child))
    return found


def _source_ids(locators: list[dict[str, Any]]) -> list[str]:
    return _unique([_sid(item["source_id"]) for item in locators])


def _has_source_ids(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and bool(item.strip()) for item in value)


def _finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _measured_benchmark_join(value: dict[str, Any]) -> bool:
    """A modern datum is usable only through its measured ancient-surface join."""
    join = value.get("modern_benchmark_join") or {}
    if not isinstance(join, dict):
        return False
    offset = join.get("measured_offset") or {}
    return (
        isinstance(offset, dict)
        and _finite_number(offset.get("value"))
        and offset.get("unit") == "m"
        and offset.get("convention") == "ancient_surface_minus_benchmark"
        and _finite_number(join.get("uncertainty_m"))
        and join["uncertainty_m"] >= 0
        and join.get("benchmark_id") == value["datum_id"]
        and join.get("ancient_surface_id") == value["surface_id"]
        and join.get("surface_phase") == value["surface_phase"]
        and join.get("reference_frame") == value["reference_frame"]
        and _has_source_ids(join.get("source_ids"))
    )


def evaluate_target(target: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a bounded target without converting unknowns into failures.

    Gate input uses state=established/contradicted/unknown, a structured value,
    source_ids and detail. A bare 'established' assertion does not pass. Reference
    frames must also agree across target, datum and reach. This evaluates whether
    a negative observation is usable; it does not identify a landmark or deposit.
    """
    evaluated = []
    supplied = target.get("gate_evidence", {})
    for gate_id, label in GATE_LABELS.items():
        evidence = supplied.get(gate_id, {})
        value = deepcopy(evidence.get("value"))
        raw_sources = evidence.get("source_ids", [])
        sources = _unique(raw_sources) if _has_source_ids(raw_sources) else []
        status = "unknown"
        detail = evidence.get("detail") or "The reviewed inputs do not establish this target-specific observation."
        state = evidence.get("state", "unknown")
        structured = isinstance(value, dict) and all(
            field in value and value[field] is not None and value[field] not in ("", [], {})
            for field in REQUIRED_VALUE_FIELDS[gate_id]
        )
        if state == "contradicted" and sources and value is not None:
            status = "contradicted"
        elif state == "established" and structured and sources:
            status = "compatible"
            truth_field = {
                "actual_reach": "covers_entire_target",
                "phase_alignment": "coexistence_verified",
                "disturbance_assessment": "target_preservation_assessed",
                "detection_method": "adequate_for_predicted_material",
            }.get(gate_id)
            if truth_field and value[truth_field] is not True:
                status = "contradicted" if value[truth_field] is False else "unknown"
            if gate_id == "disturbance_assessment" and value["unexplained_removal_used_as_rescue"] is not False:
                status = "contradicted" if value["unexplained_removal_used_as_rescue"] is True else "unknown"
            if gate_id == "disturbance_assessment" and value["negative_observation_interpretable"] is not True:
                status = "contradicted" if value["negative_observation_interpretable"] is False else "unknown"
            if gate_id == "phase_alignment":
                target_phase = value["target_phase"]
                exposed_phase = value["exposed_phase"]
                explicit_ids = (
                    value["phase_identifiers_explicit"] is True
                    and isinstance(target_phase, str)
                    and isinstance(exposed_phase, str)
                )
                equivalence = value.get("phase_equivalence") or {}
                documented_equivalence = (
                    isinstance(equivalence, dict)
                    and equivalence.get("target_phase") == target_phase
                    and equivalence.get("exposed_phase") == exposed_phase
                    and equivalence.get("relation") == "same_archaeological_state"
                    and _has_source_ids(equivalence.get("source_ids"))
                    and isinstance(equivalence.get("named_contact"), str)
                    and bool(equivalence.get("named_contact"))
                )
                if value.get("phase_relation") == "incompatible":
                    status = "contradicted"
                    detail += " The supplied phase record explicitly reports incompatible states."
                elif status == "compatible" and (not explicit_ids or (target_phase != exposed_phase and not documented_equivalence)):
                    status = "unknown"
                    detail += " Explicit matching phase identities or a sourced same-state contact are required; period labels and broad date overlap cannot establish coexistence."
        elif state == "established":
            detail += " The supplied assertion lacks a complete value or source provenance."
        evaluated.append({
            "id": gate_id, "label": label, "status": status,
            "detail": detail, "value": value, "source_ids": sources,
            "feature_ids": target.get("feature_ids", []),
        })

    datum = next(gate for gate in evaluated if gate["id"] == "ancient_datum")
    alignment = next(gate for gate in evaluated if gate["id"] == "phase_alignment")
    if datum["status"] == "compatible":
        datum_value = datum["value"]
        verified_surface = (
            datum_value["ancient_surface_verified"] is True
            and isinstance(datum_value["surface_id"], str)
            and isinstance(datum_value["surface_phase"], str)
            and _has_source_ids(datum_value["ancient_surface_source_ids"])
        )
        if not verified_surface:
            datum["status"] = "unknown"
            datum["detail"] += " A sourced, verified ancient surface identity and exact phase are required; a modern surface cannot substitute."
        elif alignment["status"] != "compatible":
            datum["status"] = "unknown"
            datum["detail"] += " The surface-to-target phase join depends on an unresolved target/exposed-state alignment."
        elif datum_value["surface_phase"] not in (alignment["value"]["target_phase"], alignment["value"]["exposed_phase"]):
            datum["status"] = "unknown"
            datum["detail"] += " The ancient surface belongs to a different phase from the accepted target/exposed state."
        elif datum_value["datum_kind"] == "ancient_surface":
            if datum_value["datum_id"] != datum_value["surface_id"]:
                datum["status"] = "unknown"
                datum["detail"] += " The direct ancient datum does not name the verified ancient surface."
        elif datum_value["datum_kind"] == "modern_benchmark":
            if not _measured_benchmark_join(datum_value):
                datum["status"] = "unknown"
                datum["detail"] += " A modern benchmark needs a sourced measured join to this exact ancient surface, phase and reference frame, with offset convention and bounded uncertainty."
        else:
            datum["status"] = "unknown"
            datum["detail"] += " Datum kind is neither a directly verified ancient surface nor a joined modern benchmark."

    framed = [gate for gate in evaluated if gate["id"] in ("ancient_target_volume", "ancient_datum", "actual_reach")]
    if all(gate["status"] == "compatible" for gate in framed):
        frames = [json.dumps(gate["value"]["reference_frame"], sort_keys=True) for gate in framed]
        if len(set(frames)) != 1:
            for gate in framed:
                gate["status"] = "unknown"
                gate["detail"] += " Target, datum and reach are in unmatched reference frames."

        reach = next(gate for gate in framed if gate["id"] == "actual_reach")
        datum = next(gate for gate in framed if gate["id"] == "ancient_datum")
        if reach["value"]["target_id"] != target["id"] or reach["value"]["datum_id"] != datum["value"]["datum_id"]:
            reach["status"] = "unknown"
            reach["detail"] += " The reach record does not name this target and the same ancient datum."

    missing = [gate["id"] for gate in evaluated if gate["status"] == "unknown"]
    failed = [gate["id"] for gate in evaluated if gate["status"] == "contradicted"]
    eligible = not missing and not failed
    finding = target.get("negative_observation") or {}
    reported_negative = (
        finding.get("no_predicted_material") is True
        and _has_source_ids(finding.get("source_ids"))
        and finding.get("target_id") == target["id"]
    )
    return {
        "id": target["id"], "label": target["label"],
        "feature_ids": target.get("feature_ids", []),
        "geometry": target.get("geometry"),
        "gates": evaluated, "missing_gate_ids": missing,
        "failed_gate_ids": failed,
        "negative_excavation_eligible": eligible,
        "negative_deposit_status": "compatible" if eligible and reported_negative else "unknown",
        "negative_claim_allowed": eligible and reported_negative,
        "negative_observation": deepcopy(target.get("negative_observation")),
        "scope": "Target-specific coverage gate only; no landmark identification or deposit-existence conclusion.",
    }


def _unknown_target(target_id: str, label: str, source_ids: list[str], details: dict[str, str], feature_ids: list[str] | None = None) -> dict[str, Any]:
    return evaluate_target({
        "id": target_id, "label": label, "feature_ids": feature_ids or [],
        "geometry": None, "negative_observation": None,
        "gate_evidence": {
            gate_id: {"state": "unknown", "value": None, "source_ids": source_ids,
                      "detail": details.get(gate_id, "No target-specific observation is established in the imported reviewed evidence.")}
            for gate_id in GATE_LABELS
        },
    })


def _deduplicate_coverage_observations(records: list[dict[str, Any]], sources: dict[str, Any]) -> list[dict[str, Any]]:
    """Collapse only explicitly shared source features, never possible aliases."""
    groups: dict[str, dict[str, Any]] = {}
    for record in records:
        citation = record["citation"]
        source = sources[citation["source_id"]]
        lineage = source.get("observation_lineage_id")
        physical_notice = record.get("normalization_notice_id")
        # An explicit numbered source feature justifies a shared-observation key.
        # Without it the historical observation ID is retained.
        key = json.dumps([physical_notice or record["id"], record["status"], lineage or citation["source_id"]])
        if key not in groups:
            groups[key] = {
                "id": "coverage-" + record["id"].lower().replace("_", "-"),
                "original_observation_ids": [], "related_notice_ids": [],
                "physical_notice_id": physical_notice,
                "status": record["status"], "campaign_id": lineage,
                "source_ids": [], "citation": deepcopy(citation),
                "geometry": None, "reference_frame": None,
                "whole_basin_unexcavated": record.get("whole_basin_unexcavated"),
                "whole_basin_destroyed": record.get("whole_basin_destroyed"),
                "target_volume_relation": None,
            }
        group = groups[key]
        group["original_observation_ids"] = _unique(group["original_observation_ids"] + [record["id"]])
        group["related_notice_ids"] = _unique(group["related_notice_ids"] + record["original_ids"])
        group["source_ids"] = _unique(group["source_ids"] + [_sid(citation["source_id"])])
    return list(groups.values())


def _source_registry(inventory: dict[str, Any], wadi: dict[str, Any], phase: dict[str, Any]) -> list[dict[str, Any]]:
    locators = _locators(inventory)
    result = []
    for source_id, source in inventory["sources"].items():
        matching = [item for item in locators if item["source_id"] == source_id]
        pages = _unique([page for item in matching for page in (item.get("printed_pages") or [])])
        figures = _unique([figure for item in matching for figure in (item.get("figures") or [])])
        result.append({
            "id": _sid(source_id), "title": source["title"],
            "citation": "Recorded inspected scope: printed pages " + (", ".join(map(str, pages)) or "see evidence note") + ("; " + "; ".join(figures) if figures else ""),
            "repo_path": INVENTORY_PATH, "url": source.get("source_url"),
            "inspection": "already_inspected", "original_campaign": source.get("observation_lineage_id"),
            "source_role": source.get("role"), "locators": _unique(matching),
        })
    original = wadi["supplied_original_review"]
    result.extend([
        {"id": "coverage-inventory", "title": "Jericho source-sector inventory and normalization",
         "citation": "J01–J28, twelve named documentary sectors, twenty-one additional coverage obligations; derived reviewed record dated 6 October 2026.",
         "repo_path": INVENTORY_PATH, "inspection": "derived", "original_campaign": None},
        {"id": "coverage-wadi-original", "title": "U. Dinur and N. Feig, Wadi Nu‘eima, ESI 5 (1986 designation; printed 1987)",
         "citation": "Complete report, printed pp. 110–111 / PDF pp. 118–119; Fig. 56 is an artifact illustration, not a bath plan.",
         "repo_path": WADI_PATH, "url": original["source"]["publisher_record_url"],
         "inspection": "already_inspected", "original_campaign": "dinur_feig_wadi_nueima_observation_lineage"},
        {"id": "coverage-sion-iv17", "title": "Ofer Sion, Regions IV and VI, ʿAtiqot 41 part 1 (2002)",
         "citation": "Printed pp. 61–64 / Plan 5 p. 63; pp. 81–83, Table 1, note 11 and editorial archive pointer. Partial article scope.",
         "repo_path": IV17_REVIEW_PATH, "url": phase["source"]["publisher_record"],
         "inspection": "already_inspected", "original_campaign": "abu_saraj_survey_dadon_l656_reporting"},
        {"id": "coverage-iv17-phase", "title": "IV/17 catalogue-to-architecture contact review",
         "citation": "Cycle 3, 2 October 2026; Sion pp. 63–64, 81–83 / Table 1 and notes; same observation lineage.",
         "repo_path": IV17_PHASE_PATH, "inspection": "derived", "original_campaign": "abu_saraj_survey_dadon_l656_reporting"},
        {"id": "coverage-iv17-assessment", "title": "Entry 25 IV/17 conditional assessment",
         "citation": "Depth branch and northern threshold datum, assessment dated 2 October 2026; derived from previously exposed evidence.",
         "repo_path": IV17_ASSESSMENT_PATH, "inspection": "derived", "original_campaign": "abu_saraj_survey_dadon_l656_reporting"},
    ])
    return result


def build(repo_root: Path) -> dict[str, Any]:
    repo_root = Path(repo_root)
    inventory = _load(repo_root, INVENTORY_PATH)
    wadi = _load(repo_root, WADI_PATH)
    phase = _load(repo_root, IV17_PHASE_PATH)
    assessment = _load(repo_root, IV17_ASSESSMENT_PATH)
    original = wadi.get("supplied_original_review")
    if not original or not original.get("complete_report_scope") or not wadi["current_status"]["original_body_obtained"]:
        raise ValueError("The current reviewed Wadi original is required; historical pending-source fields cannot be substituted.")
    record_ids = [record["original_id"] for record in inventory["records"]]
    if len(record_ids) != len(set(record_ids)):
        raise ValueError("Duplicate original documentary IDs in regional inventory")
    if set(record_ids) != {f"J{i:02}" for i in range(1, 29)}:
        raise ValueError("The imported J01–J28 baseline changed; review the documentary scope before rebuilding.")

    sources = _source_registry(inventory, wadi, phase)
    source_ids = {source["id"] for source in sources}
    notices, targets = [], []
    for record in inventory["records"]:
        refs = _source_ids(record["source_locators"])
        campaigns = deepcopy(record.get("observation_lineage_ids") or [])
        current_coverage = record["reported_coverage"]
        flags = deepcopy(record["coverage_flags"])
        feature_ids: list[str] = []
        extra: dict[str, Any] = {}
        next_observation = record["next_observation"]
        if record["original_id"] == "J23":
            refs = _unique(refs + ["coverage-wadi-original"])
            campaigns = _unique(campaigns + ["dinur_feig_wadi_nueima_observation_lineage"])
            feature_ids = ["wadi-nueima-described-miqva"]
            current_coverage = "One described bath exposed by illegal excavation; alluvial concealment and flash-flood exposure reported. Target reach and detection limits remain unknown."
            flags = _unique(flags + ["alluvial_concealment", "flash_flood_exposure", "illegal_excavation"])
            next_observation = original["next_observation"]
            extra = {
                "current_original_status": "already_inspected",
                "original_scope_complete": original["complete_report_scope"],
                "explicit_baths_described": original["cardinality"]["explicit_baths_described_in_report"],
                "complete_site_bath_count": original["cardinality"]["complete_site_bath_count"],
                "bath_locus_id": original["cardinality"]["individual_bath_locus_id"],
                "reported_depth_m": original["reported_features"][0]["reported_depth_m"],
                "bath_footprint_dimensions_m": original["reported_features"][0]["footprint_dimensions_m"],
                "bath_construction_date": original["site"]["bath_construction_date"],
                "site_period_not_bath_date": original["scope_limits"]["site_chronology_not_transferred_to_bath"],
                "western_rectangle_dimensions_not_bath_dimensions": original["scope_limits"]["adjacent_rectangle_dimensions_not_transferred_to_bath"],
                "historical_source_dependency_superseded": True,
            }
        target_id = "coverage-target-" + record["original_id"].lower()
        details = {
            "ancient_target_volume": "No bounded ancient deposit-target volume is defined for this documentary notice.",
            "ancient_datum": "No verified ancient target surface and survey-datum package is established.",
            "actual_reach": current_coverage + " This does not establish intersection with a defined ancient target volume.",
            "phase_alignment": "Published period labels do not establish target, architecture and excavated surface coexistence.",
            "disturbance_assessment": "Reported preservation flags are retained; disturbance throughout the defined target volume is not established.",
            "detection_method": "No target-specific detection method and limits are established; report silence is unknown.",
        }
        target = _unknown_target(target_id, record["label"], refs, details, feature_ids)
        targets.append(target)
        notices.append({
            "id": record["original_id"], "label": record["label"],
            "sector_id": record["sector_id"], "record_kind": record["record_kind"],
            "coverage_detail": current_coverage, "flags": flags,
            "campaign_ids": campaigns, "campaign_identity_unknown": not bool(campaigns),
            "physical_identity": {"physical_locus": record["physical_locus"],
                                  "state_family_id": record["state_family_id"],
                                  "identity_state": record["identity_state"],
                                  "distinct_eligible_feature": None},
            "geometry": None, "reference_frame": None,
            "regional_polygon_membership": record["regional_polygon_membership"],
            "present_day_field_status": record["present_day_field_status"],
            "reported_dimensions": deepcopy(record["reported_dimensions"]),
            "reported_phase": (
                {"site_period": original["site"]["reported_period_range"], "bath_construction_date": None,
                 "site_period_does_not_date_bath": True}
                if record["original_id"] == "J23" else deepcopy(record["gates"]["phase"])
            ),
            "reported_datum": deepcopy(record["gates"]["datum"]),
            "reported_detection_gates": deepcopy(record["gates"]["detection"]),
            "source_ids": refs, "source_locators": deepcopy(record["source_locators"]),
            "target_id": target_id, "gate_ids": list(GATE_LABELS),
            "missing_gate_ids": target["missing_gate_ids"],
            "negative_deposit_status": target["negative_deposit_status"],
            "next_observation": next_observation,
            "historical_record": {"reported_coverage": record["reported_coverage"],
                                  "inherited_missing_observations": record["inherited_missing_observations"],
                                  "next_observation": record["next_observation"]},
            **extra,
        })

    obligations = []
    for item in inventory["coverage_notices"]:
        obligations.append({
            "id": item["id"], "label": item["label"], "record_kind": item["record_kind"],
            "sector_id": item["sector_id"], "related_notice_ids": item["related_original_ids"],
            "source_reported_cardinality": item["source_reported_cardinality"],
            "independent_eligible_basin_count": item["independent_eligible_basin_count"],
            "regional_polygon_membership": item["regional_polygon_membership"],
            "detail": item["evidence"], "next_observation": item["next_observation"],
            "source_ids": _source_ids(item["citations"]), "citations": deepcopy(item["citations"]),
            "geometry": None, "reference_frame": None,
            "missing_gate_ids": list(GATE_LABELS),
        })

    coverage_observations = _deduplicate_coverage_observations(inventory["specific_coverage_observations"], inventory["sources"])
    iv17_details = {
        "ancient_target_volume": "The conditional three-cubit depth is symbolic below an unknown ancient northern threshold; horizontal limits and bounded target volume are unavailable.",
        "ancient_datum": "Ancient northern threshold elevation and surface date remain null; Plan 5 supplies no threshold section/level.",
        "actual_reach": "Excavation concentrated in chamber centres beneath animal-activity remains. No northern-threshold target-volume excavation footprint or reached level is published in the inspected scope.",
        "phase_alignment": "Sion's Hellenistic use/concealment reconstruction does not independently date the wall, pillar cutting or northern threshold.",
        "disturbance_assessment": "Animal-activity remains are reported; preservation and disturbance of the specified ancient threshold target volume are not established.",
        "detection_method": "Excavation baskets 656.17/656.20 exist, but published reach and target-specific detection limits are unavailable.",
    }
    iv17_target = _unknown_target("coverage-target-iv17", "IV/17 northern-opening depth branch", ["coverage-sion-iv17", "coverage-iv17-phase", "coverage-iv17-assessment"], iv17_details, ["iv17-cave", "iv17-north-mouth"])
    iv17_target.update({
        "depth_branch": deepcopy(assessment["depth_branch"]),
        "published_exposure_region": "centres of northern and southern chambers",
        "excavation_footprint": None, "maximum_reached_depth_m": None,
        "ancient_threshold_elevation": phase["result"]["ancient_threshold_datum"],
        "field_record": deepcopy(phase["next_record"]),
        "field_file_inspected": assessment["next_record"]["field_file_inspected"],
        "find_records": deepcopy([item for item in phase["evidence"] if item.get("record")]),
        "repeated_coin_evidence_deduplicated": phase["result"]["repeated_coin_evidence_deduplicated"],
        "local_plan_is_excavation_footprint": False,
    })
    targets.append(iv17_target)

    # These are documentary lineage groups. A synthesis and its base report add
    # one source grouping, never multiple independent observations or confidence.
    campaigns: dict[str, dict[str, Any]] = {}
    for notice in notices:
        for campaign_id in notice["campaign_ids"]:
            campaigns.setdefault(campaign_id, {"id": campaign_id, "kind": "recorded_observation_lineage", "notice_ids": [], "source_ids": []})["notice_ids"].append(notice["id"])
    for source in sources:
        campaign_id = source.get("original_campaign")
        if campaign_id:
            campaigns.setdefault(campaign_id, {"id": campaign_id, "kind": "recorded_observation_lineage", "notice_ids": [], "source_ids": []})["source_ids"].append(source["id"])
    for campaign in campaigns.values():
        campaign["notice_ids"] = _unique(campaign["notice_ids"])
        campaign["source_ids"] = _unique(campaign["source_ids"])
        campaign["independent_campaign_increment"] = 0

    sectors = [{
        "id": sector["id"], "label": sector["label"],
        "notice_ids": sector["original_ids"], "scope_limit": sector["scope_limit"],
        "geometry": sector["polygon"], "crs": sector["crs"],
        "uniform_detection_coverage": sector["uniform_detection_coverage"],
        "source_ids": _source_ids(sector["citations"]),
        "eligible_denominator": None,
    } for sector in inventory["sectors"]]
    kinds = dict(Counter(notice["record_kind"] for notice in notices))
    observations = [
        {"id": "coverage-wadi-depth", "feature_id": "wadi-nueima-described-miqva", "property": "reported_depth",
         "value": {"value": original["reported_features"][0]["reported_depth_m"], "unit": "m", "datum": "source-reported depth; surveyed ancient floor datum unavailable"},
         "evidence_kind": "observed", "source_ids": ["coverage-wadi-original"], "exposure": "already_inspected", "reference_frame": "published local description; no surveyed benchmark"},
        {"id": "coverage-wadi-exposure", "feature_id": "wadi-nueima-described-miqva", "property": "reported_exposure_and_disturbance",
         "value": deepcopy(original["coverage"]), "evidence_kind": "observed", "source_ids": ["coverage-wadi-original"], "exposure": "already_inspected"},
        {"id": "coverage-wadi-function", "feature_id": "wadi-nueima-described-miqva", "property": "published_function_label",
         "value": original["reported_features"][0]["function_label"], "evidence_kind": "excavator_label", "source_ids": ["coverage-wadi-original"], "exposure": "already_inspected"},
        {"id": "coverage-iv17-excavation-region", "feature_id": "iv17-cave", "property": "published_excavation_region",
         "value": {"description": "centres of two chambers beneath animal-activity remains", "footprint": None, "reached_depth_m": None},
         "evidence_kind": "observed", "source_ids": ["coverage-sion-iv17"], "exposure": "already_inspected", "reference_frame": "source local cave description; Plan 5 is not an excavation-limit plan"},
        {"id": "coverage-iv17-threshold", "feature_id": "iv17-north-mouth", "property": "ancient_threshold_datum",
         "value": phase["result"]["ancient_threshold_datum"], "evidence_kind": "inference", "source_ids": ["coverage-iv17-phase", "coverage-iv17-assessment"], "exposure": "derived", "uncertainty": "unestablished"},
    ]

    def check(check_id: str, label: str, status: str, detail: str, refs: list[str], features: list[str] | None = None, value: Any = None) -> dict[str, Any]:
        return {"id": check_id, "label": label, "status": status, "detail": detail, "source_ids": refs, "feature_ids": features or [], "value": value}

    results = [
        {"id": "coverage-regional-scope", "title": "Jericho coverage roster",
         "claim": "The documentary inventory establishes a complete eligible regional basin inventory and detection coverage.", "status": "unknown",
         "checks": [
             check("coverage-roster-complete", "Selected-source roster", "info", "All 28 original documentary IDs occur once in twelve named sectors; twenty-one additional coverage obligations are retained.", ["coverage-inventory"], value={"notices": len(notices), "sectors": len(sectors), "obligations": len(obligations)}),
             check("coverage-identity", "Physical identity and phase states", "unknown", "J01 and J02 remain distinct earlier basins; J03 is their later joined state. Possible Area AC and Cypros crosswalks are retained unresolved. Notice counts cannot supply eligible-basin counts.", ["coverage-inventory"], value=kinds),
             check("coverage-landscape", "Regional boundary and denominator", "unknown", "No geographic search polygon, distinct eligible-basin denominator or uniform regional detection coverage is established.", ["coverage-inventory"], value=deepcopy(inventory["geographic_and_search_boundary"])),
             check("coverage-partial-reach", "Unreached and destroyed portions", "info", "A(C)90 floor was unreached in four soundings; A(C)161 floor reached only in a small northeast section. AC44's eastern half, two explicitly numbered lower Cypros cisterns and AC1's last metre of feeder have reported loss. No target-volume relation is established.", ["coverage-netzer2001", "coverage-meshel-amit1989"], value={"unique_coverage_observations": len(coverage_observations), "target_volume_relation": None}),
         ],
         "unknowns": ["Distinct eligible-basin denominator", "Regional geographic/survey footprint", "Phase-specific detection coverage", "Individual identity crosswalks", "Ancient target volumes and actual excavation reach"],
         "source_ids": ["coverage-inventory", "coverage-netzer2001", "coverage-meshel-amit1989"], "feature_ids": []},
        {"id": "coverage-wadi-supersession", "title": "Wadi original supersedes the pending-source record",
         "claim": "The inspected Wadi original supplies a bounded bath target and usable negative excavation.", "status": "unknown",
         "checks": [
             check("coverage-wadi-access", "Original report inspected", "info", "The supplied complete ESI5 report verifies printed pp. 110–111. Earlier pending/403 fields remain historical; original report acquisition is resolved.", ["coverage-wadi-original"]),
             check("coverage-wadi-cardinality", "One described bath; aggregate remains", "info", "One miqva is explicitly described; the western 4.5 × 8.0 m rectangle is a separate structure. Complete site bath count and field-locus crosswalk remain null.", ["coverage-wadi-original"], ["wadi-nueima-described-miqva"], value=deepcopy(original["cardinality"])),
             check("coverage-wadi-target", "Bath depth and target datum", "unknown", "Reported bath depth 1.3 m does not define an ancient deposit target. No bath plan/section, phase-controlled contact, benchmark or target-specific reach is supplied.", ["coverage-wadi-original"], ["wadi-nueima-described-miqva"]),
         ],
         "unknowns": ["Complete bath count/locus-state crosswalk", "Bath construction date", "Bath footprint and ancient datum", "Target reach after alluvium, flood exposure and illegal excavation", "Detection method/limits"],
         "source_ids": ["coverage-wadi-original", "coverage-rosapat2011"], "feature_ids": ["wadi-nueima-described-miqva"]},
        {"id": "coverage-iv17-target", "title": "IV/17 threshold coverage",
         "claim": "The published IV/17 excavation tested the ancient three-cubit northern-opening target.", "status": "unknown",
         "checks": [dict(gate, id="coverage-iv17-" + gate["id"]) for gate in iv17_target["gates"]],
         "unknowns": [GATE_LABELS[gate_id] for gate_id in iv17_target["missing_gate_ids"]],
         "source_ids": ["coverage-sion-iv17", "coverage-iv17-phase", "coverage-iv17-assessment"], "feature_ids": ["iv17-cave", "iv17-north-mouth"]},
    ]
    referenced = _source_ids(_locators(inventory))
    if set(referenced) - source_ids:
        raise ValueError("Unregistered source locators: " + ", ".join(sorted(set(referenced) - source_ids)))
    return {
        "id": "coverage", "number": 5, "title": "Investigation coverage",
        "summary": "Track what the published investigations reached, which states they exposed and which target-specific observations remain missing.",
        "scope": "Previously inspected Jericho J01–J28 documentary notices and twenty-one coverage obligations, current ESI5 Wadi original supersession, and IV/17 northern-threshold pilot. No parked geometry rerun or new acquisition.",
        "sources": sources,
        "features": [{"id": "wadi-nueima-described-miqva", "name": "Wadi Nu‘eima miqva described in ESI5", "kind": "reported_bath", "site": "Wadi Nu‘eima", "geometry": None}],
        "observations": observations, "states": [], "results": results,
        "data": {
            "summary": {"documentary_notices": len(notices), "named_sectors": len(sectors), "coverage_obligations": len(obligations), "record_kind_counts": kinds,
                        "distinct_eligible_basins": None, "regional_eligible_denominator": None, "inventory_detection_rate": None,
                        "negative_excavation_eligible_targets": sum(target["negative_excavation_eligible"] for target in targets),
                        "independent_campaign_increment": 0, "new_source_inspection_increment": 0},
            "regional_boundary": deepcopy(inventory["geographic_and_search_boundary"]),
            "sectors": sectors, "notices": notices, "obligations": obligations,
            "coverage_observations": coverage_observations,
            "identity_relations": deepcopy(inventory["identity_relations"]),
            "campaigns": list(campaigns.values()),
            "campaign_caution": "These are recorded observation/reporting lineages, not a verified count of discrete field campaigns. Unknown lineages remain unknown; derivative publications do not add independent corroboration.",
            "targets": targets,
            "gate_definitions": [{"id": gate_id, "label": label, "required_value_fields": list(REQUIRED_VALUE_FIELDS[gate_id])} for gate_id, label in GATE_LABELS.items()],
            "supersessions": [{"id": "coverage-wadi-original-current", "notice_id": "J23", "historical_source_state": "pending_original_in_retained_normalization_and_roster",
                              "current_source_state": "already_inspected_complete_report", "repo_path": WADI_PATH,
                              "supersedes_dependency_only": True, "aggregate_parent_retained": True,
                              "complete_site_bath_count": None, "source_ids": ["coverage-wadi-original"]}],
            "parked_tests_reopened": False,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    print(json.dumps(build(args.repo_root), ensure_ascii=False, indent=2))
