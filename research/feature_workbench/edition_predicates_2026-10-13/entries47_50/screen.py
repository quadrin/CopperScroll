"""Reproduce a bounded exploratory E47/E50 screen from held coded records.

No text search absence becomes archaeological absence. No manuscript claim.
Run with Python 3; outputs are relative to this script's directory.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]


def status(observations, required):
    selected = {key: observations.get(key, "unknown") for key in required}
    if "contradicted" in selected.values():
        return "reported_form_contradiction_only"
    if set(selected.values()) == {"supported"}:
        return "limited_landmark_fit"
    return "not_identifiable_from_available_evidence"


def main():
    inputs = REPO / "research" / "regional" / "water_systems" / "water.csv"
    records = list(csv.DictReader(inputs.open()))
    registry = json.loads((ROOT / "registry.json").read_text())
    observations = []
    branch_rows = []
    for row in records:
        # Inventory eligibility concerns the described feature, never its whole site.
        main_eligible = row["type"] in ("reservoir_pool", "basin_tank")
        sensitivity_eligible = row["type"] == "cistern"
        codes = {p: "unknown" for b in registry["branches"] for p in b["required"]}
        if main_eligible:
            codes["basin"] = "supported"
        # A field labelled 'four_sides' derives from generic rectangular/square
        # descriptions. It is only a form inference, not four excavated corners.
        if row["shape"] == "four_sides" and (main_eligible or sensitivity_eligible):
            codes["four_corners"] = "supported"
        # 'not_four_sides' also contains unstated geometries; require an explicit
        # circle/round observation in the retained description before failing.
        if ("circular" in row["name"].lower() or "round" in row["name"].lower()) and (main_eligible or sensitivity_eligible):
            codes["four_corners"] = "contradicted"
        if row["id"] == "LIT-MAZ-SOL-UPPER":
            codes["upper_relation"] = "supported"
        # Native Damati p299 describes a pool IN the upper garden, not an
        # independently established upper/lower pair of pools.
        if row["id"] == "LIT-MAZ-SALEH-SPR":
            codes["spring_underground_relation"] = "supported"
        if row["site_key"] == "jer_siloam" and main_eligible:
            codes["siloam_association"] = "supported"
        # Existing date codes can concern site occupation or a reported use
        # configuration. They do not establish the construction phase of this
        # physical feature or exclude earlier fabric/reuse.
        coded_configuration_phase = "outside_window" if row["date_code"] == "out" else row["date_code"]
        # No phase-controlled feature/contact observation was independently
        # verified in this lane. All physical contemporaneity remains unknown.
        relevant = main_eligible or sensitivity_eligible
        observations.append({
            "id": row["id"], "name": row["name"], "type": row["type"],
            "eligibility": "main_pool_or_tank" if main_eligible else "cistern_sensitivity" if sensitivity_eligible else "context_only",
            "source": row["source"], "locator": row["locator"],
            "date_code": row["date_code"], "period_as_given": row["period_as_given"],
            "dup_of": row["dup_of"], "superseded_by": row["superseded_by"],
            "group_id": row["group_id"], "source_span_sha256": row["span_sha256"],
            "shape_basis": row["shape"], "notes": row["notes"], **codes,
            "earlier_fabric_reuse": "unknown",
            "coded_reported_configuration_phase": coded_configuration_phase,
            "reported_form_scope": "present described feature only; ancient form unknown",
        })
        for branch in registry["branches"]:
            if not relevant:
                verdict = "context_only"
            elif "court" in branch["required"]:
                # Water types cannot adjudicate a court at the same site.
                verdict = "courtyard_coverage_missing"
            else:
                verdict = status(codes, branch["required"])
            branch_rows.append({
                "id": row["id"], "branch": branch["id"], "eligibility": observations[-1]["eligibility"],
                "status": verdict,
                "supported": ";".join(p for p in branch["required"] if codes[p] == "supported"),
                "contradicted": ";".join(p for p in branch["required"] if codes[p] == "contradicted"),
                "unknown": ";".join(p for p in branch["required"] if codes[p] == "unknown"),
                "coded_reported_configuration_phase": coded_configuration_phase,
                "contradiction_scope": "reported form only; no ancient phase assigned" if codes["four_corners"] == "contradicted" and "four_corners" in branch["required"] else "",
            })
    for filename, rows in [("observations.csv", observations), ("branch_status.csv", branch_rows)]:
        with (ROOT / filename).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    summary = {
        "mode": "exploratory_existing_coded_records",
        "decision": "not identifiable from available evidence",
        "claim": "E47/E50 landmark identity within the held coded water inventory",
        "regional_rarity_denominator": None,
        "unseen_prediction": None,
        "hashes": {str(inputs.relative_to(REPO)): hashlib.sha256(inputs.read_bytes()).hexdigest(),
                   "registry.json": hashlib.sha256((ROOT / "registry.json").read_bytes()).hexdigest()},
        "row_counts_are_coverage_not_outcomes": True,
        "eligibility": dict(Counter(r["eligibility"] for r in observations)),
        "branches": {b["id"]: dict(Counter(r["status"] for r in branch_rows if r["branch"] == b["id"])) for b in registry["branches"]},
        "critical_unrecorded_fields": ["black_stone", "stone_at_entrance", "stone_to_entrance_2c", "stone_from_origin_2c", "stone_two_clamps", "stone_two_coins", "court", "inner_relation", "zadok_tomb_association"],
        "limits": ["Coded rows omit nearly all original prose; quote fields mostly blank.",
                   "Scope excludes east-of-Jordan Zered and lacks courtyard inventory.",
                   "Inherited date codes are diagnostics only. No inherited date-out value generates an archaeological exclusion or a contemporaneous_phase contradiction.",
                   "Explicit circular/round descriptions concern reported form only; ancient geometry and reuse remain unknown.",
                   "No source-level absence or negative excavation observation.",
                   "A whole site remains open after one recorded feature fails."],
    }
    (ROOT / "result.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
