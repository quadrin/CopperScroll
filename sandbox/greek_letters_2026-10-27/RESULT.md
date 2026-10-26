# Run 2 result: the Greek letter groups

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit 0d0240b, SHA-256 `75fa438e…e1249`. Exploratory.

## Verdict
**Not supported, for both hypotheses, on every branch** (32 string combinations from every edition's reading).
- **H-num (Greek numerals equal a quantity in their own entry):** primary strings ΚΕΝ ΧΑΓ ΗΝ ΘΕ ΔΙ ΤΡ ΣΚ give **k = 0 of 7**; p = 1.0 under both controls. Best variant: k = 1, Ullendorff's and Muchowski's ΞΕ = 65 against "sixty-five ingots of gold" (entry 7, II 4); p 0.04–0.18 depending on control. The facsimiles and the project's plate check read Θ, not Ξ.
- **H-abbr (initials of a place word within ±2 entries):** k = 0 on all three word lists (landmark lexicon, readings.json labels, all ETCBC nouns); p = 1.0. The one variant hit (ΧΚ = the talent unit ככ) matches all 61 entries, so it is an artefact.

## Method
Quantities for all 61 entries built from translation_en.json, T08 scroll_amounts.csv and readings.json variants ("displayed" and "editions" branches); equality, or ±10% under talent↔karsh 1:300 only. Controls: 10,000 random 7-entry draws; 10,000 shuffled letter strings of the same lengths (iid check also run); seed 20261027. Deviations (labelled): Ξ = 60 added for variant strings; three word lists because no structured place-word list exists; an acronym branch. Entry 15's sum (Puech [20+20+?]+14) recorded as unknown. Files: [results.json](results.json), [match_matrix.json](match_matrix.json), [wordlists.json](wordlists.json), [scripts/](scripts/).

## Rule limits found
Under the fixed transliteration table no Hebrew letter gives Η, so ΗΝ can never match as initials; and any Χ/Κ + Κ string matches the talent unit everywhere.

## Exploratory notes
- Matches in *other* entries (which drive the controls): ΤΡ = 400 = entry 29's 400 talents; ΧΑΓ = 604 ≈ entry 32's 2 gold talents as 600 karsh; ΘΕ = ΔΙ = 14 = entry 15's 14 and entry 54's 14 vessels.
- ΣΚ (end of entry 15) is a prefix of סככא, Sekakah, which first appears in entry 20 — outside the ±2 window, and weak given how many words begin ש/ס + כ. Not tested.
