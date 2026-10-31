# Novel directions on full-resolution imagery, 31 October 2026: index of four parallel runs

On 31 October 2026, four workers ran at the same time. Three reran the 30 October directions A, B and C as A2, B2 and C2. They used the full-resolution 1988 photographs of the West Semitic Research Project (WSRP) instead of the public previews of the University of Southern California (USC) Digital Library. The fourth worker started direction E, stereo elevation models from the 1974 HEXAGON (KH-9) film, which was blocked on 30 October. The work was AI only: no fieldwork, purchase, contact or human reader.

Each direction has its own branch, its own folder `research/novel_2026-10-31/<direction>/` and its own `NOTE_2026-10-31.md`. Each worker committed and pushed a frozen protocol (SHA-256 in the commit message) before its one confirmatory run. Every rule, threshold and result of 30 October had been seen, so each protocol is labelled a **new model**. The 30 October results stand as recorded in [the 30 October index](https://github.com/quadrin/CopperScroll/blob/claude/novel-2026-10-30-summary/research/novel_2026-10-30/README.md).

## Results

| Dir. | Branch (final commit) | Frozen SHA-256 (freeze commit) | New dataset | Result |
|---|---|---|---|---|
| A2. Photometric stereo | `claude/novel-2026-10-31-A2` (6a309e75) | a75f7916… (1037f3b6); split committed earlier in 3cfb4453 | `reg/*.json` (registration residuals), `confirmatory/placements_all.csv`, `split.csv` | **Not obtained.** The frozen letter rules were right on 7 of 13 held-out controls; p = 1.0 against a chance caller that allows for class imbalance. No target was scored. |
| B2. Analysis by synthesis | `claude/novel-2026-10-31-B2` (f3543d57) | 6607ea44… (15bd32c0) | `calibration_items2.json` (76 training, 33 held-out lines), `calibration_rankings2.csv`, `heldout_result2.json` | **Not obtained.** The true reading beat every observed competitor on 2 of 25 held-out lines; 4.89 expected under the exact null; P(T ≥ 2) = 0.98. Targets were not scored. |
| C2. Engraver hand on the copper | `claude/novel-2026-10-31-C2` (8f704f98) | 41dbb86e… (2b3c9b0b) | `out/copper_frames.csv` (24 frames), `out/copper_bands.csv` (318 line bands) | **Not obtained.** The measurement gate failed: only 8 of 24 frames had a usable line pattern. The III 7 claim is not identifiable from these frames. |
| E. HEXAGON 1974 stereo | `claude/novel-2026-10-31-E` (550af9e0) | c2239193… (ae8780af); exclusion zone committed earlier in 26d6a59e | `zones.geojson`, `results/confirm_JUN74_*.json`, `masking_log.csv` | **Not obtained.** No counted zone reached the frozen precision (NMAD ≤ 2.5 m against GLO-30 on held-out stable ground): Wadi Qelt 27.4 m, Jericho outskirts 22.2 m. Qumran (5.7 m) had too few valid cells to count. The Kidron zone lies outside the forward frame. |

Abbreviations: NMAD, normalised median absolute deviation. GLO-30, the Copernicus 30 m global surface model (2011–2015). ASP, NASA Ames Stereo Pipeline. W2F, the project's letter boxes on the Puech 2006 plates. ETCBC, the Eep Talstra Centre for Bible and Computer transcription (Abegg, Bowley, Cook).

## Checks by the orchestrator

For each of the four branches:

- The freeze commit is an ancestor of the result commit. For A2 the split commit is an ancestor of the freeze. For E the exclusion-zone commit is an ancestor of the freeze.
- The protocol hash is the same in four places: the file at the freeze commit, the file at the branch tip, `PROTOCOL_FROZEN.sha256`, and the commit message.
- Only the freeze commit touches `PROTOCOL_FROZEN.md`.
- No image, raster or array file is in the repository. Every changed file is inside the direction's folder. The largest file is E's `zones.geojson` (169 KB).
- No run changed a rating, the outcome ledger, ACTIVE_TEST, OPEN_QUESTIONS or the atlas data.

## Access: the full-resolution store

- **Store.** Private Google Cloud Storage bucket `copper-scroll-cog-1030`. It holds lossless Cloud-Optimised GeoTIFF (COG) copies and page-split PDFs. The final `index.json` (built 05:07:28 UTC) lists HEXAGON 27 archives / 183 tiles, CORONA 3, USC 93, photos 7, PDFs 99 (32,232 pages) and videos 9, with an empty protected list. All 283 tiles indexed at the first check were present with the indexed sizes.
- **Reader and notes**, fetched from the bucket `tools/`: `hexview.py` (SHA-256 56b21cb0d32b7d3caf1fe1f130493791898d768c087964fe5a745d0dc7630236), `README.md` (885bad09…) and `SULTAN1.md` (8abcfe31…). The store note gives no hash for `hexview.py`, so the observed hash is recorded here. All worker reads went through `hexview.py`.
- **Credentials.** The read-only HMAC key worked through the session proxy. `WSRP_MEDIA_KEY` was not set and was not needed.
- **HEXAGON build.** `hexview.py ls 1208` lists 12 frames (F010–F015, A011–A016). `ls 1209` lists 13 frames (F013–F018, A013–A019). The build was complete, so E had every frame.
- **USC delivery.** The delivery has cuts 2–8, 10, 11 and 16–23. Cuts 1, 9 and 12–15 are not in it. A typical frame is 3130 × 5447 px RGB, about 155 px per cm. A letter is about 100–150 px high, against about 27 px in the previews.

| Access test (`hexview.py`) | Wall time |
|---|---|
| First test: `crop usc:DSS_3Q15_CT10_RCT_T - 1565 2700 --size 2000` | 3.9 s |
| First test: `pdf-page Kochavi 1 --dpi 200` | 1.7 s |
| First test: `frame EV10-0125 4` | 1.4 s |
| Second test: `crop 1208-400636A015 a 18640 12334 --size 2000` (HEXAGON) | 1.9 s |
| Second test: `pdf-page Kochavi 2 --dpi 200` | 1.9 s |
| Second test: `frame EV10-0126 5` | 1.6 s |

- **Orchestrator reads before the reader was available.** The bucket was first listed with boto3. One full-resolution window was read with a stand-in rasterio reader: `D3C1209-200214F016` tile d, x and y 10000–12048. It was not displayed or saved. `SULTAN1.md` puts the tell in F016 tile b at (19406, 20648), two tiles away. That is an INFERENCE from the tile layout, not a registration; E did not register the December pair. After the owner's instruction only `hexview.py` was used.
- **Orchestrator exposure.** For the access test the orchestrator looked at a reduced view of a 2000 px window of cut 10 (CT10 RCT). Cut 10 was a C2 control cut and an A2 cut. No worker saw that view, and no parameter came from it.

## Per direction

### A2. Photometric stereo on the 1988 frames

- **AGENTS.md line: not identifiable from available evidence.** The claim was "these photometric rules separate ב/כ, ה/ח and ח/ת on the 1988 frames". The test was **not obtained**: 7 of 13 held-out controls were right (p = 1.0). Only 13 held-out letters could be scored. The ה/ח rule was right on 3 of 8.
- **New observation.**
  - Top-lit and bottom-lit frames now register without depending on the shading sign: strip outline first, then gradient magnitude. The median residual is 1.57–2.66 px on 12 cuts. It fails on cuts 5 and 10.
  - Letters are placed by correlating each 1988 strip with Puech 2006's photograph of the EDF copy, then mapping the W2F boxes into the 1988 frame. The gate accepted 12 cut/column pairs. Cut 7 carries the right part of column III and cut 8 the left part.
  - Cut 17 as a whole strip matches column X (score 3.10) better than IX (1.20). No half-strip test was run, so IX 10 at the strip's edge is not excluded.
- **What it changes.** Registration and placement are no longer the limit. The limit is the weak ב/כ and ה/ח relief signal, even on training data (leave-one-out balanced accuracy 0.65 and 0.66), and the small held-out set.
- **Limits.** Light directions come from the frame titles, with the elevation fixed at 30°. Before the freeze the worker viewed full-resolution crops of cuts 3, 6, 7 and 8 that contain held-out letters. No held-out feature was computed before the freeze, and the scoring is automatic.
- **Further AI-only session:** not justified for these relief rules on the 1988 frames. The registration and placement outputs can be reused (see "Across directions").

### B2. Analysis by synthesis on the 1988 frames

- **AGENTS.md line.** The claim "this forward model can read one-letter differences on the 1988 frames" is **rejected for this specification**. The test was **not obtained**: T = 2 of 25 observed held-out lines, against 4.89 expected (P = 0.98). The training lines also show no signal (T = 4 against 3.6). The targets (IX 10, I 12, X 15, XII 10) stay **not identifiable from available evidence** by this model. VII 11 cannot be scored, because cuts 13–14 are absent.
- **New observation.**
  - The learned letter templates collapse to the same top and bottom edges of the line band in every column. The model locks onto text rows, not letters.
  - SIFT alignment across lights found only 0–108 inliers, so each frame was scored on its own.
  - The 1/K chance baseline is too high for sets made of the true line plus one-letter variants. The exact null is the product of 1/(a + 1) over the varied letter positions, where a is the number of variants at a position. It gives about 1/32 for five variants at different positions, not 1/6.
- **Deviations.** The model worked at half resolution. The groove cross-section was set in advance, not fitted to measured profiles. "Undisputed" was decided per word, not per line. Before the split existed, the worker viewed one crop of about III 5–9; it may include the held-out line III 9.
- **Orchestrator check (exploratory, after B2's result, no record changed).** The 30 October B test used p = 1/K. Its candidate sets have the same shape as B2's: 10 of the 13 held-out lines have 5 one-letter variants. With the exact null computed from the round-1 `calibration_rankings.csv`, its held-out count of 4 of 13 has an expected value of 0.78 and P(T ≥ 4) = 0.0045. Without VII 13 (round 1 traced its letter forms from the column VII strip 13) the count is 3 of 12, expected 0.53, P(T ≥ 3) = 0.014. Under the registered 1/K null it was 2.4 expected, p = 0.21.
  - Meaning: the 30 October null is a **documented analytical error**, which AGENTS.md accepts as a reopening condition. The 30 October result is kept as registered. This check is not a confirmation. The exact null assumes that the model compares the true and the variant letter without a systematic bias, and that assumption is untested for the round-1 model.
- **Further AI-only session: justified, for one bounded test that is not B2's pipeline.** Run the round-1 B model, frozen and unchanged, on lines it has never scored (for example B2's 33 held-out lines). Register the exact null and a decoy-truth bias control (sets in which a variant takes the place of the truth) before scoring. A pass would let the targets be scored. A fail would close the analysis-by-synthesis route on the present images.

### C2. Is the III 7 change on the copper?

- **AGENTS.md line: not identifiable from available evidence.** The claim was "the letter-proportion change found in Puech's drawing between III 6 and III 8 is present on the engraved letters". The test was **not obtained**. The measurement gate failed: cut 7 had 2 usable frames of 6, cut 8 had 1, cut 10 had 2, and cut 16 had 3 (4 needed per cut). On the usable frames the column III change and the control change were the same: +0.033 and +0.035, p = 0.50.
- **New observation.**
  - Three records agree that column III is on cuts 7–8: the Puech 2006 radiograph plates CCCXXXVII–CCCXXXVIII, `controls_manifest.csv`, and round-1 A `map_cuts.py`.
  - The light codes are R + {L, C, R} + {T, B}. L, C and R are three views of the curved strip. T and B are light from the top and from the bottom.
  - These are the first measurements of letter height against line pitch on the 1988 frames of column III and the control cuts.
- **What it changes.** The III 7 change remains a feature of Puech's drawing only. It is not shown on the copper. No model of the list should treat it as an engraving feature until it is measured on the object.
- **Exploratory, after the run.** XI 7–8 on the exposed cuts 19–20 was uninformative (2 of 12 frames usable). The seams S11 and S49 were not run.
- **Further AI-only session:** not justified with automatic band measurement on these frames. It is justified only with letter-level boxes on the copper (see "Across directions").

### E. Stereo elevation models from the HEXAGON 1974 film

- **AGENTS.md line.** No identification claim was tested. Change detection is **not identifiable from available evidence**. The test was **not obtained**: the frozen failure condition is met. Pair used: June 1974, `D3C1208-400636F014` (forward) / `A015` (aft).
- **New observation.**
  - F014/A015 works as a stereo pair: 2,400–10,000 tie points per window, with real wadis and ridges in the relief image.
  - Without the panoramic (optical-bar) camera model the heights are not recovered. The fitted height per disparity pixel is 0.09–3.6 m, against about 5.2 m expected. The error grows with slope.
  - ASP 3.5.0 was installed from its GitHub release and runs. Its KH-9 route (`cam_gen --camera-type opticalbar`) needs the four frame-corner longitudes and latitudes. The store index has no corner fields, and USGS EarthExplorer needs a login. So the camera model was not used.
- **What it changes.**
  - HEXAGON stereo without the camera model cannot supply the finer elevation model that direction F (30 October) named as its reopening condition. Its error is at least about 4.4 m even on gentle slopes.
  - Even at the target precision, comparison with GLO-30 could find only changes about 50–60 m across. Cisterns, tombs and most pools are smaller.
  - GLO-30 includes buildings and trees, so only bare-ground changes could mean a lost depression.
  - No 1978 elevation model is possible: the store holds only forward frames for 1978.
- **SULTAN-1.** E set an exclusion zone before any read (commit 26d6a59e). After `SULTAN1.md` (A1 opened reading; HEXAGON failed the 0.5 m gate on 26 October and cannot test SULTAN-1), E dropped the mask. It recorded the reason in the protocol before the freeze. The Jericho-outskirts window, read at 1/2 scale, contains the tell and the 250 m strip north of it; E did not view its products. Every read is in `masking_log.csv`.
- **Deviations.** The confirmatory run stopped at the Kidron zone (no tie points: the zone lies beyond F014's last row). The Jericho-outskirts zone was then run alone with the same frozen code. The pass took about 2 h 45 min.
- **Further AI-only session:** justified only if the USGS frame-corner metadata for F014, F015, A015 and A016 becomes available, for one ASP optical-bar run. Even then, the 50–60 m detection limit against GLO-30 means that such a run suits only a named question about features of that size.

## Across directions

- **A2's placement is the input that B2 and C2 lacked.** B2 failed because its model could not find letters. C2 failed because band-level measurement is too noisy. A2 now maps W2F letter boxes into the 1988 frames for 12 cut/column pairs, including column III on cuts 7 and 8 (`confirmatory/placements_all.csv`, `reg/*.json`). A future B or C test could use those positions as a new frozen specification.
- **Caution for C.** The W2F boxes come from the Puech 2006 copy plates, so box sizes taken from them would import the drawing. For C, only the box centres may be used. Letter extent must then be measured on the copper.
- **Common limit.** The three letter directions used the same 1988 series. Cuts 1, 9 and 12–15 are absent, so VII 11 cannot be scored, and controls on those cuts are ineligible.

## Fieldwork wish list

The wish list is in Drive: "Wish list — fieldwork and equipment (after online work is exhausted)", written 30 October 2026.

- **No result shows that a wish-list item is now the only route left for a conclusion.** No item was started.
- Object item 1 (new 3D, reflectance transformation imaging (RTI) and X-ray fluorescence (XRF) imaging of the originals) asks first for "the online photometric-stereo and render-and-compare work on the 1988 USC frames". A2 and B2 have now run at full resolution, and neither separated ב/כ or ה/ח. Two AI-only routes are still open, so item 1 is not yet the only route:
  - the frozen round-1 B model under the exact null;
  - A2's letter positions as input to a new B or C specification.
- Object item 4 (a human blind panel) asks first for "an AI multi-reader panel with exposure logs". That has not been tried.

## Image products

- No crop, depth map, rendering or image figure is in the repository.
- Image products are in the session workspace, `products/<direction>/` in the scratchpad: A2 figures with a 1.2 GB cache, B2 99 MB, C2, and E about 100 MB.
- They were not put in Drive (`08 Working files/novel reruns 2026-10-31/`). The Drive connector in this session takes file content only as inline text, which does not suit these image files.
- The key figures (at most 5 per direction) were sent to the owner as one archive in the session. The workspace is temporary.
- USC/WSRP terms forbid publication of the 1988 images. A2's overlays also contain Puech 2006 copy plates, so both sets of terms apply.
