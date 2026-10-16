"""Pure reusable queries. All evidence traversal returns typed IDs and locators."""
from __future__ import annotations
from collections import defaultdict, deque

DEPENDENCIES = {'depends_on','derived_from','cites','reports','supports','conflicts',
                'prerequisite','evaluates','under_branch','in_test','interprets','state_of',
                'uses_frame','same_campaign'}


class Queries:
    def __init__(self, data):
        self.data=data
        self.by={r['key']:r for r in data['records']}
        self.out=defaultdict(list);self.reverse=defaultdict(list)
        for e in data['edges']:
            self.out[e['subject']].append(e)
            self.reverse[e['object']].append(e)

    def records(self,kind):
        return [r for r in self.data['records'] if r['kind']==kind]

    def impact(self,changed):
        """Q1/Q6: transitive dependency closure with a shortest causal path per record."""
        seeds=[changed] if isinstance(changed,str) else list(changed)
        if any(s not in self.by for s in seeds):raise ValueError('Unknown record ID')
        paths={s:[] for s in seeds};queue=deque(seeds)
        while queue:
            current=queue.popleft()
            for edge in self.reverse[current]:
                if edge['relation'] not in DEPENDENCIES:continue
                subject=edge['subject']
                # Shared predicate templates list branch applicability; changing
                # one branch does not rewrite the predicate in every other branch.
                if edge['relation']=='under_branch' and self.by[subject]['kind']=='requirement' and 'required_for' in self.by[subject]['payload']:
                    continue
                if subject not in paths:
                    paths[subject]=paths[current]+[edge]
                    queue.append(subject)
        affected=[{'record':self.by[k],'dependency_path':paths[k]} for k in sorted(paths) if k not in seeds]
        return {'changed':seeds,'status':'reassessment_required','affected':affected,
                'candidate_conclusions':[a for a in affected if a['record']['kind']=='evaluation'],
                'unknowns':['A dependency change requires review; it does not itself reverse the historical outcome.']}

    def evidence_chain(self,address):
        """Claim inspector: directed evidence closure, assumptions and competing branches."""
        if address not in self.by:raise ValueError('Unknown record ID: '+address)
        seen=set();queue=deque([address]);edges=[]
        while queue:
            current=queue.popleft()
            if current in seen:continue
            seen.add(current)
            for e in self.out[current]:
                edges.append(e)
                if e['object'] not in seen:queue.append(e['object'])
        return {'selected':address,'records':[self.by[k] for k in sorted(seen)],
                'edges':edges,'dependents':self.reverse[address],
                'assumptions':[self.by[k] for k in sorted(seen) if self.by[k]['kind'] in {
                    'branch','hypothesis','gap','interpretation','requirement','frame'}]}

    def same_observation(self):
        """Q2: actual reuse edges only. Shared campaigns stay a separate, weaker join."""
        groups=[]
        for o in self.records('observation'):
            reporters=[self.by[e['subject']] for e in self.reverse[o['key']] if e['relation']=='reports']
            if len(reporters)>1:
                groups.append({'observation':o,'reporting_records':reporters,
                               'independent_observations':1,
                               'limit':'Original drawing and its reproductions/derivations; individual derived measurements remain separate records.'})
        return {'shared_original_observations':groups,
                'campaign_lineages':[r for r in self.records('lineage') if r['payload'].get('granularity')!='original_observation'],
                'unknowns':['A shared campaign alone does not establish that two publications report the same observation. No citation-count confidence is computed.']}

    def candidate(self,identity):
        """Q3: retain each test, branch, assignment, check and source witness."""
        address=identity if identity.startswith('hypothesis/') else 'hypothesis/'+identity
        if address not in self.by:raise ValueError('Unknown hypothesis')
        evaluations=[r for r in self.records('evaluation') if r['payload']['hypothesis_key']==address]
        return {'hypothesis':self.by[address], 'evaluations':[
            {'evaluation':r,'branch':self.by[r['payload']['branch_key']],
             'evidence_keys':sorted({e['object'] for e in self.out[r['key']]}),
             'source_locators':[self.by[e['object']] for e in self.out[r['key']] if e['relation']=='cites']}
            for r in evaluations],
            'unknowns':['Different registered specifications remain separate. A reported-form match does not supply ancient phase, uniqueness or identification support.']}

    def coexistence(self):
        """Q4: construction/use diagnostics and explicit joint-accessibility evaluations."""
        return {'hypotheses':[{'record':h,'status':h['payload']['coexistence_status']} for h in self.records('hypothesis')],
                'joint_accessibility_claims':[self.evidence_chain(r['key']) for r in self.records('claim')
                    if r['payload'].get('relationship')=='coexisted_with'],
                'historical_state_tests':[r for r in self.records('test') if r['id'].startswith('states-')
                                          or r['id']=='relationships-quarry-phase-order'],
                'transitions':self.records('event'),
                'unknowns':['No imported candidate arrangement has demonstrated instruction-period coexistence.',
                            'Kenyon’s grave-before-quarry sequence contradicts same-phase construction; later joint accessibility remains unresolved.']}

    def no_external_match(self):
        """Q5: bounded search result; missing adequate negative coverage stays explicit."""
        return {'searches':[self.evidence_chain(r['key']) for r in self.records('search')
                            if r['payload']['result']=='no_external_match'],
                'unknowns':['Search coverage is incomplete. No archaeological absence or universal non-attestation follows.']}

    def acquisition(self):
        """Q7: conditional possibilities are never observations or updated results."""
        return {'targets':[self.evidence_chain(r['key']) for r in self.records('acquisition')],
                'saved_separating_observation_analysis':self.by.get('test/separation-planning-snapshot'),
                'unknowns':['These possible outcomes distinguish named branch/model classes, subject to the acquisition and exposure gates.',
                            'They neither certify an unused observation nor reopen a closed test.']}

    def uninspected(self):
        """Q8: inspection is its own state, including partially inspected works."""
        unread=[r for r in self.records('source') if r['payload'].get('inspection')=='not_inspected']
        partial=[r for r in self.records('source') if r['payload'].get('inspection')!='not_inspected'
                 and (r['payload'].get('uninspected_parts') or
                      any(s in r['payload'].get('citation','').lower() for s in ['not inspected','uninspected','partial']))]
        return {'uninspected_sources':unread,'partially_inspected_sources':partial,
                'source_dependent_conclusions':{r['key']:[a['record']['key'] for a in self.impact(r['key'])['candidate_conclusions']] for r in unread+partial},
                'gaps':self.records('gap'),
                'unknowns':['Inspected report pages do not supply a missing field observation. PDF/printed-page offsets are never inferred.']}

    def chronology(self):
        """Name chronology sorts composition ranges, showing object/story dates separately."""
        def sort(r):
            date=r['payload'].get('composition_date') or {}
            return (date.get('range_ce',[10**9])[0],r['key'])
        return {'occurrences':sorted(self.records('occurrence'),key=sort),
                'identity_proposals':[r for r in self.records('identity') if r['payload'].get('relation')=='proposed_same_referent'],
                'searches':self.records('search'),
                'unknowns':['Undated physical witnesses stay undated. Composition is not the date of the object or the period described.']}

    def entry(self,identity):
        address='entry/'+identity
        if address not in self.by:raise ValueError('Unknown canonical entry')
        keys={address}
        for e in self.data['edges']:
            if e['object']==address and e['relation']=='in_entry':keys.add(e['subject'])
        candidate_keys={h['key'] for h in self.records('hypothesis') if identity in h['payload'].get('entry_ids',[])}
        keys|=candidate_keys
        for r in self.records('evaluation'):
            if r['payload']['hypothesis_key'] in candidate_keys:keys.add(r['key'])
        for branch in list(keys):
            for e in self.out[branch]:
                if e['relation']=='requires':keys.add(e['object'])
        return {'entry':self.by[address],'records':[self.by[k] for k in sorted(keys)],
                'acquisition_targets':self.records('acquisition'),
                'spatial_view':{'url':'https://quadrin.github.io/CopperScroll/#workbench/states',
                    'mode':'Existing atlas historical states; source-plan frames and uncertainty retained. No new world overlay.'}}

    def demonstrate(self):
        return {'1_reading_dependencies':self.impact('reading/e60-janoah:4'),
                '2_same_original_observation':self.same_observation(),
                '3_candidate_requirements':self.candidate('iv17'),
                '4_coexistence':self.coexistence(),
                '5_no_external_match':self.no_external_match(),
                '6_change_impact':self.impact('claim/relationships-quarries-later-phase'),
                '7_distinguishing_observations':self.acquisition(),
                '8_uninspected_sources':self.uninspected()}
