# IAA public GIS intake

**What it is.** A place-keyed extract of four public IAA map layers, windowed to
the 37 places in `tables/phase3_places.csv` (34 with coordinates). It is a
spatial index, not a corpus: every row is a site, cave or polygon with a
coordinate, a distance to the nearest project place, and IAA's own name,
period, remains and bibliography fields where those exist.

**Why this layer.** The repository already holds the publication side — HA-ESI
features, the ASI Jerusalem sheets, ESI and Atiqot reports. What it did not hold
is the IAA's own structured site register with geometry. That is what these four
services provide, and it covers all places rather than one.

**Main result.** 1,048 ASI survey sites and 1,491 declared antiquities sites
fall within 3 km of a project place, alongside 151 Judean Desert caves and 83
Operation Scroll survey points. The cave layer names the Copper Scroll Cave
(`מערת מגילת הנחושת Q3`) and fixes it at ITM 243685/629635, 233 m from the de
Vaux point 8 as digitized in `research/history/devaux1952_cave_points`
(31.76022, 35.45809). The declared-sites layer stops at the Green Line: all 12
Jericho-group places return zero polygons.

**What stays unknown.** None of these layers dates a cave, identifies a
findspot or supplies an excavation boundary. The declared-site polygons are
coarse (~20 m grid cells), not site boundaries. ASI coverage follows published
survey sheets; silence is silence of the sheet, not absence of a site. No layer
here can change a candidate's confidence, geometry or entry count.

## Layers

| Layer | Features | Geometry | What it carries | Output |
|---|---|---|---|---|
| `CaveAtlas` | 151 | point | Cave name, ITM X/Y, elevation, excavated flag, source (`אטלס מערות`) | `data/cave_atlas.csv` |
| `MegilaSurveyPoints` | 83 | point | Operation Scroll cave number (X, XI, XII series), type, excavated flag | `data/megila_survey_points.csv` |
| `SURVEY_MAPS_SITE_POINTS_PUBLIC` | 23,312 | point | ASI site number, map sheet, name, period, remains, description, bibliography, WGS84 + ITM | `data/asi_sites.csv` (windowed) |
| `HACRAZOT_PUBLIC1` | 31,594 | polygon | Declared antiquities site number, Hebrew name, short Hebrew/English description | `data/declared_sites.csv`, `.geojson` |

Endpoints are the public ArcGIS services behind `discover.iaa.org.il`. The
public app key is read at run time from
`https://discover.iaa.org.il/api/config/gis.js`; nothing is hard-coded.

## Files

| File | Rows | Notes |
|---|---|---|
| `data/cave_atlas.csv` | 151 | All caves in the layer, sorted by distance to the nearest place |
| `data/megila_survey_points.csv` | 83 | All Operation Scroll points |
| `data/asi_sites.csv` | 1,048 | Sites within 3 km of any located place, deduplicated by OBJECTID |
| `data/declared_sites.csv` | 1,491 | Same window, Israel-side only |
| `data/declared_sites.geojson` | 1,491 | Polygon geometry, WGS84 |
| `data/place_coverage.csv` | 37 | Per-place counts at 1 km and 3 km, plus coverage flag |
| `data/places.csv` | 37 | Snapshot of `tables/phase3_places.csv` used for this run |
| `data/repo_caves.csv` | 665 | Snapshot of `research/regional/caves_entry25/caves.csv` (join target) |
| `data/cave_crosswalk.csv` | 151 | IAA cave → repository cave register → de Vaux site |
| `data/manifest.json` | — | Run time, layer metadata, field lists, counts |
| `scrape_gis.py` | — | Reproducible scrape, standard library only |
| `build_cave_crosswalk.py` | — | Reproducible crosswalk, standard library only |

`places_within_radius` lists every place whose 3 km window contains the row.
`nearest_place` is purely geometric and can be misleading: the Copper Scroll
Cave is nearer to `asla` (1,638 m) than to `kh_qumran` (1,922 m).

## Cave crosswalk

`data/cave_crosswalk.csv` links the 151-point IAA cave atlas to the repository's
own register (`research/regional/caves_entry25/caves.csv`, vendored as
`data/repo_caves.csv`). Matching uses explicit identifiers only: a Q siglum in
the IAA name, a de Vaux site number, or a curated name alias. Distance never
creates a match; the nearest register row is reported in its own columns as a
lead.

16 caves match, 9 of them with coordinates in both sources.

| IAA cave | Siglum | de Vaux | Register row | Offset |
|---|---|---|---|---|
| מערת מגילת הנחושת Q3 | 3Q | 8 | `DJD3:8` | **233 m** |
| מערת קומראן Q1 | 1Q | 14 | `DJD3:14` | **257 m** |
| מערת קומראן Q2 | 2Q | 19 | `A41:XI/19` | 4,540 m¹ |
| מערת קומראן ליד Q6 | near 6Q | 26 | `DJD3:26` | 157 m |
| מערת קומראן Q11 | 11Q | — | `DJD3:11Q` | no coordinates |
| מערת קומראן 24 | — | 24 | *(no row)* | gap |
| מערת הסנדל | — | — | `A41:VIII/28` | 2 m |
| מכלול המרגלים-אביאור | — | — | `A41:VIII/9` | 44 m |
| מערת האגרות | — | — | `ASI:147-429` | 88 m |
| מכלול התאומות | — | — | `REPO:TwinCave` | 110 m |
| מערת פכית שמן האפרסמון | — | — | `A41:X/35` | 308 m |

¹ The register's own `coord_ok` field is `no` and its `coord_basis` calls the
printed grid a misprint, so the 4.5 km is a known defect in the register row,
not a substantive disagreement.

**What this adds.**

- The two manuscript caves that can be compared both sit about 230–260 m from
  their register points — eight times the register's stated 30 m precision.
  The IAA atlas is therefore a second, independent locate point, not a
  refinement of the de Vaux digitization.
- The offsets are not a uniform datum shift. Other matched pairs in the same
  crosswalk are 2 m (Sandal), 44 m (Spies), 88 m (Letters) and 110 m (Twin).
  The method can be precise; the Qumran cliff points are the weak ones.
- The IAA atlas holds a point for de Vaux site 24, which the register has no
  row for. That is a gap fill, and the only one in this pass.
- Q2 is the exception in the other direction: the register's coordinate is
  already flagged inaccurate, and the IAA point is 4.5 km away at the Qumran
  cliff where 2Q belongs. This crosswalk is the first place the two are put
  side by side.

**What it cannot do.** None of the three sources states how its point was
derived. The 233 m bounds the disagreement between two locate points; it does
not say which is closer to the cave entrance, and it is not a survey.

### Cross-check against `MegilaSurveyPoints`

The 83-point `MegilaSurveyPoints` layer is not a fourth register. Its numbers
are Atiqot 41 cave numbers written the other way round (`53/X` = `A41:X/53`),
so it is a point subset of the same 1993 survey the repository already records.
Joining on that number (72 of 83 rows join) tests the A41 coordinates:

- **70 of 72 pairs agree within 30 m; the median is 3 m.** The repository's
  A41 coordinates are not a loose digitization.
- Two are broken: `A41:X/49` is **10.0 km** away and `A41:X/13` **504 m**.
- `XI/19` (= 2Q) agrees to 3 m — with the *misprinted* coordinate. The bad
  grid reading is in the IAA layer too, so the two are copies of one error,
  not independent witnesses. Only the cave-atlas point for Q2 stands apart.
- 11 Megila points do not join on the number: eight single caves with no
  matching register row (`X/1`–`X/4`, `XI/1`, `XI/21`, `XI/22`, `XII/50`) and
  three combined numbers the register splits into separate rows
  (`2-5/XI`, `7-8/XI`, `11-12/XI`).

The practical consequence: the A41 coordinates check out to a few metres, so
the repository's coordinate work is reliable where it can be tested. The
233 m and 257 m offsets on Q3 and Q1 are therefore a disagreement between the
1952 de Vaux points and the cave atlas, not a general failure of the
digitization.

## What the extract shows

1. **The Copper Scroll Cave is in the cave atlas.** `מערת מגילת הנחושת Q3`,
   ITM 243685/629635, elevation −270 m, flagged as excavated. It sits 233 m
   from the repository's de Vaux point 8 (which the repository reads as 3Q).
   Both are locate points of unstated derivation; the offset bounds how
   precisely either can be used, and neither is a survey of the entrance.
2. **Operation Scroll is now point data.** 83 points in the X, XI and XII cave
   series, 60 of them within 3 km of Kh. Qumran; 25 are flagged excavated.
   The repository has no prior record of this layer.
3. **The declared-sites register ends at the Green Line.** All 12 located
   Jericho-group places, plus Mar Saba, Hyrcania, Buqeia, Natuf, Gerizim and
   Ibziq, return zero polygons. Their absence is a jurisdiction boundary, not an
   archaeological result. ASI points do continue across the line (18 near Tell
   es-Sultan, 2 near Kh. Qumran).
4. **ASI gives period and feature coding, not just a name.** 721 of 1,048
   windowed sites carry a period; 1,043 carry a description. Fields
   `period_en`, `remains_en`, `bibliography_en` are the join to the HA-ESI
   feature table.

## Coverage

Each row is assigned to the map group of its **nearest** project place, so the
columns sum to the unique totals. Overlaps between neighbouring places (all the
Jerusalem points) are not double-counted.

| Group | Places | ASI ≤1 km | ASI ≤3 km | Declared ≤3 km | Caves ≤3 km | Megila ≤3 km |
|---|---|---|---|---|---|---|
| Jerusalem | 15 | 177 | 612 | 1,176 | 0 | 0 |
| Jericho / Dead Sea | 13 | 33 | 102 | 0 | 15 | 81 |
| Region | 9 | 66 | 334 | 315 | 12 | 0 |
| **Total** | **37** | **276** | **1,048** | **1,491** | **27** | **81** |

Three places have no coordinates in `phase3_places.csv` and are listed as
`not assessed`: `jordan_ford`, `jer_shaveh`, `tekoa_herodium`.

## Method

```
python3 scrape_gis.py             # 3 km default, writes data/
python3 scrape_gis.py --radius 1000
python3 build_cave_crosswalk.py   # after the scrape
```

`scrape_gis.py` reads the app key, pages each query past the service record
limit, converts every geometry to WGS84 server-side (`outSR=4326`), and
computes great-circle distances locally. Distances are point-to-centroid for
polygons. Rows are deterministic: sorted by nearest place and distance, then
name.

`build_cave_crosswalk.py` matches on explicit identifiers only — a Q siglum, a
de Vaux site number, or a curated alias checked against the register's own
name/`other_ids`. Proximity is recorded but never used to create a match.

## Limits

- **No dating for caves.** `CaveAtlas` and `MegilaSurveyPoints` carry a name,
  a point, an elevation and an excavated flag. Nothing else. They cannot date
  a cave's use or tie it to a period.
- **Declared polygons are locators.** Sampled rings are ~20 m on a side; they
  look like grid cells, not surveyed boundaries. Do not measure site area from
  them.
- **The declared layer is Israel-side.** Judea and Samaria sites are absent by
  jurisdiction, not by archaeology. Recent Qumran cave licences
  (`07-03-2017`, `06-03-2018`, `01-04-2018`) are Civil Administration
  licences and appear in none of these layers.
- **ASI coverage is sheet coverage.** 23,312 points is the published subset.
  The printed Jericho and Qumran–Feshkha sheets are still not online, which is
  why Kh. Qumran returns 2 points at 3 km.
- **`nearest_place` is geometry, not attribution.** A cave or site can be
  nearer to a neighbouring project place than to the one it conventionally
  belongs to. Use `places_within_radius` and the source name.
- **Elevation datum is unstated.** The `רום` field is used as given; do not
  convert to a depth below a surface without an independent check.
- **Public guest key.** This is the same key the public map serves. Internal
  archive, excavation-file and model endpoints stay closed (HTTP 500).

## Joins to existing repository sources

| This extract | Joins to |
|---|---|
| `cave_crosswalk.repo_cave_id` | `research/regional/caves_entry25/caves.csv` (DJD3, A41, ASI, Z23 rows) |
| `cave_crosswalk.devaux_site`, `offset_m` | `research/history/devaux1952_cave_points` |
| `cave_atlas.name_heb` (Q1–Q24) | `research/history/djd3_text_cave_list_extracted.md` (siglum list) |
| `asi_sites.site_num`, `map_id` | ASI sheet and site numbers in `research/regional/asi_jerusalem` |
| `asi_sites.period_en`, `remains_en`, `bibliography_en` | `research/regional/haesi_features/data/corpus.csv` feature coding |
| `declared_sites.atar_number` | IAA declared-site number; no current repository counterpart |
| `megila_survey_points.cave_no` | No current repository counterpart |

## Provenance

Public IAA ArcGIS services, read 30 October 2026 with the public app key.
Layer counts and field lists are recorded in `data/manifest.json`. The data are
administrative and spatial metadata published by the IAA; descriptions and
bibliographies remain IAA text. Nothing in this folder is a new identification,
a findspot claim or a change to any registered result.
