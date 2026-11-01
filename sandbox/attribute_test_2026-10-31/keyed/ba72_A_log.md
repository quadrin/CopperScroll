# ba72 describer keyer A: log (run 28)

- Source: P. Bar-Adon, "The Judaean Desert and Plain of Jericho", in Kochavi (ed.) 1972 (Hebrew). Bucket `pdf/01-ASI1-Kochavi-1972-indexed-81b7cd39`, read from page images rendered with `scripts/render_bucket.py`. The text layer was not used.
- Scope: the 25 sites in `keyed/ba72_selected.csv`. Output: `keyed/ba72_A.csv`, 109 rows covering all 25 sites. Rules: `../attribute_inventory_2026-10-31/SCHEMA.md` and `READER_INSTRUCTIONS.md`, with `describers.csv` standing in for `sources.csv`.
- Started 2026-11-01T03:32:21Z; finished 2026-11-01T03:53:44Z (UTC).
- Files opened: BRIEFS.md, describers.csv, SCHEMA.md, READER_INSTRUCTIONS.md, keyed/ba72_selected.csv, scripts/render_bucket.py. No other keyed, out, concordance, research or project-note file was opened. Reader B's file was not opened.

## Pages read

| PDF page | Printed pp. | Read for |
|---|---|---|
| 58 | 112-113 | 55 (p.113) |
| 59 | 114-115 | 61, 62 (p.114) |
| 61 | 118-119 | 85 (p.119) |
| 62 | 120-121 | 90 (p.120, with its continuation and plan in the left column); 93, 94 (p.121) |
| 63 | 122-123 | continuation of 94 (p.122, top of right column); 101, 103 (p.123) |
| 64 | 124-125 | 109, 110, 112, 113 (p.125); plan and two photos of 110 |
| 65 | 126-127 | 114, 115 (p.126) with map and photo; 118, 119, start of 128 (p.127) |
| 66 | 128-129 | continuation of 128, then 129, 130 (p.128) with 130's plan and photo; 133 (p.129); start of 136 (p.129) |
| 67 | 130-131 | continuation of 136; 137, 138, 139 (p.130) |

Each spread was first rendered at 70 dpi to find the entries, then cropped to one column at 250-450 dpi. Other sites' entries were visible in the overview renders but were not read. Some captions were read only to decide which entry a figure belonged to: p.121 (photos labelled א׳ and ה׳ belong to site 92), p.126 ("מבנה ג." belongs to site 117), p.129 (plan "ה׳ — תכנית המבנה וקצה השביל" belongs to site 131). One render was mistakenly made at 900 dpi for a whole page; it was overwritten and not used.

## Figures used

- Site 90: plan "תכנית המתחם", p.120, with scale bar (0-10 m) and north arrow. Its diameter scales to about 30 m, which matches the text. No entrance is marked.
- Site 110: plan "תכנית המצודה", p.125, with scale bar (0-20 m), north arrow and sections א-א and ב-ב. Photos on p.125: "אחד החדרים החפורים במצודה" and "המזוזה של שער המצודה".
- Site 114: map "מפת כפר ואדי א־נר", p.126, with scale bar and north arrow. Photo "מדרגות בנויות", p.126; its attribution to 114 is uncertain (see Problems).
- Site 130: plan "תכנית המבנה", p.128, with scale bar (0-4 m) and north arrow. It matches 13.5 × 7 m with the apse on the W. Photo "המבנה. מראה כללי", p.128.
- No dimension was taken from a plan (`dims_basis` is `text` throughout). Opening directions come from the text; the plans were used only as checks.

## Conventions

- feature_id: the site row is `ba72:<site>`. Sub-areas the source labels with Hebrew letters map to letters (א→a, ב→b, ג→c). In sites without letter labels, features are lettered a, b, c in order of mention. A feature inside, or grouped under, another feature gets a numeric suffix (e.g. 128.a.3.1).
- Site row: when the entry describes one main feature (an enclosure, fortress, cave or building), the site row is that feature and carries its attributes. When the entry names a group ("three buildings", "four caves", "buildings"), the site row is a container whose class is that of the first-named feature, and notes say "site row (container)". parent_id points to the containing feature, which is the site row unless the feature lies inside a sub-feature.
- Counted groups were split into one row per feature, as the schema's one-row-per-feature rule requires: 85.a-d, 94.b.1-2, 113.a-c, 115.a-c, 119.a.1-2, 119.b.1-4, 128.a.3.2-4 and 138.b.1-9. Uncounted plurals ("houses", "caves", "terraces", "wall remains") are one row each, with the plural noted.
- Dimensions: in this book, numbers in "A × B" run right to left (the first number read is the rightmost). This was confirmed by the line break inside "40 × 40 × 30" in 128.b. For footprints, the larger value is keyed as length_m and the smaller as width_m. Where the printed order differs (94.a.2 "6 × 9", 130 "7 × 13.5") the notes say so. "A × B × C" is keyed as length, width and height in printed order (118, 128.b.2). Openings are keyed as width × height: 128.b states this order, and 118.a follows it by analogy. Wall thickness is in notes, not in a dimension column. "כ־" (ca.) values are keyed bare and flagged in notes.
- Openings: the containing feature carries n_openings, and opening_dirs where the text states a direction. A doorway row is added only when the opening has its own attributes (size, construction, relation); it carries opening_dirs but leaves n_openings blank, so openings are not counted twice. "Its opening" in the singular is keyed n_openings = 1.
- construction = built only where the text names a building material, courses or "בנוי". Caves are left blank, because the text never says whether they are natural or rock-cut.
- relations name only features keyed in this file. Relations to features of other sites (85 is "at the S end of the wall of site 84 ז") and compass positions ("S of", "NW") are in notes. rel_distance_m is filled only where printed (94.a.2 8 m; 137.a.1 5 m; 136.b.1-2 4 m apart). rel_bearing_deg is always blank, because no bearing is printed.
- period is an English rendering of the printed pottery line. Where the pottery is listed by sub-area, the period goes on that sub-area's rows and the site row shows all of it. in_window: `no` when every printed period falls outside the window; `unknown` when "Roman" or "Roman-Byzantine" is printed without "Early", or when no period is printed. No entry in scope prints Hellenistic or Early Roman, so nothing is `yes`.
- grid_printed copies the header grids as given in ba72_selected.csv, which matched the pages. Sub-area grids (5-digit, e.g. "19288 12772") are copied in the same left-to-right order. All are OIG.

## Attribute summary

- n_openings: ba72:85 = 1 (N, "apparently"), ba72:110 = 1 (E), ba72:118 = 1, ba72:128.a.3 = 1, ba72:128.b = 1, ba72:139.b = 1 (N).
- opening_dirs: ba72:85 N; ba72:85.e N; ba72:110 E; ba72:110.a E; ba72:139.b N.
- Steps: one steps row, ba72:114.d (built steps, from a photo caption; n_steps not stated; low confidence).
- Pillars: none. Site 62 mentions capitals, but no count is given.
- Class-only site rows (low): 55, 93.

## Problems and uncertainties

1. **114.d steps.** The "מדרגות בנויות" photo sits in the same column as entry 114. The photos on that page are grouped, though: the one below it shows building ג of site 117. Assigning it to 114 is an inference, so the row is low confidence. Entries 116 and 117 were not read, so they were not checked for a mention of steps.
2. **118.a.** The opening is printed "8 × 10 m" without naming the axes. It is keyed as width 8, height 10, by analogy with 128.b.
3. **128.a.1.** "מידותיו 1.5 × 1.5 מ'" is assigned to the threshold (מפתן) on grammatical gender rather than to the cave.
4. **90.b.** In "צפונית לו" ("north of it"), "it" is read as the halved building 90.a. It could refer to the enclosure.
5. **110.** The text says "the eastern entrance". On the plan, the wall facing that way has an outward normal near ESE (about 113°), and the gap between the wall ends scales to about 8 m. The text's E was keyed, and the gap width was not.
6. **136.b.3.** The trough(?) is "in the north-west"; whether it is inside building 136.b or outside is not stated.
7. **136.a.** "שביל (או גדר)", path or fence, is keyed as class road. It could be wall.
8. **130.a.** "Apsidal room faces west" is treated as the apse's orientation, not as an opening.
9. Splitting groups into one row per feature, and the container site rows, may not line up with reader B's rows.
