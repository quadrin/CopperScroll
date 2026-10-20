# Site models built in Minecraft — 20 October 2026

The atlas's twelve source-based site models were built block by block in a Minecraft Java Edition server, saved, and read back from the world's region files. The atlas map now draws the read-back blocks by default (**Blocks**; **Smooth** keeps the earlier geometry). This is a display change. It adds no archaeological observation and changes no reading, identification, coordinate or confidence.

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

| Model | Block | Grid (blocks) | Minecraft origin (x, y, z) | Fill commands | Blocks placed | Read-back mismatches | Faces | Atlas file |
|---|---|---|---|---|---|---|---|---|
| qumran-ilan | 0.5 units | 360 × 56 × 240 | 0, -60, 0 | 15,080 | 2,940,292 | 0 | 25,170 | qumran-ilan.bin.gz (147 KB) |
| qumran-reeder | 0.25 units | 188 × 23 × 110 | 1024, -60, 0 | 1,052 | 167,871 | 0 | 3,245 | qumran-reeder.bin.gz (16 KB) |
| jericho-ac | 0.25 units | 142 × 14 × 188 | 2048, -60, 0 | 772 | 212,688 | 0 | 1,600 | jericho-ac.bin.gz (9 KB) |
| jericho-early | 0.25 m | 172 × 30 × 188 | 3072, -60, 0 | 440 | 424,437 | 0 | 768 | jericho-early.bin.gz (4 KB) |
| jericho-late | 0.25 m | 192 × 30 × 142 | 4096, -60, 0 | 303 | 330,080 | 0 | 584 | jericho-late.bin.gz (3 KB) |
| siloam-receiver | 0.25 units | 188 × 19 × 112 | 5120, -60, 0 | 662 | 168,774 | 0 | 1,546 | siloam-receiver.bin.gz (8 KB) |
| gerizim-precinct | 0.5 m | 510 × 43 × 580 | 6144, -60, 0 | 1,882 | 5,369,218 | 0 | 3,028 | gerizim-precinct.bin.gz (17 KB) |
| doq-waterworks | 0.25 units | 156 × 24 × 152 | 7168, -60, 0 | 1,931 | 380,264 | 0 | 4,633 | doq-waterworks.bin.gz (23 KB) |
| hyrcania-waterworks | 0.25 m | 354 × 43 × 344 | 8192, -60, 0 | 4,283 | 3,196,563 | 0 | 11,415 | hyrcania-waterworks.bin.gz (57 KB) |
| abu-saraj-iv17 | 0.25 m | 48 × 16 × 36 | 9216, -60, 0 | 401 | 11,687 | 0 | 1,379 | none: no map location; built with its roof |
| bethesda-pools | 0.5 m | 256 × 36 × 216 | 10240, -60, 0 | 858 | 1,348,927 | 0 | 1,099 | bethesda-pools.bin.gz (6 KB) |
| east-gate-warren | 0.5 m | 260 × 85 × 200 | 11264, -60, 0 | 1,216 | 2,759,472 | 0 | 2,042 | east-gate-warren.bin.gz (11 KB) |

"Units" are the source-relative units of those scenes. Every air block next to a drawn face has saved sky light; sections without saved light are open sky or solid rock. The Qumran build is fitted to the Kh. Qumran terrain patch; at Wadi Qumran the atlas keeps the smooth model.

## Source change built into this round

Qumran (qumran-ilan): basin 2 and the dam proposed at point 4 are now drawn, in both styles. Ilan & Amit 2002 Fig. 1 (p. 380; owner's library photo, 19 Oct 2026, [record](../../sources/aqueducts2002_firsthand_2026-10-20/README.md)) draws a heavy dashed line from point 3 to point 4 across the east side of basin 2; it is read as probably the dam (drawing only). The 1989 text reports no surviving dam (pp. 284, 288 n. 5). The dam is therefore copper, the atlas's colour for a published reconstruction; its height and width and the basin depth are illustrative. The plan's dashed line, earlier drawn as a copper channel, is now its own `dam` kind.

## Traced plans, reconstruction views and wider terrain — 20 October 2026, later

- A traced plan ([format](../traced_plans/SCHEMA.md)) is built once per view. **Remains** holds only what an excavation plan records as found. A reconstruction view adds what one published reconstruction draws for its phase; those parts are `smooth_sandstone`, a colour used for nothing else, and never replace a block of found remains. Heights that no source gives are illustrative and are listed in each view's **Sources & assumptions**.
- Kh. Qumran settlement ([tracing](../traced_plans/qumran-settlement.md), Magen & Peleg 2018 Fig. 9): 0.5 m blocks over the traced plan and a level display bench. Lines that the figure draws dashed, without a stated meaning, are one-slab strips.
- Surroundings: a plan with wide terrain gets two more builds, each a square ring with a hole exactly the size of the build inside it: 2 m blocks to 400 m from the centre and 8 m blocks to 1,152 m. Their ground is the wider Kh. Qumran terrain patch (Mapterhorn z13, about 8 m per pixel; [manifest](../../assets/plans/atlas-explorer/terrain-wide/manifest.json)), so the cliffs, the marl terrace and the slope to the Dead Sea are blocks too. A block in a ring is one terrain sample; the rings add no survey detail.

## The world save

[`copper-scroll-sites-26.3.zip`](copper-scroll-sites-26.3.zip) (6.5 MB) is the saved world, SHA-256 `2e9c34f6cea718ad6a9b425d3fbb12648247d8ee8cb53507346ac32904b60ea7`. Unzip the `world` folder into a Minecraft Java 26.3 `saves` folder (or a server folder) to walk the builds. The world is a void with creative mode as the default; the spawn is in front of the Qumran tunnel mouth (188, -23, 163). Each model starts at its origin in the table. In Minecraft's own scale the player is two to four times life size, because one block is 0.5 or 0.25.

## Rebuild

```sh
cd atlas
node scripts/minecraft/build-world.mjs --jar <server.jar> --java <Java 25> --work <empty folder>
node scripts/check-minecraft.mjs
```

`--skip-server` re-reads an existing save. A rebuild from unchanged models gives the same blocks; the same save gives byte-identical atlas files.
