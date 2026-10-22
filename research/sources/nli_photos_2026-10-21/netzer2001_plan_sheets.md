# Netzer 2001, *Hasmonean and Herodian Palaces at Jericho* I, plans portfolio: NLI library photos, screened reading (21 Oct 2026)

Source: E. Netzer, *Hasmonean and Herodian Palaces at Jericho: Final Reports of the 1973–1987 Excavations*, vol. I (IES, Jerusalem 2001). This is the loose plans portfolio (folding sheets). NLI copy, held as a separate grey box. The cover label reads "… 2001 / B / 1743", with "stacks_s" and "maps" (IMG_0525). Inner pockets carry barcode slips: "Hasmonean and Herodian palac[es] …".

Photos: 24 unprotected HEIC originals, IMG_0525–0558 (with gaps), taken on 21 Oct 2026 between 16:27 and 16:48. Each file's Drive ID, SHA-256, capture time and plan number are in [netzer2001_plan_sheets_originals.csv](netzer2001_plan_sheets_originals.csv). All 24 SHA-256 values were recomputed and match. The images are not in the repo.

## How this was done

1. A screened reader (a subagent) opened only the rows of `nli_photos/sorted.csv` for the portfolio whose `protected` field was empty. **IMG_0559–0564 (sheet series 1–4) were not opened.**
2. Each sheet was read from rotated crops. Captions were confirmed by OCR (`tesseract -l eng`, run on several rotations). Spot heights and locus labels were read from zoomed crops of the full-resolution photo. The 102.87 / 102.80 pair on Plan 12 was read at 2× zoom.
3. The sheets were **not** compared with the Drive PDF of vol. I (`14gko_O7BsyvRT9Il6woaO6MZxUY3EBim`). The PDF's plans may be reduced. A comparison is still to do.

## What the photos cover

| Plan | Caption (as printed) | Photos | Scale / north |
|---|---|---|---|
| 11 | "Plan of Area AA (Buried Palace and Fortified Palace)." | IMG_0533, 0534 (detail), 0535 | 0–5–10 m bar; north arrow |
| 12 | "Plan of Area AC." | IMG_0528, 0530 (detail), 0531 | 0–5–10 m bar; north up |
| 14 | "Plan of the main part of Area AB (Pools Complex)." | IMG_0536; also IMG_0545 (sheet stack) | 0–5–10 m bar; north arrow pointing to sheet left (east up when read along the caption) |
| 15 | "Detailed plan of the Western Garden and its surroundings in Area AB in Stages 2–6. The dotted walls correspond to Stage 7 and the Herodian period." | IMG_0538, 0539 | 0–5–10 m bar; north arrow |
| 22 | – | – | **No Plan 22 sheet identified.** IMG_0542 (indexed "plans 22–23") shows the Plan 23 sheet. |
| 23 | "Detailed plan of the Western Garden and its surroundings in Area AB in Stage [7] and the Herodian period" (stage numeral not legible in OCR; inferred from Plan 15's caption) | IMG_0541, 0542 | scale bar |
| 25 | "Plan of the Hasmonean Garden of the Pools Complex." | IMG_0544; also IMG_0545 | 0–5–10 m bar; north arrow |
| 26 | "Plan of Area AE (Twin Palaces)." Note on the sheet: "FOR DETAILS SEE PLAN 29" | IMG_0547; also IMG_0545, 0546 | 0–5–10 m bar; north to sheet left |
| 29 | "Plan of Areas AG and AL (the Main Wing and part of the Lower Wing of Herod's Second Palace)." | IMG_0548; also IMG_0546 | 0–5–10 m bar; north up |
| 35 | "Plan of the Northern Wing of Herod's Third Palace." | IMG_0551, 0553, 0554 | 0–5–10 m bar; north to sheet left |
| 36 | "Detailed plan of the Northern Wing of Herod's Third Palace." | IMG_0556, 0557 | 0–5–10 m bar |
| – | Portfolio cover, request slips, label | IMG_0525, 0526, 0558 | – |

All the sheets are black-and-white line plans. They use the same conventions throughout:

- solid walls are excavated;
- dashed walls are reconstructed or later;
- labels: loci are A(A)/A(B)/A(C) + number, walls are W + number;
- "EE" and "VS" prefixes mark some levels, and "※" marks floor or bottom spot heights;
- grid squares are numbered along the margins.

**There are no phase colours or phase key on any sheet.** Phases are separated only by sheet (Plans 15 / 23) or by dotted lines (Plan 15).

## Findings

EVIDENCE = drawn or printed on the sheet. INFERENCE = the project's. BK = the reader's background knowledge.

### Plan 14: Pools Complex, Area AB (entry 29)

- EVIDENCE: the sheet covers grid squares 13–21 (east–west along the long axis) by rows 044–047. It shows:
  - **Twin pools** in the centre. They are two large rectangular basins side by side, each with a stair in one corner, separated by a wall, and labelled with A(B) loci. The pool interior spot heights are not legible in the photo at sheet scale.
  - **Pavilion A(B)103** east of the pools (grid 16–18). It is a peristyle of columns around a central unit A(B)14 / [A(B)29], with walls W5–W16. Levels: 100.74–101.16 on the stylobate, 101.07–101.82 in the central unit and 101.40 at its centre. A(B)422, A(B)5, A(B)28 and A(B)16 surround it. A note reads "FOR DETAILS SEE PLAN 16". Next to it, A(B)398 and A(B)399 form a stepped installation (99.58–100.40).
  - **Storeroom row** at grid 19–21: A(B)240, 236, 272, 241, 238 and 233 between walls W303–W306, W309 and W331. Floor ※ levels are 97.62–98.60. Further north are A(B)165/181 and A(B)169. A(B)59/1 is a stepped installation with a 96.60 bottom; A(B)188 and A(B)173 are next to it.
  - **Channels**: parallel channel lines run east–west across the north part (A(B)220, A(B)202). They carry flow arrows and levels of 99.25, 98.75 and 99.23 at their west end, and 98.10, 98.01, 97.95 and 97.75 at the east end along A(B)222 / W332. A row of stones and a pipe cross diagonally at A(B)171 / [A(B)223] (97.81–98.37).
  - **Southern bathing / miqveh units** (grid 13–15):
    - A(B)9, stepped, bottom 98.20;
    - A(B)64, 99.26;
    - A(B)243, stepped, 99.08 / 98.85 / 99.62;
    - A(B)25 / A(B)131, 100.48 / 100.79;
    - A(B)211, EE 101.15;
    - A(B)78 / A(B)125 / A(B)123, a stepped unit to the south.
  - **Aqueduct**: a thick dashed curving line (AB50 → AB14 → A(B)183, with EE 98.54 / 100.59) sweeps from the SW and continues SE as W1111 / W1112 past AB12 / A(B)208. Levels nearby: 100.69, 100.62 and EE 99.60. A second straight channel line, W247, runs east–west at 100.96–101.31.
- INFERENCE: Plan 14 is the plan of the twin-pool complex itself. The sheet carries no phase key, so it does not say which basin is the "northern early Hasmonean pool" of the entry 29 test or when the two were joined. That attribution still rests on Netzer 2001 text / Trümper 2018. No inlet or outlet symbol on the pool walls could be read at photo resolution. The sheet adds the storeroom and channel network north of the pools and the aqueduct line to the south, but no measuring origin for a "collected waters" deposit.

### Plan 12: Area AC, pools A(C)94 and AC44 (`decisions-jericho-contacts`)

- EVIDENCE: **A(C)94** is a square stepped pool. AC17, AC21 and AC19 are inside it. The steps on its west side carry levels 100.07, 100.07, 101.47 and 102.24. Its floor ※ levels are 99.65, 99.74, 99.85, 99.45 and 99.65. Its rim / inner top is 102.67 and 102.75, and 102.15 on the SE.
- EVIDENCE: at **the NW corner of A(C)94**, a pair of spot heights **"102.87" over "102.80"** sits where a **diagonal double line (a pipe or channel) meets the pool's outer wall**. The line runs NW–SE from a small circle at the AC61 / AC60 boundary (with 103.08 and 103.30 nearby). The outer corner of the pool enclosure is 103.14. Wall W319 lies to the west, and spot heights of 103.21 and 103.05 are just west of the corner.
- EVIDENCE: **AC44**, east of A(C)94, is a stepped pool. Its steps run from 100.70 to 102.28, its floor is ※ 99.50 / 99.54, and it contains AC80 / AC81. A later diagonal channel or aqueduct (thick dashed line, with 101.95, 94.79, 97.95 and 100.80) cuts across its east part past AC79 and on to AC52 / AC82 (VS 101.64). A(C)146 and W318 lie between the two pools, with EE 102.24. W1084 is at the north, with EE 101.84.
- EVIDENCE: **A(C)90**, north of the pools, is a large rectangular unit. Its levels are 104.05, 103.82, 103.36 and 104.50; (AC37) is next to it. Further east are AC68, AC75, AC74, AC72, AC29 and AC69.
- EVIDENCE: the sheet does **not** say whether 102.87 and 102.80 are invert, centre, crown or wall-top. No section is drawn, no benchmark is stated and no legend for the point type is given.
- INFERENCE: the sheet confirms that 102.87 / 102.80 belong to the NW pipe junction of A(C)94. The pipe's upper end is near AC60 / AC61. It does not settle the `record_needed` question ("Invert/centre/crown versus other point definitions"). A keyed section or level register is still needed.

### Plan 11: Area AA (Buried and Fortified Palace)

- EVIDENCE: the central courtyard [A(A)102] / [A(A)104] is bounded by W17–W20. The ranges of rooms AA2–AA5 lie to the south, AA1 and AA81 to the SW, and A(A)407 / A(A)87 along W42. The north part (Area AC overlap) shows the curving channel lines and AB60–AB62 / AB14. A note reads "FOR DETAILS SEE PLAN 23". The sheet also shows A(A)375 / 383 and AA30.
- INFERENCE: this is the Hasmonean palace-fort area. The water features on the sheet are channels crossing its north side, not pools.

### Plan 15 and Plan 23: Western Garden, Area AB

- EVIDENCE: Plan 15 shows Stages 2–6, with dotted walls for Stage 7 and the Herodian period. At photo resolution it shows a stepped unit near the centre, stone-built channels and the garden enclosure; locus numbers were not read.
- EVIDENCE: Plan 23 shows the same area in the later stage(s).
- INFERENCE: these are the phase-separated details for Plan 14's south-west quarter.

### Plan 25: Hasmonean Garden of the Pools Complex

- EVIDENCE: a large rectangular garden enclosure, labelled SA1–SA23, runs along its edges. Double channel lines follow its west and east sides. Wall W1178 is at the north. Spot heights are about 97–99. At the south edge are A(B)176, 180, 182, 185, 203, 418–426 and W296–W312.

### Plan 26: Area AE (Twin Palaces)

- EVIDENCE: the two parallel palace units (AE rooms) have a **pool with a stair** in their SW (AE103, with AE97). A channel enters from the south-west (AB65 → W1113). The enclosure wall is W1045 / W600. At the east end are the E2/11–E2/13 units ("FOR DETAILS SEE PLAN 28/29").

### Plan 29: Areas AG and AL (Herod's Second Palace)

- EVIDENCE: the main wing has a peristyle court (AG). The lower wing (AL) has a large rectangular pool or sunken court AL255 / AL307 and stepped installations, and E4/1–E4/10 at the south.

### Plans 35–36: Northern Wing of Herod's Third Palace

- EVIDENCE: the sheets show:
  - peristyle courts B55, B64 and B70;
  - the round hall B68 (a domed bath / frigidarium-type room);
  - bath suite rooms B65–B69, B73 and B80;
  - a line of columns along the south ("B65").
- EVIDENCE: Plan 36 adds spot heights (about 76–80, read at low resolution) and the wall numbers.

## What these sheets do NOT say

- They give no phase colours.
- They do not state what the 102.87 / 102.80 points are or give a benchmark.
- They draw no sections.
- There is no Plan 22 sheet among the photos.
- No sheet covers Tell es-Sultan or the ground north of it.
- There is no explicit symbol for pool inlets or outlets.

## Withheld

Nothing withheld from the opened sheets. **IMG_0559–0564 (sheet series 1–4, protected) were not opened.** No opened sheet covers the SULTAN-1 strip, the Jericho escarpment caves, Qumran or Kh. ʿAlmit.

## Still missing

- Plan 22 (not photographed or not found).
- Plans 13, 16 (referred to on Plan 14), 28 and the other sheets.
- A comparison with the vol. I PDF text for the A(C)94 pipe description.
- An enlarged photo of the Plan 14 pool interiors to read their levels.
