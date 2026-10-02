# Entry-order sensitivity packet — R10, with spatial uncertainty relevant to R08

Baseline: quadrin/CopperScroll commit `bb2fde4c76dbbe34b4c7345646acee049e875229`, inspected through its AGENTS.md, deep_analysis/README.md, research/text/deeper_analysis_2026-09-30.md, tables/phase3_places.csv and tables/entry_concordance.csv. This packet runs a computational pilot using existing input hypotheses. It adds no independently inspected archaeological source, decisive candidate test or question closure.

## Target and readiness

Measure how anchor choice changes the apparent shortness of the selected-stop order. The deterministic distance pilot is complete. Regional-group stability under editorial division variants and independently fixed entry locations remains configured work; the present inputs do not supply a provenance-reviewed independent anchor set. R10 can move to In progress for this bounded pilot. R08 still needs entry-specific surface/direction/unit models; great-circle distance alone does not address those models.

## Executed method

`python sequence/pilot.py`

Inputs and outputs live in `sequence/`. `places.csv` and `concordance.csv` preserve the pinned repository content with normalized line endings. `legacy_route_jer.py` and `legacy_route_jer.json` preserve the existing calculation and delivered results. `manifest.json` records the pin, the SHA-256 of each actual local input copy, all stop scenarios and the algorithm. `results.csv` gives sixteen scenario summaries. `edges.csv` gives individual selected-stop legs with both endpoints' coordinate-precision statements.

Metric: great-circle distance on a sphere of radius 6,371 km. Each scenario enumerates all labeled-stop permutations, including reverse orders, as open paths with free endpoints. Seeds: none. The exact fraction of orders at least as short is a property of this finite comparison; it supplies no probability that an identification is correct. Distance precision in the summaries below is approximately 0.1 km; raw calculation decimals in CSV support reproduction.

The three existing baseline distance cases reproduce committed values at their reported precision. We did not rerun walking hours: no terrain grid was needed or acquired. The legacy walking model uses an isotropic slope cost and modern terrain, which also leaves ancient paths, barriers and site access unresolved.

## Initial results

Legacy Jerusalem “strict” scenario: five selected stops, scroll-order total 5.9 km, permutation median 9.6 km, shortest open path 5.3 km; 20 of 120 orders are at least as short. Its selected-leg median is available in CSV. The input table grades associations for entries 48 and 52 low, despite the legacy scenario name “strict.” Removing entry 46 changes the comparison to 1.3 km against a 1.4 km median; 10 of 24 orders are at least as short. Removing entry 55 gives 10 of 24 as well. The apparent order effect depends on the terminal anchors.

Legacy Jerusalem “lenient” scenario: seven selected stops, 17.9 km against a 32.3 km median, shortest 16.0 km; the ordering fraction is 0.0369 under this specified experiment. The earlier report's multiple-test discussion already treats this as weak, model-dependent evidence. This rerun adds no independent corroboration.

Jericho/Nuweimeh scenario: seven selected stops, 54.2 km against a 67.5 km median, shortest 30.9 km; the ordering fraction is 0.1504. Substituting the Buqeia label anchor for Achor yields 44.2 km against a 64.8 km median, shortest 29.5 km; fraction 0.0298. Both assignments remain location hypotheses. The substitution changes a label point over an area, so this statistic cannot choose between them. Omitting one selected Jericho stop gives fractions spanning about 0.056–0.364. These are sensitivity descriptions across a defined family, without a new significance claim.

## Geometry limits and next measurements

“Adjacent” here means consecutive selected stops. Unplaced intervening entries remain omitted. Existing grouped labels `1,17` and `21,22` collapse separate textual entries into one stop; they do not establish continuous travel between consecutive entries. A continuous-itinerary model must preserve every textual slot, explicit revisits and unknown intervening locations.

Every coordinate denotes a site/area anchor. A reproducible uncertainty test should first distinguish coordinate-source error from uncertainty in associating a scroll entry with that site. Approximate `~100 m` statements and `area ~3 km` labels do not form calibrated probability distributions. For the legacy Jerusalem five-stop case, treating the listed point precisions as provisional radius bounds gives a conservative total-distance bound of approximately ±1.1 km by summing each edge's endpoint bounds; this is an illustrative deterministic bound, not a confidence interval. The area labels need actual footprints before equivalent bounds can be asserted. No mouth, threshold or deposit coordinate changes follow.

Next configured outputs:

1. Anchor provenance ledger: entry ID, edition/reading, candidate alternatives, coordinate source, footprint, phase, association grade, independence from sequence reasoning and exclusion rule. Freeze the ledger before comparing orders. No current “strict” legacy set meets a claim that every location is independently fixed.
2. Regional-group stability: preserve text order, measure same-region transitions and run lengths under the frozen alternative assignments, including unresolved labels. Report which boundaries persist across cases and which depend on Achor/Secacah assignments. Do not feed sequence-derived assignments back as observations.
3. Division sensitivity: prepare text-slot mappings for entry 9's two-part alternative; combined 12/12a; attachments around 40/41/42 and 49/50; Milik's phrase attachments at 22/23 and 50–55; and the three-part alternative for 56. Concordance records these differences. They do not alter physical scroll order; they can change adjacency and feature denominators. Current route pilot has not recomputed vocabulary/name tests under these alternatives.
4. Continuous-itinerary prediction: specify an open-route or revisit model, terrain/road assumptions and unknown-slot treatment before testing. Check held-out independently anchored sites; compare model predictions with evidence acquired independently of sequence. The current selected-stop comparison leaves a district-level continuous itinerary unsupported and supplies no exact location for unplaced entries.

## Completion criterion

Complete this measurement track when the frozen provenance ledger, explicit alternative division mappings, scenario outputs and held-out tests identify the grouping conclusions that survive those choices and the itinerary predictions that fail. Keep any geographic inference at the footprint scale justified by independent observations. Computational setup and repeat baseline reproduction remain separate from archaeological-source inspection and decisive-test KPIs.
