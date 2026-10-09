# Methods round, 8 October 2026

The project owner asked for nine method extensions to run in parallel. They follow four case studies: Ephesus (successive reference points), Linear B (one assignment must explain every occurrence), Richard III (staged localization and a separate identity test) and AF447 (model what an unsuccessful search tested).

Nine workers built them at the same time. Each worker owned one folder. The integrator owned shared files and Git. All work is exploratory. No registered result changed. No identification, deposit or outcome-ledger count was added.

## What was built

| Tool | Folder | Main result |
|---|---|---|
| Feature-level audit of the Koḥlit positives | [rarity/kohlit/feature_audit](../rarity/kohlit/feature_audit/README.md) | Both coders give MATCH on 41 unit-conditions. 40 rest on a shared physical feature. The exception is Qarn Sarṭaba (S1283) C2: coder A's SWP cave-cisterns, coder B's Zertal robbing pits. Of 26 units with two or more matched conditions, 3 are jointly compatible (Qumran E754, S2430, S3961; coder A only), 22 are conditionally compatible (each needs an undated feature to exist in the window), and 1 is not shown compatible (Tananir E99: its pit went out of use before the window). Tell es-Sultan's tomb-shaft match uses one burial cave as both pit and graves. |
| Observation-process audit | [rarity/kohlit/observation_process](../rarity/kohlit/observation_process/README.md) | 61 of 63 absence statements are Zertal's "Cisterns: none". It counts cistern openings in the site record. No statement gives a search radius. A site record covers at most 1.1% of the 1 km northern sector (median 0.1%). If an absence counts only within its scope, f = 0 in every row: headline 0/0/333 instead of 0/20/313. Zertal's own volumes record cisterns in the sector for two pre-70 FAIL units (S695, S1296) and possibly a third (S386). |
| Landmark chain (Ephesus) | [assessments/kohlit_chain](../assessments/kohlit_chain/README.md) | 28 Koḥlit models, each with its next unused relation and a specific prediction. Only 11 of 28 next links can contradict a model outright. The requested pre-camp records for Tell es-Sultan can confirm but not contradict, and cannot date an opening. A registration protocol with a withheld check point is ready for those records. |
| Recurring location language (Linear B) | [text/location_language](../text/location_language/README.md) | 56 expressions, 272 occurrences (249 explicit, 12 restored, 11 proposed). The project's own records use על פי ("above" or "at its mouth"), עד ("toward" or "as far as"), שולי ("outlet" or "edge") and ha-Melaḥ (four referents) inconsistently. A choice of meaning for יגר, Achor, Sekakah, שולי, Koḥlit, על פי or עד changes the most records. |
| Discriminating observations (decision queue) | [feature_workbench/decisions](../feature_workbench/decisions/README.md) | 28 surviving Koḥlit models collapse to 10 classes; 288 entry-25 branches to 6. No record guarantees separation, because each can return an inconclusive result. Counting decisive outcomes only, the smallest separating set is XII 10, Kallai and Kenyon; each is necessary. Rank: XII 10, Kenyon, Kallai, IV/17. Manuscript reading comes before construction contact and entrance bearing; the ancient threshold separates nothing. |
| Coverage: footprint against target volume (AF447) | [feature_workbench/coverage](../feature_workbench/coverage/README.md) | IV/17: 8 of 8 target branches are undeterminable, so the chamber-centre excavation does not establish coverage of the northern-threshold target. The L-656 field file (north-mouth plan, threshold section and levels, level and basket registers, locus list) would resolve them. Tell es-Sultan: 4 of 4 joins undeterminable, because entry 60 gives no distance. |
| Recovery benchmark: harness and development batch (Richard III) | [benchmarks/recovery](../benchmarks/recovery/README.md) | 12 development cases from five open-access HA-ESI survey reports. The procedure selects correctly in 10 of 12, with 5 correct abstentions. The two errors are real failure modes: a rival that fits when the true feature is missing, and words that disagree with the map. This batch is not an independent test. |
| Recovery benchmark: reserved batch | [benchmarks/recovery/reserved](../benchmarks/recovery/reserved/MANIFEST.md) | 11 sealed cases, prepared by a separate worker that did not see the harness. The key is outside the repository; its SHA-256 is in the manifest. Run once, after the harness is frozen, and report the result whatever it is. |
| Letter-reading controls | [text/letter_controls](../text/letter_controls/PROTOCOL.md) | A calibration design for the frozen XII 10 protocol, without changing it: 326 candidate control letters and 19 decoys from columns I–X. It cannot run yet: no image in the repository can serve as a control image, and no readers are assigned. |

## Integration

- Every suite passes: 253 tests. The feature workbench was rebuilt (`build.py`, `check.py`), and the atlas site was rebuilt with the new workbench snapshot.
- Sealed keys (reserved recovery batch; letter controls) are not in the repository. The project owner holds a copy outside it.

## Proposed but not made

These need an editorial decision:
- `text/readings.json`: global records for על פי and עד; a note on e4-immersion.
- Atlas entry 6: its place and that of entries 13–14 assume different referents for ha-Melaḥ. Atlas entry 32: the same words read "at" at XII 11.
- Registry (wave 1): P46-A says Milik 1962 reads cubits at X 6, but he reads feet; P35-C assumes a cairn, but Eshel's proposal is a dam.
- Recovery schema: optional `position.kind`, `position.direction` and `position.precision_m`.
- USC or Manchester: ask for control frames (cuts 1–6, 9–10, 13–14, 17–18) together with the XII 10 frames. This is new correspondence and needs the owner's approval.
