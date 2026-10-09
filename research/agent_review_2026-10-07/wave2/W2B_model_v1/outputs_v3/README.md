# W2B outputs, v3 inputs (documented Peraea places for Goranson's Transjordan)

**What it is.** Outputs of the K2-default model on `../inputs_v3/`: the `transjordan` proxy (two 15-km points at Machaerus and Amathus) replaced by an equal-weight mixture of 12 documented Second Temple sites of Peraea. Written by `research/regional/peraea/scripts/run_v3.py` under the frozen [PLAN_v3.md](../../../../regional/peraea/PLAN_v3.md).\
**Main result.** P(entry 60 at transjordan) rises from 0.0025 to 0.0089; the Koḥlit entries 4-19 move the same way (0.0019-0.0030 to 0.0075-0.0092). No entry moves by more than 0.01 in total variation.\
**What stays unknown.** Whether Koḥlit lay east of the Jordan. These are model outputs under stated assumptions, not probabilities that the identification is right.

| File | What it is |
|---|---|
| `repro_v2/check.json` | R0: the switched-off v3 build is byte-identical to inputs_v2, and the runner reproduces `../outputs_v2/posteriors_v1_v2.csv` (3,199 values, largest difference 0) |
| `kohlit_v3.csv` | Entries 4, 11, 15, 19, 60 and the Koḥlit latent: P(transjordan), P(region TRANSJ), P(U_TRANSJ), TV against v2 and V3P, top 3 states, for v2, V3P and S1-S4 |
| `entry_tv_v3.csv` | Total variation against v2 for every entry and variant |
| `posteriors_v2_v3.csv` | Posterior per entry and state, v2 and V3P (states at or above 0.001 in either) |
| `kernel_grid_v3.csv` | The 15 `check_order_kernel.py` configurations on v2 and V3P (entry 60) |
| `results_v3.json` | All outputs, rounded to 8 decimals |

The method, sensitivity runs and caveats are in the [Peraea README](../../../../regional/peraea/README.md).
