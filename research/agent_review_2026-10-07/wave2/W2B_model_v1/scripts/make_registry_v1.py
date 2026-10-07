#!/usr/bin/env python3
"""Write registry_v1_entry60.csv: re-ranked entry-60 targets (wave-1 registry files are read, never modified).
  python3 -I make_registry_v1.py <cs_root> <W2B dir>"""
import csv, json, os, sys

cs, wd = sys.argv[1], sys.argv[2]
reg = {r['id']: r for r in csv.DictReader(open(os.path.join(cs, 'results', 'T03_T04_registry', 'registry.csv'), encoding='utf-8'))}
places = {p['place_id']: p for p in csv.DictReader(open(os.path.join(wd, 'inputs', 'places_v1.csv'), encoding='utf-8'))}
R = json.load(open(os.path.join(wd, 'outputs', 'table_order_BF_ranges.json')))
SH = dict(tell_es_sultan='Tell', ein_samiya='Samiya', muhalhil='Muhal', beit_kahil='BKahil', kuhlah='Kuhlah', carmel_siah='Carmel',
          mount_zion='Zion', transjordan='TransJ', ein_ghuweir='Ghuweir', ein_feshkha='Feshkha', kh_yanun='Yanun')


def bf(key, pid):
    if pid not in SH or SH[pid] not in R[key]:
        return 'n/a'
    lo, hi = R[key][SH[pid]]
    return f'{lo:+.2f}..{hi:+.2f}'


def coord(pid):
    if not pid:
        return '', '', '', ''
    p = places[pid]
    if p['lat']:
        return p['lat'], p['lon'], p['precision_string'], p['coord_note']
    return '', '', p['precision_string'], p['coord_note']


T = [
    # new_rank, old_rank, id, target, proposal, branches, place_id, P_heuristic, change, reasons, next test
    (1, 1, 'P60-T1', reg['P60-T1']['site_name'] + ': cemetery zone N/NW of the tell', 'Puech (hypothesis)',
     'RB-M, RB-P, RB-B', 'tell_es_sultan', '0.13-0.24',
     'unchanged (wave-1 demotion withdrawn)',
     'INFERENCE (medium): the wave-1 order-based demotion (entry 60 P 0.30->0.10, "pulled north") does not survive a '
     'density-neutral itinerary kernel: on the T06 inputs themselves P(entry 60 = Tell es-Sultan) stays 0.28 (fixed kernel; '
     'fixed+grid 0.28) and P(N of 32.05 N) falls from 0.71 to 0.10-0.39 (prior-level). Entry-60-only order Bayes factor vs '
     'ʿEin Samiya is within a factor 1.5 in all density-neutral models. EVIDENCE: only candidate where tell + spring with pool '
     'east + cemetery N with Qumran-type graves co-occur (registry). Weaknesses unchanged: Puech partly relies on name '
     'continuity (Zissu p. 149) i.e. order-derived; the name Jericho persisted; b. Qid 66a puts Kohalit "in the desert". '
     'Field reality: the sector N of the tell is built over (T09).',
     'Desk: Kenyon tomb registers (Jericho I-II; Excavations III pp. 173-174) for shafts N of the tell with Roman reuse; '
     '1918 Bavarian frames (T09).'),
    (2, 3, 'P60-T3 (re-scoped)', "ʿEin Samiya valley (Zissu): pit/shaft N of the Kh. el-Marjama tell / Kh. Samiya with tombs at "
     "its mouth (Dhahr Mirzbaneh - Kh. el-ʿAqibat shaft-tomb fields; Kh. Samiya kokhim tombs)", 'Zissu 2001',
     'RB-M, RB-P, RB-B (NOT RB-L: under RB-L the pit is at Janoah, see P60-T8)', 'ein_samiya', '0.13-0.17',
     'up 1; target re-scoped; text-dependency penalty removed',
     'EVIDENCE (Zissu 2001 pp. 146-155): name kept in Wadi Kuheila; Kh. el-Marjama is a >30-dunam tell settled into the '
     'Hellenistic-Roman periods; spring (~300 m3/h) with canals, pools and a rock-cut pool by the tell; Kh. Samiya has an Early '
     'Roman kokhim tomb with ossuary fragments (Baramki 1942, IAA file ATQ/1895) and 16 Roman-Byzantine tombs (Yeivin); desert '
     'setting matches b. Qid 66a; Zissu states the identification is NOT drawn from the list order (p. 146). INFERENCE: the '
     'registry gave a -2 penalty because the target "depends on Lefkovits\'s Janoah"; but Zissu uses Janoah only as one of '
     'several hints, and under the Janoah reading the entry-60 pit is AT Janoah (Lefkovits p. 425), so the old P60-T3 was '
     'internally inconsistent. Order: no robust effect (entry 60 only: -0.03..+0.18 log10 vs Tell, density-neutral). Caveat: '
     'name likeness alone is weak given T01\'s chance-level result; "north" relative to which feature is undefined.',
     'Desk: Mandate 1:20,000 sheet 15-18 El Mughaiyir (1941, Zissu fig. 3) to fix Wadi Kuheila vs the tell; Lapp 1966, Dever '
     '1972 (shaft tombs), Yeivin HA 36-37, Baramki 1942 file; check which tomb fields lie N (315-045 deg) of Kh. el-Marjama.'),
    (3, None, 'P60-T8 (new)', 'Kh. Yanun / Yanun (Janoah of Ephraim): pits, caves or shaft tombs at the site ("the pit which is in '
     'Janoah", Lefkovits)', 'Lefkovits 2000 (reading); Beyer; Janoah = Kh. Yanun (Finkelstein et al. 1997 via Zissu)',
     'RB-L only', 'kh_yanun', '~0.12 (0.15 x 0.8)',
     'new',
     'EVIDENCE: Lefkovits 2000 p. 425 translates XII 10 "In the deep pit which is in Janoah, in the north of Kahelet"; Beyer '
     'reads Janoah "10 km southeast of Garizim" (via Lefkovits p. 426); Zissu p. 149 places Janoah at Kh. Yanun (OIG '
     '18425/17385) or Yanun village (18370/17245), citing Finkelstein et al. 1997. INFERENCE: under RB-L the target is fixed by '
     'Janoah whatever Kohlit is, so it does not inherit the Kohlit uncertainty; it is also the one place where the order\'s weak '
     'end-of-list preference and a published reading coincide (entry-60-only BF vs Tell: -0.01..+0.54 density-neutral, '
     '+0.43..+0.82 T06 kernel). Against: Puech rejects Janoah on the engraving; the wave-1 plate check found no yod and no '
     'sade (P(RB-L) taken as ~0.15, INFERENCE low).',
     'Desk: Finkelstein, Lederman & Bunimovitz 1997 (Southern Samaria Survey) pp. 822-829 site entries for Yanun and Kh. Yanun '
     '(caves, cisterns, tombs, Early Roman sherds); then an epigraphic re-check of XII 10 on the Puech 2006 plates.'),
    (4, 2, 'P60-T2', "ʿEin el-Ghuweir - ʿEin et-Turabeh stretch (Tübingen Atlas B V 18): cemetery N of the ʿEin el-Ghuweir building",
     'TAVO B V 18 (via Puech 2015)', 'RB-M, RB-P, RB-B', 'ein_ghuweir', '0.03-0.05',
     'down 2',
     'INFERENCE: proposal basis is cartographic only (rationale unread), no tell (Puech); order gives nothing (tied BF vs Tell '
     '-0.18..+0.06 when block A is not treated as an itinerary). Keeps a testable feature: 17 excavated N-S graves of the 1st c. '
     'BCE-1st c. CE 800 m N of the building (Hachlili 2000). Coordinate now fixed from Dahari, ʿAtiqot 41 p. 246 (cave XIV/51 '
     'above the site, OIG 18920/11505).',
     'Desk: Bar-Adon\'s ʿEin el-Ghuweir report for shafts/pits among or by the graves.'),
    (5, None, 'P60-T7', "ʿAyn Feshkha area", 'proposer unidentified (Puech 2015 p. 14 rejects)', 'RB-M, RB-P, RB-B', 'ein_feshkha',
     '0.03-0.11', 'ranked (was unranked)',
     'INFERENCE: the order mildly favours the Qumran side for entry 19 (+0.45..+0.66 vs Tell) but only when entry 20 keeps '
     'Secacah = Qumran, which the atlas flags as order-derived (with those removed: ~0). No tell (Puech).',
     'None before T1-T3.'),
    (6, 4, 'P60-T4', 'Qumran-Buqeia district (repo sequence study; not a published proposal)', 'repo', 'all', '', 'n/a',
     'down 2', 'INFERENCE: regional placeholder; no anchor; the only order support is the circular Secacah link above.',
     'None.'),
    (7, None, 'P60-T9 (new)', 'Tell Muhalhil by Nebi Musa (Lurie)', 'Lurie 1963', 'RB-M, RB-P, RB-B', 'muhalhil', '0.03-0.11',
     'new', 'EVIDENCE: Bar-Adon\'s 1968 survey found only a 3.5 x 2.5 m structure (Bar-Adon 1972 site 83, via Zissu p. 148); '
     '"the only connection ... is the phonetic similarity" (Zissu). Coordinate is a PROXY (Nebi Musa). Order: slight positive '
     '(-0.08..+0.29 tied, w_A=0) because it lies between Jericho and Qumran - district-level only.',
     'Desk: locate Bar-Adon 1972 site 83 (map ref.) before any scoring.'),
    (8, None, 'P60-T6', "Carmel: Wadi ʿEin es-Siah / Fons Eliae (Milik's ʿEn Kohel), cave N of the valley", 'Milik 1959; DJD III p. 275',
     'RB-M, RB-P, RB-B', 'carmel_siah', '~0.03', 'ranked (was unranked); now locatable',
     'EVIDENCE: Milik DJD III p. 275 names Wadi ʿEin es-Siah and its spring (Fons Eliae) and a cave near el-Faraj on the N slope '
     '(SWP I p. 302); based on the Beirut plaque / Massekhet Kelim legend (medieval), criticised by Dupont-Sommer and Bardtke '
     '(via Zissu p. 148), doubtful for Puech. INFERENCE: in the T06 kernel Carmel becomes a spurious "sink" (group P up to '
     '0.40) - an artifact; density-neutral models penalise it only if block A is an itinerary (tied -1.1..0). Janoah coupling '
     'under RB-L: -2.3..-2.8.',
     'Desk only if T1-T3 fail: SWP I p. 302 cave description.'),
    (9, None, 'P60-T5', 'East of the Jordan (Goranson)', 'Goranson 1992/2002', 'all', 'transjordan', '~0.04', 'ranked last of the targets',
     'INFERENCE: no site proposed; broad-area proxy only; order neutral to mildly negative.', 'Read Goranson CSS pp. 226-232 for a '
     'named area.'),
    ('-', None, 'no target', 'Beit Kahil; Kh. Kuhlah NE of Beersheba', 'listed by Milik and Lurie', 'all', 'beit_kahil', '<0.03',
     'not a target', 'EVIDENCE: Milik himself called these attempts "peu satisfaisants" (DJD III p. 274 n. 71) before choosing '
     'Carmel. Kh. Kuhlah coordinate is a PROXY (Kukhleh). Order: negative only if block A is an itinerary.', 'None.'),
    ('-', None, 'no target', 'Mount Zion (Pixner)', 'Pixner 1983', 'n/a', 'mount_zion', 'n/a', 'not a target for entry 60',
     'EVIDENCE: Pixner reads XII 10 "in the underground passage that is in Sehab north of Kohlit" and puts Sehab at Tell Shihab '
     'near the Yarmuk (via Lefkovits p. 426), so his entry 60 is not on Mount Zion. INFERENCE: Mount Zion is favoured by the '
     'order only through block A\'s Jerusalem neighbours with w_A > 0 (up to +4.8 log10) - circular, since Pixner built his '
     'grouping of items 1-17 from the list itself.', 'None.'),
]

rows = []
for (nr, orank, tid, target, prop, br, pid, ph, change, reasons, nxt) in T:
    lat, lon, prec, src = coord(pid)
    rows.append(dict(new_rank=nr, old_rank=(orank if orank else ('unranked' if tid.startswith('P60-T') and '(new)' not in tid
                                                                  else '-')),
                     target_id=tid, target=target, kohlit_proposal=prop, reading_branches=br, place_id=pid, lat=lat, lon=lon,
                     coord_precision=prec, coord_source=src, P_target_heuristic=ph,
                     orderBF_entry60_only_densityneutral=bf('e60_mp_densityneutral', pid),
                     orderBF_entry60_only_T06kernel=bf('e60_mp_sinkhorn', pid),
                     orderBF_tied_wA0_densityneutral=bf('tied_mp_densityneutral_wA0', pid),
                     change=change, reasons=reasons, next_desk_test=nxt))
with open(os.path.join(wd, 'registry_v1_entry60.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print('wrote', len(rows), 'rows')
