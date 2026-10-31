# Run 26 result: a calibrated landscape map of the scroll's landmark words

31 Oct 2026. Rule: [RULE.md](RULE.md), commit 04a25f4, SHA-256 in `RULE.sha256`. Every change after the rule is in [FORK_LOG.md](FORK_LOG.md). Exploratory: no rating, ledger, ACTIVE_TEST or atlas change.

## Verdict

**Not obtained.** No model passed both the calibration gate and the independent check, so **no scroll entry was scored**. Both revisions that the rule allows were used.

The run did produce two measurements that the project did not have. The first is how complete the modern feature inventory is for features that someone else observed. The second is how much class-level landmark evidence ("a cistern", "a tomb") can move the odds at all.

## What was run

- **Hypotheses.** Every 300 m cell of the four study zones, recorded or not: 28,731 cells, of which 1,127 hold at least one record.
- **Inventory.** Lane J's unified feature table: 5,693 located records from HA-ESI, ASI, the Judean Desert cave survey and the columbaria list.
- **Clues.** The landmark words of `entry_features.csv`, mapped by lane J's class table. 50 of the 61 entries have at least one mapped clue (36 with one, 14 with two).
- **Likelihood.** A cell that is the true place has its landmark recorded with probability c, on top of the background. The background is the empirical rate of each pattern among cells of the same zone and the same richness in other classes.
- **Prior.** A share ρ of the prior goes to cells with records of other classes ("sites"). Region variants: R0 has no region; R1 gives 0.8 to the zones of the candidate places.
- **Gate (benchmark A).** Fake entries describing real recorded cells, scored on a thinned inventory. The 50 % and 90 % highest-posterior sets must contain the truth 42–58 % and 85–95 % of the time (G1), and the mean Bayes factor of the truth must exceed 1 (G2).
- **Independent check (benchmark B).** 56 features printed on the 1940s 1:20,000 maps (cave, aqueduct, tomb, pool, cistern), scored as one-clue entries against the modern inventory.

| Model | Test block | A: 50 % / 90 % coverage, R0 | A: R1 | A: mean BF, R1 | B: 90 % coverage R0 / R1 | B: mean BF, R1 | Outcome |
|---|---|---|---|---|---|---|---|
| Original (rule) | 1001–2000 | 0.29 / 0.80 | 0.34 / 0.83 | 3.8× | 0.59 / 0.63 | — | G1 fails |
| Rev. 1: (c, ρ) pooled across entries | 2001–3000 | 0.45 / 0.90 | 0.53 / 0.91 | 3.4× | 0.64 / 0.39 | 0.66× | Gate passes, B fails; pooling found invalid (below) |
| Rev. 2: c from the 1940s check | 3001–4000 | 0.15 / 0.82 | 0.17 / 0.81 | 1.4× | 0.86 / 0.97 (cross-fit) | 1.06× (interval spans 1) | G1 fails |

BF is 10 to the power of the mean log10 Bayes factor. Files: `out/benchA_test1.csv`, `benchA_test2.csv`, `benchA_test3.csv`, `benchB_v1.csv`, `benchB_v2_crossfit.csv`.

## Findings

**1. Measured coverage of the modern inventory is low and uneven** (`out/benchB_record_distances.csv`, `out/c_prior_v2.json`).
- The 1940s map positions are good: position error 21–79 m.
- Only 15 of 56 mapped features (0.27) have a modern record of the same class in their own cell. The share is 0.36 within 300 m and 0.52 within 1 km; the median distance to the nearest same-class record is 641 m.
- Caves fare worst: 0.17 in the cell and 0.28 within 1 km.
- Some cell matches are chance: another record of that class happens to be there. Allowing for that, the recording rate c is about 0.1. The c prior has a mean of 0.12, with 0.85 of its mass on the grid floor of 0.1, so c may be lower still.
- **Uneven:** in the desert windows (Buqeiʿa, Mar Saba, the Jericho palaces, ʿEin Samiya, Choziba), 2 of 24 features are recorded in their cell. Around Hyrcania, the Kidron, Qumran and Jericho, 13 of 32 are.
- These map windows surround candidate places, the best-studied ground, so coverage elsewhere is probably lower.

**2. Class-level landmark evidence barely moves the odds.**
- **Optimistic world** (recording rate 0.2–0.8, test 2): the truth's odds rise about 3.4× on average. The truth's median rank is about 190 of 28,731 cells, and the 90 % set covers a median of about 500 km² under R1.
- **Measured rate** (test 3): about 1.4×.
- **Against the 1940s features:** about 1.06×, and the interval spans no change.
- A practical rule for other runs: with c near 0.1, *not* finding a recorded feature of the right kind in a cell lowers that cell's odds by only about 10 %. A missing record is weak evidence against a place.

**3. The calibration depends on a number that this inventory cannot supply.**
- ρ is the share of the true places that still have records of other kinds. One entry cannot learn it.
- Learning it across entries (revision 1) counts the single shared inventory once per entry. Benchmark A hid this, because each fake entry had its own thinned copy (fork log, entry 3).
- An even prior over ρ (revision 2) is overconfident when recording is sparse. In test 3, only 12 % of the truths still sit at a recorded site, but the prior gives about half its mass to sites. Under R0 the 50 % sets caught the truth for only 4 % of the truths that were not at a site.

## What it changes

- **Methods.** Any method that scores places by "a feature of the right kind is recorded nearby" should expect the outcome "unknown": reverse lookup, rarity counts, eligibility denominators. These inventories hold about one in ten independently observed features in the right cell, and fewer in the desert. This explains, in numbers, the sandbox pattern that tests stop at "unknown" because data is missing (`claude/sandbox_runs_2026-10-27.md`). It does not reverse any earlier result.
- **Next evidence.** Narrowing has to come from feature-level detail: sizes, relations, the crack line, stair bearings. That detail is in excavation reports and plans (run 25's records), not in the inventories. The value-of-information ranking was not computed, because the scroll was not scored.
- No candidate, rating or record changes.

## Reopening conditions

- **A calibration set of securely identified places that a text of the period describes**, independent of the Copper Scroll and of these inventories. It would estimate c and ρ for text-described places, as the 1940s maps did only for mapped features.
- **A larger independent-describer set over unstudied ground**, for example another map series, to measure coverage outside the windows around candidate places.
- **A model that uses feature-level relations** (direction, distance, size) against plans with stated precision. That is a different model, not a reopening of this one.

## Limits

- Benchmark B is small: 56 items in 9 windows, all near candidate places.
- The c grid starts at 0.1, and the measured rate sits on that floor.
- The Dead Sea mask is crude.
- Direction, distance and non-landmark words (valley, threshold, court, corner, spring) carry no likelihood.
- Lane J's class mapping is used unchanged. Records without coordinates are left out (sensitivity S1 not run, because the scroll was not scored).
- The fake-entry generator assumes that scroll places are like random recorded features.
- No scroll posterior was computed, so nothing about any entry's location was seen or used.

## Checks

- Each test block ran after the commit of the model it judged:
  - rule 04a25f4 (16:04 UTC) and code 3cb050e (16:07), then test 1;
  - revision 1 and 1a, commit 4a62fc6 (16:10), then test 2;
  - revision 2, commit eca3aa2 (16:17), then test 3.
- A rerun of seeds 3001–3040 reproduces the saved rows exactly.
- The tie-sharing coverage rule agrees with a brute-force random-tie count within sampling error (10 seeds × 200 draws).
- The gate figures recompute from the saved CSVs.

## Files

- `scripts/model.py`: grid, likelihood and posteriors (original, revision 1, revision 2).
- `scripts/bench.py`: benchmarks under the original model and revision 1.
- `scripts/bench_v2.py`: benchmarks under revision 2.
- `scripts/diag.py`: dev diagnostics.
- `out/`: all benchmark outputs, including the dev runs on seeds 1–200.
- `inputs/` and `inputs.sha256`: the copied inputs.
