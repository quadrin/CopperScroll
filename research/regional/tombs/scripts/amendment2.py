#!/usr/bin/env python3
"""Exploratory Amendment 2 (PLAN_AMENDMENT_2_exploratory.md, Part B), plus two post-reading views of source HK.

Part B: the three Akeldama burial caves (Avni and Greenhut 1996, IAA Reports 1), which are not in the frozen source
list, are coded with the frozen Coder and scored with the frozen clause rules, but never enter tombs.csv, scores.csv or
scores_summary.csv. The frozen Region A headline is unchanged; this script reports what Region A counts would be if
the caves were added.

Part C (chosen after the HK tombs had been coded, so exploratory): Region B with the HK tombs in place of the two
cemetery-level WBADB rows (S2446, E349), and the HK tombs with a 1.6 km position uncertainty (INFERENCE: the report's
"16 km long" cemetery, p. 166, is probably a misprint for 1.6 km).

Run from the repository root:
    python3 -I research/regional/tombs/scripts/amendment2.py ASI_CACHE WBADB_XLSX [OUT_DIR]
Writes amendment2_akeldama_units.csv and amendment2_scores_summary.csv. Manual decisions for the caves:
data/manual_check_amendment2.csv (same codes as the frozen check, PLAN §5).
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tombs_common as T  # noqa: E402
import build_tombs as B  # noqa: E402

AK_ANCHOR = 'ASI 102/484'   # the ASI record whose text names the 1989 Avni and Greenhut caves (Part B.2)
AK_REF = 'Avni and Greenhut 1996, The Akeldama Tombs (IAA Reports 1)'
HK_SENS_UNC_KM = 1.6
CEMETERY_ROWS = ('WBADB S2446', 'WBADB E349')


def akeldama_units(plan, coder, elig):
    anchor = [u for u in elig if u['record_id'] == AK_ANCHOR][0]
    checks = {}
    with open(os.path.join(B.DATA, 'manual_check_amendment2.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            checks[(r['record_id'], r['code'])] = r
    prim = [u for u in elig if u['lat'] is not None and (u['source'] == 'ASI' or (
        u['source'] == 'WBADB' and u['in_asi_sheet'] == 'no' and not u.get('wbadb_excavation_also_surveyed')))]
    out, pending = [], []
    with open(os.path.join(B.DATA, 'akeldama_units.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            u = dict(source='AK', record_id=f"AK {r['record_id']}", name=f"Akeldama {r['record_id']}",
                     locator=f"{AK_REF}, pp. {r['pages']}; {r['figures']}; {r['inscriptions']}; {r['note']}",
                     lat=anchor['lat'], lon=anchor['lon'], unc=plan['position_uncertainty_km']['ASI'],
                     text=r['text'], period_text=None, flags=(), text_hash=T.sha256_text(r['text']))
            u.update(T.region_flags(plan, u['lat'], u['lon']))
            u.update(coder.code(u['text']))
            u['manual_rejected'] = ''
            for code in B.MANUAL_CODES:
                u[code + '_raw'] = u[code]
                if u[code] == 'yes':
                    ck = checks.get((u['record_id'], code))
                    if ck is None:
                        pending.append((u['record_id'], code))
                    elif ck['decision'] == 'reject':
                        u[code] = 'unknown'
                        u['manual_rejected'] += f"{code}: {ck['reason']}; "
            best = None
            for p in prim:
                d = T.km(u['lat'], u['lon'], p['lat'], p['lon'])
                if d <= plan['duplicate_km'] and (best is None or d < best[0]):
                    best = (d, p['record_id'])
            u['possible_duplicate_of'] = best[1] if best else ''
            u['exposure'] = ('exploratory addition (Amendment 2), first read on 11 Oct after the freeze; the same caves '
                             'are summarised in ASI 102/484, which the ASI lane coded')
            out.append(u)
    if pending:
        raise SystemExit(f'manual checks missing in data/manual_check_amendment2.csv: {pending}')
    return out


def score(plan, units, branches, sens=False):
    res = {}
    for b, spec in branches.items():
        for u in units:
            vals = [B.clause_value(plan, u, c, sens) for c in spec['clauses']]
            res[(u['record_id'], b)] = (vals, B.overall(vals))
    return res


def in_region(u, reg):
    return {'A': u['in_A'], 'A3': u['in_A3'], 'B': u['in_B1'] or u['in_B2'], 'B1': u['in_B1'], 'B2': u['in_B2'],
            'AB': u['in_A'] or u['in_B1'] or u['in_B2']}[reg]


def in_dateset(u, ds):
    return {'strict': u['dated_in_window'] == 'yes', 'lenient': u['dated_lenient'] == 'yes', 'any': True}[ds]


def main(cache, xlsx, out_dir):
    plan, coder, elig, sheets, _ = B.build_units(cache, xlsx)
    located = [u for u in elig if u['lat'] is not None]
    branches = {b: s for b, s in plan['branches'].items() if s['clauses']}
    ak = akeldama_units(plan, coder, elig)

    # ---- the caves, unit by unit
    ak_res = score(plan, ak, branches)
    ucols = ['record_id', 'name', 'locator', 'lat', 'lon', 'crs', 'position_uncertainty_km', 'd_temple_km',
             'possible_duplicate_of', 'dated_in_window', 'dated_lenient', 'period_terms', 'F1', 'F2', 'F2x', 'F3', 'F4',
             'F5', 'F6', 'F7', 'F7w', 'F10', 'F11', 'F12', 'F13', 'F14', 'F16', 'F17', 'F19', 'F20_communal', 'F21',
             'name_zadok', 'name_absalom', 'name_queen', 'name_obed', 'name_jericho', 'raw_yes_before_check',
             'manual_rejected', 'branch_results', 'exposure', 'text_sha256']
    rows = []
    for u in ak:
        r = {}
        for c in ucols:
            if c == 'crs':
                r[c] = 'EPSG:4326'
            elif c == 'position_uncertainty_km':
                r[c] = u['unc']
            elif c in ('lat', 'lon'):
                r[c] = f"{u[c]:.6f}"
            elif c == 'd_temple_km':
                r[c] = f"{u[c]:.3f}"
            elif c == 'raw_yes_before_check':
                r[c] = ';'.join(k for k in B.MANUAL_CODES if u.get(k + '_raw') == 'yes')
            elif c == 'branch_results':
                r[c] = ';'.join(f"{b}={ak_res[(u['record_id'], b)][1]}" for b in branches)
            elif c == 'text_sha256':
                r[c] = u['text_hash']
            else:
                r[c] = u.get(c, '')
        rows.append(r)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'amendment2_akeldama_units.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=ucols, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

    # ---- summaries
    def summarise(view, part, units, regions, sens_units=None):
        res = score(plan, units, branches)
        sres = score(plan, units, branches, sens=True)
        out = []
        for b, spec in branches.items():
            for reg in regions:
                for ds in plan['date_sets']:
                    us = [u for u in units if in_region(u, reg) and in_dateset(u, ds)]
                    rr = [res[(u['record_id'], b)] for u in us]
                    sr = [sres[(u['record_id'], b)] for u in us]
                    cc = ' '.join(f"{c}:{sum(v[0][i] == 'yes' for v in rr)}/{sum(v[0][i] == 'no' for v in rr)}/"
                                  f"{sum(v[0][i] == 'unknown' for v in rr)}" for i, c in enumerate(spec['clauses']))
                    out.append(dict(part=part, view=view, branch=b, region=reg, date_set=ds, N=len(rr),
                                    k_match=sum(v[1] == 'match' for v in rr), f_fail=sum(v[1] == 'fail' for v in rr),
                                    m_unknown=sum(v[1] == 'unknown' for v in rr),
                                    k_sens=sum(v[1] == 'match' for v in sr), clause_counts=cc,
                                    matches=';'.join(u['record_id'] for u, v in zip(us, rr) if v[1] == 'match')))
        return out

    union = [u for u in located if not u['possible_duplicate_of']]
    summary = []
    regA = ('A', 'A3', 'AB')
    summary += summarise('frozen union (unchanged headline)', 'B', union, regA)
    summary += summarise('union + caves, frozen duplicate rule', 'B', union + [u for u in ak if not u['possible_duplicate_of']], regA)
    summary += summarise('union + caves as new units', 'B', union + ak, regA)
    summary += summarise('caves alone', 'B', ak, regA)

    hk = [u for u in located if u['source'] == 'HK']
    hk16 = [dict(u, unc=HK_SENS_UNC_KM) for u in hk]
    regB = ('B', 'B1', 'B2')
    base = [u for u in union if u['record_id'] not in CEMETERY_ROWS]
    summary += summarise('frozen union (unchanged headline)', 'C', union, regB)
    summary += summarise('HK alone, 16 km', 'C', hk, regB)
    summary += summarise('HK alone, 1.6 km', 'C', hk16, regB)
    summary += summarise('union, HK tombs replace S2446 and E349, 16 km', 'C', base + hk, regB)
    summary += summarise('union, HK tombs replace S2446 and E349, 1.6 km', 'C', base + hk16, regB)
    with open(os.path.join(out_dir, 'amendment2_scores_summary.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(summary)
    print(f'akeldama units: {len(ak)}; duplicates: {sum(bool(u["possible_duplicate_of"]) for u in ak)}; '
          f'summary rows: {len(summary)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else T.FOLDER)
