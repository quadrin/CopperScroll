# Site exploration and photo integration

The atlas now has two primary views: **Explore** and **Read the scroll**. Find opens searchable entry browsing. The selected map card's **Explore candidate** opens a source-plan explorer for Qumran, Jericho royal palaces and Siloam. Candidates without a curated source plan retain their map and entry evidence; this is an explicit coverage limit.

## Current interaction

- Pan, scroll, pinch, or use keyboard arrows and plus/minus in a site plan. Select a numbered structure or its highlighted region to open the feature inspector.
- The inspector connects the selected feature to its description, source references, interpretation limits and relevant scroll passage.
- Qumran uses the existing independent Ilan–Amit and Reeder–Jol source-plan frames. The intake, basin, proposed dam, branch/short tunnel, boulder and long tunnel remain separate proposals.
- Jericho offers the licensed Area AC figure and early/later reconstructed Pools Complex figures. A(C)90, A(C)94, AC44, the distribution basin and aqueduct approaches have approximate image selection regions. The northern complex remains separate from Area AC.
- Siloam uses a labelled project tracing of selected W1, L103, L102/L104 and W3 relations from Greenhut & Mazor 2020 Plan 1, p. 74*. It is a simplified source-relative diagram.
- Photos opens the candidate's existing annotated photograph in the same inspector. Select a photographic detail, pan/zoom, or enlarge the image. Photograph highlights retain their image coordinates. A source-plan feature is not automatically equated with a photographed feature.
- Terrain context returns to the candidate's close map view. Selected historical-map records become clickable at site scale, with source-map dates and positional error in their inspector. Modern buildings provide present-day context.
- Back and browser Back/Forward restore entry, candidate, source plan, feature, photo/detail selection and recorded map/plan/photo cameras. Reload restores the saved history entry. Scroll column changes also enter browser history.
- Historical maps are under Map layers. Dossiers and research tools remain available on demand. The persistent three-panel register and primary Landscapes/Scene navigation have been removed.

Source-plan geometry is not geographic geometry. These figures have no established registration to the terrain; registration requires control points and a recorded residual error before any traced feature can become a terrain overlay. Source and transformation details are in [the manifest](../research/assets/plans/atlas-explorer/manifest.json), mirrored under `atlas/research/`.

## Next asset additions

Extend `app/atlas-site-plans.json` and the existing `app/atlas-scenes.json` with image/feature IDs, source references, exact captions, dates, photographer/author, licence, dimensions and frame-relative polygons. Multiple photographs per candidate should form a thumbnail gallery; a single scene is available per currently photographed place. Additional photographs of the same mapped structure can share a feature ID only after correspondence is documented.

Registered plans can add geographical footprints, channel paths and camera locations. Excavation phases should retain their own dated geometry. Simple 3D walls or basin outlines need published dimensions; a decorative reconstruction should never stand in for surveyed remains.

The supplied Drive link points to the library already indexed in `research/sources/drive_index.md`. The public folder redirects to Google sign-in and this session has no callable Drive connector; no new Drive contents were inspected. The locally archived material supports this implementation. Further intake can resume when authenticated folder access is available.
