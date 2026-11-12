# Entry places: the four open items of the first comparison are done

Date: 2026-11-11. This note continues the first comparison of the site table with the entry places (`tables/phase3_places.csv`, `research/regional/peraea/gazetteer.csv`).

## Result first

1. **Gazetteer positions.** The three wrong points are corrected in a separate table in the repository (pull request 109, not merged). The frozen files are not changed. The correction changes no entry result by more than 0.0006.
2. **ʿAin Duk** is found on two dates, 415 m from the entry-table point. Status: Probable. **Tell el-Qos** is in the built-up area of Jericho and no mound can be read. Status: Not confirmed.
3. **Jerusalem** is on the image of 1 December 1974 (tile F017b). I registered a Jerusalem window. Of the 15 Jerusalem places, 11 are at a landmark or valley that the image shows; 2 are structures that I cannot identify; 1 is a large area; 1 has no coordinate. Tell el-Ful, north of the city, agrees also.
4. **EAMENA.** 15 entry places are inside the area of the EAMENA table. 14 of them have a record within 500 m. For the three corrected sites east of the Jordan, EAMENA has a record 30 to 70 m from the image position. This is a second source for each correction.

## 1. The three gazetteer positions (pull request 109)

PLAN_v3 says that no input is changed after a result, and a test checks the SHA-256 of `gazetteer.csv` and `build_gazetteer.py`. Thus I did not change these files. I added a correction table and an exploratory run.

| Site | Frozen point | Corrected point | Moved | At the frozen point | Second source |
|---|---|---|---|---|---|
| tall_al_kafrayn | 31.84972, 35.67861 | 31.8507, 35.6526 | 2,460 m | East end of the Kafrein dam | EAMENA-0186072, 30 m |
| tell_nimrin | 31.90900, 35.63800 | 31.9010, 35.6251 | 1,508 m | A different mound: EAMENA-0184755 (name BLEIBEL) is 54 m from it | EAMENA-0184259, 40 m |
| kh_al_habbasa | 31.84457, 35.67959 | 31.8396, 35.6793 | 552 m | No structure on the two images of 1974 | EAMENA-0185957, 70 m |

- The three sites have no `w2b_place_id`. Only the sensitivity variant S2_broad uses them.
- The new script runs S2_broad two times. With the frozen points it gives the same numbers as `results_v3.json` (difference 0).
- With the corrected points: latent P(Koḥlit at transjordan) 0.0143 → 0.0141; P(entry 60 at transjordan) 0.0086 → 0.0082; largest change of one entry 0.0005 (total variation).
- The repository has 16 tests now (12 old, 4 new). All pass.

New finding: the frozen point of tell_nimrin is not a random error. It is the position of a different mound that EAMENA names BLEIBEL (Tell Bleibil).

## 2. ʿAin Duk and Tell el-Qos

**ʿAin Duk (entries 1, 17, 29, 31).** The place is north of the film edge of the registered frames. It is on the adjacent frames: F016b (1 December 1974) and F006c (5 May 1978). I linked each adjacent frame to its registered frame through the overlap (51 blocks, 8 px; 11 blocks, 10 px).

| Point | Position | On the images |
|---|---|---|
| Entry table (PEF sheet XVIII, georeferenced) | 31.8976, 35.4177 | Bare slope above the scarp. No trees, no plots, no path end. |
| Image: head of the irrigated plots | 31.8963, 35.4218 | Trees and a small structure in 1974; the head of a walled plot in 1978. The plots continue from here down the valley. |
| EAMENA-0117143 (ʿAin Duq) | 31.89629, 35.42181 | 3 m from the image point of 1974 and 13 m from that of 1978 |

- The two dates give the same ground position to 15 m. The entry-table point is 415 m west-north-west of it. Its stated precision is approximately 300 m.
- Status: **Probable**. The image shows where the watered land starts. It does not show water.
- I did not change `phase3_places.csv`. The entries that use ʿAin Duk refer to an area of springs, and 415 m does not change an entry assessment. You must decide if the point is to be moved.

**Tell el-Qos (entry 30).** The place is on the registered frames F017b (1974) and F007c (1978).

- Entry-table point (31.8551, 35.4656): an orchard with houses on the two dates.
- EAMENA-0117188 (31.85377, 35.4648), 165 m to the south: open light ground approximately 60 m across on the north bank of Wadi Qelt in 1974. In 1978, houses are on a part of it.
- No mound shape can be read between the houses and the trees. Status: **Not confirmed**. A height model with a smaller cell, or a field check, is necessary.

## 3. The Jerusalem entry places

**Registration.** Jerusalem is at the west end of tile F017b, 20 km from the area of the old transform. The old transform is 1.2 km wrong there. Thus I made a new one:

- Window x 0, y 13500, 8000 by 9000 pixels, registered to the elevation model: 141 blocks, 30 m; with a height term, 18 m.
- The blocks are in the hills east of the city. In the city the result was 48 m east of the Dome of the Rock. I moved the transform 48 m to put the Dome of the Rock right (one control point).
- Test: nine other landmarks with published coordinates are then at their places on the image, to approximately 30 m (Damascus, Herod's, Lions', Dung, Zion and Jaffa gates, al-Aqsa, Holy Sepulchre, Church of All Nations).

**Comparison.** The distance is from the entry-table point to the landmark on the image.

| Place | Entries point to | On the image | Distance | Result |
|---|---|---|---|---|
| jer_temple | Temple enclosure | Platform of the Dome of the Rock | approximately 20 m | Agrees |
| jer_east_gate | Golden Gate | Gate building on the east wall | 3 m | Agrees |
| jer_se_corner | SE corner (Solomon's Stables) | Corner of the enclosure wall | 58 m | Agrees (the point is the inner hall, not the corner) |
| jer_south_wall | Huldah Gates | South wall below al-Aqsa | 6 m | Agrees |
| jer_gethsemane | Gethsemane | Church of All Nations and garden | 31 m | Agrees |
| jer_bethesda | Pools of Bethesda | Compound of St Anne inside Lions' Gate | approximately 50 m | Agrees; the pools are not visible |
| jer_kidron_mon | Kidron monuments | East side of the valley floor below the road | – | Position is in the valley; I cannot identify the monuments one by one |
| jer_kidron_east | Silwan necropolis | North end of Silwan village on the east slope | – | Agrees with the slope |
| jer_siloam | Siloam (area) | Gardens in the valley floor, approximately 100 m east of the pool position | approximately 100 m | Inside the stated area (300 m) |
| jer_bir_ayyub | Bir Ayyub | Buildings beside the road, immediately south of the Kidron–Hinnom junction | – | Agrees with the junction |
| jer_tyropoeon | Tyropoeon valley | West of the Western Wall plaza | – | Agrees with the valley line |
| jer_tombs_kings | Tombs of the Kings | Plot at a road fork with a compound | – | Probable; I cannot see the sunk court |
| jer_baqa | el-Baqʿa (area 700 m) | Built-up area | – | No test possible |
| jer_shaveh | Valley of Shaveh | – | – | No coordinate in the table |
| ramat_rahel | Ramat Raḥel | Point is in the kibbutz; the excavated area is west of it | 136 m | Agrees at the stated 100 m level |
| tell_el_ful | Tell el-Ful | Rectangular structure on the terraced summit | 8 m | Agrees |

No Jerusalem entry place is wrong at the scale of the image. The one position that is weak is Ramat Raḥel (136 m): the Pleiades point is in the modern settlement, not on the excavation.

## 4. EAMENA heritage places and the entry places

The EAMENA table has 577 places between 31.565° and 31.929° N and 35.300° and 35.712° E. The Jerusalem places and the three northern places are outside this area.

| Entry place | Nearest EAMENA record | Distance | Records within 500 m / 1 km |
|---|---|---|---|
| mar_saba | EAMENA-0186218 | 7 m | 11 / 15 |
| jericho_palaces | EAMENA-0186925 (Tell Abu el-ʿAlayiq South) | 18 m | 8 / 23 |
| hyrcania | EAMENA-0117997 | 29 m | 3 / 9 |
| doq | EAMENA-0117191 (Jebel Quruntul) | 41 m | 15 / 23 |
| kh_qumran | EAMENA-0117926 | 58 m | 6 / 22 |
| tell_es_sultan | EAMENA-0231128 | 70 m | 11 / 28 |
| choziba | EAMENA-0117125 | 93 m | 7 / 7 |
| tell_el_qos | EAMENA-0135584 (field system); Tell el-Qos record at 166 m | 103 m | 4 / 11 |
| wadi_qumran | EAMENA-0117923 | 119 m | 6 / 18 |
| jericho_area | EAMENA-0187427 | 131 m | 4 / 10 |
| buqeia | EAMENA-0117994 | 289 m | 3 / 10 |
| nuweimeh | EAMENA-0117209 | 373 m | 2 / 7 |
| ain_duk | EAMENA-0117143 | 415 m | 3 / 9 |
| asla | EAMENA-0186605 | 489 m | 1 / 22 |
| kuteif | EAMENA-0186610 (road) | 1,822 m | 0 / 0 |

- The six places that the first comparison checked on images are also 7 to 70 m from an EAMENA record.
- Wadi Kuteif has no EAMENA record within 1 km. It is the one entry place in the area with no record near it.
- East of the Jordan, 12 of the 25 gazetteer sites are inside the area. Machaerus (10 m) and Tell er-Rameh (7 m) agree with EAMENA. The frozen points of tell_nimrin, tall_al_kafrayn and kh_al_habbasa are 54 m, 631 m and 520 m from the nearest record, and none of these records is the site itself (see item 1).
- Callirrhoe: the nearest record is 6.7 km away. The EAMENA table has no record for the gazetteer point of Callirrhoe.

## Site table

Four new lines (48 places now): ʿAin Duk, head of the spring gardens (Probable); Tell el-Qos, published point (Not confirmed); Dome of the Rock, control for the Jerusalem window (Checked); Tell el-Ful, structure on the summit (Checked).

## Not done

- Pull request 109 is not merged. Write "merge pull request 109" if you agree.
- `phase3_places.csv` is not changed (ʿAin Duk 415 m, Ramat Raḥel 136 m, Tell el-Qos 165 m). These are your decisions.
- Jerusalem is checked on one date only. The image of 5 May 1978 (F007c) also shows the city; I looked at it but did not register it.
- The Kidron monuments and the Tombs of the Kings are not identified as structures. A larger scale and the published plans are necessary.
- The EAMENA comparison uses distance only. I did not read the 577 descriptions for scroll features (cisterns, channels, tombs) near each entry place. The water-feature table (cisterns, reservoirs, aqueducts) is the next step for that.
- The ten landmark coordinates of the control test are published page coordinates. I wrote them from memory and did not look them up again. An error of 20 to 30 m in one of them is possible.

## Files

In this folder: `sites.csv`, `sites.geojson`, `sites.kml` (48 places); `figures/F017b_dec74_jerusalem_control_landmarks_marked.jpg`; `figures/F016b_dec74_ain_duk_points_marked.jpg`; three new keys in `transforms_corona_1967_df041d.json`. In `research/regional/peraea/`: the correction table, the exploratory script and its output, and the tests. The EAMENA distance table and the full-size windows are not in the repository.

Transforms (EPSG:2039, tile pixels):
- Jerusalem window of F017b: `[E, N] = [x, y, 1, h − 520] @ [[1.105740, −0.135728], [−0.244968, −0.912589], [223904.83, 648154.97], [0.524557, 0.113577]]`, then subtract (46.3, 13.2). h is the ground height in metres.
- F017b → F016b: `[[0.990121, 0.043983], [0.001391, 0.969243], [1395.50, 16613.55]]`
- F007c → F006c: `[[0.982461, −0.020826], [0.006703, 0.961338], [−958.30, 21495.04]]`
