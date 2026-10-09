# Siloam main-side L103 junction section (surveyed main-basin conduit/trough junction)

Item `szanton-siloam-l103-section`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** Nahshon Szanton, Tel Aviv University
- **Requested:** 6 Oct 2026 05:29:46 UTC (research/measurements/cycle15/siloam_bathing.md (request sent))
- **Asked for:** A named, phase-controlled main-basin junction or section with datum definitions, or the excavation limits, or a custodian referral.
- **Status on 9 October 2026:** pending. No reply recorded by 9 Oct.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: Szanton–Vukosavović–Berko 2024 pp. 27*–39* and Greenhut–Mazor 2020 are already inspected; plans published there are not new.

## What it bears on

- Open questions: R06
- Active questions (ACTIVE_TEST): none
- Entries: 49
- Reserved observation: no

## Handling on arrival

Ordinary intake.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

Source: `discriminate.py` task `decisions-siloam-main-side`, read-only. Coverage factor c = 1.0: The section is the requested record of the junction.

| Outcome id | Kind | Basis | Outcome | Excluded classes |
|---|---|---|---|---|
| `dec:main-place-established` | decisive | recorded | Main-side under-place and phase are established | none |
| `dec:terminal-or-phase-miss` | decisive | recorded | Named terminal lies outside basin or required phase | entry49-siloam: entry49-siloam-c01 |
| `dec:unexposed-junction` | partial | recorded | Survey confirms junction was not exposed | none |
| `dec:reply-or-record-inconclusive` | not_obtained | recorded | No usable main-side record arrives | none |

Class legend:
- `entry49-siloam-c01` (entry49-siloam): branch: Entry 49: Siloam main-basin terminal branch

What each class predicts for this item:
- `entry49-siloam-c01` (entry49-siloam): compatible decisive outcomes: `dec:main-place-established`. Excluded by: `dec:terminal-or-phase-miss`. Survives every other outcome, including silence.

### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)

No prediction from the other 28 chain models (no link of theirs uses this record): Tell es-Sultan (old Jericho); Kh. el-Marjama at ʿEin Samiya; Kh. Qumran; Qarn Sarṭaba (Alexandrium); Janoaḥ route (entry 60 reading שבינח); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; Tulul Abu el-'Alaiq; Kypros; Tell es-Samrat; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; unnamed WBADB unit S3961; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

No registry record uses this item.

### Closed results and their reopening criteria (ACTIVE_TEST)

- Siloam main pool, entry 49. Reopen for: A surveyed section of the main-side L103 junction with aperture, basin edge and floor in one phase, plus evidence for the bath function. Can this item satisfy it: **partly**. The section can supply the junction; the bath-function evidence is a separate requirement. Outcome ids: `closed1:reopen-triggered`, `closed1:not-triggered`.

### Other registered predictions

**pred1. Siloam named branch (decisions entry49-siloam-c01): Main-basin branch: Birket al-Hamra is the bathing pool; the place lies under a pipe inside it** (EVIDENCE: plans.json outcomes.)

- Predicts: A surveyed under-pipe place inside the main basin, with basin boundary, ancient floor and the terminal in one phase.
- Confirm if: Outcome main-place-established.
- Contradict if: Outcome terminal-or-phase-miss: the named terminal lies outside the basin or outside the required phase.
- Inconclusive if: Outcome unexposed-junction (the junction was never exposed).
- Silent if: Outcome reply-or-record-inconclusive.

**pred2. Siloam, receiver alternative (siloam_bathing.md): L103 connects to the small receiving basin, not to a place inside Birket** (EVIDENCE: recorded plan topology.)

- Predicts: The section shows the junction at the receiver side, with no main-basin under-pipe place.
- Confirm if: The junction is drawn at the receiver.
- Contradict if: A main-basin junction is drawn in the same phase.
- Inconclusive if: Junction unexposed.
- Silent if: No section.

### Families with no prediction

- Koḥlit; XII 10; entry 25; IV/17; rarity: Unrelated entry.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `dec:main-place-established`, `dec:terminal-or-phase-miss`, `dec:unexposed-junction`, `dec:reply-or-record-inconclusive`, `pred1:confirm`, `pred1:contradict`, `pred1:inconclusive`, `pred1:silent`, `pred2:confirm`, `pred2:contradict`, `pred2:inconclusive`, `pred2:silent`, `closed1:reopen-triggered`, `closed1:not-triggered`
