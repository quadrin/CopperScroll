#!/usr/bin/env python3
"""Apply exposed book facts to named physical witnesses; never write lane inputs."""
import csv
import hashlib
import io
import json
import re
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
AUDIT = 'research/sources/full_reads_2026-10-12/feature_phase_audit/audit.json'
CAVES = 'research/regional/caves_entry25/caves.csv'
TOMBS = 'research/regional/tombs/tombs.csv'
WATER = 'research/regional/water_systems/water.csv'
CAVE_SCORES = 'research/regional/caves_entry25/scores.csv'
TOMB_SCORES = 'research/regional/tombs/scores.csv'
WATER_SCORES = 'research/regional/water_systems/scores.csv'
TOMB_PLAN = 'research/regional/tombs/PLAN.md'
CORRECTIONS = 'research/regional/water_systems/manual_review_2026-10-12/merged_match_changes.csv'
M, F, U, NS = 'MATCH', 'FAIL', 'UNKNOWN', 'not_scored'


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(value).hexdigest()


def read_csv(path):
    with (REPO / path).open(encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def read_json(path):
    return json.loads((REPO / path).read_text(encoding='utf-8'))


def normalize(value):
    return {'yes': M, 'match': M, 'all-match': M, 'no': F,
            'fail': F, 'unknown': U, 'UNKNOWN': U}.get(value, value)


def overall(values):
    vals = [normalize(x) for x in values if x != NS]
    if F in vals:
        return F
    return M if vals and all(v == M for v in vals) else U


def audit_refs(audits):
    return [{'audit_id': a['audit_id'], 'source': r['source'],
             'observation_id': r['observation_id'], 'observation_file': r['observation_file'],
             'observation_row_sha256': r['observation_row_sha256'],
             'printed_pages': r['printed_locator'], 'viewer_pages': r['viewer_pages'],
             'figure_ids': r['figure_ids'], 'source_url': r['source_url']}
            for a in audits for r in a['refs']]


def build():
    cfg = json.loads((HERE / 'applications.json').read_text(encoding='utf-8'))
    audit = {r['audit_id']: r for r in read_json(AUDIT)['rows']}
    assert set(audit) == set(cfg['audit_dispositions']), 'Every book audit needs a disposition'
    inventories = {
        'cave': {r['cave_id']: r for r in read_csv(CAVES)},
        'tomb': {r['unit_id']: r for r in read_csv(TOMBS)},
        'water': {r['id']: r for r in read_csv(WATER)},
    }
    lane_scores = {'cave': read_csv(CAVE_SCORES), 'tomb': read_csv(TOMB_SCORES),
                   'water': read_csv(WATER_SCORES)}
    plan = json.loads(re.search(r'```json\n(.*?)\n```',
                               (REPO / TOMB_PLAN).read_text(encoding='utf-8'), re.S)[1])
    corrections = {(r['unit_id'], r['entry'], r['branch']): r
                   for r in read_csv(CORRECTIONS) if r['view'] == 'verified'}
    inputs = {AUDIT, CAVES, TOMBS, WATER, CAVE_SCORES, TOMB_SCORES,
              WATER_SCORES, TOMB_PLAN, CORRECTIONS,
              str((HERE / 'applications.json').relative_to(REPO)),
              str((HERE / 'evaluate.py').relative_to(REPO))}
    output, scores = [], []
    seen = set()
    for b in cfg['bindings']:
        assert b['witness_id'] not in seen
        seen.add(b['witness_id'])
        lane, parent = b['lane'], b['parent_id']
        source_row = inventories[lane][parent]  # exact-ID match; no name fallback
        audits = [audit[i] for i in b['audit_ids']]
        for path in b['context_refs']:
            inputs.add(path)
            assert (REPO / path).is_file()
        refs = audit_refs(audits)
        phases = [{k: a[k] for k in ('audit_id', 'construction', 'use', 'fill',
                                    'alteration', 'function_status', 'relationship')}
                  for a in audits]
        if not phases:
            # We have existing candidate records, not new book evidence at these features.
            phases = [{'construction': 'UNKNOWN; no exact new book observation',
                       'use': source_row.get('period_stated', source_row.get('period_as_given', '')),
                       'fill': 'UNKNOWN unless separately described in the existing record',
                       'alteration': b['phase'], 'relationship': b['reason']}]
        witness = dict(b, parent_record=source_row,
                       parent_row_sha256=digest(canon(source_row).encode()),
                       source_refs=refs, phase_evidence=phases,
                       same_feature_observation=bool(audits), independent_confirmation=False,
                       inherited_codes_note='Parent codes retained only for the existing reported-subset comparison; this is not proof that every clause coexists in one phase.')
        output.append(witness)
        keyfield = {'cave': 'cave_id', 'tomb': 'unit_id', 'water': 'id'}[lane]
        selected = [s for s in lane_scores[lane] if s[keyfield] == parent]
        assert selected, f'No baseline scores for {parent}'
        for s in selected:
            entry = 25 if lane == 'cave' else int(s['branch'].split('-')[0]) if lane == 'tomb' else int(s['entry'])
            if entry not in b['entries']:
                continue
            branch = s['branch']
            if lane == 'cave':
                branch += '|' + s['orientation'] + '|' + s['ruleset']
                codes = {k: normalize(s[k]) for k in ('c1', 'c2', 'c3', 'c4', 'c5')}
                before_raw = normalize(s['result'])
                date_raw = source_row['period_in_window']
            elif lane == 'tomb':
                clauses = plan['branches'][s['branch']]['clauses']
                if not clauses:
                    codes = {}
                else:
                    codes = dict(zip(clauses, map(normalize, s['values'].split(';'))))
                    assert len(codes) == len(clauses)
                before_raw = normalize(s['result'])
                date_raw = source_row['dated_in_window']
            else:
                codes = {k: normalize(v) for k, v in
                         (p.split('=', 1) for p in s['clauses'].split(';'))}
                before_raw = normalize(s['overall'])
                date_raw = s['date_code']
            # Existing manual corrections are the immediate baseline, not new changes.
            correction = corrections.get((parent, str(entry), s['branch'])) if lane == 'water' else None
            date_before = correction['corrected_date'] if correction else date_raw
            if correction and entry == 32 and s['branch'].endswith('T-wall'):
                # Only the existing explicit modern wall downgrade. Never guess which
                # clause changed for a different correction.
                if parent == 'ASI-109/5/6-aqueduct':
                    codes['tur'] = U
            before = overall(codes.values())
            if correction:
                assert before == correction['corrected_overall'], (parent, branch)
            after = dict(codes)
            for k, v in b['overrides'].items():
                assert v in (M, F, U)
                if k in after:
                    after[k] = v
            subset = overall(after.values()) if after else NS
            configuration = overall([subset, b['configuration_in_window']]) if after else NS
            phase_relation = overall([configuration, b['datum']]) if entry in (25, 29, 51, 56) else configuration
            changed = {k: {'before': codes[k], 'after': after[k]} for k in codes if codes[k] != after[k]}
            scores.append({'witness_id': b['witness_id'], 'parent_id': parent,
                           'lane': lane, 'entry': entry, 'branch': branch,
                           'raw_frozen_result': before_raw, 'prior_manual_result': before,
                           'raw_period_code': date_raw, 'prior_manual_period_code': date_before,
                           'clauses_before': codes, 'clauses_after': after,
                           'changed_clauses': changed, 'reported_subset_after': subset,
                           'configuration_in_window': b['configuration_in_window'],
                           'phase_required_subset': configuration, 'original_datum': b['datum'],
                           'phase_and_datum_subset': phase_relation,
                           'identification': U, 'closed_assessment_reopened': False})

    bath = cfg['bath_import']
    phase_rows = read_json(bath['phase_file'])
    phases_by_id = {p['phase_id']: p for p in phase_rows}
    inputs.update([bath['phase_file'], bath['score_file']])
    for row in read_csv(bath['score_file']):
        p = phases_by_id[row['phase_id']]
        assert row['configuration_in_window'] == p['configuration_in_window']
        scores.append({'witness_id': row['phase_id'], 'parent_id': row['origin_row'],
                       'lane': 'bath-existing-phase-review', 'entry': 46,
                       'branch': '|'.join(row[k] for k in ('function_model', 'anchor', 'radius_km')),
                       'raw_frozen_result': 'not_comparable_different_type_gate',
                       'prior_manual_result': row['reported_window_screen'],
                       'raw_period_code': row['reported_period'], 'prior_manual_period_code': row['reported_period'],
                       'clauses_before': {k: row[k] for k in ('place', 'entrance', 'function')},
                       'clauses_after': {k: row[k] for k in ('place', 'entrance', 'function')},
                       'changed_clauses': {}, 'reported_subset_after': row['reported_window_screen'],
                       'configuration_in_window': row['configuration_in_window'],
                       'phase_required_subset': overall([row['phase_join_screen'], row['configuration_in_window']]),
                       'original_datum': row['original_stair_origin'],
                       'phase_and_datum_subset': overall([row['phase_join_screen'], row['configuration_in_window'], row['original_stair_origin']]),
                       'imported_phase_join_screen': row['phase_join_screen'],
                       'imported_stair_origin_screen': row['stair_origin_screen'],
                       'full_pool_branch': row['full_pool_branch'],
                       'identification': U, 'closed_assessment_reopened': False})

    # Bind to exact parent/source records and archived source scans; the prior audit's
    # source row hashes/figure IDs are reproduced, not claimed independently inspected.
    manifest = {'baseline_commit': cfg['baseline_commit'], 'inputs': [
        {'path': p, 'bytes': (REPO / p).stat().st_size,
         'sha256': digest((REPO / p).read_bytes())} for p in sorted(inputs)]}
    dispositions = [{'audit_id': aid, 'disposition': text,
                     'source_refs': audit_refs([audit[aid]]),
                     'next_source': audit[aid]['next_observation'],
                     'invented_score': False} for aid, text in cfg['audit_dispositions'].items()]
    result = {'schema_version': 1, 'baseline_commit': cfg['baseline_commit'],
              'analysis_kind': cfg['analysis_kind'], 'rules': cfg['rules'],
              'witnesses': output, 'existing_bath_phases': phase_rows,
              'audit_dispositions': dispositions, 'scores': scores,
              'limitation': 'Selected source/physical-witness applications; no regional count, rank, rarity or confirmatory identification. Historical lane outputs untouched.'}
    native_spec = importlib.util.spec_from_file_location('native_application', HERE / 'evaluate_native.py')
    native = importlib.util.module_from_spec(native_spec)
    native_spec.loader.exec_module(native)
    native_result, native_inputs = native.build()
    result['native_application'] = native_result
    manifest['inputs'] = sorted({row['path']: row for row in manifest['inputs'] + native_inputs}.values(),
                                key=lambda row: row['path'])
    return result, manifest


def artifacts(result, manifest):
    artifacts = {'results.json': json.dumps(result, indent=2, ensure_ascii=False) + '\n',
                 'input_manifest.json': json.dumps(manifest, indent=2) + '\n'}
    buf = io.StringIO(newline='')
    cols = ['witness_id', 'parent_id', 'lane', 'entry', 'branch', 'raw_frozen_result',
            'prior_manual_result', 'raw_period_code', 'prior_manual_period_code',
            'clauses_before', 'clauses_after', 'changed_clauses', 'reported_subset_after',
            'configuration_in_window', 'phase_required_subset', 'original_datum',
            'phase_and_datum_subset', 'identification']
    writer = csv.DictWriter(buf, cols, lineterminator='\n', extrasaction='ignore')
    writer.writeheader()
    for s in result['scores']:
        writer.writerow({k: canon(v) if isinstance(v, (dict, list)) else v for k, v in s.items()})
    artifacts['applied_scores.csv'] = buf.getvalue()
    native_spec = importlib.util.spec_from_file_location('native_application_csv', HERE / 'evaluate_native.py')
    native = importlib.util.module_from_spec(native_spec)
    native_spec.loader.exec_module(native)
    artifacts['native_scores.csv'] = native.score_csv(result['native_application'])
    return artifacts


def main():
    result, manifest = build()
    for name, data in artifacts(result, manifest).items():
        (HERE / name).write_text(data, encoding='utf-8')
    changed = [r for r in result['scores'] if r['changed_clauses']]
    print(f'Applied witness comparisons written; {len(changed)} branch rows have explicit clause changes. Historical inputs untouched.')


if __name__ == '__main__':
    main()
