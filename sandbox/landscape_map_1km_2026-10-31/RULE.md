# Run 27 rule: a 1 km landscape map on inventory v2, judged against fresh 1940s map features

Written 31 Oct 2026, before any new map window is drawn or viewed, and before any scroll entry is scored. Owner request, 31 Oct 2026 09:57 America/Los_Angeles: "yes grab these" (fresh 1940s map features) and "sure this too" (the cross-check within the inventories). This follows run 26 (`sandbox/landscape_map_2026-10-31/`, not obtained) and the fifth inventory (`sandbox/west_bank_inventory_2026-10-31/`). Exploratory: nothing here changes ratings, the ledger, ACTIVE_TEST or atlas data. No result of this run is an identification.

## What changes from run 26, and why

| Item | Run 26 | Run 27 | Reason |
|---|---|---|---|
| Inventory | lane J (5 sources minus WBADB) | `features_unified_v2.csv` (lane J + WBADB) | WBADB fills the West Bank gap (inventory note) |
| Cell | 300 m | 1.0 km | Survey points mark site centres; WBADB's gain is at about 1 km |
| c and ρ | uniform, or learned from the inventory itself (invalid) | estimated from where real independent features lie (supervised), on a training fold only | Run 26: neither c nor ρ can be learned from one inventory |
| Gate | fake entries (benchmark A) | cross-fit on fresh 1940s map features (benchmark C) | Run 26: benchmark A's verdict depended on its own assumptions |
| Grid of c and ρ | 0.1–0.9 | 0.05–0.95 in steps of 0.05 | Run 26's c sat on the 0.1 floor |

Everything else follows run 26's RULE.md: the zones, the Dead Sea mask, clue mapping and merging, the background, smoothing, the likelihood, region variants and metrics. Strata are zone × other-class richness bin (0, 1, 2–4, 5–15, 16+), counted at 1 km. Directions, distances and non-landmark words carry no likelihood.

## Benchmark C: fresh 1940s features (the gate)

**Windows.** `scripts/sample_windows.py`, seed 27, written before any tile is viewed. Its output is committed with this rule.
- 60 square windows, 1.5 km on a side, aligned to the Palestine grid.
- Each centre is drawn uniformly from the hypothesis cells of run 26's zones.
- A window is rejected and redrawn if:
  - it overlaps any of the 14 windows of `research/regional/mandate_maps/windows.json` widened by 0.5 km (those features have been seen);
  - it overlaps another accepted window;
  - any of its four corners and centre lies outside the zones or inside the Dead Sea mask;
  - the Palestine Open Maps 1:20,000 tile (`pal20k-1940s`, zoom 16) at any of its four corners or centre is missing or under 3 KB. This uses file size only; no tile is viewed.

**Reading.**
- Each window is a mosaic of zoom-16 tiles (about 2 m per pixel), read by a separate model instance. Readers see only the map image and the instructions in `READER_INSTRUCTIONS.md`: no inventory, no scroll text, no candidate place.
- Readers record every printed symbol or label of these classes: cave, tomb, cistern, well (or well/cistern), pool or reservoir, aqueduct or channel. Each record gives its pixel position and the printed text.
- Ten windows (the first ten by seed order) are read twice by separate instances. Agreement is reported. The first reading is the one used.

**Items.** Each record becomes a one-clue entry, with class mapping as in run 26's benchmark B:
- cave → {cave}; tomb → {tomb};
- cistern and well → {cistern}; pool → {pool_reservoir};
- aqueduct or channel → {channel_aqueduct, dam}.

The true cell is the 1 km cell of the record's position. Pixel positions convert by Web Mercator tile arithmetic; the tiles' known offset (3–19 m) is far below 1 km. Records of the same class in the same cell count once.

**Minimum.** If fewer than 80 items result, the benchmark is underpowered. The run stops with "not identifiable from available evidence" and does not score the scroll.

**Folds.** Windows are put in a random order (seed 2727) and alternated into fold 1 and fold 2.

**Parameter estimation, on a training fold only.**
- For c: each training item contributes P(match | true) = c + b_k(1 − c) if its true cell shows the class, and (1 − c)(1 − b_k) if not. b_k is the background match rate of the item's stratum, from inventory v2.
- For ρ: each training item contributes ρ / N_site if its true cell is a site (other-class records present), and (1 − ρ) / N_other if not.
- The posterior over the 19 × 19 grid (uniform prior) is fixed after training. It is not updated by the scored entry's own inventory.

**Scoring.** Each test item is scored with the other fold's parameter posterior, under R0 and under R1. R1 names the item's true zone with probability 0.8, else another zone drawn by the zone shares of the scroll's candidate places (as amendment 1a of run 26).

**Gate**, on all items pooled across both folds:
- G1: under R0 and R1, 50 % set coverage between 0.38 and 0.62, and 90 % set coverage between 0.82 and 0.97.
- G2: under R1, mean log10 Bayes factor of the true cell above 0, with a 95 % bootstrap interval above 0. The bootstrap resamples windows, not items.

If the gate fails, the scroll is not scored. **No revision is allowed in this run**; a changed model is a new run with a new rule.

## Reported checks (not gates)

1. **Benchmark A (machinery).** Run 26 revision 2's generator, with cell-and-class thinning. c_true and ρ come from the full benchmark-C posterior, at 1 km, on test seeds 5001–6000.
2. **Leave-one-source-out (LOSO).**
   - Sample 500 WBADB sites in hypothesis cells that have at least one class (seed 2728).
   - Hide that site's own rows from inventory v2, and describe the site by one of its classes, drawn at random (seed 2729).
   - Score with the full benchmark-C posterior, under R0 and R1, as above.
   - Repeat with 500 ASI records described by their class and hidden one at a time.
   - Report coverage, Bayes factor and the share of hidden sites still matched by another source in the same cell.
3. **Reader agreement** on the ten double-read windows: share of records matched within 50 m and the same class.

## Scroll outputs (only if the gate passes)

The parameter posterior from all benchmark-C items. Per scored entry, under R0, R1 and R2:
- the top 5 cells, with the nearest W2B place and distance;
- the posterior of the top cell, and the areas of the 50 % and 90 % sets;
- the posterior within 2 km of each candidate place, against its prior;
- robustness: the share of grid points within the 90 % credible region of (c, ρ) under which the top cell stays the same.

Value of information follows run 26's definition at 1 km: the 15 cells with the largest summed gain under R1, plus the cells of Kh. Qumran, Kh. es-Samra and the Jericho palaces.

## Assumptions stated now

- The 1940s mapper is an independent describer. Its relation to the modern inventory stands in for the relation of the scroll's places to the same inventory.
  - That is how c and ρ are estimated.
  - Ancient features that were destroyed or buried before the 1940s are not represented.
  - The 1940s mapper drew visible, mostly well-known features, so ρ may be too high for the scroll's places.
- Readers can misread symbols. That noise is part of the describer.

## Not claimed

No identification, no deposit, no change to any record.

## Fork log

Every change after this rule is committed goes into `FORK_LOG.md`, with the time and the reason, before it is run.
