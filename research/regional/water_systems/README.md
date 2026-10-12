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

## IAA inventory view, 11 October 2026 (exploratory)

**What changed.** The merged IAA inventory (`research/regional/haesi_features/merged_2026-10-11/`, commit cf60d97) replaces the 17 phase-1 HA-ESI rows. In the box it gives 769 rows: 328 cisterns, 307 aqueducts or channels, 122 pools or reservoirs and 12 dams. 27 of them are superseded by literature sites, and the other 742 become merged units, which takes the lane from 1,437 to 2,162 units. Installations dated in the window go from 101 to 184 units.

No new match appears in entries 21, 22, 29, 32, 42 or 45. Entry 46 gains a dated match near ʿEin Kerem, and one near Ramat Raḥel at 2 km. Both are miqvaʾot that enter only because the IAA subtype mentions an "immersion pool" (see below). The frozen headline is unchanged. This is a source extension made after the results were seen, so it is exploratory.

- **Rules.** [PLAN_AMENDMENT_IAA_2026-10-11.md](PLAN_AMENDMENT_IAA_2026-10-11.md) was committed alone as `1804f6d` (2026-10-11T17:53:04Z), before any IAA row was mapped. SHA-256 `8387f23fdf84009a8746cf6c49ec90f41ea194de406082d37c511e77f54371c6`.
- **How the view was run.** The frozen `build_water` and `score` ran unchanged on working copies. The script first checks that the same procedure on the committed `survey_rows.csv` reproduces `counts.csv` and `headline.csv` byte for byte.
- **Two runs beside the primary.**
  - **300 m bracket.** 484 IAA rows lie within 300 m of an ASI or WBADB unit of the same type and are treated as duplicates (1,699 merged units).
  - **Quote-only.** The IAA rows are coded exactly as the frozen `build_haesi`, from the quote only, without the subtype. This gives 755 rows in the box.
- **Choice made after the rows were seen.** The quote-only run was added after the first run showed that the two new entry 46 matches depend on the subtype.

**k match / f fail / m unknown, of N** (lineage MERGED, main date rule; "dated" is k under the dated-only rule; the last column gives k in the bracket and quote-only runs):

| Entry | Branch | Frozen | With the IAA rows | k, dated only | k: bracket; quote-only |
|---|---|---|---|---|---|
| 21 | head recorded (S-open, N-side) | 12/30/241 of 283 | 12/182/372 of 566 | 8 → 8 | 12 of 380; 12 of 566 |
| 21 | stone at the head on its north | 0/30/253 of 283 | 0/182/384 of 566 | 0 → 0 | 0; 0 |
| 21 | water from the north (S-open, F-flow) | 1/40/242 of 283 | 1/192/373 of 566 | 1 → 1 | 1; 1 |
| 22 | Solomon's + fissure east ≤ 500 m | 0/27/237 of 264 | 0/80/297 of 377 | 0 → 0 | 0; 0 |
| 29 | conduit, great, northern, four sides (Q-any) | 0/76/188 of 264 | 0/131/246 of 377 | 0 → 0 | 0; 0 |
| 29 | the same at Jericho (Q-Jericho) | 0/239/25 of 264 | 0/352/25 of 377 | 0 → 0 | 0; 0 |
| 32 | built outlet or head at Wadi Qelt | 5/80/213 of 298 | 5/235/341 of 581 | 5 → 5 | 5; 5 |
| 32 | the same with a wall at the outlet | 0/80/218 of 298 | 0/235/346 of 581 | 0 → 0 | 0; 0 |
| 42 | waterfall by a conduit bend (250 m) | 2/0/4 of 6 | 2/0/4 of 6 | 0 → 0 | 2; 2 |
| 42 | dam or reservoir by a bend (250 m) | 0/28/272 of 300 | 0/84/341 of 425 | 0 → 0 | 0; 0 |
| 45 | cistern fed by channels from a trunk wadi | 1/92/559 of 652 | 1/248/720 of 969 | 1 → 1 | 1; 1 |
| 45 | the same, any wadi | 3/41/608 of 652 | 3/192/774 of 969 | 2 → 2 | 3; 3 |
| 46 | reservoir with a way in, Ramat Raḥel ≤ 1 km | 0/261/3 of 264 | 0/374/3 of 377 | 0 → 0 | 0; 0 |
| 46 | the same, ≤ 2 km | 0/256/8 of 264 | 1/364/12 of 377 | 0 → 1 | 0; 0 |
| 46 | the same, ʿEin Kerem ≤ 1 km | 0/260/4 of 264 | 1/371/5 of 377 | 0 → 1 | 1; 0 |
| 46 | reservoirs and cisterns, ʿEin Kerem ≤ 1 km | 1/908/7 of 916 | 2/1335/9 of 1346 | 0 → 1 | 2; 1 |
| 46 | reservoir with a way in, anywhere (B-any) | 25/27/212 of 264 | 38/80/259 of 377 | 18 → 24 | 32; 28 |

Every entry, branch, lineage and date rule is in [iaa_view_2026-10-11.csv](iaa_view_2026-10-11.csv), and the full count table is in [iaa_counts.csv](iaa_counts.csv).

**Headline counts, merged units** ([iaa_headline.csv](iaa_headline.csv)):
- Reservoirs: 264 → 377.
  - Described as great: 22 → 39.
  - Described as northern: 6 → 12.
  - Both great and northern: 1 → 2.
- Cisterns: 652 → 969; fed by channels: 35 → 48.
- Aqueducts: 283 → 566. No IAA aqueduct has a recorded head, so aqueduct heads stay at 17.

**What drives the change.**
- **Entry 46, ʿEin Kerem: worth a closer look, with caveats.** A rock-hewn stepped miqveh with an immersion pool (HA-ESI 128; "Early Roman (1st c. CE)") lies 164 m from the Ein Karem point. It matches the B-EinKerem branch (Conder's Beth ha-Kerem) at 1 km, both in the main set and dated. The caveats:
  - It is a ritual bath, not a reservoir. PLAN §4 admits a stepped installation only when the source also calls it a pool.
  - It enters only because the IAA subtype mentions its "immersion pool", so the quote-only run drops it.
  - It is exposed, as every IAA row is.
- **Entry 46, Ramat Raḥel at 2 km.** A miqveh at Beit Safafa (HA-ESI 119; late Second Temple) lies 1.7 km away and matches the same way. It disappears in the bracket run, since it lies within 300 m of an ASI reservoir, and in the quote-only run.
- **Entry 46, B-any.** 13 more units have a recorded way in, most of them stepped pools and miqvaʾot. The post-hoc reading does not confirm two of these: the steps at the Jewish Quarter swimming pool and the cleaning step at ʿEn ʿAminadav.
- **Entry 29.** No IAA reservoir meets all four clauses. The only IAA unit that meets three (conduit, great, four sides) is the Byzantine reservoir of the monastery survey (ESI 7–8; "large plastered reservoir (14 x 29 m, 10 m deep) fed by a long channel"), which fails on date. The best units dated in the window are still the frozen three.
- **Entry 32.** Three IAA aqueduct rows name Wadi Qelt springs (Qalʿat Musa from ʿEin Fara; the aqueducts from ʿEin el-Qilt to Jericho; the Wadi Qelt mill channel). None records the head or an outlet, so none matches.
- **Post-hoc reading** of all 427 IAA-row matches in non-trivial clauses ([iaa_posthoc_checks.csv](iaa_posthoc_checks.csv)): 325 confirmed, 7 partly confirmed, 95 not confirmed. The unconfirmed ones include all 41 "wall at the outlet" matches (walls along channels), 18 "four sides" matches (a square shaft or opening, an ellipse) and 13 "northern" matches (a wall or a room, not the reservoir's place). The counts above are not corrected for these readings, as in the frozen lane.

**New match worth a closer look:** the ʿEn Kerem miqveh (HA-ESI 128) for entry 46 B-EinKerem, read as above: a rule-edge match, exposed, and a ritual bath rather than a reservoir.

**Gaps.**
- 368 IAA water rows have no coordinates, so they are not placed, as under the frozen rule. They comprise 149 aqueducts, 118 cisterns, 89 pools or reservoirs and 12 dams. 14 of the reservoirs and 12 of the aqueducts are in the Jordan Valley zone, where entries 29 and 32 look.
- 66 ritual-bath rows are not used, because their coding never calls them a pool, reservoir or cistern.
- The primary view does not deduplicate IAA rows against ASI and WBADB (the frozen plan has no such rule), so merged units are an upper bound. The 300 m bracket gives 1,699 units.

Files: [iaa_survey_rows.csv](iaa_survey_rows.csv) (the 769 IAA rows in the survey schema, with their view supersession and unit), [iaa_counts.csv](iaa_counts.csv), [iaa_headline.csv](iaa_headline.csv), [iaa_view_2026-10-11.csv](iaa_view_2026-10-11.csv), [iaa_posthoc_checks.csv](iaa_posthoc_checks.csv), [iaa_summary.json](iaa_summary.json), [scripts/iaa_view.py](scripts/iaa_view.py), [tests/test_iaa_view.py](tests/test_iaa_view.py).
- Rebuild: `python3 -I research/regional/water_systems/scripts/iaa_view.py`. It uses committed tables only and never writes the frozen outputs.

## Phase 1–4 inventory view, 12 October 2026 (exploratory)

**What changed.** The merged inventory now covers phases 1–4 (`research/regional/haesi_features/merged_2026-10-12/`, commit b4a41cc). Run under the IAA-view rules unchanged, it adds 91 phase-4 rows in the box: 84 from ʿAtiqot, 6 from IAA Reports and 1 from ADAJ. QDAP, Guérin and SWP add none (no coordinates, or excluded). No new match appears in entries 21, 22, 29, 32, 42 or 45. Entry 46 gains one dated reservoir match within 2 km of Ramat Raḥel (the Armon ha-Naẓiv stepped pool) and two dated cistern-sensitivity matches within 2 km of ʿEin Kerem. All three are stepped installations that the excavators call ritual baths or miqvaʾot. The frozen headline and the IAA view are unchanged. Every row is exposed, so the whole view is exploratory.

B3 refresh (12 Oct): rerun with the frozen rules on the merge as rebuilt under its amendment B3 (`features_all.csv` SHA-256 `23a23214…`); nothing changed in substance. The Manaḥat miqveh (IAA Reports, row `IAAR3-manahat`) lies in the box, 3.19 km from Ramat Raḥel and 2.99 km from the lane's ʿEin Kerem point (lane script), but its coding never calls it a pool, reservoir or cistern, so it is not used (phase-4 ritual baths not used: 8 → 9). The Efrata storage cave is not a water class. Survey rows, counts, scores and matches are byte-identical; no new post-hoc reading arose. Only the script's input pins and `phase4_summary.json` changed.

- **Rules.** [PLAN_AMENDMENT_PHASE4_2026-10-12.md](PLAN_AMENDMENT_PHASE4_2026-10-12.md) was committed alone as `6508ab7` (2026-10-12T04:49:29Z), before any phase-4 water row was printed or mapped. SHA-256 `3112926d89e6197ae704b43a05672c8c7e96fe28f64a5100dfb577af11a5f977`. Its §1 lists what had been seen: READMEs, headers, value counts and the held unit ids.
- **How it was run.** `scripts/phase4_view.py` imports the frozen `build_water` and `score` and the IAA-view helpers, all unchanged. It first checks that the frozen procedure reproduces `counts.csv` and `headline.csv`, and that the IAA-view inputs reproduce `iaa_counts.csv`, byte for byte.
- **Runs beside the primary.** Phases 1–3 alone under the new grouping; the 300 m bracket (508 rows treated as duplicates, 1,729 units); quote-only (806 rows); and "with SWP". The SWP run equals the primary, because no SWP water row has coordinates. Its only effect is that two rows of the held unit `SWP3-222-tell-es-sultan` are excluded.
- **Choice made after the rows were seen.** The `new_match_units_vs_iaa` column was fixed to apply the date rule. `iaa_view.py` lists main-rule units without the date test: 13 units dated `out` appear in the entry 46 B-any listing of `iaa_view_2026-10-11.csv` (9 for reservoirs and cisterns, 4 for reservoirs only). The IAA counts are not affected, and that file is left as committed.

**What is new**
- **Rows.** 91 phase-4 rows lie in the box: 36 cisterns, 31 aqueducts, 22 pools or reservoirs and 2 dams.
  - Dating: 21 `in`, 4 `in_hedged`, 9 `partly`, 18 undated and 39 `out`.
  - None is placed by name only.
  - 3 rows are superseded by literature sites: two Siloam Road rows by the Siloam site, and Bir Qadismu by Mar Elias.
- **Report level.** 35 report groups have phase-4 rows in the box, giving 71 group × type units. Only 2 of those units share a group with phase 1–3 rows used here.
- **Site level.** 35 sites, giving 72 site × type units: 59 have phase-4 rows only and 13 are shared with phase 1–3 rows.
- **Regrouping.** 36 phase 1–3 rows of the IAA view drop out. Their report group is now led by another version (mostly a phase-4 ʿAtiqot or IAA Reports final report) that has a row of the same class.
  - For 34 of them the preferred row is in the box.
  - For 2 (Western Wall Tunnels channels, group ATQ106-195) the preferred row has no coordinates.
  - This costs one entry 46 B-any reservoir match: HA-ESI 25927, the Western Wall Plaza stepped installation. It is now an alternate to HA-ESI 1219, whose ritual-bath row is not called a pool.
  - Phases 1–3 alone give 733 rows in the box (769 in the IAA view). The column `p13new` of the view table holds their counts.
- **Totals.** 824 inventory rows and 2,216 merged units (IAA view 2,162; frozen 1,437). Units dated in the window: 184 → 201.

**k match / f fail / m unknown, of N** (lineage MERGED, main date rule; the last column gives the primary-view k in the bracket and quote-only runs):

| Entry | Branch | Frozen | IAA view (11 Oct) | Phases 1–4 | k, dated only: IAA → 1–4 | k: bracket; quote-only |
|---|---|---|---|---|---|---|
| 21 | head recorded (S-open, N-side) | 12/30/241 of 283 | 12/182/372 of 566 | 12/190/381 of 583 | 8 → 8 | 12 of 390; 12 of 583 |
| 21 | stone at the head on its north | 0/30/253 of 283 | 0/182/384 of 566 | 0/190/393 of 583 | 0 → 0 | 0 of 390; 0 of 583 |
| 21 | water from the north (S-open, F-flow) | 1/40/242 of 283 | 1/192/373 of 566 | 1/200/382 of 583 | 1 → 1 | 1 of 390; 1 of 583 |
| 22 | Solomon's + fissure east ≤ 500 m | 0/27/237 of 264 | 0/80/297 of 377 | 0/91/303 of 394 | 0 → 0 | 0 of 326; 0 of 385 |
| 29 | conduit, great, northern, four sides (Q-any) | 0/76/188 of 264 | 0/131/246 of 377 | 0/142/252 of 394 | 0 → 0 | 0 of 326; 0 of 385 |
| 29 | the same at Jericho (Q-Jericho) | 0/239/25 of 264 | 0/352/25 of 377 | 0/369/25 of 394 | 0 → 0 | 0 of 326; 0 of 385 |
| 32 | built outlet or head at Wadi Qelt | 5/80/213 of 298 | 5/235/341 of 581 | 5/243/350 of 598 | 5 → 5 | 5 of 405; 5 of 598 |
| 32 | the same with a wall at the outlet | 0/80/218 of 298 | 0/235/346 of 581 | 0/243/355 of 598 | 0 → 0 | 0 of 405; 0 of 598 |
| 42 | waterfall by a conduit bend (250 m) | 2/0/4 of 6 | 2/0/4 of 6 | 2/0/4 of 6 | 0 → 0 | 2 of 6; 2 of 6 |
| 42 | dam or reservoir by a bend (250 m) | 0/28/272 of 300 | 0/84/341 of 425 | 0/95/349 of 444 | 0 → 0 | 0 of 375; 0 of 435 |
| 45 | cistern fed by channels from a trunk wadi | 1/92/559 of 652 | 1/248/720 of 969 | 1/248/738 of 987 | 1 → 1 | 1 of 762; 1 of 982 |
| 45 | the same, any wadi | 3/41/608 of 652 | 3/192/774 of 969 | 3/192/792 of 987 | 2 → 2 | 3 of 762; 3 of 982 |
| 46 | reservoir with a way in, Ramat Raḥel ≤ 1 km | 0/261/3 of 264 | 0/374/3 of 377 | 0/390/4 of 394 | 0 → 0 | 0 of 326; 0 of 385 |
| 46 | the same, ≤ 2 km | 0/256/8 of 264 | 1/364/12 of 377 | 2/379/13 of 394 | 1 → 2 | 1 of 326; 1 of 385 |
| 46 | reservoirs and cisterns, Ramat Raḥel ≤ 2 km | 0/892/24 of 916 | 1/1299/46 of 1346 | 2/1328/51 of 1381 | 1 → 2 | 1 of 1088; 1 of 1367 |
| 46 | reservoir with a way in, ʿEin Kerem ≤ 1 km | 0/260/4 of 264 | 1/371/5 of 377 | 1/388/5 of 394 | 1 → 1 | 1 of 326; 0 of 385 |
| 46 | reservoirs and cisterns, ʿEin Kerem ≤ 1 km | 1/908/7 of 916 | 2/1335/9 of 1346 | 2/1370/9 of 1381 | 1 → 1 | 2 of 1088; 1 of 1367 |
| 46 | reservoirs and cisterns, ʿEin Kerem ≤ 2 km | 1/894/21 of 916 | 2/1313/31 of 1346 | 4/1342/35 of 1381 | 1 → 3 | 3 of 1088; 1 of 1367 |
| 46 | reservoir with a way in, anywhere (B-any) | 25/27/212 of 264 | 38/80/259 of 377 | 39/91/264 of 394 | 24 → 26 | 33 of 326; 29 of 385 |
| 46 | reservoirs and cisterns with a way in, anywhere | 36/67/813 of 916 | 60/271/1015 of 1346 | 64/282/1035 of 1381 | 29 → 34 | 49 of 1088; 40 of 1367 |

Every entry, branch, lineage and date rule is in [phase4_view_2026-10-12.csv](phase4_view_2026-10-12.csv), with the counts of every run and the new match units. The full table is in [phase4_counts.csv](phase4_counts.csv), and the headline counts are in [phase4_headline.csv](phase4_headline.csv).
- Reservoirs: 377 → 394. Described as great: 39 → 41. Described as northern: 12 → 12. Both: 2 → 2.
- Cisterns: 969 → 987. Fed by channels: 48 → 49.
- Aqueducts: 566 → 583. Aqueduct heads stay at 17.

**New matches.** Each is listed with its source unit and printed page. All are exposed, so each is compatibility only. Distances are from the lane's points.
- **Entry 46, B-RamatRahel at 2 km (reservoirs, and reservoirs with cisterns).**
  - Row: ʿAtiqot 90 (2018), the Armon ha-Naẓiv tunnel, English summary p. 165; unit `ATQ90-001s-armon-ha-naziv-tunnel-government-house`, merged row `part_e_atiqot/reading_r2/features.csv#142`.
  - What it is: the stepped pool L5, "fed by a channel from the aqueduct", filled with 1st c. CE pottery. The excavators call it "apparently a ritual bath (miqveh)".
  - Distance: 1.94 km from Ramat Raḥel. It matches only at the 2 km sensitivity tolerance, not at 1 km.
  - It survives the bracket and quote-only runs.
  - The post-hoc reading confirms the way in and the conduit.
- **Entry 46, B-EinKerem at 2 km (sensitivity with cisterns only).** Both depend on the subtype (quote-only drops them). Neither is a reservoir row.
  - ʿAtiqot 66 (2011), Rogem Gannim, p. 86 (unit `ATQ66-079-excavations-rogem-gannim-jerusalem-installations-iron`). Cistern 2 is a plastered stepped basin; the excavator says "miqweh for the grape-treaders". Early Roman. 1.25 km from ʿEin Kerem.
  - ʿAtiqot 54 (2006), Ramat Sharet, Hebrew pp. 31*–45* (unit `ATQ54-031s-installations-burial-caves-ramat-sharet-ramat`). Miqveh 1I, with four steps, late Second Temple, became a cistern only in the Mamluk period. INFERENCE: as a cistern it is Mamluk, so its `in` date belongs to the miqveh. 1.96 km from ʿEin Kerem.
- **Entry 46, B-any (place not scored).**
  - Reservoirs, dated: the Kh. Kaʿkul stepped pools identified as miqwaʾot (ʿAtiqot 54 pp. 1–73) and Armon ha-Naẓiv L5.
  - Reservoirs with cisterns, dated, also:
    - Mount Scopus cistern L1560, with a stepped corridor entrance (ʿAtiqot 113);
    - Armenian Patriarchate Road L15, "cistern or miqveh?" (ʿAtiqot 42 p. 263);
    - Mount Scopus south slope, Installation II, a cistern converted to a miqveh (ʿAtiqot 63 pp. 27–43);
    - Rogem Gannim Cistern 2 and Ramat Sharet 1I.
  - Most of these are miqvaʾot, which PLAN §4 admits only as pools or cisterns.
- **Post-hoc reading** of all 60 phase-4 matches in non-trivial clauses ([phase4_posthoc_checks.csv](phase4_posthoc_checks.csv)): 40 confirmed, 6 partly confirmed, 14 not confirmed. 405 phase 1–3 readings were reused from `iaa_posthoc_checks.csv`. The unconfirmed matches are:
  - all 5 "wall at the outlet" matches (walls along channels);
  - "great" from "Great Revolt" (Siloam Road);
  - "great" from "3.5 × 7.0 m large" (Beit Safafa);
  - "four sides" from an elliptic cistern, a cistern mouth and a square opening;
  - "northern" where it describes a building, area, courtyard or wall.

  The counts are not corrected for these readings, as in the frozen lane.

**Misses.**
- **Entry 29.** No phase-4 reservoir meets three clauses with a passing date.
  - The Kathisma cistern (IAA Reports 69, pp. 33, 36, 62, 89–90; Byzantine) meets conduit, northern and four sides, but fails on date, and its "northern" and "four sides" are not confirmed on reading.
  - Two dated rows meet great and four sides:
    - the Giv‘ati cistern L702 (IAA Reports 52 p. 28; "large, quadrangular (2.60 × 2.80 m)");
    - the Siloam Road Plastered Pool (ʿAtiqot 101 pp. 71*–86*; 8.4 × 3 m). Its "great" is the Great Revolt, and the row is superseded by the Siloam site.
- **Entry 32.** No phase-4 aqueduct records a head or outlet. Its only "wall" matches are not confirmed.
- **Entry 45.** One phase-4 cistern is fed by a channel (Kathisma Channel 147), but it is Byzantine and the channel's source is not a wadi.
- **Entries 21, 22 and 42.** Nothing new.

**What stays unknown.**
- 111 phase-4 water rows have no coordinates and are not placed (IAA §4 rule, reused): 52 aqueducts, 37 cisterns and 22 pools or reservoirs. 18 of them name a lane place, and so could bear on entries 29, 32 and 46 (ids in `phase4_summary.json`):
  - ADAJ Kh. Qumran aqueducts, cisterns and a reservoir (items starting ADAJ 2 p. 83 and ADAJ 3 p. 75);
  - Jericho reservoirs (items starting ADAJ 1 p. 44 and ADAJ 3 p. 74);
  - the Nuweimeh aqueduct (item starting ADAJ 6/7 p. 112);
  - QDAP Kh. el-Mefjer and ʿAin el-Fawwar channels and pools;
  - QDAP ʿAin Karim (Visitation) channel, cistern and pool (item starting QDAP 8 p. 170).

  The name list also caught a Kh. Fasayil aqueduct (QDAP 10 p. 202). That site lies north of the box.
- 9 phase-4 ritual baths are not used, because they are never called pools or cisterns. 10 phase-4 rows lie outside the box. 43 SWP water rows are not used (PLAN §3.5).
- Rarity is still not measurable: m ≫ k in every branch.

**Protected material.**
- No row from a held cave area, the Tell es-Sultan strip or Kh. ʿAlmit is used. The two `SWP3-222-tell-es-sultan` rows met in the SWP run were excluded by id and not read.
- No `held.csv` row other than its `unit_id` was read. The Kh. ʿAlmit extraction files were not opened.

Files:
- [phase4_survey_rows.csv](phase4_survey_rows.csv): the 824 rows used, in the survey schema, with phase, report group, site, pages and view unit.
- [phase4_scores.csv](phase4_scores.csv): the clause codes of the phase-4 rows.
- [phase4_counts.csv](phase4_counts.csv), [phase4_headline.csv](phase4_headline.csv), [phase4_view_2026-10-12.csv](phase4_view_2026-10-12.csv), [phase4_posthoc_checks.csv](phase4_posthoc_checks.csv), [phase4_summary.json](phase4_summary.json).
- [scripts/phase4_view.py](scripts/phase4_view.py) and [tests/test_phase4_view.py](tests/test_phase4_view.py).

Rebuild with `python3 -I research/regional/water_systems/scripts/phase4_view.py`.

**Proposed shared-file changes (not applied).**
- **Regional round log or key reports:** "Water systems, phase 1–4 view (12 Oct): 91 phase-4 rows in the box; no new match for entries 21, 22, 29, 32, 42 or 45. Entry 46 has three new rule-edge matches at the 2 km tolerance, all miqvaʾot." Link to this section.
- **OPEN_QUESTIONS, entry 46 (and the tracker copy):**
  - add the Armon ha-Naẓiv stepped pool (ʿAtiqot 90 p. 165) as an exploratory, exposed lead at 1.94 km from Ramat Raḥel;
  - add that this inventory now shows several dated stepped miqvaʾot within 2 km of both Beth ha-Kerem candidates.
  No status change.
- **A placement step, frozen separately:** the 18 unlocated phase-4 rows at lane places (Qumran, Jericho, Nuweimeh, ʿAin Karim) could only enter with one. It is a new exploratory step.
- No change to ACTIVE_TEST, the outcome ledger or PROGRESS_METRICS.

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


## Manual checks and native source audit, 12 October 2026

A separate [manual-review overlay](manual_review_2026-10-12/README.md) applies the existing check ledgers to the earlier coding and supplies a [source-linked follow-up shortlist](manual_review_2026-10-12/SHORTLIST.md). The new unconfirmed word hits alter no date-eligible complete match; older source/feature/date attribution checks do alter some branches. Those are evidence corrections, with unknown support distinct from physical contradiction.

The [entry-46 original-source audit](../../assessments/entry46_baths_2026-10-12/README.md) separates Armon L5 construction and fill, Rogem’s tentative stepped phase and later staircase removal, and Ramat Sharet’s medieval cistern conversion. Its earlier bath interpretation needs its own textual/type argument. The [Netzer 1981 audit](../../sources/netzer1981_targeted_2026-10-12/README.md) finds smaller pools farther north than B101 within the source-defined Herodium complex and explicitly unlocated inlet evidence. These native-source deductions are separately documented exploratory assessments, not silent recodings of the prior tables.

## Entry 46: applied function and phase review — 12 October 2026

The [pool-reading phase review](entry46_phase_review_2026-10-12/README.md) adds consistent contained-water and narrower storage/service gates to the retained receptacle inventory, including ritual-bath descriptions previously omitted by the English keyword gate. Source labels supply only a reported-form screen; unverified water use and contemporaneity remain unknown. Armon, the tentative Rogem bath and the original Ramat bath retain conditional 2 km function/access subsets; construction, site association and numerical/leftward joins remain unresolved. Original stair removal/blockage fails only that origin model; other access remains unknown. The deep-pit reading is outside this water screen. Generated source/phase outputs are exploratory and supply no rarity denominator.
