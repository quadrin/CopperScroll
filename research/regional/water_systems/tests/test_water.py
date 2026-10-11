"""Tests of the water-systems lane (standard library unittest).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/water_systems/tests -v
Optional: WATER_WBADB=/path/WBADB_data1.xlsx WATER_ASI_CACHE=/path/cache also rebuilds survey_rows.csv and checks it
is byte-identical to the committed file (needs pandas, openpyxl, pyproj).
"""
import csv
import hashlib
import os
import re
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
SCRIPTS = os.path.join(LANE, 'scripts')
REPO = os.path.abspath(os.path.join(LANE, '..', '..', '..'))
sys.path.insert(0, SCRIPTS)
import common as C  # noqa: E402
import score as S  # noqa: E402


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def rows(name):
    with open(os.path.join(LANE, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


class TestFreeze(unittest.TestCase):
    def test_plan_hashes_match_readme(self):
        with open(os.path.join(LANE, 'README.md'), encoding='utf-8') as f:
            readme = f.read()
        for fn in ('PLAN.md', 'PLAN_AMENDMENT_1.md'):
            self.assertIn(sha(os.path.join(LANE, fn)), readme, fn)

    def test_plan_is_the_frozen_commit_version(self):
        try:
            out = subprocess.run(['git', 'show', '0b07fad:research/regional/water_systems/PLAN.md'], cwd=REPO,
                                 capture_output=True, check=True).stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.skipTest('git history not available')
        self.assertEqual(hashlib.sha256(out).hexdigest(), sha(os.path.join(LANE, 'PLAN.md')))


class TestSchema(unittest.TestCase):
    def test_water_columns_and_values(self):
        w = rows('water.csv')
        from build_water import EXTRA
        with open(os.path.join(LANE, 'water.csv'), encoding='utf-8') as f:
            header = f.readline().strip().split(',')
        self.assertEqual(header, C.COLUMNS + EXTRA)
        tri = {'yes', 'no', 'unknown', ''}
        for r in w:
            self.assertTrue(r['id'] and r['lineage'] in ('WBADB', 'ASI', 'HAESI', 'LIT'), r['id'])
            self.assertIn(r['type'], C.TYPES, r['id'])
            self.assertIn(r['date_code'], ('in', 'in_hedged', 'partly', 'out', 'undated'), r['id'])
            for k in ('plaster', 'entrance', 'great', 'north', 'head', 'solomon', 'qelt', 'kidron_feed', 'qumran',
                      'jericho_oasis', 'cypros', 'feed_wadi', 'wall_at_outlet', 'bend'):
                self.assertIn(r[k], tri, (r['id'], k, r[k]))
            self.assertIn(r['in_box'], ('yes', 'no', 'unplaced'))
            if r['lat']:
                self.assertTrue(-90 < float(r['lat']) < 90 and 30 < float(r['lon']) < 40)
            self.assertLessEqual(len(r['quote'].split()), 12, r['id'])
            if r['lineage'] != 'LIT':
                self.assertEqual(r['quote'], '', 'no survey text is stored')
        ids = [r['id'] for r in w]
        self.assertEqual(len(ids), len(set(ids)))

    def test_survey_rows_in_box(self):
        for r in rows('water.csv'):
            if r['lineage'] != 'LIT':
                self.assertEqual(r['in_box'], 'yes')
                self.assertTrue(C.in_box(float(r['lat']), float(r['lon'])))

    def test_counts_add_up(self):
        for r in rows('counts.csv'):
            self.assertEqual(int(r['N']), int(r['k_match']) + int(r['f_fail']) + int(r['m_unknown']), r)

    def test_dup_and_supersede_targets_exist(self):
        w = rows('water.csv')
        ids = {r['id'] for r in w}
        for r in w:
            if r['dup_of']:
                self.assertIn(r['dup_of'], ids)
                self.assertEqual(r['lineage'], 'WBADB')


class TestRules(unittest.TestCase):
    def test_dates(self):
        self.assertEqual(C.date_code('a Herodian pool')[0], 'in')
        self.assertEqual(C.date_code('apparently of Hasmonean date')[0], 'in_hedged')
        self.assertEqual(C.date_code('carved water system (prob. Rom1)')[0], 'in_hedged')
        self.assertEqual(C.date_code('Roman cistern')[0], 'partly')
        self.assertEqual(C.date_code('Late Roman and Byzantine cisterns')[0], 'out')
        self.assertEqual(C.date_code('a cistern')[0], 'undated')
        self.assertEqual(C.date_code('Early Roman pool')[0], 'in')

    def test_types_and_exclusions(self):
        self.assertIn('cistern', C.type_hits('Two rock-hewn cisterns.'))
        self.assertNotIn('basin_tank', C.type_hits('A winepress with a collecting basin.'))
        self.assertNotIn('aqueduct', C.type_hits('Winepress: treading floor and channel to the vat.'))
        self.assertNotIn('reservoir_pool', C.type_hits("the aqueduct leading from Solomon's Pools to the Temple"))
        self.assertIn('reservoir_pool', C.type_hits("Solomon's Pools", "Solomon's Pools"))
        self.assertNotIn('well', C.type_hits('well-preserved walls'))
        self.assertIn('well', C.type_hits('a rock-hewn well'))

    def test_flow_and_within(self):
        r = dict(flow_from='N', lat='', lon='', precision_m='', dest_lat='', dest_lon='', dest_prec='')
        self.assertEqual(S.flow_clause(r), S.M)
        r['flow_from'] = 'W'
        self.assertEqual(S.flow_clause(r), S.F)
        # head 2 km north of destination -> water comes from the north
        r.update(flow_from='', lat='31.818', lon='35.300', precision_m='50', dest_lat='31.800', dest_lon='35.300',
                 dest_prec='50')
        self.assertEqual(S.flow_clause(r), S.M)
        rr = dict(lat='31.7400', lon='35.2190', precision_m='50')
        self.assertEqual(S.within(rr, (31.73999, 35.21899), 1.0), S.M)
        rr = dict(lat='31.7800', lon='35.2190', precision_m='50')
        self.assertEqual(S.within(rr, (31.73999, 35.21899), 1.0), S.F)

    def test_overall(self):
        self.assertEqual(S.overall([S.M, S.M, S.NS]), S.M)
        self.assertEqual(S.overall([S.M, S.U]), S.U)
        self.assertEqual(S.overall([S.M, S.F]), S.F)
        self.assertEqual(S.combine([S.M, S.F]), 'CONFLICT')


class TestReproduction(unittest.TestCase):
    OUTPUTS = ('water.csv', 'merged_units.csv', 'scores.csv', 'merged_scores.csv', 'counts.csv', 'headline.csv')

    def test_build_and_score_reproduce_committed_tables(self):
        before = {fn: sha(os.path.join(LANE, fn)) for fn in self.OUTPUTS}
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        for script in ('build_water.py', 'score.py'):
            subprocess.run([sys.executable, '-I', os.path.join(SCRIPTS, script)], cwd=REPO, check=True, env=env,
                           capture_output=True)
        after = {fn: sha(os.path.join(LANE, fn)) for fn in self.OUTPUTS}
        self.assertEqual(before, after)

    def test_survey_rebuild_optional(self):
        xlsx, cache = os.environ.get('WATER_WBADB'), os.environ.get('WATER_ASI_CACHE')
        if not (xlsx and cache):
            self.skipTest('WATER_WBADB / WATER_ASI_CACHE not set')
        before = sha(os.path.join(LANE, 'survey_rows.csv'))
        subprocess.run([sys.executable, '-I', os.path.join(SCRIPTS, 'build_survey.py'), xlsx, cache], cwd=REPO,
                       check=True, capture_output=True)
        self.assertEqual(before, sha(os.path.join(LANE, 'survey_rows.csv')))

    def test_headline_has_brief_counts(self):
        labels = [r['count'] for r in rows('headline.csv')]
        for want in ('heads with a stone or feature on the north side', 'reservoirs great or northern',
                     'cisterns fed by channels from a great (trunk) wadi', '... at a named wadi',
                     'installations dated in the window (in or in_hedged)'):
            self.assertIn(want, labels)
        self.assertTrue(all(re.match(r'^\d*$', r['rows_in_box']) for r in rows('headline.csv')))


if __name__ == '__main__':
    unittest.main()
