# atq41, reader B, group g2: keying log

- Started: 2026-10-31T22:02:55Z (UTC)
- Finished: 2026-10-31T22:23Z (UTC)
- Output: `keyed/atq41_B_g2.csv`, 202 rows, written with Python's `csv` module (QUOTE_MINIMAL), header in SCHEMA order.

## Read (in full, pypdf plain text)

| Article | Author | Printed pages | Notes |
|---|---|---|---|
| 2553 Regions IV and VI: Survey and Excavations of Caves along the Jebel Abu Saraj Cliff | O. Sion | 43-70 | Read every line, including Region VI (VI/31-59), the summary, tables, notes, references and captions. Page numbers taken from running heads (PDF page n = printed page n+41; first page 43 has no printed number, and Wolff's reference list gives "pp. 43-70"). |
| 2554 The Excavation of Cave IV/11 ('Cave of the Pillar') (Summary) | N. Feig | 71 | One-page English summary and captions. No page number is printed; p. 71 comes from Sion's reference list ("English summary, part 2: p. 71"). The full report (Part 1, pp. 85-90, Hebrew) is not in this group. |
| 2556 The Excavation of Cave IV/12 | S.R. Wolff | 73-83 | Read in full. First page unnumbered; 73 inferred from the next page's head "74". |

## Figures rendered (scratch only: `/tmp/claude-0/-home-claude/729c536d-b448-586f-923d-45ae3ca7c96d/scratchpad/reader_B_g2/`)

- 2553: a contact sheet of all 28 text pages, and PDF pages 2 and 9 at 60 dpi. **The English Part 2 PDF has no plans or photographs.** Plans 1-8 and Figs. 1-36 are listed in the captions but are printed only in Part 1 (Hebrew), which this group does not include. So no plan values could be taken for IV/1, IV/2, IV/7, IV/8, IV/17, VI/43, VI/46 or VI/52. Each of these rows says so in its notes.
- 2554: PDF page 2 at 60 dpi. Text and captions only, no plan.
- 2556: PDF page 2 at 100, 150 and 400 dpi, showing **Wolff Plan 1** (plan and sections 1-1 and 2-2 of Cave IV/12). It has a 3 m scale bar and a north arrow, and I measured the arrow's pixels (north = image bearing c. 296 deg). From this plan I keyed:
  - opening_dirs = NE for IV/12 and IV/12.a. The outward bearing is c. 50-70 deg depending on whether it is taken from the passage axis or the mouth line, so it sits near the NE/E boundary. The text's "branch that turns off to the right (northwest)" agrees with this orientation.
  - Pit L002 (IV/12.d) keyed as depth, because the sections show it sunk below the floor.
  - Plan-scaled values that differ from the text are recorded only in notes, per rule 3: mouth width c. 1.0 m (text 0.7 m), and c. 8.5 m from mouth to far wall (text c. 6 m).

## Unreadable or problematic

- OCR noise in the text: Cyrillic "с." for "c.", "Lil" for "L11", "I V/3" etc. Quotes are written with the printed form restored. Every quote was checked against the source text; the only mismatches are these OCR artifacts.
- Table 2 (p. 66) labels Region VI caves "IV/43", "IV/45", and so on, and attributes coins 64-65 (Cave VI/46) to "IV/45". I did not use the table for keying.
- Sion (p. 52) and Feig (p. 71) print different grids for IV/11 (19030/14415 and 19015/14415). Both are kept in `grid_printed`.
- Several "[see Cave X]" grids differ from Cave X's own grid (IV/24, IV/29, IV/30, VI/43, VI/44, VI/45, VI/50-59). They are keyed as printed with `site_grid`.

## Keying conventions used

- Rows: one per cave, rock shelter, niche or pit with a survey label. Chambers, entrances, niches, passages, walls, terraces, cisterns, steps, pillars and so on get `.a`, `.b`... suffixes in order of mention, with `parent_id` set.
  - A cave with a single chamber carries that chamber's dimensions on the cave row.
  - A cave with several described spaces carries no overall dimensions unless the text prints them.
  - Wall and passage groups the text gives as one size range ("five passages", "erosion niches") are keyed as one row with low or medium confidence.
- Background landscape features from the introduction are keyed with constructed ids and say so in notes. These are the three springs, the aqueducts, three roads, and the notch of the IV/3-8 cliff. Unlabelled features with only a relation and no physical attribute (foot paths, slopes, rock ledges, dry waterfalls, the synagogue, the Doq fort) are mentioned only in notes.
- Class `other` is used for niches, passages and corridors, since neither word is on the closed list. IV/18 is printed "Niche" and so is keyed as `other`, although the text also calls it a cave.
- Two printed texts disagree on dimensions for IV/12 (Sion vs Wolff) and VI/46 (survey vs excavation). In both cases the survey figures are on the cave row and the others are in notes.
- `opening_dirs`: keyed only where the text says "faces X", places the opening "in its eastern/northern wall" or "on the opposite side" (medium confidence), or the plan's north arrow shows it (IV/12). Location labels ("southern entrance") and cliff names ("open onto the east cliff", IV/17) are not keyed as directions.
- `n_steps = unknown` where the text mentions steps without a count: "stepped floor" (IV/7, VI/43, VI/43.e, VI/52.j), "stepped rocky slope" (IV/28) and "natural rock steps" (VI/51). VI/33's "three hewn toe-holds" are keyed as 3 steps.
- `rel_bearing_deg` is the printed direction of this row's feature from the related feature: "X is c. 10 m north of Y" gives `next_to:Y`, 10, 0.
- `in_window`: `yes` where the source dates use to the 2nd c. BCE-1st c. CE (Hasmonean/Herodian coins, Late Hellenistic/Early Roman pottery, stated dates). `no` where all stated dates fall outside the window. `unknown` for undifferentiated "Hellenistic" or mixed-phase sub-features. Blank where no date is given.
