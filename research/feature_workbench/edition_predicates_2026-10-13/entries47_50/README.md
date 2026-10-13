# E47/E50: what the available evidence can actually test

**Partly obtained:** original-edition checks correct two archaeological predicates; a bounded screen and native report checks produce no site identification. The substantive new result is an error correction, not a reduced landscape candidate list.

Entry47's schematic gives a two-cubit black-stone length. Lefkovits instead explicitly retains two **distance** attachments; Puech gives a stone at two cubits with unspecified datum. Milik reads two clamps and does not require blackness. Thus rejecting a site for lacking a one-metre black slab would apply a condition these editions do not share. No original report inspected here locates the entrance/stone relation at a dated basin.

Entry50's Upper Pool is a restored branch. Puech reads a tomb courtyard of Zadok; Lefkovits's principal text supplies an inner court and says his alternative openings are conjectural. A regional pool-only screen cannot test the courtyard branches, and four corners alone discriminates poorly between rectangular structures.

Original water-source checks: Solomon's upper pool has the modern rectangular/upper form, with ancient shape/phase unresolved; Ein Saleh has a spring chamber but no dated black-stone access relation in the pages read; Martyrius supplies a pool in the upper **garden**, with the reported monastic garden configuration later than the early window. An earlier basin reused there remains unknown. Solomon's Stables has documented vaults, reused masonry and disputed phases; its presence does not establish a Zadok tomb court.

## Deliverables and reproduction

- `EDITION_AUDIT.md`: exact edition printed/viewer pages, directly verified versus reported readings, and prior schematic error.
- `registry.json`: finite edition-specific predicates; no invented stone-length/depth requirement.
- `observations.csv` / `branch_status.csv`: row-level results from existing coded water records, including deduplication flags and unknowns. Inherited date codes are separate configuration diagnostics and generate no archaeological exclusions. Explicit round descriptions contradict the reported four-corner form only; ancient geometry, earlier fabric and reuse remain unknown.
- `native_checks.json`, `AQUEDUCT_NATIVE.md`, `STABLES_NATIVE.md`: directly inspected reports and scoped comparison outcomes.
- `screen.py`: `python3 screen.py` reads canonical `research/regional/water_systems/water.csv` and regenerates private row-level CSVs and `result.json`; the CSVs are excluded from publication.

The water input contains496 pool/tank rows plus970 cistern sensitivity rows; these are source rows with duplicates, not independent candidates or a regional denominator. One report's citations and republications do not add confirmations. The critical stone and courtyard fields are almost wholly uncoded. This prevents computing a meaningful candidate intersection; it does not prove that none of these features exists.

## Source provenance and scope

Exact source book hashes in `native_checks.json`; GitHub water blob `2570275f6cceefcb253cb96b19b5b1c26b48b1f8` (downloaded UTF-8 content hashed in `result.json`). Canonical readings blob `c71d0a98c184e156a0870e4ad948943ecdf07e14`; entry47 schematic blob `2e346cd88451b1f2ce4dd148c2ffa8138b84a151`; entry50 schematic blob `eb1102a9dd56b4460de0b7974bafd236df7938ea`. Original raw evidence was held previously; this is exploratory recoding, not an unseen prediction. No closed E49 test or archive arrival opened.

Private edition/page renders were retained in the session workspace for inspection; no page images are included in this packet. No reproduction licence established; omit page images from public repository writes. `native_figure_manifest.json` records report figures and captions preserved for private source review.

The stated claim—identifying E47/E50 landmarks from this held coded corpus—is **not identifiable from available evidence**. Reopen this specification only for a dated same-feature stone/access relation, an independently documented original basin phase/geometry, or a named tomb-court association. The restoration and dimensional errors have already supplied an analytical correction; repeating this same coded screen would add no new evidence.
