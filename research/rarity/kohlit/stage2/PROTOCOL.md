# Stage 2 coding protocol (frozen before any Stage 2 coding)

This file, `protocol_constants.json`, `coverage.json`, `build_packets.py` and `match.py` were committed together, before any unit was coded. They apply §4 and §5 of the [pre-registration](../../../preregistration/kohlit_rarity_2026-10-08.md). Where the pre-registration is silent, the choices below were made without any coded data.

**Deviation, logged.** §5 says that the matching script is committed "before Stage 1". It was committed after Stage 1 (screens 75b0af9 and 75ceb80) and before Stage 2. Stage 1 output holds no position, distance, bearing, mouth or date data, so no condition could be seen before this freeze.

## 1. Units and order

- **Units.** Every unit with Stage 1 status "to Stage 2": 244 units in R1, all period sets (190 in the main set).
- **Order.** Coder A takes units in the order of `coder_a_order` in the packet manifest. That order is a shuffle with seed 20261008. Batches have 12 units.
- **Coder B** redoes a random 20% of the units (seed 20261009) plus every unit for which coder A's sheet gives a unit MATCH in any branch, variant or Nigro setting (`match.py sample-b`). Coder B does not see coder A's sheets.
- **Merge.** Where both coders coded a unit, each condition keeps its value if the coders agree and becomes UNKNOWN if they differ. Agreement and Cohen's kappa are reported per condition.

## 2. The packet

`build_packets.py` writes one JSON packet per unit. It holds only the five §5 sources.

| § 5 source | In the packet |
|---|---|
| 1 WBADB | The unit's own row. Every WBADB row within 2 km, with `geom`: distance, grid bearing (0° = grid north, clockwise), precision and `bearing_valid`. |
| 2 Original survey entry | The pages of Finkelstein et al. 1997 when the Survey_Ref names them (open access). Other surveys: "not accessed". |
| 3 SWP Memoirs | Entries linked in Stage 1b, entries with the same name within 15 km, and entries whose text names the unit (at most 10). |
| 4 First publication | Excavated units only. The first item of WBADB `Publication_Bibliography`. Excerpts (plan, water and burial passages) where it is lawfully online. |
| 5 Nigro, Sala and Taha 2011 | Oasis units only: every catalogue entry within 2 km, with `geom`. A unit is in the oasis when one or more catalogue entries lie within 2 km of it. |

**Precision.** A WBADB point's precision is the coarsest of 1,000, 500, 100, 50 or 10 m that both its grid values are divisible by. Nigro points have a precision of 30 m, because the catalogue says its seconds are "indicative". Position rule 2 is computed for you: `bearing_valid` is true only if the distance is 3 or more times the coarser precision.

**Use nothing else.** Do not use your own knowledge of any site, other books, maps or the web. The project has already looked at several candidates (pre-registration "Exposure"). Code them exactly like every other unit.

## 3. What to record

Read every source in the packet. Record each **feature** that is a candidate for C1, C2 or C3, from any source, at any distance up to 2 km. Record the same physical feature once per source that describes it.

| `type` | What it includes | Extra field |
|---|---|---|
| `pool` | An open basin or reservoir, built or rock-cut, including spring pools. Not: a covered cistern, a vat, a trough, a winepress basin. | `pool_def`: `yes` if 3 m or more a side, or if the source calls it a pool, reservoir, birka (any spelling) or tank; `no` if the source shows it is smaller or not open; `unclear` otherwise. A bare "basin" with no size is `unclear`. |
| `pit` | A cavity with a surface opening that is not a burial: cistern, pit, silo, shaft, underground chamber, tunnel, rock-cut cave. | `is_tomb`: true if the source calls it a tomb or burial cave. |
| `grave` | Any grave, tomb, burial cave, kokh or cemetery. | `cavity_with_opening`: true for a shaft tomb, a rock-cut burial cave or a kokhim tomb; false for a cist, pit or trench grave or a cemetery of such graves. |
| `other` | Use only if a feature is needed as a reference point for another feature. | none |

A "cistern" is a `pit`. A cave is a `pit` unless the source calls it a burial or tomb cave. A "reservoir" or "pool" that the source says is roofed is a `pit` (a cistern), not a `pool`.

## 4. Position

Give exactly one `position` per feature.

- **`grid`.** The feature has its own point in the packet: a WBADB row (`ref` = its row id, for example `S1234`) or a Nigro entry (`ref` = `N` + catalogue number, for example `N21`). Use the packet's `geom`. Do not compute bearings yourself. If the row is a site with several components, use `grid` only for a component that the row itself is (for example a row named "Birket X"). Do not use `grid` for one item in a list of a site's components.
- **`words`.** The source gives a direction from the unit in words. Give `direction` as a compass point (N, NNE, NE, ENE, E, …, NNW) or, for C1 only, `east part` when the source puts the feature in the site's eastern part. Give `distance_m` only if the source gives a distance. Set `relative_to` to `unit` only if the direction is from the unit site itself. If it is from something else ("east of the cistern"), set `other`.
- **`plan`.** You measured `bearing_deg` and `distance_m` from the unit's centre on a published plan in the packet. Say which figure in `cite`.
- **`none`.** No position is given. This is the usual case for a component in a WBADB component list.

**Rules applied by `match.py`, not by you.**
- A verbal NE, SE, SW or NW lies on a quadrant edge and gives UNKNOWN (position rule 3).
- A `words` position with no distance counts as within the distance limit. A site description is taken to cover the site and its immediate surroundings.
- A `grid` position with `bearing_valid` false gives UNKNOWN.

## 5. Graves at the mouth (C3, text level)

For a grave that a source puts at a pit's opening, fill `mouth`: `pit_id` (the id of that pit in your sheet), and `distance_m` if a distance is given, or `phrase` with the source's words (for example "at its mouth", "beside the cistern"). Leave `mouth` empty otherwise.

## 6. Date

`date.code`: `D` if a source dates the feature itself to 135 CE or earlier (the window and before it; "Roman" counts, because surveys do not split the Roman period); `L` if a source dates the feature itself securely after 135 CE; `U` otherwise. A feature that has its own WBADB row takes `D` if that row records any period from LP to Rom, and `L` if it records only Byz, EIs, Med or Ott. A component of a site row takes `U`, unless a source dates the component itself. Give the reason in `date.basis`.

## 7. Explicit absence

A FAIL needs a positive statement. Record it in `explicit_absence` only when a packet source says that the feature class is **absent** at the unit: for example "no cisterns", "no tombs were found", "no water installation". Give `condition` (C1, C2 or C3), `source`, `cite` and `quote`. Silence, or a short description, is not an absence statement.

## 8. Sources read

In `sources`, give for each of "1"–"5": `read`, `not accessed`, `none in packet`, `not excavated` or `not in oasis`, as the packet shows.

## 9. Quotes and citations

- `cite`: the WBADB row id and field, "Mem III p. 220", "Finkelstein et al. 1997 p. 828", "Nigro 2011 cat. 21 p. 110", or the first publication's page.
- `quote`: the words that support the feature, 12 words at most. Sources 2, 4 and 5 are under copyright: quote only what the coding needs.

## 10. Output

Write one file per unit, `coded/<A or B>/<unit_id>.json`:

```json
{
  "unit_id": "S1234",
  "coder": "A",
  "sources": {"1": "read", "2": "not accessed", "3": "read", "4": "not excavated", "5": "not in oasis"},
  "explicit_absence": [],
  "features": [
    {"id": "f1", "source": "3", "cite": "Mem II p. 156", "quote": "on the east is a large tank",
     "type": "pool", "subtype": "tank", "pool_def": "yes",
     "position": {"kind": "words", "direction": "E", "distance_m": null, "relative_to": "unit"},
     "date": {"code": "U", "basis": "not dated by the source"}},
    {"id": "f2", "source": "1", "cite": "WBADB S1240 Site_Components", "quote": "cistern",
     "type": "pit", "subtype": "cistern", "is_tomb": false,
     "position": {"kind": "grid", "ref": "S1240"},
     "date": {"code": "D", "basis": "row S1240 records Rom"}},
    {"id": "f3", "source": "3", "cite": "Mem II p. 156", "quote": "rock-cut tombs beside the cistern",
     "type": "grave", "subtype": "rock-cut tombs", "cavity_with_opening": true,
     "position": {"kind": "none"}, "mouth": {"pit_id": "f2", "distance_m": null, "phrase": "beside the cistern"},
     "date": {"code": "U", "basis": "not dated"}}
  ],
  "notes": "short notes on anything unclear"
}
```

`python3 -I match.py validate PACKETS_DIR coded/A` checks every sheet against its packet.

## 11. What `match.py` computes

- **C1** pool (`pool_def` yes), 45°–135° or `east part`, ≤ 1 km.
- **C2** pit (`is_tomb` false), 315°–45°, ≤ 1 km.
- **C3 survey level** any grave, 315°–45°, ≤ 1 km.
- **C3 text level** a grave whose `mouth` names a pit that meets C2, at ≤ 10 m or with a mouth phrase in `protocol_constants.json`.
- **Date:** D or U passes, L fails.
- **Branches:** A survey = C1 + C2 + C3 survey (the headline); A text = C1 + C2 + C3 text; B = C1 + C2.
- **Variants:**
  - C1 at 0.5 km and at 2 km;
  - C2 with tomb shafts allowed (a `pit` with `is_tomb` true, or a `grave` with `cavity_with_opening` true);
  - dated only (D passes, U does not).
- **Nigro:** every result is computed with and without source 5 (decision 7).
- **Units that stopped at Stage 1** are UNKNOWN on every condition.
- **Report:** N, k, f and m per set (R1/R2 × main/pre-70) and branch. m is split by the coverage class of the unit's survey (`coverage.json`), and by "not recorded at Stage 1".
