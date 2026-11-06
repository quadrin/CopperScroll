# Side-quest B1c: Hadashot at scale, HA-ESI vols 130–137 (2018–2025), 6 Nov 2026

Lane B1, worker B1c. Inputs: bucket `hadashot/derived/hadtext_pdftotext.tgz` (all 9,334 EN+HE text files extracted; cards only for reports in vols 130–137, 1,322 reports), `/home/claude/swarm/baseline/reports_metadata.csv`, bucket `hadashot/pdf/{en,he}/vol-NNN/` (first pages rendered for checks), bucket `atiqot/pdf/vol-112/` (two articles), `hadashot/derived/hoard_followup_2026-10-24.md`.
D3 audited map references. This lane audits two other fields that every report prints in both languages: the **excavation date** and the **permit number**. It also uses the permit number as an independent clock. IAA "A-" permits are issued in sequence, about 250–300 a year. From the 3,000+ reports whose EN and HE years agree, the year bands are tight (`permit_year_calibration.csv`; e.g. 2017: p10–p90 = A-7905…8139; 2018: 8193…8388; 2019: 8435…8615). Known exception: the Unit for the Prevention of Antiquities Robbery reuses blanket or retroactive permits (A-6979, A-7292/2014-06, A-8577 each cover several documentations in different years). Those rows were not used as evidence.

Data: `ha_en_he_date_conflicts.csv`, `ha_en_he_permit_conflicts.csv`, `permit_year_calibration.csv`; scripts in `scripts/` (`parse.py` → `enhe_dates.py`, `enhe_permit.py`, `permcal.py`, `permdup.py`). Every site in this file is a published excavation; no unrecorded feature's coordinates appear here.

---

FIND CARD
Title (one line): In six HA 130–137 reports the English excavation year contradicts the Hebrew, and the permit number shows the Hebrew is right each time. Four of the six are in HA 132 (2020), and in all four the English reads "2019"
Lane: B1c
What is odd (2–4 sentences): I compared the opening date sentence of every report in EN and HE (4,667 pairs). After removing parse artefacts, the whole corpus has 7 real disagreements. Six fall in this slice, and one is a typo ("July 2207", HA 121, id 01284). In each of the six the Hebrew year fits the permit-number band, and the English year does not. Four are in HA 132 (published 2020): the English reads "2019" in every one, while the Hebrew has 2016, 2017 or 2018. That looks like a translator or editor defaulting to the previous year.
- 25847 Jerusalem, Old City, Dar el-Consul (HA 132): EN "January 2019", HE ינואר 2018, A-8181.
- 25860 Kefar Haruv (East) (HA 132): EN "July and August 2019", HE 2016, A-7740. The EN also drops the "A-".
- 25826 Jerusalem, Shikune Nusseiba (HA 132): EN "March–April 2019", HE 2017, A-7907.
- 25795 Hodayot (HA 132): EN "May–June 2019", HE 2018, A-8296.
- 25494 Jerusalem, Beit Hanina (HA 130): EN "February 2013", HE 2014, A-7030.
- 26233 ʿArʿara in the Negev (HA 134): EN "September–October 2012", HE 2017, A-8106.
Evidence (exact sources: file path / page / figure / frame / coordinates): bucket tarball `hadtext/en/vol-<V>/<id>_*.txt` vs `hadtext/he/vol-<V>/<id>_*.txt`, first sentence after the report type. I confirmed 25847 HE on the rendered PDF page 1 (`hadashot/pdf/he/vol-132/25847_*.pdf`: "בחודש ינואר 2018 … A-8181"). Calibration (`permit_year_calibration.csv`): 2014 band A-7010…7259; 2016 7624…7832; 2017 7905…8139; 2018 8193…8388. A-8106 cannot be 2012: the 2012 band is A-6396…6650. The full list with notes is in `ha_en_he_date_conflicts.csv`. No report in the corpus has an excavation year later than its publication date (checked for all 4,667 in both languages).
Literature check (queries run, result, tag): Repo main and `branch_only` grep for the ids with date context, and for "English and Hebrew versions": no hit. 25494 is in the project's location-misprint list (map ref), but its date is not. D3 checked map refs only. Web: no HA-ESI erratum found. I could not open the live pages (`hadashot-esi.org.il` is robots-disallowed for WebFetch; I did not get around that). **NEW TO THE LITERATURE.**
Why it might matter: The English pages are what the project's HA pipeline read. A wrong year moves an excavation by up to 5 years (ʿArʿara). The permit-number clock is a free, general check: any HA, ʿAtiqot or IAA record with an "A-" permit can be dated to about ±1 year without reading it.
How to confirm or kill it (with data in hand, or what is missing): Open the EN and HE PDFs page 1 for the six ids (5 minutes). It is killed for a report if a later corrected version exists, or if the Hebrew is the one with a misprint and the permit was issued years before work began. Retroactive permits are documented only for the robbery unit. None of these six is a robbery-unit job.
Confidence: high (25847, 25826, 25795, 26233, 25494); medium (25860, whose EN permit string is malformed)
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): Five English HA 131–133 reports print a permit number that belongs to a different excavation. The Hebrew gives a unique number each time, so the English creates false "same permit, two sites" pairs
Lane: B1c
What is odd (2–4 sentences): I looked for "the same excavation under two names" by grouping all reports by permit number. Most shared permits are genuine (preliminary vs final, or several areas of one project). But several pair unrelated sites 40–100 km apart. In each such pair in this slice, the English text of the later report differs from its own Hebrew by a 1–2 digit slip, and the English value is the other site's permit:
- Ginnaton (Jindas), 25581: EN A7197 / HE A-7191. A-7197 = Gush Halav, 23808 (HA 127).
- Revadim Quarry, 25629: EN A-6808 / HE A-6806. A-6808 = Modiʿin, opposite Horbat Hadat, 09556 (HA 126; its HE also reads A-6808).
- Horbat Hanot, 25933: EN A-8357 / HE A-8537 (a transposition). A-8357 = Gan Ha-Darom, 25874 (HA 132).
- Horbat Tittora, 25992: EN A-8736 / HE A-8710. A-8736 = Ramla, Trumpeldor St, 26002 (same volume and month).
- Tel Yavne Areas B and D, 26102: EN A-8520, A-8565 / HE A-8520, A-8656 (a transposition). A-8565 = Yeroham, 26092. A-8656 is the Tel Yavne permit used in 26361, 26442, 26445, 26515 and 26592.
None of the five Hebrew values occurs elsewhere in the corpus, and each fits its report's excavation year on the permit clock. Two more EN/HE permit conflicts in the slice cause no collision and are undecided: 25463 (A2390 / A-2360) and 26228 (S918/2019 / S-819/2019).
Evidence (exact sources: file path / page / figure / frame / coordinates): `ha_en_he_permit_conflicts.csv` (with 3 cross-slice extras: 00480, 01596, 02066; in 02066 the EN A-6171 collides with 02253). Text files: `hadtext/{en,he}/vol-<V>/<id>_*.txt`, first paragraph. I checked 25933 visually on the rendered Hebrew PDF p. 1 (`hadashot/pdf/he/vol-133/25933_*.pdf`: "הרשאה מס' A-8537"), and the Hebrew of every colliding partner (23808, 09556, 25874, 26002, 26092) in the text layer.
Literature check (queries run, result, tag): repo main + `branch_only` grep for "A-8537", "A-7191", "A-8710", "A-6806": no hits. The haesi_features tables store the EN permit only. Web: no erratum. **NEW TO THE LITERATURE.**
Why it might matter: The permit number is the IAA's primary key for an excavation (archives, finds registers, the HA image paths such as `Images//8577-5a.jpg`). Anyone who joins HA to IAA archive or ʿAtiqot records by permit from the English pages will merge Horbat Hanot with Gan Ha-Darom, or Revadim with Modiʿin. Taken with D3's map-reference cards, EN/HE comparison is now shown to catch errors in three different fields.
How to confirm or kill it (with data in hand, or what is missing): Open both PDFs of each id, page 1 (1 minute each). A row is killed if the IAA archive (not reachable here) shows the English number is in fact the right one. That would leave two excavations sharing a permit, which the IAA system should not allow.
Confidence: high (all five)
Touches the Copper Scroll? no (but the project's archive-request tracker keys requests by permit; worth checking that it uses the Hebrew value)

---

FIND CARD
Title (one line): The HA 136 final report on the Nahal Shalva treasure (id 26558) says "bronze coins" held the linen traces. The hoard it summarises (ʿAtiqot 112) contains no bronze coins, only gold and silver, some of it copper-rich alloy
Lane: B1c
What is odd (2–4 sentences): The Nahal Shalva report (Aladjem and Abadi-Reiss, HA 136, 25 Sept 2024) describes a coin cache of "136 silver coins and four gold coins" from beside a woman's skeleton in a reused pit. It then says: "some of the bronze coins retained traces of linen cloth … the fibers seem to represent two linen pouches or purses that held the coin hoard". The full publication it cites (Abadi-Reiss et al. 2023, ʿAtiqot 112:117–155) lists the hoard in Table 1 as 4 aurei, 61 denarii, 41 tetradrachms, 18 tridrachms and 12 drachms, with no bronze. It explains the textile survival by "metal artifacts containing copper". Its own text notes that the Arabian drachms are about 50:50 silver and copper alloy. The only bronze coins at the site are two isolated finds outside the hoard (Domitian/Ascalon and a worn coin). So the HA summary turned a copper-alloy remark into "bronze coins" in the hoard.
Evidence (exact sources: file path / page / figure / frame / coordinates): `hadtext/en/vol-136/26558_na-h-al-shalva.txt`, "Metal Items" and "Textiles" paragraphs. Bucket `atiqot/pdf/vol-112/iss-1/1046_a-treasure-from-nahal-shalva-exquisite-jewelry-and-a-coin-ho.pdf`: "The Coin Hoard" (140 gold and silver coins; Table 1, 136 identified, 4 unidentifiable silver; p. 127 isolated coins: 3 silver, 2 bronze) and the Textile section (copper mineralisation).
Literature check (queries run, result, tag): repo and branch grep "Shalva": not in the project's hoard tables. `hoard_followup_2026-10-24.md` lists no Nahal Shalva row (its window ends in 70 CE; this hoard closes 125–128 CE). Web: not checked beyond the two IAA publications. **NEW TO THE LITERATURE** (a small transmission error).
Why it might matter: The project's hoard rule (Test 1, "Metal") fails any bronze-only hoard and reads metal from HA summaries. A summary that adds bronze to a precious-metal hoard is the kind of error that test can be misled by. This is a second, quieter point beside the date and permit cards: HA "Final Report" summaries can disagree with the full ʿAtiqot article they cite. It is also one of the few gold-and-silver Bar Kokhba-era hoards with a recorded find context (on a body, in a pit, in two linen purses), useful as a context base-rate datum. It is outside the 63 BCE–70 CE window.
How to confirm or kill it (with data in hand, or what is missing): Read ʿAtiqot 112 Table 1 and the Textile section (10 minutes). It is killed if the textile-bearing lumps include coins that ʿAtiqot itself calls bronze. I found none in the text layer.
Confidence: medium
Touches the Copper Scroll? maybe (only via the project's hoard-metal test; not a scroll site)

---

## Dead ends

- "Unique / unparalleled / enigmatic / unclear function" sweep of vols 130–137 (about 100 reports with a hit): mostly routine author phrasing. The strongest candidates, Persian winery at Tel Yavne Area A (25883), Nahal Meshushim dolmen carvings (25709) and Maresha undeciphered marks (26015), are all already discussed in print by their excavators. None was carded.
- ʿUyun Umm el-ʿAzam West (26014): the "Syriac inscription, still being studied" is now read (deaconess Thekla; CMHL entry https://dig.corps-cmhl.huji.ac.il/node/21567, which calls it Palestinian Aramaic; press 2024). It is published, so it was dropped.
- Peace Forest ossuary lid "Yehonat[an bar She]lemya" (25865, HA 132, "never found before on an ossuary"): it is already taken up in Klein et al. 2023, ʿAtiqot 112 (Murabbaʿat Cave II Ptolemaic hoard, p. 82; bucket `atiqot/pdf/vol-112/iss-1/1044_*`), so it is not a loose end.
- "Will be published / in preparation" sweep (12 hits): Dar el-Consul inscribed lamp and dolphin statue (26256), the ʿAkko lead tablet with "indecipherable incisions" (26039) and others are left as leads. I ran no web check for the ʿAkko tablet (budget).
- Khirbat el-Qut (26229): a Bar Kokhba coin hoard "discovered nearby" is known only from "E. Kogan-Zehavi, pers. comm." One web search found nothing (the JPost 120-coin cave hoard is a different find). It is open, not carded. The report also notes an unexcavated tunnel cave, a possible hiding system; I recorded no location.
- Permit-sharing pairs that are genuine: Khirbat Khaur el-Bak (N) and Tel Poran (25740/25738, A-8127, same project, about 350 m apart); robbery-unit blanket permits (A-6979, A-7292, A-8577: e.g. Mount of Olives, documented 2013 under A-8577, a 2019-band number); Bet Ha-Bad St "A-8635-01". These are not errors.
- Republished old excavations (Tiberias 2006, Suwaʿid Humeira 2010, Horbat ʿEmed 2006, Ramat Bet Shemesh 2012–14): the later reports cite the earlier ones or are stubs. Not a "same site under two names" case.
- Publication-lag distribution: the median lag (excavation to HA publication) doubles from 2 years (vols 126–131) to 3–4 years (vols 132–137), and reports 10 or more years old rise from about 5% to 10–14%. A COVID-era backlog explains it, so it is not carded.
- Excavation dated after its publication date: none in 4,667 reports, EN or HE.

## Blocked inputs

- `https://www.hadashot-esi.org.il/Report_Detail_Eng.aspx?id=25933` (and other ids): WebFetch "robots_disallowed". I did not use curl to get around robots. So for these cards the live-page status is not checked; the bucket PDFs (which are the published versions) were used instead.
- CIIP I (Jerusalem) is not in the bucket's text-layer PDF list (`hexview.py pdfs` shows only CIIP III and IV.2). I did not search Drive 05.

## Seed / reproducibility

`python3 -I scripts/parse.py <extracted hadtext dir> parsed.csv`, then `enhe_dates.py`, `enhe_permit.py`, `permcal.py` and `permdup.py` (run from a directory holding `parsed.csv` and `all/hadtext/`). Hebrew text needs the bidi control characters U+200E/F and U+202A–E stripped. The Hebrew permit string is often split by the bidi order ("-8106 ;A").
