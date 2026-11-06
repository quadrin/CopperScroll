# Side-quest D1 (Loose ends): finds, 6 November 2026

Worker: lane D1. Inputs read: `research/OPEN_QUESTIONS.md` and `research/assessments/` (main, clone of 4 Nov), the Drive 08 archive requests tracker (all 61 rows), the Drive 08 Reading catalogue listing, the Drive "04 Further archive reading — 2026-11-02" folder (listing plus full-text marker searches, and 4 notes read in full), and the session chunks folder (top-level listing only).

The loose-end list is in `out/D1/loose_ends.csv`: 206 rows with the columns source_file, location, marker, item and data_in_hand_that_could_close_it. It holds 120 marker hits from the repo, 44 open tracker requests, 12 items found while reading Drive notes and 28 Drive file-level full-text hits. **None of these inputs uses the literal words "unmatched" or "not yet equated".** The repo uses "undated" (54), "in progress" (37), "parked" (24) and "unreconciled" (7).

---

FIND CARD
Title (one line): The ROSAPAT 07 catalogue's 21.5 m depth for Birket Musa is an error: with the catalogue's own footprint it gives a volume about 9.5 times the excavator's figure.
Lane: D1
What is odd (2–4 sentences): The PADIS/ROSAPAT catalogue entry for Birket Musa, the largest ancient reservoir at Jericho, prints "Site extension: 220 × 160 m, 21.5 m deep". The project records this as "unreconciled" and says "no typo correction ... follows". Every primary source the catalogue itself cites, and that the project holds, rules out a depth of that order. SWP saw walls 5–6 ft high. Netzer's 2002 appendix (Netzer is cited by the catalogue) gives at least 3 m depth and at least 80,000 m³. 220 × 160 × 21.5 = 756,800 m³, which is 9.5 times Netzer's minimum. Netzer's own 180 × 150 m footprint and 80,000 m³ imply about 3.0 m.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Catalogue: bucket PDF `Nigro-Sala-Taha-eds-2011-Archaeological-Heritage-in-the-Jeri-9af25da3`, PDF page 132 (printed p. 120), entry "38) Birket Musa [PADIS code 0025]", lines "Site extension: 220 × 160 m, 21.5 m deep"; its bibliography is Conder–Kitchener 1883 pp. 176, 192; Augustinović 1951 pp. 50–51; Robinson–Smith 1970 p. 563; Netzer 2002 (full reference on PDF p. 202). Read with `hexview.py pdf-text <doc> 132`.
- Project records: `research/assessments/entry29_jericho_pools/README.md` line 232 ("remain unreconciled ... no typo correction"); line 646 (Netzer & Garbrecht 2002, Appendix B p. 377: c. 180 × 150 m, at least 3 m deep, at least 80,000 m³); `regional_inventory_2026-10-06.csv` row J12 (SWP III p. 192: walls 5–6 ft surviving height; footprints 174 × 146 m and 201 × 149 m).
- Arithmetic: 220 × 160 × 21.5 = 756,800 m³; 80,000 / (180 × 150) = 2.96 m.
Literature check (queries run, result, tag): web search for `"Birket Musa" Jericho pool depth meters Netzer` found no publication that discusses or corrects the catalogue depth. Repo grep (`Birket Mus`, `PADIS 0025`): the depth appears only as "unreconciled"; it has not spread into the regional inventories. Tag: **NEW TO THE LITERATURE**. The project already flagged the mismatch, but it did not settle it.
Why it might matter: J12 is the largest basin in the entry-29 Jericho pool roster. A 21.5 m depth would make it a unique deep installation. With the depth corrected it is a shallow irrigation reservoir, and this removes one outlier from the pool denominator.
How to confirm or kill it (with data in hand, or what is missing): this is settled as an error on internal grounds. The source of the figure is not: it may be a garbled 2.15 m or 1.5 m, or a misplaced number from Augustinović. To trace it, read Augustinović 1951 pp. 50–51 and Robinson–Smith 1970 p. 563, neither of which is in hand. Netzer 2002 p. 378 is also still unread (the Drive photo `1i3nBQrf7pdPnIF03FHJNIqv6BDd45jWr` shows p. 377 only, and its OCR is poor).
Confidence: high (that 21.5 m is wrong); low (on what the right figure is).
Touches the Copper Scroll? maybe. It concerns the entry-29 Jericho pool inventory (J12), not an identification.

---

FIND CARD
Title (one line): Map check of Kh. Abu Lahm (Mandate file 8751): "E. and S. of ʿAin Duk" is right, and "4 km NE of ʿAin es-Sultan" has the wrong direction (it lies NW to NNW).
Lane: D1
What is odd (2–4 sentences): The owner's reading of 5 Nov leaves two location statements on the Mandate cards for Kh. Abu Lahm "pending a map check". One is Ory's 1928 "E. and S. of Ein Duk". The other is "by car 4 Km NE of ʿain es-Sultan", which appears on both the cover and Baramki's 1938 card. The card's own grid reference, 191.144 (Palestine grid), and ROSAPAT's position for the Maqam al-Imam ʿAli both put the ruin ESE to SE of ʿAin Duk. Both put it 2.2–3.2 km NW to NNW of Tell es-Sultan (bearing 320°–344°), not NE. "4 km" can be a road distance, but "NE" is wrong.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Mandate cards: Drive folder `Jericho_Muntar_Abu_Lhm_first_reading_2026-11-05` (`1w210OjLkLLA32zJ0XpHXFFOdnEGXoogK`), images `4534876-094900_001_000001.jpg` (cover: "191 144", "E. and S. of Ein Duk", "car 4 Km. NE of 'ain essultan") and `4494518-094900_001_000004.jpg` (Baramki, 14.5.38, "By car NE ʿAin Sultan"). The owner's note is `1xybmksmGS72XPTS9695ITTKJgtw7u1RK` ("Preserve the two statements as historical directions pending a map check").
- Positions used (all recorded public sites): Tell es-Sultan and ʿAin Duk from `tables/phase3_places.csv`; Maqam al-Imam ʿAli from ROSAPAT 07, PDF p. 141, no. 56. All three were converted to the Palestine 1923 grid (EPSG:28191 parameters, towgs84 Helmert, Cassini-Soldner). As a check, the conversion gives Tell es-Sultan 192.18/142.11, against the standard 192.142, and the Dome of the Rock 172.4/131.7.
- Results: card point 191.0/144.0 lies 2.23 km at 328° from Tell es-Sultan and 1.68 km at 126° from ʿAin Duk. The centre of the 1-km square, 191.5/144.5, lies 2.48 km at 344° and 1.93 km at 104°. The ROSAPAT maqam lies 3.22 km at 320° and 0.62 km at 132°.
- Script: `scratch/D1/py/palgrid.py` (can be copied into the repo on request; it contains no private coordinates).
Literature check (queries run, result, tag): web search for `"Abu Lahm" Jericho "Imam Ali" maqam Duyuk location`; repo grep for `Abu Lahm`; Drive full-text search for `Abu Lahm`. Nothing discusses the cards' directions; the owner's two notes leave the question open. Tag: **NEW TO THE PROJECT**. The cards are unpublished archive records.
Why it might matter: Q24 (Doq, entry 31) and the `ain_duk` rating (`ratings.csv` line 50) depend on where Abu Lahm's wall, ditch, tower and silos lie relative to the spring. The check confirms that the ruin is the spring-side site east of ʿAin Duk. Nobody should look for it NE of Jericho.
How to confirm or kill it (with data in hand, or what is missing): register the SWP XVIII square "Ps" (Mukam Imam ʿAly) on the georeferenced SWP sheet in Drive 07, and the Izzo–Fradley–Zerbini 2022 Fig. 5/Site 3 (not inspected: retrieval failed). The card grid lies about 0.9 km east of the ROSAPAT maqam point; that offset is unresolved but does not change the direction finding. This card does not date the silos. The comparison with Kh. Mefjer sherds cannot date them, as the owner's note already says.
Confidence: medium-high (direction); low (exact spot).
Touches the Copper Scroll? maybe. It bears on entry 31 (Q24, the summit versus the spring for Doq). It is not an identification.

---

FIND CARD
Title (one line): OPEN_QUESTIONS R07: the "current follow-up" line says Kallai 1972 pp. 172–173 is unread, but a line above in the same section records it as read on 19 Oct.
Lane: D1
What is odd (2–4 sentences): The live question record for R07 (Koḥlit, Achor, Sekakah) contradicts itself. Line 183 says Kallai 1972 pp. 172–173 "are read from the owner's library photos" (19 Oct) and reports a result: the pool lies west of Kh. el-Marjama, is undated, and is not called rock-cut. This result excludes classes c06, c07, c09 and c10. Line 197, under the bold label "Current follow-up (8 October ...)", still says "Kallai1972 pp.172–173 remains unread after the latest115-file audit". A reader who takes the "current" label at its word will request a source the project already holds. The same pattern of a stale status line contradicted by a newer one appears in `research/assessments/entry29_jericho_pools/README.md`. Lines 148–151 say "no located Plan 14 sheet" and "Plans 15/23 not located". Line 643 of the same file and `netzer2001-first-pass.md` line 260 record Plans 14, 15 and 23 as photographed at the NLI on 21 Oct.
Evidence (exact sources: file path / page / figure / frame / coordinates): `research/OPEN_QUESTIONS.md` lines 183 and 197 (section "R07 — Where were Koḥlit, Achor and Sekakah?"); `research/assessments/entry29_jericho_pools/README.md` lines 148–151 against line 643; `netzer2001-first-pass.md` lines 254–255 against line 260. The checkout is at origin/main, last commit 4 Nov 2026.
Literature check (queries run, result, tag): this is internal to the project; no outside literature applies. `record_conflicts.md` (79 conflicts, 15 Oct) does not list either pair. Tag: **NEW TO THE PROJECT**.
Why it might matter: stale "unread" and "missing" lines in the live records create repeat requests and repeat archive searches, and the tracker already has 26 unanswered requests. The owner can fix this in one edit. Under brief §7 I did not edit OPEN_QUESTIONS.
How to confirm or kill it (with data in hand, or what is missing): read the two pairs of lines. To kill it, the owner would have to show that line 197 means another Kallai page range. Nothing in the line suggests that.
Confidence: high
Touches the Copper Scroll? maybe. It concerns R07 (entry 60 district) and entry 29 records; it is a record-keeping fix only.

---

## Dead ends

- R05 Gerizim locus P5178: I searched the bucket PDFs for "5178". JSP 8 has no hit; JSP 20 is not in the store. The project had already reached the same result (JSP 8 read on 29 Oct), so I dropped it.
- The Szanton (26 Oct) tracker reply about Great Revolt coins in the Siloam pool-floor foundation: I checked it as a possible contradiction with R06. It is not one, because `research/measurements/cycle10/README.md` already records coin 20 at L105 (69/70 CE).
- The tracker's Summary tab against its Requests tab: I recounted all 61 rows (9 Waiting / 9 Partly / 26 No reply / 7 Answered / 10 Closed). They match, so there is no contradiction.
- Mirrored tables (`tables/` against `atlas/research/`: the phase5 index, phase3 site index and phase3 places): I compared them row by row. They are identical except for line endings.
- Dating Kh. Abu Lahm from the Mandate "Kh. Mefjer" sherd comparison: the owner's note of 5 Nov already rejects this as a date for the silos, so it is not a new find.
- Choziba cave 20 (R03, line 126): the Drive 04 PDFs of 5 Nov already treat the 2nd-c. lamp and the cell-number crosswalk. It is listed in the CSV as a post-dated update, not as a find.
- Twin Cave distance claims ("about 1 km N", "south of 11Q"): all repo statements agree.
- Netzer & Garbrecht 2002 p. 372 (9 l/s against 12,000 m³/day): this is a real published arithmetic error, but the project had already flagged it (README line 645).

## Blocked inputs

- Drive 08 "Session chunks 2026-10-31" (`1S05dJXurpT9mEHHpyVcp8ERunBux7mH7`): only the top level was listed (the subfolders `small`, `text` and split PDFs of Hebrewbooks 32811 and Hütteroth). The subfolders were not opened within the call budget. This is not a technical error.
- Drive 04 folder: about 200 items. Full-text marker searches returned 28 files with hits, but the Drive search does not give the line within the file. Only 4 notes were read in full (IAA further reading notes; Abu Lhm first reading; Muntar/Abu Lhm follow-up; and the snippet of Nablus Ras el-Ain).
- `hexview.py pdf-search` across all documents crashed with `json.decoder.JSONDecodeError: Unterminated string` on one document's `pages.jsonl` (the first partial results were printed). Per-document searches with `--doc` worked.
- Netzer & Garbrecht 2002 Appendix B p. 378: not in the bucket's `01-Aqueducts-of-Israel-2002-indexed` (216 pp, no Birket Musa page). The Drive photo of p. 377 opens, but its OCR is unreadable.
- `git grep` across all 86 branches timed out (more than 180 s on the shared disk). Checks of branches other than main were done only through the summary baselines.

## Seed / reproducibility

- `scratch/D1/py/palgrid.py` converts WGS84 to the Palestine 1923 grid (EPSG:28191 parameters); run it with `python3 -I palgrid.py "name,lat,lon" ...`.
- `scratch/D1/py/build_csv.py` regenerates `loose_ends.csv` from the repo, with the tracker rows and Drive rows hard-coded from the reads of 6 Nov.
