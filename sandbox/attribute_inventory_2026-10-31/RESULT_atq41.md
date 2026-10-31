# Attribute inventory, source 1: the 1993 northern Judean Desert cave survey (*ʿAtiqot* 41.2)

31 Oct 2026. Exploratory: no rating, ledger, ACTIVE_TEST or atlas change. Schema, reader instructions and source list were committed before any keying (9e5818f); the agreement script was committed before any keyed file existed (3f0e4fb).

## Result

- **An inventory of 431 surveyed caves and sites, with an attribute table** (`out/atq41_consolidated.csv`), from Wadi el-Makkuk and the Jebel Abu Saraj and Qurunṭul cliffs above Jericho to the escarpment above Ḥorbat Qumran and Naḥal Kidron (Regions I–XV).
- **The two readers agree closely.** On the 426 whole features both keyed, every value both gave was the same: 521 dimensions, 190 opening counts, 37 opening directions, 4 step counts. Class agreed on 96 %. Every disagreement was one reader leaving a value blank (37 items) or choosing a different class (18). A third reading settled all 58 items: 32 for reader A, 26 for reader B.
- **What the survey records well:** position and size. Opening directions, steps, plaster and pillars are rare.

| Attribute (431 labelled features) | Features with it |
|---|---|
| Printed grid, converted to WGS84 | 416 |
| A dimension | 216 |
| Number of openings | 196 (1: 163; 2: 27; 3–5: 6) |
| Opening direction | 40 |
| Step count | 4 |
| Pillars | 6 |
| Plaster | 6 |
| Use in the Hellenistic–Early Roman window stated (`in_window` = yes, both readers) | 58 (another 69 where the readers differ, unresolved) |

Caves with two or more openings: 33. Of these, 13 have a direction and 18 were in use in the window. They lie mostly in Regions XIV (9), VIII (5), IV (4) and VI (4).

## Readers

- Eight reader instances (A and B for each of four groups of articles) and one third reader. None saw the Copper Scroll text, candidate lists or the other reader's files.
- Rows keyed: A 932, B 989. On all rows, including sub-features (chambers, niches, doorways), the agreement script reports: class 0.85, dimensions within 10 % or 0.2 m 0.92 (1,023 compared), opening counts 0.90 (220), directions 0.76 (55), steps 7 of 8. These lower figures come from the readers lettering sub-features differently (`.a`, `.b`), and from counting one blank as a disagreement. The whole-feature figures above (`out/atq41_agreement_toplevel.json`, computed after the frozen script, exploratory) separate the two.
- Third-reading patterns: reader A sometimes put an entrance's size on the cave; reader B called niches "caves" (X/1–4, parts of XIV); both were inconsistent about "unknown" opening counts.

## Limits

- **No plans.** The English part of the volume (41.2) prints only captions. The plans are in the Hebrew part (41.1). Nothing was measured from a plan, which is why directions are sparse. *ʿAtiqot* 41.1 is in the bucket (`atiqot/pdf/vol-041/iss-1/`), so a plan pass could add directions and opening counts.
- **Period fields differ** between readers for 121 features (`period`) and 69 (`in_window`). These were not part of the third reading, and stay as `A|B`.
- **Page numbers:** first pages and the excavation summaries carry no printed number; readers took them from the next page or from cross-references, and said so in notes. XV/3 is `art2593`.
- **Grids:** read as the old Israel grid (EPSG:28191; 5-digit values in 10 m units). The check point Qumran 193.3/127.7 converts to 31.7417 N, 35.4561 E. One grid (XII/49, printed 12749/19288) falls outside the survey area and is not converted. It looks like a misprint.
- **Text layer:** Region XI pp. 177–179 have no text layer; both readers keyed XI/1–15 from page images.
- **Process note:** one reader reported that a hook displayed the repository's `AGENTS.md` when it opened `SCHEMA.md`; it did not use it.

## Files

- `keyed/atq41_<A|B>_g<1-4>.csv` and logs: the readers' files as delivered. `keyed/atq41_A.csv`, `keyed/atq41_B.csv`: merged. `keyed/atq41_C_adjudication.csv`: third reading.
- `out/atq41_validation.json`, `out/atq41_agreement.json`, `out/atq41_pairs.csv`: the frozen script's output. `out/atq41_agreement_toplevel.json`: whole-feature agreement.
- `out/atq41_consolidated.csv` (`scripts/consolidate.py`): one row per whole feature, with grid, WGS84 position and the attribute fields.

## Next

1. A plan pass over *ʿAtiqot* 41.1 for opening directions, opening counts and plan positions of features.
2. Key the Qumran sources (`sources.csv` orders 2–7: IIIA's lists, Magen & Peleg, Hirschfeld, Eshel et al., Bar-Adon, IVA).
3. Run 28's rule, committed before any benchmark item is scored.
