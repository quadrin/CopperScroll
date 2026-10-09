# ÉBAF's EDF copy of the scroll and the EDF X-rays of segments 21–22, seen during the 18–24 Oct visit

Item `ebaf-edf-copy-and-xrays-21-22`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** École biblique (J.-B. Humbert; visit passed to Fr. Cyrille Jalabert)
- **Requested:** 8 Oct 2026 about 04:22 UTC (research/ACTIVE_TEST.md; shared status file 8 Oct)
- **Asked for:** To see the copy and the X-rays during the visit.
- **Status on 9 October 2026:** pending. Reply 8 Oct: visit passed to Fr. Jalabert. Viewing expected 18–24 Oct.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: the protocol lists Puech's copy, photo and radiograph plates as known exposure (pls. CCCLV–CCCLVI show the cut). Whether the EDF films are those exposures is unknown: unused status unverified.
- **Exposure:** INFERENCE: the owner, if he views the X-rays himself, becomes exposed and cannot serve as a blinded reader. Record his viewing scope.

## What it bears on

- Open questions: R07
- Active questions (ACTIVE_TEST): 1
- Entries: 60
- Reserved observation: yes

## Handling on arrival

Reserved observation. No agent opens, crops or views any image of XII 8–12 or of the 21/22 cut. The frozen protocol (fd3f334, SHA-256 0e19467c…) governs: an administrator records lineage and masks the target; two blinded readers lock Stages 1 and 2. This register adds no letter prediction. It maps protocol outcomes to model classes only. On site: record film or copy identifiers, capture conditions and any photographs made, before anyone reads the target.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

Source: `discriminate.py` task `decisions-xii10`, read-only. Coverage factor c = 1.0: The X-rays are radiographs of segments 21–22. The copy part gets no decisive rows (see other predictions).

**Mapping only: no letter prediction.** Each row is a possible outcome of the frozen protocol. Rule from the protocol's components: if R4 (שבינח) is rejected, the three Janoaḥ classes (c08–c10, reading RB-L) are excluded; if R4 survives, all 10 Koḥlit classes survive, because R4 support needs a separate linguistic and geographic argument. Chain model M-JANOAH and registry record P60-T8 follow c08–c10.

| Outcome id | Protocol outcome | Kind | Surviving strings | Surviving Koḥlit classes | Excluded Koḥlit classes |
|---|---|---|---|---|---|
| `dec:finite-set-rejected:none` | finite-set-rejected | decisive | none | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:finite-set-rejected:none:open-components` | finite-set-rejected | partial | none | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:one-sequence:R1` | one-sequence | decisive | R1 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:one-sequence:R2` | one-sequence | decisive | R2 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:one-sequence:R3` | one-sequence | decisive | R3 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:one-sequence:R4` | one-sequence | decisive | R4 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |
| `dec:one-sequence:R5` | one-sequence | decisive | R5 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:one-sequence:R6` | one-sequence | decisive | R6 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:one-sequence:R7` | one-sequence | decisive | R7 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R1` | partial-reading | partial | R1 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R1+R2` | partial-reading | partial | R1, R2 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R1+R2+R3+R4+R5+R6` | partial-reading | partial | R1, R2, R3, R4, R5, R6 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |
| `dec:partial-reading:R1+R2+R3+R4+R5+R6+R7` | partial-reading | partial | R1, R2, R3, R4, R5, R6, R7 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |
| `dec:partial-reading:R1+R2+R5+R6` | partial-reading | partial | R1, R2, R5, R6 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R1+R2+R5+R6+R7` | partial-reading | partial | R1, R2, R5, R6, R7 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R1+R5+R6` | partial-reading | partial | R1, R5, R6 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R2` | partial-reading | partial | R2 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R2+R3+R4` | partial-reading | partial | R2, R3, R4 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |
| `dec:partial-reading:R2+R3+R4+R7` | partial-reading | partial | R2, R3, R4, R7 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |
| `dec:partial-reading:R2+R7` | partial-reading | partial | R2, R7 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R3` | partial-reading | partial | R3 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R3+R4` | partial-reading | partial | R3, R4 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |
| `dec:partial-reading:R3+R7` | partial-reading | partial | R3, R7 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R4` | partial-reading | partial | R4 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |
| `dec:partial-reading:R4+R5` | partial-reading | partial | R4, R5 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |
| `dec:partial-reading:R5` | partial-reading | partial | R5 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R6` | partial-reading | partial | R6 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:partial-reading:R7` | partial-reading | partial | R7 | c01, c02, c03, c04, c05, c06, c07 | c08, c09, c10 |
| `dec:reading-gate-fails` | reading-gate-fails | not_obtained | R1, R2, R3, R4, R5, R6, R7 | c01, c02, c03, c04, c05, c06, c07, c08, c09, c10 | none |

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
- `R1` (xii10): string: R1 שכנה
- `R2` (xii10): string: R2 שבנה
- `R3` (xii10): string: R3 שבצח
- `R4` (xii10): string: R4 שבינח
- `R5` (xii10): string: R5 שכינה
- `R6` (xii10): string: R6 שכונה
- `R7` (xii10): string: R7 שבצהב

What each class predicts for this item:
- `c01` (kohlit): no prediction about this item. It survives every registered outcome.
- `c02` (kohlit): no prediction about this item. It survives every registered outcome.
- `c03` (kohlit): no prediction about this item. It survives every registered outcome.
- `c04` (kohlit): no prediction about this item. It survives every registered outcome.
- `c05` (kohlit): no prediction about this item. It survives every registered outcome.
- `c06` (kohlit): no prediction about this item. It survives every registered outcome.
- `c07` (kohlit): no prediction about this item. It survives every registered outcome.
- `c08` (kohlit): compatible decisive outcomes: `dec:one-sequence:R4`. Excluded by: `dec:finite-set-rejected:none`, `dec:finite-set-rejected:none:open-components`, `dec:one-sequence:R1`, `dec:one-sequence:R2`, `dec:one-sequence:R3`, `dec:one-sequence:R5`, `dec:one-sequence:R6`, `dec:one-sequence:R7`, `dec:partial-reading:R1`, `dec:partial-reading:R1+R2`, `dec:partial-reading:R1+R2+R5+R6`, `dec:partial-reading:R1+R2+R5+R6+R7`, `dec:partial-reading:R1+R5+R6`, `dec:partial-reading:R2`, `dec:partial-reading:R2+R7`, `dec:partial-reading:R3`, `dec:partial-reading:R3+R7`, `dec:partial-reading:R5`, `dec:partial-reading:R6`, `dec:partial-reading:R7`. Survives every other outcome, including silence.
- `c09` (kohlit): compatible decisive outcomes: `dec:one-sequence:R4`. Excluded by: `dec:finite-set-rejected:none`, `dec:finite-set-rejected:none:open-components`, `dec:one-sequence:R1`, `dec:one-sequence:R2`, `dec:one-sequence:R3`, `dec:one-sequence:R5`, `dec:one-sequence:R6`, `dec:one-sequence:R7`, `dec:partial-reading:R1`, `dec:partial-reading:R1+R2`, `dec:partial-reading:R1+R2+R5+R6`, `dec:partial-reading:R1+R2+R5+R6+R7`, `dec:partial-reading:R1+R5+R6`, `dec:partial-reading:R2`, `dec:partial-reading:R2+R7`, `dec:partial-reading:R3`, `dec:partial-reading:R3+R7`, `dec:partial-reading:R5`, `dec:partial-reading:R6`, `dec:partial-reading:R7`. Survives every other outcome, including silence.
- `c10` (kohlit): compatible decisive outcomes: `dec:one-sequence:R4`. Excluded by: `dec:finite-set-rejected:none`, `dec:finite-set-rejected:none:open-components`, `dec:one-sequence:R1`, `dec:one-sequence:R2`, `dec:one-sequence:R3`, `dec:one-sequence:R5`, `dec:one-sequence:R6`, `dec:one-sequence:R7`, `dec:partial-reading:R1`, `dec:partial-reading:R1+R2`, `dec:partial-reading:R1+R2+R5+R6`, `dec:partial-reading:R1+R2+R5+R6+R7`, `dec:partial-reading:R1+R5+R6`, `dec:partial-reading:R2`, `dec:partial-reading:R2+R7`, `dec:partial-reading:R3`, `dec:partial-reading:R3+R7`, `dec:partial-reading:R5`, `dec:partial-reading:R6`, `dec:partial-reading:R7`. Survives every other outcome, including silence.
- XII 10 strings R1–R7: these are the protocol's own alternatives; the protocol scores them. No further prediction is added.

### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)

Inconclusive if the record covers the place but meets neither criterion. Silent if it does not cover the place or relation; silence is never a FAIL.

**Janoaḥ route (entry 60 reading שבינח)**, link `JANOAH-0-reading-gate` (model held by the decision classes; not counted again in the chain metric)

- Branches: RB-L. Relations: reading gate. Reading dependencies: D-E60-SECOND-WORD.
- Predicts: reading gate only. No letter expectation is restated here; the outcome follows the mapping table above (R4 rejected: contradicted; R4 surviving: not contradicted).
- Where: XII 10 at the segment 21/22 saw cut.
- Confirm if: The protocol's Janoaḥ criteria are met.
- Contradict if (two-sided): The protocol's 'situated' or other non-Janoaḥ criteria are met.
- Coverage factor: not used (the decision classes carry this model).
- Outcome ids: `chain:JANOAH-0-reading-gate:confirm`, `chain:JANOAH-0-reading-gate:contradict`, `chain:JANOAH-0-reading-gate:inconclusive`, `chain:JANOAH-0-reading-gate:silent`

No prediction from the other 27 chain models (no link of theirs uses this record): Tell es-Sultan (old Jericho); Kh. el-Marjama at ʿEin Samiya; Kh. Qumran; Qarn Sarṭaba (Alexandrium); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; Tulul Abu el-'Alaiq; Kypros; Tell es-Samrat; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; unnamed WBADB unit S3961; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

- `P60-T8` (Kh. Yanun / Yanun (Janoah of Ephraim): pits, caves or shaft tombs at the site ("the pit which is in Janoah", Lefkovits); record SHA-256 935512c4a537…): Follows the XII 10 mapping. Outcome ids: `reg:P60-T8:as-predicted`, `…:not-as-predicted`, `…:silent`.

### Closed results and their reopening criteria (ACTIVE_TEST)

None.

### Other registered predictions

**pred1. XII 10 protocol, evidence rule (protocol lines 37 and 43): Frozen protocol fd3f334** (INFERENCE from protocol wording; the integrator should confirm that a galvanoplastic copy counts as a copy, not the original.)

- Predicts: Observations on the EDF copy cannot be decisive letter components, because a decisive mark must be visible in the unadjusted original. They are reported separately (letter controls series S4).
- Confirm if: Not a letter claim; the copy is logged as series S4.
- Contradict if: Not applicable.
- Inconclusive if: Not applicable.
- Silent if: The copy is not shown.

**pred2. Letter controls (PROTOCOL §5): Series S3 calibration** (INFERENCE from the protocol's series table.)

- Predicts: S3 calibration needs EDF radiographs of segments 1–18. X-rays of 21–22 alone cannot calibrate.
- Confirm if: Only 21–22 radiographs are seen or copied.
- Contradict if: Radiographs of segments 1–18 are also obtained.
- Inconclusive if: Segment identities of the films are unrecorded.
- Silent if: No radiograph is shown.

### Families with no prediction

- Entry 25; IV/17 coverage; rarity; closed Jericho and Siloam branches: No registered model uses these images.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `dec:finite-set-rejected:none`, `dec:finite-set-rejected:none:open-components`, `dec:one-sequence:R1`, `dec:one-sequence:R2`, `dec:one-sequence:R3`, `dec:one-sequence:R4`, `dec:one-sequence:R5`, `dec:one-sequence:R6`, `dec:one-sequence:R7`, `dec:partial-reading:R1`, `dec:partial-reading:R1+R2`, `dec:partial-reading:R1+R2+R3+R4+R5+R6`, `dec:partial-reading:R1+R2+R3+R4+R5+R6+R7`, `dec:partial-reading:R1+R2+R5+R6`, `dec:partial-reading:R1+R2+R5+R6+R7`, `dec:partial-reading:R1+R5+R6`, `dec:partial-reading:R2`, `dec:partial-reading:R2+R3+R4`, `dec:partial-reading:R2+R3+R4+R7`, `dec:partial-reading:R2+R7`, `dec:partial-reading:R3`, `dec:partial-reading:R3+R4`, `dec:partial-reading:R3+R7`, `dec:partial-reading:R4`, `dec:partial-reading:R4+R5`, `dec:partial-reading:R5`, `dec:partial-reading:R6`, `dec:partial-reading:R7`, `dec:reading-gate-fails`, `chain:JANOAH-0-reading-gate:confirm`, `chain:JANOAH-0-reading-gate:contradict`, `chain:JANOAH-0-reading-gate:inconclusive`, `chain:JANOAH-0-reading-gate:silent`, `pred1:confirm`, `pred1:contradict`, `pred1:inconclusive`, `pred1:silent`, `pred2:confirm`, `pred2:contradict`, `pred2:inconclusive`, `pred2:silent`, `reg:P60-T8:as-predicted`, `reg:P60-T8:not-as-predicted`, `reg:P60-T8:silent`
