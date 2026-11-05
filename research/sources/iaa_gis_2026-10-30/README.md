# IAA public GIS layers and the Discover survey register, 30 October 2026

**What it is.** These are two scrapes of public Israel Antiquities Authority (IAA) services, made on 30 October 2026.
- `spatial/` holds four public IAA map layers, cut to a window around the project's candidate places:
  - CaveAtlas: 151 caves;
  - Operation Scroll survey points: 83;
  - Archaeological Survey of Israel (ASI) site points: 1,048 within 3 km;
  - declared antiquities sites: 1,491 within 3 km.
- `discover/` holds the IAA Discover survey register: 57 cave and Judean Desert survey records, with 80 permit rows.

Both are location and administrative indexes. They date no cave, identify no findspot, and change no candidate, rating, coordinate or count.

**Where the full copy is.** The complete scrape, including the raw layer dumps, is in Drive at `03 Surveys, gazetteers and reference/IAA GIS layers and Discover register (2026-10-30)` ([folder](https://drive.google.com/drive/folders/10W-phyNoVJAFOmjJMats9LjHyUKO4Yb2): [iaa-spatial](https://drive.google.com/drive/folders/1KxPr8bQUIowBB_grdRYIRvw8dDGV8YOG), [iaa-discover](https://drive.google.com/drive/folders/1nmE2CFe8g9gxUZKkRc5EFmeo4Vl3raKh)). The Drive copy is byte-identical to the working copy on the owner's Mac.

## What is in the repository and what stays in Drive

| In this folder | Drive only, and why |
|---|---|
| Scripts: `spatial/scrape_gis.py`, `spatial/build_cave_crosswalk.py`, `discover/scrape_iaa.py` | `asi_sites.csv` (1,048 rows) and `declared_sites.csv` / `.geojson` (1,491 polygons). They carry the IAA's descriptive text: ASI remains, descriptions and bibliography, and Hebrew site descriptions. The repository already limits how much ASI description text it reproduces (see [ASI Jerusalem](../../regional/asi_jerusalem/README.md)). |
| `spatial/data/cave_atlas.csv`: 151 caves, with name, ITM coordinates, elevation and excavated flag | `discover/data/hadashot/`: the text and figures of the Naḥal Ḥever report (© IAA) |
| `spatial/data/megila_survey_points.csv`: 83 points | `discover/scrape_hadashot.py`. It reads `hadashot.iaa.org.il`, whose robots.txt admits only search engines ([first tests, limits](../../first_tests_2026-10-24/README.md#limits)). |
| `spatial/data/cave_crosswalk.csv` and its summary | `places.csv` and `repo_caves.csv`: snapshots of repository tables that are already here |
| `spatial/data/place_coverage.csv`: counts per place at 1 km and 3 km | |
| `discover/data/surveys.json`, `survey_licenses.csv` and the manifests | |

One change was made to the repository copy. `discover/scrape_iaa.py` now sends the same honest user-agent string as `scrape_gis.py`; the Drive copy sent a desktop-browser string.

The ArcGIS app key is read from `https://discover.iaa.org.il/api/config/gis.js` each time the script runs. No key is stored.

## Results checked against the repository (30 October)

The cave offsets and the Operation Scroll join were recomputed from [`research/regional/caves_entry25/caves.csv`](../../regional/caves_entry25/caves.csv), not copied from the scrape's own report. The Green Line figures come from `spatial/data/place_coverage.csv`.

**The IAA cave atlas and the repository's 1952 de Vaux points disagree by about 230–260 m at the two manuscript caves that can be compared.**
- The Copper Scroll Cave (atlas name `מערת מגילת הנחושת Q3`, ITM 243685/629635) is **233 m** from `DJD3:8`.
- Atlas Q1 is **257 m** from `DJD3:14`.
- The register gives those rows a precision of 30 m.
- Neither source states how its point was derived. The offset bounds how precisely either point can be used; it does not show which one is right.

**The Operation Scroll points confirm the repository's ʿAtiqot 41 coordinates.**
- Their cave numbers are ʿAtiqot 41 numbers written in reverse order (`49/XII` = `A41:XII/49`).
- 72 of 83 points join on that number. Their median offset is **2.6 m**, and 70 of 72 are within 30 m.
- Two disagree: `A41:X/13` by 504 m and `A41:X/49` by 10.0 km. One source has a wrong coordinate in each case, and this check does not show which.
- 11 points do not join: eight single caves with no register row, and three combined numbers that the register splits.
- `XI/19` (2Q) agrees to 3 m, but both sources repeat the same misprinted grid. They are one witness, not two.

**Other cave matches by name are close.**
- Sandal Cave 2 m, the Spies complex 44 m, the Cave of Letters 88 m, the Twin complex 110 m, and the Balsam Oil Juglet Cave 308 m.
- The large offsets are therefore at the Qumran cliff points, not a datum shift across the whole layer.
- The atlas has a point for **de Vaux site 24**, which has no register row.

**The declared-sites layer stops at the Green Line.**
- All 12 located Jericho-group places return no polygons, and neither do Mar Saba, Hyrcania, Buqeia, Natuf, Gerizim or Ibziq. That is a jurisdiction boundary, not an archaeological absence.
- ASI points do cross the line: 18 near Tell es-Sultan and 2 at Kh. Qumran.

## Tell es-Sultan

`place_coverage.csv` counts 18 ASI points and 4 atlas caves within 3 km of Tell es-Sultan. This is open material: the SULTAN-1 blind-test rules were retired on 30 October 2026.

## Proposed register changes (not applied)

1. `DJD3:8` and `DJD3:14`: record the IAA atlas point as a second, independent locate point, with the 233 m and 257 m offsets.
2. `A41:X/13` and `A41:X/49`: check the printed ʿAtiqot 41 grid against the IAA point.
3. De Vaux site 24: add a row from the IAA atlas point, marked as atlas-derived.

## Rerun from the repository

```
python3 research/sources/iaa_gis_2026-10-30/spatial/scrape_gis.py --places tables/phase3_places.csv --out /tmp/iaa_spatial
python3 research/sources/iaa_gis_2026-10-30/spatial/build_cave_crosswalk.py --atlas /tmp/iaa_spatial/cave_atlas.csv --repo research/regional/caves_entry25/caves.csv --out /tmp/iaa_spatial/cave_crosswalk.csv
python3 research/sources/iaa_gis_2026-10-30/discover/scrape_iaa.py
```

Both `spatial` scripts use only the Python standard library. The layers are live services, so a later run can return different rows. Each run's date and feature counts are in `spatial/data/manifest.json`.

## Limits

- **Caves are not dated.** CaveAtlas and the Operation Scroll points carry a name, a point, an elevation and an excavated flag; nothing dates a cave's use. The elevation datum is not stated.
- **Polygons are not boundaries.** The declared-site polygons are grid cells of about 20 m, not site boundaries. Do not measure site areas from them.
- **ASI coverage is uneven.** It follows the published survey sheets. The Jericho and Qumran–Feshkha sheets are not online, so silence there is silence of the sheet, not absence of sites.
- **Recent Qumran cave work is missing.** It was done under Civil Administration licences (07-03-2017, 06-03-2018, 01-04-2018) and appears in none of these layers.
- **Discover survey 4477322 is not public.** Its record returns HTTP 403, so its title is unknown.
- **The `gis.israntique.org.il` services were not read.** They need an internal token.
- The detailed method and the original findings are in [spatial/README.md](spatial/README.md) and [discover/README.md](discover/README.md). Those READMEs list some files that exist only in the Drive copy; the table above says which.
