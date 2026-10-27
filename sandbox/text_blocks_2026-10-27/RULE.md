# Run 13 rule: the scroll was compiled from regional lists, and the seams show in its formulas

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
The 61 entries vary in formula: whether a depth is given ("dig N cubits"), the amount unit (ככ vs ככרין vs ככר), the amount formula, direction words, the closing Greek letters (cols. I–IV only), the presence of a place name, "in it"/"beside it" clauses. If the scroll was copied from several regional lists, the formula profile should change at a few **seams**, and the seams should coincide with changes of region.

## Steps
1. **Features (fixed now):** for each entry, from data/scroll-text.js, text/translation_en.json, research/text/inventory_features_2026-10-06.json and the T08 amounts table: depth given (y/n); unit (ככ / ככרין / ככר / none); metal (silver / gold / both / none); vessels (y/n); a direction word (y/n); a named place (y/n); Greek letters (y/n); "dig" verb form; length of the entry in words. Write the matrix to a file and give its SHA-256 before step 2.
2. **Seams:** a changepoint method on the multivariate sequence (e.g. binary segmentation or PELT on a Gower-distance cost; choose one and state it before running), allowing 1–5 seams; pick the number by a penalty fixed in advance (BIC).
3. **Control:** 10,000 permutations of the entry order give the null distribution of the best segmentation's cost gain; p = share of permutations with gain ≥ the real gain.
4. **Geography:** compare the seams with the regional blocks implied by secure place names only (Jericho, Sekakah, Kidron/Jerusalem, Gerizim, Beth-shean; anchors as in run 8). A seam "matches" if it falls within ±2 entries of a change between two secure regions.

## Decision
- **Supported** (exploratory): p < 0.01 for the segmentation, and at least half of the seams match a regional change.
- If supported, the block containing each unplaced entry constrains its region; report the block of every entry.
- Report all seams and the features that change at each.
