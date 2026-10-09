# Garstang Papers 1930–36 and pre-1948 photographs of Jericho

Item `pef-garstang-papers-jericho-photos`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** Palestine Exploration Fund, London
- **Requested:** 8 Oct 2026 about 04:09 UTC (research/ACTIVE_TEST.md; registration_protocol.md §1)
- **Asked for:** Papers and photographs; pre-1948 views of the ground north of the tell and of the spring.
- **Status on 9 October 2026:** pending. No reply recorded by 9 Oct.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: Dorrell 1993 Figs 1–4 and 20–21 are already inspected; many early spring photographs are in Dorrell's selection. Only PEF records outside Dorrell's selection count for SULTAN-5 (chain.json note).

## What it bears on

- Open questions: R07
- Active questions (ACTIVE_TEST): 2, 3
- Entries: 60, 19, 11
- Reserved observation: no

## Handling on arrival

Follow research/assessments/kohlit_chain/registration_protocol.md: intake form first, registration record before any fit, low-resolution preview (5 m per pixel or coarser) to mark the target strip, controls picked outside the strip, check point withheld. The SULTAN link predictions below are the step-2 registration that protocol requires. Before opening, list which photographs are already in Dorrell 1993; mark them exposed.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

No decision class depends on this item. Reason: Same as the Garstang Museum item: a new strip pit is not a registered pit role. A spring photograph cannot supply the sealed basin-rim contact the decisions module needs (supplementary observation 'springhouse sealed finds').

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

**Tell es-Sultan (old Jericho)**, link `SULTAN-5-basin-corner` (model held by the decision classes; not counted again in the chain metric)

- Branches: all branches using the historical basin. Relations: R-E11-POOL-NCORNER. Reading dependencies: none.
- Predicts: A record made before the 1891–93 mill works shows the spring basin with an angle on its north side.
- Where: The ʿAin es-Sultan basin at the tell's east foot.
- Confirm if: An angle on the basin's north side before 1891, not formed by the mill works.
- Contradict if: cannot contradict (one-sided). None from photographs: they show post-ancient states. A curved north end (the 1908 plan shows one for the 1898 reservoir) cannot reject an earlier cornered pool.
- Coverage factor: not used (the decision classes carry this model).
- Outcome ids: `chain:SULTAN-5-basin-corner:confirm`, `chain:SULTAN-5-basin-corner:inconclusive`, `chain:SULTAN-5-basin-corner:silent`

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

- `P60-T1` (Tell es-Sultan (Old Jericho, Elisha's spring): north-slope graves and cemetery zone N/NW of the tell; record SHA-256 95f0caa0b448…): As for the Garstang Museum item: stays 'not identifiable' unless a dated sealed context is recorded. Outcome ids: `reg:P60-T1:as-predicted`, `…:not-as-predicted`, `…:silent`.

### Coverage joins (feature_workbench/coverage)

- `coverage-volume-tell-es-sultan`: 4 joins, now undeterminable. Prediction: All 4 joins stay undeterminable (no distance band can come from a record). Outcome ids: `cov:coverage-volume-tell-es-sultan:as-predicted`, `…:not-as-predicted`.

### Closed results and their reopening criteria (ACTIVE_TEST)

None.

### Families with no prediction

- Koḥlit decision classes; XII 10 strings; entry 25; rarity: No registered class uses these records.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `chain:SULTAN-1-precamp-mouth:confirm`, `chain:SULTAN-1-precamp-mouth:inconclusive`, `chain:SULTAN-1-precamp-mouth:silent`, `chain:SULTAN-5-basin-corner:confirm`, `chain:SULTAN-5-basin-corner:inconclusive`, `chain:SULTAN-5-basin-corner:silent`, `chain:SULTAN-6-two-pits:confirm`, `chain:SULTAN-6-two-pits:inconclusive`, `chain:SULTAN-6-two-pits:silent`, `reg:P60-T1:as-predicted`, `reg:P60-T1:not-as-predicted`, `reg:P60-T1:silent`, `cov:coverage-volume-tell-es-sultan:as-predicted`, `cov:coverage-volume-tell-es-sultan:not-as-predicted`
