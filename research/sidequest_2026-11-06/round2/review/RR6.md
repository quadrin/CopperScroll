# Round-2 review RR6: lanes D1, D2, D3, E1, E2 and the entry 24 hunt note (6 Nov 2026)

Reviewer RR6 took no part in the hunt. Method: `REVIEW_BRIEF.md` as changed by `review2/REVIEW2_NOTE.md`. I did not judge by AGENTS.md procedures. For every card I re-opened the evidence behind its strongest claim, and I checked the round-1 link against `out/<lane>/FINDS.md` and reviews R2, R5, R6 and R8. I read private images only to verify. No crops were made, and nothing image-derived is in this file.

---

## D1, card 1: ʿAtiqot 41 plans and captions give the facings that `aspect.csv` codes "no facing in the record" (XI/18, XI/20, VIII/29)

- **Verdict: SURVIVES.** NEW TO THE PROJECT. **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - `research/regional/caves_entry25/aspect.csv` codes A41:XI/18, XI/20, VIII/28 and VIII/29 as "no facing in the record".
  - I recounted with `caves.csv` `published_plan`: 47 ʿAtiqot 41 caves cite a plan and 32 of them are coded "no facing". Adding XI/20, whose plan the inventory lists as "none", gives the card's 33 of 48.
  - VIII/29: the English summary (`en_2569`, D1 scratch) reads "two entrances: a northern one facing the terrace at the foot of Cave VIII/28". The Hebrew has "צפוני, הפונה אל המדרגה שלרגלי מערה VIII/28".
  - XI/18: on Plan 6 (private crop) the half-arrow points about 45° clockwise of page-up and the mouth opens to page right / up-right. That is about NNE to NE true, as the card says.
  - The geometry is right: Qumran anchor (193650/127650) → XI/18 (193450/128510) is 883 m at 347°.
- **Link definitions:** in `chain.json`, QUMRAN-1 asks for "a non-funerary cave or shaft at 315°–45° within 1 km … opening that faces 315°–45°", and it names XI/18 and XI/20 in its "where" field. Its success condition is met.
- **Novelty:** not a restatement. No round-1 card or project file reads these plans for facing.
- **Argument:** measured and correct. A cheap success on an N–S cliff discriminates little.

## D1, card 2: the four protected Tier-1 Koḥlit records read (ʿAlmit success; Tananir pool west; Highlands lacks the er-Ras features; Sheikh Dhiab "misrouted")

- **Verdict: WEAKENED.** NEW TO THE PROJECT. **Confidence:** high. **Cost:** cheap.
- **Confirmed:**
  - ʿAlmit: D1's OCR of Benjamin p. 380 has "במדרון המערבי נמצאת מערת-קבורה … בסמוך לפתח המערה נראה פתח עליון של מערת-קולומבאריום, ובה 70 גומחות".
  - Tananir: the 11 Oct extraction gives the pool "כ 50-מ' מערבה לבניין העיקרי".
  - Udala: Highlands PDF p. 735 (site 17-17/64/01) lists only "A number of cisterns" and the en-Nabi ʿUzeir sheikh-tomb complex, with "Kallai 1972 : 167".
- **Killed part (Sheikh Dhiab "misrouted"):** `chain.json` does not mistake site 194 for the tell. The link says: "315°–45° within 1 km of WBADB S6040 … Record: Zertal Vol. 4 site 194 for ʿArkan es-Suwaneh (S1454)". REC-ZERTAL-V4 reads "Site 194 (WBADB S1454, ʿArkan es-Suwaneh) not read". S1454 is the north-sector unit (894 m at 26.6°) that supplies the selected pit (R-E60-PIT-N). So site 194 is the right record for "a grave at the selected pit's mouth". The tell's own record (Zertal 2012a site 23) would add coverage for the sector search, but it does not correct a misroute. Only the README's parenthetical "(Tell esh-Sheikh Dhiab)" is loose.
- **Novelty, partial:** ʿAlmit had already been read twice: the 12 Oct Benjamin full read, and `research/regional/columbaria/PLAN_AMENDMENT_1.md` item 4 ("read in the S1 screen"). What is new is only the comparison with the chain link. The card says so.
- **Argument:** fair. It does not overclaim ʿAlmit.

## D1, card 3: Bar-Adon's ASI 1 entry for Tell Muhalhil (site 83): no pool or tomb, no Hellenistic or Roman pottery

- **Verdict: WEAKENED** (the ARGUMENT, not the evidence). NEW TO THE PROJECT. **Confidence:** high (record); low (consequence). **Cost:** cheap.
- **Evidence checked:**
  - I read the private crops of IMG_1722.
  - The header reads "T. Muḥalhil 192 133, −80 מ'".
  - The sub-sites read: ב 45 × 18 m; ג round building 4.40 m; ד 50 × 40 m; ה "תל מחלחל", a building 2.5 × 3.5 m with a wall 11 m long about 35 m to its north.
  - The pottery list reads: א Israelite; ב Chalcolithic and Israelite; ג Israelite I–II, Arab and Crusader; ד Israelite. ה has no pottery line.
  - All as the card says. Locator: the ב–ה text is under the running head "הסקר במדבר יהודה ובקעת יריחו", so it may be p. 119 column 1, not "p. 118 column 2". This is minor.
- **Kill test the card left unrun, run here:** I read the ASI online records for Map 109/5 (MapId 78, round-1 D2 dump `scratch/D2/asi/`):
  - Units 83–87 "Tell Muhalhal (1)–(5)" are Bar-Adon's sub-sites, with pottery Iron, Chalcolithic–Iron, none listed, Iron and Early Bronze.
  - Unit 99 "Tell Muhalhal (8)", fences and stone heaps: **"Pottery: Roman, Byzantine."**
  - Unit 100 "Tell Muhalhal (9)", bases of buildings: **"Pottery: Early and Late Roman, Byzantine."**
  - Units 99–100 lie about 1.5 km SE of unit 83, on the Jericho plain below the fault cliff.
- **Effect on the argument:** the card's own kill line ("any Roman-period find … would restore the candidate, but not a pool") is met for the wider Muhalhal cluster. "A large negative for any model that needs a pool in use 50 BCE–135 CE" overstates. Bar-Adon's five hill-top sub-sites have no Second Temple pottery. The same-name complex has Early Roman pottery 1.5 km away, and no pool anywhere.
- **Partly known:** `looks_v2.csv` L05 already records, via Zissu 2001, "named a tell; the survey found only a small structure".
- **Cross-link:** C2 round-1 card 1 lists Bar-Adon 83a (T. Muḥalḥil) among the nearest records to the "Mght. Ekteif" label. The Muhalhil cluster and the entry 24 search area are neighbours.

---

## D2, card 1: EDF's "cassures récentes" (code 3e) on segments 5, 6 and 8 predate Dec 1988; at segment 6 the lacunae open during treatment

- **Verdict: WEAKENED.** NEW TO THE PROJECT for segments 5 and 8. The segment 6 "NEW TO THE LITERATURE (provisional)" part is **killed**. **Confidence:** medium (5, 8). **Cost:** cheap.
- **Evidence checked:**
  - EDF copy B PDF p. 70 (segment 6, condition before treatment): "d'une cassure récente sans fragment correspondant dans la zone inférieure droite". The same text continues: "Sur le revers, dans la partie inférieure gauche, présence d'un fragment provenant d'un autre segment, soudé par les produits de corrosion de trois plaquettes de soutien en plastique".
  - Pl. CXX legend (private crop `rel_s6_avant_apres.png`): the revers lower-left (= the avers lower-right) carries "Fragment d'un autre segment collé par la corrosion", "Plaquette en Plexiglas" and "Décollement du doublage de résine".
  - Pl. CXXI after: the same zone carries "Fragments rajoutés ou modifiés" (red hatching) and the "Fragments déplacés" arrow.
  - I viewed `s6_bottom_88_94_96.png`.
- **Why the segment 6 claim fails:**
  - Before treatment EDF records a break *without a matching fragment* in this very zone. That is missing material, recorded before treatment.
  - It also records a foreign fragment, plastic support plates and a resin doubling stuck behind the zone.
  - A foreign fragment behind the lacunae, or resin behind them, makes them look closed from the front in 1988 and Feb 1994. The acetonitrile bath removed the plates and "a également défait les anciens collages"; EDF then moved or modified fragments there. The holes visible afterwards (against a pale background, where the earlier photographs have black or grey) are therefore the true lacunae, uncovered rather than newly lost.
  - So "the material that is missing now went missing during the 1994–96 treatment" and "EDF's text does not mention them" are not supported.
- **What holds:** the outlines at the segment 8 corner and along the upper segment 5 crack are already present in Dec 1988. So EDF's "récente" includes breaks older than 1988, which adds to A1d-2. That is modest.

## D2, card 2: on flat ground doors still avoid W; the preference "gives way to topography" on steep ground

- **Verdict: WEAKENED.** KNOWN BUT UNDER-DISCUSSED kept. **Confidence:** medium. **Cost:** cheap.
- **Reproduced from `flat_ground_doors.json`:**
  - Clean flat units: W 6 of 62. One-sided binomial against 0.25 gives p = 0.0021.
  - All flat units: W 9 of 75, p_W 0.002.
  - The W deficit on flat ground is real, and it answers R6's objection.
- **What does not hold:**
  - "Strongest where the ground is flat": the gentle class is stronger. W is 7 of 88 (8%) against 9 of 75 (12%) on flat ground, and the resultant is 0.365 against 0.283.
  - "The W deficit disappears on steep slopes" is a non-significant result in small n, not a demonstrated decay. Fisher's test of the W share, steep against flat + gentle: p = 0.18 for all units (8/44 against 16/163) and p = 0.13 for the clean units (7/40 against 11/140).
  - The habit-versus-cosmology inference in "Why it might matter" therefore rests on an untested difference.
- **Restated:** the doors avoid W on flat and on gentle ground. On steep ground the sample is too small to tell.

---

## D3, card 1: HCM 2016 Pl. 42 and Pl. 45 captioned "Locus 83-3"; every object is from L. 81 level 3 (incl. scroll jar KhQ 1492)

- **Verdict: SURVIVES.** NEW TO THE LITERATURE (minor, provisional). **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - Text layer PDF p. 288: "Locus 83-3, poterie et catalogue", over eight rows, all "81.3", dated 16–20/3/54. KhQ 1492 is "jarre type à manuscrit".
  - p. 291: "Planche 43, 5 … 44, 8 … Locus 83-3, photographies".
  - p. 533, the List of Plates: "Planche 42 : Locus 83-3" and "Planche 45 : Locus 83-3".
- **Extra test:**
  - L. 83 has its own plate (PDF p. 302, "Locus 83, poterie, catalogue et photographies", KhQ 4399–4400).
  - L. 83's stratigraphic table (p. 300) gives dates of 11–14/3/54, none of them in the 16–20/3/54 range of Pl. 42.
  - So the plate's objects cannot belong to L. 83. The caption is a slip for 81-3.
- **Still open:** the 2024 English edition. Not a restatement of any round-1 card.

## D3, card 2: Magen & Peleg 2018 Fig. 9 scale bar lettered "cm"; north arrows consistent

- **Verdict: SURVIVES.** NEW TO THE LITERATURE (trivial). **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - I rendered PDF p. 3 at 150 dpi. Bottom right reads "0 10 20 cm"; the north arrow points straight up.
  - L91 on the rendering is about 139 px against a bar of 166 px for 20 units, which gives about 16.8 m. That matches the card.
- **Alternative checked:** the text layer prints "Im", but the image shows "cm" clearly.
- **Not checked:** the arrow audit (accepted, ±5°).

## D3, card 3: the *Maresha IV* store copy is the IAA portal's full-volume PDF

- **Verdict: MERGE into D3b-1** (tag as D3b-1, NEW TO THE LITERATURE). **Confidence:** high (provenance). **Cost:** cheap.
- **Evidence checked:**
  - Store p. 1 is the bepress cover sheet ("Israel Antiquities Authority Publications Portal … 8-2025 … DOI: https://doi.org/10.69704/iaaRepV000.1996.82").
  - `manifest.json`: src_bytes 71974017, sha256 91710daa….
- **Why merged:** this confirms D3b-1's provenance and partly runs R8's open kill test. It is not a separate find.

---

## E1, card 1: Eshel & Safrai convert AM 3331 to "373 BCE" (should be about 431/430 BCE); the Massekhet Kelim plaques argued to be forgeries

- **Verdict: SURVIVES.** The date error is NEW TO THE LITERATURE (provisional); the forgery point is NEW TO THE PROJECT. **Confidence:** high (the arithmetic); medium (novelty). **Cost:** cheap / moderate.
- **Evidence checked:** I read Drive `153PPbwQA8dqpQrLPXe6anEYoc2wePS1d` with the connector. Note 66 reads "3331 ליצירה היא 373 לפה"ס".
- **Arithmetic:** AM 1 begins in autumn 3761 BCE, so AM 3331 runs from autumn 431 to autumn 430 BCE. No standard count gives 373.
- **More in the same note:** Eshel & Safrai call the preface "a late addition … not attested in the other witnesses (n. 7)". So the claim that the preface's only witness is the plaque version is theirs too.
- **Literature:**
  - Web search found the BAS sidebar "The Mystery of the Missing Plaques" and Dugan's BAR article (titles only; I could not open them, and a PaleoJudaica 2011 post on the "Ezekiel plates" was blocked by an approval prompt).
  - Repo grep for Dugan / Ezekiel tile / missing plaques: no hits.
  - Not searched by the card: Davila's translation and introduction of the *Treatise of the Vessels* (*Old Testament Pseudepigrapha: More Noncanonical Scriptures* 1, 2013). It may give the correct date or discuss the plaques' authenticity. It is the cheapest further kill test.
- **Argument overstatements:**
  - "Lost plaques that Milik alone saw" is too strong: RB 66 (1959) published photographs (Pl. XIV, the BAS caption).
  - Even if the plaques are genuine, the preface is a late text (by Eshel & Safrai's own note), so it was never an ancient witness to Carmel. The forgery claim adds little to "no evidential basis". The card does call the change modest.

## E1, card 2: within-report check of HA reports: Lahav Forest general ref ~2 km south of all 48 sites; Har Avihu pile 21; Oron B site 53

- **Verdict: SURVIVES.** NEW TO THE LITERATURE. **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - `en/vol-124/02162_lahav-forest.txt`: "northwest of Qibbuz Lahav … map ref. 1860–80/5835–65". All 48 site refs have northings 588276–588856. The Hebrew has the same box, "18600-800/58350-650".
  - Har Avihu: the box is 225933–7422/735867–6651, and pile 21 is printed "227352/739956". Confirmed.
  - Oron: the box is "19265-379/52793-988". Confirmed.
- **Novelty:** this extends E1-1 to the whole corpus with new cases, so it is not a restatement.

## E1, card 3: Crossref: 9,525 of 9,526 legacy HA-ESI records carry institutions as authors and no volume; the 2026 records (vol. 138) are clean

- **Verdict: MERGE into round-1 E1-3** (NEW TO THE LITERATURE). **Confidence:** high. **Cost:** cheap.
- **Re-run:**
  - `api.crossref.org/journals/1565-5334/works?rows=0` returns 9,718.
  - `10.69704/jhaesi.116.2004.2285` has the authors [IAA (first), Stern (first)].
  - `10.70967/1565-5334.1098` has volume 138, issued 2026-07-02, and Hebrew authors with "רשות העתיקות" as affiliation.
  - The bare `10.69704/jhaesi.116.2004` is a journal-level record.
- **Why merged:** the defect (IAA as author, null volume) is round-1 E1-3 as R2 reframed it. The full counts and the clean 2026 scheme sharpen that card; they are not a new find.

## E1, card 4: Khirbat ʿAmra (HA 125, 4363) uses W20–W22 for two different sets of walls

- **Verdict: SURVIVES.** NEW TO THE LITERATURE (minor). **Confidence:** high (facts); low (importance). **Cost:** cheap.
- **Evidence checked:** in the EN text, W21, W22 and W20 are the three Mamluk sub-phase walls of Sq F6, and "A room delimited by three walls (W20–W22; Figs. 15, 16) was exposed in Sq F5". The wall numbers used are W1, 5, 7–11, 13, 14, 16 and 20–22, so the numbering is a single sequence. The W8/W9 phase colours on Fig. 15 were not re-checked.

---

## E2, card 1: Dabaritta road missing from Itiner-e and from TIR North

- **Verdict: MERGE into round-1 E2-2** (NEW TO THE PROJECT). **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - Private TIR crop `tir_tabor_s.png`: no red road between Sepphoris–Tiberias, Legio–Sepphoris and the Legio–Scythopolis road. Dabaritta, Exaloth, Thabor Mons and Helenoupolis(?) lie in the gap.
  - HA 135 26342: "the site was located on the main road that led from the eastern Galilee to the Jezreel Valley and southward to Jerusalem", and "a second-century CE Roman road" (2007).
- **Why merged:**
  - Checking TIR was R6's listed "cost to confirm" for E2-2. The card runs that check, and the 2023 report adds a second published statement.
  - TIR (1993–94) predates the 2007 excavation, so its silence is expected. Only Itiner-e's (2025) silence is notable, and that is E2-2.

## E2, card 2: first full join of Itiner-e with TIR North; two scroll-region divergences (Bethlehem–Ein Gedi; Jericho–Livias ends at Tall el-Hammam)

- **Verdict: SURVIVES** (with one small correction). NEW TO THE LITERATURE (provisional; Livias debate KNOWN). **Confidence:** medium-high. **Cost:** cheap.
- **Evidence checked** (round-1 E2 arrays `scratch/E2/roads_itm.npy`, C2's `itinere_region.json`):
  - fid 3365 "Jericho-Livias" (Conjectured; bibliography "Isaac 1992, Roll 2002, TIR Iudaea-Palaestina") ends at 35.6751 E / 31.8400 N, which is Tall el-Hammam. Its closest approach to Tell er-Rameh (31.8256 N / 35.6444 E) is **1.43 km**, not the card's 1.1 km.
  - fid 3682 "Livias-Esbus" starts at the same point.
  - fid 3428 "Bethlehem-Ein Gedi": Secondary Road, Conjectured, bibliography "TIR Iudaea-Palaestina, SWP". Confirmed.
- **Not re-run:** the 85% / 79 m statistics. The scripts are present.
- **Novelty:** no project or branch file joins TIR with Itiner-e. The card is new.

## E2, card 3: E2-1's kill tests run (terrain-matched null 0.43–0.46; WBADB 0.505)

- **Verdict: MERGE into round-1 E2-1** (E2-1 holds). **Confidence:** medium. **Cost:** moderate.
- **Evidence checked:** in `hoards_roads_terrain_null.csv`, eight of the nine variants have a CI that includes 0.5. Only one, elevation ±50 m / slope ±2° (n = 76), reaches 0.430 (CI 0.363–0.498).
- **Why merged:**
  - Tightening the match drops 37 of 113 hoards, so the shift mixes terrain control with a change of sample.
  - R6 already wrote that the test "cannot exclude a weak one". The claim that this "changes the round-1 headline" therefore overstates.
  - The result is E2-1's kill test, failed to kill. The WBADB period test (0.505) is a useful second witness and belongs on E2-1.

---

## Orchestrator note: entry 24, Mughâret Ekteif, direct image search (`e24/HUNT_2026-11-06.md`)

- **Verdict: WEAKENED** (the descriptive part stands; the conclusions overstate). Tag for the road-building observation: NEW TO THE PROJECT. **Confidence:** medium (epochs); low (destruction inference). **Cost:** needs new data (field visit, or road-construction records).
- **Checked:**
  - The SWP text quoted by C2-1 (Memoirs III p. 220): "A very curious excavation in the north side of the valley … gradient about 1 by 2 for 120 feet … Steps … entrance to a subterranean chamber now choked up". The note's 37 m and 16 m drop agree with it.
  - Private `hx74_loop_c.png`: in June 1974 the road is a single sealed carriageway across the loop, with an older winding track to its NW.
  - C2 round-2 control table (`swp_pom_registration_checks.csv`).
- **Problems:**
  1. **The registration error is not a vector.** The two controls nearest Ekteif move in different directions:
     - Nebi Musa: SWP minus truth is +20 m E, +160 m N;
     - Maqam er-Raʿi: −100 m E, −60 m N.
     So "about 150 m" is a magnitude, and no local correction can be applied. The note's "SWP wadi line runs 150–250 m south of the real gorge" is 1–1.5 times that error, so "generalised" cannot be separated from the georeference. The "north side" conclusion survives, because label and line are on the same sheet.
  2. **±150 m should not replace ±250–300 m.** C2 card 2 says its 150 m is "smaller than the ±250–300 m used". That 150 m covers the sheet's registration only. The feature's position also carries the label-to-object offset: SWP cave names are set beside the object, and C2-1 itself allowed 150–250 m for label anchors. The combined uncertainty stays about 250–300 m. The zones Z1–Z3 should be read with that margin.
  3. **"Destruction or burial during road building … the most likely single explanation"** ranks one cause above others the evidence cannot exclude:
     - the passage was already "choked up" in 1873, and a sloping open cut at the foot of the fault scarp fills with slope wash;
     - Bar-Adon's 1968 survey (Tell Muhalhil sub-sites 83א–ה, about 0.6–1 km away) and Sion's 109/5 units 97–100 (fences and buildings on the cliff foot) covered this ground and recorded no passage. Whether that was before or after the road is not dated in the note.
     The road can be dated only to between the 1940s and 1974. "One of the likely explanations" is the defensible wording.
  4. **The cistern argument cuts against the entry 24 conclusion.** Entry 24's object is a tomb: `ratings.csv` line 35 says "Milik, Puech ('certain') and Lefkovits agree on 'tomb'", and the Kippa meaning "does not change the landmark sought". If the 37 m stepped passage is better read as cistern or water-chamber access, as the note argues, it is less likely to be the entry's tomb. The note still says the Ekteif excavation keeps Wadi Kuteif "a reasonable reading". Only the route part survives that. The feature part is weakened by the note's own reading.
  5. Minor: the 1974 frame was placed by eye. "In 1974 this ground was still natural" (fill after 1974) holds only to about the 1 m resolution and the unmeasured by-eye registration.
- **What stands:** the gorge loop on the 1940s map and photograph, the road built between the 1940s and 1974, its widening by 2023 with fill on the north side, and Z1/Z2 as the surviving field targets. These are useful and new to the project.

---

## Summary table

| lane | card | short title | original tag | verdict | final tag | confidence | cost |
|---|---|---|---|---|---|---|---|
| D1 | 1 | ʿAtiqot 41 plans give facings (XI/18, XI/20, VIII/29) | NEW TO THE PROJECT | SURVIVES | NEW TO THE PROJECT | high | cheap |
| D1 | 2 | Four Tier-1 Koḥlit records read | NEW TO THE PROJECT | WEAKENED (Sheikh Dhiab "misroute" wrong) | NEW TO THE PROJECT | high | cheap |
| D1 | 3 | Tell Muhalhil ASI 1: no pool, no Hell./Rom. pottery | NEW TO THE PROJECT | WEAKENED (argument; Sion units 8–9 Roman) | NEW TO THE PROJECT | high / low | cheap |
| D2 | 1 | EDF 3e breaks predate 1988; seg 6 opened in treatment | NEW TO THE PROJECT / NEW TO THE LITERATURE (prov.) | WEAKENED (seg 6 part killed) | NEW TO THE PROJECT | medium | cheap |
| D2 | 2 | Flat-ground doors avoid W; decay on steep | KNOWN BUT UNDER-DISCUSSED | WEAKENED (decay not significant) | KNOWN BUT UNDER-DISCUSSED | medium | cheap |
| D3 | 1 | HCM 2016 Pl. 42/45 "Locus 83-3" = 81-3 | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE (minor, prov.) | high | cheap |
| D3 | 2 | Magen 2018 Fig. 9 bar "cm" | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE (trivial) | high | cheap |
| D3 | 3 | Maresha IV store copy = IAA portal PDF | as D3b-1 | MERGE into D3b-1 | NEW TO THE LITERATURE | high | cheap |
| E1 | 1 | Eshel & Safrai AM 3331 = "373 BCE"; plaques forged? | NEW TO THE LITERATURE (prov.) / NEW TO THE PROJECT | SURVIVES | unchanged | high (arith.) / medium (novelty) | cheap / moderate |
| E1 | 2 | Lahav Forest, Har Avihu, Oron B refs | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | high | cheap |
| E1 | 3 | Crossref HA-ESI org-authors; 2026 clean | NEW TO THE LITERATURE | MERGE into E1-3 (r1) | NEW TO THE LITERATURE | high | cheap |
| E1 | 4 | Khirbat ʿAmra W20–22 used twice | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE (minor) | high / low | cheap |
| E2 | 1 | Dabaritta road missing from Itiner-e and TIR | NEW TO THE PROJECT | MERGE into E2-2 (r1) | NEW TO THE PROJECT | high | cheap |
| E2 | 2 | Itiner-e × TIR join; Ein Gedi and Livias divergences | NEW TO THE LITERATURE | SURVIVES (Tell er-Rameh 1.4 km, not 1.1) | NEW TO THE LITERATURE (prov.) | medium-high | cheap |
| E2 | 3 | Terrain-matched hoard null; WBADB | NEW TO THE LITERATURE | MERGE into E2-1 (r1) | NEW TO THE LITERATURE | medium | moderate |
| E24 | note | Ekteif direct image search | (note) | WEAKENED (argument) | NEW TO THE PROJECT (road observation) | medium / low | needs new data |

## Blocked inputs (this review)
- `https://paleojudaica.blogspot.com/2011/05/ezekiel-platesand-legend-of-temple.html`: WebFetch needed approval, and nobody answered. Not retried.
- The BAS sidebar and article pages were not opened (search titles only).
- Davila 2013 (*Treatise of the Vessels* translation) is not in the corpus.
