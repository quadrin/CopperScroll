import json, csv
from collections import OrderedDict

BASE = '/tmp/claude-0/-home-claude/0f9a6161-d5c4-59af-bf88-0604e304aaaf/scratchpad/tests/hoard'
OUT = BASE + '/compiled/hoards.csv'
rows = json.load(open(BASE + '/raw/rows_auto.json'), object_pairs_hook=OrderedDict)
by = {r['chre_id']: r for r in rows}

LEO99a = ('R.D. Leonard Jr., message "Re: orion-list Essenes, Zias article, etc.", Orion list, 9 Dec 1999, '
          'https://orion.huji.ac.il/orion/archives/1999b/msg00557.html')
LEO99b = ('R.D. Leonard Jr., message "Re: orion-list Essenes, Zias article, etc. - Correction", Orion list, 10 Dec 1999, '
          'https://orion.huji.ac.il/orion/archives/1999b/msg00564.html')
LEO99c = ('R.D. Leonard Jr., Orion list message (reply to S. Goranson), Dec 1999, '
          'https://orion.huji.ac.il/orion/archives/1999b/msg00642.html')
NS23 = ('Y. Abadi-Reiss, G. Bijovsky, S. Amorai-Stark, N. Sukenik, S. Israeli and E. Aladjem 2023, "A Treasure from Nahal Shalva: '
        'Exquisite Jewelry and a Coin Hoard from the Days of the Bar Kokhba Revolt", Atiqot 112, pp. 117-156 (pagination read from the PDF), '
        'DOI https://doi.org/10.70967/2948-040X.1046 (read from owner\'s Drive copy, file 1lhbF9iM4tQLwFRk7OHqt9QPDO2SuzJhh)')

def add(i, **kw):
    r = by[i]
    for k, v in kw.items():
        if k in ('confidence', 'sources_add'):
            key = 'confidence' if k == 'confidence' else 'sources'
            r[key] = (r[key] + ' || ' if r[key] else '') + v
        else:
            r[k] = v

# ---- overrides and conflict notes (all figures quoted from the pages opened) ----
add('7657',
    printed_total_weight_g='"62.47 kg, 2.933 talents" (as printed; Leonard\'s own estimate, not a measured weight)',
    printed_weight_source=LEO99b + ' (corrects his 9 Dec post, which had given Isfiya as 7.8 kg)',
    confidence='Counts differ: CHRE summary says 3,850 Tyrian tetradrachms + 110 drachms + 275 Roman denarii; CHRE total (4,560) and coin table follow Kadman 1962 as quoted on the CHRE page: 3,400 sheqels + 1,000 half-sheqels + 160 denarii of Augustus (Lugdunum); Kadman 1960 via Meir 2008:117 (quoted on CHRE): "about 4,500 ancient silver coins"; Waner & Safrai 2001 no. 132 (quoted on CHRE): "AR 6000". Not reconciled here. Dispersal per CHRE: IAA 737 coins; Kadman Numismatic Pavilion 304; Kibbutz Hanita 64; Hecht Museum 81. Meir publishes the Kadman holdings in INR 3 (2008):117-123, 4 (2009):63-71, 5 (2010):143-149 ("the remaining 69 Tyrian sheqels of regular style"), 7 (2012):25-30, 8 (2013):31-37 ("59 Tyrian half sheqels"), 9 (2014):103-107 (abstracts read on lockwoodonlinejournals.com).')
for q in ('7692', '18786', '18785'):
    add(q, confidence='Three pots from Locus 120 at Kh. Qumran (CHRE A 223 + B 185 + C 153 = 561). Leonard (Orion, Dec 1999, msg00642) describes "561 silver coins in three pots (nearly all shekels of Tyre)", latest coin "dated 118 of the era of Tyre (= 9/8 B.C.E.)", with Seyrig suggesting deposit as late as 1 BCE/1 CE. CHRE (citing Butcher 2004:217 no. 15a): "3 hoards found in the Qumran excavations, subsequently mixed together"; Lonnqvist 2007 catalogue (via CHRE) not separated by hoard. Pot-level counts therefore rest on CHRE.',
        sources_add=LEO99c)
add('7692', printed_total_weight_g='"7.8 kg, 0.366 talents" (as printed) for the Qumran hoard as a whole, all three pots; Leonard\'s own estimate',
    printed_weight_source=LEO99b + '; the same figure was first attached to Isfiya in ' + LEO99a)
add('7617',
    contents='(article, Table 1 p. 127) aurei [AV] 4 (Nero 2, Nerva 1, Trajan 1); denarii [AR] 61; tetradrachms [AR] 41; tridrachms [AR] 18; drachms [AR] 12; total 136. (CHRE coin table: aurei 4; denarii 61; tetradrachms Antioch 27 + Tyre 14; tridrachms Bostra 17 + Antioch 1; drachms Bostra 12)',
    year_found='2012 (May; salvage excavation)',
    context='Excavation (salvage, May 2012). Round pit L127 in Structure 2 (1.5 m wide, 1.5 m deep; p. 118) with a female skeleton; "eight lumps of silver coins" in front of the skeleton with linen textile remains; coins "wrapped in at least two pieces of cloth (perhaps two purses)" (pp. 118, 126). [article wording]',
    other_precious_objects='gold finger ring set with a gemstone intaglio (Hygieia) and a gold earring plus fragment of its pair (p. 118, Fig. 7); silver cosmetic tools: two spatulas and a kohl stick (p. 118); iron gladius (not precious). Three further silver coins found together in L127 "might have been part of the hoard" (p. 127)',
    confidence='Count differs inside the article: text p. 126 "140 gold and silver coins" vs. Table 1 / discussion "136 coins that comprise the hoard" (p. 127); IAA press release quoted by CHRE: "some 140 gold and silver coins". CHRE total 136. Closing: 10 Hadrian denarii COS II-III (118-119 CE and later) "predate the Bar Kokhba Revolt" (p. 135ff).',
    sources_add=NS23)
add('7726', confidence='Syon & Tepper 2021, "A Hoard of Syrian Tetradrachms from a Mass Burial in Akko-Ptolemais", INR 16:125-141 (abstract read at https://lockwoodonlinejournals.com/index.php/inr/article/view/2826): "Forty-six silver tetradrachms, 44 of them forming a hoard", terminus post quem 119 CE. CHRE: 46, with note "two of the coins may have been unrelated", terminal year 118. Abadi-Reiss et al. 2023 n. 11 p. 131 also "44 tetradrachmas".')
add('7733', confidence='CHRE 77 silver (denarii 29, tetradrachms 31, drachms 14, tridrachms 3). Abadi-Reiss et al. 2023 n. 12 p. 131: "The Amazya hoard includes 78 silver coins: 30 denarii, 31 Syrian tetradrachmas, three tridrachmas and 14 drachmas (Bijovsky, in prep.)".', sources_add=NS23)
add('7722', confidence='CHRE: 26 bronze + 3 silver (1 denarius, 2 drachms). Abadi-Reiss et al. 2023 n. 12 p. 131: "The Petora hoard consists of 29 coins, only three of which are silver: one denarius of Vespasian and three drachmas of Trajan (unpublished)" (the printed items add to 4). Unpublished hoard.', sources_add=NS23)
add('7596', confidence='CHRE coin table: 5 aurei, 8 denarii, 5 tetradrachms, 2 Bar Kokhba zuzim (shekel-type entries), 4 AE of Ascalon = 24; CHRE summary 5 AV + 15 AR + 4 AE. Zissu & Hendin 2012:222 as quoted on the CHRE page: "five gold aureii, 25 Roman denarii, five Roman provincial tetradrachms, two Bar Kokhba zuzim, and four bronze coins" (=41), value 150 zuzim. Aurei: Tiberius, Nero x2, Vitellius, Vespasian (Abadi-Reiss et al. 2023 p. 131, citing Zissu et al. 2009-2010:139-140).')
add('7594', other_precious_objects='fragment of silver jewellery (A85) (Zissu et al. 2011:268-9, quoted on CHRE; CHRE lists "Earring, silver fragment")',
    confidence='83 silver coins "restruck by the Bar Kokhba administration" (Zissu et al. 2011, quoted by CHRE); CHRE coin table splits 53 denarii-size, 20 tetradrachms, 10 shekel-type.')
add('7595', confidence='CHRE: 9 silver + 1 Hasmonean prutah; Zissu & Hendin 2012 (quoted on CHRE): 2 Bar Kokhba zuzim, 1 provincial tridrachm, 5 denarii or drachms, 1 Jewish War shekel, 1 prutah.')
add('7605', confidence='CHRE (Spijkerman 1961): 10 revolt shekels + 4 half-shekels + 1 Tyrian shekel (52/3 CE) + 1 Antiochene tetradrachm = 16; Meshorer 1989:75 as quoted on CHRE: "9 Jewish shekels, 4 Tyrian shekels and 1 provincial tetradrachm of Nero", "found in a clay lamp". Latest coin a Year 5 shekel (70 CE).')
add('7541', confidence='CHRE: "160(?)"; 64 Jewish shekels and 25 non-Jewish coins were deposited by dealers and published by Hill 1938. Kadman 1967 no. 27 (via CHRE): "Year: 1936, Number: 185 AR". Meshorer 1989:75 (via CHRE): "Found in 1935 including some 300 shekels". The CHRE coin table also lists 71 bronze coins of uncertain mint, which are not explained on the page. Silver count here = the 89 recorded silver coins.')
add('7690', confidence='CHRE 227 (purchased in Jerusalem 1952, said to be from Wadi Murabbaat); Waner & Safrai 2001 no. 18 (via CHRE): "213 AR, AD 20-132".')
add('7592', confidence='CHRE 27 (20 Tyrian shekels + 7 Nero tetradrachms); Waner & Safrai 2001 no. 144 (via CHRE) and CHRE comment: "36 AR". Found with sherds of a small juglet on a street (Syon 1993:44 via CHRE).')
add('7818', confidence='CHRE 16 denarii (a tridrachm from the same cave "does not belong to the hoard"); Waner & Safrai 2001 no. 66 (via CHRE): "17 AR".')
add('8000', confidence='CHRE: at least 12 (9 Tyrian + 3 revolt shekels acquired by Reifenberg, in a bronze pyxis); Meshorer 1989:75 (via CHRE): the pyxis "contained more than the 3 Jewish and 9 Tyrian ones"; Leonard 2000:685 (via CHRE): "About 30 Tyrian shekels and 3+ some revolt shekels".')
add('8168', confidence='Known part 15 silver (CHRE); "originally contained some thirty shekels" (Meshorer 1985:43 via CHRE). CHRE total 30.')
add('8091', window='B', window_note='window set by the Second Revolt coins named in CHRE summary (latest coins 132-136 CE); CHRE terminal range 66-136',
    confidence='"120-500 silver coins of the First and Second Jewish Revolts" (CHRE); Kadman 1963 (via CHRE) gives 1886 and "300(?) AR" of the First Revolt. Count used: 120 (CHRE minimum).')
add('8501', confidence='Mildenberg 1984:57 (via CHRE): "About 500 tetradrachms, at least 2,000 denarii"; around 100 tetradrachms and 500 denarii were registered; Waner & Safrai 2001 no. 96: "AR 2600".')
add('8499', confidence='Mildenberg 1984:56 (via CHRE): "About 200 Bar Kokhba tetradrachms and 1,000 denarii. No foreign coins, no bronzes"; said to have been in a hollowed stone "safe" in one of three adjoining caves.')
add('8189', confidence='Mildenberg 1984:56 (via CHRE): at least 100 Bar Kokhba silver + some bronzes, 1 aureus of Vespasian, about 100 denarii Vespasian-Trajan, 30 Hadrianic denarii, 150 Syrian tetradrachms...; Waner & Safrai 2001 no. 89: "250 AE+AR+AV". CHRE total 385.')
add('8464', confidence='"About 100 tetradrachms and denarii together with a few dozen Roman coins" (Mildenberg 1984:55 via CHRE); Waner & Safrai 2001 no. 82: "AE+AR 150". Count used: 100.')
add('8079', confidence='"approximately 46 tetradrachms and 200-350 denarii" (CHRE); CHRE total 396 uses the upper figure. Rival provenance accounts (Hebron cistern vs Dura/Dahariyeh, Bittir) discussed by Mason & Visona 2014, INR 9:163-172 (abstract read: hoard "said to have been found at Hebron in 1889").')
add('8134', confidence='"Possibly two hoards"; Mildenberg 1984:55 (via CHRE): "Kadman\'s figures could not be checked."')
add('8466', confidence='Silver present but number not given: "Allegedly Bar Kokhba silver and bronze together with Syrian tetradrachms and Roman denarii" (Mildenberg 1984:56 via CHRE); CHRE codes all 25 as bronze. Precious-metal count unknown.')
add('8466', total_precious_coins='unknown (silver present)', silver_coins='unknown')
add('9016', confidence='CHRE: 20 tetradrachms, 60 denarii, some Bar Kokhba bronzes, some Roman denarii and Arabian drachms; 20 further coins coded "bronze or silver". Precious total given = 80 (certain silver only).')
add('8082', other_precious_objects='"a gold seal with a gem" / engraved gem-seal (CHRE comment)', confidence='"approximately 100" shekels, Years 1-4 (CHRE); earthen pot with lead seal.')
add('7698', window='A', window_note='CHRE terminal years 72-73 reflect the end of Masada; latest coin is a Year 5 shekel (70 CE) per CHRE summary "Years 2-5"',
    other_precious_objects='two silver flans; a Tyrian shekel and half-shekel deliberately defaced, "apparently used as ingots" (Meshorer 1989:76 via CHRE)',
    confidence='CHRE data type "Group of single finds": a "scattered hoard" on the floor of Casemate 1039 (Meshorer 1989:74-75 via CHRE).')
add('8167', window_note='terminal range 70-73 reflects the end of Masada; window set by latest coin (revolt shekels)')
add('7697', confidence='"All the coins were found stuck together, with clear traces of the cloth bag" (Meshorer 1989:73 via CHRE); under floor of Building IX, L336.')
add('9012', confidence='39 aurei, 38 documented (CHRE); found by a diver 100 m offshore; publication per CHRE: Kindler 1969 (Hebrew).')
add('8173', confidence='"144 silver and two gold coins ... buried in a clay juglet" resting on bedrock, Building V, L2055 (Bijovsky 2004:243, 246-248, 279-290 via CHRE); aurei of Vespasian and Trajan (Abadi-Reiss et al. 2023 p. 131).')
add('8172', confidence='Mainly a bronze hoard ("Group B, The Bronze Hoard", Bijovsky 2004); one tetradrachm.')
add('8101', confidence='Sotheby 26 Mar 1888 lots 170-190, "recently found near Tyre"; Noe lists 38 Antioch tetradrachms Augustus-Vespasian, but the Sotheby catalogue also lists a coin of Philip, so the closing date is doubtful (CHRE). CHRE data type "Hoard?".')
add('7603', confidence='CHRE summary says 3 tetradrachms + 3 bronze (6) but CHRE total 7 and coin table 4 tetradrachms + 3 AE. Found in a kokh of a burial cave (Kloner 2000:79 via CHRE). CHRE data type "Group of single finds".')
add('8177', confidence='Two denarii of Hadrian and one bronze coin found in a skull (Barag 1980:31 no. 14 via CHRE). CHRE data type "Group of single finds".')
add('20984', confidence='Description on file at the British Museum (letter from A. Spaer), per CHRE; no other check.')
add('8033', confidence='CHRE cites IGCH 1626 (Svoronos 1824-26 Cleopatra VII tetradrachms; information from A. Spaer). Not to be confused with IGCH 1617 (also "Palestine 1942", Spaer), entered separately below.')
add('7604', confidence='"at least 20 denarii" and "a large number of bronze coins" (No Author 1962:57 via CHRE).')
add('20035', confidence='Seen on the Paris market (CGB) 1996, Prieur database (CHRE); "Cisjordania" = West Bank, exact findspot unknown.')

for i in ('20035', '20983'):
    by[i]['coord_basis'] = 'no coordinates; findspot given only as "West Bank"/"Cisjordania"'
by['20990']['lat'], by['20990']['lon'] = '31.53', '35.10'
by['20990']['coord_basis'] = 'approximate, my placement at Hebron town for the published "Hebron district" (no coordinates in CHRE)'

# ---- rows not in CHRE ----
def new(**kw):
    base = OrderedDict((k, '') for k in rows[0].keys())
    base.update(kw)
    rows.append(base)

IG = 'record read at https://coinhoards.org/id/igch{n} (ANS CoinHoards, IGCH data), 2026-10-23'
new(id='igch1616', name_as_published='Ascalon, Judaea (IGCH 1616)', chre_id='', hoard_status='IGCH hoard',
    lat='31.66', lon='34.55', coord_basis='approximate, my placement at Ascalon/Ashqelon (findspot published only as "Ascalon")',
    year_found='1927', context='not stated', closing_date='IGCH deposit "62 B.C.-1 B.C."; latest coins Ascalon tetradrachms coded 73-63 BCE', window='A',
    window_note='borderline: latest coin type range ends at 63 BCE', contents='c. 24 AR: tetradrachms of Tyre (Antiochus VII type) 1 + 1; tetradrachms of Ascalon 6; further silver 16',
    total_precious_coins='24', silver_coins='24', gold_coins='0', base_metal_or_unrecorded_coins='0', chre_total_coins='',
    sources='IGCH 1616 (M. Thompson, O. Morkholm, C.M. Kraay, An Inventory of Greek Coin Hoards, New York 1973), ' + IG.format(n=1616) + '; note "Information from E.S.G. Robinson"',
    confidence='"c. 24"', leonard2000_cited_in_chre='')
new(id='igch1617', name_as_published='Palestine (IGCH 1617), found 1942', chre_id='', hoard_status='IGCH hoard',
    lat='', lon='', coord_basis='no coordinates; findspot "Palestine"', year_found='1942', context='not stated',
    closing_date='IGCH deposit "61 B.C.-1 B.C."; latest coins Tyre tetradrachms coded 81-62 BCE', window='A',
    window_note='borderline: latest coin type range ends 62 BCE', contents='30+ AR: Antiochus VII tetradrachms of Tyre 1+; Demetrius II tetradrachms of Tyre 4+; Tyre tetradrachms 10; at least 15 more tetradrachms of Antiochus VII and Demetrius II from Tyre',
    total_precious_coins='30', silver_coins='30', gold_coins='0', base_metal_or_unrecorded_coins='0',
    sources='IGCH 1617, ' + IG.format(n=1617) + '; refs Kadman, INCJ hoard 14; disposition A. Spaer, Jerusalem',
    confidence='"30+"; possible confusion with CHRE 8033 (also "Palestine 1942", Spaer) but contents differ (Tyrian vs Ptolemaic)')
new(id='igch1622', name_as_published='Safad (anc. Seph), Galilee (IGCH 1622)', chre_id='', hoard_status='IGCH hoard',
    lat='32.96', lon='35.50', coord_basis='approximate, my placement at Safed town', year_found='1877', context='not stated',
    closing_date='IGCH deposit "49 B.C.-1 B.C."; coins coded Ascalon tetradrachms 100-49 BCE', window='A',
    window_note='window from IGCH deposit date; coin date range in the data begins before 63 BCE', contents='6+ AR tetradrachms of Ascalon',
    total_precious_coins='6', silver_coins='6', gold_coins='0', base_metal_or_unrecorded_coins='0',
    sources='IGCH 1622, ' + IG.format(n=1622) + '; refs de Saulcy, RN 1874-7, pp. 126-7; Feuardent, RN 1874-7, pp. 192-3; Kadman, INCJ hoard 8',
    confidence='"6+"')
new(id='igch1627', name_as_published='Gaza region, Judaea (IGCH 1627)', chre_id='', hoard_status='IGCH hoard',
    lat='31.50', lon='34.47', coord_basis='approximate, my placement at Gaza (findspot published as "Gaza region")', year_found='1940', context='not stated',
    closing_date='IGCH deposit "50 B.C.-30 B.C."; coins coded Ascalon tetradrachms 83-63 BCE', window='A',
    window_note='window from IGCH deposit date', contents='c. 400 AR tetradrachms of Ascalon',
    total_precious_coins='400', silver_coins='400', gold_coins='0', base_metal_or_unrecorded_coins='0',
    sources='IGCH 1627, ' + IG.format(n=1627) + '; information from A. Spaer; disposition A. Spaer 6, private coll. Jerusalem 6, private coll. Tel Aviv 20',
    confidence='"c. 400"')
ETH = ('B. Zissu and A. Ganor 2009, "Horvat Ethri - A Jewish Village from the Second Temple Period and the Bar Kokhba Revolt in the Judean Foothills", '
       'Journal of Jewish Studies 60/1, p. 99 n. 39 and p. 100 (read from owner\'s Drive copy, file 1F4upDpItQQhMwo6np_JwthNdySV7tOlE)')
for sfx, nm, cont, n, cls, note in (
        ('a', 'Horvat Ethri, outer stones of the westernmost corner of the village', 'denarii [AR] 2 (Vespasian, dated 71 CE; Hadrian 119-138)', 2, '119-138 CE (Hadrian)', 'latest coin (Hadrian 119-138) may postdate 136 CE'),
        ('b', 'Horvat Ethri, outer stones at the easternmost edge of the site', 'denarii [AR] 3 (one undated Bar Kokhba denarius; Vespasian 72/3 CE; Trajan 101/2 CE)', 3, '132-135 CE (Bar Kokhba denarius)', ''),
        ('c', 'Horvat Ethri, mass burial in ritual bath XI (L4142)', 'tetradrachm [AR] 1 (Vespasian, Antioch, 69/70 or 70/71 CE) + drachm [AR] 1 (Bostra, Trajan, 111 CE), "bonded together"', 2, '111 CE', 'pair of coins in a destruction/burial deposit; not called a hoard by the authors')):
    new(id='ethri_' + sfx, name_as_published=nm, chre_id='', hoard_status='small concealed group ("Five silver denarii concealed during the Bar Kokhba Revolt", n. 39)' if sfx != 'c' else 'borderline: two coins bonded together',
        lat='31.65', lon='34.97', coord_basis='approximate, converted by me from the published Old Israel Grid 14740/11745 (n. 1); +/- c. 0.5 km',
        year_found='excavations of the 1990s (dates not given on these pages)', context='Excavation. ' + nm.split(', ', 1)[1],
        closing_date=cls, window='B', window_note=note, contents=cont, total_precious_coins=str(n), silver_coins=str(n), gold_coins='0',
        base_metal_or_unrecorded_coins='0', sources=ETH, confidence='The two outer-stone groups (a, b) are described together as five concealed denarii; whether they are one or two deposits is my reading of the footnote.')
new(id='ashun_b', name_as_published='Horbat Ashun, Hoard B', chre_id='', hoard_status='hoard (as published)', lat='', lon='',
    coord_basis='location not given in the abstract (site in Israel; not checked against the box)', year_found='not stated in abstract',
    context='Excavation (rural settlement, Early Hellenistic to Late Roman)', closing_date='59/60-138 CE (range of the coins, abstract)', window='B',
    window_note='latest coin may postdate 136 CE', contents='"eight silver and bronze coins" (split not given in the abstract)',
    total_precious_coins='', silver_coins='unknown (of 8)', gold_coins='0', base_metal_or_unrecorded_coins='',
    sources='A.S. Tendler and S. Krispin 2025, "Three Coin Hoards from Horbat Ashun and Their Archaeological and Historical Context", INR 20:67-84 (abstract only, https://lockwoodonlinejournals.com/index.php/inr/article/view/3101; full text paywalled)',
    confidence='silver/bronze split and findspot unverified (abstract only)')
new(id='vespasian_coins_cave', name_as_published='Vespasian Coins Cave (U2-007), Judean Desert fault escarpment c. 2 km S of the Nahal Qidron outlet',
    chre_id='', hoard_status='borderline: two tetradrachms on the rock step below the cave; the 7 prutot hidden in a rock crack (bronze) are the concealed group',
    lat='', lon='', coord_basis='no coordinates published; c. 2 km south of the outlet of Nahal Qidron at the Dead Sea, 265 m bsl (p. 168)',
    year_found='2020 (December excavation; survey before)', context='Excavation of a refuge cave. Silver: L110 B3-B4, "two adjacent to the cliff wall" on the rock step at the foot of the cave (p. 172). Bronze: seven prutot "hidden in a crack in the rock, c. 1 m north of its opening" (L108).',
    closing_date='69/70 CE (Vespasian year 2, Antioch)', window='A', window_note='', contents='tetradrachms of Vespasian, Antioch [AR] 2 (years 1 and 2); (in the cave also 10 First Revolt prutot [AE])',
    total_precious_coins='2', silver_coins='2', gold_coins='0', base_metal_or_unrecorded_coins='10',
    printed_total_weight_g='no total printed; individual weights printed 13.87 g and 14.27 g (p. 175, cat. 11-12)',
    sources='O. Amichay, E. Klein, H. Hamer and C. Cohen 2023, "The Vespasian Coins Cave: A Refuge Cave from the Time of the First Jewish Revolt", in O. Sion, J. Uziel, A. Ganor and E. Klein (eds), New Studies in the Archaeology of the Judean Desert: Collected Papers, Jerusalem: IAA, pp. 168-182 (pages read); https://www.jstor.org/stable/jj.10329820.10 (read from owner\'s Drive copy, file 1Zj8bxzOzOWqoYXl-4EvyeUJn0GZZQCnW)',
    confidence='The authors call the two tetradrachms "lone" coins associated with the same activity; included only as a possible small group.')

# order: window then latest-first by id
cols = list(rows[0].keys())
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(len(rows), cols)
