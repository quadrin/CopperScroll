# HEXAGON 1974 and 1978 images registered to the elevation model — 11 November 2026

**Kind of work:** exploratory image analysis by one reader (Claude), not blind. It tests no registered prediction and changes no rating. It gives positions, sizes and image observations for places that the project records already name. It gives no date for a feature and no link to a scroll entry.

## What was done

1. Declassified satellite images (KH-9 HEXAGON, 25 June 1974, 1 December 1974 and 5 May 1978) were registered to the Copernicus GLO-30 elevation model. The image is compared with a shaded-relief picture of the model, block by block; each block gives one control point; an affine transform is fitted to all points. A height term corrects the relief displacement of the panoramic camera.
2. With the transforms, the images were rectified (north up, fixed scale). Published plans were then put on the images with the scale of their scale bar and the north of their north arrow, with one free anchor point.
3. The positions of 29 places were put in one site table.

## Main results

| Result | Evidence | Limit |
|---|---|---|
| Eleven window transforms for 1974 and one for 1978; errors of 16 to 76 m (root mean square) | `transforms.json`, notes 01, 02, 06 | Each transform is good in its windows only: the scale changes along a panoramic tile |
| The height term lowers the error (for example from 79 m to 31 m at Machaerus; the hilltop error goes from 213 m to 34 m) | note 03 | For places far below the mean ground (the Dead Sea shore) the corrected and uncorrected values differ by approximately 150 m; which is better is not known |
| Tall Barakat is at approximately 31.853 N, 35.673 E. The grid reference in Prag and Barnes 1996 (213700 / 139750) falls approximately 340 to 385 m south of it | notes 01, 02, 05, 06 | One line of evidence: the form on the image against figure 13. No ground point. The citadel line of the plan is 15 to 20 degrees different from the ridge |
| Khirbat al-Habbasa: a trapezoid enclosure with a row of four or five roofless chambers, 45 to 48 m long, on 1 December 1974. Figure 9 of Prag and Barnes agrees with true scale and north, to approximately 10 m | note 05 | The sizes of the cisterns are not known |
| Tulul Abu el-ʿAlayiq: figure 2 of Netzer 1975 agrees with true scale and north (mound, Wadi Qelt banks, sunken garden, road) | note 05 | Building B is under an orchard on the image |
| Hyrcania: figure 1 of Wright 1961 agrees with north at the top of its page. Figure 22 of Patrich 1989 must be turned approximately 40 degrees | notes 05, 07 | For the plan of Patrich two anchors were necessary |
| Tell er-Rameh is the round mound beside the straight road (45 to 95 m from the published point on two dates). Tell Iktanu (north hill) is the long hill north-west of the highway, with one rectangular outline of approximately 45 m by 30 m on its top | notes 01, 02, 06 | No plan test for either |
| Deir Hajla, Nebi Musa, Mar Saba, Khirbet Mazin: positions agree with published points to 30 to 60 m | notes 01, 02, 06 | Position only |
| 5 May 1978 at Jericho: the excavated areas agree with six area plans of Netzer 2001, placed by the site grid (10 m squares, turned 13 degrees east of north) with one anchor from plan 14. Pools Complex, Twin Palaces and Northern Wing: agreement 5 to 15 m | notes 08 to 11 | Plans were photographed obliquely and corrected from their grid borders; grid lines marked by eye; one reader. Areas AA and AC and the Second Palace are Probable only |
| CORONA, 26 September 1967, strip DF041 tile d: registered to the HEXAGON images (341 blocks, 16 m, west side; 136 blocks, 17 m, Kafrein). No Kafrein dam and no reservoir on this date; the square outline of the Plateau Fort is present | notes 08, 09; `transforms_corona_1967_df041d.json` | Approximately 2.1 m for each pixel: position and land use only. Two transforms; no control at Shunat Nimrin |
| Nebi Musa: wall lengths on the image of 1 December 1974 (66–70, 67, 66, 53 m) against published 74, 70, 68, 55 m | note 11 | Published values from a web page; primary survey not seen |
| Tell Iktanu: a lower second summit at 31.8163 N, 35.6682 E, south-east of the highway (elevation model) | note 11 | Probable south hill of the Prag monograph; her plan not seen |

## Corrections to earlier statements of the same day

The notes were written in steps, and later steps corrected earlier ones. Note 04 lists, for each older project note, what is replaced. The most important: a two-point transform of the June 1974 tile was wrong by 100 to 700 m; one mound was first taken for Tell er-Rameh and a group of military works for Tell Iktanu.

## Files

| File | Content |
|---|---|
| `sites.csv`, `sites.geojson`, `sites.kml` | 38 places: status, type, WGS 84 position, error, source of the position, note |
| `transforms.json` | Pixel-to-grid transforms (EPSG:2039) for each tile and window, with the height term where fitted |
| `regional_checklist_change_list.csv` | 20 proposed additions to the records of the regional checklist. **The record numbers were read from a two-column PDF and are not checked** |
| `scripts/` | Registration (`demtool.py`, `warp.py`, `reg.py`, `auto.py`, `reg2.py`), rectified chips and overlays (`chips.py`, `pairs.py`, `ov.py`), and the cut scripts that the owner ran on the full tiles |
| `notes/` | The eleven working notes, in order. They are written in simplified technical English |
| `figures/` | Four date pairs: the Kafrein dam site (1967 and 1974); Nebi Musa (1974 and 1978); Barakat with the end of the Kafrein dam (June and December 1974); Tulul Abu el-ʿAlayiq (December 1974 and May 1978) |

The scripts have the paths of the session that made them; they are a record of the method, not a package.

## Sources and rights

- HEXAGON and CORONA images: declassified United States government imagery, distributed by the USGS.
- Elevation model: Copernicus GLO-30 (© DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018, provided under COPERNICUS by the European Union and ESA).
- Plans compared: Netzer 1975 (IEJ 25), Prag and Barnes 1996 (Levant 28), Wright 1961 (Biblica 42), Patrich 1989. The overlays with these plans are not in the repository.
- Status words: Checked (compared with a plan, a report or an independent position), Probable, Possible, Seen.
