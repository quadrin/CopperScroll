# Warren 1884, Plate VI — Golden Gate area (17 October 2026)

Source: Charles Warren, *Plans, Elevations, Sections, &c., shewing the results of the excavations at Jerusalem, 1867–70* (PEF 1884), Plate VI, "Rock contours of the Noble Sanctuary". Internet Archive [planselevationss00warr](https://archive.org/details/planselevationss00warr) (BYU Library scan), PDF page 5. Public domain.

Files (1-bit crops of the 601 ppi line-art layer, inverted to black on white):

- `golden-gate-area.png`: the dashed Golden Gate outline, the Haram east wall, cistern XV, the "Massive Wall" with its 2338.5 level, and the square marked 2308.
- `scale-bar.png`: the plate's own scale of feet (0 ft at x 2563, 500 ft at x 3735 → 2.344 px per ft). The plate is reduced from its printed 1:1000.
- `north-arrow.png`: plate north is about 9.4° clockwise from plate up.
- `measurements.json`: pixel coordinates, the conversion to metres, derived levels and the differences between the plate and the SWP text.

Measured results:

- Golden Gate outline: 24.8 × 17.3 m (81 × 57 ft), its east side on the wall line.
- Cistern XV: 18.3 ft across on the plate (SWP p. 221: "about 18 feet"), centre 30.0 m west of the gatehouse's west face. This repeats the earlier finding F12.4 ([leads_on_old_plans_2026-09-30.md](../../../sites/leads_on_old_plans_2026-09-30.md)).
- The square marked 2308 is, by inference, the bottom of Warren's 1869 shaft (see `measurements.json`).

Used by the atlas model `east-gate-warren` (`atlas/app/atlas-site-plans.json`, `atlas/app/atlas-model-geometry.ts`). Mirror: `atlas/research/assets/plans/warren1884-plate-vi/`.
