#!/usr/bin/env python3
"""Exploratory view: the phase 1-4 merged inventory folded into the water-systems lane
(PLAN_AMENDMENT_PHASE4_2026-10-12.md). Adapted from iaa_view.py, which is imported and left unchanged.

Run from the repository root (standard library only):
  python3 -I research/regional/water_systems/scripts/phase4_view.py [--posthoc]
Codes the merged_2026-10-12 rows by the frozen build_haesi rule (subtype read as a second sentence, as in the IAA
view), then runs the frozen build_water.main and score.main, imported unchanged, in working copies outside the lane:
  0 the committed survey_rows.csv (must reproduce counts.csv and headline.csv);
  0b the IAA view inputs (must reproduce iaa_counts.csv);
  1 primary: committed survey rows without HAESI rows + merged phase 1-4 rows, SWP Memoirs excluded (PLAN 3.5);
  2 phases 1-3 rows only, under the new grouping;  3 the 300 m bracket;  4 quote-only;  5 with SWP rows.
Writes phase4_survey_rows.csv, phase4_counts.csv, phase4_headline.csv, phase4_view_2026-10-12.csv,
phase4_scores.csv and phase4_summary.json; never writes the frozen tables or the iaa_* files.
--posthoc prints the MATCHes in non-trivial clauses that still need a reading in phase4_posthoc_checks.csv.
"""
import csv
import glob
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
import iaa_view as IV  # noqa: E402  (IAA view; unchanged)

LANE = C.LANE
HF = os.path.join(C.REPO, 'research', 'regional', 'haesi_features')
MERGED = os.path.join(HF, 'merged_2026-10-12')
PHASE4 = os.path.join(HF, 'phase4_2026-10-11')
INPUT_SHA = {  # amendment §2
    'features_all.csv': '940e6c04b1ecd18c79a7c88a784a463d69056f70c6e31ad18e5a18c46866d65d',
    'report_groups.csv': '38b67f3c7095993287ac9da80eb229a9752d56ff7c27cb9bb3b1024f47da702f',
    'sites.csv': '5d7458016d7955cced5540d4307570879fbc5b2071d5f644e85d3cec0fcc16db',
}
STRIP = re.compile(r'\bt[ae]l+[- ]?(e[sl][- ])?sultan|tall al-sultan', re.I)
ALMIT = re.compile(r'almit|עלמית', re.I)
# lane places named in PLAN_AMENDMENT_1 §3, plus Ramat Rahel and Ein Kerem (amendment §4, coverage note only)
LANE_PLACE = re.compile(r'qumran|sekakah|secacah|buq[ei]', re.I), re.compile(
    r'jericho|sultan|alayiq|naaran|na.aran|duk\b|nuei?ma|nuweim|doq\b|dagon|qarantal|kuruntul|cypros|kypros|aqaba|mafjar|mefjer',
    re.I), re.compile(r'qelt|kelt|qilt|fara\b|farah|perat|prat\b|fawwar|choziba|mar jiryis|st\.? george', re.I), \
    re.compile(r'ramat ra|ramet rahel|kh\.? salih|ramat rachel', re.I), re.compile(r'ka?rem|karim', re.I)


def read(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def held_ids():
    ids = set()
    for f in glob.glob(os.path.join(PHASE4, '**', 'held*.csv'), recursive=True):
        ids |= {r['unit_id'] for r in read(f)}
    return ids


def fold(s):
    return C.fold(s or '')


def excluded(r, held):
    """Amendment §5. Returns the reason, or ''."""
    if r['report_id'] in held:
        return 'held unit'
    if r['protected_strip'] == 'yes' or STRIP.search(fold(r['site_name'])):
        return 'Tell es-Sultan (strip precaution)'
    if ALMIT.search(fold(r['site_name'])) or ALMIT.search(r['site_name']) or ALMIT.search(fold(r['quote'])) \
            or ALMIT.search(r['report_id']):
        return 'Kh. Almit'
    return ''


def merged_rows(places, phases='all', swp=False, subtype=True):
    """Rows of merged_2026-10-12 in the survey schema. phases: 'all' or 'p13'."""
    held = held_ids()
    rows, coverage, excl, meta = [], Counter(), [], {}
    for r in IV.select(read(os.path.join(MERGED, 'features_all.csv'))):
        p4 = r['phase'].startswith('4')
        if phases == 'p13' and p4:
            continue
        if r['series'] == 'SWP Memoirs' and not swp:
            coverage['SWP Memoirs row not used (PLAN 3.5)'] += 1
            continue
        why = excluded(r, held)
        if why:
            excl.append((r['row_uid'], r['report_id'], why))
            continue
        t = IV.TMAP[r['feature_type']]
        q, sub = r.get('quote', ''), (r.get('feature_subtype', '') if subtype else '')
        if t == 'ritual_bath':  # frozen build_haesi rule, subtype read too (IAA amendment §3)
            both = q + ' ' + sub
            if not re.search(r'\b(pools?|reservoirs?|cisterns?)\b', both, re.I):
                coverage['ritual bath not called a pool, reservoir or cistern' + (' (phase 4)' if p4 else '')] += 1
                continue
            t = 'reservoir_pool' if re.search(r'\b(pools?|reservoirs?)\b', both, re.I) else 'cistern'
        if not r['lat']:
            coverage[f"unlocated {t}@{r['count_zone']}" + (' (phase 4)' if p4 else '')] += 1
            if p4:
                nm = fold(r['site_name'])
                hit = [k for k, rx in zip(('qumran', 'jericho_oasis', 'qelt', 'ramat_rahel', 'ein_kerem'), LANE_PLACE)
                       if rx.search(nm)]
                if hit:
                    coverage['unlocated_phase4_named_lane_place'] = coverage.get('unlocated_phase4_named_lane_place', 0) + 1
                    meta.setdefault('_unlocated_named', []).append(f"{r['report_id']}|{r['row_uid']}|{t}|{','.join(hit)}")
            continue
        lat, lon = float(r['lat']), float(r['lon'])
        if not C.in_box(lat, lon):
            coverage['outside the box' + (' (phase 4)' if p4 else '')] += 1
            continue
        A = BS.attrs_for([s for s in (q, sub) if s], r['site_name'], places, lat, lon)
        dc, _ = C.date_code(r['period_as_given'])
        if dc == 'undated' and r['dated_in_window'] == 'no':
            dc = 'out'
        row = {k: '' for k in C.COLUMNS}
        row.update(A)
        rid = f"HAESI-{r['report_id']}-{t}-{r['row_uid']}"
        row.update(dict(
            id=rid, lineage='HAESI',
            source=f"{r['series']} {r['volume']} ({r['year']})",
            locator=f"{r['series']} {r['volume']} p. {r['pages']}; {r['url']}; merged row {r['row_uid']}",
            record_id=r['report_id'], name=r['site_name'], type=t,
            aggregate='yes' if (r['n_features'] or '1') not in ('1', '') else 'no', count=r['n_features'],
            lat=f'{lat:.6f}', lon=f'{lon:.6f}', crs=(r['crs_used'] or 'printed grid') + ' -> EPSG:4326',
            precision_m=r['precision_m'], coord_source=r['coordinate_source'], period_as_given=r['period_as_given'],
            date_code=dc, site_period_in_window='unknown', excavated=r['excavated_or_surveyed'], label='EVIDENCE',
            quote='', flow_from='unknown', span_sha256=C.sha256_text(q + '|' + sub),
            notes=f"merged_2026-10-12 row {r['row_uid']}; phase {r['phase']}; report group {r['report_group']}; "
                  f"site {r['site_id']}"))
        rows.append(row)
        meta[rid] = dict(phase=r['phase'], report_group=r['report_group'], site_id=r['site_id'], pages=r['pages'],
                         series=r['series'], report_id=r['report_id'], name_placed='yes' if r['coordinate_source'].startswith('name only') else 'no',
                         subtype=r['feature_subtype'], quote=r['quote'], dated_in_window=r['dated_in_window'])
    return rows, coverage, excl, meta


def main(argv):
    for name, h in INPUT_SHA.items():
        if IV.sha(os.path.join(MERGED, name)) != h:
            raise SystemExit(f'{name}: hash differs from the amendment value')
    places = C.load_places()
    frozen_survey = read(os.path.join(LANE, 'survey_rows.csv'))
    kept = [r for r in frozen_survey if r['lineage'] != 'HAESI']
    rows, coverage, excl, meta = merged_rows(places)
    tmp = tempfile.mkdtemp(prefix='water_p4_')
    try:
        f0 = IV.run(frozen_survey, os.path.join(tmp, 'frozen'))
        if IV.sha(f0['counts.csv']) != IV.sha(os.path.join(LANE, 'counts.csv')) or \
                IV.sha(f0['headline.csv']) != IV.sha(os.path.join(LANE, 'headline.csv')):
            raise SystemExit('the harness does not reproduce the committed counts.csv and headline.csv')
        iaa, _ = IV.iaa_rows(places)
        fi = IV.run(kept + iaa, os.path.join(tmp, 'iaa'))
        if IV.sha(fi['counts.csv']) != IV.sha(os.path.join(LANE, 'iaa_counts.csv')):
            raise SystemExit('the IAA view inputs do not reproduce the committed iaa_counts.csv')
        v = IV.run(kept + rows, os.path.join(tmp, 'view'))
        p13, _, _, _ = merged_rows(places, phases='p13')
        r13 = IV.run(kept + p13, os.path.join(tmp, 'p13'))
        bsurvey, n_bracket = IV.bracket(kept, rows, v['water.csv'])
        b = IV.run(bsurvey, os.path.join(tmp, 'bracket'))
        rq, _, _, _ = merged_rows(places, subtype=False)
        qo = IV.run(kept + rq, os.path.join(tmp, 'quote_only'))
        rs, cov_s, excl_s, meta_s = merged_rows(places, swp=True)
        sw = IV.run(kept + rs, os.path.join(tmp, 'with_swp'))

        fz, ia, nw = IV.counts(os.path.join(LANE, 'counts.csv')), IV.counts(fi['counts.csv']), IV.counts(v['counts.csv'])
        c13, br, qc, sc = IV.counts(r13['counts.csv']), IV.counts(b['counts.csv']), IV.counts(qo['counts.csv']), \
            IV.counts(sw['counts.csv'])
        water = {r['id']: r for r in read(v['water.csv'])}
        units = {u['unit_id']: u['row_ids'].split(';') for u in read(v['merged_units.csv'])}
        prior = {(s['unit_id'], s['entry'], s['branch']) for s in read(fi['merged_scores.csv']) if s['overall'] == 'MATCH'}
        new_m = defaultdict(list)
        for s in read(v['merged_scores.csv']):
            if s['overall'] == 'MATCH' and (s['unit_id'], s['entry'], s['branch']) not in prior:
                new_m[(s['entry'], s['branch'])].append((s['unit_id'], s['date_code']))
        # SWP sensitivity: matches of units holding SWP rows
        swp_new = defaultdict(list)
        sw_units = {u['unit_id']: u['row_ids'].split(';') for u in read(sw['merged_units.csv'])}
        for s in read(sw['merged_scores.csv']):
            if s['overall'] == 'MATCH' and any(meta_s.get(i, {}).get('series') == 'SWP Memoirs' for i in sw_units[s['unit_id']]):
                swp_new[(s['entry'], s['branch'])].append(s['unit_id'])
        z = dict(N='0', k_match='0', f_fail='0', m_unknown='0')
        view = []
        for key in sorted(set(fz) | set(ia) | set(nw) | set(sc)):
            e, b_, lin, rule = key
            if lin not in ('MERGED', 'HAESI') or rule not in ('main', 'dated'):
                continue
            a, i_, c, d13, d, q, s_ = (t.get(key) or z for t in (fz, ia, nw, c13, br, qc, sc))
            # units that count as k under the rule (main: date code not 'out'; dated: in or in_hedged). iaa_view.py
            # lists main-rule units without the date test; that listing is not reused here.
            nm = [u for u, dc in new_m.get((e, b_), []) if (dc != 'out' if rule == 'main' else dc in ('in', 'in_hedged'))] \
                if lin == 'MERGED' else []
            row = dict(entry=e, branch=b_, lineage=lin, date_rule=rule)
            for pre, t in (('frozen', a), ('iaa', i_), ('p13new', d13), ('new', c)):
                row.update({f'{pre}_N': t['N'], f'{pre}_k': t['k_match'], f'{pre}_f': t['f_fail'], f'{pre}_m': t['m_unknown']})
            row.update(dict(delta_vs_iaa_N=int(c['N']) - int(i_['N']), delta_vs_iaa_k=int(c['k_match']) - int(i_['k_match']),
                            delta_vs_iaa_f=int(c['f_fail']) - int(i_['f_fail']),
                            delta_vs_iaa_m=int(c['m_unknown']) - int(i_['m_unknown'])))
            for pre, t in (('bracket', d), ('quoteonly', q), ('withswp', s_)):
                row.update({f'{pre}_N': t['N'], f'{pre}_k': t['k_match'], f'{pre}_f': t['f_fail'], f'{pre}_m': t['m_unknown']})
            row['new_match_units_vs_iaa'] = ';'.join(nm)
            row['swp_match_units'] = ';'.join(swp_new.get((e, b_), [])) if lin == 'MERGED' else ''
            view.append(row)

        # post-hoc reading list (IAA amendment §6): MATCHes in non-trivial clauses of merged rows in the box
        post = []
        p4scores = []
        for s in read(v['scores.csv']):
            if s['lineage'] != 'HAESI' or s['in_box'] != 'yes':
                continue
            m = meta[s['id']]
            if m['phase'].startswith('4'):
                p4scores.append(dict(s, phase=m['phase'], report_id=m['report_id'], pages=m['pages'],
                                     report_group=m['report_group'], site_id=m['site_id'], name_placed=m['name_placed'],
                                     superseded_by=water[s['id']]['superseded_by']))
            for part in s['clauses'].split(';'):
                k, _, val = part.partition('=')
                if val == 'MATCH' and k in IV.NONTRIVIAL:
                    post.append((s['id'], k))
        post = sorted(set(post))
        old = {(r['id'], r['clause']): r for r in read(os.path.join(LANE, 'iaa_posthoc_checks.csv'))}
        p4path = os.path.join(LANE, 'phase4_posthoc_checks.csv')
        new = {(r['id'], r['clause']): r for r in read(p4path)} if os.path.exists(p4path) else {}
        if '--posthoc' in argv:
            for i, k in post:
                if (i, k) not in old and (i, k) not in new:
                    w, m = water[i], meta[i]
                    print(json.dumps(dict(id=i, clause=k, type=w['type'], name=w['name'], date=w['date_code'],
                                          period=w['period_as_given'], subtype=m['subtype'], quote=m['quote'],
                                          pages=m['pages']), ensure_ascii=False))
            return
        missing = [p for p in post if p not in old and p not in new]
        if missing:
            raise SystemExit(f'{len(missing)} post-hoc readings missing; run with --posthoc')

        hf = {r['count']: r for r in read(os.path.join(LANE, 'headline.csv'))}
        hi, hn = {r['count']: r for r in read(fi['headline.csv'])}, {r['count']: r for r in read(v['headline.csv'])}
        hb, hs = {r['count']: r for r in read(b['headline.csv'])}, {r['count']: r for r in read(sw['headline.csv'])}
        head = [dict(count=k, frozen_rows=hf[k]['rows_in_box'], frozen_units=hf[k]['merged_units'],
                     iaa_rows=hi[k]['rows_in_box'], iaa_units=hi[k]['merged_units'],
                     new_rows=hn[k]['rows_in_box'], new_units=hn[k]['merged_units'],
                     bracket_units=hb[k]['merged_units'], withswp_units=hs[k]['merged_units']) for k in hf]

        in_unit = {i: u for u, ids in units.items() for i in ids}
        cols = C.COLUMNS + ['phase', 'report_group', 'site_id', 'pages', 'name_placed', 'superseded_by_in_view',
                            'merged_unit_in_view']
        with open(os.path.join(LANE, 'phase4_survey_rows.csv'), 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
            w.writeheader()
            for r in rows:
                m = meta[r['id']]
                w.writerow(dict(r, phase=m['phase'], report_group=m['report_group'], site_id=m['site_id'],
                                pages=m['pages'], name_placed=m['name_placed'],
                                superseded_by_in_view=water[r['id']]['superseded_by'],
                                merged_unit_in_view=in_unit.get(r['id'], '')))
        shutil.copy(v['counts.csv'], os.path.join(LANE, 'phase4_counts.csv'))
        IV.write(os.path.join(LANE, 'phase4_headline.csv'), list(head[0]), head)
        IV.write(os.path.join(LANE, 'phase4_view_2026-10-12.csv'), list(view[0]), view)
        IV.write(os.path.join(LANE, 'phase4_scores.csv'), list(p4scores[0]) if p4scores else ['id'], p4scores)

        # new at row, report and site level (amendment §6)
        p4 = [r for r in rows if meta[r['id']]['phase'].startswith('4')]
        p13ids = {r['id'] for r in rows if not meta[r['id']]['phase'].startswith('4')}
        site_types13 = {(meta[i]['site_id'], water[i]['type']) for i in p13ids}
        groups13 = {meta[i]['report_group'] for i in p13ids}
        sites_new = {(meta[r['id']]['site_id'], r['type']) for r in p4}
        reps_new = {(meta[r['id']]['report_group'], r['type']) for r in p4}
        p4_units = [u for u, ids in units.items() if any(meta.get(i, {}).get('phase', '').startswith('4') for i in ids)]
        summary = dict(
            note='Exploratory view (PLAN_AMENDMENT_PHASE4_2026-10-12.md). Frozen tables and the IAA view are unchanged.',
            inputs=INPUT_SHA,
            merged_rows_in_box=len(rows), merged_rows_by_type=dict(Counter(r['type'] for r in rows)),
            phase4_rows_in_box=len(p4), phase4_rows_by_type=dict(Counter(r['type'] for r in p4)),
            phase4_rows_by_part=dict(Counter(meta[r['id']]['phase'] for r in p4)),
            phase4_rows_name_placed=sum(1 for r in p4 if meta[r['id']]['name_placed'] == 'yes'),
            phase4_rows_superseded=sum(1 for r in p4 if water[r['id']]['superseded_by']),
            phase4_rows_dated=dict(Counter(r['date_code'] for r in p4)),
            phase4_report_type_units=len(reps_new),
            phase4_report_type_units_shared_with_p13=sum(1 for g in reps_new if g[0] in groups13),
            phase4_report_groups=len({g for g, _ in reps_new}),
            phase4_site_type_units=len(sites_new),
            phase4_site_type_units_shared_with_p13=len(sites_new & site_types13),
            phase4_sites=len({s for s, _ in sites_new}),
            phase13_rows_in_box_new_grouping=len(p13ids), phase13_rows_in_box_iaa_view=len(iaa),
            merged_units_frozen=len(read(os.path.join(LANE, 'merged_units.csv'))),
            merged_units_iaa_view=len(read(fi['merged_units.csv'])), merged_units_view=len(units),
            merged_units_with_phase4_rows=len(p4_units),
            bracket_rows_treated_as_duplicates=n_bracket, merged_units_bracket=len(read(b['merged_units.csv'])),
            quote_only_rows_in_box=len(rq), with_swp_rows_in_box=len(rs),
            with_swp_swp_rows_in_box=sum(1 for r in rs if meta_s[r['id']]['series'] == 'SWP Memoirs'),
            excluded_protected=[f'{u} {rid}: {w}' for u, rid, w in excl],
            excluded_protected_with_swp=[f'{u} {rid}: {w}' for u, rid, w in excl_s],
            coverage={k: v for k, v in sorted(coverage.items())},
            unlocated_phase4_named_lane_place=sorted(meta.get('_unlocated_named', [])),
            posthoc_phase4=dict(Counter(c['verdict'] for c in new.values())),
            posthoc_reused_from_iaa=sum(1 for p in post if p in old))
        with open(os.path.join(LANE, 'phase4_summary.json'), 'w', encoding='utf-8') as fh:
            json.dump(summary, fh, indent=1, ensure_ascii=False)
            fh.write('\n')
        print(json.dumps({k: summary[k] for k in ('merged_rows_in_box', 'phase4_rows_in_box', 'phase4_rows_by_type',
                                                  'merged_units_iaa_view', 'merged_units_view')}, ensure_ascii=False))
    finally:
        shutil.rmtree(tmp)


if __name__ == '__main__':
    main(sys.argv[1:])
