#!/usr/bin/env python3
"""Extract bounded R12 inventory features from the existing tagged transcription.

Run from any directory: python research/text/inventory_extract.py [--check]
This reads the Abegg/ETCBC display data, not the manuscript or Puech's text.
The output retains the source's uncertainty classes and licenses its derivative
token data CC BY-NC 4.0, with attribution recorded in the JSON.
"""

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("inventory_features_2026-10-06.json")
BASE = "5a0e9561135fddec6af6030e8c19e52a9dd7edae"
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
FLAGS = {
    "u": "damaged or uncertain letter",
    "r": "restored in a lacuna",
    "c": "supplied or corrected by modern editor",
    "s": "written above the line by the scribe",
    "x": "removed by modern editor",
    "d": "removed by ancient editor",
    "g": "Greek",
}
FEATURES = {
    "dema": "Lemma דמע; ritual/tribute meaning remains interpretation-dependent.",
    "herem": "Lemma חרם; designation/function remains interpretation-dependent.",
    "vessels": "Lemma כלי; a listed object, not a proven deposit container.",
    "silver": "Lemma כסף; no inference about whether a following unit weighs silver.",
    "gold": "Lemma זהב; no inference about whether a following unit weighs gold.",
    "weight": "Lemma משקל.",
    "kk": "Exact displayed token ככ; no expansion imposed.",
    "kkrin": "Exact displayed token ככרין; full plural unit spelling.",
    "kkr": "Exact displayed token ככר; singular, partly restored here.",
    "written_record_suffix": "Exact וכתבן/כתבן; five full formulas plus bare II5.",
    "written_record_noun": "Lemma כתב outside suffix tokens; final הכתב.",
    "book_or_scroll": "Lemma ספר; VI5 and VIII3 have different contexts.",
    "chest": "Lemma שדה; contextual container reading.",
    "ingots": "Lemma עשת; object denomination, not a weight unit.",
    "garments": "Lemma לבוש; edition alternatives retained in accompanying note.",
    "apudah": "Lemma אפדה; garment/ephod interpretation is conditional.",
    "tithe": "Lemma מעשר (surface מעסר); second-tithe phrase crosses I10–11.",
}
LEMMA_FEATURE = {
    "דמע": "dema", "חרם": "herem", "כלי": "vessels", "כסף": "silver",
    "זהב": "gold", "משקל": "weight", "ספר": "book_or_scroll",
    "שדה": "chest", "עשת": "ingots", "לבוש": "garments", "אפדה": "apudah",
    "מעשר": "tithe",
}


def norm_lemma(s):
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn")
    return re.sub(r"_[0-9]+$", "", s)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract():
    data_path = ROOT / "data/scroll-text.js"
    source = data_path.read_text(encoding="utf-8")
    payload = source.split("window.SCROLL_TEXT = ", 1)[1].rstrip().removesuffix(";")
    data = json.loads(payload)
    ranges = list(csv.DictReader((ROOT / "tables/entry_concordance.csv").open(
        encoding="utf-8-sig", newline="")))
    lines = {(c["c"], l["l"]): l["w"] for c in data["columns"] for l in c["lines"]}
    assert len(lines) == 181 and len(ranges) == 61
    assignments = {}
    entries = []
    for row in ranges:
        match = re.fullmatch(r"(\d+):(\d+)[ab]?(?:-(\d+):(\d+)[ab]?)?", row["lefkovits_lines"])
        assert match, row
        c1, l1 = map(int, match.groups()[:2])
        c2, l2 = map(int, match.groups()[2:]) if match.group(3) else (c1, l1)
        coords = [cl for cl in sorted(lines) if (c1, l1) <= cl <= (c2, l2)]
        # Lefkovits item12 covers 12/12a. Puech has a split after III4.
        if row["entry_puech"] == "12":
            coords = [(3, l) for l in range(1, 5)]
        elif row["entry_puech"] == "12a":
            coords = [(3, l) for l in range(5, 8)]
        hits = {f: [] for f in FEATURES}
        for col, ln in coords:
            for wi, word in enumerate(lines[col, ln]):
                # Shared I6 belongs to entry2 before בבור and entry3 from בבור.
                if (col, ln) == (1, 6):
                    if row["entry_puech"] == "2" and wi >= 2:
                        continue
                    if row["entry_puech"] == "3" and wi < 2:
                        continue
                key = (col, ln, wi)
                assert key not in assignments, (key, row["entry_puech"], assignments.get(key))
                assignments[key] = row["entry_puech"]
                surface = "".join(h for h, flag in word["h"])
                classes = sorted({flag for h, flag in word["h"] if flag})
                unclear = any(ch in surface for ch in "◦…")
                unflagged = not classes and not unclear
                lemmas = {norm_lemma(m[1]) for m in word.get("m", [])}
                features = {LEMMA_FEATURE[x] for x in lemmas if x in LEMMA_FEATURE}
                if surface in ("ככ", "ככרין", "ככר"):
                    features.add({"ככ": "kk", "ככרין": "kkrin", "ככר": "kkr"}[surface])
                if surface in ("כתבן", "וכתבן"):
                    features.add("written_record_suffix")
                elif "כתב" in lemmas:
                    features.add("written_record_noun")
                for feature in features:
                    hits[feature].append({
                        "line": f"{ROMAN[col]} {ln}", "column": col,
                        "line_number": ln, "word_index_0based": wi,
                        "surface": surface, "segments": word["h"],
                        "flags": classes, "unclear_character": unclear,
                        "source_unflagged": unflagged,
                    })
        entries.append({"entry": row["entry_puech"], "col_line": row["col_line"], "features": hits})
    expected = {(c, l, i) for (c, l), words in lines.items() for i in range(len(words))}
    assert set(assignments) == expected, "Each source token must belong to exactly one canonical entry"
    counts = {}
    for f in FEATURES:
        incl = [e["entry"] for e in entries if e["features"][f]]
        strict = [e["entry"] for e in entries if any(h["source_unflagged"] for h in e["features"][f])]
        counts[f] = {
            "inclusive_token_count": sum(len(e["features"][f]) for e in entries),
            "inclusive_entry_count": len(incl), "inclusive_entries": incl,
            "source_unflagged_token_count": sum(h["source_unflagged"] for e in entries for h in e["features"][f]),
            "source_unflagged_entry_count": len(strict), "source_unflagged_entries": strict,
        }
    # These critical distinctions are specific to the stated analysis, not a
    # blanket claim that an unmarked transcription verifies an original letter.
    assert counts["dema"]["inclusive_token_count"] == 12
    assert counts["dema"]["source_unflagged_token_count"] == 10
    assert counts["written_record_suffix"]["inclusive_token_count"] == 6
    assert assignments[1, 6, 0] == "2" and assignments[1, 6, 2] == "3"
    complete_formulas = []
    for cl, words in lines.items():
        for wi in range(len(words) - 1):
            first, second = words[wi:wi + 2]
            a = "".join(x[0] for x in first["h"])
            b = "".join(x[0] for x in second["h"])
            if a in ("כתבן", "וכתבן") and b in ("אצלם", "אצלן"):
                complete_formulas.append({
                    "line": f"{ROMAN[cl[0]]} {cl[1]}",
                    "puech_entry": assignments[cl[0], cl[1], wi],
                    "surface": a + " " + b,
                    "source_unflagged": not any(flag for w in (first, second) for _, flag in w["h"])
                        and not any(ch in a + b for ch in "◦…"),
                    "retained_interpretations": ["written account with deposit (כ reading)",
                                                 "locative/distance formula (ב reading)"],
                })
    assert len(complete_formulas) == 5
    source_paths = [
        "data/scroll-text.js", "tables/entry_concordance.csv", "tools/build_scroll_text.py",
        "text/readings.json", "research/logs/findings_log.md",
        "research/logs/open_questions.md", "research/measurements/cycle10/README.md",
    ]
    return {
        "analysis": "R12 inventory form, units and chronology — exploratory evidence audit",
        "date_utc": "2026-10-06", "base_commit": BASE,
        "transcription": data["source"],
        "license": "CC BY-NC 4.0 for derivative Abegg/ETCBC token data",
        "attribution": "Martin G. Abegg Jr., James E. Bowley and Edward M. Cook; conversion Jarod Jacobs, Martijn Naaijer and Dirk Roorda; existing display build and this feature extraction are project modifications.",
        "input_sha256": {p: digest(ROOT / p) for p in source_paths},
        "scope": {
            "source_lines": len(lines), "canonical_entries": len(entries),
            "source_tokens": len(expected), "new_manuscript_observations": 0,
            "new_archaeological_observations": 0, "unused_prediction": None,
            "counts_are": "Abegg/ETCBC displayed reading with Puech entry boundaries; not counts of Puech's readings, independent deposits or authenticated original letters",
            "unflagged_rule": "Exclude every nonempty display class and explicit ◦/…; conservative notation sensitivity, not manuscript authentication",
        },
        "flag_definitions": FLAGS, "feature_definitions": FEATURES,
        "counts": counts, "full_record_formulas": complete_formulas,
        "explicit_second_tithe": {
            "entry": "4", "locus": "I 10–11", "surface": "מעסר שני",
            "source_unflagged": True,
            "retained_adjacent_meanings": ["מפוגל: disqualified (Puech)",
                                           "מפי גל: from mouth of heap (Milik)"],
            "ref": "text/readings.json#e4-disqualified; Phase1 entry4; ritual status attaches only under first branch",
        },
        "unit_comparisons": [
            {"loci": ["II 6", "IV 12"], "entries": ["8", "19"],
             "contexts": ["silver + ככרין + seventy", "silver + ככ + seventy"],
             "inference": "Parallel syntax and equal numerals permit abbreviation hypothesis; distinct deposits with equal numerals do not prove equal units."},
            {"loci": ["XII 1"], "entries": ["56"], "context": "gold + ככ + five",
             "inference": "Uniform literal expansion כסף כרש requires a valuation or metal-dependent convention here; generic karsh remains distinct from literal silver-karsh expansion."},
        ],
        "interpretation_checks": [
            {"claim": "The document adopts an inventory/retrieval form", "result": "compatible as a descriptive textual-form classification",
             "reason": "Listed objects, measures, local instructions and final duplicate-document wording survive removing all flagged hits; the disputed five-record formula is unnecessary for this conclusion.",
             "refs": ["Phase1 §4", "I 3–4", "XII 11–13"]},
            {"claim": "Five full formulas identify written accounts kept beside the deposits", "result": "not identifiable from available evidence",
             "reason": "The Abegg כ reading permits written records; retained ב/locative readings permit distance or next-entry directions. A displayed unflagged token is not manuscript authentication.",
             "surviving_models": ["written account with deposit (כ reading)", "locative/distance formula (ב reading)"],
             "refs": ["V 7", "XI 1", "XI 4", "XI 11", "XI 15", "text/readings.json#g-ktbn"]},
            {"claim": "The inventory belonged specifically to the Jerusalem Temple", "result": "not identifiable from available evidence",
             "surviving_models": ["Temple-owned property", "earmarked offerings held by contributors or administrators", "other religious/community property", "literary treasure catalogue"],
             "reason": "Ritual/accounting vocabulary is compatible with multiple owners; the displayed data supplies neither an authenticated ownership label nor a discriminating archaeological deposit."},
            {"claim": "The unit/quantity evidence identifies origin or verifies actual deposits", "result": "not identifiable from available evidence",
             "reason": "ככ expansion, corrected full spellings, quantity readings and object-versus-weight counts remain conditional; no total mass or owner follows."},
            {"claim": "A named or ancient landmark dates compilation/deposition of the entire scroll", "result": "not identifiable from available evidence",
             "reason": "Feature identification, phase, use at the time described, text copying and cave deposition remain separate dependencies; reused place names and ruins may outlast their construction."},
        ],
        "chronology_controls": [
            {"entry": "22", "refs": ["DJDIII D10–D11 pp263–264/C201 p257 (prior notes only)", "Josephus BJ5.145 = War5.4.2", "research/logs/open_questions.md#Q37"],
             "available_observation": "Josephus's retrospective pre-destruction Jerusalem description names Solomon's pool; it does not establish Secacah's reservoir or the date of that reservoir's name.",
             "compilation_bound": None, "cave_deposition_bound": None},
            {"entry": "49", "refs": ["Ariel2020 pp90*–91*, coin20/L105/basket1092", "research/measurements/cycle10/README.md"],
             "available_observation": "Published foundation coin dates69/70CE; accepting that context supplies a lower installation bound for that particular floor.",
             "conditional_text_bound": "Only an instruction referring to this built phase requires the described-use/deposit model to accommodate construction after coin minting.",
             "compilation_bound": None, "cave_deposition_bound": None},
        ],
        "entries": entries,
    }


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--check", action="store_true", help="Check committed output without rewriting it")
    options = args.parse_args()
    result = extract()
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if options.check:
        assert OUT.read_text(encoding="utf-8") == encoded, "Result differs; rerun extraction"
    else:
        OUT.write_text(encoded, encoding="utf-8")
    print(json.dumps({"entries": len(result["entries"]), "source_lines": result["scope"]["source_lines"],
                      "counts": {k: {a: v[a] for a in ("inclusive_token_count", "inclusive_entry_count",
                          "source_unflagged_token_count", "source_unflagged_entry_count")}
                                 for k, v in result["counts"].items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
