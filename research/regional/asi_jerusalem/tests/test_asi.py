"""Tests for the ASI Jerusalem-area tables.

Run from the repository root:
    python3 -I -m unittest discover -s research/regional/asi_jerusalem/tests -v
The determinism and verbatim-quote tests need the local cache; give its path in the
environment variable ASI_CACHE. Without it they are skipped.
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
import asi_common as C  # noqa: E402
import build_asi as B  # noqa: E402

CACHE = os.environ.get('ASI_CACHE', '')
OUTPUTS = ['sites.csv', 'features.csv', 'looks_asi.csv', 'place_summary.csv', 'maps_used.csv', 'sources_manifest.csv',
           'hebrew_check_v2.csv']


def read(name):
    with open(os.path.join(FOLDER, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def header(path):
    with open(path, encoding='utf-8') as f:
        return next(csv.reader(f))


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


class PlanHash(unittest.TestCase):
    def test_plan_and_amendment_hashes_match_readme(self):
        with open(os.path.join(FOLDER, 'README.md'), encoding='utf-8') as f:
            readme = f.read()
        for name in ('plan.json', 'plan_amendment_1.json', 'plan_amendment_2_posthoc.json'):
            m = re.search(re.escape(name) + r' SHA-256: `([0-9a-f]{64})`', readme)
            self.assertIsNotNone(m, name)
            self.assertEqual(sha(os.path.join(FOLDER, name)), m.group(1), name)


class Schema(unittest.TestCase):
    def test_headers(self):
        self.assertEqual(header(os.path.join(FOLDER, 'sites.csv')), B.SITE_COLS)
        self.assertEqual(header(os.path.join(FOLDER, 'features.csv')), B.FEAT_COLS)
        self.assertEqual(header(os.path.join(FOLDER, 'place_summary.csv')), B.PLACE_COLS)
        self.assertEqual(header(os.path.join(FOLDER, 'maps_used.csv')), B.MAP_COLS)
        plan = C.load_plan()
        looks_schema = header(os.path.join(C.REPO, plan['inputs']['looks_schema']['path']))
        self.assertEqual(header(os.path.join(FOLDER, 'looks_asi.csv')), looks_schema)

    def test_values(self):
        plan = C.load_plan()
        places, _ = C.load_places(plan)
        pids = {p['place_id'] for p in places}
        classes = {k for k in plan['feature_classes'] if k != 'note'}
        sites = read('sites.csv')
        self.assertGreater(len(sites), 0)
        ids = set()
        for s in sites:
            self.assertNotIn(s['record_id'], ids)
            ids.add(s['record_id'])
            self.assertIn(s['nearest_place_id'], pids)
            self.assertLessEqual(float(s['nearest_place_km']), 3.0)
            self.assertTrue(-90 <= float(s['lat']) <= 90 and -180 <= float(s['lon']) <= 180)
            self.assertIn(s['record_fetched'], ('yes', 'no'))
            self.assertIn(s['coord_method'], ('nig_epsg2039', 'source_wgs84', 'geojson_point'))
            self.assertIn(s['site_finds_in_window'], ('yes', 'overlaps', 'no', 'unknown'))
        for r in read('features.csv'):
            self.assertIn(r['record_id'], ids)
            self.assertIn(r['feature_class'], classes)
            self.assertIn(r['dated_in_window'], ('yes', 'partly', 'no', 'unknown'))
        for r in read('looks_asi.csv'):
            self.assertIn(r['place_id'], pids)
            self.assertIn(r['result'], ('reported', 'silent'))
            for k in ('coverage', 'p_recognise', 'p_report', 'p_survive'):
                if r[k]:
                    self.assertTrue(0.0 <= float(r[k]) <= 1.0)
            self.assertEqual(r['p_recognise'], '')
            self.assertEqual(r['p_report'], '')
            self.assertEqual(r['p_survive'], '')
            if r['coverage']:
                self.assertTrue(r['coverage_basis'].startswith('EVIDENCE'))


class Quotes(unittest.TestCase):
    def test_quotes_at_most_12_words(self):
        for name, cols in (('sites.csv', ['quote']), ('features.csv', ['quote']),
                           ('coverage_statements.csv', ['coverage_quote', 'detection_quote'])):
            for r in read(name):
                for c in cols:
                    self.assertLessEqual(len(r[c].split()), 12, (name, c, r[c]))
                    self.assertLessEqual(len(r[c]), 160, (name, c, r[c]))

    def test_quote_limits_after_deviation(self):
        # post-freeze deviation: no quote text in features.csv; at most one quote per record in
        # sites.csv, and only for records within 1 km of a place
        for r in read('features.csv'):
            self.assertEqual(r['quote'], '', r['record_id'])
        for r in read('sites.csv'):
            if r['quote']:
                self.assertNotEqual(r['places_within_1km'], '', r['record_id'])

    def test_no_long_text_columns(self):
        # no source prose beyond the quote columns: descriptions are never stored
        self.assertNotIn('description', B.SITE_COLS)
        self.assertNotIn('description', B.FEAT_COLS)


class Rules(unittest.TestCase):
    def test_period_precedence(self):
        plan = C.load_plan()
        rx, gcls = B.compile_periods(plan)
        f = lambda t: [(lab, k) for lab, k, _ in B.find_periods(rx, gcls, t)]  # noqa: E731
        self.assertEqual(f('Early Roman tomb'), [('Early Roman', 'within')])
        self.assertEqual(f('Hellenistic and Roman'), [('Hellenistic', 'overlaps'), ('Roman', 'overlaps')])
        self.assertEqual(f('Late Roman'), [('Late Roman', 'outside')])
        self.assertEqual(f('Early Hellenistic'), [('Early Hellenistic', 'outside')])
        self.assertEqual(B.window_all([]), 'unknown')
        self.assertEqual(B.window_all([('a', 'within', 0), ('b', 'outside', 1)]), 'partly')
        self.assertEqual(B.window_any([('a', 'outside', 0), ('b', 'overlaps', 1)]), 'overlaps')

    def test_grid_axis_rule(self):
        self.assertEqual(C.parse_grid_pair('630497, 222438'), (222438.0, 630497.0))
        lon, lat = B.ITM.transform(222438.0, 630497.0)
        self.assertAlmostEqual(lat, 31.7671, places=3)
        self.assertAlmostEqual(lon, 35.2359, places=3)


@unittest.skipUnless(CACHE and os.path.isdir(CACHE), 'set ASI_CACHE to the cache folder')
class WithCache(unittest.TestCase):
    def test_determinism_and_committed_outputs(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            B.build(CACHE, a)
            B.build(CACHE, b)
            for name in OUTPUTS:
                self.assertTrue(filecmp.cmp(os.path.join(a, name), os.path.join(b, name), shallow=False), name)
                self.assertTrue(filecmp.cmp(os.path.join(a, name), os.path.join(FOLDER, name), shallow=False),
                                'committed ' + name)

    def test_coverage_quotes_verbatim(self):
        intro_cache = {}
        for r in read('coverage_statements.csv'):
            for c in ('coverage_quote', 'detection_quote'):
                q = r[c]
                if not q:
                    continue
                found = False
                mids = [r['asi_map_id']]
                if r['asi_map_id'] == '63':
                    mids.append('72')  # Kloner's general introduction is published with Map 101
                for mid in mids:
                    name = C.cache_name('Service_Eng.aspx/GetMapIntro', mapId=mid)
                    if name not in intro_cache:
                        with open(os.path.join(CACHE, name), encoding='utf-8') as f:
                            intro_cache[name] = C.clean(json.load(f)['d'])
                    if q in intro_cache[name]:
                        found = True
                self.assertTrue(found, (r['asi_map_id'], q))


if __name__ == '__main__':
    unittest.main()
