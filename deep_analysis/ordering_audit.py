#!/usr/bin/env python3
"""Exact, retrospective audit of specified 30 September ordering claims.

Uses only the standard library and existing source files. Historical scripts and
outputs are inputs, never rewritten. All probabilities condition on explicitly
listed labels and canonical entry slots; they are not location probabilities.
"""

import argparse
import ast
import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_COMMIT = "5a0e9561135fddec6af6030e8c19e52a9dd7edae"
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")
INPUTS = (
    "data/scroll-text.js", "tools/build_scroll_text.py", "tables/entry_concordance.csv", "text/readings.json",
    "deep_analysis/features.py", "deep_analysis/tests.py",
    "deep_analysis/tests_results.json", "research/phases/phase4_summary.md",
    "research/text/deeper_analysis_2026-09-30.md",
)


def ratio(numerator, denominator):
    value = Fraction(numerator, denominator)
    return {"numerator": value.numerator, "denominator": value.denominator,
            "decimal": float(value)}


def shared_edges(ids, names):
    return [(a, b) for a, b in itertools.combinations(ids, 2)
            if set(names.get(a, ())) & set(names.get(b, ()))]


def adjacency_distribution(ids, edges):
    """Counts labeled linear orders by number of graph edges made adjacent.

    Expand E[z**S] = sum_F (z-1)**|F| P(F all adjacent). An edge subset
    F can occur in a linear order exactly when its nontrivial components are
    paths. Contract its k edges into blocks: 2**c * (n-k)! orders, where c
    counts those path components. Cycles and degree>2 have zero orders.
    """
    n = len(ids)
    if len(set(ids)) != n or n < 1:
        raise ValueError("Use distinct, nonempty entry identities")
    edges = list(edges)
    if len({frozenset(e) for e in edges}) != len(edges):
        raise ValueError("An entry pair contributes at most one adjacency")
    if any(a == b or a not in ids or b not in ids for a, b in edges):
        raise ValueError("Edges must join two listed identities")
    moments = [0] * (len(edges) + 1)
    for mask in range(1 << len(edges)):
        parent = {x: x for x in ids}
        degree = Counter()

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        valid = True
        k = mask.bit_count()
        for j, (a, b) in enumerate(edges):
            if not mask & (1 << j):
                continue
            degree[a] += 1
            degree[b] += 1
            ra, rb = find(a), find(b)
            if degree[a] > 2 or degree[b] > 2 or ra == rb:
                valid = False
                break
            parent[ra] = rb
        if valid:
            c = len({find(x) for x in degree})
            moments[k] += (2 ** c) * math.factorial(n - k)
    counts = [sum((-1) ** (k - s) * math.comb(k, s) * moments[k]
                  for k in range(s, len(moments))) for s in range(len(moments))]
    assert min(counts) >= 0 and sum(counts) == math.factorial(n)
    assert sum(s * c for s, c in enumerate(counts)) == 2 * len(edges) * math.factorial(n) // n
    return counts


def scan_distribution(n, k, width):
    """Exact counts of k-subsets by largest count in any full width window.

    State keeps the previous width-1 bits, total selected slots and largest
    completed-window count. Each binary string represents one k-subset once.
    """
    if not (1 <= width <= n and 0 <= k <= n):
        raise ValueError("Require 1 <= width <= n and 0 <= k <= n")
    mask_limit = (1 << (width - 1)) - 1
    states = {(0, 0, 0): 1}
    for position in range(n):
        following = defaultdict(int)
        for (mask, used, maximum), count in states.items():
            for bit in (0, 1):
                new_used = used + bit
                if new_used > k or new_used + n - position - 1 < k:
                    continue
                window_count = mask.bit_count() + bit
                new_max = max(maximum, window_count) if position + 1 >= width else maximum
                key = ((mask << 1 | bit) & mask_limit, new_used, new_max)
                following[key] += count
        states = following
    counts = [0] * (k + 1)
    for (_, used, maximum), count in states.items():
        assert used == k
        counts[maximum] += count
    assert sum(counts) == math.comb(n, k)
    return counts


def max_window(positions, n, width):
    return max(sum(start <= p < start + width for p in positions)
               for start in range(n - width + 1))


def load_sources():
    source = (ROOT / "data/scroll-text.js").read_text(encoding="utf-8")
    scroll = json.loads(source.split("window.SCROLL_TEXT = ", 1)[1].strip().removesuffix(";"))
    tokens = []
    line_tokens = {}
    for column in scroll["columns"]:
        for line in column["lines"]:
            key = f'{ROMAN[column["c"] - 1]} {line["l"]}'
            line_tokens[key] = []
            for index, word in enumerate(line["w"]):
                token = {"line": key, "word_zero_based": index,
                         "surface": "".join(p[0] for p in word["h"]),
                         "segments": word["h"], "number": "n" in word,
                         "numeral_word": any(m[-1] == "numr" for m in word.get("m", [])),
                         "lemmas": [m[1] for m in word.get("m", [])],
                         "editor_removed": bool(word["h"]) and all(p[1] in ("x", "d") for p in word["h"]),
                         "greek": bool(word.get("greek"))}
                line_tokens[key].append(token)
                tokens.append(token)
    with (ROOT / "tables/entry_concordance.csv").open(encoding="utf-8-sig", newline="") as handle:
        concordance = list(csv.DictReader(handle))
    keys = list(line_tokens)
    entries = {}
    for row in concordance:
        bounds = row["col_line"].replace("–", "-").replace(":", " ").split("-")
        start, end = bounds[0], bounds[-1]
        entries[row["entry_puech"]] = [token for key in keys[keys.index(start):keys.index(end) + 1]
                                       for token in line_tokens[key]]
    # The same I6 boundary correction used by features.py, retaining word IDs.
    split = next(i for i, t in enumerate(line_tokens["I 6"]) if t["surface"] == "בבור")
    entries["2"] = [t for t in entries["2"] if t not in line_tokens["I 6"][split:]]
    entries["3"] = [t for t in entries["3"] if t not in line_tokens["I 6"][:split]]
    tree = ast.parse((ROOT / "deep_analysis/features.py").read_text(encoding="utf-8"))
    names = next(ast.literal_eval(node.value) for node in tree.body
                 if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "NAMES"
                                                        for t in node.targets))
    return entries, tokens, names, concordance


def name_branch(ids, names):
    edges = shared_edges(ids, names)
    edge_set = {frozenset(e) for e in edges}
    observed_pairs = [(a, b) for a, b in zip(ids, ids[1:]) if frozenset((a, b)) in edge_set]
    observed = len(observed_pairs)
    counts = adjacency_distribution(ids, edges)
    denominator = math.factorial(len(ids))
    return {"ids": ids, "n": len(ids), "shared_name_edges": edges,
            "edge_labels": [{"entries": [a, b], "labels": sorted(set(names[a]) & set(names[b]))}
                            for a, b in edges],
            "observed_adjacent_pairs": observed_pairs, "observed": observed,
            "expected": ratio(2 * len(edges), len(ids)),
            "distribution_labeled_order_counts": counts,
            "total_labeled_orders": denominator,
            "p_ge": ratio(sum(counts[observed:]), denominator),
            "p_le": ratio(sum(counts[:observed + 1]), denominator),
            "adjacency_event_subsets_enumerated": 1 << len(edges)}


def audit():
    entries, tokens, names, concordance = load_sources()
    ids = list(entries)
    assert ids == [str(i) for i in range(1, 13)] + ["12a"] + [str(i) for i in range(13, 61)]
    early = ids[:ids.index("20")]
    later = ids[ids.index("20"):ids.index("60")]
    no15 = {entry: list(value) for entry, value in names.items()}
    no15["15"] = []  # Milik's unidentifiable name is not a new shared label.
    shallum = {entry: list(value) for entry, value in names.items()}
    shallum["23"] = ["Shallum"]
    name_results = {
        "early_restored_Kohlit15": name_branch(early, names),
        "early_no_identifiable_name15": name_branch(early, no15),
        "later_Solomon23": name_branch(later, names),
        "later_Shallum23": name_branch(later, shallum),
    }
    phrase_tokens, bare_tokens = [], []
    contexts = []
    for index, token in enumerate(tokens):
        if "כתבן" not in token["surface"]:
            continue
        entry = next(e for e, values in entries.items() if token in values)
        full = index + 1 < len(tokens) and tokens[index + 1]["surface"] in ("אצלם", "אצלן")
        (phrase_tokens if full else bare_tokens).append(entry)
        previous = index - 1
        while previous >= 0 and (tokens[previous]["number"] or tokens[previous]["numeral_word"]
                                 or tokens[previous]["editor_removed"]):
            previous -= 1
        offering_before = tokens[previous]["surface"].startswith("דמע")
        # Find the vessel by the source lemma: V6 spells it כאלין. Limit
        # context to the same canonical entry, preserving source annotations.
        context_start = previous
        while (context_start > 0 and "כְּלִי" not in tokens[context_start]["lemmas"]
               and tokens[context_start - 1] in entries[entry]):
            context_start -= 1
        contexts.append({"entry": entry, "line": token["line"],
                         "word_zero_based": token["word_zero_based"], "full_formula": full,
                         "nearest_previous_nonnumber": tokens[previous]["surface"],
                         "nearest_previous_nonnumber_line": tokens[previous]["line"],
                         "offering_precedes_after_numerals_and_editor_removed_tokens": offering_before,
                         "intervening_tokens": [{"surface": t["surface"], "segments": t["segments"]}
                                                for t in tokens[previous + 1:index]],
                         "preceding_formula_tokens": [t["surface"] for t in tokens[context_start:index]]
                         if full else [tokens[previous]["surface"]]})
    assert phrase_tokens == ["22", "50", "51", "54", "55"] and bare_tokens == ["8"]
    dema = [e for e, values in entries.items() if any("דמע" in t["surface"] for t in values)]
    assert dema == ["4", "12", "13", "22", "33", "50", "51", "54", "55", "58"]
    formula_results = {}
    for key, occurrences in (("five_full_formulae", phrase_tokens),
                             ("six_stem_occurrences", ["8"] + phrase_tokens)):
        k = len(occurrences)
        overlap = len(set(occurrences) & set(dema))
        cooc_num = sum(math.comb(len(dema), j) * math.comb(len(ids) - len(dema), k - j)
                       for j in range(overlap, min(k, len(dema)) + 1))
        positions = [ids.index(e) for e in occurrences]
        observed = max_window(positions, len(ids), 6)
        distribution = scan_distribution(len(ids), k, 6)
        maximum_windows = [ids[start:start + 6] for start in range(len(ids) - 5)
                           if sum(start <= p < start + 6 for p in positions) == observed]
        formula_results[key] = {
            "entries": occurrences, "positions_zero_based": positions,
            "dema_entries": dema, "cooccurrence_count": overlap,
            "p_entry_cooccurrence_ge": ratio(cooc_num, math.comb(len(ids), k)),
            "scan_width_slots": 6, "observed_max": observed, "maximal_windows": maximum_windows,
            "scan_distribution_subset_counts": distribution, "total_subsets": math.comb(len(ids), k),
            "p_scan_ge": ratio(sum(distribution[observed:]), math.comb(len(ids), k)),
        }
    shifted_full = [ids[ids.index(e) + 1] for e in phrase_tokens]
    # Descriptive crosswalk, not a reconstruction of every Milik entry/subitem.
    division = {
        "following_canonical_entries_if_formula_opens_next_item": shifted_full,
        "full_formula_overlap_with_dema": len(set(shifted_full) & set(dema)),
        "six_stem_overlap_with_dema": len(set(["8"] + shifted_full) & set(dema)),
        "boundary_sources": [{"entry": r["entry_puech"], "item_milik": r["item_milik"],
                              "note": r["milik_boundary_note"]}
                             for r in concordance if r["entry_puech"] in phrase_tokens],
        "complete_Milik_slot_null": None,
        "p_literal_token_adjacency": None,
        "limit": "The full Milik segmentation/null is not reconstructed. The61-slot cooccurrence and scan probabilities condition on Puech canonical slots; they are not division invariant or token-adjacency tests.",
    }
    first = ids[:16]
    later_spelling = ids[16:]
    spelling_rows = [{"entry": e, "line": t["line"], "word_zero_based": t["word_zero_based"],
                      "segments": t["segments"]}
                     for e, values in entries.items() for t in values if "ככרין" in t["surface"]]
    full_entries = [e for e in ids if any(row["entry"] == e for row in spelling_rows)]
    spelling = {
        "definition": "Entry presence of literal ככרין after joining every h segment, as in features.py; no fresh manuscript reading and no adjudication of segment flags.",
        "first16_slot_ids": first, "later45_slot_ids": later_spelling,
        "first16_present": [e for e in first if e in full_entries],
        "later45_present": [e for e in later_spelling if e in full_entries],
        "entry_presence_counts": [sum(e in full_entries for e in first),
                                  sum(e in full_entries for e in later_spelling)],
        "token_occurrence_counts": [sum(row["entry"] in first for row in spelling_rows),
                                    sum(row["entry"] in later_spelling for row in spelling_rows)],
        "token_occurrences": spelling_rows,
        "annotation_classes": {"c": "supplied/corrected by modern editor", "u": "damaged/uncertain",
                               "r": "restored in lacuna", "x": "removed by modern editor",
                               "d": "removed by ancient editor", "s": "written above line by scribe"},
        "historical_T8_claim_counts": [7, 4],
        "historical_T8_per_entry_list": None,
        "source_warning_entry38": "e38-bars records bars/pitchers alternatives; literal Abegg ככרין is not a settled unit reading.",
        "scope": "No corrected Greek-gap result follows: only the literal feature is reproduced. Missing T8 entry-level coding/edition basis prevents substituting the reported7/4 as another scored branch.",
    }
    historical = json.loads((ROOT / "deep_analysis/tests_results.json").read_text())
    return {
        "schema": "copper-scroll-ordering-audit-v1", "date_utc": "2026-10-06",
        "base_commit": BASE_COMMIT,
        "status": "completed retrospective arithmetic/definition audit",
        "exposure": "Reported patterns, source text and outputs were already inspected. No confirmatory freeze, unseen prediction or new archaeological identification.",
        "source_sha256": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in INPUTS},
        "source_text_attribution": {
            "dataset": "ETCBC Dead Sea Scrolls Text-Fabric2.0.1, 3Q15",
            "transcription_and_morphology": ["Martin G. Abegg Jr.", "James E. Bowley", "Edward M. Cook"],
            "conversion": ["Jarod Jacobs", "Martijn Naaijer", "Dirk Roorda"],
            "license": "CC BY-NC4.0", "license_url": "https://creativecommons.org/licenses/by-nc/4.0/",
            "source_file": "data/scroll-text.js",
            "project_modifications": "Existing display conversion is documented in tools/build_scroll_text.py. This audit joins displayed h segments, groups tokens by the canonical concordance with its documented I6 boundary correction, and extracts limited formula/unit contexts and metadata. It computes statistics without editing source text or adjudicating readings.",
        },
        "entry_order": ids,
        "slot_conventions": "61 Puech canonical slots include12a. Early block1–19 has20 slots; later20–59 has40. First16 canonical slots end at15; entry50 is zero-based position50 because12a shifts subsequent labels.",
        "name_adjacency": name_results,
        "retained_name_branch_combinations": [
            {"entry15": a, "entry23": b, "early_result": early_key, "later_result": later_key}
            for a, early_key in (("restored_Kohlit", "early_restored_Kohlit15"),
                                 ("no_identifiable_name", "early_no_identifiable_name15"))
            for b, later_key in (("Solomon", "later_Solomon23"), ("Shallum", "later_Shallum23"))],
        "formula_contexts": contexts, "formula_entry_statistics": formula_results,
        "formula_readings": "g-ktbn retains כתבן/בתכן and disputed meanings. The locus family exists under either consonantal interpretation; these location/count tests do not decide the reading or account-record sense.",
        "division_limits": division, "full_unit_spelling": spelling,
        "historical_outputs_retained": {key: historical[key] for key in ("T1_A", "T1_20_59", "T1_pairs", "T6_record", "T6_scan")},
        "multiple_testing": {"all_report_family_tests_revalidated": False,
                             "adjusted_p_values": None,
                             "note": "All tails here are conditional, unadjusted retrospective checks. Source-selected blocks/labels and broader alternative tests remain outside these nulls. The historical Holm table uses a claimed literal-adjacency p without a justified token null; its interpretation cannot be inherited."},
        "conclusions": {
            "later_name_clustering": "Supported descriptively relative to uniform labeled-order null under both retained entry23 readings, conditional on the historical hand-coded name list and fixed20–59 block.",
            "earlier_random_order_claim": "A large tail probability neither establishes random construction nor rules out other grouping variables.",
            "record_formula": "Five local offering-predecessor contexts are reproduced; literal-adjacency significance and historical meaning remain not identifiable from available evidence.",
            "geography": "No regional proximity, place identification, route or deposit-existence inference follows from repeated labels alone.",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "deep_analysis/ordering_audit_results.json")
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key, value in result["name_adjacency"].items():
        print(f'{key}: observed={value["observed"]}, expected={value["expected"]["decimal"]:.6g}, p_ge={value["p_ge"]["decimal"]:.12g}')
    for key, value in result["formula_entry_statistics"].items():
        print(f'{key}: cooccurrence_p={value["p_entry_cooccurrence_ge"]["decimal"]:.12g}, scan_p={value["p_scan_ge"]["decimal"]:.12g}')
    spelling = result["full_unit_spelling"]
    print(f'Literal unit spelling entry counts: {len(spelling["first16_present"])}/{len(spelling["later45_present"])}')


if __name__ == "__main__":
    main()
