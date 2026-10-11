"""Test of the exploratory IAA view (PLAN_AMENDMENT_IAA_2026-10-11.md).

Run from the repository root:  python3 -I -B -m unittest discover -s research/regional/tombs/tests -v
Checks: the amendment's hash and commit; that scripts/iaa_view.py reproduces its outputs (it also checks internally
that the frozen units reproduce scores_summary.csv and amendment1_scores_summary.csv) without touching the frozen
tables; that the view's frozen columns equal scores_summary.csv; and that the union adds exactly the non-duplicate
IAA units of each region and date set.
"""
import csv
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(FOLDER, '..', '..', '..'))
AMEND = 'research/regional/tombs/PLAN_AMENDMENT_IAA_2026-10-11.md'
AMEND_SHA = '980a020b4057c447f5127ab60fc1b25f69f27160623414b9183e04300fd1aad0'
AMEND_COMMIT = 'c14468e802422d89b3933f79aba244e9c6c33ff2'
VIEW_OUT = ['iaa_units.csv', 'iaa_scores.csv', 'iaa_view_2026-10-11.csv', 'iaa_amendment1_view.csv', 'iaa_summary.json']
FROZEN_OUT = ['tombs.csv', 'scores.csv', 'scores_summary.csv', 'features_summary.csv', 'amendment1_codes.csv',
              'amendment1_scores_summary.csv']


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(name):
    with open(os.path.join(FOLDER, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


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
            subprocess.run([sys.executable, '-I', '-B', os.path.join(FOLDER, 'scripts', 'iaa_view.py')], cwd=REPO,
                           check=True, capture_output=True)
            self.assertEqual(before, {n: sha(os.path.join(FOLDER, n)) for n in VIEW_OUT + FROZEN_OUT})
        finally:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(tmp, n), os.path.join(FOLDER, n))
            shutil.rmtree(tmp)

    def test_frozen_columns_and_union(self):
        committed = {(r['branch'], r['region'], r['date_set']): r for r in read('scores_summary.csv')
                     if r['view'] == 'all_lineages'}
        units = [u for u in read('iaa_units.csv') if u['kind'] == 'primary' and not u['possible_duplicate_of']]

        def n_new(reg, ds):
            def inr(u):
                return {'A': u['in_A'] == 'yes', 'A3': u['in_A3'] == 'yes', 'B': 'yes' in (u['in_B1'], u['in_B2']),
                        'B1': u['in_B1'] == 'yes', 'B2': u['in_B2'] == 'yes', 'B2_5': u['in_B2_5'] == 'yes',
                        'AB': 'yes' in (u['in_A'], u['in_B1'], u['in_B2'])}[reg]
            return sum(1 for u in units if inr(u) and {'strict': u['dated_in_window'] == 'yes',
                                                       'lenient': u['dated_lenient'] == 'yes', 'any': True}[ds])
        view = read('iaa_view_2026-10-11.csv')
        self.assertTrue(view)
        for r in view:
            c = committed[(r['branch'], r['region'], r['date_set'])]
            self.assertEqual([r['frozen_N'], r['frozen_k'], r['frozen_f'], r['frozen_m']],
                             [c['N'], c['k_match'], c['f_fail'], c['m_unknown']])
            self.assertEqual(int(r['union_N']) - int(r['frozen_N']), n_new(r['region'], r['date_set']))
            self.assertEqual(int(r['union_k']) + int(r['union_f']) + int(r['union_m']), int(r['union_N']))


if __name__ == '__main__':
    unittest.main()
