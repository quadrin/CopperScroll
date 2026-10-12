#!/usr/bin/env python3
"""Regression checks for unsupported function/date/access transfer."""
import gzip
import json
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import evaluate as E


class PhaseReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import csv
        with gzip.open(HERE / 'phases.csv.gz', 'rt', encoding='utf-8', newline='') as f:
            cls.phases = list(csv.DictReader(f))
        with gzip.open(HERE / 'scores.csv.gz', 'rt', encoding='utf-8', newline='') as f:
            cls.scores = list(csv.DictReader(f))

    def one(self, phase, model='contained-water', anchor='ein_kerem', radius='2'):
        return next(r for r in self.scores if r['phase_id'] == phase and
                    r['function_model'] == model and r['anchor'] == anchor and r['radius_km'] == radius)

    def test_reported_pool_and_period_do_not_prove_phase_function(self):
        p = E.default_phase(dict(id='control', name='reported reservoir', source='report', locator='p1',
                                 type='reservoir_pool', aggregate='no', lat='31.76', lon='35.17',
                                 precision_m='10', date_code='in', entrance='yes'))
        self.assertEqual(p['reported_contained_water'], E.S.M)
        self.assertEqual(p['contained_water'], E.S.U)
        self.assertEqual(p['same_phase'], E.S.U)
        self.assertEqual(p['configuration_in_window'], E.S.U)

    def test_removed_rogem_stairs_do_not_exclude_other_entrance(self):
        r = self.one('rogem-C2@later-rainwater-cistern')
        self.assertEqual(r['stair_origin_screen'], E.S.F)
        self.assertEqual(r['entrance'], E.S.U)
        self.assertEqual(r['full_pool_branch'], E.S.U)

    def test_medieval_ramat_phase_fails_window_independently(self):
        r = self.one('ramat-I1@mamluk-cistern')
        self.assertEqual(r['entrance'], E.S.U)
        self.assertEqual(r['configuration_in_window'], E.S.F)
        self.assertEqual(r['full_pool_branch'], E.S.F)

    def test_bath_containment_does_not_establish_service_storage(self):
        for phase, anchor in [('armon-L5@stepped-bath', 'ramat_rahel'),
                              ('rogem-C2@tentative-stepped-bath', 'ein_kerem'),
                              ('ramat-I1@second-temple-bath', 'ein_kerem')]:
            with self.subTest(phase=phase):
                broad = self.one(phase, anchor=anchor)
                strict = self.one(phase, model='storage-use', anchor=anchor)
                self.assertEqual(broad['phase_join_screen'], E.S.M)
                self.assertEqual(strict['function'], E.S.U)
                self.assertEqual(broad['configuration_in_window'], E.S.U)
                self.assertEqual(broad['full_pool_branch'], E.S.U)

    def test_radii_and_anchors_are_not_borrowed(self):
        self.assertEqual(self.one('armon-L5@stepped-bath', anchor='ramat_rahel', radius='1')['place'], E.S.F)
        self.assertEqual(self.one('armon-L5@stepped-bath', anchor='ramat_rahel')['place'], E.S.M)
        self.assertEqual(self.one('armon-L5@stepped-bath')['place'], E.S.F)

    def test_possible_collecting_vat_is_not_a_water_basin_by_shape(self):
        r = self.one('rogem-C2@possible-collecting-vat')
        self.assertEqual(r['function'], E.S.U)
        self.assertEqual(r['configuration_in_window'], E.S.U)

    def test_no_cross_phase_union_or_complete_unsupported_match(self):
        self.assertNotIn(E.S.M, {r['full_pool_branch'] for r in self.scores})
        self.assertEqual(len(self.scores), len(self.phases) * 8)
        self.assertEqual(len({r['phase_id'] for r in self.phases}), len(self.phases))

    def test_governing_rule_ids_and_exposure_limits_are_retained(self):
        summary = json.loads((HERE / 'summary.json').read_text())
        rules = json.loads((E.REPO / 'research/sources/full_reads_2026-10-12/storage_language_audit/function_rules.json').read_text())
        self.assertEqual(set(summary['function_rule_ids'].values()), {r['id'] for r in rules['function_branches']})
        self.assertIn('deep-pit', summary['excluded_reading'])
        self.assertTrue(summary['exploratory'])


if __name__ == '__main__':
    unittest.main()
