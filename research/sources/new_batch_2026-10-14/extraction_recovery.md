# Levy collection: recovering suppressed text

Ordinary extraction of the supplied combined 2023 volumes drops body paragraphs because of the PDF's accessibility `ActualText` replacements. The underlying glyph text is present. This is an extraction defect, distinct from a missing printed leaf.

The source-bound [extraction script](https://github.com/quadrin/CopperScroll/blob/research/resource-sweep-2026-10-14/tools/extract_levy2023_text.py) ignores those replacement strings using PyMuPDF's `TEXT_IGNORE_ACTUALTEXT`. It refuses a different source hash. The private derivative contains one record per viewer page, with default and recovered character counts and recovered text. No page images are opened by this operation.

| Item | Recorded value |
| --- | --- |
| Supplied source SHA-256 | `08fe807e0550a3e915d5e08f15bdf43e26c855cc6fa2a8809f8c71355305920b` |
| PDF viewer pages | 1,956 |
| PyMuPDF version | 1.26.6 |
| Extraction flags | 2243 |
| Default extracted characters | 4,339,392 |
| Recovered characters | 5,153,146 |
| Derivative SHA-256 | `c1af228e052988eddbbed6208986f465e22fcc9fbdcf02f19cc7b6c8cff1faee` |

Checks against underlying glyph traces and previously inspected native pages establish that omitted paragraphs can be recovered. Disputed glyphs, reading order, rotated tables and figure relationships still require native inspection. This derivative establishes text availability; the reader ledgers alone establish which pages were read. Printed-folio jumps require separate copy checks.

The extracted modern text remains private. Public records contain original observations and precise page references.
