# Run 3 result: the purity rule

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit 0d0240b, SHA-256 `03d9330b…b916` (unchanged). Exploratory.

## Verdict
**Not supported.** P1, P2 and the reverse test all fail in every edition coding and every branch (56 branches).
- **P1 (no consecrated item in a tomb):** k1 is never 0. Two entries that every edition codes as a tomb hold "vessels of offering" (כלי דמע): **entry 51** (tomb of Zadok, XI 2–4) and **entry 54** (XI 9–11, "in it, vessels of offering"). Main run: k1 = 4 (51, 54, 56, 60) of 21 consecrated and 10 funerary entries, 3.44 expected; p1 (≤ k1) = 0.789 (exact 0.782). Lowest k1 in any branch is 2 (p1 = 0.38).
- **P2 (consecrated items favour water installations):** main run k2 = 7 of 22 water entries, 7.57 expected, p2 = 0.726; range across branches 0.19–0.83.
- **Reverse (silver and gold favour tombs):** 2 of 27 (entries 2, 56), 4.43 expected; p(≥) = 0.982. If anything, metal is under-represented in tombs (p(≤) = 0.085).

Consecrated items sit in tombs and in water installations at about the chance rate. The proposed use of the rule (treating funerary readings as less likely for consecrated entries, e.g. entry 60's "tombs at its mouth") has no support.

## Method
- Item classes: research/text/inventory_features_2026-10-06.json. Consecrated = vessels (all כלי), dema, ḥerem, tithe, garments, books, ephods, written records. 21 entries (20 with flagged readings excluded; entry 56's כלין is restored in a lacuna).
- Settings: research/comparanda/concealment_contexts/scroll_contexts.csv, four edition columns (P, Pu, M, L); N = 61.
- Funerary: setting tomb, plus entries naming קבר/נפש at the hiding place (entry 60 added). Water: cistern, pool_reservoir, channel (literal); a second branch adds water_pit.
- 10,000 permutations (seed 20261027) of each entry's (funerary, water) label pair; exact hypergeometric check agrees.
- Branches run where the rule was ambiguous: water with/without pits; entry 60 in/out; flagged readings in/out; Puech's entry 50 as tomb or not; reverse test on silver/gold or on any sum. Full table: [run_output.txt](run_output.txt); per-entry data: [per_entry.csv](per_entry.csv); [results.json](results.json); [scripts/](scripts/).

## Borderline entries
- 51: "in the tomb of Zadok, under the pillar of the exedra": the spot is the tomb's porch.
- 54: clearly "in it". The project text reads טהור הו ("which is pure"; Wolters 1994 pp. 292–295); Puech 2006 reads ירחו ("of Jericho").
- 56: בית המשכב rated burial place only low–medium; its vessels are restored.
- 60: the copy is beside the tombs, not in them; Allegro reads "buried", no tombs.

## Exploratory follow-ups (not part of the rule)
- Num. 19:15 makes only an *open* vessel unclean (quoted from memory; Sefaria was not reached). A purity-aware hider could still put sealed items in a tomb, so P1 never followed strictly from the law. The text states no container for entries 51, 54, 56.
- b. Megillah 26b: a worn-out Torah scroll is stored beside a deceased sage, in an earthenware vessel. Sacred objects in graves are attested in (late, Babylonian) rabbinic practice.
- Entry 54 may point the other way: if טהור is right, the scroll marks a tomb as pure before placing vessels in it — a hider choosing a tomb, not avoiding tombs. Needs a plate check (Puech reads "Jericho").
