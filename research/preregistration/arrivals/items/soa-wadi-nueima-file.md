# Wadi Nuʿeima inspection file behind ESI 5 pp. 110–111

Item `soa-wadi-nueima-file`. Registered 2026-10-09 by the arrival register. Exploratory; no identification or ledger count follows.

- **Holder:** Archaeology Unit, Staff Officer for Archaeology (Judea and Samaria)
- **Requested:** 6 Oct 2026 14:17:38 UTC (research/assessments/entry29_jericho_pools/wadi_en_nueima_original_2026-10-06.md (archive referral sent))
- **Asked for:** The inspection file, bath drawing and accession.
- **Status on 9 October 2026:** pending. No reply recorded by 9 Oct.
- **Arrived before registration:** nothing.
- **Exposure:** EVIDENCE: Dinur–Feig, ESI 5 pp. 110–111 is fully inspected: one miqva about 1.3 m deep about 2 m north of the wadi, and a separate western rectangle.
- **Exposure:** EVIDENCE: Sion 2002 p. 82 names this archive as the holder of the IV/17 permit L-656 file. The request did not ask for it.

## What it bears on

- Open questions: R07, R08, R09
- Active questions (ACTIVE_TEST): none
- Entries: 29
- Reserved observation: no

## Handling on arrival

Ordinary intake. Note any statement about the L-656 file's custody separately; it is custody information, not a test.

## Predictions by model family

Every outcome below has an id. Score an arrival only with these ids (see ARRIVAL_PROCEDURE.md).

### Decision classes (Koḥlit 10, XII 10 strings 7, Entry 25 6, closed branches 3)

Source: `discriminate.py` task `decisions-wadi-bath-contact`, read-only. Coverage factor c = 0.5: The request is for the inspection file; whether it holds a bath plan or section is unknown.

| Outcome id | Kind | Basis | Outcome | Excluded classes |
|---|---|---|---|---|
| `dec:dated-water-contact` | decisive | recorded | Individual bath and dated water contact are recorded | none |
| `dec:state-contact-miss` | decisive | recorded | Fixed feature-state/contact branch contradicted | entry29-wadi: entry29-wadi-c01 |
| `dec:identity-without-contact` | partial | recorded | Bath identity improves but contact remains unknown | none |
| `dec:file-lost-or-unobtained` | not_obtained | recorded | No usable file or target was not recorded | none |

Class legend:
- `entry29-wadi-c01` (entry29-wadi): branch: Entry 29: Wadi Nuʿeima bath state branch

What each class predicts for this item:
- `entry29-wadi-c01` (entry29-wadi): compatible decisive outcomes: `dec:dated-water-contact`. Excluded by: `dec:state-contact-miss`. Survives every other outcome, including silence.

### Koḥlit chain models (28, research/assessments/kohlit_chain/chain.json)

No prediction from the other 28 chain models (no link of theirs uses this record): Tell es-Sultan (old Jericho); Kh. el-Marjama at ʿEin Samiya; Kh. Qumran; Qarn Sarṭaba (Alexandrium); Janoaḥ route (entry 60 reading שבינח); Kh. Samiyye (ʿEin Samiya); Tell esh-Sheikh Dhiab; Tulul Abu el-'Alaiq; Kypros; Tell es-Samrat; el-Muntar; Naḥal Mikhmas; Tell Qa'un; Tananir; Kh. es-Saleh; Udala; Qarawet et-Tahta; Kh. Sara C; Kh. el-Khudriya; Tell Maryam; unnamed WBADB unit S2849; Kh. esh-Sheikh 'Antar; Ras el-'Eizariya; unnamed WBADB unit S3961; Kh. edh-Dhra'; unnamed WBADB unit S2096; unnamed WBADB unit S2594; unnamed WBADB unit S3072.

### Entry 60 registry v2 (W2B registry_v2_entry60.json)

No registry record uses this item.

### Closed results and their reopening criteria (ACTIVE_TEST)

- Jericho pools, entry 29 (Wadi Nuʿeima). Reopen for: A phase-controlled field section tying a water aperture to a named wall face and its contemporaneous floor. Can this item satisfy it: **yes**. If the file holds the bath drawing with contacts. Outcome ids: `closed1:reopen-triggered`, `closed1:not-triggered`.

### Other registered predictions

**pred1. Wadi named branch (decisions entry29-wadi-c01): The individually identified bath has a dated water aperture, wall and floor contact in one usable state** (EVIDENCE: plans.json outcomes.)

- Predicts: The file holds a bath plan or section with a water aperture tied to a wall and a contemporaneous floor.
- Confirm if: Outcome dated-water-contact.
- Contradict if: Outcome state-contact-miss.
- Inconclusive if: Outcome identity-without-contact.
- Silent if: Outcome file-lost-or-unobtained.

**pred2. Custody of the L-656 file: None (custody fact)** (INFERENCE.)

- Predicts: Silent on L-656: it was not requested.
- Confirm if: Not applicable.
- Contradict if: Not applicable.
- Inconclusive if: Not applicable.
- Silent if: Expected.

### Families with no prediction

- Koḥlit; XII 10; entry 25 classes; rarity: Unrelated record.

## Registered outcome ids

`item:silent`, `item:partial`, `item:unregistered-observation`, `dec:dated-water-contact`, `dec:state-contact-miss`, `dec:identity-without-contact`, `dec:file-lost-or-unobtained`, `pred1:confirm`, `pred1:contradict`, `pred1:inconclusive`, `pred1:silent`, `pred2:confirm`, `pred2:contradict`, `pred2:inconclusive`, `pred2:silent`, `closed1:reopen-triggered`, `closed1:not-triggered`
