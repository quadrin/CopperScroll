# Parallel measurement worklist

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
