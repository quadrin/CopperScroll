# Hyrcania: exact conditional grid-cell test

Reviewed 2 October 2026 UTC / 1 October Los Angeles. M04 / R08. Baseline `4a6c4434ff86f213aa2471351707ef2e8d7ab663`.

Hypothesis: rounding or truncation of the guide's assumed 100 m grid components alone can contain the unchanged station-44 prediction. The guide's grid convention, feature identity and the regional registration assumptions remain unverified. This test holds them fixed and tests quantization alone.

The new computation repeats the actual datum transformation, using pyproj 3.7.2 / PROJ 9.5.1 with networking disabled, fixed x/y ordering, ballpark transformations disabled and the selected operation recorded. EPSG:28191 to WGS84 reproduces the stored guide coordinate and 244.371 m nominal residual. The transformation's stated 2 m accuracy describes the operation, not the accuracy of the printed guide point. [Transformer documentation](https://pyproj4.github.io/pyproj/stable/api/transformer.html); [PROJ transformation documentation](https://proj.org/en/stable/usage/transformation.html).

The predicted point converts to approximately E 183896.28 / N 125954.41 in the retained old-grid interpretation. It lies outside both conditional cells:

- Rounding to nearest 100 m: E 183650–183750 / N 126050–126150. Nearest transformed cell point is about 174.74 m away.
- Truncation to 100 m: E 183700–183800 / N 126100–126200. The separation infimum is about 174.53 m. Treating the rectangle as closed gives a conservative infimum when the actual upper edges are excluded.

Result: conflicting with the quantization-alone explanation under the stated assumptions. Neither cell reaches the fixed prediction. Rounded reporting is approximately 175 m in both cases. Unknown map generalization, source/feature identity, anchor, scale, north convention and scan errors remain outside this test; their bounds remain unknown. The result preserves the rejected regional fit and supplies no accepted feature coordinates.

The script minimizes WGS84 geodesic separation along the four transformed grid-cell edges and checks whether the inverse-transformed prediction lies inside each cell. It records nearest points, corner separations, software/database versions, datum pipeline and input hash. Numerical convergence does not establish geographic source accuracy.

Run from the measurement directory with `python cycle2/hyrcania_grid_cell.py` after installing `pyproj==3.7.2`. The script defaults to the parent `hyrcania_baseline.json`; use `--baseline` for another pinned copy. `--pyproj-path` optionally identifies a local package installation. Output: `hyrcania_grid_cell.json` beside the script. Runtime packages and original map images remain outside the research commit.

This completes one bounded registration-model test. It adds zero primary-source targets, decisive candidate tests or R closures. Keep the separate original-Fig.-22 availability/dimension audit and the wider unknown registration errors in the assessment.
