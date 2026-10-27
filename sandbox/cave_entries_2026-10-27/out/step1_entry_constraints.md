# Run 10, step 1: entry constraints (fixed from the text before the inventory, step 2)

Run: cave_entries_2026-10-27. Rule: sandbox/cave_entries_2026-10-27/RULE.md at commit c420100 (SHA-256 5c1bb44a716f8560eb33e3f0b189bf6feca0c2a706480e76179b915067c24195).
Written 2026-10-27 ~05:30Z from text/translation_en.json, text/readings.json, research/comparanda/concealment_contexts/scroll_contexts.csv, research/measurements/cycle4/puech_entry25.md and puech_30_32.md, research/feature_workbench/edition_predicates_2026-10-13/entries2_26/PREDICATES.md, and the entry-25 lane's PLAN.md clause definitions.

Exposure before writing (disclosed): the entry-25 lane README (its results: XII/53 all-match; Twin Cave both-mouths; IV/17, III/11, III/3 etc. near misses), the first three rows of caves.csv (A41 I/1, I/10, I/14), and ASI-Jerusalem place_summary counts. No other cave row was read. Earlier sandbox results were not read for cave content.

## Entry set

setting_P = cave: entries 7, 22, 25, 26, 30. Other editions' codings (setting_Pu, setting_M, setting_L): entry 38 is coded cave by Milik 1962 only ("a regular opening of a cave or rock face", C4 pp. 238-239); Puech and Lefkovits code it as a structure (dovecote; tower). Per the rule, entry 38 is ADDED, scored on Milik's branch only. Entry 56 has a "cave" landmark in t02 but every edition codes it as a tomb: not added.

Cubit: 0.444-0.525 m (as run 1), +-10% where a distance is scored.

## Candidate places (ratings.csv + places.csv) and inventory centres

| Entry | Candidate places | Point (WGS84), sigma |
|---|---|---|
| 7 | jer_temple | 31.77825, 35.23534, ~150 m |
| 22 | kh_qumran | 31.74183, 35.45941, ~100 m |
| 25 | kh_qumran; abu_saraj_iv17 | Qumran as above; IV/17 group ref 31.89009, 35.42477, ~300 m |
| 26 | kh_qumran | as above |
| 30 | jericho_area; tell_el_qos | 31.85611, 35.46306 (area ~3 km); 31.8551, 35.4656, ~200 m |
| 38 | natuf | 31.64436, 35.23543, ~700 m |

Inventory of each entry = every catalogued cave within 5 km of any of its candidate points; entries with a Qumran candidate (22, 25, 26) also get the whole Qumran-Feshkha cliff band, defined as lat 31.700-31.790, lon 35.420-35.475 (the repository's conservative Qumran-Feshkha box, PLAN_AMENDMENT_PHASE4 §5.3).

## Constraints per entry

Scores: pass / unknown / fail, as in run 1. Silence is unknown. "Fail" needs a record that would show the feature and does not, or contradicting geometry. Removal of a deposit is always possible, so an item constraint never fails.

### Entry 7 (II 3-4)
Text: "In the cave of the old House of [MDH], on the third ledge: sixty-five ingots of gold. ΘΕ".
Variants: key word המדה (Puech 2006/2015 'house of tribute'), המרה (Milik 1962; Milik 1960 Bet ha-Mareh), חמדה (Lefkovits 'old Beth Hemdah'), המדח (text shown; Høgenhaven 'washer's house', Temple area). ברובד השלשי: 'third course/terrace/pavement' (lexicon), 'third row of stones' (Lefkovits p. 106), stepped protruding courses (Schiffman). Greek ΘΕ (ΞΕ = 65 rejected by plate check). Landmark: an old building ("house") to which the cave belongs. Direction: none. Depth: none. Item: gold ingots (עשתות), 65.
- E7.C cave (generic).
- E7.L [landmark] building: pass if the record describes a built structure (house, building, rooms, tower, monastery building) at or attached to the cave (same locus, <=50 m); unknown otherwise; no fail.
- E7.R third ledge/course: pass if the record reports at least three ledges, terraces, levels, steps or stone courses in or at the cave; fail only if a published plan and section of the whole cave show a single level and no courses; unknown otherwise.
- E7.I gold / metal ingots found: pass if gold or metal bars/ingots are among the finds; else unknown.
- J7.

### Entry 22 (V 5-7)
Text: "In the fissure (סדק) that is in Secacah, east of the Reservoir of Solomon: vessels of offering, and their record (כתבן) beside them".
Variants: no letter variants; Milik 1960 p. 147: the reservoir is a Qumran reservoir, "undoubtedly" the cistern SE of the site; Milik 1962: legendary name; Puech אשוח. Landmark: Secacah and its Reservoir of Solomon. Direction: east of the reservoir. Feature: a fissure/crack. Items: vessels of offering + their written record.
- E22.F fissure: pass if the source types the feature as crevice, cleft, fissure, crack, or records a crack/fissure in the cave; unknown otherwise; no fail.
- E22.S [landmark] in Secacah: pass if the cave lies within 500 m of the candidate place point (run 1's S bound), counting position uncertainty (d + sigma_cave + sigma_place <= 500 m); fail if d - sigma_cave - sigma_place > 500 m; unknown otherwise. Branch E22.S-2km: same with 2 km (Secacah as a district).
- E22.E [landmark] east of the reservoir: reservoir = the candidate place point (Qumran: SE cistern within the site, sigma 100 m). Bearing reservoir -> cave with half-width atan((sigma_cave+sigma_res)/d); pass if the whole interval lies in 45°-135° (four-wind east, as the frozen entry-25 sector); fail if wholly outside; unknown otherwise or if d < sigma sum.
- E22.I vessels + record: pass if finds include both vessels (pottery, stone, metal vessels, jars) and written material (scroll, fragment, ostracon, inscription, inscribed jar); else unknown.
- J7.

### Entry 25 (VI 1-6)
Text: "[In] the cave of the pillar with the two [en]trances, facing east, [at] the northern entrance dig three [cu]bits: there is a jar, in it one scroll; under it 42 talents".
Variants: עמוד pillar (Milik, Puech) vs platform/terrace (Allegro, recorded by Puech p. 60) [B-PILLAR / B-TERRACE]; B-GATE (Allegro, Temple Double Gate) not a cave, not scored. Facing: cave-level (Milik 1960 p. 140) vs both mouths (stricter). Depth 3 cubits (1.33-1.58 m) at the northern entrance. Deposit: jar with one scroll; 42 talents (Puech: karsh) under the jar or under the scroll. No place name.
- E25.P [landmark] pillar (B-PILLAR, clause C2p) or terrace (B-TERRACE, C2t): coded as in the entry-25 lane PLAN 4.3.
- E25.2 two entrances (C3), E25.E facing east (C4, frozen entry-25 aspect rule; cave level primary, both-mouths branch), E25.N northern entrance (C5): lane PLAN 4.3 coding, primary rule set.
- E25.D three cubits at the northern entrance: pass only if a deposit, pit or jar was found at 1.2-1.8 m below the ancient surface at the northern entrance; no fail; else unknown.
- E25.I jar with scroll: pass if finds include a jar and a scroll (or scroll fragments / linen wrappers); else unknown.
- J7.

### Entry 26 (VI 7-10)
Text: "In the cave of the corner of the heap of stones facing east, dig at the entrance nine cubits: 21 talents".
Variants: הרגם heap/cairn (text shown) vs הרגב boulder (Puech 2006 p. 190, 2015 pp. 60-61: cave at the base of a boulder; rejects 'corner'); Lefkovits: cave of the builder of a sepulcher, aspect may attach to cave or landmark; Allegro: inner chamber of a watchtower (not a cave; not scored). Facing east: cave (Milik-style) or landmark. Depth 9 cubits (4.0-4.7 m) at the entrance.
- E26.L [landmark] heap of stones / boulder at the cave: pass if the record describes a cairn, stone heap or boulder at the cave mouth, corner or front; else unknown; no fail.
- E26.F facing east: the cave-level verdict of the frozen entry-25 aspect rule, as coded in the lane (C4 cave level); pass/fail/unknown. Branch E26.F-landmark: aspect attaches to the landmark, unknown for every cave.
- E26.X entrance (generic: the cave has an entrance).
- E26.D nine cubits at the entrance: unknown unless an excavation at the entrance reports a deposit at 4.0-4.7 m; no fail.
- E26.I talents (metal hoard or coins): pass if found; else unknown.
- J7.

### Entry 30 (VII 8-10)
Text: "In the cave that is next to the cool room of the House of Haqqoz, dig six cubits: six jars of silver".
Variants: המקר[ה] cool room/frigidarium (Puech 2002, 2015 pp. 62, 65) vs בקר[ב]ו 'in its vicinity' (Milik); בית הקצ priestly family Haqqoz (Milik 1962 D18, Puech 2015 p. 66: a Jericho property) vs summer house (Allegro, Beyer, Lefkovits, Schiffman); כדין pitchers (Lefkovits) vs בדין bars (Puech). Depth 6 cubits.
- E30.L [landmark] next to the cool room of a house: Puech branch: pass if the cave lies within 100 m of a recorded window-period building with a bath, or the record says so; Milik branch: pass if within 500 m of a recorded window-period building/estate; else unknown; no fail.
- E30.D six cubits: unknown unless a deposit at 2.4-3.6 m is reported.
- E30.I silver (bars or pitchers): pass if silver/metal or jars containing metal are found; else unknown.
- J7.

### Entry 38 (IX 1-3), Milik branch only
Text (Milik): "In the [cave-]opening at the edge (where the spring emerges) of the Natof, measuring from its edge thirteen cubits; dig two [cubits]: ... staters". Variants on the depth: two cubits (Milik 1960), two holes (Puech 2015), seven cubits (Beyer). Items: staters / bars (Puech) / pitchers (Lefkovits) / talents (Wilmot).
- E38.C cave or rock opening (generic).
- E38.P [landmark] at the edge of the Natof spring: pass if the record places the cave at or above a spring (stated, or <=50 m from a recorded spring); fail if the cave's point lies more than 500 m from the spring point beyond the summed uncertainty (spring sigma ~700 m); else unknown.
- E38.D 13 cubits from the edge, then dig: unknown unless reported.
- E38.I coins/staters/bars: pass if found; else unknown.
- J7.

### J7 (all entries): Second Temple finds in the cave
Window 100 BCE-135 CE as the lane's period descriptor (PLAN 4.4). Pass: period_in_window yes or yes+other. Unknown: partly, or nothing stated. Fail (primary): every stated period lies outside the window AND the cave was excavated or sounded. Branch J7-survey-fail: any 'no' fails. Branch J7-lenient: 'partly' passes.

## Lead (rule's Decision)
- Primary (literal): no fail; at least two passes not counting J7; at least one pass on an entry-specific constraint (any constraint other than E7.C, E25 C1, E26.X, E38.C and J7). Each pair takes its best branch combination (as run 1), and the combination is reported.
- Strict alternative: no fail; at least two passes on entry-specific constraints.

## Control (rule step 4)
Landmark bundles (from the t02_landmarks column): L7 = E7.L (old house); L22 = E22.S + E22.E (in the settlement, east of its reservoir); L25 = E25.P (pillar / terrace); L26 = E26.L (heap / boulder); L30 = E30.L (cool room of a house); L38 = E38.P (at the spring edge). A swap is a random derangement of the landmark bundles among the entries (seed 20261027, 10 swaps). Each entry keeps its own inventory caves and its non-landmark constraints and takes another entry's landmark bundle. Positional landmarks are resolved against the cave's own inventory place: L22's settlement and reservoir = the nearest candidate point of the cave's own entry; L30 = window-period bath buildings / estates near the cave; L38 = springs near the cave. Lead counted as above. Permutation p (one-sided) = (1 + number of swaps with lead pairs >= real) / 11. Primary set: all six entries; alternative: the five setting_P entries (38 excluded).
- Alternative pairing (cheap, labelled deviation): every entry x every inventory cave.
