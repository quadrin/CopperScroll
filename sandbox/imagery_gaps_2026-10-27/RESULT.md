# Run 14 result: can high-resolution imagery fill the survey gaps?

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit a76791d. The key and scoring scripts were frozen before any answer existed ([key/stageA_prescore.lock](key/stageA_prescore.lock), 06:11:47Z; [key/stageB_scripts.lock](key/stageB_scripts.lock), 06:12:52Z). Two fresh blind scorers saw only coded tiles and neutral instructions ([out/scorer_instructions.txt](out/scorer_instructions.txt)); their answers were locked before scoring (A: 06:15:44Z, SHA-256 `ed3face9…7a79`; B: 06:19:08Z, `58b480e9…d992`). Exploratory.

Imagery: Esri World Imagery z18 (Vantor WorldView-2, 21 Oct 2023, 0.5 m); 150 m tiles at 0.25 m/px. Tiles are not committed.

## Verdict
**Stage A passes on the literal count but fails on stricter readings; Stage B fills no gap.** Imagery is not yet a reliable way to fill the survey gaps.

**Stage A (calibration, 10 positioned features + 5 control tiles):**
- Main count: **7 of 10 found within 10 m** (bar 6); false "pool" marks 0.2 per control tile (bar < 1) → **pass**.
- **But one low-confidence mark (0.2) is the match for three pools** (L110, L117, L118). Counting each mark once, only **5** features are found → fail.
- Pre-set stricter branches: pool/cistern marks only **3**; confidence ≥ 0.5 **0**.
- Found: L71 (1.2 m), L56/58 (8.2 m), L91 (2.5 m), L110 (1.1 m, as "other"), L117, L118 (same mark), Hyrcania double pool (7.7 m, "other"). Missed: L48/49, L138, dam 44. Kh. es-Samra's cistern has no position finer than ~100 m and was not counted.
- Detection rate for pools 0.75 (< 0.8), so under the rule "not seen" stays **unknown**, never a weak fail. No stair or fissure was in the calibration set.

**Stage B (open cells):**
- **B1** (fissure 0–30 m east of L71, Hyrcania's double pool, Samra): **unknown** at all three (no marks there).
- **B2** (pool within 500 m east of Kh. Nabbuh; 36 tiles + 8 decoys): **unknown**. 8 marks in total, all confidence 0.10–0.25, none in the target wedge.
- **B3** (Jisr Abu Ghabush stair): **unknown**; no source gives coordinates (Taha 2020 p. 277: "southern bank of Wadi Nueima, c. 3 km north of Jericho"), so no tile could be placed.

## Deviations
Eleven features named, ten positioned (Samra cistern scored only in an alternative count). Qumran split into two adjoining tiles. A neutral "other" mark type added so a dam could be marked. The rule did not say whether one mark may match several features; the literal count allows it.

## What it shows
At 0.5 m, a blind reader finds the big open Qumran pools but marks them with low confidence and does not resolve cisterns, stairs or fissures. Imagery will not close J5, K2 or A1. Plans are still needed.

## Files
[key/](key/) (key and locks), [answers/](answers/) (locked answers), [out/](out/) (scores), [scripts/](scripts/).
