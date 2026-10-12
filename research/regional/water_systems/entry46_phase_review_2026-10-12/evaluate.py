#!/usr/bin/env python3
"""Exploratory, phase-separated entry-46 pool-reading screen; no frozen writes."""
import csv
import gzip
import hashlib
import io
import json
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
REPO = LANE.parents[2]
sys.path.insert(0, str(LANE / 'scripts'))
import common as C
import iaa_view as IV
import phase4_view as PV
import score as S


def read(path):
    with Path(path).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, rows):
    f = io.StringIO(newline='')
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    data = f.getvalue().encode('utf-8')
    if str(path).endswith('.gz'):
        with Path(path).open('wb') as raw:
            with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as compressed:
                compressed.write(data)
    else:
        Path(path).write_bytes(data)


def select_receptacles(water, merged):
    """Same reported-class gate for preferred candidates and all comparators.

    Keep uncertain/aggregate descriptions. These are source rows, not unique
    installations. Do not merge complementary clauses from different phases.
    Add every selected bath row, even if no English pool/cistern keyword let it
    enter the earlier water view. PV's version/region/held exclusions still apply.
    """
    rows = [dict(r) for r in water if r['in_box'] == 'yes' and
            r['type'] in ('reservoir_pool', 'cistern', 'basin_tank') and
            not r['dup_of'] and not r['superseded_by']]
    existing_ids = [r['id'] for r in rows if r['lineage'] == 'HAESI']
    held = PV.held_ids()
    added = []
    for r in IV.select(merged):
        if r['feature_type'] != 'ritual_bath' or r['series'] == 'SWP Memoirs':
            continue
        if PV.excluded(r, held) or not r['lat']:
            continue
        if not C.in_box(float(r['lat']), float(r['lon'])):
            continue
        if any(i.endswith('-' + r['row_uid']) for i in existing_ids):
            continue
        dc, _ = C.date_code(r['period_as_given'])
        if dc == 'undated' and r['dated_in_window'] == 'no':
            dc = 'out'
        item = dict(id='BATH-' + r['report_id'] + '-' + r['row_uid'],
                    lineage='HAESI', type='ritual_bath', name=r['site_name'],
                    lat=r['lat'], lon=r['lon'], precision_m=r['precision_m'],
                    aggregate='yes' if (r['n_features'] or '1') not in ('1', '') else 'no',
                    source=f"{r['series']} {r['volume']} ({r['year']})",
                    locator=f"{r['pages']}; {r['url']}; {r['row_uid']}",
                    date_code=dc, entrance='unknown', feature_subtype=r['feature_subtype'])
        # Source labels alone cannot supply an entrance observation.
        rows.append(item)
        added.append(item['id'])
    return rows, added


def default_phase(r):
    return dict(phase_id=r['id'] + '@unsplit', origin_row=r['id'],
                phase='unsplit source description', name=r['name'], source=r['source'],
                locator=r['locator'], type=r['type'], aggregate=r['aggregate'],
                lat=r['lat'], lon=r['lon'], precision_m=r['precision_m'],
                reported_period=r['date_code'], entrance=S.M if r['entrance'] == 'yes' else S.U,
                entrance_model='reported entrance; phase attachment unverified',
                original_stair_origin=S.U,
                reported_contained_water=S.U if r['type'] == 'basin_tank' else S.M,
                contained_water=S.U,
                storage_use=S.U, same_phase=S.U, configuration_in_window=S.U,
                evidence_level='reported form only; water use and phase not newly verified')


def apply_phases(rows, overrides, positions):
    replacements = {}
    for spec in overrides:
        matches = [r for r in rows if spec['origin_contains'] in r['id'] and
                   r['id'].endswith(spec['origin_endswith'])]
        if len(matches) != 1:
            raise ValueError(('ambiguous phase attachment', spec['phase_id'], len(matches)))
        r = matches[0]
        p = default_phase(r)
        pos = positions[spec['position_key']]
        p.update(lat=str(pos['lat']), lon=str(pos['lon']),
                 precision_m=str(pos['precision_envelope_m']))
        p.update({k: v for k, v in spec.items() if k not in
                  ('origin_contains', 'origin_endswith', 'position_key')})
        p['reported_contained_water'] = p['contained_water']
        replacements.setdefault(r['id'], []).append(p)
    phases = []
    for r in rows:
        phases.extend(replacements.get(r['id'], [default_phase(r)]))
    if len({p['phase_id'] for p in phases}) != len(phases):
        raise ValueError('duplicate phase identity')
    return phases


def evaluate(phases, places):
    scores = []
    for p in phases:
        for model, clause in (('contained-water', 'contained_water'), ('storage-use', 'storage_use')):
            for anchor in ('ramat_rahel', 'ein_kerem'):
                for radius in (1, 2):
                    place = S.within(p, places[anchor], radius)
                    report_function = p['reported_contained_water'] if model == 'contained-water' else p[clause]
                    screen = S.overall([place, p['entrance'], report_function])
                    period = S.M if p['reported_period'] in ('in', 'in_hedged') else (
                        S.F if p['reported_period'] == 'out' else S.U)
                    window_screen = S.overall([place, p['entrance'], report_function, period])
                    joined = S.overall([place, p['entrance'], p[clause], p['same_phase']])
                    stair = S.overall([place, p['original_stair_origin'], p[clause]])
                    # Candidate place association, left/ten readings and ancient
                    # datum lack verified joins. No unmeasured branch is a match.
                    full = S.overall([place, p['entrance'], p[clause], p['same_phase'],
                                      p['configuration_in_window'], S.U, S.U, S.U])
                    scores.append(dict(phase_id=p['phase_id'], origin_row=p['origin_row'],
                                       function_model=model, anchor=anchor, radius_km=radius,
                                       place=place, entrance=p['entrance'], function=p[clause],
                                       same_phase=p['same_phase'], configuration_in_window=p['configuration_in_window'],
                                       reported_period=p['reported_period'], reported_form_screen=screen,
                                       reported_window_screen=window_screen,
                                       original_stair_origin=p['original_stair_origin'], stair_origin_screen=stair,
                                       phase_join_screen=joined, site_association=S.U,
                                       left_origin=S.U, ten_measure_or_pits=S.U,
                                       full_pool_branch=full))
    return scores


def main(output=HERE):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    protected = {str(p): sha(p) for p in LANE.rglob('*') if p.is_file() and
                 HERE not in p.parents and '__pycache__' not in str(p)}
    inputs = [LANE / 'survey_rows.csv', LANE / 'phase4_survey_rows.csv',
              LANE / 'phase4_counts.csv', LANE / 'site_points.csv', LANE / 'sources_read.csv',
              Path(C.PLACES_CSV), HERE / 'phase_overrides.json', HERE / 'evaluate.py',
              REPO / 'research/assessments/entry46_baths_2026-10-12/positions.json',
              REPO / 'research/assessments/entry46_baths_2026-10-12/README.md',
              REPO / 'research/sources/full_reads_2026-10-12/storage_language_audit/function_rules.json']
    inputs += [LANE / 'scripts' / n for n in
               ('common.py', 'build_water.py', 'build_survey.py', 'literature_data.py',
                'literature_data_2.py', 'score.py', 'iaa_view.py', 'phase4_view.py')]
    inputs += [REPO / p for p in IV.BW.REPO_TEXT.values()]
    inputs += [REPO / 'research/regional/asi_jerusalem/sites.csv']
    inputs += sorted(Path(PV.PHASE4).glob('**/held*.csv'))
    merged_path = Path(PV.MERGED) / 'features_all.csv'
    if sha(merged_path) != PV.INPUT_SHA['features_all.csv']:
        raise ValueError('merged inventory pin differs')
    inputs.append(merged_path)
    kept = [r for r in read(LANE / 'survey_rows.csv') if r['lineage'] != 'HAESI']
    with tempfile.TemporaryDirectory(prefix='entry46_phase_review_') as tmp:
        files = IV.run(kept + read(LANE / 'phase4_survey_rows.csv'), tmp)
        if sha(files['counts.csv']) != sha(LANE / 'phase4_counts.csv'):
            raise ValueError('phase-4 baseline does not reproduce')
        rows, added = select_receptacles(read(files['water.csv']), read(merged_path))
    positions_path = REPO / 'research/assessments/entry46_baths_2026-10-12/positions.json'
    positions = {p['key']: p for p in json.loads(positions_path.read_text())['positions']}
    overrides = json.loads((HERE / 'phase_overrides.json').read_text())
    phases = apply_phases(rows, overrides, positions)
    scores = evaluate(phases, {'ramat_rahel': C.load_places()['ramat_rahel'][:2], 'ein_kerem': C.EIN_KAREM})
    write(output / 'phases.csv.gz', phases)
    write(output / 'scores.csv.gz', scores)
    counts = defaultdict(Counter)
    for r in scores:
        for layer in ('reported_form_screen', 'reported_window_screen', 'phase_join_screen', 'full_pool_branch'):
            counts[(r['function_model'], r['anchor'], r['radius_km'], layer)][r[layer]] += 1
    write(output / 'counts.csv', [dict(function_model=m, anchor=a, radius_km=r, layer=l,
                                     N=sum(c.values()), match=c[S.M], fail=c[S.F], unknown=c[S.U])
                                for (m, a, r, l), c in sorted(counts.items())])
    audited = {p['phase_id'] for p in overrides}
    write(output / 'audited_candidate_scores.csv', [r for r in scores if r['phase_id'] in audited])
    if protected != {str(p): sha(p) for p in LANE.rglob('*') if p.is_file() and
                     HERE not in p.parents and '__pycache__' not in str(p)}:
        raise ValueError('existing lane file changed')
    summary = dict(scope='all in-box retained source rows for reported pools/cisterns/basins plus omitted ritual baths; not a regional installation denominator',
                   exploratory=True, baseline_counts_reproduced=True,
                   added_ritual_bath_source_rows=added, input_sha256={str(p.relative_to(REPO)): sha(p) for p in inputs},
                   phase_rows=len(phases), scores=len(scores),
                   function_rule_ids={'contained-water': 'contained_water_basin', 'storage-use': 'storage_service'},
                   phase_window_rule='date of the retained usable configuration, not a requirement that initial cutting occurred within the window; earlier construction with dated later use may qualify',
                   excluded_reading='Lefkovits deep-pit reading needs a separately declared non-water inventory; not rejected',
                   unresolved_measurement='distance, depth and ten-small-pits readings retained; no numerical claim tested',
                   aggregation='no cross-row or cross-phase clause combination; duplicates unresolved beyond original exclusions')
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: summary[k] for k in ('phase_rows', 'scores', 'baseline_counts_reproduced')}))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else HERE)
