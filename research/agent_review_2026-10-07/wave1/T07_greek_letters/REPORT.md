# T07 — Greek letter corpus search

Agent report, 6 October 2026, saved by the coordinator. Labels: EVIDENCE / INFERENCE. Scoring rules and the chance null were fixed in PREREGISTRATION.md before any search.

## What was done
Downloaded all 5,553 records of the Inscriptions of Israel/Palestine database (IIP) from its public search endpoint (2,958 fall in 200 BCE–250 CE) and searched every abbreviation, numeral, uninterpreted letter group and token. Read sources on Herodium mason's marks, Qumran Greek inscriptions, Masada/Maresha marks (via their IIP records) and Mishnah Shekalim. Tested candidate systems against fixed word lists.

## Findings
1. **EVIDENCE, high (within IIP's coverage):** none of ΚΕΝ, ΧΑΓ, ΗΝ, ΘΕ or ΣΚ appears in the window as a mark with a known meaning. The only usable hits are Δι(ί) "to Zeus" (Caesarea) and τρ inside a Δημήτριος monogram (Maresha). Among editor-tagged uninterpreted letter groups in Judaea, chance predicts about 0.5 matches; 1 was found.
2. **EVIDENCE, medium–high:** Judaean marks are mostly Hebrew letters (Masada produce-status tags, Herodian mason's marks, ossuary lid marks). Greek marks are mostly single letters, correct numerals (ΚΓ = 23 log at Masada) or plain 1–2-letter truncations (Maresha σέ(α), κά(βοι), πυ(ρός)). Groups like ΚΕΝ/ΧΑΓ have no regional parallel.
3. **EVIDENCE, medium — two formal parallels, neither decodes the scroll:** unexplained Greek letter groups on Jerusalem ossuaries (Rahmani nos. 289, 319, 322, 582), read only tentatively as initials; and Mishnah Shekalim 3:2, where R. Ishmael says the Temple treasury baskets were labelled in Greek, alpha, beta, gamma. Those labels run in alphabetical order; the scroll's letters do not.
4. **INFERENCE, high:** no candidate system reaches 5 of 7 groups; the best is 2 of 7. Numerals, units of measure, Maresha measure/commodity words, priestly courses (0/7), months (1/7) and ordinal labels all fail on the scroll itself.

## Blocked (not circumvented)
The IIP GitHub repository; papyri.info (anti-bot check, so the Murabbaʿat and Naḥal Ḥever Greek papyri were not searched); CIIP (not open access).

## Best next step
Check the CIIP I–IV indices and the Judaean Desert Greek papyri for ΚΕΝ, ΧΑΓ and ΗΝ.

Files: PREREGISTRATION.md, data/hits_graded.csv, data/comparanda_mark_systems.csv, data/system_assessment.csv, data/corpus_coverage.csv, data/chance_expectation.json, data/system_tests.json, data/iip_all.json, scripts/.
