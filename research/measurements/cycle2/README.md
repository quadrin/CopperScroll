# Measurement follow-up, cycle 2

Reviewed 2 October 2026 UTC / 1 October Los Angeles. Input baseline `4a6c4434ff86f213aa2471351707ef2e8d7ab663`.

Three workers continued IV/17 annotation, Hyrcania source/dimension provenance and entry grouping in parallel. The integrator completed the actual Hyrcania datum/grid-cell calculation. Source images and third-party runtime packages remain outside Git.

- [IV/17 repeat](iv17_repeat_report.md): independent endpoint picks reproduce the first point measurements. Endpoint sensitivity slightly exceeds the first northern-mouth envelope. Preserve the frozen picks, corrected physical-feature labels and timestamp audit. Bearings remain relative to unspecified published north and measure local chord-normal proxies.
- [Hyrcania grid-cell test](hyrcania_grid_cell_report.md): actual datum conversion reproduces; neither conditional 100 m cell reaches the unchanged prediction. Nearest separation is about 175 m. This rejects quantization alone under the retained assumptions and leaves other registration errors unresolved.
- [Hyrcania dimensions](hyrcania_dimensions.md): original Fig. 22 is absent from current inputs. Published dimensions, old project picks and arithmetic retain separate provenance. Fresh boundary measurement awaits the original image.
- [Regional grouping](sequence_grouping.md): explicit frozen ledger, unknown slots and division stress cases. The project uses 61 canonical slots, including 12a. Coarse regional tags and current confidence grades constrain the result; preserve the independent-anchor and fine-district gaps.

From the measurement directory:

```sh
python cycle2/iv17_repeat_compute.py
python cycle2/hyrcania_dimensions_audit.py
python cycle2/sequence_grouping/measure_grouping.py
python cycle2/hyrcania_grid_cell.py
```

Only the final command requires `pyproj==3.7.2`. Each script uses recorded inputs and writes its own outputs. Regenerating the grouping ledger from original project records requires the pinned source files and freeze helper described in that packet; rerunning its measurements consumes the committed frozen ledger.

Accounting: two completed bounded tests—IV/17 point-measurement reproduction (supporting to its narrow scope, with incomplete envelope coverage) and Hyrcania quantization alone (conflicting under assumptions). No new primary target or decisive candidate test. Research totals become 18 primary targets / 5 map intakes / 19 bounded checks / 0 decisive tests / 0 closures. R08/R10 remain In progress; 9 questions In progress and 3 Queued. Preserve all six measurement tracks and pending source/phase dependencies.
