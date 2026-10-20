# Site models against reference photographs — 17 October 2026

Each walkable model was compared with the openly licensed photographs of its place ([site-photos-2026-10-17](../site-photos-2026-10-17/README.md)), from overhead and eye-level renders. Photographs guide appearance only. A change in geometry was made only where a published source supports it; other differences are listed for a later source check.

Applied to every model: base colours, masonry type and weathering derived from the photographs ([surface samples](surface-samples-2026-10-17/spec.json), built by `tools/build_site_surfaces.py`), and a reference-photo strip in walk mode.

## Kh. Qumran (qumran-ilan, qumran-reeder, Qumran pilot)

- Photographs: kh-qumran-l12-13, kh-qumran-l48, kh-qumran-pool-crack, kh-qumran-l110, wadi-qumran-kq2, wadi-qumran-caves-4-10, the existing outlet scene; historical kh-qumran-excavations-looking-west-1947-1961.
- Matches after the change: walls of irregular fieldstones (rubble), plastered pools and channels, pale marl ground, browner stone.
- Differences, not changed: the stepped pools, with the crack through L48–49's steps, and the round cistern L110 with its plastered feed channel appear in the photographs but lie outside the aqueduct models' plan frames. No photograph shows the cliff tunnels, the dam or the bend at point 16, so the photographs cannot check those parts.

## Mount Gerizim (gerizim-precinct)

- Photographs: gerizim-ovedc-c24, gerizim-yonger-2018, gerizim-fallaner-p305, gerizim-meronim-009, gerizim-deror-2205; historical gerizim-summit-ruins-c1900-1920.
- Matches after the change: large pale grey ashlar with fine joints and little weathering; brown earth in excavated rooms.
- Differences, not changed: the photographs show stone-paved courts and floors in the precinct (gerizim-ovedc-c24, gerizim-yonger-2018); the model's floors are earth. Paving needs a published plan of which surfaces were paved and in which phase. The photographs show the precinct as excavated and partly restored, so they cannot show which paving is Hellenistic.

## Hyrcania (hyrcania-waterworks)

- Photographs: hyrcania-c-hurkania-5011, hyrcania-c-hurkaniatop, hyrcania-ihm-east-stair-tunnel.
- **Changed:** the double pool is now drawn rock-cut with plastered faces instead of laid masonry. Support: Patrich 1989 p. 255 ("rock-cut double pool"); the photograph hyrcania-c-hurkania-5011 shows plastered rock walls. The coping course stays illustrative.
- Matches after the change: rubble summit walls, pale chalky rock, grey-brown ground.
- Differences, not changed: the reservoirs lie on a steep slope below the summit; the model sits on the feathered display bench used for every model. Slope geometry would need registered terrain or a published section.

## Doq (doq-waterworks)

- Photographs: doq-ihm-fortress-2 (masonry type only, at sunset), doq-deror-1190713 (cliff colour); the existing escarpment scene.
- Matches after the change: coursed squared stone for the enclosure wall; cliff and scree colours from the photograph.
- Differences, not changed: the cisterns are drawn as built round shafts; no reference photograph shows them. Stone and plaster keep the earlier palette because no ancient masonry was clean enough to sample.

## Siloam (siloam-receiver)

- Photographs: jer_siloam-steps-2017, jer_siloam-tunnel-outlet-2009, jer_siloam-tunnel-conduit-2021, the existing steps scene; historical Siloam views 1898–1946.
- Matches after the change: large squared limestone slabs.
- Differences, not changed: the photographs show the excavated pool as broad flights of steps, and the upper pool as a narrow basin between high modern walls. The model is a selected tracing of the receiving basin's relations (W1, L103, L102/L104, W3), and its wall heights are illustrative. Wall heights and step counts need the published sections.

## Jericho royal palaces (jericho-ac, jericho-early, jericho-late)

- Photographs: jericho-palaces-hasmonean-palace-2013, jericho-palaces-mikveh (both screened earlier: neither looks over the plain north of Jericho).
- Matches after the change: rough stone in rough courses; thick pale plaster on pools and steps.
- Differences, not changed: jericho-palaces-mikveh shows a mud-brick wall beside a plastered stepped pool; the models build all walls in stone. A mud-brick superstructure needs Netzer's published description of which walls were mud brick on stone foundations, per phase.

## Abu Saraj IV/17 (abu-saraj-iv17)

- Not compared. Photographs of IV/17 fall under the frozen Entry 25 rules and were not collected.

## New walkable models, 17 October 2026

Two places with reference photographs and published plans now have walkable models. Plan, model and photographs were compared after the build.

### Bethesda (bethesda-pools)

- Sources: Duprez 1970 pp. 33–41 and Pl. II; Gibson 2005 pp. 286–287 and 2011 pp. 22–28 (registration records `duprez1970_extracted.md`, `gibson2005_2011_bethesda_extracted.md`).
- Photographs: jer_bethesda-north-pool-2021, jer_bethesda-pools-dam-2021 (masonry colour and ashlar type), jer_bethesda-bw4-2010, jer_bethesda-site-2019, jer_bethesda-dzca-1101-2021; historical jer-bethesda-pool-1898-1914 and 1898-1946.
- Matches: squared ashlar faces; a long stair down into an excavated pool (north-pool-2021) agrees in kind with Gibson's steps along the southern pool's west side.
- Differences, not changed: the photographs show later walls, arches and vaults standing over and inside the pools (pools-dam-2021, bw4-2010, the historical views); the model omits Byzantine and Crusader structures. The photographs do not show the pools' full depth, the chimney or the eastern grottoes, so those parts follow the text only. Duprez reports rock in the lower parts of the faces; the model draws masonry throughout.

### Golden Gate (east-gate-warren)

- Sources: Warren 1884 Pl. VI, measured with its scale bar ([warren1884-plate-vi](../warren1884-plate-vi/README.md)); SWP Jerusalem pp. 141–145, 221.
- Photographs: jer_east_gate-exterior-2025-722 and jer_east_gate-exterior-cemetery-2014 (masonry colour and ashlar type); the other eight East Gate photographs were not used for geometry.
- Matches: very large squared blocks low on the outer face; a steep cemetery slope east of the wall; jer_east_gate-inside-2018-1 shows a sunken court in front of the gate's west facade, which agrees with the sill (2,396 ft) lying below the Haram surface (2,408 ft at cistern XV).
- Differences, not changed: the photographs show twin arched doorways, a crenellated top and a domed hall; the model draws the gatehouse as a closed block of illustrative height, because no published elevation was read. None of the photographs shows anything below the present surface, so the shaft, gallery, massive wall and cistern follow Warren only.

## Block builds and the Qumran dam, 20 October 2026

- **Changed (Qumran, qumran-ilan):** basin 2 and the dam proposed at point 4 are now drawn. Ilan & Amit 2002 Fig. 1 (p. 380) draws a heavy dashed line from point 3 to point 4 across the east side of basin 2, read as probably the dam (drawing only; [record](../../../sources/aqueducts2002_firsthand_2026-10-20/README.md)). The 1989 text reports no surviving dam (pp. 284, 288 n. 5), so the dam is copper, the colour for a published reconstruction. Basin depth and dam height and width are illustrative. The plan's dashed segment, earlier drawn as a copper channel, is now a `dam`.
- **Not changed:** Bethesda's lower faces. Duprez p. 33 says the dam is "built above and rock below" but gives no height for the change, so the model still draws masonry throughout.
- All models are also built in a Minecraft Java Edition server and read back block by block; the map shows those blocks by default ([record](../../../models/minecraft/README.md)). The blocks keep each model's sources and illustrative parts; rounding moves an edge or height by up to half a block.
