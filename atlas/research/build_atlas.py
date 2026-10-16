import csv, json
from pathlib import Path

root=Path(__file__).resolve().parent
def rows(name):
    return list(csv.DictReader((root/name).open(encoding='utf-8-sig',newline='')))

# Short factual paraphrases; these are not quotations or a new critical edition.
records='''1|Valley of Achor|עמק עכור|A ruin and a flight of steps in the Valley of Achor.
2|The monument|נפש|A monument and a course of masonry.
3|The great courtyard|חצר|A cistern, a courtyard and a colonnaded space.
4|The mound of Kohlit|כחלת|A mound, a water conduit and a rock cleft or bath of immersion at Kohlit.
5|The winding stair|מסבה|A winding stair of Manos, a place or person not otherwise known.
6|The Millo cistern|מלה|A cistern and steps at a place interpreted as the Millo or an esplanade.
7|House of Tribute|בית המדה|A cave and a stone course at the old House of Tribute, as Puech reads it.
8|The courtyard cistern|חצר|An underground chamber or tower in a courtyard, with a cistern in it.
9|The eastern gate|השער המזרחי|A cistern with a channel opposite the eastern gate.
10|The eastern wall|חומה|A cistern beneath a wall, beside a rock spur and threshold.
11|Kohlit's pool|כחלת|A corner of a pool associated with Kohlit.
12|The courtyard corner|חצר|A corner within a courtyard.
12a|The adjoining corner|פנה|Another corner, separated as entry 12a in this numbering.
13|The Millo pit|מלה|A pit at a corner or entrance of the Millo or esplanade.
14|The Millo tomb|מלה|A tomb and a slab or cover associated with the Millo.
15|Kohlit's great cistern|כחלת|A cistern and a pillar at Kohlit.
16|The entering conduit|אמא|A conduit and a pool approached on entering; the location needs restoration.
17|Achor's two features|עמק עכור|Two features in Achor, read as cavities, tamarisks or buildings by different editors.
18|Asla|העצלא|An earth pit in the area called Asla.
19|The Kohlit pit|כחלת|A pit associated with Kohlit.
20|Valley of Sekakah|סככא|A cairn or dam in the valley of Sekakah.
21|Sekakah|סככא|The head of a water conduit associated with Sekakah; the link and stone landmark are partly restored.
22|Solomon's reservoir|שלומו|A fissure in Sekakah east of a reservoir associated with Solomon.
23|Solomon or Shallum’s channel|שלומו|A trench or channel associated with Solomon or Shallum, directed toward a large landmark read as a boulder or mound.
24|The Kippa ravine|נחל הכפא|A tomb in the Kippa ravine, on the approach from Jericho toward Sekakah.
25|Cave of the Column|מערה|A cave entrance distinguished by a column.
26|The facing cave|מערה|A cave, its entrance and an adjacent mound or clod.
27|The queen's building|המלכא|A building associated with a queen, read as a tomb or as a dwelling.
28|The high priest's ford|מגזת|A cairn at a crossing associated with the high priest.
29|The collected waters|קיבוץ|A conduit, a reservoir and a collection of water; Jericho appears in a restoration.
30|House of Haqqoz|בית הקוץ|A cave next to the cool room of a house associated with Haqqoz.
31|Doq|דוק|A corner at Doq, read as a fortress or as a drying floor.
32|Koziba|כוזבא|A water outlet and a retaining wall at Koziba.
33|Ahiyah's treasury|אחיה|A conduit, a treasury and a road; the personal name is disputed.
34|The inscribed stone|כתב חרת|A valley marked by an inscribed stone.
35|Kidron|קדרון|A cairn at the mouth of the Kidron gorge.
36|Valley of Shaveh|השוא|Fallow land and an underground chamber in Shaveh.
37|Shaveh's irrigated land|השוא|Irrigated land and a chamber or stone marker in Shaveh.
38|Netophah|הנטף|A spring associated with a dovecote or cave opening.
39|The terrace|חבלה|An underground chamber facing east in the second terrace; Milik reads a place name instead of the terrace.
40|Horon or the Horites|החורין|Burial chambers facing the Sea (west) or south, and a channel; the name and the direction have competing readings.
41|The damaged entry|קומעה|A very short, uncertain expression. No candidate has a defensible map location.
42|The sounding conduit|ביב|A conduit and the sound of water; one reading supplies the name Kephar Nebo.
43|Beth Tamar|בית תמר|A pit, exposed rock and a place read as Beth Tamar.
44|The fort's upper room|מצד|A fort, an upper room and a dovecote.
45|The ravine cistern|בור|A cistern and channels in a ravine.
46|Beth ha-Kerem|בית הכרם|A large reservoir at Beth ha-Kerem.
47|The spring basin|מעין|A spring, basin and chamber in a valley whose name is disputed.
48|Absalom's monument|יד אבשלום|A freestanding monument associated with Absalom.
49|Siloam?|שלוח|A water installation and a trough; the reading that names Siloam is disputed.
50|Zadok's court|צדוק|The four corners of a court associated with Zadok (Puech), an inner court (Lefkovits) or a pool (the Text tab).
51|Zadok's tomb setting|צדוק|A tomb with a vestibule and pillar, associated with Zadok's surroundings.
52|The rock opposite Zadok|צדוק|A west-facing rock opposite Zadok's court or garden.
53|The gallery tomb|סבין|A tomb associated with galleries.
54|The Jericho people's tomb|ירחו|A tomb associated with people from Jericho.
55|House of the two pools|בית אשוחין|A double reservoir with a smaller basin; Bethesda depends on an editorial identification.
56|The burial chamber|בית המשכב|A burial complex with recesses, a cave, entrance stones and a platform.
57|Mount Gerizim|הר גריזין|A step and an upper pit on Mount Gerizim.
58|Beth Sham|בית שם|The mouth of a spring at a place usually compared with Beth Shean.
59|Bezek?|הבזך|A great conduit; the Bezek reading competes with other readings.
60|The final Kohlit entry|כחלת|A pit, tomb and opening associated with Kohlit; Lefkovits also reads Janoah.'''
descriptions={r.split('|')[0]:r.split('|')[1:] for r in records.splitlines()}
places={}
for r in rows('phase3_places.csv'):
    places[r['place_id']]={'id':r['place_id'],'name':r['name'],'lat':float(r['lat']) if r['lat'] else None,'lon':float(r['lon']) if r['lon'] else None,'precision':r['precision'],'kind':r['kind'],'region':r['map_group'],'note':r['note'],'source':r['coord_source']}
short_names={'kh_qumran':'Khirbet Qumran','wadi_qumran':'Wadi Qumran','doq':'Jebel Qarantal / Doq','choziba':'Choziba · Wadi Qelt','jer_siloam':'Silwan pool & tunnel outlet','jer_bethesda':'Bethesda · St Anne’s','ramat_rahel':'Ramat Rahel','gerizim':'Mount Gerizim','beth_shean':'Beth Shean / Scythopolis','nuweimeh':'Wadi Nuweimeh','ain_duk':'Ain Duk springs','tell_es_sultan':'Tell es-Sultan','jericho_area':'Jericho oasis','jericho_palaces':'Jericho royal palaces','hyrcania':'Hyrcania / Khirbet el-Mird','mar_saba':'Kidron gorge · Mar Saba','natuf':'Ain en-Natuf · Khareitun','ibziq':'Khirbet Ibziq','buqeia':'Buqeia plateau','jer_east_gate':'Eastern gate & wall','jer_kidron_mon':'Kidron monuments','jer_kidron_east':'Silwan necropolis','jer_temple':'Temple enclosure','jer_se_corner':'Southeastern Temple slope','jer_south_wall':'Southern Temple wall','jer_baqa':'Baqa plain','jer_shaveh':'Shaveh / King’s Valley','jer_bir_ayyub':'Bir Ayyub / En-Rogel','jer_tyropoeon':'Tyropoeon valley','jer_tombs_kings':'Tombs of the Kings','jer_gethsemane':'Gethsemane','tell_el_ful':'Tell el-Ful','asla':'Asla area','kuteif':'Wadi Kuteif','jordan_ford':'Lower Jordan crossing','tekoa_herodium':'Tekoa–Herodium sector','tell_el_qos':'Tell el-Qos'}
for k,p in places.items(): p['shortName']=short_names[k]
# Revisions after Phase 3 (the Phase 3 tables keep their original assessment).
# 29 September 2026: entry40_bethhoron_review.md adds Beth-Horon as a possible place for entry 40.
places['beth_horon']={'id':'beth_horon','name':'Upper Beth-Horon (Beit ʿUr el-Foqa)','lat':31.88530,'lon':35.11341,'precision':'~300 m','kind':'point','region':'region','note':'Village anchor from the IAA Benjamin survey (sites 28/143). Lower Beth-Horon (Beit ʿUr et-Taḥta) is equally compatible and has the only tomb with pottery of the period. Not a feature location.','source':'IAA survey, Ramallah–Benjamin map 83/1, sites 28 and 143','shortName':'Upper Beth-Horon · Beit Ur'}
revised_candidates={'40':[{'placeId':'beth_horon','status':'possible','confidence':'low'}],'59':[{'placeId':'kh_salhab','status':'possible','confidence':'low'}]}
# 29 September 2026: source_leads_2026-09-29.md (Zertal 2008, Manasseh Hill Country Survey Vol. 2) lowered
# Kh. Ibziq for entry 59 from medium to low. Later the same day, entry59_bezek_review.md read HA 40 (1971) p. 22:
# a kokhim tomb of the 1st-2nd centuries CE at Kh. Ibziq. That restores the period evidence, so Ibziq is medium again,
# as in the Phase 5 index. Kh. Salhab (Zertal site 23), Zertal's biblical Bezeq, is added at low.
revised_confidence={}
revised_candidate_confidence={}
# The Phase 5 index lists Zertal among the main sources, so no source is added here.
# 29 September 2026, second run (source_extractions_2026-09-29.md): Magen's NEAEHL entry (57), Garbrecht & Peleg 1994 (31; 16, 29, 35),
# HA 40 and the Salhab search (59), Jeremias and DJD III (40). Evidence texts updated; no confidence changes.
# 29 September 2026, third run (registration/extractions_run3/): JSP 19 adds a Hasmonean garrison on Gerizim into the 70s BCE (57).
places['ibziq']['note']='Upper Kh. Ibziq, Zertal site 44 (Old Israel Grid 1878/1971). Lower Kh. Ibziq, site 42, lies 1 km north-east. Zertal reports cisterns, burial caves and a Roman road, but no conduit. A kokhim tomb of the 1st–2nd centuries CE was excavated at Kh. Ibziq in 1971 (HA 40 p. 22). Not a feature location.'
places['kh_salhab']={'id':'kh_salhab','name':'Kh. Salhab (Kh. es-Selhab)','lat':32.35504,'lon':35.37277,'precision':'~300 m','kind':'point','region':'region','note':'Tell 3 km WSW of Upper Kh. Ibziq on the Neapolis–Scythopolis road. Zertal identifies it as biblical Bezeq (1 Sam 11:8) and holds that the name later moved to Ibziq. Early Roman pottery 15%; no conduit reported. Not a feature location.','source':'Zertal 2008, Manasseh Hill Country Survey 2, site 23 (Israel grid 1853/1957), converted to WGS84 from EPSG:28193 with pyproj; the same conversion puts Upper Ibziq about 230 m from its atlas anchor','shortName':'Kh. Salhab'}
# 12 October 2026: existing IV/17 assessment carried into the atlas, without inventing a mouth coordinate.
places['abu_saraj_iv17']={'id':'abu_saraj_iv17','name':'Jebel Abu Saraj cave IV/17','shortName':'Abu Saraj · IV/17','lat':None,'lon':None,'precision':'source-plan only; cave-group grid is not a mouth coordinate','kind':'point','region':'jericho','note':'Two-opening pillar cave retained provisionally in the existing entry-25 assessment. Sion’s shared cave-group grid does not locate its individual mouths; no exact WGS84 coordinate is assigned.','source':'Sion 2002, ʿAtiqot 41 pp. 61–64, Plan 5 p. 63; entry25_iv17 assessment (2 October 2026)'}
revised_candidates['25']=[{'placeId':'abu_saraj_iv17','status':'possible','confidence':'low'}]
places['jer_siloam']['note']='The inherited coordinate anchors the wider Siloam complex (~300 m). It does not select a particular pool or trough.'
places['mar_saba']['note']='Mar Saba is one proposed stretch of the Kidron gorge. The escarpment exit remains another possibility.'
specific={
'25':('The existing IV/17 assessment documents two openings and a rock-cut dividing pillar at Jebel Abu Saraj. The northern member lies on the right of Sion’s Plan 5 after orienting its north arrow. Qumran remains a separate site-level proposal.','IV/17 is a provisional comparison. Its current aperture normals point southeast; cave-level eastward aspect and a strict mouth-level eastward reading remain separate. Threshold elevation, wall phase, ancient floor and digging origin remain unresolved. Twin Cave and IV/11 are retained controls; a pillar and two openings are not unique.'),
'1':('Late-antique geographical tradition points north of Jericho. Wadi Nuweimeh accommodates both the northwestern springs and northeastern lower valley.','The Iron Age Achor tradition points toward the Buqeia. No reported ruin-and-steps combination decides between them.'),
'4':('Tell es-Sultan supplies a mound and a nearby cemetery. The repository retains it as one possible Kohlit candidate.','Kohlit remains unidentified. The public index maps only a subset of the proposals discussed in the full research.'),
'20':('A cairn and a dam imply different features. Puech prefers a cairn; the dam proposal must be checked independently.','The proposed Qumran dam is reconstructed. Neither it nor a particular cairn has been established as this entry’s landmark.'),
'21':('Qumran’s water system supplies a plausible conduit-head setting. Ilan–Amit’s 1989 plan puts the visible intake beside a reconstructed dam. Stacey (2007) dates the main aqueduct after the 31 BCE earthquake and makes the dam and the cliff tunnel a later stage.','The link to Sekakah and the stone noun are partly restored. Northern approach and northern side must be tested separately. Under Stacey’s phasing, the earlier channel began where the aqueduct leaves the cliff, so the head of a construction stage is an alternative to the dam intake; the phasing is a hypothesis. The pin marks the settlement.'),
'22':('Qumran’s reservoirs provide a setting to test against the fissure east of the named reservoir.','Neither the ancient reservoir name nor the specific eastern fissure has been established. Jerusalem’s similarly named pool does not relocate this entry.'),
'23':('Puech allows Shallum as an alternative to Solomon and a large boulder as the landmark. The channel’s connection to entry 22’s reservoir is conditional.','No origin or endpoint is identified for the stated distance. Entry order alone does not establish a continuous route.'),
'24':('The wording permits a regional approach test from Jericho toward Sekakah. Wadi Kuteif remains a published proposal.','The recorded rock-cut chamber is undated and does not identify the required tomb. A route from entry 23 to entry 24 is not specified.'),
'31':('A Hasmonean fortress occupied the summit, supplied by a wadi diversion, a 500 m channel and nine cisterns. The name Doq survives nearby at Ain Duk.','Editors disagree over “guard post” and “drying place.” The 2026 plate check leans to the drying place, so the fortress is not the landmark by default. The surviving name does not distinguish the summit from the spring; Q24 remains open. Garbrecht and Peleg note that Doq was apparently not rebuilt by Herod, so first-century use of the summit is not shown.'),
'40':('Under the reading “facing the Sea” (west), which the 2026 plate check favours, Beth-Horon keeps Milik’s textual basis; its name survives at Beit ʿUr, and rock-cut tombs are reported at both villages. Naṭuf rests on the order of the entries.','Milik himself later judged the Horite tombs near Beit Guvrin slightly more likely. Puech reads “south”. Jeremias dates his Beit Guvrin shaft-tomb necropolis only as Seleucid. No chamber facing west, channel or 16-cubit depth is reported anywhere.'),
'32':('Choziba preserves a related name, and the Wadi Qelt waterworks fit the outlet-and-wall description in the relevant period.','The individual outlet and retaining wall remain unidentified. The pin represents a stretch of the valley.'),
'35':('The Kidron gorge supplies the named landscape; Mar Saba and Hyrcania feature in published proposals.','“Mouth of the gorge” could also describe the escarpment exit. No cairn fixes the location; Hyrcania’s link depends on restorations.'),
'38':('The spring name and the Khareitun setting support a candidate in this district.','The required dovecote or cave feature has not been demonstrated at this spring.'),
'46':('Ramat Rahel has an earlier pool-and-channel enclosure and later settlement.','The known enclosure lay under fill containing pottery as late as the second century BCE. The current verdict is low; the required period reservoir remains unverified.'),
'48':('The standing Kidron monument has first-century architectural features.','Its earliest surviving labels name Zacharias. A first-century association with Absalom remains unestablished.'),
'49':('The tunnel outlet and surrounding pools supply a compatible water-installation setting. Szanton distinguishes the smaller Silwan pool from Birkat el-Hamra.','Siloam depends on a supplied word; the 2026 plate check shows the disputed letter as a waw-shaped stroke, which leans to Puech without deciding it. Lefkovits reads no Siloam name. The trough remains unverified; overall confidence stays medium and conditional.'),
'55':('The Bethesda complex supplies double pools and a smaller basin in the relevant period.','The smaller basin follows Milik’s and Puech’s reading לימומית; the Text tab reads “on the right”. The text may describe two pools without naming Bethesda; the 2026 plate check shows what looks like a ḥet where Milik’s Bethesda needs a taw. The nearby Strouthion twin pool prevents a unique match on that feature alone.'),
'57':('The mountain name provides the geographical anchor. Magen distinguishes the eastern monumental staircase, the southern seven-step flight, the 15-step flight at E1, and the courtyard cistern in Area P building IV. These are separate installations.','The city was destroyed about 110 BCE. A later Hasmonean garrison is reported, but feature-specific use of the stairs or cistern in the scroll’s period remains unverified. Festus specimen K35264 (58/59 CE) is catalogued at P5178, basket 51777; the total of three is a type count, not three coins demonstrated at that locus. Its architectural and deposition contexts remain unknown. No specific step or upper pit is identified.'),
'58':('Perennial springs and period water installations fit the regional setting at Beth Shean.','The scroll’s final mem differs from the usual nun in Beth Shean. No evidence selects the particular spring.'),
'59':('Zertal identifies Eusebius’s two villages called Bezek, 17 miles from Neapolis, with the two Ibziq sites. A kokhim tomb excavated at Kh. Ibziq in 1971 held pottery of the 1st–2nd centuries CE, which fits Puech’s alternative “burial chamber” reading in type. Zertal places the older Bezeq at nearby Kh. Salhab.','Zertal’s survey reports cisterns and burial caves but no conduit at either Ibziq site, and few Early Roman sherds on the surface. No conduit is reported at Kh. Salhab either. The place name depends on Puech’s reading הבזך, which Allegro and Lefkovits share; the Text tab shows הבור, “the cistern”, the reading of Wilmot and Wise.'),
}
# 15 October 2026: record-conflict corrections (research/assessments/evidence_components/record_conflicts.md).
# Each override replaces stale or overstated atlas text with what the more specific record says; no candidate,
# status or confidence changes. corrected_text: eid -> (evidence, caution); corrected_period: eid -> period text.
corrected_text={
'60':("North of Tell es-Sultan, Kenyon records Qumran-type Roman graves (Jericho II p. 2, pp. 516–545; III pp. 173–174), a Roman burial in a Bronze Age shaft (D9), later undated quarry pits that cut graves, and a Roman cistern with “Herodian” lamps toward Kh. el-Mefjar (N.S.1, II pp. 539–544).","Koḥlit is unidentified; Tell es-Sultan is Puech’s hypothesis. No pit with tombs at its mouth is recorded, and the strip just north of the tell was never searched (Kenyon II p. 169). In the registered Koḥlit rarity count its pit is UNKNOWN; it is one of 23 units meeting two of three conditions (after the source-2 addendum), and none meets all three."),
'58':("Several perennial springs are recorded at Beisan, among them ʿAin el-Melab by the theatre (SWP II pp. 81, 102–107). The town was in use in the period: a dam and pool of the 1st c. BCE–1st c. CE in its farmland (Har’el 2016) and a mausoleum of the later 1st c. BCE (Tzin and Najar 2022).","The scroll’s final mem differs from the usual nun in Beth Shean. No evidence selects the particular spring, and no spring mouth is dated. The dated dam and pool stored water in the farmland; they are not a spring outlet. Milik’s main fountain is known only from 4th–12th-century writers."),
'56':("The entry names no place. Bethesda follows from the preceding entry and Milik’s “just nearby”; the Kidron candidate follows the burial reading. No burial chamber, cave, platform or cistern tied to this entry is reported at either.","West-facing kokhim tombs with several rooms are common. The nearest documented ones, the Jehoshaphat cave and Bene Ḥezir (Kloner–Zissu pp. 140–146), stand at the Kidron monuments, which are not a candidate here. Milik splits the entry into three deposits."),
'55':("The editors report a double pool at St Anne’s, with a smaller northern basin, in use in the 1st century (John 5:2; Milik DJD III pp. 271–272; Høgenhaven p. 84). They rely on excavation reports not read in the repository (Vincent and Abel 1926; Jeremias 1949/1966).","The smaller basin follows Milik’s and Puech’s reading לימומית; the Text tab reads “on the right”. The text may describe two pools without naming Bethesda; the 2026 plate check shows what looks like a ḥet where Milik’s Bethesda needs a taw. The nearby Strouthion twin pool prevents a unique match on that feature alone."),
'54':("Both Jerusalem candidates rest on entry order; no name places the tomb in Jerusalem. Only generic tombs are recorded near either (ASI 102/420; 102/407, 102/424).","Under the Jericho reading, the regional tomb lane scored Puech’s branch in the Jericho region, not in Jerusalem. No tomb at either candidate fits the owner phrase (54-L, 54-M: 0 matches). No repository source proposes Gethsemane; Allegro put this tomb among the common graves on the Kidron’s east bank (1960 p. 93)."),
'52':("The Kidron’s east side is a west-facing rock slope with rock-cut tombs (Milik DJD III pp. 270–271; Avni & Greenhut 1996, abstract). At the Silwan necropolis anchor the survey records Iron Age II monuments and kokhim “apparently from the Herodian period” (ASI 102/420).","No source locates Zadok’s court or garden, so “opposite” has no fixed point. No rock with a great slab at its base is recorded; the tomb lane never meets the garden clause. The 1st-century CE monument that Zias dates (Absalom’s Tomb) stands at the Kidron monuments, north of this anchor."),
'51':("Rock-cut tombs of the Second Temple period are reported in the Kidron generally (Avni & Greenhut 1996, abstract only). Milik places Zadok’s tomb on the west bank below the south-east corner, from texts and traditions (DJD III pp. 270–271). At the angle itself Warren found debris and masonry, no tombs (1871 pp. 135–141).","The only recorded pillared-porch tomb nearby, Bene Ḥezir, stands on the east bank (Kloner–Zissu pp. 143–146). Phase 5 infers that the tomb type fits Jeremias’s east-bank placement better than Milik’s. No tomb is named Zadok. The slope south of the corner was a 1st-century CE refuse dump (HA-ESI 136). Lefkovits reads “ossuary”, not “stoa”."),
'49':("The tunnel outlet and surrounding pools supply a compatible water-installation setting. Szanton distinguishes the smaller Silwan pool from Birkat el-Hamra.","Siloam needs a supplied word; the plates lean to Puech’s waw without deciding it. No period trough is established. Conduit L103 is conditionally excluded as Puech’s hollowed stone and as built before a 69/70 CE coin; Milik’s pipe branch survives."),
'48':("The standing Kidron monument is dated to the first century CE by its architectural style (Zias 2023; Kloner–Zissu pp. 142–143).","Its earliest surviving labels name Zacharias. A first-century association with Absalom remains unestablished. Its original entrance is in the south wall; the western opening is a later breach (Kloner–Zissu p. 142). The entry asks only for its west side."),
'47':("ASI 102/486 records an undated ancient well at ʿEn Rogel (Bir Ayyub). No basin is recorded within 1 km, and no black stone or entrance is reported.","Bir Ayyub depends on Puech’s “valley of Job” (2015 p. 89), whose antiquity he says needs checking (n. 392); the Text tab shows Wolters’s “Valley of Zered(?)”, and Lefkovits reads “Pure Valley”."),
'45':("ASI 102/486 records an undated ancient well at ʿEn Rogel (Bir Ayyub). In the Tekoa–Herodium sector, cemented cisterns at Tekoa and a reservoir and aqueduct at Herodium are reported (SWP III pp. 27, 330–331). No cistern fed by channels from a great wadi is identified at either.","The entry names no place. Puech’s order puts it in the Tekoa–Herodium sector; the repository records no argument for Bir Ayyub, and the map region follows only the first listed candidate. A well fits only Milik’s wheel-well reading; the water survey left it unscored because its feed is unrecorded."),
'44':("Puech reads a dovecote in a “small fort”, not a place name (2015 p. 86), and places entries 39–45 near Tekoa and Herodium by their order. Herodium had a fortress with towers (SWP III pp. 330–331), and talmudic texts tie pigeons to this district (Milik C4).","No dovecote is reported in the sector. The Text tab’s “second upper storey” needs three levels; Puech’s reading needs two. In an exploratory review of 179 recorded columbaria none meets the text shown, and only Masada’s towers meet Puech’s reading, through Netzer’s reconstruction. Masada rests on Milik’s emendation (Phase 3: weak or ruled out)."),
'40':("Under “facing the Sea” (west), favoured by the 2026 plate check, Beth-Horon keeps Milik’s textual basis, which also needs his article read as “Beth”. The name survives at Beit ʿUr. Rock-cut tombs are reported at both villages; the lower village’s tomb with period pottery faces south (Peleg 2004 Fig. 1). Naṭuf rests on the order of the entries.","Milik himself later judged the Horite tombs near Beit Guvrin slightly more likely; that necropolis is a possible, low candidate that is recorded but not mapped. Puech reads “south”. Jeremias dates the necropolis only as Seleucid. No chamber facing west, channel or 16-cubit depth is reported anywhere."),
'39':("Terraced land by Tekoa, rock-cut tombs, cisterns and caves are reported in the sector (SWP III pp. 296–300). They are generic features; only the Herodium works are dated to the 1st c. BCE.","No chamber facing east is reported, and the sector is chosen by entry order, not by a name. Puech reads “second terrace”; Milik reads a place name, Tekelet ha-Šani, found only in his text. Hirschfeld’s 1985 survey of the area has not been consulted."),
'38':("The spring name and the Khareitun setting support a candidate in this district.","The required dovecote, rock opening or tower has not been demonstrated at this spring, and no columbarium is recorded within 2 km. Dated remains there are late antique and medieval. The placement rests on the name ʿAin en-Naṭuf (Milik 1960 p. 150); Lefkovits places Netophah at Kh. Badd Faluh."),
'36':("Second Temple rock-cut tombs are reported in the Kidron valley in general (Avni & Greenhut 1996, abstract only). They are generic underground chambers.","No source fixes which valley the Shaveh is (Q22): Puech looks toward Beth ha-Kerem, Milik to Bethso at the Baqʿah. No north-facing chamber is identified, and “fallow land” cannot be tested. The label position is schematic."),
'35':("The Kidron gorge supplies the named landscape; Mar Saba and Hyrcania feature in published proposals.","“Mouth of the gorge” could also describe the escarpment exit, and no cairn is reported. Hyrcania’s link needs יגר to mean “dam” (Luria, Eshel), which Puech rejects (2015 p. 73 n. 298). Eshel’s system description names no southern dam (CSS p. 95), but Patrich records southern intake station 1 (1989 p. 244); its position and date are unknown."),
'34':("The public site index keeps three candidates, in Jerusalem (Bir Ayyub), the Jericho district and Doq. No inscribed stone or other stone marker is reported at any of them.","“The outer valley” is unnamed. The three candidates follow entry order, not a name or feature argument. At En-Rogel the survey records only an undated well. The placement remains at site or district level."),
'32':("Choziba preserves a related name, attested from the 5th-century monastery. The Wadi Qelt aqueducts were built under the Hasmoneans and Herod and used in the period (Eshel CSS pp. 97–100). SWP describes a channel head at ʿAin Qelt, a division at Jisr ed-Deir and a cliffside wall opposite Deir el-Kelt.","No outlet with a wall at its mouth is recorded in the Qelt. The outlet’s function is unresolved and the wall’s period is not established. Lefkovits reads “of Buz”, and הטור may mean a wall, parapet, mountain or rock. The pin represents a stretch of the valley."),
'30':("Puech proposes an estate of the priestly family Haqqoz at Jericho (2015 p. 66). The district has palace baths and pools, and cliff caves used in the 1st c. BCE–1st c. CE (Eshel CSS pp. 99–100).","No house of Haqqoz, cool room or adjacent cave is identified, and the estate and cave chronology is unestablished. “Cool room” is Puech’s restoration; Milik reads “in its vicinity”, and several editors read “summer house”, not a family name. The placement is district-level."),
'29':("Two conditional tests are complete; both are inconclusive. At Jericho, the northern of the two early Hasmonean pools (about 18 × 13 m) does not stand out from the southern control in the offset test. At Hyrcania, the northern member of the double pool (Patrich 1989 p. 255) has no fixed measuring origin. ʿAin Duk and Tell es-Sultan have no entry-29 test.","Jericho is restored, and Hyrcania rests on Eshel’s Qi[dron], which Puech finds too long for the gap. At Jericho the original inlets are lost and Herod joined the two pools. At Hyrcania the pool’s inlet is unidentified, and Patrich dates its abandonment after Herod. No deposit point is proposed."),
'25':("The existing IV/17 assessment documents two openings and a rock-cut dividing pillar at Jebel Abu Saraj. The northern member lies on the right of Sion’s Plan 5 after orienting its north arrow. Qumran remains a separate site-level proposal.","IV/17 is a provisional comparison: its aperture normals point southeast, and threshold, wall phase, ancient floor and digging origin are unresolved. Twin Cave, about 1 km north of Kh. Qumran, is the only cave matching every clause at both-mouths level (Bar-Adon 1989), but its mouth positions and date are unknown. It and IV/11 remain controls; the form is not unique."),
'24':("The wording permits a regional approach test from Jericho toward Sekakah. Wadi Kuteif remains a published proposal.","The recorded rock-cut chamber is undated and does not identify the required tomb. The only dated tombs recorded in the wadi, four pit tombs with glass beads (WBADB E508), are Early Islamic. A route from entry 23 to entry 24 is not specified."),
'19':("North of Tell es-Sultan Kenyon records a Roman cistern (N.S.1), a hewn pit with Roman sherds (P29) and later quarry pits (Kenyon II pp. 539–544; III p. 174).","These are generic pits. None is identified as the eastern pit of a set, and N.S.1 has no plan. The quarry pits cut the 1st-century graves and have no absolute date. Koḥlit is unlocated; the placement depends on entries 4, 11, 15 and 60."),
'18':("The name survives as Wadi el-ʿAṣla / Gofet el-ʿAṣla (Milik DJD D6; SWP III p. 200). Red marl, which suits an “earth” or “red” pit, is common there (Puech 2015 p. 52 n. 206).","No pit is reported, the wadi’s archaeology is unpublished and no period is stated. The IAA escarpment survey reports Early Roman caves but does not name ʿAṣla (Yitah et al. pp. 180–185). Lefkovits reads no place name. The rating rests on the surviving name and entry order."),
'17':("Caves in the cliffs bordering Wadi Nuweiʿimeh were in use in the 1st century BCE–1st century CE (Aronshtam pp. 98, 101; Eisenberg p. 120; Sion pp. 80–81). Under Puech’s “cavities” reading the project tests one pair, V/49 and its neighbour V/48.","No source reports a pair of cavities, tamarisks or buildings. The period shown is for the Nuweiʿimeh caves: the Buqeia has only Iron Age ruins (period fit earlier only; Phase 5 check low). ʿAin Duk is kept only as the springs at the head of the same valley; nothing specific to it is recorded."),
'11':("On Puech’s hypothesis this is a pool east of Tell es-Sultan. The SWP records a shallow reservoir, 24 × 40 ft, at the spring on the tell’s east foot (via Dorrell 1993 p. 96).","The basin’s construction and early use are undated. The present reservoir was built in 1898 (Dorrell p. 111), so that branch fails the period. No northern corner is identified. Koḥlit itself is unlocated."),
'10':("Warren describes rock scarps and the masonry of the east wall and its south-east angle (Recovery pp. 135–141, 153–158), and undated cisterns with channels under the platform (pp. 204 ff.).","No report describes a cistern under the east wall with a threshold. Whether the wall is the city’s or the Temple enclosure’s is open (Lefkovits p. 130). The placement follows entry 9 (Puech 2006 p. 184); the individual feature has not been identified."),
'9':("Milik and Puech take the gate as the Temple’s East Gate (Puech 2006 p. 184). Warren records many undated rock-cut cisterns with feed channels under the platform (Recovery pp. 204 ff.).","On Warren’s Plate VI no recorded cistern lies 19 cubits (8.5–10 m) from the Golden Gate; the nearest, No. 15, is 30 m away. Only open mouths were recorded and deep debris lies before the gate, so a buried cistern is not excluded. The 1st-century gate is known only from texts."),
'4':("Tell es-Sultan supplies the mound: its main city was early, so it was an old ruin-mound by the 1st century (SWP p. 223). Channels run from the spring below it but are undated (SWP pp. 222–223).","No rock cleft or immersion installation is reported at the tell; the dated Hasmonean–Herodian baths and aqueducts lie in the palace area to the south (Eshel pp. 99–100). Koḥlit remains unidentified; Tell es-Sultan is Puech’s hypothesis."),
'3':("Milik puts the peristyle court in the Temple (DJD pp. 272–274); Puech queries the Valley of Achor (2006 p. 175). Under the Temple platform, tank No. 8, the “Great Sea”, is the largest cistern (SWP Jerusalem pp. 219–220). The project proposes it as a possible match, low.","Tank No. 8 is undated and lies under the southern outer court, while Milik’s peristyle is the inner court. No cistern is reported in relation to a peristyle court. The scroll’s individual feature has not been identified."),
'2':("The editions disagree on the third datum: a third masonry course (Puech 2015 p. 29), a third gravestone (Lefkovits 2000 p. 50) or a personal name (Milik 1960 pp. 139, 144). The entry names no place; Puech groups it with entry 1, and the Kidron monuments are kept as funerary monuments.","Zechariah’s monument is monolithic and Absalom’s lower body is rock-cut, so neither supplies a built third course (Kloner–Zissu 2003 pp. 142, 146). This excludes that branch only; the gravestone and name branches are untested. No monument is identified."),
'1':("Late-antique tradition puts Achor north of Jericho, beside Galgala (Onomasticon). On PEF Sheet XVIII Wadi Nuweiʿimeh rises at springs NW of Jericho and runs to a lower course NE of it. Whether TIR’s “Achor Vallis” label means this valley is unverified; its gazetteer page is unread.","The Iron Age Achor tradition points toward the Buqeia. No reported ruin-and-steps combination decides between them."),}
corrected_period={
'1':"No feature dated. Valley only: Early Roman houses and a stepped cistern on the south bank, a late Hellenistic tomb on the north bank (Taha 2020 pp. 277–278)",
'60':"North-slope graves 1st c. CE by grave-type comparison only; quarry pits undated; the tell itself EB only in WBADB",
'56':"No feature dated. Sites only: Bethesda pools in 1st-c. use (John 5:2, via editors); Silwan kokhim “apparently Herodian” (ASI 102/420)",}
specific.update(corrected_text)
# 8 October 2026: where a title follows an edition reading that differs from the text shown in the
# Text tab, the caution says so (text/readings.json records the readings).
reading_notes={
'5':'The title follows Puech’s reading, a spiral staircase; the Text tab shows Milik’s letters, read as a foundry.',
'37':'The title follows Milik’s and Puech’s reading ברוי, irrigated land; the Text tab shows בדור, translated “enclosure”.',
'54':'The title follows Puech’s reading ירחו, Jericho; the Text tab shows טהור, translated “ritually pure”; Wolters, reading from the metal, also found “pure” there.',
'6':'The title follows the Esplanade reading of the same word at III 8 and III 11; here Puech (2015 pp. 38–39) and Lefkovits (pp. 103–104) read a salt pit below the steps, and the Text tab shows המלח, ha-Melaḥ. No repository record says why the entry was placed in the Tyropoeon.',
'7':'The title follows Puech’s “house of Tribute” (2015 pp. 38, 40); he rejects the sense “measure”. The Text tab shows המדח, translated “Washing(?)”.',
'13':'The title follows Milik’s and Puech’s Esplanade or embankment (Puech 2015 pp. 44, 46); the Text tab shows שבמלחמ, ha-Melaḥ, with a final מ that no edition reports.',
'14':'The title follows Milik’s and Puech’s Esplanade or embankment (Puech 2015 pp. 44, 46), and the slab follows Milik’s DJD text and Puech; the Text tab shows ha-Melaḥ and “the dead(?)”.',
'16':'The pool is Puech’s restoration, “to the po[ol]” (2015 p. 48). He rejects Eshel’s restored “Hyrcania” as too long for the gap (p. 50 n. 193). The Text tab leaves the conduit’s goal unread.',
'17':'The Text tab shows הכיפין, translated “domes(?)”, which matches none of these three readings.',
'27':'Puech reads משכן as the queen’s “mausoleum” (2015 p. 60), and the Text tab translates “resting place”; the files name no editor for the dwelling sense.',
'29':'The title follows Puech’s restoration, a collection of the waters (2015 pp. 62–63); the Text tab leaves the word damaged (קי◦) and restores no Jericho.',
'33':'The title follows Puech’s house of the treasury and Aḥiyah (2015 p. 69). Milik reads place names (Bet Ḥaṣor, Ḥazor), Lefkovits reads Ahim, and the Text tab shows אחור, “Aḥor”.',
'34':'The title follows Puech’s and Lefkovits’s engraved inscription (Puech 2015 p. 69); the Text tab shows other letters, translated “in the middle of the ◦”.',
'43':'The exposed rock follows Puech’s “rocky ground” (2015 p. 75), on letters Lefkovits shares; the Text tab reads “at the outlet of the Valley of Peleʿ(?)”.',
'46':'The description’s large reservoir follows Milik’s gloss (C70), which has not been rechecked; Puech reads a pool or basin (2015 p. 85), Lefkovits a pool or a deep pit (p. 331).',
'47':'The spring and chamber follow Puech’s “underground (near) its spring” (2015 p. 85); the Text tab reads “on its west side”, as Milik and Lefkovits.',
'49':'The title and the water outlet follow Puech’s “spring (?) of Siloam waters” (2015 p. 86); the Text tab shows Milik’s letters, “basin(?) of the bathhouse(?) of Raḥil(?)”.',
'50':'The title and its Hebrew follow Puech’s “courtyard (of the tomb) of Ṣadoq” (2015 p. 139); no other edition reads Zadok at X 17. Lefkovits restores an inner court; the Text tab restores “In the upper pool”, Wise’s conjecture.',
'53':'The title and its Hebrew follow Puech’s “colonnades” (2015 p. 94); the Text tab shows הסכין, translated “rock ‘knife’(?)”.',
'56':'The cave and recesses follow Puech’s restoration and his burial niche (2015 pp. 94, 107); the Text tab leaves the cave unread and reads “the cistern”.',
}
audit=rows('phase5_archaeology_index.csv')
entries=[]
for r in rows('phase3_site_index.csv'):
    eid=r['entry']; title,hebrew,description=descriptions[eid]
    ids=list(dict.fromkeys(([r['best_place_id']] if r['best_place_id'] else [])+[x.strip() for x in r['possible_place_ids'].split(';') if x.strip()]))
    ar=[a for a in audit if a['entry']==eid]
    primary=next((a for a in ar if a['phase3_verdict']=='best-supported'),ar[0] if ar else None)
    confidence=primary['phase5_confidence'] if primary else r['best_confidence'] or ('unknown' if not ids else 'low')
    confidence=revised_confidence.get(eid,confidence)
    candidates=[]
    for pid in ids:
        preferred=pid==r['best_place_id']
        conf=confidence if preferred else 'medium' if (eid,pid) in [('17','buqeia'),('18','asla'),('30','jericho_area'),('59','ibziq')] else 'low'
        conf=revised_candidate_confidence.get((eid,pid),conf)
        status='preferred' if preferred else 'weak' if pid=='tell_el_qos' else 'possible'
        candidates.append({'placeId':pid,'status':status,'confidence':conf})
    evidence=primary['landmark_reported_at_site'].capitalize()+'.' if primary else 'The public site index retains these candidates for comparison. It supplies no uniquely identified landmark for this entry.'
    caution='The placement remains at site or district level. The scroll’s individual feature has not been identified.'
    if eid in specific: evidence,caution=specific[eid]
    if eid=='41': evidence='The public index leaves this entry unmapped.';caution='The reading and geographical setting remain unresolved.'
    if eid in reading_notes: caution=reading_notes[eid]+' '+caution
    if eid=='54': evidence+=' If the tomb was reserved for priests, Puech names the tomb of the Benê Ḥezîr in the Kidron valley as one possibility (2015 p. 101). That tomb stands at the Kidron monuments, which are not a candidate for this entry.'
    candidates+=revised_candidates.get(eid,[])
    entries.append({'id':eid,'title':title,'hebrew':hebrew,'description':description,'lines':r['col_line'],'status':r['status'],'confidence':confidence,'region':places[ids[0]]['region'] if ids else 'unplaced','candidates':candidates,'evidence':evidence,'caution':caution,'landmark':primary['landmark_types_required'] if primary else '', 'period':primary['period'] if primary else 'Not established in the public archaeology index','sources':primary['main_sources'] if primary else 'Phase 3 site index; Phase 2 landmark lexicon','featured':eid in ['21','31','32','49']})
for entry in entries:
    if entry['id'] in corrected_period:
        entry['period']=corrected_period[entry['id']]
    if entry['id'] in ['20','21','22','23','24']:
        entry['sources'] += '; Puech 2006 pp. 187–189; Qumran reference review (28 September 2026)'
    if entry['id']=='21':
        entry['sources'] += '; Lefkovits 2000 pp. 185–189; Stacey 2009, The Dam; Stacey 2007, DSD 14 pp. 222–243'
    if entry['id']=='25':
        # Put the documented cave comparison first without changing any candidate status or confidence.
        entry['candidates'].sort(key=lambda c: c['placeId'] != 'abu_saraj_iv17')
        entry['sources'] += '; Sion 2002, ʿAtiqot 41 pp. 61–64, Plan 5 p. 63; existing IV/17 assessment (2 October 2026)'
    if entry['id']=='57':
        entry['sources'] += '; Magen 2008 plan p. 1743; catalogue-methodology correction (1 October 2026)'
    if entry['id']=='39':
        entry['landmark'] = 'an underground chamber facing east, in a terrace'
    if entry['id']=='54':
        entry['sources'] += '; Puech 2015 p. 101'
    if entry['id']=='29':
        entry['period'] = 'Tested pools Hasmonean (Jericho 103–67 BCE, joined under Herod; Hyrcania, abandoned after Herod)'
        entry['sources'] += '; Trümper 2018 pp. 280–286; Netzer 1983 pp. 101, 105–106; Patrich 1989 pp. 255–256, Fig. 22; Patrich 2002 p. 336; entry-29 assessments (2 October 2026)'
out={'snapshot':'e3b51ce6523e947fe217a630d64fa16486fc3c7c','reviewDate':'12 October 2026','entries':entries,'places':list(places.values())}
assert len(entries)==61 and len(places)==40
assert all(c['placeId'] in places for e in entries for c in e['candidates'])
(root.parent/'app/atlas-data.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(f'Built {len(entries)} entries and {len(places)} places; {sum(p["lat"] is not None for p in places.values())} mapped anchors.')
