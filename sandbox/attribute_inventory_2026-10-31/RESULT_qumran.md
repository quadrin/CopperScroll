# Sources 2–7 (Qumran group): result

31 Oct 2026. Exploratory. Keying notes frozen before keying: [QUMRAN_NOTES.md](QUMRAN_NOTES.md). Same schema, instructions, agreement script and merge rule as source 1. Two readers per group, a third reading of every disagreement, then `scripts/consolidate.py`.

## Result

| Source | Whole features (both readers / one only) | Class agreement | Size agreement | Openings agreement | Usable attributes after consolidation |
|---|---|---|---|---|---|
| `qum3a` IIIA lists of loci and elements | 736 (736 / 0) | 714 / 736 | 1 / 1 | 38 / 38 | openings 42, directions 4, steps 4, plaster 16; almost no sizes |
| `mp18` Magen & Peleg 2018 | 178 (127 / 51) | 123 / 127 | 167 / 167 | 24 / 25 | lengths 76, openings 41, directions 28, steps 13, plaster 35, pillars 5 |
| `hir04` Hirschfeld 2004, ʿEin Feshkha | 60 (33 / 27) | 33 / 33 | 29 / 49 | 6 / 6 | lengths 32, openings 16, directions 15, steps 5 |
| `bad77` Bar-Adon 1977, ʿEn el-Ghuweir | 29 (12 / 17) | 12 / 12 | 9 / 9 | 1 / 1 | lengths 7; low reliability (scrambled text) |
| `esh02` Eshel et al. 2002, cemetery | 243 (162 / 81) | 162 / 162 | 2 / 4 | 1 / 1 | 230 tombs, mostly without sizes |
| `qum4a` IVA, Cave 11Q | 1 (1 / 0) | 1 / 1 | 2 / 2 | 1 / 1 | one cave: one opening with direction, a pillar, sizes |

Agreement is on values both readers gave (sizes within 10 % or 0.2 m; directions equal or neighbouring). "One only" rows are features that only one reader keyed; they are kept and marked in the `readers` column.

- **Magen & Peleg 2018 is the richest source**: 76 measured features, 28 with opening directions, 13 with steps.
- **IIIA gives structure, not sizes**: its lists name loci, walls and doorways, with plate-grid cells, but print almost no dimensions.
- **Hirschfeld's size differences are column swaps**: the readers put the same numbers in the length and width columns in different orders.

## Third reading

114 items (26 class, 22 opening counts, 19 plaster, 17 widths, 16 lengths, 10 directions, 3 step counts, 1 height). The third reader sided with A on 51, with B on 59 and with neither on 4.

- **IIIA:** A was right on 37 of 40. B gave classes the list does not support.
- **Plaster in IIIA:** the third reader keyed "de mortier" floors, basins and vats as plaster = yes, because the list uses "enduite de mortier" for plastering. This was applied to all such items.
- **Hirschfeld and Eshel sizes:** settled as longer side = length (B on 22, A on 2).
- **Magen & Peleg:** B was more complete on openings and directions. The 4 "neither" items are opening counts where both readers left out windows, slits or shared doorways.
- **Grave sizes** come from scaled plans, but the readers scaled different graves.
- **Bar-Adon T3:** A's "0 steps" has no support; left blank, low confidence.

## Limits

- **Unresolved fields.** The third reading covered the attribute fields only. `construction`, `period` and `in_window` keep `A|B` where the readers differed (most IIIA rows).
- **No converted positions.** IIIA positions are plate cells. Hirschfeld's site grid is printed north first ("1249/1929"), so the script leaves it unconverted and flags it; it is a site grid, so no feature position is lost. Bar-Adon's grid is in a form the script does not read. Magen & Peleg and Eshel print no grids.
- **Text-only copies.** Hirschfeld, Bar-Adon and Eshel were read from Drive text extractions, without page images. Eshel's per-tomb tables are unreadable in that copy.

## Files

`keyed/<src>_<A|B>[_g1].csv` and logs; `keyed/qumran_C_adjudication.csv`, split into `keyed/<src>_C_adjudication.csv` by `scripts/split_qumran_c.py`; `out/qumran_agreement_toplevel.json`, `out/qumran_to_adjudicate.csv`; `out/<src>_consolidated.csv` for the six sources.
