# Side-quest C1b, round 2: Jericho plain, escarpment and lower Wadi Qelt (6 Nov 2026)

Lane C1b (change across image epochs). Round 2 rules (ROUND2.md): the former held areas H1/H2 (Wadi Qelt gorge, Jericho escarpment, Abu Saraj) are open. The lower Wadi Ekteif / Nebi Musa area was left to the orchestrator.

What I did:
- Re-parsed the ROSAPAT 07 catalogue (bucket PDF `Nigro-Sala-Taha-eds-2011-…-9af25da3`, page indices 112–162). Round 1 had 57 entries with coordinates; this pass has 68.
- Joined all 68 entries to four witnesses: WBADB (`branch_only/sandbox__methods/.../wbadb_sites.csv`); the IAA ASI online records for maps 109/4 Wadi Qelt and 109/5 Kalia (D2's cache `scratch/D2/asi/GetPolygonsSites_Eng__MapId-68/78.json`, parsed by `asi_parse.py`); the project's Mandate 1:20,000 features; and C2's SWP sheet XVIII picks. I added Hirschfeld 1990's printed grids where they exist.
- Checked the mismatches on the 1945 1:10,000 mosaic (round-1 georeference) and on Esri World Imagery z18 (`mark.py`). The panels are private.
- Read the SWP Memoirs III passages that the 25 Oct rule had held and never coded (pp. 190, 201–205).

---

FIND CARD
Title (one line): ROSAPAT 07's "Site location" coordinates are copied WBADB 100 m grid nodes (14 of 68 within 1.5 m; about 0.001 expected by chance). Where the copied node belongs to another site, the monument is misplaced: Qasr Hisham, and also Beit Jabr et-Tahtani, Kh. Qaqun and the Monastery of the Towers.
Lane: C1b
Round-1 link: C1b-1 (Hisham's Palace, ROSAPAT 1.05 km off) and C1b-2 (Tell Abu Hindi = St Andrew). This card gives the mechanism and three new cases.
What is odd (2–4 sentences): ROSAPAT prints its latitudes and longitudes to 0.01″, which implies a precision of about 0.3 m. Converted to the Palestine grid (EPSG:28191), 14 of the 68 points fall within 1.5 m of a WBADB (Greenberg & Keinan 2009) site point, and most of these sit on exact 100 m nodes. ROSAPAT cites Greenberg & Keinan for only about 10 entries, and only some of those are among the 14. Qasr Hisham (no. 50) is the node of Bar-Adon 1972 site 59c, "Ard el-Mafjir", a sherd-and-flint scatter (WBS:2274). This explains round 1's 1.05 km error. Three more names were put on nodes of unnamed Sion 1997a "Site." rows, and in each case two independent witnesses agree with each other within 70–150 m while ROSAPAT lies 360–735 m away:
- no. 36 Beit Jabr et-Tahtani on WBS:2548 ("Rom, Site."): 507 m from ASI 109/5/5 Manzel Jabr el-Tahtani and 363 m from the SWP position. HA 69 (Porat 1979) puts the Wadi Qelt water mill "about 20 m east of Beit Jabr et-Tahtani" at 1907/1396. That is the ASI point, and ROSAPAT's own no. 32 sits on it.
- no. 69 Kh. Qaqun on WBS:2620 ("Byz, Site."), although ROSAPAT gives the site as Roman: 735 m from Mandate 19-13 "Kh. Kakūn" and 685 m from SWP "Khurbet Kakun".
- no. 25 Monastery of the Towers on WBS:2797 ("Byz, Site."): 361 m from ASI 109/5/71 and 400 m from Hirschfeld 1990's Pyrgoi grid (198.2/137.0). Esri z18 shows an excavated multi-room ruin at the ASI point and bare marl at ROSAPAT's point. ROSAPAT's no. 27, an "unidentified monastery", lies 133 m from the ASI ruin, so the catalogue probably lists the Towers twice.
Other node copies are correct sites, rounded: Deir Hajla 1–8 m, St George 108 m, ʿEin Hajla, Nuseib ʿUweishira, ʿEin en-Nuʿeima.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- ROSAPAT `pdf-text` page indices 131–132 (nos. 35, 36, 38), 148 (no. 69) and 116–117 (no. 25). The "Greenberg - Keinan 2009 … site n." citations are on the pages for nos. 7, 13, 30, 53, 59, 67, 78, 82 and 83.
- `out2/C1b/rosapat_vs_wbadb_nodes.csv`: all 68 entries with Palestine-grid coordinates, the nearest WBADB row, its source and periods, the distance, and an exact-copy flag.
- `out2/C1b/rosapat_witness_table.csv`: the per-witness distances for 14 named sites.
- Repo: `research/regional/mandate_maps/features.csv` P04; `research/regional/haesi_features/phase3_2026-10-11/part_a/data/coding_HA61-72.json` line 1266 (HA 69 water mill); `research/sources/books_usc_2026-10-30/hirschfeld1990_list_screen_2026-10-30.md` (Pyrgoi, Calamon).
- SWP picks: `private/C2/C2_swp18_feature_positions_PRIVATE.csv` (these are published SWP labels).
- Private panels: `private2/C1b/esri_towers_rosapat25_vs_asi71.jpg` and `m45_esri_beitjabr_kakun.jpg`.
Literature check (queries run, result, tag): Web: "ROSAPAT 07 Archaeological Heritage in the Jericho Oasis site coordinates errors review" found the catalogue pages, Sapienza IRIS records and the PADIS site list, with no erratum and no review that notes the coordinates. Repo main and branch_only: no file uses ROSAPAT coordinates, and round 1's grep for the shared strings found nothing. No project note links ROSAPAT to WBADB. Tag: **NEW TO THE LITERATURE** (that ROSAPAT copies WBADB nodes, and the three new mislocations). The witnesses themselves are published.
Why it might matter: ROSAPAT is the Palestinian–Italian protection catalogue of the Jericho oasis, and PADIS reuses its codes. Its false precision hides two separate errors: 100 m rounding, and in at least four cases a different site's node. Anyone who uses ROSAPAT points for protection zones, distance tests or GIS joins will put Qasr Hisham, Beit Jabr et-Tahtani, Kh. Qaqun and Pyrgoi 0.36–1.05 km from where they are. Most of ROSAPAT's other 54 coordinates are not node copies, and the round-1 Mandate check found most of them within 250 m.
How to confirm or kill it (with data in hand, or what is missing): Recompute with pyproj EPSG:28191 from ROSAPAT's printed values. The node coincidences are arithmetic and cannot be chance. Kill test for the three new cases: ROSAPAT's own site map (Pl. I) plotting them at the copied nodes would show the catalogue meant those points; but Pl. I is not in the store copy (Blocked). Augustinović's 1951 plan (ROSAPAT Pl. III, page index 239) is schematic. Its order still fits the witnesses: "Beit Gaber Tahtani" sits at the Wadi Qelt mouth west of Birket Musa, and "Kh. Qaqun" sits by the Jerusalem road west-south-west of Birket Musa. A PADIS GIS layer, if one is ever released, would settle the question.
Confidence: high (the copying and the three misplacements); medium (that no. 27 duplicates the Towers).
Touches the Copper Scroll? maybe. Entry 29's Jericho pool inventory (J15, J19) and any future ROSAPAT-based gazetteer would inherit these points. No reading changes.

---

FIND CARD
Title (one line): SWP's two-tier, 21-loculus kokhim tomb "near" ʿAin ed Duk (Memoirs III p. 190) has no counterpart in any later record that the project holds. Among about 140 recorded caves and tombs within 1.5 km of the spring, the only kokhim cave is ʿAtiqot 41 V/57, 1.4 km SSE, a different and smaller installation.
Lane: C1b
Round-1 link: new. It opens a passage the 25 Oct rule held: `phase4_2026-10-11/part_h_surveys/held.csv`, unit SWP3-190-ain-ed-duk, "read in error (deviation D1)", never coded.
What is odd (2–4 sentences): Conder and Kitchener (examined 1873) describe a hillside tomb near ʿAin ed Duk with the following features:
- a chamber 16 × 17 ft with 21 kokhim in two tiers (lower tier 3 + 4 + 4, upper tier 3 on the left);
- kokhim 2 ft × 6 ft 8 in × 3 ft 4 in;
- "other caves near it, and broken sarcophagi", and two shafts.
A two-tier kokhim plan is uncommon. None of the project's records carries this tomb: the 665-row cave inventory, the 1,159-row tomb inventory, WBADB and the 4,038-row HA/ESI/SWP feature table. ʿAtiqot 41 Regions III–VI (1993 survey) recorded about 140 caves, niches and shelters within 1.5 km, all natural cliff cavities, and only V/57 is "of the kokhim type". V/57 has one opening, three niches outside, no plan and no finds, and lies 1,405 m from the spring. A later epoch adds one clue: the 1940s Mandate sheet 19-14 prints an unlabelled cave symbol (item N15) about 500 m east of the spring, off the cliffs. The project's 2025 imagery check of N15 shows a field edge beside a building and no opening.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- SWP Memoirs III p. 190, archive.org `surveyofwesternp03conduoft` (workspace OCR `scratch/C2/dl/memoirs3.txt` lines 9957–9964).
- `research/regional/caves_entry25/caves.csv` (A41:V/57, A41:IV/1–30, A41:V/1–58) and `research/regional/tombs/tombs.csv` (T0616 = V/57).
- WBADB rows WBS:1965–2222 within 1,500 m of Mandate N02 (ʿEin ed Duyūk, PG 190041/144675). Join output in this card's workings; recompute with the WBADB file.
- `research/regional/mandate_maps/features.csv` N15. A candidate note is in `private2/C1b/ain_duk_tomb_candidate_PRIVATE.md`.
Literature check (queries run, result, tag): Web: "\"Ain Duk\" OR \"Ein Duk\" OR \"Na'aran\" kokhim tomb loculi two tiers burial cave" found only general kokhim pages. Bucket `pdf-search` for "21 kokim", "kokim in two tiers", "Duk" + tomb/kokh/loculi, and "Na'aran" + tomb/cemetery: no hits. The repo greps for these strings hit only the held lists. The HA metadata (vols. 116–137) has no ʿAin Duk/Naʿaran tomb report; the one "Naʿaran" (HA 137, 26678) is the Golan village. The ʿAtiqot 41 Hebrew text was not searched in full, because it has no text layer in the store. Tag: **NEW TO THE PROJECT** (published in 1883, with no later record found). It may be **KNOWN BUT UNDER-DISCUSSED** if ʿAtiqot 41's introduction to Regions IV–VI cites it.
Why it might matter: A large kokhim tomb with sarcophagi is a Second Temple–Roman family tomb. It would be the only built burial of that type recorded at the spring of Duk/Naʿaran, next to Naʿaran and below the Doq fortress. That area is now farmed and built over, so the tomb may be lost or unrecorded.
ARGUMENT (scroll): entry 31 (VII 11–13) is "in Doq, under the eastern corner of the [guard-post / drying-place]". The project's place point is the Jebel Quruntul summit (`tables/phase3_places.csv` "doq"; GLO-30 93 m, which fits SWP's 320 ft). The tomb shows Second Temple-period installations at the Duk spring as well as on the summit, which slightly widens the area a Doq search must cover. It does not favour any reading of the entry's object, and it is not a candidate for it: the entry names a corner of a building, not a tomb.
How to confirm or kill it (with data in hand, or what is missing): Read Sion's ʿAtiqot 41 Regions IV–VI introduction (pp. 43–46, Hebrew) and Aronshtam's V/57 entry (p. 94) for an SWP citation or a 21-loculus plan. If V/57 has 21 kokhim in two tiers, the card reduces to a 1.4 km SWP position error. Look for a rock-cut opening at Mandate N15 in the 1974/1978 HEXAGON frames, which were not reached here; it needs a local re-registration. Kill condition: any later report that describes the tomb.
Confidence: medium (absence from the project's records: high; absence from the literature: medium).
Touches the Copper Scroll? maybe. It concerns the area around entry 31's Doq; see ARGUMENT.

---

## Other records (not finds)

- ROSAPAT no. 28 (Calamon) and no. 26 (Penthucla) lie 426–818 m and about 1.3 km from the ASI and Hirschfeld points. These are identification disputes (Calamon at Deir Hajla or ʿEin Hajla), not copy errors, so I did not make cards of them.
- ROSAPAT no. 38 Birket Musa (round 1: 295 m) is not a node copy. It lies 223 m from ASI 109/5/16 and 295 m from the Mandate point, which agree within 77 m. The error is moderate and not explained.
- The project's Doq point (`phase3_places.csv`) equals ROSAPAT no. 75 / WBE:316 "Tahunat el-Hawa" to within 4 m. GLO-30 gives 93 m, which fits SWP's summit "320 [ft] above sea". No error.
- SWP III pp. 201–205, Jebel Kuruntul chapels and caves (held until now): read in full. The chapels are dated by their frescoes and inscriptions to the 12th–13th c., with Sabas, the Deesis, Gregory, Basil, Chrysostom and Athanasius. "Two large reservoirs" lie at the cave below the lower chapel. All of this is known in the Quruntul literature, so it is not a card.

## Dead ends

- Commons/NINO Scholten "Ain Duke" series (31 photos, 1921–23): the API still returns HTTP 429, so only the three store copies were viewed. Store photo `b911e983` shows a canal through banana groves above the plain. `967bdfe8` shows a conical peak, probably Jebel Quruntul, over a stony plain crossed by a stone line. Neither could be placed to better than about 1 km without the series captions, so I made no epoch comparison.
- ASI 109/5 vs WBADB "Sion 1997a" (146 rows): the median offset is 212 m, and the two are different site lists (the WBADB list is denser). They cannot be joined 1:1, so they cannot help pick between rival coordinates.
- ROSAPAT Pl. III (Augustinović 1951): schematic, with no scale fit possible at the 300–700 m level. It is useful only for site order.
- Beit Jabr et-Tahtani on the 1945 mosaic: the SWP/ASI point is at the mosaic's west edge and under a modern cluster. ROSAPAT's point is a large modern building on the plain. Neither image shows the tower itself.
- HA 137 report 26678 "Naʿaran, Syrian Village": Golan, not relevant.

## Blocked inputs

- Wikimedia Commons API `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=Scholten "Ain Duke"…`: HTTP 429 (empty body).
- ROSAPAT 07 Pl. I (the catalogue's own site map): not found in the store copy. Page indices 239–242 are Pl. III–VI, `pdf-search "Pl. I -"` returns nothing, and it is probably a loose fold-out. Pl. II was not found either.
- ʿAtiqot 41 Regions IV–VI and V (Hebrew): no text layer searchable in the store, so the SWP tomb citation check is not done.

## Reproducibility

- `asi_parse.py` (ASI JSON to CSV); `mark.py` (1945 mosaic + Esri panels with markers; needs round-1 `cmp_1945_esri.py` saved as `cmp.py` and `m45_georef.json`).
- Node test: pyproj `Transformer.from_crs(4326, 28191, always_xy=True)` on ROSAPAT's degrees–minutes–seconds values; the nearest WBADB row is taken on `oig_x`/`oig_y`. The chance rate uses the 455 WBADB rows in E 189–202 / N 133–145 and a 1.5 m radius.
