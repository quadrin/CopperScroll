# HEXAGON 1974: registration of the other windows, new positions, Tell Iktanu — 11 November 2026

This note continues `hexagon-1974-automatic-registration-to-elevation-model-2026-11-11.md`. The older notes are not changed.

## Result first

1. **Seven more window transforms are made** with the same method (comparison with the Copernicus GLO-30 elevation model). Tiles F017c and F018c had no transform before.
2. **Tell Iktanu is found. Status: Probable.** It is the light oval hill on the north-west side of the highway, at 31.8192 N, 35.6715 E. The road works that I gave as a possible place are approximately 500 m to the north-east and are not the tell.
3. **Deir Hajla: Checked by position.** Two independent transforms put the compound 50 to 60 m from the published point. The form has no test (no plan).
4. **Hyrcania: the old control pixel is 28 m from the summit of the elevation model.**
5. **Khirbet Mazin: the old transform is correct there to approximately 40 m.**
6. **A limit of the method:** a summit that is much higher than the ground around it can be wrong by approximately 200 m. Machaerus shows this (213 m).

## 1. Method (changes)

- Three or four steps from coarse to fine (80, 40, 20 tile pixels). The first steps find a shift only. The last steps fit an affine transform.
- Blocks overlap by one half. Thus the number of independent points is approximately one quarter of the number in the table.
- For tiles F017c and F018c, the first value was the linear part of the neighbour tile and one known point (Madaba; the top of Machaerus).

## 2. The new transforms

Form: `E = a·x + b·y + c`, `N = d·x + e·y + f`, Israel Transverse Mercator grid (EPSG:2039). x and y are tile pixels, but for tile A017e they are pixels of the Kafrein window after the turn of 180 degrees.

| Tile and windows | a | b | c | d | e | f | Blocks | Error (rms) | Scales |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| F018b, east shore window | 1.103914 | −0.209849 | 218502.6 | −0.107540 | −0.842760 | 630061.7 | 79 | 54 m | 1.109 / 0.868 |
| F018b, Khirbet Mazin window | old three-point transform with a shift of 40 m east and 11 m north | | | | | | 7 | 16 m | 1.016 / 0.887 |
| F018c, two windows | 0.952878 | −0.202242 | 257687.3 | −0.103945 | −0.827621 | 626007.0 | 561 | 72 m | 0.959 / 0.852 |
| F018c, Machaerus window only | 0.969831 | −0.195917 | 257535.6 | −0.099828 | −0.832932 | 626084.0 | 151 | 76 m | 0.975 / 0.856 |
| F017c, two half-size windows | 0.945391 | −0.174199 | 259261.4 | −0.109466 | −0.818103 | 641920.7 | 685 | 51 m | 0.952 / 0.836 |
| A017e, Kafrein and Rameh windows | 0.922475 | −0.022810 | 261025.7 | −0.116446 | −0.839782 | 643251.9 | 168 | 24 m | 0.930 / 0.840 |
| F017b, east-bank half-size window | 0.976340 | −0.208518 | 225178.3 | −0.148432 | −0.845583 | 647472.1 | 25 | 20 m | 0.988 / 0.871 |

- **F018b, east shore:** the old three-point transform was wrong there by approximately 430 m (north) and 100 m (east). The land in this window is a strip of approximately 2 km. Thus the scale along the rows (1.109) is not well fixed. Use this transform inside the land strip only.
- **F017b:** the east-bank part has scales of 0.988 and 0.871 m; the west part has 1.000 and 0.891 m. The scale changes along the tile, as on tile F018b.
- **Status of all transforms in this table: Checked in the windows that I used, with the error of the table.**

## 3. Tell Iktanu

- Published point: 31.819256 N, 35.671878 E (OpenBible, "point on tel"). The elevation model has a single mound of 25 m at 31.81919 N, 35.67125 E. The two are 60 m apart.
- K. Prag (2024 monograph, introduction) says that the higher hill is on the north side of the highway.
- On the June image (tile A015c), the new transform puts the two points on **one light oval hill of approximately 300 m by 200 m, directly north-west of the highway**, with dark broken ground on its top. Window pixel of its centre: approximately 3043, 5431. Position by the transform: 31.8192 N, 35.6715 E.
- From Tell er-Rameh (the round mound) this hill is 2.65 km away at 106 degrees. The published statement is "2¾ km east-south-east". Agreement.
- **The earlier candidates:**
  - the road works with the trapezoid enclosure: now at 31.8217 N, 35.6762 E, approximately 500 m north-east of the tell. They are military works, not the tell;
  - the dark oval hill south of the road: now at 31.8184 N, 35.6745 E, approximately 300 m east of the tell, on the other side of the highway. Iktanu is a double site, thus this hill can be its second part. Not confirmed.
- **Status: Tell Iktanu = the light oval hill north-west of the highway, Probable.** Reasons: two position sources and the description. I did not compare the form with the APAAME frames at full size.

## 4. New positions (the older notes have the old values)

### Kafrein area (tile A015c, automatic fit; error 30 to 100 m)

| Thing | Window pixel | New position |
|---|---|---|
| Dam crest, north-west end | 2582, 1660 | 31.8520 N, 35.6741 E |
| Dam crest, south-east end | 2942, 1920 | 31.8495 N, 35.6781 E |
| Barakat, curved scarp | 2502, 1577 | 31.8527 N, 35.6733 E |
| Plateau Fort | 3602, 2772 | 31.8416 N, 35.6845 E |
| Habbasa, dark block | 3242, 3072 | 31.8393 N, 35.6793 E |
| Tell el-Hammam, hill with lines | 2833, 2950 | 31.8407 N, 35.6744 E |
| Tree group at the foot of the tell | 2680, 3200 | 31.8387 N, 35.6719 E |
| Dark patch on the long hill north-west of the lake (Umm Ḥadhar?) | 2457, 390 | 31.8630 N, 35.6754 E |
| Tell er-Rameh, round mound | 785, 4979 | 31.8249 N, 35.6441 E |
| Oval mound (not Tell er-Rameh) | 1079, 4366 | 31.8299 N, 35.6491 E |
| Tell Iktanu, light oval hill | 3043, 5431 | 31.8192 N, 35.6715 E |
| Road works (military) | 3363, 5108 | 31.8217 N, 35.6762 E |

- The largest changes against the two-point transform: the tree group (140 m), the Umm Ḥadhar patch (500 m), the road works (550 m), the two mounds (550 to 700 m).

### West side (tile F017b, automatic fit)

| Thing | Tile pixel | Old position | New position |
|---|---|---|---|
| ʿEin Feshkha building | 23031, 22340 | 31.7160 N, 35.4517 E | 31.7159 N, 35.4525 E |
| Tulul Abu el-ʿAlayiq, southern mound | 18020, 6000 | 31.8504 N, 35.4364 E | 31.8506 N, 35.4367 E |
| Quruntul, summit enclosure | 16673, 3169 | 31.8743 N, 35.4287 E | 31.8746 N, 35.4289 E |
| Deir Hajla compound | 24800, 8690 | (control point) | 31.8200 N, 35.5014 E (west fit); 31.8204 N, 35.5015 E (east fit) |

- The changes are 30 to 80 m. No status changes, but one: **Deir Hajla, Checked by position** (Wikipedia point 31.82028 N, 35.50194 E: 50 to 60 m; the point of the church corpus: approximately the same).

### Tile F018b, west windows

| Thing | Tile pixel | New position | Compare |
|---|---|---|---|
| Hyrcania, old control pixel | 13230, 5055 | 31.7192 N, 35.3659 E | Summit of the model: 31.7189 N, 35.3659 E (28 m) |
| Mar Saba, old control pixel | 10585, 7332 | 31.7051 N, 35.3314 E | Published: 31.7050 N, 35.3311 E (30 m) |

### Machaerus (tile F018c)

- Top of the citadel hill, tile pixel 5730, 20570: 31.5670 N, 35.6216 E by the window fit.
- The elevation model has the summit at 31.5675 N, 35.6238 E (693 m). The difference is 213 m from west to east.
- **Cause (probable): relief displacement.** The tile is a panoramic photograph, and the citadel hill is much higher than the mean ground of the window. An affine transform cannot correct this.
- **Limit for all tiles:** the position of a high summit or of a deep canyon floor can be wrong by 100 to 200 m. Positions on the plain and on the plateau are better.

## Not done

- Positions of the things in the east-shore, Callirrhoe, Machaerus and east-bank notes. I do not have their pixel values in this session; the transforms above can give them when the pixel values are read again.
- A correction for relief displacement.
- A comparison of the Tell Iktanu hill with the APAAME frames at full size.
- A plan or a scaled modern image of the present monastery of Deir Hajla (see the answer in the chat: where it can be found).

## Files

Drive `08 Working files/hexagon windows 2026-11-10`:
- `A015c_jun74_tell_iktanu_area_marked_2026-11-11.jpg`
- `hexagon_elevation_model_registration_2026-11-11.py` (new version, with the coarse-to-fine part)

## Sources

- Copernicus GLO-30 elevation model, tile N31 E035 (Drive).
- https://www.openbible.info/geo/modern/m56a432/tall-iktanu
- https://ancientworldonline.blogspot.com/2025/10/excavations-at-iktanu-in-south-jordan.html (contents of K. Prag, Excavations at Iktanu, 2024)
