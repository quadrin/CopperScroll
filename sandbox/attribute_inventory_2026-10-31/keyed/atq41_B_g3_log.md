# atq41, reader B, group g3: keying log

- Started: 2026-10-31T22:02:54Z
- Finished: 2026-10-31T22:22:26Z (CSV written); log written right after
- Output: `keyed/atq41_B_g3.csv`, 262 rows, 140 distinct top-level labels (138 numbered survey caves and sites, plus 2 unnumbered Region VII features with reader-assigned ids `VII/nn1`, `VII/nn2`)

## Read

Before keying I read `SCHEMA.md` and `READER_INSTRUCTIONS.md`. I opened no other file in the repo and nothing else under `keyed/`.

| Article | Title (short) | Printed pages | Read |
|---|---|---|---|
| 2559 | Aronshtam, Region V (Jebel Quruntul, W. Abu Saraj to W. Halq er-Rummana) | 85-95 | all of the text; page images 85-90 and 95 checked |
| 2560 | Eisenberg, Excavation of Cave V/49 (summary) | 97 (unnumbered) | all of the text; page image checked |
| 2566 | Abeles, Region VII (eastern escarpment of Jebel Quruntul) | 109-115 | all of the text; page images 112-114 checked |
| 2569 | Eshel and Zissu, Region VIII (slopes of Triangulation Point 86) | 117-123 | all of the text; page images 117-123 checked |
| 2571 | Eshel and Zissu, Excavation of Cave VIII/9 (summary) | 125 (unnumbered) | all of the text; page image checked |
| 2583 | Weiss, Region IX (southern Jebel Quruntul) | 167-168 | all of the text; page images 167-168 checked |

## Figures and plans

- The English part-2 PDFs have no plans, sections or photographs. Each PDF page is a scan of text, and figures appear only as captions. The plans cited are Region V Plans 1-3, V/49 Plan 1, Region VII Plans 1-2, Region VIII Plans 1-5, VIII/9 Plans 1-2 and Region IX Plan 1. They are presumably printed in Part 1 (Hebrew), which is not in this group. **No value was measured from a plan**, no row has `dims_basis = plan_scaled`, and no direction was taken from a north arrow.
- I rendered page images only to check text that the extraction had broken. The renders are in `/tmp/claude-0/-home-claude/729c536d-b448-586f-923d-45ae3ca7c96d/scratchpad/reader_B_g3/`:
  - 2559: PDF pages 2-12
  - 2560: pages 1-2
  - 2566: pages 2, 5-7
  - 2569: pages 2-8
  - 2571: pages 1-2
  - 2583: pages 2-3
- The page images fixed three cave labels that the extraction had lost: V/48, V/57 and V/64. They also fixed many OCR misreadings of "m", such as "nt" and "nr", and of "c.".
- Several rows use caption text (`figure` column, marked "(caption)"):
  - n_openings for V/55, V/56 and V/67, from captions reading "The opening to Cave ...".
  - The two entrances of VIII/9 and the entrance of VIII/10, from Fig. 1 on p. 125.
  - W1 and W2 at V/49, from Figs. 2-3 on p. 97.
  - Halls F and G of VIII/9, from Figs. 8-9 on p. 125.
- Captions that say which way a photo looks (for example "looking west") were **not** used to set `opening_dirs`.

## Pages

- Three pages carry no printed number:
  - The first page of each regional article: 85, 109, 117 and 167. Each was keyed from the next page's printed number minus one.
  - The two excavation summaries. V/49 was keyed as p. 97, from "English summary, part 2: p. 97" in the Region V references. VIII/9 was keyed as p. 125, from "English summary, part 2: p. 125" in the Region VIII references.
- When a feature is described on pages that are not consecutive, both are given with `;` (for example `88;97`).

## Keying conventions used

- **Grid.**
  - Map refs are copied exactly as printed, including odd forms such as `19005-30/143900-95` (V/1-11) and `19101/14102` (VIII/42).
  - The source never names its grid system. I keyed `OIG` because all values are in the old-grid range (eastings about 190, northings about 140; a new-grid northing would be about 640).
  - Cluster or group map refs (Region V headers, the shared ref of VII/15-16) and refs inherited by sub-features have `position_basis = site_grid`.
  - Some map refs are printed only as "As VIII/n". These were resolved to that entry's ref, and the note says so.
- **Dimensions.**
  - Unlabeled "a x b" sizes: the long side is keyed as `length_m` and the short side as `width_m`. Labeled sizes are keyed as labeled, even where the printed width is larger than the length.
  - "c." values are keyed as plain numbers.
  - Minimums ("at least 10 m", "in excess of 2.5 m") are keyed as the printed number, with a note.
  - A range of widths or heights goes in as `a-b`.
  - Wall thickness is keyed as `width_m`.
  - Entrance widths and heights are on separate `doorway` rows, not on the cave row.
- **Classes.**
  - A numbered survey item printed as "chamber", "passage" or "cavity" is keyed `cave`. Its own word is in `class_as_printed`.
  - Niches and recesses are `other`. A chimney or shaft is `pit`. Kokhim are `burial`. A burial cave is `tomb`.
  - A numbered entry that is itself a group (for example "Three adjacent, natural recesses") is one row. Unlabeled identical sub-features with no individual attributes are one row with the count in the notes. Chambers and rooms get one row each.
- **Construction.**
  - Taken from the entry, or from a cluster header that settles it ("All of the caves are natural", "natural caves and niches").
  - For members of the clusters "Most ... are natural" (V/12-21, V/30-47), it is `unknown` unless the entry itself says otherwise.
- **Numeric columns.** Text such as "width unascertained" is put in the notes. `unknown` is never put in a numeric column.
- **Openings.**
  - `n_openings` counts the entrances the source states. A singular "the entrance" is keyed as 1.
  - "A chimney in the ceiling" is not counted as an opening.
  - `opening_dirs` comes from "faces X", or from the stated position of the entrance ("an entrance in the east", "in its long southern wall", "a northern one ... and a southern one"). Rows that use position are marked medium confidence.
- **Relations.**
  - The sub-feature-to-container link is in `parent_id` and is not repeated as `inside`.
  - Features outside a cave (walls, terraces and niches in front of it) have no parent and use `next_to`.
  - `rel_bearing_deg` is the bearing from the related feature to this row's feature, converted from a printed compass word ("c. 3.3 m north of the opening" gives 0). The note on each row says so.
- **in_window.**
  - `yes` means the source states use, or in-window finds in the feature, in Late Hellenistic, Hasmonean, Herodian or Early Roman times.
  - `no` means the source says there is no evidence of use in antiquity ("not used by man"), or it dates the use only outside the window (IX/14).
  - `unknown` means datable material is mentioned but does not settle the question ("Hellenistic", "Second Temple period", or finds near but not in the feature).
  - Blank means the source gives no dating.

## Not keyed (no attribute beyond class)

- **Region V:**
  - V/13 ("A small cave with a chimney in the ceiling", in a "most are natural" cluster)
  - V/30 ("A small cave.")
  - V/33 (several shallow niches and passages)
  - V/39 (three niches)
  - V/41 ("A large cave.")
  - V/5, V/8, V/31-32, V/36-37, V/42-45, V/47 and V/65: not described in the table.
- **Region VIII:** VIII/22 and VIII/23 ("Not examined, inaccessible").
- **Region VII:** the roughly 15 other surveyed caves not published (n. 1), and the "seven other caves ... around the cliff" (no attributes).
- **Not features:** finds, including the V/50 tabun and the loose coins. Excavation areas and loci (VIII/9 Areas I, II, IV; VII/1 L1, L13, L14) were not keyed as features.

## Unreadable / problems

- No text was unreadable once checked against the page images.
- Possible misprints, keyed as printed and noted on the rows:
  - V/64 passage [1] has width 6.1 m, greater than its length of 3.8 m.
  - VIII/42 has map ref 19101/14102.
  - VIII/13's location reads "As VIII/31".
  - VII/4 is said to be below VII/3 but c. 20 m above the wadi bed, while VII/3 is 12 m above it.
- Ambiguities:
  - V/14 is assigned to the "northern niche" by elimination.
  - VIII/27 is keyed as the cave, with the terrace as VIII/27.b. The site is named after the terrace, and p. 122 is headed "Natural Terrace".
  - V/49 has one pillar per the table ("a wide pillar"), but the summary has plural "stone columns".
  - The dimensions given after the entrances of VIII/38 and VIII/48 are split, or put in the notes, as explained on those rows.
