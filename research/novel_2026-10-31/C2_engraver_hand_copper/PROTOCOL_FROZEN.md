# C2: is the III 7 change in letter proportions on the copper? Frozen protocol (31 Oct 2026)

Worker C2, branch `claude/novel-2026-10-31-C2` (from `origin/main` 7a3b3074). **New model, new frozen protocol.** The 30 October result of direction C (branch `claude/novel-2026-10-30-C`, protocol SHA-256 505d5681…, verdict "not obtained") stays as it is. Nothing here rescues it.

## 0. Novelty gate

- Round 1 measured letter proportions only in Puech's drawing (the W2F letter boxes on the Puech 2006 facsimile). The photographs it used were the USC public previews (about 25 px per letter), which resolved only layout (line pitch, advance) and only per cut.
- This run measures the engraved letters on the WSRP (West Semitic Research Project) 1988 frames at half of full resolution (about 77 px per cm; letters about 50–75 px high), from the full-resolution store, line band by line band, inside the column III strips.
- Cuts 7 and 8 were never measured at line level by any run. This is the first test of whether the drawn change exists on the object.

## 1. Claim and registered prediction

**Claim.** The letter-proportion change found in Puech's drawing between III 6 and III 8 is present in direct measurements of the engraved letters on the WSRP 1988 frames of the column III cuts.

**Drawing effect to be matched (round-1 `out/hand_features_by_line.csv`, SHA-256 977c68be…; already exposed).** Within column III, lines III 1–6 against III 8–13 (III 7 excluded):
- `h_rel` (letter height / local line pitch, class-normalised): 0.922 → 1.081, **+0.159 = +17.2 %**. Direction: **up**.
- `gap` (intra-word gap / letter-width scale): 0.232 → 0.115. Direction: **down**.
- `asp_rel`: 0.989 → 0.980 (flat within column III; the segment-level rise 0.85 → 1.05 comes from columns I–II). No directional prediction.
- `wgap`: no III 8–13 value. No prediction.

**Registered prediction (decides).** On the copper, region-level letter height against line pitch is higher in the lower part of the column III strips (III 8–13) than in the upper part (III 1–6) by at least half the drawing effect (+8.6 %), and by at least +8.6 % more than in the control strips.

## 2. Which cuts carry column III (records, checked)

- W2F `data/plate_index.csv` (SHA-256 fcd77fd7…): Puech 2006 radiograph plates for column III are pl. CCCXXXVII (segments "8G 8D", PDF p. 658) and pl. CCCXXXVIII ("7G 7C", PDF p. 659).
- `research/text/letter_controls/controls_manifest.csv` (SHA-256 e2da8dbb…), column `usc_1988_cuts_candidate`, column III: `7;8`.
- Round-1 A `map_cuts.py`: `CUT_COLS = {7: [3], 8: [3]}`.
- The records agree with "cuts 7–8". Limit: Puech's captions name 7G and 7C (left and centre) for column III, so the right part of cut 7 may hold the II/III margin. Only the inner 60 % of each strip is analysed.
- A cut is a vertical strip of the column. Each strip carries all lines of the column for part of the line width. Lines III 1–13 are stacked top to bottom in each frame.

## 3. Inputs (SHA-256)

| Input | SHA-256 / identity |
|---|---|
| `hexview.py` (reader, from `gs://copper-scroll-cog-1030/tools/hexview.py`) | 56b21cb0d32b7d3caf1fe1f130493791898d768c087964fe5a745d0dc7630236 |
| Store index | `index.json` built 05:07:28 UTC 31 Oct (orchestrator) |
| Test frames: `usc:DSS_3Q15_CT7_{RLT,RCT,RRT,RLB,RCB,RRB}_T`, `usc:DSS_3Q15_CT8_{…}_T` | COGs `usc/DSS_3Q15_CT7_*.tif`, `usc/DSS_3Q15_CT8_*.tif`; sizes 2892×5518, 3008×5480, 3056×5395, 3216×5448, 3208×5420, 2845×5460; 2892×5512, 2951×5428, 2944×5340, 2948×5352, 2844×5424, 2991×5464 |
| Control frames: `usc:DSS_3Q15_CT10_{…}_T` (column IV, with the start of V), `usc:DSS_3Q15_CT16_{…}_T` (column IX) | sizes 3077×5406, 3130×5447, 3150×5222, 3039×5333, 3306×5429, 3013×5408; 3126×5129, 3381×5329, 3623×5201, 3202×5160, 3269×5048, 3598×5413 |
| Round-1 drawing features `hand_features_by_line.csv` (branch `claude/novel-2026-10-30-C`) | 977c68bea4778a0b373206bcce42cb47e3db39171b5ccf8875b93b02cbb56e47 |
| `data/scroll-text.js` (ETCBC dss 2.0.1) | 36ccd26b6e8c8c5048235188b8b85fe3399c8595e636c2e46cd8450341a1e07d |

Scripts (`scripts/`, run as `cd scripts && python3 -I run_test.py`):

```
91c1f423ca22e64ce52c8b24bc259f553643583cc2b7fd1b731e464f195171b5  copper.py
8ddf1ec0487734df18e2e3c3cc39952dbd37967e87eb195128356a270fdac3a2  fetch.py
2ae0c4ca3b340ac40d7b3a2ac9bec544f34afe9339a2b2f026f41ed1f3338b2d  run_test.py
ca57846f3f9cc40c1534ef2e3fd3b50c40c4130988c0530578a5d7dd1af5b1ee  explore.py              (exploratory only)
63a7c1a9b0b1699e4f31349ee1fd1f6c35cf6ca17cd60b45956d8ff4fd61adbd  explore2.py             (exploratory only)
05c1b6ba6ddaaa0fcb385b48c9be7797f4f7d90db29230f6b3fc01b2de25f0ae  explore_reliability.py  (exploratory only)
```

## 4. Light codes (from the images and round-1 A `ps_lib.py`)

`R` = recto. Second letter L / C / R = which part of the curved strip faces the camera (the strip is shifted and turned between L, C and R frames; seen on training cut 5). Third letter T / B = lit from the top or the bottom. Frames of different views are not pixel-registered, so the method measures each frame separately and uses only vertical-position statistics inside it.

## 5. Measurement method (fixed; `copper.py`, `run_test.py`)

All steps are automatic. No letter or line is placed by hand or by eye.

1. **Read.** Each of the six standard recto frames per cut, whole frame, at scale 0.5 (hexview `box`, average resampling).
2. **Scale.** The nominal full-resolution scale is 155 px/cm (brief), so 77.5 px/cm at 0.5. The ruler is measured per frame (black-and-white column, autocorrelation peak at 0.65–1.35 × the nominal 2 cm period) and reported. **No decision depends on absolute scale**: the decisive feature is a ratio of vertical lengths.
3. **Strip.** The run of high fine-texture columns nearest the image centre (≥ 1.5 cm wide); rows where the run's brightness exceeds 40 % of its median. The inner 60 % of the strip width is analysed.
4. **Stroke energy.** Luminance band-passed (difference of Gaussians, σ 0.04 cm and 0.25 cm); |∂/∂y| smoothed 0.25 cm along x and 0.03 cm along y (horizontal strokes: roofs and bases of the square script). Holes and dark blotches (luminance < 0.5 × the strip median after 0.1 cm blur, dilated 0.1 cm) are excluded from the row profile.
5. **Line bands.** Row profile of the stroke energy, smoothed 0.06 cm, detrended (4 cm moving mean). Pitch = autocorrelation peak in 1.4–2.8 cm. Bands = profile peaks ≥ 0.6 pitch apart with prominence ≥ 0.15 SD. Each band's strip position r = (y − strip top) / strip height.
6. **Letter height against line pitch (decisive).** For a region of the strip, the band windows (peak ± 0.5 pitch) are baseline-subtracted, normalised and averaged. Letter extent = the 15–85 % inter-quantile range of the mean window. h = extent / frame pitch.
7. **Regions.** "Before" = bands with r ≤ 0.45 (III 1–6 equivalent). "After" = bands with r ≥ 0.55 (III 8–13 equivalent). Bands with 0.45 < r < 0.55 (III 7 area) are excluded. Line numbers are not assigned to bands.
8. **Frame contrast.** c_h = (h_after − h_before) / h_before.
9. **Secondary features (reported, do not decide)**, as medians of per-band values in each region: local pitch; aspect = horizontal autocorrelation period of the vertical-stroke energy (letter advance) / band extent; intra-word gap = mean length of low-energy runs shorter than 1.5 advance / extent (drawing direction: down); inter-word gap = runs of 1.5–6 advance / extent; fill = share of high-energy columns.
10. **Frame acceptance.** Pitch autocorrelation ≥ 0.10 and at least 3 bands in each region.

## 6. Control comparison

- **Control cuts 10 and 16**, measured identically. Cut 10 carries column IV (Puech pls. CCCXXXIX "10C 10D2 9D", CCCXL) and the start of V (pl. CCCXLII "10G"). Cut 16 carries column IX (pls. CCCXLIX, CCCL).
- In the drawing, the same top/bottom split shows **no rise**: column IV h_rel 1.003 → 1.015 (+1.2 %); column IX 1.126 → 0.881 (−21.8 %).
- Columns with a positive drawing contrast (V +12.8 %, VI +12.8 %, X +8.8 %) are **not** used as controls.
- Exploratory training cuts 3, 5 and 6 are **not** controls.

## 7. Statistics, gate and decision rule

- D_test = median of c_h over accepted test frames (cuts 7, 8; up to 12). D_control = the same over control frames (cuts 10, 16).
- One-sided Mann–Whitney U, test frames > control frames.
- Bootstrap (10,000 resamples of frames within each group, seed 20261031) of D_test − D_control: one-sided 95 % bounds (5th and 95th percentiles).
- **Measurement gate (validity; blind to the direction):** G1, every cut has ≥ 4 accepted frames; G2, the pooled within-cut robust SD of c_h (1.4826 × the median absolute deviation from each cut's median) is ≤ 0.25. A larger SD cannot resolve an effect of +17 % with 12 frames per group (minimum detectable difference ≈ 1.645 × 0.41 × SD).
- THR = +0.086 (half the drawing effect).

| Result | Condition |
|---|---|
| **not identifiable from available evidence** (label **not obtained**) | gate fails |
| **supported relative to the registered alternatives** (label **obtained**) | gate passes, D_test ≥ THR, D_test − D_control ≥ THR, and p < 0.05 |
| **rejected** (label **not obtained**) | gate passes and the upper 95 % bound of D_test − D_control < THR: the copper excludes a column-III-specific rise of half the drawing effect |
| **not identifiable, gate passed** (label **partly**) | any other case |

Registered alternatives: (a) no column-III-specific change on the copper (the drawn change belongs to the drawing, the copy or the plate photograph); (b) a top/bottom difference common to all strips (strip damage, curvature, lighting), which the controls absorb.

**Failure condition.** The claim fails for this specification if it is rejected. It is not identifiable if the gate fails.

**Expectation stated before the run (exploratory evidence, §9).** On training cuts 5 and 6, the same pipeline gave a pooled within-cut robust SD of 0.42, and per-band h agreed across frames of the same cut with median Spearman ρ ≈ 0. The gate is therefore expected to fail. The run is made anyway, once, because the gate is computed on the reserved frames and could pass there.

**Interpretation limits fixed now.** A pass would show a letter-height change on the object inside column III. It would not identify a second engraver; surface space, tool wear or a change of punch could also cause it. A gate failure says only that this automatic measure cannot see the effect; it says nothing about the copper itself.

## 8. Run

Once, after this file is committed and pushed: `cd scripts && python3 -I run_test.py`. Outputs: `out/copper_frames.csv`, `out/copper_bands.csv`, `out/results.json`. Overlays go to `SP/products/C2/confirm_cut*_overlay.jpg`, never to the repository. Any change after the run is a new exploratory model, labelled as such.

**Optional, after the main run, exploratory only:** the seams S11 (II 12–13, cuts 5–6, training-exposed) and S49 (X 14–15, cuts 17–18). Not part of this test.

## 9. Exploratory log (before freezing)

Exposure log: `SP/C2work/exposure_log.txt` (every bucket read with box, scale and purpose).

What I looked at:
- Round 1: C note, protocol, `results.json`, `hand_features_by_line.csv` and `_by_column.csv` (all drawing and preview values, already public on the branch); A note and `map_cuts.py`; the summary index.
- W2F `plate_index.csv`; the column/cut rows of `controls_manifest.csv` (header, two rows, and the distinct column-to-cut values; no sealed key or seal output was opened).
- ETCBC text of columns II–IV (letter counts per line).
- Drawing contrasts (lines 1–6 against 8–13) for all 12 columns, computed from the round-1 line CSV. They were used to choose the controls (§6).
- **Frames read (training only):** cut 5, all six lights (overview 1/8 of RCT; crops of RCT at 0.4 and 0.6; whole frames at 0.25 and 0.5; a six-light crop panel viewed by eye); cut 6, six lights at 0.5 (numbers only, plus the smoke run); cut 3, six lights at 0.5 (numbers only). Overlays of cut 5 viewed by eye.
- Tried and dropped: cross-view photometric differences (frames of the L, C and R views are different geometry; registration failed); same-view top/bottom phase correlation (shading reverses between top and bottom light; response 0.001–0.07); per-band extents (ρ ≈ 0 across frames).
- Smoke test of `run_test.py` with cuts 5 (as "test") and 6 (as "control"): gate SD 0.42, gate failed. These numbers do not enter the test.

Not read: **no frame of cuts 7, 8, 10 or 16**, and no frame of cuts 2, 4, 11, 17–23. The orchestrator's access test read one 2000-px window of `CT10_RCT` (centre 1565, 2700) before this run; I did not see it.
