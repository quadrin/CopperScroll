# Phase 4, part F reading pass (reader r4): IAA Reports monographs

**What it is.** The coded reading of the 12 IAA Reports monographs in part F's PDF list (T2 then T3), from the owner-approved PDFs on his Mac, under the frozen phase-2 plan and the phase-4 scope freeze.
**Main result.** All 12 units lie in Z4 (Jerusalem hills) and all were read. They give 52 feature rows; 12 are dated by the report to the window (Hasmonean to 135 CE), all in Jerusalem: the Western Wall Plaza and the Giv‘ati Parking Lot.
**What stays unknown.** Two volumes were read only in part, because the portal full-text PDFs are truncated: Manaḥat (Chapter 14, the miqweh, is missing) and Efrata (Appendix 1, the Byzantine winepresses, is missing). Finds catalogues were searched for hoards and deposits, not read line by line.

## Sources and access

- PDFs: `~/Downloads/IAA portal volumes/phase4/<unit_id>.pdf` on the owner's Mac. Each SHA-256 matches `../../downloads_2026-10-11.csv`. Only these 12 files were opened.
- Text: `pdftotext -raw` and `-layout` into `~/p4text/r4/` (outside `mnt`; not in the repository).
- No text layer: IAAR3 (Manaḥat) and IAAR12 (Efrata) are scans. Both are English, so they were read by `tesseract` (eng, 300 dpi). Image-only pages inside the other volumes' architecture chapters were also read by OCR.
- Truncated PDFs:
  - IAAR3: the full-text PDF ends at p. 69 (Chapter 5). Chapters 6–16 and the appendices are not in it, including Chapter 14, "The Miqweh (Ritual Bath)": https://publications.iaa.org.il/cgi/viewcontent.cgi?filename=15&article=1071&context=iaareports&type=additional
  - IAAR12: the full-text PDF ends in Chapter 4 (p. 77). Chapters 5–9 and the appendices are not in it, including Appendix 1, "Byzantine Winepresses": https://publications.iaa.org.il/cgi/viewcontent.cgi?filename=11&article=1064&context=iaareports&type=additional
  - Both are listed in `not_read.csv` as "read in part".
- Pages read for each unit are in `reports.csv` (`pages`). The PDF pages hashed are in `data/spans.csv`.

## Method

- Rules: phase-2 plan `../../../phase2_2026-10-10/PLAN.md` (SHA-256 `5b1a5c08…b3be`), amendments A1–A4, phase-4 `../../PLAN.md`. No rule was changed.
- Order: T2 positions 1–5, then T3 positions 1–7, as in `../pdfs_needed.csv`.
- Each volume is one unit (one site).
- Reading:
  - The stratigraphy and architecture chapters were coded by site and feature.
  - Short chapters were read in full.
  - Long chapters were read at every passage that names a feature of an eligible class: Kathisma Chapters 2–3, Western Wall Plaza I Chapter 3, Giv‘ati II Chapters 2 and 12.
  - Finds chapters were searched for hoards, caches and deposits.
- Rows: one row per unit, class and feature group. A class has more than one row in a unit where the dating status or the feature group differs; `feature_site` tells them apart. In `features.csv`, `pages` gives the printed pages of the feature.
- Location: the printed map reference, converted with `geo.py`. Where a volume prints none, the unit is placed by name (`coordinate_source = name only`).
- Quotes: each is 12 words or fewer, and each was checked verbatim against the extracted text on the Mac (`data/spans.csv`).
- Hash: the text span read was hashed with whitespace collapsed.
- Labels: the excavator's function label is kept in `feature_subtype`. Class and zone assignments are INFERENCE. The choices made while reading are in `NOTES.md`.

## Results

Units read: 12 (5 T2, 7 T3; 2 of them in part). All are in Z4_JERUSALEM_HILLS. Every unit has at least one feature row.

Feature rows: 52 (yes 12 / no 29 / unknown 11)

| class | zone | rows | yes | no | unknown |
|---|---|---|---|---|---|
| cave_with_finds | Z4_JERUSALEM_HILLS | 1 | 0 | 0 | 1 |
| channel_aqueduct | Z4_JERUSALEM_HILLS | 9 | 2 | 5 | 2 |
| cistern | Z4_JERUSALEM_HILLS | 6 | 2 | 3 | 1 |
| hoard_cache | Z4_JERUSALEM_HILLS | 7 | 0 | 7 | 0 |
| pool_reservoir | Z4_JERUSALEM_HILLS | 4 | 1 | 3 | 0 |
| ritual_bath | Z4_JERUSALEM_HILLS | 4 | 3 | 0 | 1 |
| rockcut_installation | Z4_JERUSALEM_HILLS | 18 | 4 | 8 | 6 |
| tomb_burial_cave | Z4_JERUSALEM_HILLS | 3 | 0 | 3 | 0 |

The 12 in-window rows, by unit:

- **IAAR63 (Western Wall Plaza I), 5 rows:**
  - Cistern 6170;
  - Miqveh 2022 and Installation 2050;
  - Installation 5336 and Quarry 8170;
  - the Low-Level Aqueduct;
  - the Cardo drainage channels, dated "before 130 CE".
- **IAAR67 (Western Wall Plaza III), 2 rows:**
  - the Early Roman Quarries 8170 and 9588;
  - the quarrying for the Cardo, dated to the "first third of the second century CE".
- **IAAR52 (Giv‘ati I), 4 rows:** all from Stratum VII:
  - Cistern 702;
  - Miqva'ot 704 and 719;
  - Bath 714;
  - Shaft 728.
- **IAAR66p1 (Giv‘ati II, part 1), 1 row:** the Early Roman miqveh under Reservoir 6388.

Rows are not deduplicated. The same feature can appear in two volumes of one excavation, and in the HA-ESI rows of `../../../merged_2026-10-11/` (see `NOTES.md`). A count is a count of rows, not of features on the ground. Nothing here identifies a place.

## Protected and held

- No unit is in a held cave area. `held.csv` has the header only. Part F's held unit (IAAR5, Cave of the Warrior) was not in the list and was not opened.
- Tell es-Sultan north strip: no unit.
- Kh. ʿAlmit: no unit, so there is no `tier1_kh_almit_extraction.md`.
- No held text was read.

## Blocked

Nothing was blocked. No web request was made. The two missing chapter PDFs listed under Sources were not requested, because this pass reads only the downloaded files.

## Files

| File | What it holds |
|---|---|
| `reports.csv`, `features.csv` | The coded units and feature rows (phase-2 columns and order) |
| `held.csv` | Held units (none; header only) |
| `not_read.csv` | Units read in part, with the parts not read |
| `summary.json` | Counts by class, zone and dating status |
| `data/coding.json` | The hand coding: one record per unit |
| `data/spans.csv` | For each unit: PDF SHA-256, PDF pages hashed, OCR pages used, text SHA-256 and quote checks |
| `scripts/build_reading.py` | Builds the tables from `data/` (deterministic) |
| `tests/test_reading.py` | Column order, reading order, zones recomputed from coordinates, no held unit coded, quote and span checks, README counts and rebuild |
| `NOTES.md` | Choices and deviations, units read in part, probable duplicates with the merged inventory, figures to archive, and proposed changes |
