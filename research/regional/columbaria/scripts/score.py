#!/usr/bin/env python3
"""Apply the frozen clauses of PLAN.md §2 and §7 to columbaria.csv. Standard library only, deterministic.

Run:  python3 -I scripts/score.py
Writes scores.csv (one row per counted columbarium row and scope) and summary.json.
Scopes: 'frozen' uses only the sources fixed in PLAN.md §4; 'all' also applies the post-freeze
source overrides of PLAN_AMENDMENT_1.md (labelled exploratory).
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colcommon as C  # noqa: E402

FOLDER = C.FOLDER
N1 = (31.64436, 35.23543)      # atlas place natuf, ʿAin en-Naṭuf (PLAN §2)
N2 = (31.667995, 35.220669)    # ASI 108/2 site 2, Kh. Bad Faluh (PLAN §2)
R_PRIMARY, R_SENS = 1.0, 2.0   # km (PLAN §7)
LAT_SA, LAT_SB1, LAT_SB2 = 31.765, 31.62, 31.53   # PLAN §2, south lines
M_PER_DEG_LAT = 111320.0
NAMED_PARTS_FAIL = {'north', 'east', 'west', 'northeast', 'northwest'}


def dist_code(lat, lon, centre, r_km, p_m):
    if lat is None or p_m is None or p_m > 2000:
        return 'U', None
    d = C.km(lat, lon, centre[0], centre[1])
    if d <= r_km:
        return 'M', d
    if d > r_km + p_m / 1000.0:
        return 'F', d
    return 'U', d


def lat_code(lat, line, p_m):
    if lat is None or p_m is None or p_m > 2000:
        return 'U'
    margin = p_m / M_PER_DEG_LAT
    if lat < line - margin:
        return 'M'
    if lat > line + margin:
        return 'F'
    return 'U'


def period(code, relaxed=False):
    if code == 'L':
        return 'F'
    if relaxed:
        return 'M'
    return 'M' if code == 'D' else 'U'


def fort_codes(r):
    fort_site = r['fort_at_site'] == 'yes' or r['setting'] in ('fortress_inside', 'fort_site')
    tower_site = r['tower_at_site'] == 'yes' or r['setting'] == 'tower_itself'
    isolated = r['setting'] == 'isolated'
    outside = r['outside_fort'] == 'yes'
    f_survey = 'M' if fort_site else ('F' if isolated else 'U')
    f_text = 'M' if r['setting'] == 'fortress_inside' else ('F' if (outside or isolated) else 'U')
    fp_survey = 'M' if (fort_site or tower_site) else ('F' if isolated else 'U')
    if r['setting'] in ('fortress_inside', 'tower_itself'):
        fp_text = 'M'
    elif isolated or (outside and r['setting'] != 'tower_itself') or (r['outside_tower'] == 'yes' and not fort_site):
        fp_text = 'F'
    else:
        fp_text = 'U'
    return f_survey, f_text, fp_survey, fp_text


def s_c(part):
    if part == 'south':
        return 'M'
    if part in NAMED_PARTS_FAIL:
        return 'F'
    return 'U'


def combine(codes):
    if 'F' in codes:
        return 'F'
    if all(c == 'M' for c in codes):
        return 'M'
    return 'U'


def load_rows():
    with open(os.path.join(FOLDER, 'columbaria.csv'), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def scoped(rows, scope):
    out = []
    for r in rows:
        if r['dup_of'] or r['in_region'] != 'yes':
            continue
        r = dict(r)
        if scope == 'all' and r['post_freeze_override']:
            ov = json.loads(r['post_freeze_override'])
            mapping = {'date': 'date_code', 'acc': 'access', 'acc_basis': 'access_basis', 'date_text': 'date_text',
                       'uncertain': 'uncertain_identification'}
            for k, v in ov.items():
                r[mapping.get(k, k)] = ('yes' if v is True else v)
        out.append(r)
    return out


def score_row(r):
    lat = float(r['lat']) if r['lat'] else None
    lon = float(r['lon']) if r['lon'] else None
    p_m = float(r['coord_precision_m']) if r['coord_precision_m'] else None
    s = {}
    for tag, centre in (('N1', N1), ('N2', N2)):
        for rk, rname in ((R_PRIMARY, '1km'), (R_SENS, '2km')):
            code, d = dist_code(lat, lon, centre, rk, p_m)
            s[f'{tag}_{rname}'] = code
            s[f'{tag}_km'] = '' if d is None else round(d, 3)
            text = 'M' if (r['natof_text'] == 'M' and code == 'M') else ('F' if code == 'F' else 'U')
            s[f'{tag}_{rname}_text'] = text
    s['P'] = period(r['date_code'])
    s['P_relaxed'] = period(r['date_code'], relaxed=True)
    s['F_survey'], s['F_text'], s['Fplus_survey'], s['Fplus_text'] = fort_codes(r)
    s['S_A'] = lat_code(lat, LAT_SA, p_m)
    s['S_B1'] = lat_code(lat, LAT_SB1, p_m)
    s['S_B2'] = lat_code(lat, LAT_SB2, p_m)
    s['S_C'] = s_c(r['part_of_site'])
    s['L2'], s['L3'], s['A'] = r['lev2'], r['lev3'], r['access']
    s['Masada'] = 'M' if 'masada' in (r['name'] + ' ' + r['source_ref']).lower() else 'F'
    return s


def combos(s):
    out = {}
    for pk, pname in (('P', ''), ('P_relaxed', '|period_relaxed')):
        p = s[pk]
        for lvl in ('survey', 'text'):
            suf = '' if lvl == 'survey' else '_text'
            for rk in ('1km', '2km'):
                out[f'38-D-N1|{lvl}|{rk}{pname}'] = combine([s[f'N1_{rk}{suf}'], p])
                out[f'38-D-N2|{lvl}|{rk}{pname}'] = combine([s[f'N2_{rk}{suf}'], p])
            out[f'38-D-N0|{lvl}{pname}'] = combine([p])
            fort = s['F_survey'] if lvl == 'survey' else s['F_text']
            fplus = s['Fplus_survey'] if lvl == 'survey' else s['Fplus_text']
            for south in ('S_A', 'S_B1', 'S_B2', 'S_C'):
                for fname, f in (('F', fort), ('Fplus', fplus)):
                    out[f'44-D-P|{lvl}|{fname}|{south}{pname}'] = combine([f, s[south], s['L2'], s['A'], p])
                    out[f'44-D-T|{lvl}|{fname}|{south}{pname}'] = combine([f, s[south], s['L3'], s['A'], p])
            out[f'44-D-Masada|{lvl}{pname}'] = combine([s['Masada'], s['L2'], s['A'], p])
    return out


CLAUSES = ['N1_1km', 'N1_2km', 'N2_1km', 'N2_2km', 'N1_1km_text', 'N2_1km_text', 'P', 'P_relaxed', 'F_survey',
           'F_text', 'Fplus_survey', 'Fplus_text', 'S_A', 'S_B1', 'S_B2', 'S_C', 'L2', 'L3', 'A', 'Masada']
HEADLINE = ['38-D-N1|survey|1km', '38-D-N1|text|1km', '38-D-N2|survey|1km', '38-D-N2|text|1km', '38-D-N0|survey',
            '44-D-P|survey|F|S_A', '44-D-P|text|F|S_A', '44-D-T|survey|F|S_A', '44-D-T|text|F|S_A',
            '44-D-Masada|text']


def tally(values, weights):
    t = {'M': 0, 'F': 0, 'U': 0}
    tw = {'M': 0, 'F': 0, 'U': 0}
    for v, w in zip(values, weights):
        t[v] += 1
        tw[v] += w
    return {'k_match': t['M'], 'f_fail': t['F'], 'm_unknown': t['U'], 'N': len(values),
            'n_weighted': {'match': tw['M'], 'fail': tw['F'], 'unknown': tw['U'], 'N': sum(weights)}}


def main(out_dir=FOLDER):
    rows = load_rows()
    out_rows, summary = [], {'_note': 'k/f/m by counted row (duplicates removed); n_weighted sums n_columbaria, '
                                      'counting an unspecified plural as 1 (a lower bound).',
                             'scopes': {}}
    for scope in ('frozen', 'all'):
        rs = scoped(rows, scope)
        scored = []
        for r in rs:
            s = score_row(r)
            c = combos(s)
            scored.append((r, s, c))
            out_rows.append(dict(scope=scope, id=r['id'], name=r['name'], source=r['source'], **s, **c))
        weights = [int(r['n_columbaria']) if r['n_columbaria'] not in ('', None) else 1 for r, _, _ in scored]
        clause_t = {k: tally([s[k] for _, s, _ in scored], weights) for k in CLAUSES}
        combo_keys = sorted(scored[0][2].keys())
        combo_t = {k: tally([c[k] for _, _, c in scored], weights) for k in combo_keys}
        distinctive = sorted(r['id'] for r, s, _ in scored
                             if 'M' in (s['F_text'], s['L2'], s['L3'], s['A'], s['S_C'], s['N1_1km_text'],
                                        s['N2_1km_text']))
        summary['scopes'][scope] = {
            'rows_counted': len(scored),
            'columbaria_lower_bound': sum(weights),
            'rows_with_unspecified_plural': sum(1 for r, _, _ in scored if r['n_columbaria'] in ('', None)),
            'by_source': {src: sum(1 for r, _, _ in scored if r['source'] == src) for src in ('ASI', 'WBADB', 'LIT')},
            'headline': {k: combo_t[k] for k in HEADLINE},
            'clauses': clause_t,
            'combinations': combo_t,
            'rows_matching_a_distinctive_clause': distinctive,
            'rows_partial_44_text': sorted(r['id'] for r, s, c in scored
                                           if c['44-D-P|text|F|S_A'] != 'F' and s['F_text'] == 'M'),
        }
    cols = list(out_rows[0].keys())
    with open(os.path.join(out_dir, 'scores.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        w.writerows(out_rows)
    with open(os.path.join(out_dir, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write('\n')
    for scope in ('frozen', 'all'):
        print(scope, json.dumps({k: (v['k_match'], v['f_fail'], v['m_unknown'], v['N'])
                                 for k, v in summary['scopes'][scope]['headline'].items()}))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else FOLDER)
