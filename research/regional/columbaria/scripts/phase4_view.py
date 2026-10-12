#!/usr/bin/env python3
"""Exploratory view: the merged phase 1-4 inventory folded into the columbaria lane
(PLAN_AMENDMENT_PHASE4_2026-10-12.md, which applies PLAN_AMENDMENT_IAA_2026-10-11.md unchanged to the new input).

Run from the repository root:  python3 -I research/regional/columbaria/scripts/phase4_view.py [--list | --pairs]
Reads the committed columbaria.csv, summary.json and iaa_view_2026-10-11.csv; the merged inventory
research/regional/haesi_features/merged_2026-10-12/; the hand coding data/iaa_coding.json (phases 1-3) and
data/phase4_coding.json (phase 4); the duplicate decisions data/iaa_dedup_decisions.csv and
data/phase4_dedup_decisions.csv. Scores with score.py (unchanged) and reuses iaa_view.py's helpers.
Writes phase4_rows.csv, phase4_excluded.csv, phase4_scores.csv, phase4_summary.json and phase4_view_2026-10-12.csv;
never writes columbaria.csv, scores.csv, summary.json or any iaa_* file.
--list prints the in-region phase-4 rows (coding fields) for the hand coder; --pairs prints candidate pairs.
Standard library only.
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colcommon as C  # noqa: E402
import score as SC  # noqa: E402  (frozen scoring, unchanged)
import iaa_view as IV  # noqa: E402  (helpers of the IAA view, unchanged)
from assemble import COLUMNS  # noqa: E402

FOLDER = C.FOLDER
HF = os.path.join(C.REPO, 'research', 'regional', 'haesi_features')
MERGED = os.path.join(HF, 'merged_2026-10-12')
PHASE4 = os.path.join(HF, 'phase4_2026-10-11')
INPUT_SHA = {  # PLAN_AMENDMENT_PHASE4 §2
    'features_all.csv': '940e6c04b1ecd18c79a7c88a784a463d69056f70c6e31ad18e5a18c46866d65d',
    'report_groups.csv': '38b67f3c7095993287ac9da80eb229a9752d56ff7c27cb9bb3b1024f47da702f',
    'sites.csv': '5d7458016d7955cced5540d4307570879fbc5b2071d5f644e85d3cec0fcc16db',
}
PLACES_SHA = '315474bd3be8cce3e1776e119417e2444edd99e3f028c7413185302fc7663683'
VIEW_NAME = 'phase4_view_2026-10-12.csv'
OUTPUTS = ['phase4_rows.csv', 'phase4_excluded.csv', 'phase4_scores.csv', 'phase4_summary.json', VIEW_NAME]
ALMIT = re.compile(r'almit|עלמית', re.I)
SULTAN = re.compile(r'sultan', re.I)
VIEW_FIELDS = ['scope', 'kind', 'key', 'frozen_N', 'frozen_k', 'frozen_f', 'frozen_m',
               'iaa1011_N', 'iaa1011_k', 'iaa1011_f', 'iaa1011_m',
               'inv_N', 'inv_k', 'inv_f', 'inv_m', 'union_N', 'union_k', 'union_f', 'union_m',
               'delta_vs_frozen_N', 'delta_vs_frozen_k', 'delta_vs_frozen_f', 'delta_vs_frozen_m',
               'delta_vs_iaa1011_N', 'delta_vs_iaa1011_k', 'delta_vs_iaa1011_f', 'delta_vs_iaa1011_m',
               'nodedup_N', 'nodedup_k', 'nodedup_f', 'nodedup_m', 'dedup300_N', 'dedup300_k', 'dedup300_f',
               'dedup300_m', 'wordscreen_N', 'wordscreen_k', 'wordscreen_f', 'wordscreen_m',
               'new_phase4_matches']


def is_p4(r):
    return r['phase'].startswith('4')


def held_ids():
    ids = set()
    for path in glob.glob(os.path.join(PHASE4, '**', 'held*.csv'), recursive=True):
        for r in IV.read(path):
            ids.add(r['unit_id'].strip())
    return ids


def protected(r, held):
    """PLAN_AMENDMENT_PHASE4 §6. Returns a reason or ''."""
    text = ' '.join((r['site_name'], r['feature_subtype'], r['quote']))
    if r['report_id'] in held:
        return 'held unit (phase-4 held.csv): excluded, not read for this lane'
    if r['protected_strip'] == 'yes' or SULTAN.search(text):
        return 'Tell es-Sultan north strip: excluded'
    if ALMIT.search(text):
        return 'Kh. ʿAlmit: excluded, not compared with any model'
    return ''


def inputs():
    for name, h in INPUT_SHA.items():
        if IV.sha(os.path.join(MERGED, name)) != h:
            raise SystemExit(f'{name}: hash differs from the amendment value')
    if IV.sha(IV.PLACES) != PLACES_SHA:
        raise SystemExit('places_v2.csv: hash differs')
    feats = IV.read(os.path.join(MERGED, 'features_all.csv'))
    groups = {g['report_group']: g for g in IV.read(os.path.join(MERGED, 'report_groups.csv'))}
    sites = {s['site_id']: s for s in IV.read(os.path.join(MERGED, 'sites.csv'))}
    places = {r['place_id']: r for r in IV.read(IV.PLACES)}
    return feats, groups, sites, places


def load_coding():
    with open(os.path.join(FOLDER, 'data', 'iaa_coding.json'), encoding='utf-8') as f:
        c13 = json.load(f)['rows']
    path = os.path.join(FOLDER, 'data', 'phase4_coding.json')
    c4 = {}
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            c4 = json.load(f)['rows']
    return c13, c4


def build(listing=False):
    feats, groups, sites, places = inputs()
    held = held_ids()
    c13, c4 = load_coding()
    prim, screen = IV.select(feats)
    rows, excluded, todo = [], [], []
    unplaced, outside = Counter(), Counter()
    used13, used4 = set(), set()
    site_pos = {}

    def base(r, status, reason):
        return dict(row_uid=r['row_uid'], phase=r['phase'], report_id=r['report_id'], report_group=r['report_group'],
                    site_id=r['site_id'], site_name=r['site_name'], feature_type=r['feature_type'], status=status,
                    reason=reason)

    # not-counted rows of the class, or with a columbarium word, in phase 4 (amendment §3)
    for r in feats:
        if is_p4(r) and r['counted'] != 'yes' and (r['feature_type'] == IV.CLASS or
                                                   C.find_columbarium(r['feature_subtype'] + ' ' + r['quote'])):
            excluded.append(base(r, 'not counted', f"counted = no in the merged inventory ({r['not_counted_reason']})"))
    selected = {r['row_uid'] for r in prim}
    for r in feats:  # version rule (amendment §3): rows of the class not used, phase 4, or used in the IAA view
        if r['counted'] == 'yes' and r['feature_type'] == IV.CLASS and r['row_uid'] not in selected and \
                (is_p4(r) or r['row_uid'] in c13):
            excluded.append(base(r, 'alternate version: not used',
                                 f"version rule: the preferred version ({groups[r['report_group']]['preferred_report_id']}) "
                                 f"of report group {r['report_group']} gives a columbarium row"))
    for r in prim:
        p4 = is_p4(r)
        prot = protected(r, held) if p4 else ''
        if prot:
            if prot.startswith('held'):
                raise SystemExit(f'held unit has a feature row in the class: {r["row_uid"]}')
            excluded.append(base(r, 'protected', prot))
            continue
        pos = IV.position(r, places)
        if pos is None:
            unplaced['phase4' if p4 else 'phase1-3'] += 1
            s = sites.get(r['site_id'], {})
            note = ''
            if s.get('located') == 'yes' and s.get('lat') and float(s.get('spread_m') or 0) <= 2000:
                la, lo = float(s['lat']), float(s['lon'])
                site_pos[r['row_uid']] = dict(site_id=r['site_id'], lat=la, lon=lo, in_region=C.in_region(lo, la),
                                              N1_km=round(C.km(la, lo, *SC.N1), 2), N2_km=round(C.km(la, lo, *SC.N2), 2),
                                              south_of_SA=la < SC.LAT_SA)
                note = f" (merged site {r['site_id']} position, reported only: {site_pos[r['row_uid']]})"
            excluded.append(base(r, 'unplaced', 'no coordinates and no reader place within 2 km (PLAN §3)' + note))
            continue
        lat, lon, prec, basis = pos
        if not C.in_region(lon, lat):
            outside['phase4' if p4 else 'phase1-3'] += 1
            continue
        if not C.find_columbarium(r['feature_subtype'] + ' ' + r['quote'] + ' ' + r['site_name']):
            excluded.append(base(r, 'not admitted', 'no frozen columbarium word in the coding (PLAN §5)'))
            continue
        coding, used = (c4, used4) if p4 else (c13, used13)
        c = coding.get(r['row_uid'])
        if c is None:
            todo.append(r)
            continue
        used.add(r['row_uid'])
        if c.get('exclude'):
            excluded.append(base(r, 'excluded', c['exclude']))
            continue
        row = IV.make_row(r, c, lat, lon, prec, basis)
        if p4:
            row.update(id=f"P4-{r['row_uid']}", source='P4',
                       read_via=f"merged phase 1-4 inventory row {r['row_uid']} (coding fields only)")
        row['_phase'] = r['phase']
        row['_site_id'] = r['site_id']
        rows.append(row)
    # word screen (amendment §3)
    ws_rows = []
    for r in screen:
        if r['_group_has_columbarium_row']:
            excluded.append(base(r, 'word screen: not added', 'its report group already gives a columbarium_dovecote row'))
            continue
        if not is_p4(r):
            raise SystemExit(f'phase 1-3 word-screen candidate not in the IAA view: {r["row_uid"]}')
        prot = protected(r, held)
        pos = IV.position(r, places)
        if prot or pos is None or not C.in_region(pos[1], pos[0]):
            excluded.append(base(r, 'word screen: not scored', prot or ('unplaced' if pos is None else 'outside region')))
            continue
        c = c4.get(r['row_uid'])
        if c is None:
            todo.append(r)
            continue
        used4.add(r['row_uid'])
        if c.get('exclude'):
            excluded.append(base(r, 'word screen: excluded', c['exclude']))
            continue
        row = IV.make_row(r, c, *pos)
        row.update(id=f"P4WS-{r['row_uid']}", source='P4',
                   read_via=f"merged phase 1-4 inventory row {r['row_uid']} (word screen, coding fields only)")
        row['_phase'], row['_site_id'] = r['phase'], r['site_id']
        ws_rows.append(row)
    if listing:
        return todo, feats
    if todo:
        raise SystemExit(f'{len(todo)} in-region rows without hand coding; run with --list')
    stale = sorted(set(c4) - used4)
    if stale:
        raise SystemExit(f'phase-4 coding for rows not in the view: {stale}')
    dropped13 = sorted(set(c13) - used13)  # IAA-view rows no longer used (version rule on the new groups)
    cov = dict(unplaced=dict(unplaced), outside_region=dict(outside), iaa_view_rows_no_longer_selected=dropped13,
               unplaced_site_positions_reported_only=site_pos)
    return rows, ws_rows, excluded, cov, groups, sites


def decisions():
    out = {}
    for name in ('iaa_dedup_decisions.csv', 'phase4_dedup_decisions.csv'):
        path = os.path.join(FOLDER, 'data', name)
        if os.path.exists(path):
            for d in IV.read(path):
                out[(d['iaa_id'], d['other_id'])] = dict(d, _file=name)
    return out


def apply_dedup(rows, lane, mode, dec):
    pairs = IV.pair_list(rows, lane)
    missing = [p for p in pairs if (p['iaa_id'], p['other_id']) not in dec]
    if missing:
        raise SystemExit(f'{len(missing)} candidate pairs without a decision; run with --pairs')
    out = [dict(r, dup_of='') for r in rows]
    by = {r['id']: r for r in out}
    if mode == 'none':
        return out, pairs
    for p in pairs:
        same = dec[(p['iaa_id'], p['other_id'])]['decision'] == 'same' if mode == 'decided' else p['km'] <= IV.DUP_KM
        if not same:
            continue
        a = by[p['iaa_id']]
        if p['other_kind'] == 'lane':
            a['dup_of'] = a['dup_of'] or p['other_id']
        else:
            b = by[p['other_id']]
            keep, drop = sorted((a, b), key=lambda x: (-sum(x[k] not in ('U', '') for k in ('lev2', 'lev3', 'access', 'date_code')),
                                                       x['source_ref']))
            if not drop['dup_of'] and not keep['dup_of']:
                drop['dup_of'] = keep['id']
    return out, pairs


def zero():
    return dict(N=0, k_match=0, f_fail=0, m_unknown=0)


def levels(rows, groups, sites):
    """New at row, report and site level (amendment §8): counted phase-4 rows, their groups and sites."""
    p4 = [r for r in rows if r['_phase'].startswith('4') and not r['dup_of']]
    gids = sorted({r['_report_group'] for r in p4})
    sids = sorted({r['_site_id'] for r in p4 if r['_site_id']})
    return dict(
        rows=sorted(r['id'] for r in p4),
        report_groups={g: ('shared with phases 1-3' if groups[g]['phase13_groups'] else 'phase 4 only') for g in gids},
        sites={s: ('shared with phases 1-3' if sites[s]['phase13_sites'] else 'phase 4 only') for s in sids})


def main(argv):
    if '--list' in argv:
        todo, _ = build(listing=True)
        for r in todo:
            print(json.dumps({k: r[k] for k in ('row_uid', 'phase', 'report_id', 'series', 'volume', 'year', 'pages',
                                                'author', 'site_name', 'feature_type', 'feature_subtype', 'n_features',
                                                'period_as_given', 'quote', 'lat', 'lon', 'precision_m',
                                                'coordinate_source', 'report_group', 'site_id', 'version_role', 'url')},
                             ensure_ascii=False))
        return
    rows, ws_rows, excluded, cov, groups, sites = build()
    lane = IV.lane_counted()
    dec = decisions()
    if '--pairs' in argv:
        for p in IV.pair_list(rows, lane):
            if (p['iaa_id'], p['other_id']) not in dec:
                print(json.dumps(p, ensure_ascii=False))
        return
    views, pair_sets = {}, {}
    for m in ('decided', 'none', 'all300'):
        views[m], pair_sets[m] = apply_dedup(rows, lane, m, dec)
    listed = {(p['iaa_id'], p['other_id']) for p in pair_sets['decided']}
    unused_p4 = sorted(k for k, d in dec.items() if d['_file'] == 'phase4_dedup_decisions.csv' and k not in listed)
    if unused_p4:
        raise SystemExit(f'phase-4 decisions for pairs that are not listed: {unused_p4}')
    unused_iaa = sorted('|'.join(k) for k, d in dec.items() if d['_file'] == 'iaa_dedup_decisions.csv' and k not in listed)
    lane_all = IV.read(os.path.join(FOLDER, 'columbaria.csv'))
    committed = json.load(open(os.path.join(FOLDER, 'summary.json'), encoding='utf-8'))
    iaa_view = {(r['scope'], r['kind'], r['key']): r for r in IV.read(os.path.join(FOLDER, 'iaa_view_2026-10-11.csv'))}
    decided_counted = IV.counted(views['decided'])
    ws_counted = [dict(r, dup_of='') for r in ws_rows]
    out_view, score_rows = [], []
    summary = {'_note': 'Exploratory view (PLAN_AMENDMENT_PHASE4_2026-10-12.md); summary.json and the iaa_* files are '
                        'unchanged.', 'inputs': INPUT_SHA, 'coverage': cov, 'scopes': {},
               'iaa_decisions_not_listed_now': unused_iaa, 'new_at_three_levels': levels(views['decided'], groups, sites)}
    for scope in ('frozen', 'all'):
        frozen = SC.scoped(lane_all, scope)
        fz = IV.score_set(frozen)
        fcl, fco = IV.tallies(fz)
        cs = committed['scopes'][scope]
        if any(fco[k] != v for k, v in cs['headline'].items()) or fcl != cs['clauses']:
            raise SystemExit(f'the frozen scoring does not reproduce summary.json ({scope})')
        res = {}
        for mode, vrows in views.items():
            iz = IV.score_set(IV.counted(vrows))
            res[mode] = (iz, IV.tallies(iz), IV.tallies(fz + iz))
        iz, (icl, ico), (ucl, uco) = res['decided']
        wz = IV.score_set(ws_counted)
        wcl, wco = IV.tallies(fz + iz + wz)
        for r, s, c in iz:
            score_rows.append(dict(scope=scope, id=r['id'], name=r['name'], phase=r['_phase'], **s, **c))
        for r, s, c in wz:
            score_rows.append(dict(scope=scope, id=r['id'], name=r['name'], phase=r['_phase'], **s, **c))
        for kind, f_t, i_t, u_t, nd_t, d3_t, w_t in (
                ('headline', fco, ico, uco, res['none'][2][1], res['all300'][2][1], wco),
                ('clause', fcl, icl, ucl, res['none'][2][0], res['all300'][2][0], wcl)):
            keys = SC.HEADLINE if kind == 'headline' else SC.CLAUSES
            for k in keys:
                f, u = f_t[k], u_t[k]
                i = i_t.get(k, zero())
                a = iaa_view[(scope, kind, k)]
                a = dict(N=int(a['union_N']), k_match=int(a['union_k']), f_fail=int(a['union_f']), m_unknown=int(a['union_m']))
                if a['N'] != f['N'] + int(iaa_view[(scope, kind, k)]['iaa_N']):
                    raise SystemExit('iaa_view_2026-10-11.csv is inconsistent')
                new = sorted(r['id'] for r, s, c in iz if r['id'].startswith('P4-') and
                             (c.get(k) if kind == 'headline' else s.get(k)) == 'M')
                row = dict(scope=scope, kind=kind, key=k, new_phase4_matches=';'.join(new))
                for tag, t in (('frozen', f), ('iaa1011', a), ('inv', i), ('union', u), ('nodedup', nd_t[k]),
                               ('dedup300', d3_t[k]), ('wordscreen', w_t[k])):
                    row.update({f'{tag}_N': t['N'], f'{tag}_k': t['k_match'], f'{tag}_f': t['f_fail'],
                                f'{tag}_m': t['m_unknown']})
                for tag, t in (('frozen', f), ('iaa1011', a)):
                    row.update({f'delta_vs_{tag}_N': u['N'] - t['N'], f'delta_vs_{tag}_k': u['k_match'] - t['k_match'],
                                f'delta_vs_{tag}_f': u['f_fail'] - t['f_fail'],
                                f'delta_vs_{tag}_m': u['m_unknown'] - t['m_unknown']})
                out_view.append(row)
        summary['scopes'][scope] = dict(
            inventory_rows_counted=len(decided_counted),
            phase4_rows_counted=sum(1 for r in decided_counted if r['_phase'].startswith('4')),
            phase13_rows_counted=sum(1 for r in decided_counted if not r['_phase'].startswith('4')),
            inventory_rows_dup_of_lane=sum(1 for r in views['decided'] if r['dup_of'] and
                                           not r['dup_of'].startswith(('IAA-', 'P4-'))),
            inventory_rows_dup_of_inventory=sum(1 for r in views['decided'] if r['dup_of'].startswith(('IAA-', 'P4-'))),
            phase4_rows_in_view=sorted(r['id'] for r in views['decided'] if r['_phase'].startswith('4')),
            union_rows_counted=len(frozen) + len(decided_counted),
            union_headline={k: uco[k] for k in SC.HEADLINE}, union_clauses=ucl,
            wordscreen_rows=len(ws_counted),
            bracket_rows_counted=dict(no_dedup=len(IV.counted(views['none'])),
                                      dedup_300m=len(IV.counted(views['all300']))))
    for r in views['decided'] + ws_counted:
        r['phase'] = r.pop('_phase')
        r.pop('_site_id')
    IV.write(os.path.join(FOLDER, 'phase4_rows.csv'), ['phase'] + COLUMNS, views['decided'] + ws_counted)
    IV.write(os.path.join(FOLDER, 'phase4_excluded.csv'), ['row_uid', 'phase', 'report_id', 'report_group', 'site_id',
                                                           'site_name', 'feature_type', 'status', 'reason'],
             sorted(excluded, key=lambda x: (x['status'], x['row_uid'])))
    IV.write(os.path.join(FOLDER, 'phase4_scores.csv'), list(score_rows[0].keys()), score_rows)
    IV.write(os.path.join(FOLDER, VIEW_NAME), VIEW_FIELDS, out_view)
    with open(os.path.join(FOLDER, 'phase4_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write('\n')
    s = summary['scopes']['frozen']
    print(f"inventory rows counted {s['inventory_rows_counted']} (phase 4: {s['phase4_rows_counted']}); union "
          f"{s['union_rows_counted']}; word screen {s['wordscreen_rows']}")
    for r in out_view:
        if r['scope'] == 'frozen' and r['kind'] == 'headline':
            print(r['key'], 'frozen', r['frozen_k'], r['frozen_f'], r['frozen_m'], r['frozen_N'], '| iaa1011',
                  r['iaa1011_k'], r['iaa1011_f'], r['iaa1011_m'], r['iaa1011_N'], '| union',
                  r['union_k'], r['union_f'], r['union_m'], r['union_N'], r['new_phase4_matches'])


if __name__ == '__main__':
    main(sys.argv[1:])
