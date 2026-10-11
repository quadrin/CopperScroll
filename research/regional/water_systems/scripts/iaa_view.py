#!/usr/bin/env python3
"""Exploratory view: the merged IAA inventory folded into the water-systems lane (PLAN_AMENDMENT_IAA_2026-10-11.md).

Run from the repository root (standard library only):
  python3 -I research/regional/water_systems/scripts/iaa_view.py [--posthoc]
Codes the merged IAA rows by the frozen build_haesi rule (attrs_for and date_code, imported unchanged; the subtype read
as a second sentence), then runs the frozen build_water.main and score.main, imported unchanged, in working copies
outside the lane folder: (1) the committed survey_rows.csv, to check that the harness reproduces counts.csv;
(2) the committed survey rows without their 17 HAESI rows, plus the IAA rows; (3) the same with the 300 m bracket;
(4) a sensitivity coded exactly as the frozen build_haesi (quote only, no subtype).
Writes iaa_survey_rows.csv, iaa_counts.csv, iaa_headline.csv, iaa_view_2026-10-11.csv and iaa_summary.json; never
writes water.csv, scores.csv, merged_units.csv, merged_scores.csv, counts.csv or headline.csv.
--posthoc prints the IAA-row MATCHes in non-trivial clauses that need a reading in iaa_posthoc_checks.csv.
"""
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
import build_survey as BS  # noqa: E402  (frozen attrs_for; unchanged)
import build_water as BW  # noqa: E402  (frozen; unchanged)
import score as SW  # noqa: E402  (frozen; unchanged)

LANE = C.LANE
MERGED = os.path.join(C.REPO, 'research', 'regional', 'haesi_features', 'merged_2026-10-11')
INPUT_SHA = {  # PLAN_AMENDMENT_IAA §2
    'features_all.csv': '2170f7fb15b097621e07648c128719f25e50e3550d5ec8756c08fca6267e455b',
    'report_groups.csv': '06085467541339b097fcd29a55a5d7e8d49ade829b7f8329a00f981e9624b89c',
    'sites.csv': '7e89ddce959869e8a960103e63417870d621edb5f7f1b0376b3d12f54450e87b',
}
TMAP = {'cistern': 'cistern', 'pool_reservoir': 'reservoir_pool', 'channel_aqueduct': 'aqueduct', 'dam': 'dam',
        'ritual_bath': 'ritual_bath'}
BRACKET_KM = 0.3
NONTRIVIAL = {'head', 'marker', 'side', 'flow', 'name', 'fissure', 'great', 'north', 'four', 'conduit', 'channels', 'wadi',
              'great_wadi', 'plaster', 'entrance', 'bend', 'tur', 'kozeba'}


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def tier1(r):
    return bool(re.match(r'HA(28|29)-', r['report_id'])) or bool(re.search(r'almit|עלמית', r['site_name'], re.I))


def select(rows):
    """Version rule (amendment §4): preferred or single version; an alternate only for a class the preferred lacks."""
    by = defaultdict(list)
    for r in rows:
        if r['counted'] == 'yes' and r['feature_type'] in TMAP:
            by[(r['report_group'], r['feature_type'])].append(r)
    out = []
    for k in sorted(by):
        rs = by[k]
        out += [r for r in rs if r['version_role'] in ('single', 'preferred')] or rs
    return out


def iaa_rows(places, subtype=True):
    """subtype=False reproduces the frozen build_haesi coding exactly (quote only): the sensitivity run."""
    rows, coverage = [], Counter()
    for r in select(read(os.path.join(MERGED, 'features_all.csv'))):
        t = TMAP[r['feature_type']]
        q, sub = r.get('quote', ''), (r.get('feature_subtype', '') if subtype else '')
        if t == 'ritual_bath':  # frozen build_haesi rule, with the subtype read too (amendment §3)
            both = q + ' ' + sub
            if not re.search(r'\b(pools?|reservoirs?|cisterns?)\b', both, re.I):
                coverage['ritual bath not called a pool, reservoir or cistern'] += 1
                continue
            t = 'reservoir_pool' if re.search(r'\b(pools?|reservoirs?)\b', both, re.I) else 'cistern'
        if not r['lat']:
            coverage[f"unlocated {t}@{r['count_zone']}"] += 1
            continue
        lat, lon = float(r['lat']), float(r['lon'])
        if not C.in_box(lat, lon):
            coverage['outside the box'] += 1
            continue
        A = BS.attrs_for([s for s in (q, sub) if s], r['site_name'], places, lat, lon)
        dc, _ = C.date_code(r['period_as_given'])
        if dc == 'undated' and r['dated_in_window'] == 'no':
            dc = 'out'
        row = {k: '' for k in C.COLUMNS}
        row.update(A)
        row.update(dict(
            id=f"HAESI-{r['report_id']}-{t}-{r['row_uid']}", lineage='HAESI',
            source=f"{r['series']} {r['volume']} ({r['year']})",
            locator=f"{r['series']} {r['volume']} p. {r['pages']}; {r['url']}; merged row {r['row_uid']}",
            record_id=r['report_id'], name=r['site_name'], type=t,
            aggregate='yes' if (r['n_features'] or '1') not in ('1', '') else 'no', count=r['n_features'],
            lat=f'{lat:.6f}', lon=f'{lon:.6f}', crs=(r['crs_used'] or 'printed grid') + ' -> EPSG:4326',
            precision_m=r['precision_m'], coord_source=r['coordinate_source'], period_as_given=r['period_as_given'],
            date_code=dc, site_period_in_window='unknown', excavated=r['excavated_or_surveyed'], label='EVIDENCE',
            quote='', flow_from='unknown', span_sha256=C.sha256_text(q + '|' + sub),
            notes=f"merged IAA inventory row {r['row_uid']}; report group {r['report_group']}; site {r['site_id']}"
                  + ('; tier1_related (HA 28-29 or Kh. Almit)' if tier1(r) else '')))
        rows.append(row)
    return rows, coverage


def run(survey_rows, workdir):
    """Run the frozen build_water and score in a working copy; return its tables."""
    os.makedirs(workdir, exist_ok=True)
    for fn in ('site_points.csv', 'sources_read.csv'):
        shutil.copy(os.path.join(LANE, fn), os.path.join(workdir, fn))
    with open(os.path.join(workdir, 'survey_rows.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=C.COLUMNS, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        w.writerows(survey_rows)
    saved = C.LANE
    C.LANE = workdir
    try:
        BW.main()
        SW.main()
    finally:
        C.LANE = saved
    return {fn: os.path.join(workdir, fn) for fn in ('water.csv', 'merged_units.csv', 'merged_scores.csv', 'counts.csv',
                                                    'headline.csv', 'scores.csv')}


def bracket(survey, iaa, water_csv):
    """300 m bracket (amendment §5): an IAA row near a merged ASI or WBADB unit of the same type is a duplicate."""
    units = [r for r in read(water_csv) if r['lineage'] in ('ASI', 'WBADB') and r['in_box'] == 'yes'
             and not r['dup_of'] and not r['superseded_by']]
    by_type = defaultdict(list)
    for u in units:
        by_type[u['type']].append(u)
    out, n = [], 0
    for r in iaa:
        r2 = dict(r)
        best = None
        for u in by_type.get(r['type'], []):
            d = C.km(float(r['lat']), float(r['lon']), float(u['lat']), float(u['lon']))
            if d <= BRACKET_KM and (best is None or d < best[0]):
                best = (d, u['id'])
        if best:
            r2['dup_of'] = best[1]
            n += 1
        out.append(r2)
    return survey + out, n


def counts(path):
    return {(r['entry'], r['branch'], r['lineage'], r['date_rule']): r for r in read(path)}


def main(argv):
    for name, h in INPUT_SHA.items():
        if sha(os.path.join(MERGED, name)) != h:
            raise SystemExit(f'{name}: hash differs from the amendment value')
    places = C.load_places()
    frozen_survey = read(os.path.join(LANE, 'survey_rows.csv'))
    kept = [r for r in frozen_survey if r['lineage'] != 'HAESI']
    iaa, coverage = iaa_rows(places)
    tmp = tempfile.mkdtemp(prefix='water_iaa_')
    try:
        f = run(frozen_survey, os.path.join(tmp, 'frozen'))
        if sha(f['counts.csv']) != sha(os.path.join(LANE, 'counts.csv')) or \
                sha(f['headline.csv']) != sha(os.path.join(LANE, 'headline.csv')):
            raise SystemExit('the harness does not reproduce the committed counts.csv and headline.csv')
        v = run(kept + iaa, os.path.join(tmp, 'view'))
        bsurvey, n_bracket = bracket(kept, iaa, v['water.csv'])
        b = run(bsurvey, os.path.join(tmp, 'bracket'))
        iaa_q, _ = iaa_rows(places, subtype=False)
        qo = run(kept + iaa_q, os.path.join(tmp, 'quote_only'))
        fz, nw, br = counts(os.path.join(LANE, 'counts.csv')), counts(v['counts.csv']), counts(b['counts.csv'])
        qc = counts(qo['counts.csv'])
        water = {r['id']: r for r in read(v['water.csv'])}
        units = {u['unit_id']: u['row_ids'].split(';') for u in read(v['merged_units.csv'])}
        mscores = read(v['merged_scores.csv'])
        fscores = {(r['unit_id'], r['entry'], r['branch']): r for r in read(os.path.join(LANE, 'merged_scores.csv'))}
        new_m = defaultdict(list)
        for s in mscores:
            if s['overall'] == 'MATCH' and (s['unit_id'], s['entry'], s['branch']) not in fscores:
                new_m[(s['entry'], s['branch'])].append((s['unit_id'], s['date_code']))
        view = []
        for key in sorted(set(fz) | set(nw)):
            e, br_, lin, rule = key
            if lin not in ('MERGED', 'HAESI') or rule not in ('main', 'dated'):
                continue
            a, c, d, q = fz.get(key), nw.get(key), br.get(key), qc.get(key)
            z = dict(N='0', k_match='0', f_fail='0', m_unknown='0')
            a, c, d, q = a or z, c or z, d or z, q or z
            nm = [u for u, dc in new_m.get((e, br_), []) if rule == 'main' or dc in ('in', 'in_hedged')] if lin == 'MERGED' else []
            view.append(dict(entry=e, branch=br_, lineage=lin, date_rule=rule,
                             frozen_N=a['N'], frozen_k=a['k_match'], frozen_f=a['f_fail'], frozen_m=a['m_unknown'],
                             new_N=c['N'], new_k=c['k_match'], new_f=c['f_fail'], new_m=c['m_unknown'],
                             delta_N=int(c['N']) - int(a['N']), delta_k=int(c['k_match']) - int(a['k_match']),
                             delta_f=int(c['f_fail']) - int(a['f_fail']), delta_m=int(c['m_unknown']) - int(a['m_unknown']),
                             bracket_N=d['N'] if lin == 'MERGED' else '', bracket_k=d['k_match'] if lin == 'MERGED' else '',
                             bracket_f=d['f_fail'] if lin == 'MERGED' else '', bracket_m=d['m_unknown'] if lin == 'MERGED' else '',
                             quoteonly_N=q['N'], quoteonly_k=q['k_match'], quoteonly_f=q['f_fail'], quoteonly_m=q['m_unknown'],
                             new_match_units=';'.join(nm)))
        # post-hoc reading list (amendment §6): IAA-row MATCHes in non-trivial clauses
        post = []
        for s in read(v['scores.csv']):
            if s['lineage'] != 'HAESI' or s['in_box'] != 'yes':
                continue
            for part in s['clauses'].split(';'):
                k, _, val = part.partition('=')
                if val == 'MATCH' and k in NONTRIVIAL:
                    post.append((s['id'], k))
        post = sorted(set(post))
        checks = {(r['id'], r['clause']): r for r in read(os.path.join(LANE, 'iaa_posthoc_checks.csv'))} \
            if os.path.exists(os.path.join(LANE, 'iaa_posthoc_checks.csv')) else {}
        if '--posthoc' in argv:
            for i, k in post:
                if (i, k) not in checks:
                    w = water[i]
                    print(json.dumps(dict(id=i, clause=k, type=w['type'], name=w['name'], date=w['date_code'],
                                          period=w['period_as_given'], row=w['notes'].split(';')[0]), ensure_ascii=False))
            return
        missing = [p for p in post if p not in checks]
        if missing:
            raise SystemExit(f'{len(missing)} post-hoc readings missing; run with --posthoc')
        hf = {r['count']: r for r in read(os.path.join(LANE, 'headline.csv'))}
        hn = {r['count']: r for r in read(v['headline.csv'])}
        hb = {r['count']: r for r in read(b['headline.csv'])}
        head = [dict(count=k, frozen_rows=hf[k]['rows_in_box'], frozen_units=hf[k]['merged_units'],
                     new_rows=hn[k]['rows_in_box'], new_units=hn[k]['merged_units'], bracket_units=hb[k]['merged_units'])
                for k in hf]
        with open(os.path.join(LANE, 'iaa_survey_rows.csv'), 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=C.COLUMNS + ['superseded_by_in_view', 'merged_unit_in_view'],
                               lineterminator='\n', extrasaction='ignore')
            w.writeheader()
            in_unit = {i: u for u, ids in units.items() for i in ids}
            for r in iaa:
                w.writerow(dict(r, superseded_by_in_view=water[r['id']]['superseded_by'], merged_unit_in_view=in_unit.get(r['id'], '')))
        shutil.copy(v['counts.csv'], os.path.join(LANE, 'iaa_counts.csv'))
        write(os.path.join(LANE, 'iaa_headline.csv'), list(head[0]), head)
        write(os.path.join(LANE, 'iaa_view_2026-10-11.csv'), list(view[0]), view)
        nunits = sum(1 for u, ids in units.items() if all(water[i]['lineage'] == 'HAESI' for i in ids))
        summary = dict(
            note='Exploratory view (PLAN_AMENDMENT_IAA_2026-10-11.md). The frozen tables are unchanged.',
            inputs=INPUT_SHA, frozen_haesi_rows_removed=sum(1 for r in frozen_survey if r['lineage'] == 'HAESI'),
            iaa_rows_in_box=len(iaa), iaa_rows_by_type=dict(Counter(r['type'] for r in iaa)),
            iaa_rows_superseded=sum(1 for r in iaa if water[r['id']]['superseded_by']),
            iaa_merged_units=nunits, merged_units_frozen=len(read(os.path.join(LANE, 'merged_units.csv'))),
            merged_units_view=len(units), bracket_iaa_rows_treated_as_duplicates=n_bracket,
            merged_units_bracket=len(read(b['merged_units.csv'])),
            iaa_rows_unlocated=sum(v for k, v in coverage.items() if k.startswith('unlocated')),
            quote_only_iaa_rows_in_box=len(iaa_q),
            iaa_rows_dated_in_window=dict(Counter(r['date_code'] for r in iaa)),
            coverage=dict(sorted(coverage.items())),
            tier1_rows=[r['id'] for r in iaa if 'tier1_related' in r['notes']],
            posthoc=dict(Counter(c['verdict'] for c in checks.values())))
        with open(os.path.join(LANE, 'iaa_summary.json'), 'w', encoding='utf-8') as fh:
            json.dump(summary, fh, indent=1, ensure_ascii=False)
            fh.write('\n')
        print(json.dumps({k: summary[k] for k in ('iaa_rows_in_box', 'iaa_rows_superseded', 'iaa_merged_units',
                                                  'merged_units_frozen', 'merged_units_view',
                                                  'bracket_iaa_rows_treated_as_duplicates')}))
    finally:
        shutil.rmtree(tmp)


def write(path, fields, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


if __name__ == '__main__':
    main(sys.argv[1:])
