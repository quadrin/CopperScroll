# TIR General South: full-resolution archive

Credit: **University of Michigan Library (Stephen S. Clark Library).**

Tabula Imperii Romani: Iudaea · Palaestina — SOUTH: Eretz Israel during the Hellenistic, Roman and Byzantine periods. Israel Academy of Sciences and Humanities / Survey of Israel, 1993. Printed scale **1:250,000**. Editors Yoram Tsafrir and Leah Di Segni; Israel Roll credited for roads; Tsvika Tsuk for aqueducts. User supplied the TIFF and authorized repository archiving. Original copyrights remain; no open licence is asserted.

The reattached `39015106237970_south(2).tif` opens despite the inline missing-path error. Its source hash matches the earlier inspected delivery. Original dimensions: **15075 × 11146 pixels**, RGB, 400 dpi; 504,200,490 bytes. SHA-256: `cac6e77fb79bdb245945fd6e51c0de5ac7fa70db88424b99020fbd3d28515a30`.

- [Complete-sheet viewing image](tir-south-overview.jpg).
- [Northern western sector](tir-south-northern-western-sector.jpg): native-resolution JPEG crop.
- [Northern Dead Sea sector](tir-south-northern-dead-sea.jpg): native-resolution JPEG crop.
- [Legend](tir-south-legend.jpg), also available as a [lossless PNG](tir-south-legend-lossless.png).

All archived views rotate the source 90 degrees counterclockwise. JPEG crops retain native resolution and use quality 95; encoding is lossy. The PNG legend crops preserve original source pixels exactly. [Manifest](manifest.json) records original crop bounds, transformation, hashes and source details. These regional map images are not surveyed feature footprints.

## Full native-resolution sheet

The complete JPEG derivative retains **11146 × 15075 pixels**, at quality 95. Its 73,162,273 bytes are archived in 25 numbered parts because the connector accepts request bodies up to 16 MiB; base64 increases the payload size. From a checkout:

```bash
python research/assets/plans/tir-michigan/south/restore_native.py
```

The script verifies every part and the reconstructed JPEG hash. It reproduces the JPEG derivative exactly; it does not reconstruct the uncompressed source TIFF. The original TIFF is not embedded in the repository.

This is recovery of an already counted cartographic source. Research KPI totals, coordinates, candidate rankings and feature dates remain unchanged. [Earlier inspection and source record](https://github.com/quadrin/CopperScroll/blob/main/research/sources/tir_umich_map_intake_2026-10-01.md).
