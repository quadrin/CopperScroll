# Direction E: HEXAGON 1974 forward/aft stereo elevation model — frozen protocol (new model "E-local-v1"), 31 October 2026

## Novelty gate
- On 30 October direction E was blocked and never started: the 1974 archives were only in Drive (4.6 GB each).
- This run is the first use of the 1974 KH-9 HEXAGON panoramic film as a stereo pair. KH-9 = the HEXAGON reconnaissance satellite; its forward (F) and aft (A) panoramic cameras look 10° ahead and 10° behind.
- The film is now read window by window from the full-resolution store (hexview.py).
- Earlier HEXAGON work (24 and 26 Oct) used single 1978 frames for 2-D marking and the SULTAN-1 resolvability gate. No elevation model was built from HEXAGON before.
- This is a new frozen protocol. No 30 October result is rescued.

## Claim tested (method claim, not an identification)
A stereo elevation model from the 25 June 1974 pair D3C1208-400636F014 (forward) and D3C1208-400636A015 (aft), built WITHOUT a panoramic camera model, reaches the frozen vertical precision against Copernicus GLO-30 on held-out stable terrain inside the candidate zones. If it does, it can detect relief lost or created since 1974 above a stated minimum size.

## Mask decision (recorded before the freeze)
- At the start the session prompt required a SULTAN-1 / Jericho-oasis mask. I set it before any read (commit 26d6a59e): 3 km about Tell es-Sultan (WBADB E334, 31.871116 N 35.444274 E; Old Israel Grid 192150/142050 = EPSG:28193 192150/1142050) plus the oasis envelope 35.415–35.500 E, 31.835–31.905 N, buffered 1 km.
- The owner's message of 31 Oct (`SP/tools/hexview/SULTAN1.md`, SHA-256 8abcfe31…) made the mask E's choice. Amendment A1 (24 Oct) opened reading north of the tell. HEXAGON failed the 0.5 m resolvability gate (26 Oct; effective resolution about 1 m) and cannot test SULTAN-1-precamp-mouth.
- **E drops the mask.** Reason: no protocol requires it, and these frames cannot test SULTAN-1. Keeping it would remove the lower Wadi Qelt and the oasis edge from the model. `protected_boxes.json` is now empty. Nothing in E tests SULTAN-1; the 250 m strip north of the tell is not a zone.
- Reads made under the mask: A015 tile e overview 1/32 (code only, whole tile); A015 tile c overview 1/32 with the provisional box blank (viewed). See `masking_log.csv`.
- Orchestrator's early window (D3C1209-200214F016 tile d, x and y 10000–12048): the tell in F016 is in tile b (SULTAN1.md). Tiles lie side by side along x (tile offsets in this run: about 35,000 px per tile in F014 and A015). INFERENCE: the window is about 2 tiles (≈ 70 km at ≈ 1 m/px) from the tell. The December pair was not registered in this pass, so this is not confirmed.

## Inputs (SHA-256)
| Input | SHA-256 |
|---|---|
| hexview.py (bucket reader) | 56b21cb0d32b7d3caf1fe1f130493791898d768c087964fe5a745d0dc7630236 |
| GLO-30 tile Copernicus_DSM_COG_10_N31_00_E035_00_DEM (https://copernicus-dem-30m.s3.amazonaws.com/) | 29baca4a170117c090c2ab1f2a4ade53ed1dd085cdbbfaa005631049462221cf |
| ESA WorldCover 2021 v200 tile N30E033 (https://esa-worldcover.s3.eu-central-1.amazonaws.com/) | ebf8b8bde6240429c9246abc936f17a5219699f8315057410480f7ea89b59bae |
| HEXAGON F014 tiles d, e and A015 tiles c, d (store index.json src_sha256 per tile) | as in the store index |
| stage2_zone.py (confirmatory code) | 6e297fddbdcf36d055bc76a37bcfa135d0a0a9a219aab62439cda8838dfc6705 |
| stereo_local.py | 4f93713273cb372a487eaf7379bc82068187e94793fcefa92403e976797493f9 |
| frames.py | 147a5b940019164c7a2e9a15621ef1b06b3466d6cd9d99d91b43ed5a93d82806 |
| common.py | 8f5018dff372a58364968d51512788cc1c084f17aa646632091bb55fdf40d698 |
| refgrid.py | 1e1c0282461eefd40123a3cb4dccf2f4dde59ad1ce5fb3908b6d9ce0cc6a43eb |
| zones.py / zones.geojson | 14680c03b5c3c60e95f9dbf1e059a8daacc64c8fe744a2a91fb57962a7e0f836 / baf5054b06e0edb1d8ac189af763e21148190ea0b4d000c53c1d4f9386c7e026 |
| stage1_geoloc.json (frame-level geolocation) | 872ebfd73abe3bee16fe38012b5a715481c726d83791eedd836b7bcca083cd5b |
| tile_offsets.json | d8c92920cbbf66a243267c67b01a62af073cf46a43931de38d88ce31c13d08bf |

## Zones (polygons in `zones.geojson`, EPSG:4326; metric work in EPSG:32636, UTM 36N)
- QUMRAN: 35.445–35.470 E, 31.728–31.752 N (Kh. Qumran WBADB E754 plateau, marl terrace, Wadi Qumran mouth).
- QELT: 35.320–35.432 E, 31.822–31.858 N ('Ein Fara to the wadi exit, past 'Ein el-Fawwar and Deir el-Qelt).
- KIDRON: 35.325–35.385 E, 31.700–31.735 N (lower Kidron / Wadi en-Nar, Mar Saba to Hyrcania). The Jerusalem stretch is not included.
- JERICHO_OUT: ring 1–4 km from the Tell es-Sultan centre.
- TRAIN (exploratory only, not a zone): 35.395–35.430 E, 31.758–31.785 N.

## Method (code `stage2_zone.py`, `stereo_local.py`; all automatic)
- Pair: F014 (stored north-up) and A015 (stored south-up, turned 180°). December 1974 pair: not run in this pass.
- Frame geolocation (`stage1_geoloc.json`): low-resolution (1/8) stereo over the whole area, disparity correlated with GLO-30 heights over a grid of shift, rotation and scale. Brute-force optimum kept (RMSE 52 m); the unbounded Powell refinement was degenerate and is rejected (recorded in the file).
- Per zone: window = zone bounding box + 800 m (aft + 600 m more), read at 1/2 scale (≈ 1.84 m/px).
- SIFT tie points → robust affine aft→forward → epipolar direction = principal direction of the residuals → rotation; cross-epipolar residual fitted by a cubic polynomial, along-epipolar by a plane; aft warped into the rotated forward frame.
- OpenCV semi-global matching (StereoSGBM, block 5, P1 = 8·25, P2 = 32·25, uniqueness 5, speckle 100/2, disp12MaxDiff 1), disparity range from the tie points ± 6 px.
- 30 m cells: median disparity of a 16 × 16 px block (≥ 50 % valid).
- Registration and height: cell position = stage-1 affine refined by shift (grid ±1.5 km, 100 m, rotation −2…2°; then ±100 m, 20 m), then bounded Powell over shift, rotation, scale (±5 %), two shears (±0.03) and relief displacement (±4 m per px, E and N). Height h = a + b·d + plane + quadratic in (x, y), least squares.
- **Stable terrain**: WorldCover 2021 class 20, 30 or 60 and no class 10, 40, 50, 80, 90 or 95 within 60 m; GLO-30 slope ≤ 25° (at 30 m); GLO-30 height ≥ −390 m (the 1974 Dead Sea and shore lie below).
- **Hold-out**: UTM checkerboard of 600 m blocks. The registration and height fit use only stable cells on "A" blocks. Precision is measured only on stable cells on "B" blocks inside the zone polygon.

## Frozen precision target and failure condition
- Metric: NMAD (normalised median absolute deviation, 1.4826 × median |r − median r|) of HEXAGON-minus-GLO-30 on held-out stable cells (B blocks) inside the zone.
- **Target: NMAD ≤ 2.5 m.** Reason (purpose, not the training result): change detection needs 3 × NMAD ≤ about 7.5 m to see large lost depressions, cuts or pools of the size of quarries and big reservoirs.
- A zone counts only if ≥ 50 % of its expected 30 m cells have a valid elevation and ≥ 300 B cells exist.
- **Fails if** no counted zone reaches NMAD ≤ 2.5 m.
- **Obtained**: every counted zone reaches the target, and at least three zones count. **Partly**: at least one counted zone reaches it, or fewer than three zones count. **Not obtained**: no counted zone reaches it.
- Also reported (descriptive): NMAD by GLO-30 slope class (0–5°, 5–10°, 10–15°, 15–20°, 20–25°), median, RMSE, fitted metres per disparity pixel (expected about 5.2 m at 1.84 m/px and base-to-height 0.35).

## Change detection (interpretable only in zones that pass the precision target)
- Residual r = HEXAGON 1974 − GLO-30 on 30 m cells inside the zone (all valid cells).
- Candidate cells: |r| ≥ max(3 × zone NMAD, 5 m). Clusters: 8-connected, same sign, ≥ 3 cells (≥ 2,700 m²). **Minimum detectable size**: about 50–60 m across and max(3 × NMAD, 5 m) deep or high.
- r < 0 (1974 lower than 2011–15): candidate infill or loss of a depression, cut or pool since 1974 — unless ≥ 50 % of the cluster lies on WorldCover tree, crop or built-up (+60 m): then "surface object in GLO-30". r > 0: removal since 1974 (quarry, cut, erosion, new pool). Median slope > 25°: "steep-slope artefact likely".
- **GLO-30 limit**: GLO-30 is a TanDEM-X surface model from 2011–2015. It includes buildings and tree crowns. Orchards, palms and houses built after 1974 therefore appear as "1974 lower" without any ground change. Only bare-ground clusters can mean a lost depression.
- **HEXAGON 1978** (D3C1214-200439F006/F007, forward only): no 1978 stereo pair exists in the store, so no 1978 elevation model. For interpretable candidate clusters only, a 1974/1978 image chip pair is saved to SP/products for description; this is not scored.

## Camera model (stated before the run)
- Ames Stereo Pipeline (ASP) 3.5.0 was downloaded (asset StereoPipeline-3.5.0-2025-04-28-x86_64-Linux.tar.bz2, SHA-256 202f6cf6…, HTTP 200) and runs (`stereo --version`).
- Its KH-9 panoramic (optical-bar) route was not run. `cam_gen --camera-type opticalbar` needs the four frame-corner longitudes/latitudes from the USGS metadata. The store's index.json has no corner fields, and EarthExplorer needs a login. ASP's own guide (docs/examples/historical.rst, KH-9 section) calls panoramic support "highly experimental" and advises not to spend much time on it.
- So this model uses no panoramic camera model. Cost: heights come from an empirical disparity-to-height fit against GLO-30; positions come from an affine map plus relief terms, not from ray intersection; non-linear film and scan distortions inside a window are not modelled.

## Exploratory exposure before the freeze (training material only)
- Viewed: A015 tile c overview (1/32, masked), A015 and F014 frame strips (1/64), one hillshade/warp debug image of A015 c, the TRAIN relief hillshade and residual map.
- TRAIN results (exploratory, recorded in `results/explore*_JUN74_TRAIN.json`): NMAD on held-out stable cells 18.8–19.1 m at 1/2 scale and 21.1 m at 1/4 scale; 5.0–6.0 m on 0–5° slopes, 15–17 m on 5–10°, 22–26 m above 10°. Fitted −3.2 m per disparity pixel (expected about 5.2). Within 1 km tiles the disparity explains little local relief (median local NMAD 15.8 m). Adding relief-displacement terms did not help.
- No zone window (QUMRAN, QELT, KIDRON, JERICHO_OUT) was read at 1/2 scale before the freeze. They lie inside the 1/8 stage-1 area, which was matched but not viewed at zone level.

## Confirmatory run
`python3 stage2_zone.py JUN74 confirm QUMRAN QELT KIDRON JERICHO_OUT`, once, with the code above. Outputs in `results/confirm_JUN74_<ZONE>.json`. Image products only in SP/products/E.
