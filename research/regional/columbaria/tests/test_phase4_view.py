"""Test of the exploratory phase 1-4 view (PLAN_AMENDMENT_PHASE4_2026-10-12.md). Standard library unittest.

Run from the repository root:  python3 -I -m unittest discover -s research/regional/columbaria/tests -v
Checks: the amendment's hash and freeze commit; that scripts/phase4_view.py reproduces its outputs without touching
the frozen tables or the IAA view; that the frozen columns equal summary.json and the frozen headline is unchanged;
that the 11 October columns equal iaa_view_2026-10-11.csv; that union = frozen + inventory rows; that every decision
is a listed pair; that no held, Tell es-Sultan or Kh. ʿAlmit row is scored; and that the README table matches.
"""
import csv
import glob
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
AMEND = 'research/regional/columbaria/PLAN_AMENDMENT_PHASE4_2026-10-12.md'
AMEND_SHA = '566502d8907fe5060546556aeb326baf60e653d20dfc5915d0abf63c589978e1'
AMEND_COMMIT = 'f8a016e3e3fbf9c02e1e704504d446b2e2a448d0'
SCRIPT = os.path.join(FOLDER, 'scripts', 'phase4_view.py')
VIEW = 'phase4_view_2026-10-12.csv'
OUT = ['phase4_rows.csv', 'phase4_excluded.csv', 'phase4_scores.csv', 'phase4_summary.json', VIEW]
UNTOUCHED = ['columbaria.csv', 'scores.csv', 'summary.json', 'iaa_rows.csv', 'iaa_excluded.csv', 'iaa_scores.csv',
             'iaa_summary.json', 'iaa_view_2026-10-11.csv']
FROZEN_HEADLINE = {  # README "Results" (scope frozen), PLAN freeze afdd69f
    '38-D-N1|survey|1km': (0, 179, 0, 179), '38-D-N2|survey|1km': (0, 179, 0, 179), '38-D-N0|survey': (17, 2, 160, 179),
    '44-D-P|survey|F|S_A': (3, 55, 121, 179), '44-D-P|text|F|S_A': (3, 59, 117, 179),
    '44-D-T|survey|F|S_A': (0, 57, 122, 179), '44-D-T|text|F|S_A': (0, 61, 118, 179), '44-D-Masada|text': (3, 176, 0, 179)}


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(name):
    with open(os.path.join(FOLDER, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


class TestPhase4View(unittest.TestCase):
    def test_amendment(self):
        self.assertEqual(sha(os.path.join(REPO, AMEND)), AMEND_SHA)
        r = subprocess.run(['git', 'show', '--name-only', '--format=', AMEND_COMMIT], cwd=REPO, capture_output=True,
                           text=True)
        if r.returncode != 0:
            self.skipTest('amendment commit not in this clone')
        self.assertEqual(r.stdout.split(), [AMEND])

    def test_reproduces_and_others_untouched(self):
        before = {n: sha(os.path.join(FOLDER, n)) for n in OUT + UNTOUCHED}
        tmp = tempfile.mkdtemp()
        try:
            for n in OUT:
                shutil.copy(os.path.join(FOLDER, n), os.path.join(tmp, n))
            subprocess.run([sys.executable, '-I', SCRIPT], cwd=REPO, check=True, capture_output=True)
            self.assertEqual(before, {n: sha(os.path.join(FOLDER, n)) for n in OUT + UNTOUCHED})
        finally:
            for n in OUT:
                shutil.copy(os.path.join(tmp, n), os.path.join(FOLDER, n))
            shutil.rmtree(tmp)

    def test_frozen_unchanged_and_columns(self):
        with open(os.path.join(FOLDER, 'summary.json'), encoding='utf-8') as f:
            summ = json.load(f)['scopes']
        iaa = {(r['scope'], r['kind'], r['key']): r for r in read('iaa_view_2026-10-11.csv')}
        view = read(VIEW)
        self.assertEqual(len(view), len(iaa))
        for r in view:
            src = summ[r['scope']]['headline' if r['kind'] == 'headline' else 'clauses'][r['key']]
            self.assertEqual([int(r[k]) for k in ('frozen_N', 'frozen_k', 'frozen_f', 'frozen_m')],
                             [src['N'], src['k_match'], src['f_fail'], src['m_unknown']])
            a = iaa[(r['scope'], r['kind'], r['key'])]
            for x in ('N', 'k', 'f', 'm'):
                self.assertEqual(int(r[f'iaa1011_{x}']), int(a[f'union_{x}']))
                self.assertEqual(int(r[f'union_{x}']), int(r[f'frozen_{x}']) + int(r[f'inv_{x}']))
            if r['scope'] == 'frozen' and r['key'] in FROZEN_HEADLINE:
                self.assertEqual(tuple(int(r[f'frozen_{x}']) for x in ('k', 'f', 'm', 'N')), FROZEN_HEADLINE[r['key']])

    def test_no_pending_pairs_and_decisions(self):
        out = subprocess.run([sys.executable, '-I', SCRIPT, '--pairs'], cwd=REPO, check=True, capture_output=True,
                             text=True).stdout
        self.assertEqual(out.strip(), '')
        dec = read(os.path.join('data', 'phase4_dedup_decisions.csv'))
        self.assertTrue(all(d['decision'] in ('same', 'different') and d['reason'] for d in dec))

    def test_protected_not_scored(self):
        held = set()
        for p in glob.glob(os.path.join(REPO, 'research', 'regional', 'haesi_features', 'phase4_2026-10-11', '**',
                                        'held*.csv'), recursive=True):
            with open(p, encoding='utf-8') as f:
                held |= {r['unit_id'] for r in csv.DictReader(f)}
        with open(os.path.join(REPO, 'research', 'regional', 'haesi_features', 'merged_2026-10-12', 'features_all.csv'),
                  encoding='utf-8') as f:
            rid = {r['row_uid']: r['report_id'] for r in csv.DictReader(f)}
        for r in read('phase4_rows.csv'):
            if not r['phase'].startswith('4'):
                continue
            uid = re.search(r'row (\S+)', r['read_via']).group(1)
            self.assertNotIn(rid[uid], held, r['id'])
            self.assertIsNone(re.search(r'almit|עלמית|sultan', r['name'] + r['notes'], re.I), r['id'])

    def test_readme_table(self):
        with open(os.path.join(FOLDER, 'README.md'), encoding='utf-8') as f:
            readme = f.read()
        sec = readme.split('## Phase 1–4 inventory view, 12 October 2026 (exploratory)')[1]
        for r in read(VIEW):
            if r['scope'] == 'frozen' and r['kind'] == 'headline':
                cell = ' | '.join(f"{r[t + '_k']} / {r[t + '_f']} / {r[t + '_m']} of {r[t + '_N']}"
                                  for t in ('frozen', 'iaa1011', 'union'))
                self.assertIn(f"`{r['key'].replace('|', ', ')}` | {cell} |", sec, r['key'])


if __name__ == '__main__':
    unittest.main()
