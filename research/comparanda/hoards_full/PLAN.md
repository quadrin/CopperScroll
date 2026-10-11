# Hidden deposits, 200 BCE to 135 CE: frozen plan

Worker: hoards_full (regional lane, 10 October 2026). Written before any new deposit record was read or coded. The SHA-256 of this file and the freeze time go in README.md. Any later change goes in a separate, labelled amendment file. This file is never edited after the freeze commit.

## 1. Question and what this is

1. Build a fuller catalogue of recorded hoards and intentional concealments in the precedent's region, about 200 BCE to 135 CE.
2. Re-run the precedent's comparison (`research/comparanda/concealment_contexts/`, result DIFFERENT, D = 0.67) on the fuller catalogue. Only the catalogue changes. The context categories, the statistic, the runs, the decision wording and the scroll coding stay exactly as frozen there.
3. Add two descriptive comparisons fixed here (sections 9 and 10): stated depths, and placement relative to a named landmark.

This is an exploratory regional inventory and base-rate comparison. It makes no identification claim. It changes no registered outcome. It speaks only to the kind of list (R12). A landmark match or a depth match says nothing about any place or any deposit.

## 2. Exposure before freezing (honest record)

- I read the precedent's PLAN.md, README.md and RESULTS.md in full, the header and first four rows of its `comparanda.csv`, and the counts of its `setting`, `how_found` and id-prefix columns (eligible rows: unknown 90, structure 43, cave 20, open_ground 3, tomb 2, channel 1, pool_reservoir 1, cistern 1).
- I read the precedent's `concealment.py` and the header of its `sources_read.csv` (the URL list, not the saved pages).
- I read the precedent's `scroll_contexts.csv` columns `entry`, `col_line`, `setting_P`, `placement_P`, `container_P` and `primary_deposit` for all 61 entries.
- I read the T02 REPORT.md and the first record (H01) of T02 `hoards.json`. The report names: Qumran L120 ("to the right of the door … between the floors"), Ramat Raḥel (niche in the SW corner of an underground dovecote, "0.5 m above the floor and 3.5 m below the shaft"), the Jewish Quarter shekels "in a small pool", Murabbaʿat Cave II (box in a wall crack), Cave of Letters vessels, Cave of the Sandal coins.
- I read `research/schematics/searches/search_04_depths.py` (the scroll's 26 "dig N cubits" phrases and its cubit values), `registration/zissu2023_extracted.md`, and the two hoard rows of `research/regional/haesi_features/features.csv` (both Byzantine or later).
- Access checks only (no records read): coinhoards.org and nomisma.org refuse robots (WebFetch ROBOTS_DISALLOWED; curl connection reset). CHRE robots.txt allows all. atiqot.org.il robots.txt allows all. hadashot-esi.org.il robots.txt disallows all. I read the CHRE search form's option lists (province ids 31 Arabia, 44 Judaea, 54 Syria Palaestina; country ids 22 Israel, 24 Jordan, 47 Syria, 103 Palestinian Territories).
- I have computed no depth or landmark tally for any comparandum. I have not counted landmark words in the scroll.
- Background expectation (not data): excavation reports rarely give a depth for a hoard; more give a room, a floor or a wall. I record this so a reader can judge.

## 3. Frozen inputs reused unchanged (checked by SHA-256 at every run)

| file | SHA-256 |
|---|---|
| `concealment_contexts/PLAN.md` | `6d797192bffdb92473237347a6fbe59a93593eca6bd7fc32e3f54acc647369d1` |
| `concealment_contexts/concealment.py` | `976b59b1dcd8ccb60cb4a127da80ca7e12de9bbb53f8fdf78c3a476d8771b265` |
| `concealment_contexts/scroll_contexts.csv` | `c9547bb28dc93aed3d6256148d5bb7211b7403e91da922c4aa82c2be1949ae50` |
| `concealment_contexts/comparanda.csv` | `2e1f970ede7e974aa76f0fa0d8e495d0026872be93722e6d6392d3b4f5c0d542` |
| `schematics/searches/search_04_depths.py` | `71e39b3dd9f9812ba16fe59cd7e695ba8c58802dd95577c0ee5fe9de72bd059b` |
| T02 `hoards.json` | `e5972e7f486ed7bac1e5db424f9174a855895f7f02b40e03b04f4069baa3e4d8` |

- My script imports the precedent's functions (`fine_category`, `coarse_group`, `in_window`, `in_region_main`, `in_region_judaea`, `compare`, `verdict`, `comparanda_units`, `comp_labels`, `scroll_labels`, `run_one`, `bias_checks`, the constants and `RUNS`) from `concealment.py` after checking its hash. It reads `scroll_contexts.csv` in place after checking its hash. Nothing is copied or re-implemented.
- Precedent sections reused unchanged: 3 (windows and date rule), 4 (region), 5 (what counts as a concealment), 7 (unit and duplicates), 8 (coding rules), 9 (scroll coding), 10 (statistic), 11 (runs), 12 (decision wording), 13 (labels and limits).

## 4. Catalogue scope

- **Catalogue window:** deposits whose date-range midpoint (precedent rule, section 3) lies from -200 to 135. Each row also gets `window_status`: `inside` (whole range inside -200..135), `partial` (range overlaps the window but not wholly inside), `outside`. Rows outside the catalogue window are kept in `hoards.csv` with `include` as coded and are not counted.
- **Comparison windows:** the precedent's: main -150..135, sensitivity -63..70 (midpoint rule).
- **Region:** the precedent's (section 4). Main: findspots in modern Israel, the Palestinian Territories, Jordan and the Golan. Sensitivity: boxes J and V. A CHRE row with country "Syria" counts as Golan only if its coordinates fall in latitude 32.60–33.35 and longitude 35.60–35.95; its `country` is then written "Golan (CHRE: Syria)". Rows outside the main region are not added to the catalogue.
- **Eligibility:** the precedent's section 5, unchanged. Clarifications fixed now, before any record:
  - A cache of metal objects (vessels, jewellery, weapons, tools, bullion) deliberately concealed together counts as "caches … of other valuables". A single object does not count.
  - A refuge-cave deposit counts only where the source describes a deliberate concealment (hidden, wrapped, packed, in a container, in a crevice or niche, buried, sealed). Occupation debris and scattered finds in refuge caves do not count.
  - Scroll caves near Qumran other than Cave 3 count as document deposits when the source reports scroll jars or deposited manuscripts; flag `qumran_cave`.
  - Temple-related deposits (for example a source's reading of a shekel hoard as Temple dues, or hidden sacred vessels) get the flag `temple_related`. There is no separate category.

## 5. Sources and search protocol (in this order)

Search by object type only ("hoard", "cache", "treasure", "coins", "scrolls", "documents", "vessels", "jewellery", with period or region words). Never search with context words (cistern, pool, channel, tomb, cave, wall, floor, stone, threshold, pillar, corner, step, gate, field, ruin, depth, buried). This keeps the context, depth and landmark distributions from being steered by the scroll's vocabulary.

- **R1. Repository, reuse first.** Precedent `comparanda.csv` (181 rows; codings reused), `sources_read.csv`; T02 `hoards.json`, `chre_details.json`, `chre_extra.json`; `research/regional/haesi_features/features.csv` hoard rows; `registration/zissu2023_extracted.md`; grep of `research/` and `registration/` for "hoard" and "cache".
- **R2. CHRE** (chre.ashmus.ox.ac.uk, open access, robots allow). List searches with terminal year -260 to 150 for countries 22, 103, 24 and 47, and for provinces 44 (Judaea), 54 (Syria Palaestina) and 31 (Arabia). Fetch the detail page of every listed hoard not already in the precedent's `comparanda.csv` or T02 `chre_details.json` whose midpoint falls in -200..135, and re-fetch detail pages of precedent rows only to read depth and landmark wording. One request per second or slower; pages cached in the scratch folder, never committed; SHA-256 of each saved page in `sources_read.csv`.
- **R3. IGCH and *Coin Hoards* I–X** (coinhoards.org). Robots refuse access (section 2). Recorded under Blocked with exact URLs. Not bypassed.
- **R4. ʿAtiqot** (atiqot.org.il, robots allow). Every article whose title names a hoard, cache, treasure or coin find, dated by title or abstract to the window. Read the context paragraph(s) and record pages.
- **R5. HA-ESI and IAA publications.** Robots refuse the online HA-ESI; the portal PDFs sit behind a JavaScript check (haesi_features README). Recorded as Blocked. HA-ESI pages reachable through allowed routes (publications.iaa.org.il article HTML) may be read.
- **R6. Open numismatic literature.** Ariel & Fontanille, Bijovsky, Meshorer, Kadman, Eshel & Zissu (Bar Kokhba hoards), INJ and INR articles, Leonard 2000: only where open access. Otherwise Blocked with the exact catalogue or publisher URL and the pages needed.
- **R7. Owner's Mac, `~/Downloads`.** `Guide to Biblical Coins (David Hendin.pdf` (hoard lists, if any). `Judean_coins.xlsx` and `hasmonean_coins.xlsx` only if, on opening, they are plainly coin-find research data; otherwise they are closed and neither used nor described. Narrow `ls | grep` only.
- **R8. Owner's Drive library** via `research/sources/drive_index.md`, read only, for any hoard source it lists. Protected items are not opened (section 6).
- **R9. Bounded web search** for further in-window hoards and caches in open-access reports, IAA releases and open journal articles. At most 40 queries. Stop earlier after five consecutive queries add no new eligible row. Every query is logged with the rows it added.

Every row cites a source with page, figure, section or URL. Quotes are 12 words or fewer. Failed links go in README.md under Blocked, with the exact URL.

## 6. Protected items

I will not read any item in `research/preregistration/arrivals/items/`, the L-656 field file, IAA Archive cave records, the ʿAtiqot 41 cave entries, Zertal vol. 4 site 194, HA 28–29, Highlands pp. 700–702, the IAA notices on Kh. ʿAlmit, Kochavi 1972 or Zertal vol. 1. If a search result points to one, it is listed and skipped. If one is nevertheless read, its rows are marked `unexposed_at_freeze = 1` and reported separately.

## 7. Units, duplicates, provenance of each row

- Unit and clusters: precedent section 7, unchanged.
- Cross-source duplicates: two records are the same deposit if site, find year (±1) and either coin count (±10%) or closing date agree, or if a source says so. Keep one row, cite all sources, record the merge in `flags`.
- `origin`: `precedent` (row from the precedent's `comparanda.csv`), `t02` (T02 record not in the precedent), `new` (first read in this lane).
- `first_read`: `before_freeze` (the repository held the record before this freeze) or `after_freeze`.

## 8. Coding

- `setting`, `placement`, `container`, `how_found`, `date_from`, `date_to`, `cluster_id`, `include`, `exclusion_reason`, `judaea_by_name`: precedent sections 3, 5, 7 and 8, unchanged.
- **Precedent rows keep their coding.** A precedent row is recoded only when a source read here states a context or date that contradicts the precedent's coding. Each recode keeps the old value in `prec_setting`, `prec_placement`, `prec_include`, `prec_date` and gives `recode_reason`. Run x3 (section 11) restores the precedent's coding for every recoded row.
- New fields (all EVIDENCE as reported, coded by me):
  - `object_class`: coins, metal_objects, coins_and_metal, documents, sacred_objects, mixed.
  - `temple_related`: 1 if a source ties the deposit to the Temple, else 0.
  - `depth_m`, `depth_datum`, `depth_text`: section 9.
  - `landmark`, `landmark_text`: section 10.
  - `discovery_year`, `terminus_text`, `sources_pages`.
- Unknown stays empty (null), never zero or "none".

## 9. Descriptive comparison 1: stated depths

**Comparanda.** `depth_m` = the vertical distance in metres from a stated reference surface down to the deposit, as a number the source states. A range takes its midpoint. "Under the floor" without a figure is null. A height above a floor is not a depth (null; quoted in `depth_text`). `depth_datum`:
- `present_surface`: below the modern ground or field surface;
- `ancient_floor`: below an ancient floor, courtyard or cave floor;
- `feature_top`: below the top or mouth of a shaft, cistern, wall or other feature;
- `unstated`: a figure with no stated reference.

**Scroll.** The 26 "dig N cubits" phrases in `search_04_depths.py` (`DIGS`), one value per phrase. Cubit branches, each run separately: short 0.445 m, working 0.500 m, royal 0.525 m (the values in `search_04_depths.py`). Sensitivity: drop the phrases marked restored or corrupt (entries 21, 28, 38).

**Set.** Eligible comparanda in the catalogue window and main region with a numeric `depth_m`. Report also: the main-window subset; the number with no stated depth; each datum separately; surface and floor datums only.

**Report (descriptive, no test, no verdict).** For each side and branch: n, minimum, lower quartile, median, upper quartile, maximum (quartiles by `statistics.quantiles(method="inclusive")`, n ≥ 4); the share deeper than 0.5, 1, 2 and 3 m; the share of scroll depths greater than the comparanda maximum; the share of comparanda depths below the scroll minimum. If fewer than 5 comparanda have a stated depth, say "too few stated depths to describe" and list them.

## 10. Descriptive comparison 2: placement relative to a named landmark

**Classes.** `corner`, `step` (step, steps, stair, stairs, staircase), `pillar` (pillar, column), `threshold` (threshold, door, doorway, entrance, "as you go in", "on entering"), `gate`, `wall_face` (a named wall: against, beside, under, along, in or in a niche of a wall).

**Comparanda.** A class is coded only when the source places the deposit at, under, beside, against, in or relative to that element (for example "under the threshold", "in the northwestern corner of the room", "beside the north wall", "in a niche in the wall", "to the right of the door"). Naming the building or room only ("in the gatehouse", "in the tower") does not count. `landmark` = semicolon list of classes, `none_stated` when the source gives a context but no landmark, empty when the context is unknown. `landmark_text` = a quote of 12 words or fewer.

**Scroll, main.** Case-insensitive regular expressions on the precedent's `primary_deposit` field for each of the 61 entries:
- corner: `\bcorners?\b`
- step: `\b(steps?|stairs?|stairway|staircase)\b`
- pillar: `\b(pillars?|columns?)\b`
- threshold: `\b(thresholds?|doors?|doorways?|entrances?)\b|as you go in|as you enter|on entering`
- gate: `\bgates?\b|\bgateway\b`
- wall_face: `\bwalls?\b`

**Scroll, sensitivity.** The same expressions on the project translation (`text/translation_en.json`) of all lines in the entry's `col_line` range, with `{{text|id}}` markup reduced to its text. Lines shared by two entries are read for both; this can over-count and is reported as such.

**Strict variant (both sides).** threshold counts only threshold, door or doorway (not entrance, "as you go in", "on entering").

**Denominators.** (a) all eligible units in the main window and region (clusters, precedent rule); (b) those with a known context; (c) catalogue window. Scroll: 61 entries. Report per class and "any class", with the entries and rows that hit. Descriptive only; no test, no verdict.

## 11. Comparison runs

- The precedent's ten runs (`RUNS`: main, s1 to s9) and its bias checks B1, B2a, B2b and B3, computed by the imported functions on `hoards.csv`, with the precedent's seed (20261009), 20,000 permutations and 2,000 bootstrap resamples.
- Verdict, robustness and reporting sensitivity: the precedent's section 12 rules and wording, unchanged, applied to those runs.
- Additional labelled runs (reported separately; they do not enter the robustness rule):
  - x1: catalogue window -200..135 instead of -150..135;
  - x2: the precedent's main run on rows with `origin` = `new` or `t02` only;
  - x3: the main run with the precedent's coding restored for recoded rows;
  - x4: the main run on rows with `first_read` = `after_freeze` only (if any).
- A delta table: main-run counts per coarse group in the precedent and here, and which rows moved.

## 12. Decision wording

The precedent's section 12, unchanged. The headline is the main-run verdict word on the fuller catalogue, its D and p, the counts of comparanda units with known and unknown context, and whether the verdict differs from the precedent's. The descriptive comparisons carry no verdict word.

## 13. Output

- `hoards.csv`: one row per candidate deposit (eligible or excluded) with the precedent's input columns, the new fields of section 8, `origin`, `first_read`, `window_status`, `unexposed_at_freeze`, and the precedent's derived columns.
- `results.json`, `RESULTS.md`: written by `hoards_full.py run`.
- `sources_read.csv`: every URL or file read, with access date and SHA-256 of saved pages or text spans.
- `hoards_full.py`: build, run and check; standard library only; deterministic.
- `tests/`: plan hash, frozen-input hashes, schema, coding mapping, reproducibility.
- `README.md`: What it is / Main result / What stays unknown; freeze record; sources and access; method; results; Blocked (exact URLs); files; proposed changes for the integrator.

## 14. Labels and limits

- EVIDENCE: what a source reports about a deposit. INFERENCE: my coding and every count. CLAIM: an author's assertion with no field record.
- The comparanda are what was found and published. Deposits recovered in antiquity leave no record. A fuller catalogue still lists published finds only.
- The scroll side codes one edited text, not independent deposits.
- No identification claim, no outcome-ledger count, no location inference.
