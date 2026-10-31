# Run 27 result: a 1 km landscape map on inventory v2, judged against fresh 1940s map features

31 Oct 2026. Rule: [RULE.md](RULE.md), commit 8fd634f (17:08 UTC), SHA-256 in `RULE.sha256`. Windows and reader instructions were committed with the rule, before any new tile was viewed. Scripts were committed in f1aff49 (17:20 UTC), before any reading was used. No revision was made ([FORK_LOG.md](FORK_LOG.md)). Exploratory: no rating, ledger, ACTIVE_TEST or atlas change.

## Verdict

**Not obtained. The scroll was not scored.**
- **G1 passed:** the map's probabilities are calibrated against real, independent features.
- **G2 failed:** the landmark-class evidence moves the odds by nothing. The mean Bayes factor is 0.99×, and its interval spans no change.

Under the rule, a calibrated map that carries no evidence is not scored.

| Benchmark C (89 items, 33 windows) | 50 % set coverage | 90 % set coverage | mean log10 BF (window bootstrap 95 % CI) |
|---|---|---|---|
| R0 | 0.506 | 0.908 | −0.005 (−0.031 to 0.026) |
| R1 | 0.486 | 0.904 | −0.003 (−0.028 to 0.028) |

Median rank of the true 1 km cell: 379 of 2,558 (R0), 217 (R1). Median 90 % area: 1,961 km² (R0), 830 km² (R1).

## What was done

- **Inventory v2.** Lane J's table plus the West Bank and East Jerusalem Archaeological Database (`sandbox/west_bank_inventory_2026-10-31/`): 10,491 located records in 2,558 cells of 1 km, of which 749 hold records.
- **Windows.** 60 windows of 1.5 km, drawn by seed 27 across the four zones (4 Gerizim, 15 Jordan Valley, 20 Jerusalem Hills, 21 Judean Desert). They avoid the 14 windows used before, and tile presence was checked by file size only (`out/window_draw_log.json`).
- **Readers.** Seven separate model instances read the zoom-16 Palestine Open Maps mosaics with the frozen instructions. They saw no inventory, scroll text or candidate place.
  - 160 records, 89 items after merging the same class in the same cell: 42 cistern, 37 cave, 4 tomb, 3 well, 2 aqueduct, 1 pool.
  - Readings: `out/reads/`, `out/benchC_raw_reads.csv`, `out/benchC_items.csv`.
- **Reader agreement**, on C01–C10 read twice: 94 % of first-reading records were matched by the second reader within 50 m with the same class, and 86 % of second-reading records by the first.
- **Parameters**, supervised:

  | Estimated from | Recording rate c (mean) | Site share ρ (mean) |
  |---|---|---|
  | Fold 1 | 0.22 | 0.61 |
  | Fold 2 | 0.08 | 0.59 |
  | All items | 0.11 | 0.60 |

## Why the evidence is flat (exploratory, after the gate)

| True cell | Items | Its feature's class recorded there | Same class in comparable cells (background) |
|---|---|---|---|
| No other-class records | 35 | 11 % | 4 % |
| A recorded site | 54 | 74 % | 65 % |

At 1 km there are two regimes, and the evidence fails in both:
- In empty or thinly recorded ground, the true feature is usually unrecorded, so a match rarely happens.
- At recorded sites, most classes are present anyway, so a match barely separates the truth from other sites.

Reader noise is not the cause. High-confidence readings alone give a mean log10 BF of 0.011 (about 1.03×). By class, cisterns give 0.011 and caves −0.005.

## Reported checks

**Leave-one-source-out** (`out/loso_scores.csv`), with the benchmark-C parameters:

| Hidden source | Other sources still record the class in the cell | 50 % / 90 % coverage, R1 | mean log10 BF, R1 |
|---|---|---|---|
| WBADB (500 sites) | 0.85 | 0.65 / 0.96 | 0.104 (about 1.27×) |
| ASI (500 records) | 0.96 | 0.77 / 0.99 | 0.022 (about 1.05×) |

Even when another source records the hidden class 85–96 % of the time, the evidence is worth at most about 1.3×. The coverage overshoots because hidden sites sit in recorded cells more often than ρ = 0.6 assumes.

**Benchmark A** (machinery; `out/benchA27.csv`, seeds 5001–6000): 50 % / 90 % coverage 0.17 / 0.79 (R1), mean log10 BF 0.066. Its fake world puts only 17 % of truths at sites, against 61 % for the 1940s features. As in run 26, its verdict reflects its own assumptions.

## What it changes

- Across runs 26 and 27, at 300 m and at 1 km, with four or five inventories, **class-level landmark evidence cannot locate the scroll's entries.** "A cistern, cave, tomb, pool or channel is recorded here" separates the true place from others by a factor between 0.99 and about 1.4.
- Calibrated probabilities are achievable (run 27 G1), but under this evidence they equal the prior.
- This closes class-level matching against site inventories as a route to place identification. It does not reverse any earlier result, and it explains why the sandbox tests that rested on feature presence ended at "unknown".
- No candidate, rating or record changes.

## Reopening conditions

- **An inventory with feature attributes** (size, depth, plaster, steps, number of openings, orientation) that would let rarer conjunctions be scored. "A pool with steps 30 cubits east of a channel head" is rare; "a pool" is not.
- **Feature-level relations** (direction and distance between named features) against plans of stated precision. That is a different model.
- Not reopened by more class-level records: inventory v2 already records the class in the true cell at 74 % of sites, and the evidence is still flat.

## Limits

- 89 items in 33 windows is a modest calibration set, though the bootstrap interval is tight around zero.
- The 1940s features are mostly cisterns and caves.
- Readers are AI instances. Agreement is 94 % on ten windows; unlabelled "cave" marks are the least certain.
- The 1940s mapper stands in for the scroll's author. Features destroyed before the 1940s are not represented.
- R1's zone reliability (0.8) is simulated.

## Process notes

- Two readers saw other windows' file names in a folder listing; neither opened them.
- One reader (C01–C10, first reading) had several image views fail with a request limit. It then re-viewed every window in full before writing.
- Readers wrote enlarged crops to scratch folders outside the repository. No map image is in the repository.

## Files

- `windows.json`, `READER_INSTRUCTIONS.md`.
- `scripts/`: `sample_windows.py`, `make_mosaics.py`, `model27.py`, `benchC.py`, `checks27.py`, `scroll27.py` (not run: the gate failed).
- `out/`: gate record `benchC_gate.json`, scores, readings, LOSO, benchmark A, parameter posterior `theta_all.npy`, `mosaic_geometry.json`.
