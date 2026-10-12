#!/usr/bin/env python3
"""Build qualitative source-role comparisons; never aggregate evidence scores."""
import argparse
import csv
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def csv_text(rows, fields):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def build():
    evidence, rules = load("evidence.json"), load("branch_rules.json")
    sources = {s["id"]: s for s in evidence["sources"]}
    fields = {
        "PLACE_IDENTIFIER": "ancient_place_id_status",
        "OBJECT_IDENTIFIER": "ancient_object_id_status",
        "OBJECT_COUNT": "counted_objects_status",
        "CONTENT_MEASURE": "content_measure_status",
        "LOCATOR_MESSAGE": "location_instruction_status",
    }
    rows = []
    for record in evidence["records"]:
        source = sources[record["source_id"]]
        for branch in rules["branches"]:
            role = branch["id"]
            gate_status = record[fields[role]]
            relation = "UNKNOWN"
            reason = "The available record leaves the required semantic relation unresolved."
            if gate_status == "PRESENT_IN_EDITION":
                relation = gate_status
                reason = "Electronic-edition line 2 explicitly links log and the numeral; commodity identity remains uncertain."
            elif record["id"].startswith("HERODIUM") and role in ("PLACE_IDENTIFIER", "OBJECT_IDENTIFIER"):
                relation = "COMPATIBLE"
                reason = "Naveh's two permitted noun senses allow this referent; numeral/function and associated referent mapping remain unresolved."
            elif record["id"] == "MASADA_302_GROUP":
                reason = "Wine/ten/tithe alternatives leave even numerical function unresolved."
            rows.append({
                "record_id": record["id"], "role": role,
                "relation_to_role": relation, "required_relation_status": gate_status,
                "assessment": "edition relation present" if gate_status == "PRESENT_IN_EDITION" else "not identifiable from available evidence",
                "reason": reason, "source_id": record["source_id"],
                "locator": record["locator"], "ancestry_id": source["ancestry_id"],
                "provenance_tier": source["provenance_tier"],
            })
    predictions = [{
        "branch": b["id"], "scope": b["scope"],
        "required_relations": "|".join(b["requires"]),
        "predicted_observation": b["prediction"],
        "success_criterion": b["success"], "failure_criterion": b["failure"],
        "limit": b["limit"], "exposure": "exploratory; existing sources exposed; no holdout registered",
    } for b in rules["branches"]]
    return {
        "comparison.csv": csv_text(rows, list(rows[0])),
        "predictions.csv": csv_text(predictions, list(predictions[0])),
    }


def validate():
    evidence, rules = load("evidence.json"), load("branch_rules.json")
    source_ids = {s["id"] for s in evidence["sources"]}
    assert len(source_ids) == len(evidence["sources"]), "duplicate source ID"
    gate_ids = {g["id"] for g in rules["gates"]}
    assert all(set(b["requires"]) <= gate_ids for b in rules["branches"])
    records = {r["id"]: r for r in evidence["records"]}
    assert len(records) == len(evidence["records"]), "duplicate record ID"
    for record in records.values():
        assert record["source_id"] in source_ids
        assert (HERE / record["numeric_quote_ref"].split("#")[0]).is_file(), "missing numerical extract"
        assert record["contents_status"] == "UNKNOWN", "tentative contents promoted"
        assert record["ancient_place_id_status"] == "UNKNOWN", "unmapped place promoted"
        assert record["ancient_object_id_status"] == "UNKNOWN", "unmapped object promoted"
    assert records["HERODIUM_A"]["number_value_as_editor"] == 40
    assert records["HERODIUM_B"]["number_value_as_editor"] == 35
    assert records["HERODIUM_A"]["published_lines"][1] == "[מהמט]מרים שבטין"
    assert "supralinear_dots" in records["HERODIUM_A"]["editorial_markers"]
    assert "lacuna" in records["HERODIUM_B"]["editorial_markers"]
    assert records["MASADA_302_GROUP"]["number_value_as_editor"] is None, "ambiguous yod converted"
    assert records["MASADA_595"]["content_measure_status"] == "PRESENT_IN_EDITION"
    assert all(g["herodium_status"] == "UNKNOWN" for g in rules["gates"])
    assert evidence["closed_tests"]["R12"].startswith("preserved")
    canonical = HERE.parents[1] / "sources/full_reads_2026-10-12/storage_language_audit/herodium_published_readings.json"
    if canonical.is_file():
        prior = json.loads(canonical.read_text(encoding="utf-8"))
        for suffix, inscription in zip(("A", "B"), prior["inscriptions"]):
            record = records["HERODIUM_" + suffix]
            assert record["published_lines"] == inscription["published_lines_plain"]
            assert record["editorial_markers"] == inscription["editorial_markers"]
            assert record["number_value_as_editor"] == inscription["number_value_as_author_suggests"]
    return canonical.is_file()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "check"))
    args = parser.parse_args()
    canonical_checked = validate()
    for name, content in build().items():
        if args.command == "build":
            (HERE / name).write_text(content, encoding="utf-8")
        else:
            assert (HERE / name).read_text(encoding="utf-8") == content, f"stale {name}"
    print(f"{args.command}: schema, uncertainty, source references and deterministic CSVs valid; canonical Herodium checked={canonical_checked}")


if __name__ == "__main__":
    main()
