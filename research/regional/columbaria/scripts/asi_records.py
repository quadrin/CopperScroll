"""Read cached ASI records for the coder (PLAN.md §8). Nothing here is written into the repository.

Run:  python3 -I scripts/asi_records.py ASI_CACHE_DIR [site_id ...]
Prints, for each screened site in the region: map/site numbers, name, grid, Period, Finds, the English
description and the Hebrew sentences that hold a columbarium word.
"""
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colcommon as C  # noqa: E402

ROW = re.compile(r'<tr>\s*<td>\s*<b>(.*?)</b>\s*</td>\s*<td>(.*?)</td>\s*</tr>', re.S | re.I)
BLOCK = re.compile(r'<b>\s*(Description|Bibliography)\s*</b>\s*<br\s*/?>\s*(.*?)(?=<!--|<hr|<b>\s*(?:Description|Bibliography)\s*</b>|$)',
                   re.S | re.I)


def parse_site_desc(d):
    content = d.get('content') or ''
    fields = {}
    for k, v in ROW.findall(content):
        fields[C.clean(k).rstrip(':').strip()] = C.clean(v)
    for k, v in BLOCK.findall(content):
        fields[k.strip().title()] = C.clean(v)
    loc = d.get('location') or {}
    fields['_loc_lat'] = loc.get('X')
    fields['_loc_lon'] = loc.get('Y')
    fields['_name'] = C.clean(d.get('name'))
    return fields


def record(cache, sid):
    path = os.path.join(cache, C.cache_name('Service_Eng.aspx/GetSiteDesc2', Id=sid))
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        d = json.load(f)['d']
    if isinstance(d, str):
        d = json.loads(d)
    return parse_site_desc(d)


def hebrew_texts(cache, map_id):
    path = os.path.join(cache, C.cache_name('Service.aspx/GetPolygonsSites', MapId=map_id, sitesId='null'))
    with open(path, encoding='utf-8') as f:
        d = json.load(f)['d']
    if isinstance(d, str):
        d = json.loads(d)
    out = {}
    for ft in d['features']:
        p = C.geojson_props(ft)
        out[str(p.get('id'))] = (C.clean(p.get('name_heb')), C.clean(p.get('description_heb')), C.clean(p.get('finding_heb')))
    return out


def main():
    cache = sys.argv[1]
    only = set(sys.argv[2:])
    cands = list(csv.DictReader(open(os.path.join(C.FOLDER, 'data', 'candidates_asi.csv'), encoding='utf-8')))
    seen = {}
    for r in cands:
        if r['in_region'] != 'True':
            continue
        seen.setdefault(r['site_id'], r)
    heb_cache = {}
    for sid, r in sorted(seen.items(), key=lambda kv: (kv[1]['map_num'], int(kv[1]['site_num'] or 0))):
        if only and sid not in only:
            continue
        rec = record(cache, sid) or {}
        if r['map_id'] not in heb_cache:
            heb_cache[r['map_id']] = hebrew_texts(cache, r['map_id'])
        hn, hd, hf = heb_cache[r['map_id']].get(sid, ('', '', ''))
        print(f"==== ASI {r['map_num']}/{r['site_num']} id={sid} | {rec.get('_name', '')} | {hn}")
        for k in ('Additional names', 'Map', 'Site', 'New Israel Grid', 'WGS84', 'Period', 'Finds'):
            if rec.get(k):
                print(f'  {k}: {rec[k]}')
        print('  EN:', rec.get('Description', '(no record)'))
        sents = [s for s in re.split(r'(?<=[.!?])\s+', hd) if C.find_columbarium(s)]
        if sents:
            print('  HE:', ' || '.join(sents))


if __name__ == '__main__':
    main()
