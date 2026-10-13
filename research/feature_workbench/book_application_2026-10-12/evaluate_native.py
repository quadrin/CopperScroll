#!/usr/bin/env python3
"""Apply the five exposed original reports to exact witnesses and lane rows.

This companion preserves the historical regional inputs and every retained
reading. It evaluates source-specific relations, never a regional identification.
"""
import csv
import hashlib
import io
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CFG = HERE / 'native_application.json'
SOURCES = REPO / 'research/sources/full_reads_2026-10-12/five_remaining_2026-10-13/source_manifest.json'
TOMBS = REPO / 'research/regional/tombs/tombs.csv'
TOMB_SCORES = REPO / 'research/regional/tombs/scores.csv'
TOMB_PLAN = REPO / 'research/regional/tombs/PLAN.md'
PITS = REPO / 'research/text/entry46_alternatives_2026-10-12/pit_followup.csv'
READINGS = REPO / 'research/text/entry46_alternatives_2026-10-12/reading_branches.csv'
M, F, U, NS = 'MATCH', 'FAIL', 'UNKNOWN', 'not_scored'


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def canon(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(value).hexdigest()


def overall(codes):
    codes = list(codes)
    if F in codes:
        return F
    return M if codes and all(x == M for x in codes) else U


def source_ref(source_id, locator, sources):
    source = sources[source_id]
    return {'source_id': source_id, 'locator': locator,
            'source_url': source['source_url'], 'source_sha256': source['sha256'],
            'exposure': 'already_inspected_exploratory',
            'original_campaign': {'mccown': 'Tell en-Nasbeh 1926–1935',
                                 'pritchard': 'Gibeon 1956',
                                 'rahmani': "Jason's Tomb 1956–1957",
                                 'arnona2008': 'A-4785 May 2006',
                                 'arnona2024': 'A-9163 December 2021'}[source_id]}


def build():
    cfg = json.loads(CFG.read_text(encoding='utf-8'))
    sources = {s['source_id']: s for s in json.loads(SOURCES.read_text(encoding='utf-8'))}
    assert set(sources) == set(cfg['required_sources'])
    plan = json.loads(re.search(r'```json\n(.*?)\n```',
                               TOMB_PLAN.read_text(encoding='utf-8'), re.S)[1])
    tombs = {r['unit_id']: r for r in read_csv(TOMBS)}
    tomb_scores = read_csv(TOMB_SCORES)
    pits = {r['origin_row']: r for r in read_csv(PITS)}
    readings = read_csv(READINGS)
    witnesses, scores = [], []
    seen = set()

    for b in cfg['tomb_witnesses']:
        assert b['witness_id'] not in seen
        seen.add(b['witness_id'])
        parent = tombs[b['parent_id']]
        witness = dict(b, parent_record=parent,
                       parent_row_sha256=digest(canon(parent).encode()),
                       source_refs=[source_ref('rahmani', b['locator'], sources)])
        witnesses.append(witness)
        selected = [r for r in tomb_scores if r['unit_id'] == b['parent_id']
                    and int(r['branch'].split('-')[0]) in b['entries']]
        assert selected
        for model in cfg['entrance_models']:
            for row in selected:
                clauses = plan['branches'][row['branch']]['clauses']
                if not clauses:
                    codes = {}
                else:
                    codes = dict(zip(clauses, row['values'].split(';')))
                    codes = {k: {'yes': M, 'no': F, 'unknown': U}[v] for k, v in codes.items()}
                    assert len(codes) == len(clauses)
                after = dict(codes)
                for k, value in b['supported_proxy_clauses'].items():
                    if k in after:
                        after[k] = value
                # A position on a side is not itself a surveyed facing bearing.
                if 'F7w' in after:
                    after['F7w'] = b['reported_side_as_face'] if model == 'reported-side-as-face' else U
                subset = overall(after.values()) if after else NS
                full = overall([subset, b['configuration_in_window'], b['target_relation'], b['datum']]) if after else NS
                scores.append({'witness_id': b['witness_id'], 'parent_id': b['parent_id'],
                               'entry': int(row['branch'].split('-')[0]),
                               'reading': row['branch'], 'model': model,
                               'raw_result': row['result'], 'clauses_before': codes,
                               'clauses_after': after, 'reported_subset': subset,
                               'phase_and_target_relation': full,
                               'disposition': 'rejected for this witness/model' if subset == F else 'not identifiable from available evidence',
                               'identification': U, 'closed_assessment_reopened': False})

    for b in cfg['pit_witnesses']:
        assert b['witness_id'] not in seen
        seen.add(b['witness_id'])
        parent = pits[b['origin_row']]
        # Preserve the previously corrected coordinates/ranges, including blanks.
        witness = dict(b, parent_record=parent,
                       parent_row_sha256=digest(canon(parent).encode()),
                       position={k: parent[k] for k in ('lat', 'lon', 'precision_m',
                                                       'position_kind', 'range_bounds_m')},
                       reported_window_before=parent['reported_window'],
                       source_refs=[source_ref(b['source_id'], b['locator'], sources)])
        witnesses.append(witness)
        for reading in readings:
            numerical = reading['interpretation']
            # The exact listed group is finite; another unlocated group is not
            # disproved by this source's selected or interrupted excavation.
            scopes = ('listed-source-group', 'unlocated-other-set') if numerical == 'ten-small-pits' else ('existing-unresolved-target',)
            for scope in scopes:
                count = F if scope == 'listed-source-group' and b['pit_count'] != 10 else U
                numerical_status = count if numerical == 'ten-small-pits' else U
                form = parent['pit_form'] if reading['installation'] == 'deep-pit' else U
                codes = {'form': form, 'function': b['function'],
                         'configuration': b['configuration_in_window'],
                         'entrance': b['entrance'], 'same_phase': b['same_phase'],
                         'numerical_target': numerical_status,
                         'original_datum': U, 'textual_place_identity': U}
                if reading['installation'] == 'deep-pit':
                    codes['deep_qualification'] = parent['deep_qualification']
                scores.append({'witness_id': b['witness_id'], 'parent_id': b['origin_row'],
                               'entry': 46, 'reading': reading['installation']+'|'+numerical,
                               'model': scope, 'raw_result': 'existing target and geography outputs retained',
                               'clauses_before': {'reported_window': parent['reported_window'],
                                                  'configuration': parent['configuration_in_window']},
                               'clauses_after': codes,
                               'reported_subset': overall(codes.values()),
                               'phase_and_target_relation': overall(codes.values()),
                               'disposition': 'rejected for this listed group only' if count == F else 'not identifiable from available evidence',
                               'identification': U, 'closed_assessment_reopened': False})

    # No matching IDs in the inspected cave/tomb/water lanes: these remain
    # explicitly source-defined comparanda, with no invented regional scores.
    comparanda = []
    for b in cfg['source_comparanda']:
        assert b['witness_id'] not in seen
        seen.add(b['witness_id'])
        assert b['inventory_parent_id'] is None and b['geometry'] is None
        comparanda.append(dict(b, source_refs=[source_ref(b['source_id'], b['locator'], sources)]))
    relations = []
    for b in cfg['relation_checks']:
        ref = source_ref(b['source_id'], b['locator'], sources)
        if 'original_campaign' in b:
            ref['original_campaign'] = b['original_campaign']
        relations.append(dict(b, source_refs=[ref],
                              regional_score=NS, formal_outcome_ledger_eligibility=False,
                              closed_assessment_reopened=False))

    paths = [CFG, Path(__file__), SOURCES, TOMBS, TOMB_SCORES, TOMB_PLAN, PITS, READINGS]
    inputs = [{'path': str(p.relative_to(REPO)), 'bytes': p.stat().st_size,
               'sha256': digest(p.read_bytes())} for p in sorted(paths)]
    result = {'schema_version': 1, 'analysis_kind': cfg['analysis_kind'],
              'baseline_commit': cfg['baseline_commit'], 'rules': cfg['rules'],
              'witnesses': witnesses, 'source_comparanda': comparanda,
              'relation_checks': relations, 'scores': scores,
              'retained_readings': readings,
              'limit': 'Exposed selected witnesses; source-group failures are conditional. Existing geography/numerical outputs and regional denominators are retained, not recomputed. No registered unseen observation.'}
    return result, inputs


def score_csv(result):
    buf = io.StringIO(newline='')
    columns = ['witness_id', 'parent_id', 'entry', 'reading', 'model', 'raw_result',
               'clauses_before', 'clauses_after', 'reported_subset',
               'phase_and_target_relation', 'disposition', 'identification']
    writer = csv.DictWriter(buf, columns, lineterminator='\n', extrasaction='ignore')
    writer.writeheader()
    for row in result['scores']:
        writer.writerow({k: canon(v) if isinstance(v, (dict, list)) else v for k, v in row.items()})
    return buf.getvalue()


if __name__ == '__main__':
    result, inputs = build()
    print(json.dumps(result, indent=2, ensure_ascii=False))
