"""Deterministic, metadata-only atlas snapshot from reviewed canonical inputs."""
from pathlib import Path
import json
from copy import deepcopy
from .adapters import build_graph
from .model import canonical, public_view, sha, validate
from .queries import Queries, DEPENDENCIES


def project(data):
    validate(data)
    safe = deepcopy(public_view(data))
    q = Queries(safe)
    # Explicit reviewed notices travel to the public view without importing a
    # machine's SQLite history or silently replacing a historical test score.
    notices = [r for r in safe['records'] if r['kind'] == 'claim'
               and r['payload'].get('reassessment_required') is True]
    triggers = {}
    for notice in notices:
        for item in q.impact(notice['key'])['candidate_conclusions']:
            triggers.setdefault(item['record']['key'], []).append(notice['key'])
    for r in safe['records']:
        if r['key'] in triggers:
            r['payload']['reassessment'] = {
                'required': True, 'trigger_keys': sorted(triggers[r['key']]),
                'reason': 'Explicit reviewed source dependency requires reassessment; historical scores are preserved.'}
    entries = {r['id']: [x['key'] for x in q.entry(r['id'])['records']]
               for r in q.records('entry')}
    return {'schema_version': 1, 'version': sha(safe),
            'scope': 'Reviewed evidence metadata. Compatibility remains exploratory.',
            'records': safe['records'], 'edges': safe['edges'], 'entries': entries,
            'dependency_relations': sorted(DEPENDENCIES),
            'inputs': safe['inputs']}


def build(root):
    return project(build_graph(root))


def write(root, destination):
    data = build(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(canonical(data)+'\n',encoding='utf-8')
    return data['version']


if __name__ == '__main__':
    from core import ROOT
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    destination = ROOT/'atlas/app/atlas-kb.json'
    if args.check:
        expected = canonical(build(ROOT))+'\n'
        if not destination.exists() or destination.read_text(encoding='utf-8') != expected:
            raise SystemExit('Atlas KB snapshot is stale; run python -m claim_kb.web_export')
        print('Atlas KB snapshot: current')
    else:
        print(write(ROOT,destination))
