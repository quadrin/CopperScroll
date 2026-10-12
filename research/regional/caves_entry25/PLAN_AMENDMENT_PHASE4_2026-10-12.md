# Plan amendment: the phase 1–4 merged inventory as an exploratory view (12 October 2026)

Written 12 October 2026 (UTC) by the phase-4 fold worker for this lane, before any phase-4 row of the classes cave_with_finds or tomb_burial_cave was printed, mapped to this lane's box or read for this lane's clauses. `PLAN.md` (commit 2ff6e5a), `AMENDMENT_1.md` and `PLAN_AMENDMENT_IAA_2026-10-11.md` (commit 7e88f3d) are not edited.

**Status: exploratory.** This applies the frozen plan and the IAA-view method of `PLAN_AMENDMENT_IAA_2026-10-11.md` (§§3–9) unchanged, with the merged inventory `merged_2026-10-12` (phases 1–4) as input in place of `merged_2026-10-11`. It changes no frozen result ("1 match every clause, 198 fail, 436 unknown, of 635", B-PILLAR, cave level, primary), no IAA-view output (`iaa_*`, `iaa_view_2026-10-11.csv`), no registered outcome and no shared status file. Every phase-4 row is already in the repository (exposed), so a new all-match row is compatibility only and cannot serve as an unseen observation.

## 1. What had been seen when this was written

- This lane's PLAN.md, AMENDMENT_1.md, README.md (all results, including the IAA-view section), PLAN_AMENDMENT_IAA_2026-10-11.md, `scripts/iaa_view.py`, `tests/test_iaa_view.py`, `coded/iaa_coding.csv` (all 17 lines) and the head of `iaa_summary.json` (counts of unplaced and outside-box rows by class and zone, from merged_2026-10-11).
- `merged_2026-10-12/README.md` in full, including its published class × zone tables. Those tables give, for phase 4, cave_with_finds rows by zone (Z1 0/0/2, Z2 0/0/1, Z3 1/5/6, Z4 10/10/27) and tomb_burial_cave rows by zone (Z1 0/3/8, Z2 0/4/0, Z3 2/2/4, Z4 34/92/38), as yes / no / unknown in-window counts. No row behind them was seen.
- `phase4_2026-10-11/README.md` and `PLAN.md` (including the held items it names by title: IAA Reports 5, the QDAP Tell es-Sultan items, SWP Kuruntul, ʿAin ed Duk and Deir el Kelt paragraphs, the ADAJ Qumran cave passages, Kenyon ADAJ 16); phase-2 PLAN §2 (zones), the heading of §4 and §7 (protected material); the lane rules for this fold (FOLD4_RULES, PHASE4_RULES).
- Aggregate value counts over **all classes together** of the 812 phase-4 rows: `phase`, `series`, `counted`, `version_role`, `grid`, `crs_used` (shape only), presence of `lat`, `n_features` (shape only), `zone_source`, and the kinds and character shapes of the `coordinate_source` tokens (map ref 253 + feature map ref 44 with a point; name only 368 + 2 + 2 without a reader place; name only with a `places_v2` id 44; SWP square 99, no place id). No value of `site_name`, `feature_subtype`, `quote` or a position of any phase-4 row was printed.
- A check on phase 1–3 rows only: every `row_uid` of merged_2026-10-11 is in merged_2026-10-12 with identical phase-2 columns; `report_group` differs for 216 rows, `version_role` for 184 and `site_id` for 2,849 (the phase-4 joins). Which of those rows are in this lane's classes was not looked at.
- `places_v2.csv` rows for the held-area anchors listed in §5 (names and points only).

## 2. Source

- `research/regional/haesi_features/merged_2026-10-12/features_all.csv` (SHA-256 `940e6c04b1ecd18c79a7c88a784a463d69056f70c6e31ad18e5a18c46866d65d`), `report_groups.csv` (`38b67f3c7095993287ac9da80eb229a9752d56ff7c27cb9bb3b1024f47da702f`), `sites.csv` (`5d7458016d7955cced5540d4307570879fbc5b2071d5f644e85d3cec0fcc16db`), commit b4a41cc (merged in 7cac03b). Named-place points: `places_v2.csv` (`315474bd3be8cce3e1776e119417e2444edd99e3f028c7413185302fc7663683`), as before.
- The phase-4 `held.csv` files under `research/regional/haesi_features/phase4_2026-10-11/` (every part and reader folder), used only for their unit ids.
- As before, only the coding fields are used; no report is re-read.

## 3. Method: the IAA view, rerun unchanged

- Classes, eligibility, cave word, "cave or rock shelter", region box, positions, report versions, row kind, period, excavation status, joins, duplicates, N_min, clause coding, scoring and decision wording: `PLAN_AMENDMENT_IAA_2026-10-11.md` §§3–9, unchanged. The scoring uses the functions of `scripts/score.py`, imported unchanged, with the frozen aspect rule (`research/preregistration/entry25_iv17_rules/`) unchanged.
- The rerun covers every counted row of merged_2026-10-12 (phases 1–4), not only phase-4 rows, because the version rule is applied per report group and phase-4 reports join some earlier groups. The view is: the committed `caves.csv` plus every row the IAA method admits from merged_2026-10-12.
- **Changes of version.** If a phase 1–3 row admitted on 11 October is no longer the preferred or single version (a phase-4 report has become preferred), it is replaced by the rows the version rule now selects. Every such replacement, and every earlier row no longer admitted, is listed in the results.

## 4. Coding

- `coded/iaa_coding.csv` is reused unchanged for every phase 1–3 row that is still admitted. It is not edited.
- New rows (phase-4 rows, and any phase 1–3 row newly selected by the version rule) are coded in a new file, `coded/phase4_coding.csv`, with the same columns and the same rules (IAA amendment §7: keyword flag, then the coding fields only, by hand; unflagged rows take the defaults).
- **Same campaign.** If a row of a report group and class was coded `same_source` or `merge` on 11 October, a newly selected row of the same report group and class takes the same action and target, unless its coding names a different cave; then it is coded on its own and the reason is written.
- Exposure: `exposed-repo` for every row, with the UTC time this worker first mapped it.
- Choices made while coding, which this file does not settle, are written in the `notes` of the coding line and listed in the README as exploratory.

## 5. Protected material (applied before a row is read)

Applied by the script to the selected rows of this lane's classes, using only ids, positions and a term match. An excluded row's coding fields are not read; it is listed by `row_uid`, `report_id` and reason in `phase4_excluded.csv`.

1. **Held units.** A phase-4 row whose `report_id` is a unit id in any phase-4 `held.csv` is excluded (status `held`). The readers gave held units no feature row, so none is expected.
2. **Held cave areas, by term.** A phase-4 row whose `site_name`, `feature_subtype`, `quote` or `coordinate_source` matches a held-area term is excluded (status `held-area`). Terms (case-insensitive): Qumran, Feshkha / Fashkha / Feshka, Qarantal / Quruntul / Kuruntul / Qarantul / Quarantania / Temptation, Nuweiʿimeh / Nueiameh / Nuweimeh / Nueima, Duk / Doq / Dok (whole word), Qelt / Qilt / Kelt, Perat / Prat, Choziba / Khoziba, St George; Hebrew קומראן, קומרן, פשח'ה, צוקים, קרנטל, קלט, פרת.
3. **Held cave areas, by position (safety net, INFERENCE).** A phase-4 row whose point (own or reader place) lies in one of these WGS 84 boxes, drawn conservatively around the `places_v2` anchors, is excluded (status `held-area`): Qumran cliffs and marl terrace, Wadi Qumran to ʿEin Feshkha and the cliffs north of it: lat 31.700–31.790, lon 35.420–35.475 (anchors kh_qumran, wadi_qumran, ein_feshkha); Jericho escarpment, Jebel Qarantal to Wadi Nuweiʿimeh and ʿAin Duk: lat 31.860–31.915, lon 35.395–35.438 (doq, ain_duk, nuweimeh, iv17_abu_saraj); Wadi Qelt gorge west of the Jericho palaces: lat 31.825–31.865, lon 35.315–35.432 (choziba). A row placed only by one of the reader places kh_qumran, wadi_qumran, ein_feshkha, doq, ain_duk, nuweimeh, choziba or iv17_abu_saraj is excluded likewise.
4. **Tell es-Sultan north strip.** A phase-4 row with `protected_strip = yes`, a term Sultan / סולטאן, or a point within 500 m of `places_v2` tell_es_sultan (31.8717, 35.4446) is excluded (status `protected-strip`).
5. **Kh. ʿAlmit.** A row whose `site_name` or `report_id` names ʿAlmit (Almit, עלמית) is excluded from the view (status `tier1-almit`) and compared with nothing. (Kh. ʿAlmit lies west of the box in any case.)
6. **ʿAtiqot 41.** A row from ʿAtiqot 41 would be excluded (status `atiqot41`); phase 4 did not read it.
- Phase 1–3 rows are not re-screened under 2–4 (their readers applied the same held rule). Any admitted phase 1–3 row that falls in a §5.3 box is reported, not excluded.

## 6. Sources without coordinates

- The IAA amendment's name-only rule (§4) is reused unchanged: a row without its own point is in the region "by description" only if its `coordinate_source` names a `places_v2` place id (pattern `(<id>)`, lower-case letters, digits and underscores) whose point lies in the box; precision is that place's sigma.
- Every other row without a point is not admitted. This covers phase-4 rows placed by an SWP square, by a gazetteer term (`name only (gazetteer: …)`), or by a name with no place id (QDAP, ADAJ, SWP, Guérin). Such rows of zones Z2 and Z3 (the only zones that meet the box; Z1 lies north of it and Z4 west of it) are listed in `phase4_unplaced.csv` by `row_uid`, report id, series, volume, pages, `site_name`, zone and `coordinate_source`, after the §5 screen, and are not coded or scored. Rows of Z1 and Z4 are counted only.
- No SWP square, gazetteer term or old spelling is converted to a point here; that would be a new placement rule.

## 7. Outputs

- `scripts/phase4_view.py` (adapted from `scripts/iaa_view.py`; it imports `score.py` unchanged and never writes the frozen or IAA-view outputs).
- `phase4_units.csv` (admitted rows in the `caves.csv` schema, with `phase`), `phase4_excluded.csv`, `phase4_unplaced.csv`, `phase4_scores.csv`, `phase4_summary.json`, and `phase4_view_2026-10-12.csv`: per branch × level × rule set × count (rows, N_min, clusters), the frozen k / f / m of N, the 11 October IAA union, the 12 October union, the changes from each, and the new all-match rows.
- `tests/test_phase4_view.py`: this file's hash and that its commit holds only it and precedes the coding; byte-identical rerun without touching the frozen or IAA-view outputs; the frozen columns equal `summary.json` and the IAA columns equal `iaa_view_2026-10-11.csv`; union arithmetic; no excluded (held, strip, ʿAlmit) row is scored.
- README: a dated section "Phase 1–4 inventory view, 12 October 2026 (exploratory)": what is new at the row, report-group and site level; the rows matching each clause on each branch; every new match with its source unit id and printed page; the misses; what stays unknown; proposed shared-file changes at the end.

## 8. Decision wording

As PLAN §6 and the IAA amendment §9, for each branch × level × rule set: "k match every clause, f fail at least one, m unknown, of N", frozen, with the 11 October IAA rows, and with the 12 October rows. Only entry 25 is scored in this lane (B-PILLAR and B-TERRACE; B-GATE is not a cave).
