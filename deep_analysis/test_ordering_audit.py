"""Independent exhaustive finite checks of the two exact counting algorithms."""

import itertools
import math
import unittest
from collections import Counter

from ordering_audit import adjacency_distribution, max_window, scan_distribution


class ExactOrderingChecks(unittest.TestCase):
    def test_every_graph_on_four_labeled_vertices(self):
        # Includes triangles, degree-three stars, disjoint paths, empty and
        # complete graphs. Direct permutation counts share no contraction code.
        ids = list(range(4))
        possible = list(itertools.combinations(ids, 2))
        for mask in range(1 << len(possible)):
            edges = [e for j, e in enumerate(possible) if mask & (1 << j)]
            edge_set = {frozenset(e) for e in edges}
            observed = Counter(sum(frozenset((a, b)) in edge_set
                                   for a, b in zip(order, order[1:]))
                               for order in itertools.permutations(ids))
            result = adjacency_distribution(ids, edges)
            self.assertEqual(result, [observed[i] for i in range(len(edges) + 1)])

    def test_overlapping_names_count_entry_pair_once(self):
        ids = list(range(7))
        edges = [(0, 1), (0, 2), (1, 2), (2, 3), (4, 5)]
        edge_set = {frozenset(e) for e in edges}
        observed = Counter(sum(frozenset((a, b)) in edge_set
                               for a, b in zip(order, order[1:]))
                           for order in itertools.permutations(ids))
        self.assertEqual(adjacency_distribution(ids, edges),
                         [observed[i] for i in range(len(edges) + 1)])

    def test_every_subset_at_several_window_widths(self):
        # Check all k, full first/last windows, and width1/widthN cases.
        for n in (6, 8, 10):
            for width in sorted({1, 3, 6, n}):
                for k in range(n + 1):
                    direct = Counter(max_window(positions, n, width)
                                     for positions in itertools.combinations(range(n), k))
                    self.assertEqual(scan_distribution(n, k, width),
                                     [direct[i] for i in range(k + 1)])

    def test_disconnected_fixed_pairs_closed_form(self):
        # For r disjoint pairs, all must touch with2**r*(n-r)! orders.
        n, r = 8, 3
        edges = [(2 * i, 2 * i + 1) for i in range(r)]
        counts = adjacency_distribution(list(range(n)), edges)
        self.assertEqual(counts[r], 2 ** r * math.factorial(n - r))


if __name__ == "__main__":
    unittest.main()
