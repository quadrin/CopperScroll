"""Test of the exploratory IAA view (PLAN_AMENDMENT_IAA_2026-10-11.md). Standard library unittest.

Run from the repository root:  python3 -I -m unittest discover -s research/regional/columbaria/tests -v
Checks: the amendment's hash and commit; that scripts/iaa_view.py reproduces its outputs without touching the frozen
tables; that the view's frozen columns equal summary.json; that union = frozen + IAA rows; and that every hand
duplicate decision is used.
"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(FOLDER, '..', '..', '..'))
AMEND = 'research/regional/columbaria/PLAN_AMENDMENT_IAA_2026-10-11.md'
AMEND_SHA = '3187592c5b9f6cbef5d0935a90b051fc952dac70632b6c1dae6bec91448e7ff4'
AMEND_COMMIT = 'b96833a3bd1b6d9496cd4aa384eb48220101d8ae'
VIEW_OUT = ['iaa_rows.csv', 'iaa_excluded.csv', 'iaa_scores.csv', 'iaa_summary.json', 'iaa_view_2026-10-11.csv']
FROZEN_OUT = ['columbaria.csv', 'scores.csv', 'summary.json']


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


class TestIAAView(unittest.TestCase):
    def test_amendment(self):
        self.assertEqual(sha(os.path.join(REPO, AMEND)), AMEND_SHA)
        r = subprocess.run(['git', 'show', '--name-only', '--format=', AMEND_COMMIT], cwd=REPO, capture_output=True, text=True)
        if r.returncode != 0:
            self.skipTest('amendment commit not in this clone')
        self.assertEqual(r.stdout.split(), [AMEND])

    def test_reproduces_and_frozen_untouched(self):
        before = {n: sha(os.path.join(FOLDER, n)) for n in VIEW_OUT + FROZEN_OUT}
        tmp = tempfile.mkdtemp()
        try:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(FOLDER, n), os.path.join(tmp, n))
            subprocess.run([sys.executable, '-I', os.path.join(FOLDER, 'scripts', 'iaa_view.py')], cwd=REPO, check=True,
                           capture_output=True)
            self.assertEqual(before, {n: sha(os.path.join(FOLDER, n)) for n in VIEW_OUT + FROZEN_OUT})
        finally:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(tmp, n), os.path.join(FOLDER, n))
            shutil.rmtree(tmp)

    def test_frozen_columns_and_union(self):
        with open(os.path.join(FOLDER, 'summary.json'), encoding='utf-8') as f:
            summ = json.load(f)['scopes']
        with open(os.path.join(FOLDER, 'iaa_view_2026-10-11.csv'), encoding='utf-8') as f:
            view = list(csv.DictReader(f))
        self.assertTrue(view)
        for r in view:
            src = summ[r['scope']]['headline' if r['kind'] == 'headline' else 'clauses'][r['key']]
            self.assertEqual([int(r[k]) for k in ('frozen_N', 'frozen_k', 'frozen_f', 'frozen_m')],
                             [src['N'], src['k_match'], src['f_fail'], src['m_unknown']])
            for x in ('N', 'k', 'f', 'm'):
                self.assertEqual(int(r[f'union_{x}']), int(r[f'frozen_{x}']) + int(r[f'iaa_{x}']))

    def test_every_decision_is_a_listed_pair(self):
        with open(os.path.join(FOLDER, 'data', 'iaa_dedup_decisions.csv'), encoding='utf-8') as f:
            dec = list(csv.DictReader(f))
        out = subprocess.run([sys.executable, '-I', os.path.join(FOLDER, 'scripts', 'iaa_view.py'), '--pairs'], cwd=REPO,
                             check=True, capture_output=True, text=True).stdout
        pairs = {(p['iaa_id'], p['other_id']) for p in map(json.loads, out.splitlines())}
        self.assertEqual(pairs, {(d['iaa_id'], d['other_id']) for d in dec})
        self.assertTrue(all(d['decision'] in ('same', 'different') and d['reason'] for d in dec))


if __name__ == '__main__':
    unittest.main()
