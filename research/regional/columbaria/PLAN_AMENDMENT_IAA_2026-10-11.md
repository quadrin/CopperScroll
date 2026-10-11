# Plan amendment: the merged IAA inventory as an exploratory view (11 October 2026)

Written 11 October 2026 (UTC) by the IAA-fold worker, before any row of the merged IAA inventory was mapped to this lane, tested against this lane's region or read for this lane's clauses. `PLAN.md` (commit afdd69f) and `PLAN_AMENDMENT_1.md` are not edited.

**Status: exploratory.** The frozen plan named the phase-1 HA-ESI table as a source (S4); it held no columbarium row, so no IAA row is in the frozen counts. Adding the merged IAA inventory now is a source extension made after the frozen results were seen. It never changes the frozen headline (scope `frozen`: entry 38 N1/N2 0 match of 179; entry 44 Puech text level 3 match, 59 fail, 117 unknown, of 179). The results are a separate view beside it. No identification claim follows and no registered outcome changes. Every IAA row is already in the repository (exposed).

## 1. What had been seen when this was written

- This lane's PLAN.md, PLAN_AMENDMENT_1.md, README.md (all results), `scripts/assemble.py`, `scripts/score.py`, the head of `scripts/colcommon.py`, `scripts/terms.json`, the first lines of `tests/test_columbaria.py`, and one row of `data/coding.json` per source.
- The merged inventory's README (with its class × zone counts: 46 columbarium rows, 40 report groups, 35 sites, 42 of the rows in the Jerusalem hills zone), AMENDMENTS.md, the head of DEDUPE_PLAN.md and the column names of its tables.
- A region-wide print, without positions or site names, of some `feature_subtype` values of the class columbarium_dovecote: "columbarium cave" (twice); "“columbarium” structure (excavator's quotation marks)"; "round columbarium-like structure with eight niches (Area D2)"; "rock-cut columbarium cave with rows of niches"; "columbarium cave with two halls of niches, north of Givʿat Hamivtar"; "round columbarium cave entered through a rock-cut opening in the ceiling".
- The caves lane amendment (committed 7e88f3d) and the other lanes' plans and READMEs. All four amendments are written before any lane's rows are mapped.

## 2. Source

- `research/regional/haesi_features/merged_2026-10-11/features_all.csv` (SHA-256 `2170f7fb15b097621e07648c128719f25e50e3550d5ec8756c08fca6267e455b`), `report_groups.csv` (`06085467…`), `sites.csv` (`7e89ddce…`), commit cf60d97; `places_v2.csv` (`315474bd…`) for named-place points.
- Only what the IAA coding states is used: class, `feature_subtype`, `quote`, `n_features`, `period_as_given`, `site_name`, positions, `coordinate_source`, `report_group`, `version_role`, `site_id`. No report is re-read.

## 3. Classes and eligibility

- **Primary view: columbarium_dovecote rows** (counted rows only) whose `feature_subtype`, `quote` or `site_name` matches a frozen columbarium pattern (PLAN §5 and Appendix A, `scripts/terms.json`). Rows without such a word ("niches" only) are not columbaria here (PLAN §5) and go to `iaa_excluded.csv`.
- PLAN §5 exclusions apply: a columbarium word that refers to a funerary urn-niche tomb, or a place name only. Amendment 1 B9 applies: "columbarium?", "possibly a columbarium", "columbarium-like" are rows with `uncertain_identification = yes`; a comparison ("niches resembling those of columbaria") is excluded. A columbarium word that the coding puts in quotation marks (the excavator's own marks) is read as uncertain too. That last rule is chosen knowing that one such subtype exists (§1).
- **Sensitivity "word screen":** rows of any other class whose `feature_subtype` or `quote` matches a frozen columbarium pattern (phase 1 coded columbaria under rock-cut installations). Such a row is not added if its report group already gives a columbarium_dovecote row. Reported separately; never in the primary view.

## 4. Region and positions

- The frozen polygon (PLAN §3), ray-casting on WGS 84 longitude/latitude, as `colcommon.in_region`.
- A row's point is its `lat`/`lon` (WGS 84, as converted by the phase readers). Precision: the row's `precision_m`, but at least 100 m (the frozen ASI and WBADB value).
- A row without coordinates is placed at its reader's place id (`name only (<id>)` or `feature site name (<id>)`) from `places_v2.csv`, with precision = that place's sigma, if the sigma is 2 km or less (PLAN §3: a stated gazetteer, placed within 2 km). Otherwise it is listed as `unplaced` and not counted.

## 5. Units and coding

- **Versions of one report.** Rows of the preferred or single version of a report group are used; rows of an alternate version only if the preferred version has no columbarium row.
- **One row per columbarium the coding distinguishes** (PLAN §5, Amendment 1 B2): `n_columbaria` = `n_features` when it is a number, else null for a plural.
- **Clause fields**, coded by hand from the IAA coding fields only, after a script flags the frozen clause patterns (Appendix A: fort, tower, levels, access, south, Naṭof) in `feature_subtype`, `quote` and `site_name`, and the fort and tower patterns also in the other rows of the same report group:
  - `fort_at_site`, `tower_at_site` (survey level): a fort or tower word in the coding of the same report group (the same record names both; Amendment 1 B4). `setting`: `fortress_inside` only when the coding places the columbarium inside the fort; `tower_itself` for a columbarium tower; `isolated` per Amendment 1 B3; otherwise `settlement` if the coding names a settlement or building context, else `unknown`.
  - `lev2`, `lev3`, `access`, `part_of_site`, `natof_text`: M or F only on a statement in the coding (PLAN §2, Amendment 1 B5, B8); otherwise U. "An opening in the ceiling" is a way down from above (B5).
  - **Date** (PLAN §6) from `period_as_given`, by the frozen D / L / P / U definitions and Amendment 1 B1. The HA-ESI flag `dated_in_window` is not used, because it counts an unqualified "Second Temple period" as in the window, which PLAN §6 codes P.
- `exposed_before_freeze = no` (the lane's freeze); `read_via` = "merged IAA inventory row <row_uid>". `tier1_related = yes` for rows from HA 28 or HA 29 or from a report on Kh. ʿAlmit. No quote is copied; the row id points to the inventory's quote.

## 6. Joins to the lane's rows (the lane's own duplicate rule)

- PLAN §5: the same columbarium in several sources is one unit ("same site name, or points within 300 m and the same site"); Amendment 1 B2: the second source is kept with `dup_of` and not counted.
- A script lists every pair of an IAA row with a counted lane row (ASI, WBADB, literature), and of two IAA rows of different report groups, whose points lie within 300 m or whose site names share a distinctive name word. Each pair gets a hand decision, "same site" or "different site", with its reason, in `data/iaa_dedup_decisions.csv`. A pair decided "same site" makes the IAA row `dup_of` the lane row (the frozen lane row is kept and not recoded; if the IAA coding would change one of its clauses, that is reported, not applied). For two IAA rows, the row with more clause codes other than U is kept (then the earlier publication).
- Bracket, reported beside the primary: **no dedup** (every in-region IAA row counted) and **300 m only** (every pair within 300 m treated as one site).

## 7. Scoring and outputs

- `scripts/iaa_view.py` builds the IAA rows in the `columbaria.csv` schema and scores them with `score.py`'s `score_row`, `combos` and `tally`, imported unchanged, together with the committed `columbaria.csv` rows. It runs from committed tables and never writes `columbaria.csv`, `scores.csv` or `summary.json`.
- Outputs: `iaa_rows.csv`, `iaa_excluded.csv`, `iaa_scores.csv`, `iaa_summary.json`, `data/iaa_coding.json`, `data/iaa_dedup_decisions.csv`, and `iaa_view_2026-10-11.csv`: per headline combination and per clause, frozen k / f / m of N, IAA rows alone, union, change (scope `frozen`; scope `all` beside it).
- README: a dated section "IAA inventory view, 11 October 2026 (exploratory)". One test checks that the view reproduces and that its frozen columns equal `summary.json`.

## 8. Decision wording

As PLAN §9, per branch and level: "k match, f fail, m unknown, of N", frozen and with the IAA rows. A new match is listed by row with the clause evidence it rests on; it is exposed, so it is compatibility only, not a test.
