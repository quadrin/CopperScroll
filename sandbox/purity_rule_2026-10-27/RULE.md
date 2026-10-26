# Run 3 rule: a purity rule governs what was put where

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
Whoever hid the items followed priestly purity law. Corpse impurity (Num. 19) would defile consecrated objects, so:
- **P1:** no consecrated item (vessels כלים/כלי דמע, tithe מעשר, ḥerem חרם, dema דמע, garments, books/scrolls, "vessels of offering", the copy of the document) is placed in a tomb, grave or funerary monument.
- **P2:** consecrated items are placed more often in water installations (cisterns, pools, conduits, reservoirs, miqva'ot) than chance predicts.
- Silver and gold coin or bullion are not restricted.

## Data
- Item classes per entry: research/text/inventory_features_2026-10-06.json (dema, herem, vessels, silver, gold, ...).
- Hiding-place class per entry: research/comparanda/concealment_contexts/scroll_contexts.csv, column `setting_P` (frozen 10–11 Oct, before this hypothesis). Run again with `setting_Pu`, `setting_M` and `setting_L` (other editions).
- **Funerary** = setting `tomb`, plus any entry whose text names קבר/קברין/נפש at the hiding place (not merely as a landmark on the way). List those entries before counting.
- **Water** = settings coded as cistern, pool, conduit, reservoir, channel or spring.

## Test
- P1: count consecrated-item entries in funerary settings (k1). Under 10,000 permutations of the setting labels across entries, p1 = share with ≤ k1 consecrated items in funerary settings. P1 holds if k1 = 0 and p1 < 0.05.
- P2: count consecrated-item entries in water settings (k2); p2 = share of permutations with ≥ k2. P2 holds if p2 < 0.05.
- Also report the reverse: are silver/gold over-represented in tombs?
- Report all four editions' codings, every entry in each cell, and borderline cases (e.g., "beside" a tomb vs "in" it).

## Why it matters
If P1 holds, it is a predictive rule: for entries whose item is consecrated, funerary readings of a doubtful word (e.g., entry 60's "tombs at its mouth", entry 24's "tomb") become less likely, and vice versa. It would also bear on who hid the items.
