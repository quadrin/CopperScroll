# Direction C, engraver-hand change points: frozen protocol (30 Oct 2026)

Worker C, branch `claude/novel-2026-10-30-C`. Written before any confirmatory computation. Exploratory phase logged in §8.

## 1. Claim and prediction

**Claim tested.** The engraving hand of 3Q15 changes along the text, and the changes coincide with the two formula seams found by sandbox run 13.

**Seams, exact positions.** Sandbox run 13 is on branch `sb` (`origin/sandbox/methods`): rule commit a76791d, result commit 6b3163e, `sandbox/text_blocks_2026-10-27/RESULT.md`. It found two seams, "before entry 11 and before entry 49" (p = 0.0004; Puech numbering, 61 entries). Their positions come from `tables/entry_concordance.csv` (main 7a3b3074):
- **S11.** Entry 11 = II 13–15, so the seam is the boundary between II 12 and II 13 (global line 28 of 181, reading order I 1 … XII 13).
- **S49.** Entry 49 = X 15–16, so the seam is the boundary between X 14 and X 15 (global line 149). Run 13 notes a near-tie with "before 50" (X 17).
Run 13 is not on main; main holds no other seam record.

**Registered prediction.** At least one hand change is detected above the null, and the detected changes fall at S11 and S49 (§4).

## 2. Inputs (SHA-256; repository main 7a3b3074, `sb` eb0ef639)

| Input | SHA-256 |
|---|---|
| `data/scroll-text.js` (ETCBC dss 2.0.1, Abegg/Bowley/Cook) | 36ccd26b6e8c8c5048235188b8b85fe3399c8595e636c2e46cd8450341a1e07d |
| `research/agent_review_2026-10-07/wave2/W2F_plates_model/data/labels_verified.csv` (1,240 letters) | 5a1c3120589d65c6f52e2b206030f8391f396dfdc1e2cbd82967429eb034612f |
| W2F `data/fac_components_col01..12.json` (line geometry of Puech's facsimile) | col01 6a905277…5381, col02 f3bd0720…7e95, col03 05d7b0b3…6cf, col04 85ffc6ef…95b, col05 081ae151…f57, col06 23f9b507…201, col07 39711e6e…eba2, col08 71a66a35…7e5, col09 538c4b94…7c3, col10 50b67e91…ea0, col11 1205d81b…fd1, col12 3a4f271a…242c |
| `research/sources/usc_copper_scroll_images/index.csv` | 6fd093d3f015ca117ba96ecc01e0a80c2a685127a5ba9de1ef56e7f8852f6925 |
| `images/previews/cuts-01-10/*.jpg` + `images/previews/original-scroll-remaining/*.jpg` (all files concatenated in `ls` order) | 16dec51ae5c638b7a217afb666592be4c48fdf329caedd4889135121add8cf2b |
| `tables/entry_concordance.csv` | 9aa7d493bddaef8632736b56951699f3fa1d41097f00e3ef07c60f1849a507bd |

Scripts (in `scripts/`, run from there with `python3 -I run_test.py`):

```
f239ccf22bf1f4341b0752d7f03c79ed6ccaddbb686a38f1fc7c17dba81c2a38  common.py
d5bbf7b7aafa293c89949ad10e68135203d9dacefd064d87a8a965e042130a13  cp.py
acdf686d13ccd76e8a9e6f71be958a6a7cc658fffc480278df8e810669f1e5df  features_drawing.py
405be3fd728c205a31eb896e95799c0de8894424e9d3244f292d7567da73f7e4  features_text.py
1501334770fdf943fec7a245b66750af27ee7b6937b0629c4cbbe757e4269868  photo_build.py
7a4f0d1be0b9c915cbc9d6de144044fd7b694ad49842e88d15cf81315b26049d  photo_measure.py
80ebf81ed85b2f72b17f4853ccab7483a0d783405b6ec68f97f9dc6302363b38  run_test.py
```

## 3. Features (fixed)

**(a) Drawing: W2F letter boxes on Puech's 2006 facsimile.** This is a modern line drawing traced on a photograph of the EDF galvanoplastic copy. It shows the drawer's rendering of letter extent. It cannot show stroke depth, tool or ductus. All quantities are scale-free and normalised per letter class over the whole scroll (`features_drawing.py`):
- `h_rel`: letter box height / local facsimile line pitch, over the class median of the same.
- `asp_rel`: box width/height, over the class median.
- `gap`: intra-word gap between consecutive labelled letters, in units of the line's letter-width scale.
- `wgap`: inter-word gap, in the same units.

Per line, the medians are taken only with enough data: at least 3 letters for h and asp, at least 3 gaps, at least 2 word gaps. Otherwise the value is missing. Per column, medians are taken over all letters or gaps of the column.

**(c) Transcription.** `t_final_rate` per column is the share of final forms (ך ם ן ף ץ) among word-final כ מ נ פ צ. It counts unflagged final letters only, in words of 2 or more letters, and excludes the unit words ככ, ככר, ככרין, ככרים (run 13 formula words). Source: `features_text.py`. The ETCBC transcription keeps written final or medial forms; whether every editor did is a limit.

**(b) Photographs: USC public previews of the 1988 WSRP film, original cut segments, recto, all lights and films.** These previews are about 1000 px high, and a letter is about 25 px tall. Each frame is measured automatically (`photo_measure.py`):
- Scale comes from the black-and-white ruler beside the strip: its 2 cm period gives px/cm.
- `p_pitch_cm` is the line pitch: the autocorrelation of the vertical-gradient row profile over the inner 70 % of the strip.
- `p_adv_ratio` is the horizontal letter advance (autocorrelation of the horizontal-gradient column profile within text bands) divided by the pitch.

A frame is accepted for pitch if its acf is at least 0.10. It is accepted for advance if its acf is at least 0.10 with at least 5 bands. Values are aggregated as medians per cut and per column. The cut-to-column map comes from Puech 2006 radiograph plate captions (W2F `plate_index.csv`): I 1–4, II 5–6, III 7–8, IV 9–10, V 10–11, VI 11–12, VII 13–14, VIII 15, IX 16–17, X 17–18, XI 19–20, XII 21–23. A cut does not equal a column, and frames of a cut include parts of neighbouring columns. At this resolution the photographs measure layout (pitch, advance), not letter shape.

**Column XII and cuts 19–23** were exposed on 30 Oct. They are included because they carry no reading decision here; every test is also reported without XII (T1_without_XII). XII 10 is not singled out.

## 4. Change-point method, null and coincidence (fixed)

Common method (`cp.py`): features are z-scored over the sequence, missing values are set to 0 (the mean), and values are winsorised at ±3. The segmentation is the exact optimum found by dynamic programming. The cost is the within-segment sum of squares (a Gaussian mean shift, unit variance). The number of change points is K* = argmin_K [cost_K + K·pen], with pen = (d+1)·ln n (BIC-type), d = number of features and n = sequence length. The gain is G = cost_0 − (cost_K* + K*·pen).

**T1, PRIMARY (decides).** The sequence is the lines in reading order that have `h_rel` (at least 3 labelled letters). The features are `h_rel`, `asp_rel`, `gap` and `wgap` (d = 4), with K ≤ 6 and a minimum segment of 5 lines.
- *Null:* 10,000 **column-block permutations**: the order of the 12 columns is shuffled while line order within each column is kept (seed 20261030). The full procedure is re-run each time. p_block = (1 + #{G_perm ≥ G_obs}) / 10,001. A free line-shuffle null (seed +1) is also reported.
- *Coincidence:* a change point between consecutive retained lines with global indices g_a < g_b matches seam s if the interval [g_a+1, g_b] overlaps [s−3, s+3]. Here s is the global index of the first line after the seam: S11 = 28 (II 13), S49 = 149 (X 15). This is ±3 lines.
- *Joint null:* p_joint_block = share of block permutations with G ≥ G_obs **and** at least as many seams matched.
- *Placement null:* the chance that K* change points placed at random (minimum segment 5) match at least as many seams; 20,000 draws.

**T2, SECONDARY (does not decide).** Column level, 12 columns: d_h_rel, d_asp_rel, d_gap, d_wgap, t_final_rate, p_pitch_cm and p_adv_ratio. A feature is used only if at least 8 columns have it. K ≤ 3, minimum segment 2 columns, pen = (d+1)·ln 12. Null: 10,000 column-order permutations. Coincidence ("±1 column") holds if the new segment starts at column II or III (S11) or at X or XI (S49), meaning a boundary on either side of the seam's column. T2 is also run per source: drawing only, transcription only, photographs only.

**T3, SECONDARY.** Cut level (photographs): p_pitch_cm and p_adv_ratio over the cuts that have both. K ≤ 4, minimum segment 3 cuts. Null: 10,000 cut-order permutations. Coincidence holds if a new segment starts at cut 5, 6 or 7 (S11) or 17, 18 or 19 (S49).

## 5. Decision rule and failure condition (T1 decides)

| Result | Condition |
|---|---|
| **not obtained** (failure) | K* = 0, or p_block ≥ 0.05: no hand change above the column-order null |
| **not obtained** | p_block < 0.05 but no change point within ±3 lines of either seam |
| **partly** | p_block < 0.05 and at least one seam matched, but p_joint_block ≥ 0.05 |
| **partly** | p_block < 0.05, exactly one seam matched, p_joint_block < 0.05 |
| **obtained** | p_block < 0.05, both seams matched, p_joint_block < 0.05 |

T1_without_XII is reported alongside; if its verdict differs, the discrepancy is stated and the primary verdict is not upgraded. The secondary tests T2 and T3 are reported in full and do not change the verdict.

**Interpretation limits fixed now.** Source (a) is a drawing: a detected change may be the drawer's (Puech's tracing), the copy's, or the plate photography's, not the engraver's. Only (b) touches the object, and only at layout level. A change in letter size or spacing can also come from surface or space constraints (e.g. column XII), not from a different person. "Hand change" here means "change in measured writing layout or proportions". A positive coincidence would show that the seams have a physical correlate. It would not prove separate source lists.

## 6. Run

The run happens once, after this file is committed and pushed: `cd scripts && python3 -I run_test.py`. Outputs: `out/hand_features_by_column.csv`, `out/hand_features_by_line.csv`, `out/photo_frames.csv`, `out/photo_cuts.csv` and `out/results.json`. Any change after the results is a new exploratory model, labelled as such.

## 7. Novelty

Nothing in main, `sb` or `research/logs/` measures letter size, spacing or variant forms across columns. There is no stylometric or hand change-point test (greps: "stylometr", "engraver hand", "scribal hand", "two hands", "hand change", "letter height"). Precedents:
- Phase-4 hypothesis H8 ("a separate sub-list or a second hand") was tested **only through formula changes** (T8).
- H6 (a different hand for the values) is "not identifiable" for lack of 3D data.
- `deep_analysis/changepoint.py` and run 13 segment **text** features.
- W2F used the same letter boxes for a letter classifier, not for per-column measurement.

This test is the first to measure physical writing layout across the text and to test it against the textual seams.

## 8. Exploratory log (before freezing)

What I inspected:
- Run 13 RULE, RESULT, METHOD_LOCK, seam_tie and scripts (on `sb`), plus the entry concordance rows for entries 8–13 and 46–51.
- W2F: column headers, row counts per column and per line around II 9–III 3 and X 11–XI 3 (counts only), letter-class counts, the scripts that define the components and lines, and PREREGISTRATION/REPORT.
- The transcription structure, and the whole-scroll word-final letter totals (not per column).
- USC index metadata for cuts 3 and 8.
- The feasibility run of `photo_measure.py` on the 12 + 12 frames of **cuts 3 and 8 only** (column III, not at a seam). That run gave pitch of about 1.9–2.5 cm and advance of about 0.9–1.3 cm. From it I tuned the ruler rule (black/white requirement) and the acceptance threshold.
- One cut-3 frame (UC15245700), viewed by eye at half size, and its ruler crop. Both are saved only in `/root/novel/private_outputs/C/`.

What I did not look at: no feature value per column or line from any source, and no frame of any other cut. Smoke runs of `run_test.py --smoke` printed only counts and keys.
