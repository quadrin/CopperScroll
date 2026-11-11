# HEXAGON 1974: automatic registration of four tiles to the elevation model — 11 November 2026

This note closes two of the three open items of `tile-a015c-affine-transform-barakat-grid-deir-hajla-plan-2026-11-11.md`. The older notes are not changed.

## Result first

1. **A new method gives many control points for each tile.** I compare the image with a shaded picture of the Copernicus GLO-30 elevation model, block by block. The fit has 11 to 28 points for each tile and an error of 19 to 44 m (root mean square).
2. **All four transforms are now Checked in the windows that I tested.** Each tile has two scales.
3. **Tell er-Rameh is the round mound beside the road. Status: Checked by position** (45 m on the December tile, 95 m on the June tile) **and by form** (the APAAME frames of 1998).
4. **Mar Saba: Checked by an independent test.** The new transform of tile F018b puts the old control point 30 m from the published position.
5. **Barakat:** the place on the image is 31.8527 to 31.8532 N, 35.6733 E. The grid reference of the paper is 340 to 385 m south of it (no change of the result).
6. **Tile F018b is not one affine transform from west to east.** The fit of the west windows is wrong by approximately 280 m at Khirbet Mazin, 8 km to the east. Use the west fit for the Hyrcania and Mar Saba windows only.
7. **Deir Hajla: Not done.** I found no plan and no scaled modern image of the present compound.

## 1. Method

- For a window, I calculate with the old transform where each cell of the elevation model falls. I make a shaded relief picture in the pixel frame of the window (sun from azimuth 190 degrees at 28 degrees for 1 December; azimuth 120 degrees at 60 degrees for 25 June).
- I make the image smaller (20 pixels to 1) and remove the slow changes of tone from the image and from the relief picture.
- For each block of 50 by 50 small pixels (approximately 1 km), I find the shift that gives the best correlation. The shift step is 20 tile pixels (approximately 20 m). I use a block only if the correlation is 0.6 or more (0.5 for the June tile).
- Each block gives one control point. An affine transform is fitted to all points by least squares. I repeat the procedure two or three times.
- **Limits.** The method needs relief. It gives no points on the plain of Jericho or on the Dead Sea. The June image has a high sun, thus the correlation is lower (0.62) and there are 11 points only. One model cell is approximately 30 m.
- The script is in the Drive: `hexagon_elevation_model_registration_2026-11-11.py`.

## 2. The four transforms

Form: `E = a·x + b·y + c`, `N = d·x + e·y + f`, with E and N in the Israel Transverse Mercator grid (EPSG:2039). For tiles F017b and F018b, x and y are tile pixels. For tiles A015c and A017e, x and y are pixels of the Kafrein window after the turn of 180 degrees (north up).

| Tile (date) | a | b | c | d | e | f | Points | Error (rms) | Scale along rows / columns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| F017b (1 Dec 1974) | 0.987848 | −0.209328 | 224890.0 | −0.153164 | −0.866512 | 647730.0 | 28 | 44 m | 1.000 / 0.891 m |
| F018b, west windows (1 Dec 1974) | 1.025525 | −0.244158 | 222424.1 | −0.163204 | −0.876369 | 631781.3 | 25 | 44 m | 1.038 / 0.910 m |
| A017e, Kafrein window (1 Dec 1974) | 0.924421 | −0.028354 | 261033.0 | −0.122112 | −0.838848 | 643272.3 | 24 | 19 m | 0.932 / 0.839 m |
| A015c, Kafrein window (25 Jun 1974) | 1.191048 | −0.207998 | 261178.6 | −0.081858 | −0.953556 | 641794.0 | 11 | 25 m | 1.194 / 0.976 m |

## 3. Tile F017b

- The old transform (four control points) and the new one agree at the old control points: Tell es-Sultan 14 m, Nebi Musa 61 m, Qumran 56 m, Deir Hajla 57 m.
- The largest shifts of single blocks are 100 to 120 m to the east, at the west edge of the Jericho window and at the cliff of Qumran.
- Two more checks with single mounds of the elevation model (old transform):
  - the southern mound of Tulul Abu el-ʿAlayiq: 33 m;
  - Tell es-Sultan: the mound of the model is 90 m from the control point (the control point is a grid reference to 100 m).
- **Status: Checked. Error 20 to 60 m in most places, 120 m at the west edge.** The corrected sizes of the note `hexagon-1974-12-01-tile-f017b-two-scales-corrected-sizes-2026-11-11.md` do not change (the scales are 1.000 and 0.891 m; before 1.006 and 0.894 m).

## 4. Tile F018b

- Windows used: the west window (Mar Saba, aqueducts) and the Hyrcania window. 25 points, correlation 0.83.
- Scales: 1.038 m and 0.910 m. The old values (three control points) were 1.016 m and 0.887 m.
- Old control points against the new transform: Mar Saba 30 m; Hyrcania 88 m (the old point was a site coordinate for the reservoirs, not an exact place); Khirbet Mazin 280 m.
- **Khirbet Mazin.** The window of Khirbet Mazin gives two good blocks only, at the cliff west of the site. They agree with the old transform to 40 to 70 m. Thus the old control point at Khirbet Mazin is good, and the west fit cannot be used there. The cause is the panoramic camera: the scale changes along the 11 km between the two areas.
- **Status: Checked in the west windows (error approximately 45 m). For the Khirbet Mazin window, use the old three-point transform (Probable, error approximately 60 m at the site).**
- **Effect on sizes.** In the west windows, sizes from north to south that I gave with 1.05 m and 16 degrees are approximately 13 percent too large. Sizes from west to east are correct to 1 percent.

## 5. Tile A017e (Kafrein window, 1 December 1974)

- First I made a fit with four control points (Tell Kafrein, the centre of the dam crest, the Plateau Fort, Tell el-Hammam; positions from the elevation model and the paper). Then I made the automatic fit. The two agree to 25 m at all points.
- Scales: 0.932 m and 0.839 m. The old value was 1.09 m from one short base line. That value was wrong.

| Thing on the image | Position by the new transform | Compare | Difference |
|---|---|---|---|
| Habbasa, row of cisterns | 31.8397 N, 35.6792 E | Paper: 31.8393 N, 35.6793 E | 45 m |
| Round mound | 31.8260 N, 35.6446 E | Tell er-Rameh, model and published: 31.8257 N, 35.6443 E | 45 m |
| Oval mound | 31.8307 N, 35.6484 E | Hill of the model: 31.8299 N, 35.6496 E | 145 m |

- **Status: Checked (error approximately 20 to 50 m between the control points).**

## 6. Tile A015c (Kafrein window, 25 June 1974)

- The automatic fit (11 points) and the four-point fit of the earlier note agree to 50 m at the control points and to 90 m at the mounds in the south.

| Thing on the image | Four-point fit | Automatic fit | Compare |
|---|---|---|---|
| Barakat, curved scarp | 31.8532 N, 35.6732 E | 31.8527 N, 35.6733 E | Paper grid: 31.8497 N, 35.6719 E (340 to 385 m south) |
| Habbasa, dark block | 31.8393 N, 35.6789 E | 31.8393 N, 35.6793 E | Paper grid: 31.8393 N, 35.6793 E |
| Round mound | 31.8244 N, 35.6433 E | 31.8249 N, 35.6441 E | Tell er-Rameh: 31.8257 N, 35.6443 E (95 m) |
| Oval mound | 31.8296 N, 35.6485 E | 31.8299 N, 35.6491 E | Hill of the model: 31.8299 N, 35.6496 E (45 m) |

- **Status: Checked (error approximately 30 to 100 m).**

## 7. Effect on the place names

| Place | Before | Now |
|---|---|---|
| Tell er-Rameh = the round mound beside the straight road | Probable | **Checked** (position on two tiles, form on the frames of 1998) |
| The oval mound | Possible for Tell er-Rameh | Not Tell er-Rameh. It is a different hill, approximately 500 m to the north-east |
| Mar Saba on tile F018b | Checked by position (one source of control) | Checked (independent registration, 30 m) |
| Barakat, grid reference of the paper | Probable error of approximately 400 m | No change (340 to 385 m) |
| Tell Iktanu | Possible | Possible (no change). The position of the road works must be calculated again with the new transform |
| Deir Hajla | Probable | Probable (no change) |

## Not done

- A plan or a scaled modern image of the present monastery of Deir Hajla. Three searches gave no plan of the compound.
- A transform for the east part of tile F018b (the Khirbet Mazin and east-shore windows) with more points. It needs a term for the change of scale along the tile.
- The other windows of tiles A017e and F017b (east bank), and tiles F017c and F018c (Machaerus, Callirrhoe).
- New positions for all things in the older notes. The older notes are not changed. Positions in them have these errors: tile A015c with two points, 100 to 500 m; tile A017e with one scale, to 400 m in the south; tile F018b with 1.05 m and 16 degrees, to approximately 150 m.

## Files

Drive `08 Working files/hexagon windows 2026-11-10`:
- `A015c_jun74_marked_elevation_model_transform_2026-11-11.jpg` (yellow = seen on the image; blue = position from the model or the paper, put on the image by the new transform)
- `A017e_dec74_marked_elevation_model_transform_2026-11-11.jpg`
- `hexagon_elevation_model_registration_2026-11-11.py`

## Sources

- Copernicus GLO-30 elevation model, tile N31 E035 (Drive, `07 Maps and GIS`).
- Prag and Barnes 1996, Levant 28 (Drive).
