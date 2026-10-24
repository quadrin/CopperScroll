# Method 2, HEXAGON 1978: blind marking of the Qumran crop — registration

Written 2026-10-24T10:40:17Z, before the marker runs and before any mark exists.

## Why
The 4-of-8 pass in the results doc was marked by the analyst after seeing the pool outlines. This check repeats the
marking with a marker that has not seen the plan, the outlines or the earlier result.

## Marker
A fresh agent. It may open only the files in marker_inputs/ (the plain crop, the same crop with a pixel grid, and four
2x quadrant zooms). It is not told the site, the pool count, the pool names or positions, or the earlier verdict.
It returns, for every feature it marks, a box in display pixels of the plain crop (640 x 590), a class and a confidence:
- class A: any distinct dark shadow or enclosed tone edge whose outline it can draw (any kind of feature);
- class B: the subset of A it judges to be an open sunken basin (cistern or pool) rather than a room or a wall shadow.
- confidence 1 (faint) to 3 (clear).

## Geometry (fixed)
Display pixel (X, Y) -> tile-c pixel (X/5 + 29302 - 0.5, Y/5 + 19950 - 0.5). Plan -> tile by the 4-point similarity in
cp_fit.json (0.821 m/px, 9.44 deg, L110 centre at 29343.4, 19997.4). Fit RMS 1.5 m.

## Primary score (the registered Method 2 rule, applied blind)
A pool "shows (blind)" if any class-A box, of any confidence, intersects its Magen & Peleg Fig. 9 outline dilated by
1.5 m (L110: circle of radius 2.31 + 1.5 m; L56/58: the union of L56 and L58). Eight pools: L71, L56/58, L91, L110,
L48/49, L117, L118, L138.
- 4 or more of 8 -> the blind marking confirms the pass for this film.
- fewer than 4 -> the blind marking does not confirm it; the doc then says the pass rests on informed marking only.

## Secondary scores (descriptive, no pass/fail)
Same opportunity for pools and controls: a disc of radius 3 m around each locus label point of Fig. 9 ("at" in
qumran-settlement.json). A locus is hit if a box intersects its disc.
- Pools (8): L71, L56 or L58, L91, L110, L48 or L49, L117, L118, L138.
- Controls (16 described non-water rooms in the crop): L116, L115, L41, L38, L37, L24, L39, L51, L30, L52, L34, L53, L86,
  L89, L77, L74.
Report hit rates for class A and for class B, each at confidence >= 1 and >= 2.
