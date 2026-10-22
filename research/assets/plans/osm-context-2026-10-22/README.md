# OpenStreetMap context around eight atlas models — 22 October 2026

Data © OpenStreetMap contributors, under the Open Database License (ODbL) 1.0 (https://www.openstreetmap.org/copyright). These files are extracts of that database. Any reuse must keep this attribution and the ODbL terms.

Source: one OSM API 0.6 map call, bbox 35.2330,31.7715,35.2460,31.7825 (lon/lat, west/south/east/north), retrieved 22 October 2026 (generator `openstreetmap-cgimap 2.1.0`). The downloaded file (SHA-256 `c2f788b6f353…`, 4.4 MB) is not kept; its hash is in each record. Made by [`tools/build_osm_context.py`](../../../../tools/build_osm_context.py). Mirror: `atlas/research/assets/plans/osm-context-2026-10-22/`.

Files:

- `kidron.json`: 758 elements for `kidron-bene-hezir` (place `jer_kidron_mon`): every way classified as context, and every mapped single tree, within 450 m of (−35, 5) m, plus the outlines of Bene Ḥezir (w288284732), Zechariah (w288284733) and Absalom (w137729556). Context kinds: 216 buildings, 54 cemetery areas, 55 green areas (woods, orchards, grass), 6 gate buildings, 152 paths, 65 roads, 17 retaining walls, 41 stairs, 142 trees, 7 city walls.
- `great-sea.json`: 945 elements for `temple-great-sea` (place `jer_temple`): context within 400 m of (30, 60) m, plus the Haram's south-west (node 29979854) and south-east (node 2915691228) corners from relation 5862584 (Temple Mount). Context kinds: 400 buildings, 6 cemetery areas, 66 green areas, 15 gate buildings, 193 paths, 30 roads, 17 retaining walls, 54 stairs, 154 trees, 8 city walls.
- Roads, trees and green areas were added later the same day from the same download.

Six more records were made later the same day from five more API 0.6 map calls (same date, same generator):

| Record | Plans | Download bbox (lon/lat) | Elements | Placement |
|---|---|---|---|---|
| `qumran.json` | `qumran-settlement` | 35.4510,31.7360,35.4680,31.7480 | 39 | the traced frame's centre on the area centroid of way 611895589 ("Qumran", archaeological site, 99.7 × 142.8 m) |
| `bethesda.json` | `bethesda-pools` | 35.2290,31.7740,35.2460,31.7880 | 1,306 | the dam on the area centroid of way 126864878 ("Pool of Bethesda", 82.6 × 51.6 m) |
| `golden-gate.json` | `east-gate-warren` | same as Bethesda | 883 | the gatehouse centre on the area centroid of way 291836693 (Golden Gate building, 27 × 17 m); turned 5.5° so the gatehouse runs along its long sides (bearing 84.5°) |
| `jericho.json` | `jericho-early`, `jericho-late` | 35.4280,31.8460,35.4450,31.8580 | 44 | none: the models stay at the place anchor (about ±300 m) |
| `gerizim.json` | `gerizim-precinct` | 35.2640,32.1950,35.2830,32.2070 | 116 | none: at the place anchor on the summit |
| `hyrcania.json` | `hyrcania-waterworks` | 35.3570,31.7130,35.3750,31.7250 | 12 | none: at the place anchor (about ±200 m), unturned (the source has no north arrow) |

Feature lists for the atlas are in `atlas/public/context/<record>.json`; `atlas/app/atlas-site-context.json` keeps each plan's placement. The five relative-unit models (`qumran-ilan`, `qumran-reeder`, `jericho-ac`, `siloam-receiver`, `doq-waterworks`) and the unlocated `abu-saraj-iv17` get no mapped surroundings: they are not drawn at a known scale, or have no position.

Each element keeps its OSM id, version, timestamp, tags and lat/lon. Each record also holds the registration below. The atlas copy with the coordinates projected to the place frame (metres, x east, z south, the MapLibre Mercator frame at the place anchor) is `atlas/app/atlas-site-context.json`.

What the data are and are not:

- They are today's mapped streets, roads, stairs, cemetery areas, walls, buildings, trees, woods, orchards and grass. The atlas draws them as the modern setting of the two models. They are not evidence for any ancient feature, level or route.
- Tunnels, bridges, indoor and below-ground ways are left out, because the atlas drapes context on the terrain surface.
- Graves are not mapped one by one. The atlas fills the mapped cemetery areas with an illustrative grid of graves. Woods and orchards are filled the same way with trees about 7 m apart; only the single trees are mapped trees.

## Registration and placement (INFERENCE)

**Kidron.** Avigad's frame for Bene Ḥezir is placed on the centroid of the mapped tomb outline (his porch centre, 2.1 m east of the façade) and turned so that his "west" is the façade normal, 244.8°. That bearing is the mean of the normal to the outline's long sides (244.3°) and the bearing that puts Zechariah's mapped centre where Avigad's plan puts it (245.3°). Absalom stands at its mapped centre, 52.1 m from the porch (Avigad: about 50 m, p. 37), with its sides turned with its outline (4.8°). The model's rock path is the modern terrain at Absalom's centre. Avigad's "south-west" (p. 37) is a rounded direction; 244.8° falls within it.

**Great Sea.** The Haram's south-west and south-east corners were measured on Warren 1884 Pl. VII (line fits on the 600 ppi mask: (2471.1, 2161.2) and (4616.5, 2145.5) px; [plate record](../warren1884-plate-vii/README.md)). On the plate they are 278.9 m apart and the wall runs at 80.75°; mapped, 281.0 m and 80.58°. The plate frame is turned 0.17° and moved so that the midpoints coincide: each corner then lies 1.07 m from its mapped place. This puts the traced cistern under the court between the Dome platform and the north front of al-Aqsa, where the plate draws it. The outline keeps its own uncertainty of about ±2 m.

**Qumran, Bethesda, Golden Gate.** A chosen model point is put on the area centroid of one mapped outline. For Qumran and Bethesda the model is not turned, so its bearing stays the source's; the outline is larger than any single feature, so the position is good to some tens of metres (Qumran) or about 25 m (Bethesda). The Golden Gate fits closely: Warren's gatehouse (24.8 × 17.3 m) and the mapped building (27 × 17 m) differ by 2 m in length, and the turn from the building's long sides (5.5°) agrees with the bearing of the city wall beside it (about 6°).

**Jericho, Gerizim, Hyrcania.** No mapped outline ties to a model point, so the models stay at their anchors and are drawn among the mapped surroundings without registration; no mapped feature is drawn inside their own ground.
