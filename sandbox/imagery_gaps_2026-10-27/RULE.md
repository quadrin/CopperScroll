# Run 14 rule: modern high-resolution imagery can fill the survey gaps

Fixed 27 Oct 2026 before any imagery was examined for this run. Exploratory.

## Hypothesis
Runs 1, 5, 7, 11 stalled because surveys do not position pools, cisterns, stairs or rock cracks. Open high-resolution imagery (Esri World Imagery and similar public basemaps, ~0.3–0.6 m) may show open pools, cistern mouths and large rock fissures, and so turn some unknowns into pass or fail.

## Stage A: calibration (must pass first)
- **Known features (fixed now):** at Kh. Qumran, the 8 large pools of Galor (L71, L56/58, L91, L110, L48/49, L117, L118, L138), positioned by the repo's registration of Magen & Peleg Fig. 9; at Hyrcania, the double pool (Patrich 1989 Fig. 22) and dam 44 (ASI Site 48 point); at Kh. es-Samra, the 18×22 m cistern (Cross & Milik p. 11).
- **Blind test:** a scorer agent that has not seen this rule or the plans receives imagery tiles (each ~150 × 150 m, same scale), five with known features and five control tiles of similar terrain without recorded features, coded at random. It marks every pool, cistern mouth, stair and fissure it sees. Answers are hashed before the key is opened.
- **Pass:** at least 6 of the 10 known features found within 10 m, and fewer than 1 false "pool" per control tile on average.

## Stage B: only if Stage A passes
Apply the same blind procedure to the open cells:
1. Ground east of the largest reservoir at Qumran (L71), Hyrcania (double pool) and Kh. es-Samra (cistern), 0–30 m east: any fissure (run 1 J5).
2. Kh. Nabbuh (WBADB S1396/S1375): any pool within 500 m to the east (run 5 K2).
3. The Jisr Abu Ghabush area in Wadi Nuweiʿimeh: any stair visible and its direction (run 11 A1).
Report each as pass / fail / unknown with the tile code and the scorer's mark.

## Limits
Imagery shows the modern surface. A feature not seen is not absent (vegetation, fill, shadow). Only "seen" counts as a pass; "not seen" is unknown unless Stage A shows the feature type is reliably detected (≥80%) at that scale, in which case it may count as a weak fail. The scorer must never be told which tiles are targets.
