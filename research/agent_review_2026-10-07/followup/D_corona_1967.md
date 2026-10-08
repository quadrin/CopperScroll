# D — CORONA KH-4B frames DF040–042, 26 September 1967 (GOALS R07 item 6; task 9)

Coordinator report, 7 October 2026. Labels: EVIDENCE = visible in the frame; INFERENCE = interpretation.

## Data

| Frame | USGS entity ID | Download | Main target |
|---|---|---|---|
| DF040 | DS1101-2168DF040 | Standard Format, 673.5 MiB | ʿEin Samiya / Kh. el-Marjama |
| DF041 | DS1101-2168DF041 | Standard Format, 692.9 MiB | Tell es-Sultan / Jericho |
| DF042 | DS1101-2168DF042 | Standard Format, 655.2 MiB | Qumran / ʿEin Feshkha / Buqeia |

- Declass 1 (corona2), mission 1101-2, forward camera, "Stereo High", black and white, already scanned. They are free from EarthExplorer with a login.
- Each download is a `.tgz` of four 8-bit TIFF tiles (`_a` to `_d`), each 33,756 × 10,199 px. Tile `_d` holds the Jordan Valley end of the strip.
- The EE metadata corners for DF041 (NW 31.916 N 34.983 E; NE 32.25 N 37.35 E; SE 32.133 N 37.416 E; SW 31.783 N 34.983 E) are nominal.
- Measured on the images, each frame covers about 0.14° of latitude at Jericho's longitude:
  - DF041 ≈ 31.75–31.89 N;
  - DF040 ≈ 31.88–32.03 N;
  - DF042 ≈ 31.62–31.77 N.

## Geometry and method

- **Scale:** about 1.7–1.9 m per pixel at full resolution in tile `_d` (ISAC/CAMEL gives 2 m and 1:247,500). Panoramic distortion grows toward the frame ends, so positions far west in the tile (e.g. Hyrcania) are less certain.
- **Rotation:** the strip runs ENE, so image "up" is about **9.4° west of true north**. This was measured from the EE corner coordinates and confirmed by matching.
- **Matching:** each target was located by matching the frame by eye to modern satellite imagery (Esri World Imagery, rotated +9.4°, viewed at the same scale). Natural features were used: the Wadi Qumran gorge, the ʿEin Samiya gorge and spring, the Jericho escarpment, and the Wadi Qelt and ʿAin Duk fields. Automatic SIFT registration failed because 55 years of change left too few matches.
- **Accuracy:** positions marked "approx." are good to about ±100–150 m (Hyrcania ±500 m). The modern imagery is not committed.

## Positions used (tile `_d`, full-resolution pixel x, y)

| Frame | Feature | Pixel (x, y) | Note |
|---|---|---|---|
| DF041 | Tell es-Sultan (approx.) | 18700, 2630 | SE corner of the camp texture, where cultivation begins |
| DF040 | ʿEin Samiya spring | 14870, 2210 | east end of the gorge cliffs |
| DF040 | Kh. el-Marjama knoll (approx.) | 14960, 2125 | NE of the spring |
| DF040 | dark square | 15118, 2335 | ≈ 31.9892 N, 35.3363 E (±100 m); ~420 m from the tell at ~130° |
| DF040 | Zissu's grid point 181/155 | 14650, 2400 | SW slope |
| DF042 | Wadi Qumran gorge exit | ~18470, 3020 | |
| DF042 | Kh. Qumran (approx.) | 18670, 2950 | |
| DF042 | ʿEin Feshkha (approx.) | 18093, 4489 | on the 1967 shore |
| DF042 | Hyrcania / Kh. el-Mird (rough) | 13320, 3640 | ±500 m |

## Observations

### Jericho / Tell es-Sultan (DF041) — [figure](figures/CORONA_1967_Jericho_Tell_es-Sultan.jpg)

- EVIDENCE: The oasis, the town, Wadi Qelt and the ʿAin Duk/Nuweiʿima field strip are clear.
- EVIDENCE: North of the tell, between the two roads, there is a light, finely textured area about 1 km across. It sits where the ʿAin es-Sultan refugee camp stands today. INFERENCE: this is the camp, built in 1948. In September 1967 it was probably emptied after the June war but still standing.
- INFERENCE: **CORONA therefore shows no surface north of the tell from before the camp.** Shaft or tomb openings (1–2 m) are below the resolution anyway. Only the 1918 Bavarian frames (BS Pal. 1031/1032) and the 1945 RAF verticals (PS30 5107/5137) predate the camp.

### ʿEin Samiya / Kh. el-Marjama (DF040) — [figure](figures/CORONA_1967_Ein_Samiya_Kh_el-Marjama.jpg)

- EVIDENCE: The gorge cliffs, the spring at the gorge mouth, the knoll NE of the spring (Kh. el-Marjama) and the irrigated plots of 1967 are clear. The plots run ~600 m SSE down the valley floor. There is no modern road; only tracks.
- EVIDENCE: A small **dark square, about 15 m across**, lies ~420 m SE of the tell, at the east edge of the 1967 plots. A dark bar lies just SW of it.
- INFERENCE: The square could be a pool or reservoir (water images dark), a stand of trees or a structure. It cannot be told apart at this resolution. It sits SE of the tell, near the eastern edge of Byzantine Kh. Samiya ([B §4](B_kh_el_marjama.md)).
- No source describes a pool at this spot. Kallai's rock-cut pool could be this feature or something else.
- **Test:** the 600-dpi RAF scans PS32 5038 / PS30 6054 (1945; ~0.6 m pixel). A ground check would also settle it.

### Qumran / ʿEin Feshkha (DF042) — [overview](figures/CORONA_1967_Qumran_Feshkha.jpg), [Kh. Qumran close-up](figures/CORONA_1967_Kh_Qumran_fullres.jpg)

- EVIDENCE: The Wadi Qumran gorge, the escarpment, a 1967 road, a dark marsh/reed belt ~3 km long below the cliffs, and the 1967 Dead Sea shoreline are visible.
  - The road runs from the NE, bends near Qumran and heads S toward Feshkha, slightly west of today's route.
  - The marsh/reed belt ends at ʿEin Feshkha on the shore. INFERENCE: this ground is dry today.
  - The 1967 shoreline lies ~0.9 km ESE of Kh. Qumran.
- EVIDENCE: The Kh. Qumran ruins, the aqueduct, the dam and the pools do **not** resolve through the film grain. Cave mouths in the cliffs north of Qumran (Caves 1–3) are far below the resolution; those cliffs are at the frame's top edge.
- ʿEin el-Ghuweir (31.628 N) falls just south of the frame.

### Buqeia / Hyrcania (DF042) — [figure](figures/CORONA_1967_Buqeia_Hyrcania.jpg)

- INFERENCE: The broad smooth plain in the crop is probably the Buqeia. Hyrcania's position is rough (±500 m) because the panoramic scale changes toward this part of the frame.
- The Iron Age forts and dams were not checked at full resolution.

## Limits

- At about 2 m per pixel, CORONA gives the 1967 layout: roads, fields, marsh, shoreline, large ruins and the camp. It cannot resolve pools under ~10 m, cisterns, tombs or cave mouths.
- Film grain is heavy at full resolution, and contrast is low on bright desert surfaces.
- The next step is the 1945 RAF verticals at 600 dpi:
  - PS30 5107/5137 — north of the tell, before the camp;
  - PS32 5038 and PS30 6054 — ʿEin Samiya, to test the dark square;
  - PS29 6140 — Qumran.
