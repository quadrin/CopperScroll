# atq41, reader A, group g3: keying log

- Start: 2026-10-31T22:02:54Z
- Finish: 2026-10-31T22:23Z
- Output: `keyed/atq41_A_g3.csv`. It has 239 rows. 141 of them are top-level caves or sites; the other 98 are chambers or other sub-features.

## Read in full (pypdf text layer, checked against page renders)

| Article | Content | Printed pages |
|---|---|---|
| 2559 | Aronshtam, Region V: Table 1 and the Excavated Caves V/50 and V/59 | 85-95 (Table 1 pp. 85-90; V/50 pp. 90-91; V/59 pp. 92-93; captions pp. 94-95) |
| 2560 | Eisenberg, Excavation of Cave V/49 (summary) | 97 (no folio on the page; p. 97 is taken from the cross-reference in 2559's references) |
| 2566 | Abeles, Region VII | 109-115 |
| 2569 | Eshel and Zissu, Region VIII: Table 1 pp. 117-121, text pp. 121-122, captions p. 123 | 117-123 |
| 2571 | Eshel and Zissu, Excavation of Cave VIII/9 (summary) | 125 (no folio on the page; p. 125 is taken from the cross-reference in 2569's references) |
| 2583 | Weiss, Region IX: Table 1 pp. 167-168, IX/14 p. 168 | 167-168 |

## Pages rendered

The pages were rendered with `atq41_tools/render_page.py` into `/tmp/claude-0/-home-claude/729c536d-b448-586f-923d-45ae3ca7c96d/scratchpad/reader_A_g3/`. The numbers below are PDF page indices, counted from 1. They were used to check the table layout, which the text layer breaks, and to check the printed page numbers:

- 2559: pp. 2-7 (printed 85-90, Table 1)
- 2560: p. 2
- 2566: pp. 2, 5, 6, 7 (printed 109, 112, 113, 114)
- 2569: pp. 2-7 (printed 117-122)
- 2571: p. 2
- 2583: pp. 2-3 (printed 167-168)

## Not available or unreadable

- No plans. These Part 2 (English) PDFs hold only scanned text pages; every page is one scanned image with a text layer. The plans and photographs are in Part 1 (Hebrew), which is not in this group. Captions only, not the drawings, exist for:
  - V/50 Plan 2, V/59 Plan 3, V/64 Plan 1
  - V/49 Plan 1
  - VII/1 Plan 1, VII/3 Plan 2
  - VIII/2 Plan 1, VIII/7 Plan 2, VIII/9-10 Plans 3-4, VIII/6 Plan 5
  - VIII/9 Plans 1-2 (art. 2571)
  - IX/14 Plan 1
- So no value comes from a plan. `dims_basis` is never `plan_scaled`, and no direction was taken from a north arrow.
- I used some figure captions and recorded each in `figure`:
  - VIII/9: 2 entrances (Fig. 1, art. 2571)
  - VIII/10: 1 entrance, and its position above VIII/9 (Fig. 1 and Plan 3)
  - V/49 halls (Fig. 2, art. 2560)
  - VIII/28 (Fig. 3)
- Where a photo caption gives only a viewing direction ("looking west"), I did not key it as an opening direction. It is mentioned in `notes`.

## Not keyed (no attribute beyond class)

- V/30 ("A small cave"), V/33, V/39 and V/41 ("A large cave")
- VIII/22 and VIII/23 (not examined, inaccessible)
- Numbers absent from the tables or named only inside a group range: V/5, V/8, V/31-32, V/36-37, V/42-45, V/47 and V/65
- The "seven other caves" around the cliff in Region VII (p. 114)

## Conventions applied

- `a x b` dimensions: the larger value goes in `length_m` and the smaller in `width_m`, unless the text labels them.
- Minimum values are keyed with a note: V/6 "at least 10 m" and VIII/2.a "in excess of 2.5 m".
- Wall thickness is keyed as `width_m`: V/57.f and V/59.a.
- Class mapping:
  - Printed "niche", "recess" or "cavity" (small) → `other`.
  - Stand-alone "passage" in the Region VII and V lists → `cave`. Region VII counts its passages among its 16 caves.
  - Passages inside a cave → `other`.
  - Printed "chamber" or "room" → `chamber` or `room`.
  - Kokh → `burial`. Burial cave → `tomb`.
  - Chimney or shaft → `pit`.
- Construction from a group header: used when the header says "natural" for all members (V/1-11, V/22-27, V/28-29, V/51-56, V/60-62, V/65-69). Where the header says "most are natural" (V/12-21, V/30-47), construction is `unknown`.
- Grid references are in the old Israel grid (5-digit map refs), keyed as `OIG`.
  - Group map refs → `site_grid`.
  - A sub-feature takes its parent's grid → `site_grid`.
  - "As VIII/x" is resolved to the referenced grid, and the printed form is in `notes`.
  - V/63 and V/64 have no map ref → `text_only`.
- Compass words in relations ("3.3 m north of the opening") are not converted to `rel_bearing_deg`. They are in `notes`.
- Opening position used as facing: V/12 ("in the northeast/northwest"), V/19 ("in the east") and VII/11 (entrance in its southern wall) are keyed as facing those directions. Confidence is medium.
- `in_window`:
  - `yes` when Hellenistic, Late Hellenistic, Hasmonean, Herodian, Early Roman, Second Temple, or 1st c. BCE-1st c. CE material or use is reported for the feature.
  - `no` when the source dates use only to other periods, or says the cave was not used.
  - `unknown` when use in antiquity is mentioned without a period, or the window material is not tied to the feature: VIII/26 coin on the slope below, VIII/10 documents reported jointly with VIII/9, group headers "no evidence of use in antiquity".
  - Blank otherwise.
- Local ids `VII/x1` (eight unnumbered cave entrances north of VII/11) and `VII/x2` (retaining wall NE of them) were assigned by me, because the source gives no number.

## Problems and doubts (details in row notes)

- **V/49 pillars.** The table says "a wide pillar" (p. 88). The summary says "stone columns" (p. 97). Keyed `n_pillars = unknown`.
- **V/64.1 width.** Printed as 6.1 m, which is wider than the passage is long. Possibly a misprint; keyed as printed.
- **VIII/42 grid.** The northing 14102 is out of sequence with the neighbouring entries; keyed as printed.
- **VIII/27.** The site is named for the terrace, but its row describes a 2 x 2 m cave. Keyed as terrace VIII/27 plus cave VIII/27.a (low confidence).
- **VIII/38 and VIII/48.** The dimensions may belong to the entrance rather than the cave (confidence medium and low).
- **V/14.** The unlabelled northern niche (0.1 x 0.8 m) is not assigned to V/14.
- **AGENTS.md.** When I read SCHEMA.md, a tool hook automatically showed the contents of `/home/claude/cs/AGENTS.md`. I did not open it deliberately and did not use it. No other file in /home/claude/cs was opened apart from SCHEMA.md, READER_INSTRUCTIONS.md and my own outputs.
