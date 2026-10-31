# Direction B2, analysis by synthesis on the full-resolution 1988 frames: frozen protocol (NEW MODEL)

Frozen 31 October 2026 by Claude (worker B2, branch `claude/novel-2026-10-31-B2`), before any held-out or target score was computed. Everything in §8 is EXPLORATORY and used TRAIN lines only.

## 0. Novelty gate (what differs from the 30 October run)

- Source: the full-resolution USC 1988 West Semitic Research Project (WSRP) TIFF copies in the private bucket, read with `hexview.py`. Round 1 used the 1000 px public previews (20–30 px per letter). This run reads full resolution and averages it to half scale: about 77 px per cm, letters about 50–75 px high.
- Letter forms: learned for each column and each light class from aligned TRAIN-line patches, shrunk toward a scroll-wide mean and then toward a rendered V-groove template. Round 1 used one column-VII tracing for every column.
- Scoring: one candidate-blind alignment of the letters shared by all candidates, then letter classification at the disputed positions, each letter scored as a z-score against its own pooled background distribution. Round 1 slid one fixed-layout rendering of each candidate along the strip.
- Chance baseline: exact for the star-shaped candidate sets (truth plus one-letter neighbours). The round-1 baseline 1/K is too high for such sets (§5).
- Calibration: a word-level "undisputed" rule gives 33 held-out lines in columns II, III, V, IX, X, XI and XII (round 1: 13 lines). The 25 round-1 calibration lines are exposed; those that remain eligible are TRAIN only.
- This is a new model with a new frozen specification. The round-1 result (4 of 13, p = 0.21) stands and is not rescued.

## 1. Claim tested

A forward model built from the scroll's own letter appearance can tell the edition reading of a line from close, edition-style one-letter confusions of it, in the 1988 WSRP multi-light photographs at full-resolution source.

This tests a reading method. It is not an identification. It changes no rating, outcome-ledger entry, ACTIVE_TEST, OPEN_QUESTIONS or atlas data.

## 2. Inputs (SHA-256)

- Reader: `hexview.py` from `gs://copper-scroll-cog-1030/tools/hexview.py`, SHA-256 `56b21cb0d32b7d3caf1fe1f130493791898d768c087964fe5a745d0dc7630236` (observed; the store note gives no hash). Store index built 05:07:28 UTC, 31 October 2026.
- Images: bucket items `usc:DSS_3Q15_CT<n>_<code>_T`, cuts 2–8, 10, 11, 16–23 (cuts 1, 9, 12–15 are absent). Light codes used: RCT RLT RRT RCB RLB RRB (raking light from centre, left or right; top or bottom), and RT RB on cuts 4, 17 and 21. Not used: FRS (CT10), RET REB RFR (CT16), RBC RCS RTC (CT23). 86 frames on 17 cuts. Item keys, tile sizes, read boxes, rotation angles and crop sizes: `prep2_frames.json` (SHA-256 in §2a). The private crops `SP/products/B2/strips/ctNN.npz` (SP = this session's scratchpad) have their SHA-256 in that file.
- Text: ETCBC dss 2.0.1 lines, `etcbc_lines.json` (same file as round 1).
- Glyph skeletons for the rendered prior: `glyphs.json` (same file as round 1: 17 letters from the strip-13 tracing of column VII, 10 DejaVu Sans skeleton fallbacks).
- Column → cuts (cuts present only): I: 2 3 4 (cut 1 absent); II: 5 6; III: 7 8; IV: 10 (9 absent); V: 10 11; VI: 11 (12 absent); VII and VIII: none (13–15 absent); IX: 16 17; X: 17 18; XI: 19 20 21; XII: 21 22 23. Sources: Puech 2006 radiograph captions via `research/text/letter_controls/controls_manifest.csv` (columns I–X); `research/text/plate_check.md` (cuts 19–23 = columns XI–XII; XII 10 at the 21/22 cut).
- Edition-confusion data: `research/text/edition_confusions/variants.csv`, `confusions.csv`; `research/text/plate_check.md`.

### 2a. Hashes of the frozen files

| File | SHA-256 |
|---|---|
| `prep2.py` | `2dcc7841972eb0724036db87b890a9589a3401332bf146c5475a6b7efc8161da` |
| `prep2_frames.json` | `ba7e2c288c32193b1b705e9abdba376a6799654433f9a6a0887bdb1e412fad60` |
| `items2.py` | `229b339914718cbf191916dc521e2bc47be8ee00aba92b0d88231fc7aab06928` |
| `calibration_items2.json` | `c4208d4770c63d3978db4ee7fa42ce656b2dd6deb81732b697827528ec58bca5` |
| `etcbc_lines.json` | `3959751b6d0c2fdcc3f686673ba12c2728f2457d149602996885a66689dceebe` |
| `glyphs.json` | `9a320070084363b3c7223ae30b29d86a2f690ca13defc19b9886f8879df4fefa` |
| `model2.py` | `27ae9fb5dd93bfe4c652512ae7f16b974e6c0d12da4a8a50f9588b89c567b1d3` |
| `run2.py` | `cff30e42d81bd8fd39c5ac5d7f7cd160ba995af3bfe800b1694ab9c4430f7446` |
| `targets2.py` | `6b7504df2dacc631a544f3fee72e08709eac2ce37266b8f2a955f281203f7d74` |
| `frozen_params2.json` | `f68bdc6581421f1cd47c91ffc70f6632d1d33892aca975f72463aa3c66590cea` |
| `research/text/edition_confusions/variants.csv` (repo) | `07be73c9c02a04f5d5214143e98205608b8325b8968da4431d43be3f7baf8271` |
| `research/text/edition_confusions/confusions.csv` (repo) | `765ebdca01c9f4a710223c0d1498b07569f62647537b8861e7d9b9c2fdd5e5ce` |
| `research/text/plate_check.md` (repo) | `7d528ed4778273ad0c8e84e3fc22540865259ec1c3afa47a01a1039de8333385` |
| `research/text/letter_controls/controls_manifest.csv` (repo) | `e2da8dbbfed4b4355cf9acb6d33c580ab41a12354c6feb50adcfa8e50a677b7d` |
| `research/agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md` (repo) | `0e19467c618f80438c12445b7380f77f5c59b7fe241da9c80878601e2e26a2c5` |

## 3. Forward model (`model2.py`, `run2.py`)

- **Per-frame processing.** Frames are not registered to each other. Across lights, SIFT on the corrosion texture found 0–108 inliers and silhouette ECC reached only 0.82–0.86. Each frame is rectified to a vertical strip (`prep2.py`) and scored on its own. Scores are summed over frames.
- **Normalised image.** z = clip((I − G(I)) / sqrt(G((I − G(I))²)), −3, 3), G = Gaussian of σ = 1.2 Lh; zero outside the strip mask; then σ = 1 px smoothing. Lh = letter height = 70 work px.
- **Rendered groove prior.** Skeleton polylines drawn at Lh; depth profile V-shaped, h = −max(0, 1 − d/(0.08 Lh)), d = distance to the skeleton. Shading for light class direction (lx, ly): −(∂h/∂x lx + ∂h/∂y ly)/0.08 + 0.5 h. Light classes: T (RCT, RT) (0, −1); B (RCB, RB) (0, 1); LT (−0.707, −0.707); RT (0.707, −0.707); LB (−0.707, 0.707); RB (0.707, 0.707). Template size 1.3 Lh × (glyph width × Lh + 4 px).
- **Learned letter forms (same column where possible).** Two Viterbi passes on all TRAIN lines. Pass 1 aligns each TRAIN line's ETCBC text with the rendered templates at its best row in a ±1 pitch window around the nominal row; pass 2 realigns with the pass-1 templates. Aligned patches are normalised and summed per (column, light class, letter) and per (all columns, light class, letter). T_all = norm(Σ_all + 3 T_render); T_col = norm(Σ_col + 3 T_all). A letter without TRAIN patches in a column takes T_all, or T_render if it has none anywhere. The learned templates are image-derived and stay private (`SP/products/B2/templates_frozen.npz`; SHA-256 reported with the result).
- **Letter score.** For a frame, NCC map of each template over the strip (OpenCV TM_CCOEFF_NORMED). The map is max-pooled over the allowed freedom (±0.15 Lh vertically, ±0.1 Lh horizontally). μ_c and σ_c are the mean and SD of the pooled map over the strip interior. Letter score of c at (x, y) = (pooled NCC − μ_c)/σ_c − TAU, TAU = 0. Standardising the pooled map gives every letter the same null mean and SD after the max, so a sharp template's rougher NCC map gains nothing.
- **Local alignment (used for learning and for registration).** Best local alignment of a string read right to left: free start and end in the string; letters placed leftward with gaps in [−0.1, 0.6] Lh inside a word and [−0.1, 1.6] Lh across a word space (gap step 2 px); a run continues only while its cumulative score is positive.
- **Scoring rule for the held-out test: fixed shared alignment, then letter classification** (`score_item_fixed` in `run2.py`).
  1. Common string: the letters shared by all candidates of the line; at each position where candidates differ, a wildcard with score 0 and width = mean width of the alternative letters.
  2. In each frame of each cut of the column, the common string is aligned at every row of the window y_nom ± 1.0 pitch (step 6 px); y_nom = H (0.05 + 0.90 (l − 0.5)/N), pitch = 0.90 H/N, N = the column's ETCBC line count, H = strip height in the frame. The row with the highest common-string score is used. This registration is the same for every candidate (it never sees the differing letters).
  3. For each wildcard position inside the aligned run, each candidate's letter c takes its letter score (pooled, so already the maximum over ±0.1 Lh and ±0.15 Lh) at the left edge that centres c on the wildcard. A wildcard outside the run gives 0 to every candidate.
  4. Candidate score = sum of its letter scores at the wildcard positions, over the column's cuts and frames. The decision statistic is in §5.
- Reason for this rule (EXPLORATORY, §8): scoring each candidate by its own free alignment (runs E1–E3) lets alignment flexibility differ between candidates. The fixed rule compares only letter identity at one shared position.
- **Frozen parameters** (`frozen_params2.json`): LH 70, HT 1.3, HW 0.08, PROF V, GAM 0.5, SIGN +1, GMIN −0.1, GMAX 0.6, GWORD 1.6, DY 0.15, TAU 0, KS 3, ROWA 0.05, ROWB 0.90, WIN 1.0, GSTEP 2, YSTEP 6, NPASS 2. Set a priori except: TAU 0.5 → 0 (chosen from run coverage in E4, not from a truth score) and learned (NPASS 2) over rendered-only (NPASS 0) templates, chosen on the TRAIN position-level p (§8).

## 4. Calibration lines, split and competitors (`items2.py` → `calibration_items2.json`)

- **Undisputed word**: no ETCBC flag, not Greek, no row of `variants.csv` on that word (a word span such as "1-2" marks every word in it), at least 2 letters.
- **Eligible line**: column has a cut present; no Greek on the line; not in `plate_check.md`; not a target line (I 12, VII 11, IX 10, X 15, XII 10); at least 6 letters; at least 3 letters in undisputed words. (Round 1 required a whole line without any `variants.csv` row; that leaves 15 lines of ≥ 6 letters here, too few.)
- **Split**: round-1 calibration lines → TRAIN (14 remain eligible). Columns with a missing cut (I, IV, VI) → TRAIN only. The rest (columns II, III, V, IX, X, XI, XII) sorted by (column, line), permuted with `numpy.random.default_rng(20261031)`; the first half (floor) TRAIN, the rest HELD-OUT. Result: 76 TRAIN lines (33 + 29 partial-column + 14 round-1), 33 HELD-OUT lines.
- **HELD-OUT lines** (line: number of candidates): II 1:6, II 5:6, II 6:6, II 8:6, II 10:6, II 11:6, II 13:6, II 14:6, III 2:6, III 9:6, III 12:6, V 2:6, V 5:6, V 9:6, IX 2:6, IX 3:6, IX 5:6, IX 17:6, X 1:6, X 5:6, X 9:6, X 10:6, X 12:6, XI 1:4, XI 2:6, XI 10:6, XII 1:6, XII 3:6, XII 4:6, XII 5:6, XII 8:6, XII 9:6, XII 13:4.
- **Competitor rule**: the ETCBC truth plus 5 one-letter substitutions at letter positions inside undisputed words. Substitutable pairs: `confusions.csv` rows with count_places ≥ 3. All (position, partner) options are enumerated in reading order; 5 are drawn without replacement with weights equal to the pair rate, `default_rng(31102026 + 100·col + line)`. A substituted word-final letter takes its final form. Words that are not undisputed keep their ETCBC text in every candidate.

## 5. Test statistic, chance baseline, pass mark, failure condition

- **Why the round-1 baseline is not used.** Each line's candidate set is a star: the truth plus competitors that each differ from it at one letter. Scores add over letters. With no information, the truth beats competitor j with probability 1/2 at each position, so it ranks first with probability about (1/2)^5, not 1/K. The round-1 baseline 1/K was therefore too high (conservative). On TRAIN lines (§8) this structure, plus exact ties for competitors whose letter was never placed, ranked the truth below 1/K chance.
- **Observed competitor.** A competitor is observed if its substituted position lies inside the shared aligned run in at least one frame of one cut. The run is fixed before the differing letters are looked at, so this is candidate-blind. An unobserved competitor ties exactly with the truth and carries no evidence. It is left out.
- **Statistic (primary).** T = number of HELD-OUT lines with at least one observed competitor whose truth strictly outscores every observed competitor.
- **Chance baseline.** Under exchangeable letter scores, line i has p0_i = product over its observed positions of 1/(m+1), m = number of competitor letters at that position (competitors at the same position share the true letter's score). T is Poisson-binomial with these p0_i, computed exactly at run time from the observation pattern.
- **Pass mark.** PASS iff (a) at least 10 HELD-OUT lines have an observed competitor, and (b) the exact one-sided P(T ≥ t_obs) < 0.05.
- **Failure condition.** Otherwise FAIL: the held-out undisputed lines do not rank their own reading first more often than chance (or too few lines are observed to tell).
- **Secondary (registered, no decision):** W = number of observed positions where the true letter strictly outscores every competitor letter there; null Poisson-binomial with 1/(m+1); exact one-sided p. Also reported: the rank with ties counted against the truth (round-1 style), and the median |truth − best other| margin over observed lines.

## 6. Targets (`targets2.py`)

- **Scored only if the held-out test passes.** On FAIL, `target_rankings2.csv` records NOT RUN and no target is interpreted.
- If PASS, scored once with the frozen templates, in this order: IX 10 (D1 Puech מנחה רב / D2 Wolters מנה חרם / D3 Allegro, Lefkovits מן החרם; cuts 16, 17), I 12 (ניקרת / מקרת / נקרת; cuts 2–4, cut 1 absent), X 15 (ETCBC/Milik חמים של רחיל תחת / Puech המים שלוח ולתחת; cuts 17, 18), XII 10 last (R1–R7 of the frozen XII 10 protocol, SHA-256 `0e19467c618f80438c12445b7380f77f5c59b7fe241da9c80878601e2e26a2c5`; context בשית … בצפון כחלת פתח אצפון; cuts 21–23). VII 11 cannot be scored (cuts 13–14 absent).
- Target scoring rule (candidates differ in length, so the calibration rule is extended, not changed): the words shared by all candidates form the common string; the disputed span is one wildcard block of width = mean candidate-span width plus the frozen gaps. The common string is aligned and the row chosen exactly as in §3 step 2. Each candidate's disputed span is then scored by local alignment restricted to the band columns between the aligned context letters on its two sides (if a side is outside the run: 1.5 × the block width from the other side). Candidate score = sum over cuts and frames. This code is written only if the held-out test passes, follows this paragraph, and is committed with its hash before it is run. The frozen `run2.py targets` writes NOT RUN on FAIL and stops with an error on PASS until that code exists.
- A target **leans** to its top candidate only if its margin over the runner-up is at least the median |truth − best other| margin on the observed held-out lines; otherwise it is **undecided by this model**.
- Every target output is a model output on exposed images, with its uncertainty, not a reading. The XII 10 images were released by the owner on 30 October and are exposed; IX 10 on CT17 was read by eye on 30 October (branch `claude/ix10-ct17-qumran-2026-10-30`). No target result is an unused-observation test, and none is decisive under the XII 10 protocol, which requires two human readers.

## 7. Outcome labels

- **Obtained**: held-out PASS, and target rankings produced under §6.
- **Partly**: held-out PASS but a target could not be scored for a recorded reason, or the run completed for only part of the held-out lines for a recorded technical reason.
- **Not obtained**: held-out FAIL. Targets are then not scored. The AGENTS.md label for the reading method on these images is then "not identifiable from available evidence" for the target letters by this model.

## 8. Exploratory phase and exposure log

All runs below used TRAIN lines only. No held-out candidate set was scored before the freeze. Held-out line texts were not printed or viewed.

**Images viewed by eye (building and debugging only; no letter was read):**
1. Cut 7 (column III), all six frames, whole-frame overview at 1/10 scale.
2. Cut 7 RCT, whole strip at 1/4 scale.
3. Cut 7 RCT, full-resolution box x 1000–2150, y 1500–2700 at 0.6 scale (column III, about lines 5–9; it may include held-out III 9). Viewed before the split existed.
4. Cut 7, six rectified strips side by side at 1/8 scale.
5. Learned column III templates (means of TRAIN-line patches) next to the rendered templates, twice (before and after the font-glyph fix).
No image of cuts 16–23 (columns IX–XII) or of any target line was opened by eye.

**Computed, not viewed:** strip crops of all 17 cuts (`prep2.py`); row-profile autocorrelation on cuts 5 and 7 (line pitch about 150–160 work px, autocorrelation 0.07–0.17); the alignments of the exploratory runs.

**Text printed:** ETCBC text of XII 9–11, IX 10, I 12, X 15 (known edition text); the TRAIN texts of column III.

**Design steps and exploratory runs (TRAIN only; fold 0 = templates learned on half of the 76 TRAIN lines, the other half scored):**
- Cross-frame registration was tried and dropped: SIFT on the strip found 0–108 inliers between lights; silhouette ECC reached 0.82–0.86 for side lights.
- E1 (raw NCC − 0.10, free alignment per candidate) and E2 (TAU 0.2, KS 1, U profile): stopped after 3 and 1 lines. A bug was then found: the 10 font-fallback glyphs (point clouds) rendered blank. Fixed.
- E3 (z-scored NCC, free alignment per candidate): truth ranks 4, 5, 2, 6, 3, 5 of 6 on 6 lines. Stopped.
- E4 (fixed shared alignment, TAU 0.5): 18 lines; truth first on 2; 9 margins exactly 0 because the substituted position was outside the shared run. TAU set to 0 so that runs span the visible line.
- E5 (TAU 0): 30 lines; truth first on 0; 11 exact ties; MRR 0.263.
- Pooled standardisation added (letter score standardised after the max over the allowed shifts).
- E7 (pooled, rendered templates only, round-1 statistic): truth first on 1 of 38, MRR 0.242.
- Diagnosis: the below-chance ranks come from the evaluation, not from the images. The candidate set is a star around the truth, so with no information the truth is first with probability about (1/2)^5, and exact ties for unobserved competitors were counted against the truth. The statistic in §5 replaces the round-1 baseline.
- E9 (rendered only, NPASS 0, §5 statistic): 27 observed lines, T = 4 against 3.66 expected (p = 0.51); W = 31 of 77 positions against 35.4 expected (p = 0.87). The corrected null is calibrated on TRAIN.
- E8 (learned same-column templates, NPASS 2, §5 statistic): 26 observed lines, T = 4 against 3.63 expected (p = 0.51); W = 38 of 75 positions against 34.5 expected (p = 0.24).
- **Choice (the only score-based choice):** learned templates (E8) over rendered-only (E9), by the smaller TRAIN position-level p (0.24 against 0.87). TAU 0.5 → 0 was chosen from run coverage (E4), not from a truth score. All other parameters were set a priori.
- Files: `explore/E7.json`, `explore/E8.json`, `explore/E9.json` (per-line TRAIN results). E1–E6 logs were not written to JSON (runs stopped); their numbers are above.

**Expectation recorded before the confirmatory run:** on TRAIN, the frozen model shows no line-level signal (T = 4 against 3.6) and a weak, non-significant position-level tilt. A held-out PASS is therefore not expected.

**Other workers' outputs (A2, C2, E):** not used.
