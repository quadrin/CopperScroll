# Entry 25 mouth-aspect rule and IV/17 target declarations

Version 1. Written 9 October 2026 (UTC) by worker rule-freezer. Frozen before the L-656 field file or any IAA Archive cave record arrived. `rules.json` holds the same rules in machine-readable form. If the two ever disagree, the affected verdict is reported as inconclusive and the disagreement is logged.

Exploratory. These rules make no identification claim. They change no registered result and reopen no closed or parked test. A PASS is compatibility only.

Labels: **EVIDENCE** is observed in a cited source. **INFERENCE** is reasoned from evidence. **ASSUMPTION** is a declared project choice. Every number below is an ASSUMPTION unless it is marked otherwise. Each one has a short reason and its sensitivity alternatives.

## 0. Why these rules exist

- EVIDENCE: the arrival register asks for two freezes before the L-656 file or the IAA records arrive: an Entry 25 mouth-aspect rule and the IV/17 target declarations (`research/preregistration/arrivals/README.md`, proposal 4).
- EVIDENCE: the decisions module's bearing component says a "not both east" verdict needs "a qualitative aspect rule frozen before the plan is read" (`research/feature_workbench/decisions/discrimination.json`, task `decisions-iv17-l656`).
- EVIDENCE: the coverage join lists five IV/17 parameters that no record can supply: zone outline, origin point, sector, depth band and radial tolerance (`research/feature_workbench/coverage/volume_inputs.json`, `declarations`).
- EVIDENCE: the IV/17 assessment says any angular sector must be declared as a project assumption before testing (`research/assessments/entry25_iv17/README.md`, Facing).

## 1. What the rule-writer had already seen (exposure)

- EVIDENCE, exposed: Sion 2002 Plan 5 (p. 63) gives chord-normal proxies of about 123° (northern mouth) and 119° (southern gap), clockwise from the drawn north arrow. Endpoint ranges are 99.5–140.8° and 104.0–132.4°. Pilot envelopes are 101–151° and 103–143°. The arrow's north convention is unspecified.
- EVIDENCE, exposed: the northern-minus-southern midpoint offset is about 2.63 m north and 3.30 m east. The northern present chord is about 0.86 m (0.59–1.16 m). Plan 5 shows no excavation limits. Sion p. 63 places the excavation at the centres of both spaces.
- EVIDENCE, exposed: Bar-Adon describes both Twin Cave openings as east-facing. Feig describes IV/11's internal pillar without a documented exterior pair.
- Disclosure: the existing northern endpoint range already crosses the 135° edge of the primary east sector below. The line joining the two IV/17 mouth midpoints runs roughly north-east to south-west.
- The sectors come from the text side (section A5). The mouth measure follows the repository's existing chord-normal metric. The cave-level measure combines the cliff-frontage sense and the mean of the mouths. None of these choices was tuned to the exposed values.
- The rule-writer computed no verdict of these rules on any real record. Plan 5, Sion's text, Bar-Adon and Feig can never test these rules. Any later application to them is exploratory.
- Not seen: the L-656 file, any IAA cave record, and the unread ʿAtiqot 41 cave entries named in the IAA item file.

## Part A. Entry 25 mouth-aspect rule

### A1. Text and scope

- EVIDENCE: VI 2 reads [ה]פתחין הצופא מזרח in the project text. Puech prints the article before צופא as an editorial correction (`research/measurements/cycle4/puech_entry25.md`).
- EVIDENCE: Milik 1960 p. 140 attaches the eastward aspect to the cave. Puech 2015 pp. 59–60 gives no explicit requirement that both mouths face east (`research/sources/entry25_direction_review_2026-10-02.md`).
- The project keeps two hypotheses as model branches: cave-level aspect (`orientation = cave`) and individual-mouth aspect (`orientation = both-mouths`). This rule measures both.
- The rule applies the same way to every Entry 25 roster cave: IV/17, IV/11 and Twin Cave, and any cave added later. Controls get the same opportunities (AGENTS.md).
- A record counts for a cave only if it names the cave's survey number, or a recorded crosswalk links them. Otherwise the record is silent for that cave.

### A2. Azimuth and north

- Azimuths are degrees clockwise from true north, from 0 to 360.
- ASSUMPTION: the reference is true north. Reason: "east" (מזרח, the side of sunrise) is an astronomical direction.
- Every outcome record states the record's north case, the correction applied with its source, and the allowance used.

| North case in the record | Correction to true north | Allowance |
|---|---|---|
| True north stated | none | 0° |
| Grid north (Old Israel Grid, ITM, Palestine grid) | add the grid convergence γ = (site longitude − central meridian) × sin(site latitude) | 0.5° |
| Magnetic north, declination stated | add the stated declination (east positive) | 1° |
| Magnetic north, survey year known | add the IGRF declination for that year and place, cited | 1° |
| Unspecified (for example Plan 5's arrow) | none | **6°** (sensitivity 3° and 10°) |

- INFERENCE: both Israeli grids have a central meridian near 35.2°E. At the Jericho escarpment (about 35.4°E, 31.8°N) the convergence is near 0.1°.
- ASSUMPTION, 6° for an unspecified north. Reason: if the arrow is magnetic, the true direction lies a few degrees east of it in recent decades. A symmetric 6° also covers a grid or true mix-up. Check the declination against IGRF before use. Sensitivity: 3° and 10°.

### A3. Measuring one mouth

- **Primary measure: outward normal of the aperture chord.** The chord joins the two rock-cut jamb points of the mouth. Take them at the narrowest rock-cut section at the threshold level when the record draws it. Otherwise take them where the drawn mouth line meets each jamb. Outward is the side away from the chamber the mouth leads into.
- Masonry is excluded. A partly blocked mouth is measured on its rock-cut jambs. If a rock-cut jamb is hidden or not drawn, that mouth is not measurable. EVIDENCE: the IV/17 southern mouth is partly blocked, and its present gap cannot stand for the full earlier mouth (`entry25_iv17/README.md`).
- Sensitivity measure: the passage axis. It runs from the midpoint of the inner chord (where the passage meets the chamber) to the midpoint of the outer chord. Use it only where the record draws a passage. It is reported and never changes a verdict.

### A4. From a drawing to an interval

The interval is nominal azimuth ± h, where

h = asin(min(1, 2r / L)) + asin(min(1, 2e / La)) + d + n

- L is the chord length and r the endpoint radius, both in metres. If 2r ≥ L, the interval is the full circle.
- r = max(0.10 m, the record's stated survey precision, 0.5 mm at the printed scale, 2 px on a raster). ASSUMPTION 0.10 m. Reason: rock-cut jamb edges are ragged at the decimetre scale; the repository's Plan 5 repeat used ±5–6 px (about ±0.09–0.11 m) per coordinate. Sensitivity: 0.05 m and 0.20 m.
- La is the drawn north-arrow length and e its endpoint uncertainty: 0.5 mm at print, 2 px on a raster, or the stated precision. ASSUMPTION; the Plan 5 repeat used ±2 px. If 2e ≥ La, the interval is the full circle. A record with a coordinate grid instead of an arrow uses e = 0.
- d is drawing distortion: 1° for a scanned or printed plan, 0° for digital survey coordinates. ASSUMPTION. Reason: a flat scan of a printed plan keeps angles to about a degree. Sensitivity: 0° and 3°.
- n is the north allowance from A2.
- A record that gives a number instead of a drawing: h = (stated precision, or 10° if none) + n. ASSUMPTION 10°. Reason: compass readings on irregular cave mouths. Sensitivity: 5° and 15°.
- A record that gives a compass word: the interval is that word's sector at the record's resolution. Half-widths are 45° (4-point), 22.5° (8-point) and 11.25° (16-point). If the resolution is not stated, use 8-point when the record uses any intercardinal word, otherwise 4-point. No north allowance is added to a word, because the bin is far wider than any north offset. Sensitivity: add n.

### A5. Sectors for the direction words of Entry 25

| Word | Role | Primary sector | Sensitivity sectors |
|---|---|---|---|
| east, מזרח | facing | **45°–135°** | 67.5°–112.5° (eight-wind east); 62°–118° (solstice sunrise arc); 22.5°–157.5° (north-east, east and south-east winds) |
| northern, צפוני | names one mouth of the pair | no facing sector; see A6 | none |

- EVIDENCE: the project translation (`text/translation_en.json`) uses only the four cardinal words, and no intercardinal compound.
- ASSUMPTION, primary 45°–135°. Reason: with only four direction words, a facing nearer east than north or south is "east". This is the four-wind partition.
- ASSUMPTION, eight-wind 67.5°–112.5°. Reason: a stricter reader who would call a north-east facing "north-east".
- INFERENCE, sunrise arc 62°–118°. מזרח is built on the root for the sun's rising. At latitude 31.8°N the solstice sunrises lie near 62° and 118° (flat horizon, no refraction, obliquity 23.4–23.7°).
- ASSUMPTION, broad 22.5°–157.5°. Reason: a loose reader who calls any eastern-side facing "east".
- INFERENCE (direction review): "the northern opening" picks the northern member of the pair. It does not require that mouth to face north. A "facing north" reading of צפוני is not a retained branch.

### A6. Northern-member rule

- Take the two mouth-chord midpoints Ma and Mb. Δ is the northing of Ma minus the northing of Mb, in true north.
- Let α = asin(min(1, 2e / La)) + d + n. Δ ranges over every north direction within ±α, then widens by ±2r.
- Ma is the northern mouth if the whole Δ interval is above zero. Mb is northern if it is wholly below zero. Otherwise the northern member is undetermined.
- This rule can decide or leave undetermined. It cannot contradict the existing "northern-member" checks. Undetermined leaves the origin undefined (Part B).

### A7. Decision rule

For one interval against one sector:
- **PASS** only if the whole interval lies inside the closed sector.
- **FAIL** only if the interval and the sector share no arc of positive length. Touching at one edge counts as no overlap.
- **INCONCLUSIVE** otherwise. A full-circle interval is always inconclusive.
- **NOT MEASURABLE**: the record covers the cave but lacks a needed element (no north arrow, grid or convention; no scale where one is needed; a jamb not drawn; mouths not distinguished).
- **SILENT**: the record gives no geometry or facing for that cave.

### A8. Individual-mouth and cave-level verdicts

- **Individual mouths (`both-mouths`).** This needs the two ancient mouths. FAIL if any mouth fails. PASS if both pass. NOT MEASURABLE if both mouths are not measurable, or if the record shows fewer than two mouths. SILENT if the record has no facing for either mouth. INCONCLUSIVE otherwise. A single facing value for a two-mouth cave is cave-level evidence only.
- **Cave level (`cave`).** The interval is the smallest arc containing two parts:
  1. the facade normal: the outward normal of the chord joining the two mouth-chord midpoints. Outward is the normal within 90° of the mean mouth facing. Its half-width uses D, the midpoint distance, in place of L. With more than two mouths, use the two midpoints farthest apart.
  2. the mean mouth facing: from the mean of the lower ends to the mean of the upper ends, after unwrapping. If the mouth intervals ever lie 180° apart, this part is not measurable.
- For a cave with one mouth, the cave level is that mouth's interval. A record's single facing value or word for the cave is used directly as the cave-level interval.
- ASSUMPTION, the two-part hull. Reason: "the cave facing east" can mean the cliff frontage or the direction its openings face. A verdict is decisive only when both senses agree.

### A9. Phase

- The measure uses rock-cut jambs. ASSUMPTION: a verdict applies to both phase branches (`reported` and `ancient`), as the decisions module's bearing component does.
- Exception: if the record shows the rock-cut aperture was cut or enlarged after the ancient phase, the verdict applies to `phase = reported` only. The ancient branches stay undetermined.
- Sensitivity: the strict reading. The verdict reaches the ancient branches only when the jamb cutting is dated before or within the ancient phase.

### A10. Several records

- Records already in the repository are exposed. They are never scored under this rule. Their existing inventory values stay as recorded.
- Each new record is scored on its own. If one new record passes and another fails, the combined verdict is INCONCLUSIVE and both are reported. A decisive verdict plus an inconclusive one keeps the decisive verdict.
- If a new decisive verdict disagrees with an earlier published description, report the disagreement. The new verdict drives the class effect, because only it was scored under a rule frozen beforehand.

### A11. Outcomes and the Entry 25 classes

Outcome ids have the form `e25aspect:<cave>:<level>:<verdict>`, where cave is iv17, iv11 or twin; level is mouths or cave; verdict is pass, fail, inconclusive, not-measurable or silent. The suffix `:reported-only` marks the A9 exception. Only the primary sector sets the class effect.

The classes are the decisions module's own (`discriminate.py`, read-only, 8 October inputs). c01: all IV/11 and Twin Cave branches plus IV/17 cave-level reported branches (216). c02: IV/17 pillar, both mouths, ancient (12). c03: IV/17 both mouths, reported (24). c04: IV/17 pillar, cave, ancient (12). c05: IV/17 terrace, both mouths, ancient (12). c06: IV/17 terrace, cave, ancient (12).

| Outcome | Decisions value | Effect | Classes removed | Classes kept |
|---|---|---|---|---|
| `iv17:mouths:pass` | `both-east` | aspect compatible, orientation both-mouths | none | c01–c06 |
| `iv17:mouths:fail` | `not-both-east` | aspect contradicted, orientation both-mouths | **c02, c03, c05** | c01, c04, c06 |
| `iv17:mouths:fail:reported-only` | none registered | contradicted where orientation both-mouths and phase reported | **c03** | c01, c02, c04, c05, c06 |
| `iv17:mouths:inconclusive`, `not-measurable`, `silent` | `undetermined` | none | none | c01–c06 |
| `iv17:cave:pass` | none registered | aspect compatible (already compatible) | none | c01–c06 |
| `iv17:cave:fail` | none registered (proposed row) | contradicted where orientation cave | **c04, c06**, and 24 IV/17 members of c01 | c01 (through IV/11 and Twin Cave), c02, c03, c05 |
| `iv11:*:fail`, `twin:*:fail` | none registered (proposed row) | contradicted for that cave and orientation | members inside c01 only | all classes; c01 must be recomputed |
| any other outcome | none | none | none | all |

- A FAIL removes only the branches it names. Other caves and readings are untouched.
- Rows marked "proposed" need a new outcome row in the decisions module before they change its output. These rules do not add that row. They fix in advance what the row must say.
- The northern-member rule has no class effect (A6).

### A12. Sensitivity reporting

- Report every verdict under every sensitivity sector, every uncertainty alternative (r, n, d, reported precision, word allowance), the passage-axis measure and the strict phase reading.
- Sensitivity results never change the class effect. If any of them turns a PASS into a FAIL or the reverse, say so in the report.

## Part B. IV/17 target declarations

Target `coverage-tv-e25-iv17-north`, case `coverage-volume-iv17`, footprint `coverage-fp-iv17-l656`. The join expands two direction models times four cubit options into eight branches. Field names follow `volume_join.py`.

### B1. Frame

- Target and cuts must share one plan frame with a scale and a north arrow or grid. Primary: the L-656 plan's own frame, imported into the states register with `metres_per_unit`, `north_vector` and `y_axis`.
- Alternative: Plan 5's frame `states-iv17-plan5-crop`, only with a recorded registration of the L-656 cuts to it. ASSUMPTION: at least three common points and an RMS residual of 0.10 m or less.
- Without a shared frame the join is undeterminable (`frame_registration`).

### B2. Mouth and threshold chord

- The northern mouth is chosen by the A6 rule.
- Primary chord: the rock-cut jamb-to-jamb chord of the northern mouth at the ancient threshold surface.
- Fallback, declared now: the record's drawn mouth line at its rock-cut jambs. Results under the fallback are labelled "present-state chord".
- Plan 5's present chord, [548, 386]–[502, 400] px, is exposed. It serves exploratory runs only.

### B3. Origin point (`origin.point`)

- Midpoint of the threshold chord, in frame units.
- Sensitivity: midpoint of the outer chord; midpoint of the inner chord where a passage is drawn.
- The vertical branches do not use the origin directly. Their zone is built on the same chord.

### B4. Zone outline (`region.polygon`), vertical branches

- A rectangle aligned with the threshold chord. Along the chord it runs from jamb to jamb, extended by r = 0.10 m at each end. Across the chord it runs d_out + r outward and d_in + r inward.
- If the record draws a passage whose inner chord lies farther inward, the zone extends to the inner chord plus r.
- ASSUMPTION: d_out = d_in = 0.50 m. Reason: "in the northern opening" starts the digging at the doorway; about one cubit either side of the threshold line holds where a person standing there would dig. Sensitivity: 0.25 m each side; 1.00 m each side; inward only (0 m out, 1.00 m in).
- ASSUMPTION: r = 0.10 m, as in A4. Widening by r is conservative for both "covered" and "not covered".

### B5. Sector (`sector_deg`), horizontal branches

- Centre: the inward normal of the threshold chord (outward facing + 180°), measured with the frame's own `north_vector`. No true-north correction is needed, because target and cuts share the frame.
- Half-width: 45° + asin(min(1, 2r / L)).
- INFERENCE: the entry opens "in the cave", so a horizontal measure from the opening runs inward. ASSUMPTION ±45°: the same four-wind half-width as the east sector.
- Sensitivity: half-width 22.5° and 90° (plus the same chord term); an outward sector (jar in front of the mouth) with the primary half-width.

### B6. Distance band and radial tolerance, horizontal branches

- ASSUMPTION: origin uncertainty r = 0.10 m. Instruction tolerance 0.20 m: how closely a counted three-cubit distance places the jar. Sensitivity for the instruction tolerance: 0.10 m and 0.40 m.
- Range branch: `distance_band_m` = [1.10, 1.90] m, the three-cubit band widened by r.
- Single-cubit branches: `radial_tolerance_m` = 0.30 m (0.20 + 0.10). Sensitivity 0.20 m and 0.50 m.
- Unit alternative the repository already carries: 0.445–0.525 m per cubit gives 1.335–1.575 m for three cubits (`research/measurements/cycle7/kohlit_pool.md` item 5). It is a sensitivity run, not a branch.

### B7. Depth

- Vertical branches: the depth is the three cubits themselves. The project's exploratory 0.40–0.60 m cubit gives 1.20–1.80 m (range branch), and the samples give 1.20, 1.50 and 1.80 m below the ancient threshold. ASSUMPTION, inherited from the repository; not a textual calibration. Sensitivity: ±0.30 m around each single level; the 0.445–0.525 m scenario.
- Horizontal branches: `depth_band_m` = [0.00, 1.80] m below the ancient threshold surface. ASSUMPTION. Reason: the horizontal reading states no depth; the bound reuses the deepest three-cubit length in the project range, so a dig must reach that deep before the branch counts as covered. Sensitivity: [0, 0.60] m (one cubit, shallow burial); [0, 3 × unit] per branch; [0, 1.575] m.

### B8. Reference surface

- Elevation, vertical datum and phase of the ancient northern threshold come from the L-656 section or level register.
- If the record gives the threshold as a range (uneven surface or stated precision), run the join at the lowest and the highest level. The status holds only if both runs agree. Otherwise it is undeterminable. ASSUMPTION: an unstated reading precision is ±0.05 m.

### B9. Reading the footprint

- A cut's outline and its top and lowest-reached levels come from the L-656 plan, level register or basket register, in the threshold's datum.
- If a cut has only spot levels, use its highest recorded bottom for the "covered" test and its lowest recorded bottom for the "not covered" test.
- The join never infers that a deposit is absent. Accessibility, preservation, phase reached and detection limits are carried, not used for the spatial status. A covered branch still needs the six negative-excavation gates.

### B10. The eight branches

| Branch (after `coverage-tv-e25-iv17-north/`) | Model | Outline | Depth below threshold | Radial band | Tolerance |
|---|---|---|---|---|---|
| `vertical/range-0.40-0.60` | vertical | zone B4 | 1.20–1.80 m | — | — |
| `vertical/0.40` | vertical | zone B4 | 1.20 m | — | — |
| `vertical/0.50` | vertical | zone B4 | 1.50 m | — | — |
| `vertical/0.60` | vertical | zone B4 | 1.80 m | — | — |
| `horizontal/range-0.40-0.60` | horizontal | origin B3, sector B5 | 0.00–1.80 m | 1.10–1.90 m | in band |
| `horizontal/0.40` | horizontal | origin B3, sector B5 | 0.00–1.80 m | 1.20 m | ±0.30 m |
| `horizontal/0.50` | horizontal | origin B3, sector B5 | 0.00–1.80 m | 1.50 m | ±0.30 m |
| `horizontal/0.60` | horizontal | origin B3, sector B5 | 0.00–1.80 m | 1.80 m | ±0.30 m |

### B11. What a record must show

Requirements:
- **R-FRAME**: one shared frame (B1).
- **R-MOUTH**: both rock-cut jambs of the northern mouth (B2).
- **R-NORTH**: a decided northern member (A6).
- **R-THRESHOLD**: threshold elevation or range, its datum and its phase (B8).
- **R-CUT-OUTLINE**: the outline of every cut.
- **R-CUT-LEVELS**: top and lowest-reached level of every cut, in the threshold's datum.

Statuses, for every branch:
- **Covered**: all six requirements, and the cuts together contain the whole branch outline over the whole depth interval. This must hold at both threshold levels (B8) and with the highest recorded bottoms (B9).
- **Partly covered**: all six requirements, and the cuts contain part but not all of it.
- **Not covered**: every cut lies wholly outside the branch outline (needs R-FRAME, R-MOUTH, R-NORTH and R-CUT-OUTLINE only), or wholly above or below the depth interval (needs R-THRESHOLD and R-CUT-LEVELS). This must hold at both threshold levels and with the lowest recorded bottoms.
- **Undeterminable**: anything else. The result lists the missing parameters by their `volume_join.py` names.

Outcome ids: `iv17cov:<direction>/<cubit>:<status>`. Coverage outcomes remove no Entry 25 class. A threshold value can make a target computable but cannot contradict a branch (decisions README).

### B12. Field names for the coverage module

- Target level: `origin.point` (B3) and `region.polygon` (B4), in frame units.
- Horizontal direction option: `sector_deg` (B5), `depth_band_m` = [0.0, 1.8], `radial_tolerance_m` = 0.30.
- Cubit option `range-0.40-0.60`: `distance_band_m` = [1.10, 1.90]. The vertical model ignores it.
- `reference_surface.elevation_m`, `vertical_datum_id` and `phase_id` come from the record (B8).
- `check_rules.py instantiate` turns these rules plus record geometry into those values.

### B13. Limits of the declarations

- They are model choices, not observations. They make the IV/17 target computable once the record supplies geometry.
- The arrival register's coverage prediction concerns the joins without declarations. These rules leave it as frozen. A run with these declarations is a separate evaluation.

## Part C. Where these rules sit

These rules sit beside the frozen and reviewed documents below. They change none of them. `rules.json` lists each with its SHA-256 at freeze time.

- The arrival register (`research/preregistration/arrivals/`), including `MANIFEST.md`, `ARRIVAL_PROCEDURE.md` and the item files `l656-field-file.md` and `iaa-archive-cave-records.md`. Their outcome ids stay valid. An aspect verdict is scored here, beside them.
- The XII 10 reading protocol (commit fd3f334). Unrelated; unchanged.
- The Koḥlit rarity pre-registration of 8 October. Unrelated; unchanged.
- The Koḥlit chain and its registration protocol, and the Entry 60 registry v2. Their 315°–45° north sector for Entry 60 is untouched. These rules do not apply to Entry 60.
- The decisions module (`plans.json`, `discrimination.json`, `discriminate.py`). These rules supply the frozen aspect rule its bearing component asks for.
- The coverage module (`volume_inputs.json`, `volume_join.py`). These rules supply the model declarations it lists.
- The IV/17 assessment (`README.md`, `assessment.json`), the inventory (`catalog.json`, `queries.json`) and the states register. Unchanged.

## Changes to existing files

None.
