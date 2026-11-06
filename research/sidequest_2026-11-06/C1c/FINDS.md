# Side-quest C1c: Dead Sea west shore and Judean Desert, Qumran to ʿEn Gedi (6 Nov 2026)

Lane C1c. Lane C1 asks for change across the image epochs. I worked on two things. First, the shoreline of June 1974 against October 2023, measured on 30 transects from Qumran south to ʿEin el-Ghuweir (`shorelines.csv`). Second, the open-air structures of Bar-Adon's 1968 survey (ASI 1 sites 113–139; lane B2 card 2), compared on HEXAGON 1974 and on 0.5 m imagery from 2023. Exploratory. No identification claim. Nothing in the repository was changed. Site positions are only in `private/C1c/` (B2's points come from WBADB). Public files give site numbers only.

**Georeference used.** HEXAGON D3C1208-400636F015 (25 June 1974), tile d. Run E's affine does not cover this frame. Automatic SIFT matching to Esri failed both globally and locally (see Dead ends). The working transform `T_J15_v1` is a similarity transform with 0.873 m per pixel and a rotation of about 2.6°. It takes its linear part from a frame-wide SIFT fit (35 inliers). Its translation comes from one anchor placed by eye: the Kh. Qumran access road and the Route 90 junction, both matched on the 1974 image and on Esri (Qumran ≈ tile-d pixel 28458, 5470). I checked it by eye at four points between ʿEin Feshkha and the Mazin–Ghuweir plain. Route 90 lines up within about 20–70 m. In the Bar-Adon windows (N 3501–3507 km UTM 36N) the road lines up within about 10–20 m. Reference imagery: Esri World Imagery. Its identify service gives Vantor WV02, 21 Oct 2023, 0.5 m, MinMapLevel 12, so zoom levels 15–18 all show this scene.

---

FIND CARD
Title (one line): Two of Bar-Adon's 1968 plateau structures (ASI 1 sites 117a and 120) still show on 2023 imagery, and roads or tracks laid after June 1974 now pass within about 15–40 m of them
Lane: C1c
What is odd (2–4 sentences): The 2023 image shows a round feature about 12–20 m across at site 117a ("horseshoe-shaped structure; paved round structures", Iron Age; WBS:4297). It also shows a ring about 25–30 m across about 15 m from the WBADB point of site 120 ("round structure built of three concentric circles", Roman/Byzantine; WBS:4329). Both features lie inside 50 m of the 1968 point, and each matches the recorded form. On the June 1974 frame, at the same registration (±20 m), 117a has no road at all and 120 has one track about 30 m to the south. In 2023, a two-carriageway road or track corridor runs 25–40 m SW of 117a, and a track junction wraps around the ring at 120, with a grid of rectilinear tracks about 100 m to the north. Lane B2 found no later survey of either site, so this damage since 1974 has not been recorded.
Evidence (exact sources: file path / page / figure / frame / coordinates): Panels `private/C1c/m1_large.jpg` (12 sites, 500 m windows) and `private/C1c/m2_zoom.jpg` (sites 120, 119, 117a, 139a, 260 m windows, 50 m ring at the WBADB point). Left of each pair: HEXAGON D3C1208-400636F015 tile d, full resolution. Right: Esri z18. Positions and notes are in `private/C1c/site_observations_private.csv`. The transform is `private/C1c/T_J15_v1.json` and the script is `private/C1c/scripts/sites.py`. Site texts are from WBADB (`branch_only/sandbox__methods/.../wbadb_sites.csv`, `components` field). The source page is ASI 1 pp. 126–131, which I did not reread.
Literature check (queries run, result, tag): Web search "Bar-Adon 1968 survey Judean Desert round structures horseshoe-shaped resurvey condition damage roads Dead Sea plateau" found the survey catalogue entries (dig.corps-cmhl.huji.ac.il/node/9141) and Davidovich, Goldsmith, Porat & Porat 2014, *Archaeometry* 56(5): 878–897, "Dating and interpreting desert structures: the enclosures of the Judean Desert re-evaluated" (https://cris.huji.ac.il/en/publications/dating-and-interpreting-desert-structures-the-enclosures-of-the-j/). That paper revisits earlier-surveyed enclosures, but the abstract names no sites. Repository and branch_only grep for "117a" and "WBS:4329" find only the WBADB-derived tables. Tag: **NEW TO THE LITERATURE** (tentative: the change since 1974 near these two sites; no condition report found).
Why it might matter: These are single-visit 1968 sites in the area covered by the 2023 looting study. The imagery shows that at least two still exist and that both now have vehicle access within metres. That makes them candidates for a condition check. It is also a cheap way to triage the other ~40 never-revisited points in the band.
How to confirm or kill it (with data in hand, or what is missing): (1) Read ASI 1 pp. 126–131 (store `01-ASI1-Kochavi-1972-indexed-81b7cd39`, PDF pp. 65–67, images only) for the dimensions of sites 117 and 120, and check them against the ring sizes. (2) Check whether Davidovich et al. 2014 lists either site, which would kill "never revisited". (3) A dated image from 1980–2010 (Esri Wayback, Google Earth history) would date the roads. Kill condition: the 2023 rings are modern (vehicle turning circles, or a cairn rebuilt by soldiers or hikers) rather than Bar-Adon's structures. The tracks that wrap round the ring at 120 make a turning circle a real alternative.
Confidence: medium (the roads and tracks are new since 1974); low (that the 2023 rings are the 1968 structures)
Touches the Copper Scroll? no. Site protection only.

---

FIND CARD
Title (one line): The June 1974 west-shore waterline (KH-9 F015) on 30 transects: 0.4–2.6 km of retreat to October 2023, and the GLO-30 surface at the 1974 line sits about 5 m above the expected 1974 lake level
Lane: C1c
What is odd (2–4 sentences): I mapped the 25 June 1974 waterline every 500 m of northing, from Qumran (N 3513.5 km) to just north of ʿEin el-Ghuweir (N 3499.5 km). The frame ends there. Retreat to 21 Oct 2023 is 2.0–2.6 km on the ʿEin Feshkha fan, 0.38–0.9 km at the Ras Feshkha cliff foot and 1.0–2.2 km on the Kidron–Mazin plain. In 1974, Route 90 at ʿEin Feshkha ran at the water's edge. Sampled at the 1974 line, GLO-30 (TanDEM-X, 2011–2015) gives a median of −392.4 m (IQR −394.4 to −389.3; 26 transects off the cliff). The lake level expected for mid-1974 is about −398 to −399 m (USGS OF 78-176: "near −400 m in 1977", start −399.0 m).
Evidence (exact sources: file path / page / figure / frame / coordinates): `out/C1c/shorelines.csv` (transect northing, 1974 and 2023 waterline easting and longitude, DEM value, retreat, flags). Source frames: D3C1208-400636F015 tile d box 20000–34000 × 3000–24668 at 1/4. Esri strip, lat 31.44–31.785, lon 35.36–35.50, z15 at 4 m. DEM: `Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif` (AWS open data). QA overlay checked by eye (`scratch`, not kept). Scripts: `private/C1c/scripts/shore.py` and `extract_shore.py` (rebuilt with the same parameters).
Literature check (queries run, result, tag): Shoreline retreat of the Dead Sea from satellite imagery is well published (Landsat studies; Bowman et al. 2007 on fan entrenchment, cited in sandbox run 23). Repository: "shoreline" appears only in terrain manifests and run 23. No per-epoch waterline table exists. Web searches for an annual level table ("Dead Sea level by year … 1974 1976 1978 gauge") gave only the USGS 1978 report, which plots the curve without printed values for 1974. Tag: **NEW TO THE PROJECT** (waterline table). The DEM offset is **KNOWN BUT UNDER-DISCUSSED** at most: GLO-30 accuracy limits are published, but no source here tests it on the exposed lake floor.
Why it might matter: The project uses GLO-30 and "lake level by period" (run 23: −395 to −400 m in the 1st century CE; the shore "measured from the −395 m contour"). If GLO-30 runs about 5 m high on the exposed floor, a −395 m contour lies about 100–200 m lakeward of where it should on the 3–5 % slopes of the fans. That affects every "distance from the ancient shore" in runs 23 and F.
How to confirm or kill it (with data in hand, or what is missing): (1) Find a gauge value for June 1974 (Israel Hydrological Service series). The USGS report's Fig. 3 source note names IHS readings for 1967–76. (2) Repeat on the December 1974 frame (D3C1209-200214F018) and on 1978 F007, whose Qumran pixel is known (tile c 29366, 20009). Two dates with a known level difference would split a DEM bias from a picking bias. (3) Kill condition: my waterline picks are landward by about 100–150 m. Wet beach and the mask close of 9 px (about 30 m) push the line landward, so some offset is expected. Registration error (±20–70 m) adds only about 1–3 m on these slopes.
Confidence: medium (waterline positions ±70 m); low (the DEM-bias reading)
Touches the Copper Scroll? maybe. It bears on run 23 and run F's ancient-shoreline distances. No entry is argued.

---

FIND CARD
Title (one line): Bar-Adon site 139a lies about 40 m inland of the June 1974 waterline, so the 1968 grid may put it at or below the 1968 shore
Lane: C1c
What is odd (2–4 sentences): On the registered June 1974 frame, the WBADB point of site 139a ("structure with rounded corners; rectangular structure"; WBS:4495) is about 40 m from the waterline, at the inner edge of a fringe of shore vegetation. Route 90 lines up within about 15 m in this window. The lake stood higher in 1968 than in June 1974, by perhaps 2–3 m (inference from the 1960s–70s fall rate, not from a gauge). On the about 3 % shore slope measured here (1974–2023), that puts the 1968 waterline roughly 60–100 m inland of the June 1974 line, and so landward of the 1968 point. The 2023 image shows only braided gullies at the point.
Evidence (exact sources: file path / page / figure / frame / coordinates): `private/C1c/m2_zoom.jpg` (panel 139a) and `private/C1c/m1_large.jpg`. Position in `private/C1c/site_observations_private.csv`. Shore slope from `shorelines.csv` (N 3502.0 km: retreat 1,482 m for about 40 m of level fall).
Literature check (queries run, result, tag): Not searched beyond lane B2's checks. No source found that discusses Bar-Adon's shore-zone grids against the lake level. Tag: **NEW TO THE PROJECT**.
Why it might matter: If the grid is off lakeward, other shore-plain points of the 1968 survey (138b, 139b, the ʿEin el-Ghuweir group) may carry the same offset. That matters for B2 card 3, which places 138B 1.19 km from ʿEin el-Ghuweir.
How to confirm or kill it (with data in hand, or what is missing): Read ASI 1 p. 131 for site 139, and Bar-Adon's wording ("on the shore", or a distance from the water). Get a gauge level for 1968 from the IHS series. Kill condition: the 1968 level was within about 1 m of June 1974, or Bar-Adon describes the site as on the beach.
Confidence: low
Touches the Copper Scroll? no

---

## Other records (not finds)

- Sites 119, 129, 131c, 132b, 133, 136b, 137a, 138a and 138b were also compared (`m1_large.jpg`). Nothing of the 30 × 30 m "fortress" 138A shows in either epoch: Route 90 is about 70 m east, and the area is a smooth plain in both. Site 119 has a gully that is much more incised in 2023 than in 1974, new tracks and a round pit about 15 m across about 90 m to the SW, but no structure resolved. Site 129 has a date plantation about 100 m east (east of Route 90), absent in 1974. 131c (a 33 × 34 m enclosure) is not clear in either epoch.
- Coverage of the store in this area: June 1974 F015 runs from the north tip of the lake to about N 3499.5 km UTM, just north of ʿEin el-Ghuweir. No frame of June 1974 (F010–F015) or 1978 (F006–F007) reaches ʿEn Gedi. 1978 F007 ends at about the latitude of Qumran and ʿEin Feshkha. CORONA DF042 tile d covers only the northern basin. The December 1974 frame F018 covers the area but is not registered. **ʿEn Gedi has no historical satellite epoch in the store that I could confirm.**

## Dead ends

- Run E's affine (`fwd_mosaic_px_to_utm`) does not cover F015 and is off near Jericho (C1b). Not used.
- Frame-wide SIFT, HEXAGON 1974 against Esri at 16 m: 5–6 inliers, nonsense scales. At 8 m (F015 tile d, F018 tile b) it gave 35 and 38 inliers. The scale (0.873, 0.885) and rotation are usable, but the translation was off by about 800 m at Qumran. A crop at the predicted point showed a military camp with an oval track north of the Qumran junction.
- Local SIFT at 2 m around a correct seed (Qumran): 4 inliers, rotation −145°. Sun angle and 50 years of change defeat descriptor matching here. Anchors picked by eye were needed.
- AKAZE is not available in the installed OpenCV 5.0 build.
- A first waterline pick by threshold alone mistook ʿEin Feshkha reeds and dark palms for water (the retreat came out negative). Fixed by taking the largest connected dark component that holds a deep-lake seed.
- I did not reach CORONA 1967, HEXAGON December 1974, 1978, Bavarian 1918 or RAF 1940s (each needs its own anchors by eye; about 4 views per frame). Not reached either: the pools of ʿEin Feshkha, ʿEin el-Ghuweir and ʿEin Turaba, and sinkhole mapping.
- Annual Dead Sea level values for 1967, 1974 and 1978: no printed table found on the web. The USGS OF 78-176 gives only "near −400 m in 1977" in the text and plots the rest (Fig. 3, p. 17).

## Blocked inputs

- `https://metadata.maps.arcgis.com/arcgis/rest/services/World_Imagery_Metadata/MapServer/identify` returned an HTML sign-in page. I used `services.arcgisonline.com/.../World_Imagery/MapServer/identify` instead, which works.
- None of the project inputs were blocked.

## Seed / reproducibility

- Deterministic. Scripts are in `private/C1c/scripts/`: `geo.py` (Esri to UTM sampler; EPSG:28191 / 32636), `lreg.py` (hexview box wrapper), `shore.py`, `pair.py`, `sites.py`. Transform `private/C1c/T_J15_v1.json`: full-res pixel to UTM 36N, `[E,N] = qEN + L·([px,py] − q)`. Raw transect output: `private/C1c/shore_final.json`.
- Waterline rule: Gaussian blur σ = 2 px. Water is below 96 (1974, 3.5 m/px) or below 60 (Esri, 4 m/px). A 5 × 5 (Esri 7 × 7) opening is followed by the connected component that holds a deep-lake seed. For 1974 a 9 × 9 closing is added. The waterline is the first water pixel going east along the transect. The 2023 pick must lie east of the 1974 pick.
- Esri tiles are cached in scratch only (not kept). DEM is GLO-30 N31 E035 from `copernicus-dem-30m.s3.amazonaws.com`.
