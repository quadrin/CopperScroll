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

(Superseded by entry 3: revision 1 did not score the scroll.)

## 3. Benchmark B and a flaw in revision 1, logged 31 Oct 16:13 UTC (commit f32e8ec); the scroll has not been scored

**Benchmark B under revision 1** (`out/benchB_v1.csv`; 56 one-clue entries from the 1940s 1:20,000 maps in 9 windows): 50 % / 90 % set coverage 0.171 / 0.642 (R0) and 0.125 / 0.393 (R1); mean log10 BF −0.060 (−0.183 to 0.101) and −0.183 (−0.327 to −0.002). Below the 0.80 label threshold, and the evidence points slightly away from the truth. (Under the original model, for reference: `out/benchB_v0_original_model.csv`, 90 % coverage 0.592 / 0.626.)

**Why (`out/benchB_record_distances.csv`).** The map positions are good (position error 21–79 m, median 51 m). But only 15 of 56 mapped features (0.27) have a modern record of their class in the same cell; 0.36 within 300 m; 0.52 within 1 km; median distance to the nearest same-class record 641 m. Caves: 0.17 in the cell, 0.28 within 1 km. These windows surround candidate places, the best-studied ground, so coverage elsewhere is probably lower. Revision 1 learned c ≈ 0.53 (R0) and 0.69 (R1) from these items.

**Flaw in revision 1 (documented analytical error).** An entry's marginal likelihood Σ_u prior(u) LR_u uses no information about where its own truth is; it measures the whole inventory. In benchmark A each fake entry had its own independently thinned copy of the inventory, so the product over 50 entries combined 50 different datasets. In benchmark B, and in the real scroll, every entry sees the same single inventory, so the product counts the same data 50 times. Revision 1's calibration in A therefore does not carry over to the real case, and B confirms it.

**Decision.** Revision 1 does not score the scroll. One revision remains under the rule; whether to use it is the owner's call.

## 4. Revision 2 (the last one the rule allows), owner's instruction "go ahead", 31 Oct 16:16 UTC; logged before any test seed

**Principle.** The recording rate c comes from the independent check (benchmark B), not from the scroll's own inventory. There is no pooling across entries.

**Scorer.**
1. The prior over c is the likelihood of the B items on the c grid, normalised:
   L(c) = Π_i [1 − (1 − c)(1 − b_i)]^{y_i} · [(1 − c)(1 − b_i)]^{1 − y_i},
   where y_i = 1 if the item's cell has a record of its class, and b_i = P_bg(match | stratum of the item's cell), from the full inventory.
2. ρ ∈ {0.1, 0.2, …, 0.9}, uniform: we do not know how often the scroll's places lie at recorded sites.
3. Each entry's posterior over (ρ, c) is that prior times its own marginal likelihood, as in RULE.md. There is no product across entries.
4. For the scroll: the c prior uses all 56 B items.

**Benchmark A (world set to the measured rate).**
- Thinning is by cell and class: all records of one class in one cell are kept or dropped together, with probability c_true. This matches what B measures (presence of the class in the cell).
- c_true for each fake entry is drawn from the 56-item c prior on the grid, plus a uniform jitter of ±0.05. The rest of the generator, amendment 1a and the gate thresholds are unchanged. The scorer's c prior in A uses all 56 B items.

**Benchmark B (label check), two-fold cross-fit by window.** The windows in alphabetical order alternate between folds:
- fold 1: B_buqeia, B_marsaba, K_palaces, S_samiya, W_choziba (24 items);
- fold 2: B_hyrcania, J_kidron, Q_qumran, T_jericho (32 items).

Each fold's items are scored with the c prior from the other fold. Coverage is reported on all 56. Exposure: the per-window results of revision 1 had been seen. The split is fixed by alphabetical order, not chosen.

**Judged on:** test block 3, seeds 3001–4000 (gate G1, G2), and the B cross-fit (label). If the gate fails, the run stops without scoring the scroll.

## 5. Revision 2 on test block 3 (seeds 3001–4000) and the B cross-fit, 31 Oct 16:18–16:21 UTC

Code: `scripts/bench_v2.py` and the revision-2 functions in `scripts/model.py`. The c prior from all 56 items has mean 0.116 (`out/c_prior_v2.json`). Fold 1 has 2 of 24 items matched (prior mean 0.111); fold 2 has 13 of 32 (prior mean 0.210).

| | 50 % set coverage | 90 % set coverage | mean log10 BF (95 % CI) |
|---|---|---|---|
| A, R0 | 0.147 | 0.822 | 0.142 (0.107–0.181) |
| A, R1 | 0.171 | 0.809 | 0.147 (0.112–0.186) |
| B cross-fit, R0 | 0.340 | 0.861 | 0.028 (−0.046–0.144) |
| B cross-fit, R1 | 0.393 | 0.965 | 0.025 (−0.049–0.140) |

**G1 fails. G2 passes** (the evidence is barely informative). B's 90 % coverage clears its 0.80 label, but the gate has failed. The cause, from `out/benchA_test3.csv`: only 12 % of the truths keep any other-class record after thinning at the measured rate, while the uniform ρ prior gives about half its mass to such cells. Under R0, 50 % coverage is 0.041 for truths not at a site and 0.918 for truths at a site.

**The rule's revisions are exhausted. The run stops; the scroll is not scored.** Result: `RESULT.md`.
