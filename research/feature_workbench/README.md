# Feature workbench

Five source-linked research tools implement methods 2–6 using records already reviewed in this repository. The [atlas Research tools view](https://quadrin.github.io/CopperScroll/#workbench/relationships) exposes the same generated results. These are exploratory evaluations; compatibility is not identification support. No manuscript observation, source-inspection counter, confirmed feature, deposit location or outcome-ledger increment is added.

| Method | Pilot | Reusable operation |
| --- | --- | --- |
| [2. Relationships](relationships/README.md) | Koḥlit: Entry 11 pool and Entry 60 pit/grave branches | Evaluate source-derived predicates against explicit feature assignments and two saved period windows. Preserve all 40 retained combinations and conditional contradictions. |
| [3. Inventory](inventory/README.md) | Entry 25: IV/17, IV/11 and Twin Cave | Apply four reported-form and 96 digging-prerequisite branches equally to all three controls. Unknown observations never become absent features. |
| [4. Historical states](states/README.md) | IV/17 architecture, Jericho north and spring features | Separate observed remains, use reconstructions, construction dates, relative sequence and accessibility. Render only native source-plan aperture chords. |
| [5. Coverage](coverage/README.md) | Jericho pool notices and IV/17 | Import 28 documentary notices, twelve sectors and 21 coverage obligations. Evaluate target-specific excavation/datum/phase/disturbance/detection gates. Target-volume/footprint joins: entry 25 at IV/17 and entry 60 at Tell es-Sultan; all 12 branches undeterminable. |
| [6. Decisions](decisions/README.md) | Seven discriminating record dependencies | Import the six historical tracks unchanged; explore 28 unrecorded possible outcomes with conditional consequences, access, effort and qualitative priorities. Discrimination: model classes, worst-case and decisive-outcome separating sets; first rank XII 10, then Kenyon and Kallai. |

The Koḥlit relationship pilot keeps the SWP historical irregular basin separate from the reservoir built in 1898. Kallai's pool remains unlocated. Later quarrying establishes a grave-before-pit sequence without dating early pit accessibility. The cave catalog treats opening widths as measurements; Entry 25's three cubits belong to the digging instruction. Every digging-target branch remains unknown because origins, datums or phase contacts are missing. The regional eligible denominator and geographic coverage remain null.

[Shared research tools](../shared_tools/README.md) add local source retrieval, manuscript correspondence queries, entry/control adapters, calibration diagnostics and review/capture preparation.

The [case-study extensions](../shared_tools/README.md#case-study-methods) add exact feature witnesses, minimum separating-observation sets, source-grounded recovery, letter-control eligibility, repeated text constraints and a negative-notice/registration audit. Their saved results are available through `python research/shared_tools/cli.py methods`; each report retains its evidence and exposure limits.

## Applied comparisons — 12 October 2026

The [book-to-feature application](book_application_2026-10-12/README.md) joins source facts to individual structures and phases: Atara’s western conduit stays separate from its eastern pool, and Absalom’s original southern access stays separate from the later western breach and compound Jehoshaphat chambers. Cave construction/accessibility dates remain unresolved. Every applied row identifies its source, inherited clause, phase, uncertainty and next observation.

The [entry-46 alternatives](../text/entry46_alternatives_2026-10-12/README.md) evaluate pool/deep-pit, distance/depth and ten-small-pits branches equally across source records. Native Ramat Rahel and Naḥal En Kerem reports audit the feature identities and map-reference extents; a report-wide extent cannot supply a metre-precise installation point.

The [measurement resolution audit](measurement_resolution_2026-10-12/README.md) preserves failed plan checks, quantifies conditional resolution requirements and corrects the same-document picking-only shortcut. The [inventory-role comparison](../comparanda/inventory_forms_2026-10-12/README.md) separates numbered places, objects/lots, counts, contents measures and retrieval instructions. Herodium’s roles remain tentative. Each report records the observation that would distinguish its alternatives; exposed records supply no independent identification.

## Inputs and register

`features.json` holds stable physical-feature identities. A documentary notice is not automatically a physical feature, and an alias or interpretation is not silently merged. Each module's reviewed inputs remain in its own directory. The [contract](CONTRACT.md) defines the source, observation, historical-state and result records. Exact source pages/figures, inspection scope, original observation lineages, native frames, uncertainty and missing data travel with the result.

`build.py` runs all five standard-library evaluators, rejects duplicate IDs and unresolved feature/source references, and writes:

- `register.json`: shared features, sources, observations and historical states.
- `results.json`: the reviewed exploratory results and every retained module branch.
- `../../atlas/app/atlas-workbench.json`: an identical atlas snapshot, loaded only when the workbench opens.

Rebuild and check from the repository root:

```sh
python3 research/feature_workbench/build.py
python3 research/feature_workbench/check.py
```

After changing the interface or snapshot, rebuild Pages from `atlas/`:

```sh
corepack pnpm run build:pages
node scripts/check-workbench.mjs
```

The tests check false contradictions, finite/context-bound datums, phase mismatches, source-frame safety, equal control opportunities, notice/lineage deduplication, source supersession, and immutable hypothetical decisions. Generated files are deterministic and must pass `build.py --check`.

## Research status

The [active test](../ACTIVE_TEST.md) remains authoritative. The L-656 field-file request was sent on 11 October; its holding/accession remains unverified. On 12 October Rachel Bar-Nathan reported holding unorganized Jericho field notes and requested a call; the wall-junction drawing and level register have not arrived. Manchester’s TPA/1/132 route supplies general material without cutting photographs or research notes, while the archivist continues the Allegro inquiry. The [access records](../agent_review_2026-10-07/followup/F_outreach_sent.md#archive-replies--12-october-2026) and [A(C)94 custody update](../assessments/entry29_jericho_pools/netzer2001-first-pass.md#field-notes-holder-response--12-october-2026) distinguish these routes from supplied observations. A future claim needs its own finite specification, failure rule and exposure audit before genuinely unused evidence is revealed.

The interface provides saved exploratory queries, native-state views, coverage gates, provenance and a planning-only outcome selector. It supplies no precise field location or detection probability. A registered world overlay, complete regional roster, phase-controlled contacts and unused observation remain evidence dependencies.
