# Run 6 result: lost names in Eusebius and the Madaba Map

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit 0d0240b, SHA-256 `f79813b1…dbc5`. Exploratory.

## Verdict
**No new lead.** The matcher finds the known survivals and nothing above chance for the unplaced names.
- Greek-form matches: 33 of 40 scroll names (0.825) against a C1 chance level of 0.739 (P(X ≥ 33) = 0.081). C2 base rate: 39 of 40 Joshua 15/18 names (0.975); the scroll names match *less* often than ordinary biblical names (Fisher p = 0.057).
- With Jerome's Latin and in-entry names: 36 of 40 (C1 P = 0.021; C2 40 of 40).
- Literal "new leads" (located, unplaced, C1 < 1.0): Shlomo/Shallum, Qi◦, Absalom — none credible: ΣΛΜ matches by chance 92% of the time; Qi◦ rests on Eshel's restored Cy[pros] and Callirhoe; Absalom's hits are edit-distance substitutions with Bethlehem and Jerusalem. Strict leads (C1 ≤ 0.05): 0.
- Exploratory located-match control: unplaced names 13 of 24 located against 13.1 expected (P = 0.68); placed names 11 of 16 against 7.2 (P = 0.002). The method works on real survivals and shows nothing new.
- Known names recovered: Jericho, Achor ("north of Jericho", K 18:17), Bezek (K 54:5), Beth-shean, Gerizim, Kidron, and **Janoah = Iano, K 108:19** (Yanun).

## Method
Wolf 1971 translation (984 entries; Klostermann page:line from his notes, key entries checked against Klostermann 1904 OCR); Madaba Map, Piggin's collation of Piccirillo (158 labels). Skeletons by run 2's table, all branches; identical or edit distance 1 at ≥4 consonants. C1: 100 shuffles per name, seed 20261027. C2 list frozen before matching ([out/c2_names.json](out/c2_names.json)). Deviations D1 (looser edit-distance condition) and D2 (edition variants only) give the same conclusion. Per-name table: [out/per_name.csv](out/per_name.csv); all 576 match rows: [out/all_matches.csv](out/all_matches.csv); [scripts/](scripts/).

## Correction for the main records (owner decision; not applied)
T05-010 says Eusebius lacks Secacah. He lists it: **Wolf no. 848 "Skacha", Klostermann 156:27, Σχαχά (Josh 15:61), φυλῆς Ἰούδα**; Jerome "Scacha in tribu Iudae". No location is given.

## Notes
- Koḥlit: no regional name in Eusebius or the Madaba Map comes near it.
- Qomʿah's only matches are artefacts (Κώμη "village", Ἰακώβ).
- Gihon (Geiōn, K 72:22): no position.
