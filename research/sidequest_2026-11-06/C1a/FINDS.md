# Side-quest C1a — Jerusalem hills and Benjamin plateau: change across image epochs (6 Nov 2026)

Lane C1 (five epochs), area C1a: Bethlehem–Ramallah, watershed east to the Mishor Adummim line.
One bounded pass of about 80 tool calls. About 25 HEXAGON/CORONA windows read (most at reduced scale), plus about 745 web tiles (Esri World Imagery and the POM RAF 1940s layer; URL patterns in `tile_urls_summary.txt`).
Coordinates of unrecorded features are only in the private folder (`private/C1a/PRIVATE_LOCATIONS.md`). Below they are given as frame ID and pixel window.

Frame pixel convention: **F014 mosaic px** = HEXAGON D3C1208-400636F014 (25 Jun 1974, forward, stored north-up). Tiles are joined with the E-run offsets (`tile_offsets.json`, tile d x-origin 105120, y +40), so mosaic X = 105120 + tile-d x and mosaic Y = 40 + tile-d y.

---

FIND CARD
Title (one line): A pre-1978 earthwork cluster (a raised-rim ring about 80–100 m across, strips, bars) under the Mishor Adummim industrial zone, visible on HEXAGON 25 Jun 1974 and graded away by 5 May 1978
Lane: C1a
What is odd (2–4 sentences): At full resolution (about 1 m/px) the June 1974 forward frame shows a cluster of features on open desert ground: an irregular closed ring with a raised rim, about 80 × 100 m; a group of 6–8 dark parallel strips, each about 8 × 40 m; two long parallel bars about 50 m long; a bright rectangle about 25 × 40 m; and, east of a north–south track, a rectilinear compound about 70 × 60 m. On HEXAGON 5 May 1978 the same ground has been graded for the industrial zone and has its first sheds, and none of the ring, strips or bars can be found. Today the whole cluster is under factory buildings (Esri). The only record I found for the area is the Euthymius monastery excavation reports, which describe the monastery and nothing around it. The compound is probably that monastery. The ring, strips and bars appear in no corpus record I could find.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- HEXAGON D3C1208-400636F014 tile d, window x 15850–17050, y 18010–19010 (F014 mosaic X 120970–122170, Y 18050–19050), full res. Ring centre at tile d (16390, 18565); strips (16270, 18370); bars (16560, 18580); compound (16730, 18570); bright rectangle (16075, 18495).
- HEXAGON D3C1214-200439F007 tile c (5 May 1978), window x 12100–14500, y 13800–16200: graded ground, early industrial sheds, a new walled hilltop compound to the north (absent in 1974), and a first housing estate.
- RAF 1940s layer (POM, z16): a group of dark parallel strips appears in the same place. The strips F1b at least are older than 1948. The ring cannot be resolved there: the layer's effective resolution is about 9 m (project measurement, `research/regional/raf_1940s/README.md`).
- Recorded neighbour: Khan el-Ahmar / St Euthymius, ESI 7–8 (1988) p. 121 (bucket PDF `Excavations-and-Surveys-in-Israel-7-8-1-e1b758cb`, page 121): "industrial quarter of Mishor Adummim (map ref. 134/183)"; Chitty 1927–32 and Meimaris 1976–78 excavations; nothing about earthworks around the monastery.
- Private crops and estimated coordinates: `private/C1a/mishor_full_A.png`, `mish_74_78.png`, `ring_raf_esri.png`, `PRIVATE_LOCATIONS.md`.
Literature check (queries run, result, tag): bucket `pdf-search "Mishor Adummim"` found ESI 7–8 p. 121 (Euthymius) and HA-ESI 112 p. 239 (Peleg 1996, a cave between Mishor Adummim and Ma'ale Adummim, map ref. 18100/13210, a different spot). Repo and branch grep for "Mishor Adum": only HA/ESI coding rows and Dorsey road notes, no imagery work. `reports_metadata.csv`: no Mishor Adummim title. Web search "Mishor Adumim before industrial zone army camp Khan al-Ahmar 1940s British camp Euthymius aerial photograph": nothing on earlier earthworks. Wikipedia "Mishor Adumim" gives only 1998 (the year its management company took over), while the 1978 frame shows the zone already being built. Tag: **NEW TO THE PROJECT** (no record found; the literature check was too shallow to claim NEW TO THE LITERATURE).
Why it might matter: This is a dated loss: some features stood on 25 Jun 1974, and the ground was graded by 5 May 1978. It is also a test of the brief's question of what an unrecorded feature destroyed by development looks like at the resolution HEXAGON really has. Since the strips are already on the 1940s layer, part of the cluster is at least Mandate-era.
How to confirm or kill it (with data in hand, or what is missing): (1) Check the December 1974 frames (D3C1209-200214F0xx; I did not locate the area in them) and CORONA Sept 1967 (DS1101-2168DF040–042; not located; orientation unknown). If the ring is absent in 1967, it is post-1967 work, most likely military or early site preparation, and is killed as an antiquity. (2) The 1:15,000 RAF prints (Hebrew University, 600 dpi) would resolve the ring if it is older than 1948. (3) Read Mandate 1:20,000 sheet 17-13 / 18-13 near Khan el-Ahmar for a printed camp, reservoir or enclosure. (4) The best kill: a closed raised rim with no gap at 1 m/px fits a modern bulldozed berm or a pond embankment better than an ancient wall. Cross-check against the Ma'ale Adummim survey literature (not in the corpus as far as I found).
Confidence: low (that it is archaeological); high (that something visible in 1974 is gone by 1978)
Touches the Copper Scroll? no (desert fringe east of Jerusalem; no scroll entry is tied to it)

---

FIND CARD
Title (one line): The E-run (31 Oct) geolocation of HEXAGON F014 misplaces Jerusalem by about 2.2–2.4 km; a 3-point correction is supplied
Lane: C1a
What is odd (2–4 sentences): The E run's `stage1_geoloc.json` `fwd_mosaic_px_to_utm` affine (0.919 m/px, isotropic) was fitted only near Jericho. The run's own note says it covers about 26 × 32 km there. Used 25 km to the west, it puts the Dome of the Rock 1,510 px east and 1,840 px south of where the dome actually is on the frame (about 2.4 km), and the Atarot runway centre (+1,700, +720) px off (about 1.8 km). A 3-point exact affine (Tell es-Sultan from E, Dome of the Rock, Atarot runway centre) gives anisotropic scales of about 1.00 m/px along X and 0.84 m/px along Y. So a single isotropic scale is wrong over this frame, which fits the E note's diagnosis (no optical-bar camera model).
Evidence (exact sources: file path / page / figure / frame / coordinates):
- E affine: `branch_only/claude__novel-2026-10-31-E/research/novel_2026-10-31/E_hexagon_stereo/stage1_geoloc.json` → `JUN74.fwd_mosaic_px_to_utm`.
- Observed (F014 mosaic px): Dome of the Rock (31.77805 N, 35.23535 E) at (112349, 22075), read on a 1/2-scale crop centred (112359, 22115). The E affine predicts (110839, 20235) for 31.778, 35.234.
- Atarot runway centre (Esri z15 pick: 31.86662 N, 35.21723 E) at (110160, 10584). The E affine predicts (108460, 9864).
- Tell es-Sultan (131524, 7274) = E's F014 tile d (26404, 7234).
- Result: `out/C1a/F014_3point_affine.json` (px → UTM 36N: [[1.00017, −0.02375, 599827.7], [−0.08312, −0.83576, 3545797.4]]).
- Check point: at Nebi Samwil the 3-point affine is still about 300 m off (by eye). Use it to find a place, then tie by eye.
- Coverage fact for other lanes: F014's south edge passes about 2 km south of the Haram (frame row 24,668; the Dome is at row about 22,075 at about 0.84 m/row). Bethlehem is not on F014. May 1978 F007 tile c covers Jerusalem (west edge) to Jericho (north-east corner) in one tile.
Literature check (queries run, result, tag): grep of repo and `branch_only` for "fwd_mosaic_px_to_utm" and "stage1_geoloc": used only inside the E run. No later product re-checks it at Jerusalem. Tag: **NEW TO THE PROJECT** (a project-internal coordinate error, with its correction).
Why it might matter: Any lane that reuses E's georeferencing outside the Jericho box (as the C1 lane note suggests) will look 2 km in the wrong place. This cost this lane about 15 tool calls.
How to confirm or kill it (with data in hand, or what is missing): Run `python3 out/C1a/tools/trip.py NAME LAT LON 700` at any well-known landmark (for example the Haram corners or the Qalandia/Atarot runway ends). Better still, add 6–10 controls and fit a quadratic. Automatic SIFT/ORB/NCC matching of 1974 against Esri failed in every attempt (5–8 inliers, see Dead ends), so the controls must be picked by hand.
Confidence: high
Touches the Copper Scroll? no (a method product)

---

## Dead ends

- Whole-area eye scan of the RAF 1940s layer against Esri at z14 (`raf14.png` vs `esri14.png`, 31.70–31.93 N, 35.17–35.38 E): the 1940s mosaic is patchy (frame seams, tonal blocks, gaps), and at about 9 m effective resolution no pond, spring or small structure could be judged. Dropped. It confirms the earlier "too coarse" verdict for this area too.
- The POM RAF 1940s layer has **no coverage** (black) over much of the Nebi Samwil hill at z16, so 1940s versus later at Nebi Samwil is impossible from this layer.
- Nebi Samwil village (demolition reported for 1971): on the June 1974 frame the hilltop and its terraces are clear, but at the 3-point affine's error (about 300 m) I could not separate the village footprint from fields within budget. Not pursued. It would also only re-date a known event.
- Automatic co-registration of HEXAGON 1974 to Esri: SIFT on whole-tile overviews (A015 d, 1/16 and 1/32: 7–8 inliers, a degenerate homography), gradient-NCC patches on the E-warped frame (5–36 patches, correlations 0.1–0.25) and local SIFT/ORB on a 2.6 km window (5–6 inliers, degenerate) all failed. The cause is land-cover change and differences in sun and contrast. Use hand-picked controls.
- Ma'ale Adummim core (south of the old road): mostly at or beyond F014's south edge. It would need A015/A016 or F015, which I did not register.
- CORONA DS1101-2168 (Sept 1967): DF042 tile d shows a Dead Sea shore, but the frame orientation and scale are unknown (store note). I did not locate Jerusalem or Mishor Adummim within budget.
- HEXAGON December 1974 (D3C1209-200214): not located for this area within budget. This is the main missing epoch for card 1.
- Bavarian 1918: of the five plates in Drive 07 / "Bavarian aerials 1918", only BS Pal 838 (SE Jerusalem, Silwan, Kidron; atlas-adjacent) and BS Pal 901 (el-Azariye to Khan Hatrur, mostly lane C1b) touch this area. Neither covers Mishor Adummim, Nebi Samwil or the Benjamin plateau. Further plates would need the BayHStA IIIF catalogue (`gda.bayern.de`), which I did not search.
- The 1978 F007 frame also shows a walled hilltop compound north of the junction that is absent in June 1974 and present today. It is a modern structure, built between the two frames, and not an archaeological find. Noted only to help date the 1974–78 construction.

## Blocked inputs

- None hard-blocked. Not opened: the HEXAGON 1974 aft frames A016 and F015 (time), the December 1974 frames (time) and the CORONA frame georeferencing (orientation unknown, `README.md` store note).
- The search for `hexagon_colab_previews_2026-10-26.md` (repo main and `branch_only`) found no copy. I used the `hexview.py` header and the E-run offsets instead.

## Seed / reproducibility

- Tools (public, no images): `out/C1a/tools/tiles.py` (web-tile mosaic with URL log), `f014.py` (F014 mosaic reader with E offsets), `trip.py` (RAF | HEXAGON | Esri triptych for a lat/lon, using `F014_3point_affine.json`), `warp_local.py`, `georef.py` (the failed automatic attempts, kept for the record).
- Tile URL patterns and counts: `tile_urls_summary.txt` (Esri `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`; POM RAF `https://cdn.jsdelivr.net/gh/bothness/pom-tiles@2d154a8…/aerial1940s/{z}/{x}/{y}.png`). The full per-tile log is private, because it would locate the target windows.
- Private: `private/C1a/` (7 PNG crops, `PRIVATE_LOCATIONS.md`, `tile_urls_full.log`).
