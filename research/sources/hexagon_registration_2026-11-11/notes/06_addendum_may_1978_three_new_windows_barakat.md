# Atlas addendum, the image of 5 May 1978, three new windows, two more plan overlays — 11 November 2026

The owner ran the cut script and said: do the items of the "Not done" list of `atlas-change-list-plan-overlays-true-scale-north-open-items-2026-11-11.md`.

## Result first

| Item | Result | State |
|---|---|---|
| A new build of the atlas | **Not possible in this session.** I made an addendum to the atlas as a PDF (11 pages) | Done as an addendum |
| HEXAGON 5 May 1978 | **Tile c of strip F007 is registered** (165 blocks, error 24 m at preview scale). It shows Jericho without cloud. A cut script for four full-size windows is ready | Done to the cut script; the owner runs it |
| CORONA strips DF040 and DF041 | The same script makes overviews of the two strips | The owner runs it |
| Frames of 1918 and 1953 | Not done | Not done |
| Plan of Barakat on a rectified image | Done: the lower enclosure agrees; the citadel line does not agree fully | Done |
| Plan of Wright 1961 | Not done: I did not find the plan image in this session | Not done |
| The three new windows | Read: Nebi Musa, Tell Iktanu, the Umm Ḥadhar hill | Done |

## 1. The three new windows (1 December 1974, rectified, north up, 0.5 m for each pixel)

### Nebi Musa. Status: Checked by position and setting (was Probable)

- One walled compound, almost square, approximately 65 m from west to east and 85 m from north to south (the shadows are in this size). It has a court in the middle and rows of rooms along the sides.
- **Large fields of fine dots are on the north-east and south-east sides.** These are graves by form. A large cemetery round the shrine is the known setting of Nebi Musa.
- A road passes approximately 120 m west of the compound, and a track goes from it to the compound.
- The compound is approximately 30 m from the place that the transform gave. This is a test of the transform also.
- No plan test: I have no plan of the compound.

### Tell Iktanu. Status: Checked by position (was Probable); a fort on the top is Possible

- The hill is long: approximately 400 m from south-west to north-east and 120 to 150 m wide. Its north-west side is a steep scarp with a line of trees or bushes at its foot.
- **On the top, near the middle, is one rectangular outline of approximately 45 m by 30 m** with a short straight line beside it. K. Prag writes of the ruins of a fort on the top of the north hill. The outline can be this fort. Not confirmed: I have no plan.
- The highway is 100 to 150 m south-east of the hill. A dark field (the "dark oval hill" of the June image) is on the other side of the highway; on this image it is a flat field with scattered trees, not a hill. **Thus the "dark oval hill" is probably not a second tell.** The south part of the double site is not identified.
- An orchard in a narrow strip is at the north-west foot. Small pits are on the south slope.

### The Umm Ḥadhar hill. Status: hill Probable (no change); building not identified

- The window shows a promontory between two wadi beds, approximately 300 m by 550 m, with curved lines at its north end.
- **I see no outline of a building of 40 m by 30 m.**
- Two dark angular marks of 10 to 12 m, 35 m apart, are on the flat ground approximately 110 to 130 m west-south-west of the window centre, with many small pits round them. By their sharp form they are modern (shelters or pits). They are not the building of the excavators.
- The excavation of Umm Ḥadhar is later than 1974. Thus a low mound of rubble is the form to look for, and the image does not separate it from the natural ground.

## 2. The atlas addendum

- **Why no new build.** The build scripts of the atlas read the source checklist PDF, a register file and image files from a work folder of an earlier session. These files are not in the Drive. The maps of the atlas also need a map service that this session cannot reach.
- **What I made:** `Copper Scroll – Regional atlas – Addendum 1 (image work of 10–11 November 2026).pdf`, 11 pages, landscape A4:
  1. what the addendum is, and the caution on the record numbers;
  2. the 20 changes to the atlas records;
  3. the site table (29 places);
  4. seven figures (the plan overlays, the Barakat date pair, Tell Iktanu, Nebi Musa).
- It is in the Drive beside the atlas (`08 Working files/Regional atlas redesign – 2026-11-10`) and in the GIS folder.

## 3. HEXAGON, 5 May 1978

- **Correction.** I said that the project area is at the far end of the strip and that one transform is not sufficient. That was true for tile d only. **Tile c has Jericho, the plain and the west shore, and one affine transform fits it well.**
- Method: four common points between tile d and the image of 1974 gave a first transform; then the registration to the elevation model on the preview of tile c (reduced 10 times).
- Result for tile c (tile x from 23000 to 37289): 165 blocks, error 24 m, scales 0.82 and 0.81 m for each pixel. Two different sun directions gave the same transform.
- A check by eye on the preview: the predicted points of Tulul Abu el-ʿAlayiq and Birket Musa fall on the south bank of Wadi Qelt and on a square field plot. Tell es-Sultan falls at the north-west edge of the oasis.
- **Cloud:** Jericho and Wadi Qelt are clear. The plain south-east of Jericho has small clouds. The Dead Sea and its shore have thin cloud. Tile d (the Jordan and the east bank) is clear near the river, but the Kafrein forts are outside the frame.
- **The cut script** `cut_may1978_and_corona_overviews_2026-11-11.sh` cuts four full-size windows of tile c: the Jericho palaces with Quruntul, Nebi Musa, Deir Hajla, Qumran with ʿEin Feshkha. It also makes overviews of CORONA strips DF040 and DF041. I did not test it. It needs approximately 6 GB in `~/Downloads`.

## 4. Barakat (Prag and Barnes 1996, figure 13) on the rectified image

- Scale from the site grid. North from the arrow of the figure (the figure is printed on its side). Anchor: the lower enclosure.
- **The lower enclosure agrees:** on the image it is a four-sided outline of approximately 45 m by 50 m with two or three inner walls; the plan has the same form and size.
- **The citadel does not agree fully.** On the plan, the structures of the citadel are in a line to the west of the enclosure. On the image, the high narrow ridge is to the north-west and north of the enclosure. The difference of direction is approximately 15 to 20 degrees.
- Possible causes: the site grid of the survey is not exactly in line with true north; or the citadel walls are on the south slope below the crest, where I see no walls at this scale.
- **Status of Barakat: Checked by form for the lower enclosure (no change). The citadel on the image: Probable for the ridge.**

## Not done

- A new build of the atlas (the addendum replaces it for now).
- The plan of Wright 1961 on a rectified image.
- The frames of 1918 and 1953. The frames of 1953 are not in the Drive.
- The four windows of May 1978 and the CORONA overviews are not read (the script must run first).
- The south part of Tell Iktanu; the building of Umm Ḥadhar.

## Files

- Drive `08 Working files/Regional atlas redesign – 2026-11-10` and the GIS folder: the addendum PDF.
- Drive `07 Maps and GIS/Project site layer and HEXAGON chips 2026-11-11`:
  - `plan_overlays/A017e_dec74_barakat_prag_barnes_fig13_overlay_rectified_2026-11-11.jpg`
  - `chips/F017b_dec74_nebi_musa_rectified_0.5m.jpg`, `chips/A017e_dec74_tell_iktanu_rectified_0.5m.jpg`, `chips/A017e_dec74_umm_hadhar_hill_rectified_0.5m.jpg`
  - the site table (status of Nebi Musa and Tell Iktanu changed)
  - `hexagon_1974_transforms_2026-11-11.json` (the transform of 1978 added)
- Drive `08 Working files/hexagon windows 2026-11-10`: `cut_may1978_and_corona_overviews_2026-11-11.sh`
