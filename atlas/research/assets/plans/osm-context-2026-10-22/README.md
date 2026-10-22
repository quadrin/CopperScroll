# OpenStreetMap context around two atlas models — 22 October 2026

Data © OpenStreetMap contributors, under the Open Database License (ODbL) 1.0 (https://www.openstreetmap.org/copyright). These files are extracts of that database. Any reuse must keep this attribution and the ODbL terms.

Source: one OSM API 0.6 map call, bbox 35.2330,31.7715,35.2460,31.7825 (lon/lat, west/south/east/north), retrieved 22 October 2026 (generator `openstreetmap-cgimap 2.1.0`). The downloaded file (SHA-256 `c2f788b6f353…`, 4.4 MB) is not kept; its hash is in each record. Made by [`tools/build_osm_context.py`](../../../../tools/build_osm_context.py). Mirror: `atlas/research/assets/plans/osm-context-2026-10-22/`.

Files:

- `kidron.json`: 496 elements for `kidron-bene-hezir` (place `jer_kidron_mon`): every way classified as context with a vertex within 450 m of (−35, 5) m, plus the outlines of Bene Ḥezir (w288284732), Zechariah (w288284733) and Absalom (w137729556). Context kinds: 216 buildings, 54 cemetery areas, 6 gate buildings, 152 paths, 17 retaining walls, 41 stairs, 7 city walls.
- `great-sea.json`: 695 elements for `temple-great-sea` (place `jer_temple`): context within 400 m of (30, 60) m, plus the Haram's south-west (node 29979854) and south-east (node 2915691228) corners from relation 5862584 (Temple Mount). Context kinds: 400 buildings, 6 cemetery areas, 15 gate buildings, 193 paths, 17 retaining walls, 54 stairs, 8 city walls.

Each element keeps its OSM id, version, timestamp, tags and lat/lon. Each record also holds the registration below. The atlas copy with the coordinates projected to the place frame (metres, x east, z south, the MapLibre Mercator frame at the place anchor) is `atlas/app/atlas-site-context.json`.

What the data are and are not:

- They are today's mapped streets, stairs, cemetery areas, walls and buildings. The atlas draws them as the modern setting of the two models. They are not evidence for any ancient feature, level or route.
- Tunnels, bridges, indoor and below-ground ways are left out, because the atlas drapes context on the terrain surface.
- Graves are not mapped one by one. The atlas fills the mapped cemetery areas with an illustrative grid of graves.

## Registration (INFERENCE)

**Kidron.** Avigad's frame for Bene Ḥezir is placed on the centroid of the mapped tomb outline (his porch centre, 2.1 m east of the façade) and turned so that his "west" is the façade normal, 244.8°. That bearing is the mean of the normal to the outline's long sides (244.3°) and the bearing that puts Zechariah's mapped centre where Avigad's plan puts it (245.3°). Absalom stands at its mapped centre, 52.1 m from the porch (Avigad: about 50 m, p. 37), with its sides turned with its outline (4.8°). The model's rock path is the modern terrain at Absalom's centre. Avigad's "south-west" (p. 37) is a rounded direction; 244.8° falls within it.

**Great Sea.** The Haram's south-west and south-east corners were measured on Warren 1884 Pl. VII (line fits on the 600 ppi mask: (2471.1, 2161.2) and (4616.5, 2145.5) px; [plate record](../warren1884-plate-vii/README.md)). On the plate they are 278.9 m apart and the wall runs at 80.75°; mapped, 281.0 m and 80.58°. The plate frame is turned 0.17° and moved so that the midpoints coincide: each corner then lies 1.07 m from its mapped place. This puts the traced cistern under the court between the Dome platform and the north front of al-Aqsa, where the plate draws it. The outline keeps its own uncertainty of about ±2 m.
