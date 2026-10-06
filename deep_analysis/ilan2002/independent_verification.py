"""Independent frozen-pilot verification by finite enumeration, stdlib only.

Does not import or read initials_control.py. Letter spaces and alternatives are
transcribed from the published freeze. No historical population inference.
"""
import csv
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parent
CORPUS = BASE / 'pilot_forms.csv'
RESULT = BASE / 'pilot_results.json'
OUT = BASE / 'independent_verification.json'
ALPHABET = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
VOWELS = 'ΑΕΗΙΟΥΩ'
CONSONANTS = ''.join(x for x in ALPHABET if x not in VOWELS)
MENU = [('ΚΕΝ',), ('ΧΑΓ',), ('ΗΝ',), ('ΘΕ', 'ΞΕ'), ('ΔΙ',),
        ('ΤΡ', 'ΤΡΙ'), ('ΣΚ', 'ΧΚ', 'ΞΚ')]
PRIMARY = [x[0] for x in MENU]


def mask(prefix):
    return ''.join('V' if x in VOWELS else 'C' for x in prefix)


def support(prefix, forms, mode):
    spaces = [ALPHABET if mode == 'uniform24' else
              (VOWELS if t == 'V' else CONSONANTS) for t in mask(prefix)]
    occupied = {x[:len(prefix)] for x in forms if len(x) >= len(prefix)}
    hits = total = 0
    for chars in itertools.product(*spaces):
        total += 1
        hits += ''.join(chars) in occupied
    return Fraction(hits, total), {'occupied_allowed_prefixes': hits,
                                 'allowed_prefixes': total,
                                 'mask': mask(prefix)}


def union_support(alternatives, forms, mode):
    # A shorter existence prefix completely subsumes a nested longer reading.
    minimal = [p for p in alternatives if not any(
        p != other and p.startswith(other) for other in alternatives)]
    if len(minimal) == 1:
        return support(minimal[0], forms, mode)
    assert len({p[1:] for p in minimal}) == 1
    assert len({p[0] for p in minimal}) == len(minimal)
    assert len({mask(p) for p in minimal}) == 1
    pat = mask(minimal[0])
    first_space = ALPHABET if mode == 'uniform24' else (
        VOWELS if pat[0] == 'V' else CONSONANTS)
    tail_spaces = [ALPHABET if mode == 'uniform24' else (
        VOWELS if t == 'V' else CONSONANTS) for t in pat[1:]]
    occupied = {x[:len(minimal[0])] for x in forms
                if len(x) >= len(minimal[0])}
    hits = total = 0
    for tail in itertools.product(*tail_spaces):
        suffix = ''.join(tail)
        for distinct_firsts in itertools.combinations(first_space, len(minimal)):
            total += 1
            hits += any(c + suffix in occupied for c in distinct_firsts)
    return Fraction(hits, total), {
        'successful_tail_distinct_first_combinations': hits,
        'all_tail_distinct_first_combinations': total,
        'distinct_alternative_first_letters': len(minimal),
        'mask': pat}


def direct_patterns(qs, observed):
    # Exhaustively enumerate all 2**7 outcomes; no convolution/runner reuse.
    mass = [Fraction(0) for _ in range(len(qs) + 1)]
    for bits in itertools.product((0, 1), repeat=len(qs)):
        weight = Fraction(1)
        for bit, q in zip(bits, qs):
            weight *= q if bit else 1 - q
        mass[sum(bits)] += weight
    assert sum(mass) == 1
    tail = sum(mass[observed:], Fraction(0))
    return {'observed': observed,
            'q_exact': [str(q) for q in qs],
            'q': [float(q) for q in qs],
            'expected_exact': str(sum(qs)),
            'expected': float(sum(qs)),
            'pmf_exact': [str(p) for p in mass],
            'pmf': [float(p) for p in mass],
            'tail_exact': str(tail), 'tail': float(tail)}


def main():
    rows = list(csv.DictReader(CORPUS.open(encoding='utf-8', newline='')))
    assert len(rows) == 107
    forms = [r['greek_form'] for r in rows]
    assert len(set(forms)) == 107
    assert all(set(f) <= set(ALPHABET) for f in forms)
    matches = {p: [dict(name_id=r['name_id'], greek_form=r['greek_form'])
                   for r in rows if r['greek_form'].startswith(p)]
               for menu in MENU for p in menu}
    cache = {}
    for mode in ('shape', 'uniform24'):
        cache[mode] = {p: support(p, forms, mode) for p in matches}
    output = {
        'scope': '107 normalized reported Greek forms in fixed person-period pilot; '
                 'not whole-book or actual-attestation primary; ordinary-word baseline absent',
        'freeze_commit': '16267e12b9fa6d511d1c5c02cebbadd94bf008c8',
        'corpus_sha256': hashlib.sha256(CORPUS.read_bytes()).hexdigest(),
        'implementation': 'Independent finite prefix/first-letter-combination enumeration '
                          'and 128 outcome patterns; no initials_control import',
        'matches': matches, 'primary': {}, 'union': {}, 'branches': []}
    observed = sum(bool(matches[p]) for p in PRIMARY)
    union_observed = sum(any(matches[p] for p in menu) for menu in MENU)
    for mode in cache:
        q = [cache[mode][p][0] for p in PRIMARY]
        output['primary'][mode] = direct_patterns(q, observed)
        output['primary'][mode]['finite_support'] = [cache[mode][p][1] for p in PRIMARY]
        unions = [union_support(menu, forms, mode) for menu in MENU]
        output['union'][mode] = direct_patterns([x[0] for x in unions], union_observed)
        output['union'][mode]['finite_support'] = [x[1] for x in unions]
    for branch in itertools.product(*MENU):
        n = sum(bool(matches[p]) for p in branch)
        output['branches'].append({'readings': list(branch), **{
            mode: direct_patterns([cache[mode][p][0] for p in branch], n)
            for mode in cache}})
    maximum = max(b['shape']['observed'] for b in output['branches'])
    assert maximum == union_observed
    output['max_branch_hits_equals_union'] = maximum
    root = json.loads(RESULT.read_text())
    issues = []

    def compare(label, got, wanted):
        if got['observed'] != wanted['observed']:
            issues.append(label + ': observed mismatch')
        if Fraction(got['tail_exact']) != Fraction(wanted['upper_tail_exact']):
            issues.append(label + ': exact tail mismatch')
        for field, root_field in [('q', 'slot_hit_probabilities'), ('pmf', 'pmf')]:
            if len(got[field]) != len(wanted[root_field]) or any(
                abs(a-b) > 1e-14 for a,b in zip(got[field], wanted[root_field])):
                issues.append(label + ': ' + field + ' mismatch')
        if abs(got['expected'] - wanted['expected']) > 1e-14:
            issues.append(label + ': expectation mismatch')

    for kind, root_kind in [('primary', 'primary'), ('union', 'documented_union')]:
        for mode in cache:
            compare(kind + '/' + mode, output[kind][mode], root['results'][root_kind][mode])
    assert len(root['branch_sensitivity']) == 12
    for ours, theirs in zip(output['branches'], root['branch_sensitivity']):
        if ours['readings'] != theirs['readings']:
            issues.append('branch ordering/readings mismatch')
        compare('/'.join(ours['readings']), ours['shape'], theirs['shape'])
    reported = {p: ids for row in root['matches']
                for p, ids in row['name_ids_by_prefix'].items()}
    for p, found in matches.items():
        if {x['name_id'] for x in found} != set(reported[p]):
            issues.append(p + ': match form ID mismatch')
    if output['corpus_sha256'] != root['provenance']['selected_csv_sha256']:
        issues.append('corpus hash mismatch')
    output['root_comparison'] = {'material_mismatches': issues,
        'compared': 'All 12 shape branches; primary and union both-null exact tails, '
                    'slot probabilities, expectations, all PMF entries, observed form IDs, CSV hash'}
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'mismatches': issues, 'observed': observed,
        'union_observed': union_observed, 'primary_shape_tail': output['primary']['shape']['tail'],
        'union_shape_tail': output['union']['shape']['tail'],
        'matches': {p: [x['greek_form'] for x in found] for p, found in matches.items() if found},
        'output': str(OUT)}, ensure_ascii=False))
    assert not issues, issues


if __name__ == '__main__':
    main()
