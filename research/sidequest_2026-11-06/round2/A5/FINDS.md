# Side-quest A5, round 2: unknown items in the store and Drive (6 Nov 2026)

Lane A5, round 2 (rules: `ROUND2.md`). I built on round-1 `out/A5/` (R3: all three cards SURVIVE). New inputs reached this round: the blocked 145 MB IAA scans PDF, the IAA high-res page register CSV, the 24.9 MB CIIP I.1 copy, the unopened "Images may not have" folder and the other loose items in `08 Working files/Unsorted source scans/`, and the audio tracks of the Hyrcania videos. A record of every item examined is in `item_inventory_round2.csv`. The calendar check for card 1 is in `tryphon_epitaph_calendar_check.csv`. Private products are in `/home/claude/swarm/private2/A5/`: IAA scans, video frames with identifiable people, the Hyrcania transcripts, the Kidron crop, and the Kallia position.

---

FIND CARD
Title (one line): Meinardus's date of AD 592 for the Tryphon epitaph at St Andrew, Jericho, is impossible: 20 February 592 was a Wednesday. Only 637 and 682 fit between 353 and 726. The J19 reopen condition is met by files already in Drive.
Lane: A5
Round-1 link: A5-1 (Meinardus article already in Drive)
What is odd (2–4 sentences): The epitaph says Tryphon died on 20 February, "ἡμέρᾳ ε'" (the fifth day of the week, Thursday), in indiction 10. Meinardus (p. 191) says the only 6th-century year that fits is 592, and he picks it because the church was "destroyed by the Persians in 614". On the Julian calendar, 20 February 592 was a Wednesday. In every year from 350 to 800 whose February falls in indiction 10, the only years where 20 February is a Thursday are 352, 637, 682, 727 and 772. So Meinardus's own method excludes every year from 353 to 636, and on his own premise the church floor was still in use for a burial after 614. CIIP IV no. 2810 keeps 592 as a possible date. I have this only from the owner's reading of CIIP, recorded in the project README.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Meinardus, BSAC XVIII, Drive `08/Unsorted source scans/2026-10-25 13-43.pdf` (`1ZkTJ3CH9cQQJes09KRuq3Ht1s3jetwjt`). Printed p. 189 has the text and translation. p. 191 reads "The only year of the 10th Indiction in the VIth century, in which the 20th of February fell on a Thursday is the year 592 A. D." and lists 637 and 682 for the 7th century. p. 191 also writes "501/2, 515/16" for indiction-10 years; the second should be 516/17.
- Calculation: `tryphon_epitaph_calendar_check.csv`. I used a Julian day number with weekday = JD mod 7 (0 = Monday) and checked it on two anchors: JD 2299160 = 4 Oct 1582 (a Thursday), and 14 Oct 1066 (a Saturday). The indiction of a January–August date in year Y is ((Y+2) mod 15)+1. The two alternatives that Meinardus relays from Augustinović also fail on the calendar: February 575 and February 620 both fall in indiction 8, not 5.
- Project side: `research/assessments/entry29_jericho_pools/README.md`. l.450 has the Oxford summary: Worp 1991 found that 637 and 682 fit, and Di Segni prefers 637. l.565 has the CIIP IV 2810 summary: CIIP keeps "592, 637, 682" as possible dates, and "592 not fully excluded". That line also says the README makes "not a new calendrical calculation here". l.613 records that Bilad al-Sham 2008 p. 25 gives 592 and calls Tuesday the fifth day.
- Scale check of Pl. I (the plan): clean copy `08/Unsorted source scans/WhatsApp Image 2026-10-25 at 14.05.24.jpeg` (`1mFR0Kb2AIu52WkpgjXdLeuMN86bmRuAX`, 1554 × 1218 px). It is a third copy of the plan, besides `2026-10-25 13-50.pdf`. The 10 m bar is about 372 px. Measured on the plan against the text: main building 15.2 × 9.8 m (text 15.90 × 9.40); SE building 5.2 × 4.8 m (text 5.70 × 5.00); SW building 7.9 × 4.7 m (text 8.00 × 4.50); piscine L 6.0 × 4.0 m outside, which fits the 5.25 × 3.40 m interior given in the text; gap from the SW building to L 7.9 m (text "8 m south"). The north arrow points to the page's left.
- Reopen condition: `research/ACTIVE_TEST_before_reset_2026-10-30.md` ("Closed results", Jericho pools) asks for "Meinardus pp. 183–184 and 196 with the plan key and captions". CIIP, as summarised at README l.561, cites "Meinardus 196" for the complex drawing, which is Pl. I. The text of pp. 183–184, the Pl. I plan, the key (MOSAIC / OLD WALL / NEW WALL) and the captions ("Piscine or fish-pond", "Piscine with jars for spawning", "Cistern, north-west of main building") are all in the two PDFs and the JPEG.
Literature check (queries run, result, tag): IIP JERI0020 (https://search.inscriptionsisraelpalestine.org/inscriptions/jeri0020) gives only 324–640 CE. CMHL (https://dig.corps-cmhl.huji.ac.il/Monasteries/jericho-st-andrew) gives "6th c." and no year for the epitaph. The store has CIIP IV only in its Marisa part, so 2810 cannot be read there, and the store-wide `pdf-search "Tryphon"` finds no Jericho text. Worp 1991 itself is unread; the Oxford summary says it found 637 and 682. Tag: **KNOWN BUT UNDER-DISCUSSED** (Worp's result already implies that 592 fails). **NEW TO THE PROJECT** for the explicit calculation, which the README declined to make. **NEW TO THE LITERATURE (provisional)** that CIIP's retention of 592 contradicts the calendar; CIIP p. 260 itself is not read here.
Why it might matter: A corpus entry that keeps a date the calendar rules out is a documented error, and one that is cheap to check. For the project, the result removes 592 as an option. It also shows the site was in use for burial after 614 if the date is 637, or after the Arab conquest if it is 682.
ARGUMENT (entry 29, J19): This does not move J19. The epitaph dates a grave in Room II, not the piscine. Meinardus's "Herodian" date for the piscine rests only on "Cf. Pritchard, BASOR 123 (1951) p. 11" (p. 183). Pritchard's final report in the store (`Pritchard-ExcavationHerodianJericho-1952`, 143 pp.) has no hit for fish, spawn, piscine, St Andrew, Coptic or Zacchaeus, and its only "pool" hits are bibliography. BASOR 123 itself is not in the corpus. So the dating gate stays shut. The reopen condition's source items are now all in hand, so J19 can be re-examined at once, and on present evidence the result stays "not identifiable".
How to confirm or kill it (with data in hand, or what is missing): The calendar result can be re-run from the CSV. Kill it if the epitaph's day numeral is not K (20), or if the indiction numeral is not ι, on a photograph. Augustinović 1951 fig. 26 and the Bilad al-Sham p. 25 photo are not in the corpus. Also read CIIP IV.1 p. 260 to check that it really keeps 592.
Confidence: high (calculation); medium (CIIP's wording, which comes from the owner's summary)
Touches the Copper Scroll? maybe: entry 29 (J19, St Andrew piscine), as a source check only.

---

FIND CARD
Title (one line): A 1932 Mandate file records a 4th–5th-century "tall" with a stylobate foundation at Kallia on the north Dead Sea shore, built over by Potash Company housing. No modern survey of that 1-km square records it.
Lane: A5
Round-1 link: new (IAA high-res page register, a blocked input in round 1)
What is odd (2–4 sentences): On 3 December 1932, S. A. Husseini reported to the Director of Antiquities that sounding trenches at Kallia had exposed several things: "ribbed pot-sherds of the 4th or 5th cent. A.D.", "building foundations of dressed nari stones", "a stylobate foundation" with many sherds 6 m to its south, and that "the place has the features of a 'tall'". The Department allowed a pipeline across the site and workers' houses over it. The site card reads "Kallia … VIII.197.130 … stylobate foundation, artificial mound?, surface pottery … IV–V cent." The IAA online survey map of that area, ASI Map 109/5 "Kalia" (108 sites), has no site within 1.2 km of the centre of the square. WBADB has one site in the square, Bar-Adon 1972 site 87, recorded as "heap of stones; wall remains", Roman, with no stylobate.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- IAA Mandate archive, folder 13076 (ATQ 429): scan 2 (image 77021) is the report of 3 Dec 1932, citing "Report of Major Tulloch to Mr. Lambert"; scans 3–4 (77022–77023) are the continuation and the conditional permit for houses II and XIV; scan 5 (77024) is Novomeysky's letter of 5 Dec 1932.
- Folder 19128 (SRF 118): scan 1 (100244) is the site card; scan 5 (100248) is a 1:500 housing plan of 21 Aug 1932 with pipeline AB and find points C/D in red; scan 6 (100249) is two photographs, 4270/4271, of the stylobate in a trench with a scale rod.
- Drive copies are listed in `IAA_highres_combined_page_register.csv` (`18dn750HpivWncVe-dIbZmaRtv-y7Ny60`). Scans read: `private2/A5/iaa/`.
- The map reference is the printed Mandate square "VIII.197.130" (1:100,000 sheet VIII; Palestine grid 1-km square E 197–198 / N 130–131). Converted position and distances: private.
- ASI: `https://survey.iaa.org.il/aspxService/Service_Eng.aspx/GetPolygonsSites?MapId=78&sitesId=null`, fetched 6 Nov. Nearest site: no. 106, Rujm el-Bahr, 1,249 m from the square's centre.
- WBADB: `branch_only/sandbox__methods/sandbox/west_bank_inventory_2026-10-31/data/wbadb_sites.csv`, row WBS:3477 (Bar-Adon 1972 site 87, 197800/130800).
Literature check (queries run, result, tag): Repo main and branch_only grep for "Kallia|Kalya|Kalia" finds only the Twin Cave note "opposite Kalia" and survey rows, nothing about this site. Hadashot metadata has no Kalya or Kallia report. The store-wide `pdf-search "Kallia"` returns nothing, and "Kalia" returns only personal names and the ASI map citation. Two web searches (Kallia 1932 Byzantine stylobate; Kalia Byzantine church or site, Bar-Adon 87) found no hit. QDAP 1932–33 and the Mandate schedule of sites are not in the corpus. Tag: **NEW TO THE PROJECT**. **NEW TO THE LITERATURE (provisional)** for its absence from ASI Map 109/5 and WBADB.
Why it might matter: It is a dated Late Roman–Byzantine building with columns (a stylobate), probably a church or public building, on the north Dead Sea shore. It was seen once in 1932 and then built over, and the modern survey map of the area does not record it. Bar-Adon's site 87 in the same square may be what is left of it, or a different ruin. Either way, the ASI map has neither.
How to confirm or kill it (with data in hand, or what is missing):
- Get scan 19128/5 (6.8 MB, too large for the connector) and register its find points C/D on the 1940s 1:20,000 sheet or the RAF sorties.
- Read Bar-Adon 1972 site 87 in ASI 1. The store copy has no text layer for the Bar-Adon chapter, so this needs the page image.
- Kill it if Bar-Adon 87 describes the same stylobate (then it is recorded, and the tag drops to NEW TO THE PROJECT), or if QDAP or a later report publishes the 1932 finds.
Confidence: high (what the file says); medium (that no modern record exists)
Touches the Copper Scroll? no (Byzantine; about 6.5 km NE of Kh. Qumran)

---

FIND CARD
Title (one line): The guide's spoken commentary on the 20 Oct Hyrcania videos matches Gutfeld's published account of the western tunnel: a heading correction, and a dead end in "solid rock". But the filmed walls carry pick marks, which the publication says the western tunnel has lost.
Lane: A5
Round-1 link: A5 round 1 "Other records made" (EV10_0125–0128 never described; audio untranscribed)
What is odd (2–4 sentences): The commentary was extracted and machine-transcribed this round.
- In EV10-0127 (camera clock 16:52, 55.6 s) the guide says of the passage: "they just realized a bit up and right and they took a bit low and left". He adds that a colleague nicknamed a feature there "the mezuzah" for "the Americans".
- In EV10-0128 (17:04) he says the excavators came down and "this is solid rock". He names "Oren" and "Yakov … the technical person and archaeologist".
- NEAEHL (Gutfeld) says of the western tunnel: at about 55 m "its course verges slightly to the west; this deviation was later corrected by the diggers", and "Both branches terminate in a dead-end". It names C. R. Morgan of the Liberty Historical Society, Missouri, as partner in the first three seasons.
- The same entry says that in the western tunnel "the brittle rock and the floods … have eradicated all marks left during the cutting". The owner's photos (08921–08923, "the walls carry pick marks") and EV10-0128 (diagonal pick scars) show tool marks.
- So either the filmed tunnel is the eastern one, or the published "all marks eradicated" is too strong.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Audio: bucket `video/EV10-0127-ee2215dd/original.mp4` and `video/EV10-0128-89ac8cce/original.mp4`, extracted mono 16 kHz. Transcripts from faster-whisper "medium" are in `private2/A5/hyrcania/transcripts_whisper.md`. Frames at t = 2, 6, 30, 46 and 52 s (0127) and 5, 15 and 21 s (0128) are in `private2/A5/hyrcania/EV10-0127_0128_frames.jpg`. In the frames, the t = 2 and 6 s views of 0127 show a step in the passage section, and t = 46 s shows a slot high on the right wall by the guide's hand.
- NEAEHL vol. 5: store `Stern-ed-1993-2008-New-Encyclopedia-of-Archaeological-Excava-1b9b4740`, PDF pp. 252–253 (printed 1787–1788).
- Project: `research/assets/plans/hyrcania-field-2026-10-20/README.md` (l.36 wall marks; the end-face caveat "it isn't certain that the face is the tunnel's end"; l.85 and l.96, where widening is read as collapse; l.94, the ibex). That README does not use NEAEHL's measurements: 110 m length, narrowing to 50 cm at 25 m, the correction at 55 m, the 2.65 m maximum width at 96 m, and the two branches of 15 m and 17 m with dead ends.
Literature check (queries run, result, tag): Repo grep of the Hyrcania field and entry-29 Hyrcania files for "deviation|dead-end|branch|55 m|110 m|mezuz" finds no hit; "ibex/590" is already there. The store-wide `pdf-search "Hyrcania"` with "tunnel" finds only NEAEHL. Haber & Gutfeld 2024 and Gutfeld, *Qadmoniot* 125 were not read. Tag: **NEW TO THE PROJECT** (the commentary and the join with NEAEHL). **NEW TO THE LITERATURE (provisional)** for the tension between the pick marks and "eradicated all marks", if the filmed tunnel is the western one.
Why it might matter: It answers the README's open caveat about the end face. The published account gives both western branches as dead ends, and the guide, standing at the face, calls it solid rock. That supports the README's inference that this is a working face where cutting stopped, not a blocked or collapsed end. It also shows the guide speaking as a member of the 2000–05 excavation team ("the guy that I was working with … the Americans"), which bears on how much weight his relayed opinions should get.
How to confirm or kill it (with data in hand, or what is missing):
- Ask the owner which tunnel (western on the south bank, or eastern on the north bank) the 16:44–17:04 clips show. Without contact, compare the frames for bitumen layers, which the eastern tunnel has and the western does not.
- A Hebrew or English speaker should check the transcript; whisper confidence was 0.51 for 0127 and 0.66 for 0128.
- Kill it if the clips are in the eastern tunnel. The correction remark would then refer to the eastern tunnel's "slight deviation to the west", and the pick-mark tension disappears.
Confidence: medium (what is said and published); low (which tunnel, and therefore the tension)
Touches the Copper Scroll? maybe: Hyrcania (entries 29 and 32 discussions) and the tunnel-purpose question; no reading changes.

---

FIND CARD
Title (one line): A 1956 letter in IAA file PAM/1120 records that a radiocarbon test on a Murabbaʿat textile, cleared through F. E. Zeuner, gave an "early" date that did not agree with the finds, and that a second test was promised.
Lane: A5
Round-1 link: new (IAA high-res page register)
What is odd (2–4 sentences): Grace M. Crowfoot wrote to G. Lankester Harding in Amman on 12 August 1956 (aerogramme postmarked Geldeston 14 Aug 56, Amman 17 Aug). She says she has "had a line from Dr Zeuner's secretary saying that he says you can use the C14 test for the textile providing he sees the proofs so that the date can be corrected if necessary … he said another test on it would be made – I hope that will be nearer the date agreeing with your finds". She was "devoutly thankful to get an early date – any early date – for I was afraid they might be medieval". On the second page: "… can be regarded as an early group – not medieval I am happy". The file is the Department of Antiquities' "Murabbaʿat Scrolls" file. The letter discusses the basketry notes and the textile reports drawn by "Betty" (Elisabeth Crowfoot) for the Murabbaʿat publication (DJD II, 1961).
Evidence (exact sources: file path / page / figure / frame / coordinates): IAA Mandate archive, folder 13205 (ATQ PAM/1120), scans 13–14 (image ids 79374–79375). Drive copies are `1L5GldejjP8XfnxMdUXcs4KRyLcjDROq9` and `1MVHVKDfKEkycmilYmi2DD0DdsyFo3PHV`, listed in `IAA_highres_combined_page_register.csv`. Read: `private2/A5/iaa/IAA13205_pos13…jpg`, `…pos14…jpg`. Context in the same file: scans 4–8 (Crowfoot, July 1953, Islamic textile with Kufic *baraka*, "dated on one word alone" warning) and scan 15 (Harding, 1 Sept 1956: hold the basketry notes for de Vaux; all Murabbaʿat material still at the museum). The only 1950s-lab radiocarbon date on a Murabbaʿat textile that I found online is GrN-943, wool, 1815 ± 50 BP, cave 1 or 2, cited to Weinstein 1984 (https://xronos.ch/c14s/150770).
Literature check (queries run, result, tag): Repo main and branch_only grep for "PAM/1120|PAM1120|Crowfoot" finds no note on this file; the Crowfoot hits are unrelated. The owner's register note summarises the letter but links it to no measurement. Web: "GrN-943 Murabba'at" finds no source; "Murabba'at textile radiocarbon Zeuner Crowfoot" finds nothing on the 1956 test. DJD II is not in the corpus. Tag: **NEW TO THE PROJECT**. The link to GrN-943 is a hypothesis.
Why it might matter: It is an early, unpublished episode in the radiocarbon history of the Judaean Desert finds. A first result disagreed with the archaeological date, a second test was arranged, and the user of the date was required to let the lab correct it in proof. That is relevant to how the early Judaean Desert radiocarbon dates were produced and reported. Whether DJD II prints a date, and which one, is open.
How to confirm or kill it (with data in hand, or what is missing):
- Read DJD II (Crowfoot and Crowfoot, textiles chapter) for a C14 statement and its lab number.
- Read the Groningen date list that publishes GrN-943, and the Zeuner Geochronology Laboratory (London) lists, for the sample's submitter and year.
- Kill the GrN-943 link if GrN-943 was submitted by someone else or after 1957. The letter itself stands either way.
Confidence: high (letter content); low (the GrN-943 link)
Touches the Copper Scroll? no

---

## Dead ends

- IAA 19623, ATQ 199(a) (the 145 MB PDF): this is the Harvey survey of the Holy Sepulchre and Nativity, 1933–35, covering commissioning, salaries, special warrants and Treasury approvals. p. 615 reads: extra cost for "faulty rock foundations" and for "archaeological remains of the first importance" found in trial pits, and £P.149 to cover the Nativity mosaic before the Orthodox Christmas. The 1934 discovery of the Nativity mosaics is published (Harvey, Richmond). The owner's 2 Nov ledger already covers the dated letters. Not pursued.
- `IAA_highres_combined_page_register.csv`: this is the owner's 1,593-row observation register for 35 folders. It does not include folder 19623. It was mined for cards 2 and 4. Mird (SRF 141), Masada, Nabi Musa and the Wadi Qelt milestone are records of known sites.
- "Book Oct 19, 2026 (1).pdf" is SBF 36 pp. [242]–265, which duplicates the store's `01-SBF36-Christian-Archaeology-1990-indexed`. SCR-20261017-qrzs is a book page 226, "Byzantine mosaic floor in Cell no. 9", probably the same volume (not matched).
- "Images may not have" (8 PNG): screenshots of Copper Scroll Studies Figs. 6.2–6.8 and 11.7–11.8, already in `research/assets/plans/copper-scroll-studies2004/`. A scale check of Fig. 6.2 (Qumran aqueduct, measured path about 375 m against "c. 700 m" in `water.csv`) was started but not finished: the 700 m figure is a secondary citation (Galor), and the figure may not show the whole channel. Not claimed.
- Kidron IMG_9844, t = 106–111 s: the lines are Hebrew in ink or paint on the court wall, not cut into it. They are modern or pilgrim graffiti, only partly legible. Dropped.
- Hyrcania EV10-0125 audio is garbled ("National Park Authority… University…"). EV10-0126 has no site content.
- Meinardus Pl. I passes the scale check (card 1). Pl. I is internally consistent, so it gives no error card of its own.
- Murabbaʿat: Islamic textile letters of 1953 (Mayer's *baraka* reading) were not followed, because they are probably reflected in DJD II.

## Blocked inputs

- **CIIP I.1, 24.9 MB copy** (Drive `126ct8RGvh91Nh4qHqHUWwqFsaqEus8R9`, 24,908,697 B): `read_file_content` returns 213,361 characters, covering the front matter and nos. 1–9 only (to printed p. 53). The rest is cut off. `download_file_content` was not tried, because the base64 would be about 33 MB, above what the connector returned for the 6.8 MB scan below.
- **IAA 19128/5 Kallia plan** (Drive `1OmoCLtPqafLkXLOAFaR96ANxI0ZxVk9B`, 6,813,153 B): `download_file_content` failed with "message from the server was too large or could not be parsed".
- **CIIP IV.1 pp. 257–260 (nos. 2809–2810)**: the store's CIIP IV text is the Marisa part. The St Andrew entries are not in it.
- Not in the corpus: DJD II (1961); BASOR 123 (Pritchard 1951); Worp 1991; Weinstein 1984; the Groningen list for GrN-943; QDAP 1932–33; Haber & Gutfeld 2024.
- The Oxford Cult of Saints record E03571 could not be fetched: the URL is too long for the WebFetch proxy (HTTP 403).
- Resolved this round: the 145 MB IAA 19623 PDF was copied from the bucket to scratch (`gsutil cp`), read, and deleted. `IAA_highres_combined_page_register.csv` was read in full.

## Seed / reproducibility

- Audio: `gsutil cp gs://copper-scroll-cog-1030/video/<id>/original.mp4`, then `ffmpeg -vn -ac 1 -ar 16000`, then faster-whisper (`small`, then `medium` for 0127 and 0128), CPU int8, beam 3. The originals were deleted after extraction.
- ASI: `GetMaps` (GET; map id 78 = 109/5 Kalia), then `GetPolygonsSites?MapId=78&sitesId=null`. Grid to lat/lon used pyproj EPSG:28191 → 4326.
- Calendar: `tryphon_epitaph_calendar_check.csv` (formula in card 1).
