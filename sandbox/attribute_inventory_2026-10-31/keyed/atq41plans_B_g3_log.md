# Plan pass, reader B, group g3: log

- Source: *ʿAtiqot* 41.1 (Hebrew), articles 2547, 2549, 2551, 2552, 2555, 2558.
- Started: 2026-10-31T23:47:20Z. Finished: 2026-11-01T00:20Z.
- Output: `keyed/atq41plans_B_g3.csv`, 13 rows.

## Pages looked at

Every page of each article was rendered at 60 dpi and checked (81 pages):

| Article | Pages | What they hold |
|---|---|---|
| 2547 | 1–15 | p1 cover; p2–6 text, table and photos; **p7 Plan 1 (64/V)**; **p8 Plan 2 (50/V)**; p9–10, 12–13 finds; **p11 Plan 3 (59/V)**; p14–15 notes and references |
| 2549 | 1–18 | p1 cover; p2 text and photo; **p3 Plan 1 (49/V)**; p4–18 finds, text and references |
| 2551 | 1–15 | p1 cover; p2 Map VII (a map, not a plan); p3 text and photo; **p4 Plan 1 (1/VII)**; p5–11 finds and coins; **p12 Plan 2 (3/VII)**; p13–14 text; p15 notes and references (the plan caption appears only in text) |
| 2552 | 1–12 | p1 cover; p2 Map VIII (map); p3 photo; p4, 7–9 table; **p5 Plans 1 (2/VIII) and 2 (7/VIII)**; **p6 Plans 3 (10/VIII, with section of 9/VIII and 10/VIII) and 4 (9/VIII)**; **p10 Plan 5 (6/VIII)**; p11–12 text and references |
| 2555 | 1–17 | p1 cover; **p2 Plan 1 (section only)**; **p3 Plan 2 (9/VIII)**; p4–17 photos, finds, documents and references |
| 2558 | 1–4 | p1 cover; p2 Map IX (map); p3 text and table; **p4 Plan 1 (14/IX)** |

Each plan was then read at 200, 300 or 600 dpi, with crops. North-arrow bearings were taken from the arrow's axis, scale bars measured in pixels, and directions computed perpendicular to the gap, measured against the arrow.

## Plans found

| Plan | Page | Cave(s) | Row |
|---|---|---|---|
| 2547:1 | 7 | 64/V (plan + view of openings) | yes |
| 2547:2 | 8 | 50/V | yes |
| 2547:3 | 11 | 59/V (plan + sections) | yes |
| 2549:1 | 3 | 49/V (plan + section) | yes |
| 2551:1 | 4 | 1/VII (plan + section) | yes |
| 2551:2 | 12 | 3/VII (caption: north approximate) | yes |
| 2552:1 | 5 | 2/VIII | yes |
| 2552:2 | 5 | 7/VIII (plan + section) | yes |
| 2552:3 | 6 | Plan of 10/VIII; section of 10/VIII above 9/VIII | 10/VIII only (9/VIII is shown only in the section) |
| 2552:4 | 6 | 9/VIII complex | yes |
| 2552:5 | 10 | 6/VIII | yes |
| 2555:1 | 2 | Section of 9/VIII and 10/VIII (caption prints "9/III") | no: a section, not a plan |
| 2555:2 | 3 | 9/VIII (same drawing as 2552:4, plus excavation sections) | yes |
| 2558:1 | 4 | 14/IX (plan + section) | yes |

Every row has a north arrow and a scale bar. 3/VII's arrow is marked as approximate in its caption. For 10/VIII, the only scale bar is printed under the section of the same figure; I assumed it also applies to the plan.

## Conventions used

- `0` for pillars, steps or niches is used only where the plan is clear and complete and draws none. Where a drawn feature might be one of these but can't be identified, the field is left blank and the feature is described.
- "Main space" means the largest continuous chamber, without side recesses. What was measured is stated in `notes`, along with overall extents where they differ.
- A `/` direction lists the sector the best estimate falls in first, then the neighbouring sector.

## Unclear or unreadable

- **9/VIII (2552:4, 2555:2):** the openings can't be counted. The whole page-right front lies open toward a ticked scarp line, with no rock outline, and passage Z runs off the drawing. The opening fields are blank.
- **49/V:** the mouth is wide and poorly defined, and boulders may split it in two. Depending on how the gap is drawn, the direction comes out between about 13° and 37°.
- **3/VII:** this is a sketch-like plan with north given as approximate. The second, small gap may be a drafting break.
- **10/VIII:** the openings lead into the chimney and the interior is complex.
- **2/VIII:** the front is closed in the drawing only by an unhatched line, which I read as an edge line, not rock.
- **1/VII and 3/VII:** the 20 m scale bars make both caves very large (about 78–124 m and 118 m). The values are recorded as drawn.

## Exposure and process notes

- While working out the labels A–G on the 50/V plan (2547 p8), I read the adjacent text paragraph. Every value in the row was measured on the plan.
- My first helper script (`crop.py`) in the shared scratchpad root was overwritten by another process during the session. I moved my helper scripts to a private folder and re-checked the affected crops. No output depends on the overwritten file.
