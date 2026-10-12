# Regional inventory, merged and deduplicated (phases 1, 2, 3 and 4)

**What it is.** One table of every feature row coded in phases 1–4 (4,037 rows from 2,200 coded reports: HA, ESI and HA-ESI; ʿAtiqot and IAA Reports; QDAP; SWP and Guérin; ADAJ), each tied to a report group (one field campaign's report in all its versions and parts) and a site, with counts by class × zone × `dated_in_window` at three levels.
**Main result.** In the four zones, 3,902 counted rows reduce to 2,688 (report group × class × zone) units and to 2,097 (site × class × zone) units at 935 sites; dated in the window (yes / no / unknown): rows 906 / 1,366 / 1,630, reports 698 / 918 / 1,072, sites 523 / 686 / 888. Phase 4 adds 720 counted rows: 414 report units and 358 site units are new (phase 4 only), 104 report units and 129 site units also have phase 1–3 rows, and 55 phase-4 report groups (131 ʿAtiqot and IAA Reports articles and volumes) are joined to earlier HA, ESI or HA-ESI reports of the same excavation.
**What stays unknown.** A site count is still not a count of features on the ground. The QDAP, ADAJ, SWP and Guérin rows are placed by name in old spellings that rarely match modern names, so most of them stay separate sites (an upper bound). 159 report pairs could not be settled (56 `undetermined`, 103 listed but unreviewed) and may count one campaign twice. All counts are of the read corpus.

Exploratory bookkeeping, 11–12 October 2026 (phase-4 merge worker; amendment B3 added the owner-supplied Manaḥat and Efrata chapters, 12 October). No identification claim; no registered outcome changes. No phase file and nothing in `../merged_2026-10-11/` was changed, and no row was re-coded: classes, datings, quotes and coordinates are the phase readers'. Labels: EVIDENCE (a report says it), INFERENCE (our reasoning), CLAIM (an author's assertion).

## Freeze record

- Rules for phases 1–3, adopted unchanged: `../merged_2026-10-11/DEDUPE_PLAN.md` (commit bf4320f, SHA-256 `ff13b357ae37c558bf5cebba0db01541cc0d17db0d2b12e1c7b8fe0710be676f`), its amendments A1–A4, and its 88 manual decisions (the first 88 rows of [data/manual_decisions.csv](data/manual_decisions.csv), byte-identical). Run on phases 1–3 alone (`--phases13`), the build reproduces every `merged_2026-10-11` output byte for byte (tested).
- Phase-4 rules: [PLAN_EXTENSION.md](PLAN_EXTENSION.md), committed alone as `f596618` ("Freeze phase-4 merge extension"), SHA-256 `bedae3bf7ead121f84790d6346723c5e42bcf8e2aa9e00d833234a781803c3cf` (checked by the tests). Before the freeze only headers, value counts, a word-frequency list and the readers' NOTES had been seen; its §8 lists them. No pair had been compared.
- Changes after the freeze, both exploratory, in [AMENDMENTS.md](AMENDMENTS.md):
  - **B3** one more input: the two owner-supplied IAA Reports chapters (2 rows); the Manaḥat miqveh joins the earlier Manaḥat report group (ritual bath unknown → yes).
  - **B1** R1 (same page) uses the equal-key name test for phase-4 reports, and a manual decision can reject a listed R1 pair. The first run's five R1 links were all different SWP entries or round-up paragraphs printed on one page.
  - **B2** a manual decision may be `undetermined`: the review is closed with no link, and the pair is counted below as a possible over-count.

## Inputs

| Phase | Reports | Feature rows | Counted rows |
|---|---|---|---|
| 1–3 (as in `../merged_2026-10-11/`) | 1,607 | 3,223 | 3,182 |
| 4E ʿAtiqot 42–121 (readers r1, r2, r3) | 233 | 401 | 401 |
| 4F IAA Reports | 12 | 52 | 52 |
| 4G QDAP 1–14 | 71 | 88 | 88 |
| 4H SWP Memoirs II–III, Guérin *Judée* I | 200 | 195 (101 + 94 in two-zone squares) | 101 |
| 4I ADAJ | 77 | 76 | 76 |
| **All** | **2,200** | **4,037** | **3,902** |

Not counted (kept in `features_all.csv`): the 94 SWP rows of `features_zone_unresolved.csv` (zone Z2|Z3 or Z3|Z4), and, as before, 31 phase-1 `wall_tower` rows, 7 phase-1 rows outside the zones and 3 that cannot be zoned. The header-only `reports.csv` and `features.csv` at the top of parts E and F are not inputs. SHA-256 of every input is in `summary.json`.

## Method

- **Phases 1–3:** the frozen rules R1–R4 and S1–S5, unchanged.
- **Series (PLAN_EXTENSION §3):** ATQ, IAAR, QDAP, ADAJ, SWP and GUE, from the report id. SWP and Guérin are independent surveys and meet other sources only at the site level. Seasons of one excavation stay separate report groups, as in phases 1–3.
- **Phase-4 name keys:** the frozen key, with added drop words for article-title vocabulary (coins, pottery, glass, summary and so on) and generic words for old spellings (Khurbet, Wady, Kusr, Birket); phase 1–3 keys are unchanged. For a pair with a phase-4 report, the name test also passes when one key is contained in the other's title (N4).
- **Permits:** as A1, plus `A-1234/2005` is read as `A-1234` (A-numbers run on across years; HA-ESI prints them without the year).
- **New report links, applied after R1–R4:**
  - **R7:** IAA Reports volumes of one excavation (author and place tests).
  - **R5:** an ʿAtiqot finds or specialist report and its site report in the same volume (place test, and author or name test).
  - **R8:** a QDAP or ADAJ round-up paragraph and the full article (place test, article 1 year before to 4 years after).
  - **R6:** an ʿAtiqot or IAA Reports final report and the HA, ESI or HA-ESI preliminary report (author and place tests, final 2 years before to 40 years after, no contradicting permits).
  - Where a report's candidates lay in more than one group, the pair went to review and was decided by hand.
- **Sites:** S1–S5 and A4 unchanged.

## Results

Cells: yes / no / unknown (all), where yes, no and unknown are `dated_in_window`. Level 2 and 3 cells count units (report group or site) per class and zone; a unit is yes if any of its rows is yes, else no if any is no, else unknown. Generated in `summary.md` and `summary.json`.

### Level 1, rows (as coded, duplicates included)

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 1 / 6 (7) | 3 / 3 / 6 (12) | 3 / 17 / 24 (44) | 70 / 202 / 249 (521) | 76 / 223 / 285 (584) |
| pool_reservoir | 0 / 2 / 2 (4) | 11 / 3 / 6 (20) | 8 / 9 / 19 (36) | 39 / 98 / 64 (201) | 58 / 112 / 91 (261) |
| channel_aqueduct | 0 / 3 / 2 (5) | 9 / 7 / 14 (30) | 14 / 12 / 23 (49) | 94 / 281 / 175 (550) | 117 / 303 / 214 (634) |
| dam | 0 / 0 / 0 (0) | 0 / 2 / 2 (4) | 0 / 0 / 4 (4) | 10 / 5 / 12 (27) | 10 / 7 / 18 (35) |
| ritual_bath | 0 / 1 / 1 (2) | 8 / 0 / 2 (10) | 5 / 1 / 3 (9) | 109 / 9 / 20 (138) | 122 / 11 / 26 (159) |
| cave_with_finds | 0 / 0 / 3 (3) | 0 / 4 / 2 (6) | 18 / 14 / 24 (56) | 51 / 69 / 179 (299) | 69 / 87 / 208 (364) |
| tomb_burial_cave | 1 / 7 / 16 (24) | 1 / 8 / 1 (10) | 15 / 21 / 19 (55) | 277 / 285 / 203 (765) | 294 / 321 / 239 (854) |
| columbarium_dovecote | 0 / 0 / 1 (1) | 1 / 0 / 1 (2) | 0 / 0 / 1 (1) | 13 / 8 / 27 (48) | 14 / 8 / 30 (52) |
| rockcut_installation | 0 / 1 / 3 (4) | 2 / 3 / 5 (10) | 0 / 14 / 12 (26) | 122 / 225 / 495 (842) | 124 / 243 / 515 (882) |
| hoard_cache | 0 / 4 / 0 (4) | 3 / 3 / 0 (6) | 7 / 6 / 2 (15) | 12 / 38 / 2 (52) | 22 / 51 / 4 (77) |
| all classes | 1 / 19 / 34 (54) | 38 / 33 / 39 (110) | 70 / 94 / 131 (295) | 797 / 1220 / 1426 (3443) | 906 / 1366 / 1630 (3902) |

### Level 2, deduplicated reports (report group x class x zone)

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 1 / 6 (7) | 2 / 2 / 5 (9) | 3 / 13 / 14 (30) | 58 / 151 / 172 (381) | 63 / 167 / 197 (427) |
| pool_reservoir | 0 / 2 / 2 (4) | 8 / 3 / 5 (16) | 7 / 6 / 18 (31) | 27 / 74 / 49 (150) | 42 / 85 / 74 (201) |
| channel_aqueduct | 0 / 3 / 2 (5) | 6 / 5 / 12 (23) | 14 / 7 / 18 (39) | 76 / 172 / 117 (365) | 96 / 187 / 149 (432) |
| dam | 0 / 0 / 0 (0) | 0 / 2 / 1 (3) | 0 / 0 / 3 (3) | 6 / 5 / 12 (23) | 6 / 7 / 16 (29) |
| ritual_bath | 0 / 1 / 1 (2) | 6 / 0 / 2 (8) | 5 / 1 / 3 (9) | 74 / 5 / 14 (93) | 85 / 7 / 20 (112) |
| cave_with_finds | 0 / 0 / 3 (3) | 0 / 3 / 2 (5) | 17 / 13 / 13 (43) | 40 / 50 / 133 (223) | 57 / 66 / 151 (274) |
| tomb_burial_cave | 1 / 6 / 15 (22) | 1 / 8 / 1 (10) | 9 / 17 / 14 (40) | 207 / 168 / 115 (490) | 218 / 199 / 145 (562) |
| columbarium_dovecote | 0 / 0 / 1 (1) | 1 / 0 / 0 (1) | 0 / 0 / 1 (1) | 10 / 6 / 23 (39) | 11 / 6 / 25 (42) |
| rockcut_installation | 0 / 1 / 3 (4) | 1 / 2 / 4 (7) | 0 / 7 / 6 (13) | 99 / 144 / 278 (521) | 100 / 154 / 291 (545) |
| hoard_cache | 0 / 3 / 0 (3) | 3 / 3 / 0 (6) | 7 / 6 / 2 (15) | 10 / 28 / 2 (40) | 20 / 40 / 4 (64) |
| all classes | 1 / 17 / 33 (51) | 28 / 28 / 32 (88) | 62 / 70 / 92 (224) | 607 / 803 / 915 (2325) | 698 / 918 / 1072 (2688) |

### Level 3, distinct sites (site x class x zone)

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 1 / 6 (7) | 2 / 2 / 6 (10) | 2 / 15 / 18 (35) | 41 / 118 / 151 (310) | 45 / 136 / 181 (362) |
| pool_reservoir | 0 / 2 / 2 (4) | 3 / 3 / 5 (11) | 5 / 6 / 16 (27) | 21 / 57 / 38 (116) | 29 / 68 / 61 (158) |
| channel_aqueduct | 0 / 3 / 2 (5) | 5 / 6 / 9 (20) | 10 / 6 / 15 (31) | 50 / 116 / 78 (244) | 65 / 131 / 104 (300) |
| dam | 0 / 0 / 0 (0) | 0 / 2 / 1 (3) | 0 / 0 / 3 (3) | 2 / 4 / 11 (17) | 2 / 6 / 15 (23) |
| ritual_bath | 0 / 1 / 1 (2) | 4 / 0 / 1 (5) | 4 / 1 / 2 (7) | 55 / 4 / 12 (71) | 63 / 6 / 16 (85) |
| cave_with_finds | 0 / 0 / 3 (3) | 0 / 3 / 2 (5) | 14 / 12 / 15 (41) | 37 / 39 / 119 (195) | 51 / 54 / 139 (244) |
| tomb_burial_cave | 1 / 5 / 9 (15) | 1 / 5 / 1 (7) | 7 / 12 / 12 (31) | 147 / 112 / 96 (355) | 156 / 134 / 118 (408) |
| columbarium_dovecote | 0 / 0 / 1 (1) | 1 / 0 / 0 (1) | 0 / 0 / 1 (1) | 10 / 3 / 22 (35) | 11 / 3 / 24 (38) |
| rockcut_installation | 0 / 1 / 3 (4) | 1 / 2 / 5 (8) | 0 / 12 / 7 (19) | 82 / 106 / 212 (400) | 83 / 121 / 227 (431) |
| hoard_cache | 0 / 2 / 0 (2) | 3 / 3 / 0 (6) | 5 / 2 / 1 (8) | 10 / 20 / 2 (32) | 18 / 27 / 3 (48) |
| all classes | 1 / 15 / 27 (43) | 20 / 26 / 30 (76) | 47 / 66 / 90 (203) | 455 / 579 / 741 (1775) | 523 / 686 / 888 (2097) |

Without S2 (rows without coordinates joined only within their report group or by manual decision) there would be 1,173 counted sites and 2,408 site units (627 / 791 / 990). The true number of places is probably between the two figures.

## Phase-4 contribution

A unit is **phase 4 only** if all its counted rows are phase-4 rows, **shared** if it has rows from both, and **phases 1–3 only** otherwise.

| level | phase 4 only | shared | phases 1-3 only | shared units whose dating phase 4 changed |
|---|---|---|---|---|
| reports | 76 / 161 / 177 (414) | 50 / 49 / 5 (104) | 572 / 708 / 890 (2170) | 13 |
| sites | 63 / 136 / 159 (358) | 69 / 50 / 10 (129) | 391 / 500 / 719 (1610) | 16 |

- **What phase 4 adds.** Report units rise from 2,292 to 2,688 and site units from 1,756 to 2,097. Units with phase 1–3 rows fall from 2,292 to 2,274 (reports) and from 1,756 to 1,739 (sites), because phase-4 reports join some earlier groups and sites (below).
- **Datings changed in shared units.** Report units: 4 move from no to yes, 4 from unknown to yes and 4 from unknown to no. Site units: 6 no to yes, 5 unknown to yes, 5 unknown to no. The no-to-yes report units are the Mount Scopus chalk quarry cisterns and burial caves (ATQ113-i09), the Byzantine Street channel (ATQ120-i13) and the Kh. Kaʿkul installations (ATQ54-001). The list is in `summary.json` (`phase4.levels.*.shared_dating_changed_by_phase4`).

### Phase 4, level 1, rows

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 0 / 3 (3) | 0 / 1 / 2 (3) | 2 / 1 / 6 (9) | 10 / 28 / 39 (77) | 12 / 30 / 50 (92) |
| pool_reservoir | 0 / 1 / 1 (2) | 2 / 1 / 4 (7) | 3 / 1 / 7 (11) | 8 / 29 / 10 (47) | 13 / 32 / 22 (67) |
| channel_aqueduct | 0 / 1 / 2 (3) | 2 / 3 / 6 (11) | 5 / 1 / 7 (13) | 20 / 46 / 26 (92) | 27 / 51 / 41 (119) |
| dam | 0 / 0 / 0 (0) | 0 / 0 / 1 (1) | 0 / 0 / 0 (0) | 5 / 0 / 1 (6) | 5 / 0 / 2 (7) |
| ritual_bath | 0 / 1 / 1 (2) | 0 / 0 / 0 (0) | 0 / 0 / 2 (2) | 20 / 2 / 3 (25) | 20 / 3 / 6 (29) |
| cave_with_finds | 0 / 0 / 2 (2) | 0 / 0 / 1 (1) | 1 / 5 / 6 (12) | 10 / 11 / 27 (48) | 11 / 16 / 36 (63) |
| tomb_burial_cave | 0 / 3 / 8 (11) | 0 / 4 / 0 (4) | 2 / 2 / 4 (8) | 34 / 92 / 38 (164) | 36 / 101 / 50 (187) |
| columbarium_dovecote | 0 / 0 / 0 (0) | 0 / 0 / 0 (0) | 0 / 0 / 0 (0) | 3 / 0 / 3 (6) | 3 / 0 / 3 (6) |
| rockcut_installation | 0 / 1 / 2 (3) | 0 / 0 / 1 (1) | 0 / 6 / 0 (6) | 20 / 46 / 45 (111) | 20 / 53 / 48 (121) |
| hoard_cache | 0 / 4 / 0 (4) | 1 / 1 / 0 (2) | 3 / 1 / 2 (6) | 2 / 15 / 0 (17) | 6 / 21 / 2 (29) |
| all classes | 0 / 11 / 19 (30) | 5 / 10 / 15 (30) | 16 / 17 / 34 (67) | 132 / 269 / 192 (593) | 153 / 307 / 260 (720) |

### Phase 4, level 2, phase-4-only report units

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 0 / 3 (3) | 0 / 1 / 2 (3) | 2 / 1 / 6 (9) | 5 / 19 / 26 (50) | 7 / 21 / 37 (65) |
| pool_reservoir | 0 / 1 / 1 (2) | 2 / 1 / 3 (6) | 2 / 0 / 7 (9) | 4 / 17 / 7 (28) | 8 / 19 / 18 (45) |
| channel_aqueduct | 0 / 1 / 2 (3) | 1 / 3 / 6 (10) | 5 / 0 / 6 (11) | 10 / 22 / 14 (46) | 16 / 26 / 28 (70) |
| dam | 0 / 0 / 0 (0) | 0 / 0 / 1 (1) | 0 / 0 / 0 (0) | 1 / 0 / 1 (2) | 1 / 0 / 2 (3) |
| ritual_bath | 0 / 1 / 1 (2) | 0 / 0 / 0 (0) | 0 / 0 / 2 (2) | 7 / 2 / 1 (10) | 7 / 3 / 4 (14) |
| cave_with_finds | 0 / 0 / 2 (2) | 0 / 0 / 1 (1) | 1 / 5 / 6 (12) | 5 / 5 / 18 (28) | 6 / 10 / 27 (43) |
| tomb_burial_cave | 0 / 3 / 8 (11) | 0 / 4 / 0 (4) | 1 / 2 / 4 (7) | 15 / 37 / 22 (74) | 16 / 46 / 34 (96) |
| columbarium_dovecote | 0 / 0 / 0 (0) | 0 / 0 / 0 (0) | 0 / 0 / 0 (0) | 1 / 0 / 2 (3) | 1 / 0 / 2 (3) |
| rockcut_installation | 0 / 1 / 2 (3) | 0 / 0 / 1 (1) | 0 / 1 / 0 (1) | 8 / 21 / 20 (49) | 8 / 23 / 23 (54) |
| hoard_cache | 0 / 3 / 0 (3) | 1 / 1 / 0 (2) | 3 / 1 / 2 (6) | 2 / 8 / 0 (10) | 6 / 13 / 2 (21) |
| all classes | 0 / 10 / 19 (29) | 4 / 10 / 14 (28) | 14 / 10 / 33 (57) | 58 / 131 / 111 (300) | 76 / 161 / 177 (414) |

### Phase 4, level 3, phase-4-only site units

| class | Z1 Gerizim | Z2 Jordan Valley | Z3 Judean Desert | Z4 Jerusalem hills | all zones |
|---|---|---|---|---|---|
| cistern | 0 / 0 / 3 (3) | 0 / 1 / 2 (3) | 1 / 1 / 5 (7) | 5 / 16 / 25 (46) | 6 / 18 / 35 (59) |
| pool_reservoir | 0 / 1 / 1 (2) | 1 / 1 / 4 (6) | 2 / 0 / 7 (9) | 3 / 16 / 7 (26) | 6 / 18 / 19 (43) |
| channel_aqueduct | 0 / 1 / 2 (3) | 2 / 2 / 5 (9) | 3 / 0 / 5 (8) | 6 / 21 / 13 (40) | 11 / 24 / 25 (60) |
| dam | 0 / 0 / 0 (0) | 0 / 0 / 1 (1) | 0 / 0 / 0 (0) | 0 / 0 / 1 (1) | 0 / 0 / 2 (2) |
| ritual_bath | 0 / 1 / 1 (2) | 0 / 0 / 0 (0) | 0 / 0 / 2 (2) | 8 / 2 / 0 (10) | 8 / 3 / 3 (14) |
| cave_with_finds | 0 / 0 / 2 (2) | 0 / 0 / 1 (1) | 1 / 4 / 5 (10) | 4 / 4 / 16 (24) | 5 / 8 / 24 (37) |
| tomb_burial_cave | 0 / 2 / 6 (8) | 0 / 3 / 0 (3) | 1 / 1 / 4 (6) | 15 / 26 / 20 (61) | 16 / 32 / 30 (78) |
| columbarium_dovecote | 0 / 0 / 0 (0) | 0 / 0 / 0 (0) | 0 / 0 / 0 (0) | 1 / 0 / 2 (3) | 1 / 0 / 2 (3) |
| rockcut_installation | 0 / 1 / 2 (3) | 0 / 0 / 1 (1) | 0 / 6 / 0 (6) | 5 / 17 / 15 (37) | 5 / 24 / 18 (47) |
| hoard_cache | 0 / 2 / 0 (2) | 1 / 1 / 0 (2) | 2 / 1 / 1 (4) | 2 / 5 / 0 (7) | 5 / 9 / 1 (15) |
| all classes | 0 / 8 / 17 (25) | 4 / 8 / 14 (26) | 10 / 13 / 29 (52) | 49 / 107 / 99 (255) | 63 / 136 / 159 (358) |

### Phase-4 report groups joined to earlier reports

- 484 report groups hold phase-4 reports. 429 hold no phase 1–3 report; 18 of these join two or more phase-4 reports, for example an ʿAtiqot site report with its finds reports, IAA Reports 66 parts 1–3, or a QDAP round-up with Johns's Citadel summary.
- 55 groups join phase-4 reports (131 of them, all ʿAtiqot or IAA Reports) to earlier HA, ESI or HA-ESI reports:
  - 9 through a shared permit (R4);
  - 30 through R6 (author, place and years);
  - 16 only through manual decisions (reader statements or reviewed pairs).
  - No QDAP, ADAJ, SWP or Guérin unit joins an earlier report.
- 8 of these groups also join two or three earlier report groups, as seasons of one final report:
  - the Western Wall Plaza (HAESI-1219, 18755, 25927 with IAA Reports 63, 64, 67);
  - the Kathisma (with IAA Reports 69);
  - Tel Moẓa (with IAA Reports 39);
  - the Giv‘ati south-western margins (ATQ106-303);
  - the Har Ḥoma chalk-vessel assemblage (ATQ113-i02);
  - Mount Scopus East (ATQ113-i09);
  - the Byzantine Street (ATQ120-i13);
  - the Western Wall Tunnels permit A-5124 (ATQ106-195).
- At the site level, 6 sites now join two earlier sites: Mt. Scopus B, Arnona, the Western Wall Plaza, the Western Wall Tunnels, Ras el-ʿAmud and Beit Ṣafafa.

### Manual decisions

- 359 in all: the 88 frozen ones, and 271 new ones.
- New report decisions: 114 same, 97 different, 56 undetermined. New site decisions: 4 same (S5).
- Bases: 173 come from the review list, judged from coded fields (titles, authors, permits, years, positions, notes). 98 apply the readers' own statements in the phase-4 NOTES or in their `notes` fields (IAA Reports 39, 52, 63/64, 66, 69 and 3; ʿAtiqot Cave 900, Building 900, Channel 515, the Umm Leisun monastery, Sallah ed-Din Street, the ʿEn Yaʿal cave; the Tell en-Nasbeh, ʿIsawiya and Awarta same-site statements).
- All are INFERENCE and exploratory.
- Wrong automatic links undone by decision:
  - three author-skeleton collisions (Nagar / Landes-Nagar, Khalaily / Haklay, and Eshel / Shiloh in review);
  - a pottery report tied by R6 to an earlier season, although its notes name the 2018–2020 excavation (ATQ119-i13);
  - the St. Stephen's cistern (ATQ44-i16), linked to Mount Scopus (A) only through a 1 km map-reference unit.

### Conflicts (292, `conflicts.csv`)

- 195 classes coded in one version only. Mostly a finds report coding one context of its site report, or a final report coding more than the preliminary report.
- 67 different datings, 26 different stated numbers of features, and 4 positions that fail the position test.
- The 79 conflicts of phases 1–3 are among them.

## What stays uncertain

- **Old names.** QDAP, ADAJ, SWP and Guérin rows have no coordinates or only 1 km squares, and their spellings (Khurbet, Kusr, Mefjer, Nasba) rarely give the same key as modern names. They join earlier sites only where the key matches: 52 of their 265 counted rows, for example at Bethlehem, Abu Ghosh, the Citadel, Ramat Raḥel, Mamilla, Silwan, the Mount of Olives and Tell el-Ful. Phase-4-only site counts are therefore upper bounds for these sources.
- **Possible double counts at level 2:**
  - 56 `undetermined` pairs. Most are finds or final reports whose author dug several seasons at one place: the City of David, Moẓa, Giv‘ati, Wilson's Arch, Mamilla and the Armon ha-Naẓiv tunnel.
  - 103 R6 pairs listed but not reviewed: 76 where the author test failed, 27 where the place test failed.
  - Same-volume ʿAtiqot articles that no rule listed, for example the Tel Arza articles ATQ106-161 and ATQ106-187.
- **Long sites.** Sites are places joined by name and distance, so named valleys spread: Naḥal Qidron now spans 3.95 km and Naḥal Refaʾim 1.4 km. There are six sites over 1 km.
- **Two-zone squares.** 94 SWP rows stay uncounted until a georeferenced SWP gazetteer places them.
- **Classes as coded.** The phase-4 readers' choices stand. For example, IAA Reports pits are coded as rock-cut installations, and Cardo works before 130 CE count as in the window.

## Files

| File | What it is |
|---|---|
| `PLAN_EXTENSION.md` | Frozen phase-4 rules and parameters (JSON block read by the script) |
| `AMENDMENTS.md` | B1, B2, after the freeze |
| `features_all.csv` | Every input row (4,037): phase-2 columns, then `phase`, `source_file`, `report_group`, `site_id`, `row_uid`, `counted`, `count_zone`, `zone_source`, `not_counted_reason`, `version_role`, `level2_zone` |
| `report_groups.csv` | 1,883 groups: members, preferred version, link rules, level-2 units, sites, conflicts, `phase4_members`, `phase13_groups` (the `merged_2026-10-11` groups it contains) |
| `sites.csv` | 1,008 sites: rows, groups, keys, position, spread, zone, rules, level-3 units, `phase4_rows`, `phase13_sites` |
| `conflicts.csv` | 292 conflicts with resolution |
| `pair_candidates.csv` | Every report pair the rules tested and listed, with each test and the outcome (`REVIEW` closed by decisions; `LISTED` not linked) |
| `site_review.csv` | Located row pairs within the distance whose names could not be compared |
| `ha_esi_volume_map.csv` | A2 correspondence (unchanged) |
| `data/manual_decisions.csv` | 359 decisions with reason and basis (first 88 frozen) |
| `summary.json`, `summary.md` | Generated counts, the phase-4 contribution, input hashes |
| `scripts/build_merged.py` | Rebuilds everything from the source tables (standard library; `--phases13` rebuilds `merged_2026-10-11`) |
| `tests/test_merged.py` | Plan hashes and freeze commits, no input changed, phases 1–3 reproduction, byte-identical rebuild, row conservation, partition of reports, level arithmetic, phase-4 split, manual decisions, README tables |

## Run and test

From the repository root:

```sh
python3 -I -B research/regional/haesi_features/merged_2026-10-12/scripts/build_merged.py
python3 -I -B -m unittest discover -s research/regional/haesi_features/merged_2026-10-12/tests
```

## Proposed changes for the integrator

- Lanes that use the regional inventory as a denominator should take level 2 or level 3 from `merged_2026-10-12/summary.json`, quote the no-S2 bracket for sites, and say that the phase-4 old-source sites are upper bounds.
- A georeferenced SWP name list and a separately frozen transliteration rule for Mandate and nineteenth-century spellings would let the QDAP, ADAJ, SWP and Guérin rows join modern sites. Both are new exploratory steps.
- When further ʿAtiqot or IAA Reports volumes are added, rerun the script; new `REVIEW:` pairs need decisions in `data/manual_decisions.csv`.
