# Mandate 1:20,000 map regression (Palestine Open Maps)

**What it is.** A coded reading of nine Survey of Palestine 1:20,000 sheets (1940s) around the candidate places, with a check of their published georeferencing and a comparison with SWP sheet XVIII and 2025 imagery.
**Main result.** The published tiles match the printed Palestine grid within 3–19 m (median 10 m, 46 intersections), and mapped symbols match modern features with a median of 15 m; the Tell es-Sultan registration is rejected (E_total 48.8 m), and the map prints no opening or grave in the strip north of the tell.
**What stays unknown.** A 1:20,000 symbol dates nothing; the marginal legend was not read; 32 of 125 mapped features were not classed for 2025; the strip north of the tell remains untested for SULTAN-1.

Exploratory work. No identification claim. No outcome-ledger count. No registered result changes.

## Freeze record

- plan.json SHA-256 `cb434f9c1646d51552774c39de68efef1cf2beb4c67f258bb636c3df7ffcd066`, frozen 2026-10-09T22:19:00Z, before any tile was viewed and before any residual or feature was measured.
- Tell es-Sultan declaration `research/assessments/kohlit_chain/registrations/POM-pal20k-z16-19-14.declaration.json` (SULTAN-1 copied, transform, relations, control candidates, check rule, mask): SHA-256 `085b50a3f2f53726bb0f5132f8102b102448e9ab8b84662a3fef605909c0190c`, written 2026-10-09T22:19:44Z, before any view of sheet 19-14.
- Pre-preview note `…/registrations/POM-pal20k-z16-19-14.prepreview.json` (document hash, mask placement): SHA-256 `d1e3916222a1b07ebca98fcb9ca119eb6d960a774f258f4d0acfe1a7abad1ca4`, 2026-10-09T22:40:17Z, before any view of 19-14.
- Check-point decision on the coarse masked preview `…/POM-pal20k-z16-19-14.checkpoint.json`: SHA-256 `e8bcc03159400369170827f40f6fe643bafe99c7b4fbe26c000c700608728fc5`, 2026-10-09T22:41:01Z, before any full-resolution view of 19-14.
- Section-8 record `…/POM-pal20k-z16-19-14.json`: SHA-256 `5c7b1efe0f71e18ec9cf31c918e4e7d29f1f4bc6df37b142bfedf7a1abedb42f`, 2026-10-09T22:50:20Z, before the fit. (A first save at 22:50:12Z, SHA-256 `eb807bc2…`, had a garbled source-frame sentence; only that text changed.)
- Fit saved 2026-10-09T22:50:33Z (`…/POM-pal20k-z16-19-14.result.json`). The zone was first viewed at 2026-10-09T22:51:12Z.

## What Palestine Open Maps offers (read 9 October 2026)

- **Raster tiles** of the 1:20,000 series: `https://palopenmaps.org/tiles/pal20k-1940s/{z}/{x}/{y}.jpg`, Web Mercator, zoom 16 at most (about 2.0 m per pixel). The scans are credited to the National Library of Israel. Each sheet appears in one edition only. Where two files exist (19-13, 19-14: undated and 1942), the served edition was not determined.
- **Sheet downloads**: per-sheet JPEGs on Dropbox shared-folder links. Dropbox's robots.txt disallows `/sh/` for general agents, so none was fetched. The owner's Drive holds 16 sheets; the Drive tool returns base64 only, so they were not fetched either.
- **Thumbnails** (about 13 KB each) on base.palopenmaps.org. Not used.
- **Sheet index**: a GeoJSON list embedded in the home page (290 sheets of the 1:20,000 layer). Its boxes are lat/lon rectangles; the 19-14 box lies about 165 m east of the true grid corners. The tiles do not share that offset.
- **Vector overlay of the 1940s map**: crowd-sourced digitisation, `https://tiler.palopenmaps.org/maps/osm/{z}/{x}/{y}.pbf`, ODbL 1.0 ("PalestineOpenMaps and contributors"). In five windows it holds only village-land names and a few shrines. Used only as a reading check (below); no row was copied.
- **Other layers**: the 1870s SWP sheets, 1:100,000 and 1:250,000 maps, OSM-derived 2025 vectors, Esri imagery, and an **"Aerial imagery, 1940s"** layer of RAF photographs georeferenced by Shaul Holtzman (`cdn.jsdelivr.net/gh/bothness/pom-tiles@2d154a8…/aerial1940s/`). That layer covers the strip north of Tell es-Sultan. It was not opened anywhere near Jericho.
- **Terms**: the maps are public domain under the UK Copyright, Designs and Patents Act 1998 (palopenmaps.org/en/about). The vector data are ODbL 1.0 (data.palopenmaps.org/copyright). No scan, tile or image is in the repository; the tile manifest hash is recorded instead.

## Method in brief

1. Coding windows: a circle of 1.0 km (1.5 km for area places, 0.6 km in Jerusalem) around each in-scope place of places_v2 (`windows.json`).
2. I read every label and every legend-class symbol in each window from the zoom-16 tiles (`items_base.csv`, 306 items). Positions are my picks; pick error is 15 m for a symbol, 40 m for an area, 100 m for a label.
3. **G1**: printed 1 km grid intersections, found by line detection (46 accepted) or picked by hand on 4x zooms (Jerusalem, Gerizim). Residual = tile position minus the nominal grid point, via PROJ "Palestine 1923 to WGS 84 (1)".
4. **G2**: map symbols against independent references: 10 sharp features on Esri World Imagery (2025), 3 NEAEHL grid references from the W2B controls, and 5 places_v2 points with sigma ≤ 0.1 km.
5. Placement (plan rule): coordinates follow the printed grid (a window similarity fit, or the sheet's mean G1 shift). Position error = √(pick² + G2 RMS²); the G2 RMS uses only the 10 imagery controls (31 m pooled; per sheet where there are two or more).
6. Toponym flags: frozen pattern lists per root, matched word by word. Labelled INFERENCE.
7. Landscape: each mapped feature of a key class was compared with Esri imagery and given one state.

## Results

### Published georeferencing (G1, G2)

| Sheet | G1 n | Mean shift dE, dN (m) | Median / max (m) |
|---|---|---|---|
| 17-13 Jerusalem | 3 (manual) | −1.7, −3.3 | 3.5 / 4.6 |
| 17-17 Awarta | 2 (manual) | −0.3, +11.6 | 11.7 / 13.2 |
| 18-12 Deir Mar Saba | 9 | −2.9, +12.6 | 13.7 / 18.6 |
| 18-13 Wadi el Qilt | 3 | −1.3, +7.8 | 7.9 / 8.6 |
| 18-14 Wadi el Makkuk | 1 | +2.9, +4.7 | 5.5 |
| 18-15 El Mughaiyir | 2 | +2.3, +6.7 | 7.1 / 7.5 |
| 19-12 Ras Fashkha | 6 | +2.4, +3.4 | 4.7 / 5.3 |
| 19-13 Kallia | 4 | −6.1, −5.0 | 7.8 / 9.6 |
| 19-14 Jericho | 16 | −12.8, +0.6 | 13.9 / 17.2 |

- The tiles sit within 3–19 m of the printed grid. The shift is mostly a constant per sheet (RMS about the mean ≤ 4 m).
- Against 2025 imagery (10 symbols), the published positions are off by a median of 15 m (2–82 m). Correcting to the printed grid does not help (median 17 m). So the grid-to-WGS84 datum step, or the drawing itself, adds about 10–15 m.
- The worst cases are identification problems, not georeferencing: Tawahin es-Sukkar 82 m, the ʿAin es-Sultan spring dot 36 m, Kh. el-Mafjar 39 m.
- NEAEHL grid references: 15–85 m. places_v2 points: 25–150 m (most are label anchors). Details: `georef_check.csv`, `georef_check.json`.

### Tell es-Sultan (registration protocol)

- Order kept: prediction and record declared, capture form filled, coarse preview at 8 m per pixel with the zone **painted solid** (stricter than marking it), check point chosen on the preview, controls picked on masked views, record hashed, fit run, zone opened last.
- Controls: tell feet W, S, E, Tawahin (the map labels "Sugar Mills / Et Tawāḥīn"), Kh. el-Mafjar. Check: RP-SPRING ("Sp. ʿEin es Sulṭān"). Tell es-Samarat and Tell Abu Hindi were dropped before the fit because no mound could be identified on the imagery.
- **Result: rejected.** Control RMS 36.6 m, check error 48.6 m, E_total 48.8 m. It supports no relation; no geometry goes to the atlas.
- An exploratory fit to 16 printed grid intersections (RMS 7.5 m) gives a check error of 34.9 m at the spring. It would also be rejected.
- **In the strip** (viewed after the fit): a trig station (653, height −224.3), a junction of dashed tracks, the main road and contours. No cave, cistern, well, pit, tomb, cemetery, ruin or quarry is printed. Silence is not absence.
- **SULTAN-1: not testable by this record.** The link stays open for the pending Garstang, PEF, Nigro and aerial records. Sheet 19-14 (as served) is now exposed for the strip.
- Files: `research/assessments/kohlit_chain/registrations/POM-pal20k-z16-19-14.*` (declaration, prepreview, capture CSV, checkpoint, record, result, secondary_fit, zone).

### Features and names

- `features.csv`: 190 features (17 aqueduct or channel, 17 ruin, 18 cave, 11 tomb or cemetery, 10 tell, 9 spring, 5 pool, 5 mill, 4 cistern, 1 well or cistern, 10 church or monastery, 6 shrine, 7 built-up, 12 road, 53 other, 5 unidentified symbols). `names.csv`: 248 names.
- Notable mapped features near candidate places (EVIDENCE of what the map prints; no dates):
  - Kh. el-Marjama / ʿEin Samiya: the spring dot, a channel south, **11 cave symbols** (seven in two rows east and south-east of the label, two on the wadi bend west, two by the channel), "Roman Mill" with R., Kh. Samiya, "W. Kuheila".
  - Hyrcania: "Aqd." lines reaching the summit from the north-west, a cave symbol and "Vault" on the summit, a narrow rectangle west of it, "Bīr Abū Shuʿla" (cistern), "Bīr el Qattār (Birka)".
  - Kh. Qumran: "Anc. Aqueduct" from the fall, a dotted enclosure with "R" and "Cem.", a "Canal" south of the wadi mouth.
  - Jericho: "Cem." and "Caves" at the foot of Deir el Quruntul; "Ruins" and two "Cem." at Nuʿeima; "Qanāt Wāṣil" and "Qanāt Umm et Tawābīn"; mound symbols at Tell es-Samrat, Abu Hindi, el-ʿArayis and Abu Khurs.
  - The places_v2 point for cave IV/17 falls on the label "Nuqb Abū Saraj".
- **Toponym flags (INFERENCE, no identification claim)**: W. Kuheila (k-ḥ-l, 1.1 km east of the ʿEin Samiya point); Wādī el ʿAsla and Jaufat el ʿAsla (ʿ-ṣ-l); Karm es Samra (El ʿAjaz) with its R. square in the Buqeiʿa, and Karm Umm Suleimān on Gerizim (k-r-m); Valley of Kidron (q-d-r-n); Mt. Gerizim (g-r-z-m). Context only: Kh. Qumrān, Qumrān, Et Tabaqa, [El] Buqeiʿa. No name in any window matched the ʿ-k-r or s-k-k patterns.
- Known limits of the frozen patterns: "Shawāhid Sayidnā Mūsā" is flagged š-w-h by the pattern "shawa", but its root is š-h-d (a false match). "ʿEin ed Duyūk" and "Duyūk", the usual Arabic form of Doq, are not caught by the Doq patterns (a miss). Both are reported, not fixed.

### SWP sheet XVIII and 2025

- `swp_comparison.csv`: the SWP-based places_v2 points lie 277–602 m from the same names on the 1:20,000 sheets. All are inside their area sigma except **ʿAin ed Duk: 512 m** from the 1940s spring dot (sigma 300 m). "Tell el Qos" is not printed in the Jericho window.
- `landscape_change.csv` (125 features of key classes): 33 visible in 2025, 27 built over, 33 on open ground but not visible, 32 not checked.
  - Built over: the ʿAin es-Sultan camp covers the strip north of the tell; houses cover Tell es-Samrat, Abu Hindi, el-ʿArayis, Abu Khurs, Tell Deir Ghannam, the Nuʿeima ruins and cemeteries, and the aqueducts around Birkat Musa; Highway 90 runs over the ʿEin Fashkha spring dot; Silwan covers the east slope of the Kidron.
  - Visible: the Qumran ruins and cemetery, Hyrcania's summit, Mar Saba, St George, the Tell es-Sultan mound, the spring house, Kh. el-Mafjar, the Tawahin mills, the Marjama mound.
- `landscape_items.csv`: 14 window-level changes (two refugee camps since 1948, town growth, Highway 90, a paved road across the Buqeiʿa, Kiryat Luza on Gerizim).

### Reading check against the vector overlay (C3)

Two shrine symbols agree within 1 m (Sheikh Ghanim) and 14 m (Esh Sheikh Zeid). The overlay confirms the readings ʿArab Ibn ʿUbeid, Kafr Malik and Kafr Qallil.

## Deviations and exposure log

- One request reached `data.palopenmaps.org/api/capabilities` before I read that robots.txt disallows `/api/`. No further `/api/` request was made.
- The registration's reference coordinates come from Esri imagery, not GNSS. I assumed 5 m imagery error; it is not measured.
- The spring point is my identification of a rounded, roofed structure east of the road (moderate confidence).
- Identification-based drops (Samarat, Abu Hindi) were decided before the fit.
- Context flags follow the plan strictly (Buqeiʿa and Qumran windows only), so "El Mird" in the Hyrcania window is not context-flagged.
- No marginal legend was read. "R" next to a square is read as "ruin or antiquity" and "ↄ" as a cave symbol; both are INFERENCE from labelled examples.

## What stays unknown, and why

- Dates of every mapped feature: a map symbol records presence in the 1940s only.
- Features the map omits: openings of 1–2 m and most cisterns are not drawn at 1:20,000.
- The served edition of 19-13 and 19-14, and the marginal legends: the full sheets were not fetched (robots and tool limits).
- 32 features' 2025 state: cliff faces, dense town blocks and view edges.
- Esri's absolute accuracy here.

## Files

| File | What it holds |
|---|---|
| `plan.json` | The frozen plan |
| `windows.json` | Coding windows and their places |
| `items_base.csv` | My 306 readings with tile positions (input) |
| `g1_picks.csv`, `g2_controls.csv` | Georeferencing check inputs |
| `name_readings.csv` | Arabic script for 47 names (INFERENCE) |
| `landscape_change.csv`, `landscape_items.csv` | 2025 states (input) |
| `features.csv`, `names.csv` | Coded tables (output) |
| `georef_check.json`, `georef_check.csv` | Residuals in metres (output) |
| `swp_comparison.csv`, `summary.json` | SWP comparison and counts (output) |
| `mm_lib.py`, `build.py`, `test_mandate_maps.py` | Code and tests |

## Run and test

```sh
python3 -I research/regional/mandate_maps/build.py
python3 -I -m unittest discover -s research/regional/mandate_maps -p 'test_*.py'
python3 -I research/assessments/kohlit_chain/registration.py research/assessments/kohlit_chain/registrations/POM-pal20k-z16-19-14.json
```

## Failed or blocked links

- `https://www.dropbox.com/sh/qos20k3m2np6a7y/…` (sheet downloads): robots.txt disallows `/sh/`; not fetched.
- `https://data.palopenmaps.org/api/` (OSM-style data API): robots.txt disallows `/api/`.
- `https://www.wikidata.org/w/api.php` (search for Elisha's Spring): HTTP 429, "too many requests"; not retried.
- Esri World Imagery zoom 19 near Tell es-Sultan: "Map data not yet available" tiles.
- A person with a browser could open the full sheets 19-13 and 19-14 (both editions) on palopenmaps.org/en/maps to read the margins (edition, date, legend). The 19-14 margins do not show the strip; the map body does.
