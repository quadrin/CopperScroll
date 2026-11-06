# Round-2 review RR2 (6 Nov 2026): lanes A5, A6, B1a, B1b

Reviewer RR2. Method: `REVIEW_BRIEF.md` as amended by `review2/REVIEW2_NOTE.md`. AGENTS.md procedures were not applied. For each card I re-opened the evidence for at least the strongest claim, checked the Round-1 link against `out/<LANE>/FINDS.md` and the R2/R3 verdicts, and ran one cheap kill test where the worker had left one unrun. My private renders are in `private2/RR2/`: a Maresha IV p. 17 render and the BAIAS 23 p. 19 render.

---

## A5-1: Meinardus's AD 592 for the Tryphon epitaph is calendrically impossible

- **Verdict: SURVIVES, TAG CHANGED** to KNOWN BUT UNDER-DISCUSSED. The calculation is new to the project. I dropped the "NEW TO THE LITERATURE (provisional)" part.
- **Confidence:** high for the calculation; low for the claim about CIIP. **Cost:** cheap.
- **Evidence checked:**
  - Read Meinardus through Drive `1ZkTJ3CH9cQQJes09KRuq3Ht1s3jetwjt` (text layer). p. 191 has "The only year of the 10th Indiction in the VIth century, in which the 20th of February fell on a Thursday is the year 592", and "501/2, 515/16". p. 189 says K, E and I carry numeral strokes. That answers the card's own kill condition on the numerals as Meinardus read them.
  - Recomputed the Julian weekday myself from a JDN. The anchors check: 4 Oct 1582 is a Thursday and 14 Oct 1066 a Saturday. 20 Feb 592 is a **Wednesday**. For 300–800, the indiction-10 years with a Thursday 20 February are 307, 352, 637, 682, 727 and 772. The second Meinardus year should be 516/17, not 515/16. Feb 575 and Feb 620 are both indiction 8.
- **Literature:**
  - The repo README l.450 records Worp 1991 (via Oxford): only 637 and 682 fit. So the published literature already excludes 592 in effect.
  - README l.565 is the owner's summary of CIIP p. 260. It says CIIP lists 592/637/682 "stating that Worp reached the same conclusion". Whether CIIP really endorses 592 rests on that secondary summary. Oxford E03571 could not be fetched (URL too long; a shorter form needed approval).
  - Web search found no source that states the Wednesday result explicitly.
- **Round-1 link:** this is not a restatement. Round 1 found the file; the calculation and the Pl. I scale check are new. The card's "reopen condition met" part does repeat round 1.
- **ARGUMENT:** it follows from the evidence and is suitably modest ("does not move J19").

## A5-2: 1932 Mandate file on a 4th–5th-century "tall" with a stylobate at Kallia

- **Verdict: WEAKENED.** Final tag NEW TO THE PROJECT.
- **Confidence:** high for the file content; low for "unrecorded". **Cost:** moderate.
- **Evidence checked:** I read the private scans.
  - 13076/2 (3 Dec 1932) has "ribbed pot-sherds of the 4th or 5th cent. A.D.", "6 meters south of a stylobate foundation" and "the features of a 'tall'".
  - The 19128/1 card reads "VIII.197.130 … stylobate foundation, artificial mound?, surface pottery", with "IV–V cent." in a different hand.
- **Kill test run:** I re-fetched ASI `GetPolygonsSites?MapId=78`. The nearest site is no. 106, Rujm el-Bahr, at 1,248 m (confirmed). But ASI 109/5 also omits **Bar-Adon 87**, although it includes Bar-Adon 84, 85 and 86 (sites 98–106). WBADB WBS:3477 puts Bar-Adon 87 ("Heap of stones; wall remains", Roman) at 197800/130800, inside the same 1-km square. So a modern survey does record ancient walls in that square. The title's "No modern survey of that 1-km square records it" is overstated. The more economical reading is that Bar-Adon 87 is what remained of the 1932 site, which the card itself allows. The absence from ASI tells us about ASI coverage, not that the site went unrecorded.
- **Literature:** repo grep finds only the Kalya photo leads. A web search (Kallia 1932 Potash stylobate) found nothing.
- **What stands:** the 1932 file, the dated pottery and the stylobate are new to the project and worth a look at Bar-Adon 1972 p. 119. NEW TO THE LITERATURE is not supported until Bar-Adon 87 is read.

## A5-3: Hyrcania guide commentary vs Gutfeld (NEAEHL)

- **Verdict: WEAKENED.** Final tag NEW TO THE PROJECT.
- **Confidence:** low. **Cost:** needs new data (which tunnel was filmed).
- **Evidence checked:**
  - The transcript quotes match `private2/A5/hyrcania/transcripts_whisper.md` ("a bit up and right … a bit low and left", "this is the Mezuzah", "this is solid rock").
  - The NEAEHL p. 252 quotes match: "verges slightly to the west; this deviation was later corrected", "Both branches terminate in a dead-end" and "eradicated all marks left during the cutting".
- **Alternative explanation:**
  - The guide's remark is vague. It is not specific to the western tunnel: NEAEHL p. 253 also gives the eastern tunnel "a slight deviation".
  - The project README (l.20, l.105) records that the tunnel shown in the group D photos is unidentified.
  - So the "match" is loose, and the pick-mark tension, the only part offered as NEW TO THE LITERATURE, depends on an unknown.
- **What stands:** the transcription, and that the guide speaks as a 2000–05 team member. Both are new to the project.

## A5-4: 1956 Crowfoot letter on a C14 test of a Murabbaʿat textile (PAM/1120)

- **Verdict: SURVIVES.** Tag NEW TO THE PROJECT kept.
- **Confidence:** high for the letter; low for the GrN-943 link. **Cost:** moderate (DJD II).
- **Evidence checked:** both scans (13205/13–14). They have "you can use the C14 test for the textile providing he sees the proofs so that the date can be corrected", "another test on it would be made – I hope that will be nearer the date agreeing with your finds" and "devoutly thankful to get an early date – any early date". The aerogramme is addressed to Lankester Harding in Amman, postmarked Geldeston 14 Aug 56.
- **Literature:** a web search (Murabbaʿat textiles radiocarbon Zeuner Crowfoot) found nothing on this test.
- **Caveat:** "gave a date that did not agree with the finds" is a fair inference from "nearer the date agreeing with your finds", not a quotation. The GrN-943 link is correctly labelled a hypothesis.

## A6-1: Maresha IV map references shifted about 80 m NE (WGS84 projected without the datum shift)

- **Verdict: SURVIVES.** Tag NEW TO THE LITERATURE kept.
- **Confidence:** high for the offset; medium for the mechanism. **Cost:** cheap.
- **Evidence checked:**
  - Maresha IV p. 46 has "map reference 611160/190767" (SC 1), and p. 268 has Kloner's "NIG 190774, 611098".
  - The private checkerboard overlay looks good: roads, Road 35 and paths run on across the tile joins.
  - My pyproj recomputation of the naive vector gives +66.18 E / +41.08 N.
  - From the CSV, the median MIV − plan-true is dE +60, dN +48 (n = 33). The card gives +64/+48 for n = 30, a minor difference.
- **Registration-free cross-check (mine):** MIV − HA vectors are SC 1 (+106, −11), SC 89/2021 (+70, +64), SC 126 (+114, +31) and SC 169/2021 (+111, +27). So the MIV references sit 70–115 m east of the team's own HA references without any imagery. B3 round 2 noted the same easting offset in a dead end and left it unresolved.
- **Alternative mechanism tested:**
  - Treating the old Palestine grid plus 50/500 km as ITM gives (+60, −8) at Maresha (EPSG:28193 → 2039). That fits the easting as well but not the northing (+48 observed).
  - So the naive-WGS84 mechanism remains the better fit, but not a proven one. The card's "medium" is right.
- **Literature:** no erratum found. No other project file has the datum shift.

## A6-2: Three Maresha location errors (SC 89/90 shared reference; SC 169 "southwest"; SC 97 on the NW plan)

- **Verdict: SURVIVES.** Tag NEW TO THE LITERATURE (small errata) kept.
- **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - (a) 00498 (SC 90, "220 m southeast", A-4361) and 00727 (SC 89, "150 m southeast … 55 m south of SC61", A-4687) both print "NIG 190680/611086; OIG 140680/111086", in both EN and HE. The two texts describe different places, so the shared reference is an error.
  - (b) 12643 says "c. 105 m southwest of the Upper City" in both EN and HE ("מדרום-מערב"). 26015 says "105 m southeast of the tell". Note that 12643 also says the complex was found "surveying in the southwest area of Maresha", so the 2014 wording is internally consistent but geographically wrong.
  - (c) p. 176 has "Subterranean Complex 97 (Plan 1.3.2)". The p. 17 caption reads "Plan 1.3.2 … NW section". I rendered p. 17 and found no label 97 on Plan 1.3.2, so the card's kill test fails.

## B1a-1: Thiede's Moẓa sherd vs the Tel Moẓa Iron Age pre-firing jar inscriptions (ʿAtiqot 110)

- **Verdict: WEAKENED.** Final tag NEW TO THE PROJECT. The link is a hypothesis.
- **Confidence:** low. **Cost:** needs new data (the object).
- **Blocked input resolved:** BAIAS 23 (2005) can be downloaded whole from aias.org.uk (`download/1745/`). I read it and then deleted it from scratch.
  - p. 16 repeats HA: "An enigmatic ostracon, incised before firing, bearing a Second Temple period Hebrew inscription". There is no reading and no epigrapher.
  - Fig. 10H (p. 19, "incised sherd") is a drawing with a flat body-sherd profile and a few strokes. The four ʿAtiqot 110 inscriptions are on a holemouth rim and on jar handles.
  - BAIAS also gives four seasons (2001–2004), where HA gives two.
- **Overstatement:** ʿAtiqot 110's "new category of ownership inscription, found so far only in Moẓa" refers to the sender–recipient formula, not to incision before firing. So "the same rare technical trait" and the ARGUMENT's "signature of Tel Moẓa's Iron Age II workshop" overstate the prior.
- **What stands:** the confirmed absence of any reading, now in two publications, and the absence of Thiede from ʿAtiqot 110 (0 hits for Thiede or Lass). The re-dating is a reasonable question to put to an epigrapher, not a find.

## B1a-2: Ledger of 16 HA inscriptions announced as "not (yet) deciphered"

- **Verdict: SURVIVES.** Tag NEW TO THE PROJECT kept. **MERGE note:** the ʿAkko lead tablet row duplicates B1c round 2 (its ʿAkko Ha-ʿAmal card); keep it there.
- **Confidence:** medium. **Cost:** moderate.
- **Evidence checked:** 01826 (Rantis NW, A-4407, May 2005) has "another milestone bears a Latin inscription that has not yet been deciphered (Fig. 7)", and Table 1 basket 106 reads "an inscription".
- **Literature:** a web search (Rantis milestone Latin inscription Lod Neapolis) found no reading.
- The positive-control rows are plausible. The counts in the title and body agree: "14 years on" means after the HA report, 26 years after the dig.

## B1a-3: West Bank polygon test of HA coverage

- **Verdict: MERGE** into round-1 B1a-3, as R2 corrected it, as its completed kill test. It is not a separate find. Tag stays NEW TO THE PROJECT.
- **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - `ha_westbank_polygon_deep.csv`: the raw deep hits for vols 117–128 are 17. The exclusions are all D3 map-reference errors (244, 631, 638, 682, 980, 997, 8518, 24845; checked against `out/D3/ha_mapref_errors.csv` for 997, 8518, 980 and 682) or municipal Jerusalem (Silwan, Tell el-Ful, Mount Scopus, Beit Ṣafafa). That leaves 4, as stated. Vols 129–136 hold 17.
- **Round-1 link:** the result is R2's corrected pattern. What is new is the text-free method, which is why I merge it rather than kill it.
- **ARGUMENT:** it follows, but "Before 2020 … essentially blind" overstates. On the card's own data, vols 129–130 (2017–18) already hold 4 deep reports. "Before 2017" is accurate.

## B1b-1: Nine reports with the wrong excavation year in both EN and HE (permit clock)

- **Verdict: SURVIVES.** Tag NEW TO THE LITERATURE kept.
- **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - 27732 has "During October 2010 … A-6916". 26484 has "An excavation conducted at Khirbat Deir el-ʿAmud in 2013 … (Permit No. A-6916)".
  - `neighbors.py 6916` gives 17 neighbours, all Sep–Nov 2013.
  - 01633 has "February 2004 … A5878", and the A-5878 neighbours are Feb–Apr 2010.
  - 13681 has "June 2009 … A-6814". 04377 has "January 2010 … S-235/2011". 00257 has "May 2000 … A-3636* … separation fence".
- **Alternative explanation:** retroactive permits. The month-match pattern argues against them. No overlap with other round-2 lanes.

## B1b-2: Permit-citation conflicts and DOI-vs-"[Fig. 1: A-NNNN]" label errors

- **Verdict: SURVIVES.** Tag NEW TO THE LITERATURE kept.
- **Confidence:** high. **Cost:** cheap.
- **Evidence checked:**
  - 26665 has "(Kisilevitz 2014 (…2004.13705)[Fig. 1: A-9146])" in both EN and HE, and 13705 has "Permit No. A-6146".
  - 27729 has "(Shmueli, Mamlya and Balila 2017 (…25230) [Fig. 1: A-9775])". 25230 is Ofaqim by Shmueli, Mamalya and Balila, A-7775. Its own permit, A-9450, dates from Dec 2022.
  - 27698 has "Area A; Permit No. A-6345", and 02079 (Palmaḥim North, Nov–Dec 2011) has A-6345.
- **Round-1 link:** this extends round-1 B1b-2 to new volumes and adds a new test. It is not a restatement.

## B1b-3: 410 permits cited in HA with no HA report of their own; 127 traceless, 2005–2017

- **Verdict: SURVIVES.** Tags kept (KNOWN BUT UNDER-DISCUSSED for the backlog; NEW TO THE LITERATURE for the figure and list), with a caveat on the headline.
- **Confidence:** medium. **Cost:** moderate.
- **Evidence checked:**
  - I recomputed own-permit coverage from `parsed2.csv` (EN/HE first permit only): 71.1% for A-3200–8799, close to the card's 71.6%.
  - Per 500-permit block, A-3000–3499 is 43% (published before vol. 116, outside the corpus), A-3500–7999 is 68–78%, A-8000 is 65% and A-8500 is 56% (lag).
  - The examples check out: 25907 has "Remains of a settlement from the Persian period (Permit No. A-6993)", and 25562 has "Kh. er-Ruweisat … excavated in 2013 (Permit No. A-6680)". In the corpus, A-6993 and A-6680 occur only in these citing reports and in unrelated number matches.
  - A web check on Ruweisat found only the Burma Road (Zilberbod) village, a different site.
- **Caveat:**
  - "About 28% of IAA excavations of 2000–2020 have no HA report" is an upper bound. The A-3200 and A-8000+ blocks are distorted by the corpus edges, and not every A-number is an excavation (the card says so).
  - The 2005–2017 sub-window, about 25%, is the defensible figure. The ARGUMENT ("weakens absence claims by an unknown amount") follows and does not overstate.

---

| lane | card | short title | original tag | verdict | final tag | confidence | cost |
|---|---|---|---|---|---|---|---|
| A5 | 1 | Tryphon epitaph: 592 impossible (Wed) | KNOWN BUT UNDER-DISC. + NEW TO PROJECT + NEW TO LIT (prov.) | SURVIVES, TAG CHANGED | KNOWN BUT UNDER-DISCUSSED (calc new to project) | high (calc) / low (CIIP) | cheap |
| A5 | 2 | Kallia 1932 stylobate "tall" | NEW TO THE PROJECT + NEW TO LIT (prov.) | WEAKENED | NEW TO THE PROJECT | high (file) / low (unrecorded) | moderate |
| A5 | 3 | Hyrcania guide audio vs NEAEHL | NEW TO THE PROJECT + NEW TO LIT (prov.) | WEAKENED | NEW TO THE PROJECT | low | needs new data |
| A5 | 4 | 1956 Crowfoot letter, Murabbaʿat C14 | NEW TO THE PROJECT | SURVIVES | NEW TO THE PROJECT | high / low (GrN-943) | moderate |
| A6 | 1 | Maresha IV refs ~80 m NE (datum) | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | high / medium (mechanism) | cheap |
| A6 | 2 | Maresha SC 89/90, SC 169, SC 97 slips | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | high | cheap |
| B1a | 1 | Moẓa sherd vs Tel Moẓa pre-firing group | NEW TO THE LITERATURE | WEAKENED | NEW TO THE PROJECT | low | needs new data |
| B1a | 2 | 16 "not yet deciphered" inscriptions | NEW TO THE PROJECT | SURVIVES (ʿAkko row merge with B1c-r2) | NEW TO THE PROJECT | medium | moderate |
| B1a | 3 | West Bank polygon test of HA gap | NEW TO THE PROJECT | MERGE into round-1 B1a-3 | NEW TO THE PROJECT | high | cheap |
| B1b | 1 | 9 both-language year errors (permit clock) | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | high | cheap |
| B1b | 2 | DOI vs Fig. 1 permit-label errors | NEW TO THE LITERATURE | SURVIVES | NEW TO THE LITERATURE | high | cheap |
| B1b | 3 | 410 cited-but-unreported permits | KNOWN BUT UNDER-DISC. + NEW TO LIT | SURVIVES (headline is an upper bound) | unchanged | medium | moderate |
