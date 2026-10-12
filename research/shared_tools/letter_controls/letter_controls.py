"""Audit original-letter control readiness and score independent human responses.

Standard library only. Source records remain metadata; this module makes no image
inspection, glyph identity or new reading claim. Run from any working directory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = "897733283606988581155a3c1df0cd235cb7bea9"
MAPPING = "research/shared_tools/mapping_claims.json"
INDEX = "research/sources/usc_copper_scroll_images/index.csv"
MANIFESTS = ["research/sources/usc_copper_scroll_images/cuts_01_10_preview_manifest.csv",
             "research/sources/usc_copper_scroll_images/remaining_preview_manifest.csv"]
AUDIT = "registration/plate_check/original_photo_audit_2026-10-06.json"
PROTOCOL = "research/agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md"
LOCI = ["VII 11", "IX 7", "X 15", "X 16", "XII 10"]
GRADES = {"certain", "probable", "possible", "trace only", "illegible"}
DECISIONS = {"read", "abstain", "unknown"}
ABSTAIN = "[ABSTAIN]"
UNKNOWN = "[UNKNOWN]"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(value, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def csv_write(path, fields, records):
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def native_roi_valid(roi, width, height):
    return (isinstance(roi, list) and len(roi) == 4
            and all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in roi)
            and isinstance(width, int) and not isinstance(width, bool)
            and isinstance(height, int) and not isinstance(height, bool)
            and 0 <= roi[0] < roi[2] <= width and 0 <= roi[1] < roi[3] <= height)


def eligibility(item):
    """Qualification applies to real glyphs, never staging slots or edition labels.

    Project exposure determines confirmatory versus exploratory scope. Independent
    reader exposure is checked separately in scoring. Repeated images of one glyph
    must remain one item and one accuracy denominator.
    """
    gaps = []
    for condition, label in [
        (item.get("kind") == "control", "actual control glyph"),
        (item.get("substrate") == "original", "original metal substrate"),
        (item.get("source_bytes_verified") is True, "current source bytes verified"),
        (item.get("original_locus_authenticated") is True, "original locus authenticated independently of disputed glyph"),
        (bool(item.get("neighboring_original_hebrew")), "neighboring original Hebrew anchors"),
        (native_roi_valid(item.get("native_roi"), item.get("width_px"), item.get("height_px")), "bounded native glyph ROI"),
        (bool(item.get("glyph_id")), "physical glyph identity for deduplication"),
        (bool(item.get("observation_lineage")), "original observational lineage"),
        (item.get("reuse_authorized") is True, "authorized reviewer image use"),
        (item.get("damage_comparability_reviewed") is True, "recorded comparable damage/resolution stratum"),
        (item.get("local_comparator_inventory_complete") is True, "all legible local comparators inventoried under frozen selection rule"),
        (item.get("project_exposure_status") in ("exposed", "unused_verified"), "project exposure audit"),
    ]:
        if not condition:
            gaps.append(label)
    truth = item.get("truth") or {}
    if not (isinstance(truth.get("value"), str) and truth["value"].strip()
            and truth.get("basis") == "independent_original_reading"
            and truth.get("certain") is True and truth.get("original_anchor")
            and truth.get("established_before_scoring") is True
            and truth.get("independent_of_scoring_readers") is True):
        gaps.append("independently established certain truth with original anchor")
    eligible = not gaps
    return {"eligible_for_empirical_accuracy": eligible,
            "eligible_for_confirmatory_accuracy": eligible and item.get("project_exposure_status") == "unused_verified",
            "scope": ("confirmatory" if item.get("project_exposure_status") == "unused_verified" else "exploratory") if eligible else "blocked",
            "gaps": gaps}


def audit(root=ROOT):
    """Inspect source metadata and local file existence/hashes; never decode imagery."""
    root = Path(root)
    mapping = load(root / MAPPING)
    original_audit = load(root / AUDIT)
    acquired, acquisition_sources = {}, {}
    for path in MANIFESTS:
        for row in rows(root / path):
            if row["uc_identifier"] in acquired:
                raise ValueError("Duplicate acquisition identifier")
            acquired[row["uc_identifier"]] = row
            acquisition_sources[row["uc_identifier"]] = path
    historical = {row["uc_identifier"]: row for row in original_audit["source_frames"]}
    frames = []
    for catalog in rows(root / INDEX):
        if not catalog["item_type"].startswith("original"):
            continue
        identifier = catalog["uc_identifier"]
        acquisition = acquired.get(identifier, {})
        cut = int(catalog["cut"]) if catalog.get("cut") else None
        target_loci = [claim["locus"] for claim in mapping
                       if claim["locus"] in LOCI and cut in claim.get("candidate_cuts", [])]
        old = historical.get(identifier, {})
        relative = Path(acquisition.get("filename", "__missing__"))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Acquisition asset path escapes repository")
        path = root / relative
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("Acquisition asset symlink escapes repository")
        current_hash = digest(path) if path.is_file() else None
        hash_match = current_hash == acquisition.get("sha256") if current_hash else None
        gaps = ["authenticated local Hebrew anchors", "bounded native glyph ROI", "independent original glyph truth",
                "complete local comparator inventory", "damage/resolution comparability", "per-reader exposure audit",
                "independent qualified human readings"]
        if not hash_match:
            gaps.insert(0, "runtime original bytes not verified; sparse checkout absence is not a source-repository absence")
        frames.append({"view_id": identifier, "catalog_cut": cut, "substrate": "original",
                       "catalog_url": catalog.get("usc_link"), "target_loci": target_loci,
                       "catalog_source": INDEX, "acquisition_source": acquisition_sources.get(identifier),
                       "asset_filename_as_recorded": acquisition.get("filename"),
                       "source_sha256_as_recorded": acquisition.get("sha256"), "current_sha256": current_hash,
                       "current_byte_hash_matches_record": hash_match,
                       "runtime_asset_status": "materialized_hash_checked" if current_hash else "not_materialized_in_this_runtime",
                       "runtime_asset_limit": "This checkout omits image payloads; a local missing file supplies no scientific absence evidence.",
                       "width_px_as_recorded": acquisition.get("width_px") or None,
                       "height_px_as_recorded": acquisition.get("height_px") or None,
                       "prior_inspection_roles_as_recorded": old.get("inspection_roles"),
                       "project_exposure_status": "exposed" if old.get("inspection_roles") else "unused_status_unverified",
                       "exposure_limit": "Known catalogue/acquisition previews and contact sheets are exposed; a missing per-ID native ledger never establishes unused status.",
                       "original_roi": None, "neighboring_original_hebrew": None, "truth": None,
                       "empirical_control_status": "blocked", "gaps": gaps,
                       "rights_as_recorded": catalog.get("rights")})
    return {"schema_version": 1, "base_commit": BASE, "mode": "metadata_audit_only",
            "audit_generator_sha256": digest(HERE / "letter_controls.py"),
            "inputs": {p: digest(root / p) for p in [MAPPING, INDEX, *MANIFESTS, AUDIT, PROTOCOL]},
            "original_frame_candidates": frames, "locus_records": [x for x in mapping if x["locus"] in LOCI],
            "eligible_original_control_glyphs": [], "human_responses": [],
            "outcome": "not identifiable from available evidence",
            "claim": "Independent human accuracy on authenticated, comparably damaged original Hebrew glyphs",
            "limits": ["No source image decoded or inspected in this audit.",
                       "An original-frame catalogue identity supplies neither line authentication nor a letter truth.",
                       "An exposed observation remains exposed after downloading or rescanning it.",
                       "No local ROI or securely anchored original-letter truth appears in the imported target mapping."]}


def selection_slots(data):
    """All loci get the same unresolved control-pool opportunity; glyphs await audit."""
    items = []
    for locus in LOCI:
        views = [f for f in data["original_frame_candidates"] if locus in f["target_loci"]]
        claim = next(c for c in data["locus_records"] if c["locus"] == locus)
        for role in ("target", "local_control_pool"):
            items.append({"internal_id": locus.replace(" ", "_") + "_" + role,
                          "kind": role, "locus": locus, "candidate_views": views,
                          "mapping_source": MAPPING, "mapping_status": claim["status"],
                          "glyph_id": None, "native_roi": None, "truth": None,
                          "slot_is_observed_glyph": False,
                          "selection_rule": "Enumerate every legible original glyph in the authenticated target context, preserving all views per physical glyph; record damage/resolution strata before selecting or revealing answers.",
                          "component_groups": ["ב/כ", "נ/צ/י/ו and ligatures", "ה/ח/ת", "additional strokes/signs and intact readable absence"] if locus == "XII 10" else None,
                          "status": "metadata_slot_requires_original_registration_and_control_truth"})
    return items


def packet(data, destination, seed=20261009):
    destination = Path(destination)
    if destination.exists():
        raise ValueError("Use a new packet directory; preserve prior packets and locked responses")
    reviewer = destination / "reviewer"
    coordinator = destination / "coordinator"
    reviewer.mkdir(parents=True)
    coordinator.mkdir()
    slots = selection_slots(data)
    random.Random(seed).shuffle(slots)
    public, key = [], []
    for n, item in enumerate(slots, 1):
        code = f"L{n:03d}"
        key.append({"code": code, **item})
        public.append({"code": code, "images": [], "native_roi": None,
                       "stage1_task": "Record visible characters, native coordinates, strokes, gaps, damage and per-position confidence before opening Stage 2.",
                       "status": "undispatched_metadata_slot_no_image"})
    dump(public, reviewer / "items.json")
    dump([{"code": i["code"], "reader_id": None, "transcription": None,
           "positions": [], "uncountable_gaps": [], "recognition": None,
           "prior_exposure": None, "locked_at_utc": None,
           "positions_format": {"native_roi": None, "label": None, "decision": "read|abstain|unknown",
                                "grade": "certain|probable|possible|trace only|illegible", "evidence": None}}
          for i in public], reviewer / "stage1_response_template.json")
    csv_write(reviewer / "stage1_responses.csv", ["code", "reader_id", "transcription", "native_coordinates", "visible_strokes", "damage", "grade", "recognition", "prior_exposure", "locked_at_utc"],
              [{"code": i["code"]} for i in public])
    questions = []
    for item in key:
        if item["locus"] == "XII 10" and item["kind"] == "target":
            questions.append({"code": item["code"], "source": PROTOCOL,
                              "questions": ["Box-letter identity: ב, כ or other; cite native frame and feature.",
                                            "נ, צ, or י/ו+נ including a ligature; distinguish incised mark from independent sign.",
                                            "Final letter: ה, ח, ת or other; record cut damage and conflicting views.",
                                            "Additional signs or cancellation marks before the next word; grade readable absence separately from a damaged gap."]})
        else:
            questions.append({"code": item["code"], "questions": [],
                              "status": "targeted character positions await authenticated native ROI and final manifest"})
    dump({"status": "coordinator_release_after_stage1_lock_only", "questions": questions}, coordinator / "stage2_release.json")
    dump({"status": "exploratory_selection_plan_pending_original_registration", "scope": LOCI,
          "source_protocol": PROTOCOL,
          "selection": ["Authenticate each native frame and line from neighboring original Hebrew plus physical anchors independently of the disputed word.",
                        "Inventory every legible local comparator once per physical glyph, keeping all original captures as views of that item.",
                        "Record each glyph's native ROI, independent truth anchor, and incision/damage/resolution class before reader release.",
                        "Include all inventoried comparable letters under the same rule; record every exclusion and reason. Never select only favorable letterforms.",
                        "Keep intact, cut-damaged, folded/corroded, glare/shadow and resolution-limited strata separate; report accuracy by stratum when a real sample exists.",
                        "Register the final finite manifest, truth-key hash, selection exclusions and protocol hash before the future readings.",
                        "Use project-exposed original controls only for exploratory calibration with independently unexposed readers; verify an unused observational lineage before a confirmatory claim."],
          "truth_rule": "A secure original-image anchor and independent epigraphic adjudication precede scorer responses. An edition label, repaired replica or two agreeing guesses cannot supply control truth.",
          "reader_rule": "Two independent experienced human readers; preserve initial locked answers and per-item recognition/exposure. AI results exercise software only.",
          "grouping_rule": "Copies/rescans/lighting variants of one capture and multiple views of one physical glyph do not add accuracy denominators or independent observations.",
          "decisive_gate": "The frozen XII10 protocol controls actual letter verdicts; calibration adds no numerical threshold or automatic rejection."}, coordinator / "control_selection_plan.json")
    dump(key, coordinator / "source_key.json")
    dump({"seed": seed, "seed_role": "reproducible exploratory staging order; register a fresh immutable final manifest before future evidence release",
          "source_inputs": data["inputs"], "source_key_sha256": digest(coordinator / "source_key.json"),
          "manifest_sha256": digest(reviewer / "items.json"), "dispatch": "not_sent", "ready": False,
          "gates": ["authorized original frames with current hashes", "authenticated locus and bounded native ROIs",
                    "independently anchored control truths", "complete comparator inventory and comparability audit",
                    "item-level lineage and project/per-reader exposure audit", "two independent qualified human readers",
                    "locked Stage 1 before targeted Stage 2", "frozen final packet and protocol hashes before release"],
          "control_glyphs_available": [], "accuracy_obtained": False}, coordinator / "readiness.json")
    gaps = [{"code": i["code"], "locus": i["locus"], "role": i["kind"],
             "candidate_views": "|".join(v["view_id"] for v in i["candidate_views"]),
             "missing": "original line/glyph registration; ROI; comparability; control truth; exposure audit; independent readers"} for i in key]
    csv_write(coordinator / "item_gaps.csv", ["code", "locus", "role", "candidate_views", "missing"], gaps)
    (reviewer / "INSTRUCTIONS.md").write_text(
        "# Independent reading packet — staging only\n\n"
        "This folder currently contains empty image slots. It supplies no reading task until the coordinator passes the readiness gates.\n\n"
        "Receive only this reviewer folder. Work independently; use the supplied images and retain their unadjusted native view. "
        "Record a free transcription and visible damage before targeted questions. Mark an unreadable position `?` and an uncountable gap `[...]`. "
        "Use certain, probable, possible, trace only or illegible for each position. Identify cracks, glare and uncertain grooves. "
        "Record any recognition or prior exposure per item. Lock Stage 1 and its checksum/timestamp before receiving Stage 2; "
        "preserve later revisions alongside the original response. Record abstain and unknown explicitly.\n\n"
        "The source key, proposed readings, sites and truth labels stay with the coordinator. Source keys in the public research repository "
        "are preparation records; the coordinator must deliver a restricted reviewer-only package before testing blindness.\n",
        encoding="utf-8")
    return {"status": "prepared_metadata_only", "dispatch": "not_sent", "directory": str(destination)}


def score(items, responses, readers, mode="empirical"):
    """One first locked answer per reader/glyph; abstentions retain denominator.

    Stage 2 revisions remain outside calibration scores. Unknown truth never creates
    an accuracy denominator. Human qualifications and independence are explicit data.
    Synthetic mode exercises arithmetic only, with no empirical-reading claim.
    """
    if mode not in ("empirical", "synthetic_software_pilot"):
        raise ValueError("Unrecognized scoring mode")
    by_code = {i["code"]: i for i in items}
    if len(by_code) != len(items):
        raise ValueError("Duplicate item code")
    glyphs = [i.get("glyph_id") for i in items if i.get("kind") == "control" and i.get("glyph_id")]
    if len(glyphs) != len(set(glyphs)):
        raise ValueError("Multiple codes represent the same physical glyph; group its views under one code")
    by_reader = {r["reader_id"]: r for r in readers}
    if len(by_reader) != len(readers):
        raise ValueError("Duplicate reader identity")
    if mode == "empirical" and any(x.get("synthetic") is True for x in [*items, *readers]):
        raise ValueError("Synthetic items or readers cannot enter empirical accuracy")
    seen, validated = set(), []
    for response in responses:
        code, reader_id = response.get("code"), response.get("reader_id")
        if code not in by_code or reader_id not in by_reader:
            raise ValueError("Response references unknown item or reader")
        identity = (code, reader_id)
        if identity in seen:
            raise ValueError("Duplicate initial locked response; store revisions separately")
        seen.add(identity)
        if response.get("decision") not in DECISIONS or response.get("grade") not in GRADES:
            raise ValueError("Invalid decision or grade")
        label = response.get("label")
        if response["decision"] == "read" and not (isinstance(label, str) and label.strip()):
            raise ValueError("A read requires an explicit label")
        if response["decision"] != "read" and label not in (None, ""):
            raise ValueError("Abstain/unknown must not conceal a label")
        if response.get("stage") != 1 or response.get("locked_before_stage2") is not True or not response.get("locked_at_utc"):
            raise ValueError("Only initial Stage 1 answers locked before Stage 2 can be scored")
        if mode == "empirical" and response.get("synthetic") is True:
            raise ValueError("Synthetic answers cannot enter empirical accuracy")
        validated.append(response)
    qualified = {i["code"]: eligibility(i) for i in items}
    results = []
    for reader_id, reader in sorted(by_reader.items()):
        selected = [r for r in validated if r["reader_id"] == reader_id]
        matrix, excluded, targets, known = Counter(), [], [], []
        independent = reader.get("independent_human") is True and reader.get("epigraphic_experience_recorded") is True
        for response in selected:
            item = by_code[response["code"]]
            if item.get("kind") != "control":
                targets.append(response)
                continue
            reasons = list(qualified[response["code"]]["gaps"])
            if not independent:
                reasons.append("independent qualified human reader")
            if response.get("prior_exposure_audited") is not True:
                reasons.append("reader exposure audit")
            if response.get("recognized") is not False or response.get("prior_exposure") is not False:
                reasons.append("recognized or previously exposed or exposure unknown")
            if reasons:
                excluded.append({"code": response["code"], "reasons": reasons, "response": response})
                continue
            truth = item["truth"]["value"]
            predicted = response["label"] if response["decision"] == "read" else ABSTAIN if response["decision"] == "abstain" else UNKNOWN
            matrix[(truth, predicted)] += 1
            known.append({"code": response["code"], "truth": truth, "prediction": predicted,
                          "grade": response["grade"], "scope": qualified[response["code"]]["scope"]})
        denominator = len(known)
        answered = sum(x["prediction"] not in (ABSTAIN, UNKNOWN) for x in known)
        correct = sum(x["truth"] == x["prediction"] for x in known)
        missing = [code for code, q in qualified.items() if q["eligible_for_empirical_accuracy"] and (code, reader_id) not in seen]
        presented = sum(q["eligible_for_empirical_accuracy"] for q in qualified.values())
        returned = sum(qualified[r["code"]]["eligible_for_empirical_accuracy"] for r in selected)
        results.append({"reader_id": reader_id, "eligible_presented_controls": presented,
                        "scorable_locked_responses": denominator, "missing_responses": missing,
                        "correct": correct, "answered": answered,
                        "abstentions": sum(x["prediction"] == ABSTAIN for x in known),
                        "unknown_answers": sum(x["prediction"] == UNKNOWN for x in known),
                        "accuracy_including_abstentions": correct / denominator if denominator else None,
                        "accuracy_when_answered": correct / answered if answered else None,
                        "response_completeness": returned / presented if presented else None,
                        "scorable_fraction_of_presented_controls": denominator / presented if presented else None,
                        "confusion_matrix": [{"truth": a, "answer": b, "count": n} for (a, b), n in sorted(matrix.items())],
                        "scored_items": known, "excluded_control_responses": excluded,
                        "unscored_target_responses": targets})
    disagreements = []
    for left, right in itertools.combinations(sorted(by_reader), 2):
        lefts = {r["code"]: r for r in validated if r["reader_id"] == left}
        rights = {r["code"]: r for r in validated if r["reader_id"] == right}
        for code in sorted(lefts.keys() & rights.keys()):
            a, b = lefts[code], rights[code]
            same = (a["decision"], a.get("label")) == (b["decision"], b.get("label"))
            independence = (by_reader[left].get("independent_human") is True and by_reader[right].get("independent_human") is True
                            and left in by_reader[right].get("independent_of", []) and right in by_reader[left].get("independent_of", []))
            disagreements.append({"code": code, "readers": [left, right], "same_answer": same,
                                  "independence_documented": independence,
                                  "left": {k: a.get(k) for k in ("decision", "label", "grade", "recognized")},
                                  "right": {k: b.get(k) for k in ("decision", "label", "grade", "recognized")},
                                  "reconciliation": "independent answers preserved; no adjudicated replacement"})
    empirical_obtained = mode == "empirical" and any(r["scorable_locked_responses"] for r in results)
    return {"mode": mode, "empirical_accuracy_obtained": empirical_obtained,
            "outcome": "empirical descriptive accuracy computed" if empirical_obtained else "software pilot only" if mode == "synthetic_software_pilot" else "not identifiable from available evidence",
            "claim": "Independent human accuracy on original glyphs" if mode == "empirical" else "Software arithmetic on explicit synthetic response fixtures",
            "control_qualification": qualified, "reader_results": results,
            "independent_reader_comparisons": disagreements,
            "limits": ["Pairwise agreement is not an independent truth criterion.",
                       "Scores exclude targets, unresolved truths, recognition and unverified exposure; exclusions remain visible.",
                       "Accuracy including abstentions uses scorable returned controls; missing responses are reported separately.",
                       "No control-accuracy threshold overrides the frozen XII10 decisive-letter gates."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare"); p.add_argument("--root", type=Path, default=ROOT); p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("score"); p.add_argument("--input", type=Path, required=True); p.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        args.output.mkdir(parents=True, exist_ok=True)
        data = audit(args.root)
        dump(data, args.output / "control_eligibility_audit.json")
        result = packet(data, args.output / "packet")
    else:
        data = load(args.input)
        result = score(data["items"], data["responses"], data["readers"], data.get("mode", "empirical"))
        dump(result, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
