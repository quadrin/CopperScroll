# Warren 1884, Plate VII — the Great Sea (Cistern VIII) area (22 October 2026)

Source: Charles Warren, *Plans, Elevations, Sections, &c., shewing the results of the excavations at Jerusalem, 1867–70* (PEF 1884), Plate VII, "Rock contours of the Noble Sanctuary" (the southern sheet; Plate VI is the northern one). Internet Archive [planselevationss00warr](https://archive.org/details/planselevationss00warr) (BYU Library scan), PDF page 6. The PDF's SHA-256 is `9b8d2824…7c7bcf`, the same file used for [Plate VI](../warren1884-plate-vi/README.md). Public domain.

Made by [`tools/warren_plate_vii_great_sea.py`](../../../../tools/warren_plate_vii_great_sea.py) from the plate's 600 ppi line-art mask (5986 × 4835 px), inverted to black on white. Pixel boxes and file hashes are in `measurements.json`.

Files:

- `great-sea-area.png` (source crop): cisterns VI, VII, **VIII "Cistern The Great Sea"**, IX, XI and XXXIII, with the overlying dashed building lines and the 2409 rock contour. Warren draws each cistern as rock hatching.
- `great-sea-tracing.png` (project tracing over the source crop): the traced outline of VIII in red and the small circle beside its second label "Cistern" in blue.
- `scale-bar.png`: the plate's "SCALE OF FEET 1/1000". Ticks at 300 ft (x 3193) and 500 ft (x 3662) give 2.345 px per ft (0.130 m per px), the same as Plate VI.
- `north-arrow.png`: plate north is 8.8° clockwise from plate up (least-squares line through the arrow shaft; Plate VI gave 9.4°).

Measured results (EVIDENCE = drawn on the plate; INFERENCE = the project's):

- EVIDENCE: Cistern VIII is labelled "VIII / Cistern / The Great Sea". It lies south of the dashed building lines in front of cistern VI, west of VII and north of IX and XI.
- INFERENCE: the hatched area traced as VIII measures 37.7 × 48.4 m on the plate's axes and about 1,360 m² in plan. The published sizes are about 40 × 30 m (Schick) and 44 × 45 m (Pierotti), as tabulated by Gibson & Jacobson 1996 p. 33 ([record](../../../sources/nli_photos_2026-10-21/gibson_jacobson1996.md)). The traced edge is uncertain by about ±2 m.
- EVIDENCE: the plate draws no piers, no stair and no conduit inside VIII. A second label "Cistern" sits inside the hatching at its north-east; W&C p. 220 report "a small circular chamber" on the north-east. The tracing does not separate it.
- INFERENCE: the small circle beside the lower label "Cistern" is read as a mouth (shaft opening). It is the only mouth symbol drawn in VIII.

Used by the atlas model `temple-great-sea` (`atlas/app/atlas-site-plans.json`, `atlas/app/atlas-model-geometry.ts`). Mirror: `atlas/research/assets/plans/warren1884-plate-vii/`.
