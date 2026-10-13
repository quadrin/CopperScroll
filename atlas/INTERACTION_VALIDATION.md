# Atlas interaction validation

Validated in the onboarding machine on 12 October 2026 (Los Angeles).

- Frozen pnpm 11.25.0 dependency installation passed with the committed lockfile.
- TypeScript and the production Pages build passed. Vite reports existing large chunks.
- Reader model and navigation checks passed, including all 61 entry/photo routes.
- Workbench rendering passed across five modules and 179 saved selector choices; the research check ran 153 tests successfully.
- Chromium at 1440 × 1000 and 390 × 844 exercised Hebrew word cards, English show/hide, column selection, image/source disclosure, close-inspection controls, building toggle and photo feature-note selection without application exceptions.
- The generated Pages homepage passed browser checks for asset loading, translation, entry selection, word apparatus and the local manuscript-photograph route.
- Local HTTP serving passed for both repositories. JerusalemMap's browser execution stops at `d3 is not defined` because its CDN script is denied by the environment proxy.
- OpenFreeMap, Mapterhorn and Wikimedia image requests received proxy 403 responses. A fallback map initialized and accepted controls, but real basemap, elevation, building rendering and photographic imagery remain unverified. These require the saved network-domain additions to be applied, followed by another browser run.

Configuration draft fields saved: installation script, startup instructions and seven custom network domains (OpenFreeMap, Mapterhorn, OpenStreetMap tiles, Wikimedia uploads, cdnjs and the two Google Fonts hosts). Saving a draft does not apply those domains or publish a snapshot. No credentials are required by these public interfaces.

Source changes and the generated GitHub Pages assets are prepared locally. Deployment was not performed.
