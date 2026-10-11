#!/usr/bin/env python3
"""Exploratory amendment 1 (PLAN_AMENDMENT_1_exploratory.md): orientation with the survey's direction
abbreviations, and pillars at a tomb's entrance. Written after the frozen build was inspected, so every
result here is exploratory and is reported beside, never instead of, the frozen result.

Run from the repository root:
    python3 -I research/regional/tombs/scripts/amendment1.py ASI_CACHE WBADB_XLSX [OUT_DIR]
Writes amendment1_codes.csv, amendment1_scores_summary.csv and (if checks are missing)
amendment1_check_pending.csv. Manual decisions: data/manual_check_amendment1.csv.
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tombs_common as T  # noqa: E402
import build_tombs as B  # noqa: E402

ABBR = {'N': 'N', 'S': 'S', 'E': 'E', 'W': 'W', 'NE': 'NE', 'NW': 'NW', 'SE': 'SE', 'SW': 'SW'}
WINDOW = 4
ENTRANCE_PLACE = T.term_regex(['entrance', 'entrances', 'forecourt', 'antechamber', 'ante-chamber', 'vestibule',
                               'courtyard', 'porch', 'portico', 'facade', 'façade'])
PILLAR = T.term_regex(['pillar', 'pillars', 'column', 'columns'])
BRANCHES = {
    '51-S': ['L_south_corner', 'name_zadok', 'F2xa'],
    '51-O': ['F12', 'name_zadok', 'F2xa'],
    '51-J': ['L_south_corner', 'F2xa'],
    '52-M': ['F7wa', 'F6', 'F14', 'F17'],
    '52-P-proxy': ['F7wa', 'F14'],
    '56-P': ['F10', 'F7wa', 'F11'],
    '56-M': ['F10', 'F7wa', 'F16'],
}


def tokens(s):
    return [m for m in re.finditer(r"[A-Za-zÀ-ÿʿ’'ḥḤṣṢ]+", s)]


def orientation(plan, s):
    """Directions within WINDOW tokens of an opening term in one sentence."""
    words = {}
    for code, ws in plan['direction_terms'].items():
        for w in ws:
            words[w.lower()] = code
    opening = {t.lower() for t in plan['opening_terms']}
    toks = tokens(s)
    low = [t.group(0).lower() for t in toks]
    # compound written with a hyphen (north-west) appears as two tokens: join them first
    dirs = []
    open_idx = [i for i, w in enumerate(low) if w in opening or w.rstrip('s') in opening or w in ('facade', 'façade')]
    for i, t in enumerate(toks):
        raw = t.group(0)
        code = None
        if raw in ABBR:
            code = ABBR[raw]
        elif low[i] in words:
            code = words[low[i]]
            if i + 1 < len(low) and code in ('N', 'S') and low[i + 1] in ('east', 'west', 'eastern', 'western'):
                code = code + ('E' if low[i + 1].startswith('east') else 'W')
        if code and any(abs(i - j) <= WINDOW for j in open_idx):
            dirs.append((code, i))
    out = []
    for code, _ in dirs:
        if code not in out:
            out.append(code)
    return out


def main(cache, xlsx, out_dir):
    plan, coder, elig, sheets, _ = B.build_units(cache, xlsx)
    checks = {}
    p = os.path.join(B.DATA, 'manual_check_amendment1.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                checks[(r['record_id'], r['code'])] = r
    pending, rows = [], []
    for u in elig:
        if u['lat'] is None:
            continue
        sents = T.sentences(u['text'])
        dirs, trig = [], []
        for s in sents:
            d = orientation(plan, s)
            if d:
                dirs += [x for x in d if x not in dirs]
                trig.append(s)
        if not dirs:
            f7wa = 'unknown'
        elif any(x in plan['westerly'] for x in dirs):
            f7wa = 'yes'
        elif u['multi_tomb_record'] == 'yes':
            f7wa = 'unknown'   # A1b: a unit with several tombs cannot exclude a westerly entrance
        else:
            f7wa = 'no'
        f2xa = 'yes' if (u['F2x'] == 'yes' or any(ENTRANCE_PLACE.search(s) and PILLAR.search(s) for s in sents)) else 'unknown'
        raw = dict(F7wa=f7wa, F2xa=f2xa)
        rej = ''
        for code in ('F7wa', 'F2xa'):
            v = raw[code]
            if v in ('yes', 'no') and not (code == 'F2xa' and u['F2x'] == 'yes'):
                ck = checks.get((u['record_id'], code))
                if ck is None:
                    pending.append((u['record_id'], code, v))
                elif ck['decision'] == 'reject':
                    raw[code] = 'unknown'
                    rej += f"{code}: {ck['reason']}; "
                elif ck['decision'] == 'set_no':
                    raw[code] = 'no'
                    rej += f"{code} set to no: {ck['reason']}; "
        u['F7wa'], u['F2xa'] = raw['F7wa'], raw['F2xa']
        rows.append(dict(unit_id=u['unit_id'], record_id=u['record_id'], F7a=';'.join(dirs) or 'unknown',
                         F7wa_raw=f7wa, F7wa=u['F7wa'], F2xa_raw=f2xa, F2xa=u['F2xa'], rejected=rej,
                         exposure=u['exposure']))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'amendment1_codes.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: r['unit_id']))
    if pending:
        with open(os.path.join(out_dir, 'amendment1_check_pending.csv'), 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, lineterminator='\n')
            w.writerow(['record_id', 'code', 'raw'])
            w.writerows(sorted(pending))
    # scores
    located = [u for u in elig if u['lat'] is not None]

    def val(u, c, sens):
        if c in ('F7wa', 'F2xa'):
            return u[c]
        return B.clause_value(plan, u, c, sens)
    out = []
    # A3: WBADB "Rom1" read as Early Roman (INFERENCE from Rom1/Rom2; the WBADB codebook was not read)
    for u in located:
        u['rom1'] = u['source'] == 'WBADB' and bool(re.search(r'(?<![A-Za-z])Rom1', u['period_text'] or ''))
    for b, cl in list(BRANCHES.items()) + [('ALL-TOMBS', [])]:
        for reg in ('A', 'A3', 'B', 'AB'):
            for ds in plan['date_sets'] + ['strict+Rom1']:
                us = [u for u in located if not u['possible_duplicate_of'] and {
                    'A': u['in_A'], 'A3': u['in_A3'], 'B': u['in_B1'] or u['in_B2'],
                    'AB': u['in_A'] or u['in_B1'] or u['in_B2']}[reg] and {
                    'strict': u['dated_in_window'] == 'yes', 'lenient': u['dated_lenient'] == 'yes', 'any': True,
                    'strict+Rom1': u['dated_in_window'] == 'yes' or u['rom1']}[ds]]
                res = []
                for u in us:
                    vs = [val(u, c, False) for c in cl]
                    res.append((u, vs, B.overall(vs), B.overall([val(u, c, True) for c in cl])))
                cc = ' '.join(f"{c}:{sum(r[1][i] == 'yes' for r in res)}/{sum(r[1][i] == 'no' for r in res)}/"
                              f"{sum(r[1][i] == 'unknown' for r in res)}" for i, c in enumerate(cl))
                out.append(dict(branch=b, region=reg, date_set=ds, view='all_lineages', N=len(res),
                                k_match=sum(r[2] == 'match' for r in res), f_fail=sum(r[2] == 'fail' for r in res),
                                m_unknown=sum(r[2] == 'unknown' for r in res),
                                k_sens=sum(r[3] == 'match' for r in res), clause_counts=cc,
                                matches=';'.join(r[0]['record_id'] for r in res if r[2] == 'match') if cl else '(N only)',
                                matches_sens=';'.join(r[0]['record_id'] for r in res if r[3] == 'match' and r[2] != 'match')))
    with open(os.path.join(out_dir, 'amendment1_scores_summary.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(out)
    print(f'amendment rows: {len(rows)}; pending checks: {len(pending)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else T.FOLDER)
