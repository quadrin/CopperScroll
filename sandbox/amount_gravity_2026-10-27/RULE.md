# Run 21 rule: bigger caches lie nearer Jerusalem

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
If the deposits came from one centre (the Temple treasury), the amount hidden should fall off with the cost of carrying it: larger amounts nearer Jerusalem, smaller ones farther away. If so, an entry's amount hints at its distance.

## Data
- Amounts per entry: first_tests_2026-10-24/method10_hoards/scroll_sums.json, as mass in kg under the karsh reading (71 g) and under the talent reading (21.3 kg); entries with only counts of vessels or ingots are scored separately.
- Distances: walking time from the Temple Mount (places.csv jer_temple) to each placed entry, using run 8's method (Tobler on GLO-30). Two placement sets: (A) run 8's anchors only; (B) every entry with a medium or high placement in places.csv (`entries_best_supported`). Set B is partly circular (some placements use order); report it apart.

## Test
- Spearman correlation between amount and walking time; prediction: negative.
- **Control:** 10,000 permutations of the amounts across the placed entries; one-sided p.
- **Supported** (exploratory): ρ < 0 with p < 0.05 in set A, and the same sign in set B.
- Also report: the total mass per region (Jerusalem, Jericho/Qumran, north) and per walking-time band.

## Limits
Set A is small (about 7 entries). If set A has fewer than 6 entries with amounts, report the test as underpowered and give set B only as descriptive.
