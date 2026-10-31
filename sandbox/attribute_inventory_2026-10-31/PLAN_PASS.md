# Plan pass over *ʿAtiqot* 41.1: instructions and merge rule (frozen before any plan is read)

31 Oct 2026. Source 1's English text (*ʿAtiqot* 41.2) prints no plans; they are in the Hebrew part 41.1. This pass reads those plans for the attributes the text leaves open: opening count and direction above all.

## Reader instructions

1. Read only this file, `SCHEMA.md`, and the 41.1 article PDFs of your group. Render pages with `render_iss1.py` (path in the brief). Do not open the Copper Scroll text or any commentary, the project's candidate lists, ratings or atlas files, the keyed text files (`keyed/atq41_*`), or the other reader's plan file.
2. Look at **every page** of each article at low resolution (about 60–80 dpi) to find the plans. A plan is a drawing of a cave or structure seen from above. Then read each plan at 150–200 dpi, cropping if needed.
3. For each plan, record which cave or feature it shows. Use the survey label printed in the caption or on the drawing (e.g. `II/1`); the caption has the form "תוכנית N. מערה II/1 …" (Plan N, Cave II/1). One plan can show several caves: write one row per cave.
4. **North arrow and scale.** Record whether the plan has a north arrow and a scale bar. Without a north arrow, record no direction. Without a scale bar, record no size.
5. **Openings.** An opening is a gap in the outer rock outline that leads outside. Count only openings to the outside, not passages between chambers. Record windows or skylights only if marked, in `notes`.
6. **Direction an opening faces** = the direction from the inside of the cave out through the gap, perpendicular to the gap. Use the plan's north arrow, which may not point to the top of the page. Give the 8-point compass value (N, NE, E, SE, S, SW, W, NW). If the bearing is within 10° of the boundary between two points, give both, joined by `/` (e.g. `E/NE`).
7. **Sizes from the scale bar:** the greatest length and the greatest width of the main space, to the nearest 0.5 m (sizes over 20 m to the nearest 1 m). Also the width of each opening, to the nearest 0.25 m.
8. **Other drawn features:** count rock pillars or piers, steps (each tread line), niches, and built walls. Note cisterns, basins or channels that are drawn and labelled.
9. If the drawing is unclear, record the row with `confidence = low` and say why. Do not guess.

## Output

`keyed/atq41plans_<reader>_<group>.csv`, written with Python's `csv` module, with these columns in this order:

`plan_ref` (article id : plan number, e.g. `2539:1`), `pdf_page` (1-based), `caption_label` (the cave label as printed), `key` (the label in survey form, e.g. `II/1`), `north_arrow` (yes/no), `scale_bar_m` (length of the bar in m; blank if none), `n_openings_plan`, `opening_dirs_plan` (`;`-separated, one per opening, same order as `opening_widths_m`), `opening_widths_m`, `max_length_m`, `max_width_m`, `n_pillars_plan`, `n_steps_plan`, `n_niches_plan`, `other_features`, `confidence` (high/medium/low), `notes`.

Also write `keyed/atq41plans_<reader>_<group>_log.md`: every page looked at, the plans found, anything unreadable, start and finish times (UTC).

## Agreement and merge (fixed now)

- Agreement between readers A and B is measured on matched `(key)` rows: exact `n_openings_plan`; directions the same or neighbours (a `/` value matches either point); sizes within 10 % or 0.5 m.
- Disagreements are settled by a third reading of the plan, as for the text.
- **Merge into `out/atq41_consolidated.csv`:** a plan value fills a field only where the text left it blank (`n_openings`, `opening_dirs`, `length_m`, `width_m`, `n_pillars`, `n_steps`). Where the text gives a value and the plan disagrees, the text value stays and the plan value goes in a `plan_conflict` column. Every filled value is marked with its source (`text` or `plan`).
