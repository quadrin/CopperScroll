# Run 23: write out/evidence.csv and out/results.csv from the facts gathered on 30 Oct 2026.
# Usage: python3 -I build_outputs.py <out_dir>
# Tiers follow RULE.md (1 dated section same channel <=2 km; 2 dated section same catchment; 3 regional, INFERENCE; 4 form only).
# "n/a-LL" marks a lake-level parameter (RULE "Fixed parameters"), which is not a tiered aggradation fact.
import sys, csv, os
out = sys.argv[1]
SC, LC = 0.445, 0.525

E = [
 # point, fact, value, unit, source, page/fig, tier, kind
 ('ALL', 'Dead Sea level, Early Roman period (fluctuating range)', '-395 to -400', 'm asl', 'Hirschfeld 2004, IEJ 54: 37-74 (citing Frumkin 1997: 243-244)', 'p. 39', 'n/a-LL', 'EVIDENCE'),
 ('ALL', 'Approximate maximum Dead Sea level, 2100-1700 14C BP (table prints calibrated range as 100 BCE-300 BCE; probably a misprint for 300 CE)', '-390', 'm asl', 'Frumkin, Kadan, Enzel and Eyal 2001, Radiocarbon 43(3): 1179-1189', 'Table 1, p. 1187', 'n/a-LL', 'EVIDENCE'),
 ('ALL', 'Higher lake event dated 1990-1690 BP (Mt Sedom); matching lacustrine silt at Nahal Darga 2115-1750 BP', 'qualitative', '', 'Frumkin et al. 2001', 'p. 1184', 'n/a-LL', 'EVIDENCE'),
 ('ALL', 'Late Holocene lake-level range; highstand in the 2nd-1st c. BCE, 4th c. CE, 11th-12th c. CE and late 19th c.; sill at -402 m', '-390 to -415', 'm asl', 'Bookman, Enzel, Agnon and Stein 2004, GSA Bulletin 116: 555-571', 'abstract only (full text not accessed)', 'n/a-LL', 'EVIDENCE'),
 ('ALL', 'Highstands in the 2nd and 1st c. BC and the 4th c. AD; Roman and Byzantine periods relatively humid', 'qualitative', '', 'Neumann, Kagan, Leroy and Baruch 2010, J. Arid Environments 74: 756-764', 'pp. 760, 762; Fig. 2', 'n/a-LL', 'EVIDENCE'),
 ('ALL', 'Dead Sea level as of 2022', '-437', 'm asl', 'Frumkin 2023, in Sion et al. (eds), New Studies in the Archaeology of the Judean Desert (IAA)', 'p. 77', 'n/a-LL', 'EVIDENCE'),
 ('ALL', 'Dead Sea level 1896 and 2004', '-388.4 ; -417.2', 'm asl', 'Bowman, Shachnovich-Firtel and Devora 2007, Geomorphology 92: 60-75', 'abstract', 'n/a-LL', 'EVIDENCE'),
 ('ALL', 'Net base-level fall since the 1st c. CE (1st-c. range -390 to -400 minus -437)', '37 to 47', 'm', 'derived from Hirschfeld 2004 p. 39, Frumkin et al. 2001 Table 1, Frumkin 2023 p. 77', '', 'n/a-LL', 'INFERENCE'),
 ('ALL', 'The 1896 level (-388.4) stood above the 1st-c. range, so almost all of the net fall dates after c. 1930', 'qualitative', '', 'Bowman et al. 2007 abstract with Hirschfeld 2004 p. 39', '', 'n/a-LL', 'INFERENCE'),
 ('ALL', 'Entrenchment caused by the falling lake fades within about 1000 m or less of the receding shoreline (creeks on the W shore, soft sediment)', '<=1', 'km', 'Bowman et al. 2007', 'abstract', '3', 'EVIDENCE'),
 ('ALL', 'Max at-station incision much smaller than the 20th-c. lake fall (~30 m); depends on drainage area and lake bathymetry (seven W-shore channels)', 'qualitative', '', 'Ben Moshe, Haviv, Enzel, Zilberman and Matmon 2008, Geomorphology 93: 524-536', 'abstract', '3', 'EVIDENCE'),
 ('ALL', 'Max incision near outlets of Nahal Darga and Nahal Arugot', '~30', 'm', 'Ben Moshe and Lensky 2024, Remote Sensing 16: 1346', 'Sect. 1.3', '3', 'EVIDENCE'),
 ('ALL', 'Mean thalweg lowering 2019-2023, Darga / Arugot', '2.34 / 3.17', 'm', 'Ben Moshe and Lensky 2024', 'Figs 12, 13', '3', 'EVIDENCE'),
 ('ALL', 'Vertical incision rate on a small steep fan delta (Nahal Qedem)', 'up to 0.8', 'm/yr', 'Storz-Peretz, Bowman, Laronne and Svoray 2011, ESPL 36: 467-480', 'abstract', '3', 'EVIDENCE'),
 ('P1', 'Lisan-terrace caves near Qumran not yet stable owing to stream entrenchment, slope retreat and collapse', 'qualitative', '', 'Frumkin 2023', 'p. 82', '4', 'EVIDENCE'),
 ('P1', 'Some piping channels near Qumran formed over the last two millennia; cave at A3-013 younger than c. 2000 years', 'qualitative', '', 'Frumkin 2023', 'p. 83', '4', 'EVIDENCE'),
 ('P1', 'Lisan terrace at Qumran up to 50 m high above the Dead Sea plain', '50', 'm', 'Frumkin 2023', 'p. 78', '4', 'EVIDENCE'),
 ('P1', 'Dam basin above the waterfall scoured to bedrock by a flood in June 2007; partly filled by debris in May 2005; no trace of the 1st-c. dam survives the floods', 'qualitative', '', 'Stacey, "Three Notes on Qumran" (bibleinterp.arizona.edu)', 'section "The Dam" and n. 1', '4', 'EVIDENCE'),
 ('P1', 'Aqueduct channel lies c. 4-5 m above the basin bedrock (used by the author to size the dam, not as a bed-change datum)', '4-5', 'm', 'Stacey (bibleinterp)', 'section "The Dam"', '4', 'EVIDENCE'),
 ('P1', 'DEM: bed at -363 m just below a 100 m waterfall step; side relief 25-32 m within 100 m; 1.58 km above the -395 m contour, 3.99 km above the -412 m DEM shore', '25-32', 'm', 'Terrarium z13 DEM (this run, out/form_dem.csv)', 'out/form_dem.csv', '4', 'EVIDENCE'),
 ('P1', 'Modern base-level fall probably has not reached P1 (more than 1 km from the receding shore)', 'qualitative', '', 'Bowman et al. 2007 applied to DEM distance', '', '3', 'INFERENCE'),
 ('P2', 'Bounded alluvial lands in wadis of the Buqeia plateau (Iron Age runoff fields or pasture)', 'qualitative', '', 'Gibson, Lewis and Taylor 2023, Springer, doi 10.1007/978-3-031-27330-8_36', 'abstract only', '2', 'EVIDENCE'),
 ('P2', 'Soil aggradation in terraced runoff wadi fields, Horvat Haluqim (Nahal Zin basin, drains to the Dead Sea): upper 50 cm in ~1300 yr', '~0.4', 'mm/yr', 'Bruins, Jongmans and van der Plicht 2020, Quaternary International 545: 87-101', 'abstract', '3', 'EVIDENCE'),
 ('P2', 'Applied to a plateau wadi bed over 1891-2056 yr: 0 to +0.8 m (lower bound 0 because an untrapped bed need not aggrade; extrapolation beyond 1300 yr is not sourced)', '0 to +0.8', 'm', 'Bruins et al. 2020 applied', '', '3', 'INFERENCE'),
 ('P2', 'DEM: plateau bed at -6 m; side relief 1-4 m within 100 m (unincised)', '1-4', 'm', 'Terrarium z13 DEM (this run)', 'out/form_dem.csv', '4', 'EVIDENCE'),
 ('P3', 'Jericho plain near the escarpment: alluvial and sabkha sediments younger than ~3000 yr, subaerial', 'qualitative', '', 'Lazar, Ben-Avraham, Garfunkel, Porat and Marco 2010, J. Geology 118: 261-276', 'p. 268', '3', 'EVIDENCE'),
 ('P3', 'OSL: BAF-6 430+-40 yr at 0.4 m; BAF-4 1130+-70 at 0.9 m; BAF-2 1640+-180 at 1.25 m; BAF-5 2600+-190 at 1.4 m; BAF-1 2900+-460 at 1.5 m', 'see fact', 'm / yr', 'Lazar et al. 2010', 'Table 2, p. 271', '3', 'EVIDENCE'),
 ('P3', 'A 1st-c. CE horizon on that plain lies at ~1.25-1.45 m (interpolated between BAF-2 and BAF-5/BAF-1; samples from two trenches)', '+1.25 to +1.45', 'm', 'Lazar et al. 2010 Table 2 interpolated', '', '3', 'INFERENCE'),
 ('P3', 'DEM: Nuweimeh bed at -206 m entrenched 7-25 m within 100 m (23-54 m within 250 m); 21 km above the -395 m contour', '7-25', 'm', 'Terrarium z13 DEM (this run)', 'out/form_dem.csv', '4', 'EVIDENCE'),
 ('P4a', 'Kidron floods 3-12 times a year, lasting 2-24 hours', '3-12', 'floods/yr', 'Ilan and Amit 2002 (Aqueducts of Israel) via project note research/sources/nli_photos_2026-10-21/aqueducts_ilan_hyrcania_qumran.md', 'pp. 333-334', '4', 'EVIDENCE'),
 ('P4a', 'No diversion dam, regulator or bridge found at the start of the Herodian southern aqueduct on the Qidron (no bed-level datum published in the project records)', 'qualitative', '', 'Patrich 1989 p. 244; Patrich 2002 p. 338 (via ratings.csv)', 'p. 244; p. 338', '4', 'EVIDENCE'),
 ('P4a', 'DEM: gorge bed at +183 m; side relief 51-54 m within 100 m (bedrock gorge)', '51-54', 'm', 'Terrarium z13 DEM (this run)', 'out/form_dem.csv', '4', 'EVIDENCE'),
 ('P4b', 'DEM: Kidron bed drops from -128 to -364 m between 13.1 and 13.7 km below Mar Saba (fault scarp); exit cell 1.71 km above the -395 m contour and 2.17 km above the -412 m DEM shore', '1.71 ; 2.17', 'km', 'Terrarium z13 DEM (this run, scripts/detail.py)', '', '4', 'EVIDENCE'),
 ('P4b', 'Modern entrenchment probably has not reached the exit (>1 km from the receding shore), but the Kidron is a large catchment and incision scales with drainage area', 'qualitative', '', 'Bowman et al. 2007; Ben Moshe et al. 2008', '', '3', 'INFERENCE'),
 ('C1', 'Kh. Mazin (Mezad Qidron) on the NW shore: Hasmonean anchorage with slipway, breakwater (later phase); Hellenistic and Early Roman pottery', 'qualitative', '', 'Traubman 2024, HA-ESI 136 (Khirbat Mazin)', 'text', '2', 'EVIDENCE'),
 ('C1', 'Slipway area filled with sand, soil and stones collapsed from the walls; north of the slipway a stone surface overlain by a soil accumulation', 'qualitative', '', 'Traubman 2024', 'text', '2', 'EVIDENCE'),
 ('C1', 'Section 2-2: base of slipway courses at c. -394 m, layered fill rising to c. -391 m; section 1-1: floor c. -394 m, surface c. -392 to -393 m', '1 to 3 (read from drawing, +-0.5)', 'm', 'Traubman 2024', 'Fig. 2 (plan and sections)', '2', 'EVIDENCE'),
 ('C1', 'Earlier excavation: a feature above the original floor level and below later gravels', 'qualitative', '', 'Stutchbury and Nicholl 1962, ADAJ 6/7: 96-103 (via project coding research/regional/haesi_features/phase4_2026-10-11/part_i_adaj/data/coding.json; not re-read: portal certificate expired)', 'pp. 96-103', '2', 'EVIDENCE'),
 ('C1', 'Burial at Mazin is mixed: the 1896 lake (-388.4) and the 4th-c. and 11th-12th-c. highstands stood above the -394 m slipway, and part of the fill is wall collapse; it is not a clean fan-aggradation measure', 'qualitative', '', 'Bowman et al. 2007; Bookman et al. 2004; Traubman 2024', '', '2', 'INFERENCE'),
 ('C2', 'Tulul Abu el-Alayiq Pools Complex: as a result of erosion the original Hasmonean plaza floor is gone; pre-excavation surface 0.65-1.2 m below the assumed floor', '-0.65 to -1.2', 'm', 'Netzer 2001, Hasmonean and Herodian Palaces at Jericho I', 'p. 86', '2', 'EVIDENCE'),
 ('C2', 'Facing stones of the Hasmonean pools missing through erosion; garden flowerpots lost to erosion', 'qualitative', '', 'Netzer 2001', 'pp. 75, 85', '2', 'EVIDENCE'),
 ('C2', "Herod's Third Palace built on both sides of Wadi Qelt with its seasonal flow; a bridge apparently linked the two sides", 'qualitative', '', 'Netzer 2001', 'p. 9', '2', 'EVIDENCE'),
 ('C-fallback', 'Ein Feshkha square enclosure: walls covered by soil eroded from the slopes (no thickness given); foot of Ras Feshkha surveyed at -393 m (2002)', 'qualitative ; -393', 'm asl', 'Hirschfeld 2004', 'pp. 39, 66', '2', 'EVIDENCE'),
 ('P5', 'Same catchment, c. 3 km downstream on the Qelt fan: net surface lowering, not burial, at the Hasmonean palace site (C2)', '-0.65 to -1.2 (site surface, not bed)', 'm', 'Netzer 2001', 'p. 86', '2', 'EVIDENCE'),
 ('P5', 'DEM: gorge bed at -139 m; side relief 31-45 m within 100 m (bedrock gorge)', '31-45', 'm', 'Terrarium z13 DEM (this run)', 'out/form_dem.csv', '4', 'EVIDENCE'),
 ('P6', 'No fluvial or dated section found for Wadi Kuteif (searched: web, Drive, repo)', 'unknown', '', 'search log in RESULT_DRAFT.md', '', '', 'EVIDENCE'),
 ('P6', 'DEM: bed at -72 m; side relief 17 m within 100 m, 33-50 m within 250 m (incised valley)', '17', 'm', 'Terrarium z13 DEM (this run)', 'out/form_dem.csv', '4', 'EVIDENCE'),
 ('P7', 'Lower Jordan: Dead Sea fell ~22 m in 70 yr; incision reached ~8 km upstream by 1983 and ~11 km by 1993 (datum not stated in abstract); sinuosity +25% after 1980; channel width narrowed ~4x in 30 yr', 'see fact', 'km', 'Hassan and Klein 2002, Geomorphology 45: 21-33', 'abstract', '3', 'EVIDENCE'),
 ('P7', 'Lower Jordan course shortened between the 1920s and early 1970s and lengthened again afterwards (air photos)', 'qualitative', '', 'Klein 1985, ESPL 10: 525-531', 'abstract', '3', 'EVIDENCE'),
 ('P7', 'Lateral migration of the lower Jordan 1984-2016: ~17.9 m total (abstract rate 0.325 m/yr does not reconcile)', '~17.9', 'm', 'Al-Husban 2018, EREM 74(2): 34-51', 'abstract', '3', 'EVIDENCE'),
 ('P7', 'Near the mouth the incising Jordan forms a deep confined channel; upstream, near the knickzone, overbank floods and chute cutoffs', 'qualitative', '', 'Dente, Lensky, Morin, Dunne and Enzel 2019, ESPL 44: 781-795', 'abstract', '3', 'EVIDENCE'),
 ('P7', 'Byzantine church at the baptism site (E bank, opposite) built on piers against Jordan floods; chapel on piers above the river', 'qualitative', '', 'UNESCO nomination, Baptism Site (whc.unesco.org/document/169171)', 'p. 3', '4', 'EVIDENCE'),
 ('P7', 'DEM: Jordan thalweg at -387 m, 10.25 km above the -412 m DEM shore', '10.25', 'km', 'Terrarium z13 DEM (this run)', 'out/form_dem.csv', '4', 'EVIDENCE'),
 ('P8', 'No fluvial or dated section found for Wadi el-Asla / Nahal Og (searched: web, Drive, repo)', 'unknown', '', 'search log in RESULT_DRAFT.md', '', '', 'EVIDENCE'),
 ('P8', 'DEM: Mukellik/Og bed at -296 m below the scarp; side relief 15-48 m within 100 m; 6.4 km above the -395 m contour', '15-48', 'm', 'Terrarium z13 DEM (this run)', 'out/form_dem.csv', '4', 'EVIDENCE'),
]

with open(os.path.join(out, 'evidence.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['point', 'fact', 'value', 'unit', 'source', 'page_fig', 'tier', 'kind'])
    for r in E: w.writerow(r)

def dn(depth_c, lo, hi):
    out = []
    for c in (SC, LC):
        d = depth_c * c
        a = 'unknown' if lo is None else f'{d+lo:.2f}'
        b = 'unknown' if hi is None else f'{d+hi:.2f}'
        out.append(f'{a} to {b}')
    return out

R = []
def add(pid, entry, depth_c, regime, lo, hi, tier, verdict_s, verdict_l, survival, narrow, note):
    if depth_c is None:
        ds = dl = 'unknown (no stated depth; D_now = net change, unknown)'
    else:
        ds, dl = dn(depth_c, lo, hi)
    rng = f"{'unknown' if lo is None else f'{lo:+.2f}'} to {'unknown' if hi is None else f'{hi:+.2f}'}"
    R.append([pid, entry, '' if depth_c is None else depth_c, regime, rng, tier, ds, dl, survival, verdict_s, verdict_l, narrow, note, 'uncalibrated'])

add('P1', 20, 1, 'incising / scour (gorge foot below waterfall; Lisan terrace entrenching)', None, 0.0, '4',
    'unknown, lean reachable if present', 'unknown, lean reachable if present', 'unknown, lean removed',
    'A dated section (OSL/14C) or GPR profile of the bed fill below the Qumran waterfall', 'Upper bound 0 rests on form and process statements only (Frumkin 2023 pp. 82-83; DEM; Stacey): tier 4, so no number is allowed by the rule; the 0 is shown only to locate the lean.')
add('P2', 17, 3, 'aggrading or stable (unincised plateau bed)', 0.0, 0.8, '3',
    'unknown, lean reachable', 'unknown, lean reachable', 'unknown',
    "A dated trench in a Buqeia wadi bed behind an Iron Age wall (e.g. Stager's 1975 Buqeia profiles)", 'Tier-3 rate from terraced Negev fields (Bruins et al. 2020); constant rate beyond 1300 yr is unsourced.')
add('P3', 17, 3, 'incised channel on the Jericho plain margin (age of entrenchment unknown)', None, 1.45, '3 (upper) + 4',
    'unknown, lean reachable (upper bound 2.79)', 'unknown, no lean (upper bound 3.03 > 3)', 'unknown',
    'A dated section in the Wadi Nuweimeh bed or its lowest terrace near the point', 'Upper bound from the Jericho-plain OSL profile (Lazar et al. 2010), a surface not a channel; lower bound unknown because the channel is entrenched.')
add('P4a', 35, 3, 'bedrock gorge; cut-and-fill (3-12 floods/yr)', None, None, '4',
    'unknown, lean reachable (if net ~0: 1.34)', 'unknown, lean reachable (if net ~0: 1.58)', 'unknown, lean removed',
    'The level of the Herodian southern-aqueduct start (Patrich 1989 point 1) relative to the present Kidron bed', 'No number at any tier. Lean rests on gorge form only.')
add('P4b', 35, 3, 'fan apex at the canyon exit; two-sided (fan-toe burial at C1 vs possible modern entrenchment)', None, 3.0, '3 (upper: C1 transfer; Mazin sits on the Wadi Mazin delta per ADAJ coding, so not the same channel)',
    'unknown, no lean', 'unknown, no lean', 'unknown',
    'Stutchbury and Nicholl 1962 (ADAJ 6/7) sections with gravel thickness, plus one dated section at the Kidron fan apex', 'If the apex aggraded like the Mazin toe, D_now reaches 4.3-4.6 m (deep); if not, 1.3-1.6 m (reachable).')
add('P5', 32, 3, 'bedrock gorge; same catchment shows erosion, not burial (C2)', None, 0.0, '2 (sign only, site surface) + 4',
    'strict: unknown, lean reachable | lenient (C2 accepted as tier 2): reachable', 'strict: unknown, lean reachable | lenient: reachable', 'unknown, lean removed',
    'The level of a dated Qelt aqueduct intake or culvert near Choziba relative to the present bed', 'Ambiguity scored both ways. Strict: C2 measures a fan-site surface 3 km downstream, not a bed, so it is not a bed section (tier 3 at best) and gives only a lean. Lenient: C2 is a dated section in the same catchment (tier 2) and its net-erosion sign caps net change at 0, so D_now <= 1.34/1.58 m: reachable.')
add('P6', 24, 7, 'incised valley (form only)', None, None, '4',
    'unknown, lean deep (stated depth 3.12 > 3)', 'unknown, lean deep (stated depth 3.68 > 3)', 'unknown',
    'A plan with levels of the stepped chamber in Wadi Kuteif (SWP III p. 220; Milik D12) relative to the bed', 'Deep unless net incision exceeds 0.12 m (short cubit) or 0.68 m (long cubit); no number at any tier.')
add('P7', 28, 9, 'meandering floodplain; incising near the mouth since c. 1980', None, None, '3 + 4',
    'unknown, lean deep if present (stated depth 4.01)', 'unknown, lean deep if present (stated depth 4.73)', 'unknown, lean removed (meander migration over 2000 yr)',
    'A dated historical channel series at the Qasr el-Yahud crossing (SWP 1870s sheet, 1940s air photos, today) to test migration across the point', 'Numeral partly restored: if the true number is lower the depth falls; scored as read (9). No tier-1-2 migration record, so not "likely removed".')
add('P8', 18, None, 'incised fan channel below the scarp (form only)', None, None, '4',
    'unknown, no lean', 'unknown, no lean', 'unknown',
    'A dated section in the Nahal Og (Mukellik) bed at the escarpment exit', 'No stated depth; under Clermont-Ganneau\'s small-wadi branch the point and the answer are both unknown.')

with open(os.path.join(out, 'results.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['point', 'entry', 'stated_cubits', 'regime', 'net_change_m_since_60CE', 'tier', 'D_now_m_cubit_0.445', 'D_now_m_cubit_0.525', 'survival', 'verdict_cubit_0.445', 'verdict_cubit_0.525', 'single_record_that_would_narrow_most', 'note', 'calibration'])
    for r in R: w.writerow(r)
print(len(E), 'evidence rows;', len(R), 'result rows')
