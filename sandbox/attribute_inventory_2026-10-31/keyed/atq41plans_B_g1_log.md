# Plan pass, reader B, group g1: log

Source: *ʿAtiqot* 41.1 (Hebrew), articles 2538 (Region I), 2539 (Region II), 2540 (Region III).
Start: 2026-10-31T23:47:20Z. Finish: 2026-11-01T00:16:09Z (UTC, from `date -u`).

Read only PLAN_PASS.md, SCHEMA.md and the three article PDFs (through `render_iss1.py`). Page numbers are 1-based PDF pages. I checked this: page 1 renders the IAA cover sheet.

## Pages looked at (all at 70 dpi, then plan pages at 130–500 dpi)

| Article | Pages | Content |
|---|---|---|
| 2538 | 1 | cover sheet |
| | 2 | Map I (regional map, not a cave plan) |
| | 3–4 | text |
| | 5 | **Plan 1**, photos, pottery |
| | 6 | text, stone object drawing |
| 2539 | 1 | cover sheet |
| | 2 | Map II (regional map) |
| | 3–4 | text, photos |
| | 5 | **Plan 1** (plan + section), pottery |
| | 6 | **Plan 2** (plan + section) |
| | 7 | photo, pottery |
| | 8 | **Plan 3** (plan + section), text, photo |
| | 9 | glass drawing, text |
| | 10 | **Plan 4** (plan + section), photos |
| | 11 | text, photo |
| | 12 | **Plan 5** (plan + section), pottery, photo |
| | 13–17 | text, photos, coins (no plans) |
| | 18 | **Plan 6** (plan + section), photos |
| | 19 | pottery, **Plan 7** (plan only) |
| | 20 | pottery, **Plan 8** (plan + section) |
| | 21–24 | pottery, photo, text, references (no plans) |
| 2540 | 1 | cover sheet |
| | 2 | Map III (regional map) |
| | 3–6 | text, photos |
| | 7 | **Plan 1** (upper-level plan, lower-level plan, section), photos |
| | 8 | coins, text |
| | 9 | metal object, **Plan 2**, coins |
| | 10–11 | coins, text, notes, references |

## Plans found (11), one cave or structure each, so 11 rows

2538:1 I/14 (p5); 2539:1 II/1 (p5); 2539:2 II/3 (p6); 2539:3 II/4, a built cell (p8); 2539:4 II/5, a built cell (p10); 2539:5 II/11 (p12); 2539:6 II/49 (p18); 2539:7 II/51 (p19); 2539:8 II/61 (p20); 2540:1 III/8 (p7); 2540:2 III/11 (p9).

## Method notes

- **Coordinates and scale bars.** I measured coordinates in PDF points on crops with a grid overlay. I found the scale-bar ends and north-arrow pixels by tracing dark pixels.
- **North arrows.** The arrow is a thin shaft with a narrow filled head. North is the pointed tip. Several arrows do not point up the page:
  - II/3 and II/11 point to the page bottom.
  - II/61 points lower-right; III/8 points right and down.
  - II/4 points right; II/49 and II/51 point left.
  - I/14 points upper-left.
  - Each row's `notes` gives the arrow's page bearing.
- **Facing directions.** Each opening is given as an 8-point direction, with the approximate true bearing in `notes`.
- **Main space.** For a cave with several chambers (II/3, II/49, III/11) I used the largest single chamber. For II/4, a building of three rooms, I used the interior inside the outer walls. `notes` gives the whole-cave size.
  - Length is the greatest extent along the main axis, and width the greatest extent across it.
  - Sizes are to the nearest 0.5 m (to the nearest 1 m over 20 m) and opening widths to the nearest 0.25 m.
- **Walled mouths.** A mouth that a built wall spans (I/14, II/49, II/51, II/61) is still counted as one opening, because it is a gap in the rock outline. `notes` says so.
- **Blank counts.** Blank in `n_pillars_plan`, `n_steps_plan` and `n_niches_plan` means none is drawn. No steps were found on any plan.

## Problems and uncertain readings

- II/4 is a built three-room cell. No doorway is drawn and the front walls are dashed (not preserved), so `n_openings_plan` is blank and confidence is low.
- In II/3, the section shows a possible second, upper opening (L5) that the plan does not outline. It is not counted.
- III/8 has two levels that open on the same face. I counted one mouth; it could be counted as two.
- These facings fall within about 10° of a compass-point boundary and are given as two points: II/3 (W/SW), II/49 (N/NW), II/51 (N/NW), III/8 (SE/S), III/11 L1 (S/SE). The II/61 facing (~304°) is about 11° from a boundary, so it is given as NW alone.
- In I/14, the plan does not show whether the row of stones across the mouth closes it. A forecourt enclosed by walls lies in front of the mouth.
- No plan was unreadable. The III/8 plans are drawn in light grey lines but could be read at 200–350 dpi.
