#!/usr/bin/env python3
"""Recompute the cave-form intersection and Koḥlit bottlenecks from repo inputs.

Read-only against canonical inputs. Writes only adjacent derived audit outputs.
"""
from pathlib import Path
import collections
import csv
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

def load(path):
    return json.loads((REPO / path).read_text())

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, REPO / path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj

def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

cave = module('available_evidence_caves', 'research/regional/caves_entry25/scripts/score.py')
paths = ['research/regional/caves_entry25/caves.csv', 'research/regional/caves_entry25/phase4_units.csv']
rows = []
for path in paths:
    with (REPO / path).open(newline='') as f:
        rows.extend(csv.DictReader(f))
plans = load('research/regional/caves_entry25/coded/plan_measurements.json')['rows']
scored = []
for row in rows:
    if row['row_kind'] != 'cave':
        continue
    aspect = cave.aspect(row, plans)
    outcomes = []
    for reading in cave.BRANCHES:
        for orientation in cave.ORIENTATIONS:
            for ruleset in cave.RULESETS:
                value = cave.score_row(row, aspect, reading, orientation, ruleset)
                outcomes.append({'model': '|'.join((reading, orientation, ruleset)),
                                 'result': value['result'], 'failing_clauses': value['failing']})
    scored.append({'id': row['cave_id'], 'source': row['source_records'], 'models': outcomes})
failed = [r for r in scored if all(v['result'] == 'fail' for v in r['models'])]
failed_ids = {r['id'] for r in failed}
groups = cave.components([r for r in rows if r['row_kind'] == 'cave'])
whole = [g for g in groups if all(i in failed_ids for i in g)]
mixed = [g for g in groups if any(i in failed_ids for i in g) and not all(i in failed_ids for i in g)]
matches = collections.defaultdict(list)
for row in scored:
    for m in row['models']:
        if m['result'] == 'all-match':
            matches[m['model']].append(row['id'])
assert len(scored) == len({r['id'] for r in scored})
assert (len(scored), len(failed), len(whole), len(mixed)) == (643, 102, 97, 3)
save('cave_form_intersection.json', {
    'claim': 'Reported-form contradictions across the 16 separately scored models',
    'input_scope': 'Current exposed catalogue; 643 records, not a verified physical-cave census',
    'excluded_scope': ['B-GATE', 'combined coding sensitivities', 'unscored geometry/phase models',
                       'whole physical caves', 'regional uniqueness', 'deposit existence or absence'],
    'record_count': len(scored), 'failed_every_scored_model': len(failed),
    'eligible_at_least_one_unknown_or_match': len(scored) - len(failed),
    'ids': sorted(failed_ids), 'contradiction_witnesses': sorted(failed, key=lambda r: r['id']),
    'all_match_by_model': dict(matches), 'possible_duplicate_groups': len(groups),
    'wholly_failed_groups': whole, 'mixed_groups': mixed,
    'identity_limit': 'Possible-duplicate grouping remains provisional; mixed groups retain best permitted members',
})

model_path = 'research/feature_workbench/relationships/model.json'
evaluator_path = 'research/feature_workbench/relationships/evaluate.py'
model = load(model_path)
ev = module('available_evidence_relationships', evaluator_path)
readings = {r['id']: r for r in model['readings']}
branches = [ev.evaluate_branch(readings[rid], a, w, model)
            for a in model['assignments'] for rid in a['reading_ids'] for w in model['windows']]
survivors = [b for b in branches if b['status'] == 'unknown']
unknowns = sorted(set.intersection(*[{c['value']['predicate_id'] for c in b['checks']
                                    if c['status'] == 'unknown'} for b in survivors]))
window_pairs = []
for assignment in model['assignments']:
    for rid in assignment['reading_ids']:
        pair = [ev.evaluate_branch(readings[rid], assignment, w, model) for w in model['windows']]
        sigs = [tuple((c['value']['predicate_id'], c['status']) for c in b['checks']) for b in pair]
        window_pairs.append({'assignment': assignment['id'], 'reading': rid,
                             'identical_predicate_states': sigs[0] == sigs[1]})
counts = dict(collections.Counter(b['status'] for b in branches))
assert counts == {'unknown': 28, 'contradicted': 12}
assert unknowns == ['pit-period', 'pool-north-corner', 'pool-period']
assert len(window_pairs) == 20 and all(p['identical_predicate_states'] for p in window_pairs)
save('kohlit_bottlenecks.json', {
    'claim': 'Existing exposed observations distinguish retained entry-11/60 assignments',
    'result': 'not identifiable from available evidence', 'scope': 'Selected exploratory roster',
    'historical_branch_outcomes_reproduced': counts,
    'common_missing_predicates': unknowns, 'date_window_pairs': window_pairs,
    'branches': [{'id': b['id'], 'status': b['status'],
                  'checks': {c['value']['predicate_id']: c['status'] for c in b['checks']}}
                 for b in branches],
    'interpretation': 'Date-window variation supplies no discrimination for these exposed assignments',
})
inputs = paths + ['research/regional/caves_entry25/scripts/score.py',
    'research/regional/caves_entry25/coded/plan_measurements.json',
    'research/preregistration/entry25_iv17_rules/check_rules.py',
    'research/preregistration/entry25_iv17_rules/rules.json', model_path, evaluator_path]
save('reproduction_inputs.json', {p: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for p in inputs})
print('Verified cave-form intersection and Koḥlit bottlenecks from canonical inputs.')
