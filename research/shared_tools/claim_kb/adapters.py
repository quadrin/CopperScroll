"""Allowlisted adapters. Canonical project records remain authoritative.

No PDFs, image bytes, correspondence, arrival contents or reserved keys are read.
The saved workbench is retained as a historical result; its existing evaluators
recompute the selected exploratory relationships and inventory branches.
"""
from __future__ import annotations
import csv
import importlib.util
import io
from pathlib import Path
from .model import Graph, key, sha

WB = 'research/feature_workbench/'
HERE = 'research/shared_tools/claim_kb/'
NAMES = 'research/agent_review_2026-10-07/wave1/T05_period_texts/'
REGION = 'research/regional/caves_entry25/'


def csv_rows(g, root, path):
    return list(csv.DictReader(io.StringIO(g.file(root, path))))


def evaluator(g, root, module):
    path = WB + module + '/evaluate.py'
    g.file(root, path)
    spec = importlib.util.spec_from_file_location('kb_' + module, root / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_graph(root: Path):
    g = Graph()
    overlay = g.json(root, HERE + 'reviewed.json')
    snapshot = g.json(root, WB + 'results.json')
    model = g.json(root, WB + 'relationships/model.json')
    catalog = g.json(root, WB + 'inventory/catalog.json')
    invspec = g.json(root, WB + 'inventory/queries.json')
    states = g.json(root, WB + 'states/register.json')
    plans = g.json(root, WB + 'decisions/plans.json')
    # These are previously reviewed metadata/annotations, never image bytes.
    for path in ['registration/entry25_abu_saraj_features_2026-10-01.json',
                 'registration/entry25_twin_cave_features_2026-10-01.json',
                 'research/measurements/cycle2/iv17_repeat_results.json']:
        g.file(root, path)
    relation_output = evaluator(g, root, 'relationships').build(root)
    inventory_output = evaluator(g, root, 'inventory').build(root)
    state_output = evaluator(g, root, 'states').build(root)
    register = snapshot['register']
    # Source definitions are inherited, including partial-inspection citations.
    used_sources = {}
    for module in [relation_output, inventory_output, state_output]:
        source_ids=[s['id'] for s in module['sources']]
        if len(source_ids)!=len(set(source_ids)):raise ValueError('Duplicate canonical source ID')
        for s in module['sources']:
            if s['id'] in used_sources and used_sources[s['id']]!=s:raise ValueError('Conflicting canonical source ID: '+s['id'])
            used_sources[s['id']] = s
    decision_source_ids = {s for t in plans['tasks'] if t['id'] in {
        'decisions-xii10','decisions-iv17-l656','decisions-kallai-pool','decisions-kenyon-section'} for s in t['source_ids']}
    for s in plans['sources']:
        if s['id'] in decision_source_ids and s['id'] not in {'decisions-active', 'decisions-outreach'}:
            used_sources[s['id']] = s
    for s in register['sources']:
        if s['id'].startswith('coverage-'):
            used_sources[s['id']] = s
    for s in used_sources.values():
        source_path, source_pointer = WB+'results.json', '/register/sources/'+str(next((i for i,x in enumerate(register['sources']) if x['id']==s['id']),0))
        for collection, candidate_path in [(model,WB+'relationships/model.json'),(catalog,WB+'inventory/catalog.json'),(states,WB+'states/register.json'),(plans,WB+'decisions/plans.json')]:
            for si, original in enumerate(collection['sources']):
                if original['id']==s['id']:source_path,source_pointer=candidate_path,'/sources/'+str(si)
        g.add('source', s['id'], s['title'], {**s, 'rights': 'metadata only; original rights unchanged',
              'inspection_scope': s['citation'], 'access_status': s.get('inspection')},
              source_path, source_pointer)
    # Known work/edition/copy distinctions are explicit reviewed mappings, never title heuristics.
    for r in overlay['records']:
        g.add(r['kind'], r['id'], r['label'], r['payload'], HERE + 'reviewed.json',
              '/records/' + str(overlay['records'].index(r)),
              exposure=r.get('exposure', 'derived'), visibility=r.get('visibility', 'public_metadata'))
    for edge in overlay['edges']:
        g.link(edge['subject'], edge['relation'], edge['object'])
    for identity, fields in overlay['source_locators'].items():
        g.records[key('source',identity)]['locators'].append({
            'repo_path':g.records[key('source',identity)]['payload']['repo_path'],
            'pointer':'/', 'printed_page':None,'pdf_page':None,'figure':None,
            'image_region':None,'archival_identifier':None,**fields})
    for r in overlay['records']:
        if r['kind']=='source' and (root/r['payload']['repo_path']).is_file():
            g.file(root,r['payload']['repo_path'])
    # Hash reviewed project notes where present; never follow their source links.
    for s in used_sources.values():
        p=s['repo_path']
        if (root/p).is_file():g.file(root,p)
        else:g.inputs[p]='missing'

    feature_defs = {r['id']: r for r in register['features']}
    for f in feature_defs.values():
        g.add('feature', f['id'], f['name'], f, WB+'register.json',
              '/features/' + str(register['features'].index(f)))
    g.file(root, WB+'register.json')
    for frame in states['reference_frames']:
        g.add('frame', frame['id'], frame['label'], frame, WB+'states/register.json',
              '/reference_frames/'+str(states['reference_frames'].index(frame)), sources=frame['source_ids'])
    for state in state_output['states']:
        sk = g.add('state', state['id'], state['label'], state, WB+'states/register.json',
                   '/states/'+str(next((i for i,s in enumerate(states['states']) if s['id']==state['id']),0)),
                   sources=state['source_ids'])
        g.link(sk,'state_of',key('feature',state['feature_id']))
        if state.get('reference_frame') in {f['id'] for f in states['reference_frames']}:
            g.link(sk,'uses_frame',key('frame',state['reference_frame']))
    for i,event in enumerate(states['transitions']):
        ek = g.add('event', event['id'], event['relation'], event, WB+'states/register.json',
                   '/transitions/'+str(i), sources=event['source_ids'])
        g.link(ek,'transitions_from',key('state',event['from']))
        g.link(ek,'transitions_to',key('state',event['to']))

    # Preserve individual observation identities even within a common campaign.
    observations = {}
    for output in [relation_output, inventory_output, state_output]:
        for o in output['observations']:
            observations[o['id']] = o
    for o in observations.values():
        campaigns = sorted({used_sources[s].get('original_campaign') for s in o['source_ids']
                            if used_sources[s].get('original_campaign')})
        lineage_id = 'campaign-' + sha(campaigns)[:16] if campaigns else 'source-' + o['source_ids'][0]
        lk = key('lineage',lineage_id)
        if lk not in g.records:
            g.add('lineage',lineage_id,' / '.join(campaigns) or o['source_ids'][0],
                  {'granularity':'campaign_or_reporting_lineage', 'independence':'unverified',
                   'note':'Shared campaign does not merge its separate observations or establish their independence.'},
                  WB+'results.json','/register/observations')
        payload = {**o, 'lineage_key':lk}
        # New observation adapter has a stable structured-record pointer, not a guessed page offset.
        idx = next((i for i,r in enumerate(register['observations']) if r['id']==o['id']), None)
        ok = g.add('observation',o['id'],o['property'],payload, WB+'results.json',
                   '/register/observations/'+str(idx) if idx is not None else '/modules/1',
                   exposure=o['exposure'],sources=o['source_ids'])
        g.link(ok,'same_campaign',lk)
        if o.get('feature_id'):
            g.link(ok,'about',key('feature',o['feature_id']))
        ck = g.add('claim',o['id'],o['property'],{
            'subject':key('feature',o['feature_id']), 'relationship':o['property'], 'value':o['value'],
            'analyst':'existing reviewed workbench record', 'evidence_kind':o['evidence_kind'],
            'reading_confidence':None, 'site_association':None, 'feature_identity':None,
            'positional_uncertainty':o.get('uncertainty'), 'measurement_context':{
                **{k:o.get(k) for k in ('unit','reference_frame','phase','datum')},
                'endpoints':o.get('endpoints'), 'reference_surfaces':o.get('reference_surfaces'),
                'direction_convention':o.get('direction_convention'),
                'coordinate_system':None, 'point_definition_as_recorded':o.get('reference_frame')},
            'status':'unknown' if o['value'] is None else 'info', 'supersedes':[],
            'historical_context':o.get('phase'), 'revision_basis':'versioned input hash'},
            WB+'results.json',g.records[ok]['locators'][0]['pointer'])
        g.link(ck,'derived_from',ok)
        if o['value'] is None:
            gap = g.add('gap',o['id'],o.get('note',o['property']),{
                'reason': gap_reason(o['property']), 'unknown':True, 'detail':o.get('note'),
                'absence_asserted':False},WB+'results.json',g.records[ok]['locators'][0]['pointer'])
            g.link(ck,'prerequisite',gap)

    entries(g,root)
    readings(g,root)
    relationships(g,model,relation_output)
    inventory(g,catalog,invspec,inventory_output)
    regional(g,root)
    names(g,root)

    # Acquisition records carry exact targets/conditional outcomes, without private request bodies.
    for i,t in enumerate(plans['tasks']):
        if t['id'] not in {'decisions-xii10','decisions-iv17-l656','decisions-kallai-pool','decisions-kenyon-section'}:
            continue
        payload = {k:t[k] for k in ('claim','record_needed','freeze','outcomes','current_evidence')}
        # A recorded outcome travels with its target and record files; the
        # acquisition record itself stays a target, not an observation.
        for field in ('registered_readings','cut_letter_candidates','recorded_outcome','history'):
            if field in t:payload[field]=t[field]
        payload['actual_observation'] = False
        sources = [s for s in t['source_ids'] if s in used_sources]
        ak = g.add('acquisition',t['id'],t['title'],payload,WB+'decisions/plans.json',
                   '/tasks/'+str(i),sources=sources)
        targets = {'decisions-xii10':['branch/RB-L','reading_set/e60-janoah'],
                   'decisions-iv17-l656':['hypothesis/iv17'],
                   'decisions-kallai-pool':['hypothesis/samiya-kallai'],
                   'decisions-kenyon-section':['requirement/joint-accessibility','requirement/graves-at-mouth']}[t['id']]
        for target in targets:
            g.link(ak,'would_resolve',target)
        for ri,reading in enumerate(t.get('registered_readings',[])):
            rk=g.add('reading','XII10-'+reading['id'],reading['sequence'],{
                'form':reading['sequence'],'witness_basis':'registered candidate string; no stroke vote',
                'visible_letter_observation':None,'protocol':t['freeze'],
                'meaning':None},WB+'decisions/plans.json',f'/tasks/{i}/registered_readings/{ri}')
            g.link(rk,'at_locus','locus/XII 10');g.link(rk,'cites','source/decisions-xii10-protocol')
    separating=g.json(root,WB+'decisions/separation/results.json')
    g.add('test','separation-planning-snapshot','Saved minimum separating-observation analysis',{
        **separating, 'historical_result':True,
        'currentness':'Saved conditional planning result at its recorded baseline; not rerun or upgraded by migration.',
        'identification_support':False},WB+'decisions/separation/results.json','/')
    # Canonical coverage records stay distinct from candidate outcomes and inspection status.
    coverage = next(m for m in snapshot['modules'] if m['id']=='coverage')['data']
    for name in ['obligations','coverage_observations','targets']:
        for i,row in enumerate(coverage[name]):
            identity = row.get('id',name+'-'+str(i))
            g.add('coverage',identity,row.get('label',row.get('title',identity)),
                  {'record_type':name,**row}, WB+'results.json','/modules/3/data/'+name+'/'+str(i))
    for i,result in enumerate(state_output['results']):
        tk=g.add('test',result['id'],result['title'],{
            'mode':'exploratory_historical_state_query', 'status':result['status'],
            'claim':result['claim'], 'checks':result['checks'], 'unknowns':result['unknowns'],
            'decision_rule':'Existing state evaluator; chronology and accessibility are separate gates.'},
            WB+'results.json','/modules/2/results/'+str(i),sources=result['source_ids'])
        for s in result.get('source_ids',[]):g.link(tk,'depends_on',key('source',s))
    # Explicit observation ancestry within Kenyon's single reported sequence.
    g.link('claim/relationships-quarries-chronology','derived_from','claim/relationships-quarries-later-phase')
    g.link('claim/relationships-quarries-co-use','prerequisite','claim/relationships-quarries-later-phase')
    g.link('test/relationships-quarry-phase-order','depends_on','claim/relationships-quarries-later-phase')
    for r in list(g.records.values()):
        if r['kind']=='hypothesis':
            for feature in set(r['payload']['assignment'].values()):
                if feature is not None:g.link(r['key'],'assigns',key('feature',feature))
        if r['kind']=='source' and r['payload'].get('inspection')=='not_inspected':
            gap=g.add('gap','inspection-'+r['id'],r['label'],{
                'reason':'uninspected_source','unknown':True,'absence_asserted':False,
                'target':r['payload']['citation']},r['locators'][0]['repo_path'],r['locators'][0]['pointer'])
            g.link(r['key'],'prerequisite',gap)
    # Capture every adapter/schema dependency. Index generation never reads other research files.
    for path in sorted((root/HERE).glob('*.py')):
        g.file(root,path.relative_to(root).as_posix())
    g.file(root,HERE+'schema.json')
    g.file(root,'research/shared_tools/core.py')
    return g.export()


def gap_reason(prop):
    if any(x in prop for x in ['phase','chronology','construction','period']): return 'uncertain_phase'
    if any(x in prop for x in ['origin','threshold','datum']): return 'missing_reference_point'
    if any(x in prop for x in ['bear','direction','corner','width']): return 'unestablished_geometry'
    return 'not_recorded'


def entries(g,root):
    from core import entry_packets
    for p in ['tables/entry_concordance.csv','tables/feature_constraints.csv','text/readings.json','text/translation_en.json']:
        g.file(root,p)
    for packet in entry_packets(root)['entries']:
        ek = g.add('entry',packet['entry'],'Entry '+packet['entry'],packet,
                  'tables/entry_concordance.csv','/entry_puech='+packet['entry'])
        if packet['entry'] in {'11','18','25','60'}:
            lk=g.add('locus',packet['canonical_lines'],packet['canonical_lines'],{
                'entry_id':packet['entry'],'edition_concordance':packet['edition_concordance'],
                'boundary_note':packet['boundary_note'],'physical_segments':None},
                'tables/entry_concordance.csv','/entry_puech='+packet['entry'])
            g.link(lk,'in_entry',ek)
            tk = g.add('translation',packet['entry'],'Project translation, entry '+packet['entry'],{
                'lines':packet['translation_context'],'basis':'edition-based project translation',
                'boundary_note':packet['boundary_note']},'text/translation_en.json','/entry-context/'+packet['entry'])
            g.link(tk,'in_entry',ek)
            g.records[tk]['locators']=[{'repo_path':'text/translation_en.json','pointer':'/'+line['line'],
                'printed_page':None,'pdf_page':None,'figure':None,'image_region':None,'archival_identifier':None}
                for line in packet['translation_context']]


def readings(g,root):
    for i,r in enumerate(g.json(root,'text/readings.json')):
        if str(r.get('entry')) not in {'11','18','25','60'}: continue
        rk=g.add('reading_set',r['id'],r['label'],r,'text/readings.json','/'+str(i))
        g.link(rk,'in_entry',key('entry',r['entry']))
        for j,edition in enumerate(r['readings']):
            ek = g.add('reading',r['id']+':'+str(j),edition['who'],{
                'form':edition['reading'] or None,'author':edition['who'], 'edition_locator':edition['ref'] or None,
                'witness_basis':'edition-based', 'visible_letter_observation':None,
                'locus_as_recorded':r['line'], 'restoration_segmentation':'unreviewed'},
                'text/readings.json',f'/{i}/readings/{j}')
            g.link(ek,'derived_from',rk)
            ik = g.add('interpretation',r['id']+':'+str(j),edition['meaning'],{
                'meaning':edition['meaning'], 'author':edition['who'],
                'layer':'grammatical_attachment' if r['id']=='e25-direction' else 'lexical_or_identification_interpretation',
                'identity_is_proposal':True},'text/readings.json',f'/{i}/readings/{j}')
            g.link(ik,'interprets',ek)
    mapping=g.json(root,'research/shared_tools/mapping_claims.json')
    g.add('witness','3Q15','Copper Scroll original object',{'substrate':'original_object','object_date':None},
          'research/shared_tools/mapping_claims.json','/')
    selected=next((m for m in mapping if m['locus']=='XII 10'))
    lk=g.add('locus','XII 10','XII 10',selected,'research/shared_tools/mapping_claims.json','/'+str(mapping.index(selected)))
    g.link(lk,'about','witness/3Q15');g.link(lk,'in_entry','entry/60')
    for cut in selected['candidate_cuts']:
        sk=g.add('segment',str(cut),'Physical cut '+str(cut),{'cut_as_catalogued':cut,'object':'3Q15'},
                 'research/shared_tools/mapping_claims.json','/'+str(mapping.index(selected)))
        g.link(lk,'catalogue_association',sk)
    # Reuse manuscript metadata adapter, without opening any photograph.
    from core import manuscript
    for p in ['index.csv','cuts_01_10_preview_manifest.csv','remaining_preview_manifest.csv']:
        g.file(root,'research/sources/usc_copper_scroll_images/'+p)
    for image in manuscript(root)['images']:
        if image.get('cut_as_catalogued') not in [21,22] and not (image.get('substrate')=='replica' and image.get('column_as_catalogued')==12):continue
        ik=g.add('image',image['id'],image.get('title',image['id']),{
            **image, 'association_status':selected['status'],'original_roi':None,
            'rights_as_recorded':image['rights'],
            'export_policy':'Catalogue metadata only. No image bytes or crop exported.'},
            'research/sources/usc_copper_scroll_images/index.csv','/id='+str(image['id']))
        g.link(ik,'catalogue_association',lk)
    for r in overlay_gaps():
        g.add('gap',r[0],r[1],{'reason':r[2],'unknown':True,'absence_asserted':False},
              'research/shared_tools/mapping_claims.json','/'+str(mapping.index(selected)))
    g.link('locus/XII 10','prerequisite','gap/original-XII10')
    g.link('reading_set/e60-janoah','prerequisite','gap/original-XII10')


def overlay_gaps():
    return [('original-XII10','No authenticated legible original-locus stroke observation imported','unregistered_image'),
            ('editorial-segmentation','Letter/restoration segmentation needs editorial review; braces remain verbatim','unsegmented_editorial_layer')]


def relationships(g,model,output):
    path=WB+'relationships/model.json'
    basis={'RB-M':['interpretation/e60-opening:1'], 'RB-P':['interpretation/e60-opening:0'],
           'RB-L':['interpretation/e60-janoah:4'], 'RB-B':[]}
    for i,r in enumerate(model['readings']):
        bk=g.add('branch',r['id'],r['label'],r,path,'/readings/'+str(i),sources=r['source_ids'])
        for interpretation in basis[r['id']]:g.link(bk,'depends_on',interpretation)
        if not basis[r['id']]:g.link(bk,'depends_on','source/relationships-text-e60')
        g.link(bk,'in_entry','entry/60')
    for i,p in enumerate(model['predicates']):
        rk=g.add('requirement',p['id'],p['label'],p,path,'/predicates/'+str(i),sources=p['source_ids'])
        for branch in p['required_for']:
            g.link(rk,'under_branch',key('branch',branch))
            g.link(key('branch',branch),'requires',rk)
        if p['id'].startswith('pool-'):g.link(rk,'depends_on','interpretation/e11-kohlit:0')
    for i,a in enumerate(model['assignments']):
        g.add('hypothesis',a['id'],a['label'],{**a,'assignment':a['roles'],
              'coexistence_status':'unknown','state_keys':[], 'entry_ids':['11','60']},
              path,'/assignments/'+str(i),sources=a['source_ids'])
    test=g.add('test','relationships','Koḥlit finite assignment comparison',{
        'mode':'exploratory', 'specification':path,'specification_sha256':g.inputs[path],
        'retained_branches':[r['id'] for r in model['readings']],
        'candidate_control_set':[a['id'] for a in model['assignments']],
        'decision_rule':'Conjunction of necessary predicates. Contradiction rejects only this assigned branch; unknown remains unknown.',
        'windows':model['windows'],'identification_support':False,'unused_prediction':None,
        'scope':output['scope'],'limits':model['limits']},path,'/')
    bmap={b['id']:b for b in output['data']['branches']}
    for i,r in enumerate(output['results']):
        if r['id'] not in bmap: # Keep the quarry phase diagnostic as an explicit distinct test.
            g.add('test',r['id'],r['title'],r,WB+'results.json','/modules/0/results/'+str(i),sources=r['source_ids'])
            continue
        b=bmap[r['id']]; a=next(a for a in model['assignments'] if a['id']==b['assignment_id'])
        ek=g.add('evaluation',r['id'],r['title'],{
            **r,'branch_key':key('branch',b['reading_id']), 'hypothesis_key':key('hypothesis',a['id']),
            'window_id':b['window_id'], 'assignment':a['roles'], 'mode':'exploratory',
            'identification_support':False},WB+'results.json','/modules/0/results/'+str(i),sources=r['source_ids'])
        g.link(ek,'in_test',test);g.link(ek,'under_branch',key('branch',b['reading_id']))
        g.link(ek,'evaluates',key('hypothesis',a['id']))
        for check in r['checks']:
            ck=g.add('claim',check['id'],check['label'],claim_payload(check),
                     WB+'results.json','/modules/0/results/'+str(i)+'/checks/'+str(r['checks'].index(check)),sources=check['source_ids'])
            g.link(ek,'depends_on',ck)
            g.link(ck,'evaluates',key('requirement',check['value']['predicate_id']))
            for obs in check['value'].get('observation_ids',[]):
                g.link(ck,'conflicts' if check['status']=='contradicted' else 'supports',key('claim',obs))


def claim_payload(check):
    value=check.get('value'); context=value if isinstance(value,dict) else {}
    return {'subject':context.get('resolved_subject') or check.get('feature_ids',[]),
            'relationship':context.get('relation',check.get('property','satisfies_requirement')),
            'value':value,'analyst':'existing reviewed evaluator','evidence_kind':'inference',
            'reading_confidence':None,'site_association':None,'feature_identity':None,
            'positional_uncertainty':check.get('uncertainty'), 'status':check['status'],
            'measurement_context':{k:check.get(k) for k in ('phase','unit','reference_frame','datum')},
            'detail':check['detail'],'supersedes':[]}


def inventory(g,catalog,spec,output):
    path=WB+'inventory/catalog.json'
    for di,dim in enumerate(spec['dimensions']):
        for oi,option in enumerate(dim['options']):
            g.add('interpretation','inventory:'+dim['id']+':'+option['id'],option['label'],{
                **option,'dimension':dim['id'],
                'layer':'lexical' if dim['id']=='reading' else 'grammatical_attachment' if dim['id']=='orientation' else 'explicit_model_choice',
                'authority_note':'Retained workbench option; model alternatives do not imply a newly verified editorial disagreement.'},
                WB+'inventory/queries.json',f'/dimensions/{di}/options/{oi}',sources=dim.get('source_ids',[]))
    for i,c in enumerate(catalog['candidates']):
        assignment={'cave':c['feature_ids'][0],**{f:f for f in c['feature_ids'][1:]}}
        g.add('hypothesis',c['id'],c['name'],{**c,'assignment':assignment,'entry_ids':['25'],
              'coexistence_status':'unknown','state_keys':[]},path,'/candidates/'+str(i),sources=c['source_ids'])
    for qi,q in enumerate(output['data']['queries']):
        tk=g.add('test',q['id'],q['title'],{**{k:v for k,v in q.items() if k!='candidate_results'},
            'mode':'exploratory','specification':WB+'inventory/queries.json',
            'specification_sha256':g.inputs[WB+'inventory/queries.json'],
            'decision_rule':'Existing inventory evaluator; conjunction of necessary predicates.',
            'candidate_control_set':[c['id'] for c in catalog['candidates']],
            'identification_support':False},WB+'inventory/queries.json','/queries/'+str(qi),sources=q['source_ids'])
        for branch in q['branches']:
            bk=g.add('branch',branch['id'],str(branch['choices']),branch,WB+'inventory/queries.json',f'/queries/{qi}')
            g.link(bk,'in_entry','entry/25');g.link(bk,'depends_on','reading_set/e25-direction')
            g.link(bk,'cites','source/inventory-puech-entry25')
            for dimension,option in branch['choices'].items():
                g.link(bk,'depends_on','interpretation/inventory:'+dimension+':'+option)
        for ci,cr in enumerate(q['candidate_results']):
            h=g.records[key('hypothesis',cr['candidate_id'])]['payload']
            for bi,b in enumerate(cr['branches']):
                identity=cr['candidate_id']+'::'+b['branch_id']
                ek=g.add('evaluation',identity,cr['candidate_id']+' · '+b['branch_id'],{
                    **b,'branch_key':key('branch',b['branch_id']), 'hypothesis_key':key('hypothesis',cr['candidate_id']),
                    'assignment':h['assignment'],'mode':'exploratory','identification_support':False},
                    WB+'results.json',f'/modules/1/data/queries/{qi}/candidate_results/{ci}/branches/{bi}')
                g.link(ek,'in_test',tk);g.link(ek,'evaluates',key('hypothesis',cr['candidate_id']))
                g.link(ek,'under_branch',key('branch',b['branch_id']))
                for check in b['checks']:
                    rid=b['branch_id']+'::'+check['id']
                    rk=key('requirement',rid)
                    if rk not in g.records:
                        g.add('requirement',rid,check['label'],{'property':check['property'],
                            'branch_key':key('branch',b['branch_id']), 'layer':'derived_requirement'},
                            WB+'inventory/queries.json',f'/queries/{qi}',sources=q['source_ids'])
                        g.link(rk,'under_branch',key('branch',b['branch_id']))
                        g.link(rk,'depends_on',key('branch',b['branch_id']))
                    g.link(ek,'evaluates',rk)
                    obs='inventory-'+cr['candidate_id']+'-'+check['property'].replace('_','-')
                    # Use the evaluator's exact observation IDs, not guessed identities.
                    matches=[r['key'] for r in g.records.values() if r['kind']=='observation'
                             and r['payload'].get('property')==check['property']
                             and r['payload'].get('feature_id') in h['assignment'].values()
                             and r['id'].startswith('inventory-'+cr['candidate_id']+'-')]
                    for match in matches:g.link(ek,'depends_on',match)
                    for source in check['source_ids']:g.link(ek,'cites',key('source',source))


def regional(g,root):
    rows=csv_rows(g,root,REGION+'caves.csv')
    selected={'A41:IV/17':'iv17','A41:IV/11':'iv11','A41:XII/53':'A41:XII/53',
              'REPO:TwinCave':'twin','REPO:JonesNorth':'REPO:JonesNorth'}
    # Historical roster/specification is preserved in full, selected evaluations only are materialized.
    spec=g.file(root,REGION+'PLAN.md')
    for p in ['AMENDMENT_1.md','coded/a41_index_crosswalk.csv','README.md']:
        g.file(root,REGION+p)
    index_rows=csv_rows(g,root,REGION+'coded/a41_index_crosswalk.csv')
    index={r['pub_id']:r for r in index_rows}
    if len(index)!=len(index_rows):raise ValueError('Duplicate cave-index identity')
    for cave,identity in selected.items():
        row=next(r for r in rows if r['cave_id']==cave)
        if key('hypothesis',identity) not in g.records:
            fk=g.add('feature',cave,row['name_number'],{
                'site':row['where_described'],'kind':'cave','geometry':None,
                'catalogue_coordinates_as_recorded':row['coord_printed'],
                'coordinate_basis':row['coord_basis'],'coordinate_status':row['coord_ok'],
                'note':'Unregistered/ambiguous catalogue grid is retained as text; world location stays null.'},
                REGION+'caves.csv','/cave_id='+cave)
            g.add('hypothesis',identity,row['name_number'],{'assignment':{'cave':cave},
                'entry_ids':['25'],'coexistence_status':'unknown','state_keys':[],
                'target_prerequisites':'not evaluated in the original three-cave workbench; explicit gap'},
                REGION+'caves.csv','/cave_id='+cave)
        crosswalk=index.get(cave)
        if crosswalk and crosswalk['permit'] and crosswalk['permit'] not in row['other_ids']:
            raise ValueError('Catalogue permit crosswalk changed; review before migration: '+cave)
        identity_key=g.add('identity',cave,'Catalogue identity: '+cave,{
            'written_label':row['name_number'],'other_labels':row['other_ids'],
            'target':key('hypothesis',identity),'proposer':'reviewed regional catalogue compiler',
            'evidence':row['source_records'],'status':'catalogue_crosswalk_as_recorded',
            'merged':False,'notes':row['notes'],'index_crosswalk':crosswalk,
            'verification':'Reviewed catalogue rows agree; physical identity remains separately assessed' if crosswalk else 'No reviewed index crosswalk; labels retained without merging'},REGION+'caves.csv','/cave_id='+cave)
        if crosswalk:
            g.records[identity_key]['locators'].append({
                'repo_path':REGION+'coded/a41_index_crosswalk.csv','pointer':'/pub_id='+cave,
                'printed_page':None,'pdf_page':None,'figure':None,'image_region':None,
                'archival_identifier':crosswalk['permit'] or None})
    tk=g.add('test','regional-entry25','Frozen regional Entry 25 form comparison',{
        'mode':'exploratory','specification':REGION+'PLAN.md','specification_sha256':g.inputs[REGION+'PLAN.md'],
        'freeze_commit':'2ff6e5acde5caaea47917dc0fb4269dfc8173609',
        'candidate_control_set':[r['cave_id'] for r in rows],
        'materialized_subset':list(selected),'limits':'Full source roster retained; five selected rows displayed. Coverage incomplete. No landscape rarity or identification inference.',
        'decision_rule':'Saved C1–C5 codes under each of four separate rulesets; no combined rescue model.',
        'identification_support':False},REGION+'PLAN.md','/')
    for row in csv_rows(g,root,REGION+'scores.csv'):
        if row['cave_id'] not in selected:continue
        bid='regional:'+':'.join(row[k] for k in ['branch','orientation','ruleset'])
        bk=key('branch',bid)
        if bk not in g.records:
            g.add('branch',bid,bid,{'reading':row['branch'],'orientation':row['orientation'],
                  'ruleset':row['ruleset']},REGION+'scores.csv','/branch='+bid)
            g.link(bk,'in_entry','entry/25');g.link(bk,'depends_on','reading_set/e25-direction')
            g.link(bk,'cites','source/inventory-puech-entry25')
        identity=selected[row['cave_id']];h=g.records[key('hypothesis',identity)]['payload']
        status={'match':'compatible','all-match':'compatible','fail':'contradicted','unknown':'unknown'}
        cave_row=next(r for r in rows if r['cave_id']==row['cave_id'])
        labels={'c1':'Cave','c2':'Pillar / terrace association','c3':'Two exterior openings',
                'c4':'Retained eastward aspect','c5':'Northern member distinguishable'}
        basis={'c1':'feature_type_source','c2':'pillar_basis' if row['branch']=='B-PILLAR' else 'terrace_basis',
               'c3':'openings_basis','c4':'facing_basis','c5':'northern_basis'}
        sources=['kb-xii53-native'] if row['cave_id']=='A41:XII/53' else h.get('source_ids',[])
        checks=[{'id':c,'label':labels[c],'status':status[row[c]],
                 'detail':'Frozen '+row['ruleset']+' code '+row[c]+'. '+(cave_row[basis[c]] or 'No source-controlled statement for this property.'),
                 'feature_ids':[],'source_ids':sources} for c in ['c1','c2','c3','c4','c5']]
        ek=g.add('evaluation',row['cave_id']+'::'+bid,row['cave_id']+' · '+bid,{
            **row,'status':status[row['result']], 'branch_key':bk,'hypothesis_key':key('hypothesis',identity),
            'assignment':h['assignment'],'checks':checks,'mode':'exploratory','identification_support':False},
            REGION+'scores.csv','/cave_id='+row['cave_id']+'/branch='+bid)
        g.link(ek,'in_test',tk);g.link(ek,'under_branch',bk);g.link(ek,'evaluates',key('hypothesis',identity))
        g.link(ek,'depends_on',key('identity',row['cave_id']))
        for check in checks:
            rid=bid+'::'+check['id'];rk=key('requirement',rid)
            if rk not in g.records:
                g.add('requirement',rid,check['label'],{
                    'branch_key':bk,'source_clause':check['id'],'specification':REGION+'PLAN.md',
                    'layer':'retained_regional_predicate'},REGION+'PLAN.md','/')
                g.link(rk,'depends_on',bk)
            g.link(ek,'evaluates',rk)
        if row['cave_id']=='A41:XII/53':g.link(ek,'cites','source/kb-xii53-native')
        else:
            for s in h.get('source_ids',[]):g.link(ek,'cites',key('source',s))


def names(g,root):
    path=NAMES+'data/attestation_concordance.json'
    rows=g.json(root,path)
    g.file(root,NAMES+'REPORT.md')
    coverage=csv_rows(g,root,NAMES+'data/source_coverage.csv')
    for name in ['Kohlit','Asla']:
        g.add('name',name,name,{'search_form':name,'external_match_status':'reviewed_external_attestations' if name=='Kohlit' else 'no_external_match_within_recorded_scope'},path,'/name='+name)
    g.add('entity','scroll-kohlit','Koḥlit as mentioned by 3Q15',{
        'entity_type':'proposed_place','geometry':None,'location':None,
        'identity_status':'unidentified'},path,'/0')
    g.add('entity','kohalit-district','Koḥalit district in b. Qiddushin 66a',{
        'entity_type':'textual_place_referent','geometry':None,'location':None,
        'context':'District in the wilderness; geography unestablished'},path,'/0')
    for i,row in enumerate(rows):
        # Keep occurrences individual. T05-003 groups three loci and manuscript variants;
        # it remains an explicit segmentation gap, never fabricated into three exact forms.
        if row['id'] not in ['T05-001','T05-002','T05-062']:continue
        if row['id']=='T05-062':
            sk=g.add('search',row['id'],'ʿAṣla bounded unsuccessful search',{
                **row,'name_key':'name/Asla','queries':['עצלא','עצלה'],
                'corpora':['Sefaria corpus','Eusebius Onomasticon (Wolf translation)'],
                'spelling_variants':['עצלא','עצלה'],
                'inspection_scope':'T05-062 and T05 report; no name-specific exhaustive inspection log',
                'coverage_as_recorded':coverage,'result':'no_external_match',
                'limitations':['Exact-word searches can miss prefixed forms.',
                    'Onomasticon Greek/Latin were not inspected by the reviewed search.',
                    'Corpus-wide coverage is not proof that every item was inspected for this name.',
                    'Arabic toponym is an association; period attestation is unestablished.'],
                'coverage_complete':False},path,'/'+str(i))
            g.link(sk,'searched_for','name/Asla')
            gap=g.add('gap','asla-search-coverage','Name-specific negative-search coverage remains incomplete',{
                'reason':'incomplete_coverage','unknown':True,'absence_asserted':False},path,'/'+str(i))
            g.link(sk,'prerequisite',gap)
            continue
        ok=g.add('occurrence',row['id'],row['reference'],{
            'name_key':'name/Kohlit','original_spelling':'כוחלית',
            'attested_spelling_as_recorded':row['attested_form'],
            'normalized_search_forms':['כוחלית','כחלת'], 'language':'Hebrew',
            'source_location':row['reference'], 'context':row['quote'],
            'proposed_referent':row['location_implied'],'findspot':None,
            'place_mentioned':'entity/kohalit-district' if row['id']=='T05-001' else None,
            'composition_date': {'range_ce':[500,600],'basis':'reviewed approximate Bavli redaction, not a manuscript date'} if row['id']=='T05-001' else {'range_ce':[200,200],'basis':'reviewed approximate compilation date'},
            'object_date':None,
            'period_described':{'range_ce':[-103,-76],'basis':'historical reign mentioned, from reviewed T05-001'} if row['id']=='T05-001' else None,
            'date_as_recorded':row['date'],'dating_limit':'approximate composition attribution; exact manuscript witness unspecified',
            'spelling_scope':'quoted phrase / manuscript alternatives as recorded, not a collated physical witness',
            'source_url':row['source_url']},path,'/'+str(i))
        g.link(ok,'occurrence_of','name/Kohlit');g.link(ok,'cites','source/kb-name-review')
        if row['id']=='T05-001':g.link(ok,'mentions','entity/kohalit-district')
    # Scroll occurrences are entry/locus-specific; preserve written strings, including alternatives.
    for identity,name,entry,locus,form in [('scroll-kohlit-II13','Kohlit','11','II 13','כחלת'),
           ('scroll-kohlit-XII10','Kohlit','60','XII 10','כחלת'),
           ('scroll-asla-IV9','Asla','18','IV 9–10','העצלא')]:
        ok=g.add('occurrence',identity,name+' · '+locus,{
            'name_key':key('name',name),'original_spelling':form,'language':'Hebrew',
            'source_location':'3Q15 '+locus,'findspot':None,'place_mentioned':None,
            'composition_date':None,'object_date':None,'period_described':None,
            'proposed_referent':None,'context':'Edition-based occurrence; reading alternatives retained.',
            'normalized_search_forms':[form]},'text/readings.json','/id='+('e18-asla' if name=='Asla' else 'e11-kohlit' if entry=='11' else 'e60-kohlit'))
        g.link(ok,'occurrence_of',key('name',name));g.link(ok,'in_entry',key('entry',entry))
        if name=='Kohlit':
            g.records[ok]['payload']['place_mentioned']='entity/scroll-kohlit'
            g.link(ok,'mentions','entity/scroll-kohlit')
    g.link('occurrence/scroll-kohlit-II13','same_spelling','occurrence/scroll-kohlit-XII10')
    g.link('occurrence/scroll-asla-IV9','depends_on','reading_set/e18-asla')
    ik=g.add('identity','kohlit-talmud','Proposed Koḥlit / Koḥalit referent identity',{
        'proposer':'reviewed T05 analyst, T05-006','evidence':'T05-001 vs scroll occurrences; spelling differs',
        'status':'unproven','merged':False, 'same_referent':None,
        'relation':'proposed_same_referent','scope':'A common referent remains a hypothesis; no site follows.'},path,'/5')
    g.link(ik,'proposed_same_referent','occurrence/T05-001')
    g.link(ik,'proposed_spelling_variant','occurrence/scroll-kohlit-II13')
    g.link(ik,'proposed_same_referent','entity/scroll-kohlit')
    g.link(ik,'proposed_same_referent','entity/kohalit-district')
