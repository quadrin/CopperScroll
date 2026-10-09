# Feature workbench

Five source-linked research tools implement methods 2–6 using records already reviewed in this repository. The [atlas Research tools view](https://quadrin.github.io/CopperScroll/#workbench/relationships) exposes the same generated results. These are exploratory evaluations; compatibility is not identification support. No manuscript observation, source-inspection counter, confirmed feature, deposit location or outcome-ledger increment is added.

| Method | Pilot | Reusable operation |
| --- | --- | --- |
| [2. Relationships](relationships/README.md) | Koḥlit: Entry 11 pool and Entry 60 pit/grave branches | Evaluate source-derived predicates against explicit feature assignments and two saved period windows. Preserve all 40 retained combinations and conditional contradictions. |
| [3. Inventory](inventory/README.md) | Entry 25: IV/17, IV/11 and Twin Cave | Apply four reported-form and 96 digging-prerequisite branches equally to all three controls. Unknown observations never become absent features. |
| [4. Historical states](states/README.md) | IV/17 architecture, Jericho north and spring features | Separate observed remains, use reconstructions, construction dates, relative sequence and accessibility. Render only native source-plan aperture chords. |
| [5. Coverage](coverage/README.md) | Jericho pool notices and IV/17 | Import 28 documentary notices, twelve sectors and 21 coverage obligations. Evaluate target-specific excavation/datum/phase/disturbance/detection gates. |
| [6. Decisions](decisions/README.md) | Seven discriminating record dependencies | Import the six historical tracks unchanged; explore 28 unrecorded possible outcomes with conditional consequences, access, effort and qualitative priorities. |

The Koḥlit relationship pilot keeps the SWP historical irregular basin separate from the reservoir built in 1898. Kallai's pool remains unlocated. Later quarrying establishes a grave-before-pit sequence without dating early pit accessibility. The cave catalog treats opening widths as measurements; Entry 25's three cubits belong to the digging instruction. Every digging-target branch remains unknown because origins, datums or phase contacts are missing. The regional eligible denominator and geographic coverage remain null.

[Shared research tools](../shared_tools/README.md) add local source retrieval, manuscript correspondence queries, entry/control adapters, calibration diagnostics and review/capture preparation.

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

The [active test](../ACTIVE_TEST.md) remains authoritative. Existing Manchester, IAA and hydraulic-record inquiries retain their recorded scope/status; L-656's holding, accession and specific field-file request remain unverified. No new correspondence, fee, scan order or fieldwork was initiated. Parked A(C)94 geometry and acquisition remain parked. A future claim needs its own finite specification, failure rule and exposure audit before genuinely unused evidence is revealed.

The interface provides saved exploratory queries, native-state views, coverage gates, provenance and a planning-only outcome selector. It supplies no precise field location or detection probability. A registered world overlay, complete regional roster, phase-controlled contacts and unused observation remain evidence dependencies.
