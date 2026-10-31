# Attribute inventory: schema (frozen before any source is keyed)

One row per **feature** that a source describes: a cave, chamber, cistern, pool, channel section, tomb, stair, doorway and so on. A feature that contains other features (a cave with a cistern inside it) gets its own row, and each contained feature gets a row that points to it.

Write one CSV per source and reader: `keyed/<source_id>_<reader>.csv`, UTF-8, with the header below in this order.

| Column | Content | Rules |
|---|---|---|
| `feature_id` | `<source_id>:<local id>` | Local id = the source's own label (cave "XI/3", locus "L91", site "37") plus a suffix for sub-features (`XI/3.a`). |
| `source_id` | From `sources.csv` | |
| `page` | Printed page(s) | As printed, e.g. `65` or `65-66` or `12*`. |
| `figure` | Figure or plan number(s) used | Blank if none. |
| `site_name` | Site or cave name as printed | |
| `grid_printed` | Grid reference exactly as printed | Do not convert. Blank if none. |
| `grid_system` | `OIG` (old Israel/Palestine grid), `NIG`/`ITM`, `UTM`, `latlon`, or `unknown` | |
| `position_basis` | `feature_grid`, `site_grid`, `plan`, `map_estimate`, `text_only` | Where the position comes from. |
| `feature_class` | One value from the class list below | |
| `class_as_printed` | The source's own word for it (≤ 5 words) | |
| `parent_id` | `feature_id` of the containing feature | Blank if none. |
| `length_m`, `width_m`, `height_m`, `depth_m`, `diameter_m` | Numbers in metres | As printed. Convert cm to m. Blank = not stated. A range goes in as `a-b`. |
| `dims_basis` | `text`, `plan_scaled`, `table` | `plan_scaled` only with a printed scale bar; say which figure. |
| `n_openings` | Integer | Count of entrances, openings or mouths the source states or shows on a scaled plan. Blank = not stated. |
| `opening_dirs` | Directions the openings face, e.g. `E;N` | 8-point compass. Only if the source states it or a plan with a north arrow shows it. |
| `n_steps` | Integer | Blank = not stated. `0` only if the source says there are none. |
| `steps_where` | `into_feature`, `inside`, `outside`, `unknown` | |
| `plaster` | `yes`, `no`, `unknown` | |
| `construction` | `rock_cut`, `built`, `natural`, `mixed`, `unknown` | |
| `n_pillars` | Integer | Pillars, columns or rock piers. Blank = not stated. |
| `relations` | `relation:feature_id` pairs separated by `;` | Relations: `inside`, `next_to`, `leads_to`, `fed_by`, `above`, `below`, `opposite`. |
| `rel_distance_m`, `rel_bearing_deg` | Numbers, only if printed or scaled | Same order as `relations`, separated by `;`. |
| `period` | As printed | |
| `in_window` | `yes`, `no`, `unknown` | Yes = use in the Hellenistic–Early Roman period (2nd c. BCE to 1st c. CE) as the source states it. |
| `quote` | ≤ 15 words copied from the source | The evidence for the most specific attribute. |
| `confidence` | `high`, `medium`, `low` | The reader's confidence in the row as a whole. |
| `notes` | Free text | |

## Feature classes (closed list)

`cave`, `chamber`, `rock_shelter`, `cistern`, `pool`, `reservoir`, `basin`, `ritual_bath`, `conduit` (channel or aqueduct section), `outlet`, `dam`, `spring`, `tomb`, `burial`, `pit` (pit or shaft), `steps` (a staircase as a feature in its own right), `doorway` (door, threshold or entrance as a feature), `court`, `building`, `room`, `wall`, `tower`, `pillar`, `columbarium`, `cairn`, `terrace`, `road`, `fissure`, `other`.

The list covers the landmark words of the scroll entries as coded in `sandbox/landscape_map_2026-10-31/inputs/entry_features.csv`. Readers are not told which words those are, or how often each occurs.

## Blank, zero and unknown

- Blank = the source does not say.
- `0` = the source says there is none.
- `unknown` = the source mentions the attribute but does not settle it.
