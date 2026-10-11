# Water installations of the Jericho–Jerusalem region, counted against the scroll's water entries

**What it is.** An inventory of every ancient water installation recorded in a fixed box (Jericho and Naʿaran to ʿEin el-Ghuweir, ʿEin Kerem to the Jordan) in four lineages: the West Bank Archaeological Database (WBADB), the online Archaeological Survey of Israel (ASI), the HA-ESI lane's rows and hand-coded literature. Each installation is scored against the clauses of entries 21, 22, 29, 32, 42, 45 and 46 under a plan frozen before any record was coded.\
**Main result.** 2,043 installation rows (1,437 merged units) give no full match for entries 22 and 29 in any branch. Entry 29's best units lack only "northern". For the other entries the clause combinations are either common (an aqueduct whose head is recorded; a reservoir with a way in) or met by two or three units that the repository already knew: only the Naʿaran aqueduct comes from the north; only Qumran, Doq and Netzer's dry fall in the Jericho estate are waterfalls by a conduit bend; only the Hyrcania cisterns are fed by channels from a trunk wadi.\
**What stays unknown.** Most clauses are UNKNOWN for most rows, because surveys rarely record them: m ≫ k in every branch, so rarity is not measurable. No online ASI sheet covers Jericho, the Qumran–Feshkha shore or the upper ʿArrub/Biyar sources. The walled Old City of Jerusalem is covered only by a few WBADB excavation rows. Several listed pages were not read this session (see Sources).

Exploratory, 11 October 2026 UTC (10 October Los Angeles). No identification claim. No registered result, outcome count or closed test changes; the closed entry 29 results stand. Labels: EVIDENCE (the source says it), INFERENCE (our reasoning), CLAIM (an author's assertion without a field record). Unknown stays unknown.

## Freeze record

| File | SHA-256 | Commit | Time (UTC) |
|---|---|---|---|
| PLAN.md | `cc9b54f1eb3968772144b56f2836953e499fd1ef21d927982145bbc98ba9dd17` | `0b07fad` (alone) | 2026-10-11T04:10:20Z |
| PLAN_AMENDMENT_1.md | `653467fd12b5bb77aab346b958bb3503bf34540e5f3bab26d1a2e353312797f6` | `21d197d` (alone) | 2026-10-11T04:15:43Z |

- Exposure before the freeze is listed in PLAN.md §10. Amendment 1 was written after the ASI GeoJSON was fetched and one feature's field names printed, before any row was coded. It fixes operational details only.
- The plan's title says "10 October UTC"; the commit was 04:10 UTC on 11 October (10 October in Los Angeles).
- No protected arrival item and no Tier 1 record was read (`arrival.py check`: manifest ok). Four WBADB/ASI survey rows on Kh. ʿAlmit (a Tier 1 site) are flagged `yes (Kh. Almit flag)` in `first_read_after_freeze`; they are survey summaries, not the IAA notices.

**Changes after the first build (implementation, labelled; no clause, branch, tolerance or decision rule changed):**
1. HTML entities in ASI text are decoded (`&times;`, `&#7717;`); apostrophe variants are accepted in the "from/to Solomon's Pools" exclusion.
2. The Solomon clause in survey text follows plan §5 exactly (the installation must be named Solomon's); the first build had coded any Solomon word.
3. WBADB period notation is mapped onto the plan's labels (Rom1 = Early Roman; Hel, Rom = partly; Byz, IA, EIs, Med, Ott … = out), and "prob." and "(?)" count as hedges. These map notation only; they were added after the first build showed the abbreviations.
4. Reservoir rows are counted in both eligibility sets of entries 22, 29 and 46 (the first build put them in the main set only).
5. Literature groups were corrected so that one group is one installation: the two Hyrcania aqueducts and the three Hyrcania pools are separate units, and aggregate rows described in more detail elsewhere (`covered_by`) are kept in lineage counts but not merged.
6. Two Hyrcania pool rows were recoded to "unknown" for "great" and "conduit": the repository's supply audit (`research/measurements/cycle7/hyrcania_supply.md`) finds no inlet for the northern pool.

**Exploratory post-hoc checks** (`posthoc_checks.csv`, after scoring; counts are not changed): every survey-row MATCH in a non-trivial clause was read against its record. Five rule MATCHes are not confirmed: the north side at ʿEin Qelt (1) (ASI 109/4/16; "north" is the bank of Nahal Perat), its Hasmonean date (the label dates the palaces), a "head" at Kh. Umm el-ʿAmad (108/2/69; "source" of a monastery), a "wall at the mouth" in Wadi Qelt (3) (109/5/6) and a "wadi" feed at El ʿEizariya (102/447; "from N." means from the north).

## Sources and access

Region: WGS 84 box 31.600–31.900 N, 35.120–35.560 E, west of the Jordan (PLAN.md §2, with ITM and Old Israel Grid corners). Points: WBADB X/Y as EPSG:28191; ASI GeoJSON WGS 84; literature rows at a source grid reference, else the point of the WBADB/ASI record of the same named site (precision + 250 m), else a `places_v2.csv` point; 27 literature rows have no supportable point and are counted separately as "unplaced".

`sources_read.csv` gives, per source, the pages or records read, the file SHA-256, the SHA-256 of the text read, the access route and whether it was first read after the freeze.

- **WBADB** (SHA-256 `3db734cd…`, checked): 2,408 survey and 573 excavation rows in the box; 859 water rows. File not committed.
- **ASI**: English GeoJSON of maps 101, 102, 105, 106, 83/1, 83/2, 83/12, 108/2, 109/4, 109/5, 109/7, fetched 2026-10-11 04:10–04:11 UTC (one request per 1.2 s; URL, size and SHA-256 per map in `asi_manifest.csv`; the cache stays outside the repo); 971 water rows; 407 of them come from records the ASI lane had not coded.
- **HA-ESI lane rows**: 17 rows reused.
- **Literature**, 196 rows: Garbrecht & Peleg 1994; the 1989 aqueducts volume (Mazar pp. 169–195, Damati pp. 299–304 and Hirschfeld pp. 305–312 OCR'd from the owner's copy and read in full; Amit pp. 223–226, Meshel & Amit pp. 229–239, Netzer pp. 273–280, Ilan & Amit pp. 283–284 OCR'd from the repo extracts; Patrich via the repo inventory); Netzer 1975 (IEJ 25) in full; Netzer 2001 (*Palaces*) water passages; Galor's Qumran pools chapter; Tsafrir 1975 (*Qadmoniot* 8); the entry 29 inventory (28 records, 21 notices; two ritual-bath notices excluded by plan §4); repo notes on Siloam and Ramat Raḥel.
- **First read after the freeze** (new to the repository): Mazar 1989, Damati 1989, Hirschfeld 1989, Tsafrir 1975, and 407 ASI records.
- The plan attributed the Martyrius chapter to Hirschfeld; the chapter page names Emanuel Damati (an OCR misalignment of the contents page). Pages and content are as planned.

**Listed but not read this session** (no access barrier; time):
- Magen & Peleg, JSP 18 (owner's Downloads): only the repo extraction of pp. 77–79 was used. Its pool descriptions were not coded; Galor's catalogue was used for the Qumran pools.
- Netzer 2001, *Hasmonean and Herodian Palaces at Jericho* I: its table of contents and pool sections were not read. The 28 inventory rows stand in for it.
- Meshel & Amit pp. 240–242, Netzer p. 281 and Ilan & Amit pp. 285–288 (OCR exists in the scratch folder; the Ilan & Amit repo review was used).
- Patrich 1989: the OCR was made but not used; rows come from the repo inventory.
- Repo notes on Herodium were not searched; Netzer 2001 was used for Herodium.
- SWP *Memoirs*: excluded by plan §3.5. Wadi Qelt rows whose only original source is SWP (`research/sites/feature_investigation.md`) are therefore absent.

## Method (summary; rules in PLAN.md §4–§9)

1. `build_survey.py` codes WBADB, ASI and HA-ESI rows: one row per record and installation type, attributes from words in the same sentence as the feature word, dates from period labels in that sentence. It links WBADB rows to ASI records (Kloner/Patrich/Hirschfeld site numbers, else name skeleton within 300 m): 499 WBADB rows are `dup_of` an ASI row.
2. `literature_data.py` and `literature_data_2.py` hold the hand-coded rows with page or figure locators. `build_water.py` places them, sets the place columns, supersedes 79 survey rows of the same type at the same named site within 1 km, and forms 1,437 merged units.
3. `score.py` applies each clause (MATCH / FAIL / UNKNOWN; silence is never FAIL) and the date rule: main (only "out" fails), dated (in or in_hedged), strict (in). A unit combines its members: MATCH if any member matches and none fails; CONFLICT counts as unknown.

## Results

Counts read "k match, f fail, m unknown, of N". MERGED = one count per installation unit in the box. Full table per lineage and date rule: `counts.csv`; each unit's codes: `merged_scores.csv`.

| Entry | Branch | MERGED, main date rule | MERGED, dated only | Literature rows only |
|---|---|---|---|---|
| 21 | head recorded (S-open × N-side) | 12 k, 30 f, 241 m of 283 | 8 k, 259 f, 16 m | 16 k, 4 f, 9 m of 29 |
| 21 | stone at head on its north (S-stone × N-side) | 0 k, 30 f, 253 m | 0 k | 0 k, 4 f, 25 m |
| 21 | any feature at head on its north (S-any × N-side) | 1 k, 34 f, 248 m | 1 k | 0 k, 7 f, 22 m |
| 21 | pool at head on its north (S-pool × N-side) | 1 k, 34 f, 248 m | 1 k | 0 k, 7 f, 22 m |
| 21 | water from the north (S-open × F-flow) | 1 k, 40 f, 242 m | 1 k | 2 k, 18 f, 9 m |
| 21 | stone/any/pool × F-flow | 0 k (40 f) | 0 k | 0 k |
| 22 | named Solomon's + fissure east ≤ 500 m (reservoirs) | 0 k, 27 f, 237 m of 264 | 0 k | 0 k, 15 f, 70 m of 85 |
| 22 | same, ≤ 1 km; or reservoirs + cisterns | 0 k in every variant | 0 k | 0 k |
| 29 | conduit + great + northern + four sides (reservoirs, Q-any) | 0 k, 76 f, 188 m of 264 | 0 k | 0 k, 53 f, 32 m of 85 |
| 29 | Q-Kidron / Q-Cypros / Q-Jericho | 0 k in every variant | 0 k | 0 k |
| 32 | built outlet or aqueduct head at Wadi Qelt (O-built × K-Qelt) | 5 k, 80 f, 213 m of 298 | 5 k | 5 k, 6 f, 22 m of 33 |
| 32 | same, with a wall at the outlet (T-wall) | 0 k, 80 f, 218 m | 0 k | 0 k |
| 32 | spring at Wadi Qelt (O-spring × K-Qelt) | 4 k, 2 f, 55 m of 61 | 0 k (springs undated) | 2 k, 0 f, 7 m of 9 |
| 42 | waterfall within 250 m of a conduit bend (W-fall) | 2 k, 0 f, 4 m of 6 | 0 k (natural, undated) | 2 k of 3 |
| 42 | waterfall within 1 km of a bend | 3 k, 0 f, 3 m of 6 | 0 k | 3 k of 3 |
| 42 | dam or reservoir near a bend (W-dam) | 0 k, 28 f, 272 m of 300 | 0 k | 0 k |
| 45 | cistern fed by channels from a trunk wadi (C-open × G-strict) | 1 k, 92 f, 559 m of 652 | 1 k | 2 k, 10 f, 11 m of 23 |
| 45 | same, any wadi (C-open × G-loose) | 3 k, 41 f, 608 m | 2 k | 4 k |
| 45 | plastered, channels, any wadi (C-plaster × G-loose) | 1 k, 41 f, 610 m | 1 k | 2 k |
| 45 | plastered, trunk wadi (C-plaster × G-strict) | 0 k, 92 f, 560 m | 0 k | 0 k |
| 45 | wheel-well (M-well) | 0 k, 2 f, 7 m of 9 | 0 k | – |
| 46 | reservoir with a way in, within 1 km of Ramat Raḥel | 0 k, 261 f, 3 m of 264 | 0 k | 0 k, 83 f, 2 m |
| 46 | same, ʿEin Kerem | 0 k, 260 f, 4 m | 0 k | 0 k |
| 46 | reservoirs + cisterns, ʿEin Kerem ≤ 1 km | 1 k, 908 f, 7 m of 916 | 0 k | 0 k |
| 46 | reservoir with a way in, anywhere (B-any) | 25 k, 27 f, 212 m of 264 | 18 k | 22 k, 15 f, 48 m of 85 |

**What the matches are** (from `merged_scores.csv`; post-hoc verdicts in brackets):
- **21, water from the north:** the Naʿaran aqueduct from ʿEin Nuʿeima/ʿAin Duk to the Hasmonean estate (Netzer 1989 pp. 277–279; Netzer 1975 p. 89). Every other aqueduct whose origin is stated comes from the south, west or south-west: the Jerusalem aqueducts, Doq, Cypros, Qumran, Herodium and Hyrcania S. Hyrcania N is computed at 314°, 1° outside the quadrant, and FAILs under the frozen rule.
- **21, a feature on the north of the head:** the single MATCH is the survey rule at ʿEin Qelt (1) [not confirmed]. Verified count: 0. Stone at a head: only the Hyrcania N aqueduct "begins at a dam … of large stones" (ASI 109/7/48) [a stone-built dam, not a great stone]. Heads with a recorded pool: the Lower aqueduct (pool to the west), the Upper aqueduct (the middle pool to the south), Qumran (basin to the south, INFERENCE), the Cypros aqueduct at the ʿEin Fawwar spring pool, ʿEin Qelt (1) and Mar Saba (side not stated for the last three).
- **22:** two "Solomon" reservoirs are recorded: Solomon's Pools at Artas (Mazar 1989 p. 184; the name is medieval or later, n. 47) and Birket al-Hamra, which Szanton et al. 2024 (p. 27*) identify with Josephus's Pool of Solomon (CLAIM). Neither has a recorded fissure to its east. A fissure east of a reservoir is recorded only at the Qumran aqueduct head (the tunnel cracks, Magen & Peleg 2018 p. 79, ≤ c. 60 m east of the basin; INFERENCE). A second, at ʿEin Fawwar (Meshel & Amit p. 230, point 2), is bounded only within 1 km and has no stated bearing. Neither is a Solomon reservoir.
- **29:** no unit meets all four clauses. Three units dated in the window match three clauses (conduit, great, four sides) and are UNKNOWN only on "northern": the Lower Herodium great pool (Herodian), Qumran L71 (de Vaux period Ib, hedged) and Birket Musa (possibly Herodian). Wadi el-ʿEidharawi (ASI 109/7/88) does the same but is undated. Solomon's lower pool, the Chariton great reservoir and Bir el-Qattar do the same but are dated outside the window. Hyrcania's northern double-pool member is "northern" and four-sided, but "great" and "conduit" stay unknown.
- **32, Wadi Qelt:** O-built matches are the Herodian ʿEin Fawwar–Cypros aqueduct and its ʿEin Fara feeder (Meshel & Amit pp. 229–233), Netzer's six outlets of the Prat aqueduct in the Hasmonean estate (p. 276) and ʿEin Qelt (1) [date not confirmed]. The Early Arab pipe aqueduct and Wadi Qelt (3) fail on date. No outlet in Wadi Qelt has a recorded wall at its mouth; outlets with built side walls are recorded on the Prat and Naʿaran aqueducts together (Netzer p. 280, Fig. 14), not separated.
- **32, exploratory note (no frozen branch):** the ʿArrub aqueduct to Solomon's Pools begins at ʿEin Kuweiziba (Mazar 1989 p. 170; WBADB S4652, 31.603 N, 35.151 E, inside the box). The spring carries a Koziba-like name. The plan has no branch for a Kozeba other than Wadi Qelt, so this is reported, not counted.
- **42:** the three waterfalls recorded near conduit bends are the penultimate great waterfall at the Qumran aqueduct head (bend within c. 60 m, INFERENCE from Ilan & Amit p. 284); the dry fall of a tributary of Wadi Shaq ed-Dabi that the Prat aqueduct runs through, c. 250 m from its turn north (Netzer 1989 p. 275; exactly at the 250 m threshold); and the c. 2 m "small waterfall" at the Doq intake (Amit p. 224; bend within 500 m). The ASI's Naḥal Qidron waterfall below the Hyrcania S aqueduct (109/7/83) has no recorded bend.
- **45:** the Hyrcania cisterns (fed from the Kidron: Garbrecht & Peleg p. 168) are the only trunk-wadi match; the Doq cisterns (plastered, fed by a channel from a small unnamed wadi; Amit pp. 225–227) match the any-wadi branches. The El ʿEizariya match is not confirmed. Monastery cisterns at Martyrius and Chariton fail: their channels collect slope or roof runoff.
- **46:** no reservoir with a recorded way in lies within 1 or 2 km of Ramat Raḥel or ʿEin Kerem. Within 1 km of Ramat Raḥel, the excavated pool enclosure (repo note; it supersedes the "reservoirs" of ASI 106/95), the Mar Elias pool (Mazar p. 183) and ASI 106/66 are UNKNOWN for entrance (ASI 106/92 is dated outside the window). Within 1 km of ʿEin Kerem, four ASI pools (101/215, 217, 219, 221) are UNKNOWN. The cistern match near ʿEin Kerem is Beʾer Noʿomi (ASI 101/219, a rock-hewn staircase; undated; sensitivity set only).

**Headline counts** (`headline.csv`; rows in the box / merged units):

| Count | Rows | Units |
|---|---|---|
| Aqueducts / with head recorded | 390 / 23 | 283 / 17 |
| Heads with a stone recorded / with any feature / with a feature on the north | 1 / 11 / 1 | 0 / 8 / 1 (verified: 0) |
| Reservoirs / described or planned as great / as northern / either / both | 378 / 32 / 7 / 38 / 1 | 264 / 22 / 6 / 27 / 1 |
| Cisterns / fed by channels / from a wadi / from a trunk wadi | 965 / 41 / 5 / 2 | 652 / 35 / 3 / 1 |
| Entry 32 eligible (springs, outlets, recorded heads) / at a named wadi / at Wadi Qelt | 113 / 29 / 15 | 93 / 25 / 11 |
| Installations dated in the window (in or hedged) / unhedged | 130 / 74 | 101 / 56 |

**Reading under plan §9.** In every branch m ≫ k, so rarity is not measurable from the available record. Where k = 0 (entries 22 and 29, the stone and north-side branches of 21, and 32 with a wall), existing candidate fits rest on evidence or tolerances outside this inventory. That is not a rejection. Entry 46 B-any (25 units) and entry 21 head-recorded (12 units) are common combinations. Nothing here identifies a place or bears on a deposit.

**Known limits.** The survey sentence rule is crude: one sentence can carry a date or a direction that belongs to a different feature (five confirmed errors above). Patrich's ASI records write N, S, E and W, which the frozen word list does not read as directions. Positions of literature rows are site points, so no computed bearing or "near" distance uses them except the two aqueducts with stated destinations. Aggregate rows ("cisterns") count once whatever their number. OCR of the Hebrew chapters is good but not proof-read, and one dimension (Birket el-ʿArrub "?8 × 68 m") and one grid reference (ʿEin Artas) are partly illegible.

## Blocked and not covered

- English *The Aqueducts of Israel* (Amit, Patrich & Hirschfeld eds, JRA Suppl. 46, 2002): on interlibrary loan; not read. It would add the updated English versions of the 1989 chapters, with later survey data (for example Patrich on Hyrcania, pp. 336–352, and Ilan & Amit on Qumran, pp. 380–386, as cited in repo notes). Routes already recorded in the repository (`registration/hyrcania_patrich1989_extracted.md`): Google Books GWhoAAAAMAAJ (snippets only) and HathiTrust item mdp.39015051834664 (https://babel.hathitrust.org/cgi/pt?id=mdp.39015051834664, full-text search only); the owner's interlibrary-loan request is pending.
- ASI sheets that are not online, so their ground has no ASI coverage here: 83/13 (Jericho), 83/14, 108/1 (ʿArrub and upper Wadi Biyar), 109/6, 109/8 (Qumran–ʿEin Feshkha shore), 109/9 and 109/10. These sheets are not in `https://survey.iaa.org.il/aspxService/Service_Eng.aspx/GetMaps`.
- The walled Old City of Jerusalem (no ASI records; WBADB has only some excavation rows) and the east bank of the Jordan.
- The Drive copy of the 1989 volume (ID 1-6s-nqSD-PP_FpZ788Tc0dvH_z7eziZg, 73.7 MB) was not needed; the identical file (SHA-256 `2330e0b3…`) in the owner's Downloads was OCR'd on the owner's computer.

## Figures encountered (not archived here)

The lane rules allow writes only inside this folder, so no figure was copied to `research/assets/plans`. These figures were identified from their captions in the OCR or PDF text (the images themselves were not inspected) and are candidates for the archive. The 1989 volume carries the owner's prior archiving authorization (`research/assets/plans/aqueducts1989/amit-sartaba-intake.json`); viewer page = printed page + 13. The JSTOR copies (Netzer 1975, Tsafrir 1975) have no reuse status beyond the JSTOR terms.

- Mazar 1989: Fig. 1, map of the Jerusalem aqueduct system (p. 171); Figs. 4–6, Jebel Mukabbir tunnel sections and view (pp. 175–176); Fig. 9, Biar inspection chamber, view and plan (p. 179); Fig. 14, stone pipe of the upper aqueduct, view and section (p. 182); Fig. 15, Solomon's Pools and their aqueducts (p. 184); Fig. 16, ʿEin Saleh plan and section (p. 185); Fig. 17, collecting installation after Schick (p. 185); Fig. 18, ʿEin Faruja plan and section (p. 186); Fig. 20, schematic diagram of the system (p. 187); Fig. 23, sections of the Herodium aqueduct (p. 192).
- Damati 1989: Fig. 2, pool in the upper garden (p. 300); Fig. 3, plan of the east garden (p. 301).
- Hirschfeld 1989: Fig. 1, plan of the Chariton water system (p. 305); Fig. 3, section of the great reservoir (p. 307); Figs. 6 and 8, the secondary reservoirs (pp. 308–309).
- Netzer 1975 (IEJ 25): Figs. 1 and 2 (site and palace plans), as referred to in the text.
- Ilan & Amit 1989 Fig. 1 and the Cypros and Netzer figures are already archived in `research/assets/plans/aqueducts1989/`.

## Files

| File | What it holds |
|---|---|
| PLAN.md, PLAN_AMENDMENT_1.md | Frozen plan and its pre-coding amendment |
| water.csv | 2,043 installation rows (survey and literature): type, position and CRS, feed, dimensions, coded attributes, period, date code, links (`dup_of`, `superseded_by`, `group_id`, `covered_by`), exposure flag, SHA-256 of the text read. No survey text is stored. |
| survey_rows.csv | The survey part of water.csv before merging (built from WBADB and the ASI cache) |
| site_points.csv | Points of the records and grid references that literature rows cite |
| merged_units.csv | The 1,437 merged units and their member rows |
| scores.csv | One row per eligible row × entry × branch: clause codes and the overall code |
| merged_scores.csv | The same per merged unit, with conflicts |
| counts.csv | N, k, f, m per entry × branch × lineage × date rule |
| headline.csv | The brief's headline counts |
| posthoc_checks.csv | Exploratory reading of the survey-rule MATCHes |
| sources_read.csv | Sources, pages read, hashes, access, exposure |
| asi_manifest.csv | URL, HTTP status, size, SHA-256 and fetch time of the ASI responses used |
| scripts/ | `fetch_asi.py`, `common.py`, `build_survey.py`, `literature_data.py`, `literature_data_2.py`, `build_water.py`, `score.py` |
| tests/test_water.py | Plan hashes, schema, rules, and that build_water + score reproduce the committed tables |

Run from the repository root:
```
python3 -I research/regional/water_systems/scripts/fetch_asi.py CACHE_DIR
python3 -I research/regional/water_systems/scripts/build_survey.py WBADB_data1.xlsx CACHE_DIR   # needs pandas, openpyxl, pyproj
python3 -I research/regional/water_systems/scripts/build_water.py
python3 -I research/regional/water_systems/scripts/score.py
python3 -I -m unittest discover -s research/regional/water_systems/tests -v
```

## Proposed changes for the integrator

- **Regional round log / Key reports:** add "Water systems (11 Oct): 1,437 recorded water installations in the Jericho–Jerusalem box scored against entries 21, 22, 29, 32, 42, 45, 46; no full match for 22 or 29; m ≫ k everywhere" with a link to this README.
- **OPEN_QUESTIONS (and its tracker copy), entry 32 / Choziba:** note the exploratory lead that the ʿArrub aqueduct begins at ʿEin Kuweiziba (Mazar 1989 p. 170), a Koziba-like spring name outside Wadi Qelt. No branch was frozen for it. A future test would need its own frozen plan.
- **Entry 22 note:** two reservoirs carry Solomon's name in the sources: Solomon's Pools (Artas; the name is late per Mazar n. 47) and Birket al-Hamra (Szanton et al. 2024 p. 27*, CLAIM). Neither has a recorded fissure to its east.
- **Entry 29 note (no reopening):** the best regional units dated in the window lack only the "northern" clause (Lower Herodium great pool, Qumran L71, Birket Musa).
- **Asset archive:** consider archiving the Mazar, Damati and Hirschfeld figures listed above under `research/assets/plans/aqueducts1989/`, with atlas mirrors and manifests. They fall under the owner's existing authorization for this volume.
- No change to ACTIVE_TEST, the outcome ledger or PROGRESS_METRICS: this lane changes no outcome.
