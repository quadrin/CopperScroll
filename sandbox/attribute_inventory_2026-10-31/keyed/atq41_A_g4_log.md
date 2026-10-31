# atq41, reader A, group g4: keying log

- Source: `atq41`, ʿAtiqot 41, part 2 (English), Jerusalem 2002.
- Reader: A. Group: g4 (articles 2584, 2585, 2586, 2587, 2588, 2589, 2590, 2592, 2593).
- Started: 2026-10-31T22:02:54Z
- Finished: 2026-10-31T22:26Z (CSV built 22:24:43Z, then the page-169 note was added and the file rebuilt)
- Output: `keyed/atq41_A_g4.csv` has 298 rows, 144 of them top-level (no parent). The CSV was written with Python's `csv` module (QUOTE_MINIMAL). A script checked that every quote has no more than 15 words, every parent_id and relation target exists, and no feature_id repeats.

## What was read

I read SCHEMA.md, READER_INSTRUCTIONS.md and all nine extracted text files in full. I opened no other repository file and no other file under keyed/.

| Article | Section | Printed pages | Notes |
|---|---|---|---|
| 2584 | Region X (Itah, Kam, Ben-Haim) | 169-175 | Table 1 is on pp. 169-171. The captions on p. 175 stop at Fig. 4. The captions for Figs. 5-20 and Plans 1-5 are not in the PDF, which has no p. 176. Page 169 has no printed number; it is inferred from the next page, 170. |
| 2585 | Region XI (Baruch, Mazor, Sandhaus) | 177-183 | PDF pp. 2-4 (printed 177-179) are high-resolution scans with **no text layer**, and the .txt file starts at p. 180. I read XI/1-XI/15 from rendered page images. Page 177 has no printed number. The PDF holds only the 8 text pages and no plates or plans. |
| 2586 | XII/49 (Ibrahim) | 185 | No page number is printed on this page; it is inferred from the following p. 186. |
| 2587 | XII/50, XII/52, XII/53 (Cohen, Yisraeli) | 185-186 | Same printed page as 2586. |
| 2588 | XII/56 (Ibrahim) | 186 | The texts of 2586-2589 overlap: they are crops of the same two printed pages. |
| 2589 | XII/61 (Ibrahim, Hameiri) | 186 | |
| 2590 | Region XIII (Tal, Oron) | 187-193 | Table 1 is on pp. 188-191; the XIII/8 excavation is on p. 192. |
| 2592 | Region XIV (Dahari) | 209-219 | Coins are on pp. 212-214 and captions on p. 219. Page 209 has no printed number. |
| 2593 | Region XV, XV/3 (Nahlieli, Lender) | none printed | This is a single page with no page number and no neighbouring page in the PDF, so `page = art2593`. |

## Figures and plans

- **None of the plans or figures cited in these articles are in the Part 2 (English) PDFs.** The plans belong to the Hebrew Part 1. I rendered a 30-dpi thumbnail montage of all 47 PDF pages (`montage.png`), and every page is text. So there are no `plan_scaled` dimensions, and no openings or directions taken from plans. The `figure` column is blank throughout. Where a row relies on a caption (for example Fig. 12 for XI/18, Fig. 1 for XII/56 and XII/61, Fig. 20 for XIV/2/15), the caption is cited in `notes` as text only.
- Pages rendered at 150 dpi to check the text layer and to read the scanned pages. They are in `/tmp/claude-0/-home-claude/729c536d-b448-586f-923d-45ae3ca7c96d/scratchpad/reader_A_g4/`:
  - 2584: PDF pp. 2-8 (printed 169-175)
  - 2585: PDF pp. 2-6 (printed 177-181)
  - 2586: PDF p. 2
  - 2587: PDF pp. 2-3
  - 2589: PDF p. 2
  - 2590: PDF pp. 3-7 (printed 188-192)
  - 2592: PDF pp. 2-5 and 7-11 (printed 209-212 and 214-218)
  - 2593: PDF p. 2
- Text-layer errors corrected from the page images:
  - XIII/8 width: the text layer has "2.5^1.0"; the page has **2.5-4.0 m**.
  - XIV/4: "200 450 m" is 200-450 m.
  - XIV/2/3: "(I x 2 m)" is 1 x 2 m.
  - X/10: "!.0x2.5" is 1.0 x 2.5 m.
  - The ware name is el-Mefjer, not "el-Meljer".

## Keying conventions used

- **Unlabelled "a x b" dimensions.** The larger value goes in length_m and the smaller in width_m, and the row's notes give the printed order. Dimensions the source labels are copied as labelled; for example, the XIII/2 chamber is length 4 and width 6.
- **Unlabelled entrance dimensions** (Region X Table 1, "Entrance Dimensions" column). These are keyed as width x height in printed order, because the labelled rows of that column give width first, then height. Confidence is medium.
- **Entrances that have dimensions or a facing** get their own `doorway` row (`.a`), and the parent row carries `n_openings`.
- **n_openings.**
  - It holds the stated number.
  - It is 1 when the source describes one entrance or opening of the feature: a dimension, a shape, "an entrance", "its opening", or a single "Entrance Dimensions" entry in the table.
  - It is blank when no entrance is described.
  - It is `unknown` for XIV/17, where the source says "entrances" without a count.
  - Windows are not counted. One conflict: for XII/61 the text has one broad entrance but the Fig. 1 caption says "Entrances". I keyed the text.
- **opening_dirs.** Taken only from the text:
  - stated facings: "faces east" (XI/10, XIII/8), "opens to the south" (XIV/33), "faces north" (XIV/2/11), and entrances "to the east" or "to the south" (XIV/2/5)
  - entrances placed "in the northern/southern wall", "to the north and south", or "in the wall to the southeast" (XIV/2 cells), read as facing that way
  - XIV/2/15 = S, from "southern side" plus the Fig. 20 caption (medium)
  - None were taken from plans or photographs. Photo captions saying "looking west" are mentioned in notes only.
- **Numeric "unknown".** The only case is the X/42 height, which "could not be ascertained".
- **Areas.** Areas given in sq m have no column, so they are in notes only: XI/1, XI/5, XI/6.d, XI/9.c, XI/11, XI/13, XI/15, XI/18, XI/20.
- **Relations.**
  - `rel_bearing_deg` is the bearing from the related feature to the row's feature, converted from the printed compass word (east = 90, SSE = 157.5, SSW = 202.5, and so on).
  - above and below relations carry a distance only.
  - Containment is expressed through `parent_id` and is not repeated in `relations`.
- **grid_system.** OIG for every printed map reference: the 5+5-digit, 4+4-digit (centred group) and 6+6-digit (XII/50) forms.
  - The Region XIII introduction speaks of "126° latitude (UTM)", but its references are in the same format.
  - XII/49 is printed `12749/19288` (apparently transposed) and is copied as printed.
  - The XI/19 northing `12391` is out of sequence with its neighbours and is copied as printed.
- **position_basis.**
  - `feature_grid`: the feature has its own map reference.
  - `site_grid`: the reference is centred on a group, is printed as "As X/1" (X/1's reference copied, with a note), or is the parent's reference copied onto a sub-feature row.
  - `text_only`: there is no reference.
- **construction.**
  - `natural` for all 61 Region X features, from the general statement on p. 169 (natural caves, no quarrying).
  - `natural` for Region XI caves, from "22 natural caves" on p. 177.
  - `mixed` where rock cuttings or built closing walls combine with a natural cavity: XI/13 and most XIV/2 cells.
  - `built` for walls, fences, pillars, structures and stone-lined features.
- **Class mapping where the list has no exact term.**
  - niche → `other`
  - passage, tunnel or corridor → `other`
  - kokhim → `tomb`
  - tumulus → `cairn`
  - compound or courtyard → `court`
  - animal pens, installation, hearths and benches → `other`
  - Hearths are keyed only when built or when they are a numbered survey site (XI/6.e, XIII/10, XIV/2/7.b).
- **in_window.**
  - `yes` where the source states Early Roman, 1st c. BCE to 1st c. CE, Jewish War, Great Revolt or Late Hellenistic.
  - `no` where every stated period lies outside the window.
  - `unknown` where the source gives only undivided "Hellenistic" or "Roman", or a single surface find.
  - blank where no period is given.
- **Labels inferred or constructed** (each flagged in notes):
  - XIV/19-22, XIV/48-49 and XIV/56-58 are inferred from their section headings.
  - XIV/50 is printed "XIV/30".
  - Constructed IDs: `XIV/unnumbered_19340-12765`, `XIV/4.five`, `XIV/2/2a-b.a` (the pit holding the coin hoard), `C-7a` (the survey's own number) and `XIV/13-16.a`/`.b`.
  - XIV/2/2 sub-features use `.n`, `.s` and `.w` so they are not confused with Cells XIV/2/2a-b.
- **Not keyed** (no attribute beyond class, or not features):
  - the other two hawwar caves of Region XIV
  - XIV/2/12-13, which the text never describes
  - the notches in upper Nahal Samar
  - the "dozens of shallow rock hollows" around XIV/6
  - hearths known only from soot spots
  - probes, trenches and excavation squares
  - all finds

## Items that may need a third reading

- X/59: the inner chamber is given as both "9 m, width 10 m, height 0.5 m" and "(4 x 6 m, height 1.5 m)".
- XI/11: the area of 12 sq m and the height of 4.5 m are printed after "The entrance to Cave XI/11".
- XIII/6, XIII/7, XIII/12: the opening length of each rock shelter was keyed as `width_m`.
- XIII/8: the dimensions are printed after "the western third of the cave".
- XIV/2/16: the text says it lies 45 m south of "Room XIV/2/16" (a self-reference), keyed against XIV/2/15.
- XIV/4: the larger cave (1.2 x 2.0 m, height 1.5 m) is not assigned to either XIV/4/1 or XIV/4/20.

## Counts

- Rows: 298. Top-level caves and sites: 144.
- Rows with at least one dimension: 114.
- Rows with `n_openings`: 76. Rows with `opening_dirs`: 18. Rows with `n_steps`: 0. Three staircases or step features are keyed, but none gives a step count.
