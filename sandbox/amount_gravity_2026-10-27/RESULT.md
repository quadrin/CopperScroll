# Run 21 result: bigger caches nearer Jerusalem?

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit ebabf7e. Unit list fixed before any walking time was computed ([out/units.csv](out/units.csv), SHA-256 `ed07cd33…c3c2`, 06:31:15Z). Exploratory.

## Verdict
**Underpowered, and the sign runs the wrong way.** Set A (run 8's anchors) has only 5 entries with weight sums (9, 35, 49, 57, 58), below the rule's floor of 6. Every correlation is positive, not negative: bigger amounts lie *farther* from the Temple.

| Set | n | ρ karsh | p | ρ talent | p |
|---|---|---|---|---|---|
| A | 5 | +0.30 | 0.74 | +0.70 | 0.94 |
| B (descriptive; medium/high placements) | 10 | +0.05 | 0.56 | +0.38 | 0.86 |
| D1 (run 8's 11-anchor set) | 7 | +0.32 | 0.77 | +0.79 | 0.98 |

Walking time out from the Temple Mount (Tobler on GLO-30, 30 m). The same ranks hold for return time, a 90 m grid and straight-line km. The largest placed sum, 600 talents at Beth-shean (entry 58), is also the farthest (19.9 h).

## Exploratory notes
- With all 42 weighed entries at any placement confidence: ρ ≈ −0.09 (karsh) / −0.03 (talent), p ≥ 0.29 — no gradient.
- The north block (57–59) is the heaviest per entry. That fits a separate regional or summary block better than a fall-off from Jerusalem.
- Under the karsh reading, mass is set almost entirely by the unit (ככרין ≈ 300 × ככ). A better test would ask how the units are spread across regions (needs a new rule).

## Files
[out/units.csv](out/units.csv), [out/gravity_results.json](out/gravity_results.json), [out/walk_30m_n8.json](out/walk_30m_n8.json), [out/explore_allplacements.json](out/explore_allplacements.json), [scripts/](scripts/).
