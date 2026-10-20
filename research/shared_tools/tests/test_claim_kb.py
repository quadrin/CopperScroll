"""Evidence invariants and end-to-end local storage; no new research evidence."""
import copy
import hashlib
import json
import sqlite3
import sys
import tempfile
import unittest
import threading
from http.server import ThreadingHTTPServer
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core import ROOT, build_index
from claim_kb.adapters import build_graph
from claim_kb.model import Graph, validate, public_view, canonical
from claim_kb.queries import Queries
from claim_kb import store
from claim_kb.locators import resolve


class EvidenceInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=build_graph(ROOT)

    def setUp(self):
        self.d=copy.deepcopy(self.data)
        self.by={r['key']:r for r in self.d['records']}

    def invalid(self,text):
        with self.assertRaisesRegex(ValueError,text):validate(self.d)

    def test_complete_graph_has_no_broken_references(self):
        self.assertEqual(validate(self.d)['status'],'valid')

    def test_duplicate_stable_ids_rejected(self):
        self.d['records'].append(copy.deepcopy(self.d['records'][0]));self.invalid('Duplicate ID')

    def test_broken_edge_rejected(self):
        self.d['edges'].append(dict(subject='claim/missing',relation='cites',object='source/missing'));self.invalid('Broken reference')

    def test_broken_payload_reference_rejected(self):
        self.by['observation/relationships-historical-east']['payload']['source_ids']=['missing'];self.invalid('Broken payload reference')

    def test_lost_locator_rejected(self):
        self.by['claim/relationships-historical-east']['locators']=[];self.invalid('Lost source locator')

    def test_lost_provenance_rejected(self):
        self.d['edges']=[e for e in self.d['edges'] if e['subject']!='claim/relationships-historical-east'];self.invalid('lost provenance')

    def test_alias_merger_rejected(self):
        self.by['identity/twin-x47']['payload']['merged']=True;self.invalid('alias/name merge')

    def test_distinct_caves_and_ambiguous_aliases_survive(self):
        for k in ['feature/iv11-cave','feature/iv17-cave','feature/twin-cave','feature/A41:XII/53','feature/A41:X/47','feature/WB:E707','feature/DJD:32']:
            self.assertIn(k,self.by)
        self.assertEqual(self.by['identity/xii53-djd32']['payload']['status'],'unverified')
        self.assertIsNone(self.by['feature/A41:XII/53']['payload']['geometry'])
        for cave,permit in [('A41:IV/11','L-603'),('A41:IV/17','L-656'),('A41:XII/53','L-608')]:
            self.assertEqual(self.by['identity/'+cave]['payload']['index_crosswalk']['permit'],permit)
        self.assertIsNone(self.by['identity/REPO:TwinCave']['payload']['index_crosswalk'])

    def test_occurrences_and_dates_remain_separate(self):
        occ=[r for r in self.d['records'] if r['kind']=='occurrence']
        self.assertEqual(len(occ),5)
        b=self.by['occurrence/T05-001']['payload']
        self.assertEqual(b['original_spelling'],'כוחלית')
        self.assertNotEqual(b['composition_date'],b['period_described'])
        self.assertIsNone(b['object_date']);self.assertIsNone(b['findspot'])
        self.assertEqual(b['place_mentioned'],'entity/kohalit-district')

    def test_atlas_unit_change_reaches_twin_without_switching_controls(self):
        affected=Queries(self.d).impact('claim/twin-unit-assignment-review')['candidate_conclusions']
        self.assertTrue(affected)
        self.assertEqual({r['record']['payload']['hypothesis_key'] for r in affected},{'hypothesis/twin'})
        for name in ['west','east','north']:
            self.assertIsNone(self.by['feature/atlas2015-twin-'+name]['payload']['world_geometry'])
        for identity in ['atlas-baradon-units','atlas-jones-north','A4-011-XII53']:
            self.assertFalse(self.by['identity/'+identity]['payload']['merged'])
        # No newly named cave or modern floor silently fills the old northern role.
        assignment=self.by['hypothesis/twin']['payload']['assignment']
        self.assertIsNone(assignment.get('northern_opening'))
        self.assertFalse(any(str(v).startswith('atlas2015-') for v in assignment.values()))

    def test_documentary_silence_does_not_replace_missing_source(self):
        silence=self.by['observation/kallai1968-pool-silence']['payload']['value']
        self.assertFalse(silence['archaeological_absence'])
        self.assertIn('19–23',silence['inspection_scope'])
        # The 1968 silence never stood in for the 1972 pages. Those pages were
        # read on 19 October 2026 and are a separate source record.
        kallai1972=self.by['source/relationships-kallai']['payload']
        self.assertEqual(kallai1972['inspection'],'already_inspected')
        self.assertIn('p. 173',kallai1972['citation'])
        self.assertNotEqual(kallai1972['repo_path'],self.by['source/followup-kallai1968']['payload']['repo_path'])
        uninspected={r['key'] for r in Queries(self.d).uninspected()['uninspected_sources']}
        self.assertIn('source/followup-gutfeld2020-fig2',uninspected)
        # Kallai's Introduction (pp. 153-157) was not received and stays uninspected.
        self.assertIn('source/decisions-kallai-unread',uninspected)

    def test_native_plan_inspection_preserves_copy_and_slice_provenance(self):
        source=self.by['source/followup-freikman2020']['payload']
        drawing=self.by['source/followup-freikman2020-fig3']
        self.assertEqual(drawing['payload']['inspection'],'already_inspected')
        self.assertNotEqual(source['asset_sha256'],source['unrelated_attachment']['sha256'])
        self.assertEqual(source['asset_sha256'],self.by['copy/freikman-owner-capture']['payload']['sha256'])
        self.assertEqual(drawing['locators'][1]['printed_page'],95)
        self.assertEqual(drawing['locators'][1]['pdf_page'],'4–5 (capture slices)')
        q=Queries(self.d).uninspected()
        self.assertIn('source/followup-freikman2020',{r['key'] for r in q['partially_inspected_sources']})
        self.assertNotIn(drawing['key'],{r['key'] for r in q['uninspected_sources']})

    def test_later_cave_names_and_directions_do_not_switch_assignments(self):
        old=self.by['observation/cohen-israel-W2-description']['payload']['value']
        later=self.by['observation/gutfeld-entrance-2017-description']['payload']['value']
        self.assertEqual(old['entrance_direction_word'],'east')
        self.assertEqual(later['direction_word'],'northeast')
        self.assertIsNone(later['azimuth'])
        self.assertIsNone(later['wall_construction_date'])
        self.assertFalse(self.by['identity/XII53-original-A']['payload']['merged'])
        self.assertIn('feature/XII53B',self.by)
        for row in self.d['records']:
            if row['kind']=='hypothesis':
                self.assertNotIn('XII53B',row['payload']['assignment'].values())
        plan=self.by['frame/icrc2017-cave53-native']['payload']
        self.assertIn('ITM',plan['crs_as_recorded'])
        self.assertIsNone(plan['geographic_registration'])
        self.assertIsNone(self.by['feature/A41:XII/53']['payload']['geometry'])

    def test_source_scope_conflict_and_target_coverage_stay_unresolved(self):
        nature=self.by['claim/freikman-natural-scope']['payload']['value']
        coverage=self.by['observation/gutfeld-sieving-scope']['payload']['value']
        self.assertFalse(nature['masonry_absence_proven'])
        self.assertFalse(coverage['negative_target_excavation_established'])
        self.assertIsNone(coverage['ancient_target_volume'])
        affected=Queries(self.d).impact('source/followup-gutfeld2020')['candidate_conclusions']
        self.assertTrue(affected)
        self.assertEqual({r['record']['payload']['hypothesis_key'] for r in affected},{'hypothesis/A41:XII/53'})
        for row in affected:
            self.assertFalse(row['record']['payload']['identification_support'])

    def test_partial_source_coverage_is_structured_and_in_impact_answers(self):
        # Exact scope must work even when a citation lacks an inspection keyword.
        source=self.by['source/followup-gutfeld2020']
        source['payload']['citation']='Gutfeld2020, pp71–80'
        answer=Queries(self.d).uninspected()
        self.assertIn(source['key'],{r['key'] for r in answer['partially_inspected_sources']})
        self.assertTrue(answer['source_dependent_conclusions'][source['key']])

    def test_later_cave53_photo_is_not_old_excavation_observation(self):
        photo=self.by['observation/hamer-cave53-photo']['payload']
        synthesis=self.by['observation/hamer-A4-011-53']['payload']
        self.assertNotEqual(photo['lineage_key'],synthesis['lineage_key'])
        self.assertEqual(photo['value']['figure6_subject'],'Gaya, not Cave53')
        self.assertIsNone(self.by['claim/twin-modern-floor-not-datum']['payload']['value'])

    def test_lost_original_spelling_rejected(self):
        self.by['occurrence/T05-001']['payload']['original_spelling']='';self.invalid('spelling/location')

    def test_alternative_readings_not_flattened(self):
        q=Queries(self.d)
        affected=q.impact('reading/e60-janoah:4')['candidate_conclusions']
        self.assertEqual(len(affected),4)
        self.assertEqual({a['record']['payload']['branch_key'] for a in affected},{'branch/RB-L'})
        e=next(r for r in self.d['records'] if r['kind']=='evaluation')
        e['payload'].pop('branch_key');self.invalid('Flattened branch')

    def test_unknown_observation_never_scores_absence(self):
        ev=next(r for r in self.d['records'] if r['kind']=='evaluation' and any(c.get('value','x') is None for c in r['payload']['checks']))
        check=next(c for c in ev['payload']['checks'] if c.get('value','x') is None)
        self.assertEqual(check['status'],'unknown');check['status']='contradicted';self.invalid('treated as absent')

    def test_repeated_publication_not_independent_evidence(self):
        groups=Queries(self.d).same_observation()['shared_original_observations']
        self.assertEqual(len(groups),1)
        self.assertEqual(groups[0]['independent_observations'],1)
        self.assertEqual(len(groups[0]['reporting_records']),4)
        self.by['observation/sion-plan5']['payload']['independent_observations']=4
        self.invalid('Citation-derived independence')

    def test_separate_observations_within_campaign_survive(self):
        a=self.by['observation/relationships-quarries-north']['payload']
        b=self.by['observation/relationships-quarries-later-phase']['payload']
        self.assertEqual(a['lineage_key'],b['lineage_key'])
        self.assertNotEqual(a['property'],b['property'])

    def test_incompatible_states_cannot_form_one_arrangement(self):
        a=self.by['state/states-iv17-cave-recorded'];b=self.by['state/xii53-W2-reported']
        a['payload']['accessible_interval_ce']=[-100,-50];b['payload']['accessible_interval_ce']=[100,200]
        self.by['hypothesis/iv17']['payload']['state_keys']=[a['key'],b['key']]
        self.invalid('Incompatible historical states')

    def test_coexistence_needs_own_observation(self):
        self.by['hypothesis/iv17']['payload']['coexistence_status']='compatible';self.invalid('Coexistence inferred')

    def test_unregistered_world_geometry_rejected(self):
        self.by['feature/iv17-north-mouth']['payload']['world_geometry']={'type':'Point','coordinates':[35.42,31.89]}
        self.invalid('geographic precision')

    def test_native_frames_and_coordinate_uncertainty_survive(self):
        frame=self.by['frame/states-iv17-plan5-crop']['payload']
        self.assertEqual(frame['units'],'px');self.assertIsNone(frame['geographic_registration'])
        self.assertIn('misprint',self.by['feature/A41:XII/53']['payload']['coordinate_basis'])

    def test_different_assignment_within_hypothesis_rejected(self):
        ev=next(r for r in self.d['records'] if r['kind']=='evaluation' and r['payload']['hypothesis_key']=='hypothesis/jericho-historical-ns1')
        ev['payload']['assignment']['pool']='jericho-reservoir-1898';self.invalid('Feature assignment changed')

    def test_check_cannot_switch_feature(self):
        ev=next(r for r in self.d['records'] if r['kind']=='evaluation')
        ev['payload']['checks'][0]['feature_ids']=['feature-from-another-model'];self.invalid('switches features')

    def test_migration_cannot_strengthen_identification(self):
        ev=next(r for r in self.d['records'] if r['kind']=='evaluation')
        ev['payload']['identification_support']=True;self.invalid('strengthened')

    def test_unreviewed_extraction_rejected(self):
        self.by['claim/relationships-historical-east']['review_status']='proposal';self.invalid('Unreviewed proposal')

    def test_protected_dependencies_removed_from_every_public_view(self):
        for visibility in ['restricted','local_only','reserved']:
            data=copy.deepcopy(self.data)
            record=next(r for r in data['records'] if r['key']=='source/relationships-dorrell')
            record['visibility']=visibility;record['payload']['secret_fixture']='NEVER_EXPORT'
            view=public_view(data);q=Queries(view)
            serialized=canonical([view,q.chronology(),q.same_observation(),q.uninspected()])
            self.assertNotIn('NEVER_EXPORT',serialized)
            self.assertNotIn(record['key'],q.by)
            with self.assertRaisesRegex(ValueError,'unavailable'):resolve(data,ROOT,record['key'],0,'a'*40)
            self.assertFalse(any(r['kind']=='evaluation' and r['payload']['hypothesis_key']=='hypothesis/jericho-historical-ns1' for r in view['records']))

    def test_replica_does_not_authenticate_original(self):
        image=next(r for r in self.d['records'] if r['kind']=='image' and r['payload']['substrate']=='replica')
        image['payload']['association_status']='authenticated';image['payload']['original_roi']=[0,0,10,10]
        self.invalid('authenticated original')

    def test_names_no_match_is_bounded(self):
        search=self.by['search/T05-062']['payload']
        self.assertEqual(search['queries'],['עצלא','עצלה'])
        self.assertFalse(search['coverage_complete']);self.assertIn('gap/asla-search-coverage',self.by)
        search['limitations']=[];self.invalid('Unbounded negative search')

    def test_all_control_branch_opportunities_preserved(self):
        q=Queries(self.d)
        for h in ['iv17','iv11','twin']:
            results=q.candidate(h)['evaluations']
            wb=[r for r in results if r['evaluation']['id'].startswith(h+'::inventory-')]
            self.assertEqual(len(wb),100)
        sets=[]
        for h in ['iv17','iv11','twin','A41:XII/53','REPO:JonesNorth']:
            sets.append({r['evaluation']['payload']['branch_key'] for r in q.candidate(h)['evaluations'] if '::regional:' in r['evaluation']['id']})
        self.assertEqual(len(sets[0]),16)
        self.assertTrue(all(s==sets[0] for s in sets))

    def test_kohlit_outcomes_match_current_assessment(self):
        rows=[r for r in self.d['records'] if r['kind']=='evaluation' and r['id'].startswith('relationships-')]
        self.assertEqual(len(rows),40)
        # 12/28 until 19 October 2026; Kallai pp. 172-173 add the eight branches
        # that use Kallai's pool (samiya-kallai, yanun-marjama-anchor).
        self.assertEqual(sum(r['payload']['status']=='contradicted' for r in rows),20)
        self.assertEqual(sum(r['payload']['status']=='unknown' for r in rows),20)
        contradicted={r['payload']['hypothesis_key'] for r in rows if r['payload']['status']=='contradicted'}
        self.assertEqual(contradicted,{'hypothesis/jericho-modern-ns1','hypothesis/samiya-crypt',
                                       'hypothesis/samiya-kallai','hypothesis/yanun-marjama-anchor'})
        kallai=self.by['acquisition/decisions-kallai-pool']['payload']
        self.assertFalse(kallai['actual_observation'])
        self.assertEqual(kallai['recorded_outcome']['row_id'],'bearing-or-phase-miss:not-east+undated')
        self.assertEqual([o['id'] for o in kallai['outcomes'] if o['recorded']],['bearing-or-phase-miss'])

    def test_all_eight_queries_return_located_records(self):
        answers=Queries(self.d).demonstrate();self.assertEqual(len(answers),8)
        def visit(obj):
            if isinstance(obj,dict):
                if 'key' in obj and 'kind' in obj:self.assertTrue(obj['locators'])
                for v in obj.values():visit(v)
            elif isinstance(obj,list):
                for v in obj:visit(v)
        visit(answers)
        self.assertTrue(answers['6_change_impact']['candidate_conclusions'])

    def test_exact_csv_and_json_source_locators(self):
        for k in ['entry/25','reading/e60-janoah:4','occurrence/T05-001',
                  'identity/A41:XII/53','evaluation/A41:XII/53::regional:B-PILLAR:cave:primary']:
            result=resolve(self.d,ROOT,k,0,'a'*40)
            self.assertIn('source_record',result,k)
        source=self.by['source/kb-xii53-native']['locators'][1]
        self.assertEqual(source['printed_page'],'208–209');self.assertEqual(source['pdf_page'],'3–4')


class VersionedStorage(unittest.TestCase):
    def setUp(self):
        fixture_dir=ROOT/'research/shared_tools/cache/tests'
        fixture_dir.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=fixture_dir);self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.cache=self.root/'cache'
        self.input=self.root/'evidence.json';self.input.write_text('{"value":1}')
        review=self.root/'research/shared_tools/claim_kb/reviewed.json'
        review.parent.mkdir(parents=True);review.write_text('{}')
        self.data=copy.deepcopy(EvidenceInvariants.data)
        self.data['inputs']={'evidence.json':hashlib.sha256(self.input.read_bytes()).hexdigest()}
        s=next(r for r in self.data['records'] if r['key']=='source/relationships-dorrell')
        s['payload']['repo_path']='evidence.json'
        self.mock=patch.object(store,'build_graph',side_effect=lambda root:copy.deepcopy(self.data))
        self.mock.start();self.addCleanup(self.mock.stop)

    def test_deterministic_build_and_history(self):
        a=store.build(self.root,self.cache);b=store.build(self.root,self.cache)
        self.assertEqual(a['snapshot'],b['snapshot'])
        self.assertEqual(len(store.history(self.cache)['snapshots']),1)

    def test_stale_rejection_impact_and_persistent_reassessment(self):
        a=store.build(self.root,self.cache)
        self.input.write_text('{"value":2}')
        with self.assertRaisesRegex(ValueError,'Stale KB'):store.load(self.root,self.cache)
        changes=store.changes(self.root,self.cache)
        self.assertEqual(changes['status'],'reassessment_required')
        self.assertTrue(changes['impact']['candidate_conclusions'])
        self.data['inputs']['evidence.json']=hashlib.sha256(self.input.read_bytes()).hexdigest()
        b=store.build(self.root,self.cache)
        current,_=store.load(self.root,self.cache)
        ev=[r for r in current['records'] if r['kind']=='evaluation' and r['payload'].get('reassessment',{}).get('required')]
        self.assertTrue(ev)
        c=store.build(self.root,self.cache)
        self.assertEqual(b['snapshot'],c['snapshot'])
        old,meta=store.load(self.root,self.cache,snapshot=a['snapshot'],allow_stale=True)
        self.assertFalse(meta['fresh'])
        self.assertNotIn('reassessment',next(r for r in old['records'] if r['key']==ev[0]['key'])['payload'])
        self.assertEqual(len(store.history(self.cache)['snapshots']),2)

    def test_source_index_rebuild_preserves_history(self):
        a=store.build(self.root,self.cache)
        note=self.root/'research/sources/test.md';note.parent.mkdir(parents=True);note.write_text('test')
        build_index(self.root,self.cache)
        self.assertEqual(store.history(self.cache)['snapshots'][0]['snapshot'],a['snapshot'])
        with sqlite3.connect(self.cache/'evidence.sqlite') as db:
            self.assertTrue(db.execute("SELECT name FROM sqlite_master WHERE name='records'").fetchone())

    def test_failed_validation_leaves_previous_result_active(self):
        a=store.build(self.root,self.cache)
        self.data['records'].append(copy.deepcopy(self.data['records'][0]))
        with self.assertRaises(ValueError):store.build(self.root,self.cache)
        _,meta=store.load(self.root,self.cache)
        self.assertEqual(meta['snapshot'],a['snapshot'])

    def test_previously_missing_dependency_invalidates_when_it_appears(self):
        self.data['inputs']['missing-note.json']='missing'
        store.build(self.root,self.cache)
        store.load(self.root,self.cache)
        (self.root/'missing-note.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'Stale KB'):store.load(self.root,self.cache)

    def test_explicit_review_acknowledgment_persists(self):
        store.build(self.root,self.cache)
        self.input.write_text('{"value":2}')
        digest=hashlib.sha256(self.input.read_bytes()).hexdigest()
        self.data['inputs']['evidence.json']=digest
        store.build(self.root,self.cache)
        current,_=store.load(self.root,self.cache)
        ev=next(r for r in current['records'] if r['kind']=='evaluation' and r['payload'].get('reassessment',{}).get('required'))
        review=self.root/'research/shared_tools/claim_kb/reviewed.json'
        review.write_text(json.dumps({'reassessment_reviews':[{
            'evaluation_key':ev['key'],'reviewer':'synthetic fixture','note':'Reviewed synthetic change',
            'input_hashes':{'evidence.json':digest}}]}))
        result=store.build(self.root,self.cache)
        after,_=store.load(self.root,self.cache)
        now=next(r for r in after['records'] if r['key']==ev['key'])
        self.assertFalse(now['payload']['reassessment']['required'])
        self.assertEqual(result['snapshot'],store.build(self.root,self.cache)['snapshot'])


class ReadOnlyHTTP(unittest.TestCase):
    def setUp(self):
        import server
        self.data=copy.deepcopy(EvidenceInvariants.data)
        source=next(r for r in self.data['records'] if r['key']=='source/relationships-dorrell')
        source['visibility']='reserved';source['payload']['private_fixture']='NEVER_IN_HTTP'
        self.version={'snapshot':'test','base_commit':'a'*40,'fresh':True,'changed_inputs':[]}
        mock=patch.object(store,'load',return_value=(self.data,self.version));mock.start();self.addCleanup(mock.stop)
        self.http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        thread=threading.Thread(target=self.http.serve_forever,daemon=True);thread.start()
        self.addCleanup(self.http.server_close);self.addCleanup(self.http.shutdown)
        self.base='http://127.0.0.1:'+str(self.http.server_port)

    def test_all_public_routes_filter_protected_dependencies(self):
        for route in ['graph','entry?id=25','claim?id=claim/relationships-quarries-later-phase',
                      'impact?id=reading/e60-janoah:4','names']+['query?number='+str(i) for i in range(1,9)]:
            with self.subTest(route=route):
                with urlopen(self.base+'/api/kb/'+route) as response:
                    text=response.read().decode();self.assertEqual(response.status,200)
                    self.assertNotIn('NEVER_IN_HTTP',text);self.assertIn('version',json.loads(text))
        with self.assertRaises(HTTPError) as failure:
            urlopen(self.base+'/api/kb/claim?id=source/relationships-dorrell')
        self.assertEqual(failure.exception.code,400)

    def test_no_write_route_or_arbitrary_file_route(self):
        with self.assertRaises(HTTPError) as failure:
            urlopen(Request(self.base+'/api/kb/graph',data=b'{}',method='POST'))
        self.assertEqual(failure.exception.code,501)
        with self.assertRaises(HTTPError):urlopen(self.base+'/api/kb/locator?id=../../AGENTS.md')

    def test_local_interface_and_schematic_are_served(self):
        for path,content_type in [('/kb','text/html'),('/kb/schema.svg','image/svg+xml')]:
            with urlopen(self.base+path) as response:
                self.assertIn(content_type,response.headers['Content-Type'])


if __name__=='__main__':unittest.main()
