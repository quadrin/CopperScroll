#!/usr/bin/env python3
"""Merge reviewed search targets into schema-compatible, exploratory entry-60 records."""
import copy
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WD = HERE.parent
REVIEW = WD.parents[1]
OLD = REVIEW / "wave1/T03_T04_registry/registry.json"
PROTOCOL = "../../wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md"

def main():
    old = json.loads(OLD.read_text())
    originals = {r["id"]: r for r in old["records"] if r["entry"] == "60"}
    with (WD / "registry_v1_entry60.csv").open() as f:
        targets = [r for r in csv.DictReader(f) if r["target_id"].startswith("P60-T")]
    records = []
    for t in targets:
        tid = t["target_id"].split()[0]
        r = copy.deepcopy(originals.get(tid, originals["P60-T1"]))
        previous = originals.get(tid)
        r.update(id=tid, registry_version="0.2-exploratory-2026-10-08", drafted="2026-10-08",
                 status="exploratory specification; confirmation blocked until unused evidence and commit audit",
                 rank=int(t["new_rank"]), branch=t["target"], site_name=t["target"],
                 feature_detail=t["reasons"], inference=dict(label="INFERENCE",
                 text="Desk-work priority inherited from W2B; no calibrated target probability or site confirmation.",
                 confidence="low"), sources=(previous or {}).get("sources", []) + [
                 "W2B REPORT.md; registry_v1_entry60.csv",
                 "../../followup/A_jericho_spring_reservoir.md",
                 "../../followup/B_kh_el_marjama.md",
                 "../../followup/C_kenyon_jericho_II_and_kh_yanun.md",
                 "XII10 image-reading protocol"],
                 rank_scores=None, model_place_id=t["place_id"],
                 order_BF_context="Historical W2B conditional model comparison; not probability of identification.",
                 historical_W2B_target_heuristic=t["historical_W2B_P_target_heuristic"],
                 current_target_probability=None, reading_protocol=PROTOCOL,
                 claim_result="not identifiable from available evidence",
                 unused_prediction_available=None, unseen_prediction_registered=False,
                 prior_exposure="Known editions, project plates/readings, W2B model results, Kenyon II, Highlands, "
                 "Dorrell/Warren and Zohar summaries informed selection. No new Manchester master was inspected "
                 "for this update. Download recency alone cannot establish an unused observation.",
                 next_desk_test=t["next_desk_test"],
                 previous_record_sha256=previous["record_sha256"] if previous else None)
        # Keep project confidence/status and old gazetteer coordinates unchanged.
        # Added model proposals have no project gazetteer identity; coordinate model proxies are not feature positions.
        if previous is None:
            r.update(place_id=None, project_candidate_status=None, anchor_lat=None, anchor_lon=None,
                     anchor_precision="unlocated feature; no surveyed coordinate asserted",
                     anchor_note="Model coordinate/proposal is in inputs/places_v1.csv; it is not a registered pit mouth.",
                     evidence=[], reading_editions=["Lefkovits 2000 pp. 425-426; Zissu 2001 p. 149"] if tid == "P60-T8"
                     else ["Lurie 1963; Bar-Adon 1972 site 83, via Zissu 2001 p. 148"])
        r["reading_assumed"] = (
            "RB-L only: the pit is AT Janoaḥ, conditionally identified with Kh. Yanun or Yanun village; "
            "north of Koḥlit remains a separate relation. The unknown Koḥlit anchor is not used as the pit coordinate."
            if tid == "P60-T8" else
            "RB-M (Milik, north-facing opening), RB-P (Puech, concealed opening without required azimuth), "
            "and separately RB-B ('buried', no required tombs). RB-L is excluded here and routed to P60-T8.")
        r["reading_status"] = "Edition alternatives unresolved; follow the image-reading protocol before new scans."
        r["measures"] = []  # Entry 60 provides no distance/depth measure.
        r["confirm"] = (
            "Conditional feature relation only: identify and independently date an accessible pit/shaft and its "
            "mouth/tomb relation within the stated period, applying every retained reading to every eligible alternative. "
            "RB-M requires a north-facing side opening; RB-P requires evidence of concealment; RB-B requires no tomb "
            "landmark. A vertical opening has no facing azimuth without a defined entrance. For RB-L use the Janoaḥ "
            "target and separately test the north-of-Koḥlit relation. Legacy 315-045 degrees and <=5 m proximity are "
            "exploratory operational choices, not text-derived tolerances. Register field datums and finite tolerances "
            "before any reserved field observation. Identification support additionally requires a complete registered "
            "control inventory, discrimination and a demonstrably unused prediction. All remain pending.")
        r["miss"] = (
            "A securely later construction rejects only the specified feature/period branch. Contradiction of all "
            "retained relations can reject that feature branch. Report silence, undated shafts and partial coverage "
            "remain unknown. Target-wide rejection requires bounded ancient target coverage, every eligible alternative "
            "and detection limits; these are not supplied. An empty pit alone does not reject a buried document.")
        r["inconclusive"] = (
            "Current result: not identifiable from available evidence. No surveyed and dated pit-mouth/tomb-mouth "
            "relation, complete regional denominator or unused field prediction is established. New images may settle "
            "a reading branch only; they cannot independently confirm a pit or Koḥlit identification.")
        r["scorability"] = "exploratory desk evidence; field confirmation not registered"
        r["orientation_constraint"] = "north of an explicitly defined Koḥlit anchor under RB-M/P/B; RB-L pit at Janoaḥ"
        r["location_constraint"] = t["target"] + "; feature position and target coverage unknown"
        if tid == "P60-T1":
            r["evidence"] += [
                dict(label="EVIDENCE", claim="Kenyon II records Roman shaft reuse and northern pits/cistern; a "
                     "joint pit-mouth/tomb-mouth relation is not demonstrated.", source="Kenyon II pp. 276-277, 516, "
                     "539-544, followup/C; III (1981) pp. 173-174 remains unread."),
                dict(label="EVIDENCE", claim="The existing reservoir was built in 1898; the curved spring-house "
                     "wall has a tentative later ancient date.", source="Dorrell 1993 pp. 111-112; followup/A")]
            # Supersede the old statement 'no pit reported north of tell'.
            r["evidence"] = [e for e in r["evidence"] if "no pit is reported" not in e["claim"]]
        if tid == "P60-T3":
            r["evidence"] = [
                dict(label="EVIDENCE", claim="The northern shaft fields are Bronze Age; Kh. Samiya Roman tombs "
                     "are S/SE. Kallai's pool is unlocated. No joint early northern pit/tomb relation is shown.",
                     source="followup/B and C; Highlands pp. 732-735; Zissu pp. 146-155."),
                dict(label="EVIDENCE", claim="HA 76 p. 19 reports the 1979-80 settlement excavation without a "
                     "pool/reservoir/church/pipe or Roman-phase observation.", source="Zohar, HA 76 (1981) p. 19; "
                     "user-supplied original checked 8 October UTC, followup/B.")]
        if tid == "P60-T8":
            r["feature_type"] = "pit/shaft at Janoaḥ under RB-L; tomb relation remains conditional"
            r["evidence"] = [dict(label="EVIDENCE", claim="No pit/cistern/tomb is described for Kh. Yanun; "
                "Roman sherds are undivided. Burial caves are noted near Yanun village.",
                source="Highlands pp. 821-822, 828-831; followup/C.")]
        if tid == "P60-T9":
            r["feature_type"] = "unlocated pit north of the Tell Muhalhil proposal"
        for k in ("outcome", "outcome_level", "scored_report", "scored_by", "scored_date"):
            r[k] = None
        r.pop("record_sha256", None)
        h = {k: v for k, v in r.items() if not k.startswith("outcome") and not k.startswith("scored_")}
        r["record_sha256"] = hashlib.sha256(json.dumps(h, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        records.append(r)
    result = dict(meta=dict(version="0.2-exploratory-2026-10-08", source_ref="83230367bf6a592c35f8f8e060e744e3b5ff5604",
        supersedes_entry60_only="../../wave1/T03_T04_registry/registry.json",
        scope="Nine exploratory targets; historical records and all other entries unchanged.",
        image_protocol=PROTOCOL, image_protocol_commit="fd3f334ea2a40c0f8e99921ef663f8b126112fe1",
        image_protocol_sha256="0e19467c618f80438c12445b7380f77f5c59b7fe241da9c80878601e2e26a2c5", public_timestamp="Commit SHA must be recorded before any reserved scan is opened."),
        records=records)
    (WD / "registry_v2_entry60.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print("wrote", len(records), "records")

if __name__ == "__main__":
    main()
