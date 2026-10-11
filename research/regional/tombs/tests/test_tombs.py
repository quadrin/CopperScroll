"""Tests for the regional tomb inventory (standard library; pandas and pyproj only for the rebuild test).

Run from the repository root:
    python3 -I -B -m unittest discover -s research/regional/tombs/tests -v
The rebuild test needs TOMBS_ASI_CACHE (the fetch_asi_maps.py cache) and TOMBS_WBADB (WBADB_data1.xlsx);
without them it is skipped.
"""
import csv
import filecmp
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(FOLDER, 'scripts'))
import tombs_common as T  # noqa: E402


def rows(name):
    with open(os.path.join(FOLDER, name), encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


class TestFreeze(unittest.TestCase):
    def test_plan_hash(self):
        self.assertEqual(T.sha256_file(T.PLAN_MD), T.PLAN_SHA256)

    def test_readme_records_hash_and_commit(self):
        with open(os.path.join(FOLDER, 'README.md'), encoding='utf-8') as fh:
            s = fh.read()
        self.assertIn(T.PLAN_SHA256, s)
        self.assertIn('cd394d7', s)

    def test_plan_json_parses(self):
        p = T.load_plan()
        self.assertEqual(p['crs'], 'EPSG:4326')
        self.assertEqual(len(p['branches']), 24)


class TestRules(unittest.TestCase):
    def setUp(self):
        self.p = T.load_plan()

    def test_period_masking(self):
        w, pa, o = T.period_classes(self.p, 'Burial cave of the Late Roman period')
        self.assertEqual((w, pa), ([], []))
        self.assertEqual(o, ['Late Roman'])
        w, pa, o = T.period_classes(self.p, 'Herodian burial cave, reused in the Byzantine period')
        self.assertEqual(w, ['Herodian'])
        w, pa, o = T.period_classes(self.p, 'Burial cave of the Second Temple period')
        self.assertEqual(pa, ['Second Temple'])

    def test_loc_clause_uncertainty(self):
        self.assertEqual(T.loc_clause(0.40, 0.5, 0.05), 'yes')
        self.assertEqual(T.loc_clause(0.53, 0.5, 0.05), 'unknown')
        self.assertEqual(T.loc_clause(0.70, 0.5, 0.05), 'no')

    def test_frozen_orientation_ignores_abbreviations(self):
        import build_tombs as B
        c = B.Coder(self.p)
        self.assertEqual(c.code('Burial cave. The W-facing entrance leads to a chamber.')['F7w'], 'unknown')
        self.assertEqual(c.code('Burial cave. The entrance faces west.')['F7w'], 'yes')
        self.assertEqual(c.code('Burial cave. The entrance faces north.')['F7w'], 'no')

    def test_amendment_orientation(self):
        import amendment1 as A
        self.assertEqual(A.orientation(self.p, 'The W-facing entrance leads to a chamber.'), ['W'])
        self.assertEqual(A.orientation(self.p, 'Rock-hewn cave on W slope of the hill, far from anything.'), [])

    def test_region_geometry(self):
        P = self.p['points']
        f = T.region_flags(self.p, *P['jer_temple'])
        self.assertTrue(f['in_A'] and not f['in_B1'])
        f = T.region_flags(self.p, *P['kh_qumran'])
        self.assertTrue(f['in_B2'] and f['d_road_km'] < 0.01)


class TestOutputs(unittest.TestCase):
    def test_tombs_schema(self):
        t = rows('tombs.csv')
        self.assertEqual(len(t), 1055)
        need = ['unit_id', 'source', 'record_id', 'locator', 'name', 'lat', 'lon', 'crs', 'monument_F1', 'porch_F2',
                'inside_pillar_F3', 'chambers_F10', 'inscription_F4', 'named_inscription_F5', 'setting_wadi_F19',
                'period_terms', 'dated_in_window', 'exposure']
        for c in need:
            self.assertIn(c, t[0])
        for r in t:
            self.assertEqual(r['crs'], 'EPSG:4326')
            self.assertIn(r['dated_in_window'], ('yes', 'partly', 'no', 'unknown'))
            for c in ('monument_F1', 'porch_F2', 'inside_pillar_F3', 'named_inscription_F5'):
                self.assertIn(r[c], ('yes', 'unknown'))
            self.assertIn(r['west_facing_F7w'], ('yes', 'no', 'unknown'))

    def test_no_description_text_stored(self):
        for name in ('tombs.csv', 'amendment1_codes.csv'):
            for r in rows(name):
                for k, v in r.items():
                    if k in ('locator', 'manual_rejected', 'exposure', 'enrich_A64', 'rejected'):
                        continue
                    self.assertLessEqual(len(v.split()), 12, (name, k, v[:80]))

    def test_distances_reproduce(self):
        p = T.load_plan()
        for r in rows('tombs.csv'):
            if not r['lat']:
                continue
            f = T.region_flags(p, float(r['lat']), float(r['lon']))
            self.assertAlmostEqual(f['d_temple_km'], float(r['d_temple_km']), places=2)
            self.assertEqual('yes' if f['in_A'] else 'no', r['in_A'])
            self.assertEqual('yes' if f['in_B2'] else 'no', r['in_B2'])

    def test_manual_checks_complete(self):
        self.assertFalse(os.path.exists(os.path.join(FOLDER, 'manual_check_pending.csv')))
        self.assertFalse(os.path.exists(os.path.join(FOLDER, 'amendment1_check_pending.csv')))
        decided = {(r['record_id'], r['code']) for r in rows('data/manual_check.csv')}
        for r in rows('tombs.csv'):
            for code in r['raw_yes_before_check'].split(';'):
                if code:
                    self.assertIn((r['record_id'], code), decided)

    def test_scores_reproduce_overall_and_summary(self):
        p = T.load_plan()
        sc = rows('scores.csv')
        for r in sc:
            vals = r['values'].split(';')
            exp = 'match' if all(v == 'yes' for v in vals) else 'fail' if 'no' in vals else 'unknown'
            self.assertEqual(r['result'], exp)
        t = {r['unit_id']: r for r in rows('tombs.csv')}
        by = {}
        for r in sc:
            u = t[r['unit_id']]
            if u['possible_duplicate_of'] or u['dated_in_window'] != 'yes':
                continue
            reg = {'A': u['in_A'] == 'yes', 'B': u['in_B1'] == 'yes' or u['in_B2'] == 'yes'}
            for k, ok in reg.items():
                if ok:
                    by.setdefault((r['branch'], k), []).append(r['result'])
        n = 0
        for s in rows('scores_summary.csv'):
            if s['date_set'] == 'strict' and s['view'] == 'all_lineages' and s['region'] in ('A', 'B') and s['N']:
                res = by.get((s['branch'], s['region']), [])
                self.assertEqual(int(s['N']), len(res), s['branch'])
                self.assertEqual(int(s['k_match']), res.count('match'))
                self.assertEqual(int(s['f_fail']), res.count('fail'))
                n += 1
        self.assertGreater(n, 30)
        self.assertEqual(len({b for b, s in p['branches'].items() if s['clauses']}) * 1040, len(sc))


@unittest.skipUnless(os.environ.get('TOMBS_ASI_CACHE') and os.environ.get('TOMBS_WBADB'),
                     'set TOMBS_ASI_CACHE and TOMBS_WBADB to run the rebuild test')
class TestRebuild(unittest.TestCase):
    def test_rebuild_identical(self):
        import build_tombs as B
        import amendment1 as A
        with tempfile.TemporaryDirectory() as d:
            B.main(os.environ['TOMBS_ASI_CACHE'], os.environ['TOMBS_WBADB'], d)
            A.main(os.environ['TOMBS_ASI_CACHE'], os.environ['TOMBS_WBADB'], d)
            for name in ('tombs.csv', 'scores.csv', 'scores_summary.csv', 'features_summary.csv',
                         'amendment1_codes.csv', 'amendment1_scores_summary.csv'):
                self.assertTrue(filecmp.cmp(os.path.join(d, name), os.path.join(FOLDER, name), shallow=False), name)

    def test_cache_matches_manifest(self):
        for r in rows('data/asi_manifest.csv'):
            p = os.path.join(os.environ['TOMBS_ASI_CACHE'], r['cache_file'])
            self.assertEqual(T.sha256_file(p), r['sha256'], r['cache_file'])


if __name__ == '__main__':
    unittest.main()
