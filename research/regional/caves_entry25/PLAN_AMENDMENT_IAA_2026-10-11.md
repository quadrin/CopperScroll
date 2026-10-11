# Plan amendment: the merged IAA inventory as an exploratory view (11 October 2026)

Written 11 October 2026 (UTC) by the IAA-fold worker, before any row of the merged IAA inventory was mapped to this lane, filtered by this lane's box or read for this lane's clauses. `PLAN.md` (commit 2ff6e5a) and `AMENDMENT_1.md` are not edited.

**Status: exploratory.** The frozen plan did not list the IAA excavation reports (HA, ESI, HA-ESI) as a source, except the ESI cave-survey reports of S5. Adding them now is a source extension made after the frozen results were seen. It never changes the frozen headline ("1 match every clause, 198 fail, 436 unknown, of 635", B-PILLAR, cave level, primary). The results are a separate view beside it. No identification claim follows, no registered outcome changes, and every IAA row is already in the repository (exposed).

## 1. What had been seen when this was written

- This lane's PLAN.md, AMENDMENT_1.md, README.md (all results), `scripts/build_caves.py`, `scripts/score.py`, `scripts/coding.py`, `tests/test_lane.py`, and the citations of ESI and HA reports in `caves.csv` (ESI 6 pp. 66–70, ESI 7–8 pp. 92–95 and p. 117, and the WBADB rows E572 citing HA-ESI 112 and S2298 citing HA 43).
- The merged inventory's README, AMENDMENTS.md, the first 60 lines of DEDUPE_PLAN.md, the column names of `features_all.csv`, `report_groups.csv` and `sites.csv`, and its published class × zone counts.
- A print of the class counts of all 3,223 rows, and of about 60 `feature_subtype` values of the classes cave_with_finds, columbarium_dovecote, pool_reservoir, dam and ritual_bath, region-wide and without positions. The cave subtypes seen included: "two cave complexes with window openings (Qasr er-Rawabi), nothing found"; "seven rock-cut secret passages, some reached by a vertical shaft (Nahal Mukhmas)"; "caves with Second Temple pottery, stone vessels, ropes (ʿEin Farʿa)"; "cave with Chalcolithic, Persian and Roman finds, papyri"; "cave near the ʿEn Gedi spring with Ghassulian pottery"; "laura complex of natural and man-made caves; cave-church"; "cave c. 520 m long with large halls"; "grotto of St. Saba with monastery". No row was tested against this lane's box. No tomb row's text was seen.
- The other three regional lanes' plans and READMEs (columbaria, tombs, water). Their amendments are written after this one and before any lane's rows are mapped, so that rows seen for one lane do not steer another lane's rules.

## 2. Source

- `research/regional/haesi_features/merged_2026-10-11/features_all.csv` (SHA-256 `2170f7fb15b097621e07648c128719f25e50e3550d5ec8756c08fca6267e455b`), `report_groups.csv` (`06085467…`) and `sites.csv` (`7e89ddce…`), commit cf60d97. Named-place points: `research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv` (`315474bd…`).
- Only what the IAA coding states is used: `feature_type`, `feature_subtype`, `quote`, `n_features`, `period_as_given`, `dated_in_window`, `site_name`, positions, `coordinate_source`, `report_group`, `version_role`, `site_id`. No report is re-read.

## 3. Classes and eligibility

- **cave_with_finds** rows. **tomb_burial_cave** rows too, because PLAN 4.1(1) admits burial caves.
- Only counted rows (`counted = yes`).
- **Cave word.** A row is admitted only if its IAA coding calls the feature a cave (PLAN 4.1(1)): English `cave`, `caves`, `cavern(s)`, `grotto(es)`, or Hebrew מערה, מערות, מערת (with prefix letters), in `feature_subtype` or `quote`, or, for cave_with_finds rows only, in `site_name`. Other rows (hiding complexes, tunnels and cavities not called caves; tombs, graves and cist or shaft graves not called caves) go to `iaa_excluded.csv` with the reason (PLAN 4.1(2)).
- A row whose coding calls the feature "cave or rock shelter", or equivalent, is admitted with C1 = unknown (PLAN 4.1(3)).
- Other classes (cistern, rock-cut installation, hoard or cache, columbarium) can also mention caves. They are outside this view by the brief. Their in-box rows with a cave word are only counted and reported as a coverage note.

## 4. Region and positions

- The frozen box (PLAN §2): EPSG:28191 easting 180,000–197,000 m, northing 91,000–150,000 m, closed.
- A row's point is its `lat`/`lon` (WGS 84, as converted by the phase readers from the printed grid in `crs_used`), converted to EPSG:28191 with pyproj (`always_xy`). Precision is the row's `precision_m` (nominal). A point within its precision of an edge is kept and flagged `edge`.
- A row without coordinates is in the region "by description" only if its `coordinate_source` names a reader's place id (`name only (<id>)` or `feature site name (<id>)`) whose `places_v2.csv` point lies inside the box. Its precision is that place's sigma. Rows with neither are not admitted; they are listed as `unplaced` with their zone.

## 5. Units

- **Versions of one report.** A report group is one field campaign's report (merged inventory §4). The rows of its preferred or single version are used. Rows of an alternate version are used only for a class the preferred version has none of. Dating then follows the merged level-2 rule when the group has one row of the class in each version (yes if any version is yes, else no if any is no); otherwise the row's own.
- **Row kind** (PLAN 4.1(4)). `n_features` an integer ≥ 2: a cluster row with `cluster_count` = that number. `n_features` blank or not a number, with a plural cave word: a cluster row with no count. Otherwise a cave row.
- **Period** (PLAN 4.4) from `period_as_given`, coded by the frozen descriptor rules (`yes`, `yes+other`, `partly`, `no`, empty).
- **Excavation status** from `excavated_or_surveyed`.
- **Exposure:** `exposed-repo` for every IAA row (in the repository since commit cf60d97), with the time this worker first mapped it.
- **Tier 1 flag.** Rows from HA 28 or HA 29, or from a report on Kh. ʿAlmit, are flagged `tier1_related = yes`. They were extracted by the phase-3 readers; no arrival-register item exists for them. They stay in the counts and are named in the results.

## 6. Joins to the lane's rows (the lane's own duplicate rules)

1. **Same source** (PLAN 4.2, "same source, same number"). If any report of the row's report group is a report this lane already coded under S5 (ESI 6 pp. 66–70; ESI 7–8 pp. 92–95; ESI 7–8 p. 117), the row is not added. It is listed as `already in the lane`.
2. **Stated identity** (PLAN 4.2). If the IAA coding names a cave the lane holds (an ʿAtiqot 41 number, a 1952 or Q number, or one of the lane's proper names), or a lane row's citation names the IAA report (WBADB E572 "Peleg excavation (HA-ESI 112)" at Mishor Adummim; WBADB S2298 "Shantur 1972 (HA 43)" at Tell el-Jurn), the IAA row is merged into that lane row and not added. The frozen lane row is not recoded. If the IAA coding would change one of its clauses, that is reported, not applied.
3. **Possible duplicates** (PLAN 4.2, AMENDMENT_1 items 14–16). An IAA row is flagged `possible_duplicate_of` a lane row whose point (with `coord_ok`) lies within 50 m, and of an IAA row of another report group within 50 m. A same-proper-name flag is set by hand for a cave name shared with a lane row or another IAA row. Rows of one report group are one campaign and are never flagged against each other. A merged-inventory site (`site_id`) is a place, not a cave, and never merges rows by itself.
4. **N.** N_rows counts every admitted cave row; N_min merges connected groups of possible duplicates (AMENDMENT_1 item 6: a group's result is its best member's). Cluster rows are counted separately, as frozen.

## 7. Clause coding from the IAA coding

- A script flags the PLAN 4.3 keywords (pillar, terrace, opening and direction words, English and Hebrew) in `feature_subtype` and `quote`. Every flagged row is read (the coding fields only) and coded by hand in `coded/iaa_coding.csv`. Unflagged rows take the defaults: C1 match (or unknown under 4.1(3)), all other clauses unknown.
- **C2p, C2t.** Match only if the coding states a pillar or column in or at the cave, or a terrace, platform, forecourt, courtyard or porch at its mouth (AMENDMENT_1 items 2–3 apply). Fail only if the coding states there is none. No plan is opened, so the plan-based fail rule never applies.
- **C3.** An explicit number of the cave's exterior openings. A singular description (the coding speaks of the cave's opening or entrance and of no other) gives 1, basis `singular description (IAA coding)`. A short coding field is weaker evidence of a single opening than a full record, so the `s_singular_unknown` rule set is reported beside the primary.
- **C4.** Compass words for the cave or its openings in the coding, through the frozen aspect rule (rules.json, check_rules.py) unchanged; resolution 8-point if the coding uses an intercardinal word for any opening, otherwise 4-point. A stated numeric bearing as frozen.
- **C5.** As frozen.
- **s_pillar_between:** the position of every coded pillar is classified by hand in the coding table.

## 8. Scoring and outputs

- `scripts/iaa_view.py` builds the IAA rows in the `caves.csv` schema and scores them with the functions of `scripts/score.py` (aspect, score_row, components, summarise), imported unchanged, on the union of the committed `caves.csv` and the IAA rows. It runs from committed tables (no cache needed) and never writes `caves.csv`, `scores.csv`, `aspect.csv` or `summary.json`.
- Outputs: `iaa_units.csv` (admitted IAA rows), `iaa_excluded.csv` (rows read but not admitted, with reasons), `iaa_scores.csv`, `iaa_summary.json`, and `iaa_view_2026-10-11.csv`: per branch × level × rule set, the frozen k / f / m of N (rows and N_min), the IAA rows alone, the union, and the change.
- README: a dated section "IAA inventory view, 11 October 2026 (exploratory)" with old and new counts and the rows that drive any change. One test checks that the view reproduces and that the frozen counts inside it equal `summary.json`.

## 9. Decision wording

As PLAN §6, for each branch × level × rule set: "k match every clause, f fail at least one, m unknown, of N", frozen and with the IAA rows. A new all-match row is compatibility only. It is not an unseen observation (the row is exposed) and cannot support identification or rarity while m is large.
