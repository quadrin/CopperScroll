"""Test of the exploratory IAA view (PLAN_AMENDMENT_IAA_2026-10-11.md).

Run from the repository root:  python3 -I -m unittest discover -s research/regional/water_systems/tests -v
Checks: the amendment's hash and commit; that scripts/iaa_view.py reproduces its outputs (it also checks internally
that the frozen build_water and score, run on the committed survey_rows.csv, reproduce counts.csv and headline.csv)
without touching the frozen tables; that the view's frozen columns equal counts.csv; and that every IAA-row MATCH in
a non-trivial clause has a post-hoc reading.
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
LANE = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(LANE, '..', '..', '..'))
AMEND = 'research/regional/water_systems/PLAN_AMENDMENT_IAA_2026-10-11.md'
AMEND_SHA = '8387f23fdf84009a8746cf6c49ec90f41ea194de406082d37c511e77f54371c6'
AMEND_COMMIT = '1804f6dc027fa50db3aca7c0f7e1f16ccbb218e5'
VIEW_OUT = ['iaa_survey_rows.csv', 'iaa_counts.csv', 'iaa_headline.csv', 'iaa_view_2026-10-11.csv', 'iaa_summary.json']
FROZEN_OUT = ['water.csv', 'scores.csv', 'merged_units.csv', 'merged_scores.csv', 'counts.csv', 'headline.csv',
              'survey_rows.csv']


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(name):
    with open(os.path.join(LANE, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


class TestIAAView(unittest.TestCase):
    def test_amendment(self):
        self.assertEqual(sha(os.path.join(REPO, AMEND)), AMEND_SHA)
        r = subprocess.run(['git', 'show', '--name-only', '--format=', AMEND_COMMIT], cwd=REPO, capture_output=True, text=True)
        if r.returncode != 0:
            self.skipTest('amendment commit not in this clone')
        self.assertEqual(r.stdout.split(), [AMEND])

    def test_reproduces_and_frozen_untouched(self):
        before = {n: sha(os.path.join(LANE, n)) for n in VIEW_OUT + FROZEN_OUT}
        tmp = tempfile.mkdtemp()
        try:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(LANE, n), os.path.join(tmp, n))
            subprocess.run([sys.executable, '-I', os.path.join(LANE, 'scripts', 'iaa_view.py')], cwd=REPO, check=True,
                           capture_output=True)
            self.assertEqual(before, {n: sha(os.path.join(LANE, n)) for n in VIEW_OUT + FROZEN_OUT})
        finally:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(tmp, n), os.path.join(LANE, n))
            shutil.rmtree(tmp)

    def test_frozen_columns_equal_counts(self):
        frozen = {(r['entry'], r['branch'], r['lineage'], r['date_rule']): r for r in read('counts.csv')}
        view = read('iaa_view_2026-10-11.csv')
        self.assertTrue(view)
        for r in view:
            f = frozen.get((r['entry'], r['branch'], r['lineage'], r['date_rule']))
            got = [r['frozen_N'], r['frozen_k'], r['frozen_f'], r['frozen_m']]
            self.assertEqual(got, [f['N'], f['k_match'], f['f_fail'], f['m_unknown']] if f else ['0', '0', '0', '0'])
            for pre in ('frozen', 'new', 'quoteonly'):
                self.assertEqual(int(r[f'{pre}_k']) + int(r[f'{pre}_f']) + int(r[f'{pre}_m']), int(r[f'{pre}_N']))

    def test_posthoc_readings_complete(self):
        checks = read('iaa_posthoc_checks.csv')
        self.assertTrue(all(c['verdict'] in ('confirmed', 'partly confirmed', 'not confirmed') and c['reason'] for c in checks))
        out = subprocess.run([sys.executable, '-I', os.path.join(LANE, 'scripts', 'iaa_view.py'), '--posthoc'], cwd=REPO,
                             check=True, capture_output=True, text=True).stdout
        self.assertEqual(out.strip(), '')


if __name__ == '__main__':
    unittest.main()
