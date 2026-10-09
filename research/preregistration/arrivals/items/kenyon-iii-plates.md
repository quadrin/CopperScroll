# Kenyon and Holland 1981, Excavations at Jericho III, plate volume: Trench II eastern section (local 37.50–38.00 m N / 8.17 m H) and Pl. 111b

Item `kenyon-iii-plates`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** Library (not obtained)
- **Requested:** Not requested (decisions plans.json (decisions-kenyon-section); added by this register because the decisions module ranks it second)
- **Asked for:** Not on the brief's list. Added so the ranking includes the record the decisions module needs for the quarry-pit classes.
- **Status on 9 October 2026:** not_obtained. Drive holds the text volume only.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: Kenyon III text pp. 119–121, 173–174 is inspected (about 18 graves; later undated quarry pits cutting them).

## What it bears on

- Open questions: R07, R09
- Active questions (ACTIVE_TEST): 2
- Entries: 60
- Reserved observation: no

## Handling on arrival

Ordinary library intake.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

Source: `discriminate.py` task `decisions-kenyon-section`, read-only. Coverage factor c = 1.0: The section and plate are the named record.

| Outcome id | Kind | Basis | Outcome | Excluded classes |
|---|---|---|---|---|
| `dec:usable-mouth:usable-early+joint-early` | decisive | recorded | dated usable opening within 50 BCE–70 CE; jointly accessible within 50 BCE–70 CE | none |
| `dec:usable-mouth:usable-early+joint-71-135-only` | decisive | derived | dated usable opening within 50 BCE–70 CE; jointly accessible only 71–135 CE | kohlit: c04 |
| `dec:period-or-access-miss:usable-early+no-joint` | decisive | recorded | dated usable opening within 50 BCE–70 CE; not jointly accessible in either window | kohlit: c04, c05 |
| `dec:truncation-only:usable-early+undetermined` | partial | derived | dated usable opening within 50 BCE–70 CE; joint access undetermined | none |
| `dec:usable-mouth:built-71-135+joint-71-135-only` | decisive | derived | secure opening date 71–135 CE; jointly accessible only 71–135 CE | kohlit: c02, c04 |
| `dec:period-or-access-miss:built-71-135+no-joint` | decisive | derived | secure opening date 71–135 CE; not jointly accessible in either window | kohlit: c02, c04, c05 |
| `dec:period-or-access-miss:built-71-135+undetermined` | partial | derived | secure opening date 71–135 CE; joint access undetermined | kohlit: c02, c04 |
| `dec:period-or-access-miss:outside-both+no-joint` | decisive | recorded | secure opening date after 135 CE; not jointly accessible in either window | kohlit: c02, c03, c04, c05 |
| `dec:period-or-access-miss:outside-both+undetermined` | partial | recorded | secure opening date after 135 CE; joint access undetermined | kohlit: c02, c03, c04, c05 |
| `dec:period-or-access-miss:undated+no-joint` | partial | recorded | no dated usability; not jointly accessible in either window | kohlit: c04, c05 |
| `dec:truncation-only:undated+undetermined` | partial | recorded | no dated usability; joint access undetermined | none |
| `dec:drawing-gate-fails` | not_obtained | recorded | Section, plate or crosswalk unavailable | none |

Class legend:
- `c01` (kohlit): assignment: jericho-d9 / jericho-historical-ns1; reading: RB-B / RB-M / RB-P; window: early / extended
- `c02` (kohlit): assignment: jericho-quarry; reading: RB-B; window: early
- `c03` (kohlit): assignment: jericho-quarry; reading: RB-B; window: extended
- `c04` (kohlit): assignment: jericho-quarry; reading: RB-M / RB-P; window: early
- `c05` (kohlit): assignment: jericho-quarry; reading: RB-M / RB-P; window: extended
- `c06` (kohlit): assignment: samiya-kallai; reading: RB-B / RB-M / RB-P; window: early
- `c07` (kohlit): assignment: samiya-kallai; reading: RB-B / RB-M / RB-P; window: extended
- `c08` (kohlit): assignment: yanun-jericho-anchor; reading: RB-L; window: early / extended
- `c09` (kohlit): assignment: yanun-marjama-anchor; reading: RB-L; window: early
- `c10` (kohlit): assignment: yanun-marjama-anchor; reading: RB-L; window: extended

What each class predicts for this item:
- `c01` (kohlit): no prediction about this item. It survives every registered outcome.
- `c02` (kohlit): compatible decisive outcomes: `dec:usable-mouth:usable-early+joint-early`, `dec:usable-mouth:usable-early+joint-71-135-only`, `dec:period-or-access-miss:usable-early+no-joint`. Excluded by: `dec:usable-mouth:built-71-135+joint-71-135-only`, `dec:period-or-access-miss:built-71-135+no-joint`, `dec:period-or-access-miss:built-71-135+undetermined`, `dec:period-or-access-miss:outside-both+no-joint`, `dec:period-or-access-miss:outside-both+undetermined`. Survives every other outcome, including silence.
- `c03` (kohlit): compatible decisive outcomes: `dec:usable-mouth:usable-early+joint-early`, `dec:usable-mouth:usable-early+joint-71-135-only`, `dec:period-or-access-miss:usable-early+no-joint`, `dec:usable-mouth:built-71-135+joint-71-135-only`, `dec:period-or-access-miss:built-71-135+no-joint`. Excluded by: `dec:period-or-access-miss:outside-both+no-joint`, `dec:period-or-access-miss:outside-both+undetermined`. Survives every other outcome, including silence.
- `c04` (kohlit): compatible decisive outcomes: `dec:usable-mouth:usable-early+joint-early`. Excluded by: `dec:usable-mouth:usable-early+joint-71-135-only`, `dec:period-or-access-miss:usable-early+no-joint`, `dec:usable-mouth:built-71-135+joint-71-135-only`, `dec:period-or-access-miss:built-71-135+no-joint`, `dec:period-or-access-miss:built-71-135+undetermined`, `dec:period-or-access-miss:outside-both+no-joint`, `dec:period-or-access-miss:outside-both+undetermined`, `dec:period-or-access-miss:undated+no-joint`. Survives every other outcome, including silence.
- `c05` (kohlit): compatible decisive outcomes: `dec:usable-mouth:usable-early+joint-early`, `dec:usable-mouth:usable-early+joint-71-135-only`, `dec:usable-mouth:built-71-135+joint-71-135-only`. Excluded by: `dec:period-or-access-miss:usable-early+no-joint`, `dec:period-or-access-miss:built-71-135+no-joint`, `dec:period-or-access-miss:outside-both+no-joint`, `dec:period-or-access-miss:outside-both+undetermined`, `dec:period-or-access-miss:undated+no-joint`. Survives every other outcome, including silence.
- `c06` (kohlit): no prediction about this item. It survives every registered outcome.
- `c07` (kohlit): no prediction about this item. It survives every registered outcome.
- `c08` (kohlit): no prediction about this item. It survives every registered outcome.
- `c09` (kohlit): no prediction about this item. It survives every registered outcome.
- `c10` (kohlit): no prediction about this item. It survives every registered outcome.

### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)

Inconclusive if the record covers the place but meets neither criterion. Silent if it does not cover the place or relation; silence is never a FAIL.

**Tell es-Sultan (old Jericho)**, link `SULTAN-2-quarry-section` (model held by the decision classes; not counted again in the chain metric)

- Branches: jericho-quarry assignment; RB-M, RB-P. Relations: R-E60-JOINT-ACCESS, R-E60-PIT-PERIOD. Reading dependencies: D-E60-BURIED.
- Predicts: A phase-lxxvii pit cut from a surface on which phase-lxxvi grave shafts were still open or marked, with nothing later than 135 CE in the pit's lowest fill.
- No prediction from this link under: RB-B.
- Where: Kenyon Trench II/Site O, eastern section at local 37.50–38.00 m N / 8.17 m H, and the burial in Pl. 111b.
- Confirm if: The section shows no deposit between the grave tops and the pit's cutting surface, and the lowest pit fill holds no securely later material.
- Contradict if (two-sided): A deposit seals the grave tops below the pit's cutting surface, or the lowest pit fill holds securely post-135 CE material. Either rejects the quarry-pit branch only.
- Coverage factor: not used (the decision classes carry this model).
- Outcome ids: `chain:SULTAN-2-quarry-section:confirm`, `chain:SULTAN-2-quarry-section:contradict`, `chain:SULTAN-2-quarry-section:inconclusive`, `chain:SULTAN-2-quarry-section:silent`

No prediction from the other 27 chain models (no link of theirs uses this record): Kh. el-Marjama at ʿEin Samiya; Kh. Qumran; Qarn Sarṭaba (Alexandrium); Janoaḥ route (entry 60 reading שבינח); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; Tulul Abu el-'Alaiq; Kypros; Tell es-Samrat; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; unnamed WBADB unit S3961; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

- `P60-T1` (Tell es-Sultan (Old Jericho, Elisha's spring): north-slope graves and cemetery zone N/NW of the tell; record SHA-256 95f0caa0b448…): Its next desk test names this section and Pl. 111b. Follows the Kenyon decision rows. Outcome ids: `reg:P60-T1:as-predicted`, `…:not-as-predicted`, `…:silent`.

### Coverage joins (feature_workbench/coverage)

- `coverage-volume-tell-es-sultan`: 4 joins, now undeterminable. Prediction: Trench II joins stay undeterminable: the plates give local levels, but the target still lacks a declared distance band and origin. Outcome ids: `cov:coverage-volume-tell-es-sultan:as-predicted`, `…:not-as-predicted`.

### Closed results and their reopening criteria (ACTIVE_TEST)

None.

### Families with no prediction

- XII 10; entry 25; IV/17; rarity; closed tests: Unrelated.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `dec:usable-mouth:usable-early+joint-early`, `dec:usable-mouth:usable-early+joint-71-135-only`, `dec:period-or-access-miss:usable-early+no-joint`, `dec:truncation-only:usable-early+undetermined`, `dec:usable-mouth:built-71-135+joint-71-135-only`, `dec:period-or-access-miss:built-71-135+no-joint`, `dec:period-or-access-miss:built-71-135+undetermined`, `dec:period-or-access-miss:outside-both+no-joint`, `dec:period-or-access-miss:outside-both+undetermined`, `dec:period-or-access-miss:undated+no-joint`, `dec:truncation-only:undated+undetermined`, `dec:drawing-gate-fails`, `chain:SULTAN-2-quarry-section:confirm`, `chain:SULTAN-2-quarry-section:contradict`, `chain:SULTAN-2-quarry-section:inconclusive`, `chain:SULTAN-2-quarry-section:silent`, `reg:P60-T1:as-predicted`, `reg:P60-T1:not-as-predicted`, `reg:P60-T1:silent`, `cov:coverage-volume-tell-es-sultan:as-predicted`, `cov:coverage-volume-tell-es-sultan:not-as-predicted`
