#!/usr/bin/env python3
"""Independent exact finite ordinary-form benchmark; never imports project scorer."""
import argparse
import csv
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

ALPHABET = set('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_forms(path, field):
    with open(path, encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    forms = [row[field] for row in rows]
    assert len(forms) == len(set(forms)), 'Input must be unique normalized forms'
    assert forms and all(x and set(x) <= ALPHABET for x in forms), 'Invalid normalized form'
    return forms

def exact_distribution(masks, n, slots):
    """Inclusion/exclusion from finite-sample avoidance, preserving slot dependence."""
    total = len(masks)
    assert 0 <= n <= total
    denominator = comb(total, n)
    histogram = Counter(masks)
    allbits = (1 << slots) - 1
    avoidance = {}
    union_counts = {}
    for forbidden in range(1 << slots):
        blocked = sum(count for mask, count in histogram.items() if mask & forbidden)
        union_counts[forbidden] = blocked
        available = total - blocked
        avoidance[forbidden] = Fraction(comb(available, n) if available >= n else 0, denominator)
    exact_masks = {}
    score_distribution = [Fraction(0) for _ in range(slots + 1)]
    for hit in range(1 << slots):
        probability = Fraction(0)
        subset = hit
        while True:
            probability += (-1 if subset.bit_count() % 2 else 1) * avoidance[(allbits ^ hit) | subset]
            if subset == 0:
                break
            subset = (subset - 1) & hit
        assert probability >= 0
        exact_masks[hit] = probability
        score_distribution[hit.bit_count()] += probability
    assert sum(exact_masks.values()) == 1
    expected = sum(i * p for i, p in enumerate(score_distribution))
    per_slot = [1 - avoidance[1 << i] for i in range(slots)]
    assert expected == sum(per_slot)
    return histogram, union_counts, exact_masks, score_distribution, per_slot, expected

def benchmark(words, names, menu):
    def mask_for(form):
        return sum(1 << i for i, choices in enumerate(menu) if any(form.startswith(prefix) for prefix in choices))
    masks = [mask_for(form) for form in words]
    name_hits = [[form for form in names if any(form.startswith(prefix) for prefix in choices)] for choices in menu]
    observed = sum(bool(matches) for matches in name_hits)
    histogram, union_counts, exact_masks, distribution, per_slot, expected = exact_distribution(masks, len(names), len(menu))
    tail = sum(distribution[observed:])
    return {
        'readings': menu,
        'name_matches': name_hits,
        'name_score': observed,
        'word_counts_per_slot': [sum(bool(mask & (1 << i)) for mask in masks) for i in range(len(menu))],
        'matched_sample_size': len(names),
        'word_total': len(words),
        'word_complete_corpus_score': sum(any(mask & (1 << i) for mask in masks) for i in range(len(menu))),
        'word_overlap_name_forms': sorted(set(words) & set(names)),
        'word_membership_histogram': {str(k): v for k, v in sorted(histogram.items())},
        'word_union_counts': {str(k): v for k, v in union_counts.items()},
        'sample_exact_hit_masks': {str(k): str(v) for k, v in exact_masks.items()},
        'sample_score_distribution': [str(p) for p in distribution],
        'sample_per_slot_hit_probability': [str(p) for p in per_slot],
        'sample_expected_score_exact': str(expected),
        'sample_expected_score': float(expected),
        'tail_at_least_name_score_exact': str(tail),
        'tail_at_least_name_score': float(tail),
    }

def self_test():
    for masks, n, slots in [([0,1,2,3,4,5,6,7],3,3), ([0,1,1,3],2,2), ([0,0,3],0,2), ([0,0,3],3,2)]:
        _, _, exact, distribution, _, _ = exact_distribution(masks,n,slots)
        brute = Counter()
        for ix in itertools.combinations(range(len(masks)),n):
            mask = 0
            for i in ix:
                mask |= masks[i]
            brute[mask] += 1
        assert exact == {mask: Fraction(brute[mask],comb(len(masks),n)) for mask in exact}
    print('Independent exact scorer verified against exhaustive finite-population toy samples.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--words')
    parser.add_argument('--word-field', default='greek_form')
    parser.add_argument('--names')
    parser.add_argument('--name-field', default='greek_form')
    parser.add_argument('--freeze')
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    assert all([args.words,args.names,args.freeze]), 'words, names, freeze required'
    words = read_forms(args.words,args.word_field)
    names = read_forms(args.names,args.name_field)
    freeze = json.loads(Path(args.freeze).read_text())
    menu = freeze['reading_menu']
    primary = [[prefix] for prefix in freeze['primary_readings']]
    assert freeze['status'] == 'frozen_before_scoring'
    assert digest(args.words) == freeze['word_forms_sha256']
    assert digest(args.names) == freeze['names_sha256']
    def population(forms):
        return {
            'union_primary': benchmark(forms,names,menu),
            'literal_primary_sensitivity': benchmark(forms,names,primary),
            'branches': [benchmark(forms,names,[[x] for x in branch]) for branch in itertools.product(*menu)],
        }
    with open(args.words, encoding='utf-8', newline='') as f:
        word_rows = list(csv.DictReader(f))
    unmixed = [row[args.word_field] for row in word_rows if row['mixed_Ne_use'] == 'False']
    result = {
        'scope': freeze['scope'],
        'method': 'Uniform without-replacement unique Nb form subsets matched to107 name forms; exact correlated-slot inclusion/exclusion.',
        'provenance': {
            'words_sha256': digest(args.words), 'names_sha256': digest(args.names),
            'freeze_sha256': digest(args.freeze), 'benchmark_code_sha256': digest(__file__),
            'source_commit': freeze['source_commit'], 'source_xml_sha256': freeze['source_xml_sha256'],
        },
        'populations': {
            'primary_common_uses': population(words),
            'secondary_without_mixed_Ne': population(unmixed),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
