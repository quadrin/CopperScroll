# Run 2 rule: the Greek letter groups mean something in their own entry

Fixed 27 Oct 2026 before any analysis for this run. Exploratory (sandbox README).

## Hypotheses
Seven Greek letter groups end entries in cols. I–IV: ΚΕΝ (entry 1, I 4), ΧΑΓ (4, I 12), ΗΝ (6, II 2), ΘΕ (7, II 4), ΔΙ (9, II 9), ΤΡ (12a, III 7), ΣΚ (15, IV 2). Readings of the letters as in text/readings.json; where an edition reads a letter differently, run every edition's string.
- **H-num:** each group is a Greek numeral (Κ=20, Ε=5, Ν=50, Χ=600, Α=1, Γ=3, Η=8, Θ=9, Δ=4, Ι=10, Τ=300, Ρ=100, Σ=200; value = sum) that equals a quantity in its own entry: the amount (in talents, karsh or count), the depth, or a distance, in the units printed. A match is equality, or within ±10% if converted (cubits↔other units are not allowed; talents↔karsh at 1:300 is allowed).
- **H-abbr:** each group is the first letters of a Greek rendering of a place name or landmark word in its own entry or within ±2 entries. Use the fixed transliteration table: א/ע→Α or none, ב→Β, ג→Γ, ד→Δ, ה→none or Ε, ו→Ο/Υ, ז→Ζ, ח→Χ or none, ט→Τ, י→Ι, כ→Κ/Χ, ל→Λ, מ→Μ, נ→Ν, ס→Σ, פ→Π/Φ, צ→Σ, ק→Κ, ר→Ρ, ש→Σ, ת→Θ/Τ.

## Data
Quantities and place words from text/readings.json, text/translation_en.json, research/text/inventory_features_2026-10-06.json, and the amounts table T08 used in first_tests_2026-10-24/method10_hoards/scroll_sums.json.

## Test
- Count matches k over the 7 groups (an entry counts once).
- **Control:** 10,000 permutations assigning the 7 groups at random to 7 of the scroll's entries (all entries, not only cols. I–IV); count matches each time. p = share of permutations with ≥ k. A second control: 7 random Greek strings with the same lengths and letter frequencies, matched to the true entries.
- **Supported** (exploratory): k ≥ 4 and p < 0.01 under both controls. **Not supported:** otherwise. Report k, both p values, and every match with its entry and reading.

## Limits
R11 (the order in which the Greek was engraved) is closed and is not touched. This run tests meaning only. The hypothesis space (numeral or initials) is fixed here; any further idea found while looking is a new, exploratory hypothesis.
