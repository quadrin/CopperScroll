# Sources 2–7 (Qumran group): keying notes (frozen before keying)

31 Oct 2026, 19:2x PT. Owner approval: "sounds good, go ahead" (19:13). Same `SCHEMA.md` and `READER_INSTRUCTIONS.md` as source 1; two readers (A, B) per group; third reading of disagreements; agreement by `scripts/agreement.py`; consolidation by `scripts/consolidate.py`.

| Group | source_id | Text given to readers | Pages / images |
|---|---|---|---|
| Q1 | `qum3a` | IIIA (2016) Part 2 chs 11–12: list of built elements and list of loci (PDF pp. 129–138), French | Bucket page renders (`render_bucket.py`) |
| Q2 | `mp18` | Magen & Peleg 2018, *Back to Qumran*, site-description chapter (bucket copy, 91 PDF pages) | Bucket page renders |
| Q3 | `hir04`, `bad77` | Hirschfeld 2004 (*IEJ* 54, ʿEin Feshkha); Bar-Adon 1977 (*BASOR* 227, ʿEn el-Ghuweir): Drive text extraction (JSTOR copies) | Text only (the Drive copies could not be downloaded as PDFs in this session) |
| Q4 | `esh02`, `qum4a` | Eshel, Broshi, Freund & Schultz 2002 (*DSD* 9.2), Drive text extraction; IVA (2019) PDF pp. 26–111 (archival sources and diary, ch. 2 on the cave, geology appendix, 2017 notes) | Eshel text only; IVA bucket page renders |

Conventions:
- `feature_id`: `qum3a:L91` for loci; `qum3a:E366` for numbered built elements of ch. 11 (the list's own number); `mp18:<the source's locus or feature label>`; `hir04:L<n>`; `bad77:<label>`; `esh02:T<tomb no.>` for tombs; `qum4a:11Q` for the cave and `qum4a:11Q.<part>` for its parts.
- IIIA's coordinates are cells of its plates I–XII (e.g. `(E3)`): key them in `grid_printed` as printed, with `grid_system = unknown`, `position_basis = plan`, and "IIIA plate grid" in `notes`. Key the wall numbers that bound a locus in `relations` as `next_to:qum3a:E<n>`.
- A cemetery tomb with only an orientation and size is a valid row: key the orientation in `notes` as "long axis N–S" (the schema's `opening_dirs` is only for openings).
