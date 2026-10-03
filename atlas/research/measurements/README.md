# Parallel measurement worklist

Current headline counters are [identification outcomes and coverage](https://github.com/quadrin/CopperScroll/blob/main/research/PROGRESS_METRICS.md). The following cycle/source totals are activity history; their growth does not establish stronger candidate identification.


Prepared 2 October 2026 UTC / 1 October 2026 Los Angeles. Baseline: `bb2fde4c76dbbe34b4c7345646acee049e875229`. Parent tracker: [open questions](https://github.com/quadrin/CopperScroll/blob/main/research/OPEN_QUESTIONS.md).

Six independent tracks now have defined measurements, source requirements, outputs and completion criteria. Five workers prepared the cave, gorge, registration and sequence packets concurrently; the integrator prepared the unit model. This session recorded an IV/17 plan pilot and three computational outputs. Twin Cave and fresh gorge geometry await survey inputs. Future runs are unscheduled.

1. **M01 — Twin Cave:** eight jobs cover opening dimensions, spacing, bearings, connectivity, pillar, northern datum, phase and geographic control. Published descriptions provide qualitative baselines. [Packet](twin_packet.md).
2. **M02 — IV/17:** Plan 5 gives a northern gap about 0.85 m, a southern remaining gap about 1.2 m and midpoint separation about 4.2 m. Local outward-normal proxies round to 125° relative to the unspecified published north, with broad manual bounds. Original southern aperture, survey north and ancient threshold remain unresolved. Independent endpoint repetition now supports point reproduction, with wider northern-mouth sensitivity; see cycle 2. [Packet](iv17_packet.md); [raw annotations](iv17_pilot.json).
3. **M03 — Qumran gorge:** five jobs distinguish tunnel path/chord, A/B identity, channel-head connections, reservoir-to-fissure direction and hydraulic/phase levels. Existing reported metres are recorded; the schematic gorge figure lacks metric calibration. [Packet](gorge_packet.md); [scalar schema](gorge_measurement_record.json).
4. **M04 — Hyrcania:** reproduce the residual between stored geographic points, audit conditional grid-notation sensitivity and define independent future control/hold-out rules. This retains the failed regional registration. Cycle 2 reproduces the datum computation; new accepted geographic registration remains pending. [Packet](registration_packet.md).
5. **M05 — Entry order:** sixteen deterministic distance scenarios reproduce legacy baselines and expose anchor sensitivity. Cycle 2 freezes the ledger and runs coarse division/grouping sensitivity; independent associations and fine districts remain pending. The legacy “strict” set includes low-confidence associations. [Packet](sequence_packet.md); [scenario manifest](sequence/manifest.json); [results](sequence/results.csv).
6. **M06 — Cubits and datums:** conditional unit sweeps give entry 11: 1.60–2.40 m; entry 25: 1.20–1.80 m; entry 26: 3.60–5.40 m. Each feature still needs its own datum, measured axis and phase. [Packet](units_packet.md); [output](unit_sensitivity.json).

The [machine-readable queue](queue.json) stores state, next action and completion criterion for each track. “Pilot recorded” describes the stated computation or annotation; phase compatibility and geographic registration have separate evidence requirements.

## Reproduce the recorded outputs

Run from this directory:

```sh
python unit_sensitivity.py
python hyrcania_registration_audit.py
python sequence/pilot.py
python iv17_measurements.py
```

These scripts use Python's standard library. The IV/17 script recomputes numbers from recorded pixel picks; independent redigitization requires the original source page, whose checksum and render are in its JSON. The Hyrcania audit uses stored WGS84 points; it does not rerun the EPSG transformation. Sequence inputs are pinned copies with hashes in the manifest.

## Parallel execution and updates

Each lane can continue while another awaits records. Geometry workers preserve independent annotations, method and outputs in their packet. The unit lane can consume a documented threshold after the cave or phase lane establishes it. The sequence lane can run independently of site-survey geometry.

A single integrator updates the queue, source/candidate notes, main tracker and atlas mirrors after reviewing outputs. Source-native plan coordinates remain separate from geographic coordinates. Preserve failed and inconclusive results. Retrieve originals through the source links in the packets when the supplied copies are unavailable.

Record setup progress separately: six tracks configured, four with recorded pilot/audit outputs, two with protocols and source requirements. After cycle 4, research totals are 21 primary targets / 5 cartographic intakes / 21 bounded checks / 0 decisive candidate tests / 0 closures. Reinspection, arithmetic and repeated computation add no primary observations. Any later counted test needs its explicit hypothesis, inspected evidence and result.

## Cycle 2 completed

[Follow-up reports and scripts](cycle2/README.md) record independent IV/17 point reproduction, actual Hyrcania datum/grid-cell analysis and 64 frozen coarse-grouping cases. Northern-mouth sensitivity expands; quantization alone leaves about 175 m discrepancy; coarse regional runs depend on confidence rules. Two bounded checks are completed. Surveys, ancient surfaces/phases and independent association evidence remain pending. The new exact datum calculation requires pyproj 3.7.2; the four original scripts above retain their standard-library implementation.


## Cycle 3 completed

[Field-record and independent-anchor checks](cycle3/README.md) identify IV/17 permit L-656 and Bar-Adon’s general fonds 717. IV/17’s survey coins still leave architectural contacts unresolved; Tell el-Qos remains weak/low after the independent name/phase audit. Added one scoped primary target and two inconclusive bounded checks. No fresh survey measurement, precise deposit point or question closure. The queue names the exact next records and retains the parked map searches.

## Cycle 4 completed

[Original-edition and Doq-plan intake](cycle4/README.md) verifies Puech’s reading/commentary to scope and corrects Amit’s plan locator to Fig. 2 on p. 224. Two scoped targets enter the ledger; no additional bounded check or measured geographic point. Full Amit chapter reload remains limited; Puech is readable. Wall/mountain and jar/deposit alternatives remain separate.


2 October 2026 Hyrcania update: original Fig. 22 is now recovered. A conditional page-up northern-pool offset pass is recorded in [the assessment](../assessments/entry29_hyrcania/README.md); centre/rim origins differ about 11 m. North validation, measuring datum, dated surface and geographic controls remain pending. Six-track setup/output counts remain unchanged.


## Parallel cycle 8 — 2 October 2026 UTC

[Doq and Siloam results, archive and access limits](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle8/README.md). Doq’s full chapter yields a conditional C-area building/pool target; Siloam’s textual and feature identities remain conditional, with no dated trough correspondence. Four scoped primary targets and four bounded checks added: totals 33 / 5 cartographic-reference intakes / 35 bounded checks / 3 conditional assessments / 0 decisive tests / 0 closures. Thirty-five original IAA figures archived and mirrored; image intake is not a research-target increment. No question-state, coordinate or confidence changes. Feldman’s anthology search remains parked; no outreach.

## Siloam original-source cycle 9 — 2 October 2026 Los Angeles

[Complete excavation/laboratory reading, correspondence and archive](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle9/README.md). Pool L102/L104 joins the 2013 stepped corner/L124/W50 chain; lower dam plasterL108 is distinct from later pool foundation. L103 provides a measured conditional outlet comparison. Ariel’s original catalogue remains403. Two full source targets and three bounded checks added: totals 35 / 5 cartographic-reference intakes / 38 checks / 3 conditional assessments / 0 decisive / 0 closures. Both originals and nine derivative figure/context pages archived and mirrored. No coordinate/grade/status changes or outreach.

## Siloam coin cycle 10 — 2 October 2026 Los Angeles

[Original coin catalogue, context and phase audit](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle10/README.md). Foundationcoin 20/L105/1092 is year four (69/70 CE); fill coin 19 is equally late. The published foundation context supports a post-minting construction terminus; exact completion and sealing require archaeological upper bounds. One full source/one bounded check added: totals 36 / 5 cartographic-reference intakes / 39 checks / 3 conditional assessments / 0 decisive / 0 closures. Article original and two derivative pages archived and mirrored. No geographic/grade/state changes or outreach.



## Parallel cycle 11 — 3 October 2026 UTC integration

Inspections completed 2 October. Two new scoped primary targets and three bounded checks: cumulative 38 / 5 cartographic-reference intakes / 42 bounded checks / 3 conditional assessments / 0 decisive tests / 0 closures / 0 confirmed individual deposits. Strict L103 hollowed-stone model conditionally excluded; broader gutter comparison remains conditional. Earlier-pool proposal and new dam dates supply no replacement for L105 construction terminus. Doq has an exact publication lead but no verified room-plan coverage. Original Regev figures and four Netzer pages archived and mirrored; Meshel attribution corrected. All 9 In progress / 3 Queued states, coordinates and site grades retained. [Results and unread links](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle11/README.md).


## Source recovery cycle12 — 3 October 2026 UTC / 2 October Los Angeles

One new scoped primary target and one bounded coverage check; cumulative 39 / 5 cartographic-reference intakes / 43 bounded checks / 3 conditional assessments / 0 decisive tests / 0 closures / 0 confirmed deposits. The 2024 original/image audit upgrades existing evidence without recounting it. Netzer 2006 narrows Doq publication priority; actual room records remain unresolved. Appendix attachment validated as HTML. Larger Regev figures, browser capture, full 2024 report and Netzer page extract archived and mirrored. Nine In progress / three Queued states, coordinates and site grades unchanged. [Results and remaining links](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle12/README.md).


## Appendix recovery cycle13 — 3 October 2026 UTC / 2 October Los Angeles

Genuine three-page extended-methods appendix recovered, fully image-checked and archived unchanged. Collection controls and reported W114/W001 attachment documented; small-pool L105/L108/L103 joins remain unreported. One scoped primary target / one bounded collection-control check added: cumulative 40 / 5 cartographic-reference intakes / 44 bounded checks / 3 conditional assessments / 0 decisive tests / 0 closures / 0 confirmed deposits. No new field campaign, R-question state, coordinate or grade change. [Result and original](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle13/README.md).


## Parallel wording/merged-basin cycle14 — 3 October 2026 UTC / 2 October Los Angeles

Two original-source scopes and two bounded checks added: cumulative 42 primary targets / 5 cartographic-reference intakes / 46 bounded checks / 3 conditional assessments / 0 decisive tests / 0 closures / 0 confirmed deposits. Milik1960 supplies a pipe/bathing-pool branch without an explicit masonry argument; strict Puech hollowed-stone exclusion of exposed L103 remains conditional. Netzer documents a Herodian eastern outlet but leaves merged-pool supply unknown. Rounded basin dimensions allow both 24/27-cubit counterfactuals without locating a channel datum. Nine In progress / three Queued states, coordinates and grades unchanged. New encountered Netzer source pages archived and mirrored. [Results, calculations and individual missing sources](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle14/README.md).


## Parallel function/direction cycle15 — 3 October 2026 UTC / 2 October Los Angeles

One fresh Milik1960 entry29 source scope and two bounded checks added: cumulative 43 scoped primary targets / 5 cartographic-reference intakes / 48 bounded checks / 3 conditional assessments / 0 decisive tests / 0 closures / 0 confirmed deposits. Siloam’s small receiving pool has a published storage/overflow interpretation and no established bathing function. Milik’s in-pool/under-pipe relation requires the selected pool identity; a separate main-pool model needs its own function and spatial check. Jericho’s available wording does not fix hydraulic direction, leaving the Herodian outlet admissible without positive identification; Puech’s collecting-installation restoration remains conditional. Nine In progress / three Queued states, coordinates and grades unchanged. No new spatial assets: encountered figures are already archived. [Results, original-page controls and missing-source links](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle15/README.md).


## Counter redesign — 3 October 2026 UTC / 2 October Los Angeles

Reclassified43 source scopes and48 bounded checks as activity. Initial outcome ledger registers0 discriminated identifications,0 whole-candidate exclusions,3 inconclusive formal packets,2 conditional L103 model exclusions and2 nonunique comparator results. Four target-coverage records establish no verified fully excavated target or negative target excavation. Unexcavated-alternative totals, candidate excavation status distribution, regional coverage and independent observations remain unaudited; landscape-wide rarity remains unmeasured. No new source/check count, question closure, coordinate or grade change. [Definitions and ledger](https://github.com/quadrin/CopperScroll/blob/main/research/PROGRESS_METRICS.md).
