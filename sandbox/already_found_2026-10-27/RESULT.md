# Run 4 result: caches already catalogued as hoards

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit 0d0240b, SHA-256 `cbda058b…8eef8f` (unchanged). Exploratory.

## Verdict
**No lead.** k = 0 under the frozen rule in every unit branch (karsh light or heavy, talent light or heavy, all-karsh). Permutation p = 1.0. Scope: 42 entries with sums (45 sums) × 164 in-window hoards = 6,888 pairs.

- **Bottleneck: mass and context together.** At karsh light, 7 pairs match on metal-specific mass and context; none lies within 5 km of a candidate place.
- **Coverage gap (AF447-style):** 31 pairs (karsh light) and 18 (heavy) fail only because the hoard's context is unknown — 7 and 6 hoards, mostly market or chance finds (e.g. St Stephen's Gate, CHRE 7541; Jerusalem North, 7901; Jericho 1874, 8082, ~100 shekels in a pot with a lead seal).
- Talent reading: no hoard reaches a talent mass.

| Conditions (karsh light / heavy) | Pairs |
|---|---|
| C1 metal | 2,915 |
| C2 mass | 284 / 181 |
| C3 context | 143 |
| C4 place | 810 |
| C2 & C3 | 8 / 7 |
| C3 & C4 | 56 |
| all four | **0 / 0** |

Sensitivity cells (mass-range overlap, coarse context class, Qumran pots separate) give k = 1–8; their p values are uncorrected for the number of cells tried. Full tables: [results.json](results.json), [entry_table.csv](entry_table.csv), [hoard_table.csv](hoard_table.csv); [scripts/](scripts/) (`python3 -I run.py`, ~13 s).

## Method choices (where the rule was open)
Hoard pool: hoards.csv `include` = 1, midpoint date in −63 to 135 (precedent rule). Masses joined from Method 10; unknown masses fail C2. C3 = the precedent's fine category C01–C14 (coarse G1–G5 as sensitivity). C4 candidates = ratings.csv ∪ places.csv; three coordinates taken from atlas/app/atlas-data.json; four candidates unplaced, so entries 28, 39, 42, 44 use the region box. 10,000 permutations, seed 20261027.

## Exploratory follow-ups (not part of the verdict)
- **Ein Feshkha 1953 (CHRE 7586) with entries 25 and 26** — the only fine-class pairs, and only with mass-range overlap. ≥277 silver coins "in a cave somewhere in the neighbourhood of Feshkha", closing 117–138 CE; denominations not reported. Denarii (~1.05 kg) would fit entry 26 at karsh light; tetradrachms/shekels (~3.93 kg) would fit entry 25 (light) and 26 (heavy). Next record: the 1953 report ("ʿAin Feshkha", p. 89, as CHRE cites it; not identified) or Callegher in Humbert et al. 2016. Already exposed (T02 H08, Method 10). The closing date (117–138 CE) is at or past the end of the window.
- **Kh. Badd ʿIsa B (CHRE 8173) with entry 44**: passes only with the coarse class and the region box (546 g silver, 16 g gold in a juglet under a floor, 124–128 CE).
- **Near misses on mass:** Dominus Flevit (16 silver, ~185 g, tomb, Mount of Olives) for tomb entries 14, 27, 48, 53, 56; Jewish Quarter 1975 (13 shekels "in a small pool") for entries 46, 47, 49 — both 2.5–9× too light.

## Data note for the main records (not applied)
Method 10 codes silver as 0 g for four silver hoards (Masada B, Meqor Ḥayim, Tiberias 1952, Badd ʿIsa A), probably unparsed contents. Fixing two changes nothing here.

## Not accessible
https://chre.ashmus.ox.ac.uk/hoard/7586 (fetch permission not answered). The catalogue's existing blocks still apply (IGCH, *Coin Hoards* I–X, ʿAtiqot PDFs, HA-ESI, Kadman 1967, Waner & Safrai 2001); 100 of 182 included rows have unknown context.
