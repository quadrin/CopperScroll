"""Tests for the columbaria lane (standard library unittest).

Run from the repository root:
  python3 -I -m unittest discover -s research/regional/columbaria/tests -v
With ASI_CACHE and WBADB_XLSX set, the screen is also rebuilt and compared with the committed tables.
"""
import csv
import filecmp
import hashlib
import json
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(FOLDER, 'scripts'))

import colcommon as C  # noqa: E402
import assemble  # noqa: E402
import score  # noqa: E402

PLAN_SHA256 = '425021ad165163710ce3ab1bbadb5f2dfb998749abdbade4e9085bbd1334f906'


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


class TestFreeze(unittest.TestCase):
    def test_plan_hash(self):
        self.assertEqual(sha(os.path.join(FOLDER, 'PLAN.md')), PLAN_SHA256)
        with open(os.path.join(FOLDER, 'README.md'), encoding='utf-8') as f:
            self.assertIn(PLAN_SHA256, f.read())

    def test_terms_copy_appendix(self):
        with open(os.path.join(FOLDER, 'PLAN.md'), encoding='utf-8') as f:
            plan = f.read()
        appendix = plan.split('## Appendix A')[1]
        t = C.load_terms()
        pats = list(t['columbarium_en']) + list(t['columbarium_he'])
        for v in t['flags'].values():
            pats += v['en'] + v['he']
        for p in pats:
            self.assertIn('`' + p + '`', appendix, p)
        for lon, lat in t['region_polygon_lonlat_wgs84']:
            self.assertIn(f'({lon:.2f}, {lat:.2f})', plan)


class TestRules(unittest.TestCase):
    def test_screen_words(self):
        self.assertTrue(C.find_columbarium('a rock-hewn columbarium cave'))
        self.assertTrue(C.find_columbarium('columbaria'))
        self.assertTrue(C.find_columbarium('a dove-cote on the roof'))
        self.assertTrue(C.find_columbarium('מערת קולומבאריום'))
        self.assertTrue(C.find_columbarium('בשובך'))
        self.assertTrue(C.find_columbarium('מגדל יונים'))
        self.assertFalse(C.find_columbarium('חדרים עליונים'))
        self.assertFalse(C.find_columbarium('pigeon'))

    def test_region(self):
        self.assertTrue(C.in_region(35.2354, 31.6444))    # Ain en-Natuf
        self.assertTrue(C.in_region(35.3534, 31.3158))    # Masada
        self.assertFalse(C.in_region(35.42, 32.08))       # Alexandrium, north of the line
        self.assertFalse(C.in_region(34.79, 31.25))       # Beer Sheva

    def test_distance_and_latitude_codes(self):
        self.assertEqual(score.dist_code(31.64436, 35.23543, score.N1, 1.0, 100)[0], 'M')
        self.assertEqual(score.dist_code(31.70, 35.23543, score.N1, 1.0, 100)[0], 'F')
        self.assertEqual(score.dist_code(31.6534, 35.23543, score.N1, 1.0, 100)[0], 'U')  # 1.0-1.1 km
        self.assertEqual(score.dist_code(31.64, 35.23, score.N1, 1.0, 3000)[0], 'U')
        self.assertEqual(score.lat_code(31.30, score.LAT_SA, 100), 'M')
        self.assertEqual(score.lat_code(31.80, score.LAT_SA, 100), 'F')
        self.assertEqual(score.lat_code(31.7652, score.LAT_SA, 100), 'U')

    def test_clause_logic(self):
        base = dict(fort_at_site='no', tower_at_site='no', outside_fort='no', outside_tower='no')
        self.assertEqual(score.fort_codes(dict(base, setting='fortress_inside')), ('M', 'M', 'M', 'M'))
        self.assertEqual(score.fort_codes(dict(base, setting='isolated')), ('F', 'F', 'F', 'F'))
        self.assertEqual(score.fort_codes(dict(base, setting='fort_site', fort_at_site='yes', outside_fort='yes')),
                         ('M', 'F', 'M', 'F'))
        self.assertEqual(score.fort_codes(dict(base, setting='tower_itself')), ('U', 'U', 'M', 'M'))
        self.assertEqual(score.fort_codes(dict(base, setting='settlement')), ('U', 'U', 'U', 'U'))
        self.assertEqual(score.combine(['M', 'M']), 'M')
        self.assertEqual(score.combine(['M', 'U']), 'U')
        self.assertEqual(score.combine(['U', 'F']), 'F')
        self.assertEqual(score.period('D'), 'M')
        self.assertEqual(score.period('P'), 'U')
        self.assertEqual(score.period('P', relaxed=True), 'M')
        self.assertEqual(score.period('L', relaxed=True), 'F')
        self.assertEqual(score.s_c('south'), 'M')
        self.assertEqual(score.s_c('southwest'), 'U')
        self.assertEqual(score.s_c('west'), 'F')


class TestTables(unittest.TestCase):
    def test_schema_and_quotes(self):
        with open(os.path.join(FOLDER, 'columbaria.csv'), encoding='utf-8') as f:
            rd = csv.DictReader(f)
            self.assertEqual(rd.fieldnames, assemble.COLUMNS)
            rows = list(rd)
        ids = {r['id'] for r in rows}
        self.assertEqual(len(ids), len(rows))
        for r in rows:
            self.assertLessEqual(len(r['quote'].split()), 12, r['id'])
            self.assertIn(r['date_code'], 'DLPU')
            self.assertIn(r['dated_in_window'], ('yes', 'no', 'partly', 'unknown'))
            self.assertTrue(r['dup_of'] == '' or r['dup_of'] in ids)
            if not r['dup_of']:
                self.assertEqual(r['in_region'], 'yes', r['id'])
                self.assertEqual(r['crs'], 'EPSG:4326')
                float(r['lat']), float(r['lon'])
        with open(os.path.join(FOLDER, 'scores.csv'), encoding='utf-8') as f:
            hdr = next(csv.reader(f))
        self.assertEqual(hdr[:4], ['scope', 'id', 'name', 'source'])
        for k in score.CLAUSES:
            self.assertIn(k, hdr)

    def test_assemble_reproduces(self):
        with tempfile.TemporaryDirectory() as d:
            assemble.main(d)
            self.assertTrue(filecmp.cmp(os.path.join(d, 'columbaria.csv'), os.path.join(FOLDER, 'columbaria.csv'),
                                        shallow=False))
            self.assertTrue(filecmp.cmp(os.path.join(d, 'excluded.csv'), os.path.join(FOLDER, 'data', 'excluded.csv'),
                                        shallow=False))

    def test_score_reproduces(self):
        with tempfile.TemporaryDirectory() as d:
            score.main(d)
            for name in ('scores.csv', 'summary.json'):
                self.assertTrue(filecmp.cmp(os.path.join(d, name), os.path.join(FOLDER, name), shallow=False), name)

    def test_readme_headline_matches_summary(self):
        with open(os.path.join(FOLDER, 'summary.json'), encoding='utf-8') as f:
            s = json.load(f)['scopes']['frozen']['headline']
        with open(os.path.join(FOLDER, 'README.md'), encoding='utf-8') as f:
            readme = f.read()
        for key in ('44-D-P|text|F|S_A', '38-D-N1|survey|1km'):
            v = s[key]
            self.assertIn(f"{v['k_match']} match, {v['f_fail']} fail, {v['m_unknown']} unknown, of {v['N']}", readme,
                          key)


@unittest.skipUnless(os.environ.get('ASI_CACHE') and os.environ.get('WBADB_XLSX'), 'needs ASI_CACHE and WBADB_XLSX')
class TestScreenRebuild(unittest.TestCase):
    def test_rebuild(self):
        import build_inventory as B
        asi = B.asi_screen(os.environ['ASI_CACHE'])
        wb = B.wbadb_screen(os.environ['WBADB_XLSX'])
        with tempfile.TemporaryDirectory() as d:
            B.write(asi, os.path.join(d, 'a.csv'))
            B.write(wb, os.path.join(d, 'w.csv'))
            self.assertTrue(filecmp.cmp(os.path.join(d, 'a.csv'), os.path.join(FOLDER, 'data', 'candidates_asi.csv'),
                                        shallow=False))
            self.assertTrue(filecmp.cmp(os.path.join(d, 'w.csv'),
                                        os.path.join(FOLDER, 'data', 'candidates_wbadb.csv'), shallow=False))


if __name__ == '__main__':
    unittest.main()
