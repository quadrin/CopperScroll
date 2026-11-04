# Introduction assets

- `ct16-rcb.jpg`, `ct16-rct.jpg`: WSRP CT16 previews embedded as images 10 and 25 in the owner-supplied Copper_Scroll_Editable.pptx (2 November 2026). Centre-bottom / centre-top illumination; approximate correspondence only. Retained for the existing owner-private Atlas; no open licence or redistribution permission asserted. These images must be reviewed before widening site access.
- `iv17-plan.webp`: unchanged complete Plan 5 crop, Sion 2002, ʿAtiqot 41, p. 63. Ofer Sion / Israel Antiquities Authority, CC BY-NC 4.0; https://publications.iaa.org.il/atiqot/vol41/iss1/6/. Original caption, scale and north arrow retained.
- Word tracing uses atlas-photo-data.json: Osama Shukir Muhammed Amin 2020 photograph, CC BY-SA 4.0, with the existing project provisional tracing of VII 10. The tracing remains separate from the photograph and its edition reading.
- Aqueduct paths use existing atlas-site-plans.json, manually sampled source-plan coordinates after Ilan–Amit 1989, Fig. 1, p. 283. No geographic registration or measured flow simulation.

## Entry 25 walkthrough expansion

`entry25-12d.jpeg`, `entry25-12c.jpeg`, and `entry25-12g.jpeg` are the original embedded radiograph image streams extracted without re-encoding from the owner-supplied Brizemeure, Lacoudre & Puech 2006 PDF (STDJ 55), printed pp. 382–383, plates CCCXLIII–CCCXLIV, PDF pages 664–665. Xrefs and source details are in `entry25-provenance.json`. EDF retains original image rights; Émile Puech is credited for epigraphic assemblies. Used in the existing owner-private educational Atlas, with no open licence asserted. The modern Hebrew is edition-based, not a new registration or newly claimed manuscript reading.

`twin-cave-figure.webp`: source figure plus its original caption extracted from the already held Bar-Adon 1989 p. [15], Fig. B1 (`research/assets/plans/baradon1989/b1-twin-cave-p15.png`, pixel bounds 225,1050–1010,1425). Rights reserved; same private educational setting. This is an unscaled exterior photograph, not a measured cave plan.

`iv11-plan.png`: complete Plan 1 and caption from Feig 2002, printed p. 85, PDF page 2 of the held IAA report (`research/assets/plans/atiqot41/feig-iv11-pp85-90.pdf`), source-point bounds 270,390–468,560, rendered at 3×. IAA CC BY-NC 4.0; https://publications.iaa.org.il/atiqot/vol41/iss1/7/. Scale and north arrow retained. No retouching, invented geometry or candidate registration.

## Desert-to-discovery opening

`opening-terrain.json` contains a 513×513 regional grid over 46 km, a 385×385 middle grid over 12 km and a 385×385 local grid over 2.5 km, bilinearly sampled from Mapterhorn Terrarium tiles. `opening-terrain-provenance.json` retains tile URLs, source hashes, full attribution, the historical Cave 3 anchor and its uncertainty, and the illustrative nature of the close cave scene. Rebuild with `python scripts/build-opening-terrain.py` (Pillow and curl required). No remote map service is required at runtime.

The opening blends those elevations into a single smoothly shaded, nonuniform mesh, avoiding overlapping terrain layers. The same copper object continues from the cave into the discovery sentences and unrolling. Metallic word treatments and ink underlines follow scroll position; reduced motion shows completed emphasis.

## Continuous illustrated narration

`atlas-intro-sequences.tsx` provides 36 short beats across inventory, proposed locations, the worked plan, chronology, interpretations and the conclusion. Illustrations respond to scroll within each beat: routes draw, measurements extend, deposits become visible in cutaway, entry brackets appear, and competing ownership or literary proposals change the accompanying diagram. The inventory brackets are illustrative grouping marks, not a claimed transcription or diplomatic segmentation. Temple, community, landscape and vessel drawings are schematics, not reconstructions or observed deposits. The complete source plans and Entry 25 radiographs remain in their existing walkthrough.

The rolled model's material crops and repeats the existing `scroll/strip13.webp` photograph (Osama Shukir Muhammed Amin, 2020, CC BY-SA 4.0). It retains photographic Hebrew grooves, corrosion and pits; this is an illustrative remapping of strip 13, not the scroll's original column layout, appearance before corrosion, or a new letter tracing. No new manuscript reading is inferred. The same photograph also supplies the flat introductory sheet illustration. Neutral lighting and matte roughness replace the former yellow polished surface. The source photograph and licence are linked in the page's final credits. Runtime canvas cropping changes no source asset.

The cliff uses a dense nonuniform mesh, with illustrative grain and strata. Its surface is introduced before the camera reaches the modern DEM's resolution limit. Shader microdetail is illustrative and does not add surveyed geography. Motion is scroll-driven and reversible. Reduced motion renders every new illustrated beat in ordinary document flow.

## Returning candidate relief map

The locations chapter reuses the opening regional elevation grid in `atlas-intro-candidate-map.tsx`. Twin Cave, IV/17 and IV/11 drop sequentially with document scroll and remain visible together before the source-image comparison. The map uses existing Qumran (31.74183, 35.45941) and Jericho (31.85611, 35.46306) regional orientation anchors, not cave-mouth coordinates. IV/17 and IV/11 share the Jericho anchor with screen-only label offsets and dashed regional rings. No unverified catalogue grid conversion or inferred cave coordinate has been introduced. Reduced motion shows all three pins immediately, with a single map followed by all narration. WebGL failure retains an illustrative relief fallback and all regional labels.

## Generated vector illustrations

`icons/` contains nine generated illustrations converted to actual SVG paths, with a matching inline runtime asset in `app/atlas-intro-glyphs.json`. `atlas-intro-glyphs.tsx` reuses those paths in the narrative compositions, clue drawings, copy comparison and stratigraphic diagrams. Photographs, the opening 3D material, returning relief map and original plans remain separate source assets. See `icons/README.md` and `icons/provenance.json` for the family, conversion and evidence limits. Scroll controls composition, connectors and visibility; the generated paths contain no embedded bitmap or autonomous animation.

## Current realistic treatment

Object presentation now uses photographic material studies with apparent depth and oblique light. Actual strip 13 photography replaces the generated Copper Scroll, and a credited public-domain photograph of the Israel Museum’s modern Temple reconstruction replaces the generic sanctuary. It is identified as a modern reconstruction in the narration. Generic objects are illustrative cutouts; their appearance establishes no archaeological identification. `object-studies/README.md` distinguishes references and illustrations. Measurements and annotations remain SVG. The current source was matched to hosted version 30 before this change; the returning regional map, pins, entry walkthrough and source images are preserved.

## Integration into the current repository website

This repository's public build excludes `ct16-rcb.jpg`, `ct16-rct.jpg`, `entry25-12c.jpeg`, `entry25-12d.jpeg`, `entry25-12g.jpeg`, and `twin-cave-figure.webp`. Their citations above describe the separately retained owner-private image packet, not public redistribution. Public Entry 25 starts with an explicitly edition-based Hebrew passage, and Twin Cave uses a regional locator. Licensed manuscript photograph strip 13, the IAA plans, modern terrain and the credited Temple-model photograph remain available. The earlier vector icon archive is not imported into this repository's active page. The original GitHub homepage is preserved; this explainer is an additional route linked from its header.

## Entry 25 continuous investigation (current)

`atlas-entry-investigation.tsx` replaces the separate entry, meaning, locations, candidate, worked-example, time, construction, purpose, duplicate-copy and ending scenes with one continuous stage. Sixteen private-build cues retain the source → Hebrew → English sequence, build one cave clause by clause, return to the regional map, compare the actual source images, illustrate possible ground-level change and conclude. The public build omits the private radiographs and starts on the edition-based Hebrew (15 cues). One finite animation controller owns visual progress and caption fades; scroll selects the next cue and settled content holds indefinitely. Reverse and rapid scrolling cancel obsolete transitions. Reduced motion presents ordinary document flow.

`entry-investigation/limestone-cave.svg` is a new generated limestone illustration traced into actual SVG paths, with no embedded raster. Retained original, exact prompt, tracing script and art direction: `atlas/design/entry-investigation/`. Native overlays and props remain separately editable in React. The cave and its assigned northern entrance are explanatory choices, not a reconstruction of a candidate. The schematic three-cubit line establishes no digging axis, ancient datum or deposit. Generated artwork has no archaeological evidentiary status.

Only IV/17 receives source-relative markers, using the existing recorded plan coordinates (pillar 415,380; northern opening 562,416; southern opening 231,442; orientation marker around the source north arrow). Other sources receive no guessed overlays. Original source scales/captions/north arrows remain intact. Each source opens at full size. Qualifications and reading alternatives appear in expandable notes rather than the animated canvas or a comparison matrix. The regional map retains the existing regional anchors described above.
