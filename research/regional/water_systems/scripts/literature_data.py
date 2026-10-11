"""Hand-coded literature rows of the water-systems lane (plan §3 source 4).

Coded 11 October 2026 UTC by the lane worker, after the plan freeze (0b07fad) and amendment 1 (21d197d).
Every row codes what the cited pages say; INFERENCE is marked in `notes`. Attribute values follow plan §5:
yes / no / unknown; `marker_side` N, S, E, W or ''; `near_bend_m` and `fissure_m` give the largest
distance the source allows (None = not bounded). Positions: `pt` = ('asi', 'map/site'), ('wbadb', 'S123'),
('place', place_id), ('oig', easting_m, northing_m, precision_m) or None (unplaced).
No text beyond 12-word quotes is stored.
"""

SOURCES = {
    'GP94': 'Garbrecht & Peleg 1994, Biblical Archaeologist 57.3: 161-170 (repo extraction '
            'registration/garbrecht_peleg1994_extracted.md; PDF checked)',
    'MAZ89': 'A. Mazar, "Survey of the aqueducts to Jerusalem", in Amit, Hirschfeld & Patrich (eds) 1989: 169-195 '
             '(Hebrew; OCR of the owner\'s copy, viewer pp. 182-208)',
    'AMI89': 'D. Amit, "The water system of the fortress of Doq (Dagon)", in Amit et al. 1989: 223-228 (Hebrew; '
             'OCR of repo extract research/assets/plans/aqueducts1989/amit-doq-pp223-228.pdf)',
    'MA89': 'Z. Meshel & D. Amit, "The water supply of the Cypros fortress", in Amit et al. 1989: 229-242 (Hebrew; '
            'OCR of repo extract jericho-cypros-original-pages.pdf pp. 14-27)',
    'PAT89': 'J. Patrich, "The aqueducts of Hyrcania", in Amit et al. 1989: 243-260 (Hebrew; as coded in the repo '
             'inventory registration/christmas_hyrcania_primary_features_2026-09-30.json)',
    'NET89': 'E. Netzer, "The aqueducts and the Hasmonean royal estate in the western Jericho plain", in Amit et '
             'al. 1989: 273-281 (Hebrew; OCR of repo extract jericho-cypros-original-pages.pdf pp. 28-36)',
    'IA89': 'Z. Ilan & D. Amit, "The aqueduct of Qumran", in Amit et al. 1989: 283-288 (Hebrew; OCR of repo '
            'extract qumran-ein-boqeq-chapters.pdf pp. 1-6, and research/sites/ilan_amit_1989_plan_review.md)',
    'DAM89': 'E. Damati, "The irrigated gardens of the Martyrius monastery", in Amit et al. 1989: 299-304 '
             '(Hebrew; OCR of the owner\'s copy, viewer pp. 312-317)',
    'HIR89': 'Y. Hirschfeld, "The water supply system of the Chariton monastery", in Amit et al. 1989: 305-312 '
             '(Hebrew; OCR of the owner\'s copy, viewer pp. 318-325)',
    'NET75': 'E. Netzer, "The Hasmonean and Herodian winter palaces at Jericho", IEJ 25 (1975): 89-100',
    'NET01B': 'E. Netzer 2001, The Palaces of the Hasmoneans and Herod the Great (Jerusalem) (printed pages)',
    'GAL': 'K. Galor, "Qumran\'s plastered pools: a new perspective" (chapter XIII; author copy, printed pp. 257-283)',
    'MP18': 'Y. Magen & Y. Peleg 2018, Back to Qumran: final report, site description pp. 75-80 (repo extraction '
            'registration/magen2018_extracted.md)',
    'TSA75': 'Y. Tsafrir, "The desert forts of Judea in Second Temple times", Qadmoniot 8 (1975): 41-53 (Hebrew)',
}

DEFAULT = dict(aggregate='no', count='1', feed='unknown', feed_wadi='unknown', flow_from='unknown', dims='',
               capacity_m3='', shape='unknown', plaster='unknown', entrance='unknown', great='unknown',
               north='unknown', head='unknown', head_marker='', marker_side='', bend='unknown', near_bend_m=None,
               wall_at_outlet='unknown', fissure_east='unknown', fissure_m=None, solomon='unknown', named_wadi='',
               qelt='unknown', kidron_feed='unknown', period_as_given='', date_code='undated', label='EVIDENCE',
               quote='', notes='', group_id='', site_key='', pt=None, dest_pt=None, supersedes='', covered_by='')

ROWS = []


def R(rid, src, loc, name, site, typ, **kw):
    r = dict(DEFAULT)
    r.update(kw)
    r.update(id='LIT-' + rid, src=src, locator=loc, name=name, site_key=site, type=typ)
    ROWS.append(r)


# ----------------------------------------------------------------------------- Garbrecht & Peleg 1994
R('GP-DOQ-AQ', 'GP94', 'pp. 164-165', 'Doq diversion channel from a wadi on the west', 'doq', 'aqueduct',
  pt=('place', 'doq'), head='yes', head_marker='any', marker_side='', flow_from='W', feed='wadi_diversion',
  feed_wadi='yes', dims='0.50-0.70 m wide; first cistern 500 m away', plaster='unknown',
  period_as_given='Hasmonean fort (historical; not rebuilt by Herod)', date_code='in_hedged',
  notes='head: "small diverting weir"; only masonry traces (p. 164); date from fort history', group_id='G-DOQ-AQ')
R('GP-DOQ-CIS', 'GP94', 'p. 165', 'Doq cisterns (nine, plus one higher)', 'doq', 'cistern', aggregate='yes',
  count='10', pt=('place', 'doq'), feed='channel', feed_wadi='yes', plaster='yes', shape='four_sides',
  dims='L 7-11, W 3-5, H 5-7 m; total 2,100 m3', period_as_given='assumed contemporary with the fort',
  date_code='in_hedged', notes='"approximately rectangular in plan"; all lined with plaster', group_id='G-DOQ-CIS')
R('GP-CYP-HAS', 'GP94', 'pp. 165-166', 'Cypros Hasmonean collecting channel', 'cypros', 'aqueduct',
  pt=('asi', '109/5/7'), head='unknown', feed='runoff', feed_wadi='no', period_as_given='Hasmonean phase',
  date_code='in', notes='collects hill runoff (catchment c. 100,000 m2)', group_id='G-CYP-RUNOFF')
R('GP-CYP-CIS', 'GP94', 'p. 166', 'Cypros four cisterns on the eastern slope', 'cypros', 'cistern', aggregate='yes',
  count='4', pt=('asi', '109/5/7'), feed='channel', feed_wadi='no', capacity_m3='>2000',
  period_as_given='Hasmonean phase (after Meshel & Amit 1979)', date_code='in', group_id='G-CYP-CIS')
R('GP-CYP-HER', 'GP94', 'p. 167', 'Aqueduct from Ein el-Fawar to Cypros (Herodian), fed also from Ein Fara',
  'cypros', 'aqueduct', pt=('wbadb', 'S2621'), head='yes', head_marker='', flow_from='W', feed='spring',
  qelt='yes', named_wadi='Kelt', dims='14 km; ten bridges, five tunnels; bridge 135 m',
  period_as_given='Herodian', date_code='in', bend='unknown', group_id='G-CYP-HER',
  notes='head at Ein el Fawar spring (lower spring); continues to Herod\'s winter palace')
R('GP-CYP-FARA', 'GP94', 'p. 167', 'Channel from Ein Fara to Ein el-Fawar (6 km)', 'ein_fara', 'aqueduct',
  pt=('wbadb', 'S2709'), head='yes', flow_from='W', feed='spring', qelt='yes', named_wadi='Kelt',
  period_as_given='Herodian phase', date_code='in', group_id='G-CYP-FARA')
R('GP-HYR-AQ', 'GP94', 'pp. 168-169', 'Hyrcania aqueducts: diversion from two wadis (Kidron)', 'hyrcania', 'aqueduct',
  aggregate='yes', count='2', pt=('asi', '109/7/70'), head='unknown', feed='wadi_diversion', feed_wadi='yes',
  kidron_feed='yes', named_wadi='Kidron (Wadi Nur)', dims='c. 2 km and c. 9 km; saddle substructure 112 m',
  period_as_given='two phases, possibly Hasmonean and Herodian (masonry)', date_code='in_hedged',
  group_id='G-HYR-AQ-AGG', covered_by='G-HYR-NAQ;G-HYR-SAQ')
R('GP-HYR-CIS', 'GP94', 'pp. 168-169', 'Hyrcania cisterns (4 lower, 12 upper)', 'hyrcania', 'cistern',
  aggregate='yes', count='16', pt=('asi', '109/7/70'), feed='channel', feed_wadi='yes', kidron_feed='yes',
  capacity_m3='c. 16000', period_as_given='lower possibly Hasmonean; upper possibly Herodian',
  date_code='in_hedged', group_id='G-HYR-CIS')
R('GP-HYR-POOLS', 'GP94', 'p. 168', 'Hyrcania three rock-cut unroofed pools', 'hyrcania', 'reservoir_pool',
  aggregate='yes', count='3', pt=('asi', '109/7/70'), plaster='yes', dims='each c. 18 x 15 x 5 m deep',
  shape='four_sides', capacity_m3='c. 4000 total', feed='channel', feed_wadi='yes', kidron_feed='yes',
  notes='filled after the slope cisterns were full (feed by the aqueduct: INFERENCE from p. 168)',
  group_id='G-HYR-POOLS-AGG', covered_by='G-HYR-POOL-N;G-HYR-POOL-S;G-HYR-POOL-X')
R('GP-HERODION-AQ', 'GP94', 'pp. 166, 169', 'Herodion aqueduct from the Pools of Solomon', 'herodium', 'aqueduct',
  pt=('place', 'tekoa_herodium'), head='unknown', feed='spring', dims='c. 7 km', flow_from='unknown',
  period_as_given='Herodion founded by Herod', date_code='in_hedged', group_id='G-HERODIUM-AQ',
  notes='table: source "Pools of Solomon"; text: spring water from the "Solomonic Pools"')
R('GP-HERODION-CIS', 'GP94', 'p. 169', 'Herodion three cisterns (c. 2,500 m3)', 'herodium', 'cistern',
  aggregate='yes', count='3', pt=('place', 'tekoa_herodium'), capacity_m3='c. 2500', date_code='in_hedged',
  period_as_given='Herodion founded by Herod', group_id='G-HERODIUM-CIS')

# ----------------------------------------------------------------------------- Mazar 1989 (Jerusalem aqueducts)
R('MAZ-ARRUB-AQ', 'MAZ89', 'pp. 170-174, Fig. 1', 'Arrub aqueduct (Ein Kuweiziba - Birket el-Arrub - Solomon\'s Pools)',
  'arrub', 'aqueduct', pt=('wbadb', 'S4652'), head='yes', head_marker='', flow_from='S', feed='spring',
  bend='yes', dims='c. 39 km route, 10 km air distance; channel 0.40-0.50 m', plaster='yes',
  period_as_given='possibly the aqueduct of Pilate (Mazar); Mamluk repairs', date_code='in_hedged', label='CLAIM',
  named_wadi='Arrub', notes='head at Ein Kuweiziba (point 1), 830 m; very winding; position: WBADB S4652 '
  '(Ein Kuweizibe) = the head spring', group_id='G-ARRUB-AQ')
R('MAZ-ARRUB-POOL', 'MAZ89', 'p. 172', 'Birket el-Arrub', 'arrub', 'reservoir_pool', pt=('wbadb', 'S4533'),
  dims='?8 x 68 m (first digit illegible in OCR), depth 6-8 m', capacity_m3='>20000', plaster='yes',
  entrance='yes', feed='channel', shape='four_sides', named_wadi='Arrub',
  notes='steps in the SE corner; built aqueduct from springs to the west enters at the NW corner; outlet '
        'through an arched opening to a vaulted chamber', group_id='G-ARRUB-POOL')
R('MAZ-ARRUB-SMALLPOOL', 'MAZ89', 'p. 170', 'Small pool east of Birket el-Arrub (point 3; not preserved)', 'arrub',
  'reservoir_pool', pt=('wbadb', 'S4533'), feed='channel', notes='known from the Schick & Benzinger 1896 map')
R('MAZ-ARRUB-OUTLET', 'MAZ89', 'p. 172', 'Outlet of Birket el-Arrub into a vaulted control chamber', 'arrub',
  'outlet', pt=('wbadb', 'S4533'), named_wadi='Arrub', wall_at_outlet='yes',
  notes='arched opening c. 0.5 m into an ashlar barrel-vaulted room; "wall" = built ashlar chamber at the outlet')
R('MAZ-DILBA-DAM', 'MAZ89', 'p. 170', 'Dam carrying the aqueduct across Wadi Arrub at Ein ed-Dilba (point 2)',
  'arrub', 'dam', pt=('wbadb', 'S4533'), dims='original length c. 30 m', named_wadi='Arrub')
R('MAZ-DILBA-SPR', 'MAZ89', 'p. 170', 'Ein ed-Dilba spring with rock-cut spring tunnel (13 m)', 'arrub', 'spring',
  pt=('wbadb', 'S4533'), named_wadi='Arrub', notes='southern tributary of Wadi Arrub')
R('MAZ-KUWEIZIBA-SPR', 'MAZ89', 'pp. 170, 187 Fig. 20', 'Ein Kuweiziba (head spring of the Arrub aqueduct)', 'arrub',
  'spring', pt=('wbadb', 'S4652'), named_wadi='Arrub', notes='southern tributary of Wadi Arrub; name Kuweiziba')
R('MAZ-ARRUB-DAM8', 'MAZ89', 'p. 173', 'Dam in a tributary of Wadi Arrub carrying the aqueduct (point 8)', 'arrub',
  'dam', pt=('wbadb', 'S4533'), dims='23 m long, 2.5 m high, 2.5 m thick', named_wadi='Arrub',
  notes='large dressed stones; aqueduct on top')
R('MAZ-JISR-DAM', 'MAZ89', 'p. 173', 'Dam-bridge in Wadi Jisr (point 20)', 'arrub_route', 'dam', pt=None,
  dims='arch 1.80 m wide, 1.5 m high', period_as_given='pointed arch: late date', date_code='out',
  named_wadi='Jisr', notes='Schick saw earlier large-stone dam remains below')
R('MAZ-SMALLDAMS', 'MAZ89', 'p. 173', 'Small dams in Wadi Taqtaq, Wadi Udala (19) and Wadi Khalifa (22)', 'arrub_route',
  'dam', aggregate='yes', count='3', pt=None, notes='suggest the aqueduct also collected flood water')
R('MAZ-ARTAS-DAM', 'MAZ89', 'p. 173', 'Semicircular dam where the aqueduct crosses Wadi Artas (point 27)', 'artas',
  'dam', pt=('wbadb', 'S4223'), dims='14 x 3 x c. 3 m; radius c. 4 m', named_wadi='Artas',
  period_as_given='possibly a later period', date_code='undated')
R('MAZ-ARRUB-OUTLETS', 'MAZ89', 'p. 174', 'Water-drawing installations on the Arrub aqueduct (points 6, 21)',
  'arrub_route', 'outlet', aggregate='yes', count='2', pt=None, named_wadi='Arrub; Jisr',
  notes='rock-cut trough 75 x 75 cm at point 6 (Wadi Arrub); similar at point 21 (Wadi Jisr)')
R('MAZ-LOWER-AQ', 'MAZ89', 'pp. 174-177, 188', 'Lower aqueduct, Solomon\'s Pools to the Temple Mount', 'solomons_pools',
  'aqueduct', pt=('wbadb', 'S4206'), head='yes', head_marker='pool', marker_side='W', flow_from='S',
  feed='spring', bend='yes', dims='20.6 km; channel 0.40-0.50 m', plaster='yes',
  period_as_given='Hasmonean (Jannaeus?) per Mazar; Ottoman clay pipe 1541', date_code='in_hedged', label='CLAIM',
  notes='starts at the foot of the lower pool and from Ein Saleh, Ein Atan, Ein Faruja; pool lies west of the '
        'head (INFERENCE: the aqueduct leaves the east foot of the lower pool)', group_id='G-LOWER-AQ')
R('MAZ-BIAR-AQ', 'MAZ89', 'pp. 177-180, 188-189', 'Biar aqueduct (Ein Wadi el-Biyar to the upper pool)', 'biyar',
  'aqueduct', pt=None, head='yes', head_marker='any', marker_side='', flow_from='S', feed='spring',
  dims='4.7 km; tunnel 2.8 km with shafts; tunnel >500 m at Dhahr Baqqu', period_as_given='possibly Herod',
  date_code='in_hedged', label='CLAIM', named_wadi='Biyar',
  notes='head: karstic spring cave with built/cut stair and ashlar arch; position not given; inside box '
        '(between Solomon\'s Pools and the watershed, INFERENCE)', group_id='G-BIAR-AQ')
R('MAZ-BIAR-SPR', 'MAZ89', 'p. 178', 'Ein Wadi el-Biyar (Ein ed-Deraj) spring cave', 'biyar', 'spring', pt=None,
  named_wadi='Biyar', entrance='yes', notes='stepped access through an arch')
R('MAZ-BIAR-DAM', 'MAZ89', 'p. 179', 'Ancient wall damming Wadi Biyar at the tunnel end', 'biyar', 'dam', pt=None,
  dims='c. 4 m high', named_wadi='Biyar', notes='covered by the Mandate dam spoil')
R('MAZ-BIAR-POOL', 'MAZ89', 'p. 179', 'Pool at the end of the Biar tunnel (Schick)', 'biyar', 'reservoir_pool',
  pt=None, feed='wadi_runoff', feed_wadi='yes', named_wadi='Biyar', notes='to collect rain water flowing in the wadi')
R('MAZ-MUGHARA-AQ', 'MAZ89', 'p. 179', 'Built conduit from Ein Mughara to the Biar tunnel', 'biyar', 'aqueduct',
  pt=('oig', 164700, 119800, 100), head='yes', feed='spring', named_wadi='Biyar',
  notes='grid ref 1198 1647 given for Ein Mughara (read as E 164.7, N 119.8)')
R('MAZ-UPPER-AQ', 'MAZ89', 'pp. 180-183, 189', 'Upper aqueduct, Solomon\'s Pools to Jerusalem (with stone siphon)',
  'solomons_pools', 'aqueduct', pt=('wbadb', 'S4206'), head='yes', head_marker='pool', marker_side='S',
  flow_from='S', bend='yes', dims='c. 13 km; stone pipe 300 m preserved', plaster='yes',
  period_as_given='Legio X, 2nd century CE', date_code='partly',
  notes='first preserved segment 12 m north of the middle pool (pool south of the head); curves at the foot of '
        'Kh. Salih (Ramat Rahel) hill', group_id='G-UPPER-AQ')
R('MAZ-MARELIAS-POOL', 'MAZ89', 'p. 183', 'Ancient pool near Mar Elias monastery', 'mar_elias', 'reservoir_pool',
  pt=('wbadb', 'S3957'), notes='Schick linked it to the upper aqueduct; doubtful (Mazar)')
R('MAZ-RAILWAY-POOL', 'MAZ89', 'p. 183', 'Pool and channel at the Jerusalem railway station (Dalman 1908)',
  'jerusalem_railway', 'reservoir_pool', pt=None, feed='channel',
  notes='channel from the south at least 30 m; south wall of large ashlars (to 2.2 m)')
R('MAZ-SOL-UPPER', 'MAZ89', 'p. 184', 'Solomon\'s Pools: upper pool', 'solomons_pools', 'reservoir_pool',
  pt=('wbadb', 'S4206'), solomon='yes', dims='118 x 71 m, 9.5-11 m deep', capacity_m3='c. 85000',
  shape='four_sides', great='no', feed='channel', named_wadi='el-Khokh (tributary of Wadi Artas)',
  notes='rectangular; Biar aqueduct entered near its NW corner; name Burak Suleiman: travellers\' or Suleiman '
        'the Magnificent (n. 47)', group_id='G-SOL-UPPER')
R('MAZ-SOL-MIDDLE', 'MAZ89', 'p. 184', 'Solomon\'s Pools: middle pool', 'solomons_pools', 'reservoir_pool',
  pt=('wbadb', 'S4206'), solomon='yes', dims='135 m long, 50-76 m wide, 10-12 m deep', capacity_m3='c. 90000',
  shape='four_sides', great='no', feed='channel', named_wadi='el-Khokh (tributary of Wadi Artas)',
  notes='Arrub aqueduct entered at its NW corner (after Schick)', group_id='G-SOL-MIDDLE')
R('MAZ-SOL-LOWER', 'MAZ89', 'pp. 184, 190', 'Solomon\'s Pools: lower pool', 'solomons_pools', 'reservoir_pool',
  pt=('wbadb', 'S4206'), solomon='yes', dims='179 m long, 46-61 m wide, 8-16 m deep', capacity_m3='c. 113000',
  shape='four_sides', great='yes', feed='channel', named_wadi='el-Khokh (tributary of Wadi Artas)',
  period_as_given='probably built in the Mamluk period (15th c.)', date_code='out',
  notes='"the largest of the three"; inlet channel to its south wall', group_id='G-SOL-LOWER')
R('MAZ-SALEH-SPR', 'MAZ89', 'p. 185', 'Ein Saleh spring chamber (vaulted, 14.3 x 4.3 m) and tunnel', 'solomons_pools',
  'spring', pt=('wbadb', 'S4206'), entrance='yes', notes='c. 200 m NW of the upper pool')
R('MAZ-BURAQ-SPR', 'MAZ89', 'p. 186', 'Ein el-Buraq spring (below Qalat el-Buraq)', 'solomons_pools', 'spring',
  pt=('wbadb', 'S4206'))
R('MAZ-FARUJA-SPR', 'MAZ89', 'p. 186', 'Ein Faruja spring house below the lower pool', 'solomons_pools', 'spring',
  pt=('wbadb', 'S4206'), entrance='yes', notes='vaulted chamber 4.8 x 4.4 m; ashlar corridor 13 m')
R('MAZ-ATAN-SPR', 'MAZ89', 'p. 187', 'Ein Atan spring tunnel with three shafts', 'solomons_pools', 'spring',
  pt=('wbadb', 'S4206'))
R('MAZ-COLLECT', 'MAZ89', 'pp. 185-186, Fig. 17', 'Collecting installation near the upper pool (rooms A-C)',
  'solomons_pools', 'outlet', pt=('wbadb', 'S4206'), wall_at_outlet='yes', entrance='yes',
  notes='junction of Ein Saleh and Ein Buraq water; exits to the upper pool and by tunnel to the middle pool')
R('MAZ-BIRQANA-OUT', 'MAZ89', 'p. 175', 'Bir el-Qana: branch outlet of the lower aqueduct in Bethlehem', 'bethlehem',
  'outlet', pt=None, notes='a branch c. 30 m east from the south tunnel entrance; water drawn until recently')
R('MAZ-ARTAS-SPR', 'MAZ89', 'pp. 170, 193', 'Ein Artas spring (head of the Herodium aqueduct)', 'artas', 'spring',
  pt=('wbadb', 'S4223'), named_wadi='Artas')
R('MAZ-HERODIUM-AQ', 'MAZ89', 'pp. 192-193, Fig. 23', 'Aqueduct from Ein Artas to Herodium', 'herodium', 'aqueduct',
  pt=('wbadb', 'S4223'), dest_pt=('wbadb', 'S4287'), head='yes', flow_from='', feed='spring',
  dims='c. 5 km; channel c. 0.45 x 0.75 m',
  period_as_given='Herodian (Josephus); out of use in the Roman period', date_code='in_hedged', label='CLAIM',
  named_wadi='Tuhin / Artas', group_id='G-HERODIUM-AQ',
  notes='head at Ein Artas inside Artas village (grid ref partly illegible); WNW of Herodium')
R('MAZ-HERODIUM-POOL', 'MAZ89', 'p. 193', 'Built square pool at the foot of Herodium (aqueduct destination)', 'herodium',
  'reservoir_pool', pt=('wbadb', 'S4287'), shape='four_sides', feed='channel',
  notes='"it seems" the final destination (hedged)', group_id='G-LHERODIUM-POOL')

# ----------------------------------------------------------------------------- Amit 1989 (Doq)
R('AMI-DOQ-AQ', 'AMI89', 'pp. 224-226, Figs. 2-6', 'Doq aqueduct (intake A to cisterns)', 'doq', 'aqueduct',
  pt=('oig', 190600, 142600, 100), head='yes', head_marker='any', marker_side='', flow_from='W',
  feed='wadi_runoff', feed_wadi='yes', bend='yes', plaster='yes', dims='0.5 km; 0.60-0.80 m wide',
  period_as_given='plaster typical of the Hasmonean period', date_code='in', group_id='G-DOQ-AQ',
  notes='intake at grid 1906/1426 (E 190.6, N 142.6) in a small wadi NW of the fort, at a c. 2 m rock step '
        '("a kind of small waterfall"); turns north and east round the fort, then south')
R('AMI-DOQ-FALL', 'AMI89', 'p. 224', 'Small waterfall (c. 2 m rock step) at the Doq intake', 'doq', 'waterfall',
  pt=('oig', 190600, 142600, 100), near_bend_m=500, quote='מעין מפל קטן בגובה כ-2 מ\'',
  notes='bend: the 500 m aqueduct turns north, east and south (INFERENCE: every bend lies within 500 m)')
R('AMI-DOQ-POOLS', 'AMI89', 'p. 225', 'Two small pools beside the canal before point C', 'doq', 'reservoir_pool',
  aggregate='yes', count='2', pt=('place', 'doq'), plaster='yes', dims='western c. 1.5 x 1.5 m',
  shape='four_sides', entrance='yes', feed='unknown',
  notes='western pool: three plastered sides, possibly steps; below the canal level')
R('AMI-DOQ-CIS', 'AMI89', 'pp. 226-227, Fig. 7, table', 'Doq cisterns 1-9', 'doq', 'cistern', aggregate='yes',
  count='9', pt=('place', 'doq'), feed='channel', feed_wadi='yes', plaster='yes', shape='four_sides',
  capacity_m3='2090', period_as_given='probably founded with the Hasmonean fortress', date_code='in_hedged',
  notes='rectangular or trapezoidal; filled by chutes from the canal; settling basin at cistern 9',
  group_id='G-DOQ-CIS')

# ----------------------------------------------------------------------------- Meshel & Amit 1989 (Cypros)
R('MA-HER-AQ', 'MA89', 'pp. 229-233, 235-236', 'Herodian aqueduct from Ein Fawwar to Cypros', 'cypros', 'aqueduct',
  pt=('wbadb', 'S2621'), head='yes', head_marker='pool', marker_side='', flow_from='W', feed='spring',
  qelt='yes', named_wadi='Prat (Qelt)', bend='yes', dims='c. 14 km (7.25 km air)',
  period_as_given='completed under Herod; upper part possibly Hasmonean (Porath & Izdarechet)', date_code='in',
  group_id='G-CYP-HER', notes='head at Ein Fawwar, into whose spring pool the Ein Fara feeder poured')
R('MA-FAWWAR-POOL', 'MA89', 'p. 229', 'Spring pool of Ein Fawwar', 'ein_fawwar', 'reservoir_pool',
  pt=('wbadb', 'S2621'), qelt='yes', named_wadi='Prat (Qelt)', fissure_east='yes_1km', fissure_m=1000,
  feed='channel', notes='natural spring pool, joined by the Ein Fara feeder aqueduct; point 2 natural fissure (15 m long, to 4 m deep) on the aqueduct downstream '
        '(east) of the spring (INFERENCE: first kilometre east of the spring)')
R('MA-FARA-AQ', 'MA89', 'p. 229', 'Feeder aqueduct from Ein Fara to Ein Fawwar', 'ein_fara', 'aqueduct',
  pt=('wbadb', 'S2709'), head='yes', flow_from='W', feed='spring', qelt='yes', named_wadi='Prat (Qelt)',
  bend='yes', period_as_given='part of the Herodian system', date_code='in_hedged', group_id='G-CYP-FARA',
  notes='c. 6 km; crosses the stream twice to take Ein Fajira')
R('MA-FARA-SPR', 'MA89', 'p. 229', 'Ein Fara', 'ein_fara', 'spring', pt=('wbadb', 'S2709'), qelt='yes',
  named_wadi='Prat (Qelt)')
R('MA-FAWWAR-SPR', 'MA89', 'p. 229', 'Ein Fawwar', 'ein_fawwar', 'spring', pt=('wbadb', 'S2621'), qelt='yes',
  named_wadi='Prat (Qelt)', notes='karstic spring; up to 3,000 m3 per hour')
R('MA-FAJIRA-SPR', 'MA89', 'p. 229', 'Ein Fajira', 'ein_fara', 'spring', pt=None, qelt='yes',
  named_wadi='Prat (Qelt)', notes='grid ref printed 1377 1804 (not converted: reading uncertain)')
R('MA-CROSSWALLS', 'MA89', 'p. 232', 'Base walls with flood openings where the aqueduct crosses small ravines',
  'qelt_route', 'dam', aggregate='yes', count='', pt=None, qelt='yes', named_wadi='Prat (Qelt)',
  notes='"a kind of dams" with one or more openings; east of Ein Qelt')
R('MA-RUNOFF-CH', 'MA89', 'pp. 233-234, Figs. 8-9', 'Hasmonean runoff channel above Cypros', 'cypros', 'aqueduct',
  pt=('asi', '109/5/7'), head='unknown', feed='runoff', feed_wadi='no', plaster='yes',
  period_as_given='Hasmonean', date_code='in', group_id='G-CYP-RUNOFF',
  notes='rock-cut and plastered; slope above it plastered too; 62 cm wide')
R('MA-CIS', 'MA89', 'p. 234, Fig. 10', 'Cypros four large cisterns on the slope facing Jericho', 'cypros', 'cistern',
  aggregate='yes', count='4', pt=('asi', '109/5/7'), feed='channel', feed_wadi='no', plaster='unknown',
  shape='not_four_sides', dims='third cistern 17 x 7 m, 8 m deep, triangular section; >=500 m3',
  period_as_given='Hasmonean system', date_code='in', group_id='G-CYP-CIS',
  notes='only the third preserved enough; shape coded from it alone (triangular)')
R('MA-DISTR-POOL', 'MA89', 'p. 236, Fig. 13', 'Distribution pool at point 39 between the cistern pairs', 'cypros',
  'reservoir_pool', pt=('asi', '109/5/7'), feed='channel', qelt='yes', period_as_given='Herodian aqueduct',
  date_code='in_hedged', notes='floor 1 m below the sill; branches south (cisterns) and east (Jericho fields)')
R('MA-POINT38', 'MA89', 'p. 231 (map key)', 'Small pool at point 38 with a branch to the east', 'cypros',
  'reservoir_pool', pt=('asi', '109/5/7'))
R('MA-POINT40', 'MA89', 'p. 231 (map key)', 'Ancient pool under the modern purification works (point 40)', 'cypros',
  'reservoir_pool', pt=('asi', '109/5/7'))
R('MA-PIPE-AQ', 'MA89', 'pp. 237-239', 'Pipe aqueduct (pair of clay pipes) along the Qelt', 'qelt_route', 'aqueduct',
  pt=('wbadb', 'S2621'), head='yes', qelt='yes', named_wadi='Prat (Qelt)', bend='unknown',
  period_as_given='Early Arab period', date_code='out', notes='bridge over Wadi Abu Dabaa c. 130 m long, 25 m high')
R('MA-PIPE-POOLS', 'MA89', 'pp. 238-239, Fig. 18', 'Settling and pressure-release pools on the pipe aqueduct',
  'qelt_route', 'reservoir_pool', aggregate='yes', count='', pt=None, dims='1.4 x 1.4 m', shape='four_sides',
  qelt='yes', period_as_given='Early Arab', date_code='out')
R('MA-BEITJABR', 'MA89', 'p. 233, Fig. 6', 'Beit Jabr el-Fauqani reservoir (Manzal Jabr)', 'beit_jabr', 'reservoir_pool',
  pt=('asi', '109/4/20'), group_id='G-BEITJABR', feed='channel', period_as_given='Early Arab period', date_code='out',
  notes='rock-cut and built, vaulted; connected with the pipe aqueduct')

# ----------------------------------------------------------------------------- Patrich 1989 (Hyrcania), repo inventory
R('PAT-S-AQ', 'PAT89', 'pp. 244-251, Fig. 1 (HY-1)', 'Hyrcania southern aqueduct from the Kidron', 'hyrcania',
  'aqueduct', pt=None, head='yes', head_marker='any', marker_side='', flow_from='SW', feed='wadi_diversion',
  feed_wadi='yes', kidron_feed='yes', named_wadi='Kidron', dims='c. 9 km', period_as_given='Herodian',
  date_code='in', group_id='G-HYR-SAQ',
  notes='intake dam in the Kidron c. 1,300 m west of the Small Laura (not located; inside box by description)')
R('PAT-S-DAM', 'PAT89', 'p. 244 (HY-1)', 'Intake dam of the southern aqueduct in the Kidron', 'hyrcania', 'dam',
  pt=None, kidron_feed='yes', named_wadi='Kidron', period_as_given='southern line Herodian', date_code='in')
R('PAT-N-AQ', 'PAT89', 'p. 251 (HY-44); ASI 109/7/48', 'Hyrcania northern aqueduct from Wadi Abu Shula', 'hyrcania',
  'aqueduct', pt=('asi', '109/7/48'), dest_pt=('asi', '109/7/70'), head='yes', head_marker='any', marker_side='',
  flow_from='', feed='wadi_diversion', feed_wadi='yes', named_wadi='Abu Shula (Sekhakha)', dims='1,950 m',
  period_as_given='northern line Hasmonean', date_code='in', group_id='G-HYR-NAQ',
  notes='head: intake dam 17.5 m (station 44); bearing from Hyrcania computed from the ASI points')
R('PAT-N-DAM', 'PAT89', 'p. 251 (HY-44)', 'Intake dam of the northern aqueduct (17.5 m)', 'hyrcania', 'dam',
  pt=('asi', '109/7/48'), named_wadi='Abu Shula (Sekhakha)', period_as_given='northern line Hasmonean',
  date_code='in')
R('PAT-42-DAM', 'PAT89', 'p. 251 (HY-42)', 'Downstream runoff diversion dam (station 42)', 'hyrcania', 'dam',
  pt=None, period_as_given='possible Byzantine reuse', date_code='undated')
R('PAT-POOL-N', 'PAT89', 'pp. 255-256, Fig. 22 (HY-pool-N)', 'Hyrcania western double pool: northern member',
  'hyrcania', 'reservoir_pool', pt=('asi', '109/7/70'), dims='sides 19 / 15 / 18.2 / 16 m; depth 5 m',
  shape='four_sides', north='yes', great='unknown', feed='unknown', kidron_feed='unknown',
  group_id='G-HYR-POOL-N',
  notes='northern member of the double pool (west of summit); full sides given for this member only, so "great" '
        'cannot be compared; no inlet identified (research/measurements/cycle7/hyrcania_supply.md)')
R('PAT-POOL-S', 'PAT89', 'pp. 255-256, Fig. 22 (HY-pool-S)', 'Hyrcania western double pool: southern member',
  'hyrcania', 'reservoir_pool', pt=('asi', '109/7/70'), dims='depth 2.6 m', shape='four_sides', north='no',
  great='unknown', feed='unknown', group_id='G-HYR-POOL-S')
R('PAT-POOL-X', 'PAT89', 'p. 255 (HY-pool-extra-S)', 'Hyrcania additional filled pool south of the bridge', 'hyrcania',
  'reservoir_pool', pt=('asi', '109/7/70'), north='no', group_id='G-HYR-POOL-X')
R('PAT-CIS', 'PAT89', 'p. 256', 'Hyrcania rock-cut cisterns (20)', 'hyrcania', 'cistern', aggregate='yes', count='20',
  pt=('asi', '109/7/70'), feed='channel', feed_wadi='yes', kidron_feed='yes', group_id='G-HYR-CIS',
  notes='cisterns S and F are stepped installations')

# ----------------------------------------------------------------------------- Netzer 1989 (estate)
R('NET-PRAT-AQ', 'NET89', 'pp. 273-276', 'Nahal Prat (Qelt) aqueduct in the western Jericho plain', 'jericho_estate',
  'aqueduct', pt=('asi', '109/5/2'), head='unknown', flow_from='W', feed='spring', qelt='yes',
  named_wadi='Prat (Qelt)', bend='yes', plaster='yes', dims='c. 0.60 m wide, 0.40-0.50 m deep',
  period_as_given='John Hyrcanus I', date_code='in', group_id='G-QELT-JERICHO-AQ',
  notes='turns north at the mouth of Nahal Prat; slight windings over 800 m; detour 75 m into Wadi Shaq ed-Dabi')
R('NET-DRYFALL', 'NET89', 'p. 275', 'Dry waterfall of the southern tributary of Wadi Shaq ed-Dabi', 'jericho_estate',
  'waterfall', pt=('asi', '109/5/2'), near_bend_m=250, named_wadi='Shaq ed-Dabi',
  notes='aqueduct runs inside the dry fall c. 250 m north of the turn at the Nahal Prat mouth (at the threshold)')
R('NET-OUTLETS', 'NET89', 'p. 276, Fig. 1 (I-VI)', 'Six water outlets of the Prat aqueduct in the estate',
  'jericho_estate', 'outlet', aggregate='yes', count='6', pt=('asi', '109/5/2'), qelt='yes',
  named_wadi='Prat (Qelt)', wall_at_outlet='unknown', period_as_given='Hyrcanus I estate', date_code='in',
  notes='short built, plastered channels attached at the outlets')
R('NET-OUTLETS-B', 'NET89', 'p. 280, Fig. 14', 'Outlets with built side walls on the Prat and Naaran aqueducts',
  'jericho_estate', 'outlet', aggregate='yes', count='', pt=('asi', '109/5/2'), wall_at_outlet='yes',
  qelt='unknown', period_as_given='Hasmonean aqueducts', date_code='in',
  notes='opening with sides on both sides; stones added outside some openings')
R('NET-NAARAN-AQ', 'NET89', 'pp. 277-279', 'Naaran aqueduct (north and south branches)', 'jericho_estate', 'aqueduct',
  pt=('place', 'ain_duk'), head='yes', flow_from='N', feed='spring', qelt='no', named_wadi='Nueima', bend='yes',
  period_as_given='early in the reign of Alexander Jannaeus', date_code='in_hedged', group_id='G-NAARAN-AQ',
  notes='from the Naaran springs (or Ein el-Auja); branches 120 m W of the estate NW corner; arched turns; '
        'head position = places_v2 ain_duk (Netzer 1975 names Ein Nueima)')
R('NET-NAARAN-POOL', 'NET89', 'p. 277', 'Flow-control pool at the foot of the north branch (2 x 2.2 m)',
  'jericho_estate', 'reservoir_pool', pt=('asi', '109/5/2'), dims='2 x 2.2 m', shape='four_sides', feed='channel',
  period_as_given='Jannaeus', date_code='in_hedged', group_id='G-NAARAN-POOL')
R('NET-PIPE', 'NET89', 'p. 277', 'Clay pipe (12 cm) from the Prat aqueduct to the central building', 'jericho_estate',
  'aqueduct', pt=('asi', '109/5/14'), qelt='yes', dims='c. 380 m', period_as_given='Hyrcanus I', date_code='in')
R('NET-POOL-HYRC2', 'NET89', 'p. 280', 'Large swimming pool east of the Twin Palaces (20 x 12.5 m)', 'jericho_palaces',
  'reservoir_pool', pt=('asi', '109/5/14'), dims='20 x 12.5 m', shape='four_sides', period_as_given='late Hasmonean',
  date_code='in', group_id='G-POOL-HYRC2')

# ----------------------------------------------------------------------------- Ilan & Amit 1989 (Qumran)
R('IA-AQ', 'IA89', 'pp. 283-285, Fig. 1', 'Qumran aqueduct', 'kh_qumran', 'aqueduct', pt=('wbadb', 'E754'),
  head='yes', head_marker='pool', marker_side='S', flow_from='W', feed='wadi_diversion', feed_wadi='yes',
  named_wadi='Qumran', bend='yes', dims='c. 700 m (Galor)', period_as_given='later occupation phase (authors)',
  date_code='partly', group_id='G-QUMRAN-AQ',
  notes='head at the foot of the penultimate great waterfall; start on the north bank, basin in the bed to the '
        'south (INFERENCE); runs ESE')
R('IA-FALL', 'IA89', 'pp. 283-284', 'Penultimate great waterfall of Nahal Qumran at the aqueduct head', 'kh_qumran',
  'waterfall', pt=('wbadb', 'E754'), near_bend_m=60, named_wadi='Qumran',
  notes='branch 9 bends south within the first c. 40 m of channel (INFERENCE: bend within c. 60 m of the fall)')
R('IA-BASIN', 'IA89', 'pp. 283-284', 'Basin below the waterfall (point 2)', 'kh_qumran', 'reservoir_pool',
  pt=('wbadb', 'E754'), feed='channel', named_wadi='Qumran', fissure_east='yes', fissure_m=60,
  notes='the aqueduct begins at the basin ("joins" it); semi-natural pool if dammed (dam 4 reconstructed); natural cracks in the tunnel downstream to the east '
        '(MP18 p. 79; INFERENCE on bearing and distance)')
R('IA-DAM', 'IA89', 'p. 284; p. 288 n. 5', 'Proposed dam 4 (no remains)', 'kh_qumran', 'dam', pt=('wbadb', 'E754'),
  label='CLAIM', named_wadi='Qumran', notes='reconstructed by the authors; not observed')
R('IA-WALL19', 'IA89', 'p. 285', 'Wall joining the aqueduct from the north at the final turn (point 19)',
  'kh_qumran', 'dam', pt=('wbadb', 'E754'), label='CLAIM',
  notes='interpreted as a low runoff-collecting barrier (authors)')
R('MP-TUNNEL', 'MP18', 'pp. 78-79', 'Qumran aqueduct tunnels with natural cracks', 'kh_qumran', 'aqueduct',
  pt=('wbadb', 'E754'), head='unknown', flow_from='W', named_wadi='Qumran', group_id='G-QUMRAN-AQ',
  notes='12.40 m tunnel "bypassing the crag from west to east"; two cracks')
R('MP-DAM', 'MP18', 'pp. 77-78', 'Surmised diversion dam in upper Nahal Qumran (no remains)', 'kh_qumran', 'dam',
  pt=('wbadb', 'E754'), label='CLAIM', named_wadi='Qumran')

# ----------------------------------------------------------------------------- Galor (Qumran plastered pools)
_q = dict(pt=('wbadb', 'E754'), plaster='yes', named_wadi='Qumran', feed_wadi='yes',
          period_as_given='de Vaux periods (reported by Galor, who doubts exact dates)')
R('GAL-L110', 'GAL', 'pp. 259-261, Fig. 4', 'Qumran L110 circular pool', 'kh_qumran', 'reservoir_pool',
  dims='diameter 5.10 m', shape='not_four_sides', feed='channel', capacity_m3='110', date_code='in_hedged',
  **{**_q, 'period_as_given': 'Iron Age (de Vaux), refurbished period Ia'})
_rect = {'L56/58', 'L71', 'L91', 'L48/49', 'L43', 'L117', 'L118', 'L138'}  # Galor groups b and c: rectangular
for loc_id, d, cap, feed, ent, per, note in [
    ('L117', 'basin 2.4 x 1.8 m; 13 steps', '60', 'channel', 'yes', 'Ia', ''),
    ('L118', 'basin 2.4 x 1.9 m; 8 steps', '40', 'channel', 'yes', 'Ia', ''),
    ('L138', 'basin 2.2 x 0.9 m; 8 steps', '25', 'channel', 'yes', 'Ib', 'NW of the complex; via L136/L137'),
    ('L48/49', '7.2 x 2.7 m; 14 steps', '40', 'channel', 'yes', 'Ib', 'secondary channel from the south'),
    ('L56/58', '17.0 x 3.3 m; 11 steps', '85', 'channel', 'yes', 'Ib', 'later divided'),
    ('L71', '17.4 x 4.5 m; 20 steps', '300', 'channel', 'yes', 'Ib', '"the largest stepped pool" at the site'),
    ('L91', '12.6 x 4.6 m; no steps', '250', 'unknown', 'unknown', 'Ib', ''),
    ('L83', 'three steps', '5', 'channel', 'yes', 'Ib', 'directly connected to the main channel'),
    ('L85', 'basin 1.7 x 1.7 m; four steps', '5', 'channel', 'yes', 'Ib', 'aperture from L83'),
    ('L50', '2.2 x 2.1 m with stepped addition', '6', 'unknown', 'yes', 'Ib', ''),
    ('L67', '1.4 x 1.6 m', '2', 'channel', 'yes', 'Ib', ''),
    ('L68', '3.0 x 2.0 m; steps', '2.5', 'channel', 'yes', 'Ib', ''),
    ('L69', '2.72 x 2.5 m; steps', '7', 'channel', 'yes', 'Ib', ''),
    ('L72', '2.7 x 2.0 m; no steps', '2', 'channel', 'unknown', 'Ib', ''),
    ('L70', '2.7 x 1.2 m; no steps', '3', 'channel', 'unknown', 'Ib', ''),
    ('L43', 'additional entrance to L48/49', '4', 'unknown', 'yes', 'Ib', 'separated by a wall from L48/49 steps'),
    ('L54', 'narrow pool', '2', 'channel', 'unknown', 'Ib', 'small channel from L56'),
    ('L55', 'narrow pool', '6', 'unknown', 'unknown', 'Ib', 'supply cannot be reconstructed'),
    ('L57', 'narrow pool', '5', 'unknown', 'unknown', 'Ib', 'supply cannot be reconstructed'),
    ('L119', '1.8 x 1.8 m', '1', 'channel', 'unknown', 'Ia', 'channel below it to L110'),
    ('L119bis', 'small basin', '1', 'unknown', 'unknown', 'later stage', ''),
]:
    great = 'yes' if loc_id == 'L71' else 'no'
    R('GAL-' + loc_id.replace('/', '-'), 'GAL', 'pp. 258-268, Table 1', f'Qumran {loc_id} plastered pool', 'kh_qumran',
      'reservoir_pool', dims=d, capacity_m3=cap, feed=feed, entrance=ent, great=great,
      shape='four_sides' if (' x ' in d or loc_id in _rect) else 'unknown',
      date_code='in_hedged' if per in ('Ia', 'Ib') else 'undated', notes=note,
      **{**_q, 'period_as_given': f'de Vaux period {per} (reported by Galor)'})
R('GAL-L34', 'GAL', 'pp. 266-267, Fig. 11', 'Qumran L34 tubs and small basins (four)', 'kh_qumran', 'basin_tank',
  aggregate='yes', count='4', capacity_m3='0.6', date_code='in_hedged',
  **{**_q, 'period_as_given': 'de Vaux period Ib (reported by Galor)'})
R('GAL-AQ', 'GAL', 'p. 260 and n. 7', 'Qumran aqueduct from a catch basin at the head of the wadi', 'kh_qumran',
  'aqueduct', head='yes', head_marker='pool', flow_from='', feed='wadi_diversion', group_id='G-QUMRAN-AQ',
  date_code='in_hedged', **{**_q, 'period_as_given': 'built in period Ib (de Vaux, reported by Galor)'})

# ----------------------------------------------------------------------------- Damati 1989 (Martyrius) and Hirschfeld 1989 (Chariton)
_m = dict(pt=('wbadb', 'S3364'), period_as_given='Byzantine monastery (founded c. 470s); gardens possibly Early '
          'Arab', date_code='out')
R('DAM-UPPER-CIS', 'DAM89', 'p. 299', 'Martyrius upper garden cistern (c. 2,000 m3)', 'martyrius', 'cistern',
  feed='roof_runoff', feed_wadi='no', capacity_m3='c. 2000', **_m)
R('DAM-UPPER-POOL', 'DAM89', 'p. 299, Fig. 2', 'Martyrius upper garden pool (1.2 x 1.5 m)', 'martyrius',
  'reservoir_pool', dims='1.2 x 1.5 m', shape='four_sides', **_m)
R('DAM-SOUTH-CIS', 'DAM89', 'p. 299', 'Martyrius south garden cisterns (two)', 'martyrius', 'cistern',
  aggregate='yes', count='2', feed='unknown', feed_wadi='no',
  notes='collect runoff from the long western spur (catchment c. 50 dunams); channels not stated', **_m)
R('DAM-EAST-CIS', 'DAM89', 'p. 301', 'Martyrius east garden cistern fed by two channels from the spur', 'martyrius',
  'cistern', feed='channel', feed_wadi='no', capacity_m3='c. 1500', **_m)
R('DAM-EAST-POOLS', 'DAM89', 'pp. 301-302', 'Martyrius east garden pools (three)', 'martyrius', 'reservoir_pool',
  aggregate='yes', count='3', plaster='yes', dims='to 2 x 2.8 m, 1.8 m deep', shape='four_sides', **_m)
R('DAM-CHANNELS', 'DAM89', 'pp. 302-303', 'Martyrius irrigation channels of stone segments (eight)', 'martyrius',
  'aqueduct', aggregate='yes', count='8', **_m)
R('DAM-MON-CIS', 'DAM89', 'p. 304 n. 3', 'Martyrius monastery cisterns (two large; one by the west wall)',
  'martyrius', 'cistern', aggregate='yes', count='3', feed='channel', feed_wadi='no',
  notes='the west-wall cistern is fed by an aqueduct draining runoff from the western spur', **_m)
_c = dict(pt=('asi', '108/2/17'), period_as_given='Byzantine (5th-6th c. CE)', date_code='out')
R('HIR-GREAT', 'HIR89', 'pp. 306-308, Figs. 2-4', 'Chariton great reservoir Bir el-Uweiniza', 'chariton',
  'reservoir_pool', dims='19.6 x 14 m', shape='four_sides', plaster='yes', great='yes', feed='channel',
  feed_wadi='yes', notes='filled by flood water of the ravine through a c. 60 m diversion channel; "the great '
  'reservoir"; dated first half of the 5th c. CE', **_c)
R('HIR-ROUND', 'HIR89', 'pp. 308-309, Figs. 5-7', 'Chariton round secondary reservoir (no. 2)', 'chariton',
  'reservoir_pool', dims='diameter 5.1 m', shape='not_four_sides', great='no', feed='channel', **_c)
R('HIR-RECT', 'HIR89', 'p. 309, Fig. 8', 'Chariton rectangular secondary reservoir (no. 3)', 'chariton',
  'reservoir_pool', dims='10.3 x 3.2 m', shape='four_sides', great='no', feed='channel', **_c)
R('HIR-AQ', 'HIR89', 'p. 309', 'Chariton aqueduct from the great reservoir to the secondary reservoirs', 'chariton',
  'aqueduct', head='unknown', **_c)
R('HIR-CORE-CIS', 'HIR89', 'p. 306', 'Chariton laura core cisterns (about seven)', 'chariton', 'cistern',
  aggregate='yes', count='7', plaster='yes', feed='roof_runoff', feed_wadi='no', **_c)
R('HIR-GARDEN-CIS', 'HIR89', 'pp. 309-310', 'Chariton garden cisterns (three groups; 28 cisterns and reservoirs)',
  'chariton', 'cistern', aggregate='yes', count='28', feed='channel', feed_wadi='no',
  notes='first group fed by runoff channels (channel 7)', **_c)
R('HIR-POOL18', 'HIR89', 'p. 310', 'Chariton pool remains at point 18', 'chariton', 'reservoir_pool', **_c)
R('HIR-MARSABA', 'HIR89', 'p. 311', 'Mar Saba great reservoir and settling pool (Cyril of Scythopolis)', 'mar_saba',
  'reservoir_pool', pt=('asi', '109/7/98'), label='CLAIM', great='yes', period_as_given='Byzantine (literary)',
  date_code='out', notes='literary source; no field record')
R('HIR-MARTYRIUS-GREAT', 'HIR89', 'p. 311', 'Martyrius great reservoir under the courtyard (22 x 14 m)', 'martyrius',
  'reservoir_pool', pt=('wbadb', 'S3364'), dims='22 x 14 x c. 10 m', capacity_m3='c. 3000', great='yes',
  shape='four_sides', feed='runoff', period_as_given='Byzantine', date_code='out',
  notes='fed by runoff from the courtyard and buildings')
R('HIR-EUTHYMIUS', 'HIR89', 'p. 311', 'Euthymius monastery reservoirs (two-mouthed reservoir; 12 x 18 m, 15 m deep)',
  'euthymius', 'reservoir_pool', aggregate='yes', count='2', pt=('wbadb', 'S3195'), dims='12 x 18 m, 15 m deep',
  period_as_given='Byzantine (431 CE and later)', date_code='out')
R('HIR-QASRYAHUD', 'HIR89', 'p. 311', 'Reservoir west of Qasr el-Yahud (St John) with aqueduct from Ein es-Sultan',
  'qasr_el_yahud', 'reservoir_pool', pt=('wbadb', 'S2651'), group_id='G-QASRYAHUD', feed='channel', dims='c. 10 m deep',
  period_as_given='Justinian (SWP suggestion)', date_code='out', label='CLAIM')
R('HIR-QASRYAHUD-AQ', 'HIR89', 'p. 311', 'Aqueduct from Elisha\'s spring (Ein es-Sultan) to Qasr el-Yahud',
  'qasr_el_yahud', 'aqueduct', pt=('wbadb', 'E334'), dest_pt=('wbadb', 'S2651'), head='yes', flow_from='',
  feed='spring',
  period_as_given='Justinian (SWP suggestion)', date_code='out', label='CLAIM')
R('HIR-ZIYAR', 'HIR89', 'pp. 311-312', 'Kh. Ziyar el-Ghanam built reservoirs (two)', 'ziyar_el_ghanam',
  'reservoir_pool', aggregate='yes', count='2', pt=('wbadb', 'E808'), dims='one 11.1 x 7.4 m', plaster='yes',
  shape='four_sides', period_as_given='Byzantine monastery', date_code='out')

# ----------------------------------------------------------------------------- Netzer 1975 and 2001 (Jericho, Herodium)
R('NET75-NAARAN', 'NET75', 'p. 89', 'Six-kilometre aqueduct from Ein Nueima (Naaran) to the palace', 'jericho_palaces',
  'aqueduct', pt=('place', 'ain_duk'), head='yes', flow_from='N', feed='spring', qelt='no', named_wadi='Nueima',
  period_as_given='pre-Herodian, probably Hasmonean', date_code='in_hedged', group_id='G-NAARAN-AQ')
R('NET75-B93-CIS', 'NET75', 'p. 97', 'Cistern under room B93 of Herod\'s third palace', 'jericho_palaces', 'cistern',
  pt=('asi', '109/5/14'), dims='c. 8.2 x 4.4 m', shape='four_sides', period_as_given='Herodian palace',
  date_code='in')
R('NET75-B107', 'NET75', 'p. 99; NET01B p. 57', 'Pool B107 of Herod\'s third palace', 'jericho_palaces',
  'reservoir_pool', pt=('asi', '109/5/14'), dims='c. 90 x 42 m', shape='four_sides', plaster='yes', great='yes',
  period_as_given='Herodian ("I believe")', date_code='in_hedged',
  notes='"the largest within the limits of the winter palace complex" (2001 p. 57)')
R('NET01-FIRSTPOOLS', 'NET01B', 'pp. 19-20', 'Two small swimming pools west of the first Hasmonean palace',
  'jericho_palaces', 'reservoir_pool', aggregate='yes', count='2', pt=('asi', '109/5/14'), dims='second 9 x 8 m',
  shape='four_sides', feed='channel', period_as_given='John Hyrcanus I', date_code='in', group_id='G-J06',
  notes='fed by a pipe, probably an offshoot of the underground pipe')
R('NET01-POOLNORTH', 'NET01B', 'p. 29', 'Replacement pool 30 m north beyond the Naaran conduit', 'jericho_palaces',
  'reservoir_pool', pt=('asi', '109/5/14'), north='yes', period_as_given='Jannaeus (Fortified Palace stage)',
  date_code='in', notes='built when a pool was cut by the moat; "north" relative to the pools complex')
R('NET01-TWIN-E', 'NET01B', 'p. 34', 'Twin Palaces: swimming pool of the eastern garden', 'jericho_palaces',
  'reservoir_pool', pt=('asi', '109/5/14'), period_as_given='Salome Alexandra', date_code='in')
R('NET01-TWIN-W', 'NET01B', 'p. 35', 'Twin Palaces: swimming pool of the western garden (7 x 7 m)', 'jericho_palaces',
  'reservoir_pool', pt=('asi', '109/5/14'), dims='7 x 7 m', shape='four_sides', period_as_given='Salome Alexandra',
  date_code='in', notes='"the smallest one revealed so far in Jericho"')
R('NET01-HYRC2', 'NET01B', 'p. 38', 'Pool of Hyrcanus II east of the Twin Palaces', 'jericho_palaces',
  'reservoir_pool', pt=('asi', '109/5/14'), entrance='yes', plaster='yes', period_as_given='Hyrcanus II',
  date_code='in', group_id='G-POOL-HYRC2', notes='bench and steps; entered from the mansion garden')
R('NET01-RECT', 'NET01B', 'p. 38', 'Rectangular pool 5.3 x 5.5 m', 'jericho_palaces', 'reservoir_pool',
  pt=('asi', '109/5/14'), dims='5.3 x 5.5 m', shape='four_sides', period_as_given='Hasmonean (late)', date_code='in')
R('NET01-POOL57', 'NET01B', 'p. 39', 'Pool 5.7 x 3.5 m of uncertain function', 'jericho_palaces', 'reservoir_pool',
  pt=('asi', '109/5/14'), dims='5.7 x 3.5 m', shape='four_sides', period_as_given='Hasmonean', date_code='in')
R('NET01-MIKVAOT', 'NET01B', 'pp. 17, 33, 37, 39, 41', 'Hasmonean and Herodian palace stepped pools (mikvaot, '
  'frigidaria)', 'jericho_palaces', 'reservoir_pool', aggregate='yes', count='', pt=('asi', '109/5/14'),
  entrance='yes', period_as_given='Hasmonean and Herodian', date_code='in',
  notes='Netzer calls them pools; ritual-bath function per author')
R('NET01-LH-POOL', 'NET01B', 'pp. 108-110, Figs. 140-144', 'Lower Herodium great pool', 'herodium', 'reservoir_pool',
  pt=('wbadb', 'S4287'), dims='69 x 45 m, 3 m deep', shape='four_sides', plaster='yes', entrance='yes', great='yes',
  feed='channel', period_as_given='Herodian', date_code='in', group_id='G-LHERODIUM-POOL',
  notes='four flights of stairs; water outlet near the bottom (irrigation); fed by the aqueduct (p. 106)')
R('NET01-LH-BATHPOOL', 'NET01B', 'p. 111', 'Lower Herodium bathhouse pool cut into rock (10.4 x 5.2 m)', 'herodium',
  'reservoir_pool', pt=('wbadb', 'S4287'), dims='10.4 x 5.2 m', shape='four_sides', great='no',
  period_as_given='Herod\'s time', date_code='in')
R('NET01-H-CIS', 'NET01B', 'pp. 105-106', 'Herodium mountain cisterns (at the foot, intermediate, under the palace)',
  'herodium', 'cistern', aggregate='yes', count='', pt=('place', 'tekoa_herodium'), feed='unknown',
  period_as_given='Herodian', date_code='in', group_id='G-HERODIUM-CIS',
  notes='rainwater cisterns; the intermediate cistern filled by funnel and pipe')
R('NET01-HYR-POOLS', 'NET01B', 'p. 75', 'Two open pools hewn in bedrock west of Hyrcania', 'hyrcania',
  'reservoir_pool', aggregate='yes', count='2', pt=('asi', '109/7/70'), group_id='G-HYR-POOLS-AGG2', covered_by='G-HYR-POOL-N;G-HYR-POOL-S')

# ----------------------------------------------------------------------------- Tsafrir 1975
R('TSA-HYR-AQ', 'TSA75', 'p. 50', 'Hyrcania aqueduct on a rock wall across the moat', 'hyrcania', 'aqueduct',
  pt=('asi', '109/7/70'), group_id='G-HYR-AQ-AGG2', covered_by='G-HYR-NAQ;G-HYR-SAQ', period_as_given='Second Temple fort', date_code='partly')
R('TSA-HYR-STORE', 'TSA75', 'p. 50', 'Hyrcania water storage systems (c. 20,000 m3)', 'hyrcania', 'cistern',
  aggregate='yes', count='', pt=('asi', '109/7/70'), capacity_m3='c. 20000', group_id='G-HYR-CIS')
R('TSA-SIPHON', 'TSA75', 'p. 50', 'Stone siphon of the upper aqueduct at Bethlehem', 'solomons_pools', 'aqueduct',
  pt=None, group_id='G-UPPER-AQ', period_as_given='Roman', date_code='partly')
