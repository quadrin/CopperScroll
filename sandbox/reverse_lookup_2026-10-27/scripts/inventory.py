# Run 22: site feature inventories (written and hashed before step 2 scoring).
# Verdicts are [strict, lenient, basis]. P = recorded in the window (or natural);
# U = not recorded / not dated / not at the needed scale; A = absent (source states it,
# or the site was fully cleared and its report's inventory of that built feature puts
# none there, or the only example contradicts). Anything not listed = U.
# Strict J7: a dated find, phase or text tied to the feature. Lenient J7: also typology,
# "commonly attributed", or background knowledge (BK) not taken from a source read here.
# Site = the area covered by the site's own reports/descriptions (plus its own outlying
# installations such as aqueducts, dams, cemetery and caves within 500 m); landscape
# relations (valley, wadi, gorge, road) use the run 1 500 m bound.
# Sources abbreviations:
#  NZ01 = Netzer 2001, Palaces of the Hasmoneans and Herod (scratch text; printed p. = pdf - 4)
#  NZ81 = Netzer 1981, Greater Herodium (Qedem 13), OCR without page marks (chapter cited)
#  NZ10 = Netzer et al. 2010, JRA 23 (via run 9 pair_scores)
#  MP18 = Magen & Peleg 2018 (via run 1 evidence, run 12, scratch mp_water.txt)
#  dV73 = de Vaux 1973 Schweich (via run 1 / run 12)
#  PA89/PA02 = Patrich 1989 (Hebrew) / 2002 (JRA Suppl. 46) via registration/hyrcania_patrich1989_extracted.md, run 1
#  HG24 = Haber & Gutfeld 2024 (research/history/haber_gutfeld2024_hyrcania_extracted.md)
#  WC84 = Warren & Conder 1884 SWP Jerusalem; GJ96 = Gibson & Jacobson 1996 (registration/warren1884_temple_mount_cisterns_extracted.md)
#  CDx  = registration/siloam_city_of_david_2010_2022_extracted.md (R&S 2010, S&R 2011, Grossberg 2011, WB & Szanton 2014, WB & Hagbi 2022)
#  R1..R16 = earlier sandbox runs (evidence / RESULT files)
#  MHCS4 = Zertal & Bar MHCS 4 via research/assessments/sartaba_hydraulic_control/README.md
import json, sys

SITES = {
 "QUM": dict(name="Kh. Qumran", region="in", lat=31.74112, lon=35.45907),
 "JER": dict(name="Jericho Hasmonean-Herodian palaces (Tulul Abu el-ʿAlayiq)", region="in", lat=31.852, lon=35.436),
 "HYR": dict(name="Hyrcania (Kh. el-Mird)", region="in", lat=31.718768, lon=35.365219),
 "HER": dict(name="Herodium, Upper and Lower", region="in", lat=31.6658, lon=35.2414),
 "MAS": dict(name="Masada", region="out (scored, marked)", lat=31.3156, lon=35.3536),
 "KYP": dict(name="Kypros (Tell el-ʿAqaba)", region="in", lat=31.845, lon=35.43),
 "ALEX": dict(name="Alexandrium (Sartaba)", region="in", lat=32.1, lon=35.46),
 "TM": dict(name="Temple Mount (surveys and descriptions only)", region="in", lat=31.77825, lon=35.23534),
 "CD": dict(name="City of David / Siloam", region="in", lat=31.7735, lon=35.2357),
}

P, U, A = "P", "U", "A"
def v(s, l, b): return [s, l, b]

INV = {s: {} for s in SITES}
def put(site, code, s, l, b): INV[site][code] = v(s, l, b)

# ---------------- generic: ruin (destroyed/abandoned within the window), ford, spring
ruin = {
 "QUM": (P,P,"destroyed 68 CE (dV73 ch. II; BK for the exact page)"),
 "JER": (P,P,"Herod's Second Palace built 'on the ruins of the Hasmonean palace' (NZ01 contents, ch. 6)"),
 "HYR": (P,P,"destroyed by Gabinius 57 BCE; abandoned after Herod (PA02 p. 336)"),
 "HER": (P,P,"'buildings of the Herodian period already lay in ruins' (NZ81 ch. III, pool complex summary)"),
 "MAS": (P,P,"destruction 73 or 74 CE (NZ01 pdf 95, printed 91)"),
 "KYP": (P,P,"destroyed by Pompey 63 BCE (NZ01 pdf 76, printed 72)"),
 "ALEX":(U,P,"razed by Gabinius 57 BCE (BK, Josephus; not read here)"),
 "TM":  (P,P,"destroyed 70 CE (Josephus BJ 6, text)"),
 "CD":  (P,P,"70 CE destruction layers (CDx: WB & Szanton 2014 p. 5)"),
}
for s,(a,b,c) in ruin.items(): put(s,"F:ruin",a,b,c)
for s in SITES:
    put(s,"F:ford",A,A,"no river within 500 m (the Jordan is >5 km from every site): INFERENCE from geography")
for s in ["QUM","JER","HYR","HER","MAS","KYP","ALEX","TM"]:
    put(s,"F:spring",A,A,"no spring within 500 m (QUM: ʿEin Feshkha 3 km; JER: ʿAin es-Sultan ~2 km; fortresses depend on runoff/aqueducts, NZ01 pdf 72-73 'lack of water sources'; HER: aqueduct from Urtas, NZ81 ch. III; TM: none)")
put("CD","F:spring",P,P,"Gihon spring (CDx: R&S 2011; Grossberg 2011 p. 72)")
for s in SITES:
    put(s,"F:stone",P,P,"stones/boulders occur at every site (generic)")

# ---------------- QUMRAN
q = "QUM"
for code,s_,l_,b in [
 ("F:cistern",P,P,"L71, L91, L110, L56/58 etc. (MP18 p. 90; Galor 2006 Table 1 p. 259 via R12)"),
 ("F:reservoir",P,P,"L71 19.10×4.90×5.40 m, Period Ib (MP18 p. 90; R1 J5)"),
 ("F:pool",P,P,"stepped pools L48/49, L68, L69 (MP18 water section; dV73)"),
 ("F:immersion",U,P,"stepped pools read as miqvaot by de Vaux and others; MP18 p. 90 argues clay pools, not ritual baths"),
 ("F:steps",P,P,"staircases into L71 ('descended the entire length', MP18 p. 90), L68 (east and west stairs)"),
 ("F:conduit",P,P,"aqueduct from Naḥal Qumran (MP18 p. 90 phase A; Ilan & Amit 1989 Fig. 1; R1 J4)"),
 ("F:channels",P,P,"central channel and branches feeding pools (MP18 p. 90)"),
 ("F:channel",P,P,"central channel (MP18 p. 90)"),
 ("F:conduit_head",P,P,"aqueduct head at Ilan & Amit point 3, ~350 m W (R1 J4; J7 Period Ib, dV73 p. 8)"),
 ("F:dam",U,U,"reconstructed only (Ilan & Amit 2002 pp. 381-382; R1 J3-dam)"),
 ("F:great_stone",U,P,"boulder ~3 m high at the upstream channel (Reeder & Jol 2006 Fig. 4 via R1 J6)"),
 ("F:fissure",P,P,"natural cracks: N-S crack through L48-L50 (de Vaux 1973 Pl. XXXIX via R12); cracks in marl east of L71 (MP18 pp. 38, 51); natural feature, so J7 satisfied"),
 ("F:valley",P,P,"Wadi Qumran 190 m SSW (R1 J2)"),
 ("F:wadi",P,P,"Wadi Qumran (R1 J2)"),
 ("F:great_wadi",P,P,"Wadi Qumran / Naḥal Qumran, 46.76 km² catchment (R7)"),
 ("F:gorge_mouth",U,P,"site sits above the point where Wadi Qumran leaves the cliffs (R1 site description; INFERENCE)"),
 ("F:road",P,P,"'road west from Qumran and ʿEn Feshkha' (Cross & Milik 1956 p. 7 via R7)"),
 ("F:cave",P,P,"4Q, 5Q, 7Q-10Q within 500 m, Second Temple finds (R10 inventory, DJD III)"),
 ("F:tomb",P,P,"cemetery shaft graves; fills with Period Ib/II pottery, Herodian lamp (dV73 pp. 45-47; MP18 p. 99, via R1)"),
 ("F:burial_chamber",U,U,"shaft graves with loculus; no 'resting chamber' recorded"),
 ("F:cairn",U,P,"'oval-shaped heaps of stones' over graves (dV73 p. 46 via R1 J3-cairn W500)"),
 ("F:heap",U,P,"grave heaps (dV73 p. 46 via R1)"),
 ("F:great_heap",U,U,"no 'great' heap recorded (R1 J6)"),
 ("F:trench",U,P,"aqueduct/central channel (MP18 p. 90); no feature called a trench"),
 ("F:court",P,P,"courtyards of the main building (dV73; MP18)"),
 ("F:guard_post",P,P,"the tower (dV73, Period Ib)"),
 ("F:fortress",U,P,"fortified tower; Hasmonean fort phase (MP18 interpretation)"),
 ("F:wall",U,P,"enclosure walls and the long wall (dV73)"),
 ("F:enclosure",U,P,"enclosure walls (dV73)"),
 ("F:house",U,P,"main building"),
 ("F:chamber",U,U,"rooms; no underground chamber recorded"),
 ("F:underground_chamber",U,U,"none recorded in the sources read"),
 ("F:pit",P,P,"cisterns/pits (synonym class)"),
 ("F:hollow",P,P,"pits and cisterns (synonym class)"),
 ("F:basin",P,P,"small basins and sedimentation pools L67, L69 (MP18 Fig. 101)"),
 ("F:waterfall",U,P,"natural basin 2 at the aqueduct head below the fall (Strobel 1972 pp. 66-67, MP18 p. 79 via R1 J5)"),
 ("F:upper_storey",U,P,"tower upper storey (dV73; not read here)"),
 ("F:bathhouse",A,A,"no bathhouse in the excavated site (dV73, MP18): fully cleared"),
 ("F:cool_room",A,A,"no bathhouse/frigidarium (fully cleared)"),
 ("F:dovecote",A,A,"no columbarium recorded (fully cleared)"),
 ("F:peristyle_court",A,A,"no colonnaded court (fully cleared)"),
 ("F:stoa",A,A,"no portico (fully cleared)"),
 ("F:exedra",A,A,"none (fully cleared)"),
 ("F:spiral_stair",A,A,"no newel stair recorded (fully cleared)"),
 ("F:monument",A,A,"cemetery has simple shaft graves only (dV73 pp. 45-47)"),
 ("F:mausoleum",A,A,"no monumental tomb (dV73 pp. 45-47)"),
 ("F:mound",U,U,"not a tell"),
 ("Q:cistern:great",P,P,"L71 the largest (Galor 2006 Table 1 p. 259: L71 300 m³) Period Ib"),
 ("Q:reservoir:great",P,P,"L71 (as above)"),
 ("Q:cistern:plastered",P,P,"L71 'completely plastered' (MP18 p. 90); 'built and plastered aqueduct' (p. 90)"),
 ("Q:cistern:channel",P,P,"each pool connected to a branch of the central channel (MP18 p. 90)"),
 ("S:cistern:of:channels",P,P,"pools fed by branches of the central channel (MP18 p. 90)"),
 ("S:channels:fed_from:great_wadi",P,P,"'aqueduct brought water from Naḥal Qumran' (MP18 p. 90)"),
 ("S:conduit:to:reservoir",P,P,"central channel enters L71 from the west (MP18 p. 90)"),
 ("S:conduit:to:pool",P,P,"aqueduct feeds the pools (MP18 p. 90)"),
 ("S:fissure:east_of:reservoir",P,P,"crack 3.3-3.6 m E of L56/58 (R12 branch A); crack 1.5-2.2 m E of L71 (MP18 pp. 51, 67; R1)"),
 ("S:great_stone:at:conduit_head",U,P,"Reeder & Jol boulder at the upstream channel, 0-2 m (R1 J6)"),
 ("Q:conduit_head:north_side",U,P,"channel begins in a northern side branch (Schulz 1960 p. 54 via R1 J4-flow, caveat)"),
 ("Q:conduit:enterable",U,P,"rock-cut tunnel section of the aqueduct (Ilan & Amit; R1 feature table)"),
 ("S:steps:of:cistern",P,P,"staircase descending into L71 (MP18 p. 90)"),
 ("S:steps:of:pit",P,P,"as above (pit = cistern class)"),
 ("S:tomb:in:wadi",U,P,"south-cemetery graves on the S bank of Wadi Qumran (MP18 p. 94 via R1)"),
 ("S:pit:north_of:gorge_mouth",U,P,"site cisterns lie N of Wadi Qumran's exit (INFERENCE)"),
 ("Q:cave:pillar",U,U,"DJD III cave 27 'pillar' passes in R10 but undated"),
 ("Q:cave:two_entrances",U,U,"R10: unknown for 4Q-10Q"),
 ("Q:cave:faces_east",U,U,"R10: unknown"),
 ("Q:cave:north_entrance",U,U,"R10: unknown"),
]: put(q,code,s_,l_,b)
put(q,"R:jericho_route",P,P,"Cross & Milik 1956 p. 7 (R7 correction to R1 J1)")

# ---------------- JERICHO PALACES
j = "JER"
for code,s_,l_,b in [
 ("F:pool",P,P,"Hasmonean swimming pools, ~18×13 m (NZ01 ch. 2; entry29_jericho_pools assessment)"),
 ("F:reservoir",P,P,"pools of the Hasmonean pools complex (as above)"),
 ("F:cistern",P,P,"cistern under a bathhouse room, southern tell, Third Palace (NZ01 pp. 58-59 via R9)"),
 ("F:immersion",P,P,"stepped pools/miqvaot in the palaces (NZ01 pdf 91: stepped pool used as a ritual bath in the Twin Palaces' bath suites)"),
 ("F:bathhouse",P,P,"bathhouses in the Hasmonean and Herodian palaces (NZ01 pdf 56, 89, 91)"),
 ("F:cool_room",P,P,"frigidarium in the Third Palace bath wing (NZ01 pdf 56)"),
 ("F:basin",P,P,"bathtubs and basins in the Hasmonean palace bath suites (NZ01 pdf 89, 91)"),
 ("F:peristyle_court",P,P,"Third Palace courts B55, B64; Herod's First Palace 42×35 m (NZ01 pp. 40-53 via R9)"),
 ("F:court",P,P,"courts (as above)"),
 ("F:stoa",P,P,"colonnade at the N end of the gardens, Twin Palaces (NZ01 p. 35 via R9)"),
 ("F:exedra",P,P,"Second Palace distyle exedra; Third Palace round hall with exedrae (NZ01 pp. 45, 58-59 via R9)"),
 ("F:garden",P,P,"gardens of the Hasmonean pools complex and the Third Palace (NZ01 pp. 24, 56 via R9)"),
 ("F:dovecote",P,P,"round columbarium tower west of the royal estate, Hasmonean (NZ01 pdf 18, Fig. 5)"),
 ("F:guard_post",U,P,"upper part of the columbarium tower 'probably used as a guard post' (NZ01 pdf 18)"),
 ("F:fortress",P,P,"Fortified Palace of Jannaeus (NZ01 pp. 27-29 via R9)"),
 ("F:upper_storey",P,P,"Twin Palaces had two stories (NZ01 pdf 91)"),
 ("F:spiral_stair",P,P,"stairwells with a central pillar in the Twin Palaces (NZ01 pdf 98)"),
 ("F:steps",P,P,"stairways (NZ01 pdf 48 Fig. 49 stairway)"),
 ("F:conduit",P,P,"aqueducts from Wadi Qelt, Naʿaran and ʿAujah springs feeding the palaces (NZ01 ch. 1-2; R11 control)"),
 ("F:channels",P,P,"supply channels to the pools (entry29_jericho_pools; Trümper 2018 pp. 280-286)"),
 ("F:channel",P,P,"as above"),
 ("F:conduit_head",U,P,"aqueduct heads at the springs, several km away"),
 ("F:mound",P,P,"the tulul: artificial mounds (Kelso & Baramki's three phases 'in this mound', NZ01 pdf 62)"),
 ("F:valley",P,P,"Wadi Qelt (NZ01 pdf 76)"),
 ("F:wadi",P,P,"Wadi Qelt"),
 ("F:great_wadi",U,P,"Wadi Qelt; the aqueducts are spring-fed"),
 ("F:gorge_mouth",U,P,"palaces at the outlet of Wadi Qelt (NZ01 pdf 76)"),
 ("F:road",P,P,"Jerusalem-Jericho road along Wadi Qelt (NZ01 pdf 76)"),
 ("F:cave",P,P,"Ketef Jericho caves ~240 m (R10: Z23 KetefJericho, J7 pass)"),
 ("F:house",P,P,"palaces"),
 ("F:chamber",U,P,"rooms; vaulted rooms not recorded in the pages read"),
 ("F:enclosure",U,P,"royal estate enclosure (NZ01 pdf 18)"),
 ("F:pit",P,P,"cisterns/pools (synonym class)"),
 ("F:hollow",P,P,"pits/pools (synonym class)"),
 ("F:wall",U,P,"fortified palace walls (NZ01 p. 27)"),
 ("F:tomb",U,U,"no tomb recorded in the palace reports read"),
 ("F:monument",U,U,"none recorded"),
 ("F:mausoleum",U,U,"none recorded"),
 ("Q:reservoir:great",U,P,"pools ~18×13 m; 'great' not stated"),
 ("Q:reservoir:northern",U,P,"northern pool of the Hasmonean pools complex (research/assessments/entry29_jericho_pools)"),
 ("S:conduit:to:reservoir",P,P,"supply channels to the pools (Trümper 2018 pp. 280-286 via entry29 assessment)"),
 ("S:conduit:to:pool",P,P,"as above"),
 ("S:cool_room:of:house",P,P,"frigidarium in the palace bath wing (NZ01 pdf 56)"),
 ("S:basin:of:bathhouse",P,P,"basin and bathtub in the bath suites (NZ01 pdf 89, 91)"),
 ("Q:cistern:plastered",U,P,"hydraulic plaster in palace installations (NZ01; typology)"),
 ("Q:cistern:great",U,U,"only cistern named is under a bathhouse room (NZ01 pp. 58-59)"),
 ("S:cistern:in:peristyle_court",U,U,"cistern lies under a bathhouse room (NZ01 pp. 58-59)"),
 ("Q:dovecote:second_upper_storey",U,U,"Netzer 'assumes' the dovecote on the ground floor with a watchtower above (NZ01 pdf 18)"),
 ("S:pit:north_of:gorge_mouth",U,P,"northern wing pools N of the Qelt (INFERENCE)"),
]: put(j,code,s_,l_,b)
put(j,"R:jericho_route",U,U,"the site is Jericho itself (start of the route)")

# ---------------- HYRCANIA
h = "HYR"
for code,s_,l_,b in [
 ("F:fortress",P,P,"Hasmonean fortress rebuilt by Herod (PA02 p. 336)"),
 ("F:cistern",U,P,"20 rock-cut cisterns, first phase 'commonly attributed' Hasmonean/Herodian (PA02 p. 351; HG24 p. 122*)"),
 ("F:pit",U,P,"cisterns (synonym class)"),
 ("F:hollow",U,P,"cisterns (synonym class)"),
 ("F:pool",U,P,"2 built pools; rock-cut double pool NNW (PA89 p. 255; PA02 p. 352)"),
 ("F:reservoir",U,P,"double pool ~8,000 m³ (Feldman 1974 pp. 328-330 via R1 J5)"),
 ("F:conduit",U,P,"northern aqueduct, Hasmonean phase by plaster typology (PA89 pp. 244, 251; R1 J4/J7)"),
 ("F:channels",U,P,"aqueduct branches to the cisterns (PA02 p. 351)"),
 ("F:channel",U,P,"as above"),
 ("F:conduit_head",U,P,"dam 44, intake of the northern aqueduct (PA89 p. 251; R1)"),
 ("F:dam",U,P,"dam 44, 17.5 m (PA89 p. 251)"),
 ("F:bridge",U,P,"aqueduct bridges 46, 48 (PA02 pp. 338, 341, 352)"),
 ("F:valley",P,P,"Naḥal Sekhakha 0.30-0.36 km NNE (R1)"),
 ("F:wadi",P,P,"Naḥal Sekhakha (R1)"),
 ("F:great_wadi",P,P,"Naḥal Sekhakha; the S aqueduct runs along the Qidron (PA02 p. 340)"),
 ("F:road",U,P,"Hyrcania Valley road, Roman pottery at Sites 50, 73 (Mar Saba map pp. 5-6 via R1 J1)"),
 ("F:court",U,P,"summit courtyard above four cisterns; paved court Byzantine (HG24 p. 122*)"),
 ("F:guard_post",U,P,"Area B 'guard post or watchtower' (HG24 pp. 119*-120*); Hasmonean tower W-1 (p. 125*)"),
 ("F:wall",U,P,"fortification wall, Herodian proposal (HG24 p. 121*)"),
 ("F:enclosure",U,P,"fortification (HG24)"),
 ("F:monument",U,P,"'monument' 300 m SW, Herodian per Wright 1961 pp. 14-16; funerary only conjectured (HG24 p. 106* n. 4)"),
 ("F:tomb",U,P,"cemetery at the east foot, Herodian grave goods (Wright 1961 pp. 16-17 via R1)"),
 ("F:cairn",U,P,"grave 'mini-tumulus' ~1.25 m (Wright 1961 p. 16 via R1)"),
 ("F:heap",U,P,"as above"),
 ("F:cave",U,U,"'caverns' on the upper S slope; Byzantine tomb-cave (HG24 pp. 109*, 107* n. 7)"),
 ("F:chamber",U,P,"subterranean vaulted space (HG24 p. 111*)"),
 ("F:underground_chamber",U,P,"subterranean vaulted space reached by a looter's pit (HG24 pp. 111*-112*)"),
 ("F:house",U,P,"fortress-palace"),
 ("F:steps",U,P,"stepped tunnels at the cliff foot (R16 ST1, ST2)"),
 ("F:spiral_stair",U,U,"none recorded"),
 ("F:mountain",P,P,"mount (HG24 p. 103*)"),
 ("F:gorge_mouth",U,U,"not recorded"),
 ("F:fissure",U,U,"Wright's 'sharp cleft' is the quarried saddle (R1 J5)"),
 ("F:peristyle_court",U,U,"no peristyle reported (HG24; R9)"),
 ("F:treasury_house",U,P,"desert fortresses guarded part of the royal treasury (NZ01 pdf 72)"),
 ("Q:reservoir:great",U,P,"double pool ~8,000 m³ (R1 J5)"),
 ("Q:reservoir:northern",U,P,"northern member of the double pool (PA89 p. 255; entry29_hyrcania assessment)"),
 ("Q:cistern:great",U,P,"'two immense rock-hewn' cisterns (HG24 p. 122*)"),
 ("Q:cistern:plastered",U,P,"'thick layer of hydraulic plaster' (PA02 p. 351)"),
 ("Q:cistern:channel",U,P,"aqueduct branches supply the cisterns (PA02 p. 351)"),
 ("S:cistern:of:channels",U,P,"as above"),
 ("S:channels:fed_from:great_wadi",U,P,"northern aqueduct from dam 44 in Naḥal Sekhakha (PA89 p. 251)"),
 ("S:conduit:to:reservoir",U,P,"aqueduct to the pools (PA02 pp. 351-352)"),
 ("S:conduit:to:pool",U,P,"as above"),
 ("Q:conduit_head:north_side",U,P,"northern aqueduct runs S from its head (R1 J4-flow)"),
 ("S:tomb:in:wadi",U,P,"stepped tunnels in Wadi Abu Shuʿle, Gutfeld's tomb suggestion (R16 lenient)"),
 ("S:cistern:in:court",U,P,"courtyard above four cisterns (HG24 p. 122*)"),
 ("S:cistern:under:court",U,P,"as above"),
]: put(h,code,s_,l_,b)
put(h,"R:jericho_route",P,P,"Hyrcania Valley road D (Mar Saba map pp. 5-6; R1 J1 pass)")

# ---------------- HERODIUM
he = "HER"
for code,s_,l_,b in [
 ("F:fortress",P,P,"mountain palace-fortress (NZ81 ch. V)"),
 ("F:guard_post",P,P,"four towers incl. the eastern round tower (NZ81 ch. V 'Herodian multi-storeyed towers')"),
 ("F:upper_storey",P,P,"multi-storeyed towers (NZ81 ch. V)"),
 ("F:peristyle_court",P,P,"peristyle court cleared 1968-69 (NZ81 ch. II; R9 H1)"),
 ("F:court",P,P,"as above"),
 ("F:cistern",P,P,"cisterns on the NE slope 'belong to the Herodian period' (NZ81 ch. II); medium cistern at SE corner of the court (NZ10 p. 103 via R9)"),
 ("F:pit",P,P,"cisterns (synonym class)"),
 ("F:hollow",P,P,"cisterns (synonym class)"),
 ("F:pool",P,P,"Lower Herodium pool complex (NZ81 ch. III)"),
 ("F:reservoir",P,P,"pool, ~10,000 m³, 'main water reservoir of the site' (NZ81 ch. VI)"),
 ("F:conduit",P,P,"Herod's aqueduct from Urtas to the pool complex (NZ81 ch. III, boundaries and water systems)"),
 ("F:channels",P,P,"water channels (NZ81 ch. III)"),
 ("F:channel",P,P,"as above"),
 ("F:garden",P,P,"gardens of the pool complex (NZ81 ch. III)"),
 ("F:steps",P,P,"straight stairway up the NE slope (NZ81 ch. II, V)"),
 ("F:bathhouse",P,P,"Roman bath on the summit; tepidarium round room (NZ81 ch. II)"),
 ("F:cool_room",U,P,"frigidarium of the summit bath (BK)"),
 ("F:monument",P,P,"Herod's mausoleum on the NE slope (NZ10 pp. 84-90 via R9)"),
 ("F:mausoleum",P,P,"as above"),
 ("F:tomb",P,P,"as above"),
 ("F:mound",P,P,"artificial mound/mountain (NZ81 ch. II, Schick's 'tumulus')"),
 ("F:mountain",P,P,"the mountain (NZ81)"),
 ("F:chamber",P,P,"vaulted lower halls, storage hall B20 (NZ81 ch. III)"),
 ("F:underground_chamber",U,P,"underground tunnels integrated with cisterns, mainly Bar Kokhba (NZ81 ch. II)"),
 ("F:terrace",U,P,"the 'course' terrace (NZ81 ch. III)"),
 ("F:house",P,P,"large palace A101 (NZ81 ch. III)"),
 ("F:enclosure",U,P,"fortress walls"),
 ("F:wall",U,P,"fortress walls"),
 ("F:spring",A,A,"no spring; water from Urtas and cisterns (NZ81 ch. III)"),
 ("F:dovecote",U,U,"none recorded in the text read"),
 ("Q:reservoir:great",P,P,"~10,000 m³ pool (NZ81 ch. VI)"),
 ("Q:cistern:great",U,P,"'two large water cisterns' (NZ81 ch. II); the court cistern is 'medium-sized' (NZ10 p. 103)"),
 ("S:cistern:in:peristyle_court",U,P,"medium cistern at the SE corner of the courtyard, predates the palace (NZ10 p. 103 via R9)"),
 ("S:conduit:to:reservoir",P,P,"Urtas aqueduct to the pool complex (NZ81 ch. III)"),
 ("S:conduit:to:pool",P,P,"as above"),
 ("Q:cistern:plastered",U,P,"Herodian cisterns (typology)"),
]: put(he,code,s_,l_,b)

# ---------------- MASADA (outside the region; scored and marked)
m = "MAS"
for code,s_,l_,b in [
 ("F:fortress",P,P,"palatial fortress (NZ01 pdf 83)"),
 ("F:dovecote",P,P,"three columbarium towers, first Herodian phase (NZ01 pdf 86, Fig. 100)"),
 ("F:guard_post",U,P,"towers of the casemate wall (BK; Josephus BJ 7.286 text)"),
 ("F:wall",U,P,"casemate wall (BK)"),
 ("F:enclosure",U,P,"casemate wall (BK)"),
 ("F:cistern",P,P,"cisterns on the NW slope; two possibly Hasmonean (NZ01 pdf 85, 92)"),
 ("F:pit",P,P,"cisterns (synonym class)"),
 ("F:hollow",P,P,"cisterns (synonym class)"),
 ("F:reservoir",U,P,"'water system on a giant scale' on the NW slope (NZ01 pdf 92)"),
 ("F:pool",P,P,"swimming pool 18×13 m (NZ01 pdf 86, Fig. 101)"),
 ("F:immersion",P,P,"Western Palace pool 'served as a ritual bath' (NZ01 pdf 89); stepped pool on the middle terrace (pdf 96)"),
 ("F:bathhouse",P,P,"large bathhouse; Western Palace bath; small Greek-Hasmonean bathhouse (NZ01 pdf 86, 89, 97)"),
 ("F:cool_room",P,P,"frigidarium in the form of a stepped pool, lower terrace bath (NZ01 pdf 97)"),
 ("F:basin",P,P,"basin set into a wall in a decorated niche, Western Palace bathroom (NZ01 pdf 89)"),
 ("F:court",P,P,"Western Palace courtyard 12.0×10.5 m (NZ01 pdf 86)"),
 ("F:peristyle_court",U,P,"lower terrace hall flanked by porticoes; semicircular colonnade (NZ01 pdf 95-96; R9 MA)"),
 ("F:stoa",P,P,"porticoes of the lower terrace hall (NZ01 pdf 96)"),
 ("F:upper_storey",P,P,"second floor of the Western Palace (NZ01 pdf 89)"),
 ("F:spiral_stair",P,P,"stairwells with a central pillar (NZ01 pdf 98)"),
 ("F:steps",P,P,"stairwells of the Northern Palace (NZ01 pdf 96)"),
 ("F:terrace",P,P,"Northern Palace's three terraces (NZ01 pdf 94)"),
 ("F:garden",U,P,"formal garden (viridarium) on the upper terrace, Netzer's view (NZ01 pdf 95)"),
 ("F:chamber",P,P,"stone-vaulted storerooms (NZ01 pdf 98)"),
 ("F:underground_chamber",U,P,"cellar below the eastern portico (NZ01 pdf 97)"),
 ("F:house",P,P,"palaces"),
 ("F:fissure",P,P,"'holes and fissures in the bedrock' at the Northern Palace (NZ01 pdf 98); natural"),
 ("F:mountain",P,P,"rock mount (NZ01 pdf 83)"),
 ("F:conduit",U,P,"aqueducts from Wadi Masada and Wadi Ben Yair with dams (BK)"),
 ("F:channels",U,P,"as above (BK)"),
 ("F:channel",U,P,"as above (BK)"),
 ("F:dam",U,P,"as above (BK)"),
 ("F:valley",P,P,"wadis flanking the rock (NZ01 pdf 83 setting; BK names)"),
 ("F:wadi",P,P,"as above"),
 ("F:great_wadi",U,P,"Wadi Masada / Ben Yair (BK)"),
 ("F:road",U,P,"Snake Path on the eastern slope (NZ01 pdf 82 Fig. 98)"),
 ("F:east_gate",U,P,"Snake Path gate on the east (BK, Yadin)"),
 ("F:tomb",U,P,"Cave 2001 human remains (BK)"),
 ("F:cave",U,P,"cliff caves incl. Cave 2001 (BK)"),
 ("F:treasury_house",U,P,"desert fortresses guarded part of the royal treasury (NZ01 pdf 72)"),
 ("Q:cistern:great",U,P,"giant water system, NW slope (NZ01 pdf 92)"),
 ("Q:reservoir:great",U,P,"as above"),
 ("Q:cistern:plastered",U,P,"plaster of the cisterns studied (NZ01 pdf 85)"),
 ("Q:cistern:channel",U,P,"cisterns fed by channels (BK)"),
 ("S:cistern:of:channels",U,P,"as above (BK)"),
 ("S:channels:fed_from:great_wadi",U,P,"channels from Wadi Masada and Ben Yair (BK)"),
 ("S:conduit:to:reservoir",U,P,"as above (BK)"),
 ("S:conduit:to:pool",U,P,"as above (BK)"),
 ("S:dovecote:in:fortress",P,P,"columbarium towers on the fortress summit (NZ01 pdf 86)"),
 ("S:cool_room:of:house",P,P,"frigidarium of the Northern Palace lower-terrace bath (NZ01 pdf 97)"),
 ("S:basin:of:bathhouse",P,P,"Western Palace bathroom basin (NZ01 pdf 89)"),
 ("Q:fortress:south_district",U,P,"Masada lies in the south of Judaea (INFERENCE)"),
]: put(m,code,s_,l_,b)

# ---------------- KYPROS
k = "KYP"
for code,s_,l_,b in [
 ("F:fortress",P,P,"Hasmonean fortress rebuilt by Herod (NZ01 pdf 76-77; BJ 1.417)"),
 ("F:cistern",P,P,"Hasmonean cistern; two or three cisterns below the summit building (NZ01 pdf 77-78)"),
 ("F:pit",P,P,"cisterns (synonym class)"),
 ("F:hollow",P,P,"cisterns (synonym class)"),
 ("F:immersion",P,P,"Hasmonean stepped pool (mikveh or bath) (NZ01 pdf 77)"),
 ("F:pool",P,P,"stepped pools (NZ01 pdf 77-78)"),
 ("F:bathhouse",P,P,"two bathhouses (NZ01 pdf 77-79)"),
 ("F:cool_room",P,P,"small frigidarium in the form of a stepped pool (NZ01 pdf 77)"),
 ("F:basin",P,P,"large marble washbasin in the caldarium (NZ01 pdf 77)"),
 ("F:dovecote",U,P,"round watchtower which 'apparently also contained a columbarium', Hasmonean (NZ01 pdf 77)"),
 ("F:guard_post",P,P,"round watchtower (NZ01 pdf 77)"),
 ("F:upper_storey",P,P,"second story attested by fallen remains (NZ01 pdf 78)"),
 ("F:court",U,P,"hall or courtyard ~9×10 m (NZ01 pdf 79)"),
 ("F:peristyle_court",U,P,"hall or courtyard with Corinthian columns (NZ01 pdf 79)"),
 ("F:chamber",P,P,"cistern 'possibly used as a cellar' (NZ01 pdf 78)"),
 ("F:underground_chamber",U,P,"as above"),
 ("F:house",P,P,"palace"),
 ("F:conduit",P,P,"conduit from the springs of Wadi Qelt, completed under Herod (NZ01 pdf 73)"),
 ("F:channels",U,P,"water system (NZ01 pdf 73)"),
 ("F:road",P,P,"Jerusalem-Jericho road along Wadi Qelt (NZ01 pdf 76)"),
 ("F:valley",P,P,"Wadi Qelt (NZ01 pdf 76)"),
 ("F:wadi",P,P,"Wadi Qelt"),
 ("F:great_wadi",U,P,"Wadi Qelt"),
 ("F:mountain",P,P,"mountaintop (NZ01 pdf 77)"),
 ("F:terrace",U,P,"lower level area ~30 m below the summit (NZ01 pdf 77)"),
 ("F:treasury_house",U,P,"desert fortresses guarded part of the royal treasury (NZ01 pdf 72)"),
 ("S:dovecote:in:fortress",U,P,"tower on the lower level of the fortress (NZ01 pdf 77)"),
 ("S:cool_room:of:house",P,P,"frigidarium of the summit bath (NZ01 pdf 77)"),
 ("S:basin:of:bathhouse",P,P,"washbasin in the caldarium (NZ01 pdf 77)"),
 ("Q:cistern:plastered",U,P,"typology"),
]: put(k,code,s_,l_,b)
put(k,"R:jericho_route",P,P,"overlooks the Jerusalem-Jericho road (NZ01 pdf 76)")

# ---------------- ALEXANDRIUM
a = "ALEX"
for code,s_,l_,b in [
 ("F:fortress",P,P,"fortress (NZ01 pdf 73-74)"),
 ("F:peristyle_court",U,P,"'a peristyle courtyard, or alternatively a hall' 9.6×9.6 m, Herodian (NZ01 pdf 74)"),
 ("F:court",U,P,"as above"),
 ("F:cistern",P,P,"small vaulted Hasmonean cistern below the court (NZ01 pdf 74); cistern on the E side, Hasmonean-1st c. CE (MHCS4 p. 471)"),
 ("F:pit",P,P,"cisterns (synonym class)"),
 ("F:hollow",P,P,"cisterns (synonym class)"),
 ("F:pool",P,P,"small pool on the E side (MHCS4 p. 471)"),
 ("F:conduit",U,P,"siphon/aqueduct, Hellenistic per caption (MHCS4 pp. 454-456; Amit 1989)"),
 ("F:channels",U,P,"as above"),
 ("F:channel",U,P,"as above"),
 ("F:chamber",U,P,"vaulted structure (cistern?) at the base of a terrace (NZ01 pdf 74)"),
 ("F:terrace",U,P,"terrace above the courtyard (NZ01 pdf 74)"),
 ("F:wall",P,P,"Hasmonean fortification walls (NZ01 pdf 73)"),
 ("F:enclosure",P,P,"as above"),
 ("F:mountain",P,P,"mountaintop (NZ01 pdf 73)"),
 ("F:road",U,P,"main road Judaea-Galilee (NZ01 pdf 73)"),
 ("F:house",U,P,"palatial wing"),
 ("F:treasury_house",U,P,"desert fortresses guarded part of the royal treasury (NZ01 pdf 72)"),
 ("Q:cistern:great",A,A,"the only cistern under the court is 'small' (NZ01 pdf 74) [fail (c) as R9]"),
 ("S:cistern:in:peristyle_court",U,P,"small vaulted cistern beneath the court, predating it (NZ01 pdf 74)"),
]: put(a,code,s_,l_,b)
put(a,"R:jericho_route",U,P,"on the Jericho-Beth Shean road (NZ01 pdf 73)")

# ---------------- TEMPLE MOUNT (surveys and descriptions only)
t = "TM"
for code,s_,l_,b in [
 ("F:cistern",P,P,"G&J Fig. 104 p. 230 marks Cisterns 29 and 15 on the 2nd c. BCE map (WC84 extract, G&J first-hand note)"),
 ("F:pit",P,P,"cisterns (synonym class)"),
 ("F:hollow",P,P,"cisterns (synonym class)"),
 ("F:reservoir",U,U,"W8 'Great Sea' undated (WC84 pp. 219-220)"),
 ("F:court",P,P,"outer court (Josephus BJ 5.190-192 via R9)"),
 ("F:peristyle_court",P,P,"court enclosed by double stoai (BJ 5.190-192; text)"),
 ("F:stoa",P,P,"Royal Stoa; Solomon's Portico (AJ 15.411, 20.221; text)"),
 ("F:exedra",P,P,"exedrae (Josephus BJ 6.150, 6.220 via R9; text)"),
 ("F:east_gate",P,P,"Temple's eastern gate (m. Middot 1:3; Golden Gate on ancient gate foundations, WC84 p. 141)"),
 ("F:wall",P,P,"Herodian enclosure walls (Southern Wall reports; WC84)"),
 ("F:enclosure",P,P,"Herodian enclosure"),
 ("F:underground_chamber",P,P,"c. 45 subterranean chambers (G&J 1994 pp. 150-153 via R9)"),
 ("F:chamber",P,P,"as above"),
 ("F:steps",P,P,"stairs into W8, W5, W22 (WC84 pp. 218-222); undated, but steps of the Temple courts in Middot (text)"),
 ("F:spiral_stair",P,P,"winding stair (mesibbah) in the Temple building (m. Middot 4:5; text)"),
 ("F:immersion",P,P,"immersion place under the Temple court (m. Middot 1:9; text)"),
 ("F:treasury_house",P,P,"Temple treasuries (Josephus BJ 5.200; text)"),
 ("F:platform",P,P,"inner platform (WC84 p. 225)"),
 ("F:mountain",P,P,"Har ha-Bayit (m. Middot 1:1; text)"),
 ("F:valley",P,P,"Kidron valley to the east (text: John 18:1)"),
 ("F:wadi",P,P,"Kidron (נחל קדרון)"),
 ("F:great_wadi",U,P,"Kidron"),
 ("F:conduit",U,P,"conduits into W8 and W15 (WC84 pp. 220-221), undated; low-level aqueduct (BK)"),
 ("F:channels",U,P,"as above"),
 ("F:channel",U,P,"as above"),
 ("F:pillar",U,U,"rock piers of W8, central pillar of W9: undated (WC84 pp. 219-220)"),
 ("F:drain",U,U,"surface drainage ducts into W9 (WC84 p. 220), undated"),
 ("F:house",P,P,"the Temple ('the House')"),
 ("F:upper_storey",U,P,"upper chambers (Middot; text)"),
 ("F:guard_post",U,P,"towers/Antonia (text)"),
 ("F:road",P,P,"roads to the gates (text)"),
 ("Q:cistern:great",U,U,"W8 'largest of all the Sanctuary tanks' but undated (WC84 p. 220)"),
 ("Q:reservoir:great",U,U,"as above"),
 ("Q:cistern:upper_opening",U,U,"W8 numerous manholes, undated (WC84 p. 220)"),
 ("Q:cistern:plastered",U,U,"W8 plastered, undated (G&J p. 33)"),
 ("Q:cistern:channel",U,U,"conduits into W8 and W15, undated"),
 ("S:cistern:in:peristyle_court",U,P,"W8 in the open area between the Aqṣā and the platform (map-scaled INFERENCE, WC84 extract)"),
 ("S:cistern:opposite_19c:east_gate",A,A,"'No cistern is recorded within 7-10 m of the gate'; W15 is 25-30 m W (WC84 p. 221; G&J Fig. 10)"),
 ("S:underground_chamber:in:court",P,P,"subterranean chambers under the platform (G&J 1994 via R9 C1)"),
 ("S:cistern:in:underground_chamber",U,U,"no chamber with a cistern opening in its floor recorded (WC84 extract §4)"),
 ("S:cistern:under:steps",U,U,"W33 'under the stairs leading to the passage from the Double Gate', undated (WC84 p. 225)"),
 ("S:steps:of:cistern",U,U,"W8 staircase, undated (WC84 p. 220)"),
 ("S:steps:of:pit",U,U,"as above"),
]: put(t,code,s_,l_,b)
put(t,"R:jericho_route",P,P,"Jericho-Jerusalem road (Luke 10:30; text)")

# ---------------- CITY OF DAVID / SILOAM
c = "CD"
for code,s_,l_,b in [
 ("F:pool",P,P,"Second Temple stepped Siloam pool, mid-1st c. BCE-70 CE (CDx: Grossberg 2011 p. 105; R&S 2010 p. 29)"),
 ("F:reservoir",P,P,"reservoir in tower L119 with seven steps and central pillar base (CDx: WB & Szanton 2014 pp. 3-4)"),
 ("F:cistern",U,P,"L119 reservoir (as above)"),
 ("F:pit",U,P,"as above"),
 ("F:hollow",U,P,"as above"),
 ("F:immersion",P,P,"stepped plastered pool L124, late Second Temple (CDx: WB & Szanton 2014 p. 4; WB & Hagbi 2022 p. 3)"),
 ("F:steps",P,P,"pool steps (R&S 2010 p. 29); stepped street (S&R 2011 p. 174)"),
 ("F:conduit",P,P,"Channel IV, the Siloam pool's feed channel, cut in the Second Temple period (Grossberg 2011 p. 76 n. 4)"),
 ("F:channels",P,P,"Channel IV; drainage channels (CDx)"),
 ("F:channel",P,P,"as above"),
 ("F:drain",P,P,"great (western) drainage channel, 1st c. CE (S&R 2011 pp. 174-181)"),
 ("F:water_outlet",P,P,"Siloam tunnel outlet (in use; Grossberg 2011 p. 72)"),
 ("F:spring",P,P,"Gihon"),
 ("F:wall",P,P,"First Wall W11, Hasmonean (WB & Szanton 2014 p. 3)"),
 ("F:enclosure",P,P,"city wall"),
 ("F:guard_post",P,P,"tower L119, Hasmonean (WB & Szanton 2014 pp. 3-4)"),
 ("F:basin",P,P,"small round plastered basin, Herodian (WB & Lavi 2013 pp. 1-2)"),
 ("F:dam",U,U,"dam 'Iron Age II or later' (WB & Hagbi 2022 p. 2)"),
 ("F:bathhouse",U,U,"'BATHS' south of the gate, undated (R&S 2010 p. 37)"),
 ("F:trough",U,U,"no trough recorded in the pool sources (CDx negative search)"),
 ("F:terrace",P,P,"terrace walls W18, W20, W25, 1st c. CE (WB & Szanton 2014 p. 4)"),
 ("F:valley",P,P,"Kidron and Tyropoeon (CDx)"),
 ("F:wadi",P,P,"Kidron"),
 ("F:great_wadi",U,P,"Kidron"),
 ("F:stoa",U,P,"stylobate and column drums on the Siloam esplanade (Reich & Shukron in Galor & Avni 2011 p. 245 via R9)"),
 ("F:court",U,P,"paved plaza north of the pool (S&R 2011 p. 177)"),
 ("F:tomb",U,U,"Iron Age tombs only in the site reports (not in the window)"),
 ("F:road",P,P,"stepped street (S&R 2011 p. 174)"),
 ("F:house",U,P,"dwellings (CDx)"),
 ("Q:drain:great",P,P,"'great (western) channel' (S&R 2011 p. 174)"),
 ("Q:reservoir:great",U,P,"Siloam pool, large (R&S 2010)"),
 ("Q:cistern:plastered",P,P,"L119 reservoir grey hydraulic plaster (WB & Szanton 2014 pp. 3-4)"),
 ("Q:cistern:pillar",P,P,"central pillar base in L119 (WB & Szanton 2014 pp. 3-4)"),
 ("S:conduit:to:pool",P,P,"Channel IV feeds the pool (Grossberg 2011 p. 76 n. 4)"),
 ("S:conduit:to:reservoir",P,P,"as above"),
 ("Q:conduit:enterable",U,P,"Siloam tunnel (Iron II, in use)"),
 ("S:drain:of:cistern",U,U,"the great channel bypasses the pool (S&R 2011 p. 177)"),
 ("S:basin:in:valley",U,P,"pool 'at the end of the central valley' (Grossberg 2011 p. 72)"),
 ("S:steps:of:pool",P,P,"pool stairs (R&S 2010 p. 29)"),
]: put(c,code,s_,l_,b)
put(c,"R:jericho_route",P,P,"Jericho road (Luke 10:30; text)")

# ---------------- NAMES (site-level; INFERENCE notes)
NAMES = {}
def nm(name, default, over=None, basis=""):
    NAMES[name] = dict(default=default, over=over or {}, basis=basis)
nm("Achor", U, {"HER":A,"MAS":A,"ALEX":A,"TM":A,"CD":A}, "Josh 15:7 and Eusebius put Achor on Judah's NE border near Jericho; sites far from that zone fail (INFERENCE)")
for x in ["Kohlit","Manos","Melah","MDH","Mattiyah","Asla","Solomon_trench","Shallum_trench","Kippa","Queen","HighPriest","Qi","Haqqos","Kozeba","Ahor","Natof","BethTamar","Pele","Nab","Zered","Rahil","Zadok","BeneHaAm","Horites"]:
    nm(x, U, None, "unlocated, or located only by modern or later tradition")
nm("Secacah", U, {"JER":A,"ALEX":A,"TM":A,"CD":A}, "Josh 15:61 wilderness-of-Judah town; entry 24 itself separates it from Jericho (INFERENCE)")
nm("Solomon_reservoir", U, {"CD":P}, "Josephus BJ 5.145: the First Wall bends east 'to Solomon's pool' (τὴν Σολομῶνος κολυμβήθραν) above Siloam, toward Ophlas")
nm("Doq", A, None, "Dok/Dagon = Jebel Qarantal (1 Macc 16:15; Josephus; NZ01 pdf 74); none of the nine sites")
nm("Kidron", A, {"TM":P,"CD":P,"HYR":"U/P"}, "Kidron east of Jerusalem (John 18:1); Hyrcania's S aqueduct runs along the Qidron (PA02 p. 340)")
nm("Shaveh", A, {"TM":U,"CD":U}, "King's Valley, two stades from Jerusalem (Gen 14:17; Josephus AJ 7.243)")
nm("Horon", A, None, "Beth-Horon = Beit ʿUr (secure)")
nm("BethHaKerem", A, {"HER":U}, "Jer 6:1 (with Tekoa), Neh 3:14; proposals Ramat Raḥel / ʿAin Karim")
nm("Absalom", A, {"TM":U,"CD":U}, "2 Sam 18:18; Josephus AJ 7.243: two stades from Jerusalem")
nm("Gerizim", A, None, "Mount Gerizim (secure)")
nm("BethSham", A, None, "Beth Shean / Beth Shemesh (both secure; neither is a site here)")
nm("Millo", A, {"TM":U,"CD":U}, "the Millo of Jerusalem (2 Sam 5:9) (alt reading only)")
nm("wood_court", A, {"TM":P}, "chamber of wood in the Temple court (m. Middot 2:5; text) (alt reading only)")
nm("Cypros", A, {"KYP":P}, "Cypros = Kypros (BJ 1.417) (alt reading only)")
nm("Masada", A, {"MAS":P}, "Masada (alt reading only)")
nm("Siloam", A, {"CD":P}, "Siloam (alt reading only)")
nm("Jericho", A, {"JER":P}, "Jericho (alt reading only)")

def name_verdict(name, site):
    d = NAMES[name]; x = d["over"].get(site, d["default"])
    if "/" in x: s_, l_ = x.split("/")
    else: s_ = l_ = x
    return [s_, l_, d["basis"]]

# synonym classes for F lookups (a feature passes if any member passes)
SYN = {
 "pit": ["pit","cistern"], "hollow": ["hollow","pit","cistern"], "reservoir": ["reservoir","pool"],
 "pool": ["pool","reservoir"], "basin": ["basin","pool"], "chamber": ["chamber","underground_chamber"],
 "burial_chamber": ["burial_chamber","tomb"], "tomb": ["tomb","burial_chamber","mausoleum"],
 "heap": ["heap","cairn","great_heap"], "valley": ["valley","wadi"], "wadi": ["wadi","valley"],
 "guard_post": ["guard_post"], "earth_pit": ["earth_pit"],
}

if __name__ == "__main__":
    out = sys.argv[1]
    names_full = {n: {s: name_verdict(n, s) for s in SITES} for n in NAMES}
    js = json.dumps(dict(sites=SITES, inventory=INV, names=names_full, synonyms=SYN), ensure_ascii=False, indent=1)
    open(out + ".json", "w", encoding="utf-8").write(js)
    L = ["# Run 22 site inventories (written before step 2)", "",
         "Verdicts strict/lenient. Unlisted feature = U. Sources and conventions: see scripts/inventory.py header.", ""]
    for s, meta in SITES.items():
        L += [f"## {s}: {meta['name']} ({meta['region']})", "", "| Code | Strict | Lenient | Basis |", "|---|---|---|---|"]
        for code, (a_, b_, c_) in sorted(INV[s].items()):
            L.append(f"| {code} | {a_} | {b_} | {c_} |")
        L.append("")
    L += ["## Names", "", "| Name | " + " | ".join(SITES) + " | Basis |", "|---|" + "---|"*len(SITES) + "---|"]
    for n in NAMES:
        L.append(f"| {n} | " + " | ".join("/".join(names_full[n][s][:2]) if names_full[n][s][0]!=names_full[n][s][1] else names_full[n][s][0] for s in SITES) + f" | {NAMES[n]['basis']} |")
    open(out + ".md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print({s: len(INV[s]) for s in SITES})
