# Side-quest swarm round 2, lane A6 (newest publications), 6 Nov 2026

Round 1 (`out/A6/`) left these open: A6-1's kill test (the final Birket al-Hamra report), the PNAS "2.5 m lower" check, the Cana and Midras volumes (only searched in round 1), and A6-3's question of whether the Maresha IV map references can be trusted as positions. Round 2 took up the last one in depth. It set the 2025 volume against its own general plan, against satellite imagery, against the GLO-30 DEM and against the same team's earlier Hadashot reports. The Cana 2025 volume served as the control.

Data files (public, all published references of excavated complexes in a national park):
- `maresha_iv_refs_vs_plan_vs_HA.csv`: 35 rows.
- `cana2025_vs_HA2008_area_refs.csv`: 19 rows.

Private products are in `private2/A6/`: the registration overlays, the dot pixels, the transform and the scripts.

---

FIND CARD
Title (one line): The 2025 Maresha IV map references are all shifted about 80 m to the NE. The shift is the error you get by projecting WGS84 coordinates to the Israel grid without the datum shift. The team's own earlier Hadashot references do not have it.
Lane: A6
Round-1 link: A6-3, extended. A6-3 found that the references are printed northing-first. This card shows that, once read the right way round, they still point to the wrong place.
What is odd (2–4 sentences): Ch. 2 of Maresha IV prints 31 references. They agree almost perfectly with the volume's own General Top Plan (Plan 1.3.1): a similarity fit gives rotation −0.6°, 0.531 m/px and a median residual of 27 m. The trouble is the plan's satellite base. Registered to Esri imagery (and checked against the Copernicus DEM), it shows that every reference is displaced by nearly the same vector: median dE = +64 m, dN = +48 m, |d| = 80.5 m (n = 30). That vector matches, to within about 8 m, the displacement you get by projecting WGS84 latitude and longitude onto the ITM/NIG grid without the Israel 1993 → WGS84 datum shift: +66.2 m E, +41.1 m N, constant to 0.01 m across the site. Once that offset is removed, the median residual falls to 27.5 m, which is about the size of a complex. The earlier references by the same excavators sit 25–42 m from the plan positions and 54–110 m from the "naive" positions, so they are correct. These are HA 2014 SC 1, HA 2021 SC 89, HA 2023 SC 97 and SC 99, and HA 2007 "SC 57", which is SC 126. So is the one legacy reference inside the volume, Kloner's ch. 4 "NIG 190774, 611098" for SC 99.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- **Maresha IV references.** Bucket doc `Stern-2025-Maresha-IV-Subterranean-Complexes-IAA-Reports-76-db5921ab`, ch. 2, PDF pp. 46–228 (list in `out/A6/maresha_iv_refs_vs_plan_vs_HA.csv` and the round-1 `out/A6/maresha_iv_map_refs.csv`). Ch. 4, PDF p. 268: the SC 99 NIG reference.
- **General plan.** Plan 1.3.1, PDF p. 16. The page is rotated: north points to the page's left. 33 SC dots were identified by eye on a 220-dpi render and snapped to detected red-dot centroids.
- **Registration.** SIFT + RANSAC (`cv2.estimateAffinePartial2D`) of the dot- and text-masked plan to Esri World Imagery z17 tiles x 78238–78246, y 53398–53405. Result: 36 inliers, RMS 1.8 px (about 1.8 m), rotation −0.10°, scale 0.5212 (= 0.530 m per plan pixel). A checkerboard overlay shows roads and paths running on across the tile joins (private).
- **Independent check.** Copernicus GLO-30 (`Copernicus_DSM_COG_10_N31_00_E034_00_DEM`, AWS open data). The 345/350/355 m contours fall on the tell's summit path in the Esri image within a few metres; the summit maximum cell is at ITM 190391/611220 (centroid of the top 4 m: 190406/611221, used for the bearings in card 2). An 80 m shift in the imagery would show as about 80 px on the overlay. None is visible.
- **Naive-datum vector.** pyproj EPSG:4326 → EPSG:2039 (Israel 1993 to WGS 84 (2), 0.5 m), against the same TM parameters with `+towgs84=0,0,0`: +66.17 E, +41.08 N.
- **Hadashot references.**
  - `hadtext/en/vol-126/13685` (SC 1, 190661/611171).
  - `vol-133/26015` (SC 89 box 190690–735/610886–955).
  - `vol-135/26380` (SC 97 190700/611260, Hebrew text; the English drops a digit: "19070"; SC 99 190774/611098).
  - `vol-119/00499` ("SC 57" 190551/611000).
- **Control.** Cana IAA Reports 75 (2025), Table on PDF p. 14, against the 19 HA 2008 Karm er-Ras area reports. Median shift (+15, −4) m, so there is no datum signature (`cana2025_vs_HA2008_area_refs.csv`). The fault is in this volume, not a house-wide IAA Reports problem.
Literature check (queries run, result, tag): Web: `"Maresha IV" Stern 2025 "Subterranean Complexes" IAA Reports 76 review OR erratum OR corrigenda` found the academia.edu listing, AWOL and library records; no review or erratum. Project: main and `branch_only` grep for "datum shift", "towgs84" and "without datum" found only `research/sources/iaa_gis_2026-10-30/README.md` l.49, which is about the IAA GIS layer at Qumran and says "not a datum shift". No Maresha IV reference has been ingested anywhere (R3: 0 hits for 611031/190665). Tag: **NEW TO THE LITERATURE**.
Why it might matter: Maresha IV is now the reference gazetteer for 152 subterranean complexes, and its map references are the only coordinates printed for most of them. A complex plotted from them lands about 80 m NE of its entrance. At Maresha that is often on another complex. The SC 1 reference lies 28 m from SC 70's plan position and 123 m from SC 1's. The SC 169 reference lies 16 m from SC 61 and 37 m from SC 169. Anyone joining Maresha IV to the HA reports, to CIIP findspots (cf. B3-1, SC 126) or to the project's cave and columbarium inventories should subtract (66, 41) m, or better, use the HA references. The mechanism (WGS84 projected without the datum shift) is a known GIS trap, and it would also explain the error if other 2020s IAA texts took coordinates from Google Earth.
How to confirm or kill it (with data in hand, or what is missing): Done with data in hand: the registration, the DEM check, the HA comparison and the Cana control. It is killed if the satellite base of Plan 1.3.1 has the dots drawn about 80 m SW of the true entrances, i.e. the plan, not the references, is wrong. That is unlikely, because the HA references made independently over 2007–2023 agree with the plan. A cheap further test is any surveyed entrance (IAA GIS layer, GovMap orthophoto) for SC 1, SC 75 or SC 169. Also not done: checking whether Stern 2019a (SC 169 final report) and BAR S2652 (2014) already carry the shifted values; neither is in the corpus.
Confidence: high for the offset (four witnesses: plan-to-imagery registration, DEM, HA references, Kloner's ch. 4 reference); medium for the exact mechanism (the vector matches within 8 m, but a base map georeferenced with the same error would give the same result).
Touches the Copper Scroll? no

---

FIND CARD
Title (one line): The Maresha preliminary reports carry three location errors: SC 89 and SC 90 print one identical map reference 204 m from either complex, SC 169 is put "southwest" against its own reference, and Maresha IV files SC 97 under the NW plan.
Lane: A6
Round-1 link: new. It comes out of the card above, using the same registered plan.
What is odd (2–4 sentences):
- (a) HA 119 (2007) report 00498 on SC 90 (Permit A-4361) and HA 120 (2008) report 00727 on SC 89 (Permit A-4687) print the same reference, "NIG 190680/611086; OIG 140680/111086", in both English and Hebrew. On the registered plan the two complexes are 204 m apart, and the shared point lies 185 m from SC 89 and 308 m from SC 90, 70 m from SC 169. HA 2021 (26015) quietly gives SC 89 a new box, 190690–735/610886–955. Its northing 610886 differs from 611086 by one digit, so the 2007 figure is probably a one-digit slip that the 2008 report copied.
- (b) HA 126 (2014) report 12643 puts SC 169 "c. 105 m southwest of the Upper City". HA 2021 says "105 m southeast of the tell". The 2014 report's own reference (190560/611070) lies at a bearing of 134° (SE) from the DEM summit, and the plan dot lies at 126°. So "southwest" is wrong, and the 2014 reference is itself 136 m from the plan position.
- (c) Maresha IV ch. 2 (PDF p. 176) assigns SC 97 to "Plan 1.3.2" (the NW section). Plan 1.3.1 and HA 2023 ("east of the tell, 180 m east of the northeastern corner of the Upper City") both put it NE, at plan-true about 190708/611285. R3 flagged SC 99's ch. 2 reference; this is a second ch. 2 slip of the same kind.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- (a), (b): the Hadashot text extractions in `/home/claude/swarm/scratch/B1b/txt/hadtext/` (`en` and `he`, files `vol-119/00498_*`, `vol-120/00727_*`, `vol-126/12643_*`, `vol-133/26015_*`), first paragraph of each.
- (c): Maresha IV PDF p. 176 and Plan 1.3.1 (PDF p. 16); the section captions are on PDF pp. 17–18.
- Distances and bearings: `maresha_iv_refs_vs_plan_vs_HA.csv` (plan-true positions); summit from GLO-30.
Literature check (queries run, result, tag): Covered by the same searches as card 1, plus the project grep for 190680, 611086, 190560 and 611070 across out/, out2/, main and branch_only: no hit except incidental numeric matches (file sizes in drive manifests, a sandbox CSV, a results JSON). I found no erratum. The text checked is the corpus extraction of the HA PDFs; I did not open the live HA pages. Tag: **NEW TO THE LITERATURE** (small errata).
Why it might matter: HA prelims are how most people locate these complexes, and the 2007/2008 reference points to the SC 169 / SC 61 cluster. The site is heavily looted: the SC 89 and SC 169 excavations were themselves prompted by robbery. So the wrong references also affect the protection records that are filed by map reference.
How to confirm or kill it (with data in hand, or what is missing): (a) and (b) are checked in both languages. (a) is killed if the IAA site file for A-4361 or A-4687 carries 190680/611086 for a reason, for example a shared survey datum point. Nothing in either report says so. (c) is killed if Plan 1.3.2's frame in fact extends into the NE quadrant: check the SC 97 label on the PDF p. 17 render.
Confidence: high for (a) and (b); medium for (c).
Touches the Copper Scroll? no

---

## Dead ends
- **PNAS 2025 "Siloam Tunnel, whose level is 2.5 m lower" than Channel II** (round-1 leftover): it matches Reich & Shukron 2021, "ca. 2.40 m lower" (bucket doc `Reich-and-Shukron-2021-…-b71a9fc8`, PDF pp. 26 and 296). Closed, no find.
- **A6-1 kill test (the final Birket al-Hamra report):** no Birket/Siloam report in HA through vol. 137 (28 Dec 2025; the nearest is 27736, City of David Areas U and C, Vukosavović & Shalev). A web search (`Birket el-Hamra Szanton Berko Vukosavović 2026 …`) found only the 2024 conference paper and the 2025 press. A6-1 stands as it was.
- **PNAS citation of Frumkin et al. 2003** (wood 810–780 BC, short-lived plant 770–550 BC, from the tunnel's lowest plaster): the wood date is only a terminus post quem, so it agrees with "tunnel a few decades after the dam". No contradiction. Frumkin 2003 is still not in the corpus.
- **Cana IAA 75, Table on PDF p. 14, against HA 2008:** 18 of 19 areas agree within 10–40 m (median +15/−4 m, used as the control in card 1). Area E is printed 130 m east of HA 00603 (231770/739487 against 23164/73950). HA's text, "eastern part of Karm er-Ras", fits the 2025 value better. The area size also differs: "12 sq m" in HA, 20 in the table. Too small to card.
- **Horvat Midras 2025:** the only reference (NIG 193881/618214, Ilan's ashlar building, PDF p. 5) has no counterpart; HA 2012 (01929) gives only the 10-m-precision site reference 19400/61830.
- **Maresha III (Kloner 2010, Drive `1a3t8CI4mieeJFYuj1QUuCtjnTFhGauOL`):** no map references in the text layer, so the date the shifted references came in cannot be fixed from it.
- **HA 2014 (13685) "SC 75 … part of SC 1"** against Maresha IV "SC 2 mislabeled as SC 75": reconciled. Maresha IV PDF p. 48 says SC 1 Room 1 breaks through into SC 75 (= Macalister's SC 2).
- **OCR of the plan labels** (tesseract 5.3, per-dot crops) read about 10% correctly; the 33 needed labels were read by eye instead.
- **Cave of Salome reference** (A6-2) and the datum shift: it cannot be tested without a surveyed position of the cave. It does not affect A6-2 (8 km scale).

## Blocked inputs
- `https://overpass-api.de/api/interpreter`: curl (35) connection reset; proxy reported `ws_closed_mid_exchange`. `https://overpass.kumi.systems/api/interpreter`: curl (28) timeout after 60 s. Nominatim worked (Tel Maresha node 278470166).
- `https://en.wikipedia.org/w/api.php?...prop=coordinates&titles=Maresha`: "You are making too many requests" (rate limit).
- Drive `1o6RLaF7crF8fVBtZOA9I5y4QUDV1WrH-` (PNAS appendix) is still the HTML placeholder; the repository copy `research/assets/plans/siloam-cycle13/` is the usable one.
- Not in the corpus: Stern 2019a (SC 169 final report), BAR S2652 (Stern ed. 2014), the final HA-ESI Birket al-Hamra report.

## Reproducibility
- Esri World Imagery tiles z17 x 78238–78246, y 53398–53405. Plan page rendered with `hexview.py pdf-page … 16 --dpi 220`, rotated −90°. Dot detection: red mask r>170, g<80, b<80, blobs over 30 px.
- Scripts (private, `private2/A6/scripts/`): `fit.py` and `fit2.py` (plan → Maresha IV similarity), `reg.py` (plan → Esri), `table.py` (CSV).
