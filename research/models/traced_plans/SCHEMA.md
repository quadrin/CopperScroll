# Traced plans: shared format

A traced plan turns one or more published figures into metric geometry that the atlas can build in 3D (smooth and Minecraft). One JSON file per site, `<id>.json`, in this folder. The tracing records what the source draws; it adds nothing. Every element keeps its source locator and its status.

## Frame

```json
"frame": {
  "units": "metres",
  "x": "east", "z": "south",
  "origin": "what point (0, 0) is, in words",
  "north": "how north was set: the figure's north arrow (grid or true not stated) / other",
  "datum": "name of the vertical datum of published levels, or null",
  "ground": 100.4,
  "groundBasis": "how the general walking surface level was chosen, e.g. median of published floor spot levels"
}
```

Plan pixels map to the frame by the figure's own scale bar and north arrow. Record the transform in `sources[].transform` so that anyone can redo it.

## Sources

```json
"sources": [{
  "id": "netzer2001-plan17",
  "citation": "Netzer 2001 Vol. I, Plan 17, printed p. 93",
  "asset": "research/assets/plans/netzer2001/netzer2001-vol1-plan17-p93.jpg",
  "licence": "as in the asset manifest",
  "scaleBar": {"px": [[x0, y0], [x1, y1]], "metres": 10},
  "northArrowPx": [[x0, y0], [x1, y1]],
  "transform": "frame = R(theta) * (px - p0) / pxPerMetre, theta = ..., p0 = ...",
  "residual": "check of the transform against an independent dimension, e.g. a published pool length"
}]
```

## Layers

```json
"layers": [
  {"id": "remains", "label": "Excavated remains", "kind": "observed"},
  {"id": "stage3", "label": "Stage 3 (103–76 BCE), after Netzer Plan 17", "kind": "published-reconstruction", "sources": ["netzer2001-plan17"]}
]
```

`remains` holds only what an excavation report or plan shows as found. A phase layer holds what a published reconstruction draws for that phase. An element can belong to several layers.

## Elements

```json
{
  "id": "W325", "label": "Wall W325",
  "kind": "wall | pool | cistern | steps | column | channel | room | platform | garden | path | cliff-edge",
  "layers": ["stage3", "stage6"],
  "status": "observed | published-reconstruction | project-inference",
  "lineStyle": "solid | dashed | double | hatched | filled",
  "geometry": {"type": "polyline", "points": [[x, z], ...], "closed": false, "width": 0.9},
  "levels": {"top": null, "bottom": null, "floor": 99.08, "rim": null, "source": "Plan 17 spot level 99.08 at A(B)209"},
  "height": {"value": null, "basis": "unknown | published | illustrative"},
  "steps": {"count": null, "down": "n | s | e | w", "pool": "id of the pool whose floor the flight reaches, when it is not drawn inside it"},
  "source": "netzer2001-plan17", "locator": "Plan 17 p. 93",
  "note": "anything the builder or a reader must know"
}
```

Geometry types:
- `polyline` with `width` (walls, channels): centre line in metres.
- `polygon` (pools, rooms, platforms, steps): outline in metres, counter-clockwise or clockwise.
- `point` with `radius` (columns, round cisterns, shafts).
- `raster` for walls traced from a filled drawing: `{"type": "raster", "cell": 0.25, "origin": [x, z], "cols": W, "rows": H, "rle": "<run lengths, alternating 0/1, starting with 0, row by row from origin, rows along +z>"}`.

Levels are absolute in the frame's datum when published, else null. Never invent a level; use `height.basis: "illustrative"` and say so in `note`.

## Verification

```json
"verification": {
  "overlays": ["research/models/traced_plans/<id>-overlay-<source>.png"],
  "checks": ["pool A: traced 18.1 × 13.0 m against published about 18 × 13 m (Netzer 1983 p. 101)"],
  "limits": ["what the tracing cannot show"]
}
```

Each overlay draws the traced geometry over the source figure, so that a reader can see the fit.
