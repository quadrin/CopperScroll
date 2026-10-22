# New site models and reconstruction views — 22 October 2026

This round uses the 21 October NLI plan reads ([records](../sources/nli_photos_2026-10-21/)) and one new source crop to add two site models and four reconstruction views to the atlas. Each is built smooth and in Minecraft blocks ([Minecraft record](minecraft/README.md#round-of-22-october-2026)). The models are displays. They add no reading, identification, coordinate, rating or outcome count. Every height or position that no source gives is listed as illustrative in the model's **Sources & assumptions**; the code is `atlas/app/atlas-model-geometry.ts`, the plan records `atlas/app/atlas-site-plans.json`.

EVIDENCE = stated or drawn in the source. INFERENCE = the project's. ILLUSTRATIVE = a display choice with no source.

## New evidence: Warren 1884 Plate VII, cistern VIII

- Obtained: a public-domain crop of Warren 1884 Pl. VII (the southern sheet of "Rock contours of the Noble Sanctuary"), Internet Archive PDF page 6, with its scale bar and north arrow ([archive](../assets/plans/warren1884-plate-vii/README.md), [script](../../tools/warren_plate_vii_great_sea.py)). Plate VI, used for the Golden Gate model, stops north of the Dome of the Rock and does not show the southern cisterns.
- EVIDENCE: the plate labels "VIII / Cistern / The Great Sea" and draws it as rock hatching with one small circle beside a second label "Cistern". It draws no piers and no stair.
- INFERENCE: the hatched outline measures 37.7 × 48.4 m (about 1,360 m², ±2 m at the edge) at the plate's 2.345 px per foot. G&J 1996 p. 33 tabulate about 40 × 30 m (Schick) and 44 × 45 m (Pierotti). The circle is read as a mouth.
- No rating changes: the plate gives no date for the cistern.

## New models

### Bene Ḥezir, Zechariah and Absalom (`kidron-bene-hezir`, place `jer_kidron_mon`)

Source: Avigad 1954 ch. 4 and p. 79 ([record](../sources/nli_photos_2026-10-21/avigad1954.md)).

- EVIDENCE used: façade 5.75 + 4.13 = 9.88 m, faces south-west (p. 37), floor 8.50 m above the rock path (p. 42); porch 5.55–5.83 × 3.04–3.23 × 3.20–3.50 m; Doric columns 3.00 m, lower diameter 0.53–0.55 m; entablature 0.95 m; original porch opening about 0.80 m on the column axis; north stair 1.60 m wide, 13 steps from 1.78 to 4.68 m above the floor; chambers A–E with their pits, kokhim, cells and arcosolia (pp. 40–41); south corridor 8.30 m, 2.30 m wide, opening 1.35 m wide and 3.08 m from Zechariah's north-west corner; added façade with its 1.93 m recess and 0.78 × 1.65 × 1.30 m niche and the cell below (pp. 37–38, 46); Zechariah 5.50–5.60 m square with passages of 2.75–3.08, 2.95 and 2.68 m and a north rock wall of 15.30 m (p. 79); Absalom 20 m high, about 50 m from Bene Ḥezir (summary; p. 37).
- INFERENCE: Avigad's rounded cardinal frame is turned 45° so that his "west" is the façade's true south-west. Which wall carries which chamber dimension follows from the kokhim on each wall. Absalom is placed due north from Fig. 25's north-to-south order. *(Replaced later the same day by the registration to OpenStreetMap; see [Surroundings](#surroundings-and-registration).)*
- ILLUSTRATIVE: wall thicknesses (0.8 m), level chamber floors, kokh heights (0.9 m), the stair above its visible top, the Zechariah court ground (2 m below the tomb floor, from Slouschz's "about 2 m"), Zechariah's heights and Absalom's massing. *(The levels were replaced later the same day from the Fig. 25 elevation; see [Surroundings and registration](#surroundings-and-registration).)*
- Views: **Remains**; **Original state and nefesh (Avigad 1954)**: pale parts restore the 0.80 m porch doorway, the north doorway of A, D's 50 cm pit and the cleared corridor, and add Avigad's nefesh pyramid (Fig. 42, 1) over the added façade (base and height illustrative). The pyramid overlaps the north stair, as Avigad notes for any square base (p. 76).
- Surface colours: rock from the owner's 19 October photos of Zechariah, the Bene Ḥezir scarp and Absalom ([samples](../assets/plans/atlas-explorer/surface-samples-2026-10-17/spec.json)).

### The Great Sea, cistern VIII (`temple-great-sea`, place `jer_temple`)

Sources: Warren Pl. VII (above); G&J 1996 pp. 33–39 ([record](../sources/nli_photos_2026-10-21/gibson_jacobson1996.md)); W&C 1884 pp. 219–220.

- EVIDENCE used: the plate outline; floor 14 m below the surface and a rock roof about 2.5 m thick (Schick); rock 1.5 m below the surface (Warren); rock-cut and plastered; five piers (Schick); a stair from the south of 44 (Barclay) or 50 (Schick) steps with a well-like mouth (Whitty); three mouths in use (Wilson).
- ILLUSTRATIVE: pier places and size, two of the three mouths, the stair's line and width, and a display cutaway of the roof west of x = −4 m.
- The model sits at the Temple enclosure's anchor (Pleiades, about 150 m), not at the cistern's position under the southern court. This is stated in its limit. *(Replaced later the same day: the plate is registered to the mapped Haram corners; see [Surroundings](#surroundings-and-registration).)*

## New views of existing models

| Model | View | Source | What the view adds |
|---|---|---|---|
| Hyrcania (`hyrcania-waterworks`) | Remains (updated) | Patrich 2002 pp. 343–351 ([record](../sources/nli_photos_2026-10-21/aqueducts_ilan_hyrcania_qumran.md)) | East bridge 112 m long, 2.5 m at the base and 1.45 m at the top, 6 m high (drawn at its maximum along its whole length); round pit 3.05 m across and 4.3 m deep; point 49 built tunnel, 11.5 × 1.25 × 0.75 m, barrel-vaulted, south end blocked; southern pool rock-cut, unplastered |
| Hyrcania | Herodian bridge (Patrich 2002) | Patrich 2002 p. 348 | Pale upper wall from 6 to 12.5 m and a 0.5 m channel. Feldman's 170 m / 16.78 m saddle wall is recorded as an alternative, not drawn |
| Bethesda (`bethesda-pools`) | Remains (updated) | Pierre & Rousée 1981 pp. 24–25 ([record](../sources/nli_photos_2026-10-21/probatique_poc31_1981.md)) | Dam 40 m long, so the north pool is drawn 40 m east–west and 53 m north–south (INFERENCE); square 1 × 1 m shaft |
| Bethesda | Royal period (Pierre & Rousée 1981) | pp. 24–25, Fig. 3, Pl. 1 | Dam with rock base and masonry, shaft and corridor; no south basin; pale valley floor; open rock-cut canal 0.75 × 1 m running south |
| Gerizim (`gerizim-precinct`) | Persian precinct (Magen et al. 2004) | p. 3* ([record](../sources/nli_photos_2026-10-21/gerizim_I_2004.md)) | Precinct 98 × 96 m with a six-chambered north gate and pale south and east gatehouses; no west gate |

Not drawn, and why:

- Bethesda Hellenistic phase: Pierre & Rousée's vaulted canal under about 2 m of fill cannot be placed against Duprez's 14 m basin depth from the reported figures.
- Hyrcania Hasmonean phase and the Herodian line beyond the bridge: no section, level or route is published in the pages read.

Also updated: the A(C)94 feature in `jericho-ac` now quotes Netzer's Plan 12 levels (floor 99.45–99.85, rim 102.67–102.75, the 102.87 / 102.80 pipe junction) from the 21 October [plan-sheet record](../sources/nli_photos_2026-10-21/netzer2001_plan_sheets.md). The pipe-level definition is still unknown.

New terrain patches (Mapterhorn, the existing tool) for `jer_kidron_mon` and `jer_temple` let both new models sit on modern relief ([manifest](../assets/plans/atlas-explorer/terrain/manifest.json)).

## Surroundings and registration

Later on 22 October the two new models were placed in their real setting, so that they no longer stand on an isolated bench. Data: one OpenStreetMap extract (ODbL; [record](../assets/plans/osm-context-2026-10-22/README.md)) and two Mapterhorn terrain patches, 2.4 km square at 5 m spacing ([Kidron](../assets/plans/atlas-explorer/terrain-wide/jer_kidron_mon-manifest.json), [Temple](../assets/plans/atlas-explorer/terrain-wide/jer_temple-manifest.json)). Code: `tools/build_osm_context.py`, `atlas/app/atlas-model-context.ts`. No reading, identification, coordinate of a Copper Scroll candidate, rating or outcome count changes.

- New evidence: the OSM outlines of Bene Ḥezir, Zechariah and Absalom, the Haram's two south corners, and the mapped paths, stairs, cemetery areas, walls and buildings around both models. Also measured: the Haram's south corners on Warren Pl. VII ([plate record](../assets/plans/warren1884-plate-vii/README.md)).
- INFERENCE (Kidron): Avigad's frame is placed on the mapped porch and turned so that his "west" faces 244.8° (outline 244.3°, Zechariah's position 245.3°). Absalom stands at its mapped centre, 52.1 m from the porch (Avigad about 50 m). The model's rock path is the modern terrain at Absalom.
- INFERENCE (Great Sea): the plate's south wall is fitted to the mapped one (1.07 m at each corner, turn 0.17°). The cistern then lies under the court between the Dome platform and the north front of al-Aqsa. Its surface is the modern terrain there.
- ILLUSTRATIVE: the ground pads that level the Kidron valley floor in front of the tombs and raise the slope behind them to the rock surface (the terrain model is too coarse to show the scarp); grave rows inside the mapped cemetery areas (about 1 × 2 m, long axes east–west, or across the qibla in the Muslim cemetery; none where the ground under a grave falls more than 1.2 m); default path, wall and building sizes where OSM maps none (paths 2.4 m, city walls 12 m, gate buildings 9 m, buildings 6.5 m).
- Second pass (the setting still looked bare): mapped roads (asphalt, 3.5–8 m wide by class), 142 + 154 mapped single trees, trees about 7 m apart in mapped woods (pines) and orchards (olives), and green ground in mapped woods, orchards and grass, smooth and in blocks. At the Kidron the rock pad behind the façades now runs 14 m south past Zechariah, and a shoulder further back covers the north side, where the scarp bends east towards Absalom; paths are not draped where the ground is steeper than 45°. ILLUSTRATIVE: tree sizes and the planted trees' places.
- Levels from Fig. 25 (third pass, after the owner's photographs showed no drop at the monuments' feet): Avigad's west elevation was measured on the owner's photo of the foldout ([record](../sources/nli_photos_2026-10-21/avigad1954.md#fig-25-west-elevation-levels-measured-on-the-photo-22-oct-2026)). Its ground line is the rock path (the Bene Ḥezir floor measures 8.5 m above it, as p. 42 says). The model now takes from it Absalom's podium (2.1 m) and the heights of all its parts, the Jehoshaphat door sill at 1.9 m with steps beside Absalom, court walls to 9 m at Absalom and to 16.9 m at Zechariah, Zechariah's visible foot at 7.7 m and its heights, the ground climbing in front of the scarp (4.6 m at the court's north wall, 6.7 m at its south wall), terraced grave fill in the court, and two openings in the scarp below the façade. Widths of the ramps and the members' detail stay illustrative.
- Display: both models now keep the place frame (no recentring). The Minecraft builds get rings: 1 m blocks to ±304 m with the mapped surroundings in blocks (paths and stairs as paved ground, graves, walls, buildings) and 8 m blocks of terrain to ±1,152 m.

## Mapped surroundings for six more sites

Later still on 22 October the same treatment was given to the other models drawn in metres, so that they stand in modern terrain among today's mapped features instead of on an isolated bench. Data: five more OpenStreetMap extracts (ODbL; [record](../assets/plans/osm-context-2026-10-22/README.md)) and five more Mapterhorn patches (manifests in `../assets/plans/atlas-explorer/terrain-wide/`). No reading, identification, coordinate of a Copper Scroll candidate, rating or outcome count changes.

| Model | Placement (INFERENCE) | Uncertainty |
|---|---|---|
| Qumran settlement (`qumran-settlement`) | traced frame centred on the mapped settlement outline (99.7 × 142.8 m), unturned | some tens of metres; bearing the source's |
| Bethesda (`bethesda-pools`) | the dam on the mapped excavation area (82.6 × 51.6 m), unturned | about 25 m; bearing assumed, as before |
| Golden Gate (`east-gate-warren`) | gatehouse on the mapped Golden Gate building, turned 5.5° to its long sides | a few metres: Warren's gatehouse 24.8 × 17.3 m, mapped building 27 × 17 m |
| Jericho pools (`jericho-early`, `jericho-late`) | not registered: at the site anchor | about ±300 m |
| Gerizim (`gerizim-precinct`) | not registered: at the anchor on the summit, the summit platform on the modern summit | the anchor's |
| Hyrcania (`hyrcania-waterworks`) | not registered: at the anchor, unturned (no north arrow in the source) | about ±200 m, bearing unknown |

- ILLUSTRATIVE: each model's levelled ground where its display bench meets the modern terrain (at Hyrcania a flat area on the hill); the confined pads that keep Warren's Haram surface and the ground at the wall's foot at the Golden Gate.
- Not done, and why: the relative-unit models (Qumran aqueduct and Reeder plan, Jericho Area AC, Siloam receiver, Doq) are not drawn at a known scale, so mapped surroundings in metres would mislead; Abu Saraj IV/17 has no position.

## Placed by satellite imagery (night of 22 October)

The models of Gerizim, Jericho (both) and Hyrcania stood at their place anchors, and the Qumran settlement on the centre of a large mapped outline. Their source plans are now registered to Vantor WorldView-2 imagery of 21 October 2023 (Esri World Imagery, stated accuracy 5 m), and the models stand where the plans put them ([records](../assets/plans/imagery-registration-2026-10-22/README.md); tool `tools/imagery_registration.py`).

- New evidence: none from the sources. The imagery is a modern observation of the visible ruins, used for measurement only and not archived.
- INFERENCE (placement): Gerizim from Magen 2008's site and precinct plans (the two agree within 1–2 m); Jericho from Trümper Fig. 18 (Netzer's plan north points about 10.6° east of true north); Hyrcania from Patrich 1989 Fig. 22 (page-up about 4.75° west of north; its contours then follow the elevation model); Qumran from Magen & Peleg Fig. 9 (moved 15.7 m). Fits agree with the imagery within about 2–3 m.
- Changed geometry: Gerizim is rebuilt in the place frame from the plans (core walls as drawn; reported envelopes at their drawn places; the four unsourced 22 × 16 m courts are dropped). Hyrcania's installations now spread round the hill where Fig. 22 draws them, each on its own modern ground, and its blocks are 0.5 m. Jericho and Qumran are moved and turned, unchanged in shape.
- Bethesda is not refined: the pools lie in shade under trees in the imagery, and no figure ties the model to a mapped building.
- Photogrammetry of the Kidron photos (to improve the ground at the monuments' feet) failed: 3 of 62 images registered ([note](../assets/plans/kidron-field-2026-10-19/README.md#photogrammetry-test-22-october-2026)).
- No reading, identification, rating or outcome count changed.
