"""Public atlas output must preserve reviewed provenance and exposure limits."""
import copy
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core import ROOT
from claim_kb.adapters import build_graph
from claim_kb.model import canonical
from claim_kb.web_export import project, build


class PublicAtlasSnapshot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph=build_graph(ROOT)

    def test_projection_is_deterministic_and_preserves_source_locators(self):
        a=project(self.graph);b=project(copy.deepcopy(self.graph))
        self.assertEqual(canonical(a),canonical(b))
        self.assertEqual(len(a['entries']),61)
        r=next(r for r in a['records'] if r['key']=='source/followup-freikman2020-fig3')
        self.assertEqual(r['locators'][1]['printed_page'],95)
        self.assertEqual(r['locators'][1]['pdf_page'],'4–5 (capture slices)')
        self.assertIn('uninspected_parts',next(r for r in a['records'] if r['key']=='source/followup-gutfeld2020')['payload'])

    def test_protected_dependency_never_reaches_a_public_index(self):
        for visibility in ['reserved','restricted','local_only']:
            data=copy.deepcopy(self.graph)
            source=next(r for r in data['records'] if r['key']=='source/followup-gutfeld2020')
            source['visibility']=visibility
            source['payload']['private_fixture']='DO_NOT_EXPORT_THIS'
            result=project(data);raw=canonical(result)
            self.assertNotIn('DO_NOT_EXPORT_THIS',raw)
            self.assertNotIn('claim/gutfeld-northeast-aspect',{r['key'] for r in result['records']})
            keys={r['key'] for r in result['records']}
            for records in result['entries'].values():self.assertLessEqual(set(records),keys)
            for e in result['edges']:
                self.assertIn(e['subject'],keys);self.assertIn(e['object'],keys)

    def test_checked_in_atlas_snapshot_matches_reviewed_inputs(self):
        path=ROOT/'atlas/app/atlas-kb.json'
        self.assertEqual(path.read_text(encoding='utf-8'),canonical(project(self.graph))+'\n')

    def test_review_notices_preserve_scores_and_reach_only_dependents(self):
        original={r['key']:copy.deepcopy(r['payload']) for r in self.graph['records']}
        exported=project(self.graph)
        notices=[]
        for r in exported['records']:
            if r['kind']=='evaluation' and r['payload'].get('reassessment',{}).get('required'):
                notices.append(r)
                self.assertEqual(r['payload']['status'],original[r['key']]['status'])
                self.assertTrue(r['payload']['reassessment']['trigger_keys'])
        self.assertEqual({r['payload']['hypothesis_key'] for r in notices},
                         {'hypothesis/twin','hypothesis/A41:XII/53'})
        self.assertEqual(len(notices),132)
        # A projection must not mutate the accepted graph supplied by its caller.
        self.assertEqual(original,{r['key']:r['payload'] for r in self.graph['records']})

    def test_sparse_checkout_cannot_publish_tracked_inputs_as_missing(self):
        data=copy.deepcopy(self.graph)
        data['inputs']['research/ACTIVE_TEST.md']='missing'
        with patch('claim_kb.web_export.build_graph',return_value=data):
            with self.assertRaisesRegex(ValueError,'not materialized'):
                build(ROOT)
