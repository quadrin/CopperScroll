"""Typed records, explicit dependency edges and evidence-layer validation."""
from __future__ import annotations
import hashlib
import json
from copy import deepcopy
from pathlib import Path

KINDS = {'entry', 'witness', 'locus', 'segment', 'image', 'reading_set', 'reading',
         'restoration', 'interpretation', 'translation', 'branch', 'requirement',
         'feature', 'state', 'event', 'frame', 'work', 'edition', 'copy', 'source',
         'observation', 'lineage', 'claim', 'hypothesis', 'test', 'evaluation',
         'coverage', 'gap', 'acquisition', 'name', 'occurrence', 'entity', 'identity', 'search'}
RELATIONS = {'depends_on', 'cites', 'reports', 'derived_from', 'about', 'in_entry',
             'at_locus', 'on_segment', 'catalogue_association', 'interprets',
             'requires', 'assigns', 'evaluates', 'under_branch', 'in_test',
             'supports', 'conflicts', 'prerequisite', 'state_of', 'transitions_from',
             'transitions_to', 'uses_frame', 'occurrence_of', 'mentions', 'found_at',
             'proposed_same_referent', 'proposed_spelling_variant', 'same_spelling',
             'searched_for', 'would_resolve', 'supersedes', 'same_campaign'}
STATUSES = {'compatible', 'contradicted', 'unknown', 'mixed', 'info'}
GAP_REASONS = {'uninspected_source', 'insufficient_resolution', 'uncertain_phase',
               'missing_reference_point', 'incomplete_coverage', 'unverified_identity',
               'unregistered_image', 'unsegmented_editorial_layer', 'not_recorded',
               'unestablished_geometry', 'unverified_independence'}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def sha(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def key(kind, identity):
    return kind + '/' + str(identity)


class Graph:
    def __init__(self):
        self.records = {}
        self.edges = set()
        self.inputs = {}

    def add(self, kind, identity, label, payload, path, pointer='', *, exposure='derived',
            visibility='public_metadata', review='accepted', sources=()):
        address = key(kind, identity)
        if address in self.records:
            raise ValueError('Duplicate ID: ' + address)
        self.records[address] = {
            'key': address, 'kind': kind, 'id': str(identity), 'label': label,
            'review_status': review, 'exposure': exposure, 'visibility': visibility,
            'locators': [{'repo_path': path, 'pointer': pointer or '/',
                          'printed_page': None, 'pdf_page': None, 'figure': None,
                          'image_region': None, 'archival_identifier': None}],
            'payload': deepcopy(payload)}
        for source in sources:
            self.link(address, 'cites', key('source', source))
        return address

    def link(self, subject, relation, obj):
        if obj is not None:
            self.edges.add((subject, relation, obj))

    def file(self, root, path):
        """Only adapter-declared files are read. Never crawl research or source assets."""
        raw = (root / path).read_bytes()
        self.inputs[path] = hashlib.sha256(raw).hexdigest()
        return raw.decode('utf-8-sig')

    def json(self, root, path):
        return json.loads(self.file(root, path))

    def export(self):
        return {'schema_version': 1, 'records': [self.records[k] for k in sorted(self.records)],
                'edges': [dict(subject=s, relation=r, object=o) for s, r, o in sorted(self.edges)],
                'inputs': dict(sorted(self.inputs.items()))}


def validate(data):
    records = data['records']
    by = {r['key']: r for r in records}
    if len(records) != len(by):
        raise ValueError('Duplicate ID')
    edges = data['edges']
    outgoing = {}
    for e in edges:
        if e['subject'] not in by or e['object'] not in by:
            raise ValueError('Broken reference: ' + canonical(e))
        if e['relation'] not in RELATIONS:
            raise ValueError('Unknown relationship')
        outgoing.setdefault(e['subject'], []).append(e)
    for r in records:
        for field,value in r['payload'].items():
            refs=[value] if field.endswith('_key') else value if field.endswith('_keys') and isinstance(value,list) else []
            for ref in refs:
                if ref is not None and ref not in by:raise ValueError('Broken typed reference: '+r['key']+' '+str(ref))
        for field,kind in [('source_ids','source'),('feature_ids','feature'),('state_ids','state')]:
            for identity in r['payload'].get(field,[]):
                if key(kind,identity) not in by:
                    raise ValueError('Broken payload reference: '+r['key']+' '+str(identity))
    for r in records:
        p = r['payload']; k = r['key']; kind = r['kind']
        if kind not in KINDS or k != key(kind, r['id']):
            raise ValueError('Invalid typed ID: ' + k)
        if r['review_status'] != 'accepted':
            raise ValueError('Unreviewed proposal in accepted layer: ' + k)
        if not r['locators'] or any(not x.get('repo_path') or not x.get('pointer') for x in r['locators']):
            raise ValueError('Lost source locator: ' + k)
        if r['visibility'] not in {'public_metadata', 'local_only', 'restricted', 'reserved'}:
            raise ValueError('Unknown visibility')
        if kind == 'gap' and p.get('reason') not in GAP_REASONS:
            raise ValueError('Undocumented gap reason: ' + k)
        if kind == 'evaluation':
            if p.get('status') not in STATUSES or not p.get('branch_key') or not p.get('hypothesis_key'):
                raise ValueError('Flattened branch or invalid outcome: ' + k)
            h = by[p['hypothesis_key']]['payload']
            if p.get('identification_support') is not False:
                raise ValueError('Exploratory migration strengthened to identification support: '+k)
            if p.get('assignment') != h['assignment']:
                raise ValueError('Feature assignment changed inside hypothesis: ' + k)
            permitted = {v for v in h['assignment'].values() if v is not None}
            for check in p['checks']:
                if check['status'] not in STATUSES:
                    raise ValueError('Unknown check status')
                if not set(check.get('feature_ids', [])) <= permitted:
                    raise ValueError('Check silently switches features: ' + k)
                if check.get('value', 'not_supplied') is None and check['status'] == 'contradicted':
                    raise ValueError('Unknown observation treated as absent: ' + k)
        if kind == 'identity':
            if p.get('merged') is not False or not p.get('proposer') or not p.get('evidence'):
                raise ValueError('Undocumented alias/name merge: ' + k)
        if kind == 'occurrence':
            if not p.get('original_spelling') or not p.get('source_location'):
                raise ValueError('Lost occurrence spelling/location: ' + k)
            for field in ('composition_date', 'object_date', 'period_described', 'findspot', 'place_mentioned'):
                if field not in p:
                    raise ValueError('Conflated occurrence context: ' + k)
        if kind in {'feature', 'state'}:
            geo = p.get('world_geometry') or (p.get('geometry') if p.get('crs') else None)
            if geo and (not p.get('registration') or not p.get('uncertainty') or not p.get('crs')):
                raise ValueError('Undocumented geographic precision: ' + k)
        if kind == 'hypothesis':
            # Overlap cannot establish coexistence; explicit incompatible states prohibit it.
            if p.get('coexistence_status') == 'compatible' and not p.get('coexistence_observation_keys'):
                raise ValueError('Coexistence inferred without observation: ' + k)
            states = [by[x]['payload'] for x in p.get('state_keys', [])]
            intervals=[s.get('accessible_interval_ce') for s in states if s.get('accessible_interval_ce')]
            if intervals and max(x[0] for x in intervals)>min(x[1] for x in intervals):
                raise ValueError('Incompatible historical states: '+k)
            for i, a in enumerate(states):
                for b in states[i+1:]:
                    if a.get('exclusive_with') and b.get('id') in a['exclusive_with']:
                        raise ValueError('Incompatible historical states: ' + k)
        if kind == 'claim':
            if not all(x in p for x in ('subject', 'relationship', 'value', 'analyst', 'evidence_kind',
                                        'reading_confidence', 'site_association', 'feature_identity',
                                        'positional_uncertainty', 'supersedes')):
                raise ValueError('Incomplete claim: ' + k)
            if not any(e['relation'] in {'derived_from', 'cites'} for e in outgoing.get(k, [])):
                raise ValueError('Claim lost provenance: ' + k)
        if kind == 'observation':
            if not p.get('lineage_key') or p['lineage_key'] not in by:
                raise ValueError('Observation lost lineage: ' + k)
        if kind=='image' and p.get('association_status')=='authenticated' and (not p.get('original_roi') or p.get('substrate')!='original'):
            raise ValueError('Catalogue association promoted to authenticated original reading: '+k)
        if p.get('independent_observations') is not None:
            raise ValueError('Citation-derived independence counts are prohibited in accepted records: '+k)
        if kind=='search' and p.get('result')=='no_external_match':
            if not all(p.get(x) for x in ('corpora','queries','inspection_scope','limitations')):
                raise ValueError('Unbounded negative search: '+k)
    schema=json.loads(Path(__file__).with_name('schema.json').read_text())
    validate_structure(data,schema,schema)
    return {'status': 'valid', 'records': len(records), 'edges': len(edges)}


def validate_structure(value,spec,document,path='$'):
    """Small stdlib validator for the explicit JSON Schema subset used here.

    Graph/evidence invariants above remain the authoritative cross-record check.
    No remote schema resolution or automatic acceptance of extraction proposals.
    """
    if '$ref' in spec:
        target=document
        for token in spec['$ref'].removeprefix('#/').split('/'):target=target[token]
        return validate_structure(value,target,document,path)
    types={'object':lambda x:isinstance(x,dict),'array':lambda x:isinstance(x,list),
           'string':lambda x:isinstance(x,str),'null':lambda x:x is None,
           'number':lambda x:isinstance(x,(float,int)) and not isinstance(x,bool),
           'boolean':lambda x:isinstance(x,bool)}
    expected=spec.get('type')
    if expected:
        expected=expected if isinstance(expected,list) else [expected]
        if not any(types[t](value) for t in expected):raise ValueError('Schema type at '+path)
    if 'const' in spec and (type(value)!=type(spec['const']) or value!=spec['const']):raise ValueError('Schema constant at '+path)
    if 'enum' in spec and value not in spec['enum']:raise ValueError('Schema vocabulary at '+path)
    if isinstance(value,dict):
        for field in spec.get('required',[]):
            if field not in value:raise ValueError('Schema required field '+path+'/'+field)
        props=spec.get('properties',{})
        for field,item in value.items():
            if field in props:validate_structure(item,props[field],document,path+'/'+field)
            elif spec.get('additionalProperties') is False:raise ValueError('Schema unexpected field '+path+'/'+field)
            elif isinstance(spec.get('additionalProperties'),dict):validate_structure(item,spec['additionalProperties'],document,path+'/'+field)
    if isinstance(value,list):
        if len(value)<spec.get('minItems',0) or len(value)>spec.get('maxItems',float('inf')):raise ValueError('Schema array length at '+path)
        for i,item in enumerate(value):validate_structure(item,spec.get('items',{}),document,path+'/'+str(i))
    if isinstance(value,str) and len(value)<spec.get('minLength',0):raise ValueError('Schema empty string at '+path)
    for rule in spec.get('allOf',[]):validate_structure(value,rule,document,path)
    if 'if' in spec:
        try:validate_structure(value,spec['if'],document,path)
        except ValueError:pass
        else:validate_structure(value,spec.get('then',{}),document,path)


def public_view(data):
    """Fail closed over evidence dependencies; hidden content never becomes a dangling hint."""
    hidden = {r['key'] for r in data['records'] if r['visibility'] != 'public_metadata'
              or r['exposure'] == 'reserved' or r['review_status'] != 'accepted'}
    while True:
        more = {e['subject'] for e in data['edges'] if e['object'] in hidden}
        if more <= hidden:
            break
        hidden |= more
    return {**data, 'records': [r for r in data['records'] if r['key'] not in hidden],
            'edges': [e for e in data['edges'] if e['subject'] not in hidden and e['object'] not in hidden]}
