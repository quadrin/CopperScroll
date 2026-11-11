# Six next steps: results — 11 November 2026

The owner asked for all six steps of my list. This note gives the result of each step. The older notes are not changed.

## Result first

| Step | Result | State |
|---|---|---|
| 1. Site table and GIS layer | 25 places with status, position and error, as CSV, GeoJSON and KML | Done |
| 2. Water works at the candidate places | 18 image chips with world files for a GIS; corrected sizes of the water features | Done in part: no new plan overlays |
| 3. The same place at different dates | Five pairs of 25 June and 1 December 1974 at the same scale, north up | Done for 1974 only; CORONA 1967 and the frames of 1918 not done |
| 4. Comparison with the scroll entries | **Correction: the project has this already** (the regional atlas and checklist). I made a list of effects on its site records | Done as a list of proposals; no rating changed |
| 5. Technical improvements | **A height term corrects the relief displacement** (Machaerus: from 213 m to 34 m). A file with all transforms. A cut script for three new windows | Done |
| 6. Items for other people | One document in the Drive root: places for a ground visit, a draft note on the Barakat grid reference, a draft order for the HUJI scans | Done; nothing was sent |

## Step 1. The site table

- Folder: Drive `07 Maps and GIS/Project site layer and HEXAGON chips 2026-11-11`.
- Files: `copper_scroll_sites_2026-11-11.csv`, `.geojson`, `.kml`. Coordinates are WGS 84.
- Each place has: name, other names, status, type, latitude, longitude, error in metres, source of the position, image tile, and one line of notes.
- 25 places: 8 on the west side (tile F017b), 3 on tile F018b, 13 at the mouth of Wadi Kafrein, and Machaerus.
- **Use this table for positions.** The older notes have old values.
- Not in the table: Tell es-Samarat and the sugar mill (Possible; I did not have their pixels), Callirrhoe, and the places of the notes on the east shore.

## Step 2. Water works

### Image chips for a GIS

- Folder `chips/`: 18 chips of 1,000 to 1,400 pixels, each with a world file (`.jgw`) and a projection file (`.prj`, EPSG:2039). A GIS program puts each chip at its place, with the two scales and the turn.
- West side: Tulul Abu el-ʿAlayiq, Birket Musa, Tell es-Sultan, the Quruntul summit, Qumran, ʿEin Feshkha, Deir Hajla, Hyrcania, Mar Saba, Khirbet Mazin.
- East bank: Habbasa, the Plateau Fort, the dam with Barakat, Tell er-Rameh (two dates), and Tell Iktanu (June).
- With these chips, a plan from a publication can be put on the image in the GIS, at its true scale. I did not make new overlays in this session.

### Corrected sizes of the water features

| Feature | Older value | Corrected value | Published |
|---|---|---|---|
| Birket Musa | 174 m by 143 m | 171 m by 145 m | 172 m by 144 m (Survey) |
| Hyrcania, the hollow of the two reservoirs | approximately 48 m | approximately 47 m (west to east) by 42 m (north to south) | Not compared (the hollow is one shadow) |
| Hyrcania, the last part of the aqueduct course | approximately 540 m | approximately 530 m | — |
| Habbasa, the row of chambers | approximately 50 m long; each 8 to 10 m wide | approximately 42 to 47 m long; each 7 to 9 m wide | Five cisterns; no size published |
| Barakat, the lower enclosure | approximately 50 m by 60 m | approximately 45 m by 50 m | 2,763 m² |
| Khirbet Mazin, the hollow | 57 m by 34 m | No change | Building 47 m by 23 m |

- The directions of the Habbasa row and of the Barakat enclosure are not in line with north. Thus I give a range.

## Step 3. The same place at two dates

- Folder `date_pairs/`: Habbasa, Barakat with the end of the dam, the Plateau Fort, Tell el-Hammam, Tell er-Rameh.
- Each file has the image of 25 June 1974 on the left and the image of 1 December 1974 on the right, at the same scale and with north up. The two agree to approximately 30 to 40 m.
- **What the Barakat pair shows:** in June (high sun) the fort is a curved scarp only. In December (low sun) a four-sided outline with walls is clear at the same place. Thus the two dates together are better than one.
- **Not done:** CORONA 1967 (I have only small previews in this session), the frames of 1918 and of 1953, and the strips of May 1978. The registration method can be used on them when the full files are cut.

## Step 4. The scroll entries: effects on the atlas and checklist

**Correction.** I said that no comparison with the scroll entries was made. That was true only for my image notes. The project has the *Regional atlas and dated checklist* (edition of 9 November 2026, 366 sites) with a record and a rating for each place. Thus this step is a list of what the image work adds to those records. **I changed no rating and no status.** The record numbers are from the text of the atlas file; the owner must check them, because the page layout has two columns.

| Atlas record | What the image work of 10 and 11 November adds | Proposal |
|---|---|---|
| sit0098 Hyrcania / Khirbet el-Mird | Checked on the image of 1974 with the plans of Wright and Patrich. Position 31.7192 N, 35.3659 E. The two reservoirs were open and not filled in 1974 | Add the position and the image reference |
| sit0099 Hyrcania aqueducts | Northern aqueduct: one line of approximately 1.1 km, Probable (channel or path). Southern aqueduct: not visible at 1 m | Add as an image observation; no change of status |
| sit0100 Hyrcania saddle, paired reservoirs | The hollow is approximately 47 m by 42 m | Add the size with its limits |
| sit0103, sit0104 Mar Saba | Position Checked (31.7051 N, 35.3314 E) | Add the position |
| sit0019, sit0020 Tulul Abu el-ʿAlayiq and its pools | Plan test with Netzer 1975; the sunken garden wall and pool B107 are on the image | Small addition |
| Birket Musa (index entries idx0547, idx0548) | 171 m by 145 m on the image; position 31.8479 N, 35.4402 E | Supports a site record (proposed on 9 November) |
| sit0023, sit0024 Qarantal / Dok | The summit enclosure on the image is the modern wall. It is not evidence for the fort | No change; agrees with the note of 9 November |
| sit0079 Khirbet Qumran; sit0088 ʿEin Feshkha main building | The two are Checked on the image with plans. Route 90 was built over the west enclosure of ʿEin Feshkha before 1974 | Add as a record of the state in 1974 |
| Deir Hajla (sit0022 or sit0039; "region only: no individual map point") | Position 31.8200 to 31.8204 N, 35.5014 E; compound 40 m by 70 m; the present buildings are of 1882 to 1885 on the medieval plan | **Give the record a map point** |
| sit0057 Nebi Musa | Position 31.7867 N, 35.4317 E; compound approximately 70 m by 67 m; no plan test | Add the position |
| Khirbet Mazin (idx2069, "Undated …") | Checked with the report of 2024; position 31.6819 N, 35.4429 E | Add the report and the position |
| Chapter 11: Tall Barakat (Survey site 178) | The fort is at 31.853 N, 35.673 E. **The grid reference of the publication is approximately 400 m too far south** | Correct the map point; keep a note on the conflict |
| Chapter 11: Khirbat al-Habbasa (Survey site 180) | A row of four or five roofless chambers on the image of December 1974, Checked with the plan; position 31.8396 N, 35.6793 E | Add; the cistern sizes are still not known |
| Chapter 11: Tell er-Rameh | The round mound beside the road, Checked; 31.8257 N, 35.6443 E. No water work is visible in 1974 | Add |
| Chapter 11: Umm Hadar (Survey site 118) | Hill Probable; the dark patch is at 31.8630 N, 35.6754 E (changed by 500 m today) | Add with caution |
| Chapter 11: Machaerus | Identified on the image of 1974, before the excavations; two open holes on the north-east slope | Add |
| Not in the atlas: Tell Iktanu | Probable; 31.8192 N, 35.6713 E | No record is necessary (no built water store) |

**What the image work does not give:** a date for any feature, a size for a closed cistern, and a link to a scroll entry. Those stay with the text work and the excavation reports.

## Step 5. Technical improvements

### The height term

- The images are panoramic and not vertical. A point that is higher than the mean ground moves on the image.
- I added one term to the fit: the position changes by a fixed vector for each metre of height (the height is from the elevation model).

| Tile and windows | Error without the term | Error with the term | Vector for each metre of height (east, north) |
|---|---:|---:|---|
| F018c, Machaerus window | 79 m | 31 m | 0.54 m, 0.19 m |
| F017b, west windows | 47 m | 26 m | 0.56 m, −0.01 m |
| A017e, Kafrein and Rameh windows | 24 m | 19 m | 0.32 m, −0.07 m |
| F018b, west windows | 13 m | 12 m | 0.27 m, 0.03 m |

- **Test:** the top of Machaerus was 213 m from the summit of the elevation model. With the height term it is 34 m.
- The chips of step 2 use the height term where it is fitted.
- **Limit:** the height term moves low places also. For ʿEin Feshkha (−390 m) the longitude changes by approximately 150 m to the west against the fit without the term. I do not know which value is better there. The site table has the value without the term, with an error of 60 m; this error is possibly too small for ʿEin Feshkha and Khirbet Mazin.

### Files

- `hexagon_1974_transforms_2026-11-11.json`: all transforms, with the height term.
- `cut_dec1974_by_position_2026-11-11.sh`: cuts three full-size windows that we do not have: Nebi Musa (tile F017b), Tell Iktanu and the Umm Ḥadhar hill (tile A017e, December). The owner runs it in the Mac Terminal. I did not test it; it has the same form as the earlier scripts.

## Step 6. Items for other people

- File in the Drive root: `Copper Scroll – items for other people (field checks, Barakat note, HUJI order) – 2026-11-11.md`.
- Part 1: seven places for a ground visit or a drone flight, with positions and what to record.
- Part 2: a draft note to K. Prag on the grid reference of Tall Barakat.
- Part 3: a draft order for larger scans of the 19 Jerusalem air photographs.
- **Nothing was sent.** I did not look up addresses.

## Not done

- New plan overlays in the GIS (Hyrcania, the Jericho palaces, Habbasa) with the corrected transforms.
- CORONA 1967, the frames of 1918 and 1953, the strips of May 1978.
- The atlas itself is not changed. The record numbers in step 4 must be checked.
- The older notes are not changed.
- The transfer file `gis_layer.tar` is in the GIS folder. The owner can delete it.
