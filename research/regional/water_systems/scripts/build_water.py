#!/usr/bin/env python3
"""Build water.csv from survey_rows.csv, site_points.csv and the hand-coded literature rows (plan §3-§8).

Run from the repository root (standard library only):
  python3 -I research/regional/water_systems/scripts/build_water.py
Writes water.csv and merged_units.csv in the lane folder.
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
import literature_data as L  # noqa: E402
import literature_data_2  # noqa: E402,F401  (registers its rows)

# Site aliases for literature -> survey supersession (plan §7): names of survey records that describe the same site.
SITE_ALIASES = {
    'doq': r'\bdo[qk]\b|qarantal|quruntul|dagon',
    'cypros': r'cypros|kypros|tell? el-?aqaba',
    'hyrcania': r'hyrcania|mird|sekhakha|castellion',
    'herodium': r'herod',
    'kh_qumran': r'qumran',
    'jericho_palaces': r"ala[iy]i?q|alayik|tulul abu|winter palace",
    'jericho_estate': r"ala[iy]i?q|alayik|tulul abu|winter palace",
    'solomons_pools': r'solomon|khawkh|bura[qk]',
    'arrub': r"arr?[uo]b\b|kuweiz|dilb",
    'artas': r'artas|urtas',
    'birket_musa': r'birk\w* mus',
    'ein_fara': r'\bfara\b|farah|perat|prat\b',
    'ein_fawwar': r'faw+ar',
    'martyrius': r'murassas|martyri',
    'chariton': r'khureitun|khareitun|chariton',
    'mar_saba': r'mar saba',
    'euthymius': r'euthym|khan el.ahmar',
    'qasr_el_yahud': r'qa.r el.yahud',
    'tell_es_sultan': r'sultan',
    'jer_siloam': r'siloam|shilo|silwan|hamra|city of david',
    'ramat_rahel': r'ramat ra|zewaha|salih',
    'choziba': r'qelt|choziba|jiryis|george',
    'tell_el_qos': r'\bqos\b',
    'mafjar': r'mafjar',
    'suwwanet': r'suwwanet|thaniya',
    'beit_jabr': r'jabr',
    'ziyar_el_ghanam': r'ziyar|siyar|ghanam|shepherd',
    'mar_elias': r'elias|ilyas',
}
QUMRAN_RX = re.compile(r'qumran|sekaka|secacah|buqei', re.I)
JERICHO_RX = re.compile(r"jericho|sultan|alayiq|alaiq|naaran|nueima|\bdoq\b|\bdok\b|dagon|qarantal|cypros|kypros|"
                        r"mafjar|aqaba", re.I)
CYPROS_RX = re.compile(r'cypros|kypros|tell? el-?aqaba', re.I)
OASIS_KEYS = {'jericho_palaces', 'jericho_estate', 'birket_musa', 'tell_es_sultan', 'cypros', 'doq', 'mafjar',
              'tell_el_qos', 'jericho_town', 'jericho_oasis_other', 'nitla', 'suwwanet'}


def read_csv(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def load_points():
    pts = {}
    for r in read_csv(os.path.join(C.LANE, 'site_points.csv')):
        pts[r['key']] = (float(r['lat']), float(r['lon']), float(r['precision_m']), r['label'])
    return pts


def resolve(pt, pts, places):
    """Return (lat, lon, precision_m, coord_source) or (None, None, None, 'unplaced')."""
    if not pt:
        return None, None, None, 'unplaced'
    if pt[0] == 'place':
        lat, lon, sig = places[pt[1]]
        return lat, lon, sig * 1000.0, f'places_v2 {pt[1]} (sigma {sig} km; plan §6 rule 3)'
    key = {'wbadb': f'wbadb:{pt[1]}', 'asi': f'asi:{pt[1]}', 'oig': f'oig:{pt[1]},{pt[2]}' if len(pt) > 2 else ''}[pt[0]]
    lat, lon, prec, label = pts[key]
    if pt[0] == 'oig':
        return lat, lon, prec, 'source grid reference converted from EPSG:28191 (plan §6 rule 1)'
    return lat, lon, prec + 250.0, f'{label} (plan §6 rule 2: record precision + 250 m)'


REPO_TEXT = {  # literature read through a repository file: hash that file
    'PAT89': 'registration/christmas_hyrcania_primary_features_2026-09-30.json',
    'MP18': 'registration/magen2018_extracted.md',
    'E29INV': 'research/assessments/entry29_jericho_pools/regional_inventory_2026-10-06.csv',
    'SIL': 'research/measurements/cycle15/siloam_bathing.md',
    'RR': 'research/sites/site_identification_review.md',
}


def text_hashes():
    out = {}
    for r in read_csv(os.path.join(C.LANE, 'sources_read.csv')):
        out[r['key']] = r['text_read_sha256']
    for k, rel in REPO_TEXT.items():
        out[k] = C.sha256_file(os.path.join(C.REPO, rel))
    return out


def lit_rows(places):
    pts = load_points()
    hashes = text_hashes()
    out = []
    for r in L.ROWS:
        lat, lon, prec, csrc = resolve(r['pt'], pts, places)
        row = {k: '' for k in C.COLUMNS}
        for k in C.COLUMNS:
            if k in r and r[k] is not None:
                row[k] = str(r[k])
        row.update(lineage='LIT', source=L.SOURCES[r['src']], record_id=r['id'], locator=r['locator'],
                   lat=f'{lat:.6f}' if lat is not None else '', lon=f'{lon:.6f}' if lon is not None else '',
                   crs='EPSG:4326' if lat is not None else '', precision_m=f'{prec:.0f}' if prec is not None else '',
                   coord_source=csrc, first_read_after_freeze='', span_sha256=hashes.get(r['src'], ''),
                   site_period_in_window='', excavated='')
        text = ' '.join([r['name'], r['site_key'], r['named_wadi'], r['notes']])
        # place columns (amendment 1 §3): coder values win; otherwise names, then distances
        if lat is not None:
            dq = min(C.km(lat, lon, *places['kh_qumran'][:2]), C.km(lat, lon, *places['wadi_qumran'][:2]))
            db = C.km(lat, lon, *places['buqeia'][:2])
            row['qumran'] = 'yes' if (QUMRAN_RX.search(text) or dq <= 1.0 or db <= 2.5) else 'no'
            dj = min(C.km(lat, lon, *places[p][:2]) for p in ('tell_es_sultan', 'jericho_palaces', 'doq', 'ain_duk'))
            row['jericho_oasis'] = 'yes' if (JERICHO_RX.search(text) or dj <= 2.0 or
                                             r['site_key'] in OASIS_KEYS) else 'no'
            row['cypros'] = 'yes' if (CYPROS_RX.search(text) or r['site_key'] == 'cypros') else 'no'
        else:
            row['qumran'] = 'yes' if QUMRAN_RX.search(text) else 'unknown'
            row['jericho_oasis'] = 'yes' if (JERICHO_RX.search(text) or r['site_key'] in OASIS_KEYS) else 'unknown'
            row['cypros'] = 'yes' if (CYPROS_RX.search(text) or r['site_key'] == 'cypros') else 'unknown'
        if r['dest_pt']:
            dlat, dlon, dprec, _ = resolve(r['dest_pt'], pts, places)
            row['notes'] = (row['notes'] + '; ' if row['notes'] else '') + \
                f'destination point {dlat:.6f},{dlon:.6f} (precision {dprec:.0f} m)'
            row['dest_lat'], row['dest_lon'], row['dest_prec'] = f'{dlat:.6f}', f'{dlon:.6f}', f'{dprec:.0f}'
        row['covered_by'] = r['covered_by']  # aggregate described in more detail by these groups (plan §7)
        row['near_bend_m'] = '' if r['near_bend_m'] is None else str(r['near_bend_m'])
        row['fissure_m'] = '' if r['fissure_m'] is None else str(r['fissure_m'])
        out.append(row)
    return out


def supersede(survey, lit):
    """Survey rows of the same type, matching a literature site's aliases within 1 km (plan §7)."""
    by_site = {}
    for r in lit:
        if r['lat']:
            by_site.setdefault(r['site_key'], []).append(r)
    for s in survey:
        if not s['lat']:
            continue
        slat, slon = float(s['lat']), float(s['lon'])
        for key, rows in by_site.items():
            rx = SITE_ALIASES.get(key)
            if not rx or not re.search(rx, C.fold(s['name']) + ' ' + C.fold(s['notes']), re.I):
                continue
            same = [r for r in rows if r['type'] == s['type']]
            if not same:
                continue
            if min(C.km(slat, slon, float(r['lat']), float(r['lon'])) for r in same) <= 1.0:
                s['superseded_by'] = 'LITSITE:' + key
                break


EXTRA = ['near_bend_m', 'fissure_m', 'dest_lat', 'dest_lon', 'dest_prec', 'in_box', 'covered_by']

# Exposure (plan §10): was the record already read in the repository before this lane?
LIT_FIRST_READ = {'MAZ89': 'yes', 'DAM89': 'yes', 'HIR89': 'yes', 'TSA75': 'yes'}  # all other sources: 'no'


def exposure(rows):
    path = os.path.join(C.REPO, 'research', 'regional', 'asi_jerusalem', 'sites.csv')
    seen = {f"{r['map_num']}/{r['site_num']}" for r in read_csv(path)}
    src_key = {v: k for k, v in L.SOURCES.items()}
    for r in rows:
        if r['lineage'] == 'ASI':
            r['first_read_after_freeze'] = 'no' if r['record_id'] in seen else 'yes'
        elif r['lineage'] == 'WBADB':
            r['first_read_after_freeze'] = 'no'  # whole file screened by the kohlit stage 1 (8 October)
        elif r['lineage'] == 'HAESI':
            r['first_read_after_freeze'] = 'no'
        else:
            r['first_read_after_freeze'] = LIT_FIRST_READ.get(src_key.get(r['source'], ''), 'no')
        if re.search(r'\balmit\b', C.fold(r['name'])):
            # plan §3.5: survey rows on Kh. Almit (a Tier 1 site of the arrival register) are flagged; they are
            # WBADB/ASI summary records, not the protected IAA notices, which were not read
            r['first_read_after_freeze'] = 'yes (Kh. Almit flag)'


def main():
    survey = read_csv(os.path.join(C.LANE, 'survey_rows.csv'))
    places = C.load_places()
    lit = lit_rows(places)
    for s in survey:
        for k in EXTRA:
            s.setdefault(k, '')
    supersede(survey, lit)
    rows = survey + lit
    exposure(rows)
    for r in rows:
        if r['lat']:
            r['in_box'] = 'yes' if C.in_box(float(r['lat']), float(r['lon'])) else 'no'
        else:
            r['in_box'] = 'unplaced'
    cols = C.COLUMNS + EXTRA
    with open(os.path.join(C.LANE, 'water.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in cols})
    # merged units (plan §7): literature groups, then survey rows neither duplicated nor superseded
    units = {}
    for r in rows:
        if r['in_box'] != 'yes':  # rows outside the box, and unplaced rows (plan §6), are not merged
            continue
        if r['lineage'] == 'LIT':
            if r.get('covered_by'):
                continue  # an aggregate whose members are counted as their own units
            u = r['group_id'] or r['id']
        elif r['dup_of'] or r['superseded_by']:
            continue
        else:
            u = r['id']
        units.setdefault(u, []).append(r['id'])
    with open(os.path.join(C.LANE, 'merged_units.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['unit_id', 'n_rows', 'row_ids'])
        for u in sorted(units):
            w.writerow([u, len(units[u]), ';'.join(units[u])])
    print(len(survey), len(lit), len(units), file=sys.stderr)


if __name__ == '__main__':
    main()
