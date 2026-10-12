#!/usr/bin/env python3
"""Regressions for actual feature identities, phase gates and retained alternatives."""
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('book_application', HERE / 'evaluate.py')
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


class ApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result, cls.manifest = E.build()

    def rows(self, witness):
        return [r for r in self.result['scores'] if r['witness_id'] == witness]

    def test_cave_form_never_dates_architectural_configuration(self):
        for witness in ('iv17@published-present', 'twin@published-mouth-pair',
                        'xii53@published-W2-opening'):
            rows = self.rows(witness)
            self.assertEqual(len(rows), 16)
            self.assertEqual({r['branch'].split('|')[0] for r in rows}, {'B-PILLAR', 'B-TERRACE'})
            self.assertTrue(all(r['configuration_in_window'] == E.U for r in rows))
            self.assertFalse(any(r['phase_and_datum_subset'] == E.M for r in rows))
        self.assertTrue(any(r['reported_subset_after'] == E.M
                            for r in self.rows('twin@published-mouth-pair')))
        self.assertTrue(any(r['reported_subset_after'] == E.M
                            for r in self.rows('xii53@published-W2-opening')))

    def test_atara_channel_cannot_cross_aggregate_siblings(self):
        west, east = self.rows('atara176@western-pool'), self.rows('atara176@eastern-pool')
        self.assertEqual({r['branch'] for r in west}, {r['branch'] for r in east})
        self.assertTrue(all(r['clauses_before']['conduit'] == E.U for r in west + east))
        self.assertTrue(all(r['clauses_after']['conduit'] == E.M for r in west))
        self.assertTrue(all(r['clauses_after']['conduit'] == E.U for r in east))
        self.assertTrue(all(r['clauses_after']['four'] == E.U for r in west + east))
        self.assertFalse(any(r['phase_and_datum_subset'] == E.M for r in west + east))

    def test_absalom_original_face_failure_keeps_later_access_unknown(self):
        early = [r for r in self.rows('absalom@original-south-access') if r['entry'] == 56]
        late = [r for r in self.rows('absalom@later-west-breach') if r['entry'] == 56]
        self.assertEqual(len(early), 2)
        self.assertEqual({r['reported_subset_after'] for r in early}, {E.F})
        self.assertEqual({r['clauses_after']['F7w'] for r in late}, {E.M})
        self.assertEqual({r['phase_and_datum_subset'] for r in late}, {E.U})
        for r in early + late:
            self.assertEqual(r['clauses_after']['F10'], E.U)
            self.assertEqual(r['clauses_after'].get('F11', r['clauses_after'].get('F16')), E.U)
        parents = [r['parent_record'] for r in self.result['witnesses']
                   if r['parent_id'] == 'T0247']
        self.assertTrue(all(p['chambers_F10'] == 'yes' and p['kokhim_F11'] == 'yes' for p in parents))

    def test_all_book_facts_have_explicit_identity_dispositions(self):
        ds = {d['audit_id']: d for d in self.result['audit_dispositions']}
        self.assertEqual(set(ds), {f'FP{i:02}' for i in range(1, 26)})
        self.assertIn('West-of-village', ds['FP02']['disposition'])
        self.assertIn('not ASI109/4', ds['FP10']['disposition'])
        self.assertIn('not A41VIII/2', ds['FP14']['disposition'])
        self.assertTrue(all(not d['invented_score'] for d in ds.values()))
        self.assertFalse(any('beth' in w['witness_id'] for w in self.result['witnesses']))

    def test_prior_manual_corrections_are_not_new_book_evidence(self):
        for witness in ('qelt16@aqueduct-head', 'qelt16@outlet'):
            for r in self.rows(witness):
                self.assertEqual(r['raw_period_code'], 'in')
                self.assertEqual(r['prior_manual_period_code'], 'undated')
                self.assertFalse(r['changed_clauses'])
        wall = [r for r in self.rows('qelt6@modern-aqueduct') if r['branch'].endswith('T-wall')][0]
        self.assertEqual(wall['raw_frozen_result'], E.M)
        self.assertEqual(wall['prior_manual_result'], E.U)
        self.assertEqual(wall['clauses_after']['tur'], E.U)
        self.assertEqual(wall['phase_required_subset'], E.F)

    def test_bath_import_preserves_every_existing_alternative(self):
        original = E.read_csv('research/regional/water_systems/entry46_phase_review_2026-10-12/audited_candidate_scores.csv')
        imported = [r for r in self.result['scores'] if r['entry'] == 46]
        self.assertEqual(len(original), len(imported))
        self.assertEqual({r['branch'] for r in imported},
                         {'|'.join(r[k] for k in ('function_model', 'anchor', 'radius_km')) for r in original})
        ramat = [r for r in imported if r['witness_id'] == 'ramat-I1@mamluk-cistern']
        self.assertTrue(all(r['configuration_in_window'] == E.F for r in ramat))
        self.assertFalse(any(r['full_pool_branch'] == E.M for r in imported))
        self.assertFalse(any(r['phase_and_datum_subset'] == E.M for r in imported))

    def test_source_reference_rows_and_original_inputs_survive(self):
        audits = {a['audit_id']: a for a in E.read_json(E.AUDIT)['rows']}
        for w in self.result['witnesses']:
            self.assertEqual(w['parent_row_sha256'], E.digest(E.canon(w['parent_record']).encode()))
            self.assertEqual(w['source_refs'], E.audit_refs([audits[i] for i in w['audit_ids']]))
            self.assertFalse(w['independent_confirmation'])
        for p in self.manifest['inputs']:
            content = (E.REPO / p['path']).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), p['sha256'])
        self.assertFalse(any(r['closed_assessment_reopened'] for r in self.result['scores']))
        self.assertEqual({r['identification'] for r in self.result['scores']}, {E.U})

    def test_committed_outputs_rebuild_exactly(self):
        for name, text in E.artifacts(self.result, self.manifest).items():
            self.assertEqual((HERE / name).read_text(encoding='utf-8'), text, name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
