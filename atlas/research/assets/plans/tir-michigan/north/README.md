# TIR general North: full-resolution archive

Credit: **University of Michigan Library (Stephen S. Clark Library).**

*Tabula Imperii Romani: Iudaea · Palaestina — NORTH*, 1993, printed scale 1:250,000. Editors Yoram Tsafrir and Leah Di Segni; Israel Roll credited for roads; Tsvika Tsuk for aqueducts. Israel Academy of Sciences and Humanities / Survey of Israel. User supplied the TIFF and authorized repository archiving; original copyrights remain, no open licence is asserted.

The reattached TIFF opens locally despite the inline error. Its SHA-256 matches the earlier inspected North source exactly: `da5bc3e2d4a3c38ca9d9e325fd2f949dec7caefb8a56ccfbfa8d7d78c61f1054`. Original: 14,630 × 11,163 pixels, RGB, 400 dpi, 490,066,390 bytes.

## Viewable assets

- [Complete North sheet](tir-north-overview.jpg): upright viewing derivative, 3,815 × 5,000 pixels.
- [Qumran–Jericho region](tir-north-qumran-jericho.png).
- [Jerusalem–Beth-Horon region](tir-north-jerusalem-beth-horon.png).
- [Gerizim region](tir-north-gerizim.png).
- [Wadi Qelt](tir-north-wadi-qelt.png).
- [Achor / Noorath](tir-north-achor-noorath.png).
- [Qumran detail](tir-north-qumran-detail.png).
- [Hyrcania detail](tir-north-hyrcania-detail.png).
- [Legend](tir-north-legend.png).
- [Scale and publication credits](tir-north-scale-credits.png).

The nine PNGs preserve native source pixels, rotated 90 degrees counterclockwise. [Manifest](manifest.json) records exact unrotated crop bounds and hashes. These are regional source-map images, not surveyed feature footprints.

## Full native-resolution sheet

A complete upright JPEG derivative retains the source resolution: **11,163 × 14,630 pixels**, encoded at JPEG quality 95. Its 67,421,288 bytes are archived in 23 numbered parts to fit upload request limits. From a checkout:

```bash
python research/assets/plans/tir-michigan/north/restore_native.py
```

The script verifies all parts and the reconstructed JPEG hash. This reproduces the JPEG derivative exactly; JPEG encoding is lossy. The PNG crops provide lossless detail for the active research windows. The original 490 MB TIFF is not embedded in the repository.

The TIFF is the same source already counted in the five cartographic intakes. This archival recovery adds no source/test KPI, phase inference, coordinate or confidence change. [Earlier source readings](https://github.com/quadrin/CopperScroll/blob/main/research/sources/tir_umich_map_intake_2026-10-01.md).
