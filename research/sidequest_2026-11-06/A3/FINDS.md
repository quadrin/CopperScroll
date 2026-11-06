# Side-quest A3: Albright Jerusalem 1:2,000 sheets (1921–28) and the IAA Mandate archive, 6 Nov 2026

Inputs read: the 12 sheets (Drive folder `1Iu4iRoRu6p_OV6pWvBpS3zSc-1ldusWC`; re-fetched byte-identical from the AIAR Alma viewer `https://aiar.userservices.exlibrisgroup.com/view/delivery/972AI_INST/127799590002696/<file_pid>`, with SHA-256 equal to `manifest.json`). Each PDF holds a single JPEG of about 5,700 × 6,000 px, about 5.1 px per metre on the ground. Comparison layers: `research/regional/asi_jerusalem/sites.csv`, `research/regional/tombs/tombs.csv`, `research/regional/water_systems/water.csv`, and OSM (Overpass, `https://overpass.private.coffee/api/interpreter`, query in "Seed / reproducibility").

Data in this folder: `albright_sheet_georef.csv` (frame pixels and Palestine-grid/WGS84 corners of all 12 sheets), `control_points.csv` (11 control points and their residuals), `albright_imprints.csv` (survey, addition, revision and print dates read from each sheet's imprint). This folder holds no coordinates of unrecorded features. Those are in `/home/claude/swarm/private/A3/`.

---

FIND CARD
Title (one line): The 12 Albright sheets sit on one exact 1-km sheet grid whose lines are not Palestine-grid kilometre lines (offset about 326 m W and 451 m N), and the set mixes a 1925 print state with the 1927–28 one.
Lane: A3
What is odd (2–4 sentences): The sheet frames measure 1,000 m on a side (scale bar: 1,022 px = 200 m; frames 5,080–5,112 px), and all 12 sheets fit one regular grid with a single translation. Fitted to 11 OSM-located gates, tombs and pools on 6 sheets, the sheet edges fall at Palestine 1923 grid (EPSG:28191) E 169,674 + n·1000 and N 130,451 + n·1000. The fit is translation only, with RMS 6 m. A full affine fit improves this only to 4.4 m (scale 1.0015), so the Mandate sheets and the modern grid differ by no measurable rotation or scale. The sheet lines are therefore not kilometre lines of the grid adopted in 1922. Separately, V-G and VII-F carry the January 1925 Survey of Egypt print (25/195; surveyed July 1924 and August 1922 respectively), while the other sheets are Survey Office Jaffa prints of Aug 1927 to Feb 1928, "revised" in 1927. V-F was printed in February 1928, after the catalogue's 1922–27 range.
Evidence (exact sources: file path / page / figure / frame / coordinates): The sheet JPEGs extracted from `25-27-*.pdf`. The frame lines are in `albright_sheet_georef.csv`. Control-point residuals are in `control_points.csv`. Examples: Damascus Gate VI-F +4.8/+0.9 m; Tomb of Absalom VI-G +1.6/+5.8 m; Tombs of the Kings VII-F +6.4/−7.2 m. As an independent check, the sheet labels "Cave" (Minor Sanhedrin) and "Tomb" (Zachariah) land 6 m and 14 m from their OSM points. Imprints: lower-left and lower-right margins of each sheet (`albright_imprints.csv`). VI-F alone has hand-drawn orange quarter-sheet (250 m) lines, at px x = 1552 and 4104 and y = 1738 and 3024.
Literature check (queries run, result, tag): Web searches "Survey of Palestine Jerusalem 1:2,000 plan sheets 1922 1927 'Jerusalem Plan' sheet grid georeferenced" and "Jerusalem town survey 1:2,000 1920s … sheet lines origin Palestine grid offset Cassini". The Wikipedia "Palestine grid" page (grid adopted 1922; it says nothing about the town plans) and the Exeter DAME/Princeton catalogue entries give no sheet-line origin. Repo: no file on main names the sheet IDs (`25-27-`, `Plan VI-F`, `aiar`). The all-branch grep timed out at 100 s. Drive's `ALBRIGHT_STATUS_2026-11-05.txt` says the sheets are still unread. Tag: **NEW TO THE PROJECT** for the georeference and the print-state split. The offset itself may be documented in Survey of Palestine annual reports (1922–28), which were not checked.
Why it might matter: This is the first registration of these sheets. Any cave, tomb, cistern or pool on them can now be placed to about 10 m and compared with ASI/HA records (Card 2 uses this). The offset tells whoever georeferences any other Jerusalem 1:2,000 sheet of the series not to assume Palestine-grid sheet lines. The mixed print states mean V-G and VII-F show the ground as of 1922–24 without the 1927 revision, so comparisons across sheet edges mix dates.
How to confirm or kill it (with data in hand, or what is missing): Re-fit with 10 or more control points on the sheets not yet used (V-D, V-E, VI-D, VII-D, VII-E, VII-G). This needs control points read off the sheet at full resolution; this run did not have them. Compare a 1927 print of V-G or VII-F, if AIAR or NLI holds one, with the 1925 state: features added in the revision would date to 1924–27. Check a Survey of Palestine annual report for the Jerusalem town-survey origin. The offset would be killed by a published statement that the plans were drawn on Palestine-grid km lines together with a demonstration that the OSM control points are biased by about 400 m (very unlikely: 11 points agree to 6 m).
Confidence: high (fit and imprints); medium (that no publication states the offset)
Touches the Copper Scroll? maybe: it makes the 1920s Jerusalem sheets usable for the Jerusalem entries' site files, but changes no assessment.

---

FIND CARD
Title (one line): Ten "Cave"/"Tomb" labels on the 1921–27 sheets lie 113–274 m from any record in the project's ASI, tomb, water and OSM layers.
Lane: A3
What is odd (2–4 sentences): After georeferencing (Card 1), every OCR hit for cave/tomb/cistern/pool words was compared with the four layers. About 20 hits fall within 6–94 m of a recorded feature, and the named ones (Absalom 23 m, Zachariah 14 m, Minor Sanhedrin 6 m, Hezekiah's Pool 9 m, Siloam 24 m) confirm the registration. Ten labels have no record within 100 m. They are listed below by sheet and 250-m cell (A–D west→east, 1–4 north→south inside the sheet frame); coordinates are in `/home/claude/swarm/private/A3/A3_unmatched_candidates_PRIVATE.csv`. Several sit in the densely surveyed Wadi el-Joz and Ras el-ʿAmud, where Kloner's Survey of Jerusalem records individual caves, so a 150–270 m gap is unexpected.
- U1 V-E cell B1, "Cave": S of the Orphanage (Sœurs du Rosaire), on the knoll at spot height 792; 141 m from the nearest record.
- U2 V-E D1, "Caves": N of the Jôret el-ʿInab houses; 126 m.
- U3 V-G A1, "Tomb", and U4 V-G B1, "Cave": Ras el-ʿAmud, on either side of an unlabelled hachured oval about 30 × 40 m; 113 m and 167 m.
- U5 V-G A3, "Cave": grounds of the Benedictine Convent & Seminary, Mount of Offence; 154 m.
- U6 VII-F C2, "Cave": Wadi el-Joz, by the Municipality "Filters / Drainage Works"; a second "Cave" about 100 m S was not OCR'd; 109 m.
- U7 VII-F B2, "Cave": Wadi el-Joz W slope; 149 m.
- U8 VII-F D3, "Cave" and "Caves": E edge at the VII-G join; 236 m.
- U9 VII-F C4, "Cave" ×2: by the house at spot heights 769.5 and 770.76; 179–194 m.
- U10 VII-D A1, "Cave": open ground E of a path, S of spot height 814.2; 274 m.
Evidence (exact sources: file path / page / figure / frame / coordinates): Sheet pixel positions are in the private CSV. Hits against the layers are in `/home/claude/swarm/private/A3/A3_hits_vs_layers_PRIVATE.txt`. Comparison layers as listed in the header. Every label above was checked by eye on full-resolution crops; the montages are not kept.
Literature check (queries run, result, tag): Layer comparison only (ASI sites = Kloner Survey of Jerusalem records on map 102 etc.; tombs.csv includes WBADB and IAA phase-4 rows). The Kloner volume text, HA reports and IAA Mandate site files were not read at page level for these spots. Tag: **NEW TO THE PROJECT** (as candidates). Not yet shown to be new to the literature.
Why it might matter: Each is either a feature lost to 20th-century building, a feature recorded under a site point more than 100 m away, or an unrecorded cave or tomb. Wadi el-Joz (U6–U9) and Ras el-ʿAmud (U3–U4) are rock-cut tomb zones where the third case is plausible.
How to confirm or kill it (with data in hand, or what is missing): For each candidate, read the ASI records within 300 m (survey.iaa.org.il record IDs are in sites.csv) and the HA reports for the same 250-m cell (`hadashot/report_index.json`); if a record describes a cave at the spot, kill that candidate. Check the 1940s Palestine Open Maps 1:20,000 and the RAF 1940s layer for the oval at U3–U4. Recall is incomplete: OCR (tesseract, psm 11) found only about 44 feature words on 11 sheets and missed visible labels (for example the second Wadi el-Joz "Cave" and the V-G "Cistern"s), and VII-E was not swept. A full manual label read of the sheets would give a fuller list.
Confidence: low
Touches the Copper Scroll? no (Jerusalem tombs and caves in general; none is tied to an entry)

---

## Dead ends
- Full-sheet OCR as a label inventory: tesseract on binarised 2,000-px tiles reads "Cave" as "Gave" and misses many italic labels. It is fine for finding candidates and poor for listing everything.
- IAA Mandate "text extractions" in the bucket: `reading/iaa_mandate/` holds a single scanned PDF (145 MB, Holy Sepulchre/Nativity correspondence). It is not text and is too large to pull under the machine rules.
- IAA Mandate further-reading notes (Drive 06/IAA Mandate archive/04): 25 matching notes, all on Jericho and the Judean Desert (Cypros, ʿAin Duk, Wadi Qelt, Nuseib). None concerns Jerusalem caves, tombs or cisterns.
- "Features that moved between editions": the Albright set has one copy per sheet, so no within-sheet edition comparison is possible. The only edition contrast is 1925 vs 1927 print state across sheets (Card 1).
- Jason's Tomb is absent at its OSM point on V-D. This is expected (found 1956) and not a find.
- Nicanor tomb (OSM 31.79323, 35.24488): nothing marked at the predicted point on VII-G. Not followed, because VII-G's frame detection was weak (score 0.25) and its imprint was not captured.
- Unlabelled hachured oval at Ras el-ʿAmud (V-G A1/B1): no label, and its symbol could be a mound, a quarry or a planting. Kept only as context for U3–U4.
- Orange lines on VI-F: hand-drawn 250-m lines that exist on this sheet only. Not a print feature.

## Blocked inputs
- `gs://copper-scroll-cog-1030/reading/iaa_mandate/2026-11-02/IAA_19623_ATQ_199a_Holy_Sepulchre_Nativity_survey_correspondence_native_638_scans.pdf`: 145,432,675 bytes, over the bucket download limit, not in `hexview.py pdfs`. Not opened.
- Drive `IAA_highres_combined_page_register.csv` (`18dn750HpivWncVe-dIbZmaRtv-y7Ny60`, 907 KB): not read (too large for the connector budget). This is the 1,593-note register that would let the Mandate site files be searched for Jerusalem caves and cisterns.
- Overpass `overpass-api.de`: connection reset through the proxy; `overpass.kumi.systems`: timeout after 120 s. `overpass.private.coffee` worked.
- Repo all-branch `git grep` for the sheet IDs: killed at 100 s (timeout). Main-only grep found nothing.
- VII-E OCR not run (sweep stopped to stay within the CPU rules).

## Seed / reproducibility
- Sheet bytes: AIAR file PIDs in Drive `manifest.json` (`1QTtdDIPHZXdBYqyvCfqz2g-SA4L4_VwF`). URL pattern `…/view/delivery/972AI_INST/127799590002696/<file_pid>` returns the PDF directly. Image: `pdfimages -j`.
- Mosaic model: sheet (row r ∈ {V,VI,VII} → 0,1,2; col c ∈ {D,E,F,G} → 0..3). Then PG1923 E = 169674.1 + 1000c + 1000(x−L)/(R−L) and N = 130451.1 + 1000r + 1000(B−y)/(B−T), with L, R, T, B from `albright_sheet_georef.csv`, followed by EPSG:28191 → 4326 (pyproj).
- OSM query: `nwr[historic~tomb|archaeological_site|ruins|memorial|monument|wayside_shrine]`, `natural~cave_entrance|spring`, `man_made~cistern|water_well|reservoir_covered|water_tank|tunnel`, `water~pond|reservoir|basin`, and name/name:en ~ Gate|Tomb|Pool|Cave|Cistern|Grotto|Birket|Quarr, in bbox (31.755, 35.185, 31.810, 35.262). 293 elements, fetched 6 Nov 2026.
- Scripts used are in `/home/claude/swarm/scratch/A3/scripts/` (ocr_sweep, frame2, geo, fit, hits, compare, near, montage).
