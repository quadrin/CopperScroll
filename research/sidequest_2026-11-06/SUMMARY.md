# Side-quest swarm, 6 November 2026: summary

**Goal (brief of 6 Nov 2026):** find anything new, strange or overlooked in the Copper Scroll corpus, whether or not it relates to the scroll. A find must be specific, checkable and new. A find is **not** an identification. Nothing here changes a rating, the outcome ledger, ACTIVE_TEST, OPEN_QUESTIONS or the atlas data.

**What ran:**
- 25 lane workers (A1–A6, B1a–c, B2–B6, C1a–c, C2–C4, D1–D3, E1, E2). Each worker made one bounded pass. All work was AI only: no contact with people and no purchases.
- Then 6 reviewers (R1–R6) who had not taken part. They opened the cited evidence, redid every literature check, and tried to kill every card.

**Result:**
- Workers wrote **69 find cards**. The reviewers **killed 1** (E1-2) and **weakened 14**. They changed the tag of 2 cards, downgraded the tag of 1 card in part, and merged 2 cards into one (B1b-1 + B1c-2).
- **67 distinct cards survive.**
- Tags of the surviving cards, counted by each card's leading tag: **22 NEW TO THE LITERATURE, 37 NEW TO THE PROJECT, 8 KNOWN BUT UNDER-DISCUSSED.** Several cards carry a second tag for one part; each lane's `FINDS.md` has the exact tags.
- No find identifies a scroll place. Several touch scroll entries (24, 29, Qumran caves) or the project's own data. See "Corrections for the owner".

**Where everything is:**
- Each lane has its own branch, `claude/sidequest-2026-11-06-<lane>`, with `research/sidequest_2026-11-06/<LANE>/FINDS.md` plus data.
- This branch has all 25 lane folders, the reviews (`review/R1.md` … `R6.md`, `review/all_verdicts.csv`) and this summary.
- **Private products** are not in the repository: crops from USC/WSRP, IAA, HEXAGON and the owner's photos, and the coordinates of unrecorded features. They were delivered to the owner as a download (see "Private products").

Ranking rule (brief §8.4): tag (NEW TO THE LITERATURE first) × confidence × cost to confirm. Ties were broken toward variety of lanes and toward cards that touch the scroll or the project's data.

---

## Top 10

### 1. The 1955 Manchester cut-mark labels on 3Q15 and errors in their published record (A1-1)
- **Tag:** NEW TO THE LITERATURE (the errors); NEW TO THE PROJECT (the marking scheme). **Confidence:** high. **Cost:** cheap. **Touches the scroll:** yes, as a physical object.
- **What:**
  - In 1955 each segment of the large roll (segments 2–15) was labelled in white ink with a letter F–A and a number 1–12; segments 16–23 carry only their numbers.
  - EDF 2006 (Brizemeure–Lacoudre–Puech) publishes the ranges, and they cannot all be right. Segment 14 is given as "A5 à A4", but segment 13 ends at A4 and segment 15 starts at A8, so it must be A5–A7. E1 never appears, E4 is listed twice, and segments 6, 7 and 15 are marked "?".
- **Review (R1):**
  - The errors stand, but the card had the orientation inverted. Kuhn 1954 p. 195 says roll A was wound from the beginning, so F is the inner turn and A the outer.
  - That explains the card's open point: the width per mark grows from about 1.1 cm (F) to about 2.4 cm (A), as 12 marks per turn predicts, and Kuhn's "6 ½ turns" fits the six letters.
- **Evidence:** EDF 2006 PDF pp. 67–79 (segment 14 on p. 73, segment 6 on p. 70); Manchester TPA correspondence, 19 Oct 1955 and 6 Mar 1956; `A1/cut_marks_1955_record.csv`.
- **Confirm:** the EDF vol. II pre-restoration verso plates XXX–LII are in the bucket (PDF page = 316 + segment number). R1 saw a small white "6" at the foot of segment 14 (Pl. XLIII, PDF p. 330), which fits A5–A7; this reading is low confidence at book resolution.

### 2. The "near Cave 1" Arad–Beersheba sherd QUM 209 (KhQ 2575) came from locus 30 of the settlement (B6-1)
- **Tag:** NEW TO THE LITERATURE. **Confidence:** high. **Cost:** cheap. **Touches the scroll:** maybe, through the cave–settlement pottery argument.
- **What:**
  - Gunneweg & Balla 2003 put QUM 209 "north of Cave 1": App. I p. 36, II p. 41, III p. 45 and the table on p. 390. Their conclusion 1 (p. 393) rests on it.
  - Two other witnesses put it in L30: Lemaire in the same volume (p. 369, "locus 30 au 27/03/1955", provenance Arad–Beersheba) and de Vaux's register (Humbert & Chambon 1994 p. 302, "2575 : tesson marqué").
  - "North of Cave 1" is the find spot of a different object, the LYʿZRH jar KhQ 2507 (Lemaire p. 364).
- **Review (R1):** the card gets stronger. Humbert & Chambon 1994 lists 2578 as a "gobelet", so "KhQ 2578" on p. 392 is a typo, not a second Cave 1 sherd. The NAA "carved cross" matches Lemaire's incised 2575.
- **Evidence:** bucket page store of Humbert–Gunneweg 2003; Drive book photo IMG_2980; `B6/naa2003_register_conflicts.csv`.

### 3. The Siloam Dam / Birket al-Hamra: wall W114 was silently re-dated, and the charcoal date of L108 cannot be old wood (A6-1)
- **Tag:** KNOWN BUT UNDER-DISCUSSED (the RTT 6089 discrepancy was flagged in 2020); NEW TO THE LITERATURE (the silent re-dating and the old-wood argument). **Confidence:** high (the arithmetic), medium (that L108 is a later plaster). **Cost:** cheap.
- **What:**
  - Szanton, Vukosavović & Berko 2024 put W114 in "Stratum 4 (Persian–Hellenistic?)" (printed p. 33*, PDF p. 16), supported by Boaretto's 520–200 BCE date.
  - PNAS 2025, by the same team, calls W114 the core of the dam, dated about 805–795 BC.
  - RTT 6089 (charcoal, L108, 2300 ± 55 BP; ʿAtiqot 101:79–80) is 322 ± 56 radiocarbon years younger than the dam's combined 2622 ± 10 BP, a 5.8σ gap. Old wood can only make a date too old, so L108 is later re-plastering or intrusive carbon.
- **Review (R3):** survives. `research/measurements/cycle11/siloam_phase.md` on main already has most of the pieces. It lacks the Stratum 4 → dam contradiction, the old-wood argument and the 5.8σ figure.

### 4. Eight Hadashot English reports print another excavation's IAA permit number (B1b-1 + B1c-2, merged)
- **Tag:** NEW TO THE LITERATURE. **Confidence:** high. **Cost:** cheap.
- **What:**
  - In 8 reports the Hebrew text and the figure-file prefix (`Images//<permit>-n.jpg`) agree, and the English permit differs. In most cases the English number is another dig's real permit: 2066, 14719, 350, 25581, 25629, 25933, 25992, 26102.
  - Examples: Ramla Ibn Sina (2066) prints A-6171, which is Ḥ. Qishron; Ginnaton (25581) prints A-7197, which is Gush Ḥalav; Ḥorbat Ḥanot (25933) prints A-8357, which collides with Gan Ha-Darom.
  - Also: the English Tel Shaddud report (25133) leaves out a second permit and a February 2014 season.
- **Why it matters:** an IAA archive request built from the English page would retrieve the wrong excavation's file.
- **Evidence:** `B1b/ha_permit_en_he_errors.csv`, `B1c/ha_en_he_permit_conflicts.csv`; bucket `hadashot/derived/hadtext_pdftotext.tgz`.

### 5. The English HA 129 "Tiberias" report opens with a paragraph copied from another report (D3-1)
- **Tag:** NEW TO THE LITERATURE. **Confidence:** high. **Cost:** cheap.
- **What:**
  - Report 25159 (Dalali-Amos & Hanna) opens with the opening paragraph of HA 129 report 25169, Ramat Bet Shemesh D2 (Shalev), word for word except the permit numbers.
  - So the English gives the wrong site (west of Tel Yarmut), the wrong map reference (19700–05/62430–50), the wrong director and the wrong funder.
  - The Hebrew is correct (250696–755/743631–93).
- **Evidence:** `en/vol-129/25159_tiberias.txt` against `25169_…d2.txt`, lines 9–18.
- **Review (R2):** survives.

### 6. The 2003 NAA sample register contradicts itself and de Vaux's register on at least 12 samples (B6-2)
- **Tag:** NEW TO THE LITERATURE. **Confidence:** high. **Cost:** cheap.
- **What:**
  - KhQ 1080 is in L44 in all three appendices, but in L61 in Humbert & Chambon 1994 p. 312 and in the 2016 L61 catalogue p. 178.
  - KhQ 1139 is a lid from L58 in two appendices and a bowl from L61 in the third.
  - App. II gives wrong object numbers for QUM 200, 214 and 320.
  - Further slips: KhQ 1236 is put in L62 (should be L73), KhQ 1286 is called a "potter's wheel" (it is a cup), KhQ 425 appears as "L.108" (should be L10A), and KhQ 16 appears as KhQ 6.
- **Review (R1):** survives. The L44 labels on L61 samples are probably the old label carried over: Humbert & Chambon 1994 says "23-2-1954. Le locus 44 sud est divisé en … loci 59, 60 et 61". The other conflicts are unaffected.
- **Evidence:** `B6/naa2003_register_conflicts.csv`; 2003 page images pp. 35–43 and 392.

### 7. ASI Map 109/4 (Wadi Qelt) prints elevations for 18 below-sea-level sites without the minus sign (D2-2)
- **Tag:** NEW TO THE LITERATURE. **Confidence:** high. **Cost:** cheap. **Touches the project's data:** yes.
- **What:**
  - The 18 sites include St George/Choziba, the Choziba cells, the Naḥal Perat 7–9 aqueducts and ʿEin Qelt (1). Several are rows in `water.csv`.
  - With the sign flipped, the printed values match GLO-30 to a median 10.7 m; the 101 sites above sea level on the same map match to 8.8 m.
  - The Hebrew pages carry the same values. Map 18 (Rosh Pina) has the same fault at sites 310, 354 and 355.
- **Review (R6):** confirmed in two ways. The same map prints "−80 m bsl" correctly at 109/4/127, and the map introduction uses a sea-level datum.
- **Evidence:** `D2/asi_elevation_vs_glo30.csv`; e.g. https://survey.iaa.org.il/#/MapSurvey/68/site/9247

### 8. WBADB grid errors are copied into the project's water inventory, where one site is counted twice (B2-1)
- **Tag:** NEW TO THE LITERATURE. **Confidence:** high. **Cost:** cheap. **Touches the project's data:** yes.
- **What:**
  - WBADB's Patrich 1994a site 95 is 6,751 m east of the IAA online record (Map 109/7 site 95). R4 notes this record is the Great Laura at Mar Saba.
  - For Bar-Adon site 20, ASI 1 p. 107 prints only the northing; WBADB filled in the easting as 190000, about 9 km off.
  - `water.csv` on main holds both `ASI-109/7/95-cistern` and `WBADB-S4146-cistern`, unlinked and 6.7 km apart.
- **Method:** an ASI site code names its 1-km square. 83 of the 4,992 coded WBADB rows have grids outside their own square.
- **Evidence:** `B2/coordinate_audit_wbadb_vs_asi_online.csv`.

### 9. Hisham's Palace (Kh. el-Mafjar) is mislocated in ROSAPAT 07 and in the project's water inventory (C1b-1)
- **Tag:** NEW TO THE LITERATURE (the ROSAPAT offset); NEW TO THE PROJECT (row J15). **Confidence:** high. **Cost:** cheap. **Touches the project's data:** yes (entry 29).
- **What:**
  - ROSAPAT 07 (2011) p. 126, no. 50, puts the palace 1.05 km ESE of where it is; no. 51 repeats the same point.
  - The project's `water.csv` row LIT-E29-J15 puts it 4.3 km SSE. It took the coordinate of ASI 109/5/23 "Khirbet Mafjar (1)", a different place of the same name.
- **Method:** found by placing recorded sites on the March 1945 1:10,000 Jericho mosaic, which C1b georeferenced to the Palestine Grid at about 6 m RMS.
- **Evidence:** ROSAPAT bucket PDF page index 138; `water.csv` line 2017; `C1b/rosapat_vs_mandate_coords.csv`.

### 10. The Cave of Salome is published as "8 km southwest of Tel Lakhish", but its own map reference puts it 8 km east-southeast (A6-2)
- **Tag:** NEW TO THE LITERATURE. **Confidence:** high. **Cost:** cheap.
- **What:** Paran & Lifshits 2025 (ʿAtiqot 117, printed p. 109) give map reference 193105/605325. That point lies 7.95 km from Tel Lachish at a bearing of 111°, 1.6 km ENE of Amatzia. Only the compass word in the text is wrong.
- **Review (R3):** survives.

---

## All other surviving cards

Each lane's `FINDS.md` has the full card, and `review/R*.md` has the reviewer's notes and corrections. "WEAKENED" means only part of the claim holds; the review file says which part.

| # | Lane-card | Short title | Final tag | Review verdict | Confidence | Cost to confirm |
|---|---|---|---|---|---|---|
| 11 | A2-1 | Boer P17 ≠ KhQ 1627 (inventory dates) | NEW TO THE LITERATURE (prov.) | SURVIVES | low-medium | moderate |
| 12 | B1b-2 | Cited permits belong to unrelated digs | NEW TO THE LITERATURE | SURVIVES | high (1–3), medium (4) | cheap / moderate |
| 13 | B1c-1 | EN vs HE excavation year; permit clock | NEW TO THE LITERATURE | SURVIVES | high | cheap |
| 14 | B1c-3 | Naḥal Shalva "bronze coins" | NEW TO THE LITERATURE (minor) | SURVIVES | high | cheap |
| 15 | B4-1 | Gerizim 2008→2021 coin basis drift | NEW TO THE LITERATURE | SURVIVES | high (facts) / medium (meaning) | moderate |
| 16 | C1b-2 | ROSAPAT Tell Abu Hindi = St Andrew coordinate; J19 placed | NEW TO THE LITERATURE / PROJECT | SURVIVES | medium-high | cheap |
| 17 | D1-1 | ROSAPAT Birket Musa 21.5 m depth is an error | NEW TO THE LITERATURE | SURVIVES | medium (was high) | moderate |
| 18 | D3-2 | EN vs HE map refs (10) | NEW TO THE LITERATURE | SURVIVES | high | cheap |
| 19 | D3-3 | 26 map refs wrong in both languages | NEW TO THE LITERATURE | SURVIVES | high | cheap |
| 20 | E1-1 | Giv'at Avni feature refs outside box | NEW TO THE LITERATURE | SURVIVES (sharpened by Fig. 2) | high | cheap |
| 21 | E1-3 | HA DOIs "116.2004"; IAA as Crossref author | NEW TO THE LITERATURE | SURVIVES (reframe) | high | cheap |
| 22 | E2-1 | Hoards no closer to roads than excavations | NEW TO THE LITERATURE | SURVIVES | medium | moderate |
| 23 | A4-2 | Schick 8.2° frame vs Corbo/G&T 6.2–6.9°; 2,420 ft datum | NEW TO THE LITERATURE | WEAKENED | high (numbers) / low (interpretation) | cheap |
| 24 | B4-2 | Martyrius 613 override, duplicate K, no Justinian | NEW TO THE LITERATURE | WEAKENED | high (facts) / low (chronology) | cheap–moderate |
| 25 | A1-2 | 115 TIFFs = recto only; no verso | NEW TO THE PROJECT | SURVIVES | high (arithmetic); low-med (RE reason) | cheap / moderate |
| 26 | A2-2 | three HC1994 misprints | NEW TO THE PROJECT | SURVIVES (locator fix for b) | high (b, c); medium (a) | moderate |
| 27 | A2-3 | EBAF Lot 2 numbering vs header | NEW TO THE PROJECT | SURVIVES | medium | moderate |
| 28 | A3-1 | Albright sheet grid offset; 1925 vs 1927–28 print states | NEW TO THE PROJECT | SURVIVES | high (fit), medium (novelty) | cheap / moderate (annual reports) |
| 29 | A4-1 | QC report ≠ deposited build (Vincent & Abel removed; 154 absent) | NEW TO THE PROJECT (mismatch NEW TO THE LITERATURE) | SURVIVES | high | cheap |
| 30 | A5-1 | Meinardus St Andrew pp. 181–193 already in Drive | NEW TO THE PROJECT | SURVIVES | high | cheap |
| 31 | A5-2 | IMG_0771 = Avigad 1954 pp. 74–75 | NEW TO THE PROJECT | SURVIVES | high | cheap |
| 32 | A5-3 | March-1945 1:10,000 Jericho photo-mosaic | NEW TO THE PROJECT | SURVIVES (context corrected) | high (identity), unknown (use) | moderate |
| 33 | A6-3 | Maresha IV northing-first map refs | NEW TO THE PROJECT | SURVIVES (corrected: NIG named once; SC 99 refs 520 m apart) | high | cheap |
| 34 | B1a-1 | Moẓa unread Second Temple Hebrew inscription | NEW TO THE PROJECT | SURVIVES | medium / low | moderate |
| 35 | B1a-2 | Garden Tomb glass Neo-Assyrian cylinder seal | NEW TO THE PROJECT | SURVIVES | medium / low | moderate |
| 36 | B2-2 | Bar-Adon 116–139 open-air sites never re-surveyed | NEW TO THE PROJECT | SURVIVES | medium | moderate |
| 37 | B2-3 | Site 138 fortress + robbed cemetery unlinked to ʿEin el-Ghuweir | NEW TO THE PROJECT | SURVIVES | low (identity) / high (record) | moderate |
| 38 | B3-2 | CIIP 3738 placed in SC 89 Room 40 | NEW TO THE PROJECT | SURVIVES | high | cheap |
| 39 | B4-3 | Gerizim ×2 + Vespasian Cave missing from hoards.csv | NEW TO THE PROJECT | SURVIVES | high / medium | cheap |
| 40 | B6-3 | 1104 doubled; lamp 84 "393" | NEW TO THE PROJECT | SURVIVES | high (facts); low (importance) | cheap |
| 41 | C1a-2 | E-run F014 affine about 2 km off at Jerusalem; 3-point fix | NEW TO THE PROJECT | SURVIVES | high | cheap |
| 42 | C1c-2 | 1974 waterline table; GLO-30 about 5 m high | NEW TO THE PROJECT / KBUD | SURVIVES | medium / low | moderate |
| 43 | C2-1 | Mughâret Ekteif map position; no record | NEW TO THE PROJECT | SURVIVES | medium | cheap |
| 44 | C2-2 | Seven SWP XVIII features with no record | NEW TO THE PROJECT | SURVIVES | low | moderate |
| 45 | C3-1 | dup_of linker crosses publications (8 links of 4–38 km) | NEW TO THE PROJECT | SURVIVES | high | cheap |
| 46 | C3-2 | WBS:4287 "Lower Herodium" = fortress grid | NEW TO THE PROJECT | SURVIVES | medium | moderate |
| 47 | C4-1 | Price 2002 hand-dug 17 m shaft tested the 1990/1996 targets: negative | NEW TO THE PROJECT | SURVIVES (point 3 struck) | high | cheap |
| 48 | D1-2 | Abu Lahm: "NE of ʿAin es-Sultan" is wrong (NNW) | NEW TO THE PROJECT | SURVIVES | medium-high | cheap |
| 49 | D1-3 | OPEN_QUESTIONS R07 stale "Current" line (Kallai read) | NEW TO THE PROJECT | SURVIVES | high | cheap |
| 50 | E2-2 | Ḥorbat Devora road outside Itiner-e | NEW TO THE PROJECT | SURVIVES (corrected: report dates it Roman) | medium–high | cheap–moderate |
| 51 | A1-3 | CT10_FRS 7 fragments vs EDF seg 10 | NEW TO THE PROJECT (link only) | WEAKENED | high (content); low (significance) | cheap |
| 52 | A3-2 | Ten unmatched Cave/Tomb labels | NEW TO THE PROJECT (candidates) | WEAKENED | low | moderate |
| 53 | A4-3 | 38 voids; void 3 undocumented; no kokhim tomb | NEW TO THE PROJECT | WEAKENED | medium-high | cheap / needs PEF sheet |
| 54 | B1a-3 | SOA reports absent from HA 2005–2017 | NEW TO THE PROJECT | WEAKENED | high (corrected pattern) | cheap |
| 55 | B3-3 | Agathocles weight 205 vs 200; Sosibius 201 tension | NEW TO THE PROJECT | WEAKENED | medium / low | needs new data (INR 17) |
| 56 | B5-1 | Baker minute: test "on an actual piece" | NEW TO THE PROJECT (wording only) | WEAKENED | high (text); low (meaning) | needs new data |
| 57 | B5-2 | letters vs published chronology | NEW TO THE PROJECT (point 2 only) | WEAKENED | medium (2); low (1, 3) | needs new data |
| 58 | C1a-1 | Mishor Adummim earthworks 1974, gone by 1978 | NEW TO THE PROJECT | WEAKENED | high (change) / low (antiquity) | moderate |
| 59 | C1c-1 | Sites 117a/120 visible in 2023; new roads | NEW TO THE PROJECT | WEAKENED (TAG CHANGED) | medium (tracks) / low (identity) | cheap |
| 60 | C1c-3 | Site 139a grid at or below the 1968 shore | NEW TO THE PROJECT | WEAKENED | low | moderate |
| 61 | B3-1 | Heliodorus complex SC 126 not SC 57 in CIIP/IIP/Wikipedia | KNOWN BUT UNDER-DISCUSSED | SURVIVES | high / medium | cheap / BAR S2652 |
| 62 | B5-3 | Kuhn Sept–Oct 1953; cols VII–X | KNOWN BUT UNDER-DISCUSSED / NEW TO THE PROJECT | SURVIVES | high | cheap / new data for THLZ |
| 63 | C2-3 | Itiner-e omits two SWP roads; Dabbus milestone | KNOWN BUT UNDER-DISCUSSED | SURVIVES | high (gap) / low (Roman) | moderate |
| 64 | C4-2 | Qumran dump ERT: second unlabelled resistive body | KNOWN BUT UNDER-DISCUSSED / NEW TO THE LITERATURE | SURVIVES | low (feature real) | needs new data |
| 65 | D2-3 | Rock-cut entrances follow slope; no Temple preference | KNOWN BUT UNDER-DISCUSSED | SURVIVES | medium | cheap |
| 66 | C4-3 | Cave of Letters metal null only to 3.5 m; ERT debris 7–8 m | KNOWN BUT UNDER-DISCUSSED | WEAKENED | medium | moderate |
| 67 | D2-1 | Built doors E/S not W, "regardless of slope" | KNOWN BUT UNDER-DISCUSSED | WEAKENED | medium | cheap |

## Killed

- **E1-2 (Yehud, Ashkenazi Market: Early Islamic remains and a smelting kiln "never published").** R2 found ʿAtiqot 105 in the bucket (`atiqot/pdf/vol-105/iss-1/1893_*.pdf`). E1 had recorded it as missing. Jakoel 2021 publishes L808 as a metal-smelting furnace (Fig. 7) and the "scanty remains of an Early Islamic settlement" (Fig. 17). E1's own kill test is met.

## Merged

- **B1b-1 + B1c-2** → top-10 card 4. They report the same error class and use the same three-witness test.
- **A6-3 and B3-1** share only the Maresha IV renumbering (SC 57 → SC 126). B3-1 is the card for it; A6-3 cross-references it.
- **C2-3 and E2-2** do not overlap: E2's roads are in Galilee, the Golan, the Sharon and the Shephelah; C2's are on SWP sheet XVIII. Both show that Itiner-e carries the main routes and leaves out secondary roads.

## Corrections for the owner (project data; decide under AGENTS.md)

The swarm changed nothing in the project. These are errors or gaps in the project's own files that the cards document:

- `research/regional/water_systems/water.csv`:
  - Row LIT-E29-J15 (Hisham's Palace) is 4.3 km off (C1b-1).
  - `ASI-109/7/95-cistern` and `WBADB-S4146-cistern` are one site counted twice (B2-1).
  - The `dup_of` linker sends "Hirschfeld <year>, Site N" to ASI 108/2 (Hirschfeld 1985) even when the source is Hirschfeld 1983. It also matches six Kloner [101] rows to ASI-online record numbers. Results: Zawayat drops out, the Nuseib pool is counted twice, and 9 Hirschfeld 1983 rows carry a false "same site" note. See `scripts/build_survey.py` lines 277–286 (C3-1).
  - WBS:4287 "Lower Herodium" carries the fortress grid, which misplaces the end of the Artas–Herodium aqueduct and the Lower Herodium pools (C3-2).
  - The ASI 109/4 rows have the minus sign missing from their elevations (D2-2).
  - J19 (St Andrew's piscine) can now be placed to about 200 m (C1b-2; CMHL gives an independent point).
- `research/comparanda/hoards_full/hoards.csv` lacks both Gerizim hoards and the Vespasian Coins Cave crack cache (B4-3). They came into Drive after the catalogue was frozen. The Gerizim silver hoard would be the first `temple_related = 1` row; whether to re-run the test is the owner's decision.
- `research/assessments/entry29_jericho_pools/README.md`:
  - Line 490 says Meinardus pp. 183–184 are unread. They are in Drive as two untitled PDFs in `08/Unsorted source scans/` (A5-1).
  - Lines 148–151 say Plans 14, 15 and 23 were not located; line 643 of the same file says they were photographed on 21 Oct (D1-3).
- `avigad1954.md` lists pp. 74–75 as missing. They are frames 14 and 16 of the clip `IMG_0771.MOV` (A5-2).
- `research/OPEN_QUESTIONS.md` R07: line 197 ("current follow-up: Kallai pp. 172–173 unread") contradicts line 183, which records those pages as read on 19 Oct (D1-3).
- `registration/avigad1962_kidron_ossuaries_extracted.md` says "Serial No. XXX"; the page image says XXXI (B3, dead-end list).
- **Run E (31 Oct) georeference of HEXAGON 1974 frame F014:**
  - It is about 2.2–2.4 km off at Jerusalem, and about 520 m off even at Tell es-Sultan, its own anchor (C1a-2, R4).
  - A 3-point correction is in `C1a/F014_3point_affine.json`.
  - Anyone using run E's frames needs to re-register them locally first.
- **Entry 24 (Wadi Kuteif):** the project's `kuteif` point sits on the "Wady Ekteif" label. The Mughâret Ekteif rock-cut passage (Memoirs III p. 220) is on the SWP sheet about 2.4 km east, and no record lies within 567 m (C2-1). Its position is private.
- **Kh. Abu Lahm (Q24 / entry 31):** Mandate card 8751's "4 km NE of ʿAin es-Sultan" is wrong; the ruin is 2.2–3.2 km NW–NNW (D1-2).
- **Cave of Letters coding:** the metal-detector null reaches only about 3.5 m (for a drum-sized target), while ERT debris reaches about 6–7.5 m. The "no second metal deposit" coding should carry that depth limit (C4-3, as weakened by R5).
- **Qumran plateau:** Hadashot 117 report 126 (Price) records that the 1990/1996 deep "cave" targets were dug by hand to 17 m in 2002 and were natural stone lines (C4-1). The salvage records stop at S34–S36 and do not include it.
- **West Bank Hadashot coverage:** reports by the Staff Officer for Archaeology are almost absent from HA vols 117–128 (published 2005–2016). A Hadashot "silence" at a West Bank candidate in those years is a publication gap, not a negative search (B1a-3, as corrected by R2).

## Dead ends (merged across lanes; one line each)

- A1: Cuts 12–15 were not analysed; they exist only in Drive at 46–69 MB, too large for the connector. No ruling/guide-line search: C2 (31 Oct) showed line measurement fails on most frames. Cut 10 rivet count by eye: could not separate rivets from corrosion blisters. The raised flap on cut 16 is already in the USC catalogue.
- A1 side note withdrawn by R1: EDF's "grotte n° 8" is not an error (DJD III and Puech use "grotte 8 = 3Q").
- A2: The H&C 1994 photo inventory and page-register CSVs carry no captions, loci or dates (file lists only). About 39 Feshkha dates "1959" in the OCR are an italic-8 misreading of 1958. Caption parsing recovered only 175 of 538 caption starts. PEF P46–P48 cross-references off by one: trivial.
- A3: Full-sheet OCR of the Albright sheets misses many labels. The bucket's `reading/iaa_mandate/` has no text extractions. The 25 Mandate notes on caves/cisterns are about Jericho and the Judean Desert, not Jerusalem. One copy per sheet, so no edition-to-edition comparison is possible.
- A4: No published metres-above-sea-level value for Corbo's ±0.00 was found. The voids could not be matched against the plan scans, because the licence forbids extracting them. The HA 136 Sapienza report gives no levels.
- A5: Commons 512/517 mismatch: a catalogue slip. LoC 2019692525 title vs caption: LoC's own notes give both. NYPL 80365 is an engraving. The Temptation cable-car videos show nothing new. The unlabelled Nigro PDF in 99 Duplicates is Nigro & Yasine 2024.
- A6: Salome Fig. 16 caption is correct. Kloner 1978/1979: a bibliographic slip. Yechezkel 2024 U-Th dates: differences too weak. Cana 2025: nothing. City of David IV conflicts: already logged on 4 Nov.
- B1a: Word-list sweep (149 hits): routine or already published. The ʿEn Gedi coconut cave is already in the features table. Same-permit and same-place pairs: typos or bilingual names.
- B1b: Abu Ghosh revolt-coin hoard, ʿAkko tetradrachm hoard: published. 89 shared permits: multi-season digs or robbery-unit permits. Publication lag rises gradually, with no sharp break.
- B1c: The "unique/enigmatic" sweep: already discussed in print. ʿUyun Umm el-ʿAzam Syriac/Aramaic inscription: published. Peace Forest ossuary lid: already cited. The doubling of publication lag after HA 132 is explained by the COVID backlog.
- B2: Bar-Adon 56 and 120: no error. Hirschfeld 1985 site 8: only the code is wrong. Kloner 2003 [83/1] vs ASI 83/1: different numbering systems. Benjamin 1993 English list vs WBADB: agrees (the apparent gaps are OCR 2→9). JSP 8/9/10, SBF 36, Frumkin and SWP were not joined in this pass.
- B3: Avigad 1962 × CIIP I: the readings could not be compared (CIIP I blocked). The Cyrenaican names occur only in this tomb. The `CIIP_CPJ_names` sheet has mixed rows. ʿArāq Ḥāla: the CIIP and Zissu readings agree.
- B4: Wadi Ḥamam hoards agree with Leibner 2018. The Vespasian Coins Cave catalogue is consistent. Synagogue latest-coin conflicts are already published. Die links: not attempted (no die-level images).
- B5: The 1952 find date (14 vs 20 Mar) is already reconciled in DJD III. Rosalind Baker is already named in Lundberg & Zuckerman 2002. NYT 1952/1961 and Albright 1960: headline-only text, already covered. Browning and Brinkley: already covered in salvage records. Eisenman & Baigent 2000 is unread project-wide. Kuhn's roll diameters: his figure's OCR is broken.
- B6: The 2016 ch. 11–12 locus/element slips are already on `sandbox/methods`. 2016 lamp loci vs 1994: all agree. KhQ 426 and KhQ 878: explained. KhQ 1627 (A2): consistent in 2003. Magen 2018 and the 2019 volume: not cross-checked.
- C1a: RAF 1940s vs Esri over the whole area: too coarse. Automatic 1974-to-modern registration (SIFT, ORB, gradient matching) failed everywhere; controls must be picked by hand. Nebi Samwil demolition date: residual error too large.
- C1b: The whole 1945 sheet has been built over or levelled since 1945, so no ancient loss can be shown. Aqueducts cannot be told apart from the drawn contours. HEXAGON at ʿAqabat Jabr: covered by the camp.
- C1c: Automatic matching failed. A brightness-threshold waterline counted the Feshkha reeds as water (fixed). Bar-Adon sites 138a, 119, 129 and others: no clear structure visible. CORONA, Dec 1974, 1978, 1918 and ʿEn Gedi: not reached.
- C2: OCR of the 1940s tiles fails. Palmer squares (7 × 9 km) are too coarse for a join. WBADB has no Hisham's Palace row under any spelling tried. The Wadi Joreif Ghuzal hermitage is probably the ʿEin Abu Mahmud cave cluster.
- C3: Printed fortress elevations agree with GLO-30. The Ras Kunetra catchment fits. All inventory aqueducts with a destination run downhill. Springs and dams far from drainage lines, and reservoirs on summits: normal. Off-cliff caves: mostly known misprints, plus ʿAtiqot 41 Region X marl, which a 30 m DEM cannot see.
- C4: Freund 2004 vs Bauman fig. 6.5: palette only. ERT line numbering already in the S34 notes. Cemetery GPR graves, latrine and zinc coffin: already in the project. Magen's dumps were dug before the 2002 survey.
- D1: Gerizim locus P5178: no hit (already known). Tracker counts match. Mirrored tables are identical. Netzer & Garbrecht p. 372 arithmetic: already flagged.
- D2: Counting facings in 8 sectors gives false significance (surveyors round to N/E/S/W). Period subsets too small. Map references inside ASI texts vs online points: other places or grid-system swaps. H's language model: not fit for Aramaic or names. A2 registration: not attempted.
- D3: Same-site outliers over 4 km: real sub-sites or same-name places. North/east written in the wrong order: a convention slip. Five-digit truncations: trivial. The raw counts of 130 differences and 335 implausible references are parser artefacts; do not reuse them. Figure and plate cross-reference checks: not run (still open).
- E1: Rekhes Yeroḥam counts add up. Tel ʿEton heap numbering: one number dropped, too small. Leibner ch. 20: editorial slips only. The Leibner "m asl" values sit on a +100 datum (explained in ch. 1 n. 58).
- E2: Ossuary names × Ilan: too few names (about 6). Hellenistic hoards: too few (4). Milestones × Itiner-e: they agree. 139 HA reports dropped for EN/HE map references more than 2 km apart (includes Givati, HA 1377).

## Blocked inputs

- **Cuts 12–15 of 3Q15** (22 TIFFs, 46–69 MB): only in Drive folder `1K_Q5rKzL3dUwkb9saX4oiWbno9ayCiR4`, not in bucket `usc/`; too large for the connector. Remedy: run `hexcog2.py … extras` (Colab cell 4c) to add them to the bucket.
- **The 24 colour verso frames of 3Q15** (1988): in neither Drive nor the bucket; the USC preview links have expired (HTTP 403).
- **DJD III vol. I** (Drive `1knLGD17tvjrKvu6pMFkhYMsu6nj8l6G7`, 26.7 MB): over the connector limit and not in the bucket. Wright Baker's notes on pp. 203–210 are unread.
- **CIIP I.1** (Drive `1RNl4SwNvUF1XomCQ5N9Ze7WS4bMoGZb8`): reading returned only the front matter; download said "message from the server was too large". The 24.9 MB copy `126ct8RGvh91Nh4qHqHUWwqFsaqEus8R9` was not tried.
- **JSP 19** (Drive `1afKbqio94MQ1KaqChqBNw47IwfHejARy`): the connector returns text only to PDF p. 107. The coin and hoard catalogue is not reached, and the file is not in the bucket.
- **Humbert & Chambon reading PDFs** (Drive `1E7honPG4OiUFvQGRptCWwIFEAGL3Xkp8`, `1U4xvZ0WwUIwYyQzhlPn1vIbVnamEZwt0`, `1A97_Zanh50LuhHwBc0FTZB9Syt2Ph5Zj`; 55–87 MB): over the limit. The 1994 volume is not in the bucket `pdf/`.
- **Bucket `reading/iaa_mandate/2026-11-02/IAA_19623_ATQ_199a_…_638_scans.pdf`** (145 MB): not in `hexview.py pdfs`; not downloaded.
- **Drive `IAA_highres_combined_page_register.csv`** (`18dn750HpivWncVe-dIbZmaRtv-y7Ny60`, 907 KB): not read (connector).
- **Bucket `reading/04 Articles and chapters/`:** `gsutil ls` returned 403.
- **Not in the corpus:** Mizzi 2017 review; de Vaux 1973; Corbo 1981; Gibson & Taylor 1994; Baker BJRL 39 (1956); Kuhn THLZ 79/81; Lefkovits 1993 dissertation; the 2003 English edition of H&C 1994; Finkielsztejn INR 17 (2022); BAIAS 23 (2005, Moẓa); CIIP IV.1 (no text in the bucket); Frumkin et al. 2003; Jol et al. 2002; Strange 2006; Parry et al. 1998; Eisenman & Baigent 2000.
- **No text layer:** Bar-Adon 1989 (ʿAtiqot Heb. 9); Kloner & Zissu 2003; Amit–Hirschfeld–Patrich 1989 (Hebrew); ASI 1 Bar-Adon chapter.
- **Web:**
  - `hadashot-esi.org.il` Report_Detail pages are disallowed by robots.txt. Use the bucket `hadashot/pdf` prints, made 23 Oct 2026 with figures embedded.
  - `overpass-api.de`: connection reset through the proxy.
  - `publications.iaa.org.il` (ʿAtiqot 105): Cloudflare challenge. The bucket has vol. 105.
  - pnas.org: client error; PMC: reCAPTCHA. Europe PMC worked.
  - Commons and LoC APIs: HTTP 429.
  - The Wuppertal repository API returns HTML; the backup host works.
  - The old IAA permit register at `antiquities.org.il` now redirects; a Wayback fetch was not approved.
- **Tooling:**
  - `git grep` over all 86 branches times out. The orchestrator built `branch_only/` (1,876 files that exist only on branches) as a workaround.
  - `hexview.py` used `splitlines()`, which broke on U+2028 in `pages.jsonl`. Patched in the workspace copy only; the bucket `tools/hexview.py` is unchanged and should get the same one-line fix (`.split("\n")`).

## Notes on how the run was done

- **Bucket access:** used the read-only HMAC key the owner supplied in the session. The key appeared in the conversation, so rotating it is advisable.
- **Repository:** each lane branch adds only `research/sidequest_2026-11-06/<LANE>/`. Before every push, a script checked for images, files over 2 MB, the key and the owner's e-mail. No branch touches `main`, the ledger, ratings, PROGRESS_METRICS, ACTIVE_TEST, OPEN_QUESTIONS or atlas data.
- **Site protection:** coordinates of unrecorded features (A3, B2, C1a, C1c, C2, C3, D2) are only in the private products. Public cards use sheet + cell, survey + site number, or image ID + pixel window.
- **Web fetching flagged for the owner:**
  - D3 compared 31 live English Hadashot pages by curl. That site's robots.txt disallows agents; other lanes respected it.
  - B1a downloaded one IAA figure image (`hadashot.iaa.org.il/images//3472-5.jpg`); it is kept private.
  - The bucket prints of 23 Oct give the same evidence. The owner may drop D3's live-page column (`ha_mapref_errors.csv`) if preferred.
- **Licences:**
  - The Holy Sepulchre model (Siegel 2026, DOI 10.57899/bkf2-pv55) is CC BY-NC-SA 4.0. Only measured numbers are public. The source-plan scans inside it are excluded from reuse and were not extracted.
  - USC/WSRP, Allegro DQCAAS and IAA images stay private.

## Private products

There are 123 image files (crops, panels, page photos) plus the coordinate CSVs and notes, about 97 MB in all, under `private/<LANE>/`. They were packed as one zip, `sidequest_2026-11-06_private.zip`, and delivered to the owner as a download, for Drive `10 Side-quest finds/2026-11-06/`. The Drive connector cannot upload binary files of this size from the session. Nothing from them is in the repository.
