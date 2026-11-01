# Concordance reader B — run 28 log

- Reader: concordance reader B (independent of reader A; no `keyed/concordance_A*` file opened).
- Started 2026-11-01T03:01:23Z; finished 2026-11-01T03:13:03Z (UTC).
- Output: `keyed/concordance_B.csv` (36 rows, written with Python `csv`, UTF-8).

## What was read

Every ʿAtiqot 41.2 article with id 2544–2593, in id order, from the text files in
`scratchpad/atiqot/text/vol-041/iss-2/` (English Part 2): 2544, 2546, 2548, 2550, 2553, 2554, 2556,
2559, 2560, 2562, 2564, 2566, 2569, 2571, 2573, 2575, 2577, 2579, 2581, 2582, 2583, 2584, 2585,
2586, 2587, 2588, 2589, 2590, 2591, 2592, 2593. Find reports and catalogue-heavy sections
(coins, glass, metal, bones) were read for their prose, notes and captions. A keyword search over the
same files was run only afterwards, as a cross-check; it found no statement not already noted.

- 2585 (Region XI): the text layer lacks printed pp. 177–179. The bucket PDF
  `atiqot/pdf/vol-041/iss-2/2585_…pdf` was downloaded and those three pages were rendered and read as
  images. They contain no identity statement (only a general failed-identification remark, below).
- Bucket PDFs 2571, 2586, 2588 were opened only to check page numbering (no printed folios on
  those one-page summaries). Page numbers: 2571 = p. 125 (cited so in other articles' references);
  2586/2587 = p. 185; 2588/2589 = p. 186 (2592 cites XII/61 as p. 186).
- Not consulted: the Hebrew Part 1 texts (not among the files named in the brief).
- Other files opened: `BRIEFS.md`, `describers.csv`, `scripts/render_bucket.py` (to learn the bucket
  access pattern; a separate small listing/download helper was used from the scratchpad).
  Not opened: the Copper Scroll or any edition, candidate lists, ratings, atlas, sandbox results,
  `research/preregistration/`, `RULE.md`, reader A's files.
- Could not read: nothing in scope was unreadable.

## Conventions used in the CSV

- One row per identity statement **and** describer: a sentence citing two earlier surveys (II/3, II/49)
  gives two rows sharing the quote.
- `atq41_keys`: 1993 labels normalised to Roman numerals (OCR "11/3" → `II/3`); printed ranges are
  expanded (`II/20-31` → 12 labels).
- `atq_page`: printed ʿAtiqot 41.2 page where the earlier-survey reference is printed (running heads
  in the text files; first pages inferred from the next running head). Where a sentence starts on
  the previous page, the note says so.
- `ref_type`: `cave_number` / `site_number` when the earlier survey's own number is printed;
  `name` when the earlier feature is identified by its earlier name; `page` for a citation by page
  **and also** for a bare work citation or an uncited "excavated by X" statement (no number, name
  or page printed) — `describer_ref` then says "no page", "no citation", etc.
- `copied` = `yes` only when the 1993 text attributes descriptive content of the feature to the
  earlier source (dimensions, a reproduced section, the earlier excavator's finds or observations).
  Unattributed 1993 descriptions are `no` even when they follow the citation.
- `confidence` (that the text asserts this identity): `high` explicit; `medium` hedged by the
  author ("probably", "apparently") or ambiguous scope; `low` "possibly"/"perhaps" or inferred
  only through a note.

## Counts

| describer | ref_type | rows |
|---|---|---|
| ba72 | — | 0 |
| ben93 | page | 3 |
| ben93 | cave_number | 1 |
| djd3 | cave_number | 4 |
| djd3 | page | 4 |
| other (16 distinct describers) | page | 16 |
| other | name | 6 |
| other | cave_number | 2 |
| **total** | | **36** |

By ref_type: page 23, cave_number 7, name 6, site_number 0. `copied = yes`: 6 rows (II/32, VIII/9+10
section, X/35, XIV/6, XIV/18, XIV/51). Confidence: high 22, medium 11, low 3. The rows cover 49
distinct 1993 labels.

`other` describers: Frumkin 1988 (×5: four Region II rows = Upper Nahal Makuch survey; the 2571 row, p. 16, is probably Frumkin 1988a), Frumkin 1988b / CCR 1979 survey,
Goldfus 1984, Goldfus 1990, Patrich 1988, Patrich & Arubas (unpublished, ×2), Patrich & Arubas 1989
(×2), Patrich (excavations), Wendell Jones (unpublished), Kislev 1992, Kislev & Hartmann 1998,
Eshel & Zissu 1998, 1986 excavation (unnamed), uncited earlier name ('Cave of the Spies'),
Center for Cave Research survey (uncited), Bar-Adon 1989 (×3).

## Findings worth flagging

- **No ba72 identity anywhere in 2544–2593.** The only ba72 references are in 2590 (Region XIII,
  p. 188): Bar-Adon's Nos. 101 and 103 lie in Region XIII but "neither was a cave" and neither is
  matched to a 1993 label; and p. 191 compares XIII/13 with Bar-Adon 1972:126 Site 114 (comparison).
  Bar-Adon's *1989* excavations ('Atiqot HS 9) are cited for XIV/18, XIV/51, XIV/53-54 and are
  coded `other:Bar-Adon 1989`, not `ba72`.
- **ben93** identities occur only in Region II (II/3, II/20-31, II/33-41, II/49). Only one ben93 number
  is printed: II/49 = 1993:334, **No. 7**. The rest are page-only.
- **djd3**: XI/19 = Cave 19 / Q2 (photographs), XI/20 = probably Cave 20, XIII/2 = probably Cave No. 37
  (DJD III p. 12; coordinates in DJD III said to be consistently wrong), plus uncited "de Vaux"
  attributions for XI/18-19 (caption), XII/49, XII/52 (possibly), XII/61.
- **Explicit non-identifications** (not rowed): Region X p. 169 — the 1952 caves "were marked and
  numbered at the time, [but] there is a problem in identifying them topographically; consequently,
  they were renumbered"; Region XI p. 177 — an attempt to identify the caves of de Vaux and of
  Patrich & Arubas "was unsuccessful"; Region XIII p. 188 — some de Vaux caves were located "according
  to the descriptions, see below", but the English text gives no such match except via 2591 (XIII/2).

## Statements considered and not rowed

Same-campaign relabels (not an earlier survey):
- III/13 = 'Cave of the Warrior' (Schick 1998) — 2550 p. 39; repeated 2553 p. 66.
- IV/12 = "Cave 5 in Ariel 1998:133" — 2556 n. 1, p. 82 (coins from the 1993 survey).
- VIII/28 = 'Cave of the Sandal' (Eshel and Zissu 1998; 2000) — 2569 pp. 117, 119; 2575 p. 129;
  2579, 2581, 2582 (all describe the 1993 excavation).
- XIII/2 = field label C-7 — 2590 p. 188; 2591 p. 195.

Blanket or unspecific statements (no 1993 label or no named earlier record):
- 2546 p. 5: dozens of caves "(Aliliyat a-Sich; Goldfus and Golani 1993: 331-335)"; "Sixty-eight karstic
  caves were resurveyed and examined anew"; history paragraph naming the church cave (= II/32,
  rowed from its own entry) and el-Makkuk Cave (no 1993 label).
- 2550 p. 35: "a number of caves … identified as some of the caves excavated by Patrich and Arubas".
- 2550 III/5, 2585 XI/15, XI/16: debris of a previous excavation, excavator not named.
- 2584 p. 169: eight caves "most likely surveyed in the past but never published".
- 2592 n. 2: Site XIV/2 "discovered by Hanan Eshel (pers. comm.)" — no earlier record.

Comparisons or proximity only:
- 2590 p. 191: XIII/13 rock shelters "such as" the monastery at Bar-Adon 1972:126, Site 114.
- 2592 p. 209: excavated cave "near de Vaux's Cave No. 4 (de Vaux 1973)" (no 1993 label given);
  Khirbet Mazin (Bar-Adon 1989:18-20) 1300 m from XIV/2; p. 212 assemblage comparison with the
  'Cave of the Coin' (that cave is rowed from the XIV/18 entry).

Repeats without new describer information:
- 2569 p. 123 Plan 3 caption "Cave VIII/10 (Avi'or Cave …)"; 2564 p. 105 (VIII/10 finds, Kislev 1992)
  and p. 106 Table 3 header "Avi'or Cave (VIII/10)".
- 2569 Table 1: VIII/7 location "As VIII/2" and VIII/14-15 "As VIII/7" — could formally inherit the
  "first examined in 1979" remark of VIII/2; left to the VIII/2 row's note.

Outside the 1993 label system:
- 2591 p. 206: "Rock Shelter C-24 … excavated recently by Gopher … (Cave 24 was previously excavated
  by Patrich [1993])". C-24 has no ʿAtiqot region label and is said to be Gopher's recent excavation;
  not rowed. Main session may wish to review.
