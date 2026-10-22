# Site models built in Minecraft — 20 October 2026

The atlas's source-based site models were built block by block in a Minecraft Java Edition server, saved, and read back from the world's region files. The atlas map now draws the read-back blocks by default (**Blocks**; **Smooth** keeps the earlier geometry). This is a display change. It adds no archaeological observation and changes no reading, identification, coordinate or confidence.

## What was run

- Server: Minecraft Java Edition **26.3**, Mojang's official `server.jar` from the version manifest, SHA-1 `33680f5f2ac32864d6d7cf5e56a705fdb3e05f4c` (matches the manifest), chunk DataVersion 5023, run on OpenJDK 25. Running it accepted the [Minecraft EULA](https://aka.ms/MinecraftEULA), on the owner's instruction to use the actual game.
- Pipeline: [`atlas/scripts/minecraft/`](../../../atlas/scripts/minecraft/). `build-world.mjs` builds each model with the atlas's own builders (`atlas-model-geometry.ts`, `atlas-qumran-pilot.ts`), converts it to blocks (`voxelize.mjs`), starts the server on a fresh void world, places the blocks with `/fill` over RCON (`rcon.mjs`), saves, and reads every block and its sky light back from the region files (`anvil.mjs`). `mesh.mjs` turns the read-back blocks into the faces the atlas draws. Only read-back data reaches the atlas.
- Check: `node atlas/scripts/check-minecraft.mjs` (every block read back as placed; files decode inside their grids; plan features and markers on the source frame).

## How a model becomes blocks

- Block size: 0.5 m for the large sites, 0.25 for the small and source-relative scenes. Cells are half a block high, so a lone half becomes a slab (a 0.25 m or 0.125 step). Soil has no slab in Minecraft and stays in whole blocks.
- Ground: each column is filled from the model's terrain height down to the grid floor, except inside the terrain's own holes (pools, shafts, the Golden Gate cutaway). The terrain is the same Mapterhorn patch and display bench as the smooth model. Outside the block grid the atlas keeps the smooth terrain.
- Architecture: stones and walls become oriented boxes; closed solids are filled by an inside test per column; thin or open surfaces are sampled. Dimensions thinner than a cell are widened to one cell, and each stone claims 2 cm beyond its faces so that the drawn joints (1.4–3.5 cm) leave no holes. A cell centre on a face counts on one side only. Each block area is a closed solid: its sides and floor have faces too, so a walker who leaves it cannot see or walk into its inside.
- Materials: soil → `coarse_dirt`; rock → `stone`; limestone blocks → `smooth_stone`; masonry by the site's photo-derived type (rubble → `cobblestone`, coursed → `stone_bricks`, ashlar → `cut_sandstone`); plaster → `smooth_quartz`; the copper colour that marks a source's proposed course or reconstruction → `waxed_cut_copper`. Each has its slab.
- Qumran's tunnel recess, a dark plane in the smooth model, is carved as a real opening.
- In the atlas each face is shaded by the sky light Minecraft saved for the open block in front of it, so covered parts (the Qumran recess, cisterns, the IV/17 cave, Warren's gallery) are darker. While walking, the site is drawn with a near plane of about 5 cm instead of the map's half a metre, so a wall or overhang beside the eye is not cut away (the cause of an "x-ray" view into the blocks, reported 20 October). Block textures are original 16-pixel tiles in each site's photo-derived colours. No Minecraft code, textures or other assets are in the repository or the atlas.

Rounding to the block size can move an edge or a height by up to half a block. The blocks keep every simplification and illustrative dimension of the source model (listed in each model's **Sources & assumptions**); they add none of their own.

## Builds

| Build | Block | Grid (blocks) | Minecraft origin (x, y, z) | Fill commands | Blocks placed | Read-back mismatches | Faces | Atlas file |
|---|---|---|---|---|---|---|---|---|
| qumran-ilan | 0.5 units | 360 × 56 × 240 | 0, -60, 0 | 15,080 | 2,940,292 | 0 | 25,170 | qumran-ilan.bin.gz (147 KB) |
| qumran-reeder | 0.25 units | 188 × 23 × 110 | 1024, -60, 0 | 1,052 | 167,871 | 0 | 3,245 | qumran-reeder.bin.gz (16 KB) |
| jericho-ac | 0.25 units | 142 × 14 × 188 | 2048, -60, 0 | 772 | 212,688 | 0 | 1,600 | jericho-ac.bin.gz (9 KB) |
| jericho-early@stage3 | 0.25 m | 506 × 40 × 342 | 3072, -60, 0 | 1,050 | 3,755,009 | 0 | 4,433 | jericho-early@stage3.bin.gz (24 KB) |
| jericho-early | 0.25 m | 388 × 29 × 270 | 4096, -60, 0 | 746 | 2,178,413 | 0 | 1,438 | jericho-early.bin.gz (8 KB) |
| jericho-late@stage6 | 0.25 m | 504 × 40 × 336 | 5120, -60, 0 | 1,422 | 3,679,386 | 0 | 9,277 | jericho-late@stage6.bin.gz (51 KB) |
| jericho-late@herodian | 0.25 m | 502 × 39 × 322 | 6144, -60, 0 | 863 | 3,442,683 | 0 | 3,206 | jericho-late@herodian.bin.gz (17 KB) |
| jericho-late | 0.25 m | 388 × 29 × 270 | 7168, -60, 0 | 746 | 2,178,413 | 0 | 1,438 | jericho-late.bin.gz (8 KB) |
| siloam-receiver | 0.25 units | 188 × 19 × 112 | 8192, -60, 0 | 662 | 168,774 | 0 | 1,546 | siloam-receiver.bin.gz (8 KB) |
| gerizim-precinct | 0.5 m | 510 × 43 × 580 | 9216, -60, 0 | 1,882 | 5,369,218 | 0 | 3,028 | gerizim-precinct.bin.gz (17 KB) |
| gerizim-precinct@persian | 0.5 m | 510 × 42 × 580 | 10240, -60, 0 | 524 | 5,033,957 | 0 | 750 | gerizim-precinct@persian.bin.gz (5 KB) |
| doq-waterworks | 0.25 units | 156 × 24 × 152 | 11264, -60, 0 | 1,931 | 380,264 | 0 | 4,633 | doq-waterworks.bin.gz (23 KB) |
| hyrcania-waterworks | 0.25 m | 724 × 101 × 368 | 12288, -60, 0 | 7,375 | 19,237,413 | 0 | 13,662 | hyrcania-waterworks.bin.gz (73 KB) |
| hyrcania-waterworks@herodian | 0.25 m | 726 × 129 × 368 | 13312, -60, 0 | 7,441 | 19,341,407 | 0 | 13,684 | hyrcania-waterworks@herodian.bin.gz (73 KB) |
| abu-saraj-iv17 | 0.25 m | 48 × 16 × 36 | 14336, -60, 0 | 401 | 11,687 | 0 | 1,379 | none: no map location; built with its roof |
| bethesda-pools | 0.5 m | 256 × 37 × 256 | 15360, -60, 0 | 884 | 1,742,009 | 0 | 1,102 | bethesda-pools.bin.gz (6 KB) |
| bethesda-pools@royal | 0.5 m | 256 × 31 × 256 | 16384, -60, 0 | 325 | 1,490,278 | 0 | 427 | bethesda-pools@royal.bin.gz (3 KB) |
| east-gate-warren | 0.5 m | 260 × 85 × 200 | 17408, -60, 0 | 1,216 | 2,759,472 | 0 | 2,042 | east-gate-warren.bin.gz (11 KB) |
| kidron-bene-hezir | 0.25 m | 284 × 112 × 444 | 18432, -60, 0 | 40,731 | 7,495,384 | 0 | 54,535 | kidron-bene-hezir.bin.gz (314 KB) |
| kidron-bene-hezir@avigad | 0.25 m | 284 × 112 × 444 | 19456, -60, 0 | 41,101 | 7,495,268 | 0 | 55,608 | kidron-bene-hezir@avigad.bin.gz (320 KB) |
| temple-great-sea | 0.5 m | 142 × 61 × 170 | 20480, -60, 0 | 1,163 | 782,685 | 0 | 3,920 | temple-great-sea.bin.gz (20 KB) |
| qumran-settlement | 0.5 m | 248 × 17 × 408 | 21504, -60, 0 | 3,174 | 1,422,484 | 0 | 11,222 | qumran-settlement.bin.gz (56 KB) |
| qumran-settlement~ring1 | 2 m | 400 × 58 × 400 | 22528, -60, 0 | 25,754 | 3,546,029 | 0 | 37,949 | qumran-settlement~ring1.bin.gz (228 KB) |
| qumran-settlement~ring2 | 8 m | 288 × 42 × 288 | 23552, -60, 0 | 11,110 | 754,106 | 0 | 32,757 | qumran-settlement~ring2.bin.gz (189 KB) |
| kidron-bene-hezir~ring1 | 1 m | 608 × 130 × 608 | 24576, -60, 0 | 157,336 | 23,346,370 | 0 | 248,619 | kidron-bene-hezir~ring1.bin.gz (1467 KB) |
| kidron-bene-hezir~ring2 | 8 m | 288 × 27 × 288 | 25600, -60, 0 | 13,716 | 1,027,149 | 0 | 41,327 | kidron-bene-hezir~ring2.bin.gz (239 KB) |
| temple-great-sea~ring1 | 1 m | 608 × 114 × 608 | 26624, -60, 0 | 85,324 | 24,987,255 | 0 | 147,768 | temple-great-sea~ring1.bin.gz (886 KB) |
| temple-great-sea~ring2 | 8 m | 288 × 27 × 288 | 27648, -60, 0 | 12,204 | 1,074,872 | 0 | 35,190 | temple-great-sea~ring2.bin.gz (203 KB) |

A name with `@` is a reconstruction view of that plan (the plain name is its **Remains** view); `~ring1` and `~ring2` are the terrain rings. "Units" are the source-relative units of those scenes. Every air block next to a drawn face has saved sky light; sections without saved light are open sky or solid rock. The Qumran build is fitted to the Kh. Qumran terrain patch; at Wadi Qumran the atlas keeps the smooth model.

## Source change built into this round

Qumran (qumran-ilan): basin 2 and the dam proposed at point 4 are now drawn, in both styles. Ilan & Amit 2002 Fig. 1 (p. 380; owner's library photo, 19 Oct 2026, [record](../../sources/aqueducts2002_firsthand_2026-10-20/README.md)) draws a heavy dashed line from point 3 to point 4 across the east side of basin 2; it is read as probably the dam (drawing only). The 1989 text reports no surviving dam (pp. 284, 288 n. 5). The dam is therefore copper, the atlas's colour for a published reconstruction; its height and width and the basin depth are illustrative. The plan's dashed line, earlier drawn as a copper channel, is now its own `dam` kind.

## Traced plans, reconstruction views and wider terrain — 20 October 2026, later

- A traced plan ([format](../traced_plans/SCHEMA.md)) is built once per view. **Remains** holds only what an excavation plan records as found. A reconstruction view adds what one published reconstruction draws for its phase; those parts are `smooth_sandstone`, a colour used for nothing else, and never replace a block of found remains. Heights that no source gives are illustrative and are listed in each view's **Sources & assumptions**.
- Kh. Qumran settlement ([tracing](../traced_plans/qumran-settlement.md), Magen & Peleg 2018 Fig. 9): 0.5 m blocks over the traced plan and a level display bench. Lines that the figure draws dashed, without a stated meaning, are one-slab strips.
- Surroundings: a plan with wide terrain gets two more builds, each a square ring with a hole exactly the size of the build inside it: 2 m blocks to 400 m from the centre and 8 m blocks to 1,152 m. Their ground is the wider Kh. Qumran terrain patch (Mapterhorn z13, about 8 m per pixel; [manifest](../../assets/plans/atlas-explorer/terrain-wide/manifest.json)), so the cliffs, the marl terrace and the slope to the Dead Sea are blocks too. A block in a ring is one terrain sample; the rings add no survey detail.

## Round of 22 October 2026

Two new site models and four new views of existing models, built the same way, with the same server (26.3, jar SHA-1 `33680f5f…`, run on Temurin 25.0.5). Sources and what is evidence or illustrative: [site models record](../site_models_2026-10-22.md).

- New: `kidron-bene-hezir` (Bene Ḥezir, Zechariah and Absalom after Avigad 1954; 0.25 m blocks) with the view `@avigad` (original state and Avigad's nefesh pyramid), and `temple-great-sea` (cistern VIII after Warren Pl. VII and Gibson & Jacobson 1996; 0.5 m blocks).
- New views: `hyrcania-waterworks@herodian`, `bethesda-pools@royal`, `gerizim-precinct@persian`. Hand-built models can now have views like the traced plans: `buildSpecs` gives one build per entry in a plan's `layers`, whether or not the plan is traced.
- Changed remains builds: Hyrcania (the 112 m east bridge, the round pit and the point 49 tunnel, after Patrich 2002) and Bethesda (the 40 m dam, the north pool turned to 40 × 53 m, the square shaft, after Pierre & Rousée 1981). All other builds read back with the same fill counts and blocks as on 20 October.
- Rock-cut spaces (the tomb chambers, kokhim, stair and corridor at Bene Ḥezir, the stair into the Great Sea, the dam's shaft and corridor at Bethesda) are drawn as rock boxes band by band between floor and ceiling levels, so they stay open in the blocks and can be walked.
- The build script now sets the saved world's default game mode (creative) and spawn (188, −23, 163) itself, as the world save below describes.

## Later on 22 October 2026: surroundings

- `kidron-bene-hezir` and `temple-great-sea` are now registered to OpenStreetMap and keep the place frame ([record](../site_models_2026-10-22.md#surroundings-and-registration)). Both have wide terrain (Mapterhorn patches for `jer_kidron_mon` and `jer_temple`), so each gets two rings.
- Rings are now set per site (`SITES[].rings` in `build-world.mjs`; Qumran keeps 2 m to 400 m and 8 m to 1,152 m). For these two: 1 m blocks to ±304 m, with the mapped surroundings built in, then 8 m blocks of terrain to ±1,152 m.
- Surroundings in blocks: graves, city and retaining walls, gate buildings and buildings as solids; mapped paths and stairs as paved ground (the top half metre of the column takes the site's masonry block under a path and `smooth_stone` under a stair). Stair treads are built only in the fine builds, which include the surroundings inside their own area at their own block size.
- The other 21 builds read back with the same fill counts and blocks as before. All 28 read back with no mismatches.
- Second pass: four more materials for the setting only, codes 8–11: tree crowns as `oak_leaves[persistent=true]`, trunks as `oak_log`, green ground (the top half metre in mapped woods, orchards and grass) as `moss_block`, and roads as `gray_concrete`. Read-back ignores the leaves' saved distance to a log. The atlas draws them in its own colours. A build's header lists materials only up to the highest code it uses, so builds without the setting keep their bytes.

## The world save

[`copper-scroll-sites-26.3.zip`](copper-scroll-sites-26.3.zip) (23.6 MB, rebuilt on the evening of 22 October 2026 with all 28 builds, including the trees and roads) is the saved world, SHA-256 `c016872ff68126b36ca811ee54e054b591ebf9adc33eb61988e5aee99dc6ff86`. Unzip the `world` folder into a Minecraft Java 26.3 `saves` folder (or a server folder) to walk the builds. The world is a void with creative mode as the default; the spawn is in front of the Qumran tunnel mouth (188, -23, 163). Each build starts at its origin in the table; a plan's views stand side by side, 1,024 blocks apart. In Minecraft's own scale the player is two to four times life size, because one block is 0.5 or 0.25.

## Rebuild

```sh
cd atlas
node scripts/minecraft/build-world.mjs --jar <server.jar> --java <Java 25> --work <empty folder>
node scripts/check-minecraft.mjs
```

`--skip-server` re-reads an existing save. A rebuild from unchanged models gives the same blocks; the same save gives byte-identical atlas files.
