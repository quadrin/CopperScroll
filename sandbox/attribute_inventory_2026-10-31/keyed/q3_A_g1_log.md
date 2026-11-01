# Q3, reader A (g1): keying log

- Sources: `hir04` (Hirschfeld 2004, *IEJ* 54: 37–74) and `bad77` (Bar-Adon 1977, *BASOR* 227: 1–25).
- Started 2026-10-31 19:16 PT; finished 19:36 PT.
- Outputs: `keyed/hir04_A_g1.csv` (71 rows) and `keyed/bad77_A_g1.csv` (34 rows), written with the Python csv module in SCHEMA header order. One combined log, as the caller asked (READER_INSTRUCTIONS item 9 asks for one log per source).

## What was read

- `SCHEMA.md`, `READER_INSTRUCTIONS.md`, `QUMRAN_NOTES.md`.
- The two text extractions, in full: `scratchpad/qum/src/hir04.txt` (printed pp. 37–74) and `scratchpad/qum/src/bad77.txt` (printed pp. 1–25).
- I did not open `sources.csv`, any other repo file, other readers' files in `keyed/`, the Projects tool, Drive or the web. When I read the sandbox files, the environment automatically added the repo's `AGENTS.md` (general project rules; it has no scroll text, candidates or keyed data). I did not open it myself, and nothing in it was used for keying.
- `bad77` p. 22 mentions the Copper Scroll in passing, in the source's own discussion of Secacah. I read it as part of the source. Nothing was keyed from it.

## What could not be read

- No page images were available. None of the figures were seen: plans, sections and photos in hir04 figs. 1–31 and bad77 figs. 1–24. Only their captions were read. So no `plan_scaled` values were keyed, plan-only attributes are blank, and no direction comes from a north arrow.
- **hir04**: the extraction is clean apart from OCR artefacts:
  - The multiplication sign is lost in five dimension pairs: "18 24 m.", "3.8 8.4 m.", "4.4 4.5 m.", "1.5 1.8 m." and "c. 17 17 m.". The pairs are keyed as printed and flagged in notes.
  - "lxl" stands for 1x1.
  - ʿ appears as "c", and ç or é as "?".
  - Table text for the pottery figures is garbled. It was not keyed.
- **bad77**: on pp. 1–5, 12, 16–18 and 20–24 the extraction interleaves words from two columns and several lines, so the word order is scrambled. I rebuilt the sentences needed for keying. Every row that relies on rebuilt word order says so in `notes` and is `confidence = low`. Where a quote's words are not contiguous in the extraction, the note says the quote is reconstructed. The specific risks are listed below.
  1. Hall I gets 27.5x9.2 m and kitchen II gets 15.5x3.2 m. Both pairs are printed on p. 1. The assignment rests on p. 4 ("kitchen … measuring 15.5 x 3.2 m.", also scrambled) and on the hall being called "large".
  2. The inner length 5.1 m is paired with room III and 7.9 m with room IV.
  3. Tomb details: a step on the west side, 30 x 20-30 cm; a niche at the bottom of the east wall, 40-60 cm in height and depth; Tombs 4 and 18 as examples of the step; Tomb 3 as an example of a tomb with neither steps nor niches.
  4. The cemetery is c. 800 m north of the building. The fig. 1 map caption labels support the direction.
  5. Also rebuilt: the 1.4 m opening and the threshold opposite Pillar Base 4; the channel of two rows 15 cm apart; the depression 25–30 cm deep; the oasis "more than 2 km. long"; the Bedouin cemetery.

## Keying conventions used

- **Dimensions**: length and width are keyed in the order printed (first figure = length). `height_m` on walls and buildings is the preserved wall height, noted on each row. Lower bounds ("at least", "or more", "more than") are keyed as the number, with the qualifier in notes.
- **Opening directions** are keyed only when the text names a facing or names the wall an opening is in. For example, "steps in the southern wall" gives S. Each row says which basis was used. Where neither is given (e.g. the hir04 W5 doorway), the direction is left blank.
- **Figure column**: the figures the text cites for that feature. None was inspected.
- **Map references**: both are printed as "map ref." without naming the grid: hir04 "1249/1929" and bad77 "170.05/114.55". They are keyed as printed with `grid_system = unknown` and repeated as `site_grid` on features of that site. Features away from the site (the survey structures, the long wall, the bad77 cemetery and tombs) are `text_only` with no grid.
- **feature_id**: the source's labels are used where they exist (L<n>, W<n>, room numerals I–V, Tomb n → T<n>, Pillar Base n → PB<n>). Unlabelled features get descriptive ids, each noted "feature_id is the keyer's".
- **Groups keyed as one row**, noted on the row:
  - hir04: the two northern-wing rooms with a common entrance; the three de Vaux tombs.
  - bad77: two ovens; two granaries; two tombs on the southern hill.
  - bad77 also has one generic row (`bad77:tombs_N`) for the size ranges that apply to the northern-hill tombs as a group.
- **Relations** leave out the parent, which is already in `parent_id`. `rel_distance_m` has one entry per relation, left empty where no distance is given. Bearings are not keyed, because the sources give no numeric bearings. Directions such as "800 m north" are in notes.
- **Tomb orientation** goes in notes as the long axis, per QUMRAN_NOTES. Tombs 8, 12, 13 and 14 take the general statement that the tombs lie N–S. Tomb 17 is NW–SE and Tomb 15 is E–W.
- **in_window**: yes for the Early Roman features of ʿEin Feshkha Area A and for the hir04 long wall (the author dates it Early Roman; de Vaux dated it Iron Age). No for the Area B tower (late Iron Age). Unknown for the Israelite building, the isolated building, bad77 T15 and the southern-hill tombs. Blank for natural features.
- **Steps**: hir04 reservoir has `n_steps = 0` from "no staircase was found", although the pool was not excavated to its full depth. Confidence is medium. bad77 T3 has `n_steps = 0` from the rebuilt "neither steps nor niches". The hir04 miqweh has `n_steps = 1`: one step is preserved, and the author reconstructs three.

## Not keyed

- hir04: trial probe L143 (an excavation unit); L126 and de Vaux's L28 (no attributes beyond the tiles found there); the upper storey (a reconstruction); movable finds (grinding stone, cylindrical crushing stones, column drum), which are mentioned in the notes of their rows; comparison sites (Boqeq, Jericho, Masada, Qumran buildings).
- bad77: Iron II remains (not described); finds tables (vessels, coins).

## Counts

| Source | Rows | With a size | With steps | Plaster yes | With openings (count or direction) | Low confidence |
|---|---|---|---|---|---|---|
| hir04 | 71 | 49 | 7 (one is 0) | 6 | 19 | 0 |
| bad77 | 34 | 13 | 3 (one is 0) | 0 | 2 | 24 |
