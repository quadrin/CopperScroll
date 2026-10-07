# -*- coding: utf-8 -*-
"""Prediction records, part B: entries 46-59 and the Kohlit entries 4, 11, 15, 16, 19.
Entry 60 targets are in records_c.py. Same conventions as records_a.py."""

R = []

def rec(**kw):
    R.append(kw)

# ---------------------------------------------------------------- entry 46
rec(id="P46-A", entry="46", branch="Beth ha-Kerem = Ramat Raḥel; cubits = depth (Milik)",
    reading_assumed="באשיח שיבית הכרם בבואך לסמולו חפור אמות עסר", reading_editions=["Milik 1962 C70, p. 268", "Puech 2006"],
    reading_status="name agreed; 'cubits' vs Milik 1962 'ten feet' (unit open, Q15); depth (Milik) vs distance (Lefkovits)", place_id="ramat_rahel",
    feature_type="large built reservoir; deposit on the left as one enters",
    feature_detail="A large reservoir (not a household cistern) in use in the scroll's period, with a defined entrance (steps/opening).",
    orientation="'on its left' relative to a person entering the reservoir — not a compass bearing",
    measures=[{"cubits": 10, "edition": "Puech 2006 / Milik 1962 (as cubits)", "type": "digging depth (Milik) or distance (Lefkovits)"}],
    location="Ramat Raḥel (gazetteer ~100 m).",
    confirm="L2: a large reservoir at Ramat Raḥel shown in use in the 1st c. BCE–1st c. CE with a defined entrance; L3: period cut 4.45–5.25 m (10 c.) on the left of the entrance (depth model) or at that distance along the left wall (distance model).",
    miss="All large reservoirs at the site shown to be filled/out of use before the 1st c. BCE (the known pool enclosure lay under fill with pottery to the 2nd c. BCE) — a further negative would close the branch.",
    inconclusive="Reservoir use-phase undated; entrance not identified.",
    report_extra=["use/abandonment phase of each reservoir", "entrance position and access direction", "measurements from the entrance on the left side"],
    priority="low", scorability="feature-level",
    evidence=[("The known pool enclosure lies beneath fill containing pottery as late as the 2nd c. BCE; in the scroll's period the site was a small village with ritual baths.", "via repo phase5_summary §3 (Lipschits et al. 2006–07 report pp. 15–18; INJ 17 pp. 59–60)"),
              ("Aharoni's identification of Beth ha-Kerem partly rests on the scroll's own sequence.", "via repo phase5_summary §3 (Lefkovits p. 333 n. 11)")],
    inference=("The known pool already fails the period test; only an unknown reservoir could confirm.", "medium"),
    sources=["Lipschits et al., Ramat Raḥel 2006–07 report pp. 15–18", "INJ 17 pp. 59–60", "HA-ESI 137"])
rec(id="P46-B", entry="46", branch="Beth ha-Kerem = ʿAin Karim (Conder)", reading_assumed="as P46-A", reading_editions=["Conder, SWP III (1883) p. 20"], reading_status="as P46-A",
    place_id=None, feature_type="large reservoir at ʿAin Karim", feature_detail="Conder's identification of Beth ha-Kerem.", orientation="as P46-A",
    measures=[{"cubits": 10, "edition": "as P46-A", "type": "depth or distance"}], location="ʿAin Karim (not in gazetteer; no coordinate asserted).",
    confirm="As P46-A at ʿAin Karim.", miss="Feature-level only.", inconclusive="Default.", report_extra=["reservoir phase"], priority="low", scorability="area-level",
    evidence=[("Conder: ʿAin Karim.", "SWP III p. 20 via shared/readings.json e46")], inference=("", "low"), sources=["SWP III p. 20"])

# ---------------------------------------------------------------- entry 48
rec(id="P48-A", entry="48", branch="Absalom's monument = the standing Kidron monument (Puech, Høgenhaven)",
    reading_assumed="תחת יד אבשלום מן הצד המערבי חפור אמות שתין עסרה (twelve)", reading_editions=["Puech 2006 p. 199", "Høgenhaven 2020"],
    reading_status="name agreed; 'cubits' vs Milik 'feet'; Lefkovits: יד may mean 'place'", place_id="jer_kidron_mon",
    feature_type="free-standing monument named for Absalom; deposit on its west side",
    feature_detail="The Kidron monument's decorated façade faces west toward the Temple Mount.",
    orientation="west side of the monument", measures=[{"cubits": 12, "edition": "Puech 2006", "type": "digging depth"}],
    location="Kidron valley at the monuments (~100 m).",
    confirm="L2: evidence that the Kidron monument was called Absalom's in the 1st c. CE (needed for the identification); L3: period cut 5.3–6.3 m (12 c.) below the ancient surface on the west side.",
    miss="West-side ancient surface excavated to ≥6.3 m depth (or bedrock) without period cut; note the 1st-c. monument may postdate the list if the list is earlier.",
    inconclusive="Surface level on the west side not defined; Absalom name unattested in period.",
    report_extra=["ancient ground level west of the monument", "bedrock depth", "depth excavated and fill dates", "any period label/inscription naming Absalom"],
    priority="low", scorability="feature-level",
    evidence=[("The standing monument is dated by style to the 1st c. CE, but its earliest labels (4th c.) name Zacharias.", "via repo phase5_summary §4 (Zias 2023)"),
              ("Yad Avshalom faces the Old City.", "via repo deeper_analysis §2.2 (BibleWalks)")],
    inference=("A 12-cubit dig into bedrock next to a rock-cut monument is implausible as depth; a distance model is an alternative to record.", "low"),
    sources=["Zias 2023", "Høgenhaven p. 79 n. 67", "Lefkovits p. 348"])
rec(id="P48-B", entry="48", branch="Absalom's monument in the SW necropolis (Baqʿah), Milik",
    reading_assumed="as P48-A; 12 feet (Milik 1962 רגמות)", reading_editions=["Milik 1962 pp. 270, 274"], reading_status="disputed", place_id="jer_baqa",
    feature_type="monument named for Absalom in the SW necropolis", feature_detail="", orientation="west side",
    measures=[{"cubits": None, "edition": "Milik 1962: 12 feet (foot length not specified in sources; not converted)", "type": "digging depth"}],
    location="el-Baqʿa plain SW of the Old City (~700 m).", confirm="L2: a monument of the period in the SW necropolis attested as Absalom's.", miss="Not definable.", inconclusive="Default.",
    report_extra=[], priority="low", scorability="not scorable at present", evidence=[("Milik: the Hand of Absalom in the SW necropolis.", "Milik 1962 pp. 270, 274 via shared/readings.json")],
    inference=("", "low"), sources=["Milik DJD III pp. 270, 274"])

# ---------------------------------------------------------------- entry 49
c49 = dict(entry="49", place_id="jer_siloam",
    report_extra=["which pool/installation (tunnel-mouth Silwan pool vs Birket el-Ḥamra vs small tanks) with locus numbers", "any trough/gutter/pipe: position, underside/aperture level, relation to basin boundary and ancient floor, phase",
                  "construction and use dating per installation", "area excavated beneath the trough/pipe and depth reached"],
    priority="high", scorability="feature-level",
    sources=["Szanton, ʿAtiqot 113 (2023) pp. 29–44", "Puech 2006 p. 200; 2015 pp. 91–93", "Lefkovits 2000 pp. 352–354", "Milik 1962 pp. 270–271"])
rec(id="P49-A", branch="Puech: outlet of the waters of Siloam; under the trough/gutter",
    reading_assumed="Puech: 'at the outlet of the waters (יציאת המים) of Siloam, under the trough (השקת)'; the letter after של read as a cursive waw and a second של supplied as lost by haplography",
    reading_editions=["Puech 2006 p. 200; 2015 pp. 91–93"], reading_status="conditional: name depends on a supplied word and a disputed letter (plates lean to waw)",
    feature_type="trough or gutter at the outlet of the Siloam water (tunnel mouth)",
    feature_detail="A hollowed-stone trough/gutter at the tunnel-mouth outlet; the smaller Silwan pool at the outlet is Szanton's Siloam.",
    orientation="beneath the trough", measures=[], location="Siloam: tunnel outlet and Silwan pool (gazetteer ~300 m).",
    confirm="L2: a trough/gutter at the tunnel-outlet pool, physically tied to a phase in use before 70 CE (preferably 135 CE at latest); L3: a period cut beneath it.",
    miss="The tunnel-outlet zone fully published with phase plans and no trough/gutter of any pre-135 phase; or the trough shown to be post-135 with no predecessor.",
    inconclusive="Trough undated or not physically tied to a phase (current state).",
    evidence=[("Szanton distinguishes the smaller Silwan pool at the tunnel outlet from Birket el-Ḥamra; Fig. 6 shows railing stones, not the scroll's trough.", "via repo feature_investigation.md (Szanton 2023 pp. 34–42, Figs. 1, 4, 6)"),
              ("Plates lean to Puech's cursive waw; not decisive.", "via shared/feature_constraints.csv (plate_check)")],
    inference=("Highest-value Jerusalem prediction because the outlet is a single, well-excavated spot.", "medium (site); low (feature)"), **c49)
rec(id="P49-B", branch="Milik: pool of the Baths of Siloah, beneath a pipe in a bathing pool (Birket el-Ḥamra branch)",
    reading_assumed="Milik: 'pool of the Baths (בית חמים) of Siloah (שלוחי)', with the cache under the pipe/trough", reading_editions=["Milik 1960; 1962 pp. 270–271"], reading_status="disputed",
    feature_type="pipe/conduit entering a bathing pool; deposit beneath it", feature_detail="Selected conditional basin in the repo: Birket el-Ḥamra; L103 conduit's main-side junction unknown.",
    orientation="beneath the pipe", measures=[], location="Birket el-Ḥamra / Siloam pools.",
    confirm="L2: a named, surveyed main-basin conduit/trough junction with section, basin boundary and ancient floor in one pre-70 phase, plus bath function; L3: period cut beneath it.",
    miss="Main-side junction excavated and documented with no conduit/pipe of the period entering the basin.",
    inconclusive="Main-side junction unexposed (current state; request to excavator recorded as sent by the repo, reply unverified).",
    evidence=[("2020 Plan 1/p. 76*: L103's channel bottom 0.75 m above the small receiver floor; no surveyed under-pipe place inside Birket.", "via repo research_ACTIVE_TEST.md")],
    inference=("Repo marks the main-pool claim 'not identifiable from available evidence'.", "low"), **c49)
rec(id="P49-C", branch="Lefkovits: 'pool of the water closet of Jehu' — no place name", reading_assumed="Lefkovits: 'pool of the water closet of Jehu' (no place name)", reading_editions=["Lefkovits 2000 pp. 352–354"],
    reading_status="disputed", feature_type="latrine-related pool", feature_detail="No geographic anchor.", orientation="beneath the trough", measures=[],
    location="Unlocated.", confirm="Not scorable.", miss="Not scorable.", inconclusive="Default.", evidence=[("Lefkovits reads no Siloam place name.", "via shared/readings.json")],
    inference=("A confirmed P49-A would count against this branch.", "medium"), **c49)

# ---------------------------------------------------------------- entry 51/52
rec(id="P51-A", entry="51", branch="stoa = Solomon's Portico; Zadok's tomb on the Kidron slope below the SE corner (Milik: west bank)",
    reading_assumed="מתחת פנת האסטאן הדרומית בקבר צדוק תחת עמוד האכסדרן", reading_editions=["Milik 1962 D54, pp. 270–271, 273", "Puech 2015 p. 95"],
    reading_status="stoa (Milik, Puech) vs ossuary (Lefkovits)", place_id="jer_se_corner",
    feature_type="monumental tomb with a pillared exedra (vestibule), deposit under a pillar",
    feature_detail="A rock-cut tomb with vestibule/court and pillar(s), below the line of the southern corner of the Temple portico.",
    orientation="below (downslope of) the southern corner of the stoa", measures=[], location="Kidron slope below the SE corner (gazetteer ~80 m).",
    confirm="L2: a pre-70 CE tomb with a columned exedra on the slope below the SE corner; L3: period cut beneath a pillar base.",
    miss="Feature-level only.", inconclusive="Tombs without exedra; undated.", report_extra=["tomb plan with pillar positions", "date", "excavation beneath pillar bases"],
    priority="medium", scorability="feature-level",
    evidence=[("Period rock-cut tombs reported in the Kidron; monumental tombs of this type stand on the east bank (fits Jeremias's variant better than Milik's west bank).", "via repo phase5_summary §5 (Avni & Greenhut 1996)")],
    inference=("", "low-medium"), sources=["Avni & Greenhut 1996", "Milik DJD III pp. 270–271", "Warren 1871 pp. 135–141", "HA-ESI 136"])
rec(id="P51-B", entry="51", branch="Zadok's tomb on the Kidron east bank (monumental tombs; Jeremias variant)", reading_assumed="as P51-A",
    reading_editions=["Jeremias (via repo phase5_summary §5)"], reading_status="as P51-A", place_id="jer_kidron_mon",
    feature_type="monumental east-bank tomb with pillared exedra", feature_detail="", orientation="west-facing façade", measures=[], location="Kidron monuments (~100 m).",
    confirm="As P51-A on the east bank.", miss="Feature-level only.", inconclusive="Default.", report_extra=["as P51-A"], priority="medium", scorability="feature-level",
    evidence=[("Monumental tombs of this type stand on the east bank.", "via repo phase5_summary §5")], inference=("", "low"), sources=["Avni & Greenhut 1996"])
rec(id="P52-A", entry="52", branch="west-facing rock on the Kidron east slope opposite Zadok's court/garden",
    reading_assumed="בהכסח (scarp, Puech) ראש הסלע הצופא מערב נגד גנת צדוק תחת המסמא הגדולא שבשוליה", reading_editions=["Puech 2006", "Milik 1962 pp. 270–271"],
    reading_status="first word disputed (scarp / family plot / ruin); slab rated high", place_id="jer_kidron_east",
    feature_type="great slab at the base of a west-facing rock top", feature_detail="", orientation="rock faces west", measures=[],
    location="Kidron east slope, Silwan necropolis (~300 m).", confirm="L2: a west-facing rock with a large slab at its base of the period; L3: period cut under the slab.",
    miss="Feature-level only.", inconclusive="Default.", report_extra=["slab position/date", "rock face azimuth"], priority="low", scorability="area-level",
    evidence=[("West-facing slope with period tombs.", "via shared/phase5_archaeology_index.csv")], inference=("", "low"), sources=["Milik DJD III pp. 270–271", "Zias 2023"])

# ---------------------------------------------------------------- entry 55
c55 = dict(entry="55", reading_editions=["Puech 2015 p. 103", "Milik 1962 pp. 271–272", "Lefkovits 2000 pp. 392–398"],
    reading_status="'house of the two reservoirs' (Puech, Lefkovits; plates lean to ח) vs Bethesda (Milik, emended)",
    feature_type="double reservoir; deposit in the smallest basin on the right as one enters",
    orientation="'on the right' as one enters — relative to the access", measures=[],
    report_extra=["phase plan of each basin and of any small basin", "access/entry points per phase", "any vessels with a written record beside them (the entry predicts both)"],
    priority="medium", scorability="feature-level", sources=["Milik DJD III pp. 271–272", "Høgenhaven p. 84", "Warren 1871 pp. 196–197"])
rec(id="P55-A", branch="Bethesda / St Anne's double pool (Puech: smallest basin = the northern one)", place_id="jer_bethesda",
    reading_assumed="בית האשוחין 'house of the (two) reservoirs' (Puech); לימומית 'the smallest basin' (Milik, Puech), entered on the right",
    feature_detail="At Bethesda the smaller (northern) basin.", location="Pools of Bethesda (gazetteer ~50 m).",
    confirm="L2: the smaller basin shown accessible in the 1st c. BCE–1st c. CE with an entrance from which 'right' can be defined; L3: period cut on the right side of that entrance.",
    miss="Feature-level only.", inconclusive="Access undefined.", evidence=[("Puech: the smallest basin, at Bethesda the northern one.", "Puech 2015 p. 103 via shared/readings.json")],
    inference=("Excavation reports (Vincent–Abel; Jeremias) not read in the repo.", "low-medium"), **c55)
rec(id="P55-B", branch="Strouthion twin pool (Sisters of Sion)", place_id=None, reading_assumed="'house of the two reservoirs' (no Bethesda name)",
    feature_detail="Warren describes a second rock-cut twin pool in the same quarter.", location="Sisters of Sion convent (not in gazetteer; no coordinate asserted).",
    confirm="As P55-A at the Strouthion.", miss="Feature-level only.", inconclusive="Default.",
    evidence=[("Warren pp. 196–197: a second rock-cut twin pool nearby.", "via repo phase5_summary §4")], inference=("A hit here counts against P55-A.", "medium"), **c55)

# ---------------------------------------------------------------- entry 57
rec(id="P57-A", entry="57", branch="Gerizim summit: Hellenistic staircases and courtyard cistern (Magen)",
    reading_assumed="בהר גריזין תחת המעלא של השיח העליונא: 'under the step(s) of the upper pit'", reading_editions=["Milik 1962 p. 274", "Puech 2015 p. 108", "Lefkovits 2000 pp. 411–412"],
    reading_status="name secure; pit word varies but feature type stable; 'upper' implies another (lower) pit", place_id="gerizim",
    feature_type="steps leading to/into the upper of two pits (shaft/cistern); deposit under the steps",
    feature_detail="A pit/shaft with steps, the upper of at least two; candidates are Hellenistic staircases and a mansion courtyard cistern standing as ruins in the 1st c.",
    orientation="none", measures=[], location="Mount Gerizim summit (gazetteer ~500 m).",
    confirm="L2: a stepped pit/cistern that is the upper of a pair, standing (as a ruin is acceptable) in the 1st c. BCE–1st c. CE; L3: a period cut under its steps; L4: a chest with vessels and silver.",
    miss="The steps of the identified upper pit dismantled/excavated to bedrock with no cut after its construction.",
    inconclusive="Pit pairs not identified; locus P5178 deposit unpublished.",
    report_extra=["locus/basket concordance (JSP 8 and JSP 20)", "pit pairs and their relative elevations", "step construction and later disturbance", "coin findspots with elevations (e.g., Festus specimen K35264, P5178, basket 51777)"],
    priority="medium", scorability="feature-level",
    evidence=[("NEAEHL: three Hellenistic staircases and a courtyard cistern; city abandoned c. 110 BCE to the 4th c. CE; Hasmonean garrison into the 70s BCE.", "via repo site_identification_review.md (Magen NEAEHL 5 (2008) pp. 1742–1747; Gerizim III)"),
              ("Catalogue 413 records a Festus coin K35264 at P5178, basket 51777.", "via repo OPEN_QUESTIONS R05")],
    inference=("A deposit placed under ruined Hellenistic steps fits the 'standing as ruins' scenario.", "low-medium"),
    sources=["Magen, NEAEHL 5 (2008) pp. 1742–1747", "Magen et al., JSP 19 (2021)", "SWP II pp. 187–190", "Lefkovits p. 412", "Milik DJD III p. 274"])

# ---------------------------------------------------------------- entry 58
rec(id="P58-A", entry="58", branch="Beth Sham = Beth Shean (final mem problem)",
    reading_assumed="בפי המבוע של בית שם", reading_editions=["Milik 1960 (Bet-Shan); 1962 (Bet Šam)", "Puech 2015 p. 109"],
    reading_status="final mem vs nun (Q16); Puech also allows an unknown Beth Shem", place_id="beth_shean",
    feature_type="mouth of a spring", feature_detail="Perennial springs; a period dam and pool reported (HA-ESI 2016).", orientation="at the spring mouth", measures=[],
    location="Beth Shean (gazetteer ~300 m).", confirm="L2: a spring mouth with a period installation; L3: period cut at the mouth; L4: silver and gold vessels.",
    miss="Feature-level only (springs are common).", inconclusive="Default.", report_extra=["spring mouth installations and dates", "excavated area at the mouth"],
    priority="low", scorability="area-level",
    evidence=[("Perennial springs (SWP II) and a dam and pool of the period (HA-ESI 2016).", "via repo phase5_summary §4")], inference=("Springs are common in the valley; weak discrimination.", "medium"),
    sources=["SWP II pp. 81, 102–107", "Har'el, HA-ESI 2016", "Horowitz & Atrash, HA-ESI 2016"])

# ---------------------------------------------------------------- entry 59
c59 = dict(entry="59", reading_editions=["Puech 2015 pp. 110–111", "Lefkovits 2000"],
    reading_status="place word disputed (hbzk Bezek; Milik ha-Baruk/Hebron; others hkwk, hkrk, hbwr); second instance bzk or kwk ('burial chamber')",
    measures=[], report_extra=["any large conduit/drain into a cistern, with phase", "tomb (kokhim) plans and dates", "survey coverage"], priority="low", scorability="feature-level",
    sources=["HA 40 (1971) p. 22", "Zertal 2008 (MHCS 2) pp. 104–107, 151–153, 191–198", "SWP II pp. 237, 240"])
rec(id="P59-A", branch="Kh. Ibziq; great conduit/drain of the cistern", place_id="ibziq",
    reading_assumed="Puech: ביבא 'large conduit' of hbzk (ha-Bezek); second instance read בית הבזך 'house of Bezek'", feature_type="large conduit/drain feeding a cistern; deposit inside the cistern",
    feature_detail="", orientation="inside the cistern", location="Kh. Ibziq (gazetteer ~300 m).",
    confirm="L2: a large conduit/drain into a cistern at Ibziq dated before 135 CE; L3: period deposit/cut inside the cistern.",
    miss="Complete survey/excavation shows no conduit-fed cistern of the period.", inconclusive="Default.",
    evidence=[("Zertal's survey reports cisterns, burial caves and a Roman road but no conduit at either Ibziq site.", "via repo phase5_summary §3")], inference=("", "low"), **c59)
rec(id="P59-B", branch="Kh. Ibziq; 'burial chamber' reading (Puech alternative)", place_id="ibziq",
    reading_assumed="בית הכוך 'the burial chamber'", feature_type="kokhim tomb near a conduit", feature_detail="A kokhim tomb with 1st–2nd c. CE pottery was excavated in 1971.",
    orientation="", location="Kh. Ibziq.", confirm="L2: a conduit adjacent to a period kokhim tomb; L3: period deposit in the tomb.", miss="Feature-level only.", inconclusive="Default.",
    evidence=[("HA 40 (1971) p. 22: robbed kokhim tomb with 1st–2nd c. CE pottery.", "via repo phase5_summary §3")], inference=("Matches in type only.", "low"), **c59)
rec(id="P59-C", branch="Kh. Salhab (Zertal's biblical Bezeq)", place_id="kh_salhab", reading_assumed="as P59-A", feature_type="large conduit/drain feeding a cistern",
    feature_detail="", orientation="", location="Kh. Salhab (gazetteer ~300 m).", confirm="As P59-A at Salhab.", miss="As P59-A.", inconclusive="Default.",
    evidence=[("No channel on Zertal's Salhab page images.", "via repo site_identification_review.md")], inference=("", "low"), **c59)

# ======================================================== Kohlit entries
KOHLIT_REPORT = ["position (azimuth/distance) relative to Tell es-Sultan summit and to the ʿAin es-Sultan spring", "construction and use phase with dating evidence",
                 "whether the feature was open/visible in the 1st c. CE"]
rec(id="P04-A", entry="4", branch="Koḥlit = Tell es-Sultan; Milik 'crevice of immersion'",
    reading_assumed="בתל של כחלת … פתחו בשולי האמא מן הצפון אמות שש עד ניקרת הטבילה (Milik: מפי גל 'from the mouth of the heap')",
    reading_editions=["Milik 1962", "Wolters; Eshel; Schiffman (ניקרת)"], reading_status="Koḥlit secure at I 9; landmark words disputed",
    place_id="tell_es_sultan", feature_type="opening at the northern edge of a conduit, 6 cubits from a rock cleft used for immersion",
    feature_detail="A mound (tell) with a conduit; an opening at its north edge; a natural rock crevice used for immersion 6 cubits away.",
    orientation="opening on the north edge of the conduit", measures=[{"cubits": 6, "edition": "all", "type": "distance opening→cleft"}],
    location="Tell es-Sultan and the spring at its east foot (gazetteer ~150 m).",
    confirm="L2: a conduit at/below the tell in use in the 1st c. with an opening on its north edge 2.7–3.2 m (6 c.) from a rock cleft with evidence of immersion use; L4: offering vessels.",
    miss="Feature-level only.", inconclusive="Spring channels undated (current state).", report_extra=KOHLIT_REPORT + ["conduit route and openings", "immersion evidence (steps, plaster) in rock clefts"],
    priority="low", scorability="feature-level",
    evidence=[("Channels run from the spring below the tell but are undated; dated Hasmonean–Herodian aqueducts and baths are at the palaces south of the tell; no immersion installation is reported at the tell.", "via downloads/tables_phase5_assessments.csv (entry 4; SWP pp. 222–223; Eshel pp. 99–100)")],
    inference=("Kohlit identification itself is only a hypothesis (Puech 'à titre d'hypothèse').", "low"), sources=["SWP III pp. 222–223", "Eshel CSS pp. 99–100", "Puech 2015 pp. 13–14 n. 49"])
rec(id="P04-B", entry="4", branch="Koḥlit = Tell es-Sultan; Puech 'frigidarium of the bath'", reading_assumed="… עד מקרת הטבילה: 'cold room (frigidarium)' of the bath; מפוגל 'disqualified'",
    reading_editions=["Puech 2006; 2015 p. 36"], reading_status="disputed", place_id="tell_es_sultan",
    feature_type="opening at the northern edge of a conduit, 6 cubits from a bath frigidarium", feature_detail="Built bath with cold room near the tell.",
    orientation="as P04-A", measures=[{"cubits": 6, "edition": "all", "type": "distance opening→frigidarium"}], location="As P04-A.",
    confirm="L2: a 1st-c. bath with frigidarium at/next to the tell and a conduit opening 2.7–3.2 m away on the conduit's north edge.", miss="Feature-level only.", inconclusive="Default.",
    report_extra=KOHLIT_REPORT + ["bath plan and room functions"], priority="low", scorability="feature-level",
    evidence=[("No bath is reported at the tell; baths are known in Hasmonean/Herodian Jericho (palaces).", "via shared/readings.json e4-immersion (Puech 2015 p. 36)")], inference=("", "low"), sources=["Puech 2015 p. 36"])
rec(id="P11-A", entry="11", branch="pool east of Koḥlit = reservoir at ʿAin es-Sultan (east foot of the tell)",
    reading_assumed="בברכא שבמזרח כחלת במקצע הצפוני חפור אמות ארבע", reading_editions=["Puech 2015 pp. 13–14 n. 49 (hypothesis)"], reading_status="letters agreed",
    place_id="tell_es_sultan", feature_type="cornered pool east of the tell; deposit in its northern corner",
    feature_detail="SWP describes a shallow reservoir of dressed stone at Elisha's spring, undated.", orientation="northern corner of the pool (internal position)",
    measures=[{"cubits": 4, "edition": "all", "type": "digging depth"}], location="ʿAin es-Sultan, east foot of Tell es-Sultan.",
    confirm="L2: a cornered pool at the spring dated to use in the 1st c. BCE–1st c. CE; L3: period cut 1.8–2.1 m (4 c.) below its floor/ground in the northern corner.",
    miss="The spring reservoir excavated and dated post-135 CE with no earlier basin beneath.", inconclusive="Undated (current state).",
    report_extra=KOHLIT_REPORT + ["reservoir plan, corners, floor level", "earlier basins beneath"], priority="medium", scorability="feature-level",
    evidence=[("SWP pp. 222–223: a shallow reservoir of dressed stone at Elisha's spring, undated.", "via downloads/tables_phase5_assessments.csv (entry 11)")],
    inference=("Dating the spring reservoir is the cheapest test of the whole Tell es-Sultan = Koḥlit hypothesis (cycle7 next test).", "medium"),
    sources=["SWP III pp. 222–223", "Kenyon, Excavations at Jericho III pp. 173–174 (Puech's lead, via repo cycle7)"])
rec(id="P15-A", entry="15", branch="great cistern in [north of] Koḥlit (restored), pillar on its north side",
    reading_assumed="'In the great cistern [north(?) of Ko]ḥlit, in the pillar on its north side' — Puech restores [כ]חלת 'with near certainty'; Milik read only …QH", reading_editions=["Puech 2006, 2015 pp. 49–50"],
    reading_status="restored (name and direction)", place_id="tell_es_sultan", feature_type="great cistern with a pillar on its north side",
    feature_detail="", orientation="pillar on the north side of the cistern", measures=[], location="At or north of Tell es-Sultan.",
    confirm="L2: a large cistern of the period with a pillar on its north side at/north of the tell.", miss="Feature-level only.", inconclusive="Default.",
    report_extra=KOHLIT_REPORT + ["cistern plan with pillar"], priority="low", scorability="feature-level",
    evidence=[("No large cistern at or north of Tell es-Sultan is reported.", "via downloads/tables_phase5_assessments.csv (entry 15)")], inference=("Rests on restoration.", "low"),
    sources=["Puech 2015 pp. 49–50"])
rec(id="P16-A", entry="16", branch="conduit going to [the pool] (Puech): 14 cubits as you enter",
    reading_assumed="באמא הבאה ל[בר]כא בביאתך אמות ארבע[ ע]סרה", reading_editions=["Puech 2006; 2015 pp. 48–51"], reading_status="destination and number restored (14/40/41)",
    place_id="tell_es_sultan", feature_type="conduit entering a pool; deposit 14 cubits along it from its entrance",
    feature_detail="Puech's Koḥlit association comes from the preceding cistern context; entry 16 names no place.", orientation="along the inward axis of the conduit",
    measures=[{"cubits": 14, "edition": "Puech 2015 p. 51", "type": "distance (Puech excludes depth)"}], location="Spring/tell sector (low).",
    confirm="L2: a conduit-to-pool entrance of the period at the tell/spring; L3: period cut 6.2–7.4 m (14 c.) along the conduit from its entrance.", miss="Feature-level only.", inconclusive="Default.",
    report_extra=KOHLIT_REPORT + ["conduit entrance definition and inward axis"], priority="low", scorability="feature-level",
    evidence=[("14 cubits = 6.23–7.35 m at 0.445–0.525 m; no coordinate generated.", "via downloads/research_measurements_cycle7_kohlit_pool.md")], inference=("", "low"), sources=["Puech 2015 pp. 48–51"])
rec(id="P16-B", entry="16", branch="conduit going to Hyrcania (Eshel): its northern aqueduct, 41 cubits", reading_assumed="Eshel: 'the conduit that goes to Hyrcania' (restored); Milik ארבע[ין ואח]ת = 41 cubits",
    reading_editions=["Eshel 2002 CSS pp. 102–103", "Milik 1962 (41)"], reading_status="restored; Puech rejects as too long", place_id="hyrcania",
    feature_type="Hyrcania's northern aqueduct; deposit 41 cubits from its entrance", feature_detail="Datum: trail/northern-aqueduct intersection west of Hyrcania (Eshel).",
    orientation="along the conduit", measures=[{"cubits": 41, "edition": "Milik 1962; Eshel", "type": "distance"}, {"cubits": 40, "edition": "Lefkovits", "type": "distance"}],
    location="Hyrcania N aqueduct (1.95 km Wadi Abu Shuʿla line, Hasmonean).", confirm="L3: period cut 18.2–21.5 m from Eshel's datum along the channel.",
    miss="Not definable until the datum is surveyed.", inconclusive="Default.", report_extra=["datum survey", "channel phase"], priority="low", scorability="feature-level once datum fixed",
    evidence=[("Eshel's restoration assumes a geographical order; Puech 2015 n. 193 rejects it as too long.", "via shared/readings.json e16-goal")], inference=("", "low"), sources=["Eshel CSS pp. 102–103"])
rec(id="P19-A", entry="19", branch="eastern pit north of Koḥlit = north of Tell es-Sultan",
    reading_assumed="בשית המזרחית שבצפון כחלת", reading_editions=["Puech; Milik (kḥlt)"], reading_status="Allegro reads בחלה 'hole' (no place name)",
    place_id="tell_es_sultan", feature_type="the eastern of ≥2 pits north of Koḥlit",
    feature_detail="'The eastern pit' implies at least two pits in the sector north of Koḥlit; entry 60's pit is plausibly another of the set.",
    orientation="pit lies north of the anchor; it is the eastern member of its group", measures=[], location="North sector of Tell es-Sultan (see P60-T1).",
    confirm="L2: ≥2 pits/shafts of pre-135 CE date north of the tell, the eastern one identifiable; L4: silver.", miss="Feature-level only.", inconclusive="Default.",
    report_extra=KOHLIT_REPORT + ["all pits/shafts in the north sector with positions, so 'eastern' can be assigned"], priority="high", scorability="feature-level",
    evidence=[("No pits are reported north of Tell es-Sultan; a large cemetery N and W of the tell with tombs to the Roman period is.", "via downloads/tables_phase5_assessments.csv (entry 19; Sala 2014 p. 117)")],
    inference=("Joint target with P60-T1: one survey of the north sector scores both.", "medium"), sources=["Sala 2014 p. 117 (via repo)", "Puech 2015 pp. 13–14 n. 49"])
