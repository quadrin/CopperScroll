# Plan amendment: the merged IAA inventory as an exploratory view (11 October 2026)

Written 11 October 2026 (UTC) by the IAA-fold worker, before any row of the merged IAA inventory was mapped to this lane, tested against this lane's regions or coded with this lane's word lists. `PLAN.md` (commit cd394d7) and Amendments 1 and 2 are not edited.

**Status: exploratory.** The frozen plan named the phase-1 HA-ESI tables (`features.csv`, `features_unlocated.csv`) as source HAESI: 21 units, 6 located (all possible duplicates of ASI records) and 15 unlocated (not counted). Replacing them with the merged IAA inventory (phases 1, 2 and 3, deduplicated) is a source extension made after the frozen results were seen. It never changes the frozen headline (`scores_summary.csv`, view `all_lineages`; for example Region A strict N = 197, 48-Y 1 match). The results are a separate view beside it. No identification claim follows and no registered outcome changes. Every IAA row is already in the repository (exposed).

## 1. What had been seen when this was written

- This lane's PLAN.md, both amendments, README.md (all results), `scripts/build_tombs.py` (all), `scripts/amendment1.py` (all), the function list of `scripts/tombs_common.py`, and the head of `data/asi_selected_maps.json`.
- The merged inventory's README (class × zone counts: 667 tomb rows, 601 in the Jerusalem hills zone; 466 report groups; 333 sites), AMENDMENTS.md, the head of DEDUPE_PLAN.md and the column names of its tables.
- Three tomb rows' text, by accident of other prints: the first two rows of `features_all.csv` (phase 1: ESI 9 p. 55, Mt. Scopus (B), "a burial cave of the Second Temple period was damaged"; ESI 9 pp. 56–57, Supreme Court Site, "remains of a rock-cut burial cave of the Second Temple period"), and one line of the phase-3 part A summary seen in a search for the Tier 1 records: HA 28, Jerusalem, Shmuel ha-Navi St., "kokhim cave with 19 ossuaries; second tomb system with kokhim and arcosolia", end of the Second Temple period. HA 28–29 is a Tier 1 record, extracted by phase 3 part A (commit aa17f58); no arrival item exists for it.
- Region-wide subtypes of other classes (caves, columbaria, pools, dams, ritual baths), without positions. No other tomb row.
- The caves and columbaria amendments (7e88f3d, b96833a). All four amendments are written before any lane's rows are mapped.

## 2. Source

- `research/regional/haesi_features/merged_2026-10-11/features_all.csv` (SHA-256 `2170f7fb15b097621e07648c128719f25e50e3550d5ec8756c08fca6267e455b`), `report_groups.csv` (`06085467…`), `sites.csv` (`7e89ddce…`), commit cf60d97.
- Only what the IAA coding states is used: class, `feature_subtype`, `quote`, `n_features`, `period_as_given`, `dated_in_window`, `site_name`, positions, `precision_m`, `report_group`, `version_role`, `site_id`. No report is re-read.

## 3. Classes, eligibility and text

- **Primary view: tomb_burial_cave rows** (counted rows only).
- **Text coded** for a unit, as the frozen HAESI rule (`build_tombs.haesi_units`) plus the subtype: `site_name`, the class name with spaces, `feature_subtype`, `quote`, `period_as_given`, joined with ". ". The subtype is the report's own word for the feature (phase 2 §5); the frozen phase-1 table had no subtype column. Eligibility is the frozen test: a TOMB term in that text (every tomb_burial_cave row passes through its class name, as in the frozen build).
- **Sensitivity "other classes":** rows of any other class whose text passes the same TOMB-term test (the frozen build applied it to every HAESI row whatever its type). Reported separately; never in the primary view.

## 4. Units, positions, dating, coding

- **Versions of one report.** Rows of the preferred or single version of a report group are units. Rows of an alternate version are units only for a class the preferred version has none of. When a group has one tomb row in each version, the unit's dating is the merged level-2 value (yes if any version is yes, else no if any is no); otherwise the row's own.
- **Phase-1 rows are not counted twice.** The 21 frozen HAESI units are taken out of the view, and the merged rows (which include those phase-1 rows, under the version rule above) take their place. Every other frozen unit (ASI, WBADB, Kenyon, HK) is used exactly as committed in `tombs.csv`.
- **Position.** The row's `lat`/`lon` (WGS 84). Uncertainty: max(0.1 km, `precision_m` / 1000), as frozen for HAESI. A row without coordinates is not counted (frozen: "unlocated HA-ESI report; not counted"); unlocated rows are tallied by zone and reader place as a coverage note.
- **Regions** by `tombs_common.region_flags` with the frozen JSON block. A unit enters if it lies in A, B1 or the 5 km B2 corridor. `in_asi_sheet` from the committed `data/asi_selected_maps.json`.
- **Coding:** the frozen `Coder` of `build_tombs.py`, imported unchanged, on the text of §3. **Dating:** the frozen HAESI rule: strict = the row's `dated_in_window` (yes or no, else unknown); lenient = yes if strict is yes or the Coder's lenient rule says yes. `multi_tomb_record` by the frozen regular expression of `build_units`.
- **Manual check (PLAN §5).** Every `yes` on F1, F2, F2x, F3, F5, F6, F7w or a name is read (the coding fields only) and confirmed or set back to unknown with a reason, in `data/manual_check_iaa.csv`. The circularity rule applies unchanged.
- **Exposure:** "repo-coded by the merged IAA inventory (phases 1–3); first mapped by this lane on 11 Oct". `tier1_related = yes` for rows from HA 28 or HA 29 or from a report on Kh. ʿAlmit.

## 5. Duplicates (the lane's own rule)

- PLAN §3, unchanged: an IAA unit within 0.15 km of a primary unit (ASI; WBADB outside the online ASI sheets and not an Excavations row marked Surveyed), or with the same normalised name within 0.5 km, is `possible_duplicate_of` that unit and is left out of the union count. Primary units and their points come from the committed `tombs.csv` (a WBADB row is primary there exactly when `in_asi_sheet = no` and `possible_duplicate_of` is empty).
- The frozen rule does not deduplicate non-primary units among themselves. So two IAA reports at one place both count, as two HA-ESI rows did in the frozen build. The view also states how many distinct merged sites (`site_id`) the new non-duplicate units occupy.

## 6. Scoring and outputs

- `scripts/iaa_view.py` builds the IAA units, codes them, applies the duplicate rule and scores every scored branch with the frozen `clause_value` and `overall` (imported unchanged), over the committed non-HAESI units of `tombs.csv` and the IAA units. It needs no ASI cache and no WBADB file, and never writes `tombs.csv`, `scores.csv`, `scores_summary.csv` or `features_summary.csv`. Because the committed `tombs.csv` stores coded values rather than text, the frozen units are scored from their committed codes; a check confirms that this reproduces the committed `scores_summary.csv` for the frozen units.
- Views: `all_lineages` (union without duplicates; frozen HAESI units removed, IAA units added) and `lineage_IAA` (the IAA units alone, duplicates included), for every branch × region × date set, with the sensitivity tolerances.
- **Amendment 1 rules** (F7wa, F2xa, exploratory) are applied to the IAA units with the functions of `scripts/amendment1.py`, and every new F7wa yes or no and F2xa yes is checked by hand in `data/manual_check_iaa_amendment1.csv`. The Amendment 1 counts with the IAA units are reported beside `amendment1_scores_summary.csv`. For the frozen units the committed `amendment1_codes.csv` is used.
- Outputs: `iaa_units.csv`, `iaa_scores.csv`, `iaa_view_2026-10-11.csv` (frozen k / f / m of N, IAA alone, union, change), `iaa_amendment1_view.csv`, `iaa_summary.json`. README: a dated section "IAA inventory view, 11 October 2026 (exploratory)". One test checks that the view reproduces and that its frozen columns equal `scores_summary.csv`.

## 7. Decision wording

As PLAN §9: "k match, f fail, m unknown, of N", per branch, region and date set, frozen and with the IAA units. A new match is listed with its exposure and the clause evidence; it is compatibility in a denominator, not an identification.
