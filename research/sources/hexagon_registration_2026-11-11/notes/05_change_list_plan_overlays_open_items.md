# Atlas proposals applied as a change list; plan overlays with true scale and north; open items — 11 November 2026

The owner said: go on with the atlas proposals and the items of the "Not done" list of `six-next-steps-results-2026-11-11.md`.

## Result first

| Item | Result | State |
|---|---|---|
| Atlas proposals | A change list of 20 lines for the atlas records, marked "accepted by owner" | Done as a list. **The atlas file itself is not built again** |
| Older notes | A correction line in 18 notes in the Drive; one corrections index for the Project | Done (Project notes: by the index only) |
| Site table | Four more places: Tell es-Samarat, the sugar mill, the ʿAin ez-Zara oasis, the canyon mouth north of it. The table has 29 places | Done |
| Plan overlays | Three overlays on rectified images: Tulul Abu el-ʿAlayiq, Habbasa, Hyrcania | Done |
| CORONA 1967 | Not useful for building-size detail (result of the note of this morning) | Closed with a reason |
| HEXAGON 5 May 1978 | Not done: the project area is at the far east end of the strip | Not done |
| Frames of 1918 and 1953 | Not done | Not done |

## 1. The plan overlays

**New method.** Before, I put a plan on the image with the scale of its bar, one anchor, and a turn that I took from the image. Now the image is rectified first (north up, a fixed number of metres for each pixel). The plan gets the scale of its bar and the north of its arrow. Only one anchor point is free. This is a more strict test.

### Tulul Abu el-ʿAlayiq (Netzer 1975, figure 2)

- Scale from the bar (100 m). North from the arrow of the plan (approximately 19 degrees west of the page top). Anchor: the southern mound.
- **What agrees, with no more adjustment:** the ring of the mound; the two banks of Wadi Qelt, for approximately 700 m; the sunken garden on the south bank; the modern road south of the mound, which the plan has as a broken line.
- Building B of the plan (the early Herodian palace) falls in a dark orchard. I cannot see it.
- **Status: Checked (no change), now with a strict test.**

### Habbasa (Prag and Barnes 1996, figure 9)

- The figure is printed on its side; its caption says that the plan is oriented to the north. Scale from the site grid (50 m between the marks). Anchor: the row of cisterns.
- **The rectified image of 1 December 1974 shows the fort more clearly than before:** a trapezoid enclosure of approximately 80 m by 80 to 90 m with five or six parallel terrace lines in its west part, a row of four or five hollows with light edges (the cisterns) in the middle, and the steep north-east side in shadow.
- The trapezoid of the plan has the same size and the same direction as the trapezoid on the image. The difference of place is approximately 10 m.
- The row of hollows is 45 to 48 m long on the rectified image.
- **Status: Checked (no change), now with a strict test.**

### Hyrcania (Patrich 1989, figure 22)

- Scale from the bar (50 m). The plan has no north arrow.
- Two anchors were necessary: the double pool on the deep hollow, and the summit enclosure on the hilltop (the hilltop is the summit of the elevation model, to 28 m).
- **Result: the plan must be turned approximately 40 degrees against the clock. Thus the top of the plan page is not north.** With this turn, the scale of the bar gives the distance between the two anchors to 7 percent.
- With the turn: the line of cisterns on the south and south-east slope is on the dark pits of the image; the two channels follow the shadow line on the west side of the summit; the line of the bridge goes west from the saddle.
- **Limits.** Two anchors fix the turn, thus the test has less force than the two tests above. My earlier overlays had the plan with north at the top; they were less good, and I did not see it.
- **Status of Hyrcania: Checked (no change). The direction of north on the plan of Patrich: Probable, approximately 40 degrees east of the page top.**

Files: Drive `07 Maps and GIS/Project site layer and HEXAGON chips 2026-11-11/plan_overlays/`.

## 2. The atlas

- File: `atlas_change_list_from_image_work_2026-11-11.csv` in the same GIS folder. 20 lines: record, place, field, new value, evidence note, decision.
- The owner's "go on" is recorded as the decision in each line.
- **Two limits.**
  1. The atlas is a PDF that a build script makes from the project data. The data are not in this session. Thus I did not build the atlas again. The session that has the data can apply the list.
  2. The record numbers are from the text of the PDF, which has two columns. The column `record_id_checked` says "no" in each line. For Deir Hajla I could not decide between sit0022 and sit0039.
- The most important lines: a map point for Deir Hajla; the new map point for Tall Barakat with the note on the conflict; the positions for Hyrcania, Mar Saba, Nebi Musa, Khirbet Mazin, Habbasa and Tell er-Rameh.

## 3. The older notes

- Drive: 18 notes in `08 Working files` have a correction line under the title. It sends the reader to the site table and to the index.
- Project: `hexagon-1974-corrections-index-2026-11-11.md` lists, for each older note, what is replaced and what is correct now. The older Project notes are not changed.

## 4. The site table (29 places now)

| New place | Position | Status | Source of the position |
|---|---|---|---|
| Tell es-Samarat | 31.8652 N, 35.4404 E | Possible on the image of 1974; Checked on the frames of 1918 | 210 degrees and 740 m from Tell es-Sultan (Survey sheet) |
| Sugar mill (Tawahin es-Sukkar) | 31.8723 N, 35.4388 E | The same | 285 degrees and 535 m from Tell es-Sultan |
| ʿAin ez-Zara oasis (Callirrhoe) | 31.5968 N, 35.5637 E | Probable | East-shore window of tile F018b; centre of the field area; error approximately 150 m |
| Canyon mouth north of the oasis | 31.6200 N, 35.5655 E | Probable for Wadi Zarqa Maʿin | The same window |

## 5. The other dates

- **CORONA, 26 September 1967 (strip DF042).** The note of this morning has the result: only tile d has project ground (the north end of the Dead Sea), and the land is too light and too grainy for building-size detail. Thus a registration gives no use. Strips DF040 and DF041 are not opened (`.tgz` files).
- **HEXAGON, 5 May 1978 (strips F006, F007).** I opened the preview of strip F007, tile d. The Jordan valley and the Dead Sea are at the far east end of the strip. The ground is strongly compressed from west to east there, and cloud or sun glint covers the Dead Sea and its west shore. One affine transform is not sufficient at the end of a panoramic strip. **Not done.** It needs the camera model, or a fit in small parts.
- **Frames of 1918 and 1953.** Not done. The registration method needs relief; most of these frames are of the plain.

## Not done

- A new build of the atlas with the change list.
- The Project copies of the older notes (the index replaces this).
- HEXAGON 1978, the frames of 1918 and 1953, CORONA strips DF040 and DF041.
- The plans of Wright 1961 (Hyrcania) and of Barakat on rectified images.
- The cut script `cut_dec1974_by_position_2026-11-11.sh` is not run (the owner runs it).
