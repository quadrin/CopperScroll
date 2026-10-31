# atq41, reader A, group g1: keying log

- Started: 2026-10-31T22:02:54Z
- Finished: 2026-10-31T22:24Z
- Output: `keyed/atq41_A_g1.csv`, with 221 rows covering 68 survey labels. 3 of the labels are group rows (II/20-31, II/33-41, II/52-60). There is also one path row with the pseudo-label III/8-11.

## Articles and pages read (full text, pypdf extraction)

| Article | Title | Printed pages | PDF pages |
|---|---|---|---|
| 2544 | Region I: Wadi el-Makkuk and Wadi ed-Daliya (Peleg and Hameiri) | 1-4 | 2-5 |
| 2546 | Region II: Upper Wadi el-Makkuk (Hirschfeld and Riklin) | 5-19 | 2-16 |
| 2550 | Region III: Lower Wadi el-Makkuk (Barshad and Shaked) | 35-40, plus an unnumbered captions page | 2-8 |

The first page of each article carries no page number. I inferred it from the running head on the next page: 1, 5 and 35. Region II's "5" is also confirmed by the cross-reference "part 2: pp. 5-19". Region II page 8 has a running head without a number, so 8 is inferred from its position between pages 7 and 9.

## Figures and plans

- None of the plans or figures cited in the text is in the Part 2 (English) PDFs. Each article ends with a captions list only, so the plans are in Part 1. The plans concerned are Region I Plan 1; Region II Plans 1-8 and Figs. 1-27; Region III Plans 1-2 and Figs. 1-9.
- So no `plan_scaled` values were keyed, and the `figure` column is blank throughout.
- I rendered the following, all in scratch `reader_A_g1/` and none in the repo:
  - Low-resolution views of 2546 p.16, 2550 p.8, 2544 p.5 and 2550 p.2, to confirm that the captions pages and first pages hold no plans.
  - 200-dpi crops of the page images to check OCR-sensitive readings:
    - I/11 grid "18730–40/15150"
    - II/19 grid "19099/14501" (as printed)
    - I/13 "c. 200 m above it"
    - II/61 "max. height 15 m"
    - I/4 dimensions
    - the Region I intro "Shuqfan el-ʿAzvat Cave (I/5)"
    - III/11 "the cistern (L5)"
    - II/32 "(bama)"
    - II/7 "north of Cave II/9"

## Nothing unreadable

The OCR text was clean apart from "1/" and "11/" for I/ and II/ (normalised to the printed Roman labels), a few garbled coin legends (not keyed), and "(Jaamd)" for the printed "(bama)".

## Conventions used

- **length/width:** length is the larger horizontal figure. A printed "depth" of a chamber (II/10.a) went into `depth_m`, with a note.
- **Opening and other dimensions:** opening and entrance sizes are in `notes`. For buildings and terraces, `height_m` is the preserved wall height, with a note.
- **n_openings:** counts openings to the outside that the text states or names in the singular ("the entrance"). Internal openings (ceiling holes, rear sealed openings) are only in notes.
- **opening_dirs:** keyed only where the text says the opening faces a direction (I/14 S, II/4 W, II/5 N, II/18 NE, II/32 S). The "southwestern/northeastern openings" of II/2 are positions, so they were not keyed as directions.
- **Relations and bearings:**
  - A relation means "this feature is <relation> that feature".
  - `rel_bearing_deg` is the printed compass word turned into degrees, measured from the referenced feature to this feature.
  - `rel_distance_m` is given only where printed.
- **Sub-features:**
  - Suffixes .a, .b and so on follow the order of mention in the text.
  - Sub-features carry the containing site's map ref as `site_grid`.
  - Map refs printed for a group of caves (or "centered around") are also keyed as `site_grid`.
- **grid_system:** OIG. The text never names the system, but the values are old-grid style (northings 144xx-154xx).
- **construction:** filled only where the entry says natural, hewn, rock-cut or built, or names a material for walls. The region-wide "karstic" was used only for II/1, where it is combined with the entry's quarrying.
- **in_window:**
  - yes: dated finds or use in the Hellenistic-Early Roman range.
  - no: only other periods are stated.
  - unknown: ambiguous or contradictory.
  - blank: no dated finds.
- **Steps counted twice:** where steps lead into a feature, `n_steps` is on both the parent row and the steps row (II/8, II/42).
- **Niches:** class `other` with `class_as_printed` "niche".
- **Passages, corridors, tunnels and crawlways inside caves:** class `chamber`.

## Labels not keyed (no attribute beyond class)

- I/17-19: named only as part of the complex.
- II/62-63: two caves, no finds.
- II/65: a "large cave" with no dimensions.
- Unnumbered small niches around I/1-2.
- Excavation squares and loci that are not features (e.g. I/4 L5, I/14 L1 and L2).

## Source inconsistencies (flagged in notes)

- The intro calls Shuqfan el-ʿAzvat "I/5", but its entry is I/14.
- Region II Conclusions list "II/2 (northern bank)" with Early Roman finds. II/2 is on the southern bank and had no finds; II/1 fits.
- II/7 is printed as "north of Cave II/9".
- The II/19 easting is printed as 19099.
- In III/11 the labels L2 and L5 are swapped between the description and the excavation report.
- III/1 is called the easternmost but its easting is lower than III/14's (the westernmost).

## Exposure notes

- A page-inventory command globbed the shared PDF cache and printed about 60-character first lines of the other ʿAtiqot 41 article PDFs there (2553, 2554, 2556, 2559). Nothing else from them was read.
- Opening READER_INSTRUCTIONS.md triggered an automatic display of /home/claude/cs/AGENTS.md (general project rules, no feature lists). I did not act on it.
- I did not open any other file in /home/claude/cs, anything under keyed/, sources.csv, the Projects tool, Drive or the web.
