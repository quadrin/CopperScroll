# Lane H work log: language prior for disputed readings (30 Oct 2026)

## Novelty gate
Earlier work in the repository reads letters from images or compares edition variants (edition_confusions, letter_controls, lane B "analysis by synthesis" image rendering).
No work on main or `origin/sandbox/methods` used a language model, perplexity or a reading prior (repository check 30 Oct).
Lane H uses no image. It trains a character-level language model on period Hebrew (DSS non-biblical Hebrew without 3Q15, Mishnah, Tosefta).
It scores candidate readings, including word divisions, by the probability of the 3Q15 context with the candidate substituted.
It first tests on held-out agreed 3Q15 words, with realistic rivals made from the edition-confusion rates, whether this prior beats chance.

## Log
- 30 Oct. ETCBC dss sparse clone, commit dd29636120a89a91bf760bf349f07ce9dc3a2998, folder tf/2.0.2 only (scratchpad, not committed).
- Sefaria: index fetched; 62 Mishnah tractates (61 "Mishnah based on the Kaufmann manuscript, edited by Dan Be'eri", licence PD; Mishnah Ta'anit not in that version, so "Torat Emet 357", Public Domain) and 61 Tosefta tractates (Vilna Edition category, Machon Mamre versions, Public Domain). No refusals. Plain User-Agent, no email.
- prep.py (EXPLORATORY build step): DSS non-biblical Hebrew without 3Q15; Aramaic words are breaks and majority-Aramaic scrolls dropped; biblical scrolls kept in a separate file for a dev-split decision. 3Q15 word nodes read into training: 0.
- EXPLORATORY dev split, bits per character (dss_dev, rab_dev every 3rd segment), mixture lam = DSS weight:
  N=3..6, DSS-only vs DSS+biblical: adding biblical scrolls makes DSS-dev worse at every order (e.g. N=6 lam=0.5: 3.082 vs 3.101) and rab-dev better by <0.02. Decision: biblical scrolls stay OUT (3Q15 is non-biblical, late Hebrew; biblical copies hurt the non-biblical dev fit).
  N=6/7/8/10 at lam=0.5: DSS-dev 3.082/3.069/3.069/3.085; rab-dev 2.589/2.516/2.473/2.439.
- EXPLORATORY dev task (dev split only; 300 random words of >=2 letters per collection, K=4 rivals from confusions.csv, seed 7): top-1 rate with context window W=1..3 words is 0.83-0.91 against chance 0.20; with no context (W=0) 0.62-0.72. N=4 is worse (0.78-0.85). N=6 and N=8 are similar. Chosen: N=8, lam=0.5, W=3 (dss 0.853, rab 0.893). Context matters (W=0 vs W>=1).
- calib_set.py (no scoring): 293 eligible agreed 3Q15 words (K=4 rivals each), 196 held-out / 97 calibration-training. Dropped: 60 short/non-Hebrew, 114 ETCBC-flagged, 44 proper names, 219 touched by readings.json or variants.csv, 34 in target lines or XII 8-12, 29 with fewer than 4 possible rivals. Only 2 untouched names remain, so the name check will use names regardless of edition dispute (descriptive only).
- Limitation found: confusion rivals keep the word length. Word division and length (IX 10, I 12 נקרת/ניקרת, XII 10) are outside that calibration. Add a secondary registered division test (boundary shift left/right, merge). Check it on the dev split first.
- EXPLORATORY dev division task (dev split only; 300 adjacent word pairs, candidates: true, boundary one letter left, one letter right, merged): top-1 0.82 (DSS dev), 0.95 (rabbinic dev) vs chance 0.25.
- Smoke test of run_confirmatory.py on a fake "3Q15" made from DSS dev segments (no 3Q15 word scored): pipeline runs; fake held-out top-1 0.80, T=0.79.
- targets.json fixed (candidate lists with sources). XII 10 candidates include the following word בצפונ, because ETCBC joins it to the disputed word (שב{צח}צפון) as one graphic word.
- Decision: IX 10, X 15 and XII 10 candidates differ in length or division. The primary substitution calibration does not cover them. Their priors carry the secondary division calibration only, and the CSV notes say so.
- Freeze commit 004515a, PROTOCOL_FROZEN.md sha256 7b7f1bde4a7545403f142ecf2a22b749349e075fc33022dd136147d71cfa839d, pushed.
- Confirmatory run once, started 2026-10-31T06:24:56Z (container clock), inputs re-hashed and matched. C1 held-out 148/196 top-1 (chance 39.2), p = 1.4e-62: pass. C2 61/76 (chance 19), p = 7.8e-24: pass. T = 1.206. Targets scored.
- POST-RUN, descriptive only: reliability bins (held-out substitution: confidence 0.42/0.65/0.88/0.97/0.995 vs accuracy 0.50/0.73/0.81/0.90/0.95 — slight overconfidence at the top); names 22/40 top-1, mean p(true) 0.51 against 0.63 for common words.
- POST-RUN EXPLORATORY sensitivity (not a test): DSS-only and Mishnah+Tosefta-only components give the same top candidate at IX 10, I 12, VII 11, X 15 (both spans); at XII 10 DSS-only prefers שבנה (0.69), rabbinic-only שכינה (0.47) over שבנה (0.40).
