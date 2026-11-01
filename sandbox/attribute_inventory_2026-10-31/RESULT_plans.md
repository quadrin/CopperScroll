# Plan pass over *ʿAtiqot* 41.1: result

31 Oct 2026. Exploratory. Instructions and merge rule committed before any plan was read (d225775); agreement and merge script committed before any plan file existed (b3eb811). Before keying, the main session viewed one plan page (2539 p. 5, Cave II/1) to write the instructions.

## Result

- **57 cave plans** in the Hebrew part, every one with a north arrow and a scale bar. Two readers each read all of them; 55 caves were read by both.
- **The plans double the opening directions:** 81 of the 431 surveyed features now have one (40 from the text, 41 from plans).
- **Text and plans agree on directions.** On the 12 caves where both give one, 5 match exactly and the other 7 are within one compass point. The plans often show an extra opening that the text does not mention.
- **Plan sizes are weak.** Readers agreed on only 63 % of sizes, and plan sizes match the text within 10 % or 0.5 m for 16 of 27 lengths and 13 of 24 widths. The third reader traced this to scope: one reading took the whole complex, the other the main room. Plan sizes fill only text blanks (26 lengths, 29 widths); treat them as rough.

| Agreement between plan readers (55 caves) | Agree | Compared |
|---|---|---|
| Number of openings | 45 (88 %) | 51 |
| Opening directions (same or neighbouring point) | 45 (88 %) | 51 |
| Size within 10 % or 0.5 m | 62 (63 %) | 99 |

- **Third reading:** 104 items. 40 were trivial (39 a blank against 0 for pillars or steps, where none is drawn). B was right on most opening counts and directions (7 of 8 each), A on most pillar counts. Seven items cannot be settled from the plan (V/49, VII/3, VIII/9, XII/50, XII/53 sizes).

## The merged table (`out/atq41_consolidated_v2.csv`)

Plan values fill blanks only, and each filled field is marked `text`, `plan` or `plan_single` (read by one reader). Where the text has a value and the plan differs, the text stays and the plan value is in `plan_conflict` (31 rows: 25 lengths, 21 widths, 7 directions, 6 opening counts, 3 pillars, 2 steps).

| Attribute (431 features) | Before plans | After |
|---|---|---|
| Opening direction | 40 | **81** |
| Number of openings | 196 | 209 |
| A length | 216 | 242 |
| Pillars (count > 0) | 6 | 11 |
| Steps (count > 0) | 4 | 4 |

- Caves with two or more openings: 35. 21 of them now have directions and 18 were in use in the window.

## Decisions taken during the pass (all before agreement was computed)

- One plan reader wrote labels in the caption's order ("49/V"); the merge script normalises them (fe3c56d).
- Plan 2561:1 is excluded: it is captioned "57/X" like Plan 3, but it sits in the 35/X entry, which cites it. Both readers flagged it.
- An `undecidable` third-reading value counts as blank.

## Limits

- Some plans show only part of a complex (VIII/9, VI/43, VI/52), or have mouths closed by built walls (counted as openings, noted). Two Region VII scale bars look misprinted (20 m bars that give caves over 100 m long); those sizes are low confidence.
- Readers saw some article text on the rendered pages. They report that every value was measured from the plans.

## Files

`keyed/atq41plans_<A|B>_g<1-4>.csv` and logs; `keyed/atq41plans_C_adjudication.csv`; `out/atq41plans_agreement.json`, `out/atq41plans_to_adjudicate.csv`; `out/atq41_consolidated_v2.csv`.
