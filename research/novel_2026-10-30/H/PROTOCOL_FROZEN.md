# Lane H frozen protocol: a language prior for disputed 3Q15 readings

Frozen 30 October 2026, before any 3Q15 word was scored. Branch `claude/novel-2026-10-30-H`, base main `7a3b307`.
Exposure before the freeze: the 3Q15 ETCBC text, `text/readings.json`, `variants.csv`, `confusions.csv`, the target loci and their edition readings, and the existing image notes on IX 10 (lane work log). No language-model score of any 3Q15 word, calibration word or target was computed before this freeze. Exploratory model choices used the development split of the training text only (see `WORKLOG.md`).

## Claim (the stated test)

C1. A character language model trained on period Hebrew (non-biblical DSS Hebrew without 3Q15, Mishnah, Tosefta), given the 3Q15 context around a word and no image, ranks the agreed edition reading first among realistic rival readings more often than chance.

C2 (secondary). The same model, given the context, ranks the true word division of two agreed adjacent words first among shifted and merged divisions more often than chance.

Only if C1 passes are target priors computed. The priors are one half of the evidence. They do not declare a reading. They are not combined with any image likelihood here.

## Inputs (SHA-256)

Training corpus (scratchpad; not committed; ETCBC data CC BY-NC 4.0):
- ETCBC `dss` git commit `dd29636120a89a91bf760bf349f07ce9dc3a2998`, folder `tf/2.0.2`: 79 `.tf` files; SHA-256 of their concatenation in sorted name order `322ebcbdea1d8b8b9d87f2f0c924e900708c01dd47ca7288e1e3cb7df7d650ae`.
- Sefaria Hebrew texts, 123 files (62 Mishnah, 61 Tosefta) listed with version title, licence and per-file SHA-256 in `data/sefaria_manifest.json`; SHA-256 of their concatenation in sorted name order `96583e024a2df6d04bf35fbd4fd54179dba3079336e22baba1718f3f2e117d67`.
- Built text (from `code/prep.py`): `dss_train.txt` `6a95ec062d898b783f3a3a3139ac41c3bbbf71d13206c08e95b24c1273b3ce68`; `dss_dev.txt` `070f757148dc43645c0dc91852c3d0c2032c52b2334fc0959fe721657b94647e`; `rab_train.txt` `4f845945009dd80590d805424f24d88139c2413c3e2ca8f94115d2922275cedd`; `rab_dev.txt` `785ebf3db316b7d18ff4a40a728ef1df43c9c4539bc19fa10d133db0ccaefcbc`; `bib_train.txt` (not used) `9e75d57c3b3fbc6e34dfdaf1af192985d8b204b67a462dac7553cf15f12926f2`.
- `q15_words.json` (3Q15 graphic-word stream from ETCBC; not committed, rebuilt by `prep.py`) `5fb0441962d151bdfa5aa32ead470e933298eb292f61cc635d35318a1a9a33ff`.

Repository inputs:
- `text/readings.json` `ca423f9740dc0e048582ee11ab6aa8d549e1d484f0c233217ece1fed8c1d8e35`
- `research/text/edition_confusions/confusions.csv` `765ebdca01c9f4a710223c0d1498b07569f62647537b8861e7d9b9c2fdd5e5ce`
- `research/text/edition_confusions/variants.csv` `07be73c9c02a04f5d5214143e98205608b8325b8968da4431d43be3f7baf8271`
- `research/agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md` `0e19467c618f80438c12445b7380f77f5c59b7fe241da9c80878601e2e26a2c5`

Lane files (committed with this protocol):
- `code/prep.py` `44740f9fa6c7c2741bbcd55b159639b77a7141a07f8934d73142d80699a37457`
- `code/lm.py` `3eb33670bbb5274c9951981b03a7e479469f879bd00645f29496598d1b4f5055`
- `code/prior.py` `be95e890b6d33ef0a372b19a918d27ef34a302db8df587ec5befc05e93ced3ee`
- `code/calib_set.py` `0f5fa7adb69057fcd25edd8363fd2f2c5b66f7e8da4c840bf77755fe3c50f583`
- `code/run_confirmatory.py` `4cfee964c7e4ec9ed7766b6ad81a4643a4f091a4daa157320a38dc0eb319c4f6`
- `code/fetch_sefaria.py` `a9378877b44c1799eaee01498cc1ff3c0d8d3c10e856e604931161d34d6e4843`
- `data/calib_set.json` (calibration words, rivals, split, division items, names) `b86d077926f75b93bdfed55e3ef59baf79c68282438421002d9a175cff080d68`
- `data/prep_stats.json` `d984da77ab58e15589168f9a6770479ffc6ca3b9203a5b9b8798d0f9ac3a832f`
- `data/sefaria_manifest.json` `835dcda4d37021be92737e4b2244dbd741ab3fbf46e5f64e6cbc9578ba2d1622`
- `targets.json` (target loci, candidate lists, sources) `b22d33ce1e64f9b2959e7fc23fe3d8b7bcfb08682e001e3926314a10e1162411`

Software: Python 3.13.18, numpy 2.5.3, scipy 1.18.1, text-fabric 13.1.1.

## Training text and normalisation

- DSS: non-biblical scrolls of ETCBC tf/2.0.2 (scroll feature `biblical` empty). Every 3Q15 node is excluded; `prep_stats.json` records 0 scrolls named 3Q15 and 0 3Q15 word or sign nodes read into training. Aramaic and Greek words are breaks; scrolls with more than half Aramaic words are dropped. Words with a reconstructed, missing, illegible or alternative sign are dropped and break the text.
- Biblical scrolls: OUT. Reason: on the development split they raised DSS-dev bits per character at every order (N=6, mix 0.5: 3.082 without, 3.101 with), and 3Q15 is non-biblical late Hebrew.
- Mishnah: Sefaria version "Mishnah based on the Kaufmann manuscript, edited by Dan Be'eri" (licence PD), 61 tractates; Mishnah Ta'anit from "Torat Emet 357" (Public Domain). Tosefta: Vilna-edition texts from Machon Mamre on Sefaria (Public Domain), 61 tractates.
- Normalisation: consonants only; final letters become base letters; matres lectionis kept as written; one space between words; a numeral becomes `9`; a break starts a new segment.
- Development split: 10% of DSS scrolls and 10% of Mishnah/Tosefta tractates (seed 20261030). The model trains on the training split only.

## Model and score (fixed)

- Interpolated modified Kneser–Ney character 8-gram (`lm.py`), one model on DSS-train, one on Mishnah+Tosefta-train, mixed per character with weight 0.5/0.5.
- Context window W = 3 graphic words on each side, stopped by a foreign word or a line-internal break in the ETCBC token stream. Numbers stay as `9`.
- Score of a candidate = ln P(candidate + ' ' + right context | left context). This handles length and word division.

## Calibration set (fixed in `data/calib_set.json`)

- Agreed words: 3Q15 Hebrew graphic words of at least 2 letters, with no ETCBC flag (reconstructed, missing, illegible, uncertain letter, corrected, removed), not a proper name (no `np` morph component), not touched by any `readings.json` record or any `variants.csv` row, not in a target line, not in XII 8–12.
- Rivals: K = 4 per word, sampled without replacement with probability proportional to the `confusions.csv` rate over all single-letter substitutions (both directions, final letters as base letters); seed 20261030. Words with fewer than 4 possible rivals are dropped.
- Split before scoring, seed 20261030: 97 calibration-training words, 196 held-out words.
- Division items (C2): adjacent pairs of agreed words within the same split. Candidates: true division; boundary one letter left; one letter right; merged. 76 held-out, 14 calibration-training.
- Names (descriptive only): 40 proper-name words with 4 rivals, scored to show how weak the prior is on name-like strings.

## Decision rule and failure condition

- C1 pass: held-out n ≥ 100 and one-sided exact binomial p < 0.01 for the top-1 count against chance 1/(K+1) = 0.20. Top-1 means the true reading scores strictly higher than every rival.
- C1 fails: n < 100, or p ≥ 0.01. Then target priors are not computed, and `target_priors.csv` says NOT RUN.
- C2 pass: one-sided exact binomial p < 0.01 against chance 0.25 on the held-out division items.
- Calibration map: one temperature T on softmax(score/T), fitted by minimum mean negative log-likelihood over a log grid 0.05–20 on the calibration-training substitution items only. Reported on held-out: NLL, mean probability of the true reading, expected calibration error.

## Targets (only if C1 passes; candidate lists fixed in `targets.json`)

IX 10 words 2–3 (7 candidates incl. מנחה רב, מנה חרם, מן החרם, Luria מנחת רב and the other divisions); I 12 word 3 (ניקרת, נקרת, מקרת, מקדת); VII 11 word 3 (המשמרה, המשמרת, המשטח, המשטוח); X 15 words 0–2 (3 candidates) and words 3–5 (3 candidates); XII 10 R1–R7, each followed by בצפון. Output: `target_priors.csv` with locus, candidate, log_prior (normalised log-probability over the locus candidates), calibrated_probability (softmax with T), notes (entropy, calibration coverage, source). Candidates that differ in length or division are covered only by C2, and the notes say so.

## Meaning of the outcome

- Obtained: C1 passes. The prior is shown to carry information on agreed 3Q15 words. Target priors are delivered with their calibration. No reading is declared.
- Partly: C1 passes but C2 fails. Same-length priors (I 12, VII 11) are calibrated; priors at loci that turn on length or division (IX 10, X 15, XII 10) are delivered but flagged as uncalibrated.
- Not obtained: C1 fails. The priors are not evidence. Only the calibration is delivered.

The AGENTS.md closing result names claim C1 (and C2): "supported relative to the registered alternatives" (chance ranking) if it passes; "rejected" if it fails with n ≥ 100; "not identifiable from available evidence" if n < 100.
