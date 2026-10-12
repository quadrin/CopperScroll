# Part F notes (IAA Reports nos. 2–6 and 8–78)

Session of 12 October 2026 UTC (11 October in Los Angeles). Exploratory. No identification claim; no registered result changes.

## What was seen

- Arrival check (`arrival.py check`): manifest ok (29 files), run before any fetch.
- Series pages (gallery): titles, authors and the publisher's descriptions for all 84 items. The descriptions were parsed by script. By eye I saw the first item's description (no. 78, Paneas V) in a text dump, and the series list of numbers, titles and authors.
- Landing pages: for every item the parsed title, portal date, full-text size, number of chapter files and the first 80 characters of the keywords were printed once.
- Candidate descriptions read by eye (up to 1,500 characters each; only no. 69 is longer), to place them by zone: nos. 3, 12, 19, 39, 52, 63, 64, 66/1, 66/2, 66/3, 67, 69. None gives a map reference.
- Non-candidate descriptions were not read by eye. They were screened by script. Where there were hits I looked only at the matched term in context (nos. 30, 43, 51/1, 51/2, all incidental).
- Chapter titles: screened by script for all volumes; only the hits were printed (nos. 3, 12, 39, 63, 66/1, 66/2, all candidates already).
- No PDF, chapter file, figure or thumbnail was opened.

## Deviations and choices (exploratory)

- **D1. Held unit no. 5: more than the first line was seen.** Before deciding the hold I printed, in one step, the first part of the description (cut at "Cave No."), the keywords and the chapter list. The keywords were "Chalcolithic–EB I burial, Judean desert, burial practices, ancient textiles, basketry". The 25 chapter titles included "2. The Discovery of the Cave and Its Excavation", "20. Radiocarbon Dating of Finds", "22. Summary and Conclusions" and "Appendix: Hasmonean Coins Found in the Cave of the Warrior". I then printed the full first sentence (in `held.csv`) and nothing more. The rest of the description was not displayed. These titles are now exposed to this lane. They give no location beyond "Jericho area" and no opening direction. Nothing was coded from them.
- **C1. Hold for no. 5 decided on the first line.** The first line places the cave in "the survey of the caves in the Jericho area". The exact wadi is not named there. I held it as a Jericho-escarpment cave (plan §7) and did not look further to settle the wadi. If the integrator finds that its cave lies outside the held area, it becomes the only T1 unit (position 1).
- **C2. Unit ids.** `IAAR<no>-<slug>`, with a part written `p` (`IAAR66p1-…`), so ids have no slash. Slugs are fixed in `scripts/build_part_f.py`.
- **C3. One unit per volume.** No candidate volume reports separate sites in separate chapters. The Western Wall Plaza (nos. 63, 64, 67) and Giv‘ati Parking Lot (nos. 52, 66/1–66/3) volumes are separate monographs on the same excavation. Each is kept as its own unit, because each is a separate PDF and may report different features. A later merge must not count one feature twice.
- **C4. Full-text PDF requested, not chapters.** The plan reads a unit whole. Chapter PDFs are listed in `data/files.csv` if the owner prefers smaller downloads.
- **C5. A3 variants** (Hagedud, Anathoth, Land of Benjamin, Kh. el-Burj) were added to the title screen as in phase 3. None matched.
- **C6. Portal year.** `year_portal` is the portal's publication date. For some older volumes it is the upload date, not the print year (for example no. 72 shows 2024). Print years are not checked here.
- **C7. Abstract hits judged incidental** (no title term): no. 30 "jordan river" (Sea of Galilee outlet), no. 43 "ramot" (Ramot Menashe), nos. 51/1 and 51/2 "jerusalem" (the Latin Kingdom of Jerusalem). Multi-site and thematic volumes (nos. 4, 6, 9, 14, 20, 26, 46, 47) are outside the region by title and keywords; the reason is in `screen.csv`.
- **C8. Efrata (no. 12)** is placed in Z4 by the gazetteer term "efrata". Its description says "a hill on the Hebron–Jerusalem road". The exact position is not checked.

## Not read

All 12 candidates: `not read (waiting for download approval)`, tiers and positions as in `pdfs_needed.csv`. Held: no. 5.

## Figures to archive later

None met. No figure, plate or plan was opened in this pass.

## Proposed changes for the integrator

1. Ask the owner to approve the 12 downloads in `pdfs_needed.csv` (467.5 MB), saved in Chrome to `~/Downloads/IAA portal volumes/phase4/`, then read on the Mac with `pdftotext`. The older volumes (no. 3 of 1998, no. 12 of 2001, no. 19 of 2003) may be scans without a text layer, as IAA Reports 1 and 7 were. They may need OCR.
2. Decide whether the Cave of the Warrior (no. 5) lies in the held Jericho escarpment, and record it in the arrival procedure if it does.
3. `research/sources/mining_targets_2026-10-11.md`, row A2 says IAA Reports item pages return 403 to scripts. On 12 October UTC all 82 landing pages returned 200 to curl, using a trailing slash.
4. At the merge, compare the Jerusalem volumes (nos. 52, 63, 64, 66/1–3, 67) with the HA-ESI reports already coded for the same excavations (Western Wall Plaza; Giv‘ati Parking Lot), so that no feature is counted twice.
