"""Second block of literature rows: the entry 29 inventory (reused as coded) and repo notes (Siloam, Ramat Rahel).

Imported by build_water.py after literature_data.py. Same conventions.
"""
from literature_data import R, SOURCES

SOURCES['E29INV'] = ('Entry 29 regional inventory, research/assessments/entry29_jericho_pools/'
                     'regional_inventory_2026-10-06.csv and .json (sources as cited there: Netzer 1983/1989/2001, '
                     'ROSAPAT 2011, SWP 1883, Meshel & Amit 1989, Amit 1989, Netzer 2006)')
SOURCES['SIL'] = ('Repo note research/measurements/cycle15/siloam_bathing.md (citing Greenhut & Mazor, Atiqot 101 '
                  '(2020) pp. 74*-77*, 83*; Szanton, Vukosavovic & Berko 2024 pp. 27*, 33*-38*; 2014 report Fig. 3)')
SOURCES['RR'] = ('Repo note research/sites/site_identification_review.md (citing the Tel Aviv-Heidelberg Ramat Rahel '
                 'expedition 2006-2007 preliminary results, Area C1, pp. 15-18)')

PAL = ('asi', '109/5/14')

R('E29-J01', 'E29INV', 'J01; NETZER1983 pp. 100-106; NETZER1989 pp. 277-281', 'Early northern Pools Complex pool',
  'jericho_palaces', 'reservoir_pool', pt=PAL, dims='c. 18 x 13 m', shape='four_sides', north='yes', great='no',
  feed='channel', period_as_given='earlier Hasmonean separate-pool state', date_code='in', group_id='G-J01')
R('E29-J02', 'E29INV', 'J02; same sources', 'Early southern Pools Complex pool', 'jericho_palaces', 'reservoir_pool',
  pt=PAL, dims='c. 18 x 13 m', shape='four_sides', north='no', great='no', feed='channel',
  period_as_given='earlier Hasmonean separate-pool state', date_code='in', group_id='G-J02')
R('E29-J03', 'E29INV', 'J03; NETZER1989/2001; NET75 p. 92', 'Joined Herodian pool A(B)101', 'jericho_palaces',
  'reservoir_pool', pt=PAL, dims='32 x 18 m', shape='four_sides', great='unknown', entrance='yes',
  period_as_given='Herodian joining (Second Palace)', date_code='in', group_id='G-J03',
  notes='steps to the bottom of each half (NET75 p. 92); a later state of J01 + J02')
for jid, name, typ, dims, shape, per, dc in [
    ('J04', 'A(C)94', 'reservoir_pool', '8.8 x 8.2 m', 'four_sides', 'Area AC hydraulic stages', 'in_hedged'),
    ('J05', 'A(C)90', 'reservoir_pool', '8.8 x 7.7 m', 'four_sides', 'Stage 4 or 6 (Hasmonean palace stages)',
     'in_hedged'),
    ('J06', 'Small pool pair west of the central palace', 'reservoir_pool', 'c. 8 x 8.5 m each', 'four_sides',
     'Hasmonean estate pair', 'in'),
    ('J07', 'Settling tank A(B)99', 'basin_tank', '', 'unknown', 'final Hasmonean supply arrangement', 'in'),
    ('J09', 'AC44 pool', 'reservoir_pool', 'length 8.8 m (width assumed)', 'unknown', 'earlier than A(C)94',
     'in_hedged'),
    ('J10', 'Septic tank A(B)215', 'basin_tank', '2.5 x 2.4 m, 2.4 m deep', 'four_sides',
     'earlier Buried Palace drainage', 'in_hedged'),
    ('J11', 'Abu el-Alayiq north area pool (PADIS0153)', 'reservoir_pool', '', 'unknown', 'catalogue Hellenistic',
     'partly'),
    ('J17', 'Small stepped pool A(B)63', 'reservoir_pool', '1.8 x 1.4 m', 'four_sides', '', 'undated'),
    ('J25', 'AC1 distribution/settling installation', 'basin_tank', '85 x 85 cm, 75 cm deep', 'four_sides',
     'Stage 3 adaptation', 'in_hedged'),
    ('J26', 'A(C)161', 'reservoir_pool', '3.6 x 3.6 m, 3.9 m deep', 'four_sides', 'Stage 3 storage (author)',
     'in_hedged'),
    ('J27', 'A(C)150', 'reservoir_pool', '2.5 x 2.2 m', 'four_sides', '', 'undated'),
    ('J28', 'Unnamed basin near the NW corner of A(C)161', 'basin_tank', '50 x 50 cm, 70 cm deep', 'four_sides', '',
     'undated'),
]:
    R('E29-' + jid, 'E29INV', jid, name, 'jericho_palaces', typ, pt=PAL, dims=dims, shape=shape,
      period_as_given=per, date_code=dc, great='no' if typ == 'reservoir_pool' else 'unknown',
      group_id='G-J06' if jid == 'J06' else 'G-' + jid,
      feed='channel' if jid in ('J04', 'J05', 'J09', 'J25', 'J26') else 'unknown')
R('E29-J08', 'E29INV', 'J08; SWP1883 pp. 222-223; ROSAPAT2011 pp. 110-112',
  'Ain es-Sultan historical reservoir and channels', 'tell_es_sultan', 'reservoir_pool', pt=('wbadb', 'E334'),
  dims='24 x 40 feet (SWP)', shape='four_sides', feed='spring',
  notes='identity with the Roman nymphaeum / Ottoman pool unresolved')
R('E29-J12', 'E29INV', 'J12; ROSAPAT2011 p. 120; NET75 p. 93; NET01B p. 42', 'Birket Musa (PADIS0025)', 'birket_musa',
  'reservoir_pool', pt=('asi', '109/5/16'),
  dims='175 x 145 m (NET75); 150 x 180 m (NET01B); 220 x 160 m (catalogue)', shape='four_sides', great='yes',
  qelt='yes', feed='channel', period_as_given='may be Herodian (Netzer 1975)', date_code='in_hedged',
  group_id='G-J12', notes='supply from the Qelt springs (NET75 p. 93, hedged); its own site complex')
R('E29-J13', 'E29INV', 'J13; ROSAPAT2011 p. 120', 'Birket Gilgiuliyeh near Kh. en-Nitla (PADIS0157)', 'nitla',
  'reservoir_pool', pt=None, period_as_given='catalogue Byzantine', date_code='out')
R('E29-J14', 'E29INV', 'J14; ROSAPAT2011 p. 118; MESHEL_AMIT1989', 'Tell el-Aqaba/Cypros water-system aggregate',
  'cypros', 'water_system', aggregate='yes', count='', pt=('asi', '109/5/7'),
  period_as_given='late Hellenistic cisterns; Roman/Herodian pools and cisterns', date_code='in',
  group_id='G-CYP-SYSTEM', covered_by='G-CYP-HER;G-CYP-RUNOFF;G-CYP-CIS')
R('E29-J15', 'E29INV', 'J15; ROSAPAT2011 p. 126', 'Kh. el-Mafjar water-system aggregate', 'mafjar', 'water_system',
  aggregate='yes', count='', pt=('asi', '109/5/23'), period_as_given='Early Islamic palace', date_code='out')
R('E29-J16', 'E29INV', 'J16; ROSAPAT2011 p. 139', 'Tell el-Qos basin/cistern aggregate', 'tell_el_qos', 'cistern',
  aggregate='yes', count='', pt=('place', 'tell_el_qos'), plaster='yes', period_as_given='catalogue Byzantine',
  date_code='out')
R('E29-J18', 'E29INV', 'J18; ROSAPAT2011 p. 117; MESHEL_AMIT1989', 'Cypros fortress/palace water-system aggregate',
  'cypros', 'water_system', aggregate='yes', count='', pt=('asi', '109/5/7'),
  period_as_given='Hellenistic cistern/pool; Roman bathhouse', date_code='partly', group_id='G-CYP-SYSTEM',
  covered_by='G-CYP-HER;G-CYP-RUNOFF;G-CYP-CIS')
R('E29-J19', 'E29INV', 'J19; ROSAPAT2011 p. 107', "St Andrew's church area pool and cisterns (PADIS0046)",
  'jericho_town', 'reservoir_pool', aggregate='yes', count='', pt=None,
  period_as_given='catalogue Roman/Herodian heading', date_code='partly')
R('E29-J20', 'E29INV', 'J20; ROSAPAT2011 p. 122', 'Deir Mar Jariys / Deir el-Qelt cisterns (PADIS0015)', 'choziba',
  'cistern', aggregate='yes', count='', pt=('asi', '109/5/3'), qelt='yes', period_as_given='catalogue Roman',
  date_code='partly')
R('E29-J21', 'E29INV', 'J21; ROSAPAT2011 pp. 141-142', 'Quruntul-area cistern system (PADIS0149)', 'doq', 'cistern',
  aggregate='yes', count='', pt=('place', 'doq'), period_as_given='late Hellenistic/Herodian with later reuse',
  date_code='in_hedged', group_id='G-DOQ-CIS')
R('E29-J22', 'E29INV', 'J22; ROSAPAT2011 pp. 154-155', 'Suwwanet eth-Thaniya domestic cistern (PADIS0173)',
  'suwwanet', 'cistern', pt=('wbadb', 'S2228'), period_as_given='catalogue Roman', date_code='partly')
R('E29-N-DOQ10', 'E29INV', 'notice: AMIT1989_DOQ p. 227', 'Doq high filled cistern (notice 10)', 'doq', 'cistern',
  pt=('place', 'doq'), period_as_given='later/monastery context (author)', date_code='undated')
R('E29-N-DOQ11', 'E29INV', 'notice: AMIT1989_DOQ p. 224 Fig. 2', 'Doq map cistern symbol 11', 'doq', 'cistern',
  pt=('place', 'doq'))
R('E29-N-ESTATE', 'E29INV', 'notice: NETZER1983 pp. 99-101', 'Other estate and workshop water installations',
  'jericho_palaces', 'water_system', aggregate='yes', count='', pt=PAL)
for nid, name, typ, loc, pt, per in [
    ('PYRGOI', 'Pyrgoi reservoir (PADIS0037)', 'reservoir_pool', 'p. 114', None, 'Byzantine'),
    ('PENTHUCLA', 'Penthucla cisterns (PADIS0031)', 'cistern', 'p. 114', None, 'Byzantine'),
    ('BEITJABR', 'Beit Jabr reservoir (PADIS0146)', 'reservoir_pool', 'p. 119', ('asi', '109/4/20'),
     'Byzantine/Early Islamic'),
    ('HASSAN', 'Tell el-Hassan area cisterns (PADIS0140)', 'cistern', 'p. 125', None, 'Byzantine'),
    ('NITLA', 'Kh. en-Nitla reservoir (PADIS0007)', 'reservoir_pool', 'p. 135', None, 'Byzantine'),
    ('QASRYAHUD', 'Qasr el-Yehud reservoir (PADIS0034)', 'reservoir_pool', 'p. 137', ('wbadb', 'S2651'), 'Byzantine'),
    ('HAJLA', 'Qasr Hajla area cistern (PADIS0143)', 'cistern', 'p. 138', None, 'Byzantine'),
    ('MUGHEIFIR', 'Rujm el-Mugheifir reservoirs (PADIS0159/0029)', 'reservoir_pool', 'pp. 142-143', None,
     'Byzantine'),
    ('SULTANCIS', 'Tell es-Sultan area cisterns (PADIS0130)', 'cistern', 'p. 154', ('wbadb', 'E334'), 'Byzantine'),
    ('TAHUNET', 'Tahunet el-Mafjar reservoir (PADIS0162)', 'reservoir_pool', 'pp. 155-156', None,
     'Byzantine/Early Islamic'),
    ('SUKKAR', 'Tawaheen es-Sukkar cisterns (PADIS0002)', 'cistern', 'pp. 156-157', None, 'Crusader/Middle Islamic'),
    ('AELIOTES', 'Laura of Aeliotes cistern (PADIS0040)', 'cistern', 'p. 159', None, 'Byzantine'),
]:
    plural = name.split(' (')[0].endswith('s')
    R('E29-N-' + nid, 'E29INV', 'notice: ROSAPAT2011 ' + loc, name, 'jericho_oasis_other', typ,
      aggregate='yes' if plural else 'no', count='' if plural else '1', pt=pt, period_as_given=per, date_code='out',
      group_id={'BEITJABR': 'G-BEITJABR', 'QASRYAHUD': 'G-QASRYAHUD'}.get(nid, ''))

SIL = ('wbadb', 'E675')
R('SIL-BIRKET', 'SIL', 'Szanton et al. 2024 pp. 27*, 35*-38*, Figs. 5-6', 'Birket al-Hamra (larger Siloam pool)',
  'jer_siloam', 'reservoir_pool', pt=SIL, solomon='yes', label='CLAIM', dims='northern side c. 35 m (p. 38*)',
  entrance='yes', period_as_given='northern phases 3a-b: second half of 1st c. BCE / 1st c. CE (interpretive)',
  date_code='in_hedged', group_id='G-SIL-BIRKET',
  notes="the 2024 authors identify Birket with Solomon's Pool (p. 27*); a complete stepped pool is reconstructed "
        '(Fig. 6)')
R('SIL-SMALL', 'SIL', 'Greenhut & Mazor 2020 pp. 74*-77*, 83*',
  'Small plastered receiving pool beside the Siloam pool', 'jer_siloam', 'reservoir_pool', pt=SIL,
  dims='exposed 8.4 x 3 m, 3.1 m high', plaster='yes', feed='channel', great='no',
  notes='storage function (authors); fed by overflow channel L103; a floor coin of 69/70 CE gives a conditional '
        'lower bound')
R('SIL-L124', 'SIL', '2014 report, Fig. 3 (as summarised)', 'Pool L124 (six steps)', 'jer_siloam', 'reservoir_pool',
  pt=SIL, dims='3 x 2.5 m, c. 2.5 m deep', shape='four_sides', entrance='yes', great='no')
R('SIL-L119', 'SIL', '2014 report, Fig. 3 (as summarised)', 'Tower reservoir L119 (seven steps)', 'jer_siloam',
  'reservoir_pool', pt=SIL, entrance='yes')
R('SIL-L103', 'SIL', 'Greenhut & Mazor 2020 p. 76*', 'Overflow channel L103 from the main pool', 'jer_siloam',
  'aqueduct', pt=SIL, dims='2.2 x 0.65 m, 2.3 m deep', notes='later insertion inferred by the authors')
R('RR-POOLS', 'RR', 'Area C1, pp. 15-18', 'Ramat Rahel pool enclosure', 'ramat_rahel', 'reservoir_pool',
  aggregate='yes', count='', pt=('asi', '106/95'),
  notes='beneath fill with pottery as late as the 2nd c. BCE; the note gives no construction date')
