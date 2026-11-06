# Side-quest B2b: surveys against each other, the joins B2 skipped (6 Nov 2026)

Lane B2b (follow-up to B2). Two joins, chosen because both have exact keys:

1. **JSP 10 (Yezerski ed. 2009, *Excavations and Discoveries in Benjamin and Judea*) × WBADB**, keyed on the Staff Officer for Archaeology licence number, then on the grid. JSP 10 prints an L-licence and a double map reference (ITM + IOG) for almost every report. WBADB's Excavations and Surveyed sheets carry the same licences (`L-NNN/YYYY`). Source: Drive 02 `JSP 10 – …` (172 phone photos; index `00 README – JSP 10 index.md`, manifest `00 manifest – JSP 10 2026-10-29.csv`). I read the printed references on the English abstract photos IMG_1309, 1308, 1306, 1302, 1296 and 1295 and on Hebrew p. 3 (IMG_1146). For the other reports I took the references from the README summary; these are marked `README` in the CSV.
2. **ʿAtiqot 41 (2002) × WBADB × `caves_entry25/caves.csv`**, keyed on the ʿAtiqot cave number (Region/No.). WBADB rows cite it as e.g. "Weiss 2002: IX/8". `caves.csv` holds the printed ʿAtiqot grid. `caves_entry25/AMENDMENT_1.md` §15 treats these WBADB rows as "crosswalks only", so their grids had never been compared.

Data in this folder:
- `join_jsp10_x_wbadb.csv`: the 36 JSP 10 contents entries, one row each (the 6 ed-Dhahiriya points are one row). Columns: licence, printed ITM/IOG, where it was read, ITM-vs-IOG gap, WBADB rows with the licence and their distance from the printed point, nearest WBADB row, status, note. Positions of the 5 rows with no WBADB record are blanked (`PRIVATE`).
- `join_atiqot41_x_wbadb.csv`: 421 pairs of a WBADB row and an ʿAtiqot 41 number. There are no coordinates in the public file, only distance and status.
- Private (`private/B2b/`): full versions of both CSVs with coordinates, `scripts/` (`jsp10_join.py`, `a41_join.py`, `dec.py`), and `page_crops/` (11 crops of printed map references from the JSP 10 photos; library copy, keep private).

Join results:
- **JSP 10:** 31 of 36 entries have a printed grid. 25 of those agree with WBADB to within 450 m. 6 are flagged (cards 1 and 2). 5 have a licence or a site missing from WBADB.
- **ʿAtiqot 41:** 300 WBADB rows match a `caves.csv` cave. 291 agree to within 100 m and 5 more within 300 m (ranges/rounding). 2 are ʿAtiqot misprints already in AMENDMENT_1 §11 (XII/52, XIII/14). **2 are WBADB grid errors (card 3).** The other 117 WBADB rows are non-cave features (niches, shelters, cisterns) that `caves.csv` does not admit. Of 356 ʿAtiqot caves in `caves.csv`, 52 are cited by no WBADB row.

Known issues checked first: B2-1 (WBADB code-vs-grid) cannot catch any of these, because the rows have no ASI square code. C3-1 (dup_of linker) and D3 (Hadashot map refs) do not involve these sources. `research/sources/books_usc_2026-10-30/jsp10_sweep_2026-10-30.md` (main) read JSP 10 for project relevance only (B5, B6, A9 …). It did not check grids or licences, and it skipped A4.

---

FIND CARD
Title (one line): JSP 10 prints, for Peleg's 2002 dwelling cave at Kh. Abu-Mussarah (licence 959), the map reference of Peleg's 1996 Mishor Adummim cave (licence 749), 6.4 km away
Lane: B2b
What is odd (2–4 sentences): The English abstract of JSP 10 report A4 (p. 5*) gives "map ref. ITM 23100/63210; IOG 13210/18100" for a natural dwelling cave "on the southern edges of Khirbet Abu-Mussarah", found in a survey in October 2002 and dug under licence 959. ESI 112 (2000) p. 73*, "Mishor Adummim (l-749)", also by Yuval Peleg, gives "map ref. 18100/13210" for a natural cave sounded in August 1996 "between Mishor Adummim and Ma'ale Adummim". The two references are identical. They are two different caves:
- Mishor Adummim: one room 3.05 × 4.67 m, south-facing opening, Early Roman and Mamluk.
- Abu-Mussarah: 7.40 × 4.50 m, Iron II–III and late Hellenistic.

Kh. Abu Musarraḥ itself is WBADB WBS:2759 / WBE:393 (Kallai 1972 site 147; Dinur & Feig 1993 site 510). WBADB, correctly, files licence 959 there, 6,382 m NW of JSP 10's point. The JSP 10 point instead falls exactly (0 m) on WBADB WBE:566 "Mishor Adummim" (L-749/1996). So the printed reference was carried over from the author's earlier cave report.

The same join found three more misprinted references in JSP 10, smaller and not linked to this one:
- B10, Beit Sahur burial cave (p. 31*): "ITM 22279/62275; IOG 17282/11228". The IOG northing is 10.5 km south of the ITM point; WBADB WBE:813 follows the ITM point.
- B5, Wadi Ekteif (p. 29*): the IOG northing 13425 is 100 m from ITM 63415.
- A2, Geba (p. 3*): both references are printed northing first, with the leading digit dropped ("ITM 39500/22437; IOG 39500/17437").
Evidence (exact sources: file path / page / figure / frame / coordinates): JSP 10 English p. 5*, Drive photo `2-eng p04-05 Geva Binyamin + Adam + Abu Musarrah cave (IMG_1308).HEIC` (ID 14gQ7C1sKZ1mHF_a4On6K3xVb_yTD7vdO), right page, first paragraph of A4. Crop: `private/B2b/page_crops/c_musar.jpg`. ESI 112: store `HA-ESI-112-2000-Hadashot-Arkheologiyot-Excavations-and-Surve-8a63fc84`, PDF page 239 (printed 73*), and the licence index on PDF page 314 ("Mishor Adummim (l-749) Yuval Peleg 73*"). WBADB WBS:2759, WBE:393, WBE:566 (`branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv`). Beit Sahur: IMG_1295 (p. 31*), crop `c_sahur.jpg`. Ekteif: IMG_1296 (p. 29*), `c_ekteif.jpg`. Geba: IMG_1309 (p. 3*), `c_geba.jpg`. Row-level detail in `join_jsp10_x_wbadb.csv` (A4, B10, B5, A2).
Literature check (queries run, result, tag): Web: "Abu Musarrah / Abu-Mussarah dwelling cave Peleg Iron Age Hellenistic map reference" gave no hit on the report or on any correction. "West Bank Archaeological Database … errors" gave only the TAU project page and the sourcebook (https://www.tau.ac.il/humanities/abraham/archaeological-database.html). Repo main and branch_only: "23100/63210" 0 hits; "13210/18100" 0 hits. "18100/13210" appears only as the ESI 112 Mishor Adummim row (`haesi_features/phase3_2026-10-11/part_c/*`). The JSP 10 sweep note lists A4 only as "outside the period window". Tag: **NEW TO THE LITERATURE**.
Why it might matter: anyone who places the Abu-Mussarah cave from JSP 10 puts an Iron II–Hellenistic dwelling cave in the Mishor Adummim wadi, on top of a different, Early Roman cave. A count of caves with Hellenistic occupation near Maʿale Adummim would gain a false point, and the 1996 cave would look as if it had been re-excavated in 2002. The other three misprints are cheap corrections for anyone who digitises JSP 10.
How to confirm or kill it (with data in hand, or what is missing): Read the Hebrew p. 40 (IMG_1165, ID 16UlIZ94ZIUkVxDk1WB7tUZ9YRdw91mNj; not opened in this pass). If the Hebrew gives a different grid near E 177/N 137, the error is in the English abstract only. If it gives 18100/13210, the error is in the report. The card dies only if the 2002 cave can be shown to be the 1996 cave, and the published sizes and periods argue against that. The Hadashot online record for licence 959, if one exists, would settle it.
Confidence: high (the identical references and the different caves); medium (that the English carries the error, until Hebrew p. 40 is read)
Touches the Copper Scroll? no (Iron/Hellenistic cave near Anathoth; no entry argued)

---

FIND CARD
Title (one line): WBADB files five JSP 10 salvage digs under the wrong place or the wrong name (three homonyms 4.6–6.8 km away, Geba as "Gibeah", Hyrcania Valley as "En-Nabi Musa"), and licences 733 and 773 are crossed between Baal Hazor and Mattityahu
Lane: B2b
What is odd (2–4 sentences): On the licence key, WBADB attaches three JSP 10 digs at modern places to the ancient site with the same name:
- (a) **Beitar ʿIlit (West)**, A7. Licence 892, ITM 20972/62250 (p. 8*), dug April 2002. In WBADB, L-892/2000 appears only on Kh. el-Yahud / Battir (WBS:4010, WBE:775), 4,970 m NE, and no WBADB row lies at the dig. Beitar ʿIlit and Battir (Beitar) are different places with the same name.
- (b) **Carmel**, A14. Licence 936, "ITM 52974/21743" (northing first, p. 17*), Jan 2002, "to the south of the settlement". WBE:939 is at the dig (108 m), but survey row WBS:5874 for ancient Kh. el-Karmil (Kochavi 223 / Ofer T14), 4,590 m W, also carries L-934 and L-936/2001.
- (c) **Byzantine burial cave "near Khirbet Beit Sahur"**, B10. Licence 951, July 2002. WBE:813 "Cave" is right (58 m), but L-951/2002 is also on WBS:3714 "Kh. Beit Saḥur", Kloner 2000 [106] 53, 6,808 m N. That is a different ruin with the same name, near es-Sawahira.

Two digs carry another site's name:
- WBE:362 "Gibeah of Benjamin" holds the licence (1038) and grid (70 m) of JSP 10's *Geba* of Benjamin (Geva Binyamin, by Jabaʿ). Gibeah (Tell el-Ful) is a different biblical site.
- WBE:722 "En-Nabi Musa" holds the licence (996) and grid (92 m) of the "Four tombs in the Hyrcania Valley", which JSP 10 puts c. 1 km N of Kh. Karm Abu Ṭabaq.

Licence numbers 733 and 773 are crossed:
- JSP 10's English p. 3* gives Baal Hazor "License No. 773". The Hebrew p. 3 dates the dig to November–December 1995.
- ESI 112's licence index (PDF p. 315) gives "l-773" to Mattityahu (North) and "L-773-1" to Mattityahu (Northeast). The NE report is dated January 1997.
- WBADB gives Baal Hazor L-733/1995 (WBE:223, at JSP's grid, 0 m), but Mattityahu (North) L-733/1995-0 + L-773/1997-0 (WBE:239) and Mattityahu (NE) L-733/1995-1 (WBE:235).
- The licence sequence (L-749 = Aug 1996; L-762, L-773 = 1997) puts 773 in 1997. So JSP 10's English "773" is probably a misprint for 733, and WBADB's "733" on the two Mattityahu rows is probably wrong.
Evidence (exact sources: file path / page / figure / frame / coordinates): `join_jsp10_x_wbadb.csv` rows A7, A14, B10, A2, B6, A1 (licence rows and distances). JSP 10 English pp. 3*, 8*, 17*, 29*, 31* = IMG_1309, IMG_1306, IMG_1302, IMG_1296, IMG_1295. Hebrew p. 3 = IMG_1146 (ID 1AhTAjM0k2Nq1sTjc_jWPVzfm-l8CME-9), first paragraph ("נובמבר־דצמבר 1995"). ESI 112 store doc above, PDF pp. 254–255 (Mattityahu reports) and 315 (licence index). WBADB rows WBS:4010, WBE:775, WBS:5874, WBE:939, WBS:3714, WBE:813, WBE:362, WBE:722, WBE:223, WBE:235, WBE:239.
Literature check (queries run, result, tag): Web: the WBADB-errors query above found no errata. Repo main/branch_only: "L-892" appears only in the WBADB tables; "Ba.al Hazor" 0 hits on main; "En-Nabi Musa" only as data rows. The JSP 10 sweep note places B6 by grid without noting the WBADB name. Tag: **NEW TO THE LITERATURE** (record-level; no errata found).
Why it might matter: WBADB is the only joined index of West Bank fieldwork. A licence lookup there, or an IAA/SOA archive request built from it, returns the wrong site for these five digs. Survey sites at Battir, Kh. el-Karmil and Kloner's Kh. Beit Saḥur look excavated when they were not. The Beitar ʿIlit farm unit has no WBADB point at all. The homonym pattern (modern settlement named after an ancient site) is a cheap test across the whole database. A first pass (`scripts/jsp10_join.py` logic, over all 1,020 L-licences) finds 44 licences on rows more than 2 km apart. Most of those are expected: multi-site licences of 1968–73 and the 1993 cave-survey licences. The rest are unreviewed.
How to confirm or kill it (with data in hand, or what is missing): (a)–(c) are confirmed on the printed pages against WBADB's own rows; the WBADB source sheet for those rows would show whether the licence came from a report or from a name match. For 733/773: JSP 10 Hebrew p. 3 footnote 1 (bottom of IMG_1146, not in the frame) should state the licence. If it says 733, the English 773 is a misprint; if it says 773, then the SOA issued 773 twice, or ESI 112 is wrong. Missing from WBADB entirely: A10 Kh. el-Ḥanzir hiding complex (no row within 860 m), A11 (licence 5006) and B19 (licence 5010). Their positions are in `private/B2b/join_jsp10_x_wbadb_full.csv`.
Confidence: high (a, b, c, the two names); medium (733/773 direction)
Touches the Copper Scroll? no (B6 lies in the Buqeiʿa near Hyrcania, but only its name is at issue)

---

FIND CARD
Title (one line): WBADB misplaces ʿAtiqot 41 caves IX/8 (a sealed rock-cut burial cave) by 6.3 km and X/14 by 5.4 km through digit transpositions in the northing, and the wrong points have spread into sandbox layers
Lane: B2b
What is odd (2–4 sentences): On the cave-number key, 291 of 300 WBADB↔ʿAtiqot pairs agree to within 100 m, but two do not:
- **IX/8:** Weiss's Region IX Table 1 prints 19114/14071. WBADB WBS:1910 "Cave IX/8" gives 191140/**147010** (07→70).
- **X/14:** the Region X table prints 19386/13064. WBADB WBS:2931 "X/14" gives 193860/**136040** (06→60).
The ʿAtiqot values sit among their region neighbours (IX/7 19116/14079; X/16 19381/13066), so WBADB is wrong in both cases. Unlike the two ʿAtiqot misprints already listed in AMENDMENT_1 §11 (XII/52, XIII/14), where WBADB has the corrected value, these two have not been noted anywhere. ʿAtiqot describes IX/8 as a rock-cut burial cave (about 2 m long) that was deliberately blocked. WBADB therefore puts a tomb 6.3 km north of the Region IX cliff.
Evidence (exact sources: file path / page / figure / frame / coordinates): ʿAtiqot 41 bucket PDFs `atiqot/pdf/vol-041/iss-1/2558_region-ix-…pdf` (pdftotext line 69: "19114/14071 … 8/IX") and `2561_region-x-…pdf` (line 109: "19386/13064 … 14/X"). `caves.csv` rows A41:IX/8, A41:X/14 (coord_ok = yes). WBADB WBS:1910, WBS:2931. `join_atiqot41_x_wbadb.csv` (status `wbadb_grid_wrong`). Downstream copies of the wrong points:
- `branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/features_unified_v2.csv` (WBS:1910 as tomb/cave/rockcut at 31.9159 N; WBS:2931 as cave);
- `sandbox/landscape_map_1km_2026-10-31/out/loso_scores.csv` (WBS:1910);
- C2's `out/C2/swp18_features_vs_records.csv`, where Mekur es-Sidri lists "1174m WBADB:WBS:2931" as its third-nearest record. That distance is false, but C2's verdict rests on nearer records and does not change.
B2's ASI 1 join is not affected (checked: neither row is a "best later record").
Literature check (queries run, result, tag): Repo/branch_only: "WBS:1910", "WBS:2931" appear only in the data rows above; "Cave IX/8" appears only in `caves_entry25/intake/wbadb_crosswalk.csv` with no note. AMENDMENT_1 §11 lists other misprints, not these. Web: the WBADB errata query above found none. Tag: **NEW TO THE LITERATURE**.
Why it might matter: The project's cave inventory for entry 25 takes ʿAtiqot grids directly and is unaffected. The sandbox West Bank inventory, the 1 km landscape map and any WBADB-based cave or tomb density are not. They gain a false tomb point north of Region IX and a false cave point north of Region X (both in the Jordan Valley zone Z2), and they lose those features at their true positions. The cave-number join is cheap and exact, and it is the only test that catches transpositions in WBADB rows that have no ASI code.
How to confirm or kill it (with data in hand, or what is missing): Done with data in hand: the printed ʿAtiqot tables, their neighbouring caves, and WBADB. To kill it you would have to show that WBADB took these two rows from a later corrected source. No such source is cited (survey_ref is ʿAtiqot 2002 alone).
Confidence: high
Touches the Copper Scroll? maybe: Region X is the fault escarpment north of Qumran; entry 25's denominator uses ʿAtiqot directly and is unaffected; WBADB-based layers are not.

---

## Dead ends

- Frumkin 2015 (Judean Desert Caves Atlas): Drive holds only the introductory chapters, 11 Malham web-article texts without maps, and the Twin Complex entry (pp. 212–215). There is no site list, so no join is possible.
- SBF 36, JSP 8, JSP 9, SWP Memoirs II–III: not joined. JSP 8/9 are single-site or Samaria volumes outside B2's box. SBF 36 is a synthesis with no site grid list. The SWP Memoirs have no grids (Palmer squares only, too coarse, as C2 found).
- JSP 10 × WBADB, other 25 gridded entries: agree to within 450 m (A6 430 m, A15 420 m, B4 447 m: rounding of WBADB points). A13 ed-Dhahiriya: all six points within 300 m of WBE:942–956.
- JSP 10 printed-order quirks (northing first for Adam, Murran, Ayazira and Carmel; "IOG 13210/18100" for A4): a layout convention already noted in the JSP 10 README. They are not errors in themselves.
- Global WBADB test (one L-licence on rows more than 2 km apart): 44 cases. Most are the multi-site licences of 1968–73 (L-1 … L-91) and the 1993 cave-survey licences (L-588, L-606). Not reviewed one by one, so not used as evidence.
- Unmatched ʿAtiqot side: 117 WBADB rows cite ʿAtiqot features that `caves.csv` does not admit (niches, shelters, cisterns). This is expected and not a gap. 52 ʿAtiqot caves have no WBADB row; that is a gap in the compilation, not "never revisited", so no card.
- B5 Wadi Ekteif "licence 923 not in WBADB": the row is there (Excavations E508 in the jsp10 sweep's numbering), with licence "NDA".

## Blocked inputs

- JSP 10, SBF 36 and Frumkin 2015 are not in the PDF store (`hexview.py pdfs` lists JSP 8, JSP 9 and SBF 36 only). JSP 10 was read from Drive HEIC photos via `download_file_content` (2–3.5 MB base64 each). Only 7 of 172 photos were opened.
- JSP 10 Hebrew p. 40 (A4) and the footnote of p. 3 (A1 licence): not opened or not in the frame; these are the kill tests for cards 1 and 2.
- Hebrew search of the HA/ESI store for "בעל חצור" / "כוכב השחר": no hits. Either no Hebrew HA report exists or the OCR misses it.

## Seed / reproducibility

Deterministic. `python3 -I private/B2b/scripts/jsp10_join.py OUT_PUBLIC OUT_PRIVATE` (printed references are hard-coded from the page photos and the README, with their source in `ref_source`). `python3 -I private/B2b/scripts/a41_join.py OUT` (WBADB = `branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv`; caves = `research/regional/caves_entry25/caves.csv`). ITM→OIG: EPSG:2039 → EPSG:28191 (pyproj); the naive −50 km/−500 km offset agrees to ≤2 m here. Photo decoding: `dec.py` (pillow_heif).
