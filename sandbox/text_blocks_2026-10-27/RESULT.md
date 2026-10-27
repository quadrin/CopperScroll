# Run 13 result: formula seams against regional lists

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit a76791d. Feature matrix written before segmentation ([out/feature_matrix.csv](out/feature_matrix.csv), SHA-256 `f68c9c67…08447`, 06:01:20Z); method locked before any segmentation ran ([out/METHOD_LOCK.md](out/METHOD_LOCK.md), 06:02:02Z). Exploratory.

## Verdict
**Not supported.** The scroll does have real formula seams (p = 0.0004), but they do not fall at changes of region.

- **Seams (BIC, exact DP):** two, before entry 11 and before entry 49. Blocks 1–10, 11–48, 49–60. Gain over no seams +2.81; 3 of 10,000 shuffled orders do as well (p = (3+1)/10,001). Every shuffle chose one seam.
- **Geography:** 0 of 2 seams match a change between secure regions (run 8 anchors: Jerusalem 9, 10, 35, 49, 51 → Gerizim 57 → Beth-shean 58). Both seams fall between two Jerusalem anchors.
- **Near-tie:** moving the second seam from 49 to 50 costs only 0.06 in −2LL and would formally "match" the 51→57 change, but only by splitting Jerusalem anchor 49 from Jerusalem anchor 51. Wider anchor sets (adding Doq, Kozeba, Bethesda; or all medium placements, circular) give 1 of 2 matches, but 88% of random two-seam segmentations do as well.

## What the seams are
- **Before 11:** unit (ככרין/none → mostly ככ), depth given (0 → 0.67), Greek letters stop (0.5 → 0.05), named places rise (0.3 → 0.72).
- **Before 49:** depth stops (0.67 → 0), vessels rise (0.13 → 0.58).
- INFERENCE: the middle block 11–48 is exactly the stretch of the "dig N cubits" formula (first at 11, last at 48), and the ככרין → ככ unit change sits at its start. The seams mark changes in how entries were written, not where they are.

## Exploratory notes
- Feature-drop variants keep the seam at 11 (p ≤ 0.001); the second seam moves between 49 and 50 with coding.
- The project's earlier block boundaries (before 20, 36, 57) do not coincide with formula changes (cost 716.5 vs 647.4 for the optimal three-seam split 11, 16, 50).
- A Gower-distance secondary method (stated in advance) finds one seam, before 11 (p = 0.0014).

## Files
[out/feature_matrix.csv](out/feature_matrix.csv) (all 61 entries), [out/results.json](out/results.json), [out/run_output.txt](out/run_output.txt), [out/explore.json](out/explore.json), [out/seam_tie.txt](out/seam_tie.txt), [out/geo_chance.txt](out/geo_chance.txt), [scripts/](scripts/).
