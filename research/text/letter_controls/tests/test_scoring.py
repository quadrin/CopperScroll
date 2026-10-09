"""Tests for scoring.py. All data here are synthetic; no reading of any scroll image is implied.

Run from the repository root:
    python3 -I -m unittest discover -s research/text/letter_controls/tests -v
"""
import contextlib
import csv
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scoring  # noqa: E402


def make_key(question='BK', n_per_class=20, damage_every=2, n_decoys=4, series='S1', targets=1):
    classes = scoring.CLASSES[question]
    items = []
    n = 0
    for c in classes:
        count = n_per_class if c != 'ת' else max(6, n_per_class // 2)
        for i in range(count):
            n += 1
            items.append({'item_code': f'C{n:03d}', 'kind': 'control', 'question': question, 'answer': c,
                          'series': series, 'damage': 'cut_edge' if i % damage_every == 0 else 'intact'})
    for i in range(n_decoys):
        items.append({'item_code': f'D{i:03d}', 'kind': 'decoy', 'question': question, 'answer': 'illegible',
                      'series': series, 'damage': 'edge_loss'})
    for i in range(targets):
        items.append({'item_code': f'T{i:03d}', 'kind': 'target_slot', 'question': question, 'answer': None,
                      'series': series, 'damage': 'cut_edge'})
    return {'schema': 'letter_controls_key/1', 'items': items}


def truthful(item, question):
    if item['kind'] == 'decoy':
        return 'illegible', 'illegible'
    if item['kind'] == 'target_slot':
        return scoring.CLASSES[question][0] if question != 'XS' else 'absent', 'certain'
    a = item['answer']
    if question == 'XS':
        a = 'sign' if a == 'present' else 'absent'
    return a, 'certain'


def swapped(item, question):
    if item['kind'] != 'control':
        return truthful(item, question)
    classes = scoring.CLASSES[question]
    other = classes[(classes.index(item['answer']) + 1) % len(classes)]
    if question == 'XS':
        other = 'sign' if other == 'present' else 'absent'
    return other, 'certain'


class Harness:
    def __init__(self, tmp, key):
        self.tmp = Path(tmp)
        self.key_path = self.tmp / 'key.json'
        self.key_path.write_text(json.dumps(key, ensure_ascii=False), encoding='utf-8')
        self.key = key

    def responses(self, reader, rule, question, overrides=None, skip=()):
        path = self.tmp / f'{reader}.csv'
        with path.open('w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(scoring.RESPONSE_FIELDS)
            for it in self.key['items']:
                if it['item_code'] in skip:
                    continue
                ans, grade = rule(it, question)
                if overrides and it['item_code'] in overrides:
                    ans, grade = overrides[it['item_code']]
                w.writerow([reader, it['item_code'], ans, grade, 'no', '2026-10-08T00:00:00Z', ''])
        return path

    def run(self, paths, readers=None):
        _, items = scoring.load_key(self.key_path)
        return scoring.score(items, scoring.load_responses(paths, items), readers)


class BoundsTest(unittest.TestCase):
    def test_all_correct_lower_bound(self):
        self.assertAlmostEqual(scoring.cp_lower(29, 29), 0.05 ** (1 / 29), places=6)
        self.assertGreaterEqual(scoring.cp_lower(29, 29), 0.90)
        self.assertLess(scoring.cp_lower(28, 28), 0.90)

    def test_zero_upper_bound_and_symmetry(self):
        self.assertAlmostEqual(scoring.cp_upper(0, 10), 1 - 0.05 ** (1 / 10), places=6)
        for k, n in ((3, 17), (10, 40), (45, 46)):
            self.assertAlmostEqual(scoring.cp_lower(k, n), 1 - scoring.cp_upper(n - k, n), places=6)

    def test_one_error_needs_more_calls(self):
        self.assertLess(scoring.cp_lower(44, 45), 0.90)
        self.assertGreaterEqual(scoring.cp_lower(45, 46), 0.90)


class ScoringTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp = self.tmpdir.name

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_perfect_readers_pass(self):
        h = Harness(self.tmp, make_key('BK'))
        rep = h.run([h.responses('A', truthful, 'BK'), h.responses('B', truthful, 'BK')])
        res = rep['series']['S1']['BK']
        self.assertEqual(res['status'], 'PASS')
        self.assertEqual(res['joint']['decisive'], 40)
        cm = res['per_reader']['A']['confusion_matrix_all_grades']
        self.assertEqual(cm['ב']['ב'], 20)
        self.assertEqual(cm['כ']['כ'], 20)
        self.assertEqual(cm['illegible']['illegible'], 4)
        self.assertEqual(res['per_reader']['A']['accuracy'], 1.0)
        self.assertIn('Agreement alone measures nothing about accuracy', res['statement'])

    def test_agreeing_but_wrong_readers_fail(self):
        h = Harness(self.tmp, make_key('BK'))
        rep = h.run([h.responses('A', swapped, 'BK'), h.responses('B', swapped, 'BK')])
        res = rep['series']['S1']['BK']
        self.assertEqual(res['joint']['agreement_rate'], 1.0)
        self.assertEqual(res['joint']['agreements_wrong'], 40)
        self.assertEqual(res['per_reader']['A']['accuracy'], 0.0)
        self.assertEqual(res['status'], 'FAIL')

    def test_decoy_overcall_fails(self):
        h = Harness(self.tmp, make_key('BK'))
        over = {'D000': ('ב', 'certain')}
        rep = h.run([h.responses('A', truthful, 'BK', over), h.responses('B', truthful, 'BK', over)])
        res = rep['series']['S1']['BK']
        self.assertEqual(res['joint']['decoy_decisive'], 1)
        self.assertEqual(res['status'], 'FAIL')
        self.assertEqual(res['per_reader']['A']['decoy_overcalls_certain'], 1)

    def test_one_damage_matched_error_fails_despite_bound(self):
        h = Harness(self.tmp, make_key('BK', n_per_class=25))
        wrong = {'C001': ('כ', 'certain')}  # C001 is a damage-matched bet
        rep = h.run([h.responses('A', truthful, 'BK', wrong), h.responses('B', truthful, 'BK', wrong)])
        res = rep['series']['S1']['BK']
        self.assertGreaterEqual(res['joint']['decisive_precision_lower_bound'], 0.90)
        self.assertEqual(res['joint']['decisive_wrong_damage_matched'], 1)
        self.assertEqual(res['status'], 'FAIL')

    def test_too_few_controls_is_insufficient(self):
        h = Harness(self.tmp, make_key('BK', n_per_class=15))
        rep = h.run([h.responses('A', truthful, 'BK'), h.responses('B', truthful, 'BK')])
        res = rep['series']['S1']['BK']
        self.assertEqual(res['status'], 'INSUFFICIENT')
        self.assertTrue(any('keyed controls' in r for r in res['reasons']))

    def test_missing_response_is_insufficient(self):
        h = Harness(self.tmp, make_key('BK'))
        rep = h.run([h.responses('A', truthful, 'BK', skip={'C005'}), h.responses('B', truthful, 'BK')])
        self.assertEqual(rep['series']['S1']['BK']['status'], 'INSUFFICIENT')

    def test_uncertain_readers_are_not_decisive(self):
        h = Harness(self.tmp, make_key('BK'))
        probable = lambda it, q: (truthful(it, q)[0], 'probable' if it['kind'] == 'control' else truthful(it, q)[1])
        rep = h.run([h.responses('A', probable, 'BK'), h.responses('B', probable, 'BK')])
        res = rep['series']['S1']['BK']
        self.assertEqual(res['joint']['decisive'], 0)
        self.assertEqual(res['status'], 'FAIL')
        self.assertEqual(res['per_reader']['A']['accuracy'], 1.0)

    def test_xs_mark_not_sign_counts_as_absent(self):
        key = make_key('XS')
        h = Harness(self.tmp, key)
        marks = {it['item_code']: ('mark_not_sign', 'certain') for it in key['items']
                 if it['kind'] == 'control' and it['answer'] == 'absent'}
        rep = h.run([h.responses('A', truthful, 'XS', marks), h.responses('B', truthful, 'XS')])
        res = rep['series']['S1']['XS']
        self.assertEqual(res['per_reader']['A']['accuracy'], 1.0)
        self.assertEqual(res['status'], 'PASS')

    def test_taw_minimum_and_three_way_matrix(self):
        h = Harness(self.tmp, make_key('HH', n_per_class=14))
        rep = h.run([h.responses('A', truthful, 'HH'), h.responses('B', swapped, 'HH')])
        res = rep['series']['S1']['HH']
        self.assertEqual(res['n_controls'], 14 + 14 + 7)
        self.assertTrue(any('keyed controls' in r for r in res['reasons']))
        cm = res['per_reader']['B']['confusion_matrix_all_grades']
        self.assertEqual(cm['ה']['ח'], 14)
        self.assertEqual(cm['ח']['ת'], 14)
        self.assertEqual(cm['ת']['ה'], 7)

    def test_likelihood_ratio_bounds(self):
        key = make_key('BK')
        h = Harness(self.tmp, key)
        # Reader A calls kaf on 18 of 20 kafs and on 2 of 20 bets.
        bets = [it['item_code'] for it in key['items'] if it['kind'] == 'control' and it['answer'] == 'ב'][:2]
        kafs = [it['item_code'] for it in key['items'] if it['kind'] == 'control' and it['answer'] == 'כ'][:2]
        over = {c: ('כ', 'probable') for c in bets}
        over.update({c: ('ב', 'probable') for c in kafs})
        rep = h.run([h.responses('A', truthful, 'BK', over), h.responses('B', truthful, 'BK')])
        lr = rep['series']['S1']['BK']['per_reader']['A']['likelihood_ratios']['כ']
        self.assertEqual((lr['called_when_true'], lr['called_when_other']), (18, 2))
        self.assertAlmostEqual(lr['lr_point'], 9.0, places=4)
        expected = scoring.cp_lower(18, 20) / scoring.cp_upper(2, 20)
        self.assertAlmostEqual(lr['lr_lower_bound'], round(expected, 4), places=4)

    def test_target_slots_are_reported_not_scored(self):
        h = Harness(self.tmp, make_key('BK', targets=1))
        rep = h.run([h.responses('A', truthful, 'BK'), h.responses('B', truthful, 'BK')])
        res = rep['series']['S1']['BK']
        self.assertEqual(res['n_controls'], 40)
        self.assertEqual(len(res['targets']), 1)
        t = res['targets'][0]
        self.assertTrue(t['frozen_rule_decisive_in_this_block'])
        self.assertEqual(t['calibration_status'], 'PASS')
        self.assertIn('frozen', t['use'])

    def test_unusually_confident_target_flag(self):
        key = make_key('BK')
        h = Harness(self.tmp, key)
        # Readers hedge on every damage-matched control but are certain on the target slot.
        hedge = {it['item_code']: (it['answer'], 'probable') for it in key['items']
                 if it['kind'] == 'control' and it['damage'] == 'cut_edge'}
        rep = h.run([h.responses('A', truthful, 'BK', hedge), h.responses('B', truthful, 'BK', hedge)])
        t = rep['series']['S1']['BK']['targets'][0]
        self.assertTrue(t['frozen_rule_decisive_in_this_block'])
        self.assertTrue(t['unusually_confident'])
        self.assertEqual(t['damage_matched_decisive_rate'], 0.0)
        self.assertIn('fewer than a quarter', rep['series']['S1']['BK']['statement'])

    def test_extra_reader_does_not_enter_decisive_rule(self):
        h = Harness(self.tmp, make_key('BK'))
        paths = [h.responses('A', truthful, 'BK'), h.responses('B', truthful, 'BK'),
                 h.responses('C', swapped, 'BK', skip={'C001'})]
        with self.assertRaises(ValueError):
            h.run(paths)
        rep = h.run(paths, readers=['A', 'B'])
        res = rep['series']['S1']['BK']
        self.assertEqual(res['status'], 'PASS')
        self.assertEqual(res['per_reader']['C']['accuracy'], 0.0)

    def test_unassigned_series_not_scored(self):
        h = Harness(self.tmp, make_key('BK', series='unassigned'))
        rep = h.run([h.responses('A', truthful, 'BK'), h.responses('B', truthful, 'BK')])
        self.assertEqual(rep['series'], {})
        self.assertIn('nothing to score', rep['statement'])

    def test_validation_errors(self):
        h = Harness(self.tmp, make_key('BK'))
        good = h.responses('A', truthful, 'BK')
        cases = {
            'unknown': 'A,ZZZ,ב,certain,no,2026-10-08T00:00:00Z,\n',
            'grade': 'A,C001,ב,sure,no,2026-10-08T00:00:00Z,\n',
            'answer': 'A,C001,ה,certain,no,2026-10-08T00:00:00Z,\n',
            'illegible_mismatch': 'A,C001,illegible,certain,no,2026-10-08T00:00:00Z,\n',
            'unlocked': 'A,C001,ב,certain,no,,\n',
        }
        for name, line in cases.items():
            p = Path(self.tmp) / f'bad_{name}.csv'
            p.write_text(','.join(scoring.RESPONSE_FIELDS) + '\n' + line, encoding='utf-8')
            with self.assertRaises(ValueError, msg=name):
                h.run([p])
        with self.assertRaises(ValueError):
            h.run([good, good])  # duplicate responses

    def test_key_hash_check(self):
        h = Harness(self.tmp, make_key('BK'))
        right = hashlib.sha256(h.key_path.read_bytes()).hexdigest()
        scoring.load_key(h.key_path, right)
        with self.assertRaises(ValueError):
            scoring.load_key(h.key_path, '0' * 64)

    def test_bad_key_rejected(self):
        key = make_key('BK')
        key['items'][0]['answer'] = 'ה'
        with self.assertRaises(ValueError):
            Harness(self.tmp, key).run([])

    def test_cli_is_deterministic(self):
        h = Harness(self.tmp, make_key('BK'))
        a, b = h.responses('A', truthful, 'BK'), h.responses('B', swapped, 'BK')
        outs = []
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            for i in range(2):
                j = Path(self.tmp) / f'r{i}.json'
                code = scoring.main(['--key', str(h.key_path), '--responses', str(a), str(b), '--json', str(j)])
                self.assertEqual(code, 0)
                outs.append(j.read_text(encoding='utf-8'))
            bad = scoring.main(['--key', str(h.key_path), '--responses', str(a), '--expect-sha256', '0' * 64])
        self.assertEqual(outs[0], outs[1])
        self.assertEqual(bad, 2)
        self.assertIn('Agreement alone measures nothing', sink.getvalue())


if __name__ == '__main__':
    unittest.main()
