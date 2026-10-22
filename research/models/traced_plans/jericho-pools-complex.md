# Jericho Pools Complex: traced plan record

Traced on 20 October 2026. Data: [jericho-pools-complex.json](jericho-pools-complex.json), format [SCHEMA.md](SCHEMA.md). The tracing shows what the figures draw. It identifies no Copper Scroll feature and tests no entry.

## Sources

| Id | Source | Use |
|---|---|---|
| netzer2001-plan17 | Netzer 2001, Vol. I, Plan 17, p. 93 (Stage 3) | `stage3` layer |
| netzer2001-plan20 | Netzer 2001, Vol. I, Plan 20, p. 97 (Stage 6) | `stage6` layer; reference figure for the frame |
| netzer2001-plan22 | Netzer 2001, Vol. I, Plan 22, p. 99 (Herodian period) | `herodian` layer |
| trumper2018-fig18 | Trümper 2018, Fig. 18, p. 281 (overview, after Netzer 2001 p. 6 fig. 8) | East ends of the two pools only |
| trumper2018-fig20, -fig22 | Trümper 2018, Figs. 20 and 22, pp. 284, 286 (= Plans 17 and 20) | Label reading; check overlays; CC BY-NC 3.0 |
| netzer2001-text | Netzer 2001, Vol. I, pp. 73–89, 93–98, 100 ([cycle14 extract](../../assets/plans/netzer2001-cycle14/README.md)) | Published sizes, levels and find status |

All six figures are already in `research/assets/plans/`. The text extract is also in the repository. It was not on the task list, but no rule excludes it. I read pp. 74, 75, 79, 85 and 100 as page images; the other pages I read through the text layer. The early-pool and joined-basin sizes also come from the existing records: [kotar-netzer1983.md](../../assessments/entry29_jericho_pools/kotar-netzer1983.md) (1983 pp. 100–101, 105–106), [README.md](../../assessments/entry29_jericho_pools/README.md) (1989 p. 279, p. 281 n. 19) and [netzer2001-first-pass.md](../../assessments/entry29_jericho_pools/netzer2001-first-pass.md) (2001 p. 74, p. 347 n. 2).

I did not open the Netzer front matter, Drive "PROTECTED" folders, or any record north of Tell es-Sultan. According to its manifest, the illustrated-volume extract (pp. 69–72) shows only Qarantal and Cypros. Thus no isometric view, elevation or height for the Pools Complex was found in it.

## Frame and transforms

- Units are metres, with x east and z south. The origin is the outer north-west corner of the northern pool as Plan 20 draws it. At that point the outer face of the shared west wall meets the outer face of the north wall.
- North comes from the Netzer plans. Their north arrows point to the right. The frame north is the normal to the drawn outer west face of the pools, which is 0.14° from the image axis in Plan 20. No source says whether this is grid north or true north. No geographic coordinates are given. *(22 October 2026: registered to imagery through Fig. 18, the frame north lies about 10.6° anticlockwise of true north; the frame's origin is at (−183.2, −239.1) m from the `jericho_palaces` anchor; [record](../../assets/plans/imagery-registration-2026-10-22/jericho.json).)*
- Levels use the Netzer site datum (for example, the pool tops are ca. +100.40, p. 79). The inspected pages do not give the benchmark. `ground` = 100.47 is the median of ten printed Plaza floor levels (100.27–100.87).
- Plan 20 is scaled by its own bar: 0 m at px 352.6 and 10 m at px 551.3, which gives 19.87 px/m.
- Each other figure is registered with a similarity fit (scale, rotation and shift) to pool corners that it shares with Plan 20. The full coefficients are in `sources[].transform`.

| Figure | Control points | rms / max residual | Fitted vs bar scale (px/m) |
|---|---|---|---|
| Plan 17 | 16 | 0.014 / 0.024 m | 19.81 / 19.75 |
| Plan 22 | 4 | 0.052 / 0.073 m | 19.92 / 20.3 (faint bar) |
| Fig. 20 | 16 | 0.021 / 0.033 m | 17.27 / 17.35 |
| Fig. 22 | 16 | 0.033 / 0.061 m | 17.32 / 17.25 |
| Fig. 18 | 4 (outer west corners) | 0.21 / 0.28 m (1 px = 0.24 m) | 4.16 / 4.22 |

Independent checks (not used in any fit):
- The 13 column circles north of the Plaza agree within 0.1 m between Plans 17 and 20.
- The W257 line (Plan 17) agrees within 0.15 m with the Stage 6 column row that replaced it (Plan 20).
- W325 and W247 agree within 0.1 m.
- The W1112 and W1113 segments traced on Plan 22 fall within 0.04–0.13 m of their Plan 20 positions.
- The pools in Fig. 18 are rotated 2.6° from the Netzer plans. The frame follows Netzer.

## Size checks

| Item | Traced | Published | Difference |
|---|---|---|---|
| Each early pool, inner face at wall base | 17.6–17.9 × 12.8–13.0 m | about 18 × 13 m (1983 p. 101; 2001 p. 347 n. 2) | −0.1 to −0.4 / −0.03 to −0.21 m |
| Joined basin, south to north | 31.89 m | ca. 32 m (2001 p. 74; 1989 n. 19) | −0.11 m |
| Joined basin, east to west | 17.4–18.1 m (wall base); 18.1–18.8 m (bench edge) | ca. 18 m; 18.3 m (1989) | −0.6 to +0.8 m |
| Strip between the pools (outer faces) | 3.65 m | about 4 m (1983 p. 101) | −0.35 m |
| South wall of the southern pool | lines at 1.30 / 1.70 / 2.05 m | 1.7 m top incl. bench, 2.0 m base (pp. 74–75) | ≤0.05 m |
| Stair flights, width | 2.36–2.62 m | 2.3 m (p. 75) | +0.06 to +0.32 m |

The north–south sizes are measured on the plans. The east–west sizes depend on the Fig. 18 east ends (±0.3 m).

Depth: the rim is +100.40 (p. 79) and the floors are 97.00 (south) and 96.26 (north), which gives 3.40 m and 4.14 m. On p. 74, the debris is ca. 1.5 m high and ca. 2 m below the top, which gives about 3.5 m. The "3.5 m deep" in [sequence_model_followup](../../text/sequence_model_followup_2026-09-30.md) came from web summaries. It agrees only with the southern pool.

## Layers

- **remains** (19 elements, `status: observed`): only features that the text says were found:
  - the joined pool A(B)101, its west, south, north and two east walls, the central podium, and both stair flights (pp. 74–76);
  - W257 (p. 87) and W247 (pp. 76–77);
  - the platform and the minor channel at +100.40 / +100.23 (pp. 80–81);
  - A(B)99 and its two channels, "preserved along almost their entire lengths" (pp. 83–84);
  - A(B)215 (p. 94), and W43 and W57 (p. 85).

  The geometry still comes from the schematic plans. The layer also has four spot levels: the floors 97.00 and 96.26, and the outer wall-top corners 100.44 and 100.45.
- **stage3** (59 elements, Plan 17): the two pools, with nested outlines, walls, floors and stairs (11 and 10 treads); the Na'aran conduit and its 6.86 m northward jog (6.8 m on p. 78); the platform; the drain to A(B)215; the Buried Palace corner (A(B)209 at 99.08, A(B)34, A(B)66, A(B)67, W35, W41, W42, W63–W68); W325, W1088, W247, W257, W777; the Western Garden area; and 19 column bases.
- **stage6** (104 elements, Plan 20):
  - the two pools, still separate;
  - the bath block: A(B)64, A(B)79, A(B)138, AB70, A(B)125 with its steps, two small basins and room A(B)131;
  - rooms A(B)42, A(B)43, A(B)95 and A(B)132;
  - the settling tanks A(B)217 and A(B)99 and their channels;
  - the dismantled Stage 5 conduit (dashed);
  - the Grand Bypass (approximate centre line);
  - the curved wall W1112 and walls W1104, W1111 and W1113;
  - 30 column bases.

  Every room carries its printed floor level.
- **herodian** (18 elements, Plan 22 and text):
  - the joined pool A(B)101 (floor outline plus a `benchEdgePlan22` outline), its walls, the podium and both flights;
  - W43, W57 and the channel on them (p. 85, p. 100);
  - the winepress A(B)58 (p. 100);
  - three context walls that Plan 22 draws. Their notes warn that p. 100 says no Western Garden structure existed in Herod's day.

- Integrator change (20 October 2026): in `stage3` and `stage6`, the two pool outlines and the pools' outer walls (west walls, south wall of the southern pool, north wall of the northern pool) have `status: observed`. They are the walls that p. 74 reports surviving almost to their full height, and the floors carry levels from Plan 17. The dividing walls, the east ends and everything else in those layers stay `published-reconstruction`. In the atlas, a reconstruction view draws only the latter in the pale restored surface. The joined pool's two east wall segments are split: in `remains` they rise from the pool floors with no traced height (p. 74: not preserved to the original height); in `herodian`, copies with `-herodian` ids reach the pool tops (+100.40, p. 79) as `published-reconstruction`.

## Assumptions

1. Each pool side is drawn as four nested lines. I read them as the outer face, the inner edge of the wall top, the bench edge and the inner face at the wall base. The line offsets match the published 1.5 m base, 1.2 m top and 0.4 m bench, and 2.0 m and 1.7 m for the southern wall (p. 74). The pool polygon is the wall-base line (the floor outline). The other three lines are in `outlines`.
2. Plans 17, 20 and 22 crop the pools at their west ends. The outer east faces come from Fig. 18. The inner east lines are set 0.8, 1.2 and 1.5 m inside them, from the published thicknesses.
3. For the joined basin, the west, south and north walls use the Plan 20 lines of the same walls. p. 74 says these walls survived almost to their full height. No figure draws the east side across the former strip, so the polygon joins the two east segments across it.
4. The two east–west lines that Plan 22 draws at the inner faces of the old divider are read as the central podium (p. 74). This identification is mine.
5. Floor 96.26 comes from Plan 17, where it is clear. Plan 20 and the Trümper copies are blurred and could read 95.26 or 99.26. For the joined basin, use 96.26 north of the podium and 97.00 south of it. No Herodian floor level is legible.
6. `lineStyle` records only the drawing. I found no Netzer legend that separates found lines from restored lines. Captions say "partly reconstructed", and p. 100 says "schematic". Where the text says that a drawn feature is missing or hypothetical, the note cites the text: the conduit between the pools (p. 78), the drain to A(B)215 (p. 94), the channel from A(B)217 (pp. 83–84) and the Stage 5 conduit (p. 97).
7. No wall height or column height is published. Those elements have `height.basis: "illustrative"` with value null. Pool walls carry the published top (100.40) and the floor level; their height is the difference between the two.
8. The labels W324 and W327 are blurred in Plan 20, so I read them on Fig. 22. In Plan 22 all labels and levels are illegible. Herodian names come from the text.
9. Column radii are the drawn symbol radii.

## Not traced

- The Fortified Palace area in the upper left of Plans 20 and 22.
- Plans 18, 19 and 21 (Stages 4, 5 and 7).
- Area AC (Fig. 19).
- The dashed stylobate lines along the column rows.
- The partitions in the winepress vats.
- The Herodian flowerpot rows (p. 85), which are not legible on Plan 22.
- The east part of W43: p. 85 says it runs along the whole south side of the joined pool, but Plan 22 is cropped at 6.7 m.
- A Herodian inlet: the supply is unknown (p. 84).
- The detailed folded Plans 14, 15 and 23 are missing from both known copies.

## Stage 6 figure and the joined basin

Fig. 22 is Netzer Plan 20, Stage 6 (Trümper phase 6, 67–63 BCE). It draws **two separate pools** with the strip between them. In Stage 6 the main conduit stopped passing through that strip (p. 97), and two channels from A(B)99 fed the pools separately (p. 84). The joining is Herodian: it is linked to Herod's Second Palace (p. 85) and comes after the 31 BCE earthquake (p. 100), and it is drawn in Plan 22.

Thus the atlas plan `jericho-late`, which shows Fig. 22 with the "Joined basin" model, is **not correct**:
- Pair the joined basin with the `herodian` layer (Plan 22 and p. 74).
- Show Fig. 22 as the Stage 6 state of the two separate pools.
- Replace the illustrative depth of 2.5 m with the published rim and floor levels (3.40 m and 4.14 m).

## Licence

- Overlays on the Netzer plans are derived from IES-copyright scans (a research extract that the user authorized). Check before any public reuse.
- Overlays on the Trümper figures are CC BY-NC 3.0, with attribution to Trümper and Netzer.
