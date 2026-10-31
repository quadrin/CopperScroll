# A2: photometric-stereo letter rules on the full-resolution WSRP 1988 frames (frozen protocol, NEW MODEL)

Frozen 31 Oct 2026, about 06:10 UTC, before any feature was computed on any held-out control and before any target window was located, cut or viewed. This is a new model. The 30 October direction-A protocol (SHA-256 `130de878…`, commit `9b1860fb`) and its result (not obtained, 1 of 8) stay as they are and are not rescued.

## Novelty gate (what differs from 30 October)

- Input: the full-resolution USC TIFFs of the WSRP (West Semitic Research Project) 1988 frames from the bucket (about 155 px per cm), not the 1000-px public previews.
- Top-lit and bottom-lit groups are registered without the shading sign: strip-outline ECC (enhanced correlation coefficient) then gradient-magnitude ECC. Median residual 1.6–2.7 px on 13 of 15 checked cuts (round 1: 3–14 SIFT matches, no registration).
- Letters are placed by registering each 1988 strip to the photograph of the EDF copy (Puech 2006, vol. II, copy plates) by image-to-image correlation of the inscribed text. No facsimile drawing is used. Round 1 template-matched groove maps to facsimile letter boxes (NCC 0.15–0.37).
- Rules are trained on a fixed training split and tested once on a held-out split, with a chance baseline that allows for class imbalance and caller bias.

## Claim tested

Template rules on photometric features from the 1988 frames call the identity of held-out keyed control letters (ב/כ, ה/ח, ח/ת) better than a chance caller that ignores the image.

## Inputs (SHA-256)

All hashes are in `sha256_inputs.txt` (60 lines, written before the freeze). Main items:

- Reader `hexview.py` `56b21cb0…0236` (bucket `tools/hexview.py`; observed hash, the store note gives none).
- Frames: bucket items `usc:DSS_3Q15_CT<n>_<LIGHT>_T` (index built 05:07:28 UTC). Cached as luminance in the scratchpad only.
- Copy photographs: Brizemeure, Lacoudre & Puech 2006, *Le rouleau de cuivre de la grotte 3 de Qumrân (3Q15)* (STDJ 55), copy A, single-page PDFs pp. 682–704 (plates CCCLIX–CCCLXXXI, copy photographs of columns I–XII). The embedded plate image is extracted natively, so W2F pixel coordinates apply.
- `research/text/letter_controls/controls_manifest.csv` `e2da8dbb…` (see `sha256_inputs.txt` for the full value). No sealed key was opened.
- W2F `labels_verified.csv` (training letters only).
- Code: `common.py`, `register.py`, `ps.py`, `copyphoto.py`, `place.py`, `controls.py`, `rules.py`, `train_eval.py`, `score_heldout.py`, `split.py`.
- Data: `split.csv` `a0e1e508…42a0` (committed in `3cfb4453` before any control feature existed), `reg/*.json`, `place/*.json`, `loo_train.json`.

## Exploratory phase (done, logged)

1. **Light codes.** R?T = top-lit, R?B = bottom-lit; L/C/R = left/centre/right lamp; RT/RB = centre top/bottom (2-light cuts 4, 17, 21). FRS, RFR, RET, REB, RCS, RBC, RTC are other set-ups; they are not used. Side-lit frames have the far half of the curved strip in shadow; PS (photometric stereo) drops a light at a pixel below 0.25 or above 2.5 of the frame median.
2. **Registration** (`register.py`). Within a group: SIFT + RANSAC affine, 71–1041 inliers, median residual 2.3–3.7 px. Across groups (sign-free): strip outline ECC at 1/8 scale, then gradient-magnitude ECC at 1/4 and 1/2 scale. Check: phase correlation of gradient magnitude in 256-px patches (independent of the ECC objective).
   - Cross-group median residual (px, patches): cut 2 1.82 (29); 3 1.88 (34); 4 1.57 (30); 6 1.82 (39); 7 1.81 (45); 8 1.74 (48); 11 1.89 (61); 16 1.94 (70); 17 2.66 (26); 18 2.06 (65); 21 2.17 (37); 22 2.39 (27).
   - Failed: cut 5 (10.75 px) and cut 10 (3.63 px). Their bottom frames are dropped (gate: median ≤ 3.0 px with ≥ 20 patches). CT16 RET/REB/RFR and CT10 FRS also fail (37–57 px) and are not used.
   - Cuts 9, 12–15 and 1 are not in the delivery; 19, 20, 23 were not registered (no control or target need in this pass).
3. **PS** (`ps.py`). Semi-calibrated Lambertian: titled azimuths (LT 135°, CT 90°, RT 45°, LB 225°, CB 270°, RB 315°), elevation fixed at 30°, frame intensity divided by its strip median. n_y recovers horizontal strokes clearly; n_x carries a step where the shadowed light subset changes. Two-light feature `tb` = (I_top − I_bottom)/(I_top + I_bottom) from the first mirrored pair (CT/CB, T/B, LT/LB, RT/RB): a vertical photometric gradient, available on 2-light cuts.
4. **Placement** (`place.py`, `controls.py`). The strip's multi-light edge image (mean Sobel magnitude over the registered lights) is correlated with the copy plate over scale 0.34–0.60 and rotation −4…4°, then ECC-refined. Gate: distinctiveness (best peak / best peak > 1 letter height away) ≥ 1.8 and median local patch shift ≤ 0.15 letter height. A narrow-scale retry (0.37–0.43) and half-strip templates were tried for failed cuts.
   - Accepted: CT3→I (1.93), CT2→I (narrow, 1.93), CT4→I (1.82), CT6→II (2.97), CT7→III (1.96), CT8→III (2.49), CT11→V (2.95), CT16→IX (3.08), CT17→X (3.10), CT18→X (2.48), CT21→XII (3.58), CT22→XII (2.66).
   - Rejected: CT5→II, CT10→IV, CT10→V, CT11→VI, CT17→IX (1.01–1.68), in all three tries.
   - Visual check of the overlay (copy warped onto the 1988 frame): CT8, CT7 and CT3 only. Lines, the torn top edge of CT7 and the ככ of III 7 coincide. No CT21/CT22 image was viewed.
   - Observation: CT7 holds the right part of column III and CT8 the left part. Round 1 held out its ח/ת controls as "cut 8"; they are on CT7 in this placement.
   - The local phase-correlation refinement never reached its response threshold (0.10); placements rest on the global affine.
5. **Split** (`split.py`, seed 20261031, stratified by letter × column): eligible = BK/HH controls with a W2F locator box and a present cut (105). Round-1 held-out controls LC-CHH-081, 084, 085, 130, 132, 134, 135, 136 are forced into training. Held-out 39, training 66. Each het has one rule, fixed by the seed.
6. **Training data.** Training controls plus W2F verified letters (ב, כ, ה, ח, ת; columns I–X; any letter within 0.5 letter height of a held-out control centre is excluded). Columns XI–XII are not used. Placed with features: 87 items.
7. **Variant choice on training only** (`train_eval.py`, leave-one-out balanced accuracy, 6 channel sets × shift tolerance S ∈ {0, 1, 2}; `loo_train.json`). Best per rule: BK `tb` S2 0.650 (n = 46); HE_HET `tb` S0 0.661 (n = 28); HET_TAW `ny` S2 0.795 (n = 29). These are best-of-18 values and therefore optimistic.

## Frozen rules and parameters

- Placement: as in step 4; strip margin 0.4 letter height (`MARGIN_LH = 0.4`); usable lights as in step 2.
- Features: window 2.5 Lh (letter heights); channel maps high-passed (σ 0.6 Lh), smoothed (σ 0.04 Lh), central 1.4 Lh box resampled to 16 × 16, robust-standardised.
- Rule (`rules.py`): difference of class means on training items; threshold at the midpoint; class-agnostic alignment by integer grid shifts up to S.
  - BK (ב vs כ): `tb`, S = 2.
  - HE_HET (ה vs ח): `tb`, S = 0.
  - HET_TAW (ח vs ת): `ny`, S = 2 (needs ≥ 3 registered lights).
- Each held-out letter is scored once, by the rule in `split.csv`. A held-out letter whose variant channels are unavailable (for example `ny` on a 2-light cut) is listed as unscorable and excluded; unplaced letters are excluded. Both lists are reported.

## Test statistic, chance baseline and decision rule

- Statistic: pooled number correct K over the n scorable held-out letters.
- Chance baseline: a caller that ignores the image and, for each rule r, calls the first class with probability q_r (any bias). p = max over q_r on a 0.02 grid of P(K ≥ k), with the rules independent (`pooled_bias_robust_p`). This allows for class imbalance in the held-out set.
- **Pass:** p < 0.05. **Failure condition:** p ≥ 0.05: the held-out controls are not separated better than chance.
- Power, known before scoring from the placement counts (class-agnostic): the expected scorable set is BK (ב 2, כ 1), HE_HET (ה 7, ח 1) and HET_TAW (ת 2). With that composition only 13 of 13 passes (p = 0.0073); 12 of 13 gives p = 0.148. The test is weak.
- Per-rule results (accuracy, recall per class, single-rule bias-robust p) are reported as descriptive.

## Targets (frozen)

Order if the test passes: I 12, IX 10, VII 11, X 15, XII 10. Status fixed now:

| Target | Letter question (repository records) | Status under this protocol |
|---|---|---|
| I 12 | נ/י before ק against מ (ניקרת / מקרת) | No rule for this pair. Not scored. |
| IX 10 | line end ח/ה, then a cut ר-type letter; ב against ם | CT16 accepted; CT17 maps to column X. No letter-level box. Not scored. |
| VII 11 | ה/ח at the end of המשמרה / המשטח | Cuts 13–14 not in the delivery. Not scored. |
| X 15 | ה/ח in בצחיאת / ביצ{ה}יאת | CT17/CT18 accepted; W2F has only a line-level box (`X15-16_copy`). Not scored. |
| XII 10 | ב/כ (שבצח / שכנה) and ח/ה | CT21/CT22 accepted; W2F has only a line-level box. Not scored. No XII image was viewed. |

The frozen placement maps letter boxes, and no target has a letter-level box on the copy photographs. **No target is scored, whatever the held-out result.** A target letter box would need a reading-based placement, which is outside this protocol.

## Outcome definitions

- **Obtained:** the pooled held-out test passes and at least one target is scored. Excluded in advance (no target is placeable).
- **Partly:** the pooled held-out test passes; no target scored.
- **Not obtained:** the pooled held-out test fails.

The confirmatory run is `score_heldout.py OUTDIR`, run once after the freeze commit. Outputs: `confirmatory_result.json`, `heldout_calls.csv`, `placements_all.csv`.
