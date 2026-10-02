# R08 parallel packet: Hyrcania registration

Prepared 2 October 2026 UTC / 1 October 2026 Los Angeles. Baseline: `quadrin/CopperScroll` commit `bb2fde4c76dbbe34b4c7345646acee049e875229`. This packet sets measurements and acceptance rules before new controls are collected. It preserves the failed withheld check. It supplies no accepted geographic footprint or deposit coordinate.

## Scope and inputs

R08 asks how directions and measurements should be applied. This workstream tests whether Patrich's regional Fig. 1 and detailed Fig. 22 can support geographic feature placement at declared precision. Separate entry-specific tests retain reference surface, cubit range, direction convention and phase. Registration alone cannot establish an ancient phase or resolve a reading.

Current instructions and baseline were read at the pinned commit:

- [AGENTS.md](https://github.com/quadrin/CopperScroll/blob/bb2fde4c76dbbe34b4c7345646acee049e875229/AGENTS.md).
- [Registration note](https://github.com/quadrin/CopperScroll/blob/bb2fde4c76dbbe34b4c7345646acee049e875229/research/sites/hyrcania_plan_registration_2026-09-30.md).
- [Registration JSON](https://github.com/quadrin/CopperScroll/blob/bb2fde4c76dbbe34b4c7345646acee049e875229/registration/hyrcania_plan_registration_2026-09-30.json).
- [R08 tracker](https://github.com/quadrin/CopperScroll/blob/bb2fde4c76dbbe34b4c7345646acee049e875229/research/OPEN_QUESTIONS.md).

Original cited locators: Patrich 1989 p. 243 Fig. 1 and p. 256 Fig. 22 in [Kotar volume 6765980](https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=6765980); guide vol. 13 pp. 176–177 in [Kotar volume 75901013](https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=75901013). This setup reads existing project records. It makes no new claim of original-page inspection.

## Existing baseline, retained

Regional Fig. 1 uses one manually chosen summit anchor at 31.71894758 N, 35.36561976 E. The fort symbol is at (754,850); station 44 is at (673,780), in top-left-origin image coordinates. The 2 km scale bar spans 186 pixels, giving 10.752688 m/pixel. The trial imposes isotropic scan scale and treats the printed arrow as true north. One anchor supplies no independent fit RMSE.

Esri reference imagery is EPSG:3857, transformed into a WGS84 local azimuthal-equidistant frame. Imagery acquisition date and absolute accuracy remain unknown. Summit identity and map symbol position carry unquantified uncertainty.

The guide's `1837.1261` stayed outside the fit. Conditional expansion to 183700 E / 126100 N in EPSG:28191 gives 31.72741114 N, 35.35474274 E. The recorded operation reports 2 m transformation accuracy; that value describes the coordinate operation, not the guide's feature location. Grid notation, rounding/truncation and exact feature assignment remain unresolved.

Station 44's predicted position is 31.72609582 N, 35.35681167 E. The withheld residual is 244.371061 m. The alternative approximate atlas fort anchor gives 271.082326 m. Preserve both values as failed diagnostic checks. The summit-to-guide distance, 1394.063619 m, measures a straight line rather than either published aqueduct route.

Detailed Fig. 22 has a 50 m scale bar spanning 143 pixels: 0.349650 m/pixel. It has no accepted geographic fit. Existing approximate pool centers have 8-pixel pick uncertainty, the separate filled pool 10 pixels, and cistern S/F 12 pixels. Those nominal source-space values become about 2.80 m, 3.50 m and 4.20 m before registration and scale errors. They cannot support a two-metre total geographic uncertainty target.

Previous entry tests remain conditional: Patrich's northern pool sides are 19, 15, 18.2 and 16 m, with 68.2 m perimeter. Twenty-four cubits at 0.445–0.525 m gives 10.68–12.60 m; side/perimeter models fail that interval. An offset model still needs origin and inward/outward convention. Passage 49's surviving 11.5 m fails a 40/41-cubit horizontal-travel interpretation; the filled end leaves original length unknown.

## New pilot: numerical reproduction only

Run `python hyrcania_registration_audit.py` alongside `hyrcania_baseline.json`. The dependency-free script recomputes the source-image EN displacement and uses a WGS84 ellipsoidal inverse calculation on the stored geographic points. Assertions check agreement with the existing record. Output is `hyrcania_registration_audit.json`.

Result: EN displacement reproduces −834.768883 E / 792.644438 N m; geographic separation reproduces 244.371061 m. The script does not rerun the old-grid datum conversion or select new map/imagery points. A future rerun of that conversion requires a documented PROJ/pyproj installation and recorded operation; neither Python environment currently exposes pyproj.

The notation sensitivity retains two explicit conditional old-grid cells:

- Rounding to nearest 100 m: E 183650–183750, N 126050–126150. Maximum displacement from the nominal point in grid distance is 70.710678 m.
- Truncation to 100 m: E 183700–183800, N 126100–126200. Maximum displacement from the nominal point in grid distance is 141.421356 m.

Subtracting these diagonals from the 244.371061 m residual gives approximately 173.66 m and 102.95 m. These values are approximate error-budget diagnostics. They do not calculate nearest geographic cell distances, estimate total uncertainty or establish the guide's convention. Exact cell evaluation must use the verified projected scale and datum operation. Under the retained 100 m unit assumption, quantization alone offers insufficient displacement to absorb the full discrepancy. Other source and feature-assignment errors remain unbounded.

## Measurements to collect independently

1. **Guide notation and feature identity.** Identify the coordinate legend or stated grid convention for the guide. Transcribe the exact surrounding description and identify whether its point denotes intake dam 44, dam 42, a route waypoint or another feature. Record datum, units and rounding/truncation separately. Keep this record as a withheld check throughout the new registration.
2. **Regional control set.** Select at least six fit controls and three withheld controls before fitting. Prefer surveyed structural corners or channel/dam junctions with independently documented coordinates. Record the corresponding source-image point, feature identifier, locator, pick uncertainty, coordinate source, datum and horizontal uncertainty. A summit symbol and an approximate site-center point do not constitute a surveyed correspondence.
3. **Detailed-plan control set.** Independently identify bridge 48, both pool edges and distinguishable fort corners in a georeferenced survey. Use at least six fit controls and three withheld controls. Assign at least three distinct structures to each set where available; points along one obscured wall are correlated. Redigitize explicit structural corners or intersections rather than repurposing approximate labeled centers. Record whether each edge is observed, reconstructed or phase-dependent.
4. **Source-space dimensions.** Pick original scale-bar endpoints independently twice and trace visible northern-pool corners/edges. Retain source pixel geometry, scale sensitivity and any unmeasurable boundary. Compare scaled plan dimensions with the published side lengths before any geographic transformation. Keep printed dimensions and digitized measurements as separate evidence.

## Rules fixed before new fitting

Default model: a two-dimensional similarity transform with translation, uniform scale and rotation. Fit in a documented metric CRS; use WGS84 local AEQD for local residual reporting and preserve the original survey CRS. Explicitly record x/y order. Establish true/grid/magnetic north and convergence from the source metadata. Keep elevations and vertical datum separate from horizontal registration.

Freeze control identities and fit/holdout assignment in a timestamped JSON or CSV before solving. Controls must span the working footprint: the fit convex hull should cover at least 75% of the intended measurement area, and each feature released geographically must lie inside it. Require controls in at least three sectors around that area; reject a nearly collinear arrangement when the smaller/larger spatial covariance eigenvalue ratio is below 0.1. Features outside the hull retain an extrapolation flag and remain unreleased at feature precision. Report the achieved point distribution rather than silently shrinking the target area after fitting.

For every control, record residual E, N and radial distance. For fit and withheld sets separately report count, RMSE, median, maximum and source-specific uncertainty. Withhold at least three points; fit residual alone cannot validate the transformation. Preserve the guide residual as an additional historical diagnostic even if precise survey controls prove the guide describes a different feature.

No removal or movement of a withheld point to improve the fit. Any independently documented misidentification produces a new version retaining the original failed result, changed correspondence, reason and new holdout assignment. Do not switch to affine or higher-order fitting in response to residual size. A separately justified scan-distortion model requires source evidence, a new predeclared model and independent validation.

Predeclare two release levels:

- **Regional planning:** withheld RMSE ≤50 m, every withheld residual ≤100 m, and a defensible 95% horizontal error bound ≤100 m across the relevant area. This level supports regional route/source comparisons only.
- **Individual feature placement:** withheld RMSE ≤1 m, every withheld residual ≤2 m, and a defensible 95% horizontal error bound ≤2 m at each feature. Source picking, survey/imagery accuracy, transformation uncertainty and local distortion must all enter that bound. Cubit-scale offsets or depths require a separate stricter budget tied to the tested difference and an identified ancient reference surface.

These are project acceptance targets set for the next measurements, rather than estimates of existing source accuracy. Unknown accuracy prevents acceptance at either level. Estimate uncertainty through repeated independent source picks, reported survey covariance and documented transformation uncertainty; use conservative envelopes if distributional assumptions lack support. Do not label a nominal pixel uncertainty as a 95% bound without calibration.

Reject release when feature correspondences, datum or units remain ambiguous; minimum independent control count/distribution fails; any withheld threshold fails; the required error bound cannot be established; or coherent residual direction indicates unresolved distortion. Rejection retains source-relative geometry and all residuals.

TIR North/South at 1:250,000 may provide regional context and name/location checks. Its symbol center and published scale do not make it a validated survey control. Do not use TIR to validate Fig. 22 at pool/bridge precision or treat two cartographic sources as independent measured coordinates. Credit displayed map material to “University of Michigan Library (Stephen S. Clark Library).”

## Next executable measurement

The first discriminating input is a georeferenced Hyrcania survey with bridge 48, two pool edges and independently identified fort controls, plus documented datum and horizontal accuracy. Without it, execute source-space scale/corner digitization and guide-notation verification only. A fit currently lacks the six plus three defensible geographic correspondences; geography stays unset. Do not spend a measurement cycle fitting the approximate summit and guide point together.

Track completion as controls documented, controls accepted by identity review, fit/holdout count, coverage, source-space dimensions, residuals and release decision. This setup and its numerical reproduction add zero primary-source targets, zero decisive candidate tests and zero question closures. R08 remains open; Hyrcania stays possible/low for entries 16, 29 and 35.
