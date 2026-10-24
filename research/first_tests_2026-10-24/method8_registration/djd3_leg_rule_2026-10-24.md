# Method 8, DJD III leg: rule fixed before any plate page is opened

Written 24 October 2026 by Claude for the owner ("Go for it", 24 Oct). No DJD III plate page has been opened in this session. The earlier session found the repo's plates scan too blurred (edges smeared over about 4 mm, no match).

## Images
- 1988 side, as in the earlier run: USC previews UC15246882 (cut 4, top light), UC15245493 (cut 5, centre-top light), UC15246329 (cut 6, centre-top light); scale 10 mm = 29.5 px (0.34 mm per pixel, ruler in frame).
- 1956 side: DJD III *Planches*, Internet Archive loan pages in the owner's Drive (`04 Articles and chapters/Copper Scroll page captures/djd3_1962_plates_internet_archive_loan`), plates XLIX, LI, LIII, LV and LVII only. Plates LXIX–LXXI (cols. XI–XII) are reserved and are not opened, listed by content or cropped.

## Method (as the earlier run's `reg_edf.py` / `reg_edf_err.py`)
1. For each cut, match each of the five plates to the 1988 frame (CLAHE, SIFT, ratio 0.8, RANSAC homography at 4 px, rotations 0° and 180°, plate scales 0.8/1.0/1.25). Keep the plate with the most inliers.
2. Gate A, a match: at least 40 RANSAC inliers. Fewer: that cut is "no match".
3. Fit a third-order polynomial warp from the inliers and score each point on 5 held-out folds, in mm on the 1988 frame.
4. Use only points in the middle half of the strip (away from the cut edges) for the decision.

## Decision
- **PASS** (the 1956 photographs can measure metal loss at the cuts) if, for at least 2 of the 3 cuts, gate A holds and the median held-out error away from the cuts is ≤ 0.5 mm.
- **STOP** (this copy of the plates cannot measure metal loss) otherwise.
- Report all three cuts, the inlier counts, medians and 90th percentiles, whatever the result.

## Limits
- The loan pages were saved at about 300 ppi (from the Drive audit; to be checked from the files). The printed halftone screen may limit matching more than the pixel count does.
- A pass shows the 1956 photographs can be aligned. It says nothing yet about any particular cut's edge.
