"""Exploratory source-anchored clause inventory and finite constraint propagation.

No JavaScript execution, new transcription, place aliases, or independent witnesses.
Run from the repository root: python research/shared_tools/text_constraints/concordance.py
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PIN = "897733283606988581155a3c1df0cd235cb7bea9"
ROMANS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
SOURCES = ["data/scroll-text.js", "tools/build_scroll_text.py", "text/translation_en.json",
           "text/readings.json", "tables/entry_concordance.csv", "tables/feature_constraints.csv",
           "research/feature_workbench/relationships/model.json", "research/shared_tools/text_constraints/parses.json"]
FLAGS = {"x": "modern-editor removal", "d": "ancient removal", "s": "scribal supralinear",
         "c": "modern correction or supply", "r": "restored in a lacuna", "u": "uncertain or damaged", "g": "Greek"}


def normalized(lemma):
    # Homonym suffixes are retained: אמה_1 (cubit) differs from אמה_2 (conduit).
    return "".join(c for c in unicodedata.normalize("NFD", lemma) if not unicodedata.combining(c)).strip()


FAMILIES = {
    "beneath": ["תחת_1"], "opposite": ["נגד"], "between": ["בין", "אמצע"],
    "facing": ["צפה_1"], "dig": ["חפר_1"], "measure": ["משח_2"],
    "north_lexeme": ["צפון_1", "צפוני_1"], "east_lexeme": ["מזרח", "מזרחי"],
    "west_lexeme": ["מערב_2", "מערבי"], "south_lexeme": ["דרום", "דרומי"],
    "mouth_lexeme": ["פה"], "opening_lexeme": ["פתח", "פתח_1", "ביאה"],
    "cubit_unit": ["אמה_1"], "conduit_lexeme": ["אמה_2"],
    "written_record_lexeme": ["כתב"], "beside": ["אצל"],
}


def parse_scroll(source):
    """Decode only the literal assigned to SCROLL_TEXT; reject executable suffixes."""
    match = re.search(r"window\.SCROLL_TEXT\s*=\s*(\{.*\})\s*;?\s*$", source, re.S)
    if not match:
        raise ValueError("Expected a single trailing SCROLL_TEXT JSON assignment")
    return json.loads(match.group(1))


def line_key(column, line):
    return f"{ROMANS[column - 1]} {line}"


def row_owners(concordance, line_order):
    owners = defaultdict(list)
    for row in concordance:
        limits = re.split(r"[–-]", row["col_line"])
        start, end = limits[0].replace(":", " "), limits[-1].replace(":", " ")
        a, b = line_order.index(start), line_order.index(end)
        for line in line_order[a:b + 1]:
            owners[line].append(row["entry_puech"])
    return owners


def scoped_variants(variants, line, index):
    out = []
    for v in variants:
        positions = [{"line": v.get("line"), "words": v.get("words")}] + v.get("also", [])
        for pos in positions:
            if pos.get("line") == line and (pos.get("words") is None or index in pos["words"]):
                out.append({"id": v["id"], "scope": "word" if pos.get("words") is not None else "line",
                            "entry": v.get("entry"), "label": v.get("label"),
                            "readings": v.get("readings", []), "sources": v.get("sources", [])})
                break
    return out


def inventory(scroll, translations, variants, concordance):
    order = [line_key(c["c"], l["l"]) for c in scroll["columns"] for l in c["lines"]]
    owners = row_owners(concordance, order)
    hits, tokens = [], []
    for ci, column in enumerate(scroll["columns"]):
        for li, line in enumerate(column["lines"]):
            key = line_key(column["c"], line["l"])
            for wi, word in enumerate(line["w"]):
                lemmas = [normalized(m[1]) for m in word.get("m", [])]
                families = [name for name, values in FAMILIES.items() if set(values).intersection(lemmas)]
                token = {"line": key, "word_index": wi, "entries": owners[key],
                         "shared_boundary_context": len(owners[key]) > 1,
                         "source_pointer": f"/columns/{ci}/lines/{li}/w/{wi}",
                         "segments": word.get("h", []), "lemma_segments": word.get("m", []),
                         "normalized_lemmas": lemmas,
                         "flags": sorted({flag for _, flag in word.get("h", []) if flag}),
                         "surface_as_encoded": "".join(s for s, _ in word.get("h", [])),
                         "surface_without_removed_segments": "".join(s for s, f in word.get("h", []) if f not in {"x", "d"}),
                         "families": families, "variant_records": scoped_variants(variants, key, wi)}
                tokens.append(token)
                if families:
                    hits.append({**token, "translation_context": translations.get(key),
                                 "semantic_status": "lexical trigger; argument binding requires a reviewed parse"})
    # Repeated lexical bigrams are counted by source anchors, never by editions.
    bigrams = defaultdict(list)
    for left, right in zip(tokens, tokens[1:]):
        # Never bridge an unanalysed word, lacuna, Greek token, or numeral.
        if not left["normalized_lemmas"] or not right["normalized_lemmas"]:
            continue
        # A line break within an entry is permitted; cross-entry transitions are not.
        if not set(left["entries"]).intersection(right["entries"]):
            continue
        if left["shared_boundary_context"] or right["shared_boundary_context"]:
            continue
        # Prefixes are retained rather than silently converting a lexical match to syntax.
        signature = (tuple(left["normalized_lemmas"]), tuple(right["normalized_lemmas"]))
        if not any(left["families"]) and not any(right["families"]):
            continue
        bigrams[signature].append([{k: t[k] for k in ("line", "word_index", "source_pointer", "entries", "flags")} for t in (left, right)])
    repeated = [{"lemma_word_pair": [list(a), list(b)], "occurrences": refs}
                for (a, b), refs in sorted(bigrams.items()) if len(refs) > 1]
    counts = Counter(f for hit in hits for f in hit["families"])
    return {"source": scroll["source"], "flag_definitions": FLAGS, "family_definitions": FAMILIES,
            "family_counts": dict(sorted(counts.items())), "occurrences": hits, "repeated_word_pairs": repeated,
            "limits": ["The corpus is one reused edition-based ETCBC transcription, not original-image inspection.",
                       "Morphology is inherited, including homonym IDs and damaged or removed letters.",
                       "Direction words are lexical triggers; north-of, north-side and north-facing have different arguments.",
                       "Two entries that share a line are retained as ambiguous context, not independent hits.",
                       "Repeated strings never force a shared physical feature or a shared geographical name."]}


def observation_status(model, subject, relation, reference=None, window=None):
    """Exact role/reference join, three values; conflicting documentary assertions stay unknown."""
    records = [o for o in model["observations"] if subject is not None and o["feature_id"] == subject
               and o["property"] == ("chronology" if relation == "exists_during" else relation)
               and (relation == "exists_during" or o["value"].get("reference_feature_id") == reference)]
    truths = set()
    for o in records:
        value = o["value"]
        if relation == "exists_during":
            if window is None:
                continue
            start, end = value.get("secure_earliest_construction_year"), value.get("secure_last_accessible_year")
            if (start is not None and start > window[1]) or (end is not None and end < window[0]):
                truths.add(False)
            interval = value.get("dated_accessible_interval")
            if interval and max(window[0], interval[0]) <= min(window[1], interval[1]):
                truths.add(True)
        else:
            v = value.get("asserted")
            if isinstance(v, bool):
                truths.add(v)
    status = "supported" if truths == {True} else "contradicted" if truths == {False} else "unknown"
    return {"status": status, "conflicting_assertions": len(truths) > 1,
            "observation_ids": sorted({r["id"] for r in records}),
            "source_ids": sorted({s for r in records for s in r["source_ids"]})}


def propagate(model):
    """Run every registered model branch; prune only source-controlled contradictions."""
    predicates = {p["id"]: p for p in model["predicates"]}
    readings = {r["id"]: r for r in model["readings"]}
    rows = []
    for assignment, window in itertools.product(model["assignments"], model["windows"]):
        for reading_id in assignment["reading_ids"]:
            tests = []
            for pid in readings[reading_id]["predicate_ids"]:
                p = predicates[pid]
                subject = assignment["roles"].get(p["subject"])
                reference = assignment["roles"].get(p["object"]) if p["object"] else None
                status = observation_status(model, subject, p["relation"], reference, window["years"])
                tests.append({"predicate": pid, "relation": p["relation"], "subject_feature": subject,
                              "reference_feature": reference, "text_source_ids": p["source_ids"], **status})
            contradictions = [t["predicate"] for t in tests if t["status"] == "contradicted"]
            unknowns = [t["predicate"] for t in tests if t["status"] == "unknown"]
            rows.append({"assignment": assignment["id"], "reading": reading_id, "window": window["id"],
                         "status": "rejected" if contradictions else "unresolved" if unknowns else "supported_relations",
                         "minimal_single_constraint_conflicts": [[p] for p in contradictions],
                         "unknown_predicates": unknowns, "tests": tests})
    retained = [r for r in rows if r["status"] != "rejected"]
    domains = {key: sorted({r[key] for r in retained}) for key in ("assignment", "reading", "window")}
    return {"rows": rows, "retained_domains": domains,
            "claim": "Constraint compatibility for the finite exposed Koḥlit model, not identification",
            "scientific_result": "not identifiable from available evidence",
            "limits": model["limits"] + ["This is an independent implementation over existing model observations, not new archaeological evidence.",
                                        "Repeated clause frequencies add no likelihood or independent corroboration.",
                                        "Minimal conflicts identify individual contradictory required relations; they do not reject all site proposals."]}


def build(root=ROOT):
    read = lambda p: (root / p).read_text(encoding="utf-8-sig")
    hashes = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in SOURCES}
    scroll = parse_scroll(read("data/scroll-text.js"))
    variants = json.loads(read("text/readings.json"))
    with (root / "tables/entry_concordance.csv").open(encoding="utf-8-sig", newline="") as f:
        concordance = list(csv.DictReader(f))
    model = json.loads(read("research/feature_workbench/relationships/model.json"))
    corpus = inventory(scroll, json.loads(read("text/translation_en.json")), variants, concordance)
    parses = json.loads(read("research/shared_tools/text_constraints/parses.json"))
    referenced = {vid for frame in parses["frames"] for vid in frame["variant_ids"]}
    missing = referenced - {v["id"] for v in variants}
    if missing:
        raise ValueError(f"Unknown variant IDs: {sorted(missing)}")
    parses["variant_provenance"] = [v for v in variants if v["id"] in referenced]
    return {"schema": 1, "input_commit": PIN, "source_hashes": hashes,
            "exposure": "all source inputs already exposed; exploratory extraction and reanalysis",
            "concordance": corpus, "audited_parses": parses, "propagation": propagate(model)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    result = build()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = result["propagation"]["rows"]
    print(json.dumps({"output": str(args.output),
                      "lexical_family_counts": result["concordance"]["family_counts"],
                      "model_branch_statuses": dict(Counter(r["status"] for r in rows)),
                      "scientific_result": result["propagation"]["scientific_result"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
