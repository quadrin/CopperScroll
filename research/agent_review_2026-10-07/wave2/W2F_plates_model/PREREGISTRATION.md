# Pre-registration: letter-pair baseline on the Puech 2006 copy-photo plates (W2-F)

Written 6 Oct 2026, **before any classifier was trained or evaluated on real labels**. The only model-related run before this file was a timing test on random synthetic features (no real data). Up to now the labels have been checked only by eye: the facsimile alignment was verified, and a random sample of 56 photo crops was audited for centring (`work/audit1.png`).

## 1. Question
Can a simple, CPU-only letter model trained on undisputed letters of 3Q15, as shown in the colour photographs of the EDF galvanoplastic copy (Puech 2006 vol. II, pls. CCCLIX–CCCLXXXI odd), tell apart the letter pairs that matter for disputed readings: ו/ר, ח/ה, ח/ת, ב/כ? It must do this on **columns it has not seen**.

## 2. Data (frozen; SHA-256 below)
- Images: plate JPEGs extracted at native resolution (`pdfimages -all`) from the French-edition PDF scan. That scan holds the original CMYK JPEGs (Adobe-inverted, corrected in `scripts/01_convert_plates.py`). The other scan (Poffet copy) is an RGB re-encode of the same pixels: correlation 0.95 with A, lower high-frequency energy.
- Labels: `data/labels_train.csv` holds 1,107 letters. Each is (i) aligned automatically (forced alignment, `scripts/05_align_letters.py`) between the ETCBC transcription and connected components of Puech's facsimile drawing, which is affine-registered onto the copy photograph (ECC ≈ 0.42–0.51; `scripts/03_register_facsimile.py`). (ii) Each word was then **verified by eye** on review sheets (`data/review_decisions.txt`, reviewer = this AI model, non-specialist). (iii) Each letter is unflagged in the transcription and passes the wave-1 T10 "candidate undisputed" rule. (iv) No letter comes from the masked target words, which are the disputed words plus at least one word either side, at X 15, VII 11, IX 7, XII 10, XI 12, VII 14–15.
- Pair counts (non-final forms only; final ך excluded): ו 78, ר 80, ח 50, ה 66, ת 90, ב 100, כ 87. All 12 columns contribute.
- Crops: `data/crops_train_X.npy` (`scripts/08_extract_crops.py`). Each window is 1.0 H wide × 1.25 H high (H = per-column median photo letter height, 42–74 px), resampled to 32 × 40 px. Pixels are background-normalised and z-scored. Each letter has its original window plus 8 augmented windows (shift ±0.1 H, scale ±8 %, rotation ±4°, seed 20261006). The facsimile fixes only the window **centre**, never its size.

```
87f2c09d7590af4b09f22bf4e2c809083452d6b8bdd91c00a738dbe809048d80  scripts/11_evaluate_pairs.py
e8d451ae90f286c8488d9eadee4821e1f2d7523c76b3e5c5034fbf50b8756189  scripts/08_extract_crops.py
2f7931ac2d4fa93caefe46b0e7899d993d02027d62916477e1ebe3b935c19fdd  data/labels_train.csv
24c7eff65c5fc250095432fd43c74d9ea0290f77cd794ad44c9c84f58e1bc56f  data/crops_train_X.npy
96f9f1a59aea761fc70eafa58b7c3128ab25834e854b23eeef297a268a6d497b  data/disputed_centres.json
9fac24a3448e10f62b7495da0be20308c9a2b585aad67ec517597ece3fcb9eef  data/review_decisions.txt
```

## 3. Primary analysis (fixed; `scripts/11_evaluate_pairs.py`)
- Features: HOG (9 orientations, 8×8 px cells, 2×2-cell blocks, L2-Hys), 432 dimensions.
- Classifier: StandardScaler + L2 logistic regression, C = 0.1, class_weight = balanced. No hyper-parameter search.
- Validation: **leave-one-column-out** (12 folds). Training uses the original and 8 augmented windows of every letter in the other 11 columns. Testing uses only the original window of each held-out letter. Predictions from all folds are pooled.
- Metric: balanced accuracy (mean of the two class recalls) at threshold 0.5. AUC, Brier score, ECE (10 bins), per-column accuracy and 95 % bootstrap CIs (letter-stratified and column-level) are also reported.
- Permutation test: 1,000 permutations of the labels **within each column**, each run through the identical LOCO pipeline. p = (1 + #{BA_perm ≥ BA_obs}) / 1001. Seed 20261006 + pair index.
- **Gate (per pair): BA ≥ 0.85 AND permutation p < 0.01.** Holm-adjusted p over the 4 pairs is also reported. A pair that passes the gate but fails Holm at 0.01 is flagged.
- All four pairs are reported whatever the outcome. No pair, feature, crop size or C value will be changed after seeing results. Any re-run with changes is labelled exploratory.

## 4. Application to disputed letters (only for pairs that pass)
- Targets and window centres, fixed by eye on the copy photo before evaluation (`data/disputed_centres.json`): X 15 (ו/ר), VII 11 (ח/ה), XI 12 (ח/ת), XII 10 (ב/כ), VII 14 (ב/כ).
- Final model: same pipeline, trained on all columns **except the target's column**.
- Output: P(second letter of the pair). A raw value and a Platt-calibrated value are given; Platt scaling is fitted on the out-of-fold scores of the other columns. A sensitivity range is given over 9 centre shifts (±0.1 H grid). These are reported as model-evidence likelihoods under heavy caveats (damage at the disputed loci, cursive waw-like reš, ḥet/he drawn alike), never as readings.
- If a pair fails the gate, its disputed letter is reported as "not identifiable by this model". No probabilities are shown for it, not even exploratory ones.

## 5. Secondary analyses (exploratory, declared now, not gating)
1. Raw-pixel features + the same logistic regression (control).
2. A small CNN (PyTorch, CPU): 2 conv blocks + linear head, on-the-fly augmentation, same LOCO folds. BA only; no permutation test unless cheap.
3. A 7-class (ו ר ח ה ת ב כ) multinomial logistic regression on HOG, LOCO accuracy, for context.
4. A blind by-eye test by the same AI model on a random subset of pair crops (labels hidden), to give a non-model reference.

## 6. Known limitations, stated in advance
- Labels depend on Puech's facsimile for the alignment, checked by one non-specialist AI reviewer. The audit was not blind.
- Images are printed reproductions of a cast (the EDF copy) of corroded copper, single-light, JPEG-compressed (quantisation tables of mean ≈ 42).
- Disputed letters are damaged by definition. Training letters are mostly undamaged, so even a passing model may not transfer.
- Neighbouring letters intrude into fixed windows, especially around narrow letters such as ו.
