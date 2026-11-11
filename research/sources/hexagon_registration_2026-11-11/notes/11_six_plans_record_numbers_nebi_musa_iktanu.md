# Six plans of Netzer 2001 on the image of 1978; record numbers; Nebi Musa wall lengths; south hill of Iktanu — 11 November 2026

## Result first

1. **Six plans of Netzer 2001 are on the image of 5 May 1978** (plans 11, 12, 25, 26, 29, 35), all with the site grid and no free value. New: plan 12 (Area AC) and plan 29 (Herod's Second Palace) are Probable; plan 25 (the garden) cannot be tested.
2. **Correction.** I wrote that one square of the site grid is 20 m. It is 10 m. The calculation used 10 m; only the text was wrong. The northern wing is approximately 300 m from the anchor, not 350 m.
3. **The record numbers of the change list are checked** against the checklist PDF. All 26 lines are accepted by the owner. One place (the Plateau Fort) has no record.
4. **Nebi Musa: the wall lengths on the image of 1974 agree with published values** to 2 to 8 m. **Correction:** the size "65 by 77 m" from the image of 1978 was wrong; that window cuts the south part of the compound.
5. **Tell Iktanu: a lower south hill is Probable** from the elevation model, south-east of the highway.
6. **Shunat Nimrin:** the HEXAGON strip F017 does not include it. A script cuts a window from strip A017 tile e.
7. **Not done:** the frames of 1953.

## 1. Jericho palaces: six plans

Method: see `netzer-2001-plans-11-26-35-by-site-grid-on-1978-shunat-nimrin-2026-11-11.md`. Anchor: the wall between the two pools = grid column 17, row 47. Turn 13 degrees east of north. One grid square = 10 m.

| Plan | Area | Grid (columns; rows) | On the image | Status |
|---|---|---|---|---|
| 14 | AB, Pools Complex | 13–21; 44–49 | Two pools, halls, west building (direct overlay) | Checked |
| 26 | AE, Twin Palaces | 15–23; 38–43 | Rows of rooms south of the pools | Checked |
| 35 | Northern Wing, Third Palace | 38–48; 29–32 | Excavated rooms north of Wadi Qelt | Checked |
| 11 | AA, Buried and Fortified Palace | 8–13; 42–49 | Mound west of the pools | Probable |
| 12 | AC | 4–9; 43–49 | West part of the mound; dark trenches and rooms inside the frame | Probable |
| 29 | AG and AL, Herod's Second Palace | 22–27; 37–46 | Excavated rooms east of the Twin Palaces; plans 26 and 29 join at columns 22–23 as plan 26 says | Probable |
| 25 | Hasmonean Garden of the Pools Complex | 13–20; 50–55 | Open ground north of the pools | Possible (no test) |

- Not done: plans 15 and 23 (details of the area of plan 14) and plan 36.
- The small excavated area north-east of the northern wing is not on these plans. Not identified.
- The checklist PDF cites "Netzer 2001, Plan 1, p. XI", a general plan of the Jericho plain. It is not in the portfolio photographs.
- Limits: grid lines marked by eye; fold not corrected; 0.8 m for each pixel; one reader.

## 2. Record numbers

Source: the text of `Copper Scroll – Regional atlas and dated checklist – 9 November 2026 edition, redrawn 2026-11-10.pdf`. A list of its 734 record titles is saved (`checklist_record_ids_from_atlas_pdf_2026-11-11.txt`; the numbers are in the PDF).

| Place | Record |
|---|---|
| Hyrcania; aqueducts; saddle with reservoirs | sit0098; sit0099; sit0100 |
| Mar Saba | sit0103, sit0104 |
| Tulul Abu el-ʿAlayiq; palace pools | sit0019; sit0020 |
| Quruntul | sit0023, sit0024 |
| Deir Hajla | sit0039 (not sit0022, which is Tell el-Qos) |
| Nebi Musa | sit0057 |
| Khirbet Qumran; Feshkha main building | sit0079; sit0088 |
| Birket Musa; Khirbet Mazin | idx0547, idx0548; idx2069 |
| Machaerus; Callirrhoe | sit0290; sit0292 |
| Umm Hadar; Tall Barakat; Tell er-Rameh; Habbasa | sit0298; sit0299; sit0303; sit0305 |
| Plateau Fort (Kafrein) | No record in the checklist |

The checklist has also sit0304 (Tall el-Hammam) and sit0308 (Tell Nimrin). The change list has no line for them.

## 3. Nebi Musa

| Wall | Image of 1 December 1974 | Published |
|---|---|---|
| North | 66 to 70 m | approximately 74 m |
| West | 67 m | approximately 70 m |
| East | 66 m | 68 m |
| South | 53 m | approximately 55 m |

- The form agrees: a trapezoid with the short side at the south.
- The published values are from a web page (Madain Project). I did not see the primary survey. A measured plan is still not in the Drive.
- Status: Checked (two dates; wall lengths). Record sit0057.

## 4. Tell Iktanu, south hill

- A summary of the Prag monograph says: the north hill is north of the highway, rises 40 to 47 m above the plain and has a rock ridge along its north crest from north-east to south-west; there is a lower south hill.
- The image of 1974 agrees for the north hill: the dark line along its north-west crest is the ridge.
- The elevation model has a second summit at 31.8163 N, 35.6682 E, 18 m lower, approximately 450 m south-west of the north hill and south-east of the highway.
- Status: Probable. The plan of the monograph (figures 1.1, 2.1) is necessary for Checked. The JSTOR page does not load here.

## 5. Shunat Nimrin

- The published point of Tell Nimrin is north of the top edge of tile F017b. Script: `cut_dec1974_shunat_nimrin_2026-11-11.sh` (strip A017 tile e; the place is near the tile edge; not tested).

```bash
bash ~/Library/CloudStorage/GoogleDrive-*/My\ Drive/Copper\ Scroll/08\ Working\ files/hexagon\ windows\ 2026-11-10/cut_dec1974_shunat_nimrin_2026-11-11.sh
```

## 6. Site table

38 places. New: south hill of Iktanu; Second Palace; Area AC; the garden. Changed: Nebi Musa; the dark area south of the highway (not a hill).

## Not done

- The frames of 1953 (APAAME; not in the Drive).
- A second reader.

## Files

Drive `07 Maps and GIS/Project site layer and HEXAGON chips 2026-11-11`: `plan_overlays/F007c_may78_jericho_netzer_2001_six_plans_by_site_grid_overlay_2026-11-11.jpg` (not for the public repository); `date_pairs/hexagon_1974_dec_1978_may_nebi_musa_zoom_160m.jpg`; the site table (three formats); `atlas_change_list_from_image_work_2026-11-11.csv`; `checklist_record_ids_from_atlas_pdf_2026-11-11.txt`.

## Sources

- Nebi Musa wall lengths: https://madainproject.com/nabi_musa
- Iktanu: https://ancientworldonline.blogspot.com/2025/10/excavations-at-iktanu-in-south-jordan.html
