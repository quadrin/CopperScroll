# Side-quest round 2, lane B2: surveys against each other (6 Nov 2026)

Builds on B2 and B2b (round 1) and on reviews R4 and R8. Round 1 worked from the sandbox CSV (`branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv`). That file drops the excavator, comment and bibliography columns and the whole **"License List"** sheet. Round 2 used the original public workbook, `WBADB_data1.xlsx` from https://emekshaveh.org/en/wp-content/uploads/2020/08/WBADB_data1.xlsx (SHA-256 begins `3db734cdc1a7`, the same file `caves_entry25/coded/wbadb.py` cites). Its "License List" sheet is the Staff Officer for Archaeology (SOA) permit list for 1968–2007 (1,177 permits). A second witness that no earlier lane used comes from the Hebrew tables of contents of HA 97–108 and ESI 19–20. They print the SOA permit number after each West Bank report as "(קמ״ט NNN)". 52 such entries were extracted and joined to the register (`ha_toc_soa_licences_x_register.csv`).

**Note on IDs.** Workbook "Excavations N" numbers are not the sandbox `WBE:` numbers. For example, Kh. Qumran is Excavations 754 in the workbook and WBE:748 in the sandbox. Each card gives both.

Data in this folder:
- `wbadb_licence_spread_review.csv`: every WBADB row whose licence also sits on another row more than 2 km away (49 licences, 184 rows), with the register entry, the excavator and a class. Coordinates are left out. They are all published WBADB points and are in `private2/B2/licence_spread_vs_register_full.csv`.
- `ha_toc_soa_licences_x_register.csv`: the 52 HA/ESI table-of-contents SOA permit numbers matched to the register.

---

FIND CARD
Title (one line): The SOA permit list and WBADB put "Qumran, Cave Q3" (licence L-399/1986), which is 3Q, the Copper Scroll cave, on the shore plain 2.95 km SE of 3Q; the project's cave inventory counts it as a separate cave
Round-1 link: B2b dead end "44 licences on rows > 2 km apart, not reviewed" (now reviewed, card 3); same error class as B2b-3
Lane: B2
What is odd (2–4 sentences): The register gives licence L-399/1986-0 to two entries. One is "Cave 1 and Cave 2" (Joseph Patrich, HUJ). The other is "Qumran, Cave Q3" (excavator NDA) at 195500/127600, 1.85 km due east of the register's own Kh. Qumran point (193650/127650). That point is on the flat shore plain, not in the cliff. ESI 6 (1987) p. 68 reports: "In April 1986 an excavation was carried out in Cave Q3, situated 2 km north of Kh. Qumran. This is the cave in which the Copper Scroll was found during the 1952 survey. At that time it was given the number 8". Patrich directed it, with Vendyl Jones's volunteers (p. 69). So the 1986 licence, the excavator and the label all point to 3Q. The register's point is 2.95 km from the project's digitised 3Q point (caves.csv DJD3:8, 193486/129756), at a bearing of about 137°. It looks as if the "2 km north" went into the easting instead of the northing. WBADB copies the point into Excavations 756 "Cave Q-3" (sandbox WBE:750), with excavator "Vendyl Jones ('78)", a date that does not fit a 1986 licence. Its "Cave 1 and Cave 2" row (Excavations 713, WBE:707) has the comment "L-399 was also used for Qumran Cave Q3 excavations".
Evidence (exact sources: file path / page / figure / frame / coordinates): Workbook sheet "License List", rows L-399/1986-0 (two entries) and L-405/1986-0. Sheet "Excavations", Index 756 and 713. ESI 6 (store `ESI-06-1987-…-a3491691`, PDF pp. 78–80 = printed pp. 68–70, Fig. 29 "Qumran. Copper Scroll cave"). Project: `research/regional/caves_entry25/caves.csv` rows `WB:E756` (coded as a cave, `coord_ok = yes`, `possible_duplicate_of = A41:X/35; DJD3:8`) and `DJD3:8`. `caves_entry25/coded/wbadb.py` line 113 ("Cave Q-3 (Jones 1978) … The printed point lies on the plain east of Qumran (doubtful)"). `duplicates.csv` lines 17 and 34 (flagged on the label alone). `AMENDMENT_1.md` item 16 ("the conflict is reported, not resolved").
Literature check (queries run, result, tag): Web: "Cave Q3 Qumran Patrich 1986 Copper Scroll cave … database coordinates" found only general pages on the Copper Scroll and the Qumran caves (Wikipedia and mirrors). No source discusses the register or WBADB point. Repo main and `branch_only`: "L-399" appears only in the WBADB data rows, and "195500" only in data rows and in caves.csv. The project knew the point was doubtful and the label clashed. It did not have the licence link, which settles the identity. Tag: **NEW TO THE LITERATURE** (the register/WBADB position error); **NEW TO THE PROJECT** (the identity WB:E756 = DJD3:8, not X/35).
Why it might matter: The entry-25 cave inventory holds a phantom cave on the plain, and the label flag leaves open a link to X/35 (Patrich and Arubas Cave 13, the balsam-juglet cave). The licence evidence goes against that link: X/35 was dug in 1988 and in 1993–94 under L-640. Anyone who plots the WBADB or SOA register points (the sandbox inventory, the landscape map, the imagery-gap points) puts the Copper Scroll cave's 1986 excavation 2 km out on the plain.
ARGUMENT (Copper Scroll): this does not touch any reading or identification. It only cleans 3Q's own record. The 1986 re-excavation reached the floor and found that the roof had fallen long before the jars were set in rock cavities and shallow recesses (ESI 6 p. 69). That is the published basis for the "geniza, not emergency" reading of 3Q. In the corpus it now has one cave row, not two.
How to confirm or kill it (with data in hand, or what is missing): Kill it if a second 1986 cave dig "Q3" east of Qumran can be found. ʿAtiqot 41 records no cave in the plain at that point, and caves.csv has none within 1 km. The IAA archive file for licence 399 would settle it (not requested: AI only).
Confidence: high (point error; licence and year); medium-high (identity, which rests on ESI 6 plus the shared licence)
Touches the Copper Scroll? yes: the record of 3Q itself; no identification is affected.

---

FIND CARD
Title (one line): HA 106 prints SOA licence "837" for Porat's March 1995 Qumran survey, a number not issued until 1999; the register keeps it as a ghost permit, WBADB moves it onto the Kh. Qumran site point, and the Qumran licence field is cut off at 255 characters
Round-1 link: new (from the licence review)
Lane: B2
What is odd (2–4 sentences): HA 106 (1996), Hebrew table of contents p. 179, has "חורבת קומרן (קמ״ט 837)". The report (p. 129; English ESI 18 p. 84, "Horbat Qumran", Yosef Porath) describes a survey and trial dig in **March 1995** at map ref. 19325/12620: a stone-lined water channel running north from a now-dry spring to cleared and terraced fields, with sherds of the 1st c. BCE–1st c. CE. In the register the permits run in order: L-733 (Nov–Dec 1995), L-749 (Aug 1996), L-773 (1997). So 837 cannot be a March 1995 permit. The register has **L-837/1999-0 twice**, once as "Kh. Qumran, Yosef Porat" at exactly 193250/126200 (the HA point) and once as "Miẓpeh Jericho" (NDA). The "1999" was probably inferred from the number. WBADB then files 837 on its Kh. Qumran site row (Excavations 754 = WBE:748, at 193650/127650, 1.45 km away). That row's comment says "L-837 was issued to another site: Mizpeh Jericho", and the 1995 work is missing from its excavator list. The register has two NDA permits of 1994, L-679 and L-693, "The Springs Area: Qumran and Feshkha", at 193300/126300. That is 110 m from Porat's point, and Porat's report says his dig followed a preliminary survey. The same Kh. Qumran row's licence string is exactly 255 characters long and ends in "L-9". It is the only WBADB licence field at the 255 limit, and its tail is lost; the register lists L-991/2004-0 for Qumran after L-990. Round 1's licence scan read that "L-9" as Herodium's L-9/1968.
Evidence (exact sources: file path / page / figure / frame / coordinates): HA 106 store `HA-106-1996-…-35808954`, PDF p. 181 (TOC, read on the page image) and PDF p. 131 (report). ESI 18 store `ESI-18-1998-…-21038da2`, PDF p. 101. Workbook "License List" rows L-837/1999-0 (×2), L-679/1994-0, L-693/1994-0, L-733/1995-0, L-749/1996-0, L-773/1997-0, L-991/2004-0. "Excavations" Index 754 (licence field length 255) and 408 (Mizpeh Jericho, WBE:402). `ha_toc_soa_licences_x_register.csv` row HA-106 p181.
Literature check (queries run, result, tag): Web: "Porath 1995 Horbat Qumran water channel survey Qumran marsh ESI 18" found general Qumran water-system pages (cojs.org "Water Channel at Qumran", Orion "Aqueducts, Basins, and Cisterns") and nothing on the licence. Repo: "19325/12620" appears only in `haesi_features/phase3_2026-10-11` (the feature is known to the project); "L-837" and "837/1999" appear only in WBADB rows. Tag: **NEW TO THE LITERATURE** (the anachronistic permit, the ghost register entry, the truncation).
Why it might matter: An IAA/SOA archive request for "licence 837" would retrieve the Mizpeh Jericho file, not Porat's Qumran–Feshkha channel. WBADB users lose the 1995 point south of the khirbet and lose the 2004 Qumran licence. The channel is a Second Temple irrigation feature on the Qumran–Feshkha strip. Its record path matters to the project's water lanes.
How to confirm or kill it (with data in hand, or what is missing): The anachronism and the truncation are fixed facts. That 679 or 693 is Porat's true licence is an inference (both are NDA). The IAA archive would settle it. Kill it if the SOA numbering was not chronological in 1995–99. Against that: the register's 1,173 dated entries never put a higher number in an earlier year (0 inversions when sorted by number).
Confidence: high (anachronism, ghost duplicate, truncation); low-medium (679/693 as the real permit)
Touches the Copper Scroll? maybe: Qumran-area water installations; no entry is argued.

---

FIND CARD
Title (one line): The 49 WBADB licences on rows more than 2 km apart, reviewed against the SOA register: 33 are legitimate, 7 are duplicates inside the register itself, and the B2b-1 and B2b-2 errors are already in the register; JSP 10 re-read: (a)–(c) confirmed, plus a new ITM digit swap at Carmel
Round-1 link: B2b-1, B2b-2 (and the open item "44 licences never reviewed one by one"; "three JSP 10 wrong-place digs not re-read on the English photos")
Lane: B2
What is odd (2–4 sentences): The results by class (`wbadb_licence_spread_review.csv`):
- 17 multi-site permits whose sub-numbers (-0/-1/-2) match the register (the 1968–83 SOA practice).
- 16 area or cluster permits, or WBADB survey rows that collect nearby excavation licences.
- 7 permits that the register itself gives to two separate sites (L-38 Twin Cave / Kh. Muqaddam; L-77 Kypros / Hyrcania; L-248 Kh. Rabud / Kh. el-Ḥamam; L-384 Kh. Ḥablata / Kh. Nisieh; L-387 Qarn Ṣarṭaba / Hyrcania; L-493 ×3; L-512 Abu Shinja / Kh. Ṣuṣye).
- 1 WBADB-only attribution (L-358 on Qaṣr ʿAli).
- 1 known conflation (L-474).
- Cards 1 and 2.
- The B2b cases.

New on the B2b cases:
- **L-733.** The register lists L-733/1995-0 for both Baʿal Ḥaẓor and Mattityahu (north), and -1 for Mattityahu (NE), as well as L-773/1997-0 for Mattityahu (north). So the error R8 placed in WBADB's site rows comes from the register.
- **L-959.** The register entry "Kh. Abu Musarraḥ; North of Kh. Shuweikeh" has X/Y = 181000/132100, which is JSP 10's wrong point (B2b-1), while its own Location column reads 177300/137300. JSP 9 English p. 46* (store PDF p. 146) prints the same "License No. 959" for Peleg's March 2003 dig north of Kh. Shuweikeh (ITM 20310/69455), 62 km away.

The re-read of the full English photos confirms B2b-2:
- (a) p. 8*: Beitar ʿIlit, ITM 20972/62250, IOG 15972/12250, April 2002, licence 892.
- (b) p. 17*: Carmel, January 2002, licence 936.
- (c) p. 31*: "near Khirbet Beit Saḥur", ITM 22279/62275, IOG 17282/11228, July 2002, licence 951. The register calls it "Cave - Shedma".

New misprint at Carmel: "ITM 52974/21743; IOG 09274/16743". The IOG (northing first) converts to ITM N 59274, so the printed ITM northing has its 9 and 2 swapped.
Evidence (exact sources: file path / page / figure / frame / coordinates): Workbook "License List" (rows for each licence; see the CSV). Drive JSP 10 photos `2-eng p08-09 … (IMG_1306).HEIC` (1WWOTHMQ941R-VOAdDyeXGky_uZxbtBD6), `2-eng p16-17 … (IMG_1302).HEIC` (19mBEQJQS6_RR7QLLPxtUVjogcnguMzFE), `2-eng p30-31 … (IMG_1295).HEIC` (1fucNy6AfeencXqLEl6ueR7cnG_jTumGO); decoded copies in `private2/B2/jsp10/`. JSP 9 store `01-JSP9-…-e1745a0a` PDF p. 146.
Literature check (queries run, result, tag): Round 1's WBADB-errata searches (no errata) apply. Repo: "L-959", "L-733" appear only in data rows and in the round-1 cards. Tag: **NEW TO THE PROJECT** (the classification; the register as the source of the B2b errors); **NEW TO THE LITERATURE** (the Carmel ITM digit swap; licence 959 printed for two digs in JSP 9 and JSP 10).
Why it might matter: It closes the round-1 open item. Only 2 of the 49 licence spreads (cards 1 and 2) are new position or identity errors. The rest are register practice. It also shows that WBADB's "License List" is not an independent witness against JSP 10, because the B2b errors are in it too.
How to confirm or kill it (with data in hand, or what is missing): Every row can be checked in the workbook. Which of the two L-959 digs carries the misprint is open: JSP 10 Hebrew p. 40 (R8) gives 959 for Abu Musarraḥ, and JSP 9's Hebrew pp. 11–21 were not read.
Confidence: high
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): JSP 9 × SOA register (a new join): 17 licences agree on site and grid, but the Shaked (west) field tower's ITM reference was built by adding the ITM offsets to a northing-first IOG, so it points into Jordan
Round-1 link: new (the JSP 8/9 join B2b left undone)
Lane: B2
What is odd (2–4 sentences): JSP 9 (*Excavations and Discoveries in Samaria*, 2009) prints a licence and a double map reference in its English summaries, like JSP 10. Joining its 17 legible licences to the register (L-849, 853, 864, 867, 869, 903, 909, 914, 959, 960, 963, 964, 967, 971, 1040, 1067, 1088) gives the same site and the same grid in every case, within rounding. Apart from L-959 (card 3), one reference fails. "A Field Tower to the West of Shaked" (Aizik and Peleg, p. 45*, licence 869, July 1999) gives "ITM 25990/66450; IOG 20990/16450". The IOG is northing first and matches the register (164500/209900). The correct ITM is 21450/70990. The printed ITM is IOG northing + 5,000 and IOG easting + 50,000: the conversion offsets were added to the swapped pair. Read as printed, it falls about 9 km east of the Jordan.
Evidence (exact sources: file path / page / figure / frame / coordinates): JSP 9 store `01-JSP9-Excavations-and-Discoveries-in-Samaria-indexed-e1745a0a`, PDF p. 155 (= English p. 45*, photo IMG_1445), read on the page image. Register row L-869/1999-0. The other 16 pairs are in the text layer, PDF pp. 145–160.
Literature check (queries run, result, tag): Repo: "25990/66450" 0 hits; "Shaked" appears only in data rows. No errata for JSP 9 found (web, round-1 queries). Tag: **NEW TO THE LITERATURE** (minor misprint).
Why it might matter: The reference is cheap to correct for anyone who digitises JSP 9. With JSP 10 (B2b), it shows the JSP volumes' references are reliable apart from a few transcription slips. Each slip can be found by checking the ITM−IOG offset (50 km E, 500 km N).
How to confirm or kill it (with data in hand, or what is missing): The Hebrew p. 195 (not read) should print the same pair. The offset arithmetic is enough on its own.
Confidence: high
Touches the Copper Scroll? no

---

## Dead ends

- HA/ESI SOA-permit join beyond cards 1–2: 46 of the 52 TOC numbers agree with the register. Name-only differences: HA "Adam" = Kh. et-Tinat (532); "Kh. Samara" = Ras el-Lubbeid (508); "Kh. Kafr Qaraʿ" = El-Ghars (479); Kh. Kurqush and Ariʾel both 509 (the register says "Kh. Kurkush (Ariel, Industrial Zone)"). Unresolved: HA 101–102 TOC gives 456 to Har Adar (dug May 1991), while the register gives it to Kh. Khureitun (1989). The TOC image was not checked. "941" (el-Mughayir survey) is probably OCR.
- L-493: HA 97 gives it to the "Ancient road in Samaria" and HA 104 to the Map of Qalya survey (Map 109/5, Shion 1992–93). The register lists it three times, including an Avraham Eitan Iron II fortress point at 192200/139600. HA 104 p. 80 gives 19220/13960 as a 30-dunam site "found by Y. Magen (Kardom 28–30)" and treats Eitan's Vered Yeriḥo building as a different site. Too tangled to settle without Kardom 28–30 or HA 82.
- L-474 (Kh. Qumran vs Wadi Murrar): HA 100 TOC gives 474 to the ʿEin Abu Maḥmud caves only. This is already noted in `caves_entry25/coded/wbadb.py` (E519). WBADB "Cave Q-9" (L-481) sits at the khirbet, while HA 100 p. 55 puts Patrich's caves at 1935/1310; also already noted there (E760).
- L-38 Twin Cave / Kh. Muqaddam, L-77 Kypros / Hyrcania, L-387 Qarn Ṣarṭaba / Hyrcania (Meshel 1985), L-248, L-384, L-512: the register itself has the duplicate, and the WBADB comments say so. The corpus cannot show which entry is right.
- JSP 8 (Gerizim II): no licence numbers or map references in the text layer. A single-site volume, so nothing to join.
- SBF 36: no licences or map references (the only "IOG" hits are OCR coordinate noise). Its articles are syntheses, so no key.
- SWP Memoirs (Palmer squares): no key finer than 7 × 9 km (as C2 found). Not joined.
- ESI 18 English "Horbat Qumran" report prints no licence, so it cannot test the HA 106 "837".

## Blocked inputs

- None hard-blocked. The WBADB workbook was fetched from its public URL to `scratch/B2r2/dl/` (not committed; the hash matches the project's). JSP 9 Hebrew pages and the HA 101–102 TOC image were not read (budget). The IAA/SOA archive files for licences 399, 679, 693 and 837 would settle cards 1–2 but are an archive request (out of scope).

## Reproducibility

Scripts are in `private2/B2/scripts/`: `lic_spread.py` (sandbox CSV) and `lic_vs_register.py` (workbook; run `python3 -I lic_vs_register.py OUT.csv`). The HA TOC extraction is a regex for "קמ״ט NNN" over the store text layers of HA 93–108, HA-ESI 109–113 and ESI 1–20 (`hexview.pdf_pages_text`). Distances are in OIG metres.
