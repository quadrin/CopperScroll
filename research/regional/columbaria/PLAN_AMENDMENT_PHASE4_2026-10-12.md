# Plan amendment: the phase 1–4 merged inventory as an exploratory view (12 October 2026)

Written 12 October 2026 (UTC) by the columbaria fold worker, before any phase-4 row of the class `columbarium_dovecote` (or any phase-4 row with a columbarium word) was printed, mapped to this lane, tested against the region or read for a clause. `PLAN.md` (commit afdd69f), `PLAN_AMENDMENT_1.md` and `PLAN_AMENDMENT_IAA_2026-10-11.md` (commit b96833a) are not edited.

**Status: exploratory.** This applies the frozen rules (PLAN §2–§7, Amendment 1 B1–B9) and the IAA-view method (`PLAN_AMENDMENT_IAA_2026-10-11.md` §2–§8) unchanged. The only change is the input: `merged_2026-10-12` (phases 1–4) in place of `merged_2026-10-11` (phases 1–3). It is a source extension made after the frozen results and the IAA view were seen. It never changes the frozen headline (scope `frozen`: entry 38 N1/N2 0 match of 179; entry 44 Puech text level 3 match, 59 fail, 117 unknown, of 179) or the IAA view of 11 October. No identification claim follows; no registered outcome changes.

## 1. What had been seen when this was written

- Everything listed in the IAA amendment §1, the lane's IAA view outputs (`iaa_*.csv`, `iaa_summary.json`, `iaa_view_2026-10-11.csv`), `scripts/iaa_view.py`, `scripts/score.py` and the lane README in full.
- `research/regional/haesi_features/merged_2026-10-12/README.md` in full. It gives, for class `columbarium_dovecote`: 52 counted rows in phases 1–4 (14 / 8 / 30 by `dated_in_window`; 48 in Z4, 2 in Z2, 1 each in Z1 and Z3); **phase 4 adds 6 rows, all in Z4, 3 dated yes and 3 unknown by the readers' flag**; 3 phase-4-only report units (1 yes, 2 unknown) and 3 phase-4-only site units (1 / 0 / 2). It also names "the Kh. Kaʿkul installations (ATQ54-001)" among report units whose dating phase 4 changed from no to yes. Kh. Kaʿkul holds a lane columbarium (ASI 102/131). Which classes ATQ54-001 codes was not looked up.
- `research/regional/haesi_features/phase4_2026-10-11/README.md` in full (no columbarium named).
- The column headers of `features_all.csv`, `report_groups.csv`, `sites.csv` (merged_2026-10-12) and of every phase-4 `held.csv`; the value counts of `phase` (1, 2, 3A–3D, 4E–4I).
- Two checks run before this freeze, printing no row of the class:
  - The 3,223 phase 1–3 rows of `merged_2026-10-12/features_all.csv` have the same `row_uid` set as `merged_2026-10-11`, and the same values in 13 coded columns (report_id, site_name, lat, lon, precision_m, coordinate_source, feature_type, n_features, period_as_given, quote, feature_subtype, counted, count_zone).
  - For phase-4 rows of **other** classes only: `coordinate_source` patterns of rows without a point (`name only` with no id 213; `name only (<places_v2 id>)` 44; `name only (gazetteer: Z9_<zone> …)` and site-name parentheses about 100; `SWP square (zone split …)` 99), `precision_m` of rows with a point (1, 10, 100, 1000 m) and `protected_strip` (all `no`, all classes of phase 4).

Not seen: any phase-4 row of the class, its site names, subtypes, quotes, positions or report ids; any phase-4 row of another class with a columbarium word; the report-group or site membership of any phase-4 row.

## 2. Source

- `research/regional/haesi_features/merged_2026-10-12/features_all.csv` (SHA-256 `940e6c04b1ecd18c79a7c88a784a463d69056f70c6e31ad18e5a18c46866d65d`), `report_groups.csv` (`38b67f3c7095993287ac9da80eb229a9752d56ff7c27cb9bb3b1024f47da702f`), `sites.csv` (`5d7458016d7955cced5540d4307570879fbc5b2071d5f644e85d3cec0fcc16db`), commit b4a41cc; `places_v2.csv` (`315474bd3be8cce3e1776e119417e2444edd99e3f028c7413185302fc7663683`), as before. The script stops on a hash mismatch.
- As in the IAA amendment §2, only what the phase readers coded is used. No report is re-read.

## 3. Classes, eligibility and versions (unchanged)

- Primary view: counted `columbarium_dovecote` rows, phases 1–4, admitted by a frozen columbarium word in `feature_subtype`, `quote` or `site_name` (PLAN §5, Appendix A); PLAN §5 exclusions and Amendment 1 B9 as in the IAA amendment §3 (quotation marks = uncertain).
- Version rule (IAA amendment §5), now applied to the `merged_2026-10-12` report groups: rows of the preferred or single version; rows of an alternate version only if the preferred version has no columbarium row. If a phase-4 report joins an earlier report group and changes which rows are used, the change is applied and listed.
- Word-screen sensitivity (IAA amendment §3) as before: other classes with a columbarium word, not added when the report group already gives a columbarium row. Any phase-4 word-screen candidate is hand-coded and scored in a separate sensitivity line, never in the primary view.
- Rows with `counted = no` (among them the 94 SWP zone-split rows) are not used, as before. Any such row of the class, or with a columbarium word, is listed in the excluded file with its reason.

## 4. Positions and rows without coordinates (the name-only rule, reused)

- The frozen polygon (PLAN §3). A row's point is its `lat`/`lon` with precision max(`precision_m`, 100 m) (IAA amendment §4).
- A row without a point is placed at its reader's place id (`name only (<id>)` or `feature site name (<id>)`) from `places_v2.csv` with precision = that place's sigma, if the sigma is 2 km or less. Everything else is **unplaced**, listed and not counted: plain `name only`, zone-only gazetteer entries (`gazetteer: Z9_…`), site names in parentheses that are not a `places_v2` id, and SWP squares without a point.
- Reported only, never counted: for each unplaced in-class row, the position of its merged site (`sites.csv`, if `located` and spread 2 km or less), with its distance to N1 and N2 and its side of the S-A line. This shows whether an unplaced row could touch entry 38's place clause.

## 5. Coding (unchanged)

- Phase 1–3 rows keep their hand coding in `data/iaa_coding.json` (their coded fields are unchanged, §1). Phase-4 rows are coded by hand, by the same rules (IAA amendment §5), into `data/phase4_coding.json`, from `feature_subtype`, `quote`, `n_features`, `period_as_given` and `site_name`, with fort and tower words also from the other rows of the same report group. Date from `period_as_given` by PLAN §6 and Amendment 1 B1; the readers' `dated_in_window` is not used.
- Phase-4 rows carry `post_freeze_source = yes`, `exposed_before_freeze = no`, `read_via` = "merged phase 1–4 inventory row <row_uid>", `source` = `P4`.

## 6. Protected material

- A row whose `report_id` is a unit id in any phase-4 `held.csv`, or with `protected_strip = yes`, or whose site name, subtype or quote names Tell es-Sultan, is excluded and listed. The phase-4 readers gave held units no feature row, so none is expected; the script stops if one is found in the class, and the README says so.
- **Kh. ʿAlmit.** A phase-4 row whose site name, subtype or quote names ʿAlmit (`almit`, `עלמית`) is excluded from every view and not scored (no Kh. ʿAlmit extraction is compared with any model). The frozen lane row ASI 102/579 is unchanged.

## 7. Joins (unchanged)

- The same pair list as the IAA amendment §6 (300 m or a shared distinctive name word; pairs inside one report group are not listed) over all in-region rows: lane rows, phase 1–3 rows and phase-4 rows. Pairs already decided in `data/iaa_dedup_decisions.csv` keep their decisions. Every new pair gets a hand decision in `data/phase4_dedup_decisions.csv`. The keep rule for two inventory rows is unchanged.
- Brackets: no dedup, and every pair within 300 m merged.

## 8. Outputs and comparison

- `scripts/phase4_view.py` imports `score.py` (unchanged) and the helpers of `iaa_view.py`. It never writes `columbaria.csv`, `scores.csv`, `summary.json` or any `iaa_*` file.
- Outputs: `phase4_rows.csv`, `phase4_excluded.csv`, `phase4_scores.csv`, `phase4_summary.json`, `phase4_view_2026-10-12.csv`. Per headline combination and clause: frozen k / f / m of N; the IAA view union of 11 October; the phase 1–4 union; the change against each; the brackets; and the ids of phase-4 rows that match.
- New at three levels: phase-4 rows of the class (counted, in region, admitted, not duplicates), their report groups and their merged sites, each marked phase-4 only or shared with phase 1–3.
- Tests: this amendment's hash and commit; reproduction; the frozen columns equal `summary.json`; the IAA-view columns equal `iaa_view_2026-10-11.csv`; union = frozen + inventory rows; every decision used; no held, strip or ʿAlmit row scored.

## 9. Decision wording

As PLAN §9 and the IAA amendment §8. A new match is listed by row, with its source unit id and printed page. All rows are exploratory and compatibility only, not a test.
