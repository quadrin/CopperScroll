# Phase 4, part E, reader r2: ʿAtiqot PDFs, tier T2 positions 61–135

**What it is.** A reading of 75 ʿAtiqot articles (tier T2, order positions 61–135 of `../pdfs_needed.csv`), coded for the scroll's feature kinds under the frozen phase-2 rules. Exploratory; no identification claim.
**Main result.** All 75 were read; 58 record at least one eligible feature. They give 147 feature rows, all in Z4 (Jerusalem hills): 38 dated in the window, 77 outside it, 32 unknown.
**What stays unknown.** Whether rows repeat features already coded elsewhere (no deduplication in this phase), and the dates of 32 rows. 48 articles give no map reference and are placed by name only.

## Sources and access

- The PDFs were downloaded by the owner on 11 October 2026 into `~/Downloads/IAA portal volumes/phase4/` and read on his Mac with `pdftotext -raw` and `-layout`. Text was kept in `$HOME/p4text/r2/` on the Mac, outside the repository.
- Every PDF's SHA-256 matches `../../downloads_2026-10-11.csv` (`data/mac_pdf_sha256.csv`).
- All 75 PDFs have a text layer. No OCR was needed. One older article (ATQ43-i11, 2002) has an OCR text layer with errors; its quotes were chosen from clean stretches.
- 10 articles are in Hebrew. They were searched in Hebrew and read with their English summaries, which are printed in the same PDF.
- Units read: 75. Held: 0. Not read: 0.

## Method

- Order: tier T2, positions 61–135, as frozen in `pdfs_needed.csv`.
- For each article: title, authors, map reference and the eligible-class keywords (English and Hebrew) were found with a keyword script; every hit was then read in context, with the excavation description and the dating paragraphs.
- Finds and specialist reports were coded only for eligible features they name as the find context (for example a drainage channel, a burial cave, a hoard).
- Map references were converted with `../../../scripts/geo.py` (EPSG:28191 for OIG, EPSG:2039 for NIG). Articles without one were placed by name (`coordinate_source = name only`), as plan §2 allows.
- Each quote (12 words or fewer) was checked against the extracted text on the Mac by `scripts/verify_on_mac.py`. Printed pages come from the PDF page of the quote and the article's running heads (`data/page_map.csv`).
- The text SHA-256 in `reports.csv` is over the raw text of PDF pages 2 to the end (the portal cover page is left out), whitespace collapsed.
- Choices not settled by the plans are in `NOTES.md`.

## Results

Feature rows: 147 (yes 38 / no 77 / unknown 32).

By class, all in Z4_JERUSALEM_HILLS (rows | yes / no / unknown). Z1, Z2 and Z3 have no rows.

| class | rows | yes / no / unknown |
|---|---|---|
| cistern | 15 | 3 / 4 / 8 |
| pool_reservoir | 15 | 2 / 12 / 1 |
| channel_aqueduct | 27 | 7 / 15 / 5 |
| dam | 2 | 2 / 0 / 0 |
| ritual_bath | 8 | 7 / 0 / 1 |
| cave_with_finds | 11 | 4 / 3 / 4 |
| tomb_burial_cave | 34 | 5 / 24 / 5 |
| columbarium_dovecote | 2 | 2 / 0 / 0 |
| rockcut_installation | 31 | 6 / 17 / 8 |
| hoard_cache | 2 | 0 / 2 / 0 |

- Reports: 75, all in Z4. 27 are located by map reference, 48 by name.
- 43 are finds or specialist studies and 32 are excavation or site reports (INFERENCE from the article).
- 17 reports record no eligible feature.
- No row falls outside the region.

## Protected and held

- None of the 75 units concerns a held cave area, the Tell es-Sultan north strip or Kh. ʿAlmit. `held.csv` has its header only.
- The two flagged units (110.9, 116.8) are not in this reader's range.

## Blocked

Nothing was blocked. No portal URL was requested by this reader.

## Files

- `reports.csv`, `features.csv`: phase-2 columns, in the same order.
- `held.csv`, `not_read.csv`: headers only.
- `summary.md`, `summary.json`: generated counts.
- `data/coding_01.jsonl` … `coding_04.jsonl`: the hand coding, one record per unit.
- `data/page_map.csv`, `data/mac_text.csv`, `data/mac_quote_pages.csv`, `data/mac_pdf_sha256.csv`: page mapping and checks made on the Mac.
- `scripts/build_reading_r2.py` builds the tables. `scripts/export_quotes.py` and `scripts/verify_on_mac.py` check the quotes on the Mac.
- `tests/test_reading_r2.py`.
- `NOTES.md`: choices, figures to archive later and proposed changes.
