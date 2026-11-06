# Side-quest A3, round 2: Albright's Jerusalem 1:2,000 sheets and the IAA Mandate archive, 6 Nov 2026

Inputs used in this round:
- The 12 AIAR sheets, re-fetched from the Alma viewer. All 12 SHA-256 values equal `manifest.json`.
- A second, earlier copy of the same series: the National Library of Israel's Eran Laor set on Wikimedia Commons, category "Survey of Palestine maps of Jerusalem 1:2,000, 1925". It has 27 files: the index sheet, 24 plan sheets and two other files (list in `nli_1925_set_commons.csv`). This set is new to the project; no file on main, on the branches or in round-1 output names it.
- The full ASI Map 102 (Jerusalem) and Map 101 (Ein Kerem) GeoJSON, English and Hebrew, from `survey.iaa.org.il/aspxService/Service[_Eng].aspx/GetPolygonsSites`, with full site descriptions. There are 864 records; round 1 used only the 3-km subset in `sites.csv`.
- All Hadashot English texts (bucket `hadashot/derived/hadtext_pdftotext.tgz`). 216 map references fall inside the sheet area.
- The IAA Mandate page register (Drive `18dn750HpivWncVe-dIbZmaRtv-y7Ny60`, 1,593 notes). Round 1 could not open it.

Data in this folder:
- `nli_1925_set_commons.csv`: the NLI file list and which sheets overlap the AIAR set.
- `edition_changes_1925_vs_AIAR.csv`: the changes seen between editions.
- `candidate_verdicts.csv`: a verdict for each of round 1's U1–U10. Coordinates are left out.
- `asi_distance_null.csv`: the random-point test.

Private (`/home/claude/swarm/private2/A3/`): the candidate coordinates and all crops (sheet crops with ASI overlays, edition pairs, Citadel corner, imprints).

---

FIND CARD
Title (one line): The 1:2,000 Jerusalem Town Survey sheet grid has its false origin exactly 5 km south and 5 km west of the Citadel: the corner shared by sheets V-E, V-F, VI-E and VI-F falls inside the Citadel.
Lane: A3
Round-1 link: A3-1 (sheet grid offset from Palestine-grid km lines). This card supplies the origin that A3-1 left unexplained.
What is odd (2–4 sentences): Round 1 showed that the sheet lines sit about 326 m W and 451 m N off the Palestine-grid kilometre lines, and could not say why. The index sheet of the series ("INDEX TO 1:2,000 JERUSALEM TOWN SURVEY", printed on the verso of NLI sheet V-C, Survey of Egypt 25/195) labels columns A–H from west to east and rows I–IX from south to north. So the corner shared by V-E, V-F, VI-E and VI-F lies exactly 5,000 m east of the west edge of column A and 5,000 m north of the south edge of row I. On the sheets that corner falls inside the Citadel. All four sheets print the same corner name, "The Citadel (Al Qalʿa)". On VI-F the centre of the "David's Tower" symbol is 48 m E and 65 m N of the corner, so about 81 m away. The town survey therefore used a local grid with its false origin 5 km S and W of a Citadel point. This copies the Palestine grid's own rule (false origin 100 km S and W of Ali el-Muntar) at town scale, and it explains why the sheet lines do not fall on Palestine-grid kilometres.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- The index: Commons `File:Survey_of_Palestine,_Jerusalem_00-INDEX_(FL191853708_2367708).jpg`, lower half, column letters A–H and row numerals I–IX, with the note "To identify a sheet, the number of its row and the letter of its column are taken".
- The corner: AIAR VI-F JPEG px (288, 5564), V-F (304, 486), VI-E (5386, 5558) and V-E (5378, 458), from `out/A3/albright_sheet_georef.csv`. The corner is at Palestine 1923 grid E 171,674.1 / N 131,451.1, which is WGS84 31.775756 N, 35.227863 E (the Citadel's west side, just S of Jaffa Gate).
- The implied grid: false origin (SW corner of I-A) at PG 166,674.1 / 126,451.1 = 31.730662 N, 35.175093 E. NE corner of IX-H at 174,674.1 / 135,451.1.
- Crops: `private2/A3/crops/corner_quad.png`, `citadel_6F.png`, `citadel_5F.png`, `citadel_W.png`.
Literature check (queries run, result, tag):
- Web: "Survey of Palestine Jerusalem town survey 1920s plan sheets origin Citadel 'Tower of David' triangulation"; "Gavish 'Survey of Palestine' Jerusalem town survey 1921 1:2,500 local origin"; "'Jerusalem town survey' 1:2,000 1921 origin '5 km' Citadel A-H I-IX". These returned the Wikipedia Palestine grid page (false origin 100 km S and W of Ali el-Muntar, adopted 1922; nothing on town plans), Gavish's book page (not readable), Exeter DAME 1939 index metadata (no grid) and the Commons pages (no description of the sheet system).
- Repo (main and branch_only) and round-1 output: "Jerusalem Town Survey", "FL1918537", "Eran Laor": 0 hits. "Citadel" appears only as a place name.
- Tag: **NEW TO THE PROJECT**. Probably **NEW TO THE LITERATURE** for the stated origin. Gavish (2005) and the Survey of Palestine annual reports were not readable here and may state it.
Why it might matter: Anyone can now georeference any sheet of the series from its name alone: sheet (row r, column c) has its SW corner at PG E 166,674.1 + 1000·(c−A), N 126,451.1 + 1000·(r−1), with residuals of about 6 m (A3-1). This covers the 15 NLI sheets outside Albright's 12 (I-E, II-D … IX-G, V-C, VI-C). They extend coverage south to Mar Elias and north to Shuʿfat, so their cave, tomb and cistern labels can be placed without control points.
How to confirm or kill it (with data in hand, or what is missing): Check a full-resolution NLI sheet outside the AIAR set (for example IX-E or I-E) against OSM points; it should fit the formula with no new parameters. Kill: a published origin that differs, or a sheet whose landmarks miss the formula by more than about 20 m. The exact Citadel point (minaret, Phasael tower or a station) is not marked by a triangulation sign at the corner. The annual reports or the field books would name it.
Confidence: high (the index and the 5 km geometry); medium (that the Citadel was the defined origin rather than a point chosen so that the city sits near the middle of the index).
Touches the Copper Scroll? no (survey history; it makes the sheets usable for any Jerusalem site file)

---

FIND CARD
Title (one line): The February 1928 print of sheet V-F adds the Macalister–Duncan "Ancient Wall & Tower" on Ophel and other revisions, while its imprint claims only "Surveyed … April 1922"; the NLI 1925 set gives earlier states of six Albright sheets.
Lane: A3
Round-1 link: new. It answers the lane brief's "features that moved between editions", which round 1 listed as impossible because only one copy per sheet was held.
What is odd (2–4 sentences): I registered NLI's January 1925 V-F (Survey of Egypt 25/195; "Surveyed in April 1922") to AIAR's V-F. The frame fits to a 1-px shift, and ink was differenced after a 7-px dilation. The 1928 print adds:
- the label "Ancient Wall & Tower", with a drawn wall line and tower on the eastern crest of Ophel (the Macalister & Duncan PEF excavation, 1923–25);
- a row of "Stones" signs on the slope below;
- new buildings and a cistern ("c") in Silwan;
- traverse-station numbers (21/56, 28/56, 29/56) beside points that are unnumbered in 1925;
- a changed spelling (Khatuniya → Khatuniye).

The AIAR imprint reads only "Surveyed by the Survey of Palestine, April 1922". It has no "revised" line, unlike V-D, V-E, VI-D, VI-E and VII-D/E. So the 1928 V-F is an unannounced revision that records a 1923–25 excavation. V-E and VII-E were also differenced. The changes there are 1924–27 building (Talbiye; the railway yard re-laid, with "Reservoir" added) and new labels at the Sheikh ʿUkkasha cemetery ("Tombs", "Esh Sheikh Okashe", "Esh Sheikh Qeimar").
Evidence (exact sources: file path / page / figure / frame / coordinates):
- NLI files: `File:Survey_of_Palestine,_Jerusalem_17-V-F_(FL191853722_2367708).jpg`, plus 15-V-E (FL191853721) and 23-VII-E (FL191853728), read as 3840-px Commons thumbnails.
- AIAR files: `25-27-5-F.pdf`, `-5-E`, `-7-E`.
- The wall label sits about 743 m E and 207 m S of the V-F NW corner (PG ≈ 172,417 / 131,244). Round 1 had already found the OCR words "Ancient" and "Tower" 23–36 m from OSM's Stepped Stone Structure.
- Table: `edition_changes_1925_vs_AIAR.csv`. Crops: `private2/A3/crops/pairs_VF_a.png` (pair 3 = the wall), `pairs_VF_b2.png`, `pairs_VE_VIIE.png`, `imprints_VF.png`.
- Scripts: `scratch/A3r2/scripts/diff_ed.py`, `pairs.py`.
Literature check (queries run, result, tag):
- Web: "Macalister Duncan 1923-1925 Ophel tower wall Survey of Palestine 1:2,000 Jerusalem plan V-F 1928 'Ancient Wall'". This found the excavation literature (PEF Annual 4; Substack "Unwinding the Stepped Stone Structure"; BAR "The Wall That Nehemiah Built"). None mentions the Survey's plan recording it.
- Repo: the NLI set is absent.
- Tag: **NEW TO THE PROJECT** (the NLI edition and the diff); **NEW TO THE LITERATURE** (probably) that the 1928 V-F silently records the 1923–25 excavation.
Why it might matter: The 1928 V-F gives an independent, surveyed 1:2,000 position for the Macalister–Duncan wall and tower as left in 1925, before Kenyon's and Shiloh's work. It can be compared with the later plans of the Stepped Stone Structure. More generally, the round-1 assumption that a sheet's imprint dates its content fails for V-F. Imprints should not be used to date what a sheet shows without an edition comparison.
How to confirm or kill it (with data in hand, or what is missing): Overlay the drawn wall on a modern plan of Area G or the Stepped Stone Structure (City of David reports are in Drive 02). Kill: Macalister–Duncan's published plan puts their tower more than about 20 m away, which would mean the label marks something else. Also diff VI-E and VII-D (Commons answered HTTP 429 for both) and V-D (my frame detection failed on that scan).
Confidence: high (the diff and the imprints); medium (that the label is Macalister–Duncan's work rather than an earlier PEF trench)
Touches the Copper Scroll? maybe: Ophel/City of David is on the project's Jerusalem list, but no entry assessment changes.

---

FIND CARD
Title (one line): Round 1's ten "unmatched" cave/tomb labels: distance to an ASI point cannot decide the question; read against the full Map 102/101 texts, one is killed (U5 = ASI 102/480, plotted 195 m off), two are probably recorded (U1, U9), two are covered by a collective record (U6, U7), and five stay open (U2, U3, U4, U8, U10).
Lane: A3
Round-1 link: A3-2 (WEAKENED by R3)
What is odd (2–4 sentences):
- **The random-point test.** R3 noted that the distances run on without a break. The test makes this exact. 20,000 random points on the 12 sheets, with the Old City excluded, lie a median 127 m from the nearest ASI point (P90 260 m). The 43 OCR labels lie a median 94 m away. The U-labels fall at the 41st–92nd percentiles. Proximity to an ASI point therefore says almost nothing, and only the record texts can settle a label.
- **Reading the full texts.** U5, the "Cave" at the NE corner of the "Convent & Seminary (Benedictine)", is ASI 102/480: "vaulted hall … underlying the E wall of the Benedictine Monastery of St. Abraham" (Vincent 1904). The ASI point of that record is plotted 195 m due S of the convent drawn on the 1924 sheet.
- **U9.** The cave plus a dashed underground circle beside it fits ASI 102/367 (a cave with a plastered cistern N of it).
- **U1.** The open knoll S of the Sœurs du Rosaire is probably the YMCA cemetery of 102/400 (Iliffe 1932, two burial caves). The YMCA was built after the 1927 revision.
- **U6–U7.** These fall under 102/260, whose text records "additional cuttings" further along the Wadi el-Joz.
- **The open ones.** U2 (two underground circles N of Jôret el-ʿInab; none of three nearby records describes them), U3/U4 (Ras el-ʿAmud ridge; the only records are on the cemetery slope below), U8 (two labels against one recorded cave, ASI 102/258, 236 m away) and U10 (a cave mouth in Romema; the nearest record, ASI 101/122, is 274 m away with no locational support).
- **The oval.** The index sheet's legend shows that the unlabelled hachured oval next to U3/U4 is the "Quarries" sign. That closes a round-1 dead end.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `candidate_verdicts.csv` (one row per label, record and reason) and `asi_distance_null.csv` (seed 20261106).
- ASI texts: https://survey.iaa.org.il/#/MapSurvey/63/site/<id> (Map 102 = GIS map 63; Map 101 = 72). Record 480's bibliography is "Vincent 1904; Kloner 1980a:31 (No. 3-43); IAA Archives/Mandate (File 110, Area C2; Report from 1941)". Its Hebrew text names the place "אכסניית אברהם הקדוש".
- HA texts checked: vol-124 01976, vol-132 25822 (U2) and vol-125 05405 (U8).
- Crops with ASI overlays: `private2/A3/crops/U*.png`, `mosaic_a.png`, `mosaic_b.png`. Coordinates: `private2/A3/A3_unmatched_candidates_PRIVATE.csv`.
- Legend: the NLI index sheet (Card 1), "Conventional Signs" (Quarries; C = Cistern; Sheikhs' Tombs; Traverse Points).
Literature check (queries run, result, tag):
- ASI full texts were read for every record within 400 m. Their in-text "map ref." values (242 refs; 88 in the area) were all more than 250 m from the open labels.
- HA English map references (216 in the area) lie 138–286 m away and describe other features.
- The IAA Mandate register (1,593 notes) has no note on these spots. Its Jerusalem folders are the Kidron monuments, Siloam, the quarries and the sub-district.
- Tag: **NEW TO THE PROJECT** (the settlement). The ASI 480 point offset is **NEW TO THE LITERATURE** as far as checked, but the point may mark the record's second item, the 1941 cave "to S", so it is not counted as an error.
Why it might matter: The A3-2 list shrinks to five open labels: U2, U3, U4, U8 and U10. Their coordinates stay private. The same method, full ASI texts against the drawn setting, can now be run on the 15 NLI sheets outside the AIAR set, which no project layer has read.
How to confirm or kill it (with data in hand, or what is missing): For U2, U3/U4, U8 and U10, Kloner's printed volumes (Survey of Jerusalem, NE and NW sectors) have site plans. They are not in the corpus. For U8, a full-resolution read of VII-G at the join would show whether the "Caves" continue onto that sheet. For U5, the IAA Mandate file 110 (1941) would place the "cave to S"; it is not among the 34 supplied folders.
Confidence: medium (the null test and U5); low (the "probably recorded" calls)
Touches the Copper Scroll? no

---

## Dead ends
- IAA Mandate page register (1,593 notes) as a source for Jerusalem caves: the Jerusalem folders are the Kidron monuments (ATQ 706, mostly 1937–46 gate and railing work), Siloam, Solomon's Quarries and the sub-district (Beit Vegan, Kh. Salih). None concerns the A3 candidate spots.
- HA 125 report 05405 (Naḥal Qidron survey, A-4423): its map ref 222747/632989 falls 149 m from U8, but the report describes the southern sector (Kh. Beit Sahur, Umm Leisun). `haesi_features/phase2_2026-10-10/reports.csv` already flags it as a "possible misprint". Not new.
- ASI in-text map references (242) as a finer locator: none lies within 250 m of an open candidate.
- Citadel minaret or trig station as the exact origin point: OSM Overpass timed out or was reset on three mirrors, and the sheets show no triangulation sign at the corner. Left open (Card 1).
- Web literature for the town-survey origin: Gavish's book and the Survey of Palestine annual reports are not readable online here.
- NLI V-D edition diff: the frame detector picked a wrong neat line (frame 2,996 × 2,796 px instead of about 3,100 square). Not redone.
- Edition diffs of V-E and VII-E: almost all differences are 1924–27 building and labels. No cave, tomb or cistern was added or removed except new "c" cisterns at houses.

## Blocked inputs
- Commons thumbnails of `Survey_of_Palestine,_Jerusalem_20-VI-E_(FL191853725_2367708).jpg` and `22-VII-D_(FL191853727_2367708).jpg`: HTTP 429 (rate limit) on two attempts. The Commons API also answered "You are making too many requests" for imageinfo and category queries; the category HTML page worked.
- Commons original of 28-VIII-F (211 MB, 14,519 × 15,754 px): not downloaded (over the machine rules). Only 3840-px thumbnails were used, so labels smaller than about 2 m on the ground may be lost.
- Overpass (`overpass.private.coffee`: timeout at 90 s and 60 s; `overpass-api.de`: connection reset; `maps.mail.ru`: empty reply) for the Citadel features.
- `gs://copper-scroll-cog-1030/reading/iaa_mandate/2026-11-02/IAA_19623_ATQ_199a_…pdf` (145 MB): still not opened (unchanged from round 1).

## Seed / reproducibility
- Random-point test: Python `random.seed(20261106)`, 20,000 points uniform over sheet-grid 0–4000 × 0–3000 m. Old City rectangle excluded: lon 35.2275–35.2370, lat 31.7715–31.7835.
- ASI GeoJSON: `GetPolygonsSites?MapId=63|72&sitesId=null`, with header `Content-Type: application/json`, fetched 6 Nov 2026 about 12:45 UTC.
- Commons thumbnail URL pattern: `https://upload.wikimedia.org/wikipedia/commons/thumb/<md5[0]>/<md5[0:2]>/<name>/3840px-<name>`. Only standard widths (1920, 3840) work; 2400 returns HTTP 400.
- Scripts: `/home/claude/swarm/scratch/A3r2/scripts/` (asi_load, crop, ha_refs, frame_nli, diff_ed, pairs).
