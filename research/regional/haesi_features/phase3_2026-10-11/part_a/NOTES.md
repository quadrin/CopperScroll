# HA-ESI phase 3, part A: notes (HA Hebrew series 1961–1979)

The part-A reader wrote these notes on 11 October 2026, in branch `worktree-agent-aef21bb9f80551830`.

**Rules used.** The rules are those of the phase-2 frozen plan (`../../phase2_2026-10-10/PLAN.md`, SHA-256 `5b1a5c08…b3be`) with amendments A1–A4. The scope is the phase-3 freeze (`../PLAN.md`, commit 4d8325e). Nothing in either was changed.

**Outputs:**
- `reports.csv` and `features.csv`, in the phase-2 column order.
- `screen.csv`: every heading, with its decision and the reason.
- `candidates_checkoff.csv`.
- `summary.md` and `summary.json`.

**Rebuilding.** `scripts/build_part_a.py` regenerates all of these from `data/`. The tests are in `tests/test_part_a.py` (14 tests, all passing).

**Labels.** EVIDENCE means the volume says it. INFERENCE means the reader's reasoning. CLAIM means an author's assertion without a field record. This part makes no identification claim.

## What was read

**Sources.** The sources were the 50 part-A files in `~/Downloads/IAA portal volumes/` on the owner's Mac. Each file's SHA-256 matched `../partition.csv` (all 50 OK; see `data/local_sources.csv`).
- Only these PDFs were listed (filter `IAA_HA_*`) and opened. Nothing else in the folder was touched.
- Text was extracted on the Mac with `pdftotext -raw` and `-layout`. It stays in `~/p3a_scratch/`, outside `mnt/` and outside the repository.
- The Mac scripts are copied in `scripts/mac/`. Their bidi control characters are written there as `\u` escapes.

**Heading screen.**
- The portal tables of contents give 1,651 items (`data/portal_toc_items.csv`).
- Another 28 headings were found only in the text, which makes 1,679 screen rows.
- Each heading was located in the text layer. 1,114 were found by the full title, 437 by one title word and 52 by the title after a colon. 48 were not found; each of these has an explicit decision.
- Decisions:

  | Decision | Rows |
  |---|---|
  | READ | 187 |
  | READ0 | 50 |
  | TIER1 | 1 |
  | COMPOSITE | 14 |
  | OUT_TITLE | 1,289 |
  | OUT_REF | 36 |
  | OUT_NAMESAKE | 8 |
  | NONFIELD | 88 |
  | HELD | 1 |
  | STRIP_CHECK | 1 |
  | BORDER | 3 |
  | UNLOC | 1 |

- 571 decisions are explicit, in `data/screen_decisions_b01–b19.tsv`. 1,108 are defaults, for items with no gazetteer term in the title, a located heading and no map reference that falls in a zone under either number order. The tests check that rule.
- 176 of the default items had incidental body gazetteer hits. These were seen in the per-volume signal lists but are not recorded one by one.

**Reports coded.**
- 251 reports were coded, all in the region:

  | Zone | Reports |
  |---|---|
  | Z1 | 14 |
  | Z2 | 22 |
  | Z3 | 29 |
  | Z4 | 184 |
  | MULTI | 2 |

- 59 of these reports have no eligible feature.
- There are 364 feature rows. Dated in the window: yes 152, no 91, unknown 121.
- Span hashes and quotes were checked on the Mac by hash only (`scripts/span_jobs.py` → `scripts/mac/batch_spans.py` → `scripts/prep_data.py`).
  - Every quote was found.
  - In five reports one quote was found only in the layout text: HA26-024, HA38-015, HA50-009, HA51-025 and HA65-031.
  - `data/local_spans.csv` keeps the quote hashes, and a test fails if any quote changes after that check.

**Phase-1 screen candidates.** There are 215 candidates in the part-A volumes. 180 were read and coded, 34 are outside the region and 1 is a strip check (HA 43 item 21). Every candidate's portal TOC title matches its row (`candidates_checkoff.csv`).

**Volumes not in part A.** HA 40, 45 and 59–60 were read in phase 2 and are not part-A files. HA 44 is not in the portal download list and was not sought.

| HA vol. (year) | PDF pp. | headings | coded reports (feature rows) | PDF pages of coded reports | mid-volume pages without text |
|---|---|---|---|---|---|
| 1 (1961) | 19 | 13 | 1 (2) | 17-18 | - |
| 2–3 (1962) | 56 | 41 | 4 (7) | 21-23, 37-38, 48, 50 | - |
| 4 (1962) | 21 | 15 | 3 (4) | 4-5, 7-8, 17-18 | - |
| 5 (1963) | 30 | 31 | 4 (6) | 4-6, 15-16, 24, 28-29 | 2 |
| 6 (1963) | 27 | 18 | 3 (4) | 14, 18-19, 22-23 | - |
| 7 (1963) | 32 | 24 | 1 (1) | 27 | 31 |
| 8 (1963) | 33 | 18 | 1 (1) | 8-11 | - |
| 9 (1964) | 28 | 22 | 2 (1) | 1-2, 19 | - |
| 10 (1964) | 30 | 28 | 3 (6) | 5-9, 13-14 | - |
| 11 (1964) | 30 | 33 | 0 (0) | - | - |
| 12 (1964) | 28 | 14 | 0 (0) | - | - |
| 13 (1965) | 23 | 18 | 3 (4) | 1-4, 9-11 | - |
| 14 (1965) | 24 | 26 | 3 (6) | 14-15, 18-22 | - |
| 15 (1965) | 24 | 21 | 0 (0) | - | 23 |
| 16 (1965) | 29 | 24 | 2 (3) | 6, 20-21 | - |
| 17 (1966) | 36 | 31 | 0 (0) | - | 13 |
| 18–19 (1966) | 29 | 32 | 3 (5) | 11-12, 26-27 | 7 |
| 20 (1966) | 30 | 24 | 0 (0) | - | 29 |
| 21 (1967) | 34 | 32 | 1 (1) | 11 | 33 |
| 22–23 (1967) | 38 | 28 | 1 (1) | 25 | - |
| 24 (1967) | 44 | 24 | 3 (2) | 17-19, 34-35 | - |
| 25 (1968) | 41 | 25 | 4 (4) | 17-21, 24, 29-31 | - |
| 26 (1968) | 49 | 12 | 3 (4) | 22-42 | 6, 18, 23, 32, 39 |
| 27 (1968) | 41 | 38 | 10 (9) | 2-5, 18-24 | - |
| 28–29 (1969) | 53 | 46 | 7 (8) | 26-30, 37, 40-41 | - |
| 30 (1969) | 37 | 26 | 8 (14) | 20-27, 29-32 | - |
| 31–32 (1969) | 42 | 47 | 9 (10) | 14-15, 18-21, 30-31 | - |
| 33 (1970) | 29 | 26 | 6 (4) | 1-7, 9, 27 | - |
| 34–35 (1970) | 44 | 35 | 8 (13) | 13-22 | - |
| 36 (1970) | 29 | 27 | 8 (6) | 12-17 | - |
| 37 (1971) | 41 | 32 | 6 (13) | 20-22, 24, 26-27 | 34 |
| 38 (1971) | 39 | 39 | 10 (23) | 15-22 | - |
| 39 (1971) | 41 | 32 | 5 (7) | 22-24 | 40 |
| 41–42 (1972) | 56 | 46 | 11 (15) | 19-26, 38-39 | 51, 54 |
| 43 (1972) | 39 | 43 | 8 (10) | 10-12, 14-18 | 37 |
| 46 (1973) | 31 | 28 | 7 (10) | 10-16 | 29 |
| 47 (1973) | 41 | 38 | 5 (4) | 13-14, 18-20 | 38 |
| 48–49 (1974) | 103 | 47 | 8 (24) | 49-51, 65-72 | 101 |
| 50 (1974) | 35 | 29 | 6 (9) | 10-16, 30 | - |
| 51–52 (1974) | 49 | 38 | 5 (6) | 24-27 | 47 |
| 53 (1975) | 44 | 38 | 7 (9) | 18-24 | 42 |
| 54–55 (1975) | 53 | 41 | 10 (26) | 16-27 | 51 |
| 56 (1975) | 60 | 43 | 6 (8) | 22-23, 31-32, 54-55 | 58 |
| 57–58 (1976) | 53 | 50 | 10 (10) | 24-25, 29-34 | - |
| 61–62 (1977) | 68 | 69 | 11 (8) | 20, 28-33 | - |
| 63–64 (1977) | 87 | 64 | 5 (5) | 49-52 | - |
| 65–66 (1978) | 73 | 57 | 9 (13) | 29-43 | 23 |
| 67–68 (1978) | 81 | 62 | 10 (24) | 35-38, 43-51 | - |
| 69–71 (1979) | 90 | 57 | 8 (11) | 46-47, 56-59, 83-84 | 88 |
| 72 (1979) | 48 | 27 | 3 (3) | 29-31 | 45, 46 |

All pages with a text layer were screened for headings. The "PDF pages of coded reports" column lists the pages read in full for coding. Printed page numbers are in each report row.

## Protected items

- **HA 28–29 (Tier 1).**
  - The reader read it first, extraction only, and committed `tier1_HA28-29_extraction.md` alone (aa17f58) before any coding from the volume.
  - The arrival items, `MANIFEST.md` predictions and `research/assessments/kohlit_chain/chain.json` were not opened at any point.
- **Kh. ʿAlmit.**
  - No IAA notice on the site occurs in part A. HA 26 (Kallai, central Ephraim and Benjamin survey) names it twice in passing. These passages are extracted in `tier1_kh_almit_extraction.md`, committed alone as 2b2a4bc.
  - **Ordering deviation:** the HA26-019 coding row, committed earlier in ac45765, lists "Almit" among the sites named. No feature was coded from these passages. The integrator decides whether this counts as exposure.
- **Held cave areas (plan §7).**
  - HA 26 item 7.1, the caves sub-section of team 6 (printed p. 28, PDF p. 34), was read to its first lines only.
  - Built sites at the Wadi Qelt outlet and Jericho were read normally: Tulul Abu el-Alayiq (several seasons), Kypros, the Wadi Qelt mill and Tell es-Samarat.
  - Cave reports outside the held stretches were also read normally: Bar-Adon's HA 36 caves (Ein Feshkha to En Gedi), Mearat Khareitun and the En Gedi area.
- **Tell es-Sultan north strip.**
  - HA 43 item 21 is a burial cave in the abandoned refugee camp north of Jericho, west of the ancient synagogue. It is STRIP_CHECK: citation only, not coded.
  - **Exposure:** the reader displayed the four-line notice in full before the strip question was raised.
- **Not sought.** The L-656 field file and IAA Archive cave records.

## Deviations and judgement calls

1. **Map-reference number order.** `pdftotext -raw` often gives the two numbers of an unslashed reference northing first.
   - Every reference was tested in both orders against the place the text describes. It is stored as "E/N", with the printed form in `location_note`.
   - Early "first number = E" readings were corrected: el-Bira (now Z4, read), Shuʿfat, and 1663/1464, which belongs to the Migdal Tsedeq site, not Radana.
   - Eight coastal-plain items whose reversed order would fall in Z2/Z3 have explicit OUT_REF decisions (b19).
2. **Zoning by name outside the gazetteer** (exploratory "by eye"; marked in each screen note).
   - Places: Gibeon (HA 31–32, HA 69–71), Beit Neqofa, Talpiyyot, Mei Naftoah, Sheikh Jarrah, En Hemed, Beit Sahur, Kh. Umm Zuqum (by Auja et-Tahta), Rujm Abu Muhayir (west of Fasael), Givʿat ha-Mivtar and Abu Ghosh spelling variants.
   - Kh. Radana is zoned Z4 by the Ramallah gazetteer name, since the text places it by Ramallah.
3. **Classes.**
   - "מקווה/מקווי מים" is coded ritual_bath (INFERENCE: the label decides).
   - Drains and drainage channels are channel_aqueduct, as in phase 2.
   - There is one row per report, class and site/date group; rows split by date as in phase 2.
   - Funerary monuments are tomb_burial_cave. Fortifications, walls and buildings are not coded.
4. **Dating.**
   - A4 is applied: hedged dates follow the named period.
   - "Mishnah and Talmud period" overlaps the window only partly, so it is coded unknown.
   - "Byzantine, perhaps used earlier" is unknown.
   - "Probably Second Temple, perhaps Byzantine" is unknown (two alternative periods).
5. **MULTI reports.** HA26-019 and HA26-024 are regional surveys spanning zones. The report row has `region_zone` MULTI, and each feature carries its own zone by name (`coordinate_source` "feature zone by name").
6. **Body-text gazetteer hits.** These leave out 15 common Hebrew words (`NOISE` in `scripts/mac/signals.py`: גילה, ביתר, דרגה, קדר, תומר, נעמה, מוצא, פסגות, מנחת, רימונים, סככה, עוגה, רמות, גבע, מלחה). Titles were screened with the full gazetteer (`scripts/screen_titles.py`).
7. **Headings missing from the portal TOC.**
   - HA 3 is bound in the HA 2–3 file (PDF pp. 31–56, items x1–x21).
   - Indexes: HA 12 x1 and HA 25 x1.
   - HA 41–42 x1 is the En Gedi Second Temple tombs sub-heading.
   - HA 48–49 x1 covers printed pp. 77–98, all outside the region.
   - Composite sub-items are numbered n.1.
8. **Text layer.**
   - No Hebrew OCR was re-run, and unreadable words were not guessed.
   - Badly garbled pages: HA 47 p. 14 and HA 41–42 p. 24. Other garbled names, numbers and map references are noted in the report rows.
   - HA 50 PDF pp. 16–17 repeat printed p. 15.
   - HA 41–42 printed p. 49 (PDF p. 51) has no text layer. It is part of a conservation item (NONFIELD) and was not read.
9. **Repeated seasons.** Successive seasons at Tulul Abu el-Alayiq, Herodium, the Jewish Quarter, the Ein Samiya cemetery, Kypros and En Gedi repeat some features. These are not deduplicated in the rows. Same-feature notes are kept: HA07-027/HA06-016 (Jason's Tomb), HA14-016/HA13-001 (En Gedi pool), and HA72-028, which is the same campaign as phase-2 ESI02-057.

## Not read, and limits

- **Mid-volume pages with no text layer** (listed in the table above and in `data/local_sources.csv`). In HA 26, PDF pp. 23, 32 and 39 fall inside coded surveys, but the prose runs on across them (INFERENCE: unnumbered plates). The plates were not viewed. Under the lane rule no page images were made or archived, so maps and photographs on them are unarchived.
- **BORDER and UNLOC items,** listed and not coded:
  - Ein Arub (HA 27 item 17; HA 48–49 item 44): a hiding complex used in the First Revolt and the Bar Kokhba war, at about 31.62 N on the Z4 edge.
  - Ai / Kh. Hudriya and the "ואדי עוגיה" tombs (HA 28–29 item 37).
  - Roman road Netiv ha-Lamed-He to Mevo Betar (HA 12 item 3).
- **Kh. Hadatha (HA 6 item 12).** It is OUT_TITLE on the reader's INFERENCE that it is el-Haditha near Lod, following Abel's Adithaim. The text gives no map reference.

## Proposed changes for the integrator (not made here)

- Merge the part-A `reports.csv` and `features.csv` into the phase-3 tables. Treat `region_zone` MULTI on report rows as in the region, with the zones taken from the features.
- Compare `tier1_HA28-29_extraction.md` and `tier1_kh_almit_extraction.md` under the arrival procedure, and rule on the ʿAlmit ordering deviation.
- Decide on Ein Arub against the Z4 southern edge (31.62 N).
- Deduplicate repeated-season features by field campaign before any count.
- Add the HA 26 plates (PDF pp. 6, 18, 23, 32, 39), which are probably survey maps, to the archive backfill queue, if the owner permits page images.
- No shared status file was edited. ACTIVE_TEST "Last session" line, proposed: **obtained**: HA 1961–1979 portal volumes screened whole (1,679 headings), 251 in-region reports coded (364 feature rows), 215 phase-1 candidates checked off, Tier-1 extractions for HA 28–29 and the Kh. ʿAlmit mentions.
