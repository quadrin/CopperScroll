# Direction A: photometric-stereo relief rule on the 1988 WSRP previews (frozen protocol)

Frozen 31 Oct 2026 01:05 UTC (30 Oct, Los Angeles), before any relief feature was computed on any control letter and before any target window was located or viewed.

## Claim tested

Relief recovered by photometric stereo (PS) from the USC public previews of the WSRP 1988 multi-light frames separates keyed control letters ḥet (ח) from taw (ת) better than chance, using a rule fixed in advance.

## Inputs (sha256)

- Frames: USC public previews of the 1988 frames, `images/previews/cuts-01-10/` and `images/previews/original-scroll-remaining/`. These are about 1000 px on the long side, at 0.34 mm/px. The listing is in `research/sources/usc_copper_scroll_images/index.csv`. **Limit:** the private full-resolution TIFFs (Drive `06 Imagery/3Q15 Copper Scroll Zuckerman USC`) and the encrypted `private-media/wsrp-1988/*.enc` copies cannot be reached from this container, so everything here runs on the previews.
- Per-cut PS products (private, not in the repository). `ps_cut08_bla.npz` has sha256 `e23abef882e25c9d53b6924bd3f606e4b6d304c2ac08127313915d19d2c98451`. `ps_cut08_col.npz` has sha256 `83ec38ef7b8f4374c7ec9baa34fe0aa9d440a47c45bb1745d87ffe43cad1a0ce`. Both are in `/root/novel/private_outputs/A/`.
- Code:
  - `ps_lib.py` `90dd7586…0d23d`
  - `run_ps.py` `8981cd1e…06975`
  - `map_cuts.py` `125bbb90…6b906`
  - `xfilm.py` `5efa7c1d…bf879`
  - `mapping_agreement.py` `c1a8c3bc…ce0bb`. It was staged at 00:57 UTC, before its result was seen.
  - `features.py` `d5db82f5…5ec5`
  - `score_confirmatory.py` `b641c202…224e`
- Mapping data:
  - `ps_runs/cut_mapping.json` `42f3209b…44cc3`
  - `ps_runs/xfilm.json` `6e18766b…8cc3`
  - `ps_runs/mapping_agreement.json` `2279be11…bd`
- Letter truth and locators:
  - `research/text/letter_controls/controls_manifest.csv` `e2da8dbb…77d`
  - W2F `labels_verified.csv` `5a1c3120…612f`
  - W2F `registration.json` `fc1a2179…6e17`

The full hashes are listed in the commit's `sha256_inputs.txt`.

## How the controls are located (logged)

1. **Registration within a lighting group.** Inside a cut's top-lit group and inside its bottom-lit group, frames are registered by SIFT with a RANSAC affine fit. The 5-fold CV residual is about 1.0–1.5 px.
2. **Registration across groups.** The bottom-lit group is registered to the top-lit group by ECC on the silhouette, then by ECC on the Laplacian magnitude of the group means. A group is accepted when the tile phase shift is at most 2 px.
3. **Photometric stereo.** Azimuths are fixed at the titled positions (L/C/R × T/B). The elevation and per-frame intensities are fitted. Depth is integrated by the Frankot–Chellappa method. An uncalibrated SVD/Hayakawa/integrability solution was also run, but only as a diagnostic: it did not recover the titled azimuths, so it is not used.
4. **Column placement.** Each cut's groove map is placed in its column by matching it against letter boxes from Puech's 2006 facsimile (W2F components mapped onto the copy photograph by the W2F affine). The search covers rotation, scale (constrained by line spacing), aspect and tilt. Peak NCC is about 0.15–0.37.
5. **Acceptance gate** (`mapping_agreement.py`, fixed before its output was seen). The b&w and colour films are mapped independently. The two mappings are then composed through a SIFT b&w→colour registration (CV about 0.3 px). A cut is accepted only if both films chose the same column and the median disagreement over the mapped letters is below 0.5 letter height.
   - **Result:** only cut 8 (column III) passes, at 0.08 letter height.
   - Cut 18 is at 0.59. Cut 3 is at 1.18. Cuts 2, 6, 7, 12 and 16 are at 4.9–17.8.
   - Cuts 4, 5 (b&w), 9 (b&w), 11, 13, 14, 15 (colour), 17 and 19 could not be mapped. Either fewer than 3 frames registered or fewer than 3 light positions exist.
   - Cuts 19–23 (columns XI–XII) were excluded from mapping. PS arrays for cuts 20, 22 and 23 were computed automatically by the batch run but never viewed or mapped.

## Held-out controls and training split

- **Held out:** every keyed control from `controls_manifest.csv` whose W2F centre maps inside the cut-8 strip mask in both films. That set has 7 letters: 3 ח and 4 ת. The candidate IDs are fixed by the code and the inputs above.
- **Training split: empty.** No feature was computed on any control before freezing. The only relief maps seen by eye were the groove and normal maps of cuts 6 and 7 (columns II and III), used to debug registration and orientation. No letter identity was read from them.
- No BK (ב/כ) control and no ה control falls on an accepted cut. The BK and ה/ח questions therefore cannot be tested, and they are recorded as **not testable**.

## Decision rule (a priori, not tuned)

- **Window.** For each letter in each film, sample a window of 2 × Lh88, where Lh88 is the column's facsimile letter height × the mapped scale. The window is centred on the mapped W2F letter centre. It is oriented by the mapped rotation, with u running toward the reading direction (left) and v running down.
- **Relief.** Relief is the high-pass depth, with σ = 6 px. Groove is the negative relief, robustly standardised within the window.
- **Feature.** `f_left_foot` is the mean groove in the box u ∈ [0.50, 0.75], v ∈ [0.35, 0.55] Lh, minus the mean groove of the window outside the central 1 × 1 Lh box. This box is the leftward foot at the base of taw, which ḥet lacks.
- **Validity.** A film is valid when at least 70% of the window lies in the strip mask.
- **Combination.** For each letter, average `f_left_foot` over the valid films.
- **Call.** Call **ת** if the average is > 0 and **ח** otherwise. A letter with no valid film counts as an error.

## Scoring and failure condition

- **Test.** Exact one-sided binomial test of the number correct against p = 0.5 over the held-out ח/ת controls. Report accuracy with its Clopper–Pearson 95% CI and the balanced accuracy.
- **Pass:** p < 0.05. With n = 7, this requires 7 of 7 correct (p = 0.0078); 6 of 7 gives p = 0.0625, which fails.
- **Failure condition:** the held-out controls are not separated better than chance (p ≥ 0.05). Then the result is **not obtained**.
- **Power.** The test is grossly underpowered. A pass would be weak, exploratory-grade support, limited to ח/ת on one cut of column III.

## Targets (I 12, IX 10, VII 11, X 15; XII 10 last)

The rule is applied to a target only if both of these hold:

- (a) the controls pass, and
- (b) the target's cut has a mapping accepted by the same gate, and the target question is ח/ת.

Status as frozen:

| Target | Cuts | Gate status |
|---|---|---|
| I 12 | 2–4 | Failed or not mappable |
| IX 10 | 16–17 | Failed or not mappable |
| VII 11 | 13–14 | PS not run: fewer than 3 registered lights |
| X 15 | 18 | Failed (0.59) |
| XII 10 | 21–22 | Excluded; cut 21 has 2 lights only |

**No target is located, so no target is scored, whatever the control result.** This is decided now. If the controls fail, the rule is not applied to any target either. No target window is cut, viewed or computed in this session.

## Outcome definitions

- **Obtained:** the controls pass and the rule applies to at least one target.
- **Partly:** the PS dataset is produced and the controls pass, but no target can be scored.
- **Not obtained:** the controls fail.

## Dataset named

- Per-cut normal and depth maps: `ps_cutNN_{bla,col}.npz`, private.
- `relief_features_controls.csv`: public, numbers only.
- `confirmatory_result.json`: held-out accuracy.
