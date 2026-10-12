# Phase 4, part E, reader r1: notes

Reader r1 read the owner-approved ʿAtiqot PDFs on the owner's Mac (11–12 October 2026) under the frozen phase-2 plan and the phase-4 scope freeze. Everything here is exploratory. No identification claim is made and no registered result changes.

## What was read

- Assignment, in the frozen order of `../pdfs_needed.csv`: tier T1 (17), tier U (9), tier T3 (3), tier T2 positions 1–60. 89 units in all.
- Every PDF matched its SHA-256 in `../../downloads_2026-10-11.csv`. Every file had a text layer, including the 25 Hebrew ones; no OCR was needed.
- Text was extracted on the Mac into `$HOME/p4text/r1/` (`pdftotext -layout`, `-raw`, and default reading order for Hebrew). Nothing from those files is in the repository except quotes of 12 words or fewer, line spans and hashes.
- The span read for each unit is in `reports.csv` (`text_lines`, `text_sha256`), checked by `scripts/verify_spans.py` (all 85 records, 0 quote problems). Spans are line ranges of `<unit>.raw.txt` (English) or `<unit>.plain.txt` (Hebrew, default pdftotext order). Grep-guided reading: the kw search ran over the whole text, then the passages listed were read.
- 85 units read and coded; 4 dropped as outside the region (`not_read.csv`); none left unread for time.
- Page ranges are the printed pages. Where only running heads were available, the last page given is the last numbered page seen. Three units print no page numbers in their text layer (`pages` left blank or given as the article's own pagination).

## Deviations and choices (exploratory)

- **C1. Report-level zone for units with no single site.** ATQ114-i03 (southern Samaria survey) is a multi-site synthesis; its sites carry their own references and only the six in Z3 are coded. Its report row has `region_zone = multi-site (...)`. The two laboratory studies (ATQ110-i09, ATQ116-i08) are `unlocated (...)`.
- **C2. Grouping of many features with their own references inside one site.** For ATQ50-i14 (ʿEn Gedi pools and channels) and ATQ54-001 (Kh. Kaʿkul installations and tombs) the features lie within about 1 km of one site. They are grouped by class and dating status, with the site's reference (or name zone) and every feature's reference in `feature_subtype`. Separate survey sites (ATQ56-025, ATQ114-i03, ATQ119-i03, ATQ42-i27) get one row per site and class with their own reference.
- **C3. Murabbaʿat Ptolemaic hoard (ATQ112-i04).** Deposition is 171/170 BCE or slightly later; the authors weigh the Sixth Syrian War against the first years of the Maccabean Revolt and give no single answer. This partly precedes the Hasmonean period, so it is coded `unknown`.
- **C4. Bell-shaped winery pits** (ATQ114-i03) are unplastered and interpreted as wineries, so they are `rockcut_installation`, not `cistern`.
- **C5. Finds and specialist reports.** Where a finds report records its find context as an eligible feature (a burial cave, a pool, an aqueduct, a drain), that context is coded once in the finds report's own row, as the brief asks. The same feature may therefore also appear in the site report, which another reader may hold. Rows are not deduplicated (phase-4 plan).
- **C6. Flagged units.** ATQ110-i09 (inkwell residues) and ATQ116-i08 (tefillin skins): the first line names no held cave. Both are laboratory studies of objects from earlier finds and record no feature. Reading stopped after the abstract and introduction so that no cave provenance text from the held areas would be read. They are not held (`held.csv` stays empty) and have no feature rows.
- **C7. Long Hebrew reports coded from the English summary** where the summary describes every area: ATQ101-001s (Horbat ʿAlona), ATQ80-001s (Ras el-ʿAmud), ATQ88-001s (cache of quarrying tools). The others with Hebrew main text were read in Hebrew (ATQ49-i20, ATQ46-i13, ATQ84-065s, ATQ42-i33, ATQ50-i14, ATQ52-049s, ATQ56-025, ATQ91-001s, ATQ98-001s, ATQ42-i27, ATQ48-i15 installations).
- **C8. Map references.** ATQ110-i14 prints 'map ref. 23180/63088' for Mount Zion; it converts to a point about 10 km east, so the easting is taken as misprinted and the unit is located by name in Z4. ATQ98-001 prints '13115/17159' with the northing first (Old Israel Grid); it is read as OIG 17159/13115. ATQ91-001s prints the northing first (633326/215646); the phase-1 parser swaps it. ATQ71-001s gives the excavation at NIG 22249/62679 while its survey table gives six-digit points about 500 m further south; the excavation reference is used for all its rows.
- **C9. Mevoʾot Yeriḥo (ATQ119-i03).** The excavated aqueduct section and its coin foundation deposit have no printed reference; they are placed in Z2 by the gazetteer name Mevo'ot Yeriho. The report-level point (the ʿEin el-ʿAujah spring) falls in Z3.
- **C10. Units of tier U** were located by their map references once read: ATQ52-049s, ATQ43-i03 and ATQ101-001s are in Z4; ATQ101-047 and ATQ101-075 take ATQ101-001s's reference; four were outside the region and dropped.
- **C11. Hedged and typological datings** follow amendment A4: winepresses at Kh. Kaʿkul (author suggests Hasmonean/Herodian) and the En Lavan cave of Early Roman kokhim plan are `yes`; tombs dated only "late Iron Age and Hellenistic" are `unknown`.
- **C12. The jewelry deposits of Building 110** (ATQ121-i06) are coded `hoard_cache` (purposely concealed groups), with the authors' ritual interpretation in the subtype.
- **C13. Wadi el-Ḥaramiya** (ATQ121-i09) lies on the Jerusalem–Nablus road north of Ramallah; by name it is outside the region (INFERENCE, no map reference printed), so its olive press is not coded.

## Protected and held

- No unit was held. No text on Kh. ʿAlmit or the Tell es-Sultan north strip was met. No held-area cave text was read.
- ATQ56-025 cites Kochavi 1972 (the 1968 Emergency Survey) for Kh. Abu Shawan. The citation was read in passing; Kochavi 1972 itself was not sought or opened.
- Murabbaʿat (Nahal Darga) and the ʿEn Gedi mine are outside the held cave areas and were read normally.

## Problems

- None blocking. The text layers of the older Hebrew volumes interleave columns in `-layout` and reverse word order in `-raw`; the default pdftotext order was used for Hebrew reading and hashing.

## Figures worth archiving later (not stored)

- ATQ112-i04, p. 57 Fig. 3: plan of Murabbaʿat Cave II and section of Cavity C (hoard findspot); p. 54 Fig. 1 cave entrances; p. 55 Fig. 2 location map.
- ATQ119-i03: Fig. 2 map of the ʿAujah aqueducts (p. 23); Fig. 4 Installation II plan and sections; Fig. 10 Mevoʾot Yeriḥo aqueduct plan and section; Figs. 15, 29 route maps. Pages of Figs. 4–29 to be checked when archiving.
- ATQ50-i14: Fig. 2 map of the ʿEn Gedi irrigation systems, springs and pools; Plans 1–10 (channel sections, Pools f, g, h, k, Irrigation System 7). English captions pp. 238–239.
- ATQ84-065s: Plan 1, burial cave plan and sections.
- ATQ54-001: Plan 1, Kh. Kaʿkul site plan with installations and tombs (p. 4); Plan 4, columbarium; Plans 13–22, kilns, winepresses and tombs.
- ATQ56-025: Fig. 1 location map; Plan 2 winepress.
- ATQ48-i15: Fig. 1 site map; Fig. 2 location map of Caves D–J (p. 28*); Plans 1–9.
- ATQ85-037: Plan 4 excavation plan and sections; Plan 5 Miqwe 6049.
- ATQ114-i03: Fig. 7 Kh. Jibʿit complex winepress plan and section; Fig. 16 map of the southern Samaria sites (p. 40).
- ATQ98-001s: Fig. 2 map of the En Lavan survey remains.
- ATQ42-i27: Plans 1–2, Abu Tor Caves A and B.
- ATQ106-161: Plan 1, Tel Arza quarry and burial cave (p. 163).

## Proposed changes for the integrator

- Merge these tables with the other part-E readers' tables; dedupe nothing in this phase (plan), but note same-feature pairs: Burial Cave 900 (ATQ88-073, ATQ88-075), Beit Ṣafafa MB cave (ATQ106-047, ATQ106-033), Building 900 finds (ATQ112-i12/i14/i15/i17), the Western Wall tunnels finds (ATQ119-i13, ATQ119-i15) and the site reports they serve.
- `ATQ110-i14`'s misprinted map reference and `ATQ98-001`'s swapped reference (C8) could be added to the phase-4 location notes.
- No change is proposed to `ACTIVE_TEST.md`, the outcome ledger or the atlas data.
