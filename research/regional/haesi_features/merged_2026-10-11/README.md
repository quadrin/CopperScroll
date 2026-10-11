# HA-ESI inventory, merged and deduplicated (phases 1, 2 and 3)

**What it is.** One table of every feature row coded from the IAA excavation reports (HA, ESI, HA-ESI) in phases 1, 2 and 3 A–D (3,223 rows from 1,607 coded reports), with each row tied to a report group (one field campaign's report in all coded versions) and a site (a named place within a stated distance), and counts by class × zone × `dated_in_window` at three levels.
**Main result.** In the four zones, 3,182 counted rows reduce to 2,292 (report group × class × zone) units from 1,167 deduplicated reports, and to 1,756 (site × class × zone) units at 772 distinct sites. Dated in the window (yes / no / unknown): rows 753 / 1,059 / 1,370; reports 615 / 763 / 914; sites 457 / 556 / 743. 142 report groups join two versions of one report (138 Hebrew HA with English ESI, 4 online reports sharing a permit); 79 conflicts between versions are recorded.
**What stays unknown.** A site count is still not a count of features on the ground: one site can hold many cisterns or tombs, one long channel can cross several sites, and rows without coordinates (144 of the 772 sites) are joined only by name. Unread reports stay silent, not empty. All counts are of the read corpus.

Exploratory bookkeeping, 11 October 2026 (merge worker). No identification claim. No phase file was changed, and no row was re-coded: classes, datings, quotes and coordinates are the phase readers'. Labels: EVIDENCE (a report says it), INFERENCE (our reasoning), CLAIM (an author's assertion).

## Freeze record

- Rules: [DEDUPE_PLAN.md](DEDUPE_PLAN.md), committed alone as `bf4320f` ("Freeze HA-ESI merged inventory dedupe plan"), 2026-10-11T17:20:27Z. SHA-256 `ff13b357ae37c558bf5cebba0db01541cc0d17db0d2b12e1c7b8fe0710be676f` (checked by the tests). No pair of reports or rows had been compared before the freeze; the plan's §8 lists what had been seen.
- Changes after the freeze, all exploratory, in [AMENDMENTS.md](AMENDMENTS.md):
  - **A1** permit parsing: no split at `/` (permits such as `S-123/2005`), licence words removed. Seen: permit formats only.
  - **A2** HA → ESI volume correspondence for R2, derived by rule from the part-B crosswalk and unambiguous first-pass links ([ha_esi_volume_map.csv](ha_esi_volume_map.csv)). Seen: the first run, where multi-season sites (City of David, Robinson's Arch, Gallicantu, Mamilla, ʿEn Gedi, Mount Zion) paired Hebrew reports with other seasons' English reports.
  - **A3** R1 (same page) also needs the author and place tests. All five first-run R1 links were different short reports on one page.
  - **A4** rows without coordinates are not joined across different reader place hints (for example `tell_es_sultan` and `jericho_palaces`).
- 88 manual decisions, each with a reason and basis ([data/manual_decisions.csv](data/manual_decisions.csv)): 48 on report pairs (19 same, 29 different), 40 on sites (15 same, 25 different). They close every pair the rules sent for review (transliterated author names such as R. Abu Riya / Rafaʿ Abu Raya, N. Mai / Natalya May; HA volumes before HA 78 that have no English volume; misprinted references) and apply the readers' own statements in the phase NOTES. All are INFERENCE made after seeing the candidates.

## Inputs

| Phase | Reports | Feature rows | Counted rows |
|---|---|---|---|
| 1 (`../reports.csv`; `../features.csv`, `../features_unlocated.csv`) | 73 | 89 + 26 | 74 |
| 2 (`../phase2_2026-10-10/`) | 274 | 526 | 526 |
| 3A HA 1961–1979 | 251 | 364 | 364 |
| 3B HA 1980–1998 | 179 | 473 | 473 |
| 3C ESI and HA-ESI 109–115 | 248 | 579 | 579 |
| 3D online T3 Jerusalem | 582 | 1,166 | 1,166 |
| **All** | **1,607** | **3,223** | **3,182** |

Not counted (kept in `features_all.csv`): 31 phase-1 `wall_tower` rows (walls are not a phase-2 class), 7 phase-1 rows outside the four zones and 3 phase-1 rows that cannot be zoned. Phase-1 rows keep their phase-1 class codes (74 counted: tombs 19, cisterns 14, channels 14, rock-cut 12, pools 7, caves 3, ritual baths 3, hoards 2); phase 2 §5 lists the small differences in class scope. Phase-1 zones: 57 from the row's point, 38 from the title gazetteer, 14 from the reader's named place, 6 none. SHA-256 of every input file is in `summary.json` (`inputs`, `report_inputs`).

## Method

- **Report groups** (plan §4). R1 same citation (with A3); R2 Hebrew HA with English ESI: publication years −1 to +6 apart, a shared surname skeleton, the place test (positions within 250 m + √2 × the two grid units, or the same name key when a position is missing), one to one, and (A2) only within the HA → ESI volume map; R3 printed with online HA-ESI (no pair met it); R4 the same permit with the place test. The preferred version is the one with more counted rows (then more classes, a position, the later year). All versions' rows stay; at level 2 the classes are the union and the dating is yes if any version's row is yes, else no if any is no, else unknown.
- **Sites** (plan §5). S1 rows with coordinates: within 250 m + √2 × (u₁ + u₂) and the same name key; S2 rows without coordinates: same zone and key (A4: not across reader place hints), joined to a located site only if one located site has that key; S4 all report-located rows of one report group; S5 manual. Single linkage; four sites spread over 1 km (Giv'at/Har Homa 2.6 km, Ramot 1.6 km, Tell el-Ful 1.4 km, Mt. Scopus B 1.2 km). S3 (shared ASI or WBADB number) found nothing: no input row cites one.
- **Name keys.** The first title segment with a distinctive word (Jerusalem, generic words such as Kh., ʿEn, Giv'at, street, tomb, and descriptors such as survey, season, period removed), in Latin and Hebrew script separately. Lists in plan §7.

## Results

Cells: yes / no / unknown (all), where yes, no and unknown are `dated_in_window`. Level 2 and 3 cells count units (report group or site) per class and zone; a unit is yes if any of its rows is yes (in any version), else no if any is no, else unknown, so the three numbers add up to the units in the cell. Generated in `summary.md` and `summary.json`.

### Level 1, rows (as coded, duplicates included)

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 1 / 3 (4) | 3 / 2 / 4 (9) | 1 / 16 / 18 (35) | 60 / 174 / 210 (444) | 64 / 193 / 235 (492) |
| pool_reservoir | 0 / 1 / 1 (2) | 9 / 2 / 2 (13) | 5 / 8 / 12 (25) | 31 / 69 / 54 (154) | 45 / 80 / 69 (194) |
| channel_aqueduct | 0 / 2 / 0 (2) | 7 / 4 / 8 (19) | 9 / 11 / 16 (36) | 74 / 235 / 149 (458) | 90 / 252 / 173 (515) |
| dam | 0 / 0 / 0 (0) | 0 / 2 / 1 (3) | 0 / 0 / 4 (4) | 5 / 5 / 11 (21) | 5 / 7 / 16 (28) |
| ritual_bath | 0 / 0 / 0 (0) | 8 / 0 / 2 (10) | 5 / 1 / 1 (7) | 89 / 7 / 17 (113) | 102 / 8 / 20 (130) |
| cave_with_finds | 0 / 0 / 1 (1) | 0 / 4 / 1 (5) | 17 / 9 / 18 (44) | 41 / 58 / 152 (251) | 58 / 71 / 172 (301) |
| tomb_burial_cave | 1 / 4 / 8 (13) | 1 / 4 / 1 (6) | 13 / 19 / 15 (47) | 243 / 193 / 165 (601) | 258 / 220 / 189 (667) |
| columbarium_dovecote | 0 / 0 / 1 (1) | 1 / 0 / 1 (2) | 0 / 0 / 1 (1) | 10 / 8 / 24 (42) | 11 / 8 / 27 (46) |
| rockcut_installation | 0 / 0 / 1 (1) | 2 / 3 / 4 (9) | 0 / 8 / 12 (20) | 102 / 179 / 450 (731) | 104 / 190 / 467 (761) |
| hoard_cache | 0 / 0 / 0 (0) | 2 / 2 / 0 (4) | 4 / 5 / 0 (9) | 10 / 23 / 2 (35) | 16 / 30 / 2 (48) |
| all classes | 1 / 8 / 15 (24) | 33 / 23 / 24 (80) | 54 / 77 / 97 (228) | 665 / 951 / 1234 (2850) | 753 / 1059 / 1370 (3182) |

### Level 2, deduplicated reports (report group x class x zone)

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 1 / 3 (4) | 2 / 1 / 3 (6) | 1 / 12 / 8 (21) | 51 / 135 / 148 (334) | 54 / 149 / 162 (365) |
| pool_reservoir | 0 / 1 / 1 (2) | 6 / 2 / 2 (10) | 5 / 6 / 11 (22) | 23 / 56 / 43 (122) | 34 / 65 / 57 (156) |
| channel_aqueduct | 0 / 2 / 0 (2) | 5 / 2 / 6 (13) | 9 / 7 / 12 (28) | 66 / 153 / 105 (324) | 80 / 164 / 123 (367) |
| dam | 0 / 0 / 0 (0) | 0 / 2 / 0 (2) | 0 / 0 / 3 (3) | 5 / 5 / 11 (21) | 5 / 7 / 14 (26) |
| ritual_bath | 0 / 0 / 0 (0) | 6 / 0 / 2 (8) | 5 / 1 / 1 (7) | 67 / 3 / 15 (85) | 78 / 4 / 18 (100) |
| cave_with_finds | 0 / 0 / 1 (1) | 0 / 3 / 1 (4) | 16 / 8 / 7 (31) | 34 / 45 / 118 (197) | 50 / 56 / 127 (233) |
| tomb_burial_cave | 1 / 3 / 7 (11) | 1 / 4 / 1 (6) | 8 / 15 / 10 (33) | 191 / 132 / 93 (416) | 201 / 154 / 111 (466) |
| columbarium_dovecote | 0 / 0 / 1 (1) | 1 / 0 / 0 (1) | 0 / 0 / 1 (1) | 9 / 6 / 22 (37) | 10 / 6 / 24 (40) |
| rockcut_installation | 0 / 0 / 1 (1) | 1 / 2 / 3 (6) | 0 / 6 / 6 (12) | 88 / 123 / 266 (477) | 89 / 131 / 276 (496) |
| hoard_cache | 0 / 0 / 0 (0) | 2 / 2 / 0 (4) | 4 / 5 / 0 (9) | 8 / 20 / 2 (30) | 14 / 27 / 2 (43) |
| all classes | 1 / 7 / 14 (22) | 24 / 18 / 18 (60) | 48 / 60 / 59 (167) | 542 / 678 / 823 (2043) | 615 / 763 / 914 (2292) |

### Level 3, distinct sites (site x class x zone)

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 1 / 3 (4) | 2 / 1 / 4 (7) | 1 / 14 / 13 (28) | 36 / 102 / 129 (267) | 39 / 118 / 149 (306) |
| pool_reservoir | 0 / 1 / 1 (2) | 2 / 2 / 1 (5) | 3 / 6 / 9 (18) | 18 / 43 / 31 (92) | 23 / 52 / 42 (117) |
| channel_aqueduct | 0 / 2 / 0 (2) | 3 / 4 / 4 (11) | 7 / 6 / 10 (23) | 43 / 97 / 66 (206) | 53 / 109 / 80 (242) |
| dam | 0 / 0 / 0 (0) | 0 / 2 / 0 (2) | 0 / 0 / 3 (3) | 3 / 4 / 10 (17) | 3 / 6 / 13 (22) |
| ritual_bath | 0 / 0 / 0 (0) | 4 / 0 / 1 (5) | 4 / 1 / 0 (5) | 49 / 2 / 12 (63) | 57 / 3 / 13 (73) |
| cave_with_finds | 0 / 0 / 1 (1) | 0 / 3 / 1 (4) | 13 / 8 / 10 (31) | 31 / 36 / 105 (172) | 44 / 47 / 117 (208) |
| tomb_burial_cave | 1 / 3 / 3 (7) | 1 / 2 / 1 (4) | 6 / 10 / 9 (25) | 132 / 88 / 77 (297) | 140 / 103 / 90 (333) |
| columbarium_dovecote | 0 / 0 / 1 (1) | 1 / 0 / 0 (1) | 0 / 0 / 1 (1) | 9 / 3 / 20 (32) | 10 / 3 / 22 (35) |
| rockcut_installation | 0 / 0 / 1 (1) | 1 / 2 / 4 (7) | 0 / 6 / 7 (13) | 74 / 88 / 203 (365) | 75 / 96 / 215 (386) |
| hoard_cache | 0 / 0 / 0 (0) | 2 / 2 / 0 (4) | 3 / 1 / 0 (4) | 8 / 16 / 2 (26) | 13 / 19 / 2 (34) |
| all classes | 1 / 7 / 10 (18) | 16 / 18 / 16 (50) | 37 / 52 / 62 (151) | 403 / 479 / 655 (1537) | 457 / 556 / 743 (1756) |

### Duplicate reports found

- 142 report groups have two versions (284 reports), all pairs: 137 part-B Hebrew HA reports with their part-C English ESI reports, 1 part-B report with a phase-1 ESI 15 report, 4 pairs of online reports sharing a permit (3 in part D, 1 in phase 2). Links: 119 automatic R2, 19 manual R2, 4 R4. No report was coded twice in the same version.
- The HA → ESI map (A2): HA 78–81 → ESI 1, 82–83 → 2, 84–85 → 3, 86–87 → 4, 88–89 → 5, 90 → 6, 92–93 → 7–8, 94–95 → 9, 96–97 → 10, 99 → 12, 100 → 13, 101–102 → 14, 103 → 15, 104 → 16, 106 → 18, 107 → 19, 108 → 20. HA 77 and earlier have no English volume by this evidence; two HA 77 reports were joined to ESI 1 by manual decision (Kh. ʿEin et-Tut, Mount Zion).
- The three ESI 15 pairs part B asked to check are all different reports: the East Talpiyot Lower Aqueduct report (HA 100) is the Hebrew of ESI 13 p. 83, not ESI 15 pp. 78–80; Arnona (HA 101–102, Greenhut and Solimany) and ESI 15 pp. 80–81 (Billig) are different excavations 15 m apart (one site at level 3); Binyane Ha'umma as part B said.
- `report_groups.csv` also lists, per group, the uncoded Hebrew headings that part B matched to an English report (`uncoded_versions`).

### Distinct sites

- 787 sites; 772 hold counted rows; 175 of these hold more than one report group (the largest: City of David with Gihon, 36 groups; the Jewish Quarter, 29; Mt. Scopus rows without coordinates, 16; ʿEn Gedi, 14).
- 628 counted sites are located by coordinates, 144 by name only. 38 sites hold rows whose key matched more than one located site (`ambiguous_name`).
- Bracket: without S2 (rows without coordinates joined only within their report group or by manual decision) there would be 968 counted sites and 2,012 site units (yes / no / unknown 553 / 639 / 820). The true number of places is probably between the two figures.

### Conflicts between versions (79, `conflicts.csv`)

- 44 a class coded in one version only (the class is counted; often the Hebrew text is fuller, for example Kh. ʿEin et-Tut, Sataf, Mar Elias).
- 26 different datings for one class: 10 resolved to yes (one version dates the feature in the window, for example the Mount Zion pool, HA 104 yes / ESI 16 unknown), 16 to no (one version dates the feature outside the window, the other leaves it undated).
- 7 different stated numbers of features; 2 positions that fail the position test (Giv'at Massuʿa, 612 m; the Frankish buildings survey, whose report reference is not the feature's).
- No zone conflict and no site spanning two zones.

## What stays uncertain

- **Name-only sites.** S2 joins rows without coordinates by key alone, so a named area (Mt. Scopus, French Hill, the Jewish Quarter) becomes one site whatever the number of tombs or plots in it; the 16 Mt. Scopus reports without coordinates form one site because several located Scopus sites exist. Some keys are shared by different places (`kerem` for ʿEn Kerem and Bet Ha-Kerem, `ram` for Kh. er-Ram and Giv'at Ram, `gillo` for Gillo and Har Gillo); in this inventory their rows are located and kept apart by distance, but S2 would join such rows if they lacked coordinates. Use the no-S2 bracket where this matters.
- **Linear features.** The Tyropoeon drainage channel and the Lower Aqueduct cross several named sites; sites are places, so they are not merged (decision on HAESI-1884 / HAESI-26183).
- **One automatic link to watch.** ESI 15 p. 144 (*Map of ʿEn Gedi, Survey*, phase 1, no rows) was joined to HA 103 pp. 89–90 (ʿEn Gedi, Hadas, pool and ritual bath) by R2; the contents differ (survey map / excavation), and part B had treated the Hebrew report as not yet coded. It changes no class count (the English version has no rows), only the report total by one.
- **ESI 1 p. 57 'Ramot'** renders two Hebrew notices (Zias, HA 78–79; Kloner, HA 80–81). It is grouped with the first; the second stays its own report, so the two tombs count as two.
- **Phase-1 classes** differ slightly from phase 2 (dams under pools, columbaria under rock-cut, caves needing finds); 74 counted rows.
- **Author skeletons** miss short or transliterated surnames (Abu Riya / Abu Raya, Mai / May); the review list caught those within the volume map, but HA–ESI pairs whose names and positions both fail are not found.
- **HA 77 and earlier** have no English volume by the A2 evidence; ESI 1 may render some HA 76–77 reports beyond the two joined by hand.

## Files

| File | What it is |
|---|---|
| `DEDUPE_PLAN.md` | Frozen rules and parameters (JSON block read by the script) |
| `AMENDMENTS.md` | A1–A4, after the freeze |
| `features_all.csv` | Every input row (3,223): phase-2 columns, then `phase`, `source_file`, `report_group`, `site_id`, `row_uid`, `counted`, `count_zone`, `zone_source`, `not_counted_reason`, `version_role`, `level2_zone` |
| `report_groups.csv` | 1,465 groups: members, preferred version, link rules, level-2 units (`class@zone=dating`), sites, uncoded Hebrew versions, conflicts |
| `sites.csv` | 787 sites: rows, report groups, keys, mean position, spread, zone, rules, level-3 units |
| `conflicts.csv` | 79 conflicts with resolution |
| `pair_candidates.csv` | Every report pair the rules tested and listed, with each test and the outcome |
| `site_review.csv` | Located row pairs within the distance whose names could not be compared (Hebrew-only and English-only), with the manual decision |
| `ha_esi_volume_map.csv` | A2 evidence and chosen correspondence |
| `data/manual_decisions.csv` | 88 manual decisions with reason and basis |
| `summary.json`, `summary.md` | Generated counts (three levels, class × zone × dating), distinct units, bracket, conflicts |
| `scripts/build_merged.py` | Rebuilds everything from the source tables (standard library) |
| `tests/test_merged.py` | Plan hash and freeze commit, helpers, byte-identical rebuild, row conservation, partition of reports, level arithmetic, manual decisions, README tables |

## Run and test

From the repository root:

```sh
python3 -I -B research/regional/haesi_features/merged_2026-10-11/scripts/build_merged.py
python3 -I -B -m unittest discover -s research/regional/haesi_features/merged_2026-10-11/tests
```

## Proposed changes for the integrator

- Entry lanes that use the HA-ESI inventory as a denominator should use level 2 (reports) or level 3 (sites) from `summary.json`, not the phase row counts, and should quote the no-S2 bracket for sites.
- Phase-3 README "Proposed, not applied", first item (deduplicate by campaign and across Hebrew/English versions): done here; the ESI 15 checks of part B are answered above.
- If a later phase adds reports, rerun the script: the volume map and groups are rebuilt by rule; new review pairs appear in `pair_candidates.csv` with `REVIEW:` and need decisions in `data/manual_decisions.csv`.
