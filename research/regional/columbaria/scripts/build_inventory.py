#!/usr/bin/env python3
"""Screen S1 (ASI online, cached) and S2 (WBADB) for columbarium words (PLAN.md §4, §5, Appendix A).

Run:  python3 -I scripts/build_inventory.py ASI_CACHE_DIR WBADB_XLSX
Writes data/candidates_asi.csv and data/candidates_wbadb.csv: one row per screened record with a
columbarium word, its point (WGS 84), region test, matched terms and clause-flag words. No description
text is written. The hand coding (data/coding.json) refers to these rows by candidate id.
"""
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colcommon as C  # noqa: E402

WBADB_SHA256 = '3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b'
WBADB_FIELDS = ['Site_Name', 'Other_Names', 'Site_Components', 'More_Components', 'Comments', 'More_Comments']
DATA = os.path.join(C.FOLDER, 'data')


# ------------------------------------------------------------------ S1 ASI
def selected_maps(cache):
    with open(os.path.join(cache, 'Service_Eng_GetMaps.json'), encoding='utf-8') as f:
        maps = json.load(f)['d']
    with open(os.path.join(cache, 'GetIsraelGrid.json'), encoding='utf-8') as f:
        grid = json.load(f)
    online = {str(m['id']): m for m in maps}
    return C.sheets_in_region(grid, online), online


def _load(cache, endpoint, **params):
    path = os.path.join(cache, C.cache_name(endpoint, **params))
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _gj(d):
    d = d.get('d') if isinstance(d, dict) else d
    if isinstance(d, str):
        d = json.loads(d)
    return d


def asi_text(props):
    """All screenable text of a GeoJSON feature: every string property except bibliography."""
    parts = []
    for k, v in sorted(props.items()):
        if v is None or 'bibl' in str(k).lower() or k in ('icon', 'id', 'gis_map_id', 'site_num'):
            continue
        parts.append(C.clean(v))
    return ' | '.join(p for p in parts if p)


def asi_screen(cache):
    sel, online = selected_maps(cache)
    out = []
    for mid, mapnum in sel:
        for lang, ep in (('en', 'Service_Eng.aspx/GetPolygonsSites'), ('he', 'Service.aspx/GetPolygonsSites')):
            d = _load(cache, ep, MapId=mid, sitesId='null')
            if d is None:
                continue
            gj = _gj(d)
            for ft in gj.get('features', []):
                props = C.geojson_props(ft)
                text = asi_text(props)
                terms = C.find_columbarium(text)
                if not terms:
                    continue
                coords = (ft.get('geometry') or {}).get('coordinates') or [None, None]
                lon, lat = coords[0], coords[1]
                sid = str(props.get('id') or props.get('Id') or props.get('site_id') or ft.get('id') or '')
                rec = record_fields(cache, sid)
                out.append(dict(source='ASI', lang=lang, map_id=mid, map_num=mapnum,
                                site_id=sid, site_num=str(props.get('site_num') or ''),
                                name=C.clean(props.get('name_heb') or props.get('name') or ''),
                                lat=lat, lon=lon, in_region=C.in_region(lon, lat),
                                terms=';'.join(terms), flags=json.dumps(C.flag_hits(text), ensure_ascii=False),
                                text_sha256=C.sha256_text(text),
                                record_name=rec.get('_name', ''), record_nig=rec.get('New Israel Grid', ''),
                                record_wgs84=rec.get('WGS-84', ''), record_period=rec.get('Period', ''),
                                record_sha256=rec.get('_sha256', '')))
    return out


ROW = re.compile(r'<tr>\s*<td>\s*<b>(.*?)</b>\s*</td>\s*<td>(.*?)</td>\s*</tr>', re.S | re.I)


def record_fields(cache, sid):
    """Name, grid, WGS84 and Period of a cached GetSiteDesc2 record (empty dict if not fetched)."""
    path = os.path.join(cache, C.cache_name('Service_Eng.aspx/GetSiteDesc2', Id=sid))
    if not sid or not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        d = json.load(f)['d']
    if isinstance(d, str):
        d = json.loads(d)
    out = {C.clean(k).rstrip(':').strip(): C.clean(v) for k, v in ROW.findall(d.get('content') or '')}
    out['_name'] = C.clean(d.get('name'))
    out['_sha256'] = C.sha256_file(path)
    return out


# ------------------------------------------------------------------ S2 WBADB
def wbadb_screen(xlsx):
    import openpyxl
    from pyproj import Transformer
    digest = C.sha256_file(xlsx)
    if digest != WBADB_SHA256:
        sys.exit(f'WBADB hash {digest} differs from {WBADB_SHA256}')
    to_wgs = Transformer.from_crs('EPSG:28193', 'EPSG:4326', always_xy=True)
    wb = openpyxl.load_workbook(xlsx, read_only=True)
    out = []
    for sheet, prefix in (('Surveyed', 'S'), ('Excavations', 'E')):
        ws = wb[sheet]
        rows = ws.iter_rows(values_only=True)
        hdr = [h for h in next(rows)]
        for vals in rows:
            r = dict(zip(hdr, vals))
            if r.get('Index') is None:
                continue
            parts = []
            for f in WBADB_FIELDS:
                v = r.get(f)
                if isinstance(v, str) and v.strip() not in ('', '-', 'NDA'):
                    parts.append(v)
            text = ' ; '.join(parts)
            terms = C.find_columbarium(text)
            if not terms:
                continue
            try:
                x, y = float(r['X']), float(r['Y'])
                lon, lat = to_wgs.transform(x, y + 1_000_000)
            except (TypeError, ValueError):
                lon = lat = None
            periods = [p for p in ('Per', 'Hel', 'Rom', 'Byz', 'EIs', 'Med', 'Ott', 'IA', 'IA2')
                       if isinstance(r.get(p), (int, float)) and r.get(p) and r.get(p) > 0]
            out.append(dict(source='WBADB', row_id=f'{prefix}{r["Index"]}', name=r.get('Site_Name') or '',
                            other_names=r.get('Other_Names') or '', x=r.get('X'), y=r.get('Y'),
                            lat=None if lat is None else round(lat, 6), lon=None if lon is None else round(lon, 6),
                            in_region=C.in_region(lon, lat), survey_ref=r.get('Survey_Ref') or r.get('Site_No') or '',
                            excavated=r.get('Excavated') if sheet == 'Surveyed' else 'excavation sheet',
                            major_periods=r.get('Major_Periods') or '', other_periods=r.get('Other_Periods') or '',
                            period_flags=';'.join(periods), terms=';'.join(terms),
                            flags=json.dumps(C.flag_hits(text), ensure_ascii=False),
                            text_sha256=C.sha256_text(text)))
    return out


def write(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cols = list(rows[0].keys()) if rows else ['empty']
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    cache, xlsx = sys.argv[1], sys.argv[2]
    asi = asi_screen(cache)
    write(asi, os.path.join(DATA, 'candidates_asi.csv'))
    wb = wbadb_screen(xlsx)
    write(wb, os.path.join(DATA, 'candidates_wbadb.csv'))
    print(f'ASI hits {len(asi)} (in region {sum(r["in_region"] for r in asi)}); '
          f'WBADB hits {len(wb)} (in region {sum(r["in_region"] for r in wb)})')


if __name__ == '__main__':
    main()
