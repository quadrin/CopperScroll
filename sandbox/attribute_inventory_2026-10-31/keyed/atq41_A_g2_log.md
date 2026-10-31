# atq41, reader A, group g2: keying log

- Started: 2026-10-31T22:02:55Z
- Finished: 2026-10-31T22:22:54Z
- Output: `keyed/atq41_A_g2.csv` (174 rows, 32 columns, header in SCHEMA order, written with Python csv)

## Read
- SCHEMA.md and READER_INSTRUCTIONS.md.
- Article 2553, Sion, "Regions IV and VI: Survey and Excavations of Caves along the Jebel Abu Saraj Cliff", printed pp. 43-70. Read in full (pypdf text, about 94,000 characters), including coin catalogues, Tables 1-2, notes, references and captions. The printed title covers Regions IV **and** VI. All 30 Region IV caves (IV/1-30) and all 29 Region VI caves or niches (VI/31-59) are keyed, plus the background features on pp. 43-46 (springs, aqueducts, roads, notch) and the Region VI hiking trail.
- Article 2554, Feig, "The Excavation of Cave IV/11 ('Cave of the Pillar')" (English summary). Read in full. The page has no printed number. I keyed it as p. 71 from Sion's reference list ("English summary, part 2: p. 71"); this is consistent with Sion ending on p. 70 and Wolff starting on p. 73.
- Article 2556, Wolff, "The Excavation of Cave IV/12", printed pp. 73-83. Read in full. The first page has no printed number; p. 74 is the next page.

## Figures rendered (scratch: reader_A_g2/)
- 2553: contact sheets of PDF pages 2-29 at 40 dpi. Every page is text only. Plans 1-8 and Figs. 1-36 are **not** in the Part 2 PDF; only the captions are printed (p. 69-70). No plan values could be used for IV/1, IV/2, IV/7, IV/8, IV/17, VI/43, VI/46 or VI/52.
- 2554 p. 2 (100 dpi): captions only; Feig's Plan 1 is not in this PDF.
- 2556 p. 2 (150 and 300 dpi, plus crops): Wolff Plan 1 (plan and sections of Cave IV/12), with a 0-3 m scale bar and a north arrow. The arrow points c. 296 deg on the page. The entrance (top of L003) opens toward the page top, which is c. 64 deg true. I keyed this as `NE` (close to the NE/E boundary). By the scale bar, the arms measure c. 8.5 m and 7.5 m, longer than the text's "c. 6 m". The text values are keyed and the plan values are in the notes.

## Conventions used
- Dimensions: `a x b` is keyed with the longer value as length_m and the shorter as width_m. Ranges are kept as `a-b`. "c." is dropped and mentioned in the notes where it matters. "Thickness" of a wall is keyed as width. Pit "height" (IV/12 L002) is keyed as depth.
- When a cave is described as one chamber or cavity (with niches at most), the chamber dimensions are on the cave row. When it has several spaces (anteroom, hall, passages, two stories), each space gets a sub-row (`.a`, `.b`, … in text order) and the cave row carries only dimensions printed for the whole cave.
- Natural cave mouths are not keyed as `doorway` rows. Their sizes are in the cave row's notes, and their count and direction are in `n_openings` and `opening_dirs`. Doorway rows are used only for hewn or built openings (IV/6.b, VI/52.e, VI/58.b).
- `opening_dirs` is keyed only from "faces X", "open onto the east cliff", "in its X wall" / "on the opposite side", or a plan with a north arrow (IV/12). Positional names ("the southern entrance") are not converted. For IV/1 only the northern opening has a direction (E).
- `n_openings` = 1 where the text speaks of "the entrance/opening" in the singular.
- Steps: explicit steps are counted (VI/33 toe-holds 3, VI/57 step 1). "Natural rock steps" (VI/51) and stepped floors or slopes (IV/7, IV/28, VI/43, VI/43.d, VI/52.k) are keyed `n_steps = unknown`, with the wording in the notes.
- Relations: `rel_bearing_deg` is the bearing **from this row's feature to the related feature**, taken from printed compass words (e.g. "c. 10 m north of IV/1" on the IV/2 row gives 180). Distances are as printed. Each relation is keyed once, on the row whose paragraph states it.
- Grid: map refs such as 19015/14440 are keyed as printed with grid_system `OIG`, based on the number form (northing c. 144); the text does not name the grid. A ref repeated for a group ("[see Cave X]") is `site_grid`. Unique refs (IV/19, IV/20, VI/43, VI/46) are `feature_grid`. Sub-features are `text_only`.
- in_window: `yes` only where the source dates use to the 2nd c. BCE-1st c. CE or reports Hasmonean/Herodian material from the cave. Undated or non-diagnostic finds give `unknown`; caves with no finds are left blank.
- page: printed page from the running heads. Rows spanning a page break show `a-b`. IV/11 and IV/12 combine Sion with Feig or Wolff as `52; 71` and `52; 73`.

## Discrepancies noted in rows
- IV/11: Sion's map ref is 19030/14415 (keyed); Feig's is 19015/14415 (in notes).
- IV/12: Sion gives 3.2 x 7.2 m, height 2.7-4.3 (keyed). Wolff gives an L-shape with arms of c. 6 m and heights 1.8-2.6 (sub-rows). Wolff's coin note cites Sion's survey of IV/12 as "Cave IV/2".
- VI/46: survey gives 11 x 15 m (keyed); excavation gives 10.5 x 11.5 m. n_openings is left blank because the text says "the cave entrance" while the Fig. 25 caption says "The openings".
- Table 2 heads its rows "IV/43, IV/45, IV/47, IV/48" and assigns coins differently from the text (64-65 to VI/45 rather than VI/46; 66-67 to VI/47 rather than Niche VI/48; 68 to VI/48 rather than VI/49). The text is keyed; the conflict is in the notes.
- VI/50: the back part's height is printed "0.5 x 1.5 m" and keyed as 0.5-1.5. VI/51: the cavity width is printed "0.2-0.3" and keyed as printed.

## Unreadable / not available
- All plans and photographs in 2553 and 2554 (they are in Part 1, not in these PDFs). Some OCR noise (Cyrillic "с" for "c.", "Vl" for "VI") was read through without loss of numbers.
