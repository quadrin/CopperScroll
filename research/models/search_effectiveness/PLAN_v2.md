# Plan for the two new model candidates (v2), frozen before any model run

Written 9 October 2026, about 21:25 UTC. When this file was frozen, this worker had run no model: not the W2B model on v1 or v2 inputs, and not the search-effectiveness layer. Only the inputs were built (`inputs_v2/build_inputs_v2.py`, `build_looks_v2.py`). Exploratory. No decision rule. Every output below is reported whatever it shows.

## Inputs (W2B `inputs_v2/`, suffix `v2`)

v2 = v1 bytes plus these rows only. Hashes are in the JSON block.

- `places_v2.csv` + `iv17_abu_saraj`: 31.89009, 35.42477 (OIG 190300/144150 through W2B `grid_convert.oig`), sigma 0.3 km, region JERICHO, `coords_in_places_json` no.
- `candidates_v2.csv` + `60,kh_qumran,possible,weak,no,,…,xii10!=janoah,no`
- `candidates_v2.csv` + `25,iv17_abu_saraj,possible,low,no,,…,,no`
- `grid_conversions_v2.csv` + the IV/17 group reference.
- `looks_v2.csv` (this folder) = `looks.csv` with `place_id` of L43 and L44 changed from U_JERICHO to iv17_abu_saraj.

## Label choices

The model's scale: confidence unknown, weak, low, medium, high (p = 0, 0.1, 0.3, 0.6, 0.85); status weak, possible, preferred (× 0.5, 1, 1.5). Odds = p/(1 − p) × status. Rule for both rows: give the new candidate the label of the entry's existing candidates, so the inputs add a state but do not rank it.

1. Entry 60 at kh_qumran: possible / weak (odds 0.111), as each of the ten published Koḥlit proposals in the default.
   - Basis: chain.json M-QUMRAN has three compatible steps, all used to select the model. The rarity count lists Qumran among the two-of-three units (C2 and C3 survey MATCH, C1 UNKNOWN; C3 single-coded) and finds rarity not measurable (m ≫ k).
   - order_derived no: the rarity screen selected it (R2 = 30 km around Kh. Qumran, the find-spot), not the entry order.
   - conditional_on_reading `xii10!=janoah`: only the Janoaḥ reading moves the pit away from Koḥlit (D-E60-SECOND-WORD). Same gate as the ten proposals.
   - kohlit_proposal no: no edition proposes Qumran for Koḥlit. The loader then always uses the row's label, under any `kohlit_scheme`.
2. Entry 25 at iv17_abu_saraj: possible / low (odds 0.429), as the entry's only v1 candidate (kh_qumran, possible/low, order-derived "likely").
   - Basis: entry25_iv17 "feature-level compatibility; identification inconclusive"; no ranking; Twin Cave and IV/11 are controls.
   - order_derived no: the row rests on Sion's reported form; the assessment says the entry sequence adds no corroboration.
   - conditional_on_reading empty: the pillar/terrace and aspect alternatives are not model readings.
3. Place: sigma 0.3 km because 19030/14415 is a cave-group reference shared by several caves, with no stated extent (INFERENCE). Region JERICHO: the model's region for the escarpment (doq = Jebel Qarantal, ain_duk).

## Runs

All runs use `joint_model_v1.cfg_with()` (K2 "fixed", rho 0.9, w_A 0.4, w_L 0.995, kohlit_scheme None, XII 10 milik_puech) unless stated.

- R0 reproduction, before R1: the v2 runner on the unchanged W2B `inputs/` (v0 and v1) must give `kernel_sensitivity.csv` and `v0_reproduction_check.json` byte-equal to `outputs_fixed/`. Compare the hashes in `kernel_validation.json` with the files used. The layer wrapper on v1 inputs and `looks.csv` must equal `results.json`.
- R1 decomposition: A = v1; B = v2 without the two new candidate rows (place only); C = B + entry-25 row; D = B + entry-60 row; E = v2.
- R2 label sensitivity on E, one row at a time: confidence one step down and up (status fixed), then status one step down and up (confidence fixed). Entry 60: unknown (odds 0, row inert), low; status weak, preferred. Entry 25: weak, medium; status weak, preferred. The confidence steps are the primary sensitivity.
- R3 sigma of iv17_abu_saraj: 0.1 and 0.5 km.
- R4 the 15 `check_order_kernel.py` configurations on v2, with P(60 at kh_qumran) and P(25 at iv17_abu_saraj) added.
- R5 search-effectiveness layer: `run_analysis.analyse` (imported, unedited) with PLAN.md scenarios and reading sets, on v2 with `looks.csv` and with `looks_v2.csv`.

## Reported quantities

- Entries 25 and 60: probability of the new state, top states and region masses in A–E.
- Koḥlit group (4, 11, 15, 19, 60): probability at the ten proposals and kh_qumran, region masses, total variation (TV) against A, and the group latent's top states.
- Every entry with TV(A, E) > 0.01, with its TV for B, C and D.
- R2 and R3: probability of the new state and TV against E and against A for entries 25 and 60, the Koḥlit group and the most moved other entry.
- R5: double-counting status of L42, L43 and L44; whether any reported row adds a factor; factors below 1; TV of S0 against S4 for the Koḥlit entries and entry 25; probes.

TV is taken over the union of states; a state missing from an input set has probability 0 there. Numbers are rounded to 8 decimals.

## What would count as a coding error

A wrong coordinate, a label that differs from this plan, or a row added or changed beyond the list above. A fix is logged in README_v2.md with the new hash, and both runs are reported.

```json
{
 "plan_id": "model-candidates-v2-2026-10-09",
 "model": "research/agent_review_2026-10-07/wave2/W2B_model_v1/scripts/joint_model_v1.py, cfg_with() defaults (K2)",
 "tv_report_threshold": 0.01,
 "rounding_decimals": 8,
 "decomposition": {"A": "v1", "B": "v2 minus both new candidate rows", "C": "B + entry 25 row", "D": "B + entry 60 row", "E": "v2"},
 "label_steps": {
  "60|kh_qumran": {"main": ["possible", "weak"], "conf_down": ["possible", "unknown"], "conf_up": ["possible", "low"], "status_down": ["weak", "weak"], "status_up": ["preferred", "weak"]},
  "25|iv17_abu_saraj": {"main": ["possible", "low"], "conf_down": ["possible", "weak"], "conf_up": ["possible", "medium"], "status_down": ["weak", "low"], "status_up": ["preferred", "low"]}
 },
 "sigma_km": {"main": 0.3, "sensitivity": [0.1, 0.5]},
 "frozen_inputs_sha256": {
  "inputs_v2/candidates_v2.csv": "f8d70eb7fda81a8cbbc07bfaa22a8c48785dc423e73e0d989139c717cf51b2a5",
  "inputs_v2/entries_v2.csv": "7fa03e97ed46e6b4bcb550538be815bc99b7a5c2b08700c11551586d3b2c31b0",
  "inputs_v2/grid_conversions_v2.csv": "cc471959c0c66cfec87dc5472b13d4e52cded3995a9a8baaf469252ad6aab7a8",
  "inputs_v2/kohlit_proposals_v2.csv": "21001790432bcca973bb7dd8464cb407a3647893e6db06c0db80ae9bab963feb",
  "inputs_v2/name_groups_v2.csv": "82a7d44b299ee6f7ccf3b43a14aad6d4b429f7a264a11ce0e012831a02b2cc28",
  "inputs_v2/places_v2.csv": "315474bd3be8cce3e1776e119417e2444edd99e3f028c7413185302fc7663683",
  "inputs_v2/additions_v2.json": "688a1e1f29d1a4c2dcaa4ba010b273877ec7fb0114aa9fc506427a6b563a7523",
  "looks_v2.csv": "14595c45c369712fe03a921b38b58f143a153fecc2fb4b649bf5a4875362e994"
 }
}
```
