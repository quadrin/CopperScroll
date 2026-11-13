# Edit log: changes of status words, positions and table values, with the earlier value and the reason

Started: 2026-11-13. Rule of the owner (13 November 2026): "update things when we gain more confidence in them, so long as we keep a backlog/edit log of our previous thinking and why we changed." This file is that log. Each change gets one row. Rows are added at the end; a row is never deleted. If a change is reversed later, a new row says so.

What this log covers: (1) image status words (Seen, Checked, Probable, Possible, Not confirmed); (2) positions of places; (3) values of the entry-place table (location grade, offset, image dates, image evidence). What it does not cover: the strength of a match (low, medium, high) and the candidate of an entry. No such value was changed.

Status of the table: the rows of section A are the changes of this pull request to `entry_places_location_assessment_2026-11-12.csv` and `entry_assessments_with_location_grade_2026-11-12.csv`. The file names keep the date of the first version; git has the earlier text.

## A. Entry-place table (changes of 13 November 2026)

| No. | Date | Place | Field | Earlier value | New value | Why | Evidence |
|---|---|---|---|---|---|---|---|
| A1 | 13 Nov | wadi_qumran (entry 20) | location grade | C, "not tested" | **B, "agrees with area"** | The place was not looked for before. Now plate XXIX is on the image of 1978: the aqueduct is Checked, and the dam, the tunnel and the gorge mouth have positions. The table point is 370 m from the dam, inside its stated 500 m | step 18 |
| A2 | 13 Nov | wadi_qumran | offset, image dates, evidence | empty | 370 m (dam), 450 m (gorge mouth); 1 date | Same | step 18 |
| A3 | 13 Nov | wadi_qumran | point | 31.74111 N, 35.45056 E | **not changed** | A move to the gorge mouth (31.74094 N, 35.45529 E) makes grade A possible. But "below Kh. Qumran" can also mean the lower wadi east of the ruin. The reading decides this, not the image. Left for the owner | proposals note |
| A4 | 13 Nov | kh_qumran (21, 22) | offset | 99 m | 94 m | Height model for the 1978 tile. The earlier fit was 75 m wrong at the south edge of its window | step 21 |
| A5 | 13 Nov | kh_qumran | image dates; evidence | 2; "ruin on the images" | 3; two plan overlays, centre and L71 positions | Third date (25 June 1974); overlays of Humbert 2016 fig. 8 and plate XXIX | steps 9, 18, 20, 21 |
| A6 | 13 Nov | gerizim (57) | offset | 110 m | 45 m | Height model for tile F014a. The value of 110 m came from a fit with no height term on a summit | step 21 |
| A7 | 13 Nov | gerizim | evidence | "an enclosure in a forest clearing 560 m north-north-east is Probable Tell er-Ras" | Tell er-Ras is fixed at 32.2066 N, 35.2745 E, 650 m north, outside the 500 m of the row | Survey of Palestine 1:20,000 map (36 m); test with the church; plan of Bull 1967 (Probable) | steps 23, 24 |
| A8 | 13 Nov | gerizim | second place row for Tell er-Ras | none | **not added** | A second row is a candidate decision (is entry 57 at Bull's stairs or on the summit?). Left for the owner | proposals note |
| A9 | 13 Nov | ibziq (59) | image dates; offset | 1; 80 m | 2; 132 m (south field) | Second date (25 June 1974). The two ruin fields are the same on the two dates. The offset is now measured to the middle of the south field with the height model | steps 5, 25 |
| A10 | 13 Nov | ibziq | grade | B | B (no change) | A needs a published plan or description that agrees with one field | — |
| A11 | 13 Nov | tell_es_sultan | offset; evidence | 83 m; "mound on the images" | 130 m to the mound centre; overlay of Kenyon 1981 fig. 1, Trench II 17 m from the point | Height model; plan overlay | steps 11, 21, 23 |
| A12 | 13 Nov, later | ibziq (59) | location grade | B, "agrees with area (Probable)" (A10) | **A, "confirmed (Kh. Ibziq Upper of the survey)"** | Row A10 said what A needs: a published description that agrees with one field. Zertal 2008 (site 44) gives it: grid 1878/1971, 435 m, a large ruin on a slope with the tomb of Nebi Hizqin and houses on its upper part, and the road at the bottom. The image has a walled hilltop enclosure with standing buildings, cells on the slope east of it, and the road. Grid 150 m; height 437 m against 435 m; two dates. The table point is 80 m from the enclosure | step 26 |
| A13 | 13 Nov, later | ibziq | evidence | "which of the two survey ruins this is, is not known" | south ruin = Upper (site 44); north ruin = Lower (site 42) | Lower: grid 1881/1980 (120 m from my point), 375 m against 373 m, spur between two ravines, road beside it | step 26 |

Grades after the changes: A 20, B 7, C 5, D 3, E 2 (12 November: A 19, B 7, C 6, D 3, E 2).

## B. Image status words

| No. | Date | Place | Earlier | New | Why | Step or note |
|---|---|---|---|---|---|---|
| B1 | 13 Nov | Kh. el-ʿAuja el-Foqa | Not confirmed | Checked | Ruin at the published point on two dates | 15 |
| B2 | 13 Nov | Tell esh-Sheikh Dhiab | Not confirmed | Probable (pool Checked) | Grid 1907/1614 of Zertal and Bar 2019; the pool is clear, the tell is a low rise beside it | 16 |
| B3 | 13 Nov | Kh. Qumran, aqueduct on the terrace | Possible | Checked | Plate XXIX on the image; the line of step 7 is on the plan line | 18 |
| B4 | 13 Nov | Kh. Yanun | Possible ruin field | Not confirmed | On two dates the "field" is strip terraces with no building outline | 20 |
| B5 | 13 Nov | Tell Balata | Possible | Checked by position | Published point at 50 m; 1:20,000 map at 70 m | 21, 24 |
| B6 | 13 Nov | Nablus, Police Barracks quadrangle of step 13 | Possible | **withdrawn** | The 1:20,000 map shows that the compounds of step 2 are the Government and Police Offices | 24 |
| B7 | 13 Nov | Sartaba, overlay of step 17 | "plan placed" | **withdrawn**, replaced | Scale-bar placement was 10 % and up to 190 m wrong; the plan has Palestine Grid ticks | 23 |
| B8 | 13 Nov | Tell er-Ras, advice of step 21 "keep the atlas value" | keep | **withdrawn**; platform at 176.06/179.23 | The map and the church test show the atlas value is 170 m off | 24 |
| B9 | 13 Nov | ʿAin Feshkha, main building | Probable | Checked | Plate XLII: direction, road and spring agree; two dates | 25 |
| B10 | 13 Nov | **Kh. Yanun** | Not confirmed (B4) | **Checked as the place of survey site 18-17/43/01; no wall outline is seen** | The survey book (Finkelstein, Lederman and Bunimovitz 1997) gives the same grid (18425/17385) and describes "a terraced ruin" of 0.4 ha with some inhabited buildings on the summit. This is what the images show: strip terraces at the point, small buildings 60 m south-west. B4 was right about what is on the image, but its conclusion was too negative: the ruin is the terraced slope | reading round 18 |
| B11 | 13 Nov | Kh. el-Marjama (ʿAin Samiya, mound A) | Checked by form | Checked by form and by the survey grid | Survey: tell of 3 ha on a spur at 18160/15540; my point is 90 m from it | reading round 18 |
| B12 | 13 Nov | Kh. Samiya (ʿAin Samiya, building C) | Seen | Probable as part of Kh. Samiya | Survey: khirbeh of 3 ha on a slope at 18170/15500; my point C is 60 m from it | reading round 18 |
| B13 | 13 Nov | Tell esh-Sheikh Dhiab | Probable (B2) | Probable (no change), with one more line of evidence | SWP sheet XV shows the ruin symbol of "Khurbet Fusail" touching "Birket Fusail" on its north-west side | reading round 18 |
| B14 | 13 Nov, later | Kh. Ibziq, south ruin | Probable (two dates) | Checked as Kh. Ibziq (Upper), survey site 44 | See A12 | step 26 |
| B15 | 13 Nov, later | Kh. Ibziq, north ruin | Probable (two dates) | Checked as Kh. Ibziq (Lower), survey site 42 | See A13 | step 26 |
| B16 | 13 Nov, later | Kh. Ibziq, fort point (el-Quleh) | Not confirmed, "slope with trees" (step 5) | Probable: light patch of approximately 40 m in a clearing at the top of the hill, at 189.24/197.94, on two dates | Survey site 43: stone pile of approximately 40 m on the summit, 399 m. The height model has its top (393 m) 64 m north-west of the survey grid point, at the patch. In step 5 I looked at the grid point only | step 26 |
| B17 | 13 Nov, later | Two small survey sites east of ʿAin Samiya (building 20 × 25 m; el-Qasr) | not examined | Not confirmed | Rock terraces at the two grid points on two dates; no outline | step 26 |

## C. Earlier thinking that is kept for the record

- 12 November: "Tell er-Ras is Probable at an enclosure 560 m north-north-east." Replaced (A7).
- 13 November, step 13: a quadrangle at the north foot of Gerizim was taken as the Police Barracks. Replaced (B6).
- 13 November, step 17: the Sartaba plan was placed with its scale bar. Replaced (B7).
- 13 November, step 20: Kh. Yanun "Not confirmed". Replaced (B10) after the survey description was read. The lesson: for a survey "khirbeh", read the site description before the image is judged; many such ruins have no wall outline at 1 m for each pixel.
