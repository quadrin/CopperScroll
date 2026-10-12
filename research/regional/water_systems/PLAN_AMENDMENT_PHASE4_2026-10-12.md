# Plan amendment: the phase 1–4 merged inventory as an exploratory view (12 October 2026)

Written 12 October 2026 (UTC) by the phase-4 fold worker, before any phase-4 row of a water class was printed, mapped to this lane, tested against the box or coded with this lane's word lists. `PLAN.md` (0b07fad), `PLAN_AMENDMENT_1.md` (21d197d) and `PLAN_AMENDMENT_IAA_2026-10-11.md` (1804f6d) are not edited.

**Status: exploratory.** This applies the frozen lane rules and the method of `PLAN_AMENDMENT_IAA_2026-10-11.md` (the IAA view) unchanged, with `research/regional/haesi_features/merged_2026-10-12/` as input in place of `merged_2026-10-11/`. It never changes the frozen headline (`counts.csv`, lineage MERGED) or the IAA view (`iaa_*` files). No identification claim follows, no registered outcome changes, and the closed entry 29 result stands. Where this file is silent, the IAA amendment and the frozen plan rule.

## 1. What had been seen when this was written

- This lane's PLAN.md, PLAN_AMENDMENT_1.md, PLAN_AMENDMENT_IAA_2026-10-11.md, README.md (all sections, including the IAA view results), `scripts/iaa_view.py` (all), `tests/test_iaa_view.py` (all), the head and function list of `scripts/common.py`, the function lists of `build_water.py`, `score.py` and `build_survey.py`; `iaa_summary.json` (its `tier1_rows`, empty).
- `merged_2026-10-12/README.md` (all, including its class × zone tables for phase 4: in all four zones, phase 4 has 92 cistern, 67 pool_reservoir, 119 channel_aqueduct, 7 dam and 28 ritual_bath rows; these are zone counts, not box counts).
- `phase4_2026-10-11/README.md` (all). It names some in-window phase-4 rows in words: "the Siloam and Tyropoeon dams", "the ʿAujah aqueduct system with its pools and dam", "ʿEn Gedi irrigation works", "Kh. Qumran and ʿAin Feshkha installations" (ADAJ), "a Tyropoeon drain", "the Citadel's Tenth Legion drain", "the ʿAin Karim stepped chamber" (QDAP), the "Byzantine Street channel". Whether any of these lies in the box, and how it is coded, was not looked up.
- The header of `merged_2026-10-12/features_all.csv` (identical to `merged_2026-10-11`), and value counts over all 4,035 rows (all classes together) of `phase`, `series`, `version_role`, `counted`, `protected_strip` (all `no`), `coordinate_source`, `crs_used` and `exposure_at_freeze`. Among `coordinate_source` values: `name only` (696 rows), `name only (<place>)` (for example `jericho_palaces` 26, `kh_qumran` 9, `ramat_rahel` 14, `jer_siloam` 32), `SWP square (zone split …)` 94, empty 26.
- A comparison of the phase 1–3 rows of the two merged files: the same 3,223 `row_uid`s; only `report_group` (216 rows), `version_role` (184) and `site_id` (2,849) differ. No class, quote, subtype, period or position changed.
- The `unit_id` column of the phase-4 `held.csv` files (19 ids) and which of them also occur as a `report_id` in `features_all.csv`: `SWP3-192-deir-el-kelt` and `SWP3-222-tell-es-sultan`. Their rows were not printed.
- Three `report_id` examples per phase-4 part (the first three in sort order; none is a water row by its id).

## 2. Source

`research/regional/haesi_features/merged_2026-10-12/`, commit b4a41cc:

| File | SHA-256 |
|---|---|
| features_all.csv | `940e6c04b1ecd18c79a7c88a784a463d69056f70c6e31ad18e5a18c46866d65d` |
| report_groups.csv | `38b67f3c7095993287ac9da80eb229a9752d56ff7c27cb9bb3b1024f47da702f` |
| sites.csv | `5d7458016d7955cced5540d4307570879fbc5b2071d5f644e85d3cec0fcc16db` |

Only the coded fields named in IAA amendment §2 are used. No report is re-read.

## 3. Rules applied unchanged

- **Classes and types:** IAA §3 (cistern, pool_reservoir → reservoir_pool, channel_aqueduct → aqueduct, dam; ritual_bath only if its quote or subtype calls it a pool, reservoir or cistern).
- **Versions:** IAA §4, on the `version_role` and `report_group` of the new file. A phase 1–3 row whose version became `alternate` because a phase-4 report now leads its group is used only if the preferred version has no row of its class. This follows from the rule; it is reported, not corrected.
- **Coding:** the frozen `build_haesi` rule with the subtype as a second sentence (`attrs_for([quote, feature_subtype], …)`, `date_code(period_as_given)`, undated with `dated_in_window = no` → `out`). Place clauses by name as in PLAN_AMENDMENT_1 §3.
- **Lineage:** all merged rows, of every phase and series, are lineage `HAESI` (the IAA inventory lineage), as in the IAA view. The 17 frozen HAESI rows are replaced by them.
- **Duplicates:** PLAN §7 and IAA §5 unchanged; literature supersession applies; the 300 m bracket is reported beside the primary.
- **Scoring:** the frozen `build_water.main` and `score.main`, imported unchanged, in working copies outside the lane folder.

## 4. Phase-4 sources without coordinates, and name-only placements

- **Name-only rule (reused from IAA §4).** A row is placed by its own `lat`/`lon` and `precision_m` as the phase readers coded them. This includes the readers' `name only` placements (a gazetteer or `places_v2` point for a named place); this lane makes no new placement by name. A row with an empty `lat` is not placed and not counted; such rows are tallied by type and `count_zone` as a coverage note, with the number whose site name names a lane place under PLAN_AMENDMENT_1 §3 (Qumran group, Jericho-oasis group, Cypros group, Qelt group) or Ramat Raḥel or ʿEin Kerem, listed by id only.
- **Name-placed share.** The number of phase-4 rows in the box placed by name, and of new matches resting on a name placement, is reported. A clause that needs a distance or bearing is computed only under the frozen precision rule (PLAN §6: separation at least 3 × the coarser precision), which already makes most name-placed relations UNKNOWN.
- **SWP Memoirs.** PLAN §3.5 excludes the SWP *Memoirs* from this lane by name (squares too coarse). Primary view: rows of series `SWP Memoirs` are not used. Sensitivity run "with SWP": they are used under the same rules. Guérin rows are not named in §3.5; they enter as part of the merged inventory (the source the IAA amendment admitted) in both runs.

## 5. Protected material

- **Held units:** no row whose `report_id` equals a `unit_id` in any phase-4 `held.csv` is used (at freeze: `SWP3-192-deir-el-kelt`, `SWP3-222-tell-es-sultan`, both SWP and so already outside the primary). Any such row met is listed by id only, unread.
- **Tell es-Sultan north strip:** no row with `protected_strip = yes` is used (none at freeze); as a precaution, no row of any phase whose `site_name` names Tell/Tall es-Sultan is used. Such rows are counted by id only.
- **Kh. ʿAlmit:** no row of any phase whose `site_name`, quote or report id names ʿAlmit is used or scored; they are counted by id only. The Kh. ʿAlmit extraction files are not opened.
- `first_read_after_freeze = no` for all merged rows, as frozen for HAESI; every row is exposed.

## 6. Runs and outputs

Script `scripts/phase4_view.py` (adapted from `iaa_view.py`; `iaa_view.py` itself unchanged). Runs:
1. **Harness check:** the committed `survey_rows.csv` reproduces `counts.csv` and `headline.csv` byte for byte.
2. **Primary:** committed survey rows without their HAESI rows, plus the merged phase 1–4 rows (SWP excluded).
3. **Phases 1–3 under the new grouping:** as 2, without phase-4 rows; separates the effect of phase-4 rows from regrouping.
4. **Bracket:** as 2, with the 300 m rule.
5. **Quote-only:** as 2, subtype not read.
6. **With SWP:** as 2, with SWP rows.

Outputs: `phase4_survey_rows.csv` (the merged rows used, in the survey schema, with `phase`, `report_group`, `site_id`, unit in the view), `phase4_counts.csv`, `phase4_headline.csv`, `phase4_view_2026-10-12.csv` (per entry × branch, lineages MERGED and HAESI, date rules main and dated: frozen, IAA view (from `iaa_counts.csv`), run 3, primary, deltas, bracket, quote-only, with SWP, new-match units), `phase4_scores.csv` (the view's `scores.csv` rows of phase-4 rows in the box, with report group and site), `phase4_posthoc_checks.csv`, `phase4_summary.json` (new rows, report groups and sites in the box, by type; coverage; exclusions; name-placed share).

**New** means: at row level, a phase-4 row; at report level, a report group of the new file containing a phase-4 row in the box; at site level, a `site_id` with a phase-4 row in the box, split into phase-4-only and shared, as in the merged README.

**Post-hoc reading** (IAA §6, unchanged): every MATCH of a phase-4 row in a non-trivial clause is read against its coding fields and marked confirmed, partly confirmed or not confirmed; readings of phase 1–3 rows are taken from `iaa_posthoc_checks.csv` by row id, and any phase 1–3 MATCH without one is read too. Counts are not changed by these readings.

Tests: this file's SHA-256 and its commit; that `phase4_view.py` reproduces its outputs without touching the frozen or IAA-view tables; that the view's frozen and IAA columns equal `counts.csv` and `iaa_counts.csv`; that no held, strip or ʿAlmit row is used; that the post-hoc readings are complete.

## 7. Decision wording

As PLAN §9 and IAA §7: "k match, f fail, m unknown, of N", per entry, branch, lineage and date rule, beside the frozen and IAA-view counts. A new match is listed with its source unit id and printed page; it is exposed, so it is compatibility only.
