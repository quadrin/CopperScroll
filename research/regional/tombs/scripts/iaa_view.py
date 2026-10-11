#!/usr/bin/env python3
"""Exploratory view: the merged IAA inventory folded into the tombs lane (PLAN_AMENDMENT_IAA_2026-10-11.md).

Run from the repository root:  python3 -I -B research/regional/tombs/scripts/iaa_view.py [--pending]
Reads the committed tombs.csv, scores_summary.csv, amendment1_codes.csv, amendment1_scores_summary.csv and
data/asi_selected_maps.json, the merged IAA inventory (research/regional/haesi_features/merged_2026-10-11/) and the
hand checks data/manual_check_iaa.csv and data/manual_check_iaa_amendment1.csv. Codes the IAA rows with the frozen
Coder and scores every branch with the frozen clause_value and overall (build_tombs.py, imported unchanged).
No ASI cache or WBADB file is needed. Writes iaa_units.csv, iaa_scores.csv, iaa_view_2026-10-11.csv,
iaa_amendment1_view.csv and iaa_summary.json; never writes the frozen outputs. --pending lists the hand checks
still needed and stops.
"""
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tombs_common as T  # noqa: E402
import build_tombs as B  # noqa: E402  (frozen Coder, clause_value, overall; unchanged)
import amendment1 as A1  # noqa: E402  (exploratory amendment 1 rules; unchanged)

FOLDER = T.FOLDER
DATA = os.path.join(FOLDER, 'data')
MERGED = os.path.join(T.REPO, 'research', 'regional', 'haesi_features', 'merged_2026-10-11')
INPUT_SHA = {  # PLAN_AMENDMENT_IAA §2
    'features_all.csv': '2170f7fb15b097621e07648c128719f25e50e3550d5ec8756c08fca6267e455b',
    'report_groups.csv': '06085467541339b097fcd29a55a5d7e8d49ade829b7f8329a00f981e9624b89c',
    'sites.csv': '7e89ddce959869e8a960103e63417870d621edb5f7f1b0376b3d12f54450e87b',
}
CLASS = 'tomb_burial_cave'
REN = {'monument_F1': 'F1', 'porch_F2': 'F2', 'exedra_pillar_F2x': 'F2x', 'inside_pillar_F3': 'F3',
       'chambers_F10': 'F10', 'inscription_F4': 'F4', 'named_inscription_F5': 'F5', 'setting_wadi_F19': 'F19',
       'garden_ancient_F6': 'F6', 'entrance_orientation_F7': 'F7', 'west_facing_F7w': 'F7w',
       'kokhim_F11': 'F11', 'ossuaries_F12': 'F12', 'repository_F13': 'F13', 'slab_F14': 'F14',
       'cistern_F16': 'F16', 'channel_F17': 'F17', 'communal_F20': 'F20_communal', 'unused_F21': 'F21'}
MULTI = (r'(?<![\w])(two|three|four|five|six|seven|eight|nine|ten|several|many|\d+)\s+(?:[\w\-]+\s+){0,2}?'
         r'(burial caves|tombs|graves|caves|kokhim tombs)(?![\w])', r'(?<![\w])(cemetery|necropolis|burial caves|tombs|graves)(?![\w])')
REGIONS = ['A', 'A3', 'B', 'B1', 'B2', 'B2_5', 'AB']
EXPOSURE = 'repo-coded by the merged IAA inventory (phases 1-3); first mapped by this lane on 11 Oct 2026, after the IAA amendment (c14468e)'


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def yn(v):
    return v == 'yes'


def fnum(v):
    return float(v) if v not in ('', None) else None


# ---------------------------------------------------------------- frozen units from the committed tombs.csv
def frozen_units():
    out = []
    for r in read(os.path.join(FOLDER, 'tombs.csv')):
        u = {REN.get(k, k): v for k, v in r.items()}
        u['lat'], u['lon'] = fnum(r['lat']), fnum(r['lon'])
        u['unc'] = float(r['position_uncertainty_km'])
        for k in ('d_temple_km', 'd_jericho_km', 'd_road_km'):
            u[k] = fnum(r[k])
        for k in ('in_A', 'in_A3', 'in_B1', 'in_B2', 'in_B2_5'):
            u[k] = yn(r[k]) if r[k] else None
        u['is_primary'] = r['source'] == 'ASI' or (r['source'] == 'WBADB' and r['in_asi_sheet'] == 'no'
                                                    and not r['possible_duplicate_of'])
        out.append(u)
    return out


# ---------------------------------------------------------------- IAA units
def tier1(r):
    return bool(re.match(r'HA(28|29)-', r['report_id'])) or bool(re.search(r'almit|עלמית', r['site_name'], re.I))


def text_of(r):
    return '. '.join(x for x in (r['site_name'], r['feature_type'].replace('_', ' '), r['feature_subtype'], r['quote'],
                                 r['period_as_given']) if x)


def select(rows, coder):
    """Version rule (amendment §4). Primary: tomb rows. Sensitivity: other classes passing the TOMB-term test."""
    by = defaultdict(list)
    for r in rows:
        if r['counted'] == 'yes':
            by[r['report_group']].append(r)
    prim, other = [], []
    for g in sorted(by):
        rs = by[g]
        for cls in sorted({r['feature_type'] for r in rs}):
            rc = [r for r in rs if r['feature_type'] == cls]
            pref = [r for r in rc if r['version_role'] in ('single', 'preferred')] or rc
            if cls == CLASS:
                versions = defaultdict(list)
                for r in rc:
                    versions[r['report_id']].append(r)
                union = None
                if len(versions) > 1 and all(len(v) == 1 for v in versions.values()):
                    ds = [v[0]['dated_in_window'] for v in versions.values()]
                    union = 'yes' if 'yes' in ds else 'no' if 'no' in ds else 'unknown'
                for r in pref:
                    r['_dated'] = union or r['dated_in_window']
                prim += pref
            else:
                for r in pref:
                    if coder.tomb.search(text_of(r)):
                        r['_dated'] = r['dated_in_window']
                        other.append(r)
    return prim, other


def iaa_units(plan, coder, rows, sheets, kind):
    units, coverage = [], Counter()
    for r in rows:
        text = text_of(r)
        if not coder.tomb.search(text):
            coverage['no tomb term'] += 1
            continue
        if not r['lat']:
            coverage[f"unlocated@{r['count_zone']}"] += 1
            continue
        lat, lon = float(r['lat']), float(r['lon'])
        fl = T.region_flags(plan, lat, lon)
        if not (fl['in_A'] or fl['in_B1'] or fl['in_B2_5']):
            coverage['outside the regions'] += 1
            continue
        unc = plan['position_uncertainty_km']['HAESI_default']
        try:
            unc = max(unc, float(r['precision_m']) / 1000.0)
        except (TypeError, ValueError):
            pass
        u = dict(source='IAA', record_id=f"IAA {r['row_uid']}", kind=kind,
                 locator=f"{r['series']} {r['volume']} ({r['year']}) p. {r['pages']}; {r['url']}; merged row {r['row_uid']}",
                 name=r['site_name'], lat=lat, lon=lon, unc=unc, text=text, text_hash=T.sha256_text(text),
                 report_group=r['report_group'], site_id=r['site_id'], tier1_related='yes' if tier1(r) else 'no')
        u.update(fl)
        c = coder.code(text, None, ())
        c['dated_in_window'] = r['_dated'] if r['_dated'] in ('yes', 'no') else 'unknown'
        c['dated_lenient'] = 'yes' if (c['dated_in_window'] == 'yes' or c['dated_lenient'] == 'yes') else 'no-evidence'
        u.update(c)
        u['multi_tomb_record'] = 'yes' if re.search(MULTI[0], text, re.I) or re.search(MULTI[1], text, re.I) else 'no'
        u['in_asi_sheet'] = 'yes' if any(s['lat_lo'] <= lat <= s['lat_hi'] and s['lon_lo'] <= lon <= s['lon_hi']
                                         for s in sheets) else 'no'
        u['exposure'] = EXPOSURE
        units.append(u)
    return units, coverage


def manual_check(units, pending):
    checks = {(r['record_id'], r['code']): r for r in read(os.path.join(DATA, 'manual_check_iaa.csv'))}
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


def flag_duplicates(plan, units, frozen):
    prim = [p for p in frozen if p['is_primary'] and p['lat'] is not None]
    for u in units:
        best, nn = None, T.norm_name(u['name'])
        for p in prim:
            d = T.km(u['lat'], u['lon'], p['lat'], p['lon'])
            same = nn and nn == T.norm_name(p['name'])
            if d <= plan['duplicate_km'] or (same and d <= plan['duplicate_same_name_km']):
                if best is None or d < best[0]:
                    best = (d, p['record_id'])
        u['possible_duplicate_of'] = best[1] if best else ''


def amendment1_codes(plan, units, pending):
    checks = {(r['record_id'], r['code']): r for r in read(os.path.join(DATA, 'manual_check_iaa_amendment1.csv'))}
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


# ---------------------------------------------------------------- summaries
def in_region(u, reg):
    return {'A': u['in_A'], 'A3': u['in_A3'], 'B': u['in_B1'] or u['in_B2'], 'B1': u['in_B1'], 'B2': u['in_B2'],
            'B2_5': u['in_B2_5'], 'AB': u['in_A'] or u['in_B1'] or u['in_B2']}[reg]


def in_dateset(u, ds):
    return {'strict': u['dated_in_window'] == 'yes', 'lenient': u['dated_lenient'] == 'yes', 'any': True}[ds]


def tally(plan, units, clauses, val):
    res = []
    for u in units:
        vs = [val(u, c, False) for c in clauses]
        res.append((u, vs, B.overall(vs), B.overall([val(u, c, True) for c in clauses])))
    cc = ' '.join(f"{c}:{sum(r[1][i] == 'yes' for r in res)}/{sum(r[1][i] == 'no' for r in res)}/"
                  f"{sum(r[1][i] == 'unknown' for r in res)}" for i, c in enumerate(clauses))
    return dict(N=len(res), k=sum(r[2] == 'match' for r in res), f=sum(r[2] == 'fail' for r in res),
                m=sum(r[2] == 'unknown' for r in res), ks=sum(r[3] == 'match' for r in res),
                fs=sum(r[3] == 'fail' for r in res), ms=sum(r[3] == 'unknown' for r in res), cc=cc,
                matches=[r[0]['record_id'] for r in res if r[2] == 'match'])


def main(argv):
    for name, h in INPUT_SHA.items():
        if sha(os.path.join(MERGED, name)) != h:
            raise SystemExit(f'{name}: hash differs from the amendment value')
    plan = T.load_plan()
    coder = B.Coder(plan)
    with open(os.path.join(DATA, 'asi_selected_maps.json'), encoding='utf-8') as fh:
        sheets = json.load(fh)
    frozen = frozen_units()
    prim_rows, other_rows = select(read(os.path.join(MERGED, 'features_all.csv')), coder)
    units, cov = iaa_units(plan, coder, prim_rows, sheets, 'primary')
    others, cov_o = iaa_units(plan, coder, other_rows, sheets, 'other_class')
    pending = []
    manual_check(units + others, pending)
    flag_duplicates(plan, units + others, frozen)
    amendment1_codes(plan, units + others, pending)
    if '--pending' in argv or pending:
        for p in pending:
            print(json.dumps(dict(record_id=p[0], code=p[1], raw=p[2], text=p[3]), ensure_ascii=False))
        if pending:
            raise SystemExit(f'{len(pending)} hand checks pending')
        return
    for i, u in enumerate(sorted(units + others, key=lambda x: (x['kind'], x['record_id']))):
        u['unit_id'] = f"I{i + 1:04d}"

    def val(u, c, sens):
        return B.clause_value(plan, u, c, sens)

    located_frozen = [u for u in frozen if u['lat'] is not None]
    kept_frozen = [u for u in located_frozen if u['source'] != 'HAESI']
    views = {
        'frozen_all_lineages': [u for u in located_frozen if not u['possible_duplicate_of']],
        'frozen_primary': [u for u in located_frozen if u['is_primary']],
        'union_all_lineages': [u for u in kept_frozen if not u['possible_duplicate_of']] +
                              [u for u in units if not u['possible_duplicate_of']],
        'lineage_IAA': units,
        'union_all_lineages+other_classes': [u for u in kept_frozen if not u['possible_duplicate_of']] +
                                            [u for u in units + others if not u['possible_duplicate_of']],
    }
    committed = {(r['branch'], r['region'], r['date_set'], r['view']): r for r in read(os.path.join(FOLDER, 'scores_summary.csv'))}
    out, score_rows = [], []
    for b, spec in plan['branches'].items():
        if not spec['clauses']:
            continue
        for u in sorted(units + others, key=lambda x: x['unit_id']):
            vs = [val(u, c, False) for c in spec['clauses']]
            score_rows.append(dict(unit_id=u['unit_id'], record_id=u['record_id'], kind=u['kind'], branch=b,
                                   values=';'.join(vs), result=B.overall(vs),
                                   result_sensitivity=B.overall([val(u, c, True) for c in spec['clauses']]),
                                   possible_duplicate_of=u['possible_duplicate_of']))
        for reg in REGIONS:
            for ds in plan['date_sets']:
                t = {v: tally(plan, [u for u in us if in_region(u, reg) and in_dateset(u, ds)], spec['clauses'], val)
                     for v, us in views.items()}
                for fv, cv in (('frozen_all_lineages', 'all_lineages'), ('frozen_primary', 'primary')):
                    c = committed[(b, reg, ds, cv)]
                    got = t[fv]
                    # match lists are compared as sets: the frozen build lists units in source-build order
                    if [got['N'], got['k'], got['f'], got['m'], got['ks'], got['fs'], got['ms'], got['cc'], sorted(got['matches'])] != \
                            [int(c['N']), int(c['k_match']), int(c['f_fail']), int(c['m_unknown']), int(c['k_sens']),
                             int(c['f_sens']), int(c['m_sens']), c['clause_counts'], sorted(filter(None, c['matches'].split(';')))]:
                        raise SystemExit(f'frozen scoring does not reproduce scores_summary.csv: {b} {reg} {ds} {cv}')
                f, un, li, uo = t['frozen_all_lineages'], t['union_all_lineages'], t['lineage_IAA'], t['union_all_lineages+other_classes']
                out.append(dict(branch=b, headline='yes' if spec['headline'] == reg else '', region=reg, date_set=ds,
                                frozen_N=f['N'], frozen_k=f['k'], frozen_f=f['f'], frozen_m=f['m'],
                                union_N=un['N'], union_k=un['k'], union_f=un['f'], union_m=un['m'],
                                delta_N=un['N'] - f['N'], delta_k=un['k'] - f['k'], delta_f=un['f'] - f['f'],
                                delta_m=un['m'] - f['m'], union_k_sens=un['ks'], frozen_k_sens=f['ks'],
                                iaa_N=li['N'], iaa_k=li['k'], iaa_f=li['f'], iaa_m=li['m'],
                                other_classes_N=uo['N'], other_classes_k=uo['k'], other_classes_f=uo['f'], other_classes_m=uo['m'],
                                union_clause_counts=un['cc'],
                                new_matches=';'.join(x for x in un['matches'] if x.startswith('IAA ')),
                                iaa_matches=';'.join(li['matches'])))
    # Amendment 1 (exploratory) with the IAA units
    a1 = {r['unit_id']: r for r in read(os.path.join(FOLDER, 'amendment1_codes.csv'))}
    for u in located_frozen:
        r = a1[u['unit_id']]
        u['F7wa'], u['F2xa'] = r['F7wa'], r['F2xa']

    def val1(u, c, sens):
        return u[c] if c in ('F7wa', 'F2xa') else B.clause_value(plan, u, c, sens)
    a1_committed = {(r['branch'], r['region'], r['date_set']): r for r in read(os.path.join(FOLDER, 'amendment1_scores_summary.csv'))}
    out1 = []
    for b, cl in list(A1.BRANCHES.items()) + [('ALL-TOMBS', [])]:
        for reg in ('A', 'A3', 'B', 'AB'):
            for ds in plan['date_sets']:
                f = tally(plan, [u for u in views['frozen_all_lineages'] if in_region(u, reg) and in_dateset(u, ds)], cl, val1)
                un = tally(plan, [u for u in views['union_all_lineages'] if in_region(u, reg) and in_dateset(u, ds)], cl, val1)
                c = a1_committed[(b, reg, ds)]
                if [f['N'], f['k'], f['f'], f['m']] != [int(c['N']), int(c['k_match']), int(c['f_fail']), int(c['m_unknown'])]:
                    raise SystemExit(f'frozen amendment-1 scoring does not reproduce amendment1_scores_summary.csv: {b} {reg} {ds}')
                out1.append(dict(branch=b, region=reg, date_set=ds, a1_N=f['N'], a1_k=f['k'], a1_f=f['f'], a1_m=f['m'],
                                 a1_iaa_N=un['N'], a1_iaa_k=un['k'], a1_iaa_f=un['f'], a1_iaa_m=un['m'],
                                 new_matches=';'.join(x for x in un['matches'] if x.startswith('IAA ')) if cl else '(N only)'))
    ucols = ['unit_id', 'kind', 'source', 'record_id', 'locator', 'name', 'lat', 'lon', 'unc', 'd_temple_km', 'd_jericho_km',
             'd_road_km', 'in_A', 'in_A3', 'in_B1', 'in_B2', 'in_B2_5', 'in_asi_sheet', 'possible_duplicate_of', 'report_group',
             'site_id', 'multi_tomb_record', 'tomb_terms', 'F1', 'F2', 'F2x', 'F3', 'F4', 'F5', 'F6', 'F7', 'F7w', 'F10', 'F11',
             'F12', 'F13', 'F14', 'F16', 'F17', 'F19', 'F20_communal', 'F21', 'name_zadok', 'name_absalom', 'name_queen',
             'name_obed', 'name_jericho', 'period_terms', 'dated_in_window', 'dated_lenient', 'manual_rejected', 'F7a', 'F7wa',
             'F2xa', 'a1_rejected', 'tier1_related', 'exposure', 'text_hash']
    rows = []
    for u in sorted(units + others, key=lambda x: x['unit_id']):
        r = {k: u.get(k, '') for k in ucols}
        for k in ('lat', 'lon'):
            r[k] = f"{u[k]:.6f}"
        for k in ('d_temple_km', 'd_jericho_km', 'd_road_km'):
            r[k] = f"{u[k]:.3f}"
        for k in ('in_A', 'in_A3', 'in_B1', 'in_B2', 'in_B2_5'):
            r[k] = 'yes' if u[k] else 'no'
        rows.append(r)
    write(os.path.join(FOLDER, 'iaa_units.csv'), ucols, rows)
    write(os.path.join(FOLDER, 'iaa_scores.csv'), list(score_rows[0]), score_rows)
    write(os.path.join(FOLDER, 'iaa_view_2026-10-11.csv'), list(out[0]), out)
    write(os.path.join(FOLDER, 'iaa_amendment1_view.csv'), list(out1[0]), out1)
    nd = [u for u in units if not u['possible_duplicate_of']]
    summary = dict(
        note='Exploratory view (PLAN_AMENDMENT_IAA_2026-10-11.md). The frozen tables are unchanged.',
        inputs=INPUT_SHA, frozen_haesi_units_removed=sum(1 for u in frozen if u['source'] == 'HAESI'),
        iaa_units=dict(primary=len(units), primary_not_duplicate=len(nd),
                       primary_not_duplicate_distinct_sites=len({u['site_id'] for u in nd}),
                       other_class=len(others), other_class_not_duplicate=sum(1 for u in others if not u['possible_duplicate_of'])),
        iaa_units_by_region_not_duplicate={reg: sum(1 for u in nd if in_region(u, reg)) for reg in REGIONS},
        iaa_strict_not_duplicate={reg: sum(1 for u in nd if in_region(u, reg) and u['dated_in_window'] == 'yes') for reg in REGIONS},
        coverage_primary=dict(sorted(cov.items())), coverage_other_class=dict(sorted(cov_o.items())),
        tier1_units=[u['record_id'] for u in units + others if u['tier1_related'] == 'yes'])
    with open(os.path.join(FOLDER, 'iaa_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
        f.write('\n')
    print(json.dumps(summary['iaa_units']), json.dumps(summary['iaa_units_by_region_not_duplicate']))
    for r in out:
        if r['headline'] and r['date_set'] == 'strict':
            print(r['branch'], r['region'], 'frozen', r['frozen_k'], r['frozen_f'], r['frozen_m'], r['frozen_N'], '| union',
                  r['union_k'], r['union_f'], r['union_m'], r['union_N'], '|', r['new_matches'])


def write(path, fields, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


if __name__ == '__main__':
    main(sys.argv[1:])
