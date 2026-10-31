# Run 26 fork log

Changes after the rule commit (04a25f4), in order. Each entry: time, what changed, why, and which test block judged it.

Correction (16:11 UTC): the clock times first written for entries 1 and 1a (16:16, 16:24) were estimates and were later than the real times. The commit timestamps are the record.

## 0. Original model on test block 1 (seeds 1001–2000), run 31 Oct about 16:08 UTC

Code commit 3cb050e (dev seeds 1–200 only had been run). Result file `out/benchA_test1.csv`.

| Region | 50 % set coverage | 90 % set coverage | mean log10 BF (95 % CI) |
|---|---|---|---|
| R0 | 0.291 | 0.802 | 0.571 (0.505–0.636) |
| R1 | 0.343 | 0.829 | 0.577 (0.512–0.642) |

**G1 fails** (needs 0.42–0.58 and 0.85–0.95). **G2 passes.** The scroll is not scored with this model.

## 1. Revision 1, logged before it was run on any test seed (verifiable time: commit 4a62fc6, 16:10:19 UTC)

**Diagnosis (dev seeds 1–200, `scripts/diag.py`).**
- Posterior mass on cells where a clue's class is recorded: 0.636. Truth in such a cell: 0.64. Calibrated on average, but it does not follow c_true (0.64 at c_true 0.2–0.4, where the truth is in such a cell only 0.41 of the time). One entry cannot learn c.
- Posterior mass on "site" cells (other-class records present): 0.717. Truth at a site: 0.38. Among matched cells: sites hold 0.494 of the mass but 0.20 of the truths; non-sites hold 0.143 but 0.44. The ρ grid {0.5, 0.7, 0.9} does not cover the benchmark world, and one entry cannot learn ρ either.

**Change.**
1. ρ grid widened to {0.1, 0.2, …, 0.9}.
2. (c, ρ) are learned jointly from all entries of one scroll: the posterior over the 81 pairs is proportional to the product of the entries' marginal likelihoods. Given the pair, entries are scored independently as before. This matches the real case: one scroll, one inventory, shared recording rates.
3. Benchmark A unit: a fake scroll is 50 consecutive seeds, so the same number of scored entries as the real scroll. **The fake-entry generator is unchanged**, including c_true drawn per entry. R0 and R1 are pooled separately.

Nothing else changes: cells, records, clues, strata, smoothing, likelihood, region weights, metrics and gate thresholds are as in RULE.md.

**Judged on:** test block 2, seeds 2001–3000 (20 fake scrolls).

### 1a. Amendment to revision 1, logged before any test seed (verifiable time: commit 4a62fc6, 16:10:19 UTC)

**Found on dev seeds 1–200 (`out/benchA_dev_v1.csv`).** Revision 1 gives R0 coverage 0.514 (50 %) and 0.931 (90 %), inside G1. R1 gives 0.682 and 0.978, which is *under*confident. Cause: benchmark A hands R1 the true zone every time, while R1 assumes the named zone is right with probability 0.8. The 0.2 of mass outside the zone is always wasted. That was a flaw in the benchmark as written in RULE.md; under the original model it was hidden by the over-weighted site prior.

**Change (benchmark only, R1 only).** The zone handed to R1 is the true zone with probability 0.8. Otherwise it is drawn from the other zones in proportion to the zone shares. This makes the benchmark match the stated reliability of R1. The scorer, R0, the fake-entry generator and the gate thresholds do not change.

**Judged on:** test block 2, seeds 2001–3000, as for revision 1.

## 2. Revision 1 + 1a on test block 2 (seeds 2001–3000), 31 Oct 16:10–16:11 UTC

Result file `out/benchA_test2.csv`, code at 4a62fc6.

| Region | 50 % set coverage | 90 % set coverage | mean log10 BF (95 % CI) |
|---|---|---|---|
| R0 | 0.446 | 0.897 | 0.546 (0.490–0.604) |
| R1 | 0.526 | 0.907 | 0.536 (0.482–0.591) |

**G1 passes** for both regions. **G2 passes.** Revision 1 + 1a is the model that scores the scroll. No further revision.

## 3. Benchmark B and a flaw in revision 1, logged 31 Oct about 16:20 UTC; the scroll has not been scored

**Benchmark B under revision 1** (`out/benchB_v1.csv`; 56 one-clue entries from the 1940s 1:20,000 maps in 9 windows): 50 % / 90 % set coverage 0.171 / 0.642 (R0) and 0.125 / 0.393 (R1); mean log10 BF −0.060 (−0.183 to 0.101) and −0.183 (−0.327 to −0.002). Below the 0.80 label threshold, and the evidence points slightly away from the truth. (Under the original model, for reference: `out/benchB_v0_original_model.csv`, 90 % coverage 0.592 / 0.626.)

**Why (`out/benchB_record_distances.csv`).** The map positions are good (position error 21–79 m, median 51 m). But only 15 of 56 mapped features (0.27) have a modern record of their class in the same cell; 0.36 within 300 m; 0.52 within 1 km; median distance to the nearest same-class record 641 m. Caves: 0.17 in the cell, 0.28 within 1 km. These windows surround candidate places, the best-studied ground, so coverage elsewhere is probably lower. Revision 1 learned c ≈ 0.53 (R0) and 0.69 (R1) from these items.

**Flaw in revision 1 (documented analytical error).** An entry's marginal likelihood Σ_u prior(u) LR_u uses no information about where its own truth is; it measures the whole inventory. In benchmark A each fake entry had its own independently thinned copy of the inventory, so the product over 50 entries combined 50 different datasets. In benchmark B, and in the real scroll, every entry sees the same single inventory, so the product counts the same data 50 times. Revision 1's calibration in A therefore does not carry over to the real case, and B confirms it.

**Decision.** Revision 1 does not score the scroll. One revision remains under the rule; whether to use it is the owner's call.
