# W2B outputs, v2 inputs (two new candidates)

**What it is.** Outputs of the K2-default model on `../inputs_v2/` (v1 plus entry 60 at kh_qumran and entry 25 at Abu Saraj IV/17), written by `research/models/search_effectiveness/run_v2.py`.\
**Main result.** P(25 at IV/17) = 0.180 and P(60 at kh_qumran) = 0.033 (v1 0.013); the method, sensitivity and caveats are in [README_v2.md](../../../../models/search_effectiveness/README_v2.md).\
**What stays unknown.** Both identifications; nothing in v1 or `outputs_fixed/` changes.

| File | What it is |
|---|---|
| `repro_v1/` | The v2 runner on the unchanged v1 inputs: `kernel_sensitivity.csv`, `v0_reproduction_check.json` and `check.json` (comparison with `../outputs_fixed/`) |
| `entry_tv_v2.csv` | Total variation against v1 for every entry: place only (B), + entry 25 (C), + entry 60 (D), v2 (E) |
| `posteriors_v1_v2.csv` | Posterior per entry and state, v1 and v2 (states at or above 0.001 in either) |
| `kernel_sensitivity_v2.csv` | The 15 `check_order_kernel.py` configurations on v1 and v2, with P(60 at kh_qumran) and P(25 at IV/17) |
