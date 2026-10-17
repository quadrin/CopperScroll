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

A static build of the same atlas is published at <https://quadrin.github.io/CopperScroll/>. The built assets are committed in `../atlas-site/`; `../index.html` loads them at the repository homepage. The existing `/atlas-site/` URL remains available.

Root `_config.yml` excludes the children of `atlas/`, `research/` and `images/` with `/**` patterns, and disables the documentation theme. Literal `exclude: atlas` also matches `atlas-site`. Adding `include: atlas-site` keeps the parent directory but does not protect its children; do not restore that configuration. The research archives remain in GitHub.

After building, run `bash scripts/check-pages-build.sh <empty-output-directory>`. It uses the same pinned Docker image as GitHub's `jekyll-build-pages` action and validates the actual output with `check-pages-payload.mjs --site-dir ...`. Every app file must retain its bytes, both entrypoints must resolve, archives must be absent and the published output must fit the size limit. Serve that output under `/CopperScroll/` for the browser checks. They load the bare homepage, reject missing local assets, and exercise a failed startup import followed by Reload. Check the deployed commit and artifact in GitHub Actions after pushing; a raw Vite build does not validate Pages publication.

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

Candidate lists, the scroll register, the dossier and the "Evidence" sort show evidence components instead of the single low/medium label: reading, place, feature and date, each rated 0–3, plus uniqueness, with the weakest part setting the label ([rubric and ratings](../research/assessments/evidence_components/README.md)). `python3 ../tools/build_evidence_components.py` writes `app/atlas-components.json` from the reviewed ratings. The low/medium fields remain in `app/atlas-data.json` for the existing data checks.

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

The map opens with all 36 geographically placed sites in view, including the northern candidates. **Sites** searches all 40 candidates; the four without an established coordinate remain in the list without a pin. **Show all sites** returns to the full extent. Entry searches do not hide other map pins.

Select a pin or a name in **Sites**, then use **Zoom to site** for a close-up at its approximate anchor. Zoom buttons work on phones and desktops; wheel, pinch and keyboard zoom remain available. Nearby site names appear at close zoom. **Plan & details**, **Photos** and **Sources** share one inline panel beside the map. Photos also contains site videos. Historical maps open from **Options**. Plans pan and zoom up to 32×; candidates without a plan expose their existing references. The plan, numbered feature list, description, interpretation, citations and expandable Hebrew/English passage are native atlas content. They share the same panel on desktop and phone, without a separate explorer or collapsed inspector drawer. Unplaced IV/17 opens its plan for legacy source/model/walk links and is not assigned an invented map pin.

Plan captions and the map’s **Sources** panel link the cited works to the owner’s Google Drive Copper Scroll library. The mapping in `app/atlas-library-references.json` uses the checked-in Drive manifest and existing plan/asset records, retaining exact printed-page and figure locators. It is a catalogue match, not a new inspection or verification of live Drive access. Reeder–Jol 2006 has no identified Drive copy and is marked explicitly. Source galleries also link the library’s historical-map and imagery collections. Photos retain their own source credits; a plan reference does not authenticate or register a photograph.

At close zoom, supported source-based 3D models appear in the geographic map itself; they use the same MapLibre canvas and camera. **Zoom to site** flies into the selected model. Drag the yellow **Walk** figure onto the model, or tap it, for eye-level inspection. It stays beside an open reference panel and above the phone sheet. An unplaced site such as IV/17 explains its map-walking limitation when tapped. Drag to look, including above the horizon, and use W/A/S/D, arrow keys or the phone movement buttons to move. Double-tap W to sprint forward or S to sprint backward; releasing the key ends that sprint. Ctrl also sprints. Space jumps, and holding it repeats the jump after landing. Shift crouches. Phones have Jump, Sprint and Crouch controls. Double-click captures the mouse for first-person look; Escape releases it, and R resets the position. The yellow figure becomes **Exit** and restores the overhead camera. Plans, photographs and references stay within this map surface. Older source/model/walk URLs remain entry points to this unified view.

Qumran has an uneven, tapering limestone ridge and a shaded, irregular tunnel recess around the published aqueduct relationships. Its ground has an irregular feathered boundary; soil, rock, scree and channel floors adapt together to loaded map elevations while preserving source-plan horizontal relationships. The vertical terrain fit is illustrative. The former rectangular tile and full-depth cliff slabs are removed. Channels have open plaster-lined troughs. Jericho, Siloam, Gerizim, Doq and Hyrcania retain their source-qualified layouts, with individual chipped masonry courses, coping stones, soil relief, rubble and sparse vegetation. Site-specific palettes distinguish limestone, ashlar and worn plaster. World-space surface mapping keeps the grain and joints at a consistent scale as the camera moves. Directional shadows and a sky at eye level provide depth; repeated stones are instanced to reduce draw calls. Position, bearing, heights and missing architecture retain the existing limits. Walking uses a 1.8 m capsule body with a 0.30 m radius, gravity and collision against the displayed ground, rock, walls and ceilings. Eye height is 1.62 m standing and 1.27 m crouching, with one blocky right forearm fixed in the lower-right corner of the view. The character steps over ledges up to 0.60 m, climbs slopes up to 50 degrees, slides along walls and cannot stand up under a low ceiling. Sneaking slows movement to about 1.30 m/s and prevents walking off unsupported ledges. Instanced masonry uses oriented box colliders; vegetation and tiny rubble are excluded. Movement uses Minecraft Java-style acceleration, ground friction, air momentum and vertical drag at 20 Hz, with collision and positions advanced at 120 Hz. Walking reaches 4.317 m/s, sprinting 5.612 m/s and the jump rises about 1.25 m; sprint-jumping adds directional momentum. The world view gently bobs with footsteps and eases from 70° to 81° while sprinting. Reduced-motion preferences disable bobbing and FOV effects. These display colliders do not establish a surveyed ancient walking route. Surface art is original procedural illustration, informed by the archived photographs and published plans. Individual cracks, blocks, vegetation and surface colours are not surveyed observations. The partial Qumran aqueduct does not reconstruct the whole settlement.

The four existing photographs are served at their original source resolutions from `public/dossiers/site-photos/`, with matching research archives and attribution manifests. They remain flat photographs with unregistered camera poses. YouTube references play below the photographs in **Photos**; the existing Qumran leads are marked unreviewed, and users can add video links saved in their browser. **View library scan here** opens the cited Drive file inline using the viewer account’s existing access. Video playback and private Drive previews require provider access; their successful live playback is separate from local interaction tests.

**Satellite** displays Esri World Imagery with provider attribution. It shows the modern landscape, and image dates and native resolution vary by location. The map can zoom to level 22; imagery beyond level 19 enlarges the available tiles rather than adding measured detail. Satellite imagery needs access to `server.arcgisonline.com`. A loading failure is shown explicitly, while pins, site selection and source plans remain usable. **Map** retains the physical-geography basemap, and **Terrain** enables elevation in the current background.

Run `node scripts/check-walk-physics.mjs` for thin-wall sprinting, sliding, stepping, jumping, ceilings, slopes and actual Qumran geometry before and after terrain fitting. Run `node scripts/check-walk-camera-browser.mjs` for rendered-camera checks with a real MapLibre map and controlled negative DEM: missing terrain samples, crouching, sprint FOV, jumping, looking, delayed elevation, resize and map return. It requires no live services; `ATLAS_WALK_SOURCE` can select an older controller to confirm the regression fails. Run `node scripts/check-map-browser.mjs` against the static development server for desktop/phone checks of the full extent, northern-site zoom, satellite failure handling, source plans, photos and unplaced candidates. The test uses Chromium and `playwright-core`; `ATLAS_CHROMIUM`, `ATLAS_PLAYWRIGHT_MODULE` and `ATLAS_TEST_ORIGIN` can select installed tools and the server address. Set `ATLAS_TEST_MOTION=normal` to exercise normal movement effects and assert sprint field-of-view changes; the default uses reduced motion. Run `node scripts/check-site-reference-browser.mjs` for the IV/17 figure, visible feature list, inline evidence/passage and legacy aliases on desktop and phone. The checks retain the same atlas canvas. It also verifies that pins and zoom work when all external map services fail. The satellite failure fixture does not verify real imagery coverage.

MapLibre GL JS renders an OpenFreeMap basemap based on OpenMapTiles and OpenStreetMap, with Mapterhorn elevation tiles. A neutral background preserves site pins if the primary style is unavailable. The map uses modern geographical data, not a reconstructed ancient coastline or road network. The Terrain control enables terrain and a pitched camera, with 1.5× vertical exaggeration. Close-up scale is preserved on entry. Loaded elevations are retained during transient zero samples so below-sea-level sites do not jump back to sea level; the camera follows the loaded height. The browser regression uses a controlled negative-elevation DEM. During walking, the capsule controller owns the final camera transform, overriding MapLibre’s separate terrain-camera correction. A missing elevation sample must not lift a below-sea-level character to sea level. The draw matrix independently reports the actual eye position; browser checks compare it with the physical character. Walking camera updates do not replace the saved overhead map view.

Map source attribution remains visible. MapLibre's local worker and shared module preserve the package license headers; they come from installed version 6.10.0. If upgrading MapLibre, refresh both files in `public/maplibre/` together.

MapLibre owns each marker's outer `site-marker` element, including its absolute position, transform and terrain visibility classes. Selection changes only the child button. Do not overwrite the outer element's class list or set relative positioning on it: this introduces document-flow offsets and makes pins drift during zoom. Settlement labels use the vector tile `place` category rather than relying on style-layer name prefixes.

## Interaction

The primary map opens the regional overview and zooms continuously into supported site geometry. **Find a place or entry** opens searchable browsing; entry details and research tools open on demand. **Plan & details** opens the selected source plan and feature inspector beside the geographic view. Site evidence and interpretations remain in the same panel under Sources. Other places retain their references and a clear source-plan coverage gap. IV/17 has a source plan but no established geographic location for map-based eye level.

Drag to pan, scroll/pinch to zoom, and select plan features to focus the map camera. Show all sites restores the regional overview. The surrounding landscape uses sampled Mapterhorn elevation at the existing site anchor; model placement, bearing and the display bench remain illustrative. Sources & assumptions explains the display geometry. Three.js 0.186.1 supplies the renderer; its MIT notice is in `public/licenses/three-LICENSE.txt`. Run `node scripts/check-models.mjs` for source-dimension and geometry checks.

Site plans remain in their source-coordinate frames. **Regional terrain** is a secondary locator with relief, water and regional names. Modern buildings, roads, land-use/POIs and modern-street raster fallback are excluded. Historical survey records are available only in the archive tools. Source-derived geometry is displayed at the gazetteer anchors with explicit approximate alignment. This display placement supplies neither a surveyed footprint nor verified compass bearing.

**Photos** is contextual to the selected site. The existing four photographs retain annotated details, credits and image-relative polygons; the inspector distinguishes photographed context from an unregistered plan feature. Zoom/pan works with mouse, touch and keyboard. The photograph stays inside the atlas reference panel.

**Back**, browser Back/Forward and reload restore the selected entry/candidate, source plan, feature and recorded geographic camera. Plan pan/zoom persists while its panel is open; photo controls are local to the selected photo panel. Column changes in the scroll enter history. Source-plan routes include `#entry-21/site/qumran-ilan/D`, `#entry-29/site/jericho-ac/AC94` and `#entry-49/site/siloam-receiver/L103`; a `/photo` suffix opens contextual imagery.

See [photo and feature integration](PHOTO_INTEGRATION.md) for coverage, provenance, source-coordinate limits and next asset additions. Data checks are `node scripts/check-explorer.mjs` and `node scripts/check-terrain-style.mjs`. `node scripts/check-explorer-browser.mjs` runs both unified-map and native-reference browser checks (requires Playwright Core and Chromium); `ATLAS_PLAYWRIGHT_MODULE` can select the installed Playwright module.

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

`app/atlas-home.tsx` routes the homepage and `#kb` links to the knowledge base. The default passage view follows three steps: read the passage and retained alternatives, compare candidates under one branch and period, then inspect the additional observations that could decide the unresolved requirements. Candidate rows expand to show fixed assignments, individual checks and source links. The Entry 25 comparison starts with its four primary reading/aspect combinations; an explicit checkbox reveals all registered depth and sensitivity combinations. Evidence opens in a keyboard-accessible dialog with Back, Close and Escape; the page keeps its place underneath. The connection graph and all saved tests remain secondary views alongside names, sources and change impact.

`atlas-kb-model.ts` exposes pure traversal and comparison functions. Comparisons join exact branch/window keys across candidates; missing results stay explicit, and duplicate cells fail instead of choosing one. URLs preserve entry, view and selected evidence. Search covers every exported record. The single document flow stacks on narrow screens; graph panning stays within its own view.

`app/atlas-kb.json` is a deterministic projection, never an evidence-editing surface. Refresh it from the repository root after reviewing canonical inputs:

```sh
PYTHONPATH=research/shared_tools python3 -m claim_kb.web_export
PYTHONPATH=research/shared_tools python3 -m claim_kb.web_export --check
cd atlas
corepack pnpm run check:kb
corepack pnpm run build:pages
```

The Pages build rejects a stale snapshot. The existing hosted Site uses the same checked-in snapshot; update evidence in the repository before synchronizing Site source. Public export calls the pilot's `public_view` filter before building entry indexes. Its version is a content hash of canonical records and input versions; explicit reviewed claim notices propagate reassessment flags to affected public results, while SQLite history stays in the local pilot. The public impact view computes dependency paths and preserves historical test outcomes. It does not simulate new archaeological evidence or revise a conclusion.

Validation covers all entry graphs, guided passage sections, every retained branch/window comparison, explicit missing controls, duplicate-cell rejection, source locators, name dates and dependency effects. Live desktop browser checks covered candidate expansion, source drill-down, Back and Escape with the expanded candidate preserved. Mobile layout remains CSS-checked; automated rendering checks alone do not verify touch interaction.


## Navigation and close inspection

The shared header has three destinations: **Evidence**, **Map** and **Scroll**, retaining the selected entry. Sources and research comparisons belong to Evidence. Plans, photos, videos, historical imagery and site evidence are accessible within the map; its panel has Plan, Photos and Sources, with videos under Photos and historical maps under Options. The site-plan selector opens every available source plan. Invalid routes show a recovery view. Geographic routes use an explicit `/2d` suffix; legacy bare entry links retain their historical site view.

Source plans support up to 32× zoom. Geographic overzoom reaches level 22 and enlarges the available imagery; it adds no survey detail. A source plan can be linked directly with `#entry-25/site/abu-saraj-iv17/source`. A located site can open directly at eye level with `#entry-21/site/qumran-ilan/walk`.

Eye level uses the geographic map camera over the existing illustrative geometry. Drag to look, use W/A/S/D or arrows to move, or hold the on-screen movement buttons. Eye height follows the modeled ground; a wall-collision mesh and surveyed walking route are not supplied. Sources and assumptions remain available beside the map. Leaving eye level restores the previous geographic camera.

### Building measured 3D sites

A measured site asset needs a local coordinate frame, plan scale, sections or spot heights, and a phase assignment. Trace walls, floors, openings and roofs only where the source constrains them. Fit photographs to known control points; overlapping photographs or a scan can supply a present-day surface, with scale bars and independent check measurements. A single photograph cannot establish hidden rooms or an absent roof. Register the local model to the map only after independent control points support that transformation; source-relative assets remain in their own frame.

Keep surviving remains, proposed ancient reconstruction and illustrative context as separate layers. Each modeled component should carry its feature ID, source locator, date/phase, measurement basis, uncertainty and whether it is observed, reconstructed or illustrative. Export local site meshes as GLB/glTF for the existing Three.js viewer. Dense regional scans could use streamed 3D Tiles later. A grounded walkthrough requires measured floor topology, passage and ceiling clearances, a collision mesh and a navigation mesh. These are additional evidence and asset requirements, rather than a consequence of higher zoom.

The IV/17 model is a suitable bounded pilot: its plan scale and reported height constrain part of the geometry, while its roof profile, thresholds and geographic registration require further evidence. Preserve those gaps in any new asset.


### Phone navigation

At phone widths, Evidence, Map and Scroll fit in a single row. The passage, candidate and site-plan selectors live in the expandable passage/place panel; the current selection and search stay visible. Native selectors use 16px text and controls use 44px targets. Escape, outside taps and navigation close the panel. The map keeps mode/north controls in its first row and details/layers/zoom in a second row, above a bounded selected-site card. The reference panel opens as a bottom sheet while the same geographic canvas stays mounted. Safe-area spacing follows the dynamic viewport.
## Qumran aqueduct detail

Select Khirbet Qumran or Wadi Qumran on the map and choose **Zoom to site**. Close zoom reveals the aqueduct in MapLibre’s shared 3D render pipeline. The yellow person enters eye level; source-plan feature selection moves the same camera.

Ilan–Amit 1989 p. 283 Fig. 1 supplies sampled channel/branch relationships; the existing Davey CJD979, Reeder–Jol Fig. 2 and Magen–Peleg Fig. 87 comparison supplies tunnel-mouth references. Weathering, rubble, masonry, vertical geometry, display scale, bearing and the raised outcrop are illustrative. The existing Wadi Qumran anchor has approximately 500 m uncertainty. The model is neither surveyed placement nor photogrammetry. No reference photographs or publication-page pixels are redistributed as textures.

`node scripts/check-qumran-pilot.mjs` checks continuous cliff geometry, finite coordinates, anchor directions and camera stops without a GPU. Chromium checks exercise actual WebGL rendering and eye-level movement; screenshots are visually compared against the archived material references. The result is a stylized interpretation.

## Interface simplification

Current navigation exposes Evidence, Map and Scroll. The More menu, duplicated section links and unused About overlay are removed. Sources and research comparisons remain in Evidence; old research bookmarks still open. The passage/place selector collapses at every width. Maps render one compact site card and one Options menu, with close zoom revealing the source-based model and inline panels showing its references. Separate pilot/selection cards, compass, terrain-settings panel and map-layer toolbar no longer render. Options dismisses on outside click, Escape and view changes. `node scripts/check-interface.mjs` checks navigation/defaults alongside existing route and geometry tests.
