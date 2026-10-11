# Plan amendment: the merged IAA inventory as an exploratory view (11 October 2026)

Written 11 October 2026 (UTC) by the IAA-fold worker, before any row of the merged IAA inventory was mapped to this lane, tested against this lane's box or coded with this lane's word lists. `PLAN.md` (commit 0b07fad) and `PLAN_AMENDMENT_1.md` (21d197d) are not edited.

**Status: exploratory.** The frozen plan named the phase-1 HA-ESI table (`features.csv`) as source 3; it gave 17 rows in the box (lineage HAESI). Replacing them with the merged IAA inventory (phases 1, 2 and 3, deduplicated) is a source extension made after the frozen results were seen. It never changes the frozen headline (`counts.csv` lineage MERGED; for example entry 29 Q-any, reservoirs, main date rule: 0 match, 76 fail, 188 unknown, of 264). The results are a separate view beside it. No identification claim follows, no registered outcome changes, and the closed entry 29 result stands. Every IAA row is already in the repository (exposed).

## 1. What had been seen when this was written

- This lane's PLAN.md, PLAN_AMENDMENT_1.md, README.md (all results), `scripts/build_survey.py` (head, `build_haesi`, `dedup`, `main`), `scripts/build_water.py` (all), `scripts/score.py` (all), the head of `scripts/common.py` and the test names of `tests/test_water.py`; the 17 HAESI rows of `water.csv` (ids, types, date codes).
- The merged inventory's README (class × zone counts), AMENDMENTS.md, the head of DEDUPE_PLAN.md and the column names of its tables.
- A region-wide print, without positions and mostly without site names, of some `feature_subtype` values of pool_reservoir, dam and ritual_bath rows. Among them: "large plastered reservoir (14 x 29 m, 10 m deep) fed by a long channel"; "great pool (70 x 45 m) with rock-hewn steps"; "large pool with four corner flights of steps, and a small feeding pool"; "pool on the aqueduct crossing the wadis"; "double pool with connecting channel"; "vaulted plastered reservoir with settling basin (Qasr ʿAli)"; "masonry reservoir No. 18 near spring VI, three plaster layers"; "reservoir formed by masonry walls at a spring"; "large rock-cut reservoir" (twice); "hillside reservoirs (harabbe) dammed by a wall"; "diversion dam"; "breached terrace dam in the wadi bed"; "stepped pool in a building; excavator: probably a ritual bath"; "stepped plastered rock-hewn reservoir (excavators: water store), later an oil press"; "rock-cut plastered pool or ritual bath (Area J)". Some of these could bear on entry 29 (conduit, great, four sides). Whether they lie in the box was not known.
- The caves, columbaria and tombs amendments (7e88f3d, b96833a, c14468e). All four amendments are written before any lane's rows are mapped.

## 2. Source

- `research/regional/haesi_features/merged_2026-10-11/features_all.csv` (SHA-256 `2170f7fb15b097621e07648c128719f25e50e3550d5ec8756c08fca6267e455b`), `report_groups.csv` (`06085467…`), `sites.csv` (`7e89ddce…`), commit cf60d97.
- Only what the IAA coding states is used: class, `feature_subtype`, `quote`, `n_features`, `period_as_given`, `dated_in_window`, `excavated_or_surveyed`, `site_name`, positions, `precision_m`, `crs_used`, `coordinate_source`, `report_group`, `version_role`, `site_id`. No report is re-read.

## 3. Classes and types (PLAN §4)

| Merged class | Lane type |
|---|---|
| cistern | cistern |
| pool_reservoir | reservoir_pool |
| channel_aqueduct | aqueduct |
| dam | dam (a PLAN §4 type; phase 1 had put dams under pools) |
| ritual_bath | only if the coding also calls it a pool or reservoir (→ reservoir_pool) or a cistern (→ cistern), as the frozen `build_haesi` rule; otherwise not used (PLAN §4: ritual baths are not a lane type) |

Other classes (rock-cut basins, hoards) are not used. Counted rows only.

## 4. Rows, coding, positions

- **Versions of one report.** Rows of the preferred or single version of a report group are used; rows of an alternate version only for a class the preferred version has none of.
- **Phase-1 rows are not counted twice.** The 17 frozen HAESI rows are taken out of `survey_rows.csv` for the view, and the merged rows (which include the phase-1 rows, under the version rule) take their place, in the same lineage `HAESI`.
- **Coding** by the frozen `build_haesi` rule, unchanged except that the subtype is read as a second sentence beside the quote: `attrs_for([quote, feature_subtype], site_name, …)`, then `date_code(period_as_given)` with an undated row whose `dated_in_window` is `no` coded `out`. The subtype is the report's own word for the feature (phase 2 §5); the phase-1 table had no subtype column. `aggregate` and `count` from `n_features` as frozen.
- **Positions** as frozen for HAESI: the row's `lat`/`lon`, `precision_m`. A row without coordinates is not placed (the frozen rule skipped such rows); unlocated rows are tallied by type and zone as a coverage note.
- **Exposure:** `first_read_after_freeze = no` for HAESI, as frozen; the frozen Kh. ʿAlmit flag applies by name; rows from HA 28 or HA 29 are named in the notes (`tier1_related`).

## 5. Duplicates and merging (the lane's own rules)

- PLAN §7 unchanged. The WBADB → ASI rule does not concern HA-ESI rows. The literature supersession rule (`build_water.supersede`: same type, site alias, within 1 km) applies to the IAA rows as to every survey row. The frozen plan has no rule joining an HA-ESI row to an ASI or WBADB record, so in the primary view each IAA row in the box is its own merged unit unless superseded.
- **Bracket**, reported beside the primary: an IAA row within 300 m of a merged ASI or WBADB unit of the same type is treated as a duplicate of it (the distance of the frozen WBADB ↔ ASI rule, without its name test).

## 6. Scoring and outputs

- `scripts/iaa_view.py` writes the IAA rows in the `survey_rows.csv` schema (`iaa_survey_rows.csv`), then runs the frozen `build_water.main` and `score.main`, imported unchanged, in a working copy outside the lane folder (the committed `survey_rows.csv` without its HAESI rows, plus the IAA rows; the committed `site_points.csv` and `sources_read.csv`). It runs from committed tables and never writes `water.csv`, `scores.csv`, `merged_units.csv`, `merged_scores.csv`, `counts.csv` or `headline.csv`.
- Outputs in the lane folder: `iaa_survey_rows.csv`, `iaa_counts.csv` (the full count table of the view), `iaa_headline.csv`, `iaa_view_2026-10-11.csv` (per entry × branch, lineages MERGED and HAESI, date rules main and dated: frozen k / f / m of N, with the IAA rows, the change, and the bracket), `iaa_summary.json`.
- **Post-hoc reading** (exploratory, as the frozen `posthoc_checks.csv`): every IAA-row MATCH in a non-trivial clause (head, marker, side, flow, Solomon, fissure, great, northern, four sides, conduit or feed, wadi, plaster, entrance, bend, wall, Qelt) is read against its coding fields and marked confirmed or not in `iaa_posthoc_checks.csv`. Counts are not changed by it.
- README: a dated section "IAA inventory view, 11 October 2026 (exploratory)". One test checks that the view reproduces and that its frozen columns equal `counts.csv`.

## 7. Decision wording

As PLAN §9: "k match, f fail, m unknown, of N", per entry, branch, lineage and date rule, frozen and with the IAA rows. A new match is listed with the evidence it rests on; it is exposed, so it is compatibility only.
