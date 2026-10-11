#!/usr/bin/env python3
"""Build survey_rows.csv (WBADB, ASI, HA-ESI rows in the box) under PLAN.md §3–§7 and amendment 1.

Run from the repository root:
  python3 -I research/regional/water_systems/scripts/build_survey.py WBADB_data1.xlsx ASI_CACHE_DIR
Needs pandas, openpyxl and pyproj (WBADB only). The xlsx must match the frozen SHA-256.
No source text is written: rows hold matched terms, codes, record ids and SHA-256 hashes of the
sentences read.
"""
import csv
import json
import os
import re
import sys
from difflib import SequenceMatcher

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

NUM_WORDS = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
             'eleven': 11, 'twelve': 12, 'some twenty': 20, 'twenty': 20, 'thirty': 30, 'a pair of': 2, 'one': 1,
             'a': 1, 'an': 1, 'single': 1}
QUMRAN_NAMES = re.compile(r'qumran|sekaka|secacah|sekakah|buqei|bouqei|buqeia', re.I)
JERICHO_NAMES = re.compile(r"jericho|sultan|abu el-?alay|alayiq|alaiq|naaran|na'aran|ain duk|ein duk|nueima|nuweim|"
                           r"\bdoq\b|\bdok\b|dagon|qarantal|quruntul|cypros|kypros|el-?aqaba|mafjar", re.I)
CYPROS_NAMES = re.compile(r'cypros|kypros|tell? el-?aqaba|tel el akaba', re.I)
KIDRON_NAMES = re.compile(r'kidron|qidron|wadi en-?nar|\bnar\b', re.I)
QELT_NAMES = re.compile(r"\bqelt\b|\bkelt\b|\bqilt\b|nahal (?:prat|perat)|ein (?:fara|farah|prat|perat|fawwar|fawar|qelt)|"
                        r"ain (?:fara|farah|fawwar|fawar|qelt)|wadi (?:fara|farah)|choziba|koziba|khoziba|st\.? george|"
                        r"mar jiryis|deir el-?qelt", re.I)
WADI_NAME = re.compile(r"\b(?:wadi|nahal|n\.)\s+([A-Za-zʿʾ'’\-]+(?:\s+[a-zA-Zʿʾ'’\-]+)?)", re.I)


def count_before(sentence, m):
    pre = fold_pre = sentence[:m.start()].lower()
    mnum = re.search(r'(\d+)\s*(?:\w+\s){0,2}$', pre)
    if mnum:
        return int(mnum.group(1))
    for w, n in NUM_WORDS.items():
        if re.search(r'\b' + re.escape(w) + r'\s+(?:\w+\s){0,2}$', fold_pre):
            return n
    return None


def attrs_for(sents_with, name, places, lat, lon):
    """Attribute codes from the sentences that contain the type word (plan §5 survey text)."""
    j = ' '.join(sents_with)
    A = {}
    A['great'] = 'yes' if C.ATTR_RE['great'].search(j) else 'unknown'
    A['north'] = 'yes' if C.ATTR_RE['north'].search(j) else 'unknown'
    A['plaster'] = 'yes' if C.ATTR_RE['plaster'].search(j) else 'unknown'
    A['entrance'] = 'yes' if C.ATTR_RE['entrance'].search(j) else 'unknown'
    four = bool(C.ATTR_RE['four'].search(j))
    notfour = bool(C.ATTR_RE['notfour'].search(j))
    A['shape'] = 'four_sides' if four and not notfour else ('not_four_sides' if notfour and not four else 'unknown')
    A['fissure_east'] = 'unknown'  # survey text gives no bearing for a fissure; words only in literature
    # plan §5 entry 22: the installation is named Solomon's; a "from/to Solomon's Pools" phrase does not name it
    sol_text = C.SOLOMON_PHRASE.sub(' ', j)
    A['solomon'] = 'yes' if (C.SOLOMON_POOL.search(name or '') or C.SOLOMON_POOL.search(sol_text)) else 'unknown'
    A['bend'] = 'yes' if C.ATTR_RE['bend'].search(j) else 'unknown'
    A['wall_at_outlet'] = 'yes' if C.ATTR_RE['wall'].search(j) else 'unknown'
    head_s = [s for s in sents_with if C.ATTR_RE['head'].search(s)]
    A['head'] = 'yes' if head_s else 'unknown'
    marker = []
    side = 'unknown'
    for s in head_s:
        if C.ATTR_RE['stone'].search(s):
            marker.append('stone')
        if C.ATTR_RE['pool_marker'].search(s):
            marker.append('pool')
        if C.ATTR_RE['any_marker'].search(s):
            marker.append('any')
        if marker and C.ATTR_RE['north'].search(s):
            side = 'N'
    A['head_marker'] = ';'.join(sorted(set(marker)))
    A['marker_side'] = side if marker else ''
    feed = 'unknown'
    if any(rx.search(j) for rx in C.FEED_RE):
        feed = 'channel'
    A['feed'] = feed
    A['feed_wadi'] = 'yes' if feed == 'channel' and C.WADI_FEED_RE.search(j) else 'unknown'
    wn = [m.group(1) for m in WADI_NAME.finditer(j + ' ' + (name or ''))]
    A['named_wadi'] = ';'.join(sorted(set(w.strip() for w in wn)))
    allt = j + ' ' + (name or '')
    A['qelt'] = 'yes' if QELT_NAMES.search(C.fold(allt)) or QELT_NAMES.search(allt) else ('no' if wn else 'unknown')
    A['kidron_feed'] = 'yes' if KIDRON_NAMES.search(allt) else 'unknown'
    A['cypros'] = 'yes' if CYPROS_NAMES.search(C.fold(allt)) else 'unknown'
    # place columns with distances (amendment 1 §3)
    if lat is not None:
        dq = min(C.km(lat, lon, *places['kh_qumran'][:2]), C.km(lat, lon, *places['wadi_qumran'][:2]))
        db = C.km(lat, lon, *places['buqeia'][:2])
        A['qumran'] = 'yes' if (QUMRAN_NAMES.search(C.fold(allt)) or dq <= 1.0 or db <= 2.5) else 'no'
        dj = min(C.km(lat, lon, *places[p][:2]) for p in ('tell_es_sultan', 'jericho_palaces', 'doq', 'ain_duk'))
        A['jericho_oasis'] = 'yes' if (JERICHO_NAMES.search(C.fold(allt)) or dj <= 2.0) else 'no'
        if A['cypros'] != 'yes':
            A['cypros'] = 'no'
    else:
        A['qumran'] = 'yes' if QUMRAN_NAMES.search(C.fold(allt)) else 'unknown'
        A['jericho_oasis'] = 'yes' if JERICHO_NAMES.search(C.fold(allt)) else 'unknown'
    codes = []
    labels = []
    for s in sents_with:
        c, lab = C.date_code(s)
        codes.append(c)
        labels += lab
    A['date_code'] = C.combine_dates(codes)
    A['period_as_given'] = ';'.join(dict.fromkeys(l.lower() for l in labels))
    return A


def rows_for_record(lineage, source, locator, record_id, name, text_sents, lat, lon, prec, crs, coord_source,
                    places, extra):
    """One row per type found in the record's sentences (name counts as a sentence)."""
    out = []
    all_sents = ([name] if name else []) + text_sents
    by_type = {}
    for s in all_sents:
        for t in C.type_hits(s, name or ''):
            by_type.setdefault(t, []).append(s)
    if name and C.SPRING_NAME.search(name):
        by_type.setdefault('spring', []).append(name)
    for t in C.TYPES:
        if t not in by_type:
            continue
        ss = list(dict.fromkeys(by_type[t]))
        rx = C.TYPE_RE[t]
        plural, cnt = False, None
        for s in ss:
            for m in rx.finditer(s):
                if m.group(0).lower().endswith('s') and not m.group(0).lower().endswith(('ss', 'works')):
                    plural = True
                c = count_before(s, m)
                if c:
                    cnt = c if cnt is None else max(cnt, c)
        A = attrs_for(ss, name, places, lat, lon)
        matched = sorted(set(m.group(0).lower() for s in ss for m in rx.finditer(s)))
        r = {k: '' for k in C.COLUMNS}
        r.update(dict(
            id=f'{lineage}-{record_id}-{t}', lineage=lineage, source=source, locator=locator, record_id=record_id,
            name=name or '', site_key='', type=t,
            aggregate='yes' if (plural and (cnt is None or cnt > 1)) else 'no',
            count=str(cnt) if cnt else ('1' if not plural else ''),
            lat=f'{lat:.6f}' if lat is not None else '', lon=f'{lon:.6f}' if lon is not None else '',
            crs=crs, precision_m=str(prec), coord_source=coord_source,
            flow_from='unknown', dims='', capacity_m3='', label='EVIDENCE',
            first_read_after_freeze='', quote='', span_sha256=C.sha256_text('\n'.join(ss)),
            notes='matched: ' + ', '.join(matched),
        ))
        r.update(A)
        r.update(extra)
        out.append(r)
    return out


def build_wbadb(xlsx, places):
    import pandas as pd
    import pyproj
    if C.sha256_file(xlsx) != C.WBADB_SHA256:
        sys.exit('WBADB file differs from the frozen SHA-256')
    t = pyproj.Transformer.from_crs('EPSG:28191', 'EPSG:4326', always_xy=True)
    sheets = pd.read_excel(xlsx, sheet_name=['Surveyed', 'Excavations'], dtype=str)
    rows, meta = [], {}
    for sh, df in sheets.items():
        pre = 'S' if sh == 'Surveyed' else 'E'
        for _, r in df.iterrows():
            try:
                x, y = float(r['X']), float(r['Y'])
            except (TypeError, ValueError):
                continue
            lon, lat = t.transform(x, y)
            if not C.in_box(lat, lon):
                continue
            if sh == 'Excavations' and str(r.get('Surveyed', '')).strip().lower() == 'yes':
                pass  # kept: excavation rows are records of their own (dedup by name/distance below)
            rid = f'{pre}{int(float(r["Index"]))}'
            name = '' if str(r.get('Site_Name')) in ('nan', '-') else str(r.get('Site_Name'))
            other = '' if str(r.get('Other_Names')) in ('nan', '-') else str(r.get('Other_Names'))
            texts = []
            for col in ('Site_Components', 'More_Components', 'Comments', 'More_Comments'):
                v = r.get(col)
                if v is not None and str(v) not in ('nan', '-', ''):
                    texts += C.sentences(str(v))
            if other:
                texts = [other] + texts
            prec = 100 if (x % 100 == 0 and y % 100 == 0) else 10
            hel = str(r.get('Hel', '0')) not in ('0', 'nan', '', 'None')
            rom = str(r.get('Rom', '0')) not in ('0', 'nan', '', 'None')
            exc = 'yes' if sh == 'Excavations' or str(r.get('Excavated', '')).strip().lower() not in (
                '', '-', 'no', 'nan') else 'no'
            ref = str(r.get('Survey_Ref', '')) if sh == 'Surveyed' else ''
            extra = dict(site_period_in_window='partly' if (hel or rom) else 'no', excavated=exc)
            loc = f'WBADB {sh} row Index {int(float(r["Index"]))}' + (f'; Survey_Ref {ref}' if ref and ref != 'nan' else '')
            rr = rows_for_record('WBADB', 'WBADB (Greenberg & Keinan 2009)', loc, rid, name, texts, lat, lon, prec,
                                 'EPSG:28191 X/Y -> EPSG:4326', 'WBADB site point', places, extra)
            rows += rr
            meta[rid] = dict(ref=ref, name=name, other=other, lat=lat, lon=lon, prec=prec)
    return rows, meta


def build_asi(cache, places):
    rows, meta = [], {}
    for mid, mapnum in C.ASI_MAPS.items():
        path = os.path.join(cache, f'GetPolygonsSites_en_map{mid}.json')
        with open(path, encoding='utf-8') as f:
            d = json.load(f)['d']
        if isinstance(d, str):
            d = json.loads(d)
        for ft in d['features']:
            lon, lat = ft['geometry']['coordinates'][:2]
            if not C.in_box(lat, lon):
                continue
            p = ft['properties']
            p = {x['key']: x['value'] for x in p} if isinstance(p, list) else dict(p)
            snum = str(p.get('site_num') or '').strip()
            name = C.clean(p.get('name_heb') or '')
            texts = C.sentences(p.get('description_heb') or '') + C.sentences(p.get('finding_heb') or '')
            rid = f'{mapnum}/{snum}'
            extra = dict(site_period_in_window='unknown', excavated='unknown')
            rr = rows_for_record('ASI', f'ASI Map {mapnum} (online)', f'ASI Map {mapnum}, site {snum} (db id {p.get("id")})',
                                 rid, name or f'ASI {rid}', texts, lat, lon, 50, 'EPSG:4326 (ASI GeoJSON)',
                                 'ASI record point', places, extra)
            rows += rr
            meta[rid] = dict(name=name, lat=lat, lon=lon, map=mapnum, site=snum)
    return rows, meta


def build_haesi(places):
    path = os.path.join(C.REPO, 'research', 'regional', 'haesi_features', 'features.csv')
    tmap = {'cistern': 'cistern', 'channel_aqueduct': 'aqueduct', 'pool_reservoir': 'reservoir_pool',
            'ritual_bath': 'ritual_bath'}
    rows = []
    with open(path, encoding='utf-8') as f:
        for i, r in enumerate(csv.DictReader(f)):
            if r['feature_type'] not in tmap or not r['lat']:
                continue
            lat, lon = float(r['lat']), float(r['lon'])
            if not C.in_box(lat, lon):
                continue
            t = tmap[r['feature_type']]
            q = r.get('quote', '')
            if t == 'ritual_bath':
                if not re.search(r'\b(pools?|reservoirs?|cisterns?)\b', q, re.I):
                    continue
                t = 'reservoir_pool' if re.search(r'\b(pools?|reservoirs?)\b', q, re.I) else 'cistern'
            A = attrs_for([q], r['site_name'], places, lat, lon)
            dc, lab = C.date_code(r['period_as_given'])
            if dc == 'undated' and r['dated_in_window'] == 'no':
                dc = 'out'
            row = {k: '' for k in C.COLUMNS}
            row.update(A)
            row.update(dict(
                id=f'HAESI-{r["report_id"]}-{t}-{i}', lineage='HAESI', source=f'{r["series"]} {r["volume"]} ({r["year"]})',
                locator=f'{r["series"]} {r["volume"]} p. {r["pages"]}; {r["url"]}', record_id=r['report_id'],
                name=r['site_name'], type=t, aggregate='yes' if (r['n_features'] or '1') not in ('1', '') else 'no',
                count=r['n_features'], lat=f'{lat:.6f}', lon=f'{lon:.6f}', crs=r['crs_used'] + ' -> EPSG:4326',
                precision_m=r['precision_m'], coord_source=r['coordinate_source'],
                period_as_given=r['period_as_given'], date_code=dc, site_period_in_window='unknown',
                excavated=r['excavated_or_surveyed'], label='EVIDENCE', quote='', flow_from='unknown',
                span_sha256=C.sha256_text(q), notes='reused from haesi_features/features.csv',
            ))
            rows.append(row)
    return rows


def dedup(wrows, wmeta, ameta, arows):
    """WBADB -> ASI duplicates (plan §7)."""
    asi_types = {}
    for r in arows:
        asi_types.setdefault(r['record_id'], set()).add(r['type'])
    asi_by_skel = []
    for rid, m in ameta.items():
        asi_by_skel.append((rid, C.skeleton(m['name']), m['lat'], m['lon']))
    link = {}
    for rid, m in wmeta.items():
        ref = m.get('ref') or ''
        target = None
        mk = re.search(r'Kloner \d{4}, Site \[([0-9/]+)\] (\d+)', ref)
        mp = re.search(r'(?<!and )Patrich \d{4}, Site (\d+)', ref)
        mh = re.match(r'\s*Hirschfeld \d{4}, Site (\d+)', ref)
        if mk:
            target = f'{mk.group(1)}/{mk.group(2)}'
        elif mp:
            target = f'109/7/{mp.group(1)}'
        elif mh:
            target = f'108/2/{mh.group(1)}'
        if target and target in ameta:
            link[rid] = (target, 'ref')
            continue
        sk = [C.skeleton(m['name'])] + ([C.skeleton(m['other'])] if m.get('other') else [])
        best = None
        for arid, ask, alat, alon in asi_by_skel:
            if not ask:
                continue
            dkm = C.km(m['lat'], m['lon'], alat, alon)
            if dkm > 0.3:
                continue
            for s in sk:
                if len(s) >= 3 and len(ask) >= 3 and SequenceMatcher(None, s, ask).ratio() >= 0.85 or \
                        (len(s) == 2 and s == ask):
                    if best is None or dkm < best[1]:
                        best = (arid, dkm)
        if best:
            link[rid] = (best[0], 'name+300m')
    for r in wrows:
        L = link.get(r['record_id'])
        if L and r['type'] in asi_types.get(L[0], set()):
            r['dup_of'] = f'ASI-{L[0]}-{r["type"]}'
            r['notes'] += f'; same site as ASI {L[0]} ({L[1]})'
        elif L:
            r['notes'] += f'; same site as ASI {L[0]} ({L[1]}), type not in ASI text'
    return link


def write_site_points(wmeta, ameta, path):
    """Points of the WBADB/ASI records and grid references that literature rows cite (plan §6 rule 1-2)."""
    import pyproj
    import literature_data as L
    import literature_data_2  # noqa: F401  (registers its rows)
    t = pyproj.Transformer.from_crs('EPSG:28191', 'EPSG:4326', always_xy=True)
    out = {}
    for r in L.ROWS:
        for pt in (r['pt'], r['dest_pt']):
            if not pt:
                continue
            kind = pt[0]
            if kind == 'wbadb' and pt[1] in wmeta:
                m = wmeta[pt[1]]
                out['wbadb:' + pt[1]] = (m['lat'], m['lon'], m['prec'], 'WBADB ' + pt[1] + ' ' + m['name'])
            elif kind == 'asi' and pt[1] in ameta:
                m = ameta[pt[1]]
                out['asi:' + pt[1]] = (m['lat'], m['lon'], 50, 'ASI ' + pt[1] + ' ' + m['name'])
            elif kind == 'oig':
                lon, lat = t.transform(pt[1], pt[2])
                out[f'oig:{pt[1]},{pt[2]}'] = (lat, lon, pt[3], 'source grid reference (EPSG:28191)')
            elif kind in ('wbadb', 'asi'):
                sys.exit(f'literature point {pt} not found in the box records')
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['key', 'lat', 'lon', 'precision_m', 'label'])
        for k in sorted(out):
            lat, lon, prec, lab = out[k]
            w.writerow([k, f'{lat:.6f}', f'{lon:.6f}', prec, lab])


def main(xlsx, cache, out_csv):
    places = C.load_places()
    wrows, wmeta = build_wbadb(xlsx, places)
    arows, ameta = build_asi(cache, places)
    hrows = build_haesi(places)
    dedup(wrows, wmeta, ameta, arows)
    write_site_points(wmeta, ameta, os.path.join(C.LANE, 'site_points.csv'))
    rows = wrows + arows + hrows
    rows.sort(key=lambda r: (r['lineage'], r['id']))
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=C.COLUMNS, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    print(len(wrows), len(arows), len(hrows), file=sys.stderr)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else
         os.path.join(C.LANE, 'survey_rows.csv'))
