# The image of 5 May 1978 at Jericho, CORONA 1967 coverage, the plan of Wright on a rectified image — 11 November 2026

The owner ran `cut_may1978_and_corona_overviews_2026-11-11.sh` and asked for the items of the last "Not done" list.

## Result first

1. **The image of 5 May 1978 gives a third date for Jericho.** At Tulul Abu el-ʿAlayiq it agrees with the image of 1974 to approximately 35 m. **It shows new excavation areas north of Wadi Qelt that are not on the image of 1 December 1974.**
2. **CORONA 1967: strip DF041, tile d, covers Jericho, the lower Jordan and the fields east of the river.** I said this morning that CORONA had no use; that was true for strip DF042 only. A script for four full-size windows is ready.
3. **The plan of Wright 1961 (figure 1) agrees with the rectified image with north at the top of its page.** Thus the plan of Wright is north-up, and the plan of Patrich (figure 22) is the one that is turned (approximately 40 degrees).
4. **The south part of Tell Iktanu: not done.** The monograph of K. Prag is open on JSTOR, but the page does not load in this session.
5. The frames of 1918 and 1953: not done.

## 1. Jericho on 5 May 1978 (strip F007, tile c)

Source: window `F007c_may78_jericho_palaces_quruntul_full` (the owner cut it). I rectified it with the transform of tile F007c and put it beside the image of 1 December 1974 at the same scale (0.9 m for each pixel, north up).

- **Agreement of the two dates:** the southern mound with the square structure on its top, the road, the orchards and Birket Musa are at the same places. The difference is approximately 35 m. This is a test of the transform of 1978, which was fitted on a preview only.
- **Birket Musa** is a dark field of approximately 171 m from west to east on the image of 1978. This is the size of 1974 and of the Survey.
- **New in 1978, north of Wadi Qelt:** three or four areas with rows of small rectangular cells (exposed walls or excavation squares), each area 40 to 100 m long, on the terrace north of the wadi and at a small side gully. On the image of 1 December 1974 this terrace has only faint marks at one of these places.
  - The excavations of E. Netzer at the Hasmonean and Herodian palaces started in 1973 (literature; not looked up today). The new areas are probably his excavation areas of 1975 to 1978. I did not compare them with a plan.
- **The sun is high in May.** Walls have no long shadows, but the ground is not white as on the image of December. Field edges, tracks and excavation areas are clearer in 1978; mounds and scarps are clearer in 1974.
- The other three windows of 1978 (Nebi Musa, Deir Hajla, Qumran with ʿEin Feshkha) are in the Drive. I did not read them in this step.

File: `date_pairs/jericho_1974_dec_1978_may_tulul_abu_el_alayiq.jpg` and `…_tell_es_sultan.jpg`.

## 2. CORONA, 26 September 1967: strips DF040 and DF041

Source: the eight overviews that the script made (reduced 12 times).

| Tile | What it shows | Use |
|---|---|---|
| DF041 d | **The north end of the Dead Sea at the lower edge, the Jordan from north to south, the Jericho oasis west of the river, and fields with a wadi mouth east of the river** | Jericho, the plain, the east bank in 1967 |
| DF040 d | The Jordan valley north of the Jericho frame, with one oasis west of the river | Probable ʿAuja or Fasayil area; not identified |
| DF040 a, b, c and DF041 a, b, c | Desert, lava fields and hill country without detail at this size | None seen |

- The date is 26 September 1967 (film edge of the two strips). This is before the excavations at Jericho of the 1970s. For the east bank, the Kafrein dam is of 1967; I cannot say from the overview if the lake is there.
- **Limit:** on strip DF042 the land was too light and too grainy for building-size detail. The same limit is probable here. The full-size windows will show it.
- **Script:** `cut_corona1967_windows_2026-11-11.sh` cuts four full-size windows: the Jericho oasis with the scarp, the plain to the Jordan, the east bank, and the oasis of DF040. It uses the tiles that are in `~/Downloads/corona1967` now. I did not test it.

## 3. Hyrcania: the plan of Wright 1961, figure 1, on the rectified image

- Scale from the bar of the plan (300 m). North at the top of the page (the plan has no arrow). One anchor: the two pools on the deep hollow.
- **What agrees, with no more adjustment:**
  - the cliff lines north-west of the pools follow the edge of the deep shadow for approximately 300 m;
  - the fort enclosure is on the hilltop, approximately 30 m west of the centre of the dark pits;
  - the "Monument" falls on a small knoll with marks, approximately 250 m south-west of the pools;
  - the dotted path to the south-east follows a light line on the image for approximately 300 m.
- **Thus the plan of Wright is north-up, to approximately 10 degrees.**
- **Effect on the plan of Patrich (figure 22):** on that plan the direction from the double pool to the summit is approximately 40 degrees different from the image and from the plan of Wright. Thus the page of Patrich's figure is turned, and my turn of 40 degrees in the earlier overlay is supported by a second source. Status of "north of the plan of Patrich": Probable (no change), with more support.
- **Status of Hyrcania: Checked (no change), now with a strict test.**

## 4. Not done

- The south part of Tell Iktanu and a plan of the fort on the north hill. The source is K. Prag, *Excavations at Iktanu* (2024, open access). If the owner puts the introduction chapter in the Drive, I can do it.
- The CORONA windows (after the script).
- The windows of 1978 for Nebi Musa, Deir Hajla and Qumran.
- A comparison of the new excavation areas of 1978 with the plans of Netzer.
- The frames of 1918 and 1953.

## Files

- Drive `07 Maps and GIS/Project site layer and HEXAGON chips 2026-11-11`: `date_pairs/jericho_1974_dec_1978_may_*.jpg` (two files), `plan_overlays/F018b_dec74_hyrcania_wright_1961_fig1_overlay_rectified_2026-11-11.jpg`
- Drive `08 Working files/hexagon windows 2026-11-10`: `cut_corona1967_windows_2026-11-11.sh`
- Drive `08 Working files/hyrcania sheets 2026-11-11`: the plan page of Wright (two page images)
