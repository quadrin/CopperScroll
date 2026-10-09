# Zertal 1992, Manasseh Hill Country Survey vol. I (14 Stage 2 rarity units)

Item `zertal-vol-1`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** Library (not obtained; Berkeley library day planned)
- **Requested:** Not requested (research/rarity/kohlit/stage2/addendum_s2/ADDENDUM.md ('Not read'); shared status file 'Next')
- **Asked for:** Units S103, S153, S178, S563, S778, S806 (main set) and S112, S137, S144, S152, S157, S203, S780, S798 (pre-70 set only).
- **Status on 9 October 2026:** not_obtained. Not in the Drive index (Zertal folder holds vols 2–4 only).
- **Arrived before registration:** nothing.

## What it bears on

- Open questions: R07
- Active questions (ACTIVE_TEST): none
- Entries: 11, 60
- Reserved observation: no

## Handling on arrival

Code under the frozen Stage 2 protocol and match.py (b7a682b), following addendum_s2/PROCEDURE.md; two coders as before.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

No decision class depends on this item. Reason: No decision class uses these units.

### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)

No prediction from the other 28 chain models (no link of theirs uses this record): Tell es-Sultan (old Jericho); Kh. el-Marjama at ʿEin Samiya; Kh. Qumran; Qarn Sarṭaba (Alexandrium); Janoaḥ route (entry 60 reading שבינח); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; Tulul Abu el-'Alaiq; Kypros; Tell es-Samrat; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; unnamed WBADB unit S3961; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

No registry record uses this item.

### Closed results and their reopening criteria (ACTIVE_TEST)

None.

### Other registered predictions

**pred1. Rarity count, registered rules (preregistration §6; RESULTS headline after both addenda): Headline branch A, survey level: k = 0, f = 20, m = 313 of 333** (INFERENCE: arithmetic bound on registered numbers.)

- Predicts: The verdict 'not measurable from available evidence' cannot change: Vol. I touches 6 main-set units, so k ≤ 6 while m ≥ 307.
- Confirm if: After coding, m ≫ k still holds (deterministic bound).
- Contradict if: Impossible under the bound.
- Inconclusive if: Not applicable.
- Silent if: Not applicable.

**pred2. Observation-process audit (rarity/kohlit/observation_process/README.md): Absence statements are site-scoped** (EVIDENCE: 61 of the 63 absence statements in the rarity count are Zertal's 'Cisterns: none'; none gives a search radius.)

- Predicts: Every new C2 FAIL rests on a site-level absence statement ('Cisterns: none' or similar) that gives no search radius over the 1 km northern sector. Under the audit's scope rule f stays 0.
- Confirm if: Each new FAIL cites a site-record absence without a radius.
- Contradict if: A new FAIL rests on a statement that a defined area of the northern sector was searched.
- Inconclusive if: No new FAIL.
- Silent if: Volume not obtained.

**pred3. Reference rate (not a model test): Vols 2–4 outcome** (INFERENCE.)

- Predicts: INFERENCE: if vol. I resembles vols 2–4 (19 of 60 main-set Zertal units became C2 FAIL), about 2 of the 6 main-set units become C2 FAIL. Recorded as a calibration check, not scored as a model test.
- Confirm if: 1–3 main-set C2 FAILs.
- Contradict if: 0 or more than 3 (no model is affected).
- Inconclusive if: Not applicable.
- Silent if: Volume not obtained.

### Rarity units

- units_main: S103, S153, S178, S563, S778, S806
- units_pre70_only: S112, S137, S144, S152, S157, S203, S780, S798

### Families with no prediction

- Koḥlit chain models: None of the 14 units is one of the 28 chain models.
- Koḥlit decision classes; XII 10; entry 25; IV/17; closed tests: Unrelated.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `pred1:confirm`, `pred1:contradict`, `pred1:inconclusive`, `pred1:silent`, `pred2:confirm`, `pred2:contradict`, `pred2:inconclusive`, `pred2:silent`, `pred3:confirm`, `pred3:contradict`, `pred3:inconclusive`, `pred3:silent`
