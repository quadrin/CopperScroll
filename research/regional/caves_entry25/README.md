# Every recorded cave in the region, scored against entry 25

**What it is.** An exploratory inventory of the caves recorded between Wadi el-Makkuk/Jericho and Naḥal Ḥever (Old Israel Grid E 180–197 km, N 91–150 km), each coded against the clauses of entry 25 (VI 1–6: "the cave of the pillar with the two entrances, facing east, at the northern entrance …") under the plan frozen in [PLAN.md](PLAN.md). It gives a denominator. It makes no identification claim and changes no registered outcome, class or closed test.

**Main result.** Of **635** cave rows (**605** after merging possible duplicates; plus 30 cluster records), the cave-level pillar reading (B-PILLAR, Milik's eastward attachment) has **1 match every clause, 198 fail at least one, 436 unknown, of 635** (1 / 186 / 418 of 605). The one row is **ʿAtiqot 41 cave XII/53** (Naḥal Qumran): its east-facing opening is divided into a northern and a southern part by a built pillar (W2). At the stricter both-mouths level the only all-match row is the **Twin Cave** (repository record, exposed; exploratory). Under the terrace reading (B-TERRACE) **no** row matches every clause (0 / 195 / 440 of 635). Allegro's Temple reading (B-GATE) is not a cave; this inventory does not bear on it.

**What stays unknown.** Most rows: 412 of 635 give no usable opening count, 607 no cave-level facing and 618 no statement about a pillar. Several recorded cave populations are not in the inventory or are only partly in it (see Coverage gaps). The counts therefore cannot support a claim that a feature is rare in the landscape. A match is compatibility only: it says nothing about the jar, the scroll or the 42 talents, and XII/53's key features are now exposed, so it cannot serve as an unseen holdout.

15 October 2026 source follow-up: the atlas distinguishes Twin West, East and North, and documents substantial modern sediment removal in West. The Bar-Adon unit / atlas entrance crosswalk requires review before reusing the Twin compatibility result; Atlas North must not silently replace the earlier northern unit. Hamer2023 supplies an explicit A4-011 / Cave53 label, while the proposed XII/53 crosswalk and W2 phase remain separate questions. [Exact pages, lineage, states and acquisition target](../../feature_workbench/available_evidence_2026-10-13/cave_native_check.md#15-october-2026-intake-atlas-follow-up). The frozen results above are retained historically.

## Freeze record

| Item | Value |
|---|---|
| Plan | [PLAN.md](PLAN.md), SHA-256 `b6bc2cd9fa22df86d4ac8d0c5c723384a17f7c4670c848ac1039a711e6a77193` |
| Freeze commit | `2ff6e5acde5caaea47917dc0fb4269dfc8173609` (PLAN.md alone), 2026-10-11T04:07:54Z |
| Frozen aspect rule used | `research/preregistration/entry25_iv17_rules/` rules.json `24a1377d…`, RULES.md `794a4e5e…`, functions of check_rules.py called read-only |
| Arrival intake | [intake/atiqot41_intake.json](intake/atiqot41_intake.json): ʿAtiqot 41 zip SHA-256 `576e957a…`, 25 files hashed at 04:08:05Z, before any unread entry was opened |
| Post-freeze coding calls | [AMENDMENT_1.md](AMENDMENT_1.md) (all exploratory) |

Exposure is marked per row (`exposure`, `first_read_utc`): of the 665 rows, 434 were first read after the freeze, 149 were already in the repository and 82 stood on pages an earlier worker had opened. [exposure_audit.csv](exposure_audit.csv) checks the ʿAtiqot 41 numbers against the repository. ʿAtiqot 41 is the observation for arrival-register item `iaa-archive-cave-records`; this worker had read that item's predictions, so the extraction is not blind and the comparison is left to the integrator.

## Sources and access

| Key | Source | Coverage in this lane |
|---|---|---|
| S1–S3 | de Vaux, DJD III pp. 3–34; RB 60 pl. XX points; Reed, BASOR 135 | 1952 sites 1–40: 30 are caves (site 19 merged with XI/19); 10 sites and 2 stray finds excluded (heap, crevices, clefts, shelters, camp, building). Also caves A and B, 4Q, 5Q, 7Q–10Q, 11Q and the unfinished oval cave. Reed adds no cave; his "Cave No. 14 … a very shallow crevice" fits DJD site 15, not 14 (= 1Q). |
| S4 | ʿAtiqot 41 Part 1 (Hebrew): Regions I–XV, all excavation reports, Preface (Table 1), Index | 349 cave rows and 7 clusters; 118 records excluded. Index → [coded/a41_index_crosswalk.csv](coded/a41_index_crosswalk.csv) (1993 numbers, codes, permits, nicknames). Part 2 (finds) and the English volume not read. |
| S5 | ESI 2, 3, 5, 6, 7–8, 9, 15 (heading scan of every volume) | In-box cave reports: ESI 6 pp. 66–70 and ESI 7–8 pp. 92–95 (Patrich's cave survey: Wadi Qilt, upper and lower Wadi Makkuk, Naʿaran–Jericho cliff, Naḥal Og, Q3 = 3Q, Twin Cave) and ESI 7–8 p. 117 (Makkuk Cave). ESI 3 pp. 61–62 lies west of the box. |
| S6 | Patrich and Arubas, IEJ 39 (1989) | Only Cave 13 is described; merged with A41 X/35 (identity stated). |
| S7, S8, S14 | Bar-Adon 1989 ch. B (Twin Cave); Jones's "north entrance"; IV/11; IV/17 | Ordinary rows from repository notes. |
| S9 | ASI online maps 83/12, 109/4, 109/5, 109/7, 147 | 137 cave rows and 8 clusters from 93 records with cave words; [intake/asi_manifest.csv](intake/asi_manifest.csv). |
| S10 | WBADB (`WBADB_data1.xlsx`, SHA-256 `3db734cd…`, not committed) | 461 cave-word rows in the box: 412 cite an inventoried source (crosswalk, [intake/wbadb_crosswalk.csv](intake/wbadb_crosswalk.csv)); 34 cave rows and 12 clusters added. |
| S11 | Zissu 2023 (repository extraction) | 10 cave rows and 3 clusters not otherwise inventoried (Murabbaʿat, Naḥal David, ʿEn Gedi, Naḥal Ḥever caves). |
| S12 | Open refuge-cave and karst catalogues (Eshel, Porat, Frumkin) | Five searches and one page fetch found no readable open list. |
| S13 | IEJ 11–12 (1961–62) expedition reports; Yadin 1963 | No open copy found. |

Source files, sizes and hashes: [intake/sources_manifest.csv](intake/sources_manifest.csv).

### Coverage gaps (each one limits the counts)

- ʿAtiqot 41 has no survey list for Regions XII and XV (Preface, Table 1 note 7): only five Region XII caves and one Region XV cave are described.
- ASI sheets not online for the Qumran–Feshkha shore (109/8), the Jericho plain (83/13), and 109/9–11, 109/3, 134: their surveyed caves are missing unless another source has them.
- Naḥal Darga to Naḥal Ḥever (N 91–110 km) rests on the ʿEn Gedi ASI sheet, WBADB rows and Zissu's names; the 1960–61 expedition reports, the Porat–Eshel refuge-cave surveys and Eshel and Zissu 2019 were not read.
- The SPNI Cave Research Center surveys (Niqrot Zurim; noted in the ʿAtiqot 41 Preface) and Patrich's own 1984–85 Qumran survey numbering (Cave 13, Cave 24, Q-numbers) were not read.
- Bar-Adon 1989 beyond chapter B: WBADB rows citing it (hermits' caves in Wadi Murrar, a cave in Wadi Mazin, caves west of ʿEin et-Turabe) are crosswalk-only by PLAN 4.2 and are not counted.
- Overlaps that cannot be resolved without crosswalks: Patrich's 30 Naʿaran–Jericho cliff caves and his upper and lower Wadi Makkuk caves versus ʿAtiqot 41 Regions II–VIII; Zissu's Ketef Jericho caves versus the Quruntul regions.
- Published plans were opened only where they could change a two-opening or pillar/terrace row (AMENDMENT_1 item 8).

## Method

1. Coding by hand from each record, region by region, into [coded/](coded/) (one module per source; helper [scripts/coding.py](scripts/coding.py)). Clauses and descriptors as PLAN.md 4.1–4.5, with the calls of [AMENDMENT_1.md](AMENDMENT_1.md).
2. [scripts/build_caves.py](scripts/build_caves.py): merges stated identities (1952 site 19 = XI/19 = 2Q; ESI 6 "Q3" = 1952 site 8; Patrich survey Qilt Nos. 13, 16 = ASI Choziba Complex 7, Cell 10), adds the Index crosswalk, converts EPSG:28191 to WGS84 and ITM with pyproj, tests the box, and flags possible duplicates (within 50 m across field campaigns, or the same proper name; [duplicates.csv](duplicates.csv), 40 pairs).
3. [scripts/score.py](scripts/score.py): clauses C1–C5 for B-PILLAR and B-TERRACE, at the cave and both-mouths levels, under the four rule sets. The facing clause uses the frozen rule unchanged (word intervals, A8 levels, combine_mouths, cave_interval); PASS → match, FAIL → fail, anything else → unknown. Two plans were measured under A3–A6 because they met the triage (two openings and a pillar): XII/53 Plan 3 and, from the repository's picks, IV/17 Plan 5 ([coded/plan_measurements.json](coded/plan_measurements.json)).
4. [scripts/exposure_audit.py](scripts/exposure_audit.py) and [tests/test_lane.py](tests/test_lane.py) (plan hash and freeze commit, rule hashes, schema, byte-for-byte rebuild, spot checks).

Rebuild: `python3 -I -B scripts/build_caves.py && python3 -I -B scripts/score.py` (from this folder or anywhere).

## Results

**k match every clause, f fail at least one, m unknown, of N** (cave rows; in brackets, N_min groups):

| Branch | Level | primary | s_open_ge2 | s_singular_unknown | s_pillar_between |
|---|---|---|---|---|---|
| B-PILLAR | cave | 1 / 198 / 436 of 635 (1 / 186 / 418 of 605) | 1 / 190 / 444 | 1 / 120 / 514 | 1 / 199 / 435 |
| B-PILLAR | both-mouths | 1 / 201 / 433 (1 / 189 / 415) | 1 / 195 / 439 | 1 / 116 / 518 | 1 / 202 / 432 |
| B-TERRACE | cave | 0 / 195 / 440 (0 / 184 / 421) | 0 / 187 / 448 | 0 / 117 / 518 | 0 / 195 / 440 |
| B-TERRACE | both-mouths | 0 / 198 / 437 (0 / 187 / 418) | 0 / 192 / 443 | 0 / 113 / 522 | 0 / 198 / 437 |

All 30 cluster records are unknown on every branch.

**Partial matches by clause** (B-PILLAR, cave level, primary; match / fail / unknown of 635):

| Clause | Match | Fail | Unknown |
|---|---|---|---|
| C1 cave | 608 | 0 | 27 |
| C2p pillar | 14 | 3 | 618 |
| C2t terrace (B-TERRACE) | 30 | 0 | 605 |
| C3 two entrances | 28 | 195 | 412 |
| C4 east, cave level | 15 | 13 | 607 |
| C4 east, both mouths | 1 | 5 | 629 |
| C5 northern entrance | 9 | 187 | 439 |

**The all-match rows.**
- **XII/53** (Cohen and Israel, ʿAtiqot 41 pp. 207–210, Plan 3). EVIDENCE: a cave in conglomerate; the central hall's opening "faces east"; the 4.5 m opening was divided in two by a pillar W2, "probably built to stabilise" it; its southern part was blocked by a boulder; layers Early Islamic, Early Roman, Pottery Neolithic, PPNB. INFERENCE: two openings (northern open, southern blocked); the word "east" passes the primary sector (45°–135°) but is inconclusive for the eight-wind and sunrise sectors; Plan 3's facade chord gives 61° ± 11° (pass primary, inconclusive stricter); Fig. 4 is captioned "looking south-west". Limits: the pillar is built and undated; the printed grid (19125/12725) is probably misprinted; at the both-mouths level neither part can be measured (the pillar is masonry, A3), so that level is unknown.
- **Twin Cave** (both-mouths level only): two mouths, both described as east-facing; a thick rock pillar between the northern and southern units (Bar-Adon 1989, via the repository). All records exposed; the cave level is not measurable (no mouth positions).

**The four modelled caves** (B-PILLAR, primary):
- Twin Cave: cave level C1–C3 and C5 match, C4 not measurable → unknown; both-mouths all-match.
- Jones's "north entrance": C1 match; C2–C5 unknown (no plan, count or facing) → unknown.
- IV/11: C3 fails (one opening, Feig) and therefore C5 → fail; unknown under s_singular_unknown.
- IV/17: C1–C3 and C5 match; C4 inconclusive at both-mouths (northern mouth 123° ± 23°; southern mouth not measurable), not measurable at cave level → unknown.

**Near misses** (no failing clause, at least three matches, primary): III/11 and IV/17 (pillar between two openings, facing unmeasurable), III/3 (natural pillar at the upper of two openings), II/2, IV/21, VIII/29 and ASI 147 site 91 (two openings with a northern member; pillar and facing unrecorded). Rows whose pillar clause would change under a looser reading (AMENDMENT_1 item 2): VI/53 (a stone partition in the opening), X/51 (a drawn rock mass between its two openings), lower Wadi Makkuk Cave 1 (a rock column on the ledge in front) and Mar Saba Complex 34 (pillars carrying the front wall). Mar Saba Complex 48 has a rock pillar at its opening but an unknown number of openings.

## IAA inventory view, 11 October 2026 (exploratory)

**What changed.** The merged IAA inventory (`research/regional/haesi_features/merged_2026-10-11/`, commit cf60d97) adds 7 cave rows and 3 cluster records to this lane's region. No new row matches every clause, so the frozen headline above stands unchanged. Most of the new rows fail on the number of entrances or stay unknown. The lane did not use HA-ESI before, so the whole view is a source extension made after the results were seen. It is exploratory.

- **Rules.** [PLAN_AMENDMENT_IAA_2026-10-11.md](PLAN_AMENDMENT_IAA_2026-10-11.md) was committed alone as `7e88f3d` (2026-10-11T17:50:20Z), before any IAA row was mapped. SHA-256 `fc23efe51213b269742f50537e01f76a9816aa21ea66096e71ebedfdb1ef4125`. Choices made after the rows were seen are in the hand-coding notes ([coded/iaa_coding.csv](coded/iaa_coding.csv)).
- **Rows in the box.** 23 cave and tomb rows of the merged inventory lie in the box (preferred report versions): 22 by their own point, and 1 by its reader's place. 6 tomb rows do not call the feature a cave (graves, tumuli, rock-cut tombs, shaft graves, a tomb with built kokhim, a late burial), so they are not rows (PLAN 4.1(2)).
- **Already in the lane, not added (7).**
  - Eshel's "Makkuk Cave" (ESI 7–8) is the report the lane coded under S5.
  - Six rows are merged by a stated identity:
    - three seasons at the Cave of the Pool, Naḥal David (a lane proper name);
    - the "grotto of St. Saba" in Patrich's Mar Saba map notice (ESI 2), the survey the lane holds as ASI 109/7;
    - Patrich and Arubas's Wadi Murrar ʿEin Abu Mahmud caves (ESI 13 p. 61), which WBADB E519 cites;
    - Peleg's Mishor Adummim cave (HA-ESI 112 p. 73*), which WBADB E572 cites.
- **Added (10).**
  - Caves: the ʿEn Gedi burial cave in the cliff (HAESI-1594), the Cave of the Rope (No. 347B) and the seal-impression cave in Naḥal ʿArugot, Naḥal Ḥever Cave B, the Ḥever Nostrils Cave, a small cave in Naḥal Ḥazazon, and Bar-Adon's cave above ʿEin el-Ghuweir (HA 40; placed by description; INFERENCE: probably A41:XIV/51, but no source states it).
  - Clusters: the Wadi el-Makkuk laura caves and its two burial caves (ESI 3), and a monastery cave with a cave church (Hirschfeld, ESI 7–8). Cluster records go from 30 to 33; every cluster record is unknown.

**k match every clause / f fail at least one / m unknown, of N** (primary rule set; rows, with N_min in brackets):

| Branch | Level | Frozen | With the IAA rows |
|---|---|---|---|
| B-PILLAR | cave | 1 / 198 / 436 of 635 (1 / 186 / 418 of 605) | 1 / 201 / 440 of 642 (1 / 189 / 421 of 611) |
| B-PILLAR | both-mouths | 1 / 201 / 433 of 635 (1 / 189 / 415 of 605) | 1 / 205 / 436 of 642 (1 / 192 / 418 of 611) |
| B-TERRACE | cave | 0 / 195 / 440 of 635 (0 / 184 / 421 of 605) | 0 / 198 / 444 of 642 (0 / 187 / 424 of 611) |
| B-TERRACE | both-mouths | 0 / 198 / 437 of 635 (0 / 187 / 418 of 605) | 0 / 202 / 440 of 642 (0 / 190 / 421 of 611) |

The other rule sets are in [iaa_view_2026-10-11.csv](iaa_view_2026-10-11.csv). No rule set gains an all-match row. The all-match rows are still XII/53 (cave level) and the Twin Cave (both-mouths).

**What drives the change** (B-PILLAR, primary; codes come from the IAA coding fields only, and no plan was opened):
- **Fail on C3.** Three caves fail at both levels. The ʿEn Gedi burial cave and the Naḥal Ḥazazon cave each have one entrance, described in the singular. The Nostrils Cave has three entrances. Under `s_singular_unknown` the two singular cases become unknown.
- **Ḥever Cave B** (HAESI-25608) is the only new cave with two entrances. It is coded "two entrances (east and west)". At the both-mouths level it fails, because the west mouth lies outside the east sector. At the cave level it stays unknown, because the mouths have no positions. It has no northern member. Its point lies 36 m from ASI 147 site 413 (the Gavei Ḥever two-chamber cave), so N_min joins the two.
- **Unknown on every clause except C1:** the Cave of the Rope, the seal-impression cave and the cave above ʿEin el-Ghuweir.
- **Reported, not applied.** The IAA coding of Mishor Adummim gives one opening, facing south. If applied to WBADB E572, that row would move from unknown to fail on both branches. The frozen row is not recoded.

**New match worth a closer look:** none for entry 25. No new row records a pillar or a terrace. The only new east-facing entrance (Ḥever Cave B) is paired with a west-facing one.

**Gaps.**
- Rows of these classes with neither coordinates nor a reader place: 15 caves and 17 tombs in the Jordan Valley and Judean Desert zones. Some of them may lie in the box.
- The coding fields are short, so most clauses stay unknown.
- Three rows of other classes in the box mention a cave (a niche at the Cave of the Pool; storage pits in the Murrar caves). All belong to caves above.

Files: [iaa_units.csv](iaa_units.csv) (the 10 added rows in the `caves.csv` schema), [iaa_excluded.csv](iaa_excluded.csv) (the 13 rows read but not added, with reasons), [iaa_scores.csv](iaa_scores.csv), [iaa_summary.json](iaa_summary.json), [iaa_view_2026-10-11.csv](iaa_view_2026-10-11.csv), [scripts/iaa_view.py](scripts/iaa_view.py), [tests/test_iaa_view.py](tests/test_iaa_view.py).
- Rebuild: `python3 -I -B scripts/iaa_view.py`. It reads only committed tables and never writes the frozen outputs.

## Phase 1–4 inventory view, 12 October 2026 (exploratory)

**What changed.** The merged inventory now holds phases 1–4 (`research/regional/haesi_features/merged_2026-10-12/`, commit b4a41cc). Phase 4 adds one cave row to this lane's region: the "Small Pyrite Cave" near ʿEn Gedi. It stays unknown on every clause except C1. No new row matches every clause. The frozen headline and the 11 October IAA view stand unchanged. Phase 4 was read after the frozen results were seen, so the whole view is exploratory.

- **Rules.** [PLAN_AMENDMENT_PHASE4_2026-10-12.md](PLAN_AMENDMENT_PHASE4_2026-10-12.md) was committed alone as `9fad7f4` (2026-10-12T04:51:00Z), before any phase-4 row of this lane's classes was printed or mapped. SHA-256 `50e7a8762cc08e065251dde9e7bb248225ff1ef43a4a4d5ea0cec61885a6d8c1`. Its §1 lists what had been seen. It reruns the IAA-view method unchanged on all phases. It adds a screen for protected material, applied before a phase-4 row is read.
- **Version changes.** Phase-4 reports join some earlier report groups. Even so, all 10 rows added on 11 October are still the selected version, and the 13 rows not added then are still not added.
- **B3 refresh (12 Oct):** rerun unchanged on merged_2026-10-12 as rebuilt under its amendment B3 (input hashes in `scripts/phase4_view.py`). Nothing changed in substance. Of the two added rows, only the Efrata storage cave (`IAAR12-efrata`, cave_with_finds) is in this lane's classes; it lies west of the box, so the outside-box count goes from 83 to 84. No row was added, excluded or newly placed, there were no new review items, and every count and score is unchanged.

**Phase-4 rows of this lane's classes met by the view (10).** The three rows that were read (added or merged) are in report groups and sites that hold only phase-4 rows. None of them joins an earlier report.
- **Added (1 cave).** Hadas, ʿAtiqot 46 (2004) pp. 5–14 (Hebrew; English summary pp. 127*–128*), unit `ATQ46-i13-pyrite-lemonite-mine-near-spring-en`, site S0789. It is a rock-cut pyrite and limonite mine in the fault-escarpment cliff, 15 m long, called the "Small Pyrite Cave". It is admitted because its coding calls it a cave by name (PLAN 4.1(1)). Admitting a hewn mine is an exploratory choice. Its period is coded `partly` (Second Temple unqualified, with other periods). The same report's burial row does not call the feature a cave, so it is not admitted.
- **Merged by stated identity (2).**
  - Harding, ADAJ 2 (1953) p. 85, unit `ADAJ2-085-wadi-murabbaat`: "four large caves" in Wadi Murabbaʿat. These are the lane's Murabbaʿat caves Nos. 1–4 (Zissu 2023).
  - Klein et al., ʿAtiqot 112 (2023) pp. 53–92, unit `ATQ112-i04-hoard-ptolemaic-coins-found-murabbaat-cave`: Murabbaʿat Cave II, which is the lane's No. 2. INFERENCE: Roman II is No. 2 of the 1952 numbering.
  - Neither coding gives a pillar, terrace, opening or facing, so no clause would change.
- **Excluded as protected (6).** They were listed by id only, and their coding fields were not read for this lane.
  - 1 row whose unit is in the part-H `held.csv` (§5.1): SWP III p. 192, Deir el Kelt.
  - 3 rows by a held-area term (§5.2): ADAJ 2 p. 83 (Kh. Qumran), ADAJ 2 p. 90 (a Wadi en-Nar cave) and SWP III p. 210 (Khurbet Kumran).
  - 2 Jericho tomb rows placed at Tell es-Sultan, by strip term or position (§5.4): ADAJ 3 p. 74 and ADAJ 4–5 (Arabic) p. 6.
  - The phase-4 readers had given these rows feature rows. This lane did not check why, and excludes all of them under its conservative screen. Kh. ʿAlmit lies outside the box, and no ʿAtiqot 41 row appeared.
- **Not admitted (1).** The ʿAtiqot 46 burial row, as above.

**k match every clause / f fail at least one / m unknown, of N** (primary rule set; rows, with N_min in brackets):

| Branch | Level | Frozen | With the 11 Oct IAA rows | With the phase 1–4 rows |
|---|---|---|---|---|
| B-PILLAR | cave | 1 / 198 / 436 of 635 (1 / 186 / 418 of 605) | 1 / 201 / 440 of 642 (1 / 189 / 421 of 611) | 1 / 201 / 441 of 643 (1 / 189 / 422 of 612) |
| B-PILLAR | both-mouths | 1 / 201 / 433 of 635 | 1 / 205 / 436 of 642 | 1 / 205 / 437 of 643 |
| B-TERRACE | cave | 0 / 195 / 440 of 635 | 0 / 198 / 444 of 642 | 0 / 198 / 445 of 643 |
| B-TERRACE | both-mouths | 0 / 198 / 437 of 635 | 0 / 202 / 440 of 642 | 0 / 202 / 441 of 643 |

Cluster records stay at 33 (all unknown). The other rule sets are in [phase4_view_2026-10-12.csv](phase4_view_2026-10-12.csv). Each rule set gains exactly one unknown row and no all-match or fail row.

**Clause by clause** (B-PILLAR, cave level, primary; match / fail / unknown of 643):
- C1 cave: 616 / 0 / 27.
- C2p pillar: 14 / 3 / 626. C2t terrace (B-TERRACE): 30 / 0 / 613.
- C3 two entrances: 29 / 198 / 416.
- C4 east: 15 / 13 / 615 at the cave level, and 1 / 5 / 637 at both mouths.
- C5 northern entrance: 9 / 189 / 445.

The new phase-4 row adds a C1 match only. Among all IAA-method rows, only Naḥal Ḥever Cave B (HAESI-25608) matches anything beyond C1: C3, with two entrances. No added row matches a pillar, a terrace, an east facing or a northern entrance on either branch. Entry 25 is the only entry this lane scores.

**New matches:** none. **Misses:** the Pyrite Cave is unknown on C2–C5, and its record gives no opening count or facing. The two Murabbaʿat records give no clause value for the lane's Murabbaʿat rows.

**What stays unknown.**
- **Unplaced phase-4 rows.** 13 rows in zones Z2 and Z3 have no point and no `places_v2` id, so they are not admitted ([phase4_unplaced.csv](phase4_unplaced.csv)).
  - Probably in the box, by name (INFERENCE from `places_v2` points; not checked on a map): the SWP III Mar Saba rows (p. 219, a cave row and a tomb row), Neby Musa (p. 220), Tell Muhalhal (p. 222), Khurbet es Sumrah (pp. 212–213) and Kurm Abu Tubk (p. 213). The lane already holds the Mar Saba laura caves (ASI 109/7).
  - Probably outside the box: the QDAP ʿIrq el-Ahmar, Umm Qatafa and Umm ez-Zuweitina rows (Wadi Khareitun, west), and SWP Sebbeh (Masada, south).
  - Unknown: SWP Khurbet Samieh and Kusr el ʿAreijeh.
- **The rest of the region.** 84 phase-4 cave and tomb rows lie outside the box, and 92 have no position and lie in zones Z1 and Z4, which do not meet the box.
- **Coding limits.** The coding fields are short, and no plan was opened. The coverage gaps listed above for the frozen inventory remain.
- **Safety box.** The Qumran safety box (§5.3) also covers Nebi Musa, so it is broader than the held area. No admitted row was affected.

**Files.**
- [phase4_units.csv](phase4_units.csv): the 11 added rows (10 from 11 October and 1 from phase 4), with `phase`.
- [phase4_excluded.csv](phase4_excluded.csv) and [phase4_unplaced.csv](phase4_unplaced.csv).
- [phase4_scores.csv](phase4_scores.csv), [phase4_summary.json](phase4_summary.json) and [phase4_view_2026-10-12.csv](phase4_view_2026-10-12.csv).
- [coded/phase4_coding.csv](coded/phase4_coding.csv), [scripts/phase4_view.py](scripts/phase4_view.py) and [tests/test_phase4_view.py](tests/test_phase4_view.py).
- Rebuild with `python3 -I -B scripts/phase4_view.py`. It never writes the frozen or IAA-view outputs.

**Proposed shared-file changes (for the integrator; not applied).**
- ACTIVE_TEST / findings log: the phase 1–4 view adds 1 unknown cave row. It leaves the entry-25 denominator otherwise unchanged (B-PILLAR cave, primary: 1 / 201 / 441 of 643, exploratory). No registered outcome changes.
- Merged inventory: sites S0782 (ʿAtiqot 112, Murabbaʿat Cave II) and S0995 (ADAJ 2, Wadi Murabbaʿat) lie 43 m apart and name the same caves, but are kept as separate sites. The site count is probably one too high.
- Phase 4: four ADAJ rows (Kh. Qumran, Wadi en-Nar, two Jericho rows placed at Tell es-Sultan) and two SWP III rows (pp. 192 and 210) have feature rows. The integrator may want to confirm that they are built-site or cemetery records and not held cave records.
- Placement: a frozen rule that places SWP gazetteer terms by their `places_v2` point would let the six SWP rows probably in the box be scored. It would be a new exploratory step.

## Blocked or not read

- Israel Exploration Journal 11 (1961) and 12 (1962), the Judean Desert expedition reports (Naḥal David, Naḥal Ḥever, Cave of Letters, Cave of Horror): no open copy found. Routes: Israel Exploration Society offprints https://www.israelexplorationsociety.com/product-page/judean-desert-caves-i and https://www.israelexplorationsociety.com/product-page/copy-of-judean-desert-caves-ii (for sale); JSTOR (subscription).
- Porat and Eshel refuge-cave reports: bibliographic entries only, e.g. https://orion-bibliography.huji.ac.il/node/56426 and https://orion-bibliography.huji.ac.il/node/56864 (not opened; no full text found).
- Frumkin, karst-cave surveys (Niqrot Zurim): https://digitalcommons.usf.edu/kip_articles/3155 opened 15 October2026: Langford–Frumkin2013, *The longest limestone caves of Israel*, not a Cave53 catalogue.
- ESI 4 (1985) p. 21 (second season of Patrich's survey): not in the owner's library; not sought online.
- ʿAtiqot 41 Part 2 and the English edition; DJD I, II and VI; Yadin 1963; Patrich 1994b; ESI 13 (1995) p. 64; Porat et al. 2004, 2006, 2007; Sion and Riklin 1993: not read.
- Not sought, by instruction: the L-656 field file and IAA Archive cave records.

## Files

| File | Content |
|---|---|
| [caves.csv](caves.csv) | one row per cave or cluster (665 rows) |
| [scores.csv](scores.csv) | per row × branch × level × rule set: C1–C5, the aspect verdict, result |
| [aspect.csv](aspect.csv) | per row and level: interval and verdicts in the primary and three sensitivity sectors; plan sensitivities |
| [excluded.csv](excluded.csv) | 168 records read but not admitted, with the reason |
| [duplicates.csv](duplicates.csv) | possible-duplicate pairs and their basis |
| [summary.json](summary.json) | all counts, by clause, for rows, N_min groups and clusters |
| [exposure_audit.csv](exposure_audit.csv) | ʿAtiqot 41 numbers found in the repository |
| [coded/](coded/) | hand-coded modules, the Index crosswalk, plan measurements, Table 1 coverage |
| [intake/](intake/) | arrival intake record, source manifest, ASI manifest, WBADB crosswalk |
| [scripts/](scripts/), [tests/](tests/) | build, score, audit, intake parsers; tests |

## Proposed changes for the integrator

- **Arrival register (`iaa-archive-cave-records`).** ʿAtiqot 41 has now been opened (intake 04:08:05Z). Facts relevant to the item, for the integrator's comparison: no ʿAtiqot 41 record gives a compass facing for IV/11, IV/17 or the Twin Cave; X/47 is "two caves excavated by Vendyl Jones" with no Twin Cave, Bar-Adon or 1952 number; XI/19 is identified with 1952 cave 19 (2Q) and XI/20, hedged, with cave 20; IX/9 is a niche; VIII/28 and VIII/29 give no compass facings; the Index gives IV/17 (Cave with the Masonry Wall) as fault-escarpment Unit 1 No. 10, permit L-656, and IV/11 (Cave of the Pillar) as Unit 1 No. 4, permit L-603.
- **ACTIVE_TEST / OPEN_QUESTIONS.** Record the lane's denominator and its gaps as above; no registered outcome changes. Suggest that any future entry-25 test register XII/53 as a named alternative (its features are now exposed, so it is a control, not a holdout).
- **Twin Cave identity.** WBADB Excavations 707 'Cave of the Pillar' (193500/129600, no data) and Excavations 715 'Cave of the Twins' (193700/129300) are separate records c. 360 m apart; A41 X/47 lies c. 470 m from the Twin Cave locator. A crosswalk would settle whether the Twin Cave is in the 1993 survey.
- **"Q3".** ESI 6 p. 68 calls the Copper Scroll cave (1952 no. 8) "Cave Q3"; ʿAtiqot 41 p. 180 says Patrich and Arubas's Cave 13 (X/35) "was called Q3". Worth a note wherever the repository cites either.
- **Privacy note.** One Downloads listing in this lane used too broad a filter ("ESI" matched other file names). The extra names were not opened, copied or recorded anywhere.

## 11Q source correction, 14 October 2026 UTC

[Humbert–Fidanzio 2019 targeted review](../../sources/new_batch_2026-10-13/cave_text_changes.md) records March 2017 reinspection of the particular northern crevasse previously proposed as a second exterior entrance: Humbert says it could not have been a passage (p. 52/viewer 77). This is an exploratory correction of that named opening model. The natural pillar is internal, and the volume retains conflicting ancient-partition versus excavation-support interpretations of the masonry (pp. 63–64 and 82–85). No alternate two-mouth history is silently eliminated; the frozen regional codes/results are preserved pending a separately documented source amendment. The source supplies no IV/17 or Twin Cave ancient threshold/wall datum.


### 15 October 2026: later XII/53 source review

The [source note](../../feature_workbench/available_evidence_2026-10-13/cave_native_check.md#correct-attachment-native-freikman-figures-inspected) now verifies Freikman2020 Figure3 as the ICRC2017 survey, and records Gutfeld2020’s later northeast entrance description and original53 / XII53A naming history. Upper XII53B is a distinct cavity. Earlier east and later northeast descriptions require a reference-frame/feature crosswalk before reusing orientation results; the inspected survey does not date W2 or the ancient threshold. The historical table above preserves its original inputs. The KB exposes the later descriptions as separate observations and flags dependent XII53 evaluations for reassessment.
