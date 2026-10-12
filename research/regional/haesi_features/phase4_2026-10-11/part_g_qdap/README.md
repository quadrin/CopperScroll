# Phase 4, part G: QDAP, vols 1–14 (1931–1950)

**What it is.** A screen and coding of the Quarterly of the Department of Antiquities in Palestine for recorded examples of the scroll's feature kinds in the four phase-2 zones, under the frozen phase-4 scope (commit b002e03) and the phase-2 rules.
**Main result.** 71 in-region units were read and coded. They give 88 feature rows, 75 of them in the Jerusalem hills (Z4). Only 8 rows are dated in the window, all in Z4; none in the Jordan valley, the Judean desert or Gerizim.
**What stays unknown.** Vol. 6 nos. 3–4 (Mefjer II, a St Stephen's Gate note and the 1935-6 round-up) and vol. 10 nos. 2–3 could not be read. No in-region unit gives a grid reference, so every row is placed by name only. Four Tell es-Sultan units are held.

## Sources and access

- Internet Archive collection `pub_quarterly-department-of-antiquities-palestine`: 45 items. Text came from the hOCR search text with its page index; the DjVu XML was used where that was refused. OCR text stayed in the scratch folder.
- Printed page numbers come from the running heads in the OCR, not from the archive.org page-number files, which were one leaf off.
- Not read: vol. 6 nos. 3–4 (every OCR file refused, HTTP 500); vol. 10 nos. 2–3 (not on archive.org); the text of Hill's "Autonomous Shekels of Tyre" in vol. 7 (not found in the item; a coin study). Vol. 7 is otherwise present, against the brief.
- British Library EAP1544-1-1-54 to -79 are page images only. They were not OCRed. `NOTES.md` lists what each record could fill; -63 and -69 probably hold vol. 6 and vol. 10.

## Method

- Every article title and every round-up or Notes site paragraph was screened against the phase-2 gazetteer (screen S-G). Mandate spellings the gazetteer missed were added by eye (screen S-MAN, exploratory; listed in `NOTES.md`).
- Each unit was checked against the held cave areas, the Tell es-Sultan north strip and the Kh. ʿAlmit rule before reading.
- Reading order: T1, then T2, then T3; within a tier, ascending sha256 of the unit id. The stop rule was not reached. One unit (the Silwan shekel hoard) was added late by an exploratory check and read last.
- Long units were read with their opening pages in full and then every paragraph with an eligible-class keyword. Each record says how it was read. The SHA-256 covers the whole span, whitespace collapsed.
- Classes, the in-window rule and the columns are the phase-2 ones. Rows carry `exposure_at_freeze = unexposed at freeze`.

## Results

Units screened: 346 (IN 71, HELD 4, NO_TEXT 4, NOT_FIELD 83, OUT_REGION 182, OUT_TITLE 2).
Units read and coded: 71 (T1 20, T2 42, T3 9). 22 of them have no eligible feature.
Feature rows: 88 (yes 8, no 44, unknown 36)
Held or protected: 4

By class (rows, then dated in window yes / no / unknown):

| class | rows | yes | no | unknown |
|---|---|---|---|---|
| cistern | 16 | 0 | 9 | 7 |
| pool_reservoir | 6 | 0 | 3 | 3 |
| channel_aqueduct | 25 | 2 | 11 | 12 |
| dam | 0 | 0 | 0 | 0 |
| ritual_bath | 2 | 0 | 1 | 1 |
| cave_with_finds | 7 | 1 | 4 | 2 |
| tomb_burial_cave | 22 | 3 | 11 | 8 |
| columbarium_dovecote | 0 | 0 | 0 | 0 |
| rockcut_installation | 8 | 1 | 4 | 3 |
| hoard_cache | 2 | 1 | 1 | 0 |

By zone:

| zone | rows | yes | no | unknown |
|---|---|---|---|---|
| Z1_GERIZIM | 0 | 0 | 0 | 0 |
| Z2_JORDAN_VALLEY | 6 | 0 | 3 | 3 |
| Z3_JUDEAN_DESERT | 7 | 0 | 5 | 2 |
| Z4_JERUSALEM_HILLS | 75 | 8 | 36 | 31 |

The eight rows dated in the window are listed in `summary.md`. They are a Tyropoeon drain, the Ramat Rahel and Waʿr Abu es-Safa kokhim tombs, a Kidron kokhim tomb, the ʿAin Karim stepped chamber, the Mahneh Yehudah quarry, a Tenth Legion drain in the Citadel and the Silwan shekel hoard (findspot from a dealer). Same-site units are not deduplicated.

## Protected and held

- Four Tell es-Sultan units are citation only (`held.csv`); three have `protected_strip = yes`. One is a one-line 1931 notes entry.
- Deviation D1: a paragraph-start screen showed short opening fragments of two held Jericho units. Nothing was coded from them (`NOTES.md`).
- No cave in the held cave areas was met.
- Kh. ʿAlmit: two passing mentions in Avi-Yonah's "Map of Roman Palestine" (QDAP 5, pp. 147, 189), in `tier1_kh_almit_extraction.md`.

## Blocked

All returned HTTP 500 from archive.org on three attempts:

- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1937_6_3-4/quarterly-department-of-antiquities-palestine_1937_6_3-4_djvu.txt` and the item's `_hocr_searchtext.txt.gz`, `_hocr_pageindex.json.gz` and `_djvu.xml`
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1944_11_1-2/quarterly-department-of-antiquities-palestine_1944_11_1-2_djvu.txt` (search text obtained later and used)
- `https://archive.org/download/quarterly-department-of-antiquities-palestine_1934_4_1-2/quarterly-department-of-antiquities-palestine_1934_4_1-2_hocr_searchtext.txt.gz` (DjVu XML used)
- index items 1932_1_index, 1934_3_index and 1945_11_index (partly; no units)

`https://eap.bl.uk/archive-file/EAP1544-1-1-54` returned HTTP 202 with an empty body; the IIIF manifests opened.

## Files

- `reports.csv`, `features.csv`: coded units and feature rows, phase-2 columns.
- `screen.csv`: every screened unit with its decision, tier and reading position.
- `held.csv`: held units, citation and first line only.
- `summary.md`, `summary.json`: generated counts.
- `tier1_kh_almit_extraction.md`: the Kh. ʿAlmit facts.
- `data/units/*.json`: one coding record per read unit (span, hash, quotes). `data/screen_units.tsv`, `data/held_units.tsv`: hand screen and held lists.
- `scripts/build_part_g.py`: builds the tables. `tests/test_part_g.py`: checks columns, zones, held units, reading order and these counts.
- `NOTES.md`: access log, choices, figures to archive, proposed changes.
