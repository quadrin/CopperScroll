# ben93, reader A: keying log (run 28)

- Source: Goldfus & Golani, "Map of Wadi el-Makkukh", Part IV of Finkelstein & Magen (eds), *Archaeological Survey of the Hill Country of Benjamin* (1993). I keyed from the Hebrew entries. I used the English summaries only as a supplement, and the notes say where.
- Started: 2026-11-01T03:01:23Z. Finished: 2026-11-01T03:30:53Z (UTC).
- Output: `keyed/ben93_A.csv`, 196 rows. It was written with Python `csv`, in UTF-8, with the SCHEMA.md header in its set order.
- I did not open ʿAtiqot 41, `keyed/ben93_B*`, any `../attribute_inventory_2026-10-31/keyed` or `out` file, the concordance files or the project notes.

## Pages read

The Hebrew scan is in the bucket at `pdf/Magen-Finkelstein-eds-1993-Archaeological-Survey-of-the-Hill-528e30a1`. Printed page = PDF page − 22.

| Printed page | PDF page | Content | How read |
|---|---|---|---|
| 258, 318 | 280, 340 | Used only to find the page offset | low-res image |
| 265–282 | 287–304 | Part IV title, introduction, roads, periods (used only to find the site entries) | low-res images, skimmed |
| 283–290 | 305–312 | Sites 322–327, with 327's figs. 1–6. Fig. 5 (p. 289) is the site map; I viewed it but took no measurements from it. | images and OCR |
| 291–292 | 313–314 | Sites 328–331 (and 332–333 as neighbours) | images and OCR |
| 294–296 | 316–318 | Sites 339, 340, 343 | images and OCR |
| 304–306 | 326–328 | Site 363 | images and OCR |
| 325–330 | 347–352 | Sites 415, 416, 418, 419, 423, 424, 425 | images and OCR |
| 331–335 | 353–357 | Section C, "Caves of Wadi el-Makkukh": the introduction on p. 331, the cave map on p. 332 (viewed, not used), and the cave list on pp. 332–335 | images and OCR |

- The English summary is in the bucket at `pdf/01-Benjamin-1993-indexed-94423925`. I viewed PDF pp. 267 (46\*–47\*), 268 (48\*–49\*), 272 (56\*–57\*) and 273 (58\*–59\*). They give one-line site summaries and no cave list.
- I used them for two things only:
  - to confirm that grids are printed E then N;
  - to add "80 dunams" to the notes for site 327.
- Pages 285, 287, 288, 289 and 332 are separate small-format scans with a different page size. They read normally.
- Reading aids: I OCRed PDF pages 305–360 with Tesseract, in both `heb` and `eng` modes, and used the output to locate the site headers. Every keyed entry was checked against the page image.
  - `heb` gives the logical (reading) order of the text.
  - `eng` gives the left-to-right visual order of the number groups. I used it to fix the printed order of grids and dimensions, after checking that order by cropping single lines into segments.

## Reading conventions and decisions

1. **Grids.** A grid is copied as it reads left to right on the page, for example `18080 14450`. This is the E N order, confirmed against the cave-map axes and the English summary. Grid system = `OIG` (נ"צ ר"י). The UTM pair printed in each site header goes in the notes.
2. **Unlabelled cave dimensions.** The cave list prints dimensions as `מידותיה a × b × c מ'` without saying which is length, width or height.
   - I keyed a, b and c as length, width and height in the left-to-right typeset order. That is the same convention the page uses for grids.
   - A right-to-left Hebrew reading would reverse the order. Neither order gives consistently plausible heights. For example, cave 29-20A reads 50 × 7 × 3, while cave 8-29A reads 2 × 2 × 15.
   - Every such row therefore has `confidence = medium`, and its notes give the printed string and say the assignment is uncertain.
3. **Hyphen ranges** are printed Hebrew-style, with the larger number on the left: `5-1` means 1 to 5. Ranges are keyed in ascending order (`1-5`). The quotes keep the printed form.
4. **feature_id for caves** = cave number + MALHAM photo/bank code as printed, for example `ben93:92-28A`. The footnote on p. 331 defines the code: A = south bank, B = north bank, number = photo. The bare cave numbers repeat across photos, and some would collide with site numbers.
5. **Sub-features** take the suffix `.<tag>` (for example `.cistern`, `.kokhim`, `.hall`).
   - A plural with no count, or a counted plural whose members are not described separately, gets one **group row**. Its notes say "group row" and give the count when one is printed.
   - Members the source describes separately get separate rows, for example 340.a/.b (diameters 18 and 16.4 m) and 416.a/.b (6.4 and 7.1 m).
6. **parent_id** is set only where the feature is physically inside or part of another feature. Those rows also carry `inside:` in relations. Features at a distance from a site carry `next_to:` with the printed distance, and parent_id is left blank.
7. **Bearings.** Compass directions in the text ("c. 150 m east of site 324") go in the notes. `rel_bearing_deg` is left blank because no bearing is printed as a number.
8. **n_openings** is set only where the source says how many openings there are:
   - 328 = 3 openings;
   - 1, from singular wording ("the cave has a small hidden opening", "a square opening is cut", "the opening is square", "its opening", "the entrance"), for 3-45B, 37-21A, 84-28A, 8-25B, 36-21A and 363.cave.
   - Uncounted plural openings (70-25A, 4-44B) are left blank and explained in the notes.
9. **opening_dirs:** no opening direction is stated anywhere in scope. Two cases are left blank on purpose and explained in their notes:
   - the east-facing **niche** in 5-7A (a niche, not an opening);
   - the windows of 85/87-28A, which face "the slope", not a compass point.
10. **Steps:** no step count is printed in scope, so `n_steps` is blank everywhere. `steps_where` is filled where steps are mentioned.
11. **Kokhim (כוכים)** are keyed as class `other`, because burial use is not stated. Niches, recesses, mortars, benches and windows are also `other`. A cupmark (ספלול) or trough (שוקת) is `basin`. A pen (מכלאה) or threshing floor (גורן) is `other`.
12. **Construction:** `unknown` is used where the source mentions cutting but does not say whether the cave is natural or cut, so the attribute is raised but not settled.
13. **Periods** are translated from Hebrew. `in_window`:
    - `yes` only where the source reports Hellenistic sherds (sites 340, 363) or "1st–2nd centuries CE" (cave 7-29A);
    - "Roman" with no further date is `unknown`;
    - `no` for 3-45B, because the section introduction on p. 331 ties its Roman-period use to the Bar-Kokhba revolt.
    - Sub-features of sites take no period, because the sherds are dated per site.
14. **site_name** is the printed name where there is one: the Latin form printed in the header (Khallat ed-Dinnabiya, 'Ein en-Nueimeh) or the Hebrew cave name (מערת הכנסייה and so on). It is blank for unnamed sites and caves.

## In scope but not keyed (no attribute beyond class)

- **Cave entries:**
  - `12 — 30A` (p. 335): grid only.
  - `5 — 32A` (p. 335): grid only.
  - `4 — 52A` (p. 335): grid, sherds and robbery traces only.
  - The **second** entry labelled `7 — 29A` (p. 334, grid 18110 14420): robbery traces only.
- **Sites:**
  - **339** (p. 294): "scant remains of a small structure, either square or round". No size, construction or relation is given.
  - **425** (p. 329): building remains and sherds were reported by the 1968 survey, but none were found in this survey and no attributes are given.

## Other points for the third reading

- The cave list begins on **p. 332**, with caves 5-7A and 82-25A, not on p. 333 as the brief says. Both are keyed.
- The label `7 — 29A` is printed twice on p. 334. I keyed only the first, "Spring Cave" (מערת הנביעה).
- `1 — 34A` (18270 14425) shares the photo code 34A with `6 — 34A` (18160 14415), about 1.1 km away. It is keyed as printed and the notes say so.
- Caves 85 and 87, "Cave of the Steps", are described jointly. Both have cave rows. Their sub-features are keyed under 85-28A with an `inside:` relation to 87-28A as well.
- Cave 57-25A (cave list) and 327.church (site 327 entry) are the same Church Cave. Both rows are kept because they come from separate entries, and each row's notes point to the other.
- Site 327's sub-features are keyed from the running text on pp. 286–290: upper-level dwellings, lower-level caves, path, channels, cisterns, the church and its parts, the burial complexes, a small cave, and two buildings.
- Site 415's road has these sub-features:
  - three points of cuttings and retaining walls;
  - a dam (2 × 15.5 m) with terraces;
  - the northern branch, with rock-cut steps at 1891 1456;
  - the southern branch.
- Git shows `keyed/ben93_A.csv` as modified against HEAD. A version is already tracked in the repo. I did not open it, and I did not commit.
