"""Validate the salvage-records tables and write descriptive counts.

Run from the repository root or anywhere:
    python3 -I research/history/salvage_records/summarize.py
It writes summary.json next to this file. Counts are descriptive only (see PLAN.md).
"""
import csv
import json
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PLACES = os.path.join(REPO, "research", "agent_review_2026-10-07", "wave2", "W2B_model_v1", "inputs", "places_v1.csv")

CATALOGUE_COLS = [
    "cat_id", "reference", "composed", "event_date", "place_named", "place_id",
    "objects", "action", "agent", "kind", "kind_note", "bears_on",
    "s_removed", "s_unrecovered", "s_literary", "scenario_reason",
    "dependency_group", "translation", "quote", "quote_locator",
    "source_ids", "access", "notes",
]
SEARCH_COLS = [
    "search_id", "place_id", "place_match", "entry_ids", "record", "who",
    "when_start", "when_end", "when_text", "purpose", "looked_at", "where_name",
    "coords", "coord_crs", "method", "extent_depth", "found", "result", "kind",
    "documentation", "source_ids", "access", "coverage_notes", "notes",
]
SOURCE_COLS = ["source_id", "citation", "url", "access", "scope_read", "licence_note", "notes"]
FILE_COLS = ["source_id", "file", "url", "bytes", "sha256", "retrieved"]

KINDS = {"EVIDENCE", "TRADITION", "CLAIM"}
SCEN = {"supports", "weakens", "neutral"}
ACTIONS = {"hidden", "recovered", "handed_over", "removed", "destroyed", "returned", "transferred",
           "claimed_buried", "searched_not_found", "search_aborted", "hidden_people"}
CAT_ACCESS = {"read", "via_repo", "via_secondary"}
RESULTS = {"negative", "other_finds", "claimed_find", "unknown"}
PURPOSES = {"scroll_deposit_search", "scroll_motivated", "scroll_find_site", "manuscript_survey",
            "excavation_of_named_place", "claim_only", "unknown"}
MATCH = {"exact", "near", "none"}
SEARCH_ACCESS = {"read", "read_owner_copy", "via_repo"}
SOURCE_ACCESS = {"read", "read_owner_copy", "via_repo", "via_secondary", "not_accessed", "failed"}
MAX_QUOTE_WORDS = 12
DATE_RE = re.compile(r"^$|^\d{4}(-\d{2}(-\d{2})?)?$")


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def place_ids():
    with open(PLACES, encoding="utf-8", newline="") as f:
        return {r["place_id"] for r in csv.DictReader(f)}


def word_count(s):
    return len(s.split())


def validate():
    errors = []
    places = place_ids()
    s_cols, sources = read("sources.csv")
    f_cols, files = read("source_files.csv")
    c_cols, cat = read("catalogue.csv")
    q_cols, srch = read("searches.csv")
    if s_cols != SOURCE_COLS:
        errors.append("sources.csv columns")
    if f_cols != FILE_COLS:
        errors.append("source_files.csv columns")
    if c_cols != CATALOGUE_COLS:
        errors.append("catalogue.csv columns")
    if q_cols != SEARCH_COLS:
        errors.append("searches.csv columns")
    sids = [s["source_id"] for s in sources]
    if len(sids) != len(set(sids)):
        errors.append("duplicate source_id")
    known = set(sids)
    for s in sources:
        if s["access"] not in SOURCE_ACCESS:
            errors.append("source access " + s["source_id"])
        if not s["citation"] or not s["url"]:
            errors.append("source citation/url " + s["source_id"])
    for r in files:
        if r["source_id"] not in known:
            errors.append("file source " + r["file"])
        if not re.fullmatch(r"[0-9a-f]{64}", r["sha256"]):
            errors.append("sha " + r["file"])
    for r in cat:
        rid = r["cat_id"]
        if r["kind"] not in KINDS:
            errors.append(rid + " kind")
        for c in ("s_removed", "s_unrecovered", "s_literary"):
            if r[c] not in SCEN:
                errors.append(rid + " " + c)
        for a in r["action"].split(";"):
            if a not in ACTIONS:
                errors.append(rid + " action " + a)
        if r["access"] not in CAT_ACCESS:
            errors.append(rid + " access")
        if r["place_id"] and r["place_id"] not in places:
            errors.append(rid + " place_id")
        if word_count(r["quote"]) > MAX_QUOTE_WORDS:
            errors.append(rid + " quote too long")
        ids = [x for x in r["source_ids"].split(";") if x]
        if not ids or any(x not in known for x in ids):
            errors.append(rid + " source_ids")
    for r in srch:
        rid = r["search_id"]
        if r["result"] not in RESULTS:
            errors.append(rid + " result")
        if r["purpose"] not in PURPOSES:
            errors.append(rid + " purpose")
        if r["kind"] not in KINDS:
            errors.append(rid + " kind")
        if r["place_match"] not in MATCH:
            errors.append(rid + " place_match")
        if (r["place_id"] == "") != (r["place_match"] == "none"):
            errors.append(rid + " place_id/place_match")
        if r["place_id"] and r["place_id"] not in places:
            errors.append(rid + " place_id")
        if r["access"] not in SEARCH_ACCESS:
            errors.append(rid + " access")
        if not DATE_RE.match(r["when_start"]) or not DATE_RE.match(r["when_end"]):
            errors.append(rid + " dates")
        ids = [x for x in r["source_ids"].split(";") if x]
        if not ids or any(x not in known for x in ids):
            errors.append(rid + " source_ids")
    return errors, sources, files, cat, srch


def summary(cat, srch):
    out = {"catalogue_rows": len(cat), "search_rows": len(srch)}
    out["catalogue_by_kind"] = dict(sorted(Counter(r["kind"] for r in cat).items()))
    scen = {}
    for c in ("s_removed", "s_unrecovered", "s_literary"):
        rows = Counter(r[c] for r in cat)
        groups = defaultdict(set)
        for r in cat:
            groups[r[c]].add(r["dependency_group"])
        scen[c] = {
            "rows": dict(sorted(rows.items())),
            "distinct_dependency_groups": {k: len(v) for k, v in sorted(groups.items())},
            "supporting_rows_by_kind": dict(sorted(Counter(r["kind"] for r in cat if r[c] == "supports").items())),
        }
    out["scenario_coding"] = scen
    out["dependency_groups"] = len({r["dependency_group"] for r in cat})
    out["searches_by_result"] = dict(sorted(Counter(r["result"] for r in srch).items()))
    out["searches_by_purpose"] = dict(sorted(Counter(r["purpose"] for r in srch).items()))
    out["searches_by_kind"] = dict(sorted(Counter(r["kind"] for r in srch).items()))
    by_place = defaultdict(list)
    for r in srch:
        by_place[r["place_id"] or "(none)"].append(r["search_id"])
    out["searches_by_place_id"] = {k: v for k, v in sorted(by_place.items())}
    both = sorted(r["cat_id"] for r in cat if r["s_unrecovered"] == "supports" and r["s_literary"] == "supports")
    out["rows_supporting_unrecovered_and_literary"] = both
    out["evidence_rows_supporting_unrecovered"] = sorted(
        r["cat_id"] for r in cat if r["kind"] == "EVIDENCE" and r["s_unrecovered"] == "supports")
    out["note"] = "Descriptive counts only; rows are not independent and are not weights of evidence (PLAN.md)."
    return out


def main():
    errors, _, _, cat, srch = validate()
    if errors:
        raise SystemExit("validation failed: " + "; ".join(errors))
    out = summary(cat, srch)
    with open(os.path.join(HERE, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
