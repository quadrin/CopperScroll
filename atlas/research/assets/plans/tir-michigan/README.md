# Michigan TIR map archive

Credit: **University of Michigan Library (Stephen S. Clark Library).**

User-supplied reproductions of *Tabula Imperii Romani: Iudaea · Palaestina*. Original publisher copyrights remain; no open licence is asserted. [Original intake and chronological access record](https://github.com/quadrin/CopperScroll/blob/main/research/sources/tir_umich_map_intake_2026-10-01.md). User authorized archiving on 2 October 2026.

- [Full-resolution North archive and native detail crops](north/README.md), reattached and archived 2 October 2026.
- [General North preview](tir-general-north-preview.jpg), 786 × 600.
- [General South preview](tir-general-south-preview.jpg), 799 × 591.
- [Synagogues preview](tir-synagogues-preview.jpg), 544 × 800.
- [Eretz Israel/Sinai preview](tir-eretz-israel-sinai-preview.jpg), 515 × 799.
- [Churches: full-sheet viewing image](tir-churches-overview.jpg). Resized derivative; use the original or native crops for small labels.
- [Churches: Gerizim](churches-gerizim.jpg), [Judaea/Beth-Horon](churches-judaea-west.jpg), [eastern Jericho region](churches-jericho-east.jpg), [legend and credits](churches-legend-credits.jpg). Native pixel crops; exact bounds in the manifest.

The previews retain their original sideways orientation where supplied. Their pixels do not resolve fine labels. The Churches overview and crops contain the church layer; the eastern Jericho crop must not be treated as an individual measured Qumran feature plan.

## Full-resolution original

The original Churches JPEG is 7,394 × 10,909 pixels and 34,641,208 bytes. A single upload exceeded the connector request size, so its exact bytes are stored in 35 numbered parts. From a checkout, run:

```bash
python research/assets/plans/tir-michigan/restore_churches.py
```

The script verifies every part, reconstructs `tir-churches-full-resolution.jpg`, and verifies its original SHA-256. It refuses to replace a different existing file. [Manifest](manifest.json) records the original identity and all asset checksums. The complete concatenation was verified locally before publication.

The later South, Synagogues and Eretz Israel/Sinai TIFFs are currently absent from this workspace. The North TIFF was recovered on 2 October 2026 and its complete-sheet derivatives and native detail crops are now archived. Their earlier inspection remains documented; these preview JPEGs do not replace them. [Missing-source register](../MISSING.md).
