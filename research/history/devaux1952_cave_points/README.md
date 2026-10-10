# De Vaux 1952 survey map (RB 60, pl. XX): digitized cave points

10 Oct 2026, Claude. Exploratory measurement. No identification claim. Nothing in the repository was changed.

Tags: **EVIDENCE** = the plate, a source or a pixel test shows it; **INFERENCE** = my measurement or conclusion; **BK** = background knowledge or convention.

## Source

R. de Vaux, "Exploration de la région de Qumrân. Rapport préliminaire", *Revue Biblique* 60.4 (1953) 540–561, **pl. XX**, "Carte de la région de Qumrân, avec la localisation des grottes". JSTOR stable 44091669. File `de Vaux 1953 – Exploration de la région de Qumrân (RB 60, 540-561).pdf`, SHA-256 `81a4b15119725556d23c1f2092fbc6953276e89b14cfa74528a399c59fd1571d` (checked). Pl. XX is PDF p. 23 (north part) and p. 24 (south part).

- The embedded JPEGs were extracted unchanged with `pdfimages -j`, 1950 × 3000 px at 300 ppi each. Their SHA-256: p. 23 `a08e409c…fe227`, p. 24 `46e48fcb…cdb3d`. Re-rendering at 600 dpi would add no detail.
- **EVIDENCE (pixel test):** the two pages are crops of **one raster**. North rows 2440–2735 equal south rows 264–559 pixel for pixel across the full width (mean absolute difference 0.0), so the offset is exactly 2176 rows. Points 22 and 26–29, which appear on both pages, are therefore **not** an independent cross-check (contrast `research/history/devaux1953_cave_list_extracted.md` §4). All measurements below use one stitched frame.
- **EVIDENCE (plate):** 1-km grid labelled 192, 193, 194 (eastings) and 124–131 (northings). The plate prints "1:20.000". It has no north arrow, legend or graphic scale.

## Outputs (this folder)

- `devaux1952_cave_points.csv`: one row per point (the requested columns).
- `devaux1952_cave_points_measurements.csv`: pixel positions, per-half transform values, sigma, and control symbols.
- `pl_XX_points_overlay.png` (not in Git, because it reproduces the copyrighted plate): the stitched map with measured dots circled, plus insets A (3Q cluster), B (1Q/2Q cluster) and C (W. Qumran outlet). Regenerate it with `scripts/overlay.py` from the JSTOR PDF.
- `scripts/` (gridfit, affine, blobs, points, build, overlay; run `python3 -I scripts/X.py <folder> [repo]`) and intermediates `transforms.json`, `points_px.json`, `build_summary.json`.

## Method (INFERENCE unless tagged)

1. **Grid lines.** I traced each of the 3 easting lines and 8 northing lines every 4 px by taking the centroid of the narrow dark run nearest the nominal line, then fitted a robust straight line. 289–462 samples were kept per line, with an RMS of 0.3–0.6 px. The exception is N 128 at 2.2 px: there the line is drawn **double**, two strokes about 4 px apart. The lines are not exactly parallel: tilts range from −0.27° to +0.21°. That fits hand-ruled lines or slight print distortion. Intersecting the fitted lines gave 24 grid intersections.
2. **Transform.** I fitted one 6-parameter affine transform from stitched pixels to Palestine-grid km, using all 24 intersections. Per-half fits and a 2nd-order polynomial served as checks.
3. **Dots.** Dark pixels below 110 of 255 were opened with a 5-px-radius disk. This removes strokes and digits and leaves the solid site dots. Each dot was then refined to the centroid of its distance-transform core. Dot core radius is 7–10 px, so the dots are about 17–20 px across, roughly 30 m on the ground.
4. **Labels.** I read every label by eye on 3–8× crops and assigned each to the adjacent dot. I also scanned the whole cliff band at 1×. No further numbered label exists, so I gave no coordinates to illegible numbers.
5. **CRS chain (BK; repo convention from `research/agent_review_2026-10-07/wave2/W2B_model_v1/scripts/grid_convert.py`).** Old Israel Grid metres are the Palestine-grid km × 1000, i.e. EPSG:28191 (Cassini-Soldner, Palestine 1923 datum).
   - WGS84: PROJ "Palestine 1923 to WGS 84 (1)", stated accuracy 2 m.
   - ITM (EPSG:2039): "Palestine 1923 to Israel 1993 (1)" plus Israeli TM, stated accuracy 1.5 m. Going instead via WGS84 differs by at most 1.4 m.
   - pyproj 3.8.0 / PROJ 9.8.1.

## Transform and residuals (INFERENCE)

| Fit | n | RMS (m) | Max (m) |
|---|---|---|---|
| **Affine, stitched, all intersections (used)** | 24 | **5.4** | **10.7** (E194/N131) |
| Affine, north part only | 12 | 3.7 | 6.1 |
| Affine, south part only | 12 | 1.6 | 2.8 |
| Similarity, stitched | 24 | 7.1 | 15.1 |
| 2nd-order polynomial, stitched | 24 | 2.5 | 4.5 |

- Leave-one-out error is at most 13.5 m.
- Scale: 597.2 px/km (E) and 593.6 px/km (N), i.e. 1.67–1.69 m per pixel. At a nominal 300 ppi this is 1:19,800–19,900. The plate's "1:20.000" is consistent, and the 0.6% x/y difference is absorbed by the affine fit.
- The per-half fits move points by at most 7.9 m (the W. Qumran band, where each half extrapolates).

## Results (INFERENCE; 27 points)

Coordinates are Palestine grid km. "Label" is legibility of the printed number; "dot" is confidence in which blob is the site dot. The full CSV adds OIG, ITM and WGS84 coordinates.

| Pt | E | N | Label | Dot | To 8 (m) | Pt | E | N | Label | Dot | To 8 (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 193.116 | 130.211 | sure | sure | 587 | 21 | 193.220 | 128.565 | sure | sure | 1220 |
| 2 | 193.195 | 130.092 | sure | sure | 444 | 22 | 192.945 | 127.635 | probable | uncertain | 2190 |
| 3 | 193.340 | 129.876 | sure | probable | 189 | 26 | 193.253 | 127.539 | sure | probable | 2229 |
| 4 | 193.410 | 129.857 | probable | probable | 126 | 27 | 193.156 | 127.403 | sure | probable | 2376 |
| 7 | 193.422 | 129.766 | probable | probable | 65 | 28 | 193.141 | 127.286 | sure | sure | 2495 |
| **8** | **193.486** | **129.756** | sure | sure | 0 | 29 | 193.199 | 127.309 | sure | probable | 2463 |
| 9 | 193.350 | 129.722 | probable ("5"?) | sure | 140 | 30 | 193.171 | 127.237 | sure | sure | 2539 |
| 10 | 193.403 | 129.678 | sure | sure | 114 | 31 | 193.061 | 127.053 | sure | sure | 2736 |
| 12 | 193.276 | 129.172 | sure | probable | 621 | 32 | 193.119 | 127.043 | sure | sure | 2738 |
| 14 | 193.256 | 128.869 | sure | probable | 916 | 35 | 193.624 | 126.909 | sure | sure | 2851 |
| 15 | 193.250 | 128.804 | sure | probable | 981 | 37 | 192.246 | 124.989 | sure | probable | 4926 |
| 17 | 193.329 | 128.699 | sure | sure | 1068 | 39 | 192.752 | 124.050 | sure | sure | 5753 |
| 18 | 193.318 | 128.741 | sure | sure | 1029 | 40 | 192.593 | 123.823 | sure | uncertain | 6001 |
| 19 | 193.272 | 128.755 | sure | probable | 1024 | | | | | | |

**Point 8 = 3Q** (EVIDENCE for the number: "la grotte nº 8", RB 60 p. 555). Its measured position (INFERENCE):

| CRS | Value |
|---|---|
| Palestine grid | 193.486 / 129.756 km |
| OIG (EPSG:28191) | 193486 / 129756 |
| ITM (EPSG:2039) | 243486 / 629758 |
| WGS84 | 31.76022 N, 35.45809 E |

The unlabelled dots at about 192.42/130.68 and 192.53/126.83 (also noted in the prior reading) are not cliff sites and were not given numbers. The 13 numbers 5, 6, 11, 13, 16, 20, 23–25, 33, 34, 36 and 38 do not appear on the plate (EVIDENCE: full scan).

**Against the prior by-eye reading** (`devaux1953_cave_list_extracted.md`, same plate): all 27 points agree within 2–16 m, with a median of about 6 m. The largest differences are 22 (16 m), 26 (11 m) and 17 (11 m). For point 8 the difference is 7 m. The labels and dot assignments are the same, so the readings agree, but this is not independent evidence.

## Absolute check against repo controls (INFERENCE from EVIDENCE)

The plate prints three symbols that the repository locates independently.

| Plate symbol | Plate E / N | Reference (repo) | Offset plate − ref (dE, dN) | Distance |
|---|---|---|---|---|
| "−72" trig Δ | 192.826 / 126.789 | Mandate 1:20k 19-12 trig 639 (h −72.1), `mandate_maps/features.csv` Q12, ±35 m | −5, −40 m | 40 m |
| "−388" trig Δ | 194.245 / 126.963 | trig 636 (h −387.7), Q11, ±35 m | −3, −13 m | 14 m |
| Filled square under "Kh. Qumrân" (identity INFERENCE) | 193.592 / 127.604 | Esri 2025 main-complex centre (`g2_controls` ESRI-Q04, ±11 m) | +14, −41 m | 43 m |
| same | | Mandate "R" in enclosure (Q04) | +1, −31 m | 31 m |
| same | | CHRE 7692 (31.741119, 35.459027) | +12, −34 m | 36 m |
| same | | NEAEHL 193620/127720 (100 m rounding) | −28, −116 m | 119 m |

NEAEHL (119 m) and the Pleiades/places point (116 m, not tabulated) are rounded references and do not test the plate.

- The usable controls put de Vaux's printed features **14–43 m** from their Mandate or modern positions. All three lie about 13–41 m **south** (mean dN about −30 m, dE about +2 m).
- All three controls are at N 126.8–127.6, 2.2–3 km south of 3Q. The repo has no control near 3Q. I therefore applied **no** shift. If the same −30 m applied at 3Q, point 8 would move to about N 129.786.
- The other heights printed in the north part ("−44", "−61", "−13", "+68", "−356", "−373") could test the plate near 3Q if they were picked from Mandate sheets 19-12/19-13. That has not been done.

## Error budget (1 sigma)

| Term | Size | Basis |
|---|---|---|
| Dot-centre measurement | 2 m (sure), 4 m (probable), 8 m (uncertain) | 1–5 px; the distance-transform centre moved ≤1.8 px from the raw blob centroid |
| Transform | 5 m (max 11 m); model choice ≤8 m | residuals above |
| Drafting / plotting | **20 m** (assumed) | 1 mm on the 1:20,000 sheet. The plate gives no survey method; dot diameter is about 1 mm (30 m), and dense clusters may be displaced for legibility |
| Base map, grid and datum to the modern frame | **15 m** (assumed) | repo: Mandate 1:20k symbols vs 2025 imagery median 15 m; controls above 14–43 m. De Vaux's grid is unlabelled as to datum; its values match the Palestine grid (BK + controls) |
| **Total, absolute** | **≈ 26 m → quote ±30 m (1σ), ±60 m (≈95%)** | uncertain dots (22, 40) slightly more |
| Distances between nearby points | ≈ ±30 m (1σ) | grid, datum and transform terms largely cancel; drafting does not |

So no position here is better than a few tens of metres. Neighbours of 8 that are 65–140 m away are separated by only 2–5 sigma, and their order is not secure.

## Comparison with repository coordinates

**(a) 3Q, 1Q, 2Q.**
- **3Q: the repo has no coordinate.** EVIDENCE: `research/agent_review_2026-10-07/wave1/T02_hoard_match/hoards.json` H10 has lat/lon null; `research/comparanda/concealment_contexts/comparanda.csv` t02H10 is blank; salvage-records S11 (3Q re-excavation, ESI 6) has no coords.
  - The only repo position is the prior plate reading, 193.49/129.75, which is **7 m** from this measurement. It comes from the same plate.
  - Point 8 lies **2.11 km at bearing 357°** from the 2025 Kh. Qumran control. That agrees with de Vaux's "environ 2 km au nord de Khirbet Qumrân" (p. 555, EVIDENCE).
- **1Q (point 14):** the only repo coordinate is hoards.json H09, 31.7418/35.4594. That is the Kh. Qumran (Pleiades) point under another name, **1.21 km** from point 14 (INFERENCE). It should not be used as a 1Q location.
- **2Q (point 19):** the repo has no coordinate. On the plate, 1Q–2Q is 115 m apart.
- **4Q–11Q:** the repo has no coordinates. The plate does not show them (4Q–6Q were found after the survey; RB 60 p. 541 n.).

**(b) Distances from 8** (bearing from 8; relative sigma about 30 m): 7 65 m W (278°); 10 114 m SW; 4 126 m NW; 9 140 m WSW; 3 189 m NW; 2 444 m NW; 1 587 m NW; 12 621 m SSW; 14 = 1Q 916 m SSW; 15 981 m; 19 = 2Q 1024 m; 18 1029 m; 17 1068 m; 21 1220 m; 22 and 26–32 at 2.19–2.74 km; 35 2.85 km; 37 4.93 km; 39 5.75 km; 40 6.00 km. The full list is in the CSV.

**(c) Possible matches to repo cave records. These are proposals only (INFERENCE), not identifications.**
- **Patrich & Arubas 1989, Cave 13** (salvage S13; IEJ 39 pp. 43–44). The sources give three different indications:
  - Text: "about 2.8 km. to the north of Kh. Qumran", 150 m W of the Qalia–Almog track, faces east, in Samra-formation conglomerate (EVIDENCE).
  - Footnote 3: the cave "may have been No. 2 in the 1952 survey" (EVIDENCE).
  - **Their Fig. 1 (p. 44) plots Cave 13 only 0.25 km N of 3Q** (EVIDENCE). I measured this at 0.252 km N and 0.010 km W, using the figure's 0–2 km bar (125.5 px/km on a 200-dpi render). On the same figure, 3Q is 2.27 km and Cave 13 2.52 km from the Qumran ruin symbol.
  - Applied to point 8, the figure's offset gives about 193.477/130.008. Nearest plate points: **4 (165 m), 3 (189 m)**, 2 (293 m).
  - Applied to the 2025 Kh. Qumran point, the text distance gives N ≈ 130.445. That is **233 m north of point 1** and 353 m north of point 2, both the northernmost numbered points.
  - The figure and text disagree by about 0.4 km. The project status note ("0.5–0.8 km from 3Q") follows the text, not the figure.
  - Description: point 2 is "un petit amas de poterie sous des blocs écroulés" (p. 543). Cave 13 has fallen ceiling blocks in its N part with Roman-period finds and traces of earlier digging (pp. 43–44). That is a loose description fit for 2. Point 2's map position fits the text distance less well than 1, and fits the figure less well than 3/4.
  - **Result: not identifiable from these sources.** Candidates 1, 2, 3 and 4 stay open; P&A's "No. 2" is their own suggestion.
- **Twin Cave** (Bar-Adon locator 1937/1293; Greenberg-Keinan rec. 709, 193700/129300, 100 m). The nearest plate points are 12 (443 m), 10 (481 m), **8 (504 m)** and 7 (542 m). The locator lies about 0.4 km **east** of the numbered cliff points near that northing, beyond the error budget. **No match is proposed.** Twin Cave may simply be absent from pl. XX.
- **ESI 6 (1987/88) pp. 68–70** states 3Q = 1952 cave 8 (EVIDENCE via `research/sources/esi6_cave_survey_review_2026-10-01.md`) but gives no grid. ESI 7–8 has no Qumran cave record. I found no 1993-survey cave coordinates in the repo, so there was nothing to match.

## What this does NOT establish

- **No cave identity is proven by proximity.** A dot within 30–60 m of a modern cave does not make them the same cave. In the 3Q and 1Q/2Q clusters, 4–6 dots fall within 150 m of each other.
- The **numbers** come from the printed plate only. RB 60 has no numbered list. The DJD III **text volume** (1962), which the repo does not hold (only the plates), is still needed to confirm numbers, descriptions and any revised positions. It is needed especially for 7 and 9 (could be 5), and for 22 and 40, whose dots are uncertain.
- The map's survey method, base sheet and datum are **not stated**. The ±30 m figure rests on an assumed 1-mm drafting error and on three controls 2–3 km south of 3Q.
- Each point marks where de Vaux's cartographer placed a 1-mm dot. It does not locate a cave mouth, the 1952 find spot or the copper-roll niche.
- It says nothing about the 13 missing numbers, which caves held which pottery, or whether 35 is a cave. Point 35 is never mentioned in the text.
- Reed 1954 Fig. 2 (BASOR 135; the owner's JSTOR PDF) and DJD III Plate I (cliff views marking 14 and 19) were **not** used here.

## Suggested next evidence

1. DJD III text volume: the cave list and the map (if it reprints or revises pl. XX).
2. Mandate 1:20k sheets 19-12/19-13 spot heights near 3Q ("−44", "−61", "+68", "−13"), picked from the Palestine Open Maps tiles. These would give a control near 3Q.
3. A surveyed modern 3Q mouth coordinate (e.g. ESI 6 Fig. 29 if it carries a grid, or a published GPS fix). Point 8 can then be tested against it.
