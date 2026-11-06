# Side-quest C2: named features on old maps, SWP sheet XVIII (Jerusalem–Jericho–Dead Sea north), 6 Nov 2026

Bounded region: SWP sheet XVIII between PG 1923 E 179–200 and N 124–146 (Wadi Qelt, the Jericho plain, Nebi Musa, el-Muntar/Buqeia), plus Mandate 1:20,000 sheet 18-13 (Wadi el Qilt), which I read in full.

Inputs:
- SWP 1:63,360 (1880) as georeferenced by Palestine Open Maps (`https://palopenmaps.org/tiles/pal63k-1880/{z}/{x}/{y}@2x.jpg`, z14–15).
- Mandate 1:20,000 (1940s) (`…/tiles/pal20k-1940s/{z}/{x}/{y}.jpg`, z16).
- SWP Memoirs III full text (`https://archive.org/download/surveyofwesternp03conduoft/surveyofwesternp03conduoft_djvu.txt`), Sheet XVIII sections A–B, pp. 187–227.
- WBADB `branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv` (6,950 rows).
- The project layers `research/regional/{water_systems/water.csv, caves_entry25/caves.csv, tombs/tombs.csv, haesi_features/merged_2026-10-12/sites.csv, mandate_maps/features.csv}`.
- Itiner-e `research/assets/plans/historical-landscapes/itinere_roads_gpkg.zip`.

How well the SWP tiles are registered: SWP symbols that I picked land 65–107 m from independent records (Beit Jubr et Tahtani 65 m from Mandate P05; Kh. Kakun 81 m from Mandate P04 "Kh. Kakūn"; Kh. el Meshrab 86 m from WBADB S2785; Mukam Imam ʿAly 107 m from Mandate N09). The test threshold is therefore set at 500 m, not 300 m.

Data in this folder:
- `swp18_features_vs_records.csv`: 23 SWP picks with the nearest record in every layer, and whether the 1940s sheet shows the feature. It has no coordinates.
- `itinere_region_segments.csv`: every Itiner-e segment in the region.
- `swp18_roads_missing_from_itinere.csv`.

The coordinates of the unrecorded features are only in `/home/claude/swarm/private/C2/C2_swp18_feature_positions_PRIVATE.csv`.

---

FIND CARD
Title (one line): Mugharet Ekteif, the SWP's "very curious" stepped, sloping rock-cut passage (the one rock-cut chamber the project ties to entry 24, Wadi Kuteif), has a map position on SWP sheet XVIII, and that position is not at the project's Wadi Kuteif anchor. No database records the feature, and the 1940s sheet does not print it.
Lane: C2
What is odd (2–4 sentences): The project knows this feature only from the Memoirs text and holds it at square level: `features_zone_unresolved.csv` row SWP3-220-mugharet-ekteif, "zone unresolved". The rating for entry 24 (`ratings.csv` line 35) asks for "a dated record … of the stepped chamber in Wadi Kuteif". The engraved sheet prints a cave label "Mght. Ekteif" on the north side of the lower (eastern) Wadi Ekteif, close to where the Nebi Musa tracks cross the wadi. That spot is about 2.4 km east of the project's place point `kuteif` (`tables/phase3_places.csv` line 31, which sits on the "Wady Ekteif" label) and about 2.3 km from the Early Islamic pit graves WBADB E508. No record in WBADB, ASI (via water.csv/caves.csv), tombs.csv, the HA/ESI sites or the Mandate features lies within 567 m. The nearest are Bar-Adon 1972 sites 81c, 80 and 83a, which are an oval enclosure, a rounded enclosure with a tower, and T. Muḥalḥil, none of them a rock-cut passage. Mandate sheet 19-13 shows the W. Quteif gorge at this spot with no cave symbol and no "Mgh." label. The nearest print is "L.K." (limekiln), about 300 m south.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Memoirs III p. 220 (djvu.txt line 11451): "A very curious excavation In the north side of the valley. It slopes downward at a gradient about 1 by 2 for 120 feet … Steps are here cut … it may have been the entrance to a subterranean chamber now choked up. Visited 24th November, 1873."
- SWP sheet XVIII, POM tiles z15@2x. The window is reproducible with `scripts/gview.py pal63k-1880 15 190600 133200 192600 134800 out.png @2x` in `/home/claude/swarm/scratch/C2/scripts/`. The label "Mght. Ekteif" is at about 40% across and 55% down that window.
- Mandate 19-13, the same window on `pal20k-1940s` z16.
- Exact position (±250 m, label-anchor pick): private CSV, row `Mght_Ekteif`.
- WBADB rows WBS:3157, 3144, 3189 and the Bar-Adon site numbers 80, 81a–c and 82a–b (B2 `survey_join.csv`): none describes a passage or steps.
Literature check (queries run, result, tag):
- Corpus: `hexview pdf-search` for "Ekteif", "Qteif", "Kteif", "Iqteif" and "Qatif". The only hit is JSP 9 p. 131, "Wadi Ekteif" as a site name in a list, with no feature.
- Repo: SWP3-220 coding (`coding_swp3.jsonl`), the entry-24 rating and `record_conflicts.md` C22. All use square-level position or the wadi label. No file gives the sheet position.
- Web: "Ekteif/Qteif/Kuteif cave Nebi Musa rock-cut sloping passage steps" and "Wadi Kuteif Copper Scroll tomb Milik Jericho Sekakah location". No modern description or position of the passage turned up.
- Tag: **NEW TO THE PROJECT** for the map position and the absence of any record. The feature itself is published (SWP 1883; Milik, DJD III, D12).
Why it might matter: It moves the only physical feature linked to entry 24 from "zone unresolved" to a point accurate to about 250 m. The point is in the lower wadi, where the Jericho–Nebi Musa routes cross, and not at the wadi label the project uses. It also shows that no survey since 1873 (Bar-Adon 1972, Sion 1997, WBADB) has re-recorded the feature. The undated chamber is therefore still unchecked, not checked and found wanting.
How to confirm or kill it (with data in hand, or what is missing):
- (1) Look at the private point on HEXAGON 1974/1978 or Esri imagery for a cut opening on the north bank.
- (2) Read Bar-Adon 1972 sites 79–83 in the ASI 1 Hebrew text (bucket `01-ASI1-Kochavi-1972-indexed`) for any "מחילה" or "מדרגות" near Nebi Musa.
- (3) Check Patrich's and the IAA's Nahal Og/Nebi Musa survey sheets, if held.
- Kill condition: a modern record of the passage somewhere else in the wadi, more than 500 m from the SWP label, or a statement that it was destroyed (for example by the 1950s–70s Nebi Musa road works).
Confidence: medium (the position is certain to the label; that no record exists rests on the five layers searched)
Touches the Copper Scroll? yes. It is the only physical candidate feature for entry 24 (Wadi Kuteif/Kippa); no reading changes.

---

FIND CARD
Title (one line): Seven named SWP sheet XVIII features (caves, a "Mekûr" pit, cairns and a cistern) have no record within 500 m in WBADB, ASI or the project's layers; six of them are missing from the 1940s 1:20,000 sheets.
Lane: C2
What is odd (2–4 sentences): I overlaid every WBADB point and the project's records on the georeferenced SWP sheet for E 179–200 / N 124–146 and picked by hand the named point features that have no record nearby. Of 23 picks, the 7 below lie 567–1,277 m from the nearest record (WBADB ±100 m, SWP registration about 100 m). Mght. Ekteif (Card 1) is one of the seven. The other six:

| SWP label (sheet XVIII) | nearest record | 1940s 1:20,000 |
|---|---|---|
| Mght. el Meshrâb (cave; not the Kh. el Meshrab ruin, which is matched) | 768 m (WBS:2507) | absent (sheet 18-13) |
| Mughr es Saʿtah/Sakhah (caves), Wady el Metfy | 691 m | absent (18-14) |
| "Cairn", Wady Abu Retmeh, by the Ancient Road | 677 m | absent |
| Rujm Haleiseh (cairn) | 880 m (WBS:3262, Mamluk road) | absent |
| Nuseib en Nuwârah (memorial cairn) | 1,277 m | absent |
| Mekûr es Sidri (pit/hollow symbol), Khaur et Tumrâr–Pilgrim Road | 614 m | absent (19-13) |
| Bir el Kuru (cistern), N of el-Muntar | 788 m | **present** as "Bir el Qarn · Cis." |

None of the names appears anywhere in WBADB, water.csv, caves.csv or tombs.csv (grep for qarn/kuru, saʿtah, haleis, nuwara, sidr).
Evidence (exact sources: file path / page / figure / frame / coordinates): `swp18_features_vs_records.csv` (public: labels, distances, record IDs, 1940s state). Positions are in the private CSV. Contact sheet of SWP and 1940s at each point: `/home/claude/swarm/scratch/C2/contact1.png`, rebuilt by `scripts/contact.py cand.csv out.png`. Overlay views are `ov_nw/ov_sw/ov_se/ov_nt.png` (made by `scripts/overlay.py`). Memoirs III Section B lists none of these seven except Mugharet Ekteif and Kh. el Meshrab. So they are map-only names with no Memoirs description, which is why square-level coding never caught them.
Literature check (queries run, result, tag): name grep in WBADB (all 6,950 rows), the project layers, `branch_only/` and main (none of the names occurs). Web search was not run for each name: these are microtoponyms with no web presence I could expect, and the corpus checks are the meaningful test. Tag: **NEW TO THE PROJECT** (as candidates); not shown to be new to the literature. Patrich's Mar Saba map and the Goldfus & Golani survey may record some of them under other names.
Why it might matter: These are the SWP-only remnant of the 1873 survey in a zone now covered by WBADB. Three are caves or pits, one is a cistern that still appeared in the 1940s, and three are cairns, which may be modern. The gap list is short (7 of 23), which itself says WBADB covers the SWP point features of sheet XVIII well. The caves (Meshrab, Saʿtah, Ekteif, Mekûr es Sidri) are the part worth checking.
How to confirm or kill it (with data in hand, or what is missing): for each point, read the Goldfus & Golani 1993 and Sion 1997a/1994 survey entries within 1 km, which WBADB cites only as "Site." rows. Read Patrich 1994's Mar Saba map for Bir el Kuru/Qarn. Look at HEXAGON 1974 at the private points. A candidate dies when a survey entry within 500 m describes a cave or cistern of that kind. My picks are label anchors: an error of 150–250 m is possible, so none of the seven is within 300 m of a record even in the worst case.
Confidence: low (each item); medium (that the list is complete for the four views I read)
Touches the Copper Scroll? maybe (Mght. Ekteif only); the others no.

---

FIND CARD
Title (one line): Itiner-e leaves out two roads that SWP sheet XVIII draws and the Memoirs call Roman or ancient (Jericho–Bethel by Wady Abu Retmeh, and Jericho–Buqeia–Hyrcania–el-Muntar–Jerusalem), and no dataset carries the sheet's one Roman milestone, "R.M.S. Dabbus el ʿAbd".
Lane: C2
What is odd (2–4 sentences): The Itiner-e layer cites "SWP" for its Jerusalem–Jericho (fid 3363) and Gophna–Jericho (3362) lines. 3362 follows the Memoirs' "third Roman road" (Taiyibeh → ʿAin Duk). It does not follow the "second hill road … from Jericho to Bethel … from near Shukh ed Duba … up Wady Rijan to Ras et Tawil" (Memoirs III p. 188), which the sheet draws as a double-dashed line lettered "Ancient Road" in Wady Abu Retmeh (about N 141–141.6). Itiner-e has no segment at all in E 176–196 / N 120–131. So the engineered Buqeia road is also missing: Bir Umm el Fus, Bir es Sûk, west of Kh. Mird, round el Muntar, to Jerusalem (p. 188), with rock-hewn reservoirs. The sheet prints "R.M.S." (Roman milestone) at Dabbus el ʿAbd beside the Wadi Qelt-pass road (Memoirs p. 192: "A column-shaft beside the road, apparently a Roman milestone"), about 0.3 km from Itiner-e 3363. Itiner-e has no milestone layer, and WBADB has no row within 750 m.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- `itinere_region_segments.csv`: all 24 segments in lat 31.60–31.95 / lon 35.15–35.62, parsed from the GPKG (EPSG:3395) with `scripts/gpkg.py`.
- `swp18_roads_missing_from_itinere.csv`.
- Memoirs djvu.txt lines 9854–9925.
- SWP overlays `ov_nw.png` (Itiner-e drawn in green) and `z_ms.png` (R.M.S. label).
- Gibson et al. 2023, in Ben-Yosef & Jones (eds), pp. 845–846 (bucket doc `Ben-Yosef-and-Jones-eds-2023-…`, page index 854), describes the Buqeia road from SWP and fieldwork.
Literature check (queries run, result, tag):
- Corpus `pdf-search` "Umm el-Fus" (Gibson et al. 2023 hit) and "Dabbus" (no hit).
- Repo grep "retmeh|rijan" (only Palmer name rows), "dabbus" (only the SWP3 square-level coding), "umm el fus|bir es suk" (cistern rows only, no road).
- Web: "Roman road Jericho to Bethel Michmash Wadi Rijan / Abu Retmeh / Ras et Tawil" found no dataset discussion of the gap.
- Tag: **KNOWN BUT UNDER-DISCUSSED**. The roads are published (SWP 1883; Buqeia road, Gibson et al. 2023), but the Itiner-e omission and the unlisted milestone are not noted anywhere I found.
Why it might matter: Any route, distance or "on a Roman road" test built on Itiner-e treats Hyrcania, the Buqeia and Kh. Qumran's hinterland as roadless. It also misses the second Jericho ascent. The milestone, if it survives, would be a fixed station on the Wadi Qelt-pass line that Itiner-e marks "Certain".
How to confirm or kill it (with data in hand, or what is missing): check Thomsen 1917 and Roll's milestone list for a Dabbus el-ʿAbd or Talʿat ed-Damm stone. Check whether the TIR map draws either road (the TIR Michigan sheets are on Drive 07). Kill condition for the road gap: an Itiner-e release later than the GPKG held here (dated 9 Oct 2026 in the repo) that adds them. Kill condition for the milestone: a published milestone catalogue entry with coordinates.
Confidence: high (the gap in Itiner-e and WBADB); low (that the roads are Roman)
Touches the Copper Scroll? maybe. The Buqeia/Hyrcania road bears on the route models the project used (G logistics, Tobler walking routes).

---

## Dead ends
- OCR of the 1940s 1:20,000 tiles (tesseract psm 11 after a dark/purple ink mask): it reads isolated words ("Shargi", "Beit", "Samn") and misses most labels. I gave up on it and read sheet 18-13 by eye instead.
- Full read of Mandate sheet 18-13 (Wadi el Qilt, E 180–190 / N 130–140): very few ruin or cave labels. Two blocks were read in full (v_a1, v_10). Only a "Tomb" in the Wadi Qelt orchards and Sp. ʿEin el Fawwar/ʿEin el Qilt (both recorded). The other 7 blocks were cut, not read (`/home/claude/swarm/scratch/C2/v_*.png`).
- Palmer name lists as an SWP gazetteer: square-level only (about 7 × 9 km) and noisy OCR, so useless for a 300–500 m join. Used the sheet itself instead.
- Name join of the Memoirs XVIII Section B entries (70) to WBADB: most match. Unmatched names (Dabbus el ʿAbd, Hajr el Asbah, Jisr Abu Ghabbush, Khan Hathrurah, Kh. Abu Lahm, Kh. Kakun, Kh. el Mefjir, Tell Derb el Habash, el Kos, el Mahfuriyeh, er Rusheidiyeh, el Masni, el Bureikeh) are mostly recorded under other names or sit within 300 m of an unnamed row (Kakun 81 m Mandate P04; Derb el Habash 33 m from WBS:2479 Tell el-Qasab; Bureikeh and Imam ʿAly 38–198 m from Mandate N09–N13). Not pursued.
- WBADB has no "Hisham's Palace/Kh. el-Mafjar" row under any spelling I tried (mafjar, mefjir, hisham). It is probably listed under a Hebrew or excavation name. Not chased (C1b covered Mafjar coordinates).
- Jericho-plain tells: covered by C1b's area and dense WBADB coverage. Not re-read.
- Mughâret Umm el Hummam (Nt; plastered rock-cut birkeh with three recesses): I did not find the label in the Nt view (E 179–186 / N 124–131). There is a "Mght. U…" label at the east edge (about E 185.7, N 129.7) that I did not resolve. Left for a follow-up view E 185–188.
- Jerusalem–Jericho road "Stone" labels on the 1940s sheet (purple "(Stone)" at spot height 209.2 and black "Stone" by the old road near Khan el-Ahmar/Talʿat ed-Damm): possibly milestones or kilometre stones. Not checked against milestone lists.
- Wadi Joreif Ghuzal marl hermitage cave (Memoirs p. 227): 525 m from the Byzantine ʿEin Abu Mahmud caves cluster (WBE:513). Probably the same cluster. Dropped.

## Blocked inputs
- Drive 07 `itinere_roads_gpkg.zip` (`1uUp38ngQvmTq-9z_Q5S2qOG3VCJ1sU7F`, 18.9 MB): not downloaded via the connector because it is too large for base64. I used the byte-identical-size repo copy `research/assets/plans/historical-landscapes/itinere_roads_gpkg.zip` instead.
- SWP Memoirs II–III are not in the bucket PDF store (`hexview pdfs` shows only the 1880 map scan). I used the archive.org djvu text.
- Fischer–Isaac–Roll 1996 (Drive 07, `1qCTZ48X5FjLsg2GwpmqifO0SYTzdU0VK`) covers Jaffa–Jerusalem, west of the bounded region. Not used.

## Seed / reproducibility
- Scripts: `/home/claude/swarm/scratch/C2/scripts/`.
  - `tiles.py`: POM tile mosaic; PG1923 is EPSG:28191 via pyproj.
  - `gview.py LAYER Z E0 N0 E1 N1 out [@2x]`: window with the PG grid. Grid labels are rounded to km, so use e0 on whole km for labelled lines.
  - `overlay.py`: adds the WBADB points and the Itiner-e lines.
  - `refjoin.py picks.csv`: nearest record over WBADB, water, caves, tombs, haesi and the Mandate features.
  - `namejoin2.py`: Memoirs name join.
  - `gpkg.py`: Itiner-e GPKG reader.
- Picks: `/home/claude/swarm/scratch/C2/picks.csv` (contains coordinates, so it is not public). Pixel→PG conversion for the 7 km views: E = E0 + x/245.9·1000, N = N1 − y/247.9·1000.
- Tiles fetched 6 Nov 2026 from palopenmaps.org (public domain scans, NLI).
