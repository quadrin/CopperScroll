# Plan pass log: reader A, group g1 (ʿAtiqot 41.1, articles 2538, 2539, 2540)

- Start: 2026-10-31T23:47:20Z
- Finish: 2026-11-01T00:21Z
- Read: `PLAN_PASS.md`, `SCHEMA.md`, and the three 41.1 article PDFs through `render_iss1.py`. No other project file, keyed file, web or Drive source was opened.
- Output: `keyed/atq41plans_A_g1.csv` (11 rows, one per cave or structure).

## Pages looked at

Every page was rendered at 70 dpi and viewed in contact sheets of three pages each.

| Article | Pages | Contents found |
|---|---|---|
| 2538 (Region I) | 1–6 | p1 cover; p2 Map I (regional map, not a plan); p3–4 text; **p5 Plan 1 (14/I)** with photos and finds; p6 text, finds drawing (fig. 4) |
| 2539 (Region II) | 1–24 | p1 cover; p2 Map II; p3–4 text and photos; **p5 Plan 1 (1/II)**; **p6 Plan 2 (3/II)**; p7 finds and photo; **p8 Plan 3 (4/II)**; p9 finds; **p10 Plan 4 (5/II)**; p11 text and photo; **p12 Plan 5 (11/II)**; p13–17 text, photos and coins; **p18 Plan 6 (49/II)**; **p19 Plan 7 (51/II)**; **p20 Plan 8 (61/II)**; p21 finds and photo; p22–24 text, notes and references |
| 2540 (Region III) | 1–11 | p1 cover; p2 Map III; p3–6 text and photos; **p7 Plan 1 (8/III, two level plans and a section)**; p8 coins and text; **p9 Plan 2 (11/III)**; p10–11 text, notes and references |

There are 11 plans and 11 cave or structure rows. The three regional maps are not plans. The sections were used only to understand the plans.

## How each plan was read

- Each plan was cropped at 150–250 dpi with a grid in PDF points, then at 300–800 dpi for north arrows, lips and doorways.
- **Scale.** Each scale bar was measured from runs of dark pixels at 300 dpi; the rate in pt/m is given in `notes`. Distances on the plan come from grid crops and pixel scans of rows and columns, accurate to about ±1–2 pt.
- **North arrow.** The arrows are half-arrowheads with a notched base. The shaft runs on from the base, and the sharp tip is read as north. The bearing on the page was fitted as the main axis of the arrow's dark pixels. Three plans have the tip pointing down the page: 3/II and 11/II point straight down and 61/II points lower right. They were recorded as drawn.
- **Opening direction.** This is the outward perpendicular to the line joining the two lips, minus the arrow's bearing on the page.
- **Opening width.** This is measured lip to lip. A lip is where the cave wall meets the cliff face or ends.
  - A mouth that flares is measured at the cliff face, and the narrower neck inside is given in `notes` (3/II, 11/II).
  - A rock gap closed by a built wall is still counted as an opening and noted (14/I, 51/II, 61/II, and part of 49/II).
- **Main space.** For a cave, this is the largest single chamber. Where the chambers form one continuous space, it is the whole interior (11/II and the lower level of 8/III). For a built structure (4/II, 5/II), the outer size of the building is given, with the room sizes in `notes`.
- **Pillars, steps and niches.**
  - `0` means none is drawn on a clear and complete plan.
  - `n_steps_plan` is blank for 49/II, where three small arcs may or may not be steps.
  - `n_niches_plan` = 2 for 5/II counts the stippled recesses beside the door. The plan does not show whether they are niches or windows.
- All other drawn features are in `other_features`. Directions there are given as page positions (page-top and so on).

## Unclear or difficult points

- **8/III** (confidence low): the drawing is very light. Both openings, one per level, are defined by where the solid rock outline ends, with only ticked or dashed lines across them. A single north arrow serves both level plans. The far end of the lower level is dashed.
- **3/II**: the section marks two entrance arrows, but the plan shows only one gap in the rock outline (the L4 mouth). The upper (L5) level is not drawn as a gap in the plan.
- **4/II**: the doorways are drawn as tick-edged threshold fills in the wall, not as clear gaps. No doorway is drawn for room L4.
- **Borderline values**:
  - The 61/II direction (about 303°) is about 10.5° from the W/NW boundary.
  - Several widths fall near a 0.25 m rounding step: 11/II about 4.65 m, 49/II about 1.85 m, 61/II about 13.85 m.
- **What I saw of the text**: the low-resolution contact sheets showed article text. I did not read the text to set any value. While scanning, I did glimpse fragments of a few descriptions, such as the wording on the 4/II doors and the 11/III note on two openings with rock between them. All recorded values come from measuring the plans.
