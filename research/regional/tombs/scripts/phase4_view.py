#!/usr/bin/env python3
"""Exploratory view: the phase 1-4 merged inventory folded into the tombs lane (PLAN_AMENDMENT_PHASE4_2026-10-12.md).

Run from the repository root:  python3 -I -B research/regional/tombs/scripts/phase4_view.py [--pending]
Applies the method of the IAA amendment (scripts/iaa_view.py, imported unchanged) to
research/regional/haesi_features/merged_2026-10-12/ in place of merged_2026-10-11, after the protected-material
exclusions of amendment §5. It first rebuilds the 11 October IAA view from merged_2026-10-11 and checks it against the
committed iaa_view_2026-10-11.csv, and checks the frozen units against scores_summary.csv (inside the shared tally).
Writes phase4_units.csv, phase4_scores.csv, phase4_view_2026-10-12.csv, phase4_amendment1_view.csv and
phase4_summary.json; never writes the frozen outputs or the 11 October view files. --pending lists the hand checks
still needed and stops.
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tombs_common as T  # noqa: E402
import build_tombs as B  # noqa: E402  (frozen Coder, clause_value, overall; unchanged)
import amendment1 as A1  # noqa: E402  (exploratory amendment 1 rules; unchanged)
import iaa_view as V  # noqa: E402  (IAA amendment method; unchanged)

FOLDER = T.FOLDER
DATA = os.path.join(FOLDER, 'data')
HF = os.path.join(T.REPO, 'research', 'regional', 'haesi_features')
MERGED12 = os.path.join(HF, 'merged_2026-10-12')
MERGED11 = V.MERGED
PHASE4 = os.path.join(HF, 'phase4_2026-10-11')
INPUT_SHA = {  # merged_2026-10-12 as rebuilt under its amendment B3 (12 Oct); amendment §2 gives the b4a41cc values
    'features_all.csv': '23a23214ed475b5c3a3a213f29d4094518acbdf1b187cffd7c78949a635eae38',
    'report_groups.csv': 'e3121121f77a4cdc85aca2158839d66372c785bde7a53746ece5861bb2d1b47d',
    'sites.csv': '749dfca8fed2473a117cb15fe1172da94206ca4779465133d460dffdc77f2626',
}
EXPOSURE4 = ('repo-coded by the phase-4 readers and merged_2026-10-12; first mapped by this lane on 12 Oct 2026, '
             'after the phase-4 amendment (d5a837e)')
EXPOSED_BY_NAME = ('ATQ113-i09',)  # amendment §1: named, with its dating, in the merge README
# amendment §5
HELD_PLACE = re.compile(r'qumran|feshkha|fashkha|qarantal|quruntul|kuruntul|quarantania|\bdu[kq]\b|nuwei|nueima|qelt|kelt', re.I)
CAVE = re.compile(r'cave', re.I)
STRIP = re.compile(r't[ae]ll?[\s_-]*(es|el|al|e)?[\s_-]*sultan', re.I)
ALMIT = re.compile(r'almit|עלמית', re.I)
CHECK_FILES = (['manual_check_iaa.csv', 'manual_check_phase4.csv'],
               ['manual_check_iaa_amendment1.csv', 'manual_check_phase4_amendment1.csv'])
LISTED_CODES = ('F1', 'F5', 'name_zadok', 'name_absalom', 'name_queen', 'name_obed')


def p4(r):
    return r['phase'].startswith('4')


def held_ids():
    ids = set()
    for f in glob.glob(os.path.join(PHASE4, '**', 'held.csv'), recursive=True):
        ids |= {r['unit_id'] for r in V.read(f) if r['unit_id']}
    return sorted(ids)


def exclusions(plan, rows):
    held = held_ids()
    ts = plan['points']['tell_es_sultan']
    out = {}
    for r in rows:
        why = []
        if any(r['report_id'] == h or r['report_id'].startswith(h) for h in held):
            why.append('held unit')
        if r['protected_strip'] == 'yes':
            why.append('protected_strip = yes')
        if r['report_id'].startswith('ATQ41-'):
            why.append('Atiqot 41')
        if p4(r):
            place = ' '.join((r['site_name'], r['coordinate_source'], r['quote']))
            if HELD_PLACE.search(place) and CAVE.search(' '.join((r['site_name'], r['feature_subtype'], r['quote']))):
                why.append('held cave area (name guard)')
            if r['lat'] and T.km(float(r['lat']), float(r['lon']), ts[0], ts[1]) <= 0.5:
                why.append('Tell es-Sultan strip (0.5 km guard)')
            if STRIP.search(r['site_name'] + ' ' + r['coordinate_source']):
                why.append('Tell es-Sultan strip (name guard)')
            if ALMIT.search(r['site_name'] + ' ' + r['report_id']):
                why.append('Kh. Almit (no comparison)')
        if why:
            out[r['row_uid']] = '; '.join(why)
    return out


def load_checks(names):
    checks = {}
    for n in names:
        p = os.path.join(DATA, n)
        if os.path.exists(p):
            for r in V.read(p):
                checks.setdefault((r['record_id'], r['code']), r)
    return checks


def manual_check(units, pending, checks):
    """As iaa_view.manual_check, with the decisions of several files."""
    for u in units:
        u['manual_rejected'] = ''
        for code in B.MANUAL_CODES:
            u[code + '_raw'] = u[code]
            if u[code] == 'yes':
                ck = checks.get((u['record_id'], code))
                if ck is None:
                    pending.append((u['record_id'], code, '', u['text']))
                elif ck['decision'] == 'reject':
                    u[code] = 'unknown'
                    u['manual_rejected'] += f"{code}: {ck['reason']}; "


def amendment1_codes(plan, units, pending, checks):
    """As iaa_view.amendment1_codes, with the decisions of several files."""
    for u in units:
        sents = T.sentences(u['text'])
        dirs = []
        for s in sents:
            dirs += [x for x in A1.orientation(plan, s) if x not in dirs]
        if not dirs:
            f7wa = 'unknown'
        elif any(x in plan['westerly'] for x in dirs):
            f7wa = 'yes'
        elif u['multi_tomb_record'] == 'yes':
            f7wa = 'unknown'
        else:
            f7wa = 'no'
        f2xa = 'yes' if (u['F2x'] == 'yes' or any(A1.ENTRANCE_PLACE.search(s) and A1.PILLAR.search(s) for s in sents)) else 'unknown'
        raw = dict(F7wa=f7wa, F2xa=f2xa)
        u['F7a'] = ';'.join(dirs) or 'unknown'
        u['a1_rejected'] = ''
        for code in ('F7wa', 'F2xa'):
            v = raw[code]
            if v in ('yes', 'no') and not (code == 'F2xa' and u['F2x'] == 'yes'):
                ck = checks.get((u['record_id'], code))
                if ck is None:
                    pending.append((u['record_id'], code, v, u['text']))
                elif ck['decision'] == 'reject':
                    raw[code] = 'unknown'
                    u['a1_rejected'] += f"{code}: {ck['reason']}; "
                elif ck['decision'] == 'set_no':
                    raw[code] = 'no'
                    u['a1_rejected'] += f"{code} set to no: {ck['reason']}; "
        u['F7wa'], u['F2xa'] = raw['F7wa'], raw['F2xa']


def build(plan, coder, sheets, frozen, rows, check_names, pending):
    prim_rows, other_rows = V.select(rows, coder)
    units, cov = V.iaa_units(plan, coder, prim_rows, sheets, 'primary')
    others, cov_o = V.iaa_units(plan, coder, other_rows, sheets, 'other_class')
    manual_check(units + others, pending, load_checks(check_names[0]))
    V.flag_duplicates(plan, units + others, frozen)
    amendment1_codes(plan, units + others, pending, load_checks(check_names[1]))
    return units, others, cov, cov_o, prim_rows


def unlocated_listing(plan, coder, prim_rows, by_uid, pending, checks):
    """Amendment §4: unlocated counted phase-4 tomb rows, coded only to list F1, F5 and name yeses. Never counted."""
    out, places = [], Counter()
    for r in prim_rows:
        if r['lat'] or not p4(r) or r['feature_type'] != V.CLASS:
            continue
        places[(r['count_zone'], r['coordinate_source'])] += 1
        text = V.text_of(r)
        c = coder.code(text, None, ())
        rid = f"IAA {r['row_uid']}"
        for code in LISTED_CODES:
            if c[code] == 'yes':
                ck = checks.get((rid, code))
                if ck is None:
                    pending.append((rid, code, 'unlocated', text))
                elif ck['decision'] != 'reject':
                    out.append(dict(record_id=rid, report_id=r['report_id'], pages=r['pages'], site_name=r['site_name'],
                                    zone=r['count_zone'], reader_place=r['coordinate_source'], code=code,
                                    dated_in_window=r['_dated']))
    return out, places


def main(argv):
    for name, h in INPUT_SHA.items():
        if V.sha(os.path.join(MERGED12, name)) != h:
            raise SystemExit(f'{name}: hash differs from the amendment value')
    plan = T.load_plan()
    coder = B.Coder(plan)
    with open(os.path.join(DATA, 'asi_selected_maps.json'), encoding='utf-8') as fh:
        sheets = json.load(fh)
    frozen = V.frozen_units()

    # 1. the 11 October view, rebuilt and checked against its committed file
    p11 = []
    u11, o11, *_ = build(plan, coder, sheets, frozen, V.read(os.path.join(MERGED11, 'features_all.csv')),
                         (['manual_check_iaa.csv'], ['manual_check_iaa_amendment1.csv']), p11)
    if p11:
        raise SystemExit('the 11 October view has hand checks pending; it does not reproduce')

    # 2. the phase 1-4 view
    rows = V.read(os.path.join(MERGED12, 'features_all.csv'))
    by_uid = {r['row_uid']: r for r in rows}
    excl = exclusions(plan, rows)
    kept = [r for r in rows if r['row_uid'] not in excl]
    pending = []
    units, others, cov, cov_o, prim_rows = build(plan, coder, sheets, frozen, kept, CHECK_FILES, pending)
    listing, places = unlocated_listing(plan, coder, prim_rows, by_uid, pending, load_checks(CHECK_FILES[0]))
    if '--pending' in argv or pending:
        for p in pending:
            print(json.dumps(dict(record_id=p[0], code=p[1], raw=p[2], text=p[3]), ensure_ascii=False))
        if pending:
            raise SystemExit(f'{len(pending)} hand checks pending')
        return

    groups = {g['report_group']: g for g in V.read(os.path.join(MERGED12, 'report_groups.csv'))}
    sites = {s['site_id']: s for s in V.read(os.path.join(MERGED12, 'sites.csv'))}
    for u in units + others:
        r = by_uid[u['record_id'][4:]]
        u['phase'] = r['phase']
        u['report_id'] = r['report_id']
        u['pages'] = r['pages']
        u['new_row'] = 'yes' if p4(r) else 'no'
        u['new_report'] = 'yes' if all(x.startswith('4') for x in groups[r['report_group']]['phases'].split(';')) else 'no'
        u['new_site'] = 'yes' if not sites[r['site_id']]['phase13_sites'] else 'no'
        if p4(r):
            u['exposure'] = EXPOSURE4 + ('; exposed by name and dating in the merge README' if r['report_id'] in EXPOSED_BY_NAME else '')
    for i, u in enumerate(sorted(units + others, key=lambda x: (x['kind'], x['record_id']))):
        u['unit_id'] = f"P{i + 1:04d}"

    def val(u, c, sens):
        return B.clause_value(plan, u, c, sens)

    located_frozen = [u for u in frozen if u['lat'] is not None]
    kept_frozen = [u for u in located_frozen if u['source'] != 'HAESI']
    base = [u for u in kept_frozen if not u['possible_duplicate_of']]
    views = {
        'frozen_all_lineages': [u for u in located_frozen if not u['possible_duplicate_of']],
        'iaa11_union': base + [u for u in u11 if not u['possible_duplicate_of']],
        'union_all_lineages': base + [u for u in units if not u['possible_duplicate_of']],
        'lineage_IAA': units,
        'union_all_lineages+other_classes': base + [u for u in units + others if not u['possible_duplicate_of']],
    }
    committed = {(r['branch'], r['region'], r['date_set']): r for r in V.read(os.path.join(FOLDER, 'scores_summary.csv'))
                 if r['view'] == 'all_lineages'}
    committed11 = {(r['branch'], r['region'], r['date_set']): r for r in V.read(os.path.join(FOLDER, 'iaa_view_2026-10-11.csv'))}
    out, score_rows = [], []
    for b, spec in plan['branches'].items():
        if not spec['clauses']:
            continue
        for u in sorted(units + others, key=lambda x: x['unit_id']):
            vs = [val(u, c, False) for c in spec['clauses']]
            score_rows.append(dict(unit_id=u['unit_id'], record_id=u['record_id'], kind=u['kind'], phase=u['phase'],
                                   branch=b, values=';'.join(vs), result=B.overall(vs),
                                   result_sensitivity=B.overall([val(u, c, True) for c in spec['clauses']]),
                                   possible_duplicate_of=u['possible_duplicate_of']))
        for reg in V.REGIONS:
            for ds in plan['date_sets']:
                t = {v: V.tally(plan, [u for u in us if V.in_region(u, reg) and V.in_dateset(u, ds)], spec['clauses'], val)
                     for v, us in views.items()}
                f, e, un, li, uo = (t['frozen_all_lineages'], t['iaa11_union'], t['union_all_lineages'], t['lineage_IAA'],
                                    t['union_all_lineages+other_classes'])
                c, c11 = committed[(b, reg, ds)], committed11[(b, reg, ds)]
                if [f['N'], f['k'], f['f'], f['m'], f['cc'], sorted(f['matches'])] != \
                        [int(c['N']), int(c['k_match']), int(c['f_fail']), int(c['m_unknown']), c['clause_counts'],
                         sorted(filter(None, c['matches'].split(';')))]:
                    raise SystemExit(f'frozen scoring does not reproduce scores_summary.csv: {b} {reg} {ds}')
                e_new = [x for x in e['matches'] if x.startswith('IAA ')]
                if [e['N'], e['k'], e['f'], e['m'], e['cc'], ';'.join(e_new)] != \
                        [int(c11['union_N']), int(c11['union_k']), int(c11['union_f']), int(c11['union_m']),
                         c11['union_clause_counts'], c11['new_matches']]:
                    raise SystemExit(f'the 11 October view does not reproduce iaa_view_2026-10-11.csv: {b} {reg} {ds}')
                un_iaa = [x for x in un['matches'] if x.startswith('IAA ')]
                out.append(dict(branch=b, headline='yes' if spec['headline'] == reg else '', region=reg, date_set=ds,
                                frozen_N=f['N'], frozen_k=f['k'], frozen_f=f['f'], frozen_m=f['m'],
                                iaa11_N=e['N'], iaa11_k=e['k'], iaa11_f=e['f'], iaa11_m=e['m'],
                                union_N=un['N'], union_k=un['k'], union_f=un['f'], union_m=un['m'],
                                delta11_N=un['N'] - e['N'], delta11_k=un['k'] - e['k'], delta11_f=un['f'] - e['f'],
                                delta11_m=un['m'] - e['m'], delta_frozen_N=un['N'] - f['N'], delta_frozen_k=un['k'] - f['k'],
                                union_k_sens=un['ks'], iaa_N=li['N'], iaa_k=li['k'], iaa_f=li['f'], iaa_m=li['m'],
                                other_classes_N=uo['N'], other_classes_k=uo['k'], other_classes_f=uo['f'],
                                other_classes_m=uo['m'], union_clause_counts=un['cc'],
                                union_iaa_matches=';'.join(un_iaa),
                                new_matches_vs_11oct=';'.join(x for x in un_iaa if x not in e_new),
                                lost_matches_vs_11oct=';'.join(x for x in e_new if x not in un_iaa),
                                iaa_matches=';'.join(li['matches'])))
    # Amendment 1 (exploratory) with the phase 1-4 units
    a1 = {r['unit_id']: r for r in V.read(os.path.join(FOLDER, 'amendment1_codes.csv'))}
    for u in located_frozen:
        r = a1[u['unit_id']]
        u['F7wa'], u['F2xa'] = r['F7wa'], r['F2xa']

    def val1(u, c, sens):
        return u[c] if c in ('F7wa', 'F2xa') else B.clause_value(plan, u, c, sens)
    a1_11 = {(r['branch'], r['region'], r['date_set']): r for r in V.read(os.path.join(FOLDER, 'iaa_amendment1_view.csv'))}
    out1 = []
    for b, cl in list(A1.BRANCHES.items()) + [('ALL-TOMBS', [])]:
        for reg in ('A', 'A3', 'B', 'AB'):
            for ds in plan['date_sets']:
                e = V.tally(plan, [u for u in views['iaa11_union'] if V.in_region(u, reg) and V.in_dateset(u, ds)], cl, val1)
                un = V.tally(plan, [u for u in views['union_all_lineages'] if V.in_region(u, reg) and V.in_dateset(u, ds)], cl, val1)
                c = a1_11[(b, reg, ds)]
                if [e['N'], e['k'], e['f'], e['m']] != [int(c['a1_iaa_N']), int(c['a1_iaa_k']), int(c['a1_iaa_f']), int(c['a1_iaa_m'])]:
                    raise SystemExit(f'the 11 October amendment-1 view does not reproduce: {b} {reg} {ds}')
                e_new = [x for x in e['matches'] if x.startswith('IAA ')]
                out1.append(dict(branch=b, region=reg, date_set=ds, a1_N=c['a1_N'], a1_k=c['a1_k'], a1_f=c['a1_f'], a1_m=c['a1_m'],
                                 a1_iaa11_N=e['N'], a1_iaa11_k=e['k'], a1_iaa11_f=e['f'], a1_iaa11_m=e['m'],
                                 a1_p4_N=un['N'], a1_p4_k=un['k'], a1_p4_f=un['f'], a1_p4_m=un['m'],
                                 new_matches_vs_11oct=';'.join(x for x in un['matches'] if x.startswith('IAA ') and x not in e_new)
                                 if cl else '(N only)'))
    ucols = ['unit_id', 'kind', 'phase', 'new_row', 'new_report', 'new_site', 'source', 'record_id', 'report_id', 'pages',
             'locator', 'name', 'lat', 'lon', 'unc', 'd_temple_km', 'd_jericho_km', 'd_road_km', 'in_A', 'in_A3', 'in_B1',
             'in_B2', 'in_B2_5', 'in_asi_sheet', 'possible_duplicate_of', 'report_group', 'site_id', 'multi_tomb_record',
             'tomb_terms', 'F1', 'F2', 'F2x', 'F3', 'F4', 'F5', 'F6', 'F7', 'F7w', 'F10', 'F11', 'F12', 'F13', 'F14', 'F16',
             'F17', 'F19', 'F20_communal', 'F21', 'name_zadok', 'name_absalom', 'name_queen', 'name_obed', 'name_jericho',
             'period_terms', 'dated_in_window', 'dated_lenient', 'manual_rejected', 'F7a', 'F7wa', 'F2xa', 'a1_rejected',
             'tier1_related', 'exposure', 'text_hash']
    rows_out = []
    for u in sorted(units + others, key=lambda x: x['unit_id']):
        r = {k: u.get(k, '') for k in ucols}
        for k in ('lat', 'lon'):
            r[k] = f"{u[k]:.6f}"
        for k in ('d_temple_km', 'd_jericho_km', 'd_road_km'):
            r[k] = f"{u[k]:.3f}"
        for k in ('in_A', 'in_A3', 'in_B1', 'in_B2', 'in_B2_5'):
            r[k] = 'yes' if u[k] else 'no'
        rows_out.append(r)
    V.write(os.path.join(FOLDER, 'phase4_units.csv'), ucols, rows_out)
    V.write(os.path.join(FOLDER, 'phase4_scores.csv'), list(score_rows[0]), score_rows)
    V.write(os.path.join(FOLDER, 'phase4_view_2026-10-12.csv'), list(out[0]), out)
    V.write(os.path.join(FOLDER, 'phase4_amendment1_view.csv'), list(out1[0]), out1)

    nd = [u for u in units if not u['possible_duplicate_of']]
    ids11 = {u['record_id'] for u in u11}
    ids11_nd = {u['record_id'] for u in u11 if not u['possible_duplicate_of']}
    ids12 = {u['record_id'] for u in units}

    def levels(us):
        return {lvl: {reg: {ds: sum(1 for u in us if u[lvl] == 'yes' and V.in_region(u, reg) and V.in_dateset(u, ds))
                            for ds in plan['date_sets']} for reg in ('A', 'B', 'AB')}
                for lvl in ('new_row', 'new_report', 'new_site')}

    codes = ['F1', 'F2', 'F2x', 'F3', 'F4', 'F5', 'F6', 'F7w', 'F7wa', 'F2xa', 'F10', 'F11', 'F12', 'F13', 'F14', 'F16',
             'F17', 'F19', 'F21', 'name_zadok', 'name_absalom', 'name_queen', 'name_obed', 'name_jericho']
    new_nd = [u for u in nd if u['new_row'] == 'yes']
    summary = dict(
        note='Exploratory view (PLAN_AMENDMENT_PHASE4_2026-10-12.md). The frozen tables and the 11 October view files are unchanged.',
        inputs=INPUT_SHA,
        excluded_rows={uid: why for uid, why in sorted(excl.items())},
        excluded_by_reason=dict(Counter(w for v in excl.values() for w in v.split('; '))),
        excluded_tomb_rows=sum(1 for uid in excl if by_uid[uid]['feature_type'] == V.CLASS),
        units=dict(primary=len(units), primary_not_duplicate=len(nd),
                   primary_not_duplicate_distinct_sites=len({u['site_id'] for u in nd}),
                   primary_from_phase4_rows=sum(1 for u in units if u['new_row'] == 'yes'),
                   primary_from_phase4_rows_not_duplicate=len(new_nd),
                   other_class=len(others), other_class_not_duplicate=sum(1 for u in others if not u['possible_duplicate_of'])),
        change_vs_11oct=dict(units_11oct=len(u11), units_now=len(units),
                             phase13_units_dropped=sorted(ids11 - ids12),
                             phase13_units_added=sorted(x for x in ids12 - ids11 if by_uid[x[4:]]['phase'][0] != '4'),
                             dating_changed=sorted(u['record_id'] for u in units if u['record_id'] in ids11 and
                                                   u['dated_in_window'] != {v['record_id']: v for v in u11}[u['record_id']]['dated_in_window']),
                             not_duplicate_11oct=len(ids11_nd), not_duplicate_now=len(nd)),
        not_duplicate_by_region={reg: sum(1 for u in nd if V.in_region(u, reg)) for reg in V.REGIONS},
        strict_not_duplicate_by_region={reg: sum(1 for u in nd if V.in_region(u, reg) and u['dated_in_window'] == 'yes')
                                        for reg in V.REGIONS},
        new_levels_not_duplicate=levels(nd),
        new_levels_all=levels(units),
        new_row_units_not_duplicate_codes={reg: {ds: {c: sum(1 for u in new_nd if V.in_region(u, reg) and V.in_dateset(u, ds)
                                                             and u.get(c) == 'yes') for c in codes}
                                                  for ds in plan['date_sets']} for reg in ('A', 'B')},
        phase4_duplicates_of=sorted({u['possible_duplicate_of'] for u in units if u['new_row'] == 'yes' and u['possible_duplicate_of']}),
        coverage_primary=dict(sorted(cov.items())), coverage_other_class=dict(sorted(cov_o.items())),
        unlocated_phase4_tomb_rows_by_zone_and_reader_place={f'{z} | {p}': n for (z, p), n in sorted(places.items())},
        unlocated_phase4_listing=listing,
        tier1_units=[u['record_id'] for u in units + others if u['tier1_related'] == 'yes'])
    with open(os.path.join(FOLDER, 'phase4_summary.json'), 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    print(json.dumps(summary['units']), json.dumps(summary['not_duplicate_by_region']))
    for r in out:
        if r['headline'] and r['date_set'] == 'strict':
            print(r['branch'], r['region'], 'frozen', r['frozen_k'], r['frozen_f'], r['frozen_m'], r['frozen_N'],
                  '| 11oct', r['iaa11_k'], r['iaa11_f'], r['iaa11_m'], r['iaa11_N'],
                  '| now', r['union_k'], r['union_f'], r['union_m'], r['union_N'], '|', r['new_matches_vs_11oct'])


if __name__ == '__main__':
    main(sys.argv[1:])
