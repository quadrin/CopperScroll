# Direction B: analysis by synthesis on the 1988 WSRP multi-light frames — frozen protocol

Frozen 30 October 2026 (PDT) by Claude (worker B, branch `claude/novel-2026-10-30-B`), before any held-out or target score was computed. Everything before this file is EXPLORATORY and is listed in §7.

## 1. Claim tested

A mechanical forward model can tell the edition-agreed reading of a line from close, edition-style confusions of it, using the public USC previews of the 1988 West Semitic Research photographs. Only if it can do so on held-out undisputed lines are the target candidate sets scored, once.

This tests a **reading method**. A target ranking is a reading-level observation from exposed images. It is not an identification, and it changes no rating, outcome-ledger entry or ACTIVE_TEST.

## 2. Inputs (all hashed)

- **Images.** USC Digital Library public previews of the 1988 WSRP film photographs, recto, every frame with a lighting label L/C/R × top/bottom (about 1000 px on the long side; `images/previews/cuts-01-10/`, `images/previews/original-scroll-remaining/`; sha256 per frame in `prep_registration.json`). Frames titled edge, fragments, side or "bot/top ctr" are excluded.
- **Blocked input.** The private full-resolution WSRP TIFFs (Drive `06 Imagery/3Q15 Copper Scroll Zuckerman USC`) are not reachable from this container, and the encrypted repo copies (`private-media/wsrp-1988/*.enc`) need the secret `WSRP_MEDIA_KEY`. They are not used and no decryption was tried.
- **Cut 1** has no frame with a lighting label, so it is not used. Column I is scored on cuts 2–4 only.
- **Registered stacks.** `prep.py` (sha256 `0d52fced5d4a281fcee78b74d333e47f120bcb6368cbb6dc9c6c8992ab0cf8b7`) registers every frame of a cut to the frame with the most SIFT matches (homography, RANSAC 3 px, at least 40 inliers), rotates the strip to vertical and crops it. Private stacks are `/root/novel/private_outputs/B/stacks/cutNN.npz`, with sha256 in `stack_hashes.sha256` (`7c51fd3f5e3898acfbc7b6b4e3a99bdfefd7685085457501d3a493f3ca60338b`). Registration numbers are in `prep_registration.json` (`4f7d83047af75261a07015143ad5e8226af0b103bbeeb87ff954dc725392c11a`).
- **Cut-to-column map** (Puech 2006 radiograph captions, via `research/text/letter_controls/controls_manifest.csv` and the W2F plate index). I: 2,3,4; II: 5,6; III: 7,8; IV: 9,10; V: 10,11; VI: 11,12; VII: 13,14; VIII: 15; IX: 16,17; X: 17,18; XII: 21,22.
- **Text.** ETCBC dss 2.0.1 (`data/scroll-text.js` → `etcbc_lines.json`, `3959751b6d0c2fdcc3f686673ba12c2728f2457d149602996885a66689dceebe`).
- **Glyph templates.** `glyphs.py` → `glyphs.json` (`9a320070084363b3c7223ae30b29d86a2f690ca13defc19b9886f8879df4fefa`).
  - 17 letter forms are the stroke polylines of the scroll's own letters, from the hand tracing of VII 7–11 on the strip 13 photograph (`registration/photo_tracing_strip13.json`), one instance per letter.
  - Logged deviation from "same column": one column (VII) supplies the templates for all columns, because no other stroke-level tracing exists in the repo.
  - ג ז ט נ ס פ צ ך ם ף fall back to skeletonised DejaVu Sans Hebrew glyphs. This fallback is a known weakness of the model.

## 3. Forward model (`model.py`, `191855431575fcfe91a023c57b34527de707ef7355d7cb0b755c755c0b6ed39a`)

- **Surface.** z = smooth curvature − groove. The groove has depth profile U (√(1−u²)) and half-width 0.07 × letter height, at distance d from the glyph skeleton, u = d / half-width.
- **Smooth curvature and corrosion.** Curvature is removed by a Gaussian high-pass (σ = hp × letter height, applied identically to observation and rendering). Corrosion texture is the Gaussian residual.
- **Layout.** Letters are set right to left with inter-letter gap 0.22 and word space 0.45 (letter-height units). Letter height = rho × line pitch.
- **Saw kerf.** The 0.15 mm kerf is 0.44 px at 0.34 mm/px, below one preview pixel, so it is not modelled.
- **Shading.** Lambertian, small slope. Each frame f is modelled as a_f + b_f·∂z/∂x + c_f·∂z/∂y + d_f·groove.
  - (b_f, c_f) is the frame's in-plane light vector; d_f absorbs the dark groove (occlusion or dirt).
  - All four coefficients are fitted per frame by least squares, with the same freedom for every candidate. This is the "estimated light direction" of each frame.
  - Specular term: off.

## 4. Likelihood and registration (`abs_score.py`, `6d0f1362145299bbbcc49f51d4cbd45158f9a105d63a33fa17c70963b3295c61`)

**Per-frame likelihood.** For each frame, a Gaussian residual with fitted variance: log L_f = −(n/2)·log(RSS_f/SST_f) over the band of ±0.62 pitch around the line row. The sum over frames is maximised over the horizontal offset (anywhere along or past the strip) and over the row.

**Registration** is the same for every candidate and does not use the scored line's text.
1. Nominal row y_nom = Hs·(0.05 + 0.9·(l − 0.5)/N). Search window y_nom ± 1.5 pitch, over both 180° orientations.
2. The shared location (orientation, row) is the argmax of the mean of all candidates' score curves.
3. Each candidate then takes its best row within ±0.15 pitch of that location.

**Line score** = sum of strip scores over the column's cuts. Rank 1 = highest. A tie with the truth counts against the truth.

**Frozen parameters** (`frozen_params.json`, `df825c762bb3784b71051744a6cc5f74bc1ab680403fcc8c7d4a06f030d23f39`): prof = U, hw = 0.07, rho = 0.60, hp = 2.5, gap = 0.22, space = 0.45, band = 0.62, WIN = 1.5, LOC = 0.15.

## 5. Calibration lines and candidates (`candidates.py`, `4702a998e6d138bc7d92b48384038deefa48313795ca5a098f80a1dc271988e1` → `calibration_items.json`, `66b0979bb6d0b3334d6fd1d84539046851dd90b50462fbbde0472bc8ff4c7996`)

**Eligible lines** (columns I–X), all of these together:
- no ETCBC flag and no Greek on the line;
- no row of `research/text/edition_confusions/variants.csv`;
- not in `research/text/plate_check.md`;
- not cited in `text/readings.json`;
- not a target line.

That leaves 25 lines. A seeded split (rng 20261030) puts 12 in TRAIN and 13 in HELD-OUT.

**Candidates per line.**
1. The truth (ETCBC) plus up to 5 one-letter substitutions.
2. Substitutions come from the shape pairs with at least 3 places in `edition_confusions/confusions.csv`.
3. They are drawn with weights equal to the pair's confusion rate (rng 20261030 + 100·col + line).
4. A substituted word-final letter takes its final form.

**HELD-OUT lines** (col:line : number of candidates): III 6:6, III 10:6, V 10:6, V 11:6, VI 10:6, VI 12:6, VI 13:6, VII 13:3, VIII 16:5, IX 13:6, IX 16:6, X 2:5, X 4:6.

## 6. Decision rule, failure condition, targets

**Held-out test (exact, one-sided).**
- Statistic: T = number of held-out lines whose truth ranks strictly first.
- Null: T ~ Poisson-binomial with p_i = 1/K_i, the chance of a random ranking (expected 2.40).
- **PASS iff P(T ≥ t_obs) < 0.05**, which here means T ≥ 6 of 13 (P(T ≥ 6) = 0.020; P(T ≥ 5) = 0.073).
- **Failure condition:** T ≤ 5. The held-out undisputed lines then do not pick out their own reading more often than chance, and **the targets are not scored or interpreted** (`target_rankings.csv` records "NOT RUN").

**Targets, only after a PASS**, scored once in this order: IX 10, I 12, VII 11, X 15, and XII 10 last (`targets.py`, `29f5fe8d42688328f9464cddf9dca1adafe093913c6a1596d0e3b00852af885f`).
- **XII 10**: R1 שכנה, R2 שבנה, R3 שבצח, R4 שבינח, R5 שכינה, R6 שכונה, R7 שבצהב (frozen XII 10 protocol, SHA-256 `0e19467c…2c5`). Context: בשית … בצפון כחלת פתח אצפון.
- **IX 10**: כסף מנחה רב (Puech) / מנה חרם (Wolters) / מן החרם (Allegro, Lefkovits).
- **I 12**: ניקרת / מקרת / נקרת.
- **VII 11**: המשמרה / המשטח.
- **X 15**: בים בית חמים של רחיל תחת (ETCBC, Milik) / בים בית המים שלוח ולתחת (Puech's engraved sequence).

Each target ranking is reported with its log-likelihood margins.

**Interpretation (frozen).**
- A target is said to **lean** to its top candidate only if the margin to the runner-up is at least the median absolute truth-minus-best-other margin on the held-out lines. Otherwise it is **undecided by this model**.
- No target result is decisive under the XII 10 protocol, which requires two human readers. These are exposed images, so every target result is exploratory reading evidence, not an unused-observation test.

**Outcomes.**
- **Obtained**: held-out PASS and target rankings produced.
- **Partly**: held-out FAIL, so the model is shown not to read on these previews and targets are not scored.
- **Not obtained**: the run fails to execute.

## 7. Exploratory phase and exposure log

- **Viewed by eye**, for building and debugging only: whole-frame preview UC15246329 (cut 6), crops of cut 5 (UC15245493) and cut 7 (six registered lights, top 340 px), and the mean of cut 5. No target-line crop was viewed. No image of cuts 16–18, 21 or 22 was opened by eye.
- **Computed but not viewed**: registration of cuts 19–23.
- **Tuning**: on TRAIN lines only, 8 settings in 4 grids (`tuning/tune_[ABCD].json`). Train mean reciprocal rank ranged 0.51–0.70; the frozen setting had the best train MRR (0.704, 7 of 12 first).
- **Earlier registration designs**, abandoned on train/feasibility runs:
  - a text-based leave-one-out comb (the scored line's neighbours locate it) was unstable on cut 7 (line argmaxes clustered at the strip ends);
  - an autocorrelation line-pitch estimate gave inconsistent pitches.
  - Both were replaced by the nominal-row window above. No held-out line was looked at to make that choice. Feasibility maps of cut 7 / column III and cut 11 / column VI were computed in the abandoned design. They rendered only the ETCBC text of those columns' lines, including held-out lines, and never any substituted candidate, so they gave no rank information on held-out candidate sets.
- **Text exposure**: the ETCBC text of XII 10 was printed in the terminal while listing columns (known edition text, not an image).
- **Worker A**: neither A's outputs nor their existence was used.
