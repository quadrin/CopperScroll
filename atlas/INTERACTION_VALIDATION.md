# Atlas interaction validation

Validated in the onboarding machine on 12 October 2026 (Los Angeles).

- Archaeology-first correction: desktop/mobile browser checks passed for the default source plan, entry 27’s regional excavation catalogue, Area AC feature selection, Back and migration of saved old city-map views. The applied terrain style reports zero modern urban layers.
- The real OpenFreeMap style and a failure fixture passed checks removing buildings, roads, land-use/POIs, hidden height layers and modern-raster fallback while retaining physical-geography layers.
- Pinned pnpm installation, TypeScript and the production Pages build passed. Dependency manifests and the lockfile were preserved. Vite retains a large-chunk warning.
- Source-plan data checks passed for provenance, frame bounds, valid entry/place references and feature/view deep-link roundtrips. Existing reader and navigation checks passed, including manuscript-photo routes and legacy aliases.
- Research-tool rendering passed for all five modules and saved selector choices.
- Desktop and mobile browser scenarios exercise candidate/feature selection, source-plan pan/zoom, photo highlights/enlargement, passage translation, phase changes, search, Back/Forward, and saved cameras. The tests exposed and fixed history initialization on manually opened deep links and mobile controls occluded by the detail sheet.
- Browser checks of the generated Pages homepage passed for local asset loading, source-plan selection, reload, scroll-column Back and view restoration. Mobile touch pinch and detail-sheet expand/minimize were verified; a pointer drag of the sheet handle also collapsed it successfully.
- Actual OpenFreeMap/Mapterhorn content and Wikimedia photographs loaded through the environment HTTPS proxy. Browser tests forward only public asset requests through curl with normal TLS verification; Chromium uses software WebGL. No fabricated map or photo responses are substituted.

Qumran and Siloam project drawings retain source-relative coordinates. Jericho figure overlays are approximate image selection regions. No source-plan feature is declared geographically registered; the sources and transformations are recorded in `research/assets/plans/atlas-explorer/manifest.json` and its atlas mirror. Feature identity and scroll association remain separate.

Authenticated Drive access was subsequently verified on 12 October through the user’s Chrome session; the source-plan intake is documented in [PHOTO_INTEGRATION.md](PHOTO_INTEGRATION.md).

Pages assets were regenerated for the implementation. A Git push and a successful build do not establish that the public Pages deployment has completed.

## Interactive 3D site models

Browser observations on 12 October verified structural models rendering with source feature markers, map-style drag panning, orbit navigation, feature focus, top view, camera persistence on reload, Source plan switching and browser Back restoration. The historical SWP map retains its flat view. The cave exposes its roof/cutaway control. Desktop and 390 × 844 viewport checks cover the overview and feature inspector; the selected mobile detail sheet gives the model its own visible surface and keeps navigation controls above the sheet. Touch pan and pinch handlers are configured through OrbitControls; physical touch-device testing is pending.

The surrounding ground uses archived Mapterhorn elevations around mapped site anchors, with a disclosed display bench. IV/17’s setting is labelled illustrative and receives no geographic coordinates. Elevation-grid, finite-geometry and source-dimension tests passed, including the separately published pool depths and cave height range. Existing explorer, reader, terrain-style and navigation checks passed. TypeScript and the Pages production build passed; the large-chunk warning remains.
