# Run 28 result: attribute test stopped at the power floor

31 Oct 2026. Rule: [RULE.md](RULE.md), frozen at 63c7858 (SHA-256 in `RULE.sha256`) before any reader started. Scripts were committed at 2ce1f4b, before any reader file existed. Decisions taken after the freeze: [FORK_LOG.md](FORK_LOG.md). Exploratory: no rating, ledger, ACTIVE_TEST or atlas change.

## Verdict

**Not identifiable from available evidence. The scroll was not scored.** The rule needs at least 30 benchmark items; the held sources give **10**. `bench28.py gate` was run once (`out/gate.json`).

## Why so few items

Three earlier surveys were keyed by two readers each, with a third reading: the 1952 cliff survey (DJD III, all 40 sites), the Benjamin survey's Wadi el-Makkuk map (the cave list and 19 nearby sites), and Bar-Adon 1972 (the 25 sites within 1 km of a 1993 cave). Together they give 270 whole features.

| Reason a feature is not an item | Features |
|---|---|
| Not a cave, water, channel or tomb feature (buildings, enclosures, terraces, courts) | 144 |
| No opening count, opening direction, pillar or steps recorded | 95 |
| No link to a 1993 feature: no concordance entry, and no 1993 feature of the same kind within 150 m (300 m for Bar-Adon grids) | 21 |
| **Items** | **10** (1952 survey 8, Benjamin 1, Bar-Adon 1) |

- **The 1993 survey rarely says which earlier cave is which.** Both concordance readers found the same four links only: Benjamin list No. 7 = II/49; 1952 caves 19, 20 and 37 = XI/19, XI/20 and XIII/2. The Region X and XI reports say they could not match their caves to the 1952 survey. No 1993 feature is linked to a Bar-Adon 1972 site.
- **The earlier surveys rarely record what the test needs.** The Benjamin cave list has 8 opening counts, 1 direction, no pillars and no step counts; most of its caves also lack their own grid. Bar-Adon's sites near the cliffs are mostly buildings and enclosures.
- **Location is a weak substitute.** Where an item's truth comes from location, it is a group of 2–4 caves of the same cliff cluster, not one cave.

## Reported checks (pre-specified; not gates)

| Check | Items | 50 % / 90 % coverage (attributes) | Mean log10 BF, attributes (95 % CI) | Class only | Gain from attributes (95 % CI) |
|---|---|---|---|---|---|
| 1. Same team, other medium: 1993 plans as clues against the 1993 text | 53 | 0.76 / 0.95 | 0.34 (0.22–0.48), about ×2.2 | 0.16, about ×1.4 | 0.18 (0.07–0.30), about ×1.5 |
| 2. Kh. Qumran: Magen & Peleg loci against IIIA's lists | 35 | 0.49 / 0.93 | 0.39 (0.25–0.52), about ×2.4 | 0.37, about ×2.3 | 0.02 (−0.03 to 0.08), none |
| 3. Benchmark items, truth by location only | 8 | 0.83 / 1.00 | 0.05 | 0.06 | −0.01 |
| 4. Benchmark items, without features the main session had seen | 9 | 0.84 / 1.00 | 0.10 | 0.07 | 0.04 |

- **Check 1 is the best case:** the same survey team, drawing and writing about the same caves. Attributes add about ×1.5 beyond the class, for about ×2.2 in all. Its 50 % sets cover 76 %, outside the 0.36–0.64 band, so the attribute model is under-confident there.
- **Check 2 shows no gain,** because IIIA's lists record almost no openings, steps or pillars.
- **Checks 3–5** rest on 8–10 items and say nothing. The fitted α values (`out/checks.json`, check 5) rest on 0–3 pairs each and stay near their prior.
- Rank is not reported: with many tied candidates the class-only rank is trivially 1.

## What it changes

- **The independent-describer test of attributes cannot be run with the sources held.** Earlier surveys of these cliffs either did not record openings and directions, or cannot be tied to the 1993 caves one by one.
- **Even in the best case the effect is modest.** When the same team describes a cave twice, the attributes the scroll uses (openings, direction, pillar, steps) add about ×1.5 beyond the class. An independent describer would be expected to agree less, so the gain would be smaller.
- No candidate, rating or record changes. Run 27's reopening condition stays open, and it is narrower now: a second, independent description of the **same caves** that records openings and directions, with a cave-by-cave match. Candidates: the Cave Atlas (on interlibrary loan) and the 1980s Patrich survey of the Qumran caves (not held).

## Limits

- Benjamin sizes are left unresolved (`A|B`): the source prints three unlabelled numbers and the two readers read them in opposite orders. Sizes are not used by the model.
- In the Bar-Adon and 1952 tables, the readers sometimes used one key for different sub-features. The third reading kept reader A's feature; reader B's feature under that key drops out (FORK_LOG).
- All readers are AI instances.

## Files

- `keyed/`: concordance A, B and merged; `djd3`, `ben93`, `ba72` reader files, logs and third readings; `ba72_headers.csv`, `ba72_selected.csv`.
- `out/`: `<src>_consolidated.csv`, `<src>_agreement.json`, `<src>_to_adjudicate*.csv`, `bench_items.csv`, `gate.json`, `checks.json`, `check1_plans_scores.csv`, `check2_qumran_scores.csv`, `check3_location_scores.csv`.
- `scripts/`: `model28.py`, `bench28.py`, `score28.py` (not run: the run stopped), `concordance_merge.py`, `select_ba72.py`, `to_adjudicate.py`, `consolidate28.py`, `agreement.py`, `render_bucket.py`.
