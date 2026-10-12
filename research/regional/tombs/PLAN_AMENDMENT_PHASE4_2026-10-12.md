# Plan amendment: the phase 1–4 merged inventory as an exploratory view (12 October 2026)

Written 12 October 2026 (UTC) by the phase-4 fold worker, before any phase-4 row of class `tomb_burial_cave` was read, mapped to this lane, tested against its regions or coded with its word lists. `PLAN.md` (cd394d7), Amendments 1 and 2 and `PLAN_AMENDMENT_IAA_2026-10-11.md` (c14468e) are not edited.

**Status: exploratory.** This amendment applies the method of `PLAN_AMENDMENT_IAA_2026-10-11.md` (§2–§7) unchanged. The one change is the input: the merged inventory over phases 1–4 (`merged_2026-10-12`) replaces the merged inventory over phases 1–3 (`merged_2026-10-11`). This is a further source extension made after the frozen results and the 11 October IAA view were seen. It never changes the frozen headline (`scores_summary.csv`), the Amendment 1 and 2 outputs or the 11 October IAA view files. Its results are a separate view beside them. No identification claim follows and no registered outcome changes.

## 1. What had been seen when this was written

- Everything listed in the IAA amendment §1, and every output of the 11 October IAA view: `iaa_units.csv` (through its README summary), `iaa_view_2026-10-11.csv` (through the README table), `iaa_summary.json` (all), `scripts/iaa_view.py` (all), `tests/test_iaa_view.py` (all), this lane's README (section headings; the head, the IAA section, Blocked, Files, Proposed changes).
- The fold rules for this round and the phase-4 worker rules (protected material, storage, attribution).
- `merged_2026-10-12/README.md` in full. It gives class × zone counts, including the phase-4 tomb counts:
  - 187 counted phase-4 tomb rows (36 yes / 101 no / 50 unknown), 164 in the Jerusalem hills;
  - 96 phase-4-only tomb report units and 78 phase-4-only tomb site units.
  It also names, among shared units whose dating phase 4 changed from no to yes, "the Mount Scopus chalk quarry cisterns and burial caves (ATQ113-i09)". That one phase-4 tomb report is therefore exposed by name and dating, without its position or features.
- `phase4_2026-10-11/README.md` in full. It says QDAP's in-window rows include "kokhim tombs" in Jerusalem and its hills. It lists the held items by citation, including Kenyon's "Burial Customs at Jericho" (ADAJ 16) and an ADAJ 2 p. 88 passage on the 1952 Jericho tombs, both held.
- Column headers of `features_all.csv`, `report_groups.csv` and `sites.csv`, and the `unit_id` column of every phase-4 `held.csv` (15 distinct held units).
- Value counts over all rows (no row text):
  - `phase`, `counted` and `protected_strip`; the last is `no` in all 4,035 rows;
  - phase-4 `feature_type` (208 tomb rows, counted or not);
  - phase-4 report-id prefixes and `count_zone`;
  - `precision_m`;
  - `coordinate_source`. Its values name reader places for all classes together, for example `jer_tombs_kings`, `jer_gethsemane`, `tell_es_sultan`, `kh_qumran`, Ketef Hinnom and Mordot Arnona;
  - a cross-tab of coordinate source by the presence of `lat` and `precision_m`. Every phase-4 row placed by name only, and every SWP square row, has no coordinates; every located phase-4 row has a map reference (precision 1, 10, 100 or 1000 m);
  - `report_groups.phases`, and whether `sites.phase13_sites` and `sites.phase4_rows` are filled.
- A check that the 3,223 phase 1–3 rows have the same `row_uid`, report, class, quote and latitude in both merged inventories (they do).
- No phase-4 tomb row's site name, quote, subtype, period text, position or dating, apart from the ATQ113-i09 line above.

## 2. Source

- `research/regional/haesi_features/merged_2026-10-12/features_all.csv` (SHA-256 `940e6c04b1ecd18c79a7c88a784a463d69056f70c6e31ad18e5a18c46866d65d`), `report_groups.csv` (`38b67f3c7095993287ac9da80eb229a9752d56ff7c27cb9bb3b1024f47da702f`), `sites.csv` (`5d7458016d7955cced5540d4307570879fbc5b2071d5f644e85d3cec0fcc16db`), commit b4a41cc (merged in 7cac03b).
- Only the coded fields named in the IAA amendment §2 are used, plus `phase`, `coordinate_source`, `report_id`, `pages` and `protected_strip`. No report is re-read.

## 3. Method (unchanged)

- **Classes, text, eligibility:** IAA amendment §3. Primary view: counted `tomb_burial_cave` rows. Sensitivity "other classes": counted rows of other classes that pass the TOMB-term test.
- **Version rule, positions, dating, coding, duplicates, scoring:** IAA amendment §4–§6, applied to the whole merged_2026-10-12 inventory (phases 1–4). Phase 1–3 units are rebuilt under the new report groups, so a phase 1–3 unit can drop out when a phase-4 report joins its group and becomes the preferred version. Such changes are reported, not hidden.
- **Same functions.** The frozen `Coder`, `clause_value`, `overall`, the duplicate rule against the committed primary units of `tombs.csv`, and the Amendment 1 functions are imported unchanged. The 21 frozen HAESI units are taken out, as in the IAA view.
- **Manual check (PLAN §5).** A hand decision already recorded for the same `record_id` (`IAA <row_uid>`) in `data/manual_check_iaa.csv` or `data/manual_check_iaa_amendment1.csv` is reused, because phase 1–3 rows keep their `row_uid` and coded text. Every other `yes` on F1, F2, F2x, F3, F5, F6, F7w or a name, and every new F7wa yes or no and F2xa yes, is read (coding fields only) and recorded in `data/manual_check_phase4.csv` or `data/manual_check_phase4_amendment1.csv`.
- **Exposure:** a phase-4 unit gets "repo-coded by the phase-4 readers and merged_2026-10-12; first mapped by this lane on 12 Oct 2026". Phase 1–3 units keep the IAA view's exposure text. ATQ113-i09 is marked exposed by the merge README.

## 4. Phase-4 sources without coordinates (the IAA name-only rule, reused)

- A row without `lat`/`lon` is not counted, whatever its reader place. Per the cross-tab in §1, this covers every QDAP row, most SWP, Guérin and ADAJ rows, the name-only ʿAtiqot rows and the 94 uncounted SWP zone-split rows. Unlocated counted rows are tallied by zone and by reader place (`coordinate_source`) as a coverage note.
- **Unlocated name listing (coverage note only, never counted).** Unlocated counted phase-4 tomb rows are coded by the same `Coder`. Every `yes` on F1, F5 or a name (Zadok, Absalom, queen, Obed) is hand-checked as in §3 and listed with its row id, report id and printed pages. No such row enters any N or k.
- A row is never placed by hand, and a reader place is never turned into a point.

## 5. Protected material

These rules apply before any coding. An excluded row is listed by `row_uid` and reason only. Its text is not printed or coded.

- **Held cave areas.** Excluded:
  - any row whose `report_id` equals, or begins with, a `unit_id` in a phase-4 `held.csv`;
  - any phase-4 row whose site name, reader place or quote names a held-area place (regular expression, case-insensitive: `qumran|feshkha|fashkha|qarantal|quruntul|kuruntul|quarantania|\bdu[kq]\b|nuwei|nueima|qelt|kelt`) and whose site name, subtype or quote contains `cave`.
  The readers gave held units no feature row, so both counts are expected to be 0.
- **Tell es-Sultan north strip.** Excluded:
  - any row with `protected_strip = yes`;
  - any phase-4 row whose point lies within 0.5 km of `tell_es_sultan` (31.8717, 35.4446);
  - any phase-4 row whose site name or reader place matches `t[ae]ll?[\s_-]*(es|el|al|e)?[\s_-]*sultan` (case-insensitive; this leaves out Jerusalem's Sultan's Pool).
  The frozen Kenyon and IAA Reports 7 units of `tombs.csv` are frozen inputs and stay as committed.
- **Kh. ʿAlmit.** Excluded from every view, score and listing: any phase-4 row whose site name or report id matches `almit|עלמית`. Not compared with any model. (The IAA view found no phase 1–3 Kh. ʿAlmit row in the regions.)
- **ʿAtiqot 41.** Excluded: any row whose report id begins `ATQ41-`.

## 6. Outputs

- Script: `scripts/phase4_view.py`. It reuses the functions of `scripts/iaa_view.py`, which stays unchanged.
- Outputs:
  - `phase4_units.csv`;
  - `phase4_scores.csv`;
  - `phase4_view_2026-10-12.csv`, with frozen k / f / m of N, the 11 October IAA union, the phase 1–4 union, the change from each, the phase 1–4 IAA units alone and the other-classes sensitivity;
  - `phase4_amendment1_view.csv`;
  - `phase4_summary.json`.
- **What counts as new:**
  - row: a unit from a phase-4 row;
  - report: a unit whose report group has no phase 1–3 member;
  - site: a unit whose `site_id` has no phase 1–3 site.
  A new match is a union match absent from the 11 October IAA union.
- Tests in `tests/test_phase4_view.py`:
  - this amendment's hash and its commit, which holds this file alone;
  - the script reproduces its outputs;
  - the frozen tables, the Amendment 1 and 2 outputs and the 11 October IAA view files are byte-unchanged;
  - the view's frozen columns equal `scores_summary.csv`;
  - its 11 October columns equal `iaa_view_2026-10-11.csv`;
  - no excluded (held, strip, Kh. ʿAlmit, ʿAtiqot 41) row is a unit.
- README: a dated section "Phase-4 inventory view, 12 October 2026 (exploratory)".

## 7. Decision wording

As PLAN §9 and the IAA amendment §7: "k match, f fail, m unknown, of N", per branch, region and date set, frozen, with the 11 October IAA units and with the phase 1–4 units. A new match is listed with its source unit id, printed page, exposure and clause evidence. It shows compatibility within a denominator, not an identification.
