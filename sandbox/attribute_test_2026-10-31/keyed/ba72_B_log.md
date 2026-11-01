# ba72 describer keyer B — run 28 log

- Source: P. Bar-Adon, "The Judaean Desert and Plain of Jericho", in Kochavi (ed.) 1972 (Hebrew). Bucket `01-ASI1-Kochavi-1972-indexed-81b7cd39`.
- Scope: the 25 sites in `keyed/ba72_selected.csv` (55, 61, 62, 85, 90, 93, 94, 101, 103, 109, 110, 112, 113, 114, 115, 118, 119, 128, 129, 130, 133, 136, 137, 138, 139).
- Read beforehand: BRIEFS.md, describers.csv (row ba72), ../attribute_inventory_2026-10-31/SCHEMA.md and READER_INSTRUCTIONS.md. I opened no other file in keyed/ and no ʿAtiqot, concordance, research or project-note file.
- Started 2026-11-01T03:32Z, finished 2026-11-01T03:52Z (UTC).
- Output: `keyed/ba72_B.csv`, 82 rows (25 site rows and 57 sub-feature rows), written with Python's csv module in UTF-8.

## Pages read (page images only; the text layer is not used)

| PDF page | Printed pages | Entries and figures read |
|---|---|---|
| 58 | 112–113 | 55 (p.113) |
| 59 | 114–115 | 61, 62 (p.114) |
| 61 | 118–119 | 85 (p.119); checked the area map on p.119 ('מפת המבנים השונים בשטח'): its grid lines (189500–189750 E, 129250–129500 N) do not reach 85 or 90 |
| 62 | 120–121 | 90 (p.120, both columns) with the plan 'תכנית המתחם'; 93, 94 (p.121) |
| 63 | 122–123 | end of 94 (p.122); 101, 103 (p.123) |
| 64 | 124–125 | 109, 110 with plan 'תכנית המצודה' and two photos; 112, 113 (p.125) |
| 65 | 126–127 | 114 with map 'מפת כפר ודי א-נר' and photo 'מדרגות בנויות'; 115 (p.126); 118, 119, start of 128 (p.127) |
| 66 | 128–129 | end of 128; 129; 130 with plan 'תכנית המבנה' and photo (p.128); 133, start of 136 (p.129) |
| 67 | 130–131 | end of 136; 137, 138, 139 (p.130) |

I rendered the pages at 60–70 dpi to find the entries, then cropped columns at 250–400 dpi. The PNGs are in the scratchpad folder r28_ba72_B.

Figures I looked at only to see which site they belong to, and did not use:
- p.126 photo 'מבנה ג.': this is site 117 (not in scope).
- p.127 photo 'א' — הסלע בעל הכוכים': site 121.
- p.129 plans 'א' ה' / ב' ה'' and p.128 photo 'ג' ה'': their captions follow the series for site 131 point ה (a path).
- p.129 plan 'ג' — תכנית המבנה המלבני': site 132.
- Photos on pp.112–115 and 120–124: other sites.

## Conventions used

- **Site rows.** Each site has a row `ba72:<site>`. If the entry describes one feature, or one group of identical features (101, 109, 110, 112, 115, 118, 130, and the caves of 113), that row carries the attributes. Otherwise the site row is a parent row with the pottery summary.
- **Lettered points.** The source's points א/ב/ג map to suffixes `.a/.b/.c`. A secondary feature inside a point gets `.a.1`, `.a.2` and so on.
- **parent_id.** As the brief says, `parent_id` always points to the site row. Closer containment (a feature inside a building or cave below site level) is written as `inside:` in `relations`.
- **Groups.** Identical features described together get one row, with the count in `class_as_printed` or `notes`: 85.a (4 buildings), 94.b.1 (2), 113 (3 caves), 113.a (terraces), 115 (3 round buildings), 119.a.1 (2), 119.b (4), 133.a.1 (2 ovens), 136.b.1 (2 walls), 138.b.1 (9 graves).
- **Grids.** `grid_printed` is the site header grid. Where the entry prints a grid for a point (נ.צ.), that grid is used and `position_basis = feature_grid`. A secondary feature inside a point carries the point's grid, and its notes say so. All grids are OIG.
- **Dimensions.** "a × b" goes in as length = larger and width = smaller. Three unlabelled values (118 cave, 128.b.2 hall) go in as length, width and height in printed order; their notes say the height is not labelled. "c." values are keyed as the number, and the notes say they are approximate. Wall thicknesses are in notes, not on separate wall rows.
- **Doorway rows.** An opening gets its own row (`doorway`, `n_openings` 1, `leads_to:` the space it opens into) only when it has more than its parent row already records: dimensions, construction or a relation. These are 85.b, 110.a, 118.a, 128.a.1, 128.a.4 and 128.b.1. The parent row also carries `n_openings` and `opening_dirs` when the text states them.
- **Bearings.** `rel_bearing_deg` is only a printed compass word converted on 8 points (N=0, E=90, S=180 and so on). It is the bearing from the related feature to the row's feature. `rel_distance_m` is filled only where a distance is printed (94.a.2 at 8 m, 137.a.1 at 5 m).
- **Periods.** `period` is the pottery line, translated into English. Where the source splits it by point, it goes on that point's rows; otherwise it is on the site row only.
- **in_window.**
  - `no`: only Chalcolithic, Israelite, Byzantine or Arab periods are printed.
  - `unknown`: an unspecified "Roman", "Roman-Byzantine" or "Roman (?)" is printed.
  - blank: no period is printed for the row.
  - No entry in scope prints Hellenistic or Early Roman.
- **Classes.**
  - `other`: a tell, an enclosure (מתחם), a village, an oven, a kokh, a dolmen. The Hebrew word is in `class_as_printed`.
  - `basin`: a trough (אבוס).
  - `cistern`: בור (118.c, which could also be a pit).
  - `road`: a path, including 136.a, which the source calls "path (or fence)".
  - `burial`: the cemetery and the graves.
  - `cairn`: stone heaps (גלי אבנים).

## Features with openings, directions, pillars and steps

- **n_openings:** 85 and 85.b (1, N, "apparently"); 110 and 110.a (1, E, "the eastern entrance"); 118 and 118.a (1, "its opening"); 128.a.3 and 128.a.4 (1, opening 8 m wide); 128.b and 128.b.1 (1, 40 m wide and 35 m high); 139.b (1, N).
- **opening_dirs:** 85 and 85.b N; 110 and 110.a E; 139.b N.
- **n_pillars:** none. 62 mentions capitals but gives no count of columns.
- **n_steps:** none. 114.a is a 'built steps' photo with no count; it is low confidence and is assigned to site 114 by its position on the page.

## Problems and uncertainties

- **90 plan.** The plan 'תכנית המתחם' (p.120) names no site. I assigned it to 90 because it is printed right after the entry and shows a circular enclosure. It scales to about 27.5 m against the text's 30 m. Two gaps on the W side are not marked as entrances, so I left `n_openings` blank.
- **110 dimensions.** The text gives 42 × 28 m. The plan scales to about 39 × 17 m for the solid walls and about 46 × 24 m for the dashed outline. I keyed the text values and put the plan values in notes.
- **90.b position.** "North of it" most likely refers to the divided building 90.a.
- **Pottery lines.** Entries 101, 109, 118, 119 and 133 print no pottery line.
- **Hebrew number order.** Where a quote contains "a × b", it follows the order as I read it in the image. Field values do not depend on that order.
- **Quotes.** Each quote is at most 15 words, with niqqud dropped. The quote for 118 elides the opening dimensions with "...".
