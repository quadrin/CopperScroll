"""Test of the exploratory phase-4 view (PLAN_AMENDMENT_PHASE4_2026-10-12.md).

Run from the repository root:  python3 -I -B -m unittest discover -s research/regional/tombs/tests -v
Checks: the amendment's hash and freeze commit; that scripts/phase4_view.py reproduces its outputs without touching
the frozen tables, the Amendment 1 and 2 outputs or the 11 October IAA view (the script also checks internally that
the frozen units reproduce scores_summary.csv and that the 11 October view rebuilds from merged_2026-10-11); that the
view's frozen and 11 October columns equal the committed files; that the union adds exactly the non-duplicate units;
that no held, strip, Kh. Almit or Atiqot 41 row is a unit; and that the README quotes the summary.
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
FOLDER = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(FOLDER, '..', '..', '..'))
AMEND = 'research/regional/tombs/PLAN_AMENDMENT_PHASE4_2026-10-12.md'
AMEND_SHA = 'f9b0ad579e2e551b04708aaa825c828b98c2fae7a82f49b95f953cc40875b9bc'
AMEND_COMMIT = 'd5a837e14f7bccda6450215fb33f397ee9e84de5'
VIEW_OUT = ['phase4_units.csv', 'phase4_scores.csv', 'phase4_view_2026-10-12.csv', 'phase4_amendment1_view.csv',
            'phase4_summary.json']
FROZEN_OUT = ['tombs.csv', 'scores.csv', 'scores_summary.csv', 'features_summary.csv', 'amendment1_codes.csv',
              'amendment1_scores_summary.csv', 'amendment2_akeldama_units.csv', 'amendment2_scores_summary.csv',
              'iaa_units.csv', 'iaa_scores.csv', 'iaa_view_2026-10-11.csv', 'iaa_amendment1_view.csv', 'iaa_summary.json']


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(name):
    with open(os.path.join(FOLDER, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def load(name):
    with open(os.path.join(FOLDER, name), encoding='utf-8') as f:
        return json.load(f)


def git_blob_sha(rev, rel):
    r = subprocess.run(['git', 'show', f'{rev}:{rel}'], cwd=REPO, capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None


class TestPhase4View(unittest.TestCase):
    def test_amendment(self):
        self.assertEqual(sha(os.path.join(REPO, AMEND)), AMEND_SHA)
        r = subprocess.run(['git', 'show', '--name-only', '--format=', AMEND_COMMIT], cwd=REPO, capture_output=True, text=True)
        if r.returncode != 0:
            self.skipTest('amendment commit not in this clone')
        self.assertEqual(r.stdout.split(), [AMEND])

    def test_frozen_files_unchanged_since_freeze(self):
        for n in FROZEN_OUT:
            got = git_blob_sha(AMEND_COMMIT, f'research/regional/tombs/{n}')
            if got is None:
                self.skipTest('amendment commit not in this clone')
            self.assertEqual(sha(os.path.join(FOLDER, n)), got, n)

    def test_reproduces_and_frozen_untouched(self):
        before = {n: sha(os.path.join(FOLDER, n)) for n in VIEW_OUT + FROZEN_OUT}
        tmp = tempfile.mkdtemp()
        try:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(FOLDER, n), os.path.join(tmp, n))
            subprocess.run([sys.executable, '-I', '-B', os.path.join(FOLDER, 'scripts', 'phase4_view.py')], cwd=REPO,
                           check=True, capture_output=True)
            self.assertEqual(before, {n: sha(os.path.join(FOLDER, n)) for n in VIEW_OUT + FROZEN_OUT})
        finally:
            for n in VIEW_OUT:
                shutil.copy(os.path.join(tmp, n), os.path.join(FOLDER, n))
            shutil.rmtree(tmp)

    def test_frozen_and_11oct_columns_and_union(self):
        committed = {(r['branch'], r['region'], r['date_set']): r for r in read('scores_summary.csv')
                     if r['view'] == 'all_lineages'}
        c11 = {(r['branch'], r['region'], r['date_set']): r for r in read('iaa_view_2026-10-11.csv')}
        units = [u for u in read('phase4_units.csv') if u['kind'] == 'primary' and not u['possible_duplicate_of']]

        def n_new(reg, ds):
            def inr(u):
                return {'A': u['in_A'] == 'yes', 'A3': u['in_A3'] == 'yes', 'B': 'yes' in (u['in_B1'], u['in_B2']),
                        'B1': u['in_B1'] == 'yes', 'B2': u['in_B2'] == 'yes', 'B2_5': u['in_B2_5'] == 'yes',
                        'AB': 'yes' in (u['in_A'], u['in_B1'], u['in_B2'])}[reg]
            return sum(1 for u in units if inr(u) and {'strict': u['dated_in_window'] == 'yes',
                                                       'lenient': u['dated_lenient'] == 'yes', 'any': True}[ds])
        view = read('phase4_view_2026-10-12.csv')
        self.assertEqual(len(view), len(c11))
        for r in view:
            k = (r['branch'], r['region'], r['date_set'])
            c, e = committed[k], c11[k]
            self.assertEqual([r['frozen_N'], r['frozen_k'], r['frozen_f'], r['frozen_m']],
                             [c['N'], c['k_match'], c['f_fail'], c['m_unknown']])
            self.assertEqual([r['iaa11_N'], r['iaa11_k'], r['iaa11_f'], r['iaa11_m']],
                             [e['union_N'], e['union_k'], e['union_f'], e['union_m']])
            self.assertEqual(int(r['union_N']) - int(r['frozen_N']), n_new(r['region'], r['date_set']))
            self.assertEqual(int(r['union_k']) + int(r['union_f']) + int(r['union_m']), int(r['union_N']))

    def test_no_protected_row_is_a_unit(self):
        s = load('phase4_summary.json')
        ids = {u['record_id'] for u in read('phase4_units.csv')}
        for uid in s['excluded_rows']:
            self.assertNotIn(f'IAA {uid}', ids)
        merged = os.path.join(REPO, 'research', 'regional', 'haesi_features', 'merged_2026-10-12', 'features_all.csv')
        with open(merged, encoding='utf-8') as f:
            rows = {r['row_uid']: r for r in csv.DictReader(f)}
        for u in read('phase4_units.csv'):
            r = rows[u['record_id'][4:]]
            self.assertNotEqual(r['protected_strip'], 'yes')
            self.assertFalse(r['report_id'].startswith('ATQ41-'))
            if r['phase'].startswith('4'):
                self.assertIsNone(re.search(r'almit|עלמית', r['site_name'] + r['report_id'], re.I))
                self.assertIsNone(re.search(r't[ae]ll?[\s_-]*(es|el|al|e)?[\s_-]*sultan', r['site_name'] + ' ' +
                                            r['coordinate_source'], re.I))
        self.assertEqual(s['tier1_units'], [])

    def test_readme_quotes_summary(self):
        s = load('phase4_summary.json')
        with open(os.path.join(FOLDER, 'README.md'), encoding='utf-8') as f:
            text = f.read()
        sec = text.split('## Phase-4 inventory view, 12 October 2026 (exploratory)')[1].split('\n## ')[0]
        view = {(r['branch'], r['region'], r['date_set']): r for r in read('phase4_view_2026-10-12.csv')}
        a = view[('14-M62', 'A', 'strict')]
        self.assertIn(f"{a['iaa11_N']} to {a['union_N']}", sec)
        self.assertIn(f"{s['units']['primary_from_phase4_rows']} phase-4 tomb units", sec)
        self.assertIn(f"{s['units']['primary_from_phase4_rows_not_duplicate']} are new", sec)
        s11 = load('iaa_summary.json')
        self.assertIn(f"Non-duplicate units: {s11['iaa_units']['primary_not_duplicate']} → "
                      f"{s['units']['primary_not_duplicate']}, at {s['units']['primary_not_duplicate_distinct_sites']} distinct", sec)
        self.assertIn(f"{s['units']['primary']} IAA tomb units have coordinates", sec)


if __name__ == '__main__':
    unittest.main()
