"""Test of the exploratory phase-4 view (PLAN_AMENDMENT_PHASE4_2026-10-12.md).

Run from the repository root:  python3 -I -m unittest discover -s research/regional/water_systems/tests -v
Checks: the amendment's hash and that its commit holds it alone; that scripts/phase4_view.py reproduces its outputs
(it also checks internally that the frozen build_water and score reproduce counts.csv and headline.csv, and that the
IAA view inputs reproduce iaa_counts.csv) without touching the frozen or IAA-view tables; that the view's frozen and
IAA columns equal counts.csv and iaa_counts.csv; that no held, Tell es-Sultan or Kh. Almit row is used; and that every
MATCH in a non-trivial clause has a post-hoc reading.
"""
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(LANE, '..', '..', '..'))
AMEND = 'research/regional/water_systems/PLAN_AMENDMENT_PHASE4_2026-10-12.md'
AMEND_SHA = '3112926d89e6197ae704b43a05672c8c7e96fe28f64a5100dfb577af11a5f977'
AMEND_COMMIT = '6508ab72894b678ac8fa7900fbd59ced814491f1'
VIEW_OUT = ['phase4_survey_rows.csv', 'phase4_counts.csv', 'phase4_headline.csv', 'phase4_view_2026-10-12.csv',
            'phase4_scores.csv', 'phase4_summary.json']
UNTOUCHED = ['water.csv', 'scores.csv', 'merged_units.csv', 'merged_scores.csv', 'counts.csv', 'headline.csv',
             'survey_rows.csv', 'iaa_survey_rows.csv', 'iaa_counts.csv', 'iaa_headline.csv', 'iaa_view_2026-10-11.csv',
             'iaa_summary.json', 'iaa_posthoc_checks.csv', 'phase4_posthoc_checks.csv']


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(name):
    with open(os.path.join(LANE, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


class TestPhase4View(unittest.TestCase):
    def test_amendment(self):
        self.assertEqual(sha(os.path.join(REPO, AMEND)), AMEND_SHA)
        r = subprocess.run(['git', 'show', '--name-only', '--format=', AMEND_COMMIT], cwd=REPO, capture_output=True,
                           text=True)
        if r.returncode != 0:
            self.skipTest('amendment commit not in this clone')
        self.assertEqual(r.stdout.split(), [AMEND])

    def test_reproduces_and_frozen_untouched(self):
        before = {n: sha(os.path.join(LANE, n)) for n in VIEW_OUT + UNTOUCHED}
        tmp = tempfile.mkdtemp()
        try:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(LANE, n), os.path.join(tmp, n))
            subprocess.run([sys.executable, '-I', os.path.join(LANE, 'scripts', 'phase4_view.py')], cwd=REPO,
                           check=True, capture_output=True)
            self.assertEqual(before, {n: sha(os.path.join(LANE, n)) for n in VIEW_OUT + UNTOUCHED})
        finally:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(tmp, n), os.path.join(LANE, n))
            shutil.rmtree(tmp)

    def test_frozen_and_iaa_columns(self):
        frozen = {(r['entry'], r['branch'], r['lineage'], r['date_rule']): r for r in read('counts.csv')}
        iaa = {(r['entry'], r['branch'], r['lineage'], r['date_rule']): r for r in read('iaa_counts.csv')}
        view = read('phase4_view_2026-10-12.csv')
        self.assertTrue(view)
        for r in view:
            key = (r['entry'], r['branch'], r['lineage'], r['date_rule'])
            for pre, table in (('frozen', frozen), ('iaa', iaa)):
                f = table.get(key)
                got = [r[f'{pre}_N'], r[f'{pre}_k'], r[f'{pre}_f'], r[f'{pre}_m']]
                self.assertEqual(got, [f['N'], f['k_match'], f['f_fail'], f['m_unknown']] if f else ['0'] * 4)
            for pre in ('frozen', 'iaa', 'p13new', 'new', 'bracket', 'quoteonly', 'withswp'):
                self.assertEqual(int(r[f'{pre}_k']) + int(r[f'{pre}_f']) + int(r[f'{pre}_m']), int(r[f'{pre}_N']))
        # the primary view's counts are the full count table
        full = {(r['entry'], r['branch'], r['lineage'], r['date_rule']): r for r in read('phase4_counts.csv')}
        for r in view:
            f = full.get((r['entry'], r['branch'], r['lineage'], r['date_rule']))
            if f:
                self.assertEqual([r['new_N'], r['new_k']], [f['N'], f['k_match']])

    def test_no_protected_rows(self):
        held = set()
        p4 = os.path.join(REPO, 'research', 'regional', 'haesi_features', 'phase4_2026-10-11')
        for root, _, files in os.walk(p4):
            for fn in files:
                if fn.startswith('held') and fn.endswith('.csv'):
                    with open(os.path.join(root, fn), encoding='utf-8') as f:
                        held |= {r['unit_id'] for r in csv.DictReader(f)}
        self.assertTrue(held)
        for r in read('phase4_survey_rows.csv'):
            self.assertNotIn(r['record_id'], held)
            self.assertIsNone(re.search(r'almit|עלמית', r['name'] + r['record_id'], re.I))
            self.assertIsNone(re.search(r'\bt[ae]l+[- ]?(e[sl][- ])?sultan', r['name'], re.I))
            self.assertNotIn('SWP', r['source'])

    def test_summary_consistent(self):
        with open(os.path.join(LANE, 'phase4_summary.json'), encoding='utf-8') as f:
            s = json.load(f)
        rows = read('phase4_survey_rows.csv')
        self.assertEqual(s['merged_rows_in_box'], len(rows))
        self.assertEqual(s['phase4_rows_in_box'], sum(1 for r in rows if r['phase'].startswith('4')))

    def test_posthoc_readings_complete(self):
        checks = read('phase4_posthoc_checks.csv')
        self.assertTrue(all(c['verdict'] in ('confirmed', 'partly confirmed', 'not confirmed') and c['reason']
                            for c in checks))
        out = subprocess.run([sys.executable, '-I', os.path.join(LANE, 'scripts', 'phase4_view.py'), '--posthoc'],
                             cwd=REPO, check=True, capture_output=True, text=True).stdout
        self.assertEqual(out.strip(), '')


if __name__ == '__main__':
    unittest.main()
