# C3: is the III 7 letter-proportion change on the copper? Letter-level frozen protocol (31 Oct 2026)

Worker C3, branch `claude/novel-2026-10-31-C3` (from `origin/main` 7a3b3074). **New model, new frozen protocol.** The 30 October result of direction C (branch `claude/novel-2026-10-30-C`, verdict "not obtained") and the 31 October C2 result (branch `claude/novel-2026-10-31-C2`, "not identifiable", gate failed) stay as they are. Nothing here rescues either.

## 0. Novelty gate

- C2 measured letter height against line pitch per line **band**, by an automatic row profile, without knowing which band was which line. Its band measure was unreliable (Spearman ρ ≈ 0 between frames of one cut).
- C3 measures **each letter** at a known position: the W2F (wave-2 plate model) letter centre on the Puech 2006 copy photograph, mapped into the 1988 frame by A2's text registration. Line numbers come from the edition alignment, not from band detection.
- Reliability is a split-half test per letter: top-lit lights against bottom-lit lights, registered pixel to pixel by A2.
- Only box **centres** are used. The drawn box sizes never enter the copper measurement.

## 1. Claim and registered prediction

**Claim.** The rise in letter height against line pitch that Puech's drawing shows between III 1–6 and III 8–13 (III 7 excluded) is present on the engraved copper (WSRP, West Semitic Research Project, 1988 frames of cuts 7 and 8), beyond any top/bottom difference on the control column.

**Drawing effect (already exposed; drawing only).** Round 1 (`hand_features_by_line.csv`): mean of line medians of class-normalised `h_rel`, III 1–6 against III 8–13 = 0.922 → 1.081, **+17.2 %**. On the 62 column III letters that A2's placement puts on cuts 7–8 (`out/drawing_contrasts.json`), letter-level medians: **+14.6 %** (46 letters before, 16 after). Direction: **up**.

**Registered prediction (decides).** Copper contrast in column III, c_III = median(h_rel_cu, III 8–13) / median(h_rel_cu, III 1–6) − 1, is ≥ THR = **+0.038**, and exceeds the same contrast in control column I by ≥ THR, with bootstrap p < 0.05.

Registered alternatives:
- (a) no column-III-specific change on the copper: the drawn change belongs to the drawing, the copy or the plate photograph;
- (b) a top/bottom difference common to strips (curvature, corrosion, lighting), which the control absorbs.

## 2. Exposure (declared)

- Cuts 7 and 8 (column III) were viewed by eye by the A2, B2 and C2 workers and measured at band level by C2. No model has measured them **at letter level**. This test is therefore weaker than an unseen-image test: a person or model who saw the frames could in principle have formed an impression of the lower lines. No choice in this protocol was made from cuts 7 or 8.
- Control column I (cuts 2, 3, 4): cut 3 was viewed by A2 (crops, overlay). Cuts 2 and 4 were processed by code only (A2 registration and placement). No letter-level measurement of cuts 2–4 before this freeze.
- The drawing values of all columns are exposed (round 1, C2, `out/drawing_contrasts.json`). They were used to choose the control (§6) and to set THR (§8). That is allowed: they are the drawing, not the copper.
- I (C3) viewed **no image** of any cut. All design choices were made on numbers from training cuts 6, 11, 16, 17, 18, 21, 22 (`out/exposure_log.txt`).
- Reserved observation: the letter-level copper heights of cuts 7, 8 (test) and 2, 3, 4 (control). They qualify as unscored because no model has computed any per-letter quantity from these frames. They are not unseen.

## 3. Inputs (SHA-256)

| Input | SHA-256 |
|---|---|
| A2 code, commit 6a309e75 of `origin/claude/novel-2026-10-31-A2` (extracted to `SP/C3work/ref/...`; checked at run time by `c3lib.check_a2`): `common.py` | 97f6e952f3045c327eecd3fc012adf3d220e316853f0a961947275e470b85a10 |
| `register.py` | f48ec4f671489da39bc58959693f4e2fc662ec3d56ce6bc59a4aafbf74f61b99 |
| `ps.py` | 9a7cf1346d97c3a0732cdc0958ca55fad208a3e9bafd70627db7356f6cb2ff0d |
| `copyphoto.py` | 0e7a0278a7ffec29c2861e33c239bcfe189f6cbcf745205881679fb7cb00b25a |
| `place.py` | af0b6480fba0d79276d4c52e379cd86e11f978e973ce548ccc591922f1362059 |
| `controls.py` | 40e93babe98c71bac3a520d387ee5a46802180f334a71f342ef2458b52fac9cf |
| A2 `reg/reg_cut02/03/04/07/08.json` | 0523bae2…, 3c068af1…, 6be255af…, b089dcd5…, d039bb4e… (full values in A2 `sha256_inputs.txt`) |
| A2 `place/place_cut02_I_narrow.json`, `place_cut03_I.json`, `place_cut04_I.json`, `place_cut07_III.json`, `place_cut08_III.json` | f98a9cac…, 442e9e31…, e47914da…, 32dad804…, a9e79053… |
| W2F `labels_verified.csv` | 5a1c3120589d65c6f52e2b206030f8391f396dfdc1e2cbd82967429eb034612f |
| W2F `fac_components_col01.json`, `col03.json` (drawing line pitch) | 6a905277…, 05d7b0b3… |
| `hexview.py` (reader; not called in this run, frames from A2's cache) | 56b21cb0d32b7d3caf1fe1f130493791898d768c087964fe5a745d0dc7630236 |
| Image arrays: A2 cache `SP/a2work/cache/gray_{2,3,4,7,8}_*.npy` (full-resolution luminance of `usc:DSS_3Q15_CT{n}_{light}_T`, read through hexview.py by A2) | not hashed (scratchpad) |
| `out/placed_letters.csv` (step 1) | 28ead052de93d401971cd90834d431c7d85690ec22c94db0bd6842422628e83b |
| `out/drawing_contrasts.json` | 866d2b2d5cd7d6e151c3b82ef2e3dedad0047c610b2ba6a85740012109888e98 |
| `out/class_medians.json` (frozen class table, training) | c71d3cb539f5f89e06d04bf5429cc75c42a752e167613b5449b0ddc756eac017 |

Scripts (`scripts/`, run as `python3 -I scripts/run_test.py`):

```
a8e9b4cdf4f88d14a9e58078a67cdf1f0176883af055deecefdd691749bee58e  c3lib.py
862aaa3a24f040b5094abb8399226ed6130be054ea35fc6419c4931dffc6f033  measure.py
8daf65e860953ce94c2c70509e7dfdbe9851e17a411ec36d8469e543c5120b77  measure_set.py
e7cc81348c0978d3c3654e346999944e76b6cb7d8d18d547bde3b456db363fb2  run_test.py
3e90e3a2463f51a1abc82c5cc9977953a7357b390eb6a47654657bf7c3d8c2d5  placements.py        (step 1, already run)
fa74662a4e15f5738b07e2feefc2a9ff30842d9b09b6f886d35d6047cc76f35e  train_table.py       (exploratory, already run)
800fbe429f039f08c31585d5c8334d0d126f5c8672d83db1f6497460b039d111  explore.py           (exploratory only)
69fc9aa64cd374e47b04228f1c19524da32d2ba823a77d0dcb5b69c5090bda69  explore2.py          (exploratory only)
```

## 4. Placement (centres only)

- Letters: W2F verified letters (`labels_verified.csv`) of the test and control columns. Centre = (`px`, `py`) on the copy photograph (Puech 2006, vol. II, copy A PDF p. 682 for column I, p. 686 for column III).
- Mapping: inverse of A2's accepted affine `A_88ref_to_copy` (global fit; A2's local refinement never passed and is not used).
- Kept if a square of half-size 0.4 Lh around the mapped centre lies inside A2's strip mask (A2's margin rule). If two cuts qualify, the one with the larger horizontal distance to the strip edge is used.
- Lh (nominal letter height, 1988 px) = W2F copy-photo letter height of the column / placement scale (A2 `COPY_LH`). It is one number per column, a scale prior. No drawn box size is used.
- Result (already computed, `out/placed_letters.csv`): column III 62 letters (cut 7: 31, cut 8: 31); column I 96 (cut 2: 28, cut 3: 55, cut 4: 13).
- Column III letters per line, cut 7 / cut 8: III 1 0/6, III 3 7/7, III 4 7/0, III 5 5/6, III 6 3/5, III 8 3/0, III 10 4/0, III 11 0/5, III 12 2/2; III 2, 7, 9, 13 none.

## 5. Measurement rule (`measure.py`, `measure_set.py`; parameters `FINAL`)

For each placed letter, in the 1988 reference frame of its cut, at full resolution:
1. **Signal.** Every usable light (A2 `usable_lights`) is warped into the reference frame (A2 `stack_window`, frame-median normalised). Gaussian blur σ = 2 px; Sobel gradient magnitude; divided by its 95th percentile in the window. Gradient magnitude does not change sign with the lamp. Group images: ALL (all lights), T (top-lit lights), B (bottom-lit lights).
2. **Pitch (copper).** Row profile of the ALL image over |x − x₀| ≤ 1.5 Lh and |y − y₀| ≤ 2.8 Lh; Gaussian 0.06 Lh; mean removed; autocorrelation. Pitch P = the lag of the highest autocorrelation value in [1.4, 3.0] Lh, parabola-refined. A maximum on the range boundary gives no pitch.
3. **Pitch fallback.** If a letter has no own pitch, P = median own pitch of the letters of the same cut on lines l − 1 … l + 1. If none, the letter is not measured.
4. **Extent (clipping by neighbouring lines).** Row profile E(y) of the group image over |x − x₀| ≤ 0.4 Lh and |y − y₀| ≤ 0.5 P (never beyond half a pitch). Gaussian 0.03 Lh. E′ = max(E − 10th percentile of E, 0). Extent = y(0.8) − y(0.2) of the cumulative distribution of E′.
5. **Height.** h_g = extent_g / P, for g = ALL, T, B (same P).
6. **Class normalisation.** h_rel_cu = h_ALL / class median from the frozen training table (`out/class_medians.json`: training cuts only, classes with ≥ 5 letters; 16 classes; other classes use the overall training median 0.4230).

## 6. Regions, lines with few letters, controls, training

- **Regions.** Before = lines 1–6; after = lines 8–13; line 7 excluded (as round 1). The same line numbers for the control column.
- **Lines with few letters.** Letters are pooled per region. Every measured letter counts once. There is no per-line minimum, so III 8 (3 letters) and III 12 (4) enter. Round 1's line-level statistic (mean of line medians, lines with ≥ 3 letters) is reported as secondary only.
- **Control: column I (cuts 2, 3, 4)**, fixed at 07:56 UTC before any copper letter measurement. Among A2's accepted pairs it is the only column whose drawing contrast under the primary statistic, on its placed letters, is below 5 % in size (+2.5 %; 60 letters before, 32 after). Other accepted columns: II +11.5 %, V +8.5 %, IX −8.2 %, X +14.7 %, XII −13.5 % (`out/drawing_contrasts.json`). Cut 10 (C2's column IV control) was rejected by A2 and is unavailable.
- **Training (exploration only):** columns II, V, IX, X, XII (cuts 6, 11, 16, 17, 18, 21, 22). They are neither test nor control.

## 7. Gate (validity; direction-blind; computed on the confirmatory letters)

| Condition | Rule | Training value (exploratory) |
|---|---|---|
| G1_all | split-half Spearman ρ(h_T, h_B) over all measured test + control letters ≥ 0.50 | 0.546 |
| G1_test | the same over column III letters only ≥ 0.40 | (per cut 0.26–0.71) |
| G2 | median relative spread |h_T − h_B| / mean(h_T, h_B) ≤ 0.15 | 0.122 |
| G3 | ≥ 30 measured letters before and ≥ 10 after, in column III and in column I | — |
| G4 | class validity, pooled test + control: tall letters (ך ל ן ק ף ץ) median h_ALL > the rest, and י < the rest | 1.16, 0.87 |

The split-half halves are independent exposures (different lamps; for the 6-light cuts also different views L, C, R), registered by A2 (1.6–2.7 px).

## 8. Statistics, threshold and decision

- c_col = median(h_rel_cu | after) / median(h_rel_cu | before) − 1, letters pooled over the column's cuts.
- Δ = c_III − c_I.
- Bootstrap: 10,000 resamples of letters within each column × region cell, seed 20261031. p_boot = share of Δ* ≤ 0. One-sided 95 % bounds: 5th and 95th percentiles of Δ*.
- Reported: one-sided Mann–Whitney, after > before, in each column.

**Threshold THR = +0.038, justified.**
- The copper measure is compressed. On training letters, copper class medians vary with drawn class medians with slope k = **0.527** (log scale, through the origin, 16 classes; `out/exploratory/train_summary.json`). Class height differences are certain properties of the script, so k calibrates how much of a real height difference the measure shows.
- Under the claim, the expected copper contrast in column III is k × 0.146 = 0.077.
- THR = half of that = **0.038**. This is the analogue of C2's "half the drawing effect" (+0.086), corrected for the measured compression.
- Sensitivity only (does not decide): the uncalibrated half-effect 0.073.

| Result | Condition |
|---|---|
| **not identifiable from available evidence** (label **not obtained**) | the gate fails |
| **supported relative to the registered alternatives** (label **obtained**) | the gate passes, c_III ≥ THR, Δ ≥ THR, and p_boot < 0.05 |
| **rejected** (label **not obtained**) | the gate passes and the 95th percentile of Δ* < THR: the copper excludes a column-III-specific rise of half the calibrated drawing effect |
| **not identifiable, gate passed** (label **partly**) | any other case |

**Failure condition.** The claim fails for this specification if it is rejected. It is not identifiable if the gate fails or if the interval straddles THR.

## 9. Paired analysis (frozen; secondary; does not decide)

For the measured letters of column III, and separately column I (regions only):
- P1. Spearman ρ between copper and drawing heights: class-normalised (h_rel_cu against h_rel_dr) and raw (h_ALL against fac_h / facsimile pitch).
- P2. OLS h_rel_cu = a + b·h_rel_dr + d·after. b = letter-level tracking; d = copper step not predicted by the drawing. Bootstrap 90 % intervals (2,000, letters within region).
  - If the copper reproduces the drawn step, b > 0 and d ≈ 0.
  - If the drawn step is an artefact of the drawing, d ≈ −b × (drawing step) < 0.
- P3. OLS h_rel_dr = a + g₀·after, and h_rel_dr = a + b′·h_rel_cu + g·after. Share of the drawing step explained by the copper = 1 − g / g₀. The drawing step "survives" the copper if this share is < 0.5.
- Expectation: with letter-level copper–drawing ρ ≈ 0.3 in training (raw), P2–P3 have little power; they are descriptive.

## 10. Expectation stated before the run

- Training shows split-half ρ ≈ 0.55 and a within-region robust SD of 0.23 in h_rel_cu. The gate passed on training, narrowly for G1.
- With about 45 / 16 letters in column III and 60 / 32 in column I, the bootstrap SD of Δ is expected near 0.10–0.12 (smoke run on training: 90 % interval 0.4 wide).
- The expected Δ under the claim is about 0.077 − 0.527 × 0.025 ≈ 0.064. Power to reach "supported" is low (about 0.2–0.3). "Rejected" needs Δ ≲ −0.13.
- The most likely outcome is therefore **not identifiable** (gate passed or failed), whatever the truth. The run is made once anyway, because it is the first letter-level copper measurement of column III and its numbers bound the effect.
- Training columns already show that copper column contrasts do not follow drawing contrasts beyond noise of about ±0.1 (II +0.075/+0.115, IX −0.148/−0.082, V −0.135/+0.085, X +0.026/+0.147, XII +0.007/−0.135; copper/drawing).

## 11. Interpretation limits fixed now

- A "supported" result would show a letter-height change on the object inside column III. It would not identify a second engraver. Surface space, tool wear or a change of punch could cause it.
- A "rejected" result would exclude the drawn step at the calibrated half-size for these letters and this measure. It would not exclude a smaller change.
- The calibration k comes from class differences (ascenders, descenders, yod). A uniform height change may be compressed differently. This is a limit on THR.
- Placement rests on A2's global affine fit (local median shift 0.07–0.10 Lh on cuts 7–8). A misplaced centre measures a neighbouring letter or a gap, which adds noise, not direction.
- No identification, reading, rating or location claim follows from any outcome.

## 12. Run

Once, after this file is committed and pushed: `OMP_NUM_THREADS=1 python3 -I scripts/run_test.py`. Outputs: `out/results.json`, `out/letters_measured.csv`. Overlays, if made, go to `SP/products/C3/`, never to the repository. Any change after the run is a new exploratory model, labelled as such.

Optional, after the main run, exploratory only and labelled: the formula seams S11 (II 12 | II 13, cut 6, a training cut) and S49 (X 14 | X 15, cuts 17–18, training cuts). They are not part of this test.
