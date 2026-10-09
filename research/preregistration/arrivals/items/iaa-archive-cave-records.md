# Judean Desert cave-survey records: Qumran cliffs and marl, Jericho escarpment (Jebel Qarantal to Wadi Nuweiʿimeh/ʿAin Duk), Wadi Qelt gorge

Item `iaa-archive-cave-records`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** Israel Antiquities Authority Archive (to forward to the Judean Desert survey project)
- **Requested:** 7 Oct 2026 15:43 UTC (research/agent_review_2026-10-07/followup/F_outreach_sent.md row 3)
- **Asked for:** Per cave: identifier, coarse location (100–250 m cell), number of openings and their facing, features, size, periods, disturbance.
- **Status on 9 October 2026:** pending. No reply recorded by 9 Oct.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: the 2002 cave-survey entries cited by WBADB are supplied but unread for these caves (chain record REC-ATIQOT41-CAVES). INFERENCE: they are the same survey lineage. Whichever is opened first is the observation; these predictions apply to both.
- **Exposure:** EVIDENCE: IV/17 (Sion 2002 Plan 5) is already inspected; its chord-normal proxies are 123° and 119° (entry25_iv17/README.md).

## What it bears on

- Open questions: R07, R02
- Active questions (ACTIVE_TEST): none
- Entries: 60, 25
- Reserved observation: no

## Handling on arrival

Ordinary intake. Before reading facing fields, check that this register is pushed.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

No decision class depends on this item. Reason: No decision task uses the cave inventory. Entry 25 mouth bearings could separate classes, but no aspect rule is frozen (decisions README), so this item gets no Entry 25 rows (RANKING_PLAN).

### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)

Inconclusive if the record covers the place but meets neither criterion. Silent if it does not cover the place or relation; silence is never a FAIL.

**Kh. Qumran**, link `QUMRAN-1-opening-facing`

- Branches: RB-M only. Relations: R-E60-OPENING-N. Reading dependencies: D-E60-OPENING, D-E60-SECOND-WORD.
- Predicts: At least one non-funerary cave or shaft at 315°–45° within 1 km of the site has an opening that faces 315°–45°.
- No prediction from this link under: RB-P, RB-B.
- Where: The marl terraces and cliffs north and north-west of Kh. Qumran, including Caves XI/18 and XI/20.
- Confirm if: A recorded north-facing opening on a north-sector cave or shaft.
- Contradict if (two-sided): The records give a facing for every north-sector cave within 1 km, and none faces 315°–45°. This rejects RB-M at the recorded caves only.
- Coverage factor c = 0.5.
- Outcome ids: `chain:QUMRAN-1-opening-facing:confirm`, `chain:QUMRAN-1-opening-facing:contradict`, `chain:QUMRAN-1-opening-facing:inconclusive`, `chain:QUMRAN-1-opening-facing:silent`

**Kh. Qumran**, link `QUMRAN-2-mouth`

- Branches: RB-M, RB-P. Relations: R-E60-TOMBS-AT-MOUTH. Reading dependencies: D-E60-BURIED.
- Predicts: A grave within 10 m of the mouth of a non-funerary cave, cistern or shaft north of the site.
- No prediction from this link under: RB-B.
- Where: The northern secondary cemetery and any opening beside it.
- Confirm if: A grave and an opening drawn in one plan within 10 m.
- Contradict if (absence-statement only): Only a complete plan of the north cemetery area showing every opening more than 10 m from every grave.
- Coverage factor c = 0.25.
- Outcome ids: `chain:QUMRAN-2-mouth:confirm`, `chain:QUMRAN-2-mouth:contradict`, `chain:QUMRAN-2-mouth:inconclusive`, `chain:QUMRAN-2-mouth:silent`

**Tulul Abu el-'Alaiq**, link `S2539-1-graves-north`

- Branches: RB-M, RB-P. Relations: R-E60-GRAVES-N-SECTOR, R-E60-TOMBS-AT-MOUTH. Reading dependencies: D-E60-BURIED, D-E60-SECOND-WORD.
- Predicts: A grave or tomb, not securely later than 135 CE, in the north sector; ideally within 10 m of the selected pit's mouth.
- No prediction from this link under: RB-B.
- Where: 315°–45° within 1 km of WBADB S2539 (191400/139750, OIG). Record: Weiss 2002 IX/9, IX/10, IX/17; Hirschfeld site 19.
- Confirm if: A placed grave in the sector, or a grave at the selected pit's mouth.
- Contradict if (absence-statement only): The record lists every grave near the site, places all of them outside the north sector, and states the list is complete; or the only northern grave is securely later than 135 CE.
- Coverage factor c = 0.25.
- Outcome ids: `chain:S2539-1-graves-north:confirm`, `chain:S2539-1-graves-north:contradict`, `chain:S2539-1-graves-north:inconclusive`, `chain:S2539-1-graves-north:silent`

**Tulul Abu el-'Alaiq**, link `S2539-2-opening-facing`

- Branches: RB-M only. Relations: R-E60-OPENING-N. Reading dependencies: D-E60-OPENING, D-E60-SECOND-WORD.
- Predicts: At least one of the selected north-sector caves has an opening facing 315°–45°.
- No prediction from this link under: RB-P, RB-B.
- Where: Weiss 2002 IX/9, IX/10, IX/17 (natural caves, no finds).
- Confirm if: A recorded north-facing opening.
- Contradict if (two-sided): Every selected cave has a recorded facing and none faces 315°–45°: this rejects RB-M at these caves only.
- Coverage factor c = 0.5.
- Outcome ids: `chain:S2539-2-opening-facing:confirm`, `chain:S2539-2-opening-facing:contradict`, `chain:S2539-2-opening-facing:inconclusive`, `chain:S2539-2-opening-facing:silent`

**Kypros**, link `S2589-1-graves-north`

- Branches: RB-M, RB-P. Relations: R-E60-GRAVES-N-SECTOR, R-E60-TOMBS-AT-MOUTH. Reading dependencies: D-E60-BURIED, D-E60-SECOND-WORD.
- Predicts: A grave or tomb, not securely later than 135 CE, in the north sector; ideally within 10 m of the selected pit's mouth.
- No prediction from this link under: RB-B.
- Where: 315°–45° within 1 km of WBADB S2589 (190500/139050, OIG). Record: Weiss 2002 IX/21, IX/22; Hirschfeld site 18.
- Confirm if: A placed grave in the sector, or a grave at the selected pit's mouth.
- Contradict if (absence-statement only): The record lists every grave near the site, places all of them outside the north sector, and states the list is complete; or the only northern grave is securely later than 135 CE.
- Coverage factor c = 0.25.
- Outcome ids: `chain:S2589-1-graves-north:confirm`, `chain:S2589-1-graves-north:contradict`, `chain:S2589-1-graves-north:inconclusive`, `chain:S2589-1-graves-north:silent`

**Kypros**, link `S2589-2-opening-facing`

- Branches: RB-M only. Relations: R-E60-OPENING-N. Reading dependencies: D-E60-OPENING, D-E60-SECOND-WORD.
- Predicts: At least one of the selected north-sector caves has an opening facing 315°–45°.
- No prediction from this link under: RB-P, RB-B.
- Where: Weiss 2002 IX/21, IX/22 (natural caves, no finds).
- Confirm if: A recorded north-facing opening.
- Contradict if (two-sided): Every selected cave has a recorded facing and none faces 315°–45°: this rejects RB-M at these caves only.
- Coverage factor c = 0.5.
- Outcome ids: `chain:S2589-2-opening-facing:confirm`, `chain:S2589-2-opening-facing:contradict`, `chain:S2589-2-opening-facing:inconclusive`, `chain:S2589-2-opening-facing:silent`

**Tell es-Samrat**, link `S2430-2-opening-facing`

- Branches: RB-M only. Relations: R-E60-OPENING-N. Reading dependencies: D-E60-OPENING, D-E60-SECOND-WORD.
- Predicts: At least one of the selected north-sector caves has an opening facing 315°–45°.
- No prediction from this link under: RB-P, RB-B.
- Where: Eshel and Zissu 2002a VIII/28 (Cave of the Sandal) and VIII/29 (Cave of the Pruṭa).
- Confirm if: A recorded north-facing opening.
- Contradict if (two-sided): Every selected cave has a recorded facing and none faces 315°–45°: this rejects RB-M at these caves only.
- Coverage factor c = 0.5.
- Outcome ids: `chain:S2430-2-opening-facing:confirm`, `chain:S2430-2-opening-facing:contradict`, `chain:S2430-2-opening-facing:inconclusive`, `chain:S2430-2-opening-facing:silent`

**unnamed WBADB unit S3961**, link `S3961-2-opening-facing`

- Branches: RB-M only. Relations: R-E60-OPENING-N. Reading dependencies: D-E60-OPENING, D-E60-SECOND-WORD.
- Predicts: At least one of the selected north-sector caves has an opening facing 315°–45°.
- No prediction from this link under: RB-P, RB-B.
- Where: Cave Q-4 (E761) and Cave B-49 (S3900).
- Confirm if: A recorded north-facing opening.
- Contradict if (two-sided): Every selected cave has a recorded facing and none faces 315°–45°: this rejects RB-M at these caves only.
- Coverage factor c = 0.5.
- Outcome ids: `chain:S3961-2-opening-facing:confirm`, `chain:S3961-2-opening-facing:contradict`, `chain:S3961-2-opening-facing:inconclusive`, `chain:S3961-2-opening-facing:silent`

No prediction from the other 23 chain models (no link of theirs uses this record): Tell es-Sultan (old Jericho); Kh. el-Marjama at ʿEin Samiya; Qarn Sarṭaba (Alexandrium); Janoaḥ route (entry 60 reading שבינח); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

- `P60-T4` (Qumran-Buqeia district (repo sequence study; not a published proposal); record SHA-256 363864ac306c…): No prediction: next test 'None'. Outcome ids: `reg:P60-T4:as-predicted`, `…:not-as-predicted`, `…:silent`.
- `P60-T7` (ʿAyn Feshkha area; record SHA-256 37dd3093edc9…): No prediction: next test 'None before T1–T3'. Outcome ids: `reg:P60-T7:as-predicted`, `…:not-as-predicted`, `…:silent`.

### Closed results and their reopening criteria (ACTIVE_TEST)

None.

### Other registered predictions

**pred1. Entry 25 (decisions iv17 task, bearing component): Classes needing both mouths east (entry25-c02, c03, c05)** (INFERENCE. Proposal: the integrator freezes an aspect rule before this item or the L-656 file arrives.)

- Predicts: No scoreable prediction: no aspect rule is frozen. A per-mouth facing for IV/17 is logged as data only.
- Confirm if: Not scoreable.
- Contradict if: Not scoreable.
- Inconclusive if: Always, until an aspect rule is frozen before the record is read.
- Silent if: No per-mouth facing for IV/17.

### Families with no prediction

- XII 10 strings; IV/17 coverage; rarity counts; closed tests: No registered model uses a cave inventory; no model predicts how many two-mouth caves the region holds (R02 regional eligibility).

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `chain:QUMRAN-1-opening-facing:confirm`, `chain:QUMRAN-1-opening-facing:contradict`, `chain:QUMRAN-1-opening-facing:inconclusive`, `chain:QUMRAN-1-opening-facing:silent`, `chain:QUMRAN-2-mouth:confirm`, `chain:QUMRAN-2-mouth:contradict`, `chain:QUMRAN-2-mouth:inconclusive`, `chain:QUMRAN-2-mouth:silent`, `chain:S2539-1-graves-north:confirm`, `chain:S2539-1-graves-north:contradict`, `chain:S2539-1-graves-north:inconclusive`, `chain:S2539-1-graves-north:silent`, `chain:S2539-2-opening-facing:confirm`, `chain:S2539-2-opening-facing:contradict`, `chain:S2539-2-opening-facing:inconclusive`, `chain:S2539-2-opening-facing:silent`, `chain:S2589-1-graves-north:confirm`, `chain:S2589-1-graves-north:contradict`, `chain:S2589-1-graves-north:inconclusive`, `chain:S2589-1-graves-north:silent`, `chain:S2589-2-opening-facing:confirm`, `chain:S2589-2-opening-facing:contradict`, `chain:S2589-2-opening-facing:inconclusive`, `chain:S2589-2-opening-facing:silent`, `chain:S2430-2-opening-facing:confirm`, `chain:S2430-2-opening-facing:contradict`, `chain:S2430-2-opening-facing:inconclusive`, `chain:S2430-2-opening-facing:silent`, `chain:S3961-2-opening-facing:confirm`, `chain:S3961-2-opening-facing:contradict`, `chain:S3961-2-opening-facing:inconclusive`, `chain:S3961-2-opening-facing:silent`, `pred1:confirm`, `pred1:contradict`, `pred1:inconclusive`, `pred1:silent`, `reg:P60-T4:as-predicted`, `reg:P60-T4:not-as-predicted`, `reg:P60-T4:silent`, `reg:P60-T7:as-predicted`, `reg:P60-T7:not-as-predicted`, `reg:P60-T7:silent`
