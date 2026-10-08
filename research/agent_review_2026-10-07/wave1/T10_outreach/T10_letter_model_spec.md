# T10 — Technical specification: a letter-shape model for disputed readings in 3Q15

Status: specification. The proof of concept (§0.2) shows that openly licensed images are not enough; this spec says what data, labels, model and tests a real attempt needs, and how its output would be used on the 30 lines of `tables/plate_check.csv`.

## 0. Evidence base for this spec

### 0.1 Images available now (checked 6 Oct 2026)

Openly licensed (Wikimedia Commons; licence, size and author from the Commons API; full table in `data/commons_copper_scroll_images.csv`; EVIDENCE):

| Commons file(s) | Size (px) | Licence / author | Content | Letter-shape use |
|---|---|---|---|---|
| The Copper Scroll 03, 04, 05, 06 | 5552×7408 to 9616×7216 | CC BY-SA 4.0, Mohammad hajeer, 12 Jul 2026 | 3–5 original strips per frame, through the display glass (e.g. 05 = strips 11 and 10) | poor: glare, curvature, corrosion; strokes not separable by eye |
| Strip 11, Strip 13, Strip 15, Strips 1 and 2, overview, "Strip … Amman" (+crop) | 1346×3638 to 5254×3691 | CC BY-SA 4.0, Osama Shukir Muhammed Amin, 2018–2020 | single strips, close | poor: near-saturated glare 2–8% of pixels (`data/image_audit.csv`) |
| Part of Qumran Copper Scroll | 903×1379 | tagged "Public domain", author "na", date "na" | photograph of the EDF copy, right half of column I | best contrast; ~50 px letter height; licence doubtful (probably scanned from a publication — INFERENCE) |
| Part of Qumran Copper Scroll (2) | 903×1104 | same | EDF copy, another column (unidentified) | ~25–30 px letters; same doubt |
| Fac-similé … (Louvre, AO 31164) | 2112×2816 | "Public domain" (uploader) | 1997 facsimile in 3 pieces | context only |

Download note: originals from upload.wikimedia.org returned HTTP 429 (Retry-After 600 s) from the shared IP; 3840-px thumbnails were fetched instead. For files narrower than 3840 px the server returned upscaled thumbnails (no added detail). Only `Part_of_Qumran_Copper_Scroll.jpg` is the SHA-1-verified original.

Restricted or unverified:
- USC Digital Library (WSRP; InscriptiFact closed): 1988 Zuckerman photographs of the originals, facsimile photographs, static RTI posters; "for study purposes only" (https://dornsife.usc.edu/wsrp/for-scholars/). The project already holds 942 previews (1,000 px high) and has asked WSRP for masters.
- Leon Levy DSS Digital Library: a manuscript page "3Q Copper Scroll" exists at https://www.deadseascrolls.org.il/explore-the-archive/manuscript/3Q15-1 (© IAA), but its content is script-rendered; whether it shows PAM negatives could **not** be verified.
- Manchester Museum Allegro archive (via DQCAAS): 720-px previews, teaching/non-commercial use; high resolution via the University. Brill microfiche *The Allegro Qumran Collection* (1996), "nearly 1500" photographs including a Copper Scroll group (https://www.johnallegro.org/?p=85).
- Published plates (DJD III 1962; Puech 2006 vol. II; *Copper Scroll Studies*): publisher copyright.
- 3D: Facsimile Editions scanned the EDF electroformed copies, not the originals, and "EDF-Valectra only reproduced the front of the three plates" (https://facsimile-editions.com/cs/). No 3D or RTI data of the original segments was found.
- Jordan Museum: no image portal; website "going through re-development" (https://jordanmuseum.jo/en). ÉBAF holds one of the four EDF copies, plus photographs of the replica and EDF X-rays used for the decipherment (https://www.ebaf.edu/?p=28351).

### 0.2 Proof-of-concept result

- Data: `Part_of_Qumran_Copper_Scroll.jpg`. 19 letters were boxed by eye on undisputed words (בחרובא without its disputed fourth letter, המעלות, אמות, שש, גבה, שני) by a non-specialist annotator (an AI model). Confidence grades: 1 high, 9 medium, 9 low (`data/poc_col1/letter_boxes.json`; overlays in `data/poc_col1/grid/ov_*.png`).
- Method (`scripts/letter_poc.py`): HOG or raw-pixel features on contrast-normalised 40×40 crops; leave-one-out 1-NN (cosine); 5,000-shuffle label permutation test.
- Result: HOG 2/12 correct (0.17; permutation mean 0.08; p = 0.28); pixels 0/12 (p = 1.0). With only the high- and medium-confidence letters, a single class (ב, n = 3) can be tested. Nearest neighbours are mostly other classes (`data/poc_col1/results/poc_results.json`).
- Segmentation: background-normalised thresholding yields one-sided, fragmentary strokes (the shadowed groove wall; `data/poc_col1/binary_q0.12_s6.0.png`). Vertical-profile splitting did not find the letter gaps.
- Reading: no evidence of separability with these images and labels. This is a negative result about the open data, not about any disputed reading. INFERENCE (high): lighting-independent surface data (RTI normals, 3D curvature) is needed, as in 3D cuneiform work.

## 1. What the model is for, and what it is not for

- **For**: given an image region at a disputed locus, estimate how well the visible marks fit each **edition alternative** (e.g. ו vs ר at X 15), as a likelihood ratio learned from undisputed letters of the same scroll, with stated uncertainty. Also: whether a stroke is present at all in a given gap (IX 7, XII 10).
- **Not for**: producing a new transcription, choosing a reading on its own, or reading the Greek groups (only seven groups exist; there is no training set). Its output goes to the blind panel (T13) as one more piece of evidence.

## 2. Why ink-manuscript methods do not transfer directly

- Popović, Dhali and Schomaker (2021) binarise ink traces with BiNet and then compare allographic (Kohonen self-organising map) and textural (Hinge) features across 54 columns of 1QIsaa, using images "from 600 by 600 pixels to 2800 by 3400 pixels" and IAA multispectral images; they caution that "pattern recognition and artificial intelligence techniques do not give certainty of identification but statistically proven probabilities" (*PLOS ONE*, 2021, doi:10.1371/journal.pone.0249769). EVIDENCE.
- The "Enoch" model (Popović et al., *PLOS ONE*, 4 June 2025, doi:10.1371/journal.pone.0323185) used the same feature families with Bayesian ridge regression on 24 radiocarbon-dated manuscripts (75 images), because the small dataset "precluded deep learning"; cross-validated MAE 27.9–30.7 years. EVIDENCE. Lesson: with tens of training points, use simple features and simple models, and validate by leave-one-out.
- Copper Scroll letters are **punched/engraved grooves** in a corroded copper surface. In a single-light photograph a groove appears as one shadowed wall and one lit wall, so binarisation keeps only shadows. The POC binarisation of the column I copy photograph shows exactly this: fragmentary, one-sided strokes (`data/poc_col1/binary_q0.12_s6.0.png`). INFERENCE (high).
- 3D-script precedent: Stötzner, Homburg and Mara (ICCV 2023, arXiv:2308.11277) detect cuneiform signs using "Phong-shaded 3D models, and photographs as well as illumination augmentation" and GigaMesh's MSII curvature renderings, transferring annotations from 3D renderings to photographs (HeiCuBeDa/MaiCuBeDa, "around 500 annotated tablets"). EVIDENCE. This is the closest model for 3Q15: train on lighting-independent surface geometry, augment with synthetic relighting, and apply to whatever photographs exist.
- Tooling: GigaMesh (Forensic Computational Geometry Laboratory) is open-source mesh software for inscribed objects. It provides MSII curvature visualisation and unwrapping, and its group publishes the HeiCuBeDa/MaiCuBeDa cuneiform datasets (https://gigamesh.eu/). EVIDENCE. Stroke-order methods (RTI/PTM superimposition; microscopy of intersecting incisions) are cited in `drafts/T14_T15_T16_jordan_imaging_proposal.md`, WP2.
- Text-only models: Ithaca (Assael et al., *Nature* 603:280–283, 2022) restores and attributes Greek inscriptions from text only (62% top-1 restoration; 71% geographic attribution); Aeneas (Assael et al., *Nature* 645:141–147, 2025, doi:10.1038/s41586-025-09292-5) adds images for Latin inscriptions (geographic attribution 72% with multimodal input; trained on >176,000 inscriptions). EVIDENCE (Nature page; DeepMind blog). These rely on large corpora; 3Q15 is a single object of ~2,900 letters (`data/inventory_class_counts.csv`), so a language prior from them is not available for this Mishnaic-Hebrew list text. INFERENCE (high).

## 3. Data needed (in order of availability)

| Tier | Source | What it gives | Rights | Status |
|---|---|---|---|---|
| 0 | Wikimedia Commons photographs (§0.1) | high-pixel but low-contrast views of the originals through glass; one copy photograph of part of column I at ~50 px letter height | CC BY-SA 4.0; two copy photographs tagged "Public domain" with author "na" (doubtful) | **downloaded**; insufficient (POC) |
| 1a | Puech 2006 vol. II plates (copy photographs ~1,400 × 1,800 px per column; radiographs ~400–800 px per strip) | lighting-fixed copy relief; radiographic groove depth | publisher copyright; study use | already used by the project |
| 1b | USC Digital Library, WSRP 1988 photographs (originals recto/verso, 3 rotations × top/bottom light; facsimile photographs; static RTI posters) | paired lighting on the originals | "for study purposes only. Permission to publish must be obtained in writing from WSR and collaborating institutions" (https://dornsife.usc.edu/wsrp/for-scholars/) | 1,000-px previews held by the project; master files requested |
| 1c | DJD III (1962) photograph plates; Allegro photographs (Manchester Museum) | pre-1990s state, near saw cuts | publisher / museum permission | partly held |
| 2 | New RTI and 3D scans of the 23 segments and the Amman EDF copy (T14) | normals, curvature, groove depth; independent of lighting | DoA / Jordan Museum | **not yet requested** |

Minimum for a real test: Tier 1a + 1b at full resolution for the columns containing the disputed loci. Tier 2 is what makes a model trustworthy.

## 4. Labelling plan

1. **Candidate undisputed letters.** From the project transcription (`atlas_text.json`, Abegg/Bowley/Cook ETCBC dss 2.0.1) take letters with no uncertainty/reconstruction flag, and drop any word subject to a consonantal dispute in `readings.json` (script: `scripts/letter_inventory.py`). Result: **2,370 of 2,939 letters**; per-class counts in `data/inventory_class_counts.csv`. Rare classes: ט 4, ץ 2, ך 6, ג 25, ז 27 — too few to model alone.
2. **Human pass** over the candidate list: also drop letters within one letter-width of a saw cut, crack or fold, and any letter the three editions read differently even if `readings.json` does not list it (that file covers selected disputes only).
3. **Boxes and registration.** Two annotators independently draw polygons on each image series; accept a letter when IoU ≥ 0.5, otherwise adjudicate. Each box carries (column, line, character index, image ID, segment number, lighting). Original-segment boxes are registered through the EDF copy, which is a cast of each segment, and checked against the adjacent Hebrew (the project's own rule: no target box from edition layout alone).
4. **Masking.** During annotation, the 30 plate-check loci and one letter on each side are masked, so annotators never label disputed material.
5. **Stratification.** Record column and sheet for each letter; Tov proposes several hands (*Copper Scroll Studies* pp. 288–290, as recorded in `phase4_summary.md`), so class models must be checked for hand differences.
6. **Extra classes.** "Blank corroded surface" and "crack/saw-cut edge" patches (for stroke-presence questions); numeral signs from undisputed sums (for VII 16, IX 6, X 16 and the unresolved sums).

## 5. Model

- **Inputs per letter**: aligned patches from each available modality (copy photograph; radiograph; WSRP top/bottom-light pair; later RTI normal map and 3D curvature/depth). Missing modalities are allowed.
- **Baseline** (required, runs on CPU): HOG + contour (elliptic Fourier) + skeleton features → k-NN and linear SVM. The POC code (`scripts/letter_poc.py`) is this baseline.
- **Main model**: a small CNN, or frozen self-supervised vision features with a linear head, trained with lighting augmentation (synthetic relighting of 3D/RTI data, as in Stötzner et al. 2023) and elastic deformation (as in Popović et al. 2021). Class-balanced sampling; pairwise heads for the confusable pairs.
- **Calibration**: temperature scaling on held-out folds; report reliability diagrams.
- **Output at a disputed locus**: log-likelihood ratio between the edition alternatives, with a bootstrap interval over training letters and over box jitter (±3 px), plus the nearest undisputed exemplars shown side by side.

## 6. Evaluation (fixed before any disputed locus is scored)

- **Leave-one-out** on undisputed letters (as requested) — and, because neighbouring letters share lighting and damage, also **leave-one-line-out** and **leave-one-column-out**. The column-out score is the one that counts.
- Metrics: top-1 accuracy; per-class recall; balanced accuracy and calibration (Brier score, ECE) for each confusable pair: ו/ר, ח/ה, ח/ת, ב/כ, ו/ד, מ/ט, ט/ס, א/ג, י/ו.
- **Damage-matched test**: accuracy on undisputed letters that lie in damage comparable to the disputed loci (near cracks or cuts), because disputed letters are damaged by definition.
- **Permutation control**: label-shuffle test as in the POC; the model must beat it with p < 0.01.
- **Gate (pre-registered)**: a pair model may be applied to a disputed locus only if its column-out balanced accuracy is ≥ 0.90 and ECE ≤ 0.05 on damage-matched letters of that pair. Otherwise the locus is reported as "not identifiable by the model".
- **Human comparison**: model vs blind panel (T13) on the control items.

## 7. Applying it to `plate_check.csv`

| Line (entry) | Question | Model task | Training support (undisputed instances) | Expected usefulness |
|---|---|---|---|---|
| X 15 (49) | ו vs cursive ר after של | pair LR ו/ר | ו 198, ר 146 | **Good candidate**; reports which population the stroke resembles; cannot exclude Puech's waw-like reš |
| VII 11 (31) | מ vs ט; ח vs ה | pair LR ח/ה; מ/ט | ח 106, ה 134; ט **4** | ח/ה feasible; מ/ט not (ט too rare) |
| XI 12 (55) | ח vs ת; ו vs ד | pair LRs | ח 106, ת 161; ו 198, ד 56 | Feasible |
| XII 10 (60) | ב vs כ; yod present between ב and נ? | pair LR; stroke presence | ב 184, כ 157 | Feasible |
| IX 7 (40) | traces of ד, ר in the gap (דרום vs ים) | stroke presence vs blank corroded surface | blank/crack patches (to be labelled) | Feasible only with radiograph or 3D; photographs alone unlikely |
| VII 14 (32) | כ vs ב | pair LR | as above | Feasible after re-crop |
| VII 15 (32) | ט vs ס | pair LR | ט 4, ס 56 | Not feasible (ט too rare) |
| X 6, X 13 (46, 48) | gimel-shaped sign: א or ג | similarity to undisputed א vs ג | א 143, ג 25 | Partly feasible; Puech's cursive alef explanation means the classes overlap |
| IX 6, VII 16, X 16, VIII 9, VIII 13, X 11 | numeral signs and counts | numeral-sign classifier + counting | numerals in undisputed sums (to be counted) | Feasible for counts; sign values rely on the editors' sign table |
| V 8–9 (23) | word space or not | gap-width distribution (within-word vs between-word) from undisputed lines | all lines | Feasible as a likelihood ratio |
| II 4, III 7, IV 2 (Greek) | Θ/Ξ; third stroke; Σ/Χ/Ξ | none | no training set | **Out of scope** |
| IV 3–4, V 1–3, IV 6, XI 13 | lacunae, unlocated words | none | — | Out of scope (no traces) |

## 8. Effort

- Baseline on Tier 1 data: about 2–3 person-weeks (registration and two-annotator boxing of ~1,500 letters is most of it); compute trivial.
- Main model with Tier 2 data: about 2–3 person-months after the imaging, including the damage-matched and column-out evaluation.
