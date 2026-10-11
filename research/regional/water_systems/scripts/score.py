#!/usr/bin/env python3
"""Score water.csv against entries 21, 22, 29, 32, 42, 45 and 46 under PLAN.md §5 (standard library only).

Run from the repository root:
  python3 -I research/regional/water_systems/scripts/score.py
Writes scores.csv (row x entry x branch), counts.csv (N, k, f, m per entry x branch x lineage x date rule)
and headline.csv (the brief's headline counts).
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

M, F, U, NS = 'MATCH', 'FAIL', 'UNKNOWN', 'not_scored'
TRUNK = re.compile(r'qelt|kelt|prat|perat|kidron|qidron|\bnar\b|mukallik|\bog\b|darajeh|darga|khureitun|nueima|nuweim',
                   re.I)
LINEAGES = ['WBADB', 'ASI', 'HAESI', 'LIT']
DATE_RULES = {'main': lambda d: d != 'out', 'dated': lambda d: d in ('in', 'in_hedged'), 'strict': lambda d: d == 'in'}


def tri(v, yes=M, no=F):
    return yes if v == 'yes' else (no if v == 'no' else U)


def overall(codes):
    vals = [c for c in codes if c != NS]
    if F in vals:
        return F
    if vals and all(c == M for c in vals):
        return M
    return U


def flt(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def within(r, place, limit_km):
    """MATCH / FAIL / UNKNOWN for 'within limit_km of place', allowing for the row's precision (plan §6)."""
    lat, lon, prec = flt(r['lat']), flt(r['lon']), flt(r['precision_m']) or 0.0
    if lat is None:
        return U
    d = C.km(lat, lon, place[0], place[1])
    p = prec / 1000.0
    if d + p <= limit_km:
        return M
    if d - p > limit_km:
        return F
    return U


def flow_clause(r):
    f = (r['flow_from'] or '').strip()
    if f == 'N':
        return M
    if f in ('S', 'E', 'W', 'SW', 'SE', 'WSW', 'ESE', 'SSW', 'SSE', 'WNW', 'ENE'):
        return F
    if f in ('NE', 'NW', 'NNE', 'NNW'):
        return U  # verbal quadrant edges / near-north wording are not resolved by the frozen rule
    lat, lon, dlat, dlon = flt(r['lat']), flt(r['lon']), flt(r.get('dest_lat')), flt(r.get('dest_lon'))
    if None in (lat, lon, dlat, dlon):
        return U
    sep = C.km(dlat, dlon, lat, lon) * 1000.0
    prec = max(flt(r['precision_m']) or 0.0, flt(r.get('dest_prec')) or 0.0)
    if sep < 3 * prec:
        return U
    b = C.bearing(dlat, dlon, lat, lon)  # from destination to head = direction the water comes from
    return M if (b >= 315 or b <= 45) else F


def marker_present(r, s):
    hm = r['head_marker'] or ''
    if r['head'] != 'yes':
        return U
    if s == 'stone':
        return M if 'stone' in hm else U
    if s == 'pool':
        return M if 'pool' in hm else U
    if s == 'any':
        return M if hm else U
    return NS


def e21(r):
    out = []
    if r['type'] != 'aqueduct':
        return out
    H = tri(r['head'], no=U)
    for s in ('stone', 'pool', 'any', 'open'):
        mk = marker_present(r, s)
        # N-side: the marker must lie on the north side of the head
        if s == 'open':
            side = NS
        elif mk == M:
            ms = (r['marker_side'] or '').strip()
            side = M if ms == 'N' else (U if ms in ('', 'NE', 'NW') else F)
        else:
            side = U
        out.append(('21', f'S-{s}|N-side', dict(head=H, marker=mk, side=side)))
        out.append(('21', f'S-{s}|F-flow', dict(head=H, marker=mk, flow=flow_clause(r))))
    return out


def eligibilities(r):
    """Main set: reservoir_pool rows; sensitivity set: reservoir_pool plus cistern rows (plan §5)."""
    return ['res', 'res+cis'] if r['type'] == 'reservoir_pool' else ['res+cis']


def fissure(r, km_limit):
    v = r['fissure_east']
    fm = flt(r.get('fissure_m'))
    if v in ('yes', 'yes_1km'):
        if fm is not None and fm <= km_limit * 1000:
            return M
        return U
    return U


def e22(r):
    out = []
    if r['type'] not in ('reservoir_pool', 'cistern'):
        return out
    name = M if r['solomon'] == 'yes' else U
    for elig in eligibilities(r):
        for lim, lab in ((0.5, 'fissure-500m'), (1.0, 'fissure-1km')):
            out.append(('22', f'{elig}|{lab}', dict(name=name, fissure=fissure(r, lim))))
    return out


def conduit29(r):
    f = r['feed']
    if f in ('channel', 'wadi_diversion', 'aqueduct'):
        return M
    if f in ('runoff', 'roof_runoff', 'spring_in_situ'):
        return F
    return U


def e29(r):
    out = []
    if r['type'] not in ('reservoir_pool', 'cistern'):
        return out
    base = dict(conduit=conduit29(r), great=tri(r['great']), north=tri(r['north']),
                four=M if r['shape'] == 'four_sides' else (F if r['shape'] == 'not_four_sides' else U))
    located = bool(r['lat'])
    q = {
        'Q-any': NS,
        'Q-Kidron': M if r['kidron_feed'] == 'yes' else (F if located else U),
        'Q-Cypros': M if r['cypros'] == 'yes' else (F if located else U),
        'Q-Jericho': tri(r['jericho_oasis']),
    }
    for elig in eligibilities(r):
        for qb, qc in q.items():
            out.append(('29', f'{elig}|{qb}', dict(base, place=qc)))
    return out


def e32(r):
    out = []
    t = r['type']
    if t not in ('spring', 'aqueduct', 'outlet'):
        return out
    k = M if r['qelt'] == 'yes' else (F if r['qelt'] == 'no' else U)
    wall = M if r['wall_at_outlet'] == 'yes' else U
    if t == 'spring':
        o = {'O-spring': M}
    elif t == 'outlet':
        o = {'O-built': M}
    else:
        o = {'O-built': tri(r['head'], no=U)}
    for ob, oc in o.items():
        out.append(('32', f'{ob}|K-Qelt|T-wall', dict(outlet=oc, kozeba=k, tur=wall)))
        out.append(('32', f'{ob}|K-Qelt|T-none', dict(outlet=oc, kozeba=k)))
    return out


def e42(r):
    out = []
    t = r['type']
    if t == 'waterfall':
        w = 'W-fall'
    elif t in ('dam', 'reservoir_pool'):
        w = 'W-dam'
    else:
        return out
    nb = flt(r.get('near_bend_m'))
    for lim, lab in ((250, 'bend-250m'), (1000, 'bend-1km')):
        out.append(('42', f'{w}|{lab}', dict(bend=M if (nb is not None and nb <= lim) else U)))
    return out


def e45(r):
    out = []
    t = r['type']
    if t not in ('cistern', 'well'):
        return out
    ch = M if r['feed'] in ('channel', 'wadi_diversion', 'aqueduct') else \
        (F if r['feed'] in ('roof_runoff', 'runoff', 'groundwater') else U)
    wadi = tri(r['feed_wadi'])
    nw = r['named_wadi'] or ''
    if r['kidron_feed'] == 'yes' or (nw and TRUNK.search(nw)):
        strict = M
    elif nw:
        strict = F
    else:
        strict = U
    plaster = tri(r['plaster'])
    branches = ['C-plaster', 'C-open'] if t == 'cistern' else ['M-well']
    for b in branches:
        for g, gc in (('G-strict', strict), ('G-loose', NS)):
            d = dict(channels=ch, wadi=wadi, great_wadi=gc)
            if b == 'C-plaster':
                d['plaster'] = plaster
            out.append(('45', f'{b}|{g}', d))
    return out


def e46(r, places):
    out = []
    if r['type'] not in ('reservoir_pool', 'cistern'):
        return out
    ent = M if r['entrance'] == 'yes' else U
    rr = places['ramat_rahel'][:2]
    for elig in eligibilities(r):
        for lim, lab in ((1.0, '1km'), (2.0, '2km')):
            out.append(('46', f'{elig}|B-RamatRahel-{lab}', dict(place=within(r, rr, lim), entrance=ent)))
            out.append(('46', f'{elig}|B-EinKerem-{lab}', dict(place=within(r, C.EIN_KAREM, lim), entrance=ent)))
        out.append(('46', f'{elig}|B-any', dict(entrance=ent)))
    return out


def score_row(r, places):
    res = []
    for fn in (e21, e22, e29, e32, e42, e45):
        res += fn(r)
    res += e46(r, places)
    return res


def combine(codes):
    """Group rule (plan §7): MATCH if any MATCH and no FAIL; FAIL if any FAIL and no MATCH; CONFLICT -> UNKNOWN."""
    codes = [c for c in codes if c != NS]
    if not codes:
        return NS
    if M in codes and F in codes:
        return 'CONFLICT'
    if M in codes:
        return M
    if F in codes:
        return F
    return U


def main():
    lane = C.LANE
    places = C.load_places()
    with open(os.path.join(lane, 'water.csv'), encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    with open(os.path.join(lane, 'merged_units.csv'), encoding='utf-8') as f:
        units = {u['unit_id']: u['row_ids'].split(';') for u in csv.DictReader(f)}
    by_id = {r['id']: r for r in rows}
    score_rows = []
    per_row = {}
    for r in rows:
        if r['in_box'] == 'no':
            continue
        for entry, branch, clauses in score_row(r, places):
            ov = overall(clauses.values())
            per_row.setdefault(r['id'], {})[(entry, branch)] = clauses
            score_rows.append(dict(id=r['id'], lineage=r['lineage'], type=r['type'], entry=entry, branch=branch,
                                   clauses=';'.join(f'{k}={v}' for k, v in clauses.items()), overall=ov,
                                   date_code=r['date_code'], in_box=r['in_box']))
    with open(os.path.join(lane, 'scores.csv'), 'w', newline='', encoding='utf-8') as f:
        cols = ['id', 'lineage', 'type', 'entry', 'branch', 'clauses', 'overall', 'date_code', 'in_box']
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        w.writerows(score_rows)

    # counts per lineage
    counts = {}

    def add(key, code, date_code, rule):
        c = counts.setdefault(key, dict(N=0, k=0, f=0, m=0))
        c['N'] += 1
        if not DATE_RULES[rule](date_code):
            c['f'] += 1
        elif code == M:
            c['k'] += 1
        elif code == F:
            c['f'] += 1
        else:
            c['m'] += 1

    for s in score_rows:
        lin = s['lineage'] if s['in_box'] == 'yes' else s['lineage'] + '-unplaced'
        for rule in DATE_RULES:
            add((s['entry'], s['branch'], lin, rule), s['overall'], s['date_code'], rule)
    # merged units
    merged_detail = []
    for u, ids in units.items():
        keys = set()
        for i in ids:
            keys |= set(per_row.get(i, {}))
        for key in sorted(keys):
            members = [per_row[i][key] for i in ids if key in per_row.get(i, {})]
            clause_names = sorted({c for m in members for c in m})
            comb = {c: combine([m.get(c, NS) for m in members]) for c in clause_names}
            codes = [U if v == 'CONFLICT' else v for v in comb.values()]
            ov = overall(codes)
            dates = [by_id[i]['date_code'] for i in ids]
            dc = 'in' if 'in' in dates else ('in_hedged' if 'in_hedged' in dates else
                                             ('partly' if 'partly' in dates else
                                              ('undated' if 'undated' in dates else 'out')))
            for rule in DATE_RULES:
                add((key[0], key[1], 'MERGED', rule), ov, dc, rule)
            merged_detail.append(dict(unit_id=u, entry=key[0], branch=key[1], overall=ov, date_code=dc,
                                      conflicts=';'.join(c for c, v in comb.items() if v == 'CONFLICT')))
    with open(os.path.join(lane, 'merged_scores.csv'), 'w', newline='', encoding='utf-8') as f:
        cols = ['unit_id', 'entry', 'branch', 'overall', 'date_code', 'conflicts']
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        w.writerows(sorted(merged_detail, key=lambda d: (d['entry'], d['branch'], d['unit_id'])))
    with open(os.path.join(lane, 'counts.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['entry', 'branch', 'lineage', 'date_rule', 'N', 'k_match', 'f_fail', 'm_unknown'])
        for key in sorted(counts):
            c = counts[key]
            w.writerow(list(key) + [c['N'], c['k'], c['f'], c['m']])
    headline(rows, units, per_row, merged_detail)


def headline(rows, units, per_row, merged_detail):
    """The brief's headline counts (plan §8), over in-box rows and over merged units."""
    inbox = [r for r in rows if r['in_box'] == 'yes']
    unit_rows = {u: [r for r in inbox if r['id'] in set(ids)] for u, ids in units.items()}
    out = []

    def both(label, pred_row):
        rows_hit = [r for r in inbox if pred_row(r)]
        units_hit = [u for u, rs in unit_rows.items() if any(pred_row(r) for r in rs)]
        out.append([label, len(rows_hit), len(units_hit)])

    def unit_branch(entry, branch):
        return sum(1 for d in merged_detail if d['entry'] == entry and d['branch'] == branch and d['overall'] == M)

    both('aqueduct rows (all)', lambda r: r['type'] == 'aqueduct')
    both('aqueducts with head recorded', lambda r: r['type'] == 'aqueduct' and r['head'] == 'yes')
    both('heads with a stone recorded', lambda r: r['type'] == 'aqueduct' and r['head'] == 'yes' and
         'stone' in (r['head_marker'] or ''))
    both('heads with any feature recorded', lambda r: r['type'] == 'aqueduct' and r['head'] == 'yes' and
         bool(r['head_marker']))
    both('heads with a stone or feature on the north side', lambda r: r['type'] == 'aqueduct' and
         r['head'] == 'yes' and bool(r['head_marker']) and r['marker_side'] == 'N')
    both('reservoirs/pools (all)', lambda r: r['type'] == 'reservoir_pool')
    both('reservoirs described or planned as great', lambda r: r['type'] == 'reservoir_pool' and r['great'] == 'yes')
    both('reservoirs described or planned as northern', lambda r: r['type'] == 'reservoir_pool' and
         r['north'] == 'yes')
    both('reservoirs great or northern', lambda r: r['type'] == 'reservoir_pool' and
         (r['great'] == 'yes' or r['north'] == 'yes'))
    both('reservoirs great and northern', lambda r: r['type'] == 'reservoir_pool' and r['great'] == 'yes' and
         r['north'] == 'yes')
    both('cisterns (all)', lambda r: r['type'] == 'cistern')
    both('cisterns fed by channels', lambda r: r['type'] == 'cistern' and
         r['feed'] in ('channel', 'wadi_diversion', 'aqueduct'))
    both('cisterns fed by channels from a wadi', lambda r: r['type'] == 'cistern' and
         r['feed'] in ('channel', 'wadi_diversion', 'aqueduct') and r['feed_wadi'] == 'yes')
    both('cisterns fed by channels from a great (trunk) wadi', lambda r: r['type'] == 'cistern' and
         r['feed'] in ('channel', 'wadi_diversion', 'aqueduct') and r['feed_wadi'] == 'yes' and
         (r['kidron_feed'] == 'yes' or bool(TRUNK.search(r['named_wadi'] or ''))))
    both('outlets/springs/aqueduct heads (entry 32 eligible)', lambda r: r['type'] in ('spring', 'outlet') or
         (r['type'] == 'aqueduct' and r['head'] == 'yes'))
    both('... at a named wadi', lambda r: (r['type'] in ('spring', 'outlet') or
                                         (r['type'] == 'aqueduct' and r['head'] == 'yes')) and bool(r['named_wadi']))
    both('... at Wadi Qelt', lambda r: (r['type'] in ('spring', 'outlet') or
                                      (r['type'] == 'aqueduct' and r['head'] == 'yes')) and r['qelt'] == 'yes')
    both('installations dated in the window (in or in_hedged)', lambda r: r['date_code'] in ('in', 'in_hedged'))
    both('installations dated in the window, unhedged', lambda r: r['date_code'] == 'in')
    out.append(['entry 21 S-stone|N-side MATCH (merged units)', '', unit_branch('21', 'S-stone|N-side')])
    out.append(['entry 21 S-any|N-side MATCH (merged units)', '', unit_branch('21', 'S-any|N-side')])
    with open(os.path.join(C.LANE, 'headline.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['count', 'rows_in_box', 'merged_units'])
        w.writerows(out)


if __name__ == '__main__':
    main()
