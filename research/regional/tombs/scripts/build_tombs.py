#!/usr/bin/env python3
"""Build tombs.csv, scores.csv, scores_summary.csv and features_summary.csv from the frozen plan.

Run from the repository root:
    python3 -I research/regional/tombs/scripts/build_tombs.py ASI_CACHE WBADB_XLSX [OUT_DIR]
ASI_CACHE is the folder written by fetch_asi_maps.py; WBADB_XLSX is WBADB_data1.xlsx (hash checked).
OUT_DIR defaults to the lane folder. Rules: the JSON block of PLAN.md (commit cd394d7).
Source HK (IAA Reports 7, added 11 October 2026) is read from data/hk_units.csv, coded as PLAN_AMENDMENT_2 Part A
fixes; its units are numbered after the frozen build's 1,055, and scores_summary.csv gains the view lineage_HK.
Manual checks (PLAN §5) are read from data/manual_check.csv; each one names the unit, the code and
the decision. Nothing else is set by hand.
"""
import csv
import json
import os
import re
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tombs_common as T  # noqa: E402

WBADB_SHA256 = '3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b'
DATA = os.path.join(T.FOLDER, 'data')
HAESI = os.path.join(T.REPO, 'research', 'regional', 'haesi_features')

MANUAL_CODES = ('F1', 'F2', 'F2x', 'F3', 'F5', 'F6', 'F7w', 'name_zadok', 'name_absalom', 'name_queen',
                'name_obed', 'name_jericho')


class Coder:
    def __init__(self, plan):
        self.p = plan
        rx = T.term_regex
        self.tomb = rx(plan['tomb_terms'])
        self.mon = rx(plan['monument_terms'])
        self.porch = rx(plan['porch_terms'])
        self.col = rx(plan['column_terms'])
        self.interior = rx(plan['interior_terms'])
        self.insc = rx(plan['inscription_terms'])
        self.namecue = rx(plan['name_cues'])
        self.opening = rx(plan['opening_terms'])
        self.kokh = rx(plan['kokh_terms'])
        self.oss = rx(plan['ossuary_terms'])
        self.repo = rx(plan['repository_terms'])
        self.slab = rx(plan['slab_terms'])
        self.cistern = rx(['cistern'])
        self.channel = rx(plan['channel_terms'])
        self.wadi = rx(plan['wadi_terms'])
        self.gravef = rx(plan['grave_field_terms'])
        self.famtype = rx(plan['family_type_terms'])
        self.unused = rx(plan['unused_terms'])
        self.garden = rx(['garden'])
        self.pillar = rx(['pillar'])
        self.scroll = rx(plan['scroll_mention_terms'])
        self.names = {k: rx(v) for k, v in plan['names'].items()}
        dirs = []
        for code, words in plan['direction_terms'].items():
            for w in words:
                dirs.append((w, code))
        dirs.sort(key=lambda x: len(x[0]), reverse=True)
        self.dirs = dirs
        nums = plan['chamber_number_words']
        nouns = sorted(plan['chamber_nouns'], key=len, reverse=True)
        self.chnum = re.compile(r'(?<![\w])(' + '|'.join(list(nums) + [r'\d+']) + r')\s+(?:[\w\-]+\s+){0,2}?('
                                + '|'.join(re.escape(n).replace(r'\ ', r'\s+') for n in nouns) + r')(?![\w])',
                                re.IGNORECASE)
        self.single = T.term_regex(plan['single_chamber_phrases'])
        self.numwords = nums

    def directions(self, s):
        masked, found = s, []
        for w, code in self.dirs:
            r = re.compile(r'(?<![\w])' + re.escape(w) + r'(?![\w])', re.IGNORECASE)
            if r.search(masked):
                found.append(code)
                masked = r.sub(lambda m: '#' * len(m.group(0)), masked)
        return found

    def code(self, text, period_text=None, period_flags=()):
        """Return the feature codes of one unit. period_text replaces the sentence rule (WBADB)."""
        f = OrderedDict()
        sents = T.sentences(text)
        tomb_sents = [s for s in sents if self.tomb.search(s)]
        f['tomb_terms'] = ';'.join(sorted({t.lower() for t in T.find_terms(self.tomb, text)}))
        # dating (PLAN §4)
        if period_text is not None:
            w, pa, o = T.period_classes(self.p, period_text)
            if w:
                strict = 'yes'
            elif pa or period_flags:
                strict = 'partly'
            elif o:
                strict = 'no'
            else:
                strict = 'unknown'
            st_labels = w + pa + o + list(period_flags)
            # lenient (PLAN §4): "Second Temple" in the period text or in a sentence with a TOMB term
            tomb_pa = [x for s in tomb_sents for x in T.period_classes(self.p, s)[1]]
            second_temple = any(x.lower() == 'second temple' for x in pa + tomb_pa)
            w_any = T.period_classes(self.p, text + ' ' + period_text)[0]
        else:
            W, PA, O = [], [], []
            for s in tomb_sents:
                w, pa, o = T.period_classes(self.p, s)
                W += w
                PA += pa
                O += o
            strict = 'yes' if W else 'partly' if PA else 'no' if O else 'unknown'
            st_labels = W + PA + O
            second_temple = any(x.lower() == 'second temple' for x in PA)
            w_any = T.period_classes(self.p, text)[0]
        f['period_terms'] = ';'.join(dict.fromkeys(st_labels))
        f['dated_in_window'] = strict
        f['dated_lenient'] = 'yes' if (strict == 'yes' or second_temple or w_any) else 'no-evidence'
        # features (PLAN §5)
        mon = T.find_terms(self.mon, text)
        f['F1'] = 'yes' if mon else 'unknown'
        f['F1_terms'] = ';'.join(dict.fromkeys(m.lower() for m in mon))
        f2 = [s for s in sents if self.porch.search(s) and self.col.search(s)]
        f['F2'] = 'yes' if f2 else 'unknown'
        f['F2_terms'] = ';'.join(dict.fromkeys(t.lower() for s in f2 for t in T.find_terms(self.porch, s) + T.find_terms(self.col, s)))
        f2x = f2 or [s for s in sents if self.porch.search(s) and self.pillar.search(s)]
        f['F2x'] = 'yes' if f2x else 'unknown'
        f3 = [s for s in sents if self.col.search(s) and self.interior.search(s) and not self.porch.search(s)]
        f['F3'] = 'yes' if f3 else 'unknown'
        f['F3_terms'] = ';'.join(dict.fromkeys(t.lower() for s in f3 for t in T.find_terms(self.col, s)))
        insc_s = [s for s in sents if self.insc.search(s)]
        f['F4'] = 'yes' if insc_s else 'unknown'
        f5 = [s for s in insc_s if self.namecue.search(s)]
        f['F5'] = 'yes' if f5 else 'unknown'
        f['F5_terms'] = ';'.join(dict.fromkeys(t.lower() for s in f5 for t in T.find_terms(self.namecue, s)))
        gardens = [s for s in sents if self.garden.search(s)]
        f['garden_mention'] = 'yes' if gardens else 'no-evidence'
        f['F6'] = 'yes' if any(T.period_classes(self.p, s)[0] for s in gardens) else 'unknown'
        dirs = []
        for s in sents:
            if self.opening.search(s):
                dirs += self.directions(s)
        dirs = list(dict.fromkeys(dirs))
        f['F7'] = ';'.join(dirs) if dirs else 'unknown'
        if not dirs:
            f['F7w'] = 'unknown'
        elif any(d in self.p['westerly'] for d in dirs):
            f['F7w'] = 'yes'
        else:
            f['F7w'] = 'no'
        nmax = 0
        for m in self.chnum.finditer(text):
            g = m.group(1).lower()
            n = int(g) if g.isdigit() else self.numwords.get(g, 0)
            nmax = max(nmax, n)
        if nmax >= 2:
            f['F10'] = 'yes'
        elif self.single.search(text):
            f['F10'] = 'no'
        else:
            f['F10'] = 'unknown'
        f['F10_n'] = str(nmax) if nmax else ''
        for code, r in (('F11', self.kokh), ('F12', self.oss), ('F13', self.repo), ('F14', self.slab),
                        ('F16', self.cistern), ('F17', self.channel), ('F19', self.wadi), ('F21', self.unused)):
            hits = T.find_terms(r, text)
            f[code] = 'yes' if hits else 'unknown'
            f[code + '_terms'] = ';'.join(dict.fromkeys(h.lower() for h in hits))
        gf, ft = bool(self.gravef.search(text)), bool(self.famtype.search(text))
        f['F20_communal'] = 'yes' if (gf and not ft) else 'no' if (ft and not gf) else 'unknown'
        f['F4_any_inscription'] = f['F4']
        scroll = bool(self.scroll.search(text))
        f['scroll_mention'] = 'yes' if scroll else 'no'
        for k, r in self.names.items():
            hits = T.find_terms(r, text)
            in_insc = any(r.search(s) for s in insc_s)
            if scroll:
                f['name_' + k] = 'unknown'
            else:
                f['name_' + k] = 'yes' if hits else 'unknown'
            f['name_' + k + '_in_inscription'] = 'yes' if (in_insc and not scroll) else 'unknown'
        return f


# ---------------------------------------------------------------- sources
def asi_units(plan, cache):
    with open(os.path.join(cache, 'selected_maps.json'), encoding='utf-8') as fh:
        sel = json.load(fh)
    units, sheets = [], []
    for s in sel:
        sheets.append(s)
        with open(os.path.join(cache, f"GetPolygonsSites_Eng__MapId-{s['map_id']}.json"), encoding='utf-8') as fh:
            d = json.load(fh)['d']
        for ft in d['features']:
            pr = ft.get('properties')
            pr = {p.get('key'): p.get('value') for p in pr} if isinstance(pr, list) else dict(pr or {})
            lon, lat = ft['geometry']['coordinates'][:2]
            name = T.clean(pr.get('name_heb'))
            desc = T.clean(pr.get('description_heb'))
            finds = T.clean(pr.get('finding_heb'))
            text = '. '.join(x for x in (name, desc, finds) if x)
            units.append(dict(source='ASI', record_id=f"ASI {s['map_num']}/{pr.get('site_num')}",
                              locator=f"ASI Map {s['map_num']} ({s['name']}), site {pr.get('site_num')}; "
                                      f"https://survey.iaa.org.il/#/MapSurvey/{s['map_id']}/site/{pr.get('id')}",
                              name=name, lat=float(lat), lon=float(lon), unc=plan['position_uncertainty_km']['ASI'],
                              text=text, period_text=None, flags=(), text_hash=T.sha256_text(text),
                              asi_site_id=str(pr.get('id')), map_num=s['map_num']))
    return units, sheets


def wbadb_units(plan, xlsx):
    import pandas as pd
    from pyproj import Transformer
    if T.sha256_file(xlsx) != WBADB_SHA256:
        raise SystemExit('WBADB hash differs from the frozen value')
    tr = Transformer.from_crs('EPSG:28193', 'EPSG:4326', always_xy=True)
    book = pd.ExcelFile(xlsx)
    out = []
    for sheet, pref in (('Surveyed', 'S'), ('Excavations', 'E')):
        df = book.parse(sheet)
        for _, r in df.iterrows():
            try:
                x, y = float(r['X']), float(r['Y'])
            except (TypeError, ValueError):
                continue
            if x != x or y != y:
                continue
            lon, lat = tr.transform(x, y + 1_000_000)

            def val(c):
                v = r.get(c)
                if isinstance(v, str) and v.strip() not in ('', '-', 'NDA'):
                    return v.strip()
                return ''
            name = val('Site_Name')
            text = '. '.join(x for x in (name, val('Other_Names'), val('Site_Components'), val('More_Components'),
                                         val('Comments'), val('More_Comments')) if x)
            ptext = ' ; '.join(x for x in (val('Major_Periods'), val('Other_Periods')) if x)
            flags = []
            for c in ('Hel', 'Rom'):
                try:
                    if int(r.get(c)) > 0:
                        flags.append(c)
                except (TypeError, ValueError):
                    pass
            surveyed_dup = sheet == 'Excavations' and str(r.get('Surveyed', '')).strip().lower() == 'yes'
            ssn = val('Survey_Site_Number')
            sref = val('Survey_Ref')
            tier1 = bool(re.match(r'^[IVX]+/\d+', ssn)) and '2002' in sref
            out.append(dict(source='WBADB', record_id=f"WBADB {pref}{int(r['Index'])}", tier1_lineage=tier1,
                            locator=f"WBADB_data1.xlsx sheet {sheet}, Index {int(r['Index'])}; grid {int(x)}/{int(y)} (OIG, no false northing)"
                                    + (f"; survey ref {sref}" if sref else ''),
                            name=name, lat=lat, lon=lon, unc=plan['position_uncertainty_km']['WBADB'],
                            text=text, period_text=ptext, flags=tuple(flags), text_hash=T.sha256_text(text + '|' + ptext),
                            wbadb_excavation_also_surveyed=surveyed_dup))
    return out


def haesi_units(plan):
    out = []
    for fn, located in (('features.csv', True), ('features_unlocated.csv', False)):
        with open(os.path.join(HAESI, fn), encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                text = '. '.join(x for x in (r['site_name'], r['feature_type'].replace('_', ' '), r['quote'],
                                             r['period_as_given']) if x)
                try:
                    lat, lon = float(r['lat']), float(r['lon'])
                except (TypeError, ValueError):
                    lat = lon = None
                unc = plan['position_uncertainty_km']['HAESI_default']
                try:
                    unc = max(unc, float(r['precision_m']) / 1000.0)
                except (TypeError, ValueError):
                    pass
                out.append(dict(source='HAESI', record_id=f"HAESI {r['report_id']} {r['feature_type']}",
                                locator=f"{r['series']} {r['volume']} ({r['year']}) p. {r['pages']}; {r['url']}",
                                name=r['site_name'], lat=lat, lon=lon, unc=unc, text=text, period_text=None, flags=(),
                                text_hash=T.sha256_text(text), haesi_dated=r['dated_in_window'] or 'unknown',
                                haesi_located=located and lat is not None))
    return out


HK_ANCHOR = 'WBADB S2446'   # the WBADB row for this cemetery (Amendment 2, Part A.4)
HK_UNC_KM = 16.0            # the cemetery's extent as the report states it: "16 km long" (p. 166)
HK_REF = 'Hachlili and Killebrew 1999, Jericho: The Jewish Cemetery of the Second Temple Period (IAA Reports 7)'
ADDENDUM_SOURCES = ('HK',)  # numbered after the 1,055 units of the frozen build, so no earlier unit id moves


def hk_units(plan, anchor_lat, anchor_lon):
    """Source HK (PLAN §3), coded from data/hk_units.csv as Amendment 2, Part A fixes: one transcription per tomb,
    position = the WBADB cemetery point, uncertainty = the extent the report states."""
    out = []
    with open(os.path.join(DATA, 'hk_units.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            typ = f"; Type {r['report_type']} (p. 59)" if r['report_type'] else ''
            ins = f"; {r['inscriptions']}" if r['inscriptions'] else ''
            out.append(dict(source='HK', record_id=f"HK {r['record_id']}",
                            locator=f"{HK_REF}, Hill {r['hill']}, pp. {r['pages']}; Figs. {r['figures']}{typ}{ins}; "
                                    f"position = {HK_ANCHOR} point (no grid given), ±{HK_UNC_KM:g} km (p. 166)",
                            name=f"Jericho, Tomb {r['record_id']}" if not r['record_id'].startswith('nefesh')
                            else f"Jericho, Hill D {r['record_id']}",
                            lat=anchor_lat, lon=anchor_lon, unc=HK_UNC_KM, text=r['text'], period_text=None,
                            flags=(), text_hash=T.sha256_text(r['text']), linked_to=r['linked_to']))
    return out


def kenyon_units(plan):
    out = []
    lat, lon = plan['points']['tell_es_sultan']
    with open(os.path.join(DATA, 'kenyon_ii_units.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            out.append(dict(source='KEN', record_id=f"Kenyon II {r['record_id']}",
                            locator=f"Kenyon, Excavations at Jericho II (1965), p. {r['page']}, Area {r['area']}; via {r['source_note']}",
                            name=f"Jericho tomb {r['record_id']}", lat=lat, lon=lon,
                            unc=plan['position_uncertainty_km']['KEN'], text=r['text'], period_text=None, flags=(),
                            text_hash=T.sha256_text(r['text'])))
    return out


# ---------------------------------------------------------------- scoring
def clause_value(plan, u, clause, sens=False):
    P, tol, unc = plan['points'], plan['tolerances_km'], u['unc']
    if u['lat'] is None:
        if clause.startswith('L_') and clause != 'L_name_only':
            return 'unknown'
    if clause == 'L_millo':
        return T.loc_clause(T.km(u['lat'], u['lon'], *P['jer_south_wall']), tol['L_millo'], unc)
    if clause == 'L_south_corner':
        t = tol['L_south_corner_sensitivity'] if sens else tol['L_south_corner']
        return T.loc_clause(T.km(u['lat'], u['lon'], *P['jer_south_wall']), t, unc)
    if clause == 'L_temple':
        return T.loc_clause(T.km(u['lat'], u['lon'], *P['jer_temple']), tol['L_temple'], unc)
    if clause == 'L_road':
        t = plan['regions']['B2_sensitivity_halfwidth_km'] if sens else plan['regions']['B2_halfwidth_km']
        return T.loc_clause(u['d_road_km'], t, unc)
    if clause == 'L_east_road':
        return T.loc_clause(T.km(u['lat'], u['lon'], *P['wadi_qumran']), tol['L_east_road'], unc)
    if clause == 'L_jericho':
        if T.loc_clause(u['d_jericho_km'], plan['regions']['B1_radius_km'], unc) == 'yes':
            return 'yes'
        return 'yes' if u['name_jericho'] == 'yes' else 'unknown'
    if clause == 'L_name_only':
        return 'unknown'
    if clause == 'F20_family':
        return {'yes': 'no', 'no': 'yes'}.get(u['F20_communal'], 'unknown')
    return u[clause]


def overall(vals):
    if all(v == 'yes' for v in vals):
        return 'match'
    if any(v == 'no' for v in vals):
        return 'fail'
    return 'unknown'


def exposure_of(u, listed, asi_lane_ids):
    """Exposure status of a unit (PLAN §1); listed = data/exposure.csv."""
    if u['record_id'] in listed:
        return 'exposed: ' + listed[u['record_id']]
    if u['source'] == 'KEN':
        return 'exposed: repo extraction of Kenyon II read before the freeze'
    if u['source'] == 'HK':
        return ("exposed: PLAN §1 lists Jericho's cemetery as exposed; this tomb record (IAA Reports 7) was first read "
                "on 11 Oct, after the freeze")
    if u['source'] == 'HAESI':
        return 'repo-coded by the HA-ESI lane (9 Oct); rows not seen by this lane before the freeze'
    if u.get('tier1_lineage'):
        return ('first read after the freeze (unexposed at freeze); WBADB summary of a cave of the 2002 northern '
                'Judean Desert cave survey (ʿAtiqot 41 lineage, a Tier 1 source)')
    if u['source'] == 'ASI' and u['record_id'] in asi_lane_ids:
        return 'repo-coded by the ASI lane (9 Oct); first read in full by this lane after the freeze'
    return 'first read after the freeze (unexposed at freeze)'


def build_units(cache, xlsx):
    plan = T.load_plan()
    coder = Coder(plan)
    asi, sheets = asi_units(plan, cache)
    wb = wbadb_units(plan, xlsx)
    anchor = [u for u in wb if u['record_id'] == HK_ANCHOR][0]
    units = asi + wb + haesi_units(plan) + kenyon_units(plan) + hk_units(plan, anchor['lat'], anchor['lon'])

    # eligibility and region
    elig = []
    for u in units:
        if not coder.tomb.search(u['text']):
            continue
        if u['source'] == 'HAESI' and u['lat'] is None:
            u.update(d_temple_km=None, d_jericho_km=None, d_road_km=None, in_A=None, in_A3=None, in_B1=None,
                     in_B2=None, in_B2_5=None)
            u['region_note'] = 'unlocated HA-ESI report (Jerusalem by title); not counted'
            elig.append(u)
            continue
        fl = T.region_flags(plan, u['lat'], u['lon'])
        if not (fl['in_A'] or fl['in_B1'] or fl['in_B2_5']):
            continue
        u.update(fl)
        u['region_note'] = ''
        elig.append(u)

    # coding
    for u in elig:
        c = coder.code(u['text'], u['period_text'], u['flags'])
        if u['source'] == 'HAESI':
            c['dated_in_window'] = u['haesi_dated'] if u['haesi_dated'] in ('yes', 'no') else 'unknown'
            c['dated_lenient'] = 'yes' if (c['dated_in_window'] == 'yes' or c['dated_lenient'] == 'yes') else 'no-evidence'
        u.update(c)
        u['multi_tomb_record'] = 'yes' if re.search(
            r'(?<![\w])(two|three|four|five|six|seven|eight|nine|ten|several|many|\d+)\s+(?:[\w\-]+\s+){0,2}?(burial caves|tombs|graves|caves|kokhim tombs)(?![\w])',
            u['text'], re.I) or re.search(r'(?<![\w])(cemetery|necropolis|burial caves|tombs|graves)(?![\w])', u['text'], re.I) else 'no'
        # ASI sheets: a point inside any selected sheet
        u['in_asi_sheet'] = 'yes' if u['lat'] is not None and any(
            s['lat_lo'] <= u['lat'] <= s['lat_hi'] and s['lon_lo'] <= u['lon'] <= s['lon_hi'] for s in sheets) else 'no'

    # manual check
    checks = {}
    mpath = os.path.join(DATA, 'manual_check.csv')
    if os.path.exists(mpath):
        with open(mpath, encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                checks[(r['record_id'], r['code'])] = r
    pending = []
    for u in elig:
        u['manual_rejected'] = ''
        for code in MANUAL_CODES:
            u[code + '_raw'] = u[code]
            if u[code] == 'yes':
                ck = checks.get((u['record_id'], code))
                if ck is None:
                    pending.append((u['record_id'], code))
                elif ck['decision'] == 'reject':
                    u[code] = 'unknown'
                    u['manual_rejected'] += f"{code}: {ck['reason']}; "
    # F2x follows a rejected F2 only when its own check says so (checked separately)

    # duplicates (PLAN §3)
    def primary(u):
        if u['source'] == 'ASI':
            return True
        if u['source'] == 'WBADB':
            return u['in_asi_sheet'] == 'no' and not u.get('wbadb_excavation_also_surveyed')
        return False
    prim = [u for u in elig if primary(u) and u['lat'] is not None]
    for u in elig:
        u['possible_duplicate_of'] = ''
        if primary(u) or u['lat'] is None:
            continue
        best = None
        nn = T.norm_name(u['name'])
        for p in prim:
            d = T.km(u['lat'], u['lon'], p['lat'], p['lon'])
            same = nn and nn == T.norm_name(p['name'])
            if d <= plan['duplicate_km'] or (same and d <= plan['duplicate_same_name_km']):
                if best is None or d < best[0]:
                    best = (d, p['record_id'])
        if best:
            u['possible_duplicate_of'] = best[1]
        elif u['source'] == 'WBADB' and u.get('wbadb_excavation_also_surveyed'):
            u['possible_duplicate_of'] = 'WBADB survey row (Excavations row marked Surveyed)'

    # unit ids: the frozen build's units keep their ids; addendum sources follow, in natural order
    def natural(s):
        return tuple((0, int(p)) if p.isdigit() else (1, p) for p in re.findall(r'\d+|\D+', s))

    def id_key(x):
        add = x['source'] in ADDENDUM_SOURCES
        return (add, x['source'], natural(x['record_id']) if add else x['record_id'])
    for i, u in enumerate(sorted(elig, key=id_key)):
        u['unit_id'] = f"T{i + 1:04d}"

    # exposure (PLAN §1)
    listed = {}
    with open(os.path.join(DATA, 'exposure.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            listed[r['record_id']] = r['reason']
    asi_lane_ids = set()
    with open(os.path.join(T.REPO, 'research', 'regional', 'asi_jerusalem', 'sites.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            asi_lane_ids.add(f"ASI {r['map_num']}/{r['site_num']}")
    for u in elig:
        u['exposure'] = exposure_of(u, listed, asi_lane_ids)
    # exploratory enrichment from the repo's Allegro 1964 extraction (PLAN §6): reported, never scored
    enrich = {}
    with open(os.path.join(DATA, 'enrichment_a64.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            enrich.setdefault(r['record_id'], []).append(f"{r['code']}={r['value']} ({r['page']})")
    for u in elig:
        u['enrich_A64'] = '; '.join(enrich.get(u['record_id'], []))
    return plan, coder, elig, sheets, pending


def main(cache, xlsx, out_dir):
    plan, coder, elig, sheets, pending = build_units(cache, xlsx)

    # ---------------------------------------------------------------- write tombs.csv
    tcols = ['unit_id', 'source', 'record_id', 'locator', 'name', 'lat', 'lon', 'crs', 'position_uncertainty_km',
             'd_temple_km', 'd_jericho_km', 'd_road_km', 'in_A', 'in_A3', 'in_B1', 'in_B2', 'in_B2_5', 'region_note',
             'in_asi_sheet', 'possible_duplicate_of', 'linked_to', 'multi_tomb_record', 'tomb_terms',
             'monument_F1', 'F1_terms', 'porch_F2', 'F2_terms', 'exedra_pillar_F2x', 'inside_pillar_F3', 'F3_terms',
             'chambers_F10', 'F10_n', 'inscription_F4', 'named_inscription_F5', 'F5_terms', 'setting_wadi_F19', 'F19_terms',
             'garden_mention', 'garden_ancient_F6', 'entrance_orientation_F7', 'west_facing_F7w',
             'kokhim_F11', 'ossuaries_F12', 'repository_F13', 'slab_F14', 'F14_terms', 'cistern_F16', 'channel_F17',
             'communal_F20', 'unused_F21',
             'name_zadok', 'name_absalom', 'name_queen', 'name_obed', 'name_jericho',
             'name_obed_in_inscription', 'name_queen_in_inscription', 'scroll_mention',
             'period_terms', 'dated_in_window', 'dated_lenient', 'manual_rejected', 'raw_yes_before_check',
             'exposure', 'enrich_A64', 'text_sha256']
    ren = {'monument_F1': 'F1', 'porch_F2': 'F2', 'exedra_pillar_F2x': 'F2x', 'inside_pillar_F3': 'F3',
           'chambers_F10': 'F10', 'inscription_F4': 'F4', 'named_inscription_F5': 'F5', 'setting_wadi_F19': 'F19',
           'garden_ancient_F6': 'F6', 'entrance_orientation_F7': 'F7', 'west_facing_F7w': 'F7w',
           'kokhim_F11': 'F11', 'ossuaries_F12': 'F12', 'repository_F13': 'F13', 'slab_F14': 'F14',
           'cistern_F16': 'F16', 'channel_F17': 'F17', 'communal_F20': 'F20_communal', 'unused_F21': 'F21'}
    rows = []
    for u in sorted(elig, key=lambda x: x['unit_id']):
        r = {}
        for c in tcols:
            k = ren.get(c, c)
            if c == 'crs':
                r[c] = 'EPSG:4326'
            elif c == 'position_uncertainty_km':
                r[c] = u['unc']
            elif c == 'raw_yes_before_check':
                r[c] = ';'.join(code for code in MANUAL_CODES if u.get(code + '_raw') == 'yes')
            elif c == 'text_sha256':
                r[c] = u['text_hash']
            elif c in ('lat', 'lon'):
                r[c] = '' if u[c] is None else f"{u[c]:.6f}"
            elif c.startswith('d_'):
                r[c] = '' if u.get(c) is None else f"{u[c]:.3f}"
            elif c.startswith('in_') and c != 'in_asi_sheet':
                r[c] = '' if u.get(c) is None else ('yes' if u[c] else 'no')
            else:
                v = u.get(k, '')
                r[c] = v
        rows.append(r)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'tombs.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=tcols, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

    # ---------------------------------------------------------------- scores
    branches = plan['branches']
    scols = ['unit_id', 'record_id', 'branch', 'values', 'result', 'result_sensitivity']
    srows = []
    located = [u for u in elig if u['lat'] is not None]
    for b, spec in branches.items():
        if not spec['clauses']:
            continue
        for u in sorted(located, key=lambda x: x['unit_id']):
            vals = [clause_value(plan, u, c) for c in spec['clauses']]
            svals = [clause_value(plan, u, c, sens=True) for c in spec['clauses']]
            srows.append(dict(unit_id=u['unit_id'], record_id=u['record_id'], branch=b,
                              values=';'.join(vals), result=overall(vals),
                              result_sensitivity=overall(svals)))
    with open(os.path.join(out_dir, 'scores.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=scols, lineterminator='\n')
        w.writeheader()
        w.writerows(srows)

    # ---------------------------------------------------------------- summaries
    def in_region(u, reg):
        return {'A': u['in_A'], 'A3': u['in_A3'], 'B': u['in_B1'] or u['in_B2'], 'B1': u['in_B1'],
                'B2': u['in_B2'], 'B2_5': u['in_B2_5'], 'AB': u['in_A'] or u['in_B1'] or u['in_B2']}[reg]

    def in_dateset(u, ds):
        return {'strict': u['dated_in_window'] == 'yes', 'lenient': u['dated_lenient'] == 'yes', 'any': True}[ds]

    def in_view(u, view):
        if view.startswith('lineage_'):   # PLAN §3: each lineage is also counted on its own (duplicates included)
            return u['source'] == view[len('lineage_'):]
        return view == 'all_lineages' and not u['possible_duplicate_of'] or view == 'primary' and (
            u['source'] == 'ASI' or (u['source'] == 'WBADB' and u['in_asi_sheet'] == 'no'
                                     and not u.get('wbadb_excavation_also_surveyed')))
    views = ('all_lineages', 'primary', 'lineage_HK')

    by_unit = {}
    for s in srows:
        by_unit[(s['unit_id'], s['branch'])] = s
    sumcols = ['branch', 'headline', 'region', 'date_set', 'view', 'N', 'k_match', 'f_fail', 'm_unknown',
               'k_sens', 'f_sens', 'm_sens', 'clause_counts', 'matches']
    sum_rows = []
    regions = ['A', 'A3', 'B', 'B1', 'B2', 'B2_5', 'AB']
    for b, spec in branches.items():
        for reg in regions:
            for ds in plan['date_sets']:
                for view in views:
                    if not spec['clauses']:
                        sum_rows.append(dict(branch=b, headline='', region=reg, date_set=ds, view=view, N='',
                                             k_match='', f_fail='', m_unknown='', k_sens='', f_sens='', m_sens='',
                                             clause_counts=spec.get('note', ''), matches=''))
                        continue
                    us = [u for u in located if in_region(u, reg) and in_dateset(u, ds) and in_view(u, view)]
                    res = [by_unit[(u['unit_id'], b)] for u in us]
                    cc = []
                    for i, c in enumerate(spec['clauses']):
                        vs = [r['values'].split(';')[i] for r in res]
                        cc.append(f"{c}:{vs.count('yes')}/{vs.count('no')}/{vs.count('unknown')}")
                    hl = spec['headline'] == reg
                    sum_rows.append(dict(
                        branch=b, headline='yes' if hl else '', region=reg, date_set=ds, view=view, N=len(res),
                        k_match=sum(r['result'] == 'match' for r in res), f_fail=sum(r['result'] == 'fail' for r in res),
                        m_unknown=sum(r['result'] == 'unknown' for r in res),
                        k_sens=sum(r['result_sensitivity'] == 'match' for r in res),
                        f_sens=sum(r['result_sensitivity'] == 'fail' for r in res),
                        m_sens=sum(r['result_sensitivity'] == 'unknown' for r in res),
                        clause_counts=' '.join(cc),
                        matches=';'.join(r['record_id'] for r in res if r['result'] == 'match')))
    with open(os.path.join(out_dir, 'scores_summary.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=sumcols, lineterminator='\n')
        w.writeheader()
        w.writerows(sum_rows)

    fcols = ['region', 'date_set', 'view', 'N', 'monument_F1', 'columned_porch_F2', 'exedra_pillar_F2x',
             'inside_pillar_F3', 'inscription_F4', 'named_inscription_F5', 'garden_ancient_F6', 'garden_mention',
             'west_facing_F7w_yes', 'west_facing_F7w_no', 'road_zone_B2_3km', 'road_zone_B2_5km',
             'dated_in_window_strict', 'dated_lenient', 'multi_tomb_records']
    frows = []
    for reg in regions:
        for ds in plan['date_sets']:
            for view in views:
                us = [u for u in located if in_region(u, reg) and in_dateset(u, ds) and in_view(u, view)]
                frows.append(dict(
                    region=reg, date_set=ds, view=view, N=len(us),
                    monument_F1=sum(u['F1'] == 'yes' for u in us), columned_porch_F2=sum(u['F2'] == 'yes' for u in us),
                    exedra_pillar_F2x=sum(u['F2x'] == 'yes' for u in us), inside_pillar_F3=sum(u['F3'] == 'yes' for u in us),
                    inscription_F4=sum(u['F4'] == 'yes' for u in us), named_inscription_F5=sum(u['F5'] == 'yes' for u in us),
                    garden_ancient_F6=sum(u['F6'] == 'yes' for u in us),
                    garden_mention=sum(u['garden_mention'] == 'yes' for u in us),
                    west_facing_F7w_yes=sum(u['F7w'] == 'yes' for u in us), west_facing_F7w_no=sum(u['F7w'] == 'no' for u in us),
                    road_zone_B2_3km=sum(bool(u['in_B2']) for u in us), road_zone_B2_5km=sum(bool(u['in_B2_5']) for u in us),
                    dated_in_window_strict=sum(u['dated_in_window'] == 'yes' for u in us),
                    dated_lenient=sum(u['dated_lenient'] == 'yes' for u in us),
                    multi_tomb_records=sum(u['multi_tomb_record'] == 'yes' for u in us)))
    with open(os.path.join(out_dir, 'features_summary.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fcols, lineterminator='\n')
        w.writeheader()
        w.writerows(frows)

    ppath = os.path.join(out_dir, 'manual_check_pending.csv')
    if pending:
        with open(ppath, 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, lineterminator='\n')
            w.writerow(['record_id', 'code'])
            w.writerows(sorted(pending))
    elif os.path.exists(ppath):
        os.remove(ppath)
    print(f'units eligible: {len(elig)}; located: {len(located)}; score rows: {len(srows)}; '
          f'manual checks pending: {len(pending)}')


if __name__ == '__main__':
    out = sys.argv[3] if len(sys.argv) > 3 else T.FOLDER
    main(sys.argv[1], sys.argv[2], out)
