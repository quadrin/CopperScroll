"""score.py on a toy table (synthetic data; no real reading is implied).

Run from the repository root:
    python3 -I -m unittest discover -s research/text/edition_confusions/tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import score  # noqa: E402

EVENTS = [('ב–כ', 'I 1 w0', ''), ('ב–כ', 'I 2 w0', ''), ('ב–כ', 'I 3 w0', ''),
          ('ד–ר', 'I 4 w0', ''), ('ה–ח', 'II 1 w0', 'rj:t1')]
YW = [('I 5 w0', '')]


def run(loc, a, b, **kw):
    return score.score(loc, a, b, events=EVENTS, yw_events=YW, **kw)


class TestScore(unittest.TestCase):
    def test_common_pair(self):
        r = run('II 5', 'בדין', 'כדין')
        s = r['shape'][0]
        self.assertEqual((s['pair'], s['loo_places'], s['flag']), ('ב–כ', 3, 'COMMON'))
        self.assertAlmostEqual(s['rate'], round(4 / (5 + 231), 6))
        self.assertLessEqual(s['ci90'][0], s['ci90'][1])
        self.assertFalse(r['needs_rare_confusion'])

    def test_leave_one_place_out(self):
        s = run('I 1', 'בדין', 'כדין', words=[0])['shape'][0]
        self.assertEqual((s['loo_places'], s['flag']), (2, 'UNCOMMON'))
        s = run('I 1', 'בדין', 'כדין', words=[3])['shape'][0]
        self.assertEqual(s['loo_places'], 3)
        s = run('I 1', 'בדין', 'כדין')['shape'][0]  # no word given: the whole line is left out
        self.assertEqual(s['loo_places'], 2)

    def test_rare_pair(self):
        r = run('III 1', 'אבג', 'אבד')
        self.assertEqual(r['shape'][0]['flag'], 'RARE')
        self.assertEqual(r['shape'][0]['rate'], round(1 / (5 + 231), 6))
        self.assertTrue(r['needs_rare_confusion'])

    def test_yod_waw_is_matres_not_rare(self):
        r = run('III 1', 'חפור', 'חפיר')
        self.assertEqual(r['shape'], [])
        self.assertEqual(r['yod_waw'][0]['flag'], 'MATRES')
        self.assertFalse(r['needs_rare_confusion'])

    def test_record_rows_left_out(self):
        self.assertEqual(run('III 2', 'הה', 'הח')['shape'][0]['loo_places'], 1)
        self.assertEqual(run('III 2', 'הה', 'הח', rj_id='t1')['shape'][0]['flag'], 'RARE')

    def test_indels_reported_not_flagged(self):
        r = run('III 1', 'אבג', 'אבגד')
        self.assertEqual(r['insertions'], ['ד'])
        self.assertFalse(r['needs_rare_confusion'])

    def test_refuses_reserved_lines(self):
        with self.assertRaises(ValueError):
            run('XII 10', 'אב', 'אג')
        with self.assertRaises(ValueError):
            run('XI 3', 'אב', 'אג', also=[('XII', 9, None)])

    def test_alternatives_split(self):
        self.assertEqual(sorted(score.split_alternatives('ḥrwbh / ḥrwbhʾ')), ['ḥrwbh', 'ḥrwbhʾ'])
        self.assertEqual(sorted(score.split_alternatives('תב/רקע')), ['תבקע', 'תרקע'])


if __name__ == '__main__':
    unittest.main()
