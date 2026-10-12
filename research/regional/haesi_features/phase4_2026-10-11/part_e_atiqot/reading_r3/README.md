# Phase 4, part E, reader r3: ʿAtiqot T2 positions 136–208

**What it is.** The coded reading of 73 ʿAtiqot articles (tier T2, order positions 136–208 of `../pdfs_needed.csv`), all in Jerusalem and its hills (Z4), under the frozen phase-2 rules. Exploratory; no identification claim.
**Main result.** All 73 units were read. 53 record at least one eligible feature, giving 110 feature rows (37 dated in the window, 55 outside it, 18 unknown). No unit was held.
**What stays unknown.** How many of these rows are the same feature on the ground (finds reports repeat their excavation's features; see `NOTES.md`), and every unit outside positions 136–208.

Units read: 73 of 73. Feature rows: 110.

## Sources and access

- PDFs: the owner-approved downloads in `~/Downloads/IAA portal volumes/phase4/` on the owner's Mac, one file per unit (`<unit_id>.pdf`). All 73 SHA-256 values match `../../downloads_2026-10-11.csv`. Nothing else in `~/Downloads` was opened.
- Text: `pdftotext -raw` and `-layout` on the Mac, kept in `$HOME/p4text/r3/` and not committed. All PDFs have a text layer. 21 articles are in Hebrew and were read in Hebrew, with their English summary where the PDF has it.
- Not read: none (`not_read.csv` has its header only). Blocked: none.

## Method

- Order: tier T2, positions 136 to 208, one unit at a time (one swap, see `NOTES.md` D1).
- Location: the article's printed map reference, converted with the phase-1 `geo.py` (NIG EPSG:2039, OIG EPSG:28191); a range is converted at its first value. Without a usable reference the unit is placed by the name in its title (plan §2, `coordinate_source = name only`). Every converted point fell in Z4.
- Coding: phase-2 classes, in-window rule, labels and columns (plan §§5–6, amendments A1–A4). One row per (unit, class), split by `feature_site` where one class has different dates or different work. Finds and specialist reports code the feature their material came from (choice C2). Choices C1–C10 are in `NOTES.md`.
- Checks: every quote (12 words or fewer) was found in the source text, and the SHA-256 of the lines read was computed on the Mac (`scripts/verify_spans.py`, results in `data/spans_r3.jsonl`).

## Results

All rows are in Z4 (Jerusalem hills). Rows count report rows, not features on the ground.

| Class | Zone | Rows | yes | no | unknown |
|---|---|---|---|---|---|
| cistern | Z4 | 10 | 4 | 5 | 1 |
| pool_reservoir | Z4 | 9 | 2 | 6 | 1 |
| channel_aqueduct | Z4 | 15 | 4 | 9 | 2 |
| dam | Z4 | 2 | 2 | 0 | 0 |
| ritual_bath | Z4 | 5 | 4 | 1 | 0 |
| cave_with_finds | Z4 | 9 | 3 | 2 | 4 |
| tomb_burial_cave | Z4 | 37 | 14 | 22 | 1 |
| columbarium_dovecote | Z4 | 0 | 0 | 0 | 0 |
| rockcut_installation | Z4 | 22 | 4 | 9 | 9 |
| hoard_cache | Z4 | 1 | 0 | 1 | 0 |

Units without eligible features: 20 (mostly coin, finds and epigraphic reports; also a Roman villa and kiln, a prehistoric site, a Middle Bronze farmstead and three syntheses of earlier work).

## Protected and held

- No unit concerned a cave in a held area, the Tell es-Sultan north strip or Kh. ʿAlmit. `held.csv` has its header only.

## Blocked

- None.

## Files

- `reports.csv`, `features.csv` — phase-2 columns and order.
- `held.csv` (part-E header), `not_read.csv` — headers only.
- `summary.json` — counts.
- `data/units/*.json` — the hand coding, one file per unit; `data/spans_r3.jsonl` — span hashes and quote checks.
- `scripts/build_r3.py` — builds the tables; `scripts/verify_spans.py` — run on the Mac next to the text files.
- `tests/test_r3.py` — column order, zones recomputed from coordinates, no held unit coded, README counts, deterministic rebuild.
- `NOTES.md` — deviations and choices, same-feature rows, figures to archive later, proposed changes.
