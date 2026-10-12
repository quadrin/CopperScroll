# Phase 4, part I: the Annual of the Department of Antiquities of Jordan (ADAJ)

**What it is.** A screen of every ADAJ title (vols 1-62, 1951-2025) and of every site heading in the news and round-up sections of vols 1-12/13 (1951-1968, the years of Jordanian administration of the West Bank), with every unit in the region read and coded under the phase-2 frozen plan. Exploratory; no identification claim.
**Main result.** 1,869 titles and headings screened; 78 units in the region; 77 read and coded, giving 76 feature rows in the region (dated in the window: yes 14, no 37, unknown 25). Nine held or protected items were cited only. Nothing was left unread by the stop rule.
**What stays unknown.** Rows are per unit and class, and several finds are reported twice (same-feature rows are kept), so these are not counts of features on the ground. Most rows are undated or dated outside the window. Arabic pages were read from images without OCR, and later volumes (14-62) were screened by title only.

README counts: units coded 77; feature rows 76 (yes 14 / no 37 / unknown 25); held or protected 9; screen rows 1869.

## Sources and access

- Jordan Department of Antiquities publication portal, <https://publication.doa.gov.jo/Publications/Search> (Publication Type = ADAJ). The early volumes are all there: 1 (1951), 2 (1953), 3 (1956), 4/5 (1960), 6/7 (1962), 8/9 (1964), 10 (1965), 11 (1966), 12/13 (1968), and every later volume to 62.
- Fetched from the workspace, one request at a time, at least 3.5 s apart: the whole ADAJ listing (179 pages), all 109 volume pages (tables of contents), 146 chapter pages, and 22 PDFs (the nine early volumes, two separate Arabic parts and the later candidates' chapter PDFs). SHA-256 of every PDF: `data/pdf_sources.csv`. PDFs and OCR text stay in the scratch folder, not in the repository.
- No PDF has a text layer. English pages: `tesseract` 5 OCR. Arabic pages: read visually from page images (no Arabic OCR model; see Blocked); the hash for those units covers a transcription of the passages used.
- **Not read:** ADAJ 6/7 printed p. 116 (blank in the portal scan); the "Notes & News" listed in ADAJ 11's contents (absent from the scan). Arabic parts other than those of 4/5, 6/7, 8/9, 11, 12/13, 17 and 36 were screened by portal title only. Volumes 14-62 were screened by contents title only.

## Method

1. Screen: every portal contents title, and every early-volume news or round-up heading, against the gazetteer (A1 normalisation, A3 variants; `scripts/screen_titles.py`, reusing phase-2 `common.py`). Each hit and each hand addition has a decision and reason (`data/screen_decisions.csv`). East-bank sites are listed as outside and not coded (Machaerus included).
2. Order: tiers T1 → T2 → T3 (plan §3.4), ascending SHA-256 of the unit id within a tier. The screen was committed before reading (e7d445b).
3. Coding: phase-2 classes, in-window rule and labels; one row per unit and class (`data/coding.json`). Quotes are verbatim, 12 words or fewer, and checked against the OCR or transcription by `scripts/verify_spans.py` (`data/spans.csv`, SHA-256 of each whitespace-collapsed span). Palestine Grid references are converted with EPSG:28191 (phase-1 `geo.py`).
4. Build: `scripts/build_part_i.py` writes `reports.csv` and `features.csv` (phase-2 column order), `screen.csv`, `held.csv`, `summary.md`, `summary.json`. Deterministic.

## Results

Feature rows in the region, by class (yes / no / unknown): tombs and burial caves 28 (0 / 16 / 12); hoards and caches 12 (3 / 8 / 1); channels and aqueducts 9 (3 / 4 / 2); cisterns 7 (2 / 2 / 3); pools and reservoirs 7 (4 / 2 / 1); caves 7 (2 / 2 / 3); rock-cut installations 5 (0 / 3 / 2); columbaria 1 (0 / 0 / 1); dams 0; ritual baths 0.

By zone: Z1 Gerizim 13 (0 / 9 / 4); Z2 Jordan Valley 5 (1 / 4 / 0); Z3 Judean Desert 17 (11 / 2 / 4); Z4 Jerusalem hills 41 (2 / 22 / 17).

The rows dated in the window come from Kh. Qumran (ADAJ 2, 3), 'Ain Feshkha (ADAJ 4/5), Wadi Murabba'at (ADAJ 2), Tulul Abu el-Alayiq (ADAJ 1) and the Herodian cave at Kh. Siyar el-Ghanam (ADAJ 3). One more in-window row, the Herodian kokhim tomb at Wadi el-Badhan (ADAJ 2 pp. 78-81), is outside the region: its printed map reference converts to a point just east of the Z1 box. 31 units in the region have no eligible feature (permit lists, conservation notes, reviews, churches and walls). Full tables: [summary.md](summary.md).

## Protected and held

- **Held cave passages (citation and first line only; `held.csv`):** ADAJ 1 p. 6 (Cave 1 linen), ADAJ 2 p. 5 (Taamireh caves; held as a precaution), ADAJ 2 pp. 5-6 (Qumran Cave 4), ADAJ 2 p. 7 (expedition to the Qumran caves), ADAJ 2 pp. 82-83 (Qumran Caves), ADAJ 2 p. 89 (cave cache near Feshkha; precaution), ADAJ 4/5 Arabic pp. 25-26 (Feshkha section, caves and Kh. Qumran together).
- **Tell es-Sultan north strip (precaution):** ADAJ 16 pp. 5-30 (Kenyon, *Burial Customs at Jericho*; reading stopped at p. 12) and ADAJ 2 p. 88 (Jericho 1952, paragraph on tombs north of the tell). Neither is coded; no feature row has `protected_strip = yes`.
- Some held text was seen while screening or before the strip check; the exact lines are in [NOTES.md](NOTES.md), deviations D2-D4. Nothing was coded from them.
- **Kh. ʿAlmit:** not mentioned in any OCR'd text (search for "Almit"); no extraction file was needed. ʿAtiqot 41, Kochavi 1972, the L-656 file and the IAA Archive cave records were not sought.

## Blocked

- `https://github.com/tesseract-ocr/tessdata_fast/raw/main/ara.traineddata` (Arabic OCR model, a tool, not a source): HTTP 403 from the workspace proxy. Not worked around; Arabic pages were read visually instead.
- No portal request was refused. `https://publication.doa.gov.jo/robots.txt` returns 404.

## Files

- `reports.csv`, `features.csv` (phase-2 columns), `screen.csv` (every title and heading, decision, tier, position, status), `held.csv`, `summary.md`, `summary.json`.
- `data/`: `portal_toc.csv`, `portal_chapters.csv`, `early_headings.csv`, `screen_decisions.csv`, `coding.json`, `spans.csv`, `held.csv` (input), `pdf_sources.csv`.
- `scripts/`: `screen_titles.py`, `verify_spans.py` (needs the OCR folder), `build_part_i.py`.
- `tests/test_part_i.py`: column order, zones recomputed from coordinates, no held unit coded, README counts. Run from the repository root: `python3 -I -m unittest discover -s research/regional/haesi_features/phase4_2026-10-11/part_i_adaj/tests`.
- [NOTES.md](NOTES.md): fetch log, deviations and choices, figures to archive later, proposed changes.
