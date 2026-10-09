"""Consistency tests for controls_manifest.csv and its builder.

Run from the repository root:
    python3 -I -m unittest discover -s research/text/letter_controls/tests -v
"""
import contextlib
import csv
import io
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_manifest as bm  # noqa: E402
import scoring  # noqa: E402

MANIFEST = HERE.parent / 'controls_manifest.csv'


def rows():
    with MANIFEST.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


class ManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = rows()
        cls.letters, _ = bm.load_letters()
        cls.edition = {(r['ref'], int(r['word_index'])): r for r in bm.read_csv(bm.INPUTS['edition_checks'])}

    def test_manifest_is_current(self):
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink):
            code = bm.main(['--check'])
        self.assertEqual(code, 0, sink.getvalue())

    def test_columns_and_fields(self):
        with MANIFEST.open(encoding='utf-8', newline='') as f:
            self.assertEqual(next(csv.reader(f)), bm.FIELDS)
        for r in self.rows:
            if r['use'] == 'target_slot':
                self.assertEqual(r['ref'], 'XII 10')
                self.assertEqual(r['crop_box'], '')
                continue
            self.assertLessEqual(bm.COL[r['column']], 10, r['candidate_id'])

    def test_no_letter_used_twice(self):
        seen = set()
        for r in self.rows:
            if r['use'] in ('control', 'decoy'):
                k = (r['ref'], r['word_index'], r['char_index'])
                self.assertNotIn(k, seen, r['candidate_id'])
                seen.add(k)

    def test_answers_and_tiers(self):
        for r in self.rows:
            if r['use'] == 'control':
                self.assertIn(r['secure_answer'], scoring.CLASSES[r['question']], r['candidate_id'])
                self.assertIn(r['tier'], ('A', 'B'))
                L = self.letters[(r['ref'], int(r['word_index']), int(r['char_index']))]
                self.assertEqual(bm.norm(L['letter']) if r['question'] != 'XS' else L['base'],
                                 r['secure_answer'] if r['question'] != 'XS' else L['base'])
                if r['tier'] == 'A':
                    self.assertEqual(L['flag'], '')
                    self.assertTrue(L['t10'])
                    self.assertIn(self.edition[(r['ref'], int(r['word_index']))]['puech2015'],
                                  ('same', 'same_adjacent_lacuna'))
                else:
                    self.assertIn('Lefkovits', r['edition_notes'] + r['why_secure'])
                    self.assertNotEqual(r['damage_from_editions'], '')
            elif r['use'] == 'decoy':
                self.assertEqual(r['secure_answer'], 'illegible')
                L = self.letters[(r['ref'], int(r['word_index']), int(r['char_index']))]
                self.assertEqual(L['flag'], 'r')

    def test_plate_check_lines_only_by_readmission(self):
        pc = bm.plate_check_lines()
        manual = bm.load_manual()
        for r in self.rows:
            if r['use'] == 'control' and r['ref'] in pc:
                self.assertTrue(any(m['action'] == 'readmit' and m['ref'] == r['ref'] for m in manual), r['candidate_id'])

    def test_exclusions_respected(self):
        manual = [m for m in bm.load_manual() if m['action'] == 'exclude']
        for r in self.rows:
            if r['use'] != 'control':
                continue
            for m in manual:
                self.assertFalse(bm.manual_matches(m, r['ref'], r['etcbc_word'], int(r['char_index'])),
                                 f"{r['candidate_id']} hits exclusion {m['ref']} {m['etcbc_word']}")

    def test_sealed_hash_column(self):
        recorded = bm.current_sealed_sha()
        for r in self.rows:
            self.assertEqual(r['sealed_key_sha256'], recorded)

    def test_minimum_pool_sizes(self):
        counts = {}
        for r in self.rows:
            if r['use'] == 'control':
                counts[(r['question'], r['secure_answer'])] = counts.get((r['question'], r['secure_answer']), 0) + 1
        for (q, c), need in {('BK', 'ב'): 24, ('BK', 'כ'): 24, ('HH', 'ה'): 24, ('HH', 'ח'): 24,
                             ('HH', 'ת'): 12, ('XS', 'present'): 24, ('XS', 'absent'): 24}.items():
            self.assertGreaterEqual(counts.get((q, c), 0), need, (q, c))


class CompareWordTest(unittest.TestCase):
    def test_compare_rules(self):
        self.assertEqual(bm.compare_word(['כסף'], 'כסף'), 'same')
        self.assertEqual(bm.compare_word(['בירכ'], 'בירך'), 'same')
        self.assertEqual(bm.compare_word(['עסרין['], 'עסרין'), 'same_adjacent_lacuna')
        self.assertEqual(bm.compare_word(['[ה]פתחין'], 'הפתחין'), 'restored')
        self.assertEqual(bm.compare_word(['השל<י>שי'], 'השלישי'), 'corrected')
        self.assertEqual(bm.compare_word(['בדין'], 'כדין'), 'differs')


if __name__ == '__main__':
    unittest.main()
