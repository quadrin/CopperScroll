# -*- coding: utf-8 -*-
"""Entry 60 (XII 10-13) ranked search targets. All flagged priority=high.

Reading branches that apply to every target (scored separately):
  RB-M  Milik 1960/1962: pit/'tunnel' (Milik 1960: 'in the Smooth Rock') north of Kohlit,
        'which opens towards the north', tombs at its mouth.
  RB-P  Puech 2006/2015: pit 'situated' (שכנה) on the north of Kohlit, 'its opening hidden'
        (צפון read as 'hidden'), tombs at its mouth.  No orientation constraint.
  RB-L  Lefkovits 2000 / Beyer: 'in Janoah' (שבינח) north of Kohlit — adds a place name;
        the repo plate check does not support the required yod.
  RB-B  'buried at its mouth' (קברין as passive participle; Wikipedia rendering citing
        Lurie 1964): no tomb landmark required.
"""

R = []

def rec(**kw):
    R.append(kw)

RB_TEXT = ("Scored per reading branch: RB-M (Milik: mouth faces north; tombs at mouth), RB-P (Puech: mouth hidden/concealed; tombs at mouth; no orientation), "
           "RB-L (Lefkovits/Beyer: 'in Janoah' — requires a Janoah toponym north of Koḥlit), RB-B ('buried at its mouth': no tomb requirement).")
DEPOSIT = ("'A copy of this document, and its explanation, and their measurements, and the details of each and every one' — a written document (material unstated) "
           "duplicating and/or keying the list; any inscribed list of hiding places with measurements found at the pit mouth is an L4 result.")
REPORT60 = ["for every pit/shaft/cistern/tomb in the target sector: surveyed coordinates with datum and accuracy, mouth outline, depth, fill sequence and dating",
            "mouth/entrance azimuth for inclined shafts or side openings (true north), and evidence of concealment (blocking stones, covering slabs, fill)",
            "distances (and azimuths) from each pit mouth to every tomb entrance within 20 m, with tomb dates and reuse phases",
            "whether each pit was open/accessible in the 1st c. BCE–2nd c. CE (sealing deposits, reuse finds)",
            "bearing and distance of each pit from the Koḥlit anchor (tell summit / spring) and from the other pits (to assign 'eastern', entry 19)",
            "coverage map of excavated/surveyed vs unsurveyed ground in the sector, so absence can be scored",
            "any inscribed objects (copper, parchment, papyrus, ostraca, wood) with findspot x,y,z"]
CONFIRM60 = ("L2: in the sector north of the anchor, a pit/shaft that (i) existed and was accessible within 50 BCE–135 CE, (ii) has one or more tomb entrances at its mouth "
             "(report the distances; ≤5 m is the default 'at its mouth' threshold), (iii) under RB-M has its mouth/entrance facing north (azimuth 315°–045°), under RB-P shows evidence of concealment, "
             "and (iv) belongs to a group of ≥2 pits in the sector (entry 19's 'eastern pit'). L3: a cut, niche or disturbance of that date at the mouth. L4: an inscribed list of hiding places/measurements.")
MISS60 = ("Target-level MISS: a complete, published systematic survey or excavation of the whole north sector of the anchor (coverage map required) records every pit/shaft and none meets (i)–(iii) "
          "under the branch being scored. Feature-level MISS: the mouth zone of a qualifying pit is excavated to its rock floor with no disturbance of the period.")
INCONC60 = "Partial coverage; pits undated; mouth orientation or tomb distances not recorded; Koḥlit anchor unconfirmed (always caps the result at 'conditional'). "

rec(id="P60-T1", entry="60", rank=1, branch="Koḥlit = Tell es-Sultan; target = the cemetery zone north/north-west of the tell",
    reading_assumed=RB_TEXT, reading_editions=["Milik 1960 (item 64); 1962", "Puech 2006 p. 175 n. 49; 2015 pp. 13–14 n. 49", "Lefkovits 2000", "Lurie 1964 (via Wikipedia)"],
    reading_status="Koḥlit secure at XII 10; second word disputed (plates fit Puech's 'situated'); צפון = 'north' (Milik) or 'hidden' (Puech); קברין = 'tombs' or 'buried'",
    place_id="tell_es_sultan",
    feature_type="pit/shaft north of the Koḥlit anchor with tombs at its mouth (one of ≥2 pits there)",
    feature_detail=("Candidate feature classes (INFERENCE, low): (a) a Bronze Age vertical shaft tomb reopened/reused in the Roman period, whose shaft is the 'pit'; "
                    "(b) a cistern or storage pit amid Roman-period graves; (c) a Qumran-type shaft-grave field with a larger pit among the graves."),
    orientation="north of the anchor (sector 315°–045° from the tell summit; stricter variant 337.5°–022.5°); mouth facing north under RB-M only",
    measures=[], location="Sector north of Tell es-Sultan (anchor ~150 m precision), within the documented cemetery north and west of the tell; distance not stated by the text.",
    confirm=CONFIRM60, miss=MISS60, inconclusive=INCONC60 + "Current state: no pit reported north of the tell.",
    deposit=DEPOSIT, report_extra=REPORT60, priority="high", scorability="feature-level (desk-testable first against published tomb registers)",
    rank_scores={"C1_published_kohlit_proposal": 2, "C2_text_dependency_penalty": 0, "C3_tell_present(entry4)": 2, "C4_spring_or_pool_east(entry11)": 2,
                 "C5_tombs_north_of_anchor": 2, "C6_shaft_or_pit_features": 2, "C7_1st_c_presence_near_target": 2},
    evidence=[("Puech proposes Koḥlit = Tell es-Sultan 'à titre d'hypothèse', north of Hasmonaean/Herodian Jericho.", "Puech 2006 p. 175 n. 49; 2015 pp. 13–14 n. 49 — via shared/readings.json e60-kohlit and repo cycle7 kohlit_pool.md"),
              ("Høgenhaven: Koḥlit perhaps ʿEin Kohel near Carmel (Milik) or Tell es-Sultan north of Jericho (Puech).", "Høgenhaven, Dansk Teologisk Tidsskrift 79 (2016) p. 72 n. 22 — https://tidsskrift.dk/dtt/article/download/105777/154549/217156"),
              ("A large cemetery lies north and west of Tell es-Sultan with tombs from EB I to the Roman period; Puech, citing Kenyon, reports Qumran-type graves on the north side; no pit is reported.", "via downloads/tables_phase5_assessments.csv entry 60 (Sala 2014 p. 117; Puech 2015 pp. 13–14 n. 49)"),
              ("Middle Bronze Jericho had an extensive cemetery with vertical shaft-tombs and underground burial chambers; a scarab came from a cemetery NW of Jericho.", "https://en.wikipedia.org/wiki/Tell_es-Sultan (tertiary)"),
              ("Kenyon, Excavations at Jericho III pp. 173–174 is Puech's cemetery lead.", "via downloads/research_measurements_cycle7_kohlit_pool.md")],
    inference=("Only candidate where all of Koḥlit's landmark classes (tell, spring with pool east, tombs north, shafts) co-occur; still a hypothesis, and 'north' entries could fall anywhere in a wide sector.", "low-medium (that the target zone is right, conditional on Koḥlit = Tell es-Sultan); low overall"),
    sources=["Puech 2006 p. 175 n. 49", "Puech 2015 pp. 13–14 n. 49", "Sala 2014 p. 117", "Kenyon, Excavations at Jericho III pp. 173–174", "SWP III pp. 222–223", "Høgenhaven 2016 DTT 79 pp. 70, 72"])

rec(id="P60-T2", entry="60", rank=2, branch="Koḥlit between ʿAyn el-Ghuweir and ʿAyn et-Turabeh (Tübingen Bible Atlas B V 18); target = cemetery north of the ʿEin el-Ghuweir building",
    reading_assumed=RB_TEXT, reading_editions=["Tübingen Bible Atlas sheet B V 18 (via Puech 2015 p. 14, via repo cycle7)"], reading_status="as P60-T1",
    place_id=None, feature_type="pit/shaft north of the settlement with graves at its mouth",
    feature_detail="ʿEin el-Ghuweir has a cemetery 800 m north of the building with 17 excavated north–south graves dated 1st c. BCE–1st c. CE.",
    orientation="as P60-T1", measures=[], location="ʿEin el-Ghuweir, western Dead Sea shore c. 15 km south of Qumran (not in gazetteer; no coordinate asserted).",
    confirm=CONFIRM60, miss=MISS60, inconclusive=INCONC60 + "Puech objects: no tell (entry 4) and freshwater abundance.",
    deposit=DEPOSIT, report_extra=REPORT60, priority="high", scorability="feature-level once the anchor is fixed",
    rank_scores={"C1_published_kohlit_proposal": 1, "C2_text_dependency_penalty": 0, "C3_tell_present(entry4)": 0, "C4_spring_or_pool_east(entry11)": 1,
                 "C5_tombs_north_of_anchor": 2, "C6_shaft_or_pit_features": 1, "C7_1st_c_presence_near_target": 2},
    evidence=[("Puech p. 14 identifies the Tübingen Bible Atlas B V 18 placement and objects to a missing tell and freshwater abundance; the atlas sheet itself was not inspected.", "via downloads/research_measurements_cycle7_kohlit_pool.md"),
              ("ʿEn el-Ghuweir cemetery: '800 m north of the building, 15 km south of Qumran'; 17 tombs excavated, oriented north–south; 1st c. BCE–1st c. CE.", "Hachlili, 'The Qumran Cemetery: A Reconsideration', in DSS Fifty Years After (2000) pp. 661–667 — via https://cojs.org/the_qumran_cemetery-_a_reconsideration-_rachel_hachlili/")],
    inference=("Tombs north of a period settlement match RB-M/RB-P's tomb clause in kind; the Koḥlit link is cartographic only.", "low"),
    sources=["Puech 2015 p. 14 (via repo)", "Hachlili 2000 pp. 661–667", "Bar-Adon's ʿEn el-Ghuweir excavation report (not read; exact citation not verified here)"])

rec(id="P60-T3", entry="60", rank=3, branch="Koḥlit (Kaḥelet) = ʿEin Samiya / Wadi Kuḥeila, Samarian desert (Zissu 2001); target = shaft-tomb hills by the spring",
    reading_assumed=RB_TEXT + " This target additionally depends on RB-L (Lefkovits's Yanoaḥ reading), per Puech.", reading_editions=["Zissu, PEQ 133 (2001) pp. 145–158", "Zissu, Judea and Samaria Research Studies 10 (2001) pp. 119–136 (Hebrew)"],
    reading_status="depends on 'in Janoah' (RB-L), which the repo plate check does not support", place_id=None,
    feature_type="pit/shaft north of the Kaḥelet anchor with tombs at its mouth",
    feature_detail="The ʿEin Samiya cemetery covers hills (Kh. el-ʿAqibat, Kh. Samiya, Dhahr el-Mirz) with mostly Middle Bronze I shaft tombs; Roman/Byzantine remains and aqueduct traces are reported nearby.",
    orientation="as P60-T1; the anchor (Zissu's 'Tel Kakhelet') must be fixed first from Zissu 2001", measures=[],
    location="ʿEin Samiya, east of Kafr Malik (Ramallah governorate). External reference only: Wikipedia gives 31°59′21″N 35°20′00″E for the village (village-level; not a feature coordinate; not in the project gazetteer).",
    confirm=CONFIRM60, miss=MISS60, inconclusive=INCONC60 + "Zissu's exact anchor and arguments not read (PEQ page returned 403).",
    deposit=DEPOSIT, report_extra=REPORT60, priority="high", scorability="feature-level once Zissu's anchor is read",
    rank_scores={"C1_published_kohlit_proposal": 2, "C2_text_dependency_penalty": -2, "C3_tell_present(entry4)": 1, "C4_spring_or_pool_east(entry11)": 2,
                 "C5_tombs_north_of_anchor": 1, "C6_shaft_or_pit_features": 2, "C7_1st_c_presence_near_target": 1},
    evidence=[("Zissu, 'The Identification of the Copper Scroll's Kahelet at ʿEin Samiya in the Samarian Desert', PEQ 133.2 (2001) 145–158.", "https://cris.biu.ac.il/en/publications/the-identification-of-the-copper-scrolls-kahelet-atein-samiya-in-/ ; https://orion-bibliography.huji.ac.il/node/58804"),
              ("Puech p. 14 says Zissu's proposal depends first on Lefkovits's Yanoaḥ reading at XII 10, which he rejects; plate check fails to support the required yod.", "via downloads/research_measurements_cycle7_kohlit_pool.md; repo plate_check.md"),
              ("ʿAin Samiya goblet came from Tomb 204 in a cemetery covering Kh. el-ʿAqibat, Kh. Samiya and Dhahr el-Mirz; MB I.", "https://en.wikipedia.org/wiki/%27Ain_Samiya_goblet (citing IEJ 21, 1971)"),
              ("Necropolis of >300 tombs in six clusters, mostly MB I shaft tombs; Zissu suggested the site as 'Tel Kakhelet'.", "https://biblewalks.com/samiya (popular source)"),
              ("Hillsides covered with EB, MB I and later tombs; about 150 examined (Lapp; Meshorer; Yevin).", "https://holylandphotos.org/browse/dhahr-mirzbaneh-ein-samiya (popular source)")],
    inference=("Shaft tombs make the 'pit with tombs at its mouth' class abundant here, which lowers the discriminating power of any single hit.", "low"),
    sources=["Zissu 2001 PEQ 133 pp. 145–158", "Zissu 2001 JSRS 10 pp. 119–136", "Shantur & Labadi 1971 IEJ 21; Yeivin 1971 IEJ 21 (via Wikipedia)"])

rec(id="P60-T4", entry="60", rank=4, branch="Qumran–Buqeia regional alternative (repo sequence study)", reading_assumed=RB_TEXT, reading_editions=["repo deeper_analysis_2026-09-30 §2.1"],
    reading_status="as P60-T1", place_id=None, feature_type="pit with tombs at its mouth north of an unnamed Koḥlit anchor in the Qumran–Buqeia district",
    feature_detail="Regional only. Do not merge with Sekakah = Qumran.", orientation="as P60-T1", measures=[], location="District-level; no anchor.",
    confirm="Not scorable until an anchor is proposed.", miss="Not scorable.", inconclusive="Default.", deposit=DEPOSIT, report_extra=REPORT60, priority="high", scorability="not scorable at present",
    rank_scores={"C1_published_kohlit_proposal": 0, "C2_text_dependency_penalty": 0, "C3_tell_present(entry4)": 0, "C4_spring_or_pool_east(entry11)": 1,
                 "C5_tombs_north_of_anchor": 1, "C6_shaft_or_pit_features": 1, "C7_1st_c_presence_near_target": 2},
    evidence=[("Sequence study leaves the Qumran–Buqeia district alternative open; Qumran has small cemeteries to the north and south besides the main one.", "repo research_text_deeper_analysis_2026-09-30.md §2.1, §10 (Wikipedia: Qumran cemetery)")],
    inference=("Regional placeholder.", "low"), sources=["repo deeper_analysis_2026-09-30"])

rec(id="P60-T5", entry="60", rank=None, branch="Koḥlit in Transjordan (Goranson; b. Qiddushin 66a + Jannaeus's campaigns)", reading_assumed=RB_TEXT,
    reading_editions=["Goranson, JJS 43 (1992) 282–287; 'Further Reflections', CSS (2002) 226–232, p. 231"], reading_status="as P60-T1", place_id=None,
    feature_type="pit with tombs at its mouth north of a Transjordanian Koḥlit", feature_detail="No site proposed in the sources read.", orientation="as P60-T1", measures=[],
    location="Unlocated (east of the Jordan).", confirm="Not scorable until a site is proposed.", miss="Not scorable.", inconclusive="Default.", deposit=DEPOSIT, report_extra=REPORT60,
    priority="high", scorability="not scorable at present", rank_scores=None,
    evidence=[("Goranson identifies Koḥlit (also b. Qid 66a) as an area east of the Jordan.", "Cook, review of Copper Scroll Studies, Scriptura 88 (2005) 225–229, citing Goranson CSS p. 231 — https://scriptura.journals.ac.za/pub/article/view/1007/960"),
              ("b. Qiddushin 66a: King Yannai 'went to Koḥalit in the desert and conquered sixty cities there'.", "https://www.sefaria.org/Kiddushin.66a")],
    inference=("'In the desert' does not select Transjordan by itself (repo cycle7).", "medium"), sources=["Goranson 1992; 2002", "b. Qiddushin 66a"])

rec(id="P60-T6", entry="60", rank=None, branch="Koḥlit = ʿEin Kohel near Mount Carmel (Milik, via Massekhet Kelim)", reading_assumed=RB_TEXT,
    reading_editions=["Milik 1962 pp. 274–275, 280–281"], reading_status="as P60-T1", place_id=None, feature_type="pit with tombs at its mouth north of a Carmel spring",
    feature_detail="Puech calls the identification doubtful; the medieval legend does not establish a 1st-c. location.", orientation="as P60-T1", measures=[], location="Unlocated (no coordinate for 'ʿEin Kohel' in sources read).",
    confirm="Not scorable until the spring is located.", miss="Not scorable.", inconclusive="Default.", deposit=DEPOSIT, report_extra=REPORT60, priority="high", scorability="not scorable at present",
    rank_scores=None,
    evidence=[("Milik (1962, 274–275, 280–281) connects Koḥlit with ʿEin Kohel at Mount Carmel mentioned in Massekhet Kelim (cf. Davila 2013, 400 n. 22).", "Høgenhaven 2016 DTT 79 p. 72 n. 22"),
              ("Puech pp. 13–14 reports Milik's southern-Carmel proposal and calls it doubtful.", "via downloads/research_measurements_cycle7_kohlit_pool.md")],
    inference=("", "low"), sources=["Milik DJD III pp. 274–275, 280–281", "Høgenhaven 2016 p. 72 n. 22"])

rec(id="P60-T7", entry="60", rank=None, branch="Koḥlit = ʿAyn Feshkha area (discussed and rejected by Puech)", reading_assumed=RB_TEXT, reading_editions=["Puech 2015 p. 14 (via repo cycle7)"],
    reading_status="as P60-T1", place_id=None, feature_type="pit with tombs at its mouth north of ʿAyn Feshkha", feature_detail="Proposer not identified in the sources read; Puech rejects for absence of a tell.",
    orientation="as P60-T1", measures=[], location="ʿAyn Feshkha (not in gazetteer).", confirm="Not scorable until an anchor is proposed.", miss="Not scorable.", inconclusive="Default.",
    deposit=DEPOSIT, report_extra=REPORT60, priority="high", scorability="not scorable at present", rank_scores=None,
    evidence=[("Puech p. 14 rejects ʿAyn Feshkha for absence of a tell and other contextual considerations.", "via downloads/research_measurements_cycle7_kohlit_pool.md")],
    inference=("", "low"), sources=["Puech 2015 p. 14"])
