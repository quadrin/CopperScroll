#!/usr/bin/env python3
"""Build v1 inputs from the (copied, unmodified) T06 v0 inputs + the Kohlit candidate places.

  python3 -I build_inputs_v1.py ../inputs
reads  places_v0.csv candidates_v0.csv name_groups_v0.csv entries_v0.csv grid_conversions.csv
writes places_v1.csv candidates_v1.csv name_groups_v1.csv entries_v1.csv kohlit_proposals_v1.csv

Every coordinate below is either (a) a published Old Israel (Palestine) grid reference converted by
grid_convert.py (EPSG:28191 -> WGS84), or (b) a Wikidata P625 value (raw API responses saved under
../downloads/wikidata/), or (c) a stated proxy / broad area built from (a)/(b) with an explicit sigma.
Nothing is typed from memory.
"""
import csv, os, sys

ind = sys.argv[1]
rd = lambda f: list(csv.DictReader(open(os.path.join(ind, f), encoding='utf-8')))
G = {r['id']: r for r in rd('grid_conversions.csv')}

places = rd('places_v0.csv')
for p in places:
    p['components'] = ''
    p['kind'] = 'v0'

NEW = [
    # place_id, name, lat, lon, sigma_km, components, region, precision_string, coord_note, kind
    ('ein_samiya', "ʿEin Samiya valley (Kh. Samiya, Kh. el-Marjama tell, ʿEin Samiya spring)",
     G['ein_samiya_neaehl']['lat'], G['ein_samiya_neaehl']['lon'], 0.7, '', 'SAMDES', '~700 m (valley 1 km x 350 m)',
     "NEAEHL vol. 5 (2008) p. 2118 map-ref table, 'Ein Samiya and Dhahr Mirzbaneh, OIG 181010/155470 -> EPSG:28191->WGS84. "
     "Cross-checks: Kh. Marjameh OIG 181600/155400 (NEAEHL p. 2121) -> %s,%s (0.6 km E); Zissu PEQ 133 (2001) p. 150 "
     "map ref. 181/155 -> %s,%s (0.5 km S); Wikidata Q6708772 village 31.98917,35.33333 (0.7 km SE)" % (
         G['kh_marjameh_neaehl']['lat'], G['kh_marjameh_neaehl']['lon'],
         G['ein_samiya_valley_zissu']['lat'], G['ein_samiya_valley_zissu']['lon']), 'kohlit'),
    ('kh_yanun', 'Kh. Yanun (Janoah of Ephraim; Lefkovits/Beyer reading of XII 10)',
     G['kh_yanun_zissu']['lat'], G['kh_yanun_zissu']['lon'], 0.5, '', 'NORTH', '~500 m (Kh. Yanun / Yanun village 1.5 km apart)',
     "Zissu PEQ 133 (2001) p. 149 citing Finkelstein et al. 1997: 828-29, OIG 18425/17385 -> EPSG:28191->WGS84. "
     "Cross-check: Yanun village OIG 18370/17245 -> %s,%s vs Wikidata Q8048992 32.14544,35.35568 (0.03 km)" % (
         G['yanun_village_zissu']['lat'], G['yanun_village_zissu']['lon']), 'janoah'),
    ('muhalhil', 'Tell Muḥalḥil "adjacent to Nebi Musa" (Lurie) - PROXY at Nebi Musa',
     '31.78648', '35.43180', 2.0, '', 'DESERT', 'area ~2 km (proxy)',
     'PROXY: no published coordinate found for Tell Muhalhil (Bar-Adon 1972 site 83 not available); Nebi Musa Wikidata '
     'Q2909131 P625 31.78648,35.43180; "adjacent to Nebi Musa" Zissu p. 148, "near Nabi Musa" Lefkovits 2000 p. 74', 'kohlit'),
    ('beit_kahil', 'Beit Kahil, WNW of Hebron (Milik/Lurie name resemblance)', '31.56966', '35.06600', 1.0, '', 'HEBNEG',
     '~1 km (village)', 'Wikidata Q2898790 P625; Milik DJD III p. 274 D-71 ("Beit Kahil à l\'ouest-nord-ouest d\'Hébron")', 'kohlit'),
    ('kuhlah', 'Kh. Kuḥlah / Kuḥleh NE of Beersheba (Milik/Lurie) - PROXY at Kukhleh', '31.29310', '35.05530', 3.0, '',
     'HEBNEG', 'area ~3 km (proxy)',
     'PROXY: modern Bedouin village Kukhleh (Wikidata Q7214177 P625, precision 0.01 deg; en.wikipedia Kukhleh 31.287,35.048), '
     'assumed to preserve the name of "H. Kuhlah au nord-est de Bersabée" (Milik DJD III p. 274 D-71); identity INFERENCE', 'kohlit'),
    ('carmel_siah', "Wadi ʿEin es-Siaḥ, W slope of Carmel (Milik's ʿEn Koḥel / Fons Eliae)", '32.80100', '34.97500', 2.0, '',
     'CARMEL', 'area ~2 km', 'Wikidata Q4025762 (Nahal Siach) P625; Milik DJD III p. 275 D-71 (Wadi ʿEin es-Siah, Fons Eliae, '
     'with ʿAin Umm el-Faraj to its east)', 'kohlit'),
    ('mount_zion', 'Mount Zion (Greek Orthodox cemetery area; Pixner)', '31.77167', '35.22861', 0.3, '', 'JER', '~300 m',
     'Wikidata Q332444 P625; Pixner RevQ 11 (1983) via Zissu p. 148 and Lefkovits p. 74', 'kohlit'),
    ('transjordan', 'East of the Jordan (Goranson) - BROAD AREA', '', '', 15.0,
     '31.56694:35.63361:15|32.18556:35.68667:15', 'TRANSJ', 'broad area (two 15-km components)',
     'BROAD AREA, modelling proxy only: two components at the Hasmonaean Peraean fortresses Machaerus (Wikidata Q1549278) and '
     'Amathus (Wikidata Q2841350), sigma 15 km each; Goranson names no site', 'kohlit'),
    ('ein_ghuweir', "ʿEin el-Ghuweir - ʿEin et-Turabeh stretch (Tübingen Atlas B V 18 placement)",
     G['ein_ghuweir_cave_xiv51']['lat'], G['ein_ghuweir_cave_xiv51']['lon'], 1.5, '', 'QUMRAN', 'area ~1.5 km',
     "Dahari, ʿAtiqot 41 (2002) Region XIV p. 246: cave XIV/51 above the ʿEin el-Ghuweir site, OIG 18920/11505 -> WGS84; "
     "Qasr et-Turabeh survey centre OIG 1887/1129 -> %s,%s (2.2 km S); sigma covers the stretch" % (
         G['qasr_turabeh_area']['lat'], G['qasr_turabeh_area']['lon']), 'kohlit'),
    ('ein_feshkha', 'ʿEin Feshkha', '31.71444', '35.45333', 0.5, '', 'QUMRAN', '~500 m',
     'Wikidata Q405816 P625', 'kohlit'),
]
cols = list(places[0].keys())
for (pid, name, lat, lon, sig, comps, reg, prec, note, kind) in NEW:
    places.append(dict(place_id=pid, name=name, lat=lat, lon=lon, sigma_km=sig, mixture_of='', model_region=reg,
                       coords_in_places_json='no', precision_string=prec, coord_note=note, components=comps, kind=kind))

# ---------------------------------------------------------------- Kohlit proposals (one row per proposal)
PROPOSALS = [
    # place_id, proponents, order_derived flag (for Kohlit tests), reading dependence, evidence note
    ('tell_es_sultan', 'Puech 1997/2006/2015 (hypothesis); Hogenhaven 2016 option', 'documented',
     '', 'atlas flags as order-derived; Zissu p. 149: Puech "also relies on the continuity of names in the scroll"'),
    ('ein_samiya', 'Zissu 2001 (PEQ 133; JSRS 10)', 'no', 'janoah-supported',
     'Zissu p. 146: "no continuity or pattern can be found that would aid in identifying the place"; rests on Wadi Kuheila name, '
     'tell (Kh. el-Marjama), spring/pool, Second Temple Jewish settlement (Kh. Samiya kokhim, ossuaries), desert setting, '
     'and Lefkovits\'s Janoah (pp. 146, 149-150)'),
    ('muhalhil', 'Lurie 1963 (via Zissu p. 148; Lefkovits p. 74)', 'no', '', 'phonetic resemblance only (Zissu p. 148)'),
    ('beit_kahil', 'Milik (listed, judged unsatisfactory: DJD III p. 274); Lurie list', 'no', '', 'name resemblance'),
    ('kuhlah', 'Milik (listed, judged unsatisfactory: DJD III p. 274); Lurie list', 'no', '', 'name resemblance'),
    ('carmel_siah', 'Milik 1959; DJD III p. 275', 'no', '',
     'Beirut plaque / Massekhet Kelim legend; Milik p. 274: Kohlit caches "dispersées capricieusement à travers la liste"'),
    ('mount_zion', 'Pixner 1983 (via Zissu p. 148; Lefkovits p. 74)', 'likely', '',
     'Pixner grouped items 1-17 near the Essene Gate (ABD via registry) - partly order-based'),
    ('transjordan', 'Goranson 1992/2002 (via Cook 2005; atlas)', 'no', '', 'b. Qid 66a + Jannaeus campaigns; no site'),
    ('ein_ghuweir', 'Tübingen Bible Atlas B V 18 (via Puech 2015 p. 14)', 'unknown', '', 'rationale unread'),
    ('ein_feshkha', 'proposer not identified (Puech 2015 p. 14 rejects)', 'unknown', '', 'no tell (Puech)'),
]

cands = rd('candidates_v0.csv')
for c in cands:
    c['conditional_on_reading'] = ''
    c['kohlit_proposal'] = 'no'
# the five Kohlit entries: replace the single v0 Tell es-Sultan row by the full proposal set
KOH = ['4', '11', '15', '19', '60']
cands = [c for c in cands if not (c['entry'] in KOH and c['place_id'] == 'tell_es_sultan')]
for e in KOH:
    for (pid, who, od, dep, note) in PROPOSALS:
        cands.append(dict(entry=e, place_id=pid, status='possible', confidence='weak', order_derived=od, prior_override='',
                          source=f'Kohlit proposal: {who}', conditional_on_reading=('xii10!=janoah' if e == '60' else ''),
                          kohlit_proposal='yes'))
# entry 60 under Lefkovits/Beyer "in Janoah": the pit is AT Janoah
cands.append(dict(entry='60', place_id='kh_yanun', status='possible', confidence='medium', order_derived='no', prior_override='',
                  source='Lefkovits 2000 pp. 425-428 (reading); Janoah = Kh. Yanun per Finkelstein et al. 1997 via Zissu p. 149; '
                         'Beyer "10 km southeast of Garizim" (via Lefkovits p. 426)',
                  conditional_on_reading='xii10=janoah', kohlit_proposal='no'))

groups = rd('name_groups_v0.csv')
for g in groups:
    if g['group'] == 'Kohlit' and g['entry'] == '60':
        g['conditional_on_reading'] = 'xii10!=janoah'

out = lambda f, rows: (lambda w: (w.writeheader(), w.writerows(rows)))(
    csv.DictWriter(open(os.path.join(ind, f), 'w', newline='', encoding='utf-8'), fieldnames=list(rows[0].keys())))
out('places_v1.csv', places)
out('candidates_v1.csv', cands)
out('name_groups_v1.csv', groups)
out('entries_v1.csv', rd('entries_v0.csv'))
out('kohlit_proposals_v1.csv', [dict(place_id=a, proponents=b, order_derived=c, reading_dependence=d, note=e)
                                 for a, b, c, d, e in PROPOSALS])
print('places', len(places), 'candidates', len(cands), 'groups', len(groups))
