#!/usr/bin/env python3
"""Build columbaria.csv from the screen tables and the hand coding (PLAN.md §5, §8).

Run:  python3 -I scripts/assemble.py
Reads data/candidates_asi.csv, data/candidates_wbadb.csv and data/coding.json. Standard library only.
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colcommon as C  # noqa: E402

DATA = os.path.join(C.FOLDER, 'data')
OUT = os.path.join(C.FOLDER, 'columbaria.csv')

DEFAULTS = dict(part='', n=1, cons='unknown', niches=None, setting='unknown', fort_at_site='no',
                tower_at_site='no', outside_fort=False, outside_tower=False, levels=None, lev2='U', lev3='U',
                lev_basis='', lev_pos='', acc='U', acc_basis='', part_of_site='', date='U', date_text='',
                natof='U', quote='', dup_of='', prio=2, exposed='no', post_freeze_source=False,
                tier1_related=False, uncertain=False, check=False, notes='', read_via='',
                post_freeze_override=None)

COLUMNS = ['id', 'source', 'source_ref', 'record_url', 'name', 'part', 'lat', 'lon', 'crs', 'coord_basis',
           'coord_precision_m', 'in_region', 'construction', 'levels', 'niche_count', 'n_columbaria',
           'setting', 'fort_at_site', 'tower_at_site', 'outside_fort', 'outside_tower', 'part_of_site',
           'lev2', 'lev3', 'lev_basis', 'lev_position', 'access', 'access_basis', 'site_periods',
           'date_code', 'date_text', 'dated_in_window', 'natof_text', 'quote', 'dup_of', 'priority',
           'uncertain_identification', 'exposed_before_freeze', 'post_freeze_source', 'post_freeze_override',
           'tier1_related', 'check_flag', 'read_via', 'notes']

WINDOW = {'D': 'yes', 'L': 'no', 'P': 'partly', 'U': 'unknown'}


def load_csv(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def asi_index():
    out = {}
    for r in load_csv('candidates_asi.csv'):
        if r['site_id'] not in out or r['lang'] == 'en':
            prev = out.get(r['site_id'], {})
            merged = dict(prev)
            merged.update({k: v for k, v in r.items() if v not in ('', None)})
            out[r['site_id']] = merged
    return out


def yn(v):
    return 'yes' if v is True or v == 'yes' else ('no' if v in (False, 'no', None, '') else str(v))


def build():
    with open(os.path.join(DATA, 'coding.json'), encoding='utf-8') as f:
        coding = json.load(f)
    asi = asi_index()
    wb = {r['row_id']: r for r in load_csv('candidates_wbadb.csv')}
    rows = []
    for c in coding['rows']:
        r = dict(DEFAULTS)
        r.update(c)
        src = r['src']
        out = dict(id=r['cid'], source=src, part=r['part'], crs='EPSG:4326')
        if src == 'ASI':
            a = asi[r['key']]
            out['name'] = a.get('record_name') or a.get('name', '')
            out['source_ref'] = (f"ASI Map {a['map_num']}, site {a['site_num']} (survey.iaa.org.il record {a['site_id']}); "
                                 f"printed page not given online")
            out['record_url'] = f"https://survey.iaa.org.il/#/MapSurvey/{a['map_id']}/site/{a['site_id']}"
            out['lat'], out['lon'] = round(float(a['lat']), 6), round(float(a['lon']), 6)
            out['coord_basis'] = 'ASI database point of the site record (WGS 84); NIG ' + a.get('record_nig', '')
            out['coord_precision_m'] = 100
            out['site_periods'] = a.get('record_period', '')
        elif src == 'WBADB':
            w = wb[r['key']]
            out['name'] = w['name'] or w['other_names']
            ref = w['survey_ref'] or 'excavation sheet'
            out['source_ref'] = f"WBADB {w['row_id']} ({ref})"
            out['record_url'] = 'https://emekshaveh.org/en/wp-content/uploads/2020/08/WBADB_data1.xlsx'
            out['lat'], out['lon'] = float(w['lat']), float(w['lon'])
            out['coord_basis'] = (f"WBADB X/Y {w['x']}/{w['y']} (Old Israel Grid without false northing) "
                                  f"-> EPSG:28193 -> EPSG:4326 (pyproj)")
            out['coord_precision_m'] = 100
            out['site_periods'] = '; '.join(p for p in (w['major_periods'], w['other_periods']) if p and p != '-')
        else:
            out['name'] = r.get('name', '')
            out['source_ref'] = r.get('ref', '')
            out['record_url'] = ''
            out['lat'], out['lon'] = r.get('lat'), r.get('lon')
            out['coord_basis'] = r.get('coord_src', '')
            out['coord_precision_m'] = r.get('p_m')
            out['site_periods'] = ''
        out['in_region'] = yn(C.in_region(out['lon'], out['lat'])) if out['lat'] is not None else 'unplaced'
        out.update(construction=r['cons'], levels=r['levels'], niche_count=r['niches'], n_columbaria=r['n'],
                   setting=r['setting'], fort_at_site=yn(r['fort_at_site']), tower_at_site=yn(r['tower_at_site']),
                   outside_fort=yn(r['outside_fort']), outside_tower=yn(r['outside_tower']),
                   part_of_site=r['part_of_site'], lev2=r['lev2'], lev3=r['lev3'], lev_basis=r['lev_basis'],
                   lev_position=r['lev_pos'], access=r['acc'], access_basis=r['acc_basis'],
                   date_code=r['date'], date_text=r['date_text'], dated_in_window=WINDOW[r['date']],
                   natof_text=r['natof'], quote=r['quote'], dup_of=r['dup_of'], priority=r['prio'],
                   uncertain_identification=yn(r['uncertain']), exposed_before_freeze=r['exposed'],
                   post_freeze_source=yn(r['post_freeze_source']),
                   post_freeze_override=json.dumps(r['post_freeze_override'], ensure_ascii=False)
                   if r['post_freeze_override'] else '',
                   tier1_related=yn(r['tier1_related']), check_flag=yn(r['check']), read_via=r['read_via'],
                   notes=r['notes'])
        rows.append(out)
    return rows, coding.get('excluded', [])


def validate(rows):
    ids = [r['id'] for r in rows]
    assert len(ids) == len(set(ids)), 'duplicate ids'
    known = set(ids)
    for r in rows:
        assert not r['dup_of'] or r['dup_of'] in known, r['id']
        assert len(str(r['quote']).split()) <= 12, (r['id'], 'quote longer than 12 words')
        assert r['date_code'] in WINDOW and r['lev2'] in 'MFU' and r['lev3'] in 'MFU' and r['access'] in 'MFU'


def write(rows, out=OUT):
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: ('' if r.get(k) is None else r.get(k)) for k in COLUMNS})


def main(out_dir=None):
    rows, excluded = build()
    validate(rows)
    write(rows, os.path.join(out_dir, 'columbaria.csv') if out_dir else OUT)
    with open(os.path.join(out_dir or DATA, 'excluded.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['src', 'key', 'label', 'reason'], lineterminator='\n')
        w.writeheader()
        w.writerows(excluded)
    counted = [r for r in rows if not r['dup_of']]
    print(f'{len(rows)} rows, {len(counted)} not duplicates, {len(excluded)} excluded records')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
