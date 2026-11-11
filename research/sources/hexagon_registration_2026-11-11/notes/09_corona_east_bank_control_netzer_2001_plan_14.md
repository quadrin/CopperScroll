# CORONA 1967 with control east of the Jordan; plans of Netzer 2001 on the image of 1978; site table updated — 11 November 2026

## Result first

1. **There is no Kafrein dam and no reservoir on 26 September 1967.** The valley floor is open. The dam is thus later than this date.
2. **CORONA now has control east of the Jordan.** 136 blocks agree with the HEXAGON image of 25 June 1974; the error is 17 m (rms).
3. **Correction.** I estimated that the first CORONA transform was wrong by 100 to 200 m on the east bank. It was wrong by approximately 330 m at Kafrein.
4. **Correction.** I said that the final report of Netzer is not in the Drive. The portfolio of plans of Netzer 2001 is in the Drive, as photographs of 21 October.
5. **The two pools of the Hasmonean Pools Complex at Jericho are Checked** on the image of 5 May 1978 with plan 14 of Netzer 2001.
6. **The site table has 33 places now** (4 new, 4 changed). The atlas change list has 6 new lines, not decided.

## 1. CORONA, 26 September 1967: east bank

- Method: the same as for the west side. Blocks of the CORONA window were compared with the rectified HEXAGON image of 25 June 1974 (tile A015c).
- Transform for the east window (EPSG:2039; E, N = [x, y, 1] × A): `[[2.042853, 0.414548], [0.182893, −2.053031], [203924.97, 639253.95]]`. Scale 2.08 by 2.06 m for each pixel. Valid for tile x 26900 to 29700, y 4300 to 7600.
- The scale on the west side is 2.17 by 2.12 m. One transform for the full tile is not sufficient, because the film is panoramic.
- For Shunat Nimrin there is still no control. The two transforms give the road junction at 31.9003 N, 35.6220 E, with an error of approximately 200 m.

| Place | 26 September 1967 | 25 June 1974 | Status |
|---|---|---|---|
| Kafrein dam site | Open valley with the wadi line and a track; an oval enclosure of approximately 100 m on the valley floor, south of the later dam line | Dam and full reservoir | Checked (no dam in 1967) |
| Plateau Fort | A square outline of approximately 50 m | The same square | Checked (two dates) |
| Tell er-Rameh | The oval field boundary, the tree line and the straight road are the same; few houses | More houses | Checked by position |
| Tell Iktanu | The highway is there. The long hill north-west of it is there. I see no military works | Military works north-east of the hill and beside the highway | Seen |
| Habbasa, Tell el-Hammam | Dark and light areas only | — | No result at this scale |
| Nebi Musa (west side) | One dark spot of approximately 60 m, approximately 90 m north of the position of 1974 (the west transform is extended to the south here) | Compound | Position only |

- The area south of the highway at Tell Iktanu that is dark in 1974 is light in 1967. Thus it is probably plants of one season, not a hill. This agrees with my correction of this morning.
- I cannot say what the oval enclosure at the dam site is.

## 2. Jericho: plans of Netzer 2001

The portfolio is in Drive `08 Working files/Unsorted source scans/NLI 10 26/Netzer 2001 Jericho Palaces plans portfolio (NLI photos 21 Oct)`: 24 photographs. I read 18 of them. The captions that I read:

| Plan | Caption |
|---|---|
| 11 | Area AA (Buried Palace and Fortified Palace) |
| 12 | Area AC |
| 14 | Main part of Area AB (Pools Complex) |
| 15, 23 | Western Garden and its surroundings in Area AB |
| 26 | Area AE (Twin Palaces) |
| 35 | Northern Wing of Herod's Third Palace |

There is no general plan of the full site in the portfolio. The plans have a site grid of 10 m squares on their borders.

### Plan 14 on the image of 5 May 1978

- Test: scale from the bar of the plan (10 m), one anchor (the wall between the two pools).
- With north from the arrow of the plan, the north pool agrees and the south pool is 4 m off.
- With a turn of 13 degrees, the two pools, the halls east of them and the rooms west of them agree. The arrow of the plan is along the site grid; the buildings and the grid are approximately 13 degrees east of north. The plan of 1975 gave 12.6 degrees in the free fit. The two values agree.
- Each pool is approximately 18 by 14 m on the image.

| Excavated area of 1978 (my list of the last note) | Identification | Status |
|---|---|---|
| The two basins | The two pools of the Pools Complex (plan 14) | Checked |
| Rooms east of the basins | The row of long halls on the east side of plan 14 | Checked by the same overlay |
| Rooms west of the basins | The building on the west side of plan 14 | Checked by the same overlay |
| Large area between the pools and the northern wing (approximately 75 by 68 m with walls) | The site grid puts the Twin Palaces (plan 26) at its north-west part. The other parts are probably the next areas to the east and south | Probable |
| Rooms on the mound west of the pools | Area AA by plan 11 (not tested) | Possible |
| Small area north-east of the northern wing | Not identified | Seen |

- **Limit:** the photographs of the plans are oblique and have a fold. I used no correction of the perspective. For plan 26 I used the grid numbers only; this has an error of 20 to 40 m. A flat scan is necessary for a full overlay.
- Do not share the photographs of the plans as they are: parts of a person are on them.

## 3. Site table and change list

Site table (`copper_scroll_sites_2026-11-11`, three formats), 33 places:

- Changed: Nebi Musa (Checked at two dates; 65 by 77 m; no plan test), Deir Hajla (three dates), Plateau Fort (two dates), Kafrein dam (built after 26 September 1967).
- New: Jericho Pools Complex (31.8541 N, 35.4345 E, Checked); northern wing of the third palace (31.8522 N, 35.4367 E, Checked); excavated area south of the pools (Probable); Shunat Nimrin road junction (Probable, error 200 m).

Atlas change list: 6 new lines with the decision "not decided". The record numbers are not found; I did not look for them.

## Not done

- Flat scans of the plans of Netzer 2001, and overlays of plans 11, 26 and 35.
- The 6 other photographs of the portfolio (covers, label, second photographs).
- Control for CORONA at Shunat Nimrin; the place of Tell Nimrin.
- The south hill of Tell Iktanu; the frames of 1953.
- The public repository is not changed by this work.

## Files

Drive `07 Maps and GIS/Project site layer and HEXAGON chips 2026-11-11`:
- `copper_scroll_sites_2026-11-11.csv`, `.geojson`, `.kml` (replaced)
- `atlas_change_list_from_image_work_2026-11-11.csv` (26 lines)
- `corona_1967_df041d_transform_2026-11-11.json` (replaced; west and east transforms)
- `date_pairs/corona_1967_sep_hexagon_1974_jun_kafrein_dam_site.jpg`, `…_hammam_habbasa_plateau_fort.jpg`, `…_tell_er_rameh.jpg`, `…_tell_iktanu.jpg`, `corona_1967_sep_hexagon_1974_dec_nebi_musa.jpg`
- `plan_overlays/F007c_may78_jericho_pools_complex_netzer_2001_plan14_overlay_2026-11-11.jpg` (has a published plan in it: not for the public repository)
- `chips/F007c_may78_jericho_pools_complex_x4.jpg`
