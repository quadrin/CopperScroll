# Plan pass log: reader B, group g2 (ʿAtiqot 41.1, articles 2543 and 2545)

- Start: 2026-10-31T23:47:20Z
- Finish: 2026-11-01T00:15Z
- Files read: `PLAN_PASS.md`, `SCHEMA.md`, and page renders of 2543 and 2545 made with `render_iss1.py`. No other project files were opened.
- Output: `keyed/atq41plans_B_g2.csv` (9 rows).

## Pages looked at

**2543** (42 pages). All 42 were rendered at 70 dpi and checked as 2x2 contact sheets.

| PDF page | Content |
|---|---|
| 1 | English cover |
| 2 | Map IV–VI, a regional map of the cave positions. Not a cave plan, so no row. |
| 3 | Hebrew title and text |
| 4 | **Plan 1**: Cave IV/1 (schematic) |
| 5 | text, photos |
| 6 | **Plan 2**: rock shelter IV/2, plan and section 1-1 |
| 7–12 | text, coins, photos, pottery and a lamp drawing; no plans |
| 13 | **Plan 3**: Cave IV/7, plan and section 1-1 |
| 14–17 | pottery figures and tables, text, coins; no plans |
| 18 | **Plan 4**: Cave IV/8 |
| 19–20 | text, coins, photo |
| 21 | **Plan 5**: Cave IV/17 |
| 22–28 | text, photos, an arrowhead drawing; no plans |
| 29 | **Plan 6**: Cave VI/43 |
| 30 | text, photos |
| 31 | **Plan 7**: Cave VI/46 |
| 32–33 | pottery, photos, text |
| 34 | **Plan 8**: Cave VI/52 |
| 35–42 | photos, small finds, text, tables, notes and references; no plans. Page 40 is the notes and tables page, with no drawing. |

**2545** (7 pages). All 7 were rendered at 70 dpi.

| PDF page | Content |
|---|---|
| 1 | English cover |
| 2 | **Plan 1**: Cave IV/11, and photos |
| 3–7 | text, pottery and vessel drawings, references; no plans |

**Plans found: 9.** There are 8 in 2543 and 1 in 2545. Each plan shows one cave, so the CSV has 9 cave rows.

All plans were then read at 300–450 dpi. Detail crops (600–1000 dpi) were used for the north arrows, the entrance areas, and the complex plans 2543:6 and 2543:8. Coordinates were measured on gridded renders. Scale bars, widths and arrow axes were measured by pixel scans: run lengths along rows and columns, and a principal-axis fit for each arrow.

## Conventions used

- **North arrows.** Every plan has the same half-arrow symbol: shaft, then barbs, then a long narrow point. The narrow point was read as north. Page bearings of north:
  - IV/1: ~66°
  - IV/2: ~77.5°
  - IV/7: ~181°. This arrow points to the bottom of the page; it was checked at 900 dpi.
  - IV/8: 0°
  - IV/17: ~39.5°
  - VI/43: 0°
  - VI/46: ~308°
  - VI/52: ~20°
  - IV/11: ~293°
- **Opening direction.** This is the outward normal of the gap's chord, converted to true bearing as page bearing minus the north bearing. It is given as `X/Y` when within 10° of a sector boundary.
- **Openings and built walls.** An opening is a gap in the **rock** outline. Where a built wall stands in the gap (IV/2, IV/7, IV/17 opening 1), the width and direction are those of the rock gap. The passage the wall leaves open is given in `notes`.
- **Counts of 0 and blank.** `0` in the pillar, step and niche columns means none is drawn on a plan detailed enough to show them. Blank means the drawing is ambiguous. These zeros are drawing observations, not statements by the source.
- **Pillars.** `n_pillars_plan` counts free-standing hatched rock masses read as piers: the front strip in IV/1, the front rock mass in IV/17, and the mass in IV/11. Where many masses could be pillars or fallen blocks (VI/43, VI/46, VI/52), the count is blank and they are described in `other_features`.
- **Sizes.** Lengths and widths are for the main space along its long axis, rounded as instructed. For VI/43 and VI/52 they are left blank, because no single main space can be defined. Approximate overall extents are in `notes`.

## Unclear or unreadable

- **2543:6 (VI/43)**
  - The plan has no legend. Rock is drawn both as crosshatch and as ticked lines, and a double dashed line runs from Entrance I.
  - At Entrance I no gap can be read, so its direction is recorded as `unknown`.
  - Entrances II and III are drawn as very narrow mouths, about 0.25 m and 0.5 m.
  - Widths and sizes are left blank. Confidence is low.
- **2543:8 (VI/52)**
  - There are four entrance arrows. Gaps are readable for entrances 1 and 3. For entrances 2 and 4 the direction comes from the reversed arrow.
  - Widths and sizes are left blank. Confidence is low.
- **2545:1 (IV/11)**
  - The opening is taken at the dashed line, read as a drip line. Area L14 outside it is treated as outside the cave. An alternative reading is given in `notes`.
- **2543:1 (IV/1)**
  - The caption calls it a schematic plan, so sizes are approximate.

## Exposure note

The page renders include each article's running text, and the captions were read as instructed. A few text phrases near plans were visible at render resolution, on 2543 pages 13 and 34 and on 2545 page 2. They were not used. Every value in the CSV was measured from the drawings.
