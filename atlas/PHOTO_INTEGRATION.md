# Site exploration and photo integration

The atlas now has two primary views: **Explore** and **Read the scroll**. Find opens searchable entry browsing. The selected map card's **Explore candidate** opens a source-plan explorer for Qumran, Jericho royal palaces, Siloam, Gerizim, Doq, Hyrcania and the provisional Abu Saraj IV/17 comparison. Candidates without a specific source plan open a catalogue of documented regional excavations and the entry’s unresolved feature requirements. Regional plans are context, not substitute identifications. Saved older city-map views migrate to this archaeological starting point.

## Current interaction

- Pan, scroll, pinch, or use keyboard arrows and plus/minus in a site plan. Select a numbered structure or its highlighted region to open the feature inspector.
- The inspector connects the selected feature to its description, source references, interpretation limits and relevant scroll passage.
- Qumran uses the existing independent Ilan–Amit and Reeder–Jol source-plan frames. The intake, basin, proposed dam, branch/short tunnel, boulder and long tunnel remain separate proposals.
- Jericho offers the licensed Area AC figure and early/later reconstructed Pools Complex figures. A(C)90, A(C)94, AC44, the distribution basin and aqueduct approaches have approximate image selection regions. The northern complex remains separate from Area AC.
- Siloam uses a labelled project tracing of selected W1, L103, L102/L104 and W3 relations from Greenhut & Mazor 2020 Plan 1, p. 74*. It is a simplified source-relative diagram.
- Photos opens the candidate's existing annotated photograph in the same inspector. Select a photographic detail, pan/zoom, or enlarge the image. Photograph highlights retain their image coordinates. A source-plan feature is not automatically equated with a photographed feature.
- Regional terrain is a secondary physical-geography locator. Modern buildings, street geometry, land-use/POIs and modern-raster fallback have been removed. Historical-map records remain in the optional archive tools.
- Back and browser Back/Forward restore entry, candidate, source plan, feature, photo/detail selection and recorded map/plan/photo cameras. Reload restores the saved history entry. Scroll column changes also enter browser history.
- Historical maps are under Map layers. Dossiers and research tools remain available on demand. The persistent three-panel register and primary Landscapes/Scene navigation have been removed.

Source-plan geometry is not geographic geometry. These figures have no established registration to the terrain; registration requires control points and a recorded residual error before any traced feature can become a terrain overlay. Source and transformation details are in [the manifest](../research/assets/plans/atlas-explorer/manifest.json), mirrored under `atlas/research/`.

## Next asset additions

Extend `app/atlas-site-plans.json` and the existing `app/atlas-scenes.json` with image/feature IDs, source references, exact captions, dates, photographer/author, licence, dimensions and frame-relative polygons. Multiple photographs per candidate should form a thumbnail gallery; a single scene is available per currently photographed place. Additional photographs of the same mapped structure can share a feature ID only after correspondence is documented.

Registered plans can add geographical footprints, channel paths and camera locations. Excavation phases should retain their own dated geometry. Simple 3D walls or basin outlines need published dimensions; a decorative reconstruction should never stand in for surveyed remains.

Authenticated Drive access was verified on 12 October 2026. The newly uploaded 28-page scan is the 1880 SWP map set, with 26 sheets, key and title; Sheet XI is available beside the Gerizim structural diagram as historical context. Raviv–Zissu 2022 is linked as a regional comparison for phased reuse of underground installations. Gerizim, Doq and Hyrcania diagrams use reinspected archived source pages. IV/17 displays the published Plan 5 with its source caption, north arrow and scale under the IAA’s verified CC BY-NC 4.0 policy. Simplified project outlines retain explicit omissions, source orientation and archaeological limits. Gerizim’s stale three-coin mansion inference is corrected to one catalogued findspot and a separate type total. The IV/17 mouth coordinates remain unassigned.
