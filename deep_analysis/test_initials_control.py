"""Synthetic mechanics tests only. No historical personal-name corpus scored."""
from fractions import Fraction
import json
import subprocess
import sys
from itertools import combinations
from pathlib import Path
import tempfile
import unittest

from initials_control import (ALPHABET, CONSONANTS, VOWELS, collapse_nested,
    exact_slot_probability, load_corpus, monte_carlo, normalize_form,
    poisson_binomial, score)


class MethodTests(unittest.TestCase):
    def test_cli_blocks_unavailable_corpus_without_output(self):
        here = Path(__file__).parent
        result = subprocess.run([sys.executable, str(here / "initials_control.py"),
            "--freeze", str(here / "greek_personal_initials_protocol.json")],
            capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("frozen_before_scoring", result.stderr)

    def test_cli_rejects_reading_drift_before_scoring(self):
        here = Path(__file__).parent
        with tempfile.TemporaryDirectory(dir=here) as folder:
            manifest = json.loads((here / "greek_personal_initials_protocol.json").read_text())
            manifest["status"] = "frozen_before_scoring"
            manifest["primary_readings"][0] = "ΑΑ"
            path = Path(folder) / "freeze.json"
            path.write_text(json.dumps(manifest))
            result = subprocess.run([sys.executable, str(here / "initials_control.py"),
                "--freeze", str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertIn("frozen readings differ", result.stderr)

    def test_cli_rejects_changed_corpus_without_output(self):
        here = Path(__file__).parent
        with tempfile.TemporaryDirectory(dir=here) as folder:
            manifest = json.loads((here / "greek_personal_initials_protocol.json").read_text())
            manifest.update(status="frozen_before_scoring", corpus_csv="synthetic.csv", corpus_sha256="0" * 64)
            path = Path(folder) / "freeze.json"
            path.write_text(json.dumps(manifest))
            (Path(folder) / "synthetic.csv").write_text("name_id,greek_form\nx,ΒΑ\n")
            result = subprocess.run([sys.executable, str(here / "initials_control.py"),
                "--freeze", str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertIn("checksum differs", result.stderr)

    def test_normalization_and_sigma(self):
        self.assertEqual(normalize_form("  σόςϲ  ", subscript="omit"), ("ΣΟΣΣ", False))
        self.assertEqual(normalize_form("αΐ", subscript="omit"), ("ΑΙ", False))

    def test_subscript_never_silently_casefolded(self):
        self.assertEqual(normalize_form("ᾳ", subscript="omit"), ("Α", True))
        self.assertEqual(normalize_form("ᾳ", subscript="expand"), ("ΑΙ", True))
        with self.assertRaises(ValueError):
            normalize_form("ᾳ", subscript="reject")

    def test_no_token_join_or_transliteration(self):
        for raw in ("Α Β", "Α-Β", "Alex", "", "ϝ"):
            with self.assertRaises(ValueError):
                normalize_form(raw, subscript="omit")

    def test_alphabet_partition(self):
        self.assertEqual(len(ALPHABET), 24)
        self.assertEqual((len(VOWELS), len(CONSONANTS)), (7, 17))

    def test_exact_single_uniform(self):
        self.assertEqual(exact_slot_probability(frozenset({"ΑΒΓ"}), ("ΑΒ",),
                                               "uniform24"), Fraction(1, 24**2))

    def test_exact_single_shape(self):
        # Synthetic strings, not attested names.
        self.assertEqual(exact_slot_probability(frozenset({"ΒΑΒ"}), ("ΒΑ",),
                                               "shape"), Fraction(1, 17*7))

    def test_union_shared_tail_distinct_first(self):
        self.assertEqual(exact_slot_probability(frozenset({"ΒΑΒ"}), ("ΒΑ", "ΓΑ"),
                                               "shape"), Fraction(2, 17*7))

    def test_union_against_independent_finite_enumeration(self):
        # Enumerate every unordered distinct pair of first consonants and vowel
        # tail, without calling the production layout/probability functions.
        synthetic = frozenset({"ΒΑ", "ΓΑ", "ΔΕ"})
        numerator = denominator = 0
        for pair in combinations(CONSONANTS, 2):
            for vowel in VOWELS:
                denominator += 1
                numerator += any(first + vowel in synthetic for first in pair)
        self.assertEqual(exact_slot_probability(synthetic, ("ΒΑ", "ΓΑ"), "shape"),
                         Fraction(numerator, denominator))

    def test_csv_header_and_zero_rows_fail(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
            path = Path(folder) / "synthetic.csv"
            for text in ("", "wrong,header\n", "name_id,greek_form\n"):
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_corpus(path, "reject")
            path.write_text("name_id,greek_form\nx,Latin\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_corpus(path, "reject")

    def test_csv_form_dedup_and_bearer_neutrality(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
            path = Path(folder) / "synthetic.csv"
            path.write_text("name_id,greek_form\nx,ΒΑ\nx,ΒΑ\ny,ΒΑ\n", encoding="utf-8")
            names, by_id, rejected, subs = load_corpus(path, "reject")
            self.assertEqual(names, frozenset({"ΒΑ"}))
            self.assertEqual(set(by_id), {"x", "y"})
            self.assertEqual((rejected, subs), ([], []))

    def test_nested_reading_is_subsumed(self):
        self.assertEqual(collapse_nested(("ΒΒ", "ΒΒΑ")), ("ΒΒ",))
        names = frozenset({"ΒΒΑ"})
        self.assertEqual(exact_slot_probability(names, ("ΒΒ", "ΒΒΑ"), "shape"),
                         exact_slot_probability(names, ("ΒΒ",), "shape"))

    def test_empty_and_saturated_support(self):
        self.assertEqual(exact_slot_probability(frozenset(), ("ΒΑ",), "shape"), 0)
        full = frozenset(c+v for c in CONSONANTS for v in VOWELS)
        self.assertEqual(exact_slot_probability(full, ("ΒΑ", "ΓΑ"), "shape"), 1)

    def test_pmf_exact(self):
        self.assertEqual(poisson_binomial([Fraction(1,2), Fraction(1,3)]),
                         [Fraction(1,3), Fraction(1,2), Fraction(1,6)])

    def test_type_duplicates_and_group_statistic(self):
        self.assertEqual(score(frozenset({"ΒΑ", "ΒΑΒ", "ΒΑΓ"}), (("ΒΑ",),)), 1)

    def test_mc_seed_reproducibility_and_exact_agreement(self):
        names = frozenset(c+v for c in CONSONANTS[:8] for v in VOWELS)
        a = monte_carlo(names, (("ΒΑ",),), "shape", 10000, 1729)
        self.assertEqual(a, monte_carlo(names, (("ΒΑ",),), "shape", 10000, 1729))
        exact = float(exact_slot_probability(names, ("ΒΑ",), "shape"))
        self.assertLess(abs(a["upper_tail_plus_one"]-exact), .025)


if __name__ == "__main__":
    unittest.main()
