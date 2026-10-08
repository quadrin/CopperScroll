# Decision queue

`plans.json` specifies seven exact record dependencies and four possible outcomes for each. The evaluator imports all six tracks from `research/measurements/queue.json` unchanged, with the source hash and original dates. Historical execution states and counters remain historical.

The atlas can select `data.tasks[].id`, then an item in `outcomes[]`. `preview()` returns **Possible outcome — not observed**, the conditional consequence and the unchanged current evidence. It never records the selected outcome, sends a request or reopens a closed test. The generated `results` use only each task's recorded evidence status; all seven currently remain unknown.

Run from the repository root:

```sh
python research/feature_workbench/decisions/evaluate.py
python research/feature_workbench/decisions/evaluate.py --task decisions-xii10 --outcome one-sequence
python -m unittest discover -s research/feature_workbench/decisions -p 'test_*.py'
```

The record dependencies are Manchester XII10; IV/17 permit L-656 and baskets656.17/656.20; Kallai1972 pp.172–173; Kenyon's separate eastern section and Plate111b; and phase-controlled Jericho, Siloam and Wadi hydraulic contacts. Priorities are qualitative, with reasons and access/effort fields. They contain no numerical information-gain or confidence estimates.

The IAA inquiry already sent concerns the regional cave inventory. It is a related pending request, not a verified L-656 request or file holding. Manchester, Jericho, Siloam and Wadi sent-request records retain unverified delivery/replies. Kallai originals and Kenyon's referenced drawings remain uninspected; Kenyon III's text and the Wadi report are already inspected.

XII10's letter protocol is frozen at `fd3f334ea2a40c0f8e99921ef663f8b126112fe1`; its unused-observation status remains unverified. Other archaeological decisions here are planning branches. Before a reserved observation is used, the finite feature/reading/phase/datum/axis/unit/tolerance choices and decision rule need an actual freeze and exposure audit. Compatibility alone supplies no identification.

No original source is newly inspected, no activity count changes, and no correspondence, purchase, delivery check or parked acquisition is performed. A future record may resolve only part of a dependency; missing documentation and unexposed contacts remain unknown. A negative deposit conclusion still requires an ancient target volume, phase/datum, excavation reach, disturbance and detection limits.
