# Run 8 rule: the entry order is a walking route

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
The list was written along a route someone walked. Earlier order models (W2B, T06) used straight-line distance, which ignores the Judean Desert's relief. If the order is a route, the scroll's sequence of securely placed entries should be short in **walking time**, not just in kilometres.

## Anchors (fixed now; only names the project calls known or securely placed)
**Anchor rule:** an entry is an anchor if (a) its cache is placed at or relative to a place fixed by a surviving name or an agreed monument (Mount Gerizim, Beth-shean, Absalom's monument, Siloam, the Kidron, Jericho, Zadok's tomb on the Kidron west bank, the Temple enclosure), and (b) places.csv lists it among that place's `entries_best_supported` at medium or high confidence. A route mention ("on the way from Jericho") does not make an anchor. Each anchor takes that place's coordinate from research/measurements/sequence/places.csv. Write the anchor list (entry, place, coordinate, basis) to a file and give its SHA-256 **before** any path is computed. If fewer than 6 anchors qualify, stop and report that the test is underpowered.

## Test
- **Cost:** walking time by Tobler's hiking function on the Copernicus GLO-30 DEM (or the best open DEM available), least-cost path between each consecutive pair of anchors in scroll order. Compare with straight-line distance.
- **Statistic:** total walking time T of the anchors in scroll order.
- **Control:** 10,000 random orderings of the same anchors (with the first anchor fixed, and also free); p = share of orderings with total time ≤ T.
- **Also report** the same statistic with straight-line distance, so the gain (or loss) from relief is visible.
- **Supported** (exploratory): p < 0.01 under walking time, and walking time gives a smaller p than straight distance.
- If supported, report (a) the optimal route through the anchors and where the scroll departs from it, and (b) for each unplaced entry between two anchors, the corridor of points whose detour cost is ≤ 1 hour (a prediction zone), written to a file.
