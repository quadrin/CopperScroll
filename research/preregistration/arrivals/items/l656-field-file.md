# Michael Dadon's IV/17 excavation file, permit L-656: plan with the north mouth, threshold section and levels, level and basket registers (656.17, 656.20), locus list, method notes

Item `l656-field-file`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** Archive of the Archaeology Staff Officer for Judea and Samaria (named in Sion 2002 p. 82); present holding unverified
- **Requested:** Not requested (the 7 Oct IAA request is related only) (research/feature_workbench/coverage/README.md; decisions plans.json (decisions-iv17-l656))
- **Asked for:** See coverage/volume_inputs.json field records.
- **Status on 9 October 2026:** not_obtained. No specific request sent.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: Sion 2002 pp. 61–64 and Plan 5 are inspected; survey coins 60/61 and basket numbers are published without contacts.

## What it bears on

- Open questions: R02, R08, R09
- Active questions (ACTIVE_TEST): none
- Entries: 25
- Reserved observation: no

## Handling on arrival

Ordinary intake. Before reading threshold levels or wall contacts, freeze the Entry 25 branches and an aspect rule (decisions README).

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

Source: `discriminate.py` task `decisions-iv17-l656`, read-only. Coverage factor c = 1.0: The file is the named record. Rows needing a mouth bearing are replaced by 'bearing undetermined' rows (RANKING_PLAN).

| Outcome id | Kind | Basis | Outcome | Excluded classes |
|---|---|---|---|---|
| `dec:dated-state:established+undetermined` | partial | recorded | mouths, pillar and wall coexist in a declared ancient phase; individual-mouth aspect undetermined | none |
| `dec:state-conflict:arrangement-later+undetermined` | partial | recorded | two-mouth arrangement absent or inaccessible in the ancient phase; individual-mouth aspect undetermined | entry25: e25-c02, e25-c04, e25-c05, e25-c06 |
| `dec:state-conflict:pillar-later+undetermined` | partial | derived | only the pillar postdates the ancient phase; individual-mouth aspect undetermined | entry25: e25-c02, e25-c04 |
| `dec:partial-file:undated+undetermined` | partial | recorded | no sealed wall, mouth or threshold contact; individual-mouth aspect undetermined | none |
| `dec:file-unavailable` | not_obtained | recorded | Specific L-656 record unavailable or not identified | none |

Class legend:
- `e25-c01` (entry25): candidate: iv11 / iv17 / twin; reading: pillar / terrace; orientation: both-mouths / cave; unit: 0.40 / 0.50 / 0.60; direction: horizontal / vertical; phase: ancient / reported; deposit: below-book / below-jar
- `e25-c02` (entry25): candidate: iv17; reading: pillar; orientation: both-mouths; unit: 0.40 / 0.50 / 0.60; direction: horizontal / vertical; phase: ancient; deposit: below-book / below-jar
- `e25-c03` (entry25): candidate: iv17; reading: pillar / terrace; orientation: both-mouths; unit: 0.40 / 0.50 / 0.60; direction: horizontal / vertical; phase: reported; deposit: below-book / below-jar
- `e25-c04` (entry25): candidate: iv17; reading: pillar; orientation: cave; unit: 0.40 / 0.50 / 0.60; direction: horizontal / vertical; phase: ancient; deposit: below-book / below-jar
- `e25-c05` (entry25): candidate: iv17; reading: terrace; orientation: both-mouths; unit: 0.40 / 0.50 / 0.60; direction: horizontal / vertical; phase: ancient; deposit: below-book / below-jar
- `e25-c06` (entry25): candidate: iv17; reading: terrace; orientation: cave; unit: 0.40 / 0.50 / 0.60; direction: horizontal / vertical; phase: ancient; deposit: below-book / below-jar

What each class predicts for this item:
- `e25-c01` (entry25): no prediction about this item. It survives every registered outcome.
- `e25-c02` (entry25): compatible decisive outcomes: none. Excluded by: `dec:state-conflict:arrangement-later+undetermined`, `dec:state-conflict:pillar-later+undetermined`. Survives every other outcome, including silence.
- `e25-c03` (entry25): no prediction about this item. It survives every registered outcome.
- `e25-c04` (entry25): compatible decisive outcomes: none. Excluded by: `dec:state-conflict:arrangement-later+undetermined`, `dec:state-conflict:pillar-later+undetermined`. Survives every other outcome, including silence.
- `e25-c05` (entry25): compatible decisive outcomes: none. Excluded by: `dec:state-conflict:arrangement-later+undetermined`. Survives every other outcome, including silence.
- `e25-c06` (entry25): compatible decisive outcomes: none. Excluded by: `dec:state-conflict:arrangement-later+undetermined`. Survives every other outcome, including silence.

### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)

No prediction from the other 28 chain models (no link of theirs uses this record): Tell es-Sultan (old Jericho); Kh. el-Marjama at ʿEin Samiya; Kh. Qumran; Qarn Sarṭaba (Alexandrium); Janoaḥ route (entry 60 reading שבינח); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; Tulul Abu el-'Alaiq; Kypros; Tell es-Samrat; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; unnamed WBADB unit S3961; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

No registry record uses this item.

### Coverage joins (feature_workbench/coverage)

- `coverage-volume-iv17`: 8 joins, now undeterminable. Prediction: With the file alone, all 8 joins stay undeterminable. The file can supply cut outlines, levels, datum and the threshold surface, but every branch also needs a model declaration no record can supply: the target-zone outline (vertical branches) or origin point, sector and depth band (horizontal branches), plus a radial tolerance for single-cubit branches. Proposal: declare these before the file arrives. Outcome ids: `cov:coverage-volume-iv17:as-predicted`, `…:not-as-predicted`.

### Closed results and their reopening criteria (ACTIVE_TEST)

None.

### Families with no prediction

- Koḥlit; XII 10; rarity; closed tests: Unrelated.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `dec:dated-state:established+undetermined`, `dec:state-conflict:arrangement-later+undetermined`, `dec:state-conflict:pillar-later+undetermined`, `dec:partial-file:undated+undetermined`, `dec:file-unavailable`, `cov:coverage-volume-iv17:as-predicted`, `cov:coverage-volume-iv17:not-as-predicted`
