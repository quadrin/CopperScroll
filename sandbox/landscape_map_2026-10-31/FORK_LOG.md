# Run 26 fork log

Changes after the rule commit (04a25f4), in order. Each entry: time, what changed, why, and which test block judged it.

## 0. Original model on test block 1 (seeds 1001–2000), 31 Oct 16:08 UTC

Code commit 3cb050e (dev seeds 1–200 only had been run). Result file `out/benchA_test1.csv`.

| Region | 50 % set coverage | 90 % set coverage | mean log10 BF (95 % CI) |
|---|---|---|---|
| R0 | 0.291 | 0.802 | 0.571 (0.505–0.636) |
| R1 | 0.343 | 0.829 | 0.577 (0.512–0.642) |

**G1 fails** (needs 0.42–0.58 and 0.85–0.95). **G2 passes.** The scroll is not scored with this model.

## 1. Revision 1, logged 31 Oct 16:16 UTC, before it was run on any test seed

**Diagnosis (dev seeds 1–200, `scripts/diag.py`).**
- Posterior mass on cells where a clue's class is recorded: 0.636. Truth in such a cell: 0.64. Calibrated on average, but it does not follow c_true (0.64 at c_true 0.2–0.4, where the truth is in such a cell only 0.41 of the time). One entry cannot learn c.
- Posterior mass on "site" cells (other-class records present): 0.717. Truth at a site: 0.38. Among matched cells: sites hold 0.494 of the mass but 0.20 of the truths; non-sites hold 0.143 but 0.44. The ρ grid {0.5, 0.7, 0.9} does not cover the benchmark world, and one entry cannot learn ρ either.

**Change.**
1. ρ grid widened to {0.1, 0.2, …, 0.9}.
2. (c, ρ) are learned jointly from all entries of one scroll: the posterior over the 81 pairs is proportional to the product of the entries' marginal likelihoods. Given the pair, entries are scored independently as before. This matches the real case: one scroll, one inventory, shared recording rates.
3. Benchmark A unit: a fake scroll is 50 consecutive seeds, so the same number of scored entries as the real scroll. **The fake-entry generator is unchanged**, including c_true drawn per entry. R0 and R1 are pooled separately.

Nothing else changes: cells, records, clues, strata, smoothing, likelihood, region weights, metrics and gate thresholds are as in RULE.md.

**Judged on:** test block 2, seeds 2001–3000 (20 fake scrolls).

### 1a. Amendment to revision 1, logged 31 Oct 16:24 UTC, before any test seed

**Found on dev seeds 1–200 (`out/benchA_dev_v1.csv`).** Revision 1 gives R0 coverage 0.514 (50 %) and 0.931 (90 %), inside G1. R1 gives 0.682 and 0.978, which is *under*confident. Cause: benchmark A hands R1 the true zone every time, while R1 assumes the named zone is right with probability 0.8. The 0.2 of mass outside the zone is always wasted. That was a flaw in the benchmark as written in RULE.md; under the original model it was hidden by the over-weighted site prior.

**Change (benchmark only, R1 only).** The zone handed to R1 is the true zone with probability 0.8. Otherwise it is drawn from the other zones in proportion to the zone shares. This makes the benchmark match the stated reliability of R1. The scorer, R0, the fake-entry generator and the gate thresholds do not change.

**Judged on:** test block 2, seeds 2001–3000, as for revision 1.
