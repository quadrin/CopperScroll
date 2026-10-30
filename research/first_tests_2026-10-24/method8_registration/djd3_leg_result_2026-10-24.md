# Method 8, DJD III leg: result (24 October 2026, 16:50 UTC)

Rule: [djd3_leg_rule_2026-10-24.md](djd3_leg_rule_2026-10-24.md), SHA-256 `d132a9b152c74178be70df214c09d9e20bf675cf50fe11548caa32f516a7cdb0`, fixed at 16:35 UTC before any plate page was opened. Script: [reg_djd3.py](reg_djd3.py); numbers: [reg_djd3_results.json](reg_djd3_results.json).

**Result: STOP.** No cut reached gate A (40 RANSAC inliers). This copy of the DJD III plates cannot be aligned to the 1988 frames automatically, so it cannot measure metal loss at the cuts by this method.

| Cut | 1988 frame | Best plate | Inliers (gate 40) | Inliers on the other plates |
|---|---|---|---|---|
| 4 | UC15246882 | XLIX | 16 | 7–11 |
| 5 | UC15245493 | LI | 13 | 8–11 |
| 6 | UC15246329 | XLIX | 15 | 9–14 |

- The expected plates came first for cuts 4 and 5 (col. I is pl. XLIX, col. II pl. LI), but every count is at the level of random matches.
- **Analytical error, corrected:** the first run keyed the plates by a part of the folder name, so only one plate was tried. The key was fixed and the run repeated with the rule unchanged; only the corrected run is reported.
- **Images opened:** plates XLIX, LI, LIII, LV, LVII (Internet Archive loan pages, 2,662 × 3,669 px) and the three 1988 previews. Not opened: plates XLIII–XLVIII, L, LII, LIV, LVI, LVIII–LXXI; LXIX–LXXI (cols. XI–XII) are reserved.

## Why (exploratory look after the result; INFERENCE)
Plate LI (viewed at quarter size) prints column II as ten pieces, the five segments each in an upper and a lower half, low in contrast under soft light. The 1988 frame shows one whole strip under hard light from above, after decades more cleaning and handling. The corrosion texture that SIFT matches is not the same in the two. The plate letters are legible by eye (about 80–100 px high, per the loan README).

## What could still work (new exploratory specification, not run)
Manual landmarks: a person marks the centres of 15–20 letters shared by a plate and a 1988 frame on one segment, away from the cuts, and the same third-order warp is scored on held-out letters. That would be a new test with its own rule, not a rescue of this one.
