"""Independent integer generating-function verification of exact word sampling.

Accepts result histogram only; does not import or use the benchmark algorithm.
"""
from collections import Counter
from fractions import Fraction
import json
from math import comb
from pathlib import Path
import sys


def distribution(histogram, n, slots):
    counts = {int(k): v for k, v in histogram.items()}
    zero = counts.pop(0, 0)
    total = zero + sum(counts.values())
    states = {(0, 0): 1}
    for mask, count in counts.items():
        new = Counter()
        for (chosen, hit), ways in states.items():
            for k in range(min(count, n-chosen)+1):
                new[chosen+k, hit | (mask if k else 0)] += ways*comb(count, k)
        states = new
    mass = [0]*(slots+1)
    for (chosen, hit), ways in states.items():
        if 0 <= n-chosen <= zero:
            mass[hit.bit_count()] += ways*comb(zero, n-chosen)
    denom = comb(total, n)
    assert sum(mass) == denom
    return [Fraction(x, denom) for x in mass]


def main():
    path = Path(sys.argv[1])
    result = json.loads(path.read_text())
    checked = 0
    for population in result['populations'].values():
        for b in [population['union_primary'], population['literal_primary_sensitivity'],
                  *population['branches']]:
            pmf = distribution(b['word_membership_histogram'], b['matched_sample_size'], 7)
            assert pmf == [Fraction(x) for x in b['sample_score_distribution']]
            assert sum(pmf[b['name_score']:]) == Fraction(b['tail_at_least_name_score_exact'])
            assert sum(i*p for i,p in enumerate(pmf)) == Fraction(b['sample_expected_score_exact'])
            checked += 1
    print(json.dumps({'independent_integer_verification': 'passed', 'comparisons': checked,
                      'method': 'category binomial weights and OR-mask generating function'}))


if __name__ == '__main__':
    main()
