# ben93, reader B: keying log (run 28)

- Source: Goldfus & Golani, Map of Wadi el-Makkukh (Part IV), in Finkelstein & Magen (eds), *Archaeological Survey of the Hill Country of Benjamin* (1993).
- Started 2026-11-01T03:01Z (container clock). Finished 2026-11-01T03:29Z.
- Output: `keyed/ben93_B.csv`, 211 rows. sha256 980962e6ca28215523ac1a33a93cc564f2751583cb4d2c4e419b7f766c2b32f9.
- I did not open `keyed/ben93_A*`, *ʿAtiqot* 41, the concordance files, any `../attribute_inventory_2026-10-31/keyed` or `out` file, or the project notes.

## Pages read

The Hebrew scan is `pdf/Magen-Finkelstein-eds-1993-...-528e30a1`. The PDF page number is the printed page plus 22 throughout Part IV.

| Printed page | PDF page | Content | How read |
|---|---|---|---|
| 285 | 307 | Site 324 (start); fig. 3 of site 322 | 200 dpi |
| 286 | 308 | Sites 324 (end), 325, 326, 327 (start) | 200 dpi |
| 287 | 309 | Site 327 text; figs 1-2 (photographs) | 200 dpi |
| 288 | 310 | Site 327 figs 3-4 (photographs) | 200 dpi |
| 289 | 311 | Site 327 text; fig. 5 (site map, scale 0-400 m, north arrow) | 200 dpi |
| 290 | 312 | Site 327 text (end); fig. 6 (sherds) | 200 dpi |
| 291 | 313 | Sites 328, 329, 330 | 200 dpi |
| 292 | 314 | Site 331 | 200 dpi |
| 294 | 316 | Site 339 | 200 dpi |
| 295 | 317 | Site 340 | 200 dpi |
| 296 | 318 | Site 343 | 200 dpi |
| 305 | 327 | Site 363 | 200 dpi |
| 325-326 | 347-348 | Sites 415, 416 | 200 dpi |
| 327 | 349 | Sites 418, 419 | 200 dpi |
| 329 | 351 | Sites 423, 424, 425 | 200 dpi |
| 331 | 353 | Introduction to the caves of Wadi el-Makkukh, with a footnote on the cave labels | 40 and 200 dpi |
| 332 | 354 | Start of the cave list (caves 5 — 7A and 82 — 25A); map of the Wadi el-Makkukh caves | 150 and 600 dpi |
| 333-335 | 355-357 | Cave list | 90-250 dpi strips and crops |
| 336 | 358 | Appendices (shows that the list ends on p. 335) | 40 dpi |

I also looked at some pages at 30-40 dpi only to find the others: printed 258, 265, 278, 293, 297, 303-304, 306-307, 313, 323-324, 328 and 330, plus PDF p. 305 (a plate page). I did not key anything from them. Printed p. 278, the overview by period, mentions "site 330" as a cave in Wadi Uja with Chalcolithic finds. That does not match entry 330 (an animal pen), and I did not key it.

English summaries, from the photographed copy `pdf/01-Benjamin-1993-indexed-94423925`:

- Pages 46*-49*, 56*-57* and 58*-59* were read. Pages 66*-67* were seen at low resolution while locating pages.
- The English adds only one thing: the area of site 327 (80 dunams), which is recorded in that row's notes.
- The English confirms the order of the grid numbers (easting first, for example "18080 14310" for site 324).
- The English summary has no entries for the cave list.

Tesseract (`heb`) OCR of these pages was used only as a reading aid, and every number keyed was checked against the scan. The OCR made one error that matters: it dropped "4." from the width of site 418. The scan reads 4.5 m, and 4.5 is what is keyed.

## Conventions

- **Cave ids.**
  - The note on p. 331 says each cave is labelled with its serial number in the Cave Research Unit (MALHAM) survey, then the photo number, then the bank (A is the south bank, B the north bank). It prints the label as, for example, `5 — 7A`.
  - Cave numbers repeat between photos, so the feature_id is `ben93:<cave no.>-<photo><bank>`, for example `ben93:5-7A`.
  - The source prints `7 — 29A` twice for two different caves: the Spring Cave at 18108 14427, and another cave at 18110 14420. The second one is keyed as `ben93:7-29A(2)`.
  - Caves 85 and 87 — 28A have a single entry (the Cave of the Steps). They are keyed as a complex row `ben93:85+87-28A`, plus `85-28A`, `87-28A` and the complex's sub-features.
- **Scope.** The brief gives the cave list as pp. 333-335, but the list starts on p. 332 (caves 5 — 7A and 82 — 25A). Those two caves are keyed too. The list ends on p. 335 with cave 3 — 45B.
- **Grids** are recorded easting first, as the numbers stand from left to right on the page and as the English summary prints the same references. All grids are the Israel grid ("נ"צ ר"י") of 1993, so `OIG`. The UTM references printed for each site are given in the notes of the site rows only.
- **Unlabelled dimensions.**
  - Most caves give only "מידותיה a × b × c מ'", with no labels.
  - I keyed the three numbers as length, width and height in Hebrew reading order: the number next to the word מידותיה comes first.
  - Reasons for that order: ranges in this text read in ascending order right to left (for example "ל־2-3 יחידות", "1-5 מ'"), and Tesseract gives the same order.
  - On the page itself, read left to right, the order is reversed.
  - The source never says which number is the length, width or height. The order is not consistent either: in some caves the largest number comes last, as in 25 — 25A, 70 — 25A and 29 — 20A. These rows therefore have confidence medium, and the note says the assignment is by reading order.
- **Constructions.**
  - `natural` = the source says "טבעית".
  - `mixed` = natural with cutting or building added, or "widened by cutting".
  - `rock_cut` = the source says "חצובה" of the cave itself.
  - `unknown` = only "cuttings seen".
  - Blank otherwise.
- **Steps** are never counted in the source, so `n_steps` is always blank. `steps_where` follows the wording:
  - "lead to it": `into_feature`
  - "cut in it" or flights joining levels: `inside`
  - "around the cave": `outside`
  - "steps seen": `unknown`
- **Openings.** `n_openings` is filled only where the source names one opening or gives a count: 84 — 28A, 36 — 21A, 37 — 21A and its doorway, 8 — 25B, 3 — 45B, 363.cave, and site 328 (3 openings). Plural or "several" openings are left blank and described in the notes.
- **Opening directions.** The only compass direction for an opening in scope is the niche facing east in cave 5 — 7A (`5-7A.niche`, `E`).
- **Pillars.** The source records no pillars anywhere in scope. "פירים" means shafts, and they are keyed as `pit`.
- **Bearings.** `rel_bearing_deg` is the direction in which this row's feature lies as seen from the related feature. For example, "200 m west of the pen" is keyed as 270. Distances given as "כ-" (about) are keyed as printed, with "c." in the notes.
- **Group rows.** Repeated features that are not described one by one (kokhim, niches, several cisterns, and so on) get one row, with the count in the notes. Chambers whose number is stated get one row each, following rule 6: 5 rooms in 5 — 7A, and 7 cavities in 85/87 — 28A. Those rows have low or medium confidence.
- **Kokhim** (כוכים) are classed as `chamber`, because the source does not state their function. **Animal pens** (מכלאה) are classed as `court` (a walled enclosure). Threshing floors and stone circles of uncertain use are classed as `other`.
- **in_window** is set as follows:
  - `yes`: Hellenistic sherds, or the 1st-2nd centuries CE (the Spring Cave 7-29A, and sites 340 and 363).
  - `no`: every dated find lies outside the window.
  - `unknown`: undated, no datable sherds, or "Roman" without further detail.
  - Blank: the source says nothing about date.
  - The period recorded for a site applies to the site row only. Sub-features are blank unless the source dates them.
- **Relations.**
  - Caves 56, 55, 54, 67, 64, 63 and 58 are listed under "near the Church Cave". They get `next_to:ben93:57-25A`.
  - Caves 25-91 are listed under "an additional complex a little south of the church". They get `next_to:ben93:57-25A` with a bearing of 180. That heading has no end marker, so I took the group to end before 45 — 22A, and those rows are flagged medium in their notes.
  - Cave 57 — 25A gets `inside:ben93:327`, because the source cross-refers it to site 327. The church in site 327 (`327.church`) and cave 57 — 25A are the same feature by that cross-reference. Each is keyed under its own entry.
- **Quotes** are copied from the Hebrew, with the maqaf typed as "-", and no quote is longer than 15 words.

## Rows with no attribute beyond class

These rows are kept because the scope names every cave in the list and every listed site, and they have confidence low:

- 12 — 30A and 5 — 32A (grid only)
- 7 — 29A(2) and 4 — 52A (grid, sherds, robbers' digging)
- Site 339 (shape uncertain)
- Site 425 (the remains reported in 1968 were not found)

## Problems

1. Duplicate cave label 7 — 29A (see above).
2. The order of the unlabelled dimensions is uncertain (see above). This affects about 30 rows.
3. It is not clear which caves belong to the group "south of the church" (see above).
4. Cave 64 — 25A is listed as a cave but described as a single cut kokh (0.5 × 1 × 1 m). It is keyed as `chamber`.
5. The source gives the total length of the Makkukh Cave (3 — 45B) as "more than 150 m". This is a lower bound, so it is recorded in the notes and not keyed as a number.
6. No dimensions were measured from plans. Fig. 5 of site 327 has a scale and a north arrow, but the text gives the dimensions needed. The map of the caves on p. 332 is a location map only.
