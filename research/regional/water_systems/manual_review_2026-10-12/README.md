# Corrected exploratory water shortlist

The existing manual checks change several older counts, but **the 14 not-confirmed phase-4 clause hits remove no date-eligible complete matches**. Their apparent complete entry-46 matches were already excluded by their dates. The actual Armon ha-Naẓiv stepped pool L5 is row `#142`; the unsupported tunnel-entrance hit is a different reservoir row, `#141`.

This overlay repairs evidence attribution in the existing coding. It does not independently identify a landmark, date a construction phase, or test a deposit. The identification claims remain **not identifiable from available evidence**. The [specification](PLAN.md) records exposure and correction rules; earlier outputs remain byte-identical.

## What changes

The primary overlay uses confirmed clauses, assigns UNKNOWN to unconfirmed or partly-confirmed support, and assigns FAIL only to the explicitly contradictory plans/lining recorded in [decisions.csv](decisions.csv). Every operation retains the original verdict and reason in [correction_audit.csv](correction_audit.csv). Missing evidence is not physical rejection.

For merged units under the main date rule, numbers below are match / fail / unknown:

| Entry and branch | Original phase-4 view | Existing-check overlay | Reason |
|---|---:|---:|---|
| 21, head recorded, S-open / N-side | 12 / 190 / 381 | 11 / 190 / 382 | ASI 108/2/69 names a monastery water source, not the conduit head |
| 21, built marker north of head, S-any / N-side | 1 / 194 / 388 | 0 / 194 / 389 | ASI 109/4/16 describes the aqueduct's northern wadi bank, not the marker's side |
| 21, pool north of head, S-pool / N-side | 1 / 194 / 388 | 0 / 194 / 389 | Same unsupported north relation |
| 29, reservoirs, Q-any | 0 / 142 / 252 | 0 / 143 / 251 | Existing review explicitly records an L-shaped pool, contradicting four sides |
| 45, open cistern / any wadi | 3 / 192 / 792 | 2 / 192 / 793 | ASI 102/447's “from N.” means north; it supplies no wadi connection |
| 46, reservoirs with a way in, B-any | 39 / 91 / 264 | 38 / 91 / 265 | HA-ESI 24896's stepped seats belong to a different pool |
| 46, reservoirs + cisterns with a way in, B-any | 64 / 282 / 1035 | 61 / 282 / 1038 | The preceding error, a pillar-supporting step at HA-ESI 25163, and unresolved conversion phase at Mount Scopus |

The dated-only entry-32 built-outlet / Qelt / no-wall count falls from 5 to 3. The removed date support at ASI 109/4/16 belongs to the destination palaces; its aqueduct and outlet remain undated possibilities. Main-rule count remains 5 because that rule admits undated structures. Dated-only entry-21 heads similarly fall from 8 to 7. Date-rule failures are eligibility failures, not archaeological contradictions.

The six partly-confirmed phase-4 checks cause one date-eligible complete match to become unknown: the Mount Scopus south-slope cistern/miqveh conversion, ʿAtiqot 63 pp. 27–43, row `#74`, entry 46 `res+cis|B-any`. The staircase belongs to the miqveh conversion rather than the original cistern phase. [retain_partial_counts.csv](retain_partial_counts.csv) preserves its original support as an optimistic sensitivity. [phase4_unconfirmed_only_counts.csv](phase4_unconfirmed_only_counts.csv) isolates the 14 not-confirmed checks from all older checks and partial cases.

## Surviving leads

The [source-linked shortlist](SHORTLIST.md) and [full branch table](surviving_leads.csv) record verified clauses, missing fields and rejection/discrimination observations. The three new entry-46 bath leads remain in the older-ledger overlay: Armon L5 at Ramat Raḥel 2 km, Rogem Gannim and Ramat Sharet at ʿEin Kerem 2 km. None gains identification support here. The parallel native-source bath audit must separate their phase/type claims; the Lower Herodium audit supersedes its historical near miss under the source-complex northernmost reading.

## Limits and reproducibility

The primary overlay keeps all existing place-constrained entry-46 counts: Ramat Raḥel 1 km has no complete match; Ramat Raḥel 2 km has two reservoir matches; ʿEin Kerem 1 km has one reservoir/two +cistern matches; ʿEin Kerem 2 km has one reservoir/four +cistern matches. These are the earlier extraction's counts, not a phase-specific native-plan recoding. In particular, the parallel bath audit's construction/phase and coordinate findings can justify another documented exploratory correction.

Unknown-heavy records, unlocated installations, aggregated rows, broad date labels and unresolved source identities continue to limit discrimination. A confirmed ledger item can confirm the earlier coded text rather than inspection of its original PDF. “Other MATCH clauses” in the CSV explicitly distinguishes those inherited codes from manual-check confirmations. No unreported original-source verification is implied.

Outputs:

- [all_view_counts.csv](all_view_counts.csv): cumulative verified, partial-retained, phase-4-only, not-confirmed-only, duplicate-bracket and quote-only count tables.
- [verified_clause_counts.csv](verified_clause_counts.csv): clause match/fail/unknown counts for all entry, branch, lineage and date combinations.
- [verified_merged_scores.csv](verified_merged_scores.csv): merged clauses, overall codes and dates after the overlay.
- [merged_match_changes.csv](merged_match_changes.csv): only changed complete-branch/date codes, with phase-4-only and cumulative effects separated.
- [summary.json](summary.json): input and implementation hashes, inspection scope and preservation check.

Run from the repository root:

```sh
python3 -I research/regional/water_systems/manual_review_2026-10-12/rebuild.py
python3 -I -m unittest discover -s research/regional/water_systems/manual_review_2026-10-12 -p test_review.py -v
```

Seven tests pass: unconfirmed-versus-contradictory evidence, partly-confirmed sensitivity and marker reading, derived head/outlet and date correction, superseded-row protection, byte-identical reconstruction, the 14-hit effect on date-eligible complete matches, and source-linked shortlist/count invariants. The rebuild first reproduces the original phase-4 counts and then checks that existing lane files stayed byte-identical.

**Obtained:** a reproducible correction of the existing water-clause checks and a source-linked surviving-lead/follow-up list. The analytical error is resolved for this fixed input; later native-source findings require a separate documented overlay.
