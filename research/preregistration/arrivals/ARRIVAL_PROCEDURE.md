# What to do when a requested item arrives

Frozen with the register on 9 October 2026. It applies to every item in `items/`. Where an older protocol governs an item, this procedure points to it and adds nothing to it:
- XII 10 and the 21/22 cut: the frozen reading protocol, `research/agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md` (commit fd3f334).
- Records of the ground north of Tell es-Sultan: `research/assessments/kohlit_chain/registration_protocol.md`.
- Rarity units (Zertal vol. I, Kochavi 1972): the frozen Stage 2 protocol and `match.py` (b7a682b), following `research/rarity/kohlit/stage2/addendum_s2/PROCEDURE.md`.

## 1. Before anything is opened

1. Run `python3 -I research/preregistration/arrivals/arrival.py check`. It must print `manifest: ok`. If it fails, stop: the frozen files were changed.
2. Find the commit that first added `MANIFEST.md` on the remote, and its push time. Write both into the outcome record.
   - If that push came before the item arrived, the item is a test of the predictions in its file.
   - If not, the item is still scored, but every score is exploratory (`"test_status": "exploratory"`).
3. Record the intake before reading the content: who received it, when (UTC), from whom, and what came (identifiers, file names, sizes, SHA-256). Use `research/shared_tools/cli.py capture` where it fits. Note what was asked and what was not sent.
4. Check the item file's list "arrived before registration". Any part named there is exposed. Its scores are marked `"exposed": true` and test nothing.

## 2. Who opens it

- **Reserved items** (USC masters, Manchester Museum and Joan Taylor scans, ÉBAF X-rays and copy, any photograph, film or drawing of segment 21/22 or of XII 8–12 in any other item):
  - No agent opens, crops or views them.
  - A human administrator named by the project owner records frame lineage with the target masked, as the frozen protocol requires.
  - Two blinded human readers lock Stages 1 and 2. The integrator receives only the locked records and the administrator's lineage record.
  - If the owner views an original on site (for example the ÉBAF X-rays), he writes down what he saw and when. He then cannot serve as a blinded reader.
- **Tell es-Sultan records** (Garstang Museum, PEF, Nigro): one designated worker follows the registration protocol. Preview at 5 m per pixel or coarser first, mark the target strip, pick controls outside it, withhold the check point, and save the fit before opening the strip at full resolution.
- **All other items:** one designated worker (the reader) opens the item.

## 3. Extract first, compare second

1. **Extraction.** The reader extracts the facts without looking at the item file's predictions. Use the fields the existing record names: `record_needed` in `research/feature_workbench/decisions/plans.json`, the field records in `research/feature_workbench/coverage/volume_inputs.json`, or the chain link's `where`. Cite page, figure or frame for each fact. Keep observation, published reconstruction, excavator label and inference separate (EVIDENCE / INFERENCE / TRADITION / CLAIM).
2. **Comparison.** A second person (the comparer; normally the integrator) opens the frozen item file and assigns outcomes. If one person must do both steps, record that in the outcome record.
3. For each prediction in the item file, choose exactly one registered outcome id:
   - `…:confirm` or `dec:<row>` when the stated criterion is met, with the evidence cited;
   - `…:contradict` only for a two-sided or absence-statement link whose contradiction criterion is met;
   - `…:inconclusive` when the item covers the place or relation but meets neither criterion;
   - `…:silent` when the item does not cover the place or relation.
4. **Silence is never a FAIL.** A silent item excludes nothing. An undated feature is unknown, not absent.
5. A decision row (`dec:…`) is the row whose components match what the item shows. Only one row per item.
6. Anything seen outside the registered outcomes is scored `item:unregistered-observation` and described verbatim. It starts a separate exploratory specification. It tests nothing in this register.

## 4. Partial items and inconclusive results

- **Partial arrival.** Score only the parts received. Add `item:partial` and list `parts_pending`. The pending parts keep their frozen predictions. A later part is scored against the same frozen file in a new outcome record.
- **Several copies of one observation.** The USC, Manchester Museum and Joan Taylor items, and the IAA records with the supplied ʿAtiqot 41 cave entries, may show the same exposures. The first copy opened is the observation. Later copies are recorded as the same lineage and add no second observation.
- **Inconclusive.** Record `…:inconclusive` with the reason (resolution, missing datum, undated, unregistrable, gate failed). An inconclusive result is a result. It is reported like any other.
- **Not obtained.** A refusal or a lost file is recorded as the item's `not_obtained` row where one exists (for example `dec:file-unavailable`), otherwise as `item:silent` with a note.

## 5. Recording

1. Write `outcomes/<item-id>_<YYYY-MM-DD>.json` in this folder (format below).
2. Run `python3 -I research/preregistration/arrivals/arrival.py validate outcomes/<file>.json`. It must print `record: valid`.
3. The integrator commits the record. Nobody edits `items/`, `register.json` or `RANKING.md` after an arrival. A changed prediction goes into a new file as a new exploratory model and cites the old one.

```json
{
 "item_id": "kochavi-1972",
 "register_commit": "<commit that first added MANIFEST.md>",
 "register_pushed_before_arrival": true,
 "arrived_utc": "2026-11-02T18:00:00Z",
 "opened_by": "<reader>",
 "compared_by": "<comparer>",
 "manifest_check": "pass",
 "parts_received": ["Kallai pp. 172–173"],
 "parts_pending": [],
 "intake": {"files": [{"name": "...", "sha256": "...", "bytes": 0}], "notes": "..."},
 "scores": [
  {"outcome_id": "dec:identity-only:east+undated", "evidence": "Kallai p. 173, site 66", "exposed": false},
  {"outcome_id": "chain:S2376-1-pool-east:silent", "evidence": "", "exposed": false}
 ],
 "unregistered_observations": [],
 "notes": ""
}
```

## 6. Reporting

- Report every outcome, whatever it is: confirmations, contradictions, inconclusive results and silence.
- Write the item's result into the existing evidence record it bears on and into the "Last session" line of ACTIVE_TEST (integrator).
- A contradiction removes only the classes or branches its row or link names. Other sites and readings are untouched.
- A confirmation is not an identification. AGENTS.md requires discrimination against registered alternatives plus an unseen prediction. Locating an opening does not date it.
- Reopening a closed result means re-evaluating it under its own rules. The previous result is preserved.
