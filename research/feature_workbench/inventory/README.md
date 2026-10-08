# Entry 25 inventory queries

This pilot applies one saved branch set to IV/17, IV/11 and Twin Cave. It imports already reviewed evidence into a reusable catalog and evaluates necessary predicates as compatible, contradicted or unknown. It uses no numerical candidate score.

`catalog.json` records the source, evidence kind, feature state and reference frame for each property. `queries.json` records the retained dimensions. `evaluate.py` exposes `build(repo_root)` for the workbench and reusable `evaluate_predicate`, `expand_branches` and `evaluate_query` functions. It fails on selected reviewed-quantity drift rather than silently adopting a changed measurement.

The reported-form query applies four landmark/aspect combinations to every cave. IV/17 is compatible with the pillar/cave-aspect branch; its stricter individual-mouth aspect remains unknown. Twin Cave is compatible with both pillar/aspect branches in the published description. IV/11 supplies an internal pillar but no established exterior pair. All platform/terrace branches remain unknown. These outcomes concern reported form, not ancient identification or landscape rarity.

The target-prerequisite query applies 96 combinations per cave: two landmark readings, two eastward attachments, three cubit sensitivity samples, two distance interpretations, two feature-state choices and two deposit antecedents. The 0.40/0.50/0.60 m samples yield conditional distances of 1.20/1.50/1.80 m. The instruction concerns digging distance or depth and supplies no entrance-width criterion. Deposit alternatives change the predicted assembly; they do not require discovery of a jar to identify a cave feature.

Every target branch remains unknown. A vertical model lacks a registered northern threshold elevation/datum; a horizontal model lacks a registered origin and declared path. The ancient-state branches also lack dated architectural contacts. Reported cave heights, cavity dimensions, general excavation depths, later floor levels and source-plan aperture widths cannot fill these gaps.

The reusable threshold gate requires a finite scalar elevation in metres, the queried phase, and an explicit feature binding to `candidate.reference_features.northern_opening`. A threshold record must also name a local vertical `datum` with `id`, `reference_point`, `reference_frame` and `positive_direction: "up"`; that frame must match the observation's reference-frame label or ID. A local benchmark is sufficient for a local symbolic height relation and supplies no world coordinates. Boolean flags, nonfinite numbers, placeholder strings, a different mouth, an unregistered datum or a mismatched frame remain unknown. Generic `known` predicates can still accept structured horizontal origins and paths.

The observed 0.8 m IV/17 opening report and derived 0.859 m plan chord remain distinct. Plan-chord normals are not true or passage bearings; endpoint sensitivity is not a statistical confidence interval. The edition provides no angular tolerance. Connectivity is not a mandatory predicate: a continuous route in a two-dimensional plan supplies no clearance or ancient traversal observation.

All evidence is exposed exploratory material. The three caves are previously examined controls, not a regional census. The regional boundary, eligible denominator and coverage completeness remain unknown. There is no unused prediction, deposit point, deposit-existence inference, ranking, new source inspection, research-counter increment or reopening of a parked test.

Run from the repository root:

```sh
python3 -m unittest discover -s research/feature_workbench/inventory -p 'test_*.py'
python3 research/feature_workbench/inventory/evaluate.py --repo-root .
```

The tests exercise missing-versus-absent evidence, frame/unit/phase eligibility, finite threshold quantities and datum/feature binding, interval overlap, all-control branch equality, retained contradictions, and the prohibition on converting three cubits into a width test. They also check that no complete target is emitted from the available catalog.
