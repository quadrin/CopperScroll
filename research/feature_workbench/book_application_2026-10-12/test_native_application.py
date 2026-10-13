#!/usr/bin/env python3
"""Guard the scientific consequences of feature, phase and count separation."""
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('native_application_test', HERE / 'evaluate_native.py')
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


class NativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result, cls.inputs = E.build()

    def rows(self, witness, entry=None):
        return [r for r in self.result['scores'] if r['witness_id'] == witness
                and (entry is None or r['entry'] == entry)]

    def test_side_position_cannot_become_measured_bearing(self):
        for ident in ('jason@forecourt-south-step', 'jason@internal-north-door'):
            rows = self.rows(ident, 56)
            face = [r for r in rows if r['model'] == 'reported-side-as-face' and r['reading'] != '56-L']
            bearing = [r for r in rows if r['model'] == 'surveyed-bearing' and r['reading'] != '56-L']
            self.assertEqual({r['reported_subset'] for r in face}, {E.F})
            self.assertEqual({r['reported_subset'] for r in bearing}, {E.U})
            self.assertTrue(all(r['clauses_after']['F7w'] == E.U for r in bearing))
        unselected = [r for r in self.rows('jason@unselected-entrance', 56) if r['reading'] != '56-L']
        self.assertTrue(all(r['reported_subset'] == E.U for r in unselected))

    def test_chambers_niches_and_column_proxy_have_distinct_roles(self):
        for w in [w for w in self.result['witnesses'] if w.get('parent_id') == 'T0226']:
            self.assertEqual(w['burial_chambers'], 2)
            self.assertEqual(w['kokhim_in_A'], 10)
            self.assertEqual(w['first_cut_kokh_count'], E.U)
            self.assertEqual(w['partly_built_kokhim'], [9, 10])
        for row in self.rows('jason@forecourt-south-step', 56):
            if row['reading'] != '56-L':
                self.assertEqual(row['clauses_after']['F10'], E.M)
        for row in self.rows('jason@forecourt-south-step', 51):
            self.assertEqual(row['clauses_after']['F2x'], E.M)
            self.assertNotEqual(row['phase_and_target_relation'], E.M)
            if 'name_zadok' in row['clauses_after']:
                self.assertEqual(row['clauses_after']['name_zadok'], E.U)
        cistern = [r for r in self.rows('jason@forecourt-south-step', 56) if r['reading'] == '56-M']
        self.assertTrue(all(r['clauses_after']['F16'] == E.U for r in cistern))

    def test_exact_group_count_failure_cannot_disprove_unlocated_other_set(self):
        pits = [w for w in self.result['witnesses'] if 'origin_row' in w]
        self.assertEqual({w['pit_count'] for w in pits}, {1, 3, 8})
        large = next(w for w in pits if w['witness_id'] == 'arnona-A@L105-L112')
        self.assertEqual(large['pit_count'], 1)
        self.assertEqual(large['locus_labels'], ['L105', 'L112'])
        for w in pits:
            group = [r for r in self.rows(w['witness_id']) if r['model'] == 'listed-source-group']
            other = [r for r in self.rows(w['witness_id']) if r['model'] == 'unlocated-other-set']
            self.assertTrue(group and other)
            self.assertTrue(all(r['phase_and_target_relation'] == E.F for r in group))
            self.assertTrue(all(r['phase_and_target_relation'] == E.U for r in other))

    def test_every_numerical_reading_survives_without_depth_conversion(self):
        readings = {(r['installation'], r['interpretation']) for r in self.result['retained_readings']}
        for w in [w for w in self.result['witnesses'] if 'origin_row' in w]:
            rows = self.rows(w['witness_id'])
            self.assertEqual({tuple(r['reading'].split('|')) for r in rows}, readings)
            for r in rows:
                if 'ten-small-pits' not in r['reading']:
                    self.assertEqual(r['clauses_after']['numerical_target'], E.U)
            self.assertTrue(all(r['clauses_after']['original_datum'] == E.U for r in rows))

    def test_native_reading_keeps_disabled_positions_and_qualifies_dates(self):
        pits = {w['witness_id']: w for w in self.result['witnesses'] if 'origin_row' in w}
        for ident in ('arnona-A@eight-pits', 'arnona-A@L105-L112', 'arnona-B@three-pits'):
            self.assertEqual(pits[ident]['position']['lat'], '')
            self.assertEqual(pits[ident]['position']['lon'], '')
            self.assertIn('disabled', pits[ident]['position']['position_kind'])
        b = pits['arnona-B@three-pits']
        self.assertEqual(b['reported_window_before'], E.M)
        self.assertEqual(b['reported_window_after_native'], E.U)
        self.assertEqual(b['parent_record']['reported_window'], E.M)
        mordot = pits['mordot-arnona@bell-pit']
        self.assertGreater(float(mordot['position']['precision_m']), 20)
        self.assertEqual(mordot['position']['range_bounds_m'], mordot['parent_record']['range_bounds_m'])

    def test_comparanda_never_acquire_invented_lane_or_map_identity(self):
        for c in self.result['source_comparanda']:
            self.assertIsNone(c['inventory_parent_id'])
            self.assertIsNone(c['geometry'])
        gibeon = [c for c in self.result['source_comparanda'] if c['witness_id'].startswith('gibeon@')]
        self.assertEqual(len(gibeon), 4)  # Three water installations and separate tunnel access.
        self.assertEqual(len({c['witness_id'] for c in gibeon}), 4)
        nasbeh = next(r for r in self.result['relation_checks'] if r['id'] == 'nasbeh-Ci320-colonnade')
        self.assertEqual(nasbeh['status'], E.F)
        self.assertFalse(nasbeh['formal_outcome_ledger_eligibility'])
        atara = next(r for r in self.result['relation_checks'] if r['id'] == 'atara-western-conduit')
        self.assertIn('inherited', atara['source_refs'][0]['original_campaign'])

    def test_source_and_parent_bytes_are_bound_and_no_closed_test_reopens(self):
        for item in self.inputs:
            self.assertEqual(hashlib.sha256((E.REPO / item['path']).read_bytes()).hexdigest(), item['sha256'])
        for witness in self.result['witnesses']:
            self.assertEqual(witness['parent_row_sha256'], E.digest(E.canon(witness['parent_record']).encode()))
            self.assertTrue(witness['source_refs'][0]['source_sha256'])
        self.assertTrue(all(not r['closed_assessment_reopened'] for r in self.result['scores']))
        self.assertEqual({r['identification'] for r in self.result['scores']}, {E.U})

    def test_saved_native_results_and_csv_rebuild_exactly(self):
        result = json.loads((HERE / 'results.json').read_text())
        self.assertEqual(result['native_application'], self.result)
        self.assertEqual((HERE / 'native_scores.csv').read_text(), E.score_csv(self.result))


if __name__ == '__main__':
    unittest.main(verbosity=2)
