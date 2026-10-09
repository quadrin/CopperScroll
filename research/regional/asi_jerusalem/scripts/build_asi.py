#!/usr/bin/env python3
"""Build sites.csv, features.csv, looks_asi.csv and the summary tables from the ASI cache.

Run:  python3 -I scripts/build_asi.py CACHE_DIR [OUT_DIR]
OUT_DIR defaults to this folder. Rules: plan.json and plan_amendment_1.json (frozen).
Only the standard library and pyproj are used. Output is deterministic for a given cache.
"""
import csv
import json
import os
import re
import sys

from pyproj import Transformer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import asi_common as C  # noqa: E402

ITM = Transformer.from_crs('EPSG:2039', 'EPSG:4326', always_xy=True)

SITE_COLS = ['asi_map_id', 'map_num', 'map_name', 'site_num', 'record_id', 'name', 'name_he', 'additional_names',
             'field_num', 'record_fetched', 'nig_e', 'nig_n', 'lat', 'lon', 'coord_method', 'src_wgs84_lat',
             'src_wgs84_lon', 'coord_check_m', 'coord_check_flag', 'nearest_place_id', 'nearest_place_km',
             'places_within_1km', 'places_within_3km', 'feature_classes', 'heb_only_classes', 'period_field',
             'periods_as_given', 'site_finds_in_window', 'protected_zone_nearby', 'quote',
             'citation', 'url']
FEAT_COLS = ['asi_map_id', 'map_num', 'site_num', 'record_id', 'site_name', 'lat', 'lon', 'nearest_place_id',
             'nearest_place_km', 'places_within_1km', 'feature_class', 'match_field', 'matched_text',
             'period_as_given', 'period_window_classes', 'dated_in_window', 'site_finds_in_window',
             'heb_confirms', 'record_fetched', 'quote', 'citation']
PLACE_COLS = ['place_id', 'name', 'model_region', 'maps_containing_point', 'maps_within_1km', 'n_sites_1km',
              'n_sites_3km', 'n_sites_1km_without_record', 'cistern_1km', 'pool_1km', 'reservoir_1km',
              'conduit_1km', 'spring_well_1km', 'tomb_1km', 'cave_1km', 'n_features_1km_dated_yes',
              'n_features_1km_dated_partly', 'n_sites_1km_finds_in_window_yes']
MAP_COLS = ['asi_map_id', 'map_num', 'name', 'author', 'isbn', 'lat_lo', 'lat_hi', 'lon_lo', 'lon_hi',
            'n_sites_online', 'n_sites_in_sites_csv', 'n_records_fetched_in_sites_csv', 'places_within_3km_of_sheet',
            'coverage_value', 'coverage_statement_type', 'intro_en_sha256', 'intro_he_sha256']
HEB2_COLS = ['record_id', 'asi_map_id', 'site_num', 'classes_he_v2', 'heb_only_v2']
FIELD_ORDER = ['description', 'name', 'additional_names', 'finds_field', 'geojson_finding', 'remains']


def read_json(cache, name):
    path = os.path.join(cache, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def compile_classes(plan):
    return [(k, re.compile(v, re.I)) for k, v in plan['feature_classes'].items() if k != 'note']


def compile_hebrew(plan):
    return [(k, re.compile(v)) for k, v in plan['hebrew_check'].items() if k != 'note']


def compile_periods(plan):
    alts = []
    for cls in ('within', 'overlaps', 'outside'):
        for pat in plan['periods'][cls]:
            alts.append((pat, cls))
    alts.sort(key=lambda a: (-len(a[0]), a[0]))
    groups = '|'.join(f'(?P<g{i}>{pat})' for i, (pat, _) in enumerate(alts))
    rx = re.compile(r'\b(?:' + groups + ')', re.I)
    return rx, [cls for _, cls in alts]


def find_periods(rx, gcls, text):
    out = []
    for m in rx.finditer(text or ''):
        for name, val in m.groupdict().items():
            if val is not None:
                out.append((m.group(0), gcls[int(name[1:])], m.start()))
                break
    return out


def window_any(labels):
    kinds = {k for _, k, _ in labels}
    if 'within' in kinds:
        return 'yes'
    if 'overlaps' in kinds:
        return 'overlaps'
    if 'outside' in kinds:
        return 'no'
    return 'unknown'


def window_all(labels):
    if not labels:
        return 'unknown'
    kinds = [k for _, k, _ in labels]
    if all(k == 'within' for k in kinds):
        return 'yes'
    if any(k in ('within', 'overlaps') for k in kinds):
        return 'partly'
    return 'no'


def uniq(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def fmt(x, nd=6):
    return '' if x is None else f'{x:.{nd}f}'


def selected_maps(places, maps, sheets):
    online = {str(m['id']): m for m in maps}
    out = []
    for mid, sh in sorted(sheets.items(), key=lambda kv: int(kv[0])):
        if mid in online:
            d = min(C.rect_km(p['lat_f'], p['lon_f'], sh['lat_lo'], sh['lat_hi'], sh['lon_lo'], sh['lon_hi'])
                    for p in places)
            if d <= 3.0:
                out.append(mid)
    return out


def circle_inside(lat, lon, sh, r):
    if not (sh['lat_lo'] <= lat <= sh['lat_hi'] and sh['lon_lo'] <= lon <= sh['lon_hi']):
        return False
    return min(C.km(lat, lon, sh['lat_lo'], lon), C.km(lat, lon, sh['lat_hi'], lon),
               C.km(lat, lon, lat, sh['lon_lo']), C.km(lat, lon, lat, sh['lon_hi'])) >= r


def build(cache, out):
    plan = C.load_plan()
    places, _ = C.load_places(plan)
    pmap = {p['place_id']: p for p in places}
    classes = compile_classes(plan)
    heb = compile_hebrew(plan)
    prx, pcls = compile_periods(plan)
    maps = read_json(cache, 'Service_Eng_GetMaps.json')['d']
    online = {str(m['id']): m for m in maps}
    sheets = C.sheets_from_grid(read_json(cache, 'GetIsraelGrid.json'))
    mids = selected_maps(places, maps, sheets)

    sites, feats = [], []
    map_stats = {}
    for mid in mids:
        m = online[mid]
        author = C.clean(m.get('Author') or '')
        en = read_json(cache, C.cache_name('Service_Eng.aspx/GetPolygonsSites', MapId=mid, sitesId='null'))
        he = read_json(cache, C.cache_name('Service.aspx/GetPolygonsSites', MapId=mid, sitesId='null'))
        he_by_id = {}
        if he:
            for ft in he['d']['features']:
                pr = C.geojson_props(ft)
                he_by_id[str(pr['id'])] = pr
        feats_en = en['d']['features'] if en else []
        st = map_stats.setdefault(mid, dict(n_online=len(feats_en), n_in=0, n_rec=0))
        for ft in feats_en:
            pr = C.geojson_props(ft)
            sid = str(pr['id'])
            glon, glat = ft['geometry']['coordinates'][:2]
            if min(C.km(glat, glon, p['lat_f'], p['lon_f']) for p in places) > 3.5:
                continue
            recj = read_json(cache, C.cache_name('Service_Eng.aspx/GetSiteDesc2', Id=sid))
            rec = C.parse_site_desc(recj['d']) if recj and recj.get('d') else None
            src_lat = src_lon = None
            nig = None
            if rec:
                nig = C.parse_grid_pair(rec.get('New Israel Grid'))
                w = C.parse_wgs_pair(rec.get('WGS-84'))
                if w:
                    src_lat, src_lon = w
            if nig:
                lon, lat = ITM.transform(nig[0], nig[1])
                method = 'nig_epsg2039'
            elif src_lat is not None:
                lat, lon, method = src_lat, src_lon, 'source_wgs84'
            else:
                lat, lon, method = glat, glon, 'geojson_point'
            dists = sorted((round(C.km(lat, lon, p['lat_f'], p['lon_f']), 6), p['place_id']) for p in places)
            if dists[0][0] > 3.0:
                continue
            check_m = None
            if nig and src_lat is not None:
                check_m = C.km(lat, lon, src_lat, src_lon) * 1000.0
            name = C.clean(rec.get('Site Name')) if rec else C.clean(pr.get('name_heb'))
            fields = {
                'description': C.clean(rec.get('Description')) if rec and rec.get('Description') else C.clean(pr.get('description_heb')),
                'name': name,
                'additional_names': C.clean(rec.get('Additional Names')) if rec else '',
                'finds_field': C.clean(rec.get('Finds')) if rec else '',
                'geojson_finding': C.clean(pr.get('finding_heb')),
                'remains': '',
            }
            rem = read_json(cache, C.cache_name('Service_Eng.aspx/GetSiteRemains', Id=sid))
            if rem:
                d = rem.get('d')
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except ValueError:
                        d = []
                if d:
                    fields['remains'] = C.clean(json.dumps(d, ensure_ascii=False, sort_keys=True))
            period_field = C.clean(rec.get('Period')) if rec else ''
            hp = he_by_id.get(sid, {})
            he_text = C.clean(hp.get('description_heb')) + ' ' + C.clean(hp.get('finding_heb'))
            he_classes = {k for k, rx in heb if rx.search(he_text)}
            # classes
            site_classes = []
            desc = fields['description']
            sentences = C.split_sentences(desc)
            for cls, rx in classes:
                first = None
                for fname in FIELD_ORDER:
                    mm = rx.search(fields[fname])
                    if mm:
                        first = (fname, mm)
                        break
                if not first:
                    continue
                site_classes.append(cls)
                fname, mm = first
                labels = []
                for s0, s1 in sentences:
                    if rx.search(desc[s0:s1]):
                        labels.extend(find_periods(prx, pcls, desc[s0:s1]))
                if fname == 'finds_field':  # a comma-separated term list: quote the one matching term
                    a = fields[fname].rfind(',', 0, mm.start()) + 1
                    b = fields[fname].find(',', mm.end())
                    quote = fields[fname][a:b if b >= 0 else None].strip()
                else:
                    quote = C.quote_window(fields[fname], mm.start())
                feats.append(dict(cls=cls, fname=fname, matched=mm.group(0),
                                  labels=labels, quote=quote,
                                  heb=('yes' if cls in he_classes else 'no') if cls in dict(heb) else '',
                                  sid=sid))
            all_text = ' '.join(fields[f] for f in FIELD_ORDER) + ' ' + period_field
            site_labels = find_periods(prx, pcls, all_text)
            near1 = [(d, pid) for d, pid in dists if d <= 1.0]
            near3 = [(d, pid) for d, pid in dists if d <= 3.0]
            s = dict(
                asi_map_id=mid, map_num=m['map_num'], map_name=C.clean(m['name']), site_num=str(pr.get('site_num') or ''),
                record_id=sid, name=name, name_he=C.clean(hp.get('name_heb')),
                additional_names=fields['additional_names'], field_num=C.clean(rec.get('Field Num')) if rec else '',
                record_fetched='yes' if rec else 'no',
                nig_e=f'{nig[0]:.0f}' if nig else '', nig_n=f'{nig[1]:.0f}' if nig else '',
                lat=fmt(lat), lon=fmt(lon), coord_method=method,
                src_wgs84_lat=fmt(src_lat), src_wgs84_lon=fmt(src_lon),
                coord_check_m='' if check_m is None else f'{check_m:.1f}',
                coord_check_flag='' if check_m is None else ('gt50m' if check_m > 50 else 'ok'),
                nearest_place_id=dists[0][1], nearest_place_km=f'{dists[0][0]:.3f}',
                places_within_1km=';'.join(f'{pid}:{d:.3f}' for d, pid in near1),
                places_within_3km=';'.join(f'{pid}:{d:.3f}' for d, pid in near3),
                feature_classes=';'.join(site_classes),
                heb_only_classes=';'.join(k for k, _ in heb if k in he_classes and k not in site_classes),
                period_field=period_field,
                periods_as_given=';'.join(uniq(lab for lab, _, _ in site_labels)),
                site_finds_in_window=window_any(site_labels),
                protected_zone_nearby='yes' if ('tell_es_sultan' in pmap and C.km(lat, lon, pmap['tell_es_sultan']['lat_f'], pmap['tell_es_sultan']['lon_f']) <= 1.0) else 'no',
                # post-freeze deviation (README): one quote per record, only within 1 km of a place
                quote=C.first_words(desc, 12) if near1 else '',
                citation=f"{author}, ASI Map of {C.clean(m['name'])} ({m['map_num']}), site {pr.get('site_num')}; survey.iaa.org.il record {sid}; printed page not given online",
                url=f'https://survey.iaa.org.il/#/MapSurvey/{mid}/site/{sid}',
            )
            s['_lat'], s['_lon'], s['_near1'], s['_classes'] = lat, lon, near1, site_classes
            s['_he_text'] = he_text
            sites.append(s)
            st['n_in'] += 1
            st['n_rec'] += 1 if rec else 0
    sites.sort(key=lambda s: (int(s['asi_map_id']), int(s['site_num'] or 0), int(s['record_id'])))
    by_id = {s['record_id']: s for s in sites}
    order = {c: i for i, (c, _) in enumerate(classes)}
    frows = []
    for f in feats:
        s = by_id.get(f['sid'])
        if not s:
            continue
        frows.append(dict(
            asi_map_id=s['asi_map_id'], map_num=s['map_num'], site_num=s['site_num'], record_id=s['record_id'],
            site_name=s['name'], lat=s['lat'], lon=s['lon'], nearest_place_id=s['nearest_place_id'],
            nearest_place_km=s['nearest_place_km'], places_within_1km=s['places_within_1km'],
            feature_class=f['cls'], match_field=f['fname'], matched_text=f['matched'],
            period_as_given=';'.join(uniq(lab for lab, _, _ in f['labels'])),
            period_window_classes=';'.join(uniq(k for _, k, _ in f['labels'])),
            dated_in_window=window_all(f['labels']), site_finds_in_window=s['site_finds_in_window'],
            # post-freeze deviation (README): no quote text in features.csv; matched_text keeps the term
            heb_confirms=f['heb'], record_fetched=s['record_fetched'], quote='', citation=s['citation']))
    frows.sort(key=lambda r: (int(r['asi_map_id']), int(r['site_num'] or 0), int(r['record_id']), order[r['feature_class']]))

    os.makedirs(out, exist_ok=True)
    write_csv(os.path.join(out, 'sites.csv'), SITE_COLS, sites)
    write_csv(os.path.join(out, 'features.csv'), FEAT_COLS, frows)

    # per place summary
    feats_by_site = {}
    for r in frows:
        feats_by_site.setdefault(r['record_id'], []).append(r)
    prow = []
    for p in sorted(places, key=lambda p: p['place_id']):
        pid = p['place_id']
        s1 = [s for s in sites if any(q == pid for _, q in s['_near1'])]
        s3 = [s for s in sites if pid in [x.split(':')[0] for x in s['places_within_3km'].split(';') if x]]
        f1 = [r for s in s1 for r in feats_by_site.get(s['record_id'], [])]
        cnt = lambda c: str(sum(1 for r in f1 if r['feature_class'] == c))  # noqa: E731
        prow.append(dict(
            place_id=pid, name=p['name'], model_region=p['model_region'],
            maps_containing_point=';'.join(online[mid]['map_num'] for mid in mids if C.rect_km(p['lat_f'], p['lon_f'], sheets[mid]['lat_lo'], sheets[mid]['lat_hi'], sheets[mid]['lon_lo'], sheets[mid]['lon_hi']) == 0.0),
            maps_within_1km=';'.join(online[mid]['map_num'] for mid in mids if C.rect_km(p['lat_f'], p['lon_f'], sheets[mid]['lat_lo'], sheets[mid]['lat_hi'], sheets[mid]['lon_lo'], sheets[mid]['lon_hi']) <= 1.0),
            n_sites_1km=str(len(s1)), n_sites_3km=str(len(s3)),
            n_sites_1km_without_record=str(sum(1 for s in s1 if s['record_fetched'] == 'no')),
            cistern_1km=cnt('cistern'), pool_1km=cnt('pool'), reservoir_1km=cnt('reservoir'),
            conduit_1km=cnt('conduit'), spring_well_1km=cnt('spring_well'), tomb_1km=cnt('tomb'), cave_1km=cnt('cave'),
            n_features_1km_dated_yes=str(sum(1 for r in f1 if r['dated_in_window'] == 'yes')),
            n_features_1km_dated_partly=str(sum(1 for r in f1 if r['dated_in_window'] == 'partly')),
            n_sites_1km_finds_in_window_yes=str(sum(1 for s in s1 if s['site_finds_in_window'] == 'yes'))))
    write_csv(os.path.join(out, 'place_summary.csv'), PLACE_COLS, prow)

    # maps used
    cov = {}
    with open(os.path.join(C.FOLDER, 'coverage_statements.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            cov[r['asi_map_id']] = r
    manifest = {}
    mpath = os.path.join(cache, 'manifest.csv')
    if os.path.exists(mpath):
        with open(mpath, encoding='utf-8') as f:
            manifest = {r['cache_file']: r for r in csv.DictReader(f)}
    mrows = []
    for mid in mids:
        m, sh, st = online[mid], sheets[mid], map_stats[mid]
        ie = C.cache_name('Service_Eng.aspx/GetMapIntro', mapId=mid)
        ih = C.cache_name('Service.aspx/GetMapIntro', mapId=mid)
        mrows.append(dict(
            asi_map_id=mid, map_num=m['map_num'], name=C.clean(m['name']), author=C.clean(m.get('Author') or ''),
            isbn=m.get('isbn') or '', lat_lo=fmt(sh['lat_lo']), lat_hi=fmt(sh['lat_hi']), lon_lo=fmt(sh['lon_lo']),
            lon_hi=fmt(sh['lon_hi']), n_sites_online=str(st['n_online']), n_sites_in_sites_csv=str(st['n_in']),
            n_records_fetched_in_sites_csv=str(st['n_rec']),
            places_within_3km_of_sheet=';'.join(p['place_id'] for p in sorted(places, key=lambda p: p['place_id'])
                                                 if C.rect_km(p['lat_f'], p['lon_f'], sh['lat_lo'], sh['lat_hi'], sh['lon_lo'], sh['lon_hi']) <= 3.0),
            coverage_value=cov.get(mid, {}).get('coverage_value', ''),
            coverage_statement_type=cov.get(mid, {}).get('statement_type', 'not read'),
            intro_en_sha256=manifest.get(ie, {}).get('sha256', ''), intro_he_sha256=manifest.get(ih, {}).get('sha256', '')))
    write_csv(os.path.join(out, 'maps_used.csv'), MAP_COLS, mrows)

    # looks
    looks = build_looks(plan, places, pmap, sites, frows, mids, online, sheets, cov)
    with open(os.path.join(C.REPO, plan['inputs']['looks_schema']['path']), encoding='utf-8') as f:
        look_cols = next(csv.reader(f))
    write_csv(os.path.join(out, 'looks_asi.csv'), look_cols, looks)

    # post-hoc Hebrew check (plan_amendment_2_posthoc.json); frozen columns above are unchanged
    with open(os.path.join(C.FOLDER, 'plan_amendment_2_posthoc.json'), encoding='utf-8') as f:
        hv2 = [(k, re.compile(v)) for k, v in json.load(f)['patterns'].items()]
    hrows = []
    for s in sites:
        found = [k for k, rx in hv2 if rx.search(s['_he_text'])]
        hrows.append(dict(record_id=s['record_id'], asi_map_id=s['asi_map_id'], site_num=s['site_num'],
                          classes_he_v2=';'.join(found),
                          heb_only_v2=';'.join(k for k in found if k not in s['_classes'])))
    write_csv(os.path.join(out, 'hebrew_check_v2.csv'), HEB2_COLS, hrows)

    # source manifest (URLs and hashes of what was read; no content)
    srows = []
    for k in sorted(manifest):
        r = manifest[k]
        srows.append(dict(url=r['url'], http_status=r['http_status'], bytes=r['bytes'], sha256=r['sha256'],
                          fetched_utc=r['fetched_utc']))
    srows.sort(key=lambda r: r['url'])
    write_csv(os.path.join(out, 'sources_manifest.csv'), ['url', 'http_status', 'bytes', 'sha256', 'fetched_utc'], srows)
    return dict(sites=len(sites), features=len(frows), looks=len(looks), maps=len(mids))


def build_looks(plan, places, pmap, sites, frows, mids, online, sheets, cov):
    L = plan['looks']
    cross = L['lookable_landmark_crosswalk']
    repo = C.REPO
    entries_path = os.path.join(repo, os.path.dirname(plan['inputs']['places']['path']), 'entries_v2.csv')
    with open(entries_path, encoding='utf-8') as f:
        eorder = {r['entry']: int(r['order']) for r in csv.DictReader(f)}
    with open(os.path.join(repo, plan['inputs']['entry_landmarks']['path']), encoding='utf-8') as f:
        landmarks = {r['entry']: [x for x in r['landmarks'].split(';') if x] for r in csv.DictReader(f)}
    with open(os.path.join(repo, plan['inputs']['candidates']['path']), encoding='utf-8') as f:
        cands = list(csv.DictReader(f))
    feats_by_site = {}
    for r in frows:
        feats_by_site.setdefault(r['record_id'], set()).add(r['feature_class'])
    dated_by_site = {}
    for r in frows:
        if r['dated_in_window'] in ('yes', 'partly'):
            dated_by_site.setdefault(r['record_id'], set()).add(r['feature_class'])
    rows = []
    for c in cands:
        pid, entry = c['place_id'], c['entry']
        if pid not in pmap:
            continue
        p = pmap[pid]
        lms = sorted(lm for lm in landmarks.get(entry, []) if lm in cross)
        if not lms:
            continue
        for mid in mids:
            sh = sheets[mid]
            if C.rect_km(p['lat_f'], p['lon_f'], sh['lat_lo'], sh['lat_hi'], sh['lon_lo'], sh['lon_hi']) > 1.0:
                continue
            m = online[mid]
            author = C.clean(m.get('Author') or '')
            msites = [s for s in sites if s['asi_map_id'] == mid and any(q == pid for _, q in s['_near1'])]
            n_norec = sum(1 for s in msites if s['record_fetched'] == 'no')
            inside = circle_inside(p['lat_f'], p['lon_f'], sh, 1.0)
            cs = cov.get(mid, {})
            if cs.get('coverage_value') and inside:
                coverage = cs['coverage_value']
                cov_basis = f"EVIDENCE: the introduction states '{cs['coverage_quote']}' ({cs['citation']}); the 1 km circle lies inside the sheet"
            else:
                coverage = ''
                why = []
                if cs.get('coverage_quote'):
                    why.append(f"the introduction says '{cs['coverage_quote']}' ({cs['statement_type']})")
                else:
                    why.append('no coverage statement found in the introduction')
                if not inside:
                    why.append('the 1 km circle extends beyond this sheet')
                cov_basis = 'UNKNOWN: ' + '; '.join(why)
            det = cs.get('detection_quote', '')
            prec_basis = ('UNKNOWN: no detection rate stated' + (f"; the introduction says '{det}'" if det else ''))
            for lm in lms:
                cls = cross[lm]
                hits = [s for s in msites if feats_by_site.get(s['record_id'], set()) & set(cls)]
                hits.sort(key=lambda s: int(s['site_num'] or 0))
                nums = ', '.join(s['site_num'] for s in hits)
                dated = [s['site_num'] for s in hits if dated_by_site.get(s['record_id'], set()) & set(cls)]
                if hits:
                    result = 'reported'
                    rbasis = f"EVIDENCE: ASI record(s) within 1 km coded {'/'.join(cls)} by the frozen keyword rule (sites {nums})"
                    record = f"{author}, ASI Map of {C.clean(m['name'])} ({m['map_num']}), sites {nums} (survey.iaa.org.il; printed pages not given online)"
                    sat = 'unknown'
                else:
                    result = 'silent'
                    rbasis = f"EVIDENCE: none of the {len(msites)} records of this map within 1 km is coded {'/'.join(cls)} by the frozen keyword rule"
                    record = f"{author}, ASI Map of {C.clean(m['name'])} ({m['map_num']}), records within 1 km of the place (survey.iaa.org.il; printed pages not given online)"
                    sat = ''
                notes = []
                if hits:
                    notes.append(f"{len(dated)} of {len(hits)} hit sites date a matching feature in or partly in the window by the record text" + (f" (sites {', '.join(dated)})" if dated else ''))
                if n_norec:
                    notes.append(f"{n_norec} of {len(msites)} sites within 1 km coded from GeoJSON text only (record not fetched)")
                if any(s['protected_zone_nearby'] == 'yes' for s in msites):
                    notes.append('a record within 1 km of Tell es-Sultan is involved; not usable as unseen evidence for the protected strip')
                notes.append('No identification is implied.')
                rows.append(dict(
                    _sort=(eorder.get(entry, 999), pid, lm, int(mid)),
                    entry_id=entry, place_id=pid, relation_id=f"R-E{entry}-{lm.upper()}",
                    required_feature=f"{lm} (T02 entry_features landmark class; ASI classes {'/'.join(cls)})",
                    reading_condition=c.get('conditional_on_reading', ''), placement_relevant='yes',
                    record=record, record_key=f"ASI Map {m['map_num']}", record_id='',
                    lineage=f"ASI Map {m['map_num']} field survey ({author})",
                    looked_at=f"ASI Map {m['map_num']} sheet within 1 km of {pid} ({len(msites)} records within 1 km)",
                    coverage=coverage, coverage_basis=cov_basis,
                    p_recognise='', p_recognise_basis=prec_basis,
                    p_report='', p_report_basis='UNKNOWN: the source gives no reporting rate',
                    p_survive='', p_survive_basis='UNKNOWN: not stated',
                    result=result, result_basis=rbasis, satisfies_requirement=sat, counted_via='',
                    project_use='research/regional/asi_jerusalem (exploratory; not used by the model)',
                    notes='; '.join(notes)))
    rows.sort(key=lambda r: r['_sort'])
    for i, r in enumerate(rows, 1):
        r['look_id'] = f'ASI-L{i:03d}'
        del r['_sort']
    return rows


def write_csv(path, cols, rows):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in cols})


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    res = build(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else C.FOLDER)
    print(json.dumps(res, sort_keys=True))
