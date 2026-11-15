# New sources of 15 November (Papyri.info, Palestine Open Maps 1945 gazetteer, UK National Archives, GLiM, JRC Global Surface Water): checked in the bucket. The surface-water rasters have no data north of 30° N, so they do not cover the project area. GLiM is too coarse at the places. No change — 14 November 2026 (night, PT)

The other session reported five new sets. I checked them in the bucket, compared them with Drive, and made a first use at the 34 candidate places that have a point.

## Result first

1. **All five sets are in the bucket, and the counts agree with the report.** Papyri.info 50 texts; Palestine Open Maps 2,543 localities (2,534 in the study box); National Archives 709 records (445 after the filter); GLiM 351 polygons; JRC surface water 3 rasters. `blocked-2026-11-15.md` is at the top of `open-sources/`.
2. **The JRC Global Surface Water rasters do not cover the project area.** All three rasters have data only from 29.40° to 30.00° N (the Gulf of Aqaba). From 30° N to 33.6° N every cell is "no data" (255). There is no water within 5.5 km of Kh. Qumran, ʿAin Feshkha, ʿAin es-Sultan, ʿAin Duk, Kh. el-Mird, or the Jordan east of Jericho, not even the Dead Sea. The probable cause is the tile choice: the README names tiles `30E_20N` and `30E_30N`. JRC tiles are named by their north-west corner, so the project area (31–33° N) is in tile `30E_40N`, which was not downloaded. **Not usable until that tile is added.**
3. **GLiM is too coarse at the candidate places** (1:1,000,000). It puts Tell es-Sultan, Jericho and Tell el-Qos on carbonate rock, where GSI 1:200,000 has Lisan marl. It puts Kh. Qumran, Wadi Qumran, the Cave 3Q point and ʿAin Feshkha inside its Dead Sea "water body" polygon (Cave 3Q is about 90 m inside its edge). **No candidate place in the table is on the east bank**, so its Transjordan cover has no use for the present ratings. Keep it as a regional layer only.
4. **Palestine Open Maps 1945 gazetteer: usable, small use now.** The nearest 1945 localities to the candidate places agree with the project names (for example Jericho 3,010 people in 1945; Nuʿeima 240; Duyuk 130; Ibziq). Only 1,009 of the 2,534 rows have a 1945 population. The other rows include modern settlements and neighbourhoods (for example Pisgat Zeʾev, Tkoʿa), so filter on the 1945 fields before use. The table has no licence file; it must not be published.
5. **National Archives: three records bear on the history of the Copper Scroll**, all catalogue entries only, not digitised: the John Allegro research papers (JMA, 1950–70, University of Manchester Library); the W. H. Brownlee Dead Sea Scrolls papers (WHB, same library); and the Royal Institution file of Sir Lawrence Bragg's correspondence with Allegro, 31 May 1957 to 12 February 1958, with letters from Kenyon and Harding (W.L. BRAGG/93A/36-51). Also Treasury and Foreign Office files on the purchase and editing of the scrolls, 1959–66 (T 218/371, T 218/438, T 218/692, FO 924/1316, FO 924/1387, FO 924/1540, FO 371/186611). None gives a place for a scroll entry.
6. **Papyri.info: metadata only.** 8 records are P. Jericho (Greek, 2nd century CE). One record is from Pathyris in Egypt: a false positive of the filter. No text, so no place names to compare.
7. **Library of Congress: the report says that the scripts are in `open-sources/loc/`. That folder is empty in the bucket.**
8. **No rating, candidate or match strength was changed.**

## Table: new layers at the candidate places

`new_datasets_at_places_2026-11-14.csv` (34 places with a point; jer_shaveh, tekoa_herodium and jordan_ford have no point). Columns: GLiM class, GSI unit (from the note of 14 Nov), surface water at the point and within 300 m (all empty, see result 2). The repository copy leaves out the nearest-1945-locality column, because the gazetteer has no licence; the Drive copy has it.

## Limits

- One reader. The surface-water result was checked over the whole raster (rows with data by latitude), not only at the places.
- GLiM and GSI were compared at points only.
- The National Archives records were screened by keyword in the title and description.

## Not done

- Download of JRC tile `30E_40N` and new clips. (This needs a download to the cloud workspace or the other session; storage.googleapis.com may be reachable from there.)
- A name check of the 1945 gazetteer (Arabic and Hebrew forms) against the atlas place names.

## Where the files are

- Bucket: `open-sources/{papyri,pom,tna,glim,gsw}/`.
- Drive, tables folder: `new_datasets_at_places_2026-11-14.csv`.
- Session: `/home/claude/cs/os4/` (`first_use.py`, `dl/`).

No rating or candidate was changed.
