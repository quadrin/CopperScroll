# Side-quest D3: Errors in published sources (6 Nov 2026)

Lane D3, worker D3. Route: data, not eyes. I parsed every map reference in the 4,667 Hadashot Arkheologiyot (HA-ESI) reports, vols 116–137, in both the English and Hebrew text layers (`gs://copper-scroll-cog-1030/hadashot/derived/hadtext_pdftotext.tgz`, 9,382 text files). Then I ran three automatic checks:
(a) does the English map reference agree with the Hebrew one for the same report;
(b) when a report prints both an NIG and an OIG reference, is NIG = OIG + 50 km E / +500 km N;
(c) is the reference within a few km of the median of the other HA reports with the same site group (`group_en`).
I read every candidate in context and fetched 31 live English pages (`https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=<ID>`, 6 Nov 2026). For 24 of the 36 table rows the same error is still on the live page. Three more fetched pages are project-noted cases (still wrong online). On two pages (ids 148 and 177) no map reference was found. For Shilat (738) only the first point was compared.

Data: `ha_mapref_errors.csv` (36 verified rows, each with the printed values, the wrong part, the evidence for the correct value, the size of the offset and the live-page status). Scripts: `mapref.py` (extraction), `compare.py` (check a), `pairs.py` (check b), `outliers.py` (check c). All of these are published, excavated or surveyed sites; none is an unrecorded feature.

**Excluded because the project already noted them** (location notes in `research/regional/haesi_features/*/reports.csv` and `coding_online*.json` on main): HAESI-78, 163, 303, 432, 436, 458, 631, 638, 686, 689, 754, 758, 1510, 1619, 1801, 2094, 4358, 5405, 13671, 24845, 25494, 26590. These include the Jerusalem ʿAmr ibn el-ʿAs St, Salah a-Din St, Mount Scopus and Moza misprints, which the same checks also found.

---

FIND CARD
Title (one line): The English HA 129 report "Tiberias" (id 25159) opens with a paragraph copied from a Ramat Bet Shemesh report, so its site, map reference, director and funder are wrong
Lane: D3
What is odd (2–4 sentences): The English version of Dalali-Amos & Hanna, "Tiberias" (HA-ESI 129, 01/02/2017, Final Report) opens: "In August 2015, a trial excavation was conducted west of Tel Yarmut (Permit Nos. A-7403, A-7489; map ref. 19700-05/62430-50) … prior to the construction of Neighborhood D2 in Ramat Bet Shemesh … directed by O. Shalev …". That paragraph matches, word for word, the opening of HA 129 report 25169 "Bet Shemesh, Ramat Bet Shemesh D2" (O. Shalev, 23/01/2017, permit A-7493). Only the permit numbers were changed to Tiberias's. From the next sentence on, the English text is about Tiberias again ("Five excavation squares … c. 70 m west of the Tiberias municipal park"). The Hebrew version has the correct opening: Tiberias, May and August 2015, map ref. 250696-755/743631-93, directed by Dalali-Amos and Hanna, with a different staff list.
Evidence (exact sources: file path / page / figure / frame / coordinates): bucket `hadashot/derived/hadtext_pdftotext.tgz` → `hadtext/en/vol-129/25159_tiberias.txt` lines 9–18 vs `hadtext/en/vol-129/25169_bet-shemesh-ramat-bet-shemesh-d2.txt` lines 9–18 (identical apart from the permit numbers); Hebrew `hadtext/he/vol-129/25159_tiberias.txt` (נ"צ 250696-755/743631-93). PDFs: `hadashot/pdf/en/vol-129/25159_*.pdf` and `pdf/he/vol-129/25159_*.pdf`. Live page https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=25159, fetched 6 Nov 2026, still shows the Tel Yarmut paragraph. The English map reference lies about 131 km from the median of the 48 other HA Tiberias reports (251125/743315).
Literature check (queries run, result, tag): web search "Hadashot Arkheologiyot 129 Tiberias Dalali-Amos Hanna 2017 final report" found no correction or erratum, and the live page is still wrong. Repo: the string "19700-05" does not appear in the haesi_features data on main. **NEW TO THE LITERATURE.**
Why it might matter: Anyone who geocodes HA from the English text puts an Abbasid flood-wall excavation in Tiberias at Tel Yarmut (Shephelah). The English text also credits the wrong director, funder and staff. The error is 9 years old and still live. It is a clean, checkable case for a correction request (to be made by the owner, not by this swarm).
How to confirm or kill it (with data in hand, or what is missing): Open the two English PDFs side by side (2 minutes). It is killed only if the IAA has since published a corrected English version under another id. I found none among the 4,667 records.
Confidence: high
Touches the Copper Scroll? no (Tiberias and the Shephelah are outside every scroll region)

---

FIND CARD
Title (one line): In 10 HA-ESI reports the English map reference contradicts the Hebrew original. In Zikhron Yaʿaqov and Caesarea the English swaps the northings between the NIG and OIG references
Lane: D3
What is odd (2–4 sentences): HA-ESI publishes each report in Hebrew and English, and the two map references should be identical. In 10 reports the English differs. In each case the Hebrew value fits the site, and the English value fits neither the site nor its own OIG or NIG twin. The clearest are HA 119 report 530 (Zikhron Yaʿaqov) and report 521 (Caesarea, High Aqueduct in Nahal ʿAda). In the English of both, the NIG northing is the OIG northing (e.g. "NIG 1958–9/2187–8; OIG 1458–9/7187–8"); the Hebrew has "NIG 1958-9/7187-8; OIG 1458-9/2187-8". In the others the English has a transposed or rotated digit group: Horbat Maʿon 51886 for 58186; Yattir Forest (B) 60853 for 58530; Horbat Bet ʿAnava (W) 614520 for 645202; Nahal Yarmut 17518/64680 for 19680/62518; Ibthan 687066 for 697066; ʿEn Zippori 229510 for 225910; Jerusalem Nahal Qidron, where the OIG easting is 14770 for 17470; Shefarʿam, where the English easting is 21000 for 21600.
Evidence (exact sources: file path / page / figure / frame / coordinates): `ha_mapref_errors.csv` rows with class "B EN/HE twin": report ids 530, 521 (HA 119); 48 (116); 997 (121); 860 (120); 148, 177, 270 (117); 8518 (126); 339 (118). The text files are `hadtext/{en,he}/vol-<V>/<id>_*.txt`. Every row gives the median of the other same-site HA reports, which agrees with the Hebrew value, e.g. 23 Caesarea reports, median 190200/711974; 30 Yattir Forest reports, median 203285/584900. Seven of the 10 (530, 521, 48, 997, 860, 8518, 339) were confirmed unchanged on the live English pages on 6 Nov 2026. For 148 and 177 the parser found no map reference on the live page, and 270 was not re-fetched.
Literature check (queries run, result, tag): web search for HA-ESI map-reference errata or audits found nothing. Repo: none of these ids is in the project's misprint list, and git grep on main for "60853", "51886", "614520", "17518/64680" and "21000/75400" returns no hits. **NEW TO THE LITERATURE.**
Why it might matter: The English pages are what most non-Hebrew readers use, and what the project's own HA/ESI extraction used. A systematic English-vs-Hebrew comparison is a cheap quality check that catches errors no single-language reader can see. The two vol. 119 northing swaps look like one translator or typesetter's habit, which suggests checking other HA 119 reports by hand.
How to confirm or kill it (with data in hand, or what is missing): Open the English and Hebrew PDFs (`hadashot/pdf/en|he/vol-<V>/<id>_*.pdf`) for each id and read the first paragraph. The pdftotext layer could in principle have garbled the Hebrew digit order. But in every case the Hebrew value is the one that agrees with the OIG twin and with the other same-site reports, so a mistake by the extractor would not explain the pattern.
Confidence: high for 530, 521, 48, 997, 860, 8518 and 177; medium for 148, 270 and 339
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): At least 26 HA-ESI map references are wrong in both language versions. Some are exact 50 km grid mix-ups (Qazrin, Tiberias Courtyard of the Jews, Ramat Aviv, Eshtaʾol), some are NIG/OIG pairs that disagree in the same sentence, and Tel Qaqun is printed at N 969200
Lane: D3
What is odd (2–4 sentences): HA 116–121 print both an NIG and an OIG reference, and the two must differ by exactly +50 km E and +500 km N. In 12 reports they do not. One of the two is off by a round amount (10, 20, 27, 50, 100, 300 or 450 km), and the other agrees with the site.
- OIG wrong: Bet Sheʾan (OIG N +300 km); ʿIsfiya; Kinneret Berenice aqueduct.
- NIG wrong: Ramla military cemetery (NIG N 198680, should be 648680); Eshtaʾol (NIG E 251383, should be 201383); Shilat (NIG N 747303, should be 647303); Tell Qasile; Horbat ʿOmrit 2007; Shimshit; Ramla Bar-Ilan St; Yafo flea market; Shefarʿam (NIG N 75400, should be 74500).
In 4 further reports the NIG and OIG agree with each other but are both off by a grid-sized amount, so the mistake was made before conversion:
- Qazrin (id 1028): NIG E 2134 (the true OIG easting), 50 km west in the Lower Galilee.
- Tiberias, Courtyard of the Jews (1182): NIG E 30115, 50 km east, in Jordan.
- Saviyonei Ramat Aviv (635): N 616765, 50 km south.
- Tel Aviv Exhibition Grounds (1035): N 676787 for about 667.
Single-grid references from later volumes include Tel Qaqun 199553/969200 (which falls outside Israel; 699200 intended) and Naʿura 742459 for 724459. Kefar Abraham (Petah Tiqwa), Ramla South, Azor, Elʿad, Amazya, the Yafo flea market compound (id 900, which plots in SW Jerusalem) and Kh. Buleiʿis are also off by 18–78 km.
Evidence (exact sources: file path / page / figure / frame / coordinates): `ha_mapref_errors.csv`, classes "C NIG/OIG pair" (12 rows) and "D both grids wrong / single grid wrong" (14 rows). Report ids: 1200, 980, 993, 738, 339, 967, 634, 729, 901, 595, 186, 431; 1028, 1182, 635, 1035, 26175, 1878, 2175, 1418, 900, 1181, 682, 1180, 1075, 25572. Each row gives the printed string, the wrong part, and the evidence: the twin grid value, or the median of other same-site HA reports. Examples: Qazrin report 841 gives 2633–40/7661–8; Ramla's 175 reports have median 187786/648376; Omrit 2009 (report 1638) gives 262220/791530. For the rows marked "live EN page 2026-11-06: same", the error is still on the live English site.
Literature check (queries run, result, tag): web search for audits or errata of HA map references found none. The project has caught 22 such misprints, all within its Judean study zones, and they are excluded above. None of the 26 is in the project's lists. **NEW TO THE LITERATURE** (as an audit; a reader may have noticed some single cases privately).
Why it might matter: HA-ESI is the main gazetteer of Israeli salvage excavations, and pipelines (including this project's haesi_features, water, tomb and cave inventories) geocode it from the printed map reference. The error classes are systematic and repeat, so they are worth guarding against in code: the 50 km E or N offset between grids, the 500 km NIG/OIG northing swap, and 2-digit transpositions. A single rule would catch most of them: reject a reference whose NIG and OIG disagree, or that falls more than 5 km from the named place.
How to confirm or kill it (with data in hand, or what is missing): Re-run `pairs.py` and `outliers.py` on the tarball; each row takes about 1 minute to check against the PDF. The rows marked "not re-fetched" (967, 634, 729, 901, 595, 186, 431, 1075, 270) were read from the bucket text layer only. A row is killed if the report says the excavation lay somewhere other than the named site. I read every opening sentence to rule that out, but the medians of large groups (Ramla, Yafo) are coarse.
Confidence: high for the NIG/OIG pair rows, 1028, 1182, 635 and 26175; medium for the rest
Touches the Copper Scroll? maybe. None of the 26 lies in the scroll regions. But the same error classes, applied to the HA reports the project does use, are what its pipeline guard should catch (the project's own fixes so far were made one by one).

---

## Dead ends
- Within-site outliers over 4 km (check c) are mostly real sub-sites or different places with the same name (ʿArʿara in the Negev vs Wadi ʿAra; the two Tamras; Dor vs the Haggit power station; Bet Shemesh/Har Tuv; Nahal Besor/Nahal Patish surveys). I dropped them unless a digit pattern or a twin grid shows the error.
- Ramla reports 124 (Grez St) and 614 (Qiryat Menachem Begin) both point to about 199/637–638, 15 km from Ramla. They are consistent with each other and the error is not proven, so I dropped them.
- Tarshiha survey (1689): EN 76740 vs HE 76840. Both are plausible for Tarshiha, so I dropped it. Kh. el-Keikh (1093): a 1 km NIG/OIG mismatch whose correct value cannot be decided.
- The Highway 5 cave between Rosh Ha-ʿAyin and Ariel (244, NIG N 64891, probably 66891) is plausible but ambiguous, so I dropped it.
- North and east written in the wrong order (Merot 25773, Tell el-Ful 1888, Jatt 26477, Tel Yavne 26437, Nes Ziyyona 1870, Ashqelon 25167 and others) is a convention slip with no positional ambiguity. Low value, not carded.
- 5-digit truncations in one language only (Givʿat Homa 653, Tel ʿAkko 26307, Nahal Shalva 25914, Rosh Ha-ʿAyin 25900, Tifʾeret Yisraʾel 25692) are trivial typos, not carded.
- Most raw EN/HE "differences" (130) and "implausible" refs (335) are parser artefacts: the Hebrew bidi order reverses ranges ("237/623449" from "198222–237"), and permit numbers like "138/2009" are caught as references. I filtered them by hand; do not re-run the raw counts as findings.
- Figure and plate cross-reference checks (`hexview.py pdf-search "Fig."/"Pl."` on the page-split monographs) were not run because of the call budget. This route is still open for a later worker.
- `tables/qumran_published_gps.csv` (4 rows, one source) and `qumran_survey_crosswalk.csv` (7 rows, no coordinates) are too small for a coordinate cross-check. The cave inventory's misprinted ʿAtiqot 41 grids are already flagged in `research/regional/caves_entry25/AMENDMENT_1.md` §11.

## Blocked inputs
- `git grep` across all 86 `origin/*` branches for "wrong grid|erratum|misprint|typo" did not finish (it was still running when backgrounded at 120 s, and a second run was killed at 100 s). The novelty check therefore used main (HEAD) plus the haesi_features `reports.csv` and `coding_online*.json` files, which hold the project's HA misprint notes. A branch-only note could have been missed.

## Seed / reproducibility
- Input: `gs://copper-scroll-cog-1030/hadashot/derived/hadtext_pdftotext.tgz` (24.8 MB), extracted to scratch; metadata `/home/claude/swarm/baseline/reports_metadata.csv`.
- `python3 -I mapref.py <extract_root>` → `refs_raw.json`; then `compare.py` (EN vs HE), `pairs.py` (NIG−OIG ≠ 50 km/500 km), `outliers.py` (more than 4 km from the same-group median). The scripts expect the scratch paths used on 6 Nov; edit the paths at the top to re-run them.
- Live checks: `curl https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=<ID>`, 6 Nov 2026.
