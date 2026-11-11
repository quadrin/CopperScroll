# CORONA 1967 registered; May 1978 at Nebi Musa, Deir Hajla and Qumran; Netzer plan on the image of 1978 — 11 November 2026

## Result first

1. **CORONA 1967 (strip DF041, tile d) now has a transform.** 341 blocks agree with the HEXAGON image of 1 December 1974; the error is 16 m (rms) west of the Jordan. The scale is 2.17 by 2.12 m for each pixel.
2. **Correction.** The window that I named "east bank Kafrein" is not Kafrein. It is Shunat Nimrin (South Shuna) at the mouth of Wadi Shueib, approximately 5 km north of Kafrein. Kafrein, Tell er-Rameh and Tell Iktanu are on the tile, but outside the four windows. A new script cuts them.
3. **The image of 5 May 1978 is sharper than the image of December 1974.** Deir Hajla and Nebi Musa are Checked at a second date, with the same sizes.
4. **The plan of Netzer 1975 (figure 2) agrees with the image of 1978** with the scale of its bar, north from its arrow and one anchor. The image of 1978 shows also four excavation areas that are not on that plan.
5. **CORONA is too coarse for buildings.** It shows position and land use only.
6. **Not done:** Tell Iktanu on the image (the south hill), the frames of 1953, and a full use of the frames of 1918.

## 1. CORONA, 26 September 1967: registration

- Method: I rectified the CORONA window with a first transform (two points). Then I compared blocks of it with the rectified HEXAGON image of 1 December 1974 (tile F017b). Each block that agreed gave one control point.
- The first method (shading of the elevation model) did not work here. The land is too light on this film.

| Window | Blocks | Error (rms) |
|---|---|---|
| Jericho oasis and scarp | 206 | 13 m |
| Plain and the Jordan | 129 | 4 m |
| Both, one transform | 341 | 16 m |

- Transform (EPSG:2039; E, N = [x, y, 1] × A, tile pixels): `[[2.139369, 0.362865], [0.128294, −2.117663], [201811.9, 640967.5]]`.
- **Limit:** there is no control east of the Jordan. The two transforms of the two windows differ by 60 to 80 m at Shunat Nimrin. I estimate an error of 100 to 200 m on the east bank.

### What the four windows show

| Window | Content | Status |
|---|---|---|
| Jericho oasis and scarp | Wadi Qelt gorge, Tulul Abu el-ʿAlayiq, Tell es-Sultan, the town, the camps | Checked by registration |
| Plain and the Jordan | Deir Hajla at its left edge, the Jordan, a road bridge at the bottom | Checked by registration |
| "East bank Kafrein" | **Shunat Nimrin**: road junction near 31.901 N, 35.624 E, village, orchards, a walled compound of approximately 70 m east of the village (31.898 N, 35.629 E), an oval track | Probable (extended transform); the place of Tell Nimrin is not identified |
| DF040 d, oasis | An oasis at a wadi mouth, north of the Jericho frame | Not identified; no transform |

### 1967 against 1974

| Place | 26 September 1967 | Change to 1 December 1974 |
|---|---|---|
| Tulul Abu el-ʿAlayiq | The terrace north of Wadi Qelt has no marks. The cliff line agrees with 1974. | In 1974: a new road loop north of the site, a first excavation mark on the mound north of the wadi, large plantations south of the wadi. |
| Tell es-Sultan | The road bend at the spring agrees. The mound is a light area. | No change that I can see at this scale. |
| Deir Hajla | One dark spot of approximately 50 m at the place of the compound (agreement approximately 40 m). A wadi with plants 350 m to the north-east. | The same. |

- I do not see excavation marks on the terrace in 1967. But a pixel of 2 m cannot show small trenches. Status: Not confirmed.

### Position of the east-bank places on tile DF041 d (for the new script)

| Place | x | y |
|---|---|---|
| Kafrein dam, centre | 28790 | 5435 |
| Tell Kafrein | 27760 | 5285 |
| Tell el-Hammam | 28665 | 5960 |
| Habbasa | 28895 | 6055 |
| Tell er-Rameh | 27320 | 6520 |
| Tell Iktanu | 28485 | 7055 |
| Nebi Musa (west side) | 17890 | 6975 |

The dam was built in 1967 and 1968. The window will show its state in September 1967.

Command for the Mac Terminal (not tested):

```bash
bash ~/Library/CloudStorage/GoogleDrive-*/My\ Drive/Copper\ Scroll/08\ Working\ files/hexagon\ windows\ 2026-11-10/cut_corona1967_kafrein_nebi_musa_2026-11-11.sh
```

## 2. HEXAGON, 5 May 1978: three windows

| Place | What the image of 1978 shows | Agreement with 1974 | Status |
|---|---|---|---|
| Nebi Musa | Compound of approximately 65 by 77 m with courts in steps; fields of graves to the north and south-east; the road passes 150 m to the west | Position 25 to 40 m; form the same | Checked (two dates) |
| Deir Hajla | South block of approximately 39 by 37 m with a round mark (dome) in its court; walled north court of approximately 26 by 34 m, empty; trees on the west side. Total approximately 40 by 69 m | Position approximately 40 m; form the same | Checked (two dates) |
| Khirbet Qumran | The rooms are clear. A paved road and a parking area are north of the site. Regular plantations are east of the shore road | Position 160 m (poor) | Checked by form |
| ʿEin Feshkha | Not on the film. The edge of the film, with its round marks, is north of the building | — | No result |

- **Limit:** the transform of 1978 was fitted near Jericho. At Qumran, at the south end of the tile, it is wrong by approximately 160 m. Do not use it there for positions.
- A black straight line across the Deir Hajla window is a defect of the film.
- Earlier today I gave Nebi Musa as 70 by 67 m from the image of 1974. The image of 1978 is sharper; I think 65 by 77 m is better. A plan test is still not done.

## 3. Jericho palaces: the plan of Netzer 1975 on the image of 1978

Plan: E. Netzer, IEJ 25 (1975), figure 2 (general plan after the season of 1973/74). Test: scale from the bar (1.69 pixels of the scan for each metre), north from the arrow (16.5 degrees), one anchor (the building on the southern mound).

| Part of the plan | On the image of 5 May 1978 | Agreement |
|---|---|---|
| 5, southern mound | A square excavated building of approximately 25 m at the centre of a round mound | Anchor |
| 7, northern wing | An excavated area with rooms, directly north of the wadi | 10 to 20 m |
| 3, swimming pool (complex A) | Two rectangular basins side by side | Approximately 15 m |
| 1 and 9, central building (complex A) | Excavated rooms on and around the mound | Agrees in a general way |
| 4, building B | Below a plantation; not visible | — |
| 6, sunken garden | Trees and a path; no clear line | Not confirmed on this date |

- A free fit of the two best points gives a turn of 12.6 degrees and a scale 6 % larger. Thus the plan and the image agree to approximately 4 degrees and 6 %.
- **Areas that are excavated in 1978 and are not on the plan of 1975** (position on the rectified image; Seen, not identified):
  1. a large building with rows of rooms, approximately 70 by 60 m, between complex A and the northern wing;
  2. rooms directly east of the two basins;
  3. a small area approximately 130 m north-east of the northern wing;
  4. a small area at the west end of complex A.
- These are probably the seasons of 1975 to 1978. I did not compare them with the final report (Netzer 2001), which is not in the Drive.

## 4. The frames of 1918

- AWM B03552 is a German frame (squadron 303, 16 June 1918). Its header says "Str. Nebi Musa–Jericho". It shows the road, not the shrine.
- AWM B03561 is a vertical frame of the Jericho oasis. At 640 pixels it has approximately 6 m for each pixel. It is not better than CORONA for our places.
- I did not register these frames. The larger German plates (The National Archives, AIR 1/2270) are still not requested.
- The frames of 1953 (Hunting survey) are not in the Drive.

## 5. Tell Iktanu, south part

- The summary of the monograph (K. Prag, *Excavations at Iktanu in South Jordan*, open access on JSTOR) says: the higher north hill, north of the highway, has the name Tell Iktanu; there is a lower south hill that early visitors did not see; Area C is at the north-east end of the south hill; Site A (Intermediate Bronze Age) is on the south hill.
- This agrees with the site table for the north hill (the long hill north-west of the highway).
- I cannot identify the south hill on the image of 1974 without the plan (figures 1.1 and 2.1 of the monograph). The chapters did not load in this session.

## Not done

- The CORONA windows of Kafrein and Nebi Musa (after the new script).
- Control for CORONA east of the Jordan.
- A comparison with the final report of Netzer.
- The south hill of Tell Iktanu on the image.
- The frames of 1953; the German plates of 1918 at full size.
- The site table and the atlas change list are not changed by this note.

## Files

Drive `07 Maps and GIS/Project site layer and HEXAGON chips 2026-11-11`:
- `date_pairs/`: `hexagon_1974_dec_1978_may_nebi_musa.jpg`, `…_deir_hajla.jpg`, `…_khirbet_qumran.jpg`, `…_tulul_palaces_1000m.jpg`; `corona_1967_sep_hexagon_1974_dec_tulul_abu_el_alayiq.jpg`, `…_tell_es_sultan.jpg`, `…_deir_hajla.jpg`; `corona_1967_sep_shunat_nimrin_rectified.jpg`
- `plan_overlays/F007c_may78_tulul_abu_el_alayiq_netzer_1975_fig2_overlay_rectified_2026-11-11.jpg` (has a published plan in it: do not put it in the public repository)
- `chips/F007c_may78_tulul_abu_el_alayiq_rectified_0.5m.jpg`
- `corona_1967_df041d_transform_2026-11-11.json`

Drive `08 Working files/hexagon windows 2026-11-10/cut_corona1967_kafrein_nebi_musa_2026-11-11.sh`

## Sources

- Netzer 1975: Drive `04 Articles and chapters/Netzer 1975 – Hasmonean and Herodian winter palaces at Jericho (IEJ 25).pdf`
- Prag, Iktanu (summary of the chapters): https://ancientworldonline.blogspot.com/2025/10/excavations-at-iktanu-in-south-jordan.html
- AWM B03552 and B03561: Drive `06 Imagery/AWM 1918 and Kluger 1937-38 aerials 2026-11-10`
