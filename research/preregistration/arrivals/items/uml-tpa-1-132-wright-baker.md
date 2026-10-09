# File GB 133 TPA/1/132 (Allegro–Harding–Wright Baker letters on the cutting) and other Wright Baker records

Item `uml-tpa-1-132-wright-baker`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** University of Manchester Library, Special Collections
- **Requested:** 7 Oct 2026 15:43 UTC (research/agent_review_2026-10-07/followup/F_outreach_sent.md row 2)
- **Asked for:** Whether the file holds or mentions photographs, negatives, drawings, measurements or reports of the cuts; Faculty of Science (GB 133 FSC) and UMIST records; any Allegro papers.
- **Status on 9 October 2026:** pending. No reply recorded by 9 Oct.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: Wright Baker's published account (BJRL 39.1, 1956, pp. 45–56) is already read in G_saw_gap_xii10.md. Statements in the file by the same author are the same lineage.

## What it bears on

- Open questions: R07, R11
- Active questions (ACTIVE_TEST): 1
- Entries: 60
- Reserved observation: yes

## Handling on arrival

Correspondence may be read by any worker. Any photograph, negative or drawing that shows text near segments 21/22 goes to the XII 10 protocol administrator unopened.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

Source: `discriminate.py` task `decisions-xii10`, read-only. Coverage factor c = 0.25: Only if the file holds photographs of segment 21/22 made before the cut (protocol line 45). Correspondence is the expected content.

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

No prediction from the other 28 chain models (no link of theirs uses this record): Tell es-Sultan (old Jericho); Kh. el-Marjama at ʿEin Samiya; Kh. Qumran; Qarn Sarṭaba (Alexandrium); Janoaḥ route (entry 60 reading שבינח); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; Tulul Abu el-'Alaiq; Kypros; Tell es-Samrat; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; unnamed WBADB unit S3961; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

No registry record uses this item.

### Closed results and their reopening criteria (ACTIVE_TEST)

- R11 Greek engraving order. Reopen for: engraving_order_results.json: labelled column reconstruction or archival mapping linking edition line ends to cut faces. Can this item satisfy it: **partly**. INFERENCE: a 1955–56 record of which text lies on which segment would be such a mapping for the cut side; it would not supply the Figure 4.6 component map named in ACTIVE_TEST. Outcome ids: `closed1:reopen-triggered`, `closed1:not-triggered`.

### Other registered predictions

**pred1. Saw-gap check (followup/G_saw_gap_xii10.md): Result 1: a whole letter cannot have been lost in the cut** (EVIDENCE for the 0.006 in figure (BJRL p. 50); thresholds from G's stated letter sizes.)

- Predicts: Any blade or kerf figure in the file agrees with 0.006 in (0.152 mm), and no record gives a kerf or edge loss at 21/22 of 1 mm or more.
- Confirm if: A recorded blade or kerf of 0.25 mm or less.
- Contradict if: A recorded kerf or edge loss at cut 21/22 of 1 mm or more (the size G says would be needed to lose a whole letter).
- Inconclusive if: Figures given for the saw in general but not for cut 21/22, or units unclear.
- Silent if: The file gives no saw or cut measurements.

**pred2. Edition placement of the 21/22 cut (W2A, as cited in G): Editions place cut 21/22 through the last letter of word 2 of XII 10** (EVIDENCE (editions, recorded in W2A). No letter identity is predicted. A diagram showing letters is routed to the administrator.)

- Predicts: A cutting record that marks cut positions places cut 21/22 within word 2 of XII 10, not between words.
- Confirm if: A written statement or diagram key places the cut in word 2.
- Contradict if: A record places cut 21/22 in another line position or between words. This questions the 21/22 target hypothesis, which the protocol already treats as a hypothesis.
- Inconclusive if: Cut positions are given by segment only.
- Silent if: No cut-position record.

### Families with no prediction

- Koḥlit chain models; entry 25; IV/17; rarity; closed Jericho and Siloam branches: No registered model uses cutting records.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `dec:finite-set-rejected:none`, `dec:finite-set-rejected:none:open-components`, `dec:one-sequence:R1`, `dec:one-sequence:R2`, `dec:one-sequence:R3`, `dec:one-sequence:R4`, `dec:one-sequence:R5`, `dec:one-sequence:R6`, `dec:one-sequence:R7`, `dec:partial-reading:R1`, `dec:partial-reading:R1+R2`, `dec:partial-reading:R1+R2+R3+R4+R5+R6`, `dec:partial-reading:R1+R2+R3+R4+R5+R6+R7`, `dec:partial-reading:R1+R2+R5+R6`, `dec:partial-reading:R1+R2+R5+R6+R7`, `dec:partial-reading:R1+R5+R6`, `dec:partial-reading:R2`, `dec:partial-reading:R2+R3+R4`, `dec:partial-reading:R2+R3+R4+R7`, `dec:partial-reading:R2+R7`, `dec:partial-reading:R3`, `dec:partial-reading:R3+R4`, `dec:partial-reading:R3+R7`, `dec:partial-reading:R4`, `dec:partial-reading:R4+R5`, `dec:partial-reading:R5`, `dec:partial-reading:R6`, `dec:partial-reading:R7`, `dec:reading-gate-fails`, `pred1:confirm`, `pred1:contradict`, `pred1:inconclusive`, `pred1:silent`, `pred2:confirm`, `pred2:contradict`, `pred2:inconclusive`, `pred2:silent`, `closed1:reopen-triggered`, `closed1:not-triggered`
