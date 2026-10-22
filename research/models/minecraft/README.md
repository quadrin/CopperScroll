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
- A plan in a mapped setting also gets bare builds for its **Ancient ground** view: the same model and terrain without today's mapped features ([below](#bare-builds-for-the-ancient-ground-view--night-of-22-october-2026)).
- In the atlas each face is shaded by the sky light Minecraft saved for the open block in front of it, so covered parts (the Qumran recess, cisterns, the IV/17 cave, Warren's gallery) are darker. While walking, the site is drawn with a near plane of about 5 cm instead of the map's half a metre, so a wall or overhang beside the eye is not cut away (the cause of an "x-ray" view into the blocks, reported 20 October). Block textures are original 16-pixel tiles in each site's photo-derived colours. No Minecraft code, textures or other assets are in the repository or the atlas.

Rounding to the block size can move an edge or a height by up to half a block. The blocks keep every simplification and illustrative dimension of the source model (listed in each model's **Sources & assumptions**); they add none of their own.

## Builds

| Build | Block | Grid (blocks) | Minecraft origin (x, y, z) | Fill commands | Blocks placed | Read-back mismatches | Faces | Atlas file |
|---|---|---|---|---|---|---|---|---|
| qumran-ilan | 0.5 units | 360 × 56 × 240 | 0, -60, 0 | 15,080 | 2,940,292 | 0 | 25,170 | qumran-ilan.bin.gz (147 KB) |
| qumran-reeder | 0.25 units | 188 × 23 × 110 | 1024, -60, 0 | 1,052 | 167,871 | 0 | 3,245 | qumran-reeder.bin.gz (16 KB) |
| jericho-ac | 0.25 units | 142 × 14 × 188 | 2048, -60, 0 | 772 | 212,688 | 0 | 1,600 | jericho-ac.bin.gz (9 KB) |
| jericho-early@stage3 | 0.25 m | 512 × 39 × 344 | 3072, -60, 0 | 3,381 | 3,815,253 | 0 | 9,763 | jericho-early@stage3.bin.gz (54 KB) |
| jericho-early | 0.25 m | 392 × 29 × 272 | 4096, -60, 0 | 2,255 | 2,216,391 | 0 | 3,890 | jericho-early.bin.gz (22 KB) |
| jericho-late@stage6 | 0.25 m | 504 × 39 × 340 | 5120, -60, 0 | 4,088 | 3,716,295 | 0 | 13,123 | jericho-late@stage6.bin.gz (72 KB) |
| jericho-late@herodian | 0.25 m | 504 × 38 × 324 | 6144, -60, 0 | 2,639 | 3,474,965 | 0 | 4,954 | jericho-late@herodian.bin.gz (28 KB) |
| jericho-late | 0.25 m | 392 × 29 × 272 | 7168, -60, 0 | 2,255 | 2,216,391 | 0 | 3,890 | jericho-late.bin.gz (22 KB) |
| siloam-receiver | 0.25 units | 188 × 19 × 112 | 8192, -60, 0 | 662 | 168,774 | 0 | 1,546 | siloam-receiver.bin.gz (8 KB) |
| gerizim-precinct | 0.5 m | 512 × 123 × 580 | 9216, -60, 0 | 36,713 | 25,299,838 | 0 | 68,761 | gerizim-precinct.bin.gz (432 KB) |
| gerizim-precinct@persian | 0.5 m | 512 × 123 × 580 | 10240, -60, 0 | 36,814 | 25,330,445 | 0 | 69,051 | gerizim-precinct@persian.bin.gz (433 KB) |
| doq-waterworks | 0.25 units | 156 × 24 × 152 | 11264, -60, 0 | 1,931 | 380,264 | 0 | 4,633 | doq-waterworks.bin.gz (23 KB) |
| hyrcania-waterworks | 0.5 m | 380 × 123 × 380 | 12288, -60, 0 | 60,337 | 9,418,334 | 0 | 91,583 | hyrcania-waterworks.bin.gz (553 KB) |
| hyrcania-waterworks@herodian | 0.5 m | 380 × 123 × 380 | 13312, -60, 0 | 60,665 | 9,426,151 | 0 | 92,518 | hyrcania-waterworks@herodian.bin.gz (559 KB) |
| abu-saraj-iv17 | 0.25 m | 48 × 16 × 36 | 14336, -60, 0 | 401 | 11,687 | 0 | 1,379 | none: no map location; built with its roof |
| bethesda-pools | 0.5 m | 258 × 57 × 258 | 15360, -60, 0 | 3,630 | 1,813,937 | 0 | 9,555 | bethesda-pools.bin.gz (53 KB) |
| bethesda-pools@royal | 0.5 m | 258 × 54 × 258 | 16384, -60, 0 | 3,161 | 1,622,956 | 0 | 8,434 | bethesda-pools@royal.bin.gz (47 KB) |
| east-gate-warren | 0.5 m | 262 × 98 × 202 | 17408, -60, 0 | 11,302 | 2,967,635 | 0 | 31,027 | east-gate-warren.bin.gz (169 KB) |
| kidron-bene-hezir | 0.25 m | 284 × 112 × 444 | 18432, -60, 0 | 39,906 | 7,835,222 | 0 | 50,353 | kidron-bene-hezir.bin.gz (292 KB) |
| kidron-bene-hezir@avigad | 0.25 m | 284 × 112 × 444 | 19456, -60, 0 | 40,265 | 7,835,097 | 0 | 51,403 | kidron-bene-hezir@avigad.bin.gz (298 KB) |
| temple-great-sea | 0.5 m | 142 × 61 × 170 | 20480, -60, 0 | 1,163 | 782,685 | 0 | 3,920 | temple-great-sea.bin.gz (20 KB) |
| qumran-settlement | 0.5 m | 250 × 25 × 402 | 21504, -60, 0 | 4,300 | 1,414,255 | 0 | 12,937 | qumran-settlement.bin.gz (65 KB) |
| qumran-settlement~ring1 | 1 m | 608 × 111 × 608 | 22528, -60, 0 | 69,569 | 14,632,150 | 0 | 100,728 | qumran-settlement~ring1.bin.gz (621 KB) |
| qumran-settlement~ring2 | 8 m | 288 × 42 × 288 | 23552, -60, 0 | 11,972 | 785,951 | 0 | 35,385 | qumran-settlement~ring2.bin.gz (204 KB) |
| jericho-early~ring1 | 1 m | 608 × 47 × 608 | 24576, -60, 0 | 35,098 | 7,951,470 | 0 | 52,271 | jericho-early~ring1.bin.gz (330 KB) |
| jericho-early~ring2 | 8 m | 288 × 30 × 288 | 25600, -60, 0 | 10,589 | 463,069 | 0 | 31,784 | jericho-early~ring2.bin.gz (176 KB) |
| jericho-late~ring1 | 1 m | 608 × 47 × 608 | 26624, -60, 0 | 35,098 | 7,951,470 | 0 | 52,271 | jericho-late~ring1.bin.gz (330 KB) |
| jericho-late~ring2 | 8 m | 288 × 30 × 288 | 27648, -60, 0 | 10,589 | 463,069 | 0 | 31,784 | jericho-late~ring2.bin.gz (176 KB) |
| gerizim-precinct~ring1 | 1 m | 608 × 157 × 608 | 28672, -60, 0 | 77,025 | 27,471,124 | 0 | 120,153 | gerizim-precinct~ring1.bin.gz (769 KB) |
| gerizim-precinct~ring2 | 8 m | 288 × 48 × 288 | 29696, -60, 0 | 18,887 | 1,641,944 | 0 | 57,183 | gerizim-precinct~ring2.bin.gz (340 KB) |
| hyrcania-waterworks~ring1 | 1 m | 608 × 166 × 608 | 30720, -60, 0 | 103,510 | 25,149,700 | 0 | 149,770 | hyrcania-waterworks~ring1.bin.gz (955 KB) |
| hyrcania-waterworks~ring2 | 8 m | 288 × 38 × 288 | 31744, -60, 0 | 18,695 | 806,779 | 0 | 56,768 | hyrcania-waterworks~ring2.bin.gz (322 KB) |
| bethesda-pools~ring1 | 1 m | 608 × 98 × 608 | 32768, -60, 0 | 111,127 | 20,772,115 | 0 | 186,926 | bethesda-pools~ring1.bin.gz (1129 KB) |
| bethesda-pools~ring2 | 8 m | 288 × 24 × 288 | 33792, -60, 0 | 11,432 | 940,697 | 0 | 32,277 | bethesda-pools~ring2.bin.gz (183 KB) |
| east-gate-warren~ring1 | 1 m | 608 × 106 × 608 | 34816, -60, 0 | 100,886 | 18,291,641 | 0 | 182,229 | east-gate-warren~ring1.bin.gz (1092 KB) |
| east-gate-warren~ring2 | 8 m | 288 × 26 × 288 | 35840, -60, 0 | 12,049 | 1,048,633 | 0 | 35,241 | east-gate-warren~ring2.bin.gz (203 KB) |
| kidron-bene-hezir~ring1 | 1 m | 608 × 132 × 608 | 36864, -60, 0 | 157,308 | 23,346,172 | 0 | 248,541 | kidron-bene-hezir~ring1.bin.gz (1467 KB) |
| kidron-bene-hezir~ring2 | 8 m | 288 × 27 × 288 | 37888, -60, 0 | 13,716 | 1,027,149 | 0 | 41,327 | kidron-bene-hezir~ring2.bin.gz (239 KB) |
| temple-great-sea~ring1 | 1 m | 608 × 114 × 608 | 38912, -60, 0 | 85,324 | 24,987,255 | 0 | 147,768 | temple-great-sea~ring1.bin.gz (886 KB) |
| temple-great-sea~ring2 | 8 m | 288 × 27 × 288 | 39936, -60, 0 | 12,204 | 1,074,872 | 0 | 35,190 | temple-great-sea~ring2.bin.gz (203 KB) |
| jericho-early@stage3.bare | 0.25 m | 512 × 39 × 344 | 40960, -60, 0 | 3,381 | 3,815,253 | 0 | 9,763 | jericho-early@stage3.bare.bin.gz (54 KB) |
| jericho-early.bare | 0.25 m | 392 × 29 × 272 | 41984, -60, 0 | 2,255 | 2,216,391 | 0 | 3,890 | jericho-early.bare.bin.gz (22 KB) |
| jericho-late@stage6.bare | 0.25 m | 504 × 39 × 340 | 43008, -60, 0 | 4,088 | 3,716,295 | 0 | 13,123 | jericho-late@stage6.bare.bin.gz (72 KB) |
| jericho-late@herodian.bare | 0.25 m | 504 × 38 × 324 | 44032, -60, 0 | 2,639 | 3,474,965 | 0 | 4,954 | jericho-late@herodian.bare.bin.gz (28 KB) |
| jericho-late.bare | 0.25 m | 392 × 29 × 272 | 45056, -60, 0 | 2,255 | 2,216,391 | 0 | 3,890 | jericho-late.bare.bin.gz (22 KB) |
| gerizim-precinct.bare | 0.5 m | 512 × 115 × 580 | 46080, -60, 0 | 26,395 | 25,146,851 | 0 | 39,089 | gerizim-precinct.bare.bin.gz (253 KB) |
| gerizim-precinct@persian.bare | 0.5 m | 512 × 115 × 580 | 47104, -60, 0 | 26,364 | 25,177,458 | 0 | 39,176 | gerizim-precinct@persian.bare.bin.gz (253 KB) |
| hyrcania-waterworks.bare | 0.5 m | 380 × 123 × 380 | 48128, -60, 0 | 52,826 | 9,418,092 | 0 | 82,477 | hyrcania-waterworks.bare.bin.gz (496 KB) |
| hyrcania-waterworks@herodian.bare | 0.5 m | 380 × 123 × 380 | 49152, -60, 0 | 53,166 | 9,425,909 | 0 | 83,432 | hyrcania-waterworks@herodian.bare.bin.gz (501 KB) |
| bethesda-pools.bare | 0.5 m | 258 × 36 × 258 | 50176, -60, 0 | 776 | 1,732,122 | 0 | 1,120 | bethesda-pools.bare.bin.gz (7 KB) |
| bethesda-pools@royal.bare | 0.5 m | 258 × 31 × 258 | 51200, -60, 0 | 405 | 1,541,871 | 0 | 515 | bethesda-pools@royal.bare.bin.gz (3 KB) |
| east-gate-warren.bare | 0.5 m | 262 × 86 × 202 | 52224, -60, 0 | 3,688 | 2,856,431 | 0 | 5,249 | east-gate-warren.bare.bin.gz (31 KB) |
| kidron-bene-hezir.bare | 0.25 m | 284 × 112 × 444 | 53248, -60, 0 | 23,407 | 7,792,586 | 0 | 40,468 | kidron-bene-hezir.bare.bin.gz (236 KB) |
| kidron-bene-hezir@avigad.bare | 0.25 m | 284 × 112 × 444 | 54272, -60, 0 | 23,767 | 7,792,461 | 0 | 41,515 | kidron-bene-hezir@avigad.bare.bin.gz (242 KB) |
| temple-great-sea.bare | 0.5 m | 142 × 32 × 170 | 55296, -60, 0 | 703 | 633,610 | 0 | 3,301 | temple-great-sea.bare.bin.gz (16 KB) |
| qumran-settlement.bare | 0.5 m | 250 × 17 × 402 | 56320, -60, 0 | 3,179 | 1,413,716 | 0 | 11,066 | qumran-settlement.bare.bin.gz (55 KB) |
| qumran-settlement~ring1.bare | 1 m | 608 × 111 × 608 | 57344, -60, 0 | 60,383 | 14,620,949 | 0 | 86,816 | qumran-settlement~ring1.bare.bin.gz (543 KB) |
| qumran-settlement~ring2.bare | 8 m | 288 × 42 × 288 | 58368, -60, 0 | 11,922 | 785,951 | 0 | 35,297 | qumran-settlement~ring2.bare.bin.gz (204 KB) |
| jericho-early~ring1.bare | 1 m | 608 × 47 × 608 | 59392, -60, 0 | 29,898 | 7,941,592 | 0 | 46,239 | jericho-early~ring1.bare.bin.gz (290 KB) |
| jericho-early~ring2.bare | 8 m | 288 × 30 × 288 | 60416, -60, 0 | 10,536 | 463,069 | 0 | 31,696 | jericho-early~ring2.bare.bin.gz (175 KB) |
| jericho-late~ring1.bare | 1 m | 608 × 47 × 608 | 61440, -60, 0 | 29,898 | 7,941,592 | 0 | 46,239 | jericho-late~ring1.bare.bin.gz (290 KB) |
| jericho-late~ring2.bare | 8 m | 288 × 30 × 288 | 62464, -60, 0 | 10,536 | 463,069 | 0 | 31,696 | jericho-late~ring2.bare.bin.gz (175 KB) |
| gerizim-precinct~ring1.bare | 1 m | 608 × 153 × 608 | 63488, -60, 0 | 51,986 | 27,357,977 | 0 | 73,456 | gerizim-precinct~ring1.bare.bin.gz (483 KB) |
| gerizim-precinct~ring2.bare | 8 m | 288 × 48 × 288 | 64512, -60, 0 | 18,682 | 1,641,944 | 0 | 56,750 | gerizim-precinct~ring2.bare.bin.gz (337 KB) |
| hyrcania-waterworks~ring1.bare | 1 m | 608 × 166 × 608 | 65536, -60, 0 | 97,329 | 25,149,700 | 0 | 145,485 | hyrcania-waterworks~ring1.bare.bin.gz (926 KB) |
| hyrcania-waterworks~ring2.bare | 8 m | 288 × 38 × 288 | 66560, -60, 0 | 18,670 | 806,779 | 0 | 56,687 | hyrcania-waterworks~ring2.bare.bin.gz (322 KB) |
| bethesda-pools~ring1.bare | 1 m | 608 × 91 × 608 | 67584, -60, 0 | 40,736 | 20,439,786 | 0 | 56,314 | bethesda-pools~ring1.bare.bin.gz (359 KB) |
| bethesda-pools~ring2.bare | 8 m | 288 × 24 × 288 | 68608, -60, 0 | 11,278 | 940,697 | 0 | 31,940 | bethesda-pools~ring2.bare.bin.gz (181 KB) |
| east-gate-warren~ring1.bare | 1 m | 608 × 90 × 608 | 69632, -60, 0 | 41,162 | 18,025,397 | 0 | 56,008 | east-gate-warren~ring1.bare.bin.gz (350 KB) |
| east-gate-warren~ring2.bare | 8 m | 288 × 26 × 288 | 70656, -60, 0 | 11,882 | 1,048,633 | 0 | 34,840 | east-gate-warren~ring2.bare.bin.gz (200 KB) |
| kidron-bene-hezir~ring1.bare | 1 m | 608 × 125 × 608 | 71680, -60, 0 | 69,126 | 23,158,731 | 0 | 94,809 | kidron-bene-hezir~ring1.bare.bin.gz (587 KB) |
| kidron-bene-hezir~ring2.bare | 8 m | 288 × 27 × 288 | 72704, -60, 0 | 13,520 | 1,027,149 | 0 | 40,874 | kidron-bene-hezir~ring2.bare.bin.gz (236 KB) |
| temple-great-sea~ring1.bare | 1 m | 608 × 97 × 608 | 73728, -60, 0 | 37,284 | 24,696,409 | 0 | 50,486 | temple-great-sea~ring1.bare.bin.gz (319 KB) |
| temple-great-sea~ring2.bare | 8 m | 288 × 27 × 288 | 74752, -60, 0 | 12,117 | 1,074,872 | 0 | 34,972 | temple-great-sea~ring2.bare.bin.gz (202 KB) |

A name with `@` is a reconstruction view of that plan (the plain name is its **Remains** view); `~ring1` and `~ring2` are the terrain rings; `.bare` is the Ancient ground view of the build it follows. "Units" are the source-relative units of those scenes. Every air block next to a drawn face has saved sky light; sections without saved light are open sky or solid rock. The Qumran build is fitted to the Kh. Qumran terrain patch; at Wadi Qumran the atlas keeps the smooth model.

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
- Third pass: the three Kidron builds that hold the monuments (the fine build, its original-state view and the inner ring) carry their new detail and the corrected ground at their feet. The other 25 builds read back unchanged.

## Later still on 22 October 2026: six more settings, Kidron levels from Fig. 25

- The other models drawn in metres now stand in their mapped surroundings ([record](../site_models_2026-10-22.md#mapped-surroundings-for-six-more-sites)). `jericho-early`, `jericho-late`, `gerizim-precinct`, `hyrcania-waterworks`, `bethesda-pools`, `east-gate-warren` and the traced `qumran-settlement` get the same rings as the Kidron and the Great Sea: 1 m blocks to ±304 m with the mapped surroundings, then 8 m blocks of terrain to ±1,152 m. Qumran's rings were 2 m and 8 m before. Their own builds now sit in the wide terrain, so they are larger than before. 40 builds in all.
- The Kidron builds carry the levels read from Avigad's Fig. 25 elevation ([record](../site_models_2026-10-22.md#surroundings-and-registration)): Absalom's podium and parts, the Jehoshaphat sill and steps, Zechariah's visible foot and heights, the higher court walls, the ground climbing in front of the scarp and two scarp openings. The four Kidron builds were rebuilt alone after the full run, and their region files (x 18,432–19,967 and 36,864–38,399) were copied into the full run's save. A re-read of the merged save gives byte-identical atlas files for the Kidron builds and for their neighbours (the Golden Gate and the Great Sea). The outer Kidron ring did not change.
- All 40 builds read back with no mismatches.

## Night of 22 October 2026: models placed by satellite imagery

- Gerizim, Jericho (both), Hyrcania and the Qumran settlement were moved to where their plans, registered to satellite imagery, put them ([record](../site_models_2026-10-22.md#placed-by-satellite-imagery-night-of-22-october)). Their 20 builds (views and rings) were rebuilt alone and their world strips copied into the full save; a re-read of the merged save gives byte-identical atlas files for them and their neighbours.
- Hyrcania now spreads round its hill (about 110 m of relief) and is built in 0.5 m blocks: at 0.25 m it would need 1,172 × 450 × 960 blocks, beyond one strip and the height limit.
- All 40 builds read back with no mismatches.

## Bare builds for the Ancient ground view — night of 22 October 2026

- The atlas's **Ancient ground** view draws a plan in its mapped setting without today's mapped features. The block builds hold those features, so until now that view was drawn smooth.
- Each plan in a mapped setting now has bare builds: every view and both rings built again from the model without the mapped surroundings. They have no graves, walls, buildings, trees, roads, paving or green ground. Their ground is today's terrain.
- When the plan's Ancient ground entry gives published levels (`ground: 'published'` in `atlas/app/atlas-ancient-ground.ts`), its pads are built in too. Qumran's entry does: its bare builds carry one pad at −324.54 m, the median of Magen & Peleg's published room and court levels. A bare build records the pads it was built with. The atlas uses it only while they match the view's, and the check fails when they differ.
- Names add `.bare` to the build they stand for: `kidron-bene-hezir.bare`, `kidron-bene-hezir@avigad.bare`, `kidron-bene-hezir~ring1.bare`. In `index.json` each has `bare: true`, `normalBuild` and `pads`, and a bare near build lists its bare rings. The rings leave the same holes as the normal rings.
- The bare builds take the world strips after all the others, from strip 40 (x = 40,960), in the same order as the normal builds. No other build moves. There are 34: 16 views and 18 rings of the nine plans.
- In the atlas, **Ancient ground** with **Blocks** draws the bare build of the current view and its rings. Where a view has no bare build, it is drawn smooth, as before, and the caption says so. **Today** keeps the normal builds.
- All 34 are built (table above). The Great Sea's three were first built in a test run of that plan alone, whose normal builds came out byte-identical to the files already in the atlas; then all 34 were built together with the Qumran settlement's three normal builds, rebuilt because its ground is now the published level. Their world strips were copied into the full save, and a re-read of the whole save gives byte-identical files for all 74 builds, with no mismatches.
- Check: `check-minecraft.mjs` decodes every bare build and finds no block of today's setting (codes 8–11). Outside the model's own footprint (its parts seen from above, one block wider), a bare build may show only soil and rock; the normal build shows today's features there. For the Great Sea, 73 % of the block area is outside the footprint; there the normal build has 10,468 faces of today's features and the bare build none. Each ring's hole is checked against the build inside it. Bare builds not built yet are listed; `--require-bare` makes them a failure.

## The world save

[`copper-scroll-sites-26.3.zip`](copper-scroll-sites-26.3.zip) (41.7 MB, rebuilt on the night of 22 October 2026 with the 40 normal builds, including the Qumran settlement on its published level; it does not hold the bare builds, whose region files r.80–r.147 are left out) is the saved world, SHA-256 `25d6d7a31fd09f36b71a7acc17ae1a1494432f66fe7635a718f29ac593e35f2f`. Unzip the `world` folder into a Minecraft Java 26.3 `saves` folder (or a server folder) to walk the builds. The world is a void with creative mode as the default; the spawn is in front of the Qumran tunnel mouth (188, -23, 163). Each build starts at its origin in the table; a plan's views stand side by side, 1,024 blocks apart. In Minecraft's own scale the player is two to four times life size, because one block is 0.5 or 0.25.

## Rebuild

```sh
cd atlas
node scripts/minecraft/build-world.mjs --jar <server.jar> --java <Java 25> --work <empty folder>
node scripts/check-minecraft.mjs
```

The bare builds alone:

```sh
node scripts/minecraft/build-world.mjs --jar <server.jar> --java <Java 25> --work <empty folder> --bare-only
node scripts/check-minecraft.mjs --require-bare
```

`--sites` takes build names or plan ids; a plan id selects its normal and bare builds, and `--bare-only` keeps only the bare ones. A partial run saves a fresh world with only its own strips. Strip n is region files x = 2n and 2n + 1; copy those into the full save, not the neighbouring region files that the server touches. `--skip-server` re-reads an existing save. A rebuild from unchanged models gives the same blocks; the same save gives byte-identical atlas files.
