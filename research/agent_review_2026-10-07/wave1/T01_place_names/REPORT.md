# T01 — Computational place-name search

Agent report, 6 October 2026, saved by the coordinator (the agent could not write .md files). Labels: EVIDENCE = what a source says; INFERENCE = reasoning, with confidence.

## Bottom line
No identification moves. I scored 9,368 OCR'd records from E. H. Palmer, *SWP Arabic and English Name Lists* (1881), against 70 consonantal variants of 40 scroll names. No new match passes both of Elitzur's conditions (an area fixed by ancient sources, plus a name matching in all or almost all letters).

## What was done
- Parsed archive.org's OCR of all 26 sheets (6,618 records); re-OCR'd the priority sheets XIV, XV, XVII, XVIII, XXI and XXII with tesseract (166 pages, 2,750 records).
- Wrote sourced Hebrew→Arabic sound rules (Palmer's preface pp. iii–iv; Kampffmeyer, ZDPV 15, 1892) — `data/sound_rules.csv`, applied in `scripts/toponym.py`.
- Scored every name against every variant; tested the scorer on 40 known identifications; ran a chance test with random Hebrew-like names over the whole region and within sub-areas; checked 14 top candidates against the Arabic script on the page images and against SWP Memoirs vol. III.

## Findings
1. **INFERENCE, high: name likeness alone is chance-level here.** The scorer finds real survivals (32 of 37 known ones score ≥ 0.75; median 0.957). But a random three-consonant name finds a match ≥ 0.75 in the Jericho–Qumran squares 46% of the time (Jerusalem 37%, Judean desert 62%). Observed matches for Koḥlit (p = 0.10), Sekakah (0.17), ha-Melaḥ (0.30) and Achor (0.36) are within chance — and so is the accepted survival Doq = ʿAin ed-Dûk (p = 0.59).
2. **EVIDENCE: Palmer's Latin transliteration merges s/ṣ, k/q, t/ṭ and h/ḥ** (preface p. iii). Of 14 candidates checked on the Arabic script, 3 false matches came from these merged letters and 1 from an OCR misreading ("Zerd" is Zerʿ). About 83% of matching names are ordinary Arabic words (salt, paths, kohl, barren, rock pool).
3. **Lead, weak to low: ha-Melaḥ ↔ Mâlḥah (مالحة), about 5 km SW of Jerusalem** (XVII p. 322 Mt). Memoirs III p. 136: caves and "on the east … a tomb with six kokim" — compare entry 14, "the tomb … in ha-Melaḥ, on its east side". Against: an ordinary Arabic word; Memoirs p. 21 already equates it with Manahath; Milik and Puech read ha-Melaḥ as part of the Temple area.
4. **Lexical lead, low to medium:** Palmer records hŭrubbeh/herâbi (هربة) = "cistern" at four Judean-desert places (e.g., XVIII p. 344; XXI p. 393; Memoirs III App. p. 439: a rock-cut cistern with an aqueduct). If entry 1's חרובא is this word rather than "little ruin", entry 1 describes a stepped cistern. Obstacle: Arabic ه where Hebrew has ח.
5. **Others low or rejected:** Beit Kâḥel (exact k-ḥ-l, rock-cut tombs, but NW of Hebron), Birket Ḥarb, ʿAin el-Qelt, Beit Taʿâmir (named for a tribe). Wadi el-Qelt keeps no Arabic form of Koziba.

## Chance control detail
Random-name matches ≥ 0.75 on the priority sheets (mean count; share with ≥ 1): 2 strong consonants 11.6 / 93%; 3: 7.7 / 83%; 4: 3.0 / 64%; 5: 1.5 / 35%. Observed vs random mean (p95, p): Achor 8 vs 7.3 (25, 0.36); Koḥlit 20 vs 6.7 (25, 0.10); Sekakah 17 vs 8.3 (31, 0.17); ha-Melaḥ 9 vs 8.3 (0.30); Doq 5 vs 10.0 (0.59). Only names with very common Arabic roots (Sulaymān, ḥ-ṣ-r, ḥ-r-b, m-s-l-m, ʿ-b-d) exceed chance. Positive-control misses: Gibeon/el-Jîb 0.65, Beth-Horon/Beit ʿÛr 0.56, Jericho/Erîḥa 0.70, Siloam/Silwân 0.73.

## Candidates checked on the page image (`data/verified_candidates.csv`)
| Scroll name | Palmer name (sheet, page, square) | Arabic | Verdict |
|---|---|---|---|
| ha-Melaḥ | Mâlḥah (XVII p. 322 Mt) | مالحة | Weak to low |
| Ḥorebbeh (entry 1) | Birket Ḥarb (XVIII p. 342 Os) | بركة حرب | Low |
| ḥrwbʾ (entry 1, lexical) | Hŭrubbet el-Ḥaṭṭâbeh (XVIII p. 344 Nu); Herâbi el-Beid (XXI p. 393) | هربة | Low to medium |
| Koḥlit | ʿAin el-Qelt (XVIII p. 339 Os) | عين القلت | Low |
| Koḥlit | Beit Kâḥel (XXI p. 388 Kw) | بيت كاحيل | Low |
| Beth Tamar | Beit Taʿâmir (XVII p. 287 Mu) | بيت تعامر | Low |
| Achor | ʿAqûr (XVII p. 283 Kt) | عقور | Reject |
| Sekakah | Bâb es-Sikâk; Iskâka; Mughâret eṣ-Ṣaqîʿ | — | Reject |
| Zered | Bîr ez-Zerʿ (XVIII p. 342) | بئر الزرع | Reject (OCR error) |
| Manos, Nebaṭ, ha-Melaḥ (Mellâḥet, el-Malḥah) | various | — | Reject |

No first-century date was found for any candidate.

## Limits
Arabic script not OCR'd (only the 14 candidates were checked against it); non-priority sheets rely on noisier OCR; grid locations accurate only to an SWP square (~7 × 9 km; residual 2–3 km); web-search budget ran out (ʿIr ha-Melaḥ = Qumran, archaeology at al-Maliha and Beit Kahil, and Elitzur's phonology chapters unverified); edition readings come from the project's summaries.

## Best next step
Check the etymology of hurubbeh and any pre-Arabic record of Mâlḥah; find whether al-Maliha's kokhim tomb is dated.

## Sources
- Palmer 1881: https://archive.org/details/surveyofwesternp00conduoft
- Conder & Kitchener, SWP Memoirs III (1883): https://archive.org/details/surveyofwesternp03conduoft
- Kampffmeyer, ZDPV 15 (1892): https://archive.org/details/zeitschriftdesde15deut
- Elitzur 2004 via the repo's findings log F2.21–22
- Zissu, PEQ 133 (2001) 145–158: https://orion-bibliography.huji.ac.il/node/58804

Files: `data/` (scroll_names.json, palmer_names.csv, sound_rules.csv, candidates_ranked.csv, new_candidates_by_name.csv, verified_candidates.csv, positive_controls_result.csv, chance_control.csv, chance_regional.csv, grid_calibration.json), `scripts/`, `downloads/`.
