"""The hard exclusion: no position in column XII lines 8-12 and nothing about the 21/22 cut
may appear in any data file of this folder. This test fails if one does.

Run from the repository root:
    python3 -I -m unittest discover -s research/text/edition_confusions/tests -v
"""
import csv
import json
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from exclusion import is_excluded, ref_excluded, mentions_excluded  # noqa: E402
import score  # noqa: E402

DATA_FILES = ['variants_manual.csv', 'ap_variants.csv', 'ap_overrides.csv', 'variants.csv',
              'confusions.csv', 'confusions.json', 'scored_readings.csv']


class TestRule(unittest.TestCase):
    def test_positions(self):
        for line in range(8, 13):
            self.assertTrue(is_excluded('XII', line))
            self.assertTrue(is_excluded('12', str(line)))
        for col, line in [('XII', 7), ('XII', 13), ('XI', 10), ('I', 10)]:
            self.assertFalse(is_excluded(col, line))
        self.assertTrue(is_excluded('XII', None))
        self.assertTrue(ref_excluded('XII 10'))
        self.assertFalse(ref_excluded('XI 12'))

    def test_text_mentions(self):
        for s in ['see XII 10', 'XII:9', 'Lefkovits 12:11', 'the 21/22 cut', 'cuts 21–22']:
            self.assertTrue(mentions_excluded(s), s)
        for s in ['XI 12', 'XII 4', 'p. 12', '12:4', 'XII 13', 'pp. 112']:
            self.assertFalse(mentions_excluded(s), s)


class TestDataFiles(unittest.TestCase):
    def test_no_excluded_text(self):
        for name in DATA_FILES:
            text = (HERE / name).read_text(encoding='utf-8')
            self.assertFalse(mentions_excluded(text), f'{name} names the excluded zone')

    def test_no_excluded_rows(self):
        for name in DATA_FILES:
            if not name.endswith('.csv'):
                continue
            with open(HERE / name, encoding='utf-8', newline='') as f:
                for r in csv.DictReader(f):
                    if 'column' in r and r.get('line'):
                        self.assertFalse(is_excluded(r['column'], r['line']), f"{name}: {r['column']} {r['line']}")
                    if r.get('location'):
                        self.assertFalse(ref_excluded(r['location']), f"{name}: {r['location']}")
                    for k in ('places', 'shape_events', 'yod_waw_events'):
                        for item in filter(None, (r.get(k) or '').split(';')):
                            ref = item.split('@')[-1]
                            self.assertFalse(ref_excluded(' '.join(ref.split()[:2])), f'{name}: {item}')

    def test_no_excluded_places_in_json(self):
        d = json.loads((HERE / 'confusions.json').read_text(encoding='utf-8'))
        places = [p for r in d['unordered'] for p in r['places'].split(';')]
        places += d['yod_waw_vowel_letter_places']['places']
        self.assertTrue(places)
        for p in places:
            self.assertFalse(ref_excluded(' '.join(p.split()[:2])), p)

    def test_score_refuses_excluded_location(self):
        for line in range(8, 13):
            with self.assertRaises(ValueError):
                score.score(f'XII {line}', 'בדין', 'כדין', events=[], yw_events=[])

    @unittest.skipUnless(os.environ.get('PUECH2015'), 'set PUECH2015 to the local extract to test the parser')
    def test_puech_parser_drops_excluded_lines(self):
        import build_ap
        lines = build_ap.parse_puech_lines(Path(os.environ['PUECH2015']))
        self.assertTrue(lines)
        self.assertFalse(any(is_excluded(c, l) for c, l in lines))


if __name__ == '__main__':
    unittest.main()
