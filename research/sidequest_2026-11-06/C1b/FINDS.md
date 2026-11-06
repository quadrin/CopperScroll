# Side-quest C1b: Jericho plain, lower Wadi Qelt, Jordan valley (6 Nov 2026)

Lane C1b (change across image epochs, Jericho area). I georeferenced the March 1945 1:10,000 photo-mosaic (bucket `photos/Great-Britain-army-517-Field-Survey-Company-Jericho-FL105210-23117f24.tif`) to the Palestine Grid. I used 20 printed grid intersections and a 2nd-order polynomial: RMS 6.8 / 4.0 px, about 6 m. The fit is in `m45_georef.json` and `m45_nodes.json`, and `cmp_1945_esri.py` reproduces it. I then compared nine 1.7 km windows and eight full-resolution windows against Esri World Imagery (tile URLs in `esri_tiles_used.txt`). The comparison panels are private (`/home/claude/swarm/private/C1b/`).

The comparison found no lost ancient feature that I could confirm. Between 1945 and today the whole mosaic area has been built over or levelled. The halftone screen of the 1945 sheet limits it to features of a few metres. While I was placing recorded sites on the georeferenced sheet, two coordinate errors showed up. The two cards below are about those errors. Every location given is that of an already recorded, published site.

---

FIND CARD
Title (one line): Hisham's Palace (Kh. el-Mafjar, PADIS 0012) is mislocated twice: by 1.05 km in ROSAPAT 07 (2011), and by 4.3 km in the project's water inventory (J15), through a "Mafjar" name collision.
Lane: C1b
What is odd (2–4 sentences): ROSAPAT 07 cat. no. 50 (p. 126) gives Qasr Hisham as 31°52'36.95" N, 35°28'8.85" E. Cat. no. 51 (Byzantine monastery) gives almost the same point. This point lies in fields north of Wadi en-Nuʿeima, about 1,045 m ESE of the palace, which is at the Mandate 1:20,000 "Khirbat el Mafjar (R.)" (project item U15, PG 193602/143235). Separately, the project's `water.csv` row `LIT-E29-J15` ("Kh. el-Mafjar water-system aggregate", the same PADIS 0012 early-Islamic palace system) takes its coordinate from ASI 109/5/23 "Khirbet Mafjar (1)", at 31.844490 / 35.473717. That is a different "Mafjar": a channel-and-cistern site beside Tell Mughayfir / Rujm el-Mugheifir, 4.3 km SSE of the palace.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- ROSAPAT text: bucket PDF `Nigro-Sala-Taha-eds-2011-Archaeological-Heritage-in-the-Jeri-9af25da3`, page index 138 (printed p. 126), entries 50 and 51 (`python3 hexview.py pdf-text <doc> 138`).
- Project row: `research/regional/water_systems/water.csv` line 2017, `LIT-E29-J15`, coord_source "ASI 109/5/23 Khirbet Mafjar (1) (plan §6 rule 2 …)". Source row: ASI-109/5/23 (db id 12547), same file. The entry-29 label is in `research/assessments/entry29_jericho_pools/regional_inventory_2026-10-06.md` lines 18 and 48 ("PADIS0012").
- Palace position: `research/regional/mandate_maps/features.csv` U15 (state_2025 = visible_2025). Esri World Imagery z18 shows the palace square and the modern roof over the bath hall at U15. The ROSAPAT point falls on a field track (private panel `esri_mafjar_pair.jpg`; tiles listed in `esri_tiles_used.txt`).
- ROSAPAT is not wrong in general. 11 of the 15 sites I could pair with Mandate features fall within 250 m. Tell es-Sultan is 128 m off and ʿAin es-Sultan 10 m. See `rosapat_vs_mandate_coords.csv`.
Literature check (queries run, result, tag): repo main + all branch-only files grepped for the ROSAPAT coordinate (`52'36`, `31.8769`, `35.4691`): no hit. The repo uses no ROSAPAT coordinates; `water.csv` placed J15 from ASI. Web: the Sapienza PADIS site list (sites.google.com/uniroma1.it/sapienza-padis-project/archaeological-sites) shows no coordinates and no erratum. I did not open the individual PADIS site pages. Tag: **NEW TO THE LITERATURE** (ROSAPAT offset; no erratum found). **NEW TO THE PROJECT** (J15 mislocation).
Why it might matter: Any distance, sector or "in_box" test that uses `water.csv` puts the palace's channels and reservoir 4.3 km south, in the Rujm el-Mugheifir water cluster. It also double-counts that cluster (ASI 109/5/23 + J15). Anyone who takes ROSAPAT's coordinate for Qasr Hisham lands 1 km off, on the wrong side of the Nuʿeima fields.
How to confirm or kill it (with data in hand, or what is missing): Open ROSAPAT p. 126 and compare its coordinate with any modern image of Hisham's Palace. Check whether any downstream table (`merged_units.csv` line 1011, `merged_scores.csv`) used J15's coordinate. Kill condition: ROSAPAT's no. 50 point is meant as a site-extent centroid (65 dunams is about 250 m across, which still cannot reach 1 km), or J15 was deliberately meant to cover the southern Mafjar.
Confidence: high
Touches the Copper Scroll? maybe. The entry-29 regional pool inventory (J15) carries a wrong location; no reading changes.

---

FIND CARD
Title (one line): ROSAPAT 07 gives Tell Abu Hindi (no. 10, PADIS 0023) the St Andrew's Church coordinate (no. 12, PADIS 0046); Meinardus 1966 p. 181 gives the geometry that separates them by about 1.4 km, and so places the project's "unplaced" J19.
Lane: C1b
What is odd (2–4 sentences): ROSAPAT nos. 10 (Tell Abu Hindi/Tell Mitri, 30–40 dunams) and 12 (St Andrew's Church, 0.75 dunams) have the identical coordinate, 31°51'12.61" N, 35°27'1.41" E (PG 192.733/140.098). Meinardus's opening paragraph sets the relations. St Andrew's lies on the northern bank of the Wadi Kelt, about 1 km south of the Church of Anthimos, which is "south of Tell Abu Hindi" (p. 184). ROSAPAT's own Anthimos point (no. 11, 31°51'46.74" N 35°26'46.76" E) lies 270 m SSE of the Mandate-map Tell Abu Hindi (T26) and 1,120 m SSE (az 160°) of the no. 12 point. So the chain Tell Abu Hindi, then Anthimos, then St Andrew holds for nos. 11 and 12, and no. 10 is a copied coordinate: the real tell is about 1.39 km NNW (WBADB S2425 and Mandate T26, about PG 192.2/141.37).
Evidence (exact sources: file path / page / figure / frame / coordinates):
- ROSAPAT bucket PDF (as above), printed pp. 106–107, entries 10, 11 and 12.
- Meinardus, BSAC XVIII p. 181 (location paragraph and route: turn west after the Wadi Kelt bridge, then south along the western edge of town). Also p. 182 (Coptic buildings erected 1937–39) and p. 185 (150 m from the Roman road south of the wadi). Drive `08 Working files/Unsorted source scans/2026-10-25 13-43.pdf` (ID `1ZkTJ3CH9cQQJes09KRuq3Ht1s3jetwjt`).
- WBADB: `branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv` WBS:2425 "Tell Abu Hindi, Church of Antymos" 192200/141350, and WBS:2522 "Andrea Church, Deir el-Kuft" 192700/139900 (200 m S of ROSAPAT no. 12, on a 100 m-rounded grid).
- Project: `water.csv` line 2020 `LIT-E29-J19` coord_source "unplaced". `entry29_jericho_pools/README.md` lines 246–255 cite only Meinardus pp. 183–184; A5's card read pp. 183–184 but not the location paragraph on p. 181.
- 1945 mosaic: the north bank west of the Wadi Kelt bridge (key 11) shows a small building cluster at about PG 192.58/140.03 (private panel `f_andrew_pair.jpg`). That fits 1937–39 buildings but is not confirmed.
Literature check (queries run, result, tag): repo and branch grep for the shared coordinate (`51'12`, `31.8535`, `35.4504`): only unrelated hits (OSM vertices, an ASI aqueduct). The project has never placed J19. Web: PADIS site list, no coordinates or erratum shown. The relations are published (Meinardus 1966); the duplication is not reported anywhere I found. Tag: **NEW TO THE LITERATURE** (no. 10 duplicate). **NEW TO THE PROJECT** (a coordinate and the p. 181 location for J19).
Why it might matter: J19 (St Andrew's piscine with jars) is one of the entry-29 gates and has no position in the project. ROSAPAT no. 12 agrees with Meinardus's relations within about 100–200 m (1.12 km from Anthimos, about 1.0 km W of the Russian Compound, key 6 of the 1945 sheet). It can serve as J19's working point with about 200 m precision. Meinardus's "2 km SW of Tell Hassan" does not fit well (about 1.1 km), so use the Anthimos and bridge relations. ROSAPAT's Tell Abu Hindi (no. 10) must not be used.
How to confirm or kill it (with data in hand, or what is missing): Read ROSAPAT Pl. I and III (site map) for nos. 10–12. Look for the Coptic compound of 1937–39 (main building 15.9 × 9.4 m with two smaller buildings) in the 1945 mosaic and in modern imagery near PG 192.6–192.75/140.03–140.10, north of the Qelt. Kill condition: ROSAPAT's map plots no. 10 at the same spot, which would mean "Tell Mitri" is a second mound at St Andrew's and not a copy error.
Confidence: medium (the duplicate is certain; which point is "Tell Abu Hindi" depends on the name, but WBADB, the Mandate map and Meinardus agree).
Touches the Copper Scroll? maybe. It gives entry 29's J19 a location; no reading changes.

---

## Other records (not finds)

- `rosapat_vs_mandate_coords.csv`: 15 ROSAPAT 07 sites against the project's georeferenced Mandate 1:20,000 features. The two errors above stand out. Kh. Qaqun / Kh. Kakūn differ by 735 m and Birket Musa by 295 m; I did not resolve either.
- The 1945 mosaic has a sharp-edged light lens about 68 × 47 m, 85 m from WBADB WBS:2608 ("Rom. Site", Sion 1997a, a 100 m-rounded point). It is now under ʿAqabat Jabr camp. It sits on a drawn contour spur and may just be bare marl. Pixel window: mosaic full-res x 1376–1776, y 5615–6015 (private crop `m45_oval_1576_5815.png`). Not checked against Sion 1997a.
- The 1945 sheet's key (full-res crop at 5650, 7380) lists 13 buildings, among them 2 Coptic Church, 6 Russian Compound, 11 Wadi Kelt Bridge and 12 Police Station. The 1:10,000 sheet gives a 1945 position for each.

## Dead ends

- 1945 vs modern over the whole mosaic (E 190.7–195.5, N 138–143): everything is now town, camp or levelled fields, so nothing ancient can be shown to be "lost". The halftone screen makes the 1945 sheet effectively coarser than its 0.84 m pixel.
- Telling aqueducts from drawn contours on the 1945 sheet: the white 25 m contours run along the same slopes as the channels; I found no line I could separate as a channel.
- HEXAGON 1974 F014 via E's `fwd_mosaic_px_to_utm` (stage1_geoloc.json): it misplaces features by several hundred metres north of the JERICHO_OUT zone. A crop meant for Hisham's Palace showed Wadi en-Nuʿeima fields. Re-register locally before any HEXAGON epoch use here. At ʿAqabat Jabr, 1974 shows the dense, largely roofless camp, which covers every 1945 surface.
- HEXAGON 1978, CORONA, Bavarian 1918 and the Jordan valley beyond the mosaic: not reached within budget.
- Esri z19 tiles: "Map data not yet available" here; z18 is the maximum.

## Blocked inputs

- None hard-blocked. Individual PADIS site pages (sites.google.com/uniroma1.it/sapienza-padis-project/archaeological-sites/…) were not opened, because their URLs would have been guessed.

## Seed / reproducibility

- `python3 cmp_1945_esri.py E_km N_km size_km res_m out [zoom]` (needs hexview and `m45_georef.json` beside it). Windows used: 191.55/193.15/194.75 × 138.85/140.5/142.15 (1.7 km, 2.1 m); 192.62/140.12 (0.6 km, 0.75 m); 191.65/138.72; 191.15/139.7.
- ROSAPAT coordinates: `pdf-text` page indices 112–162 of the ROSAPAT document; I parsed the "Site location: Lat./Long." lines.
