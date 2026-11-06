# Side-quest E1, round 2: random deep read (6 Nov 2026)

Lane E1, round-2 worker. Six new documents, drawn with the seed string "2026-11-06-r2" (procedure under "Seed / reproducibility" at the end). Every drawn file could be read, so there were no redraws. Five draws are Hadashot Arkheologiyot (HA-ESI) reports and one is a *Cathedra* article on the Copper Scroll (draw 5). Following ROUND2.md, I also extended the two round-1 E1 cards that survived:
- E1-1 (Giv'at Avni): extended into a check of every HA report;
- E1-3 (HA DOIs): extended with a full Crossref harvest.

Every map reference below belongs to a published survey or excavation; none is an unrecorded feature.

Round-1 E1 status, from review R2: E1-1 SURVIVES (Fig. 2 settled it); E1-2 KILLED (ʿAtiqot 105 publishes both the Early Islamic phase and the smelting kiln); E1-3 SURVIVES, to be reframed as a defect in the Crossref records rather than in the DOI string.

---

FIND CARD
Title (one line): Eshel & Safrai (*Cathedra* 103, 2002) convert the Massekhet Kelim preface date AM 3331 to "373 BCE"; the correct value is about 431/430 BCE. The plaques that are the preface's only witness are now argued to be modern forgeries, which the project's Koḥlit dossier does not record.
Lane: E1
Round-1 link: new (draw 5)
What is odd (2–4 sentences):
- Eshel & Safrai quote the preface that Milik read on the Beirut marble plaques of Massekhet Kelim ("Ein Kaḥal … in Mount Carmel", the basis of Milik's Carmel identification of כחלת). They date it "שנת שלשה אלפים ושלוש מאות ושלושים ואחד ליצירה" and write: "on the count accepted today, based on Seder Olam Rabbah, 3331 to Creation is 373 BCE".
- On that count AM 1 begins in 3761 BCE, so AM 3331 is autumn 431 to autumn 430 BCE. That is 7 years before the rabbinic date of the First Temple's destruction (AM 3338, 423/422 BCE).
- "373 BCE" is not that date under any standard reckoning. Under the rabbinic chronology it falls inside the exile, after the destruction and before the rabbinic Second Temple date (AM 3408).
- Separately, E. Dugan (BAR Summer 2023, sidebar "The Mystery of the Missing Plaques") argues that the lost Massekhet Kelim plaques were probably modern forgeries. They were near-twins of the "Ezekiel plaques" in the Ben-Zvi Institute, which Y. Schwartz (MA thesis, Ben-Gurion University, 2021) showed to be "modern forgeries, crafted in Syria in the early 20th century".
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Drive `01 Copper Scroll and DSS – editions and studies/Eshel and Safrai – אילו אוצרות נרשמו במגילת הנחושת [JSTOR capture].pdf` (ID 153PPbwQA8dqpQrLPXe6anEYoc2wePS1d). *Cathedra* 103 (Nisan 5762), pp. 7–20, n. 66 (printed p. 19). Text layer read with the Drive connector. The year is printed twice, once in words and once as "3331".
- Conversion: 3761 − 3331 = 430. The rabbinic destruction date AM 3338 = 422/423 BCE is given at https://en.wikipedia.org/wiki/Missing_years_(Jewish_calendar).
- Forgery: https://library.biblicalarchaeology.org/sidebar/the-mystery-of-the-missing-plaques/ and its endnote 2 (https://library.biblicalarchaeology.org/endnote/endnote-2-the-mystery-of-the-missing-plaques/), citing Schwartz, *The Riddle of the Ezekiel Tiles*, MA thesis, BGU 2021 (Hebrew). Main article: Dugan, "Jerusalem's Temple Treasures: Where Did They Go?", BAR Summer 2023.
- Project: `research/agent_review_2026-10-07/wave2/W2A_kohlit_dossier/REPORT.txt`, entry P04 "Milik 1962 … Basis: the Beirut plaque / Massekhet Kelim". The dossier records only Zissu's "suspect".
Literature check (queries run, result, tag):
- Web: "Treatise of the Vessels Massekhet Kelim Carmel 3331"; Milik RB 1959 "Notes d'épigraphie" plaques 3331; the Hebrew "מסכת כלים כחל כרמל 3331"; "Tractate Keilim 3331 / 373 BCE Eshel". No publication converts or discusses the 3331 date.
- The 2015 English reprint (Eshel & Safrai, "What Treasures are Listed in the Copper Scroll", in Tzoref & Selavan eds, *Exploring the Dead Sea Scrolls*, JAJSup 18, pp. 113–129; Orion record https://orion-bibliography.huji.ac.il/node/69474) could not be read, so it may correct the date.
- Repo main and branch_only: no "3331"; no "Dugan", "Ezekiel plaque" or "forger" in any Copper Scroll file.
- Tags: the date error is **NEW TO THE LITERATURE (provisional, until the 2015 reprint is checked)**; the forgery argument as it bears on Milik's Koḥlit is **NEW TO THE PROJECT**.
Why it might matter:
- The only text that puts כחלת on the Carmel is this preface, and its only witness is two lost plaques that Milik alone saw.
- The corrected date makes the preface agree with the First Temple hiding story it introduces.
- The forgery argument removes the witness altogether.
How to confirm or kill it (with data in hand, or what is missing):
- (1) Read the 2015 English reprint, p. 127 or nearby. The date part dies if the reprint already prints about 430 BCE.
- (2) Read Milik, RB 66 (1959) 567–575 for the exact wording of the year on the plaque. The connector text gives only Eshel & Safrai's quotation. The original is not in the corpus.
- (3) For the forgery claim, Schwartz 2021 would be needed. It is not in the corpus.
Confidence: high (the arithmetic); medium (that no one has corrected it); medium (the forgery argument is Dugan's, from the Ezekiel twin, not a test of the Kelim plaques themselves)
Touches the Copper Scroll? yes (entries 4, 11, 15, 19, 60: Koḥlit, via Milik's Carmel candidate)

ARGUMENT (separate from the evidence):
- Among the Koḥlit candidates in W2A, Milik's Carmel (ʿEin es-Siah) rests on nothing except the plaque preface. If the plaques are early-20th-century work, Carmel has no ancient witness. It should then fall from "rejected by most" to "no evidential basis". That is a modest change, since almost no one holds it now.
- The other candidates (Zissu's ʿEin Samiya, Puech's Tell es-Sultan reading, the Qumran-area proposals) are neither helped nor hurt directly.
- The date points the same way but is weaker. In the rabbinic count, AM 3331 is about Zedekiah's 4th year, the year of Jer 28:1–6 (Hananiah promises that the Temple vessels will return) and Jer 51:59. A modern forger working with the traditional *luaḥ* would plausibly choose such a year. This is a reason for suspicion, not a test.

---

FIND CARD
Title (one line): A within-report check of all HA reports finds three more Giv'at Avni-type errors: the Lahav Forest survey's own map reference lies about 2 km south of all 48 of its sites, Har Avihu stone pile 21 is printed 3.3 km north of its dig, and Oron B site 53 is printed 9 km south of its neighbours
Lane: E1
Round-1 link: E1-1 (Giv'at Avni), extended to the whole corpus
What is odd (2–4 sentences):
- I compared the general map reference in each English HA report's opening with every later sub-feature reference in the same report. There are 646 flags in 73 reports; most are legitimate (multi-site or linear surveys, cited sites). The cleanest new cases follow.
- (1) **Lahav Forest survey** (HA 124, id 2162). The general box "1860–80/5835–65" (NIG 186000–188000/583500–586500; the Hebrew is identical, "18600-800/58350-650") lies south of Kibbutz Lahav. But the text says "northwest of Qibbuz Lahav", and all 48 site references fall at N 588276–588856, 1.7–2.3 km north of the box. 47 of them lie at E 185612–186233, about 1.8 km WNW of the kibbutz (OSM 31.3794N 34.8701E = ITM 187640/587540). So the general reference is wrong (the northing is probably "5882–9"). Site 1's easting 188114 is probably a slip for 186114: it lies 2 km east of the other 47 sites, which run along E 185612–186233. The English drops a digit of site 32's easting ("18574"; the Hebrew has 185747).
- (2) **Nazareth, Har Avihu** (HA 128, id 24974). "Stone Piles 21, 39, 45, 46 (map refs. 227352/739956, 226877/736114, 226751/736146, 226742/736118)". Pile 21 is 3.3 km north of the dig box 225933–227422/735867–736651. The Hebrew is the same. Reading 735956 puts it inside the box, by its sister piles.
- (3) **Oron survey B** (HA 125, id 5449). Site 53 "193940/520171" sits between sites 52 (194008/529188) and 55 (194450/529229), so 520171 is very probably 529171: one digit dropped, 9 km off. In addition, 34 of the 43 site references lie outside the report's own general box "19265-379/52793-988". Sites run east to E 194688, and the box ends at 193790.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Bucket `hadashot/derived/hadtext_pdftotext.tgz` (extracted copy `scratch/B1b/txt/hadtext/`):
  - `en/vol-124/02162_lahav-forest.txt` (opening; sites 1–48; l. 77 site 32), `he/vol-124/02162_lahav-forest.txt` (opening; l. 65 "185747/588634");
  - `en|he/vol-128/24974_nazareth-har-avihu.txt` ("Stone Piles 21, 39, 45, 46");
  - `en|he/vol-125/05449_oron-survey-b.txt` (sites 52–55).
- Script `subref_scan.py`; all flags `ha_subref_flags_all.csv`; the card cases with distances `ha_subref_vs_general_box.csv` (this folder).
Literature check (queries run, result, tag): no erratum found for these reports on the web or in the corpus. Repo main and branch_only, and D3's `ha_mapref_errors.csv`: none of ids 2162, 24974 or 5449 is listed. D3 compared English with Hebrew and with same-site medians, not a report with its own box. **NEW TO THE LITERATURE** (small source-level slips; the Hebrew agrees in all three).
Why it might matter:
- Any gazetteer that places HA surveys by their opening reference puts the whole Lahav survey about 2 km south of where it was.
- The check costs one script and catches errors that bilingual and median checks miss, because the error is printed the same way in both languages.
How to confirm or kill it (with data in hand, or what is missing):
- Open Fig. 1 of 2162 (embedded in `hadashot/pdf/en/vol-124/02162_lahav-forest.pdf`) and read the survey area against the grid. The Lahav case dies only if the map shows the area south of the kibbutz, which the 48 site references and "northwest" both contradict.
- For 24974 and 5449, the plans (Figs. 1–2) show whether pile 21 and site 53 sit with their neighbours.
- I did not open the figures.
Confidence: high (Lahav, Oron site 53); medium-high (Har Avihu pile 21)
Touches the Copper Scroll? no (northern Negev and Lower Galilee)

---

FIND CARD
Title (one line): Crossref holds 9,718 HA-ESI records. In 9,525 of the 9,526 legacy records (10.69704) the authors' institutions were deposited as authors ("Israel Antiquities Authority" in 9,348), and every legacy record has no volume. The 192 new records of 2026 (vol. 138, 10.70967/1565-5334.*) are clean, and the legacy records were never re-deposited.
Lane: E1
Round-1 link: E1-3, extended (R2's reframe tested)
What is odd (2–4 sentences):
- A full Crossref harvest by ISSN 1565-5334 (6 Nov 2026) returns 9,718 records:
  - 9,526 legacy DOIs `10.69704/jhaesi.116.2004.<id>` (4,834 English, 4,692 "-he"; 4,838 distinct ids), all with `volume: null`;
  - 192 records of 2026 under a new scheme `10.70967/1565-5334.<n>`, with `volume: 138`.
- In the legacy records the affiliation was put in the author list. The 109 such "authors" include "Israel Antiquities Authority" (9,348 records), "University of Haifa" (69) and "Tel Aviv University" (26). Most legacy records (9,523) therefore have two `sequence: first` authors.
- The 2026 records carry the institution correctly in `affiliation` and have no organisation authors (0 of 192).
- There is also a record for the bare DOI `10.69704/jhaesi.116.2004` titled with the journal's name. This confirms R2's view that "116.2004" is a fixed journal-level token, not a wrong volume.
Evidence (exact sources: file path / page / figure / frame / coordinates): https://api.crossref.org/journals/1565-5334/works (cursor harvest, `select=DOI,volume,author,issued,title`, 10 pages, 6 Nov 2026). Tallies in `crossref_ha_org_authors.csv` (this folder). Example: 10.69704/jhaesi.116.2004.2124 has authors [IAA (first), Sonntag (first), IAA, Paran]. The new-scheme example 10.70967/1565-5334.1098 has authors פרץ, אבנר with affiliation רשות העתיקות.
Literature check (queries run, result, tag): web search for "10.69704/jhaesi.116.2004" and for HA-ESI Crossref metadata found nothing. Repo: only `research/regional/haesi_features/README.md` l. 116 mentions the DOIs. **NEW TO THE LITERATURE** (a metadata defect, quantified; the 2026 fix and the journal-DOI record are new to the project).
Why it might matter:
- Reference managers, OpenAlex/Scopus-type indexes and citation counts drawn from Crossref credit the IAA (or a university) as first author of about 4,800 reports and give no volume.
- The fix exists for vol. 138 but was not applied backwards, so the legacy records will stay wrong unless they are re-deposited.
- For the project: take volume and date from `reports_metadata.csv`, never from Crossref.
How to confirm or kill it (with data in hand, or what is missing): re-run the harvest (2 minutes). It is killed if Crossref shows the legacy records re-deposited with affiliations moved out of `author`.
Confidence: high
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): Khirbat ʿAmra (HA 125, id 4363) uses the wall numbers W20, W21 and W22 for two different sets of walls, in Area A (Sq F6) and Area B (Sq F5), on its plans as well as in its text. The F5 plan's phase colours contradict the text for W8 and W9.
Lane: E1
Round-1 link: new (draw 2)
What is odd (2–4 sentences):
- In the text, Area A Sq F6 has three Mamluk sub-phase walls: W21 (earliest), W22 (middle) and W20 (latest).
- Area B Sq F5, on the lower hillside, has "a room delimited by three walls (W20–W22)".
- Both plans print W20, W21 and W22 (Fig. 5 for F6, Fig. 15 for F5). So one number stands for two walls in three cases, while W2–W4, W15 and W17–W19 appear nowhere. The Hebrew text has the same numbers.
- On Fig. 15, W8 is coloured "Ottoman" and W9 "Late Mamluk". The text builds W8 in the latest Mamluk phase ("a wall was built (W8)"), which "continued to be used" in the Ottoman period, and introduces W9 only in its Ottoman section.
Evidence (exact sources: file path / page / figure / frame / coordinates): bucket `hadashot/pdf/en/vol-125/04363_khirbat-amra.pdf` (HeadlessChrome print, 23 Oct 2026), p. 12 (Fig. 5) and p. 20 (Fig. 15), extracted with `pdfimages`. Text in `hadtext/en/vol-125/04363_khirbat-amra.txt` and `hadtext/he/vol-125/04363_khirbat-amra.txt` (HE ll. 55–63 for W21/W22/W20 in F6; ll. 115–116 for "W22–W20" in F5; ll. 123–124 for W8). Private crops: `private2/E1/IAA_HA125_4363_fig5_F6_plan.jpg`, `…fig15_F5_plan.jpg` (IAA images, not for publication).
Literature check (queries run, result, tag): no final publication of A-4370 beyond HA was found. HA 122 id 1520 (Kogan-Zehavi 2010) mentions only that A-4370 found remains in the north of the site. Repo: Khirbat ʿAmra is not coded with locus or wall detail. **NEW TO THE LITERATURE** (minor editorial and recording error).
Why it might matter: anyone who reuses the locus and wall register (for example a final report, or a database of Mamluk village architecture) cannot tell which "W20" is meant without the square number. The phase colours on Fig. 15 would put a wall into the wrong period.
How to confirm or kill it (with data in hand, or what is missing): it is already confirmed on both plans. It would die only if the IAA archive register gives separate numbers that the HA text and plans did not use.
Confidence: high (the facts); low (importance)
Touches the Copper Scroll? no

---

## Dead ends and minor observations (one line each)

- Draw 1 (HA 127 id 24834, Upper Aqueduct, Billig, A-6513):
  - The box 220750–99/628023–91 fits the 65 m section.
  - The English drops the Hebrew's "six" squares in A3.
  - It gives no dating evidence beyond the sherd counts, and the "rare lead bullae" have no follow-up in HA.
  - Nothing to card. The Herodian-vs-Roman dating debate of the Upper Aqueduct is not advanced by this report.
- Draw 3 (HA 126 id 5453, ʿAtlit salt installations survey):
  - The Carmel-coast box 192525–193628/725134–733864 is a 1.1 km strip that stops about 0.7 km short of ʿAtlit's northern bay, where the text places lifting slopes. The fortress area is at ITM about 194075/734596 by OSM.
  - The cited sites (naval base, 19349/73224; Nahariyya, 208240/766692) fit. Too small to card.
- Draw 4 (HA 125 id 2314, Umm Ṭuba, ʿAdawi): "c. 150 m southwest of Khirbat Umm Tuba". The dig box centre (221648/626235) is about 250 m due west of the ruin as other HA reports place it (id 18760: 221904–31/626225–38, "Site 118"). The report cites Kloner Site 115, not 118. Minor.
- Draw 4 side note: several Umm Ṭuba reports print the map reference northing first (ids 12659 "626215/221800", 25420 "626325–35/222155–65"). This is a format quirk; round 1 (A6-3) has the same habit at Maresha.
- Draw 6 (HA 129 id 25287, Jerusalem, Ha-Porzim St):
  - The map ref 220038–58/630465–80 matches Ha-Porzim St, Old Katamon (OSM 220104/630464).
  - The text says the walls had "three layers of plaster", but the plaster analysis and Fig. 6 say "two layers". Minor.
  - The Iron II plaster comparison (Ḥezekiah's Tunnel, Zova, Qishla) is unpublished for Zova and Qishla.
- Draw 5: Eshel & Safrai's item numbers follow Lefkovits 2000. I checked the Koḥlit items (4, 11, 15, 19, 60), the Secacah items (20–22, 24), item 2 (*nefesh*), item 25 (*qalal*) and item 51 (Zadok) against `tables/entry_concordance.csv` and `landmark_lexicon_index.csv`: all consistent. Their "item 21 … Doq" is an OCR-garbled passage; the Doq item is 31 (VII 11), and the page image could not be opened to check.
- Draw 5: the talent arithmetic (about 4,500 talents × 21.3 kg ≈ 96 t, "almost 100 tons") reconciles.
- Within-report scan, rejected cases: Nahal Bitron (2216), Nahal Dudaim (1935, 1994), Miqve Israel (1716), the Akko–Karmiel railway (1925) and Yavne (437) flag many sub-refs, but these are linear or multi-area surveys whose opening ref covers only part of the area. Not errors.
- Within-report scan, minor: Karmiel, Giv'at Makosh (1833) prints site refs northing first while its general ref is easting first. Its site 3 "75619/22608" is about 900 m west of its siblings (22691–22702). Minor.
- Round-1 leftover, Waʿara el-Soda (Leibner 2018 Ch. 20 n. 30): no HA report in vols 116–137, as expected for a 1960 dig. Not followed further.
- Round-1 leftover, Yehud (E1-2): killed by R2; nothing more to do.
- Round-1 leftover, Giv'at Avni (E1-1): settled by R2 from Fig. 2. Carried forward as the corpus-wide check in card 2, not repeated.

## Blocked inputs

- Drive file 153PPbwQA8dqpQrLPXe6anEYoc2wePS1d (Eshel & Safrai, 27.4 MB): `download_file_content` failed with "File too large for download, over limit of 10 MB". There is no bucket copy in `reading/01 …/` or `copper-scroll-sources/` (the latter returned `AccessDeniedException: 403`). So the page image of n. 66 was not checked; the text layer was read with `read_file_content`.
- `https://www.hamichlol.org.il/מסכת_כלים_(כלי_המקדש)`: WebFetch "client_error".
- The 2015 English reprint (JAJSup 18, pp. 113–129): not available. The publisher's preview PDF (theologische-buchhandlung.de, ISBN 978-3-525-55096-0) has front matter only.
- Milik, RB 66 (1959) 567–575, and Schwartz 2021 (MA thesis): not in the corpus and not fetched.

## Seed / reproducibility

- Seed string "2026-11-06-r2". Seed number = the first 8 bytes (big-endian) of SHA-256("2026-11-06-r2"), which is **9377107723180580898**. RNG: Python `random.Random(seed)`, six calls to `rng.randrange(N)`.
- Population: the round-1 file `out/E1/population_E1_2026-11-06.csv` (9,902 Drive documents, sorted by Drive ID), minus the five round-1 draws, giving **N = 9,897**. Order is kept.
- Script: `draw_e1_r2.py`. Run `python3 draw_e1_r2.py ../../out/E1/population_E1_2026-11-06.csv`.
- No book over 300 pages was drawn, so no page draw was needed.
- Draws:
  1. index 3729, `1Mz3PNtV5buMEGWB7fnSAnF2giCaONajm`: HA 127 (he) 24834, Jerusalem, Hebron Road, the Upper Aqueduct. Read in full, HE and EN.
  2. index 6368, `1cx85afUWh9pFzDeiEJn0kO4OWV5LKKs_`: HA 125 (en) 04363, Khirbat ʿAmra. Read in full, plus the HE and Figs. 5 and 15.
  3. index 5514, `1YeoHhlfplRYllV-MehqOMIhdCyqCdnAZ`: HA 126 (he) 05453, ʿAtlit, salt production installations, survey. Read in full, HE and EN.
  4. index 3780, `1NMma-bMfCZhAzOueHE-UBC-7MKAnCvNW`: HA 125 (he) 02314, Jerusalem, Umm Ṭuba. Read in full, HE and EN.
  5. index 925, `153PPbwQA8dqpQrLPXe6anEYoc2wePS1d`: Eshel & Safrai, *Cathedra* 103 (2002) 7–20 [JSTOR capture]. Read in full (text layer).
  6. index 5009, `1VPEMrk-ycN6CHayVEHnJLANB1Jt_Z--A`: HA 129 (en) 25287, Jerusalem, Ha-Porzim Street. Read in full.
- Within-report scan: `python3 subref_scan.py <hadtext root> out.csv`. A sub-ref is flagged at more than 300 m outside every opening-paragraph box (OIG converted to NIG; northing-first refs swapped).
