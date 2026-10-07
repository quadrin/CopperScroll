# T08 — Real-or-legend statistics

Agent report, 6 October 2026, saved by the coordinator. Labels: EVIDENCE / INFERENCE.

## What was done
- Extracted every amount from the scroll: 59 amounts in 54 entries; a script checks each against the numerals of its line (58 of 59 match; the exception is מנה, a noun). Edition variants from `readings.json`.
- Coded per-entry features (dig, depth, distance, direction, container).
- Genuine comparison set: 12 Athenian inventories and accounts (Attic Inscriptions Online) and the Elephantine collection list (Cowley 22). Legendary set: the Treatise of the Vessels (Jellinek's Hebrew), *Kitab al-Durr al-Maknuz* (Kamal 1907), Chronicles/Kings treasure figures, 2 Macc 2 and 2 Bar 6.

## Findings
1. **EVIDENCE — two features separate legend from genuine in these lists.** Roundness: among amounts ≥ 10, 88–93% are multiples of ten in the legends; the genuine documents' median is 45% (10 of 12 at or below 54%). Myriads (≥ 10,000): the legends use them (up to 59% of the Treatise's amounts); no genuine document does.
2. **EVIDENCE / INFERENCE, moderate — on both features the scroll sits with the genuine lists:** 37% of its amounts are multiples of ten (95% CI 0.21–0.51); the largest is 900. It also has no magic, famous objects, named hider or end-time frame.
3. **EVIDENCE — on remainders below the unit the scroll looks like the legends:** only 2 of 45 amounts have one (genuine documents: 9–69%), and all five scroll amounts ≥ 100 are exact hundreds. So the profile is mixed.
4. **EVIDENCE — correction to the repo:** the finding that entries 1–19 are rounder than 20–56 (p = 0.022, reproduced) falls to p = 0.15 counted per amount, and tracks how numbers are written: word numerals are round 9/11 times, numeral signs 5/28 (p = 0.0004). Comparing blocks within each writing style gives p = 0.36.
5. **EVIDENCE — totals:** Lefkovits's conditional total reproduced (59,790 kg vs his 59,794 kg). Read with every ככ as talents, the weight amounts come to 3,755 talents (80–221 t depending on the talent's mass).

**Moves the question?** A little: it weighs against "folklore like the Treatise of the Vessels", but cannot tell real deposits from a realistic composed list.

## Amount features
| Set | n | m10 [95% CI] | m100 (n) | sub-unit | myriads | log10 sd |
|---|---|---|---|---|---|---|
| Scroll, weight amounts | 45 | 0.37 [0.21–0.51] | 1.00 (5) | 0.04 | 0 | 0.53 |
| Athenian inventories | 563 | 0.47 | 0.37 (59) | 0.27 | 0 | 0.92 |
| Athenian payments and loans | 182 | 0.34 | 0.22 | 0.66 | 0 | 2.02 |
| Tribute quota lists | 112 | 0.51 | 0.78 | 0.51 | 0 | 0.70 |
| Chronicles/Kings treasure figures | 19 | 0.89 | 0.89 | 0 | 0.32 | 1.22 |
| Treatise of the Vessels | 39 | 0.88 | 1.00 | 0 | 0.59 | 2.04 |
| *Kitab* treasure counts | 203 | 0.93 | 0.98 | 0 | 0.06 | 1.30 |

A toy nearest-centroid classifier (15 documents, leave-one-out 14/15 correct) puts the scroll on the genuine side; on remainders alone it would call it legendary. Illustration only: just 3 legendary documents. Benford's law uninformative (two orders of magnitude).

## Formula features per entry
| Feature | Scroll (61) | *Kitab* (160) | Treatise (12) |
|---|---|---|---|
| numeric amount | 0.89 | 0.41 | 0.83 |
| dig instruction | 0.43 | 0.70 | 0 |
| depth in cubits | 0.43 | 0.11 | 0 |
| direction word | 0.54 | 0.91 | 0 |
| container named | 0.13 | 0.36 | 0 |
| magic/supernatural | 0 | 0.46 | 0.42 |

The scroll has 13 distinct depths (1–24 cubits, median 7); in the *Kitab* 81% of 210 depths are "one" unit. The Treatise (m. 2) says its list was written "on a tablet of copper" (על לוח נחושת), and m. 10 places silver "in ʿEin Kaḥal" (עין כחל) — checked on Jellinek pp. 88–90 page images; the resemblance of כחל to the scroll's כחלת is the agent's observation only.

## Edition disagreements on figures
Entry 6: 41 vs 42 (all three editions); 10: 6 vs Milik prelim. 600; 14: 13 vs Puech 14; 15: 14 vs Puech ≥ 54; 28: 22 vs Puech 22+40/60, Lefkovits none; 32: 80 vs Milik/Lefkovits 60; 35: 7 vs Milik 4; 36: 65 vs 66/67; 39: 23½ vs Allegro 24; 47 cups: 20 vs Lefkovits 10. No conclusion changes under the Puech, Milik or Lefkovits figures.

## Limits
Genuine lists are Athenian/Elephantine, 5th–3rd c. BCE; only 3 legendary texts have numbers; *Kitab* coded by pattern-matching on French OCR (5–7 disagreements in 120 spot checks); Murabbaʿat/Masada accounts not found openly online; Davila's Treatise translation and the Delian inventories not used; some contrasts noticed while reading.

## Best next step
Code one genuine Judean or Near Eastern deposit/hoard list (Murabbaʿat or Naḥal Ḥever accounts) for remainders below the unit.

Files: scripts/ (scroll_amounts.py, parse_aio.py, parse_kanz.py, handcoded_corpora.py, analysis.py — run with python3 -I), data/ (amount_features.csv, block_tests.json, unit_totals.csv and others), downloads/.
