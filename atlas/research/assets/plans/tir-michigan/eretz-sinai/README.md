# TIR Eretz Israel/Sinai: full-resolution archive

Credit: **University of Michigan Library (Stephen S. Clark Library).**

Tabula Imperii Romani: Iudaea · Palaestina — Eretz Israel and Sinai during the Hellenistic, Roman and Byzantine periods. Israel Academy of Sciences and Humanities / Survey of Israel, 1993. Printed scale **1:1,000,000**. Editors Yoram Tsafrir and Leah Di Segni; Israel Roll credited for roads. User supplied the TIFF and authorized repository archiving. Original copyrights remain; no open licence is asserted.

The reattached `39015106237970_eretz_sinai(2).tif` opens despite the inline missing-path error. Its source hash matches the earlier inspected delivery. Original dimensions: **7029 × 10909 pixels**, RGB, 400 dpi; 230,155,840 bytes. SHA-256: `4bfe934f0349191b31d605c7c5fe225ec0a3f2e88eb20e4bc429e23bc209e076`.

- [Complete-sheet viewing image](tir-eretz-sinai-overview.jpg).
- [Judaea / Dead Sea](tir-eretz-sinai-judaea-dead-sea.jpg): native-resolution JPEG crop.
- [Legend, scale and credits](tir-eretz-sinai-legend-credits.jpg), also available as lossless PNG [left](tir-eretz-sinai-legend-credits-lossless-left.png) and [right](tir-eretz-sinai-legend-credits-lossless-right.png) halves.

Source orientation is retained. JPEG crops retain native resolution and use quality 95; encoding is lossy. The PNG legend crops preserve original source pixels exactly. [Manifest](manifest.json) records original crop bounds, transformation, hashes and source details. These regional map images are not surveyed feature footprints.

## Full native-resolution sheet

The complete JPEG derivative retains **7029 × 10909 pixels**, at quality 95. Its 33,963,734 bytes are archived in 12 numbered parts because the connector accepts request bodies up to 16 MiB; base64 increases the payload size. From a checkout:

```bash
python research/assets/plans/tir-michigan/eretz-sinai/restore_native.py
```

The script verifies every part and the reconstructed JPEG hash. It reproduces the JPEG derivative exactly; it does not reconstruct the uncompressed source TIFF. The original TIFF is not embedded in the repository.

This is recovery of an already counted cartographic source. Research KPI totals, coordinates, candidate rankings and feature dates remain unchanged. [Earlier inspection and source record](https://github.com/quadrin/CopperScroll/blob/main/research/sources/tir_umich_map_intake_2026-10-01.md).
