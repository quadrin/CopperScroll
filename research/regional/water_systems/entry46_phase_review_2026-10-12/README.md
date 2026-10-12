# Entry 46: pool-reading function and phase review

12 October 2026. This exploratory application of the [native edition audit](../../../sources/full_reads_2026-10-12/storage_language_audit/README.md) replaces neither the frozen water lane nor the earlier manual overlay. The assessed claim is conditional: a reported water receptacle satisfies entry 46 under a stated pool reading, place/radius, function and phase model. **Result: not identifiable from available evidence.** Some selected function/access/place subsets match, but dated usable configurations, ancient place association and numerical/directional joins remain missing.

## Reading and function branches

Puech 2015 pp. 55–56, 85, 87–88, 103 and Lefkovits 2000 pp. 331, 333, 394 were natively inspected in the linked audit. A physical bathing basin is compatible with the retained pool reading. Requiring water storage for withdrawal/service beyond immersion is a narrower operational sensitivity, not a verified lexical necessity. An inlet supplying a bath does not prove that the bath supplied other users.

Lefkovits's deep-pit alternative remains outside this water-only screen; it requires a separately specified inventory and cannot be rejected here. His distance/depth/ten-small-pits alternatives and inherited feet/notches branches also remain separate. Nothing in this review converts ten pits into a length or chooses one leg of a turning staircase as the ancient origin. `text/readings.json` and its atlas mirror now retain the native edition alternatives and correct the earlier claim that all editions read the reservoir word identically.

## Equal application and evidence levels

[evaluate.py](evaluate.py) rebuilds the committed phase-4 source view and requires identical `phase4_counts.csv` before deriving this review. It retains all in-box, nonsuperseded/nonduplicate source rows typed as reservoir/pool, cistern or basin/tank, and adds selected ritual-bath rows omitted by the earlier English pool/cistern keyword gate. Existing preferred-version, SWP, held, Almit and protected-strip exclusions apply. The same function/place/radius evaluator processes candidates and comparators.

- `reported_form_screen` is a date-free screen of reported water-form, reported entrance and distance. A type label supplies only this provisional form gate, not phase-specific water-use evidence. Basin/tank shape alone leaves water function unknown.
- `reported_window_screen` adds the source's reported period eligibility. Use/fill/typological association is explicitly separate from construction dating.
- `phase_join_screen` requires actual phase-attached function and entrance. Unreviewed source descriptions have UNKNOWN water function and contemporaneity even when their reported form passes.
- `stair_origin_screen` tests the particular original stair-origin model. Its failure does not reject every possible entrance.
- `full_pool_branch` adds dating of the retained usable configuration, ancient site association, leftward origin and the selected ten-measure/pits relation. Earlier construction with dated later use may qualify; initial cutting need not fall within the window. Unsupported joins remain UNKNOWN. Distance failures are conditional on the named anchor/radius; they do not exclude the region or another reading.

Full outputs are [phases.csv.gz](phases.csv.gz) and [scores.csv.gz](scores.csv.gz), with [counts.csv](counts.csv) and readable [audited_candidate_scores.csv](audited_candidate_scores.csv). They count source/phase descriptions, including unresolved physical duplicates and aggregates; they supply no landscape denominator or rarity estimate. Known candidates have received more native inspection than most comparators, so the phase-join counts cannot establish discrimination.

## Applied candidate consequences

The phase records in [phase_overrides.json](phase_overrides.json) are derived from the [native bath audit](../../../assessments/entry46_baths_2026-10-12/README.md), its coordinate envelopes and the [Rogem source-lineage check](../../../sources/full_reads_2026-10-12/source_lineage_audit/README.md).

- Armon L5's stepped bath passes the contained-water/place/access subset at 2 km from Ramat Rahel and fails that distance subset at 1 km. Its construction, W11 phase, Beth ha-Kerem association and leftward/numerical datum remain unresolved. The inlet does not establish separate storage/service use.
- Rogem retains the possible earlier collecting vat, tentative Early Roman stepped bath and later probable rainwater cistern separately. The bath passes the contained-water subset at 2 km from Ein Kerem, outside 1 km. Roman soil L114 lies **near** Cistern 2; WP3 and Cave 1 contexts do not date stair construction. Removal of the original stairs fails that stair-origin model in the later phase; another entrance and its date remain unknown.
- Ramat Sharet's typologically Second Temple bath passes the same 2 km Ein Kerem subset; construction-associated finds are absent. Its Mamluk cistern conversion is out of the relevant window and blocks the original stair passage. Medieval storage cannot supply the ancient bath's function or an open original entrance; other access remains unassessed.

All three ancient bath phases remain UNKNOWN under the storage/service requirement and for a full entry identification. The broadened class gate also admits previously omitted comparator bath descriptions; it is not a candidate-only rescue.

## Verification and next evidence

Run `python3 -I -B research/regional/water_systems/entry46_phase_review_2026-10-12/evaluate.py`, then `python3 -I -B research/regional/water_systems/entry46_phase_review_2026-10-12/test_review.py`. Snapshots rebuild deterministically; existing lane files stay byte-identical. [summary.json](summary.json) pins source inputs, governing rules and evaluator bytes. The regression checks cover unsupported label/phase promotion, alternate access, date transfer, separate function models and anchor/radius treatment.

Next: original Sion 2002 pp. 115–122 or the 1999 locus/section records for Rogem; stratified L5 access/W11/W1 contacts for Armon; an original bath-phase dating context at Ramat. A confirmatory identification further requires equally inspected controls and a registered, demonstrably unseen observation. This review's selected sources and alternatives are exposed exploratory evidence.

**Obtained** — a reproducible pool-reading function/phase screen and applied bath branches, with original-stair failures separated from unknown alternative access.
