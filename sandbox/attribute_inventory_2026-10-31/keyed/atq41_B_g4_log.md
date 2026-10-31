# atq41, group g4: reader B log

- **Reader:** B
- **Source:** atq41, *'Atiqot* 41, part 2 (English), 2002
- **Started:** 2026-10-31T22:02:54Z
- **Finished:** 2026-10-31T22:26Z
- **Output:** `keyed/atq41_B_g4.csv`, 308 rows. The rows cover 140 survey entries (caves and sites). With cells and sub-numbers counted separately, there are 164 distinct labels.

## Files read

I read only SCHEMA.md, READER_INSTRUCTIONS.md, the 9 article text files listed in the task, and PDF pages that I rendered with `render_page.py`. Renders are in the scratch folder `reader_B_g4/`, outside the repo.

| Article | Section | Printed pages | Text file | Pages rendered and checked |
|---|---|---|---|---|
| 2584 | Region X | 169–175 | OCR text read in full | PDF pp. 2–7 (printed 169–174). All table values and measurements checked against the page images. |
| 2585 | Region XI | 177–183 | Read in full. The text **lacks printed pp. 177–179** (PDF pp. 2–4 are image-only scans) | PDF pp. 2, 3, 4 (printed 177–179, holding XI/1–XI/15). These were keyed from the images. Also PDF p. 5 (180) and p. 8 (183, captions). |
| 2586 | XII/49 | 185 (inferred) | Read in full | Not needed |
| 2587 | XII/50, 52, 53 | 185–186 | Read in full | PDF p. 2 (cropped strip, no page number) |
| 2588 | XII/56 | 186 | Read in full | Not needed. The text is the same as in 2587/2589. |
| 2589 | XII/61 | 186 | Read in full | PDF p. 2 (cropped strip) |
| 2590 | Region XIII | 187–193 | OCR text read in full | PDF pp. 2–7 (printed 187–192). Table 1 checked. |
| 2592 | Region XIV | 209–219 | OCR text read in full | PDF pp. 2, 3, 4, 5, 7, 8, 9, 10, 11 (printed 209–212 and 214–218). Checked. |
| 2593 | Region XV | not printed | Read in full | PDF p. 2 |

## Figures and plans

**No plan could be used.** Every plan and figure cited in these articles ("Plan 1", "Fig. 4" and so on) belongs to the Hebrew Part 1. The Part 2 PDFs hold only the English text and the captions. Article 2585 has only 8 pages, and none of them is a plate; its 3 image-only pages are scanned text.

As a result, all dimensions are `text` or `table`, none are `plan_scaled`, and the `figure` column is blank throughout. Wherever a feature has a plan in Part 1, the notes say so ("plan in Part 1 (Hebrew), not in this PDF"), so that a third reading could measure it.

## Page numbers

- **Inferred first pages.** The first page of each article carries no printed number, so I took it from the next page:
  - Region X: p. 169
  - Region XI: p. 177
  - Region XIII: p. 187
  - Region XIV: p. 209
- **XII/49 and XII/50–53: p. 185, inferred.** The next page's running head is "186", and the XII/53 captions continue across onto it. Each of these rows says so in its notes.
- **XV/3: keyed as `art2593`.** No page number is visible.

## Conventions I applied

- **Entrances as separate rows.** An entrance whose size is given has its own `doorway` row, with `parent_id` pointing to the cave. The cave row carries `n_openings` and `opening_dirs`.
- **Unlabelled entrance sizes.** For an entrance printed as "a × b" with no labels (Region X, Table 1), I keyed width = a and height = b. Each such row has confidence medium and a note.
- **Unlabelled room or cave sizes.** For a cave or room printed as "a × b", I keyed the larger value as `length_m` and the smaller as `width_m`. Each case is noted. Labelled values are keyed as labelled.
- **Wall thickness** goes into `width_m`, with a note.
- **Areas** ("c. 8 sq m") have no column. They are recorded only in notes.
- **`n_openings`:**
  - **1** when the source describes one entrance or opening of the feature, including a single entry in Region X's Table 1 "Entrance Dimensions" column.
  - **`unknown`** for XIV/17, where "entrances" is plural but no number is given.
  - **Windows are not counted.** They are recorded in notes.
- **`opening_dirs`** is keyed only where the text states it. "Faces east" and "entrance in the northern wall" both count; photo captions such as "looking west" do not.
- **Construction from general statements.** Two articles make a statement that covers all their caves:
  - Region X: "entrances to 61 natural caves... no signs of quarrying".
  - Region XI: "22 natural caves".

  On that basis every Table 1 entry X/1–X/61 is keyed with construction `natural`, at confidence medium; most of these entries have no other attribute. Region XI caves are also keyed `natural`, except XI/13, which is `mixed` because rock cuttings are stated. Cells and niches that are closed by built walls are `mixed`.
- **Relation bearings.** `rel_bearing_deg` is the bearing from the related feature to the row's feature. I converted the printed words to degrees: east = 90, south-southeast = 157.5, and so on. `rel_distance_m` is as printed.
- **`in_window`:**
  - `yes` where Hellenistic, Early Roman, Herodian, first-century CE or Jewish War (67–68 CE) material is stated.
  - `no` where the dated material is stated only for other periods.
  - `unknown` for "Roman", "Roman?" or other unclear dating.
  - Blank where the source gives no date.
- **Grid references** are copied exactly as printed. `grid_system` is `unknown` throughout, because no article names its grid. Region XIII mentions "126° latitude (UTM)" for the survey limits only.
- **Group entries are keyed as one row each**, with notes. Examples: "Three adjacent caves", XIV/3, XIV/23-32, XIV/13-16, and the hearths, cairns and pens.
- **One row with no survey label.** The marl cave near Horbat Qumran at map ref 19340/12765 is keyed as `atq41:XIV/hawwar`.

## Unreadable or problem points

- **Region XI, pp. 177–179.** These pages are missing from the extracted text and were read from the page images instead (fully legible).
- **XI/19.** The map ref is printed "19343/12391" and is keyed as printed.
- **XII/49.** The map ref is printed "12749/19288" (the two numbers appear swapped) and is keyed as printed.
- **XIV/2/16.** The text says it lies "c. 45 m south of Room XIV/2/16", which refers to itself. No relation is keyed.
- **XIV/48–50.** The third cave is printed "XIV/30".
- **XIV/4.** The Fig. 23 caption names XIV/4/2, where the text has XIV/4/20.
- **X/59, inner chamber.** The measurements are ambiguous and the row is keyed at confidence low.
- **XIII/6.** The entrance is printed "(width c. 8 m, max. length 3 m)", and the length is ambiguous.
- **XIII/8.** The dimensions follow the words "the western third of the cave". They are keyed as the cave's dimensions, at confidence medium.

## Counts

| Measure | Rows |
|---|---|
| Rows in total | 308 |
| With any dimension | 120 |
| With `n_openings` | 78 |
| With `opening_dirs` | 16 |
| With `n_steps` | 0 (three staircase rows; none gives a count) |
| With pillars | 1 (XII/53, 2 pillars) |
| With plaster | 0 (plaster is never mentioned) |
