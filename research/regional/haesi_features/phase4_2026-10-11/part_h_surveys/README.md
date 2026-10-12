**What it is.** An exploratory screen and coding, under the phase-2 rules, of the site entries in the *Survey of Western Palestine* Memoirs III (Judaea) and II (Samaria) and in Guérin's *Judée* I, for cisterns, pools, channels, dams, stepped pools, caves, tombs, columbaria, rock-cut installations and hoards in the study region.
**Main result.** 1817 units screened; 200 units read and coded (178 SWP, 22 Guérin) give 101 feature rows with one zone and 94 further rows in the region whose zone is split between two zones. No row is dated by its author to the window (yes 0); 24 rows are dated outside it and the rest are unknown.
**What stays unknown.** These are nineteenth-century survey notes: features are counted as described, without dates for the features themselves. 360 SWP entries in squares cut by the region boundary, 83 other entries with no usable location, and Guérin *Judée* II, *Judée* III and *Samarie* I were not read.

## Sources and access

| Source | Route | Read | Not read |
|---|---|---|---|
| SWP Memoirs III, Judaea (Conder and Kitchener 1883), Sheets XVII–XXVI, Section B | archive.org `surveyofwesternp03conduoft`, OCR (hOCR search text and page index) | 1,058 headings screened; every candidate read | 174 unlocated entries |
| SWP Memoirs II, Samaria (1882), Sheets IX–XVI, Section B | archive.org `surveyofwesternp02conduoft` | 677 headings screened; every candidate read | 213 unlocated entries; pp. 401–408 missing from the scan |
| Guérin, *Judée* I (1868) | archive.org `descriptiongeogr01guer` | 82 headings screened; every candidate read | 56 headings with no gazetteer match |
| Guérin, *Judée* II, *Judée* III, *Samarie* I | archive.org `descriptiongeogr02guer`, `03guer`, `04guer` | — | not read (time limit); not screened |

OCR text was fetched with curl, one request at a time, at least 3 s apart, and kept outside the repository. Pages are printed pages. Each read span has a SHA-256 hash in `reports.csv`.

## Method

1. Each site entry (SWP) or site heading (Guérin) is one unit. SWP squares give the zone where the whole square, with a 0.25-square margin, lies in one zone; otherwise the name is matched to the frozen phase-2 gazetteer. Guérin is placed by name only.
2. The screen of each volume was committed before reading. Reading followed tier (T1, T2, T3) and the SHA-256 order of unit ids.
3. Held cave areas were checked from the heading or first line before reading. Built sites in those areas were read.
4. Features were coded to the phase-2 classes and columns, with the author's words for the period. Choices and deviations are in `NOTES.md`.

## Results

Units by status:

| status | units |
|---|---|
| Tier-1 extraction only | 1 |
| held or protected (citation only) | 2 |
| not read (no description) | 8 |
| not read (out) | 1163 |
| not read (unlocated) | 443 |
| read | 81 |
| read (zone unresolved) | 119 |

Feature rows by class (one zone | zone split):

| class | rows | yes | no | unknown | split rows | split yes | split no | split unknown |
|---|---|---|---|---|---|---|---|---|
| cistern | 24 | 0 | 1 | 23 | 36 | 0 | 2 | 34 |
| pool_reservoir | 14 | 0 | 2 | 12 | 9 | 0 | 2 | 7 |
| channel_aqueduct | 11 | 0 | 0 | 11 | 9 | 0 | 3 | 6 |
| dam | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| ritual_bath | 4 | 0 | 1 | 3 | 0 | 0 | 0 | 0 |
| cave_with_finds | 16 | 0 | 0 | 16 | 14 | 0 | 2 | 12 |
| tomb_burial_cave | 23 | 0 | 6 | 17 | 21 | 0 | 5 | 16 |
| columbarium_dovecote | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rockcut_installation | 9 | 0 | 0 | 9 | 4 | 0 | 0 | 4 |
| hoard_cache | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Feature rows by zone (one zone):

| zone | rows | yes | no | unknown |
|---|---|---|---|---|
| Z1_GERIZIM | 17 | 0 | 2 | 15 |
| Z2_JORDAN_VALLEY | 12 | 0 | 2 | 10 |
| Z3_JUDEAN_DESERT | 23 | 0 | 1 | 22 |
| Z4_JERUSALEM_HILLS | 49 | 0 | 5 | 44 |

Zone-split rows: Z2|Z3 22, Z3|Z4 72. The "no" rows are traditional saints' and prophets' tombs, Muslim graves, Byzantine, Crusader or modern works, as the authors date them.

## Protected and held

There are 6 held records in `held.csv`: 'Ain ed Duk (read in error before the hold check, deviation D1; not coded), Jebel Kuruntul with its caves (held from the first line), Tell es-Sultan north strip (citation only, `protected_strip = yes`), two Deir el Kelt cliff paragraphs (held by caution), and Kh. ʿAlmit (extraction only, `tier1_kh_almit_extraction.md`). No held unit has a feature row.

## Blocked

Nothing was blocked. All archive.org requests returned HTTP 200.

## Files

- `features.csv`: feature rows with one zone (phase-2 columns).
- `features_zone_unresolved.csv`: rows in the region whose zone is split (same columns).
- `reports.csv`: one row per unit read (phase-2 columns).
- `screen.csv`: every unit screened, with location, decision, tier, order and status.
- `held.csv`: held, protected and Tier-1 records.
- `summary.json`, `summary.md`: counts, generated.
- `tier1_kh_almit_extraction.md`: Kh. ʿAlmit facts with pages.
- `NOTES.md`: method details, deviations and choices, missed headings, not read, figures to archive, proposals.
- `data/`: committed screens, hand coding (`coding_*.jsonl`), held records, fixes, name variants, SWP grid calibration points.
- `scripts/`: `swp_grid.py`, `names.py`, `screen_swp.py`, `screen_gue.py`, `add_coding.py`, `build_part_h.py`.
- `tests/test_part_h.py`: run `python3 -I research/regional/haesi_features/phase4_2026-10-11/part_h_surveys/tests/test_part_h.py` from the repository root.
