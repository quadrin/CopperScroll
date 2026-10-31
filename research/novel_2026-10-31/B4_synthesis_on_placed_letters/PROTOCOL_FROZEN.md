# B4: analysis by synthesis on letters placed by A2's registration — frozen protocol (NEW MODEL)

Frozen 31 October 2026 by Claude (worker B4, branch `claude/novel-2026-10-31-B4`), before any held-out letter was featurised or scored. Everything in §10 is EXPLORATORY and used TRAIN letters only.

## 0. Novelty gate (what differs from B2 and round 1)

- Letter positions are given, not searched for. Each letter's centre comes from a W2F (wave-2 plate model) verified letter box on the Puech 2006 copy photograph, mapped into the 1988 frame by A2's accepted copy-photo registration. B2's templates collapsed to line-band edges because its model had to find the letters; this model never aligns text to the image.
- Multi-light appearance comes from A2's registered stack (all usable lights of a cut in one reference frame), not from frames scored one by one.
- Templates are learned at placed TRAIN letters, per cut with shrinkage to a scroll-wide template, and re-centred by congealing.
- The split is new (seed 43102026) and covers only lines with placed letters on A2's accepted cut/column pairs. This is a new model with a new frozen specification. The round-1 result (4 of 13, p = 0.21 under 1/K) and B2's result (T = 2 of 25, P = 0.98) stand.

## 1. Claim tested

On the full-resolution 1988 West Semitic Research Project (WSRP) frames, a template model of the scroll's own letters, evaluated at letter positions supplied by registration (not by reading), ranks the edition reading of held-out undisputed lines first among edition-style one-letter confusions more often than the exact chance rate.

This tests a reading method. It is not an identification. It changes no rating, outcome-ledger entry, ACTIVE_TEST, OPEN_QUESTIONS or atlas data.

## 2. Inputs

All SHA-256 values are in `sha256_inputs.txt` (written by `hash4.py` before this freeze). Key items:

- Reader `hexview.py` 56b21cb0…0236 (observed). Images: A2's full-resolution grey cache in the session scratchpad (`a2work/cache`, read only; `b4lib.check_cache` stops the run if a file is missing, so A2's cache is never written).
- A2 code and outputs, copied unchanged into `a2_reused/` from `origin/claude/novel-2026-10-31-A2` at 6a309e75 (`common.py`, `ps.py`, `place.py`, `register.py`, `copyphoto.py`, `controls.py`, `reg/`, `place/`; `place.py` af0b6480… equals the A2 branch file).
- W2F `labels_verified.csv` 5a1c3120… (1,240 verified letters; all 1,240 match the ETCBC letter at their word and character index). For targets only: `registration.json` fc1a2179…, `viterbi_col10.json` fcf66bd9…, `fac_components_col10.json` 50b67e91….
- Text: ETCBC dss 2.0.1 lines `etcbc_lines.json` 3959751b… (same file as round 1 and B2). Edition data: `variants.csv` 07be73c9…, `confusions.csv` 765ebdca…, `plate_check.md` 7d528ed4…. XII 10 protocol 0e19467c….
- B4 frozen code: `b4lib.py` 7726c523…, `items4.py` ea652dd5…, `model4.py` 752b92c1…, `run4.py` 095e19b3…, `targets4.py` c2681941…. Pre-freeze data: `items4.json` ff30c36b…, `placements4.csv` a3bf376f….

Abbreviations: Lh, letter height; NCC, normalised cross-correlation; CT/CB, centre-top/centre-bottom raking light (codes RCT/RT and RCB/RB); LT, LB, RT, RB, left/right top/bottom raking lights (RLT, RLB, RRT, RRB).

## 3. Letter placement (`b4lib.py`, log `placements4.csv`)

- Accepted cut/column pairs: A2's gate (distinctiveness ≥ 1.8, local median shift ≤ 0.15 Lh), 12 pairs: CT2, CT3, CT4 → I; CT6 → II; CT7, CT8 → III; CT11 → V; CT16 → IX; CT17, CT18 → X; CT21, CT22 → XII.
- Centre of a W2F letter: x = facsimile box centre, y = line centre at that x (W2F `plx`, `ply`, copy-photo pixels). The box size is not used, so the drawing's letter extent is not imported.
- Mapping: inverse of A2's `A_88ref_to_copy` affine for the first accepted cut of the column (ascending cut number) in whose strip mask a square of half-size 0.45 Lh around the centre lies entirely. Lh in 1988 px = W2F copy letter height / A2 scale.
- Result: 436 of 1,240 W2F letters placed. Each row of `placements4.csv` logs line, word index, letter index, cut, reference frame, box (centre ± 0.5 Lh), placement file, distinctiveness, local median shift and a placement confidence (high: distinctiveness ≥ 2.4; medium otherwise).
- Local search (frozen): each template is matched over a shift window of ±0.20 Lh horizontally and ±0.15 Lh vertically around the mapped centre.

## 4. Lines, split and candidates (`items4.py` → `items4.json`)

- Undisputed word (B2 rule): no ETCBC flag, not Greek, no `variants.csv` row on the word, at least 2 letters.
- Eligible line: column with an accepted pair (I, II, III, V, IX, X, XII); no Greek; not in `plate_check.md`; not a target line (I 12, VII 11, IX 10, X 15, XII 10); at least 6 letters and 3 letters in undisputed words; at least 2 placeable positions (letters in undisputed words with a placed W2F box). 44 lines.
- Split: lines sorted by (column, line), permuted by `numpy.random.default_rng(43102026)`; first half TRAIN (22), rest HELD-OUT (22). No line is forced into TRAIN.
- TRAIN letters: every placed W2F letter not on a held-out line and not on a target line: 256 letters. A letter form (final forms separate) is modelled if it has ≥ 4 TRAIN letters (22 forms).
- Candidates: the ETCBC truth plus up to 5 one-letter substitutions at placeable positions whose truth form is modelled. Partners: `confusions.csv` rows with count_places ≥ 3 whose substituted form (final form at word end) is modelled. Up to 5 (position, partner) options drawn without replacement, weights = pair rate, `default_rng(35102026 + 100·col + line)`.
- Dropped after the split (no modelled option): I 13 and II 11 (held-out), X 9 (train).
- HELD-OUT lines (line: competitors, varied positions): I 5:5,3; I 8:5,5; II 1:5,3; II 8:5,5; II 10:5,4; III 3:5,4; III 5:5,4; III 10:5,3; III 12:5,3; IX 1:5,3; IX 2:5,2; IX 4:3,1; X 1:5,3; X 5:5,4; X 8:3,1; X 10:5,3; X 12:5,3; XII 1:5,3; XII 2:5,4; XII 3:5,4; XII 7:5,5; XII 9:5,3. In all: 22 lines, 73 varied positions.

## 5. Model (`model4.py`, frozen parameters; exploratory choice V12, §10)

- Patch: registered stack window (A2 `ps.stack_window`; intensity divided by the frame median), 2.0 Lh square, resampled to 20 px per Lh.
- Channels: one per light class, high-passed (subtract Gaussian σ = 0.5 Lh): CT, CB, LT, LB, RT, RB (those present on the cut). Two photometric ratio channels: TB = (top − bottom)/(top + bottom), LR = (left − right)/(left + right), smoothed σ = 0.03 Lh and high-passed. Two-light cuts (4, 17, 21) have CT, CB and TB only; cut 2 has no CT/CB and uses LT+RT and LB+RB for TB.
- Templates: 1.2 Lh square. Scroll-wide template of a form = mean of standardised TRAIN patches, re-centred twice by congealing (each TRAIN patch shifted within the search window to its best match with its form's template, then re-averaged). Cut template = (sum of that cut's TRAIN patches of the form + 5 × scroll-wide template), standardised.
- Raw score of form c at a placed letter: channel-mean NCC of c's cut template over the patch, maximum over the shift window.
- Calibrated score: z = (raw − μ_c)/σ_c, with μ_c, σ_c the mean and SD of c's raw score over TRAIN letters of every other form. This removes differences in the general response level of templates built from different numbers of letters.
- Line score: sum of letter scores. All candidates share every letter except at the varied positions, and each position's score depends only on the image there and the candidate letter, so the ranking is decided by the varied positions alone. The score of a candidate does not depend on the other candidates in its set.

## 6. Statistics, pass mark, failure condition (`run4.py`)

- **Primary.** T = number of held-out lines whose edition reading strictly outscores every competitor. A tie counts against the truth (recorded). Exact null: line i has p0_i = product over its varied positions of 1/(a+1), a = number of distinct competitor letters at the position. T is Poisson-binomial; P(T ≥ t_obs) exact. From the item structure alone: E[T] = 1.50 over 22 lines; P(T ≥ 4) = 0.053, P(T ≥ 5) = 0.012. So T ≥ 5 is needed.
- **Decoy-truth bias control.** For each held-out line, a seeded competitor V (`default_rng(4202610 + 100·col + line)`, uniform over the line's competitors). The decoy set is the line with V's letter at V's position against the edition letter and the other competitor letters at that position. V ranks first iff its letter strictly outscores all of them. Null 1/(a+1); T_decoy Poisson-binomial.
  - Why one position: this model's string score is set-independent and adds over positions. A decoy set that also varies other positions would let a working model favour the decoy wherever the decoy carries edition letters, which is information, not bias. At V's own position a working model ranks V first less often than chance, an unbiased blind model at chance, and a model biased toward the set centre more often.
- **Pass mark.** PASS iff (a) at least 10 held-out lines are scored, (b) P(T ≥ t_obs) < 0.05, and (c) P(T_decoy ≥ t_decoy) ≥ 0.05.
- **Failure condition.** Otherwise FAIL: held-out undisputed lines do not rank their own reading first more often than the exact null (or the decoy shows a centre bias, or too few lines).
- **Secondary (registered, reported; they qualify the label in §8):**
  - Label-permutation null of T. TRAIN labels permuted within cut (200 permutations, `default_rng(31104)`), templates and calibration rebuilt, held-out T recomputed. P_perm = (1 + #{T_perm ≥ t_obs})/201. This null keeps the class sizes, so it includes any bias from unequal template sample sizes.
  - W = held-out positions where the edition letter beats every competitor letter there; null 1/(a+1), Poisson-binomial.
  - Per-letter accuracy for ב/כ (and ך/ב) and ה/ח: TRAIN letters by leave-one-line-out; all placed held-out letters of these forms (not only varied positions), templates from all TRAIN letters.
  - Median |truth − best competitor| score margin over held-out positions.

## 7. Targets (`targets4.py`; scored only on PASS, once)

Scorable only if the competing readings align letter by letter with letters that W2F's Viterbi alignment assigned to facsimile components, and those letters place on an accepted pair. Status fixed now, from placement only (no image read):

| Target | Status | Reason |
|---|---|---|
| X 15 | scorable on PASS | ETCBC/Milik חמים של רחיל תחת vs Puech המים שלוח ולתחת: 13 letters each, one to one; they differ at ETCBC word 2 letter 0 (ח/ה), word 4 letter 0 (ר/ו), word 4 letter 2 (י/ו). All three place on CT18. |
| IX 10 | not scorable | Under the accepted CT16 → IX placement, the first two words (בקומעה כסף) lie on CT16. The disputed words מנה חרמ map 0.15–6.4 Lh beyond CT16's left strip edge, i.e. onto CT17, whose IX placement A2 rejected. |
| XII 10 | not scorable | The disputed word is a wildcard in W2F's alignment (no letter units); R1–R7 differ in length. |
| I 12 | not scorable | ניקרת (5 letters) against מקרת / נקרת (4 letters): no one-to-one letter alignment. |

X 15 output: summed z-score per reading, the margin, and per position the held-out accuracy among positions whose margin is at least as large. A target **leans** to the higher reading only if its total margin is ≥ 3 × the held-out median per-position margin; otherwise **undecided by this model**. This worker has viewed no image of X 15. The X 15 letters have been examined on Puech's plates (W2F, 7 October) and in the edition literature, and other workers have handled cuts 17–18. The output is a model output, not a reading and not an unused-observation test.

## 8. Outcome labels

- **Obtained**: PASS, P_perm < 0.05, and X 15 scored.
- **Partly**: PASS but P_perm ≥ 0.05 (the pass is not robust to the sample-size bias check), or X 15 not scored for a recorded technical reason.
- **Not obtained**: FAIL. Targets are not scored (`target_rankings4.csv` records NOT RUN). For the target letters the AGENTS.md label stays "not identifiable from available evidence" for this model.

## 9. Why the held-out lines count as unseen for THIS model

- No held-out letter was featurised, viewed or scored before this freeze. TRAIN templates, calibration and every exploratory choice used TRAIN letters only (`x_explore.py` asserts that no TRAIN letter lies on a held-out line).
- Earlier models scored some of these lines: round 1 (I 8, III 3, III 10), B2 (its held-out lines include II 1, II 8, II 10, III 12, IX 2, X 1, X 5, X 10, X 12, XII 1, XII 3, XII 9). Those models used other letter forms and alignment, and their per-line outcomes were not read by this worker (`calibration_rankings*.csv` of round 1 and B2 were not opened). Nothing in this model was fitted or chosen on those results.
- A2 used W2F letters of ב, כ, ה, ח, ת in columns I–X as TRAINING data for its relief rules, and other workers viewed crops of cuts 3, 6, 7 and 8 by eye. Those are other models' exposures. No parameter of this model comes from them.
- The candidate letters are drawn by a seeded rule from the edition confusion table and do not depend on the images.

## 10. Exploratory phase and exposure log (TRAIN only)

**Images viewed by eye (this worker):** two montages of 70 TRAIN letter patches (forms ב כ ו ש ה; channels E and CT; cuts 2, 3, 4, 6, 7, 8, 11, 16, 17, 18), scratchpad `products/B4/x_montage_E.png`, `x_montage_CT.png`. They showed the letters roughly centred in the template box; ב/כ show top and base strokes, ש diagonals. No held-out letter, no target window and no column XII image was viewed.

**Computed, not viewed:** TRAIN patches of 256 letters (`products/B4/train_patches.npz`); placement of all W2F letters; the placement of IX 10 letters relative to CT16 and CT17; the placement of the X 15 target letters (coordinates only).

**Text printed:** TRAIN line candidate pairs (truth/alt letters); ETCBC text of I 11–13, IX 9–11, X 14–16, XII 9–11 (known edition text) and which W2F letters on them place; held-out line identifiers and counts (no held-out text or candidate letters).

**Variants (leave-one-line-out on TRAIN letters; selection metric fixed before the runs: pairwise accuracy truth vs partner over the confusion pairs, weighted by pair rate).** Files `explore/EX_V*.json`. TRAIN-line T (22 lines, E = 2.56 under the exact null) is reported for each but was not the selection metric.

| Variant | Channels | Calibration / shift | Congealing | Weighted pair acc. | ב/כ | ה/ח | TRAIN T |
|---|---|---|---|---|---|---|---|
| V1 | 6 lights + E (gradient magnitude) | z / own | 0 | 0.551 | 0.42 | 0.64 | 3 |
| V2 | 6 lights | z / own | 0 | 0.559 | 0.50 | 0.48 | 5 |
| V3 | E | z / own | 0 | 0.498 | 0.40 | 0.44 | 1 |
| V5 | TB + LR | z / own | 0 | 0.581 | 0.56 | 0.52 | 4 |
| V6 | TB + LR | raw / own | 0 | 0.581 | 0.56 | 0.56 | 2 |
| V7 | 6 lights + TB + LR | z / own | 0 | 0.583 | 0.54 | 0.60 | 3 |
| V8 | TB + LR | raw / shared | 0 | 0.561 | 0.54 | 0.52 | 2 |
| V9 | 6 lights + TB + LR | raw / shared | 0 | 0.583 | 0.60 | 0.52 | 3 |
| V10 | 6 lights | raw / shared | 0 | 0.553 | 0.50 | 0.48 | 7 |
| V11 | 6 lights + TB + LR | raw / shared | 2 | 0.599 | 0.58 | 0.60 | 2 |
| **V12** | **6 lights + TB + LR** | **z / own** | **2** | **0.623** | **0.65** | **0.64** | **4** |
| V13 | TB + LR | raw / shared | 2 | 0.583 | 0.56 | 0.52 | 5 |

("shared": one shift per position, the argmax of the mean NCC map of the forms in the set; "own": each form takes its own maximum.) V1–V3 ran on a 7-channel feature file before TB/LR were added; V4 was not run. The choice V12 is best of 12 on the same TRAIN letters, so its 0.62 is optimistic. Top-1 accuracy over 25 forms is 0.07–0.14 (chance 0.04).

**Design choices not based on scores:** placement margin 0.45 Lh (from placed-letter counts at 0.30/0.45/0.60: 460/436/414); centre (plx, ply) rather than the stroke centroid (W2F found the centroid leaks letter shape); MIN_TRAIN 4; MIN_POS 2; KAPPA 5; shift window ±0.20/±0.15 Lh; 20 px per Lh; template 1.2 Lh; decoy and permutation design.

**Code test before the freeze** (`x_codetest.py`): the scoring, decoy, permutation and per-letter paths of `run4.py` were run on TRAIN items relabelled as held-out with in-sample templates. The numbers mean nothing and are not reported. X 15 letters were placed (coordinates only).

**Expectation recorded before the confirmatory run.** On TRAIN the chosen model reaches about 0.62 pairwise accuracy (optimistic) and T = 4 against 2.56 expected on 22 TRAIN lines (not significant). With per-position accuracy near 0.6, the expected held-out T is about 4–5 against a pass threshold of 5. A pass is possible but not expected.
