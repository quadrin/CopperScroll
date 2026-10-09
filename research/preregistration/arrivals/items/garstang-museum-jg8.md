# Garstang Jericho papers JG/8; pre-camp photographs and plans of the ground north of Tell es-Sultan

Item `garstang-museum-jg8`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** Garstang Museum of Archaeology, University of Liverpool
- **Requested:** 8 Oct 2026 about 04:09 UTC (research/ACTIVE_TEST.md; registration_protocol.md §1)
- **Asked for:** Papers and pre-1948 records of the strip north of the tell.
- **Status on 9 October 2026:** pending. No reply recorded by 9 Oct.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: no Garstang record has been inspected in the repository (git grep finds only request mentions).

## What it bears on

- Open questions: R07
- Active questions (ACTIVE_TEST): 2
- Entries: 60, 19, 11
- Reserved observation: no

## Handling on arrival

Follow research/assessments/kohlit_chain/registration_protocol.md: intake form first, registration record before any fit, low-resolution preview (5 m per pixel or coarser) to mark the target strip, controls picked outside the strip, check point withheld. The SULTAN link predictions below are the step-2 registration that protocol requires.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

No decision class depends on this item. Reason: decisions/discrimination.json, supplementary observation 'north-strip pit mouth': a newly recorded pit in the strip is a new feature assignment, not one of the registered pit roles, so it separates no registered Koḥlit class.

### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)

Inconclusive if the record covers the place but meets neither criterion. Silent if it does not cover the place or relation; silence is never a FAIL.

**Tell es-Sultan (old Jericho)**, link `SULTAN-1-precamp-mouth` (model held by the decision classes; not counted again in the chain metric)

- Branches: RB-M, RB-P, RB-L. Relations: R-E60-TOMBS-AT-MOUTH. Reading dependencies: D-E60-SECOND-WORD, D-E60-BURIED, D-E60-OPENING.
- Predicts: A non-funerary opening (shaft, cistern or pit mouth, 1 m or wider) with at least one grave cut or tomb opening within 10 m of it.
- No prediction from this link under: RB-B.
- Where: The strip from the tell's north foot to about 250 m north: Kenyon II p. 169 skipped it; Area D lies about 100–200 m north (Fig. 91, inference). Under the ʿAin es-Sultan camp since 1948.
- Confirm if: The opening and the grave appear in one registered record, and their distance is 'inside' 10 m under registration_protocol.md.
- Contradict if: cannot contradict (one-sided). Photographs and plans alone cannot contradict: absence may be concealment, burial or resolution. A contradiction needs a coverage-gated excavation record of the strip (coverage module gates) that reached the ancient surface and reports no such pair.
- Coverage factor: not used (the decision classes carry this model).
- Outcome ids: `chain:SULTAN-1-precamp-mouth:confirm`, `chain:SULTAN-1-precamp-mouth:inconclusive`, `chain:SULTAN-1-precamp-mouth:silent`

**Tell es-Sultan (old Jericho)**, link `SULTAN-6-two-pits` (model held by the decision classes; not counted again in the chain metric)

- Branches: RB-M, RB-P, RB-B. Relations: R-E19-EASTERN-PIT-N. Reading dependencies: D-E19-ALLEGRO.
- Predicts: At least two pits or shaft mouths north of the tell whose east–west order can be read.
- Where: The same strip and Kenyon's Areas D, J and G.
- Confirm if: Two openings whose east–west separation exceeds four times the registration error.
- Contradict if: cannot contradict (one-sided). None from photographs alone.
- Coverage factor: not used (the decision classes carry this model).
- Outcome ids: `chain:SULTAN-6-two-pits:confirm`, `chain:SULTAN-6-two-pits:inconclusive`, `chain:SULTAN-6-two-pits:silent`

No prediction from the other 27 chain models (no link of theirs uses this record): Kh. el-Marjama at ʿEin Samiya; Kh. Qumran; Qarn Sarṭaba (Alexandrium); Janoaḥ route (entry 60 reading שבינח); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; Tulul Abu el-'Alaiq; Kypros; Tell es-Samrat; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; unnamed WBADB unit S3961; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

- `P60-T1` (Tell es-Sultan (Old Jericho, Elisha's spring): north-slope graves and cemetery zone N/NW of the tell; record SHA-256 95f0caa0b448…): Its confirm rule needs an independently dated pit and mouth–tomb relation. Photographs and plans locate but do not date (registration_protocol §6). Predicted: P60-T1 stays 'not identifiable' whatever these records show, unless they include a sealed, dated context. Outcome ids: `reg:P60-T1:as-predicted`, `…:not-as-predicted`, `…:silent`.

### Coverage joins (feature_workbench/coverage)

- `coverage-volume-tell-es-sultan`: 4 joins, now undeterminable. Prediction: All 4 joins stay undeterminable. Entry 60 states no distance, so the target needs a declared distance band, which no field record can supply (volume_inputs.json declarations). Outcome ids: `cov:coverage-volume-tell-es-sultan:as-predicted`, `…:not-as-predicted`.

### Closed results and their reopening criteria (ACTIVE_TEST)

None.

### Other registered predictions

**pred1. SULTAN-5-basin-corner (chain.json): Tell es-Sultan, all branches using the historical basin** (EVIDENCE: chain.json link text.)

- Predicts: Silent by construction for records made in 1930–36: the link needs a record made before the 1891–93 mill works.
- Confirm if: Only a pre-1891 record in the papers showing an angle on the basin's north side.
- Contradict if: None from photographs (one-sided).
- Inconclusive if: A pre-1891 record that does not show the north side.
- Silent if: No record older than 1891 (expected).

### Families with no prediction

- Koḥlit decision classes; XII 10 strings; entry 25; rarity: See decision_none_reason; no other family uses this ground.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `chain:SULTAN-1-precamp-mouth:confirm`, `chain:SULTAN-1-precamp-mouth:inconclusive`, `chain:SULTAN-1-precamp-mouth:silent`, `chain:SULTAN-6-two-pits:confirm`, `chain:SULTAN-6-two-pits:inconclusive`, `chain:SULTAN-6-two-pits:silent`, `pred1:confirm`, `pred1:contradict`, `pred1:inconclusive`, `pred1:silent`, `reg:P60-T1:as-predicted`, `reg:P60-T1:not-as-predicted`, `reg:P60-T1:silent`, `cov:coverage-volume-tell-es-sultan:as-predicted`, `cov:coverage-volume-tell-es-sultan:not-as-predicted`
