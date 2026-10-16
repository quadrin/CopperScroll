# The Copper Scroll Atlas

The [GitHub Pages homepage](https://quadrin.github.io/CopperScroll/) opens the claim-centred knowledge base. Select a passage, follow typed graph relationships, compare retained branches, inspect name chronology, or preview the consequences of a changed reading or observation. Places and Read the scroll preserve the spatial atlas and photographic reader, including existing deep links. A Knowledge base link returns from those views.

The reviewed public snapshot contains evidence metadata and source pointers. It excludes protected dependency chains and source-image bytes. Each inspector links the underlying record and exact printed/PDF/figure locators. Graph positions are a reading layout; they carry no geographic or confidence meaning.

The existing atlas remains available through its named routes. Browse all 61 scroll entries and their candidate places in the register, inspect sites on the map, or switch to the full scroll text from the top navigation. Landscapes compares dated maps and archive photographs. Place dossiers connect the retained readings to individual features, archaeological phases and source figures. The selected entry has Sites, Text, and Evidence tabs. In the wide views, **Entry notes** restores the detail panel. On narrow screens, the bottom navigation moves between the register, map or scroll, and entry details.

## Textual scenes

The central atlas surface includes a **Scene** tab beside Map, Terrain and Photos. Entries 11 and 25 have plan/cutaway models with a depth-trace animation, an exploratory metres-per-cubit control and explicit architecture/origin assumptions. Entry selection synchronizes the register and reading folio. Other entries offer links to these examples. The source is `app/atlas-scene.tsx`; scenes add no archaeological coordinates, dates or confidence changes. Direct links use `#entry-11/scene` and `#entry-25/scene`.

## Run locally

Use Node.js 24 and pnpm 11.25.0 (the version pinned in `package.json`). From the repository root:

```sh
cd atlas
corepack pnpm install --frozen-lockfile
corepack pnpm dev
```

Open the local address printed by the development server. Run `corepack pnpm build` for a production build, and `corepack pnpm exec tsc --noEmit --incremental false` for the type check. No map API key is required. Basemap, elevation and photograph loading need an internet connection.

This directory contains the source deployed as the [Copper Scroll Atlas](https://copper-scroll-atlas.alexkesin.chatgpt.site), including the marker-positioning fix. The hosted Site retains its existing access settings. `.openai/hosting.json` identifies that Site and contains no credentials; local execution does not require a Sites connection. The initial GitHub import comes from Site source commit `ce7728e84d85422322ea8e3af661ea7d5f904ae2`.

## GitHub Pages build

A static build of the same atlas is published at <https://quadrin.github.io/CopperScroll/>. The built assets are committed in `../atlas-site/`; `../index.html` loads those assets directly at the repository homepage. The existing `/atlas-site/` URL also remains available.

To rebuild it after a change, from this directory:

```sh
corepack pnpm install --frozen-lockfile
corepack pnpm run build:pages
```

The build copies the atlas entry page to `../index.html` and omits `../atlas-site/research/qumran-video-comparison.html`. That comparison embeds frames from a watermarked stock-video preview and archival photographs whose reuse terms have not been checked. The page that links to it, `research/entry21-comparison.html`, is published.

`pages/index.html` and `pages/main.tsx` are the static entry. `vite.pages.config.ts` sets the Pages base path and writes to `../atlas-site/`. The MapLibre worker URL follows the build's base path, so it works both on the hosted Site and under the Pages sub-path.

## Research

Follow [`../AGENTS.md`](../AGENTS.md) to investigate and map specific sites and individual features. Add candidate coordinates, feature outlines and spatial hypotheses with their sources, assumptions and uncertainty. Update their precision as evidence improves.

The data originated in `quadrin/AncientHebrewTexts`, research snapshot `5220e8bd008cba1ade10ddce42c6c577170206ba` (28 September 2026). The committed CSV files in `research/` preserve the input tables. Run `python research/build_atlas.py` to regenerate `app/atlas-data.json`.

Descriptions are short factual editorial paraphrases, not quoted translations. Hebrew labels reproduce names or selected editorial readings from the public lexicon. Current confidence follows the revised Phase 5 assessment: Siloam is medium and conditional; Ramat Rahel is low; Tell el-Qos is a weak alternative. Kh. Ibziq (entry 59) stays medium: it was lowered to low after Zertal's survey and restored the same day after *HA* 40 (29 September 2026). Kh. Salhab is added as a low alternative (a dated revision in `research/build_atlas.py`). A second run the same day updated the evidence texts for entries 31, 40, 57 and 59 (Magen on Gerizim, Garbrecht & Peleg, *HA* 40, Jeremias) without changing any confidence; see `../research/sources/source_extractions_2026-09-29.md`. A third run revised the entry 57 text (a Hasmonean garrison into the 70s BCE) and the Hyrcania period note, again without a confidence change. Four places have no coordinates and remain unpinned.

Current pins use the gazetteer's site anchors. Filled areas with dashed outlines show their approximate positional precision. Each geometry should state whether it represents a site anchor, an observed feature footprint or a modeled candidate area. The selected candidate is shaded copper, other candidates sage, in both map dimensions. Selection fits the shaded area, including small archaeological anchors. The current Siloam coordinate anchors the pool complex; individual pool, outlet and trough candidates require their own feature records. The public index contains a subset of the candidates discussed in the unpublished full assessment.

## The Scroll view

**Read the scroll** in the top navigation replaces the map with the whole text of the scroll. A compact column selector provides all twelve columns. The default reading surface is a narrow vertical copper-inspired column, labelled as an edition-based transcription in modern Hebrew type. Each line gives its number and clickable Hebrew; **English translation** reveals or hides the project translation. **Image & sources** opens the existing image coverage and source panel. Entry headings select that entry in the register, map and field note while the view stays on the scroll. Selecting an entry elsewhere brings its lines into view. Words and underlined phrases open the same reading cards as the field note. `#entry-21/scroll` opens the view at an entry; `#scroll` opens it at the current one. The field note's **Read in context** link also switches to this view.

## The photographic reader

The **Reading desk** gives the photograph and reading the full surface by default. **Entries** reveals the register; **More** contains Research tools, Entry notes and About. **Image tools** reveals zoom, the image-version selector, provisional tracing and trace opacity. The original photograph is the default and tracing starts off; **Grooves · computed** and **Relief · computed** label image processing explicitly. A compact word selector replaces the persistent word-card rail. Reading arguments, lettering notes and source details open on demand. The aligned coverage remains eight provisional word tracings on strip 13, VII 7–11. Other columns display their coverage gap and a link to the photographed example. Original metal, radiographs and facsimiles remain distinct source types.

**Read the photograph** opens the original at the selected entry’s mapped words. A clicked word selects its owning entry; selecting an entry outside the photographed coverage returns to that entry’s full text. Pan, zoom, adjust trace opacity or hold the comparison control to inspect the photograph alone. Entries 31 and 49 have coherent reading alternatives with edition pages, feature requirements and map consequences. `#entry-31/scroll/photo` restores entry 31 at VII 11; `#entry-21/scroll` restores column V. Coverage and tracing sources remain in [the photographic reader note](research/photographic_reader.md).

## The text in each field note

The Text tab in each field note shows the entry's lines of the scroll: the Hebrew, from Martin G. Abegg Jr.'s transcription in the ETCBC Dead Sea Scrolls dataset (CC BY-NC 4.0), and an English translation written for this project. Selecting a Hebrew word shows its parts, their meanings and any notes; selecting an underlined phrase shows how the editions read it, with pages from the research files. The data is `app/atlas-text.json`, loaded as a separate chunk the first time a field note opens. `../tools/build_scroll_notes.py` writes it from `../text/`; rebuild the atlas data after changing the translation or notes. The full scroll, column by column, is in the [atlas Scroll view](https://quadrin.github.io/CopperScroll/#scroll).

## Map

MapLibre GL JS renders an OpenFreeMap basemap based on OpenMapTiles and OpenStreetMap, with Mapterhorn elevation tiles. An OpenStreetMap raster fallback handles failure to obtain the primary style. The map uses modern geographical data, not a reconstructed ancient coastline or road network. The 3D control enables actual terrain and a pitched camera, with 1–3× vertical exaggeration.

Map source attribution remains visible. MapLibre's local worker and shared module preserve the package license headers; they come from installed version 6.10.0. If upgrading MapLibre, refresh both files in `public/maplibre/` together.

MapLibre owns each marker's outer `site-marker` element, including its absolute position, transform and terrain visibility classes. Selection changes only the child button. Do not overwrite the outer element's class list or set relative positioning on it: this introduces document-flow offsets and makes pins drift during zoom. Settlement labels use the vector tile `place` category rather than relying on style-layer name prefixes.

## Interaction

The main navigation has **Explore** and **Read the scroll**. Explore opens an interactive 3D site schematic by default. Candidates without a specific plan open an archaeology catalogue with documented regional excavations; those sites are labelled as context rather than identified locations. **Find a place or entry** opens searchable browsing; entry details and research tools open on demand. The selected map card's **Explore candidate** opens a navigable local site explorer for Qumran, Jericho royal palaces, Siloam, Gerizim, Doq, Hyrcania and Abu Saraj IV/17. Source-plan regions and numbered structures open one feature inspector with evidence, source references, photographs and scroll links. Other places retain a clear source-plan coverage gap.

Drag to pan, scroll/pinch to zoom, select features to focus, and switch Pan/Rotate to inspect the 3D volumes. Top and Show whole site provide overview controls. The surrounding landscape uses sampled Mapterhorn elevation at the existing site anchor; model placement, bearing and the display bench remain illustrative. IV/17 has a labelled illustrative rock setting because its coordinates are unassigned. Source plan opens the cited figure or tracing, while Model assumptions records display geometry. The cave includes a roof/cutaway toggle. Three.js 0.186.1 supplies the renderer; its MIT notice is in `public/licenses/three-LICENSE.txt`. Run `node scripts/check-models.mjs` for source-dimension and geometry checks.

Site plans remain in their source-coordinate frames. **Regional terrain** is a secondary locator with relief, water and regional names. Modern buildings, roads, land-use/POIs and modern-street raster fallback are excluded. Historical survey records are available only in the archive tools. Traced features are not placed on the terrain until registration is established.

**Photos** is contextual to the selected site. The existing four photographs retain annotated details, credits and image-relative polygons; the inspector distinguishes photographed context from an unregistered plan feature. Zoom/pan works with mouse, touch and keyboard. Enlarged photographs remain in the same history stack.

**Back**, browser Back/Forward and reload restore the selected entry/candidate, source plan, feature, photograph/detail, and recorded map/model/plan/photo cameras. Column changes in the scroll also enter history. New source-plan routes include `#entry-21/site/qumran-ilan/D`, `#entry-29/site/jericho-ac/AC94` and `#entry-49/site/siloam-receiver/L103`; a `/photo` suffix opens contextual imagery.

See [photo and feature integration](PHOTO_INTEGRATION.md) for coverage, provenance, source-coordinate limits and next asset additions. Tests are `node scripts/check-explorer.mjs`, `node scripts/check-terrain-style.mjs`, `node scripts/check-archaeology-browser.mjs` and `node scripts/check-explorer-browser.mjs` (requires Playwright Core and Chromium). In the cloud runner use `ATLAS_PLAYWRIGHT_MODULE=/opt/codex/cua_node/lib/node_modules/playwright-core`; external public requests use curl through the environment proxy with TLS verification preserved.

## Landscapes and dossiers

**Historical maps & archive**, under **Map layers**, gives the synchronized swipe map the full surface, with the register closed by default. **Entries** opens the register; compact layer selectors compare the 1880 survey, 1940s Survey of Palestine and modern OpenStreetMap. **Map layers** reveals optional overlays, source dates, alignment limits and local map records. Selected source records open over the map. The view selector switches to archive photographs or the source library, each with a compact date selector. The 1918 aerials and 1967 CORONA views retain their complete captions and explicit registration limits. The 1974/1978 HEXAGON sources open their packages; those images are not yet registered overlays. The optional 1940s records retain positional error and review state, while Roman roads retain source certainty, dating fields and bibliography. These layers provide context, not a reconstructed route or identified deposit. The **1952 cave survey (de Vaux)** overlay plots the 27 legible numbered sites of de Vaux’s map of the March 1952 cliff survey (RB 60, 1953, pl. XX), as digitized in [`../research/history/devaux1952_cave_points/`](../research/history/devaux1952_cave_points/README.md): about ±30 m (1σ), ±60 m at 95%, shown as faint rings. Point 8 is Cave 3 (3Q). Selecting a point gives its label confidence and a one-line summary from DJD III. These are survey points, not candidate places; they stay out of the register, dossiers and place counts. Desktop and phone browser checks cover the comparison, optional controls, record inspection and entry selection.

Source originals, hashes, dimensions, licences and transformations are in [`../research/assets/plans/historical-landscapes/manifest.json`](../research/assets/plans/historical-landscapes/manifest.json), mirrored under `research/`. `python3 ../tools/build_landscape_data.py --intake-dir <download-directory>` rebuilds the public full-image derivatives and the permitted overlays (requires Pillow and pyproj). The protected map records are excluded. `python3 ../tools/build_cave_survey_layer.py` rebuilds the 1952 survey overlay, `app/atlas-landscape-cave-survey.json`, from the digitized CSV.

**Place dossier** opens from an entry’s Sites or Evidence tab, or from Landscapes. Curated dossiers cover Qumran, Doq, Siloam, Tell es-Sultan, the Jericho palaces and the Marjama/Samiya comparison. The interpretation tab preserves 17 reading arguments across entries 11, 25, 29, 31, 49 and 60, with the same saved feature comparisons used in Research tools. The Jericho source gallery compares licensed early/later Pools Complex plans and the separate Area AC figure. Other figures retain source-record links where reproduction is restricted. Deep links include `#entry-29/dossier` and `#entry-31/landscape`.

The retired `#history` and `#entry-N/history` links open Places, preserving the requested entry where supplied.

## Validation

The feature workbench, added 8 October 2026, has five research views at `#workbench/relationships`, `/inventory`, `/states`, `/coverage` and `/decisions`. Open **Research tools** from the main navigation or the entry's Evidence tab. The views load a separate generated snapshot from `../research/feature_workbench/build.py`; [its guide](../research/feature_workbench/README.md) documents the inputs, evaluators and research limits. Native aperture chords retain source coordinates; they are not map overlays. Decision outcome selections are hypothetical and write no evidence or request status.

Run `python3 ../research/feature_workbench/check.py` to check semantic tests and snapshot freshness. After dependency installation, `node scripts/check-workbench.mjs` renders all five modules and all 179 saved selector choices without starting a browser. It checks control inclusion, selected branch results, source qualifiers and planning labels. The October 2026 revamp was tested in the browser on desktop and mobile; the earlier workbench rendering check remains available.

The data generator verifies entry and place counts and candidate references. TypeScript and production build checks validate the implementation. The initial creation session lacked a browser preview; the revamp adds browser verification of the linked views, reader routing and film controls. Run `node app/atlas-reader-model.test.mjs` and `node scripts/check-revamp.mjs` for the focused reader and navigation checks.

The Site uses the package manager, build scripts and hosting manifest supplied by the Sites starter.


## Feature evidence review

Entries 21, 32, 49, 31 and 55 now have a “Compare features & evidence” dialog. It separates reading, site and exact-feature judgments, exposes source dependencies/access gaps, and states discriminating checks. Other candidates are explicitly marked as not yet assessed on separate axes. Site confidence and existing sorting remain unchanged.

Edit `app/atlas-evidence.json` for the shared Site/Pages content. The narrative dossier is in `research/feature_investigation.md`; its repository-wide copy is `../research/sites/feature_investigation.md`. Keep both copies aligned. The constraint register is `research/feature_constraints.csv`, mirrored in `../tables/feature_constraints.csv`. Refine locality envelopes into feature outlines or modeled candidate areas as sources permit, recording the geometry method and positional uncertainty.


## Knowledge-base landing page

`app/atlas-home.tsx` routes the empty homepage and `#kb` links to the knowledge base, loading the spatial atlas separately for its existing routes. `app/atlas-kb.tsx` renders the graph, requirements, names, impact and source views; `atlas-kb-model.ts` holds pure traversal functions. The inspector exposes full typed relationships, source locations, assumptions, unknowns and the underlying reviewed record. The graph shows a bounded selection; search and the inspector retain access to every exported record. Mobile places the inspector below the graph, with horizontal graph panning and zoom controls.

`app/atlas-kb.json` is a deterministic projection, never an evidence-editing surface. Refresh it from the repository root after reviewing canonical inputs:

```sh
PYTHONPATH=research/shared_tools python3 -m claim_kb.web_export
PYTHONPATH=research/shared_tools python3 -m claim_kb.web_export --check
cd atlas
corepack pnpm run check:kb
corepack pnpm run build:pages
```

The Pages build rejects a stale snapshot. The existing hosted Site uses the same checked-in snapshot; update evidence in the repository before synchronizing Site source. Public export calls the pilot's `public_view` filter before building entry indexes. Its version is a content hash of canonical records and input versions; explicit reviewed claim notices propagate reassessment flags to affected public results, while SQLite history stays in the local pilot. The public impact view computes dependency paths and preserves historical test outcomes. It does not simulate new archaeological evidence or revise a conclusion.

Validation covers both edition-reading alternatives, all entry graph contexts, equal candidate options, exact source locators, name/date fields, dependency effects and five server-rendered views. Existing atlas navigation, site-plan and model checks remain available. Browser QA for this update could not run: the managed preview supervisor was unavailable. Responsive CSS and server rendering were checked; browser appearance and touch interactions remain unverified.
