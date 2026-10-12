# Phase 4, part F: IAA Reports nos. 2–6 and 8–78 (screen and PDF list)

**What it is.** A screen of every IAA Reports monograph on the IAA portal against the phase-2 gazetteer, with the list of full-text PDFs needed to read the in-region units.
**Main result.** 12 monographs lie in the region, all in the Jerusalem hills (Z4): 5 in tier T2 and 7 in tier T3. One more (no. 5, Cave of the Warrior) is a held cave and is not read. No unit is read yet.
**What stays unknown.** Every feature count from these 12 volumes. Reading waits for the owner's approval to download the PDFs.

## Sources and access

- Series pages fetched from the workspace with curl: `https://publications.iaa.org.il/iaareports/` and its `index.2.html` and `index.3.html`. They list 84 portal items for nos. 1–78 (nos. 34, 51, 58, 66 and 74 come in parts).
- Landing pages: all 82 items except nos. 1 and 7, one at a time, 3.5 s apart, on 12 October 2026 UTC (11 October in Los Angeles). The first pass returned HTTP 301 (the URLs need a trailing slash) and gave no content; the second pass returned HTTP 200 for all 82. Hashes are in `data/fetched_pages.csv`.
- The portal does not split a volume into chapter pages. Each landing page lists the full-text PDF and the chapter PDFs as files. All are recorded in `data/volumes.csv` and `data/files.csv`. Chapter files listed: 1103.
- No PDF or `viewcontent` URL was fetched. Landing pages show file sizes but not page counts, so `pages` is blank.
- Nos. 1 and 7 were already read by the tombs lane (`research/regional/tombs`, sources AK and HK). They are listed as already read and were not fetched again.
- Not read: all 12 candidate volumes (waiting for download approval).

## Method

- Rules: the phase-2 frozen plan (`../../phase2_2026-10-10/PLAN.md`, SHA-256 `5b1a5c08…b3be`) with amendments A1–A4, under the phase-4 scope freeze (`../PLAN.md`, commit b002e03).
- Titles and chapter titles were screened with the phase-2 normalisation (A1) and gazetteer plus the A3 name variants (`scripts/common_f.py`, which reuses `phase2/scripts/common.py`). Abstract hits were recorded as signals only.
- No landing page gives a map reference. Candidates are placed by name (`coordinate_source = name only`). Tiers follow plan §3.4: T1 = Z1–Z3 or a region-wide term, T2 = Z4 not starting "Jerusalem", T3 = Z4 starting "Jerusalem".
- Unit id: `IAAR<no>-<slug>`; a part number is written `p`, for example `IAAR66p1-…`. Each volume reports one site, so each volume is one unit. Order within a tier is ascending SHA-256 of the unit id.

## Results

- Portal items screened: 84
- Candidates in the region: 12 (all Z4)
- Out of region by title: 69
- Already read elsewhere: 2 (nos. 1 and 7)
- Held: 1 (no. 5)
- Units read: 0
- Feature rows: 0. There are no counts by class and zone yet; `reports.csv` and `features.csv` hold the phase-2 headers only.

PDFs needed (`pdfs_needed.csv`), 467.5 MB in all:

- T1: 0 PDF
- T2: 5 PDF (148.3 MB): nos. 39 Tel Moẓa, 3 Manaḥat, 19 Abu Ghosh, 69 Kathisma, 12 Efrata, in that order
- T3: 7 PDF (319.2 MB): nos. 67, 66/2, 66/3, 63, 64, 52, 66/1, in that order (Western Wall Plaza I–III; Giv‘ati Parking Lot I and II parts 1–3)

Other volumes already met in the repository: no. 17 (pp. 42–45, columbaria lane), no. 36 (ch. 4 through indexed text), no. 45 (cited second-hand), no. 52 (listed as a target). Nos. 17, 36 and 45 are outside the region; no. 52 is a T3 candidate and has not been read.

## Protected and held

- Held cave: no. 5, Schick 1998, *The Cave of the Warrior*. Its first line places the cave in "the survey of the caves in the Jericho area". It is held under plan §7 (Jericho escarpment) and is not read and not in the PDF list. See `held.csv`.
- Tell es-Sultan north strip: no unit.
- Kh. ʿAlmit: no unit, so there is no `tier1_kh_almit_extraction.md`.

## Blocked

Nothing was blocked. All landing pages returned HTTP 200 once the trailing slash was added. No PDF was requested.

## Files

| File | What it holds |
|---|---|
| `screen.csv` | Every portal item: unit id, title, authors, portal year, landing and PDF URLs, size, title, chapter and abstract hits, decision, zone, tier, reason |
| `pdfs_needed.csv` | The 12 candidates in reading order, with exact PDF URLs, size, zone, tier and position |
| `held.csv` | The held unit: citation, first line, held area |
| `reports.csv`, `features.csv` | Phase-2 headers only (nothing read yet) |
| `summary.json` | The counts above |
| `data/volumes.csv`, `data/files.csv`, `data/fetched_pages.csv` | Landing-page metadata (no abstracts), every listed file, and every page fetched with its hash |
| `scripts/` | `parse_series.py`, `parse_landing.py`, `prep_data.py` (saved pages → data), `common_f.py` (gazetteer), `build_part_f.py` (data → tables) |
| `tests/test_part_f.py` | Column order, zone and tier rule, held units not coded, PDF order, README counts, rebuild |
| `NOTES.md` | Exposure, choices and deviations, figures, proposed changes |
