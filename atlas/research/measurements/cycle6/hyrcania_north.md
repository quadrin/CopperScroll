# Hyrcania: source-to-source north-reference audit

2 October 2026. Result: **approximate inherited orientation supports the existing page-up proxy; survey bearing and geographic registration remain unvalidated**. Eshel's detailed reused plan adds an explicit north arrow. It does not add independent surveyed control.

## Sources and frozen correspondences

Patrich, “אמות המים להורקניה”, in *The Aqueducts of Ancient Palestine* (1989), Fig. 1 p. 243 and Fig. 22 p. 256, supplied chapter PDF pp. 1 and 14. Original archived full-page images are 1488 × 2033 px. [Fig. 1](../../assets/plans/aqueducts1989/patrich-fig1-p243.png), [Fig. 22](../../assets/plans/aqueducts1989/patrich-fig22-p256.png).

Hanan Eshel, “Aqueducts in the Copper Scroll”, *Copper Scroll Studies*, supplied 2004 paperback of the 2002 publication, p. 96 / Figs. 6.3–6.4, chapter-extract PDF p. 5. [Archived chapter](../../assets/plans/copper-scroll-studies2004/eshel-aqueducts-pp92-107.pdf). Fig. 6.3 explicitly derives from Patrich's aqueduct chapter; Fig. 6.4 credits Patrich, “Hyrcania”, and redraws the detailed waterworks layout. The N arrow points approximately page-up; the source does not specify true, grid or magnetic north. Fig. 6.5 p. 97 is a perspective reconstruction, unsuitable as plan control.

Before fitting, freeze three distinct controls: round cistern northeast of the double pool; northern outer fort vertex; cistern J centre. Hold out both double-pool centres, room L centre, cistern T centre, and the bridge's southeast junction. Feature identities use named/lettered labels and plan topology. Drawn centres and vertices are approximate, not surveyed marks. Eshel picks use `tmp/eshel-p96.png` (718 × 1170 px), rendered directly from `recovered/reference-figures/eshel-aqueducts-pp92-107.pdf`, PDF page 5, using PyMuPDF `page.get_pixmap(matrix=fitz.Matrix(2,2))`. The archived `copper-fig-113.png` has 359 × 585 px: divide these Eshel coordinates and pixel residuals by two to express them in that archived raster. The render is not an enlargement of the archived PNG. ±4 render px corresponds to ±2 archived px. The JSON records all eight full-image coordinate pairs; the script preserves the enlarged-inspection coordinate picks and resampling transformations.

Fig. 1's regional north arrow can establish its own drawn orientation. Its fort and station 48 bridge are generalized small symbols; the double pools are unresolved. It cannot supply three detailed independent corners or a pool hold-out. No regional-to-detail transform is accepted from those symbols. The earlier approximately 244 m withheld-control geographic mismatch remains unresolved.

## Fit, hold-outs and distortion

An orientation-preserving similarity fitted on the three controls gives image rotation −0.935° from Patrich to Eshel. Transferring Eshel's vertical arrow back gives Patrich image unit vector approximately (0.0163, −0.9999): about 0.94° clockwise from page-up. This is a derivative-plan angular convention, not an independently established cardinal bearing.

Training residuals are 2.17, 3.06 and 0.93 Eshel pixels. Held-out residuals are northern pool 5.80 px; southern pool 8.45 px; room L 4.40 px; T 13.34 px; bridge junction 1.43 px. No held-out point was moved to improve the fit. T is a lettered eastern installation in both drawings, but its drawn shape and position differ. The evidence cannot partition that discrepancy between redraw/generalization, approximate centre picking and local distortion. This one residual cannot diagnose a mistaken archaeological identity or reject the whole angular correspondence.

Manual picking sensitivities are ±8 native Patrich px per coordinate and ±4 Eshel px per coordinate. Ten thousand independent bounded perturbation draws (seed 29) produce rotation −2.69° to +0.78°. This range measures picking sensitivity only; it excludes north-convention error and drawing distortion, and is not a statistical confidence interval.

The three-control affine diagnostic has singular-value ratio 1.170. With exactly three controls, that affine interpolates by construction and supplies no fitted validation; no affine correction is accepted. The scale bars independently also disagree: Patrich 50 m / 231 px, Eshel 40 m / approximately 83 px. The similarity predicts 0.426 m/Eshel px versus the Eshel bar's 0.482 m/px, about 11.6% disagreement. Consequently this redraw is not established as a metrically interchangeable copy. Scale disagreement and possible shear do not alone disprove approximately shared north orientation.

## Effect on entry 29

Retain Fig. 22's conditional page-up offsets and unset WGS84 coordinates. Add the source-grounded statement that a derivative detailed drawing shows an explicit approximately page-up north convention. Do not replace the proxy with “validated true north”. The centre-versus-rim datum difference remains approximately 11 m; no new ancient reference surface, conduit contact or pool phase was recovered.

Next discriminating evidence: the original control-bearing plan or surveyed points for bridge, pool corners and fort, with defined north convention and a withheld independent landmark. That would address geographic registration. A local original drawn north reference could improve source-space direction without geographic registration.

Accounting: zero new source targets (reinspection of archived Patrich/Eshel); one completed bounded orientation/control audit, inconclusive for survey bearing; zero decisive tests, closures or new candidate assessments. No source access failure and no outreach.


[Reproducible calculation](hyrcania_north_recompute.py), [fixed inputs, held-out residuals and raster provenance](orientation-transfer.json). Inputs distinguish the 718×1170 direct Eshel render from the 359×585 archived image; do not mix their pixel coordinates.
