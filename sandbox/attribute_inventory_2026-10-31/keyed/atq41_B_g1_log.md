# atq41, reader B, group g1: keying log

- Reader: B. Source: atq41 (ʿAtiqot 41, part 2, English, 2002).
- Started: 2026-10-31T22:02:54Z. Finished: 2026-10-31T22:21Z (UTC).
- Output: `keyed/atq41_B_g1.csv`, with 217 rows covering 68 distinct survey labels.

## Files read
- `SCHEMA.md` and `READER_INSTRUCTIONS.md`.
- All three g1 text files were read in full:
  - 2544, Region I (Peleg and Hameiri). Printed pp. 1-4. The text runs to p. 3; p. 4 holds the notes, references and captions.
  - 2546, Region II (Hirschfeld and Riklin). Printed pp. 5-19. The site entries are on pp. 5-16; pp. 16-19 hold the conclusions, notes, references and captions.
  - 2550, Region III (Barshad and Shaked). Printed pp. 35-41. The entries are on pp. 35-40; p. 41 holds the captions.
- Printed page numbers come from the running heads. The first page of each article has no number, so I took it from the sequence: 1, 5 and 35. Region II p. 8 has a head without a number; I confirmed it on the page image.

## Pages rendered (100 dpi, kept in my scratch dir only)
- I rendered every page of the three PDFs. I viewed these: 2544 PDF pp. 2-5; 2546 PDF pp. 3-12 (printed 6-15); 2550 PDF pp. 2, 3, 4, 6 (printed 35, 36, 37, 39). I used them to check the OCR on numbers, grid references and Roman-numeral labels. The OCR prints "1/1" and "11/2" where the page has I/1 and II/2.
- **No plans or figures exist in these PDFs.** The English part 2 has scanned text pages and caption lists only. Plans 1-8 (Region II), Plan 1 (Region I) and Plans 1-2 (Region III) are in Part 1, which I did not have. So no value is `plan_scaled`, the `figure` column is blank throughout, and every dimension is `text`.

## Conventions used
- **Grid system.** Map references such as `18900/14590` and `1809/1448` are keyed as `OIG` and copied exactly.
  - `feature_grid` means the reference belongs to the feature itself.
  - `site_grid` means a shared or group reference (I/1-2, I/6-7, I/15-19, II/11, II/20-31, II/33-41, II/52-60, II/68, III/8-11, III/12-13), or a sub-feature that carries its parent's reference.
  - `text_only` covers I/12, I/13, III/2 and III/5, which have no reference.
- **Length and width.** For "a x b" I put the longer number in `length_m` and the shorter in `width_m`. Max. heights go in `height_m`, with a note.
- **Cave entrances.** Entrance width and height are not keyed as separate rows; they go in the cave's notes. The exception is II/51.b, a doorway built into a wall.
- **n_openings.** Keyed only where the text states the count or refers to a single entrance or opening. Facing directions are keyed only where the text says "faces": I/14 S, II/4 W, II/5 N, II/18 NE, II/32 S. "Southwestern opening" (II/2) describes where the opening is, not which way it faces, so it is not keyed as a direction.
- **parent_id.** Used only for physical containment. Features outside a cave (forecourts, terraces, niches nearby, walls in front) have no parent and are linked by `relations`.
- **Bearings.** `rel_bearing_deg` is the printed compass word turned into degrees, for example "100 m west of I/11" gives 270. It gives the bearing *from the related feature to this row's feature*.
- **Suffixes.** `.a`, `.b`, ... follow the order in which the text mentions sub-features. Groups that have no single label of their own get group rows: II/20-31, II/33-41, II/52-60, and III/8-11.a for the approach path.
- **in_window.**
  - `yes`: Hellenistic, Early Roman, Hasmonean or Second Temple finds or use is reported at the feature.
  - `no`: every dated material reported falls outside the window, or the text excludes the window outright (I/14).
  - `unknown`: there are no finds, only non-diagnostic finds, or the dating is ambiguous.
  - Blank: the source says nothing about dating for that sub-feature.
- **Construction for Region II caves.** Most are keyed `natural` because the region intro (p. 6) calls all 68 surveyed caves "karstic"; each such row says so in its notes. Caves with hewn elements are keyed `mixed`.

## Features not keyed (no attribute beyond class)
I/17-19 (not described individually), the unnumbered niches around I/1-2, II/62-63, II/65 (only "large"), III/13 (Cave of the Warrior, which the text refers to Schick 1998), and el-Makkuk Cave (mentioned in the history of research only).

## Problems and conflicts noted in rows
- Region I intro calls Shuqfan el-ʿAzvat "I/5", but the text describes it as I/14.
- II/2: its entry says there were no traces of human activity, yet the Conclusions list II/2 ("northern bank") among the caves with Early Roman finds. This probably means II/1, which is on the northern bank and has Early Roman sherds.
- II/7 is printed as "north of Cave II/9", while II/9 is described as north of II/6-8.
- II/19's grid is printed `19099/14501`, probably a misprint for 18099. It is keyed as printed.
- II/5 "Cell II/4 to its north" is ambiguous; the map references put II/5 north of II/4.
- III/11 uses its locus labels inconsistently. The description has L5 as the plastered depression and L2 as the bell-shaped cistern, but the excavation text calls the cleaned cistern L5.
- III/14 is called "westernmost", but its easting is larger than that of III/1, which is called "easternmost".
- I/13 "c. 200 m above" I/12 is keyed as printed.
