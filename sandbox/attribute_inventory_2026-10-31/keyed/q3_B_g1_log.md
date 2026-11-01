# Q3 reader B (g1) keying log: hir04, bad77

- Reader: B, group Q3. Started 2026-10-31 19:16 PT, finished 19:35 PT. Not committed.
- Outputs: `keyed/hir04_B_g1.csv` (65 rows) and `keyed/bad77_B_g1.csv` (25 rows), written with the Python csv module in SCHEMA header order.
- Read: `SCHEMA.md`, `READER_INSTRUCTIONS.md`, `QUMRAN_NOTES.md`, and the two source texts in full (scratchpad `qum/src/hir04.txt`, `qum/src/bad77.txt`). I opened no other repo file, no file under `keyed/` except my own, no Projects, Drive or web.
- Exposure note: when I first read this folder, the environment showed the repo's `AGENTS.md` automatically. It contains no source data, and I did not use it. The bad77 text itself mentions the Copper Scroll (p. 22, Secacah). That passage was not used for keying.

## Pages and figures

- hir04: *IEJ* 54 (2004) pp. 37-74 read in full. The description is on pp. 37-39, 42, 44-45, 47, 49, 51-53, 55-56, 58, 60-66 and 68-71. The other pages carry figures, the pottery tables and the references.
- bad77: *BASOR* 227 (1977) pp. 1-25 read in full. The description is on pp. 1, 3-5, 12, 16-18 and 20-23. The rest is finds tables, figures and the bibliography.
- No figure or page image was seen. The `figure` column lists the figures that the text cites for each feature; none of them was used. Plan-only attributes are left blank, and no `plan_scaled` values were keyed.

## Problems

1. **bad77 OCR is column-interleaved** on pp. 1, 3, 4, 12 and 16-17: words from adjacent lines are merged out of order. I rebuilt readings from the word sets and flagged every such row in `notes` ("Column-interleaved OCR..."). Where no contiguous wording exists, `quote` is blank. The specific uncertainties are:
   - Hall I 27.5 x 9.2 m versus kitchen II 15.5 x 3.2 m. The pairing is my reading; 15.5 x 3.2 appears twice near "kitchen".
   - Rooms III and IV: I read 5.1 m and 7.9 m as lengths, since their "inner width" could not be estimated because the south side is eroded. Both rows are low confidence.
   - The threshold, 1 m wide, read as being in the northern wall of Hall II, opposite Pillar Base 4. The channel to its west has two rows of stones 15 cm apart.
   - The cemetery "about 800 m north of the building".
   - Tomb rectangles of 1.0-1.3 x 2.2-2.4 m, and pits of 1.8-2.0 x 0.5-0.7 x 1.7-2.0 m (third figure keyed as depth).
   - A step along the west side (e.g. T4, T18) and an east-wall niche of 40-60 cm. Which dimension the 40-60 cm is cannot be read.
   - T3 is cited as an example of either the niche or of tombs with no step and no niche. The text does not settle which, so T3 is kept as a low-confidence row with `n_steps` blank.
   - Unreadable and not keyed: the passage on the east end of Hall I and Pillar Base 4 (a 1.5 m wall stub or opening, the floor level of Hall II).
2. bad77 map ref. `170.05/114.55` is copied from the OCR text and has not been checked against a page image. The text does not name the grid system. `OIG` (old grid) is keyed for both sources from the form of the map refs (hir04 `1249/1929`).
3. The hir04 extraction drops the × sign in some dimensions ("18 24 m.", "3.8 8.4", "4.4 4.5", "1.5 1.8", "17 17"), and "lxl" stands for 1x1. These are keyed as a x b and noted. One quote restores "façade" where the extraction has "fa?ade".
4. hir04 fig. 25's caption calls the eastern cell (L119) the "southern cell". The text is keyed, and the caption is noted.

## Conventions used

- `length_m` is the longer horizontal side. When the printed order differs, it is given in `notes`. `height_m` on buildings and walls is the preserved wall height.
- `page` lists non-adjacent pages separated by `;`.
- `rel_bearing_deg` is the bearing from the related feature to this feature. It is keyed only where the text prints a distance together with a compass direction. Other compass words are kept in `notes`.
- Doorway rows leave `n_openings` blank, because the row is itself the opening.
  - Opening directions come from the wall that is named: "in the northern wall" gives N.
  - For hir04's northern wing, they come from the statement that the rooms' doorways face south.
  - A doorway whose facing is not stated is left blank, e.g. W5's doorway and the L119 steps "from the NW corner".
- hir04 counts:
  - The miqweh pool's `n_steps` is 1, the step preserved; the author assumes 3.
  - The reservoir's `n_steps` is 0 ("no staircase was found").
  - "About ten" pillars is keyed as 10.
  - The isolated building's "pillar-like constructions" are keyed as 2.
- bad77 counts: the grave-pit ledge ("step") is keyed as 1 step `inside`.
- Excavator function labels are kept in `class_as_printed`. L119.pool is classed `ritual_bath` (the author's miqweh). The isolated building is classed `building`; the columbarium suggestion is in `notes`.

## Seen but not keyed (no attribute beyond class, objects, or unreadable)

- **hir04:**
  - The L143 trial probe (2x4 m; an excavation probe, not a feature).
  - De Vaux's L28 tile concentration, and L126.
  - Walls W3, W7, W10, W13, W16-W19, W29, W31, W33 and W36. These are referenced in the notes of the rooms and pools they bound.
  - The two rooms east of the stable; only their common entrance is keyed.
  - The wings as groups.
  - Movable objects, given in `notes`: the grinding stone, the cylindrical crushing stones and the column drum.
  - The coastal passage at Ras Feshkha.
- **bad77:**
  - Tombs 8, 12, 13 and 14 (finds or fig. 19 only).
  - The two southern-hill tombs, and the Bedouin burials.
  - The "benches" near a western wall.
  - The possible third room at the NE corner.
  - The Iron II remains (not described).
  - The oasis springs.

## Counts

| | rows | with a size | with steps | with plaster | with openings (count or direction) |
|---|---|---|---|---|---|
| hir04 | 65 | 50 | 10 | 6 | 17 |
| bad77 | 25 | 13 | 2 | 0 | 3 |
