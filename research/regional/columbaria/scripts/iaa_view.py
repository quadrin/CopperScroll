#!/usr/bin/env python3
"""Exploratory view: the merged IAA inventory folded into the columbaria lane (PLAN_AMENDMENT_IAA_2026-10-11.md).

Run from the repository root:  python3 -I research/regional/columbaria/scripts/iaa_view.py [--pairs]
Reads the committed columbaria.csv and summary.json, the merged IAA inventory
(research/regional/haesi_features/merged_2026-10-11/), the hand coding data/iaa_coding.json and the duplicate
decisions data/iaa_dedup_decisions.csv. Scores with score.py's score_row, combos and tally, imported unchanged.
Writes iaa_rows.csv, iaa_excluded.csv, iaa_scores.csv, iaa_summary.json and iaa_view_2026-10-11.csv; never writes
columbaria.csv, scores.csv or summary.json. --pairs prints the candidate duplicate pairs that need a decision.
Standard library only.
"""
import csv
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colcommon as C  # noqa: E402
import score as SC  # noqa: E402  (frozen scoring, unchanged)
from assemble import COLUMNS, WINDOW  # noqa: E402

FOLDER = C.FOLDER
MERGED = os.path.join(C.REPO, 'research', 'regional', 'haesi_features', 'merged_2026-10-11')
PLACES = os.path.join(C.REPO, 'research', 'agent_review_2026-10-07', 'wave2', 'W2B_model_v1', 'inputs_v2', 'places_v2.csv')
INPUT_SHA = {  # PLAN_AMENDMENT_IAA §2
    'features_all.csv': '2170f7fb15b097621e07648c128719f25e50e3550d5ec8756c08fca6267e455b',
    'report_groups.csv': '06085467541339b097fcd29a55a5d7e8d49ade829b7f8329a00f981e9624b89c',
    'sites.csv': '7e89ddce959869e8a960103e63417870d621edb5f7f1b0376b3d12f54450e87b',
}
CLASS = 'columbarium_dovecote'
DUP_KM = 0.3                  # PLAN §5
MAX_PLACE_SIGMA_M = 2000.0    # PLAN §3: placed within 2 km
MIN_PREC_M = 100.0            # amendment §4: at least the frozen ASI/WBADB value
GENERIC = set('''jerusalem kh khirbet khirbat horvat survey surveys map region area areas road new north south east
west northern southern eastern western the of and season excavation excavations el er es ed et ez en ha al ein
ain cave caves columbarium columbaria site sites near street st mount mt har givat giv at slopes slope upper lower
central bet beit tel tell wadi nahal judea samaria brief news jordan valley'''.split())
VIEW_FIELDS = ['scope', 'kind', 'key', 'frozen_N', 'frozen_k', 'frozen_f', 'frozen_m', 'iaa_N', 'iaa_k', 'iaa_f',
               'iaa_m', 'union_N', 'union_k', 'union_f', 'union_m', 'delta_N', 'delta_k', 'delta_f', 'delta_m',
               'nodedup_N', 'nodedup_k', 'nodedup_f', 'nodedup_m', 'dedup300_N', 'dedup300_k', 'dedup300_f',
               'dedup300_m', 'new_matches']


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def fold(s):
    s = unicodedata.normalize('NFKD', s or '')
    return ''.join(ch for ch in s if not unicodedata.combining(ch)).lower()


def tokens(name):
    return {t for t in re.findall(r'[a-z]+', fold(name).replace("'", '').replace('‘', '').replace('’', ''))
            if len(t) >= 4 and t not in GENERIC}


def tier1(r):
    return bool(re.match(r'HA(28|29)-', r['report_id'])) or bool(re.search(r'almit|עלמית', r['site_name'], re.I))


def select(rows):
    """Version rule (amendment §5). Returns primary rows and word-screen rows (other classes, amendment §3)."""
    by = defaultdict(list)
    for r in rows:
        if r['counted'] == 'yes':
            by[r['report_group']].append(r)
    prim, screen = [], []
    for g in sorted(by):
        rs = by[g]
        for cls in sorted({r['feature_type'] for r in rs}):
            rc = [r for r in rs if r['feature_type'] == cls]
            pref = [r for r in rc if r['version_role'] in ('single', 'preferred')] or rc
            if cls == CLASS:
                prim += pref
            else:
                for r in pref:
                    if C.find_columbarium(r['feature_subtype'] + ' ' + r['quote']):
                        r['_group_has_columbarium_row'] = any(x['feature_type'] == CLASS for x in rs)
                        screen.append(r)
    return prim, screen


def position(r, places):
    if r['lat']:
        return float(r['lat']), float(r['lon']), max(MIN_PREC_M, float(r['precision_m'] or 0)), \
            f"merged IAA row point (WGS 84, converted by the phase reader from {r['crs_used']} {r['map_ref_as_given']})"
    m = re.search(r'\(([a-z0-9_]+)\)', r['coordinate_source'])
    if m and m.group(1) in places:
        p = places[m.group(1)]
        sig = float(p['sigma_km'] or 0) * 1000.0
        if sig <= MAX_PLACE_SIGMA_M:
            return float(p['lat']), float(p['lon']), sig, f"reader place {m.group(1)} (places_v2, sigma {sig:g} m)"
    return None


def candidates():
    for name, h in INPUT_SHA.items():
        if sha(os.path.join(MERGED, name)) != h:
            raise SystemExit(f'{name}: hash differs from the amendment value')
    places = {r['place_id']: r for r in read(PLACES)}
    prim, screen = select(read(os.path.join(MERGED, 'features_all.csv')))
    return prim, screen, places


def lane_counted():
    return [r for r in read(os.path.join(FOLDER, 'columbaria.csv')) if not r['dup_of'] and r['in_region'] == 'yes']


def pair_list(iaa, lane):
    """Candidate pairs (amendment §6): within 300 m, or a shared distinctive name word."""
    out = []
    pts = [(x['id'], float(x['lat']), float(x['lon']), x['name'], 'lane') for x in lane if x['lat']]
    pts += [(x['id'], float(x['lat']), float(x['lon']), x['name'], x['_report_group']) for x in iaa if x['lat'] != '']
    for i, a in enumerate(iaa):
        if a['lat'] == '':
            continue
        for b in pts:
            if b[0] == a['id'] or (b[4] != 'lane' and (b[4] == a['_report_group'] or b[0] < a['id'])):
                continue
            d = C.km(float(a['lat']), float(a['lon']), b[1], b[2])
            shared = tokens(a['name']) & tokens(b[3])
            if d <= DUP_KM or shared:
                out.append(dict(iaa_id=a['id'], other_id=b[0], other_kind='lane' if b[4] == 'lane' else 'iaa',
                                km=round(d, 3), shared_words=' '.join(sorted(shared)), iaa_name=a['name'], other_name=b[3]))
    return out


def build():
    prim, screen, places = candidates()
    with open(os.path.join(FOLDER, 'data', 'iaa_coding.json'), encoding='utf-8') as f:
        coding = json.load(f)['rows']
    rows, excluded, unplaced, outside, used = [], [], Counter(), 0, set()
    for r in prim:
        pos = position(r, places)
        base = dict(row_uid=r['row_uid'], report_id=r['report_id'], report_group=r['report_group'],
                    site_name=r['site_name'], feature_type=r['feature_type'])
        if pos is None:
            unplaced[r['count_zone']] += 1
            excluded.append(dict(base, status='unplaced', reason='no coordinates and no reader place within 2 km (PLAN §3)'))
            continue
        lat, lon, prec, basis = pos
        if not C.in_region(lon, lat):
            outside += 1
            continue
        if not C.find_columbarium(r['feature_subtype'] + ' ' + r['quote'] + ' ' + r['site_name']):
            excluded.append(dict(base, status='not admitted', reason='no frozen columbarium word in the IAA coding (PLAN §5)'))
            continue
        c = coding.get(r['row_uid'])
        if c is None:
            raise SystemExit(f'in-region row without hand coding: {r["row_uid"]}')
        used.add(r['row_uid'])
        if c.get('exclude'):
            excluded.append(dict(base, status='excluded', reason=c['exclude']))
            continue
        rows.append(make_row(r, c, lat, lon, prec, basis))
    if set(coding) - used:
        raise SystemExit(f'coding for rows not in the region: {sorted(set(coding) - used)}')
    scr = [dict(row_uid=r['row_uid'], report_id=r['report_id'], report_group=r['report_group'], site_name=r['site_name'],
                feature_type=r['feature_type'],
                status='word screen: not added' if r['_group_has_columbarium_row'] else 'word screen: candidate',
                reason='its report group already gives a columbarium_dovecote row (amendment §3)'
                if r['_group_has_columbarium_row'] else 'other class with a columbarium word') for r in screen]
    if any(s['status'] == 'word screen: candidate' for s in scr):
        raise SystemExit('word-screen candidates need hand coding; none was expected')
    return rows, excluded + scr, dict(unplaced_by_zone=dict(unplaced), outside_region=outside)


def make_row(r, c, lat, lon, prec, basis):
    n = r['n_features'].strip()
    out = {k: '' for k in COLUMNS}
    out.update(
        id=f"IAA-{r['row_uid']}", source='IAA',
        source_ref=f"{r['series']} {r['volume']} ({r['year']}) p. {r['pages']}, {r['author']}; merged IAA inventory row {r['row_uid']}",
        record_url=r['url'], name=r['site_name'], part=c.get('part', ''), lat=round(lat, 6), lon=round(lon, 6),
        crs='EPSG:4326', coord_basis=basis, coord_precision_m=f'{prec:g}', in_region='yes',
        construction=c.get('cons', 'unknown'), levels='', niche_count=c.get('niches', ''),
        n_columbaria=int(n) if n.isdigit() else ('' if c.get('plural') else 1),
        setting=c.get('setting', 'unknown'), fort_at_site=c.get('fort_at_site', 'no'),
        tower_at_site=c.get('tower_at_site', 'no'), outside_fort=c.get('outside_fort', 'no'),
        outside_tower=c.get('outside_tower', 'no'), part_of_site=c.get('part_of_site', ''),
        lev2=c.get('lev2', 'U'), lev3=c.get('lev3', 'U'), lev_basis=c.get('lev_basis', ''),
        lev_position='', access=c.get('acc', 'U'), access_basis=c.get('acc_basis', ''),
        site_periods='', date_code=c['date'], date_text=c.get('date_text', ''), dated_in_window=WINDOW[c['date']],
        natof_text=c.get('natof', 'U'), quote='', dup_of='', priority=2,
        uncertain_identification='yes' if c.get('uncertain') else 'no', exposed_before_freeze='no',
        post_freeze_source='yes', post_freeze_override='', tier1_related='yes' if tier1(r) else 'no',
        check_flag='yes' if c.get('check') else 'no', read_via=f"merged IAA inventory row {r['row_uid']} (coding fields only)",
        notes=c.get('notes', ''))
    out['_report_group'] = r['report_group']
    return out


def apply_dedup(rows, lane, mode):
    """mode 'decided' (hand decisions), 'none' (bracket: no dedup), 'all300' (bracket: every pair within 300 m)."""
    decisions = {(d['iaa_id'], d['other_id']): d for d in read(os.path.join(FOLDER, 'data', 'iaa_dedup_decisions.csv'))}
    pairs = pair_list(rows, lane)
    missing = [p for p in pairs if (p['iaa_id'], p['other_id']) not in decisions]
    if missing:
        raise SystemExit(f'{len(missing)} candidate pairs without a decision; run with --pairs')
    out = [dict(r, dup_of='') for r in rows]
    by = {r['id']: r for r in out}
    if mode == 'none':
        return out
    for p in pairs:
        same = decisions[(p['iaa_id'], p['other_id'])]['decision'] == 'same' if mode == 'decided' else p['km'] <= DUP_KM
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
    return out


def score_set(rows):
    out = []
    for r in rows:
        s = SC.score_row(r)
        out.append((r, s, SC.combos(s)))
    return out


def tallies(scored):
    w = [int(r['n_columbaria']) if str(r['n_columbaria']) not in ('', 'None') else 1 for r, _, _ in scored]
    clauses = {k: SC.tally([s[k] for _, s, _ in scored], w) for k in SC.CLAUSES}
    keys = sorted(scored[0][2]) if scored else []
    combos = {k: SC.tally([c[k] for _, _, c in scored], w) for k in keys}
    return clauses, combos


def counted(rows):
    return [r for r in rows if not r['dup_of'] and r['in_region'] == 'yes']


def main(argv):
    rows, excluded, coverage = build()
    lane = lane_counted()
    if '--pairs' in argv:
        for p in pair_list(rows, lane):
            print(json.dumps(p, ensure_ascii=False))
        return
    views = {m: apply_dedup(rows, lane, m) for m in ('decided', 'none', 'all300')}
    lane_all = read(os.path.join(FOLDER, 'columbaria.csv'))
    committed = json.load(open(os.path.join(FOLDER, 'summary.json'), encoding='utf-8'))
    out_view, summary = [], {'_note': 'Exploratory view (PLAN_AMENDMENT_IAA_2026-10-11.md); summary.json is unchanged.',
                             'inputs': INPUT_SHA, 'coverage': coverage, 'scopes': {}}
    score_rows = []
    for scope in ('frozen', 'all'):
        frozen = SC.scoped(lane_all, scope)
        fz = score_set(frozen)
        fcl, fco = tallies(fz)
        cs = committed['scopes'][scope]
        if any(fco[k] != v for k, v in cs['headline'].items()) or fcl != cs['clauses']:
            raise SystemExit(f'the frozen scoring does not reproduce summary.json ({scope})')
        res = {}
        for mode, vrows in views.items():
            iz = score_set(counted(vrows))
            res[mode] = (iz, tallies(iz), tallies(fz + iz))
        iz, (icl, ico), (ucl, uco) = res['decided']
        for r, s, c in iz:
            score_rows.append(dict(scope=scope, id=r['id'], name=r['name'], **s, **c))
        for kind, f_t, i_t, u_t, nd_t, d3_t in (
                ('headline', fco, ico, uco, res['none'][2][1], res['all300'][2][1]),
                ('clause', fcl, icl, ucl, res['none'][2][0], res['all300'][2][0])):
            keys = SC.HEADLINE if kind == 'headline' else SC.CLAUSES
            for k in keys:
                f, u = f_t[k], u_t[k]
                i = i_t.get(k, dict(N=0, k_match=0, f_fail=0, m_unknown=0))
                new = sorted(r['id'] for r, s, c in iz if (c.get(k) if kind == 'headline' else s.get(k)) == 'M')
                out_view.append(dict(scope=scope, kind=kind, key=k,
                                     frozen_N=f['N'], frozen_k=f['k_match'], frozen_f=f['f_fail'], frozen_m=f['m_unknown'],
                                     iaa_N=i['N'], iaa_k=i['k_match'], iaa_f=i['f_fail'], iaa_m=i['m_unknown'],
                                     union_N=u['N'], union_k=u['k_match'], union_f=u['f_fail'], union_m=u['m_unknown'],
                                     delta_N=u['N'] - f['N'], delta_k=u['k_match'] - f['k_match'],
                                     delta_f=u['f_fail'] - f['f_fail'], delta_m=u['m_unknown'] - f['m_unknown'],
                                     nodedup_N=nd_t[k]['N'], nodedup_k=nd_t[k]['k_match'], nodedup_f=nd_t[k]['f_fail'],
                                     nodedup_m=nd_t[k]['m_unknown'], dedup300_N=d3_t[k]['N'], dedup300_k=d3_t[k]['k_match'],
                                     dedup300_f=d3_t[k]['f_fail'], dedup300_m=d3_t[k]['m_unknown'], new_matches=';'.join(new)))
        iaa_counted = counted(views['decided'])
        summary['scopes'][scope] = dict(
            iaa_rows_counted=len(iaa_counted),
            iaa_rows_dup_of_lane=sum(1 for r in views['decided'] if r['dup_of'] and not r['dup_of'].startswith('IAA-')),
            iaa_rows_dup_of_iaa=sum(1 for r in views['decided'] if r['dup_of'].startswith('IAA-')),
            union_rows_counted=len(frozen) + len(iaa_counted),
            union_headline={k: uco[k] for k in SC.HEADLINE}, union_clauses=ucl,
            bracket_rows_counted=dict(no_dedup=len(counted(views['none'])), dedup_300m=len(counted(views['all300']))))
    write(os.path.join(FOLDER, 'iaa_rows.csv'), COLUMNS, views['decided'])
    write(os.path.join(FOLDER, 'iaa_excluded.csv'), ['row_uid', 'report_id', 'report_group', 'site_name', 'feature_type',
                                                     'status', 'reason'], excluded)
    write(os.path.join(FOLDER, 'iaa_scores.csv'), list(score_rows[0].keys()), score_rows)
    write(os.path.join(FOLDER, 'iaa_view_2026-10-11.csv'), VIEW_FIELDS, out_view)
    with open(os.path.join(FOLDER, 'iaa_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write('\n')
    s = summary['scopes']['frozen']
    print(f"IAA rows: {len(rows)} in region, {s['iaa_rows_counted']} counted, {s['iaa_rows_dup_of_lane']} dup of lane, "
          f"{s['iaa_rows_dup_of_iaa']} dup of IAA; union {s['union_rows_counted']}")
    for r in out_view:
        if r['scope'] == 'frozen' and r['kind'] == 'headline':
            print(r['key'], 'frozen', r['frozen_k'], r['frozen_f'], r['frozen_m'], r['frozen_N'], '| union',
                  r['union_k'], r['union_f'], r['union_m'], r['union_N'], r['new_matches'])


def write(path, fields, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


if __name__ == '__main__':
    main(sys.argv[1:])
