# Two new candidates in the joint placement model (v2)

**What it is.** A v2 input set for the W2B joint placement model (K2 default) that adds entry 60 at Kh. Qumran (the project's own M-QUMRAN model) and entry 25 at Abu Saraj cave IV/17, with a rerun of the search-effectiveness layer.\
**Main result.** Entry 25 puts 0.180 on IV/17 (Kh. Qumran falls from 0.545 to 0.448); entry 60 puts 0.033 on Kh. Qumran (v1 0.013), now its highest listed place but below the unlisted Jerusalem state (0.186). The Koḥlit entries move by 0.023–0.032 (total variation). About 40–50% of that, and nearly all the change in 12 other entries, appears when the place is added with no new evidence. L42 is now counted once, through the candidate odds; L43 too once the look is coded at the new place; no double counting appears in the layer.\
**What stays unknown.** Whether either place is the right one. Both labels are set equal to the entry's existing candidates; entry 25's result depends strongly on that label (0.054–0.435). This identifies nothing.

Exploratory method work, 9 October 2026. No registered result, outcome count or identification changes. The W2B v1 inputs, scripts, outputs and reports, and the layer's own files, are unchanged. Labels: EVIDENCE (what a source or a model output says), INFERENCE (our reasoning).

## Freeze record

- PLAN_v2.md SHA-256: `7219e6bfeb1cc3d67f6e94a5efb6a822c256b63ca38570f7c9d16600f1bd4c04`, frozen 2026-10-09T21:21:57Z. No model had been run by this worker before that time. The inputs had been built; their hashes are inside PLAN_v2.md.
- One deviation. PLAN_v2 R0 asked for byte equality with `outputs_fixed/kernel_sensitivity.csv`. 22 of 30 rows are byte-equal; 8 differ in the last digits (largest difference 1.4 × 10⁻¹⁴). W2B's own `check_order_kernel.py`, run here, gives exactly the same bytes as the v2 runner. So the difference is floating-point round-off of this machine (numpy 2.5.3, OpenBLAS 0.3.34), not the runner. The run accepted R0 at a tolerance of 10⁻¹² plus byte equality with W2B's script run here.
- No input, label or run changed after the freeze. `run_v2.py` and the tests were written after it. `build_inputs_v2.py` was later edited only to close its files; its output is byte-identical (`--check`).

## What was added

Inputs live in [`W2B_model_v1/inputs_v2/`](../../agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/). `build_inputs_v2.py` copies the v1 bytes and appends the declared rows. `additions_v2.json` lists the rows and the hashes. `entries`, `name_groups` and `kohlit_proposals` are byte copies.

| File | Added row |
|---|---|
| places_v2.csv | `iv17_abu_saraj`: 31.89009, 35.42477; sigma 0.3 km; region JERICHO |
| candidates_v2.csv | `60,kh_qumran,possible,weak,no,,…,xii10!=janoah,no` |
| candidates_v2.csv | `25,iv17_abu_saraj,possible,low,no,,…,,no` |
| grid_conversions_v2.csv | the IV/17 group reference 190300/144150 |
| looks_v2.csv (this folder) | L43 and L44: `place_id` U_JERICHO → iv17_abu_saraj; nothing else |

**The coordinate.**
- EVIDENCE: Sion 2002 (ʿAtiqot 41, Hebrew p. 61, Fig. 12) gives the cave group the Old Israel Grid reference 19030/14415. The [entry 25 assessment](../../assessments/entry25_iv17/README.md) says it locates the shared group, not the mouths.
- The conversion uses W2B's own `scripts/grid_convert.py` `oig()` (EPSG:28191 to WGS84), imported and not edited. It reproduces all seven W2B grid conversions.
- Control: Tell es-Sultan's WBADB anchor, OIG 192150/142050, lands 0.07 km from the model's `tell_es_sultan`. W2B's first control (Kh. Qumran, NEAEHL) lands 0.005 km from `kh_qumran`.
- IV/17's group point lies 1.07 km from `ain_duk`, 1.79 km from `doq` and 2.77 km from `tell_es_sultan`.
- INFERENCE: sigma 0.3 km. Several caves share the reference, and their extent is not stated. 0.3 km is the class the model gives other cliff and spring places (doq, ain_duk). Sigma 0.1 or 0.5 km changes P(25 at IV/17) by less than 0.001.
- Region JERICHO: the model's region for the escarpment. It holds doq (Jebel Qarantal) and ain_duk.

## Label choices and why

The model's scale: confidence unknown, weak, low, medium, high (p = 0, 0.1, 0.3, 0.6, 0.85); status weak, possible, preferred (× 0.5, 1, 1.5); odds = p/(1 − p) × status. One rule for both rows: the new candidate gets the label of the entry's existing candidates. The inputs then add a place without ranking it.

| Field | Entry 60 at kh_qumran | Entry 25 at iv17_abu_saraj |
|---|---|---|
| status / confidence | possible / weak (odds 0.111): the label of each of the ten published Koḥlit proposals | possible / low (odds 0.429): the label of the entry's only v1 candidate (kh_qumran) |
| Repository basis | [chain.json](../../assessments/kohlit_chain/chain.json) M-QUMRAN: three compatible steps, all used to select it. Rarity count: two of three (C2 caves north, C3 northern cemetery, de Vaux 1973 pp. 57–58); C1 UNKNOWN; C3 coded by one coder; rarity not measurable | Assessment: "feature-level compatibility; identification inconclusive"; no ranking; Twin Cave and IV/11 are controls |
| order_derived | no: the rarity screen chose it (R2 = 30 km around Kh. Qumran, the find-spot), not the entry order | no: it rests on Sion's reported two mouths and pillar; the assessment says the sequence adds no corroboration |
| conditional_on_reading | `xii10!=janoah`: only the Janoaḥ reading moves the pit away from Koḥlit (D-E60-SECOND-WORD); the ten proposals carry the same gate | empty: the pillar/terrace and aspect alternatives are not model readings |
| kohlit_proposal | no: no edition proposes Qumran for Koḥlit. The source column says "Project model, not a published Kohlit proposal". The loader then always uses the label, under any Koḥlit odds scheme | no |

How the loader uses these fields (`joint_model_v1.py` `evidence()`): rows with `kohlit_proposal = yes` take their odds from a `kohlit_scheme` when one is set (and drop to 0 if the place is not in it); other rows use status and confidence. `order_derived` decides which exclusion list applies. A false condition switches the row off. Tests check each case.

## Results (K2 default, XII 10 read with Milik and Puech)

### R0. Reproduction first

- `v0_reproduction_check.json`: byte-equal to `outputs_fixed/`.
- `kernel_sensitivity.csv`: equal to round-off (see the deviation above); [check.json](../../agent_review_2026-10-07/wave2/W2B_model_v1/outputs_v2/repro_v1/check.json).
- The layer wrapper, run on the v1 inputs and `looks.csv`, gives `results.json` exactly.
- EVIDENCE: `outputs_fixed/kernel_validation.json` records SHA-256 values that match the committed `check_order_kernel.py` but not `joint_model_v1.py` or any of the nine input files. Git holds the same input blobs at its `source_ref` (83230367) and at HEAD. So the recorded hashes describe other bytes (INFERENCE: perhaps a working copy that was never committed). The numbers still reproduce.

### R1. What changes, step by step

A = v1; B = v2 without the two candidate rows (place only); C = B + entry 25; D = B + entry 60; E = v2.

| Set | P(25 at IV/17) | P(25 at kh_qumran) | P(60 at kh_qumran) | P(60 at tell_es_sultan) | TV 25 | TV 60 |
|---|---|---|---|---|---|---|
| A | 0 | 0.5451 | 0.0132 | 0.0215 | – | – |
| B | 0.0052 | 0.5465 | 0.0129 | 0.0201 | 0.0105 | 0.0126 |
| C | 0.1802 | 0.4483 | 0.0129 | 0.0201 | 0.1802 | 0.0126 |
| D | 0.0052 | 0.5466 | 0.0324 | 0.0196 | 0.0106 | 0.0320 |
| E | 0.1802 | 0.4484 | 0.0325 | 0.0196 | 0.1802 | 0.0321 |

- EVIDENCE (model output): entry 25's QUMRAN region falls from 0.610 to 0.501; JERICHO rises from 0.119 to 0.281.
- EVIDENCE: for entry 60, kh_qumran (0.0325) is now the highest listed place, above mount_zion (0.0296) and ein_feshkha (0.0276). The unlisted Jerusalem state stays first (0.186). QUMRAN region: 0.125 → 0.145.
- EVIDENCE: adding the place alone (B) moves 24 entries by more than 0.01; the largest is entry 1 (0.029: ain_duk −0.021, IV/17 +0.019). The cause is W2B's per-place background prior: each listed place gets equal prior mass, so JERICHO's share rises from 0.204 to 0.220. KERNEL_CORRECTION.md already warns that new prior mass can change results.

**Koḥlit group** (probability at kh_qumran; region masses; TV against v1):

| Entry | kh_qumran v1 | v2 | QUMRAN v1 | v2 | TV B | TV D | TV E |
|---|---|---|---|---|---|---|---|
| 4 | 0.0120 | 0.0211 | 0.1146 | 0.1293 | 0.0132 | 0.0259 | 0.0259 |
| 11 | 0.0106 | 0.0192 | 0.1030 | 0.1172 | 0.0115 | 0.0231 | 0.0232 |
| 15 | 0.0125 | 0.0218 | 0.1200 | 0.1350 | 0.0130 | 0.0262 | 0.0263 |
| 19 | 0.0428 | 0.0573 | 0.2303 | 0.2482 | 0.0122 | 0.0269 | 0.0270 |
| 60 | 0.0132 | 0.0325 | 0.1245 | 0.1451 | 0.0126 | 0.0320 | 0.0321 |

- EVIDENCE: every published proposal loses a little (for example Tell es-Sultan, entry 60: 0.0215 → 0.0196). The shared Koḥlit latent now gives kh_qumran 0.026 (eighth state; Tell es-Sultan 0.016).
- EVIDENCE (kernel grid, R4): with the names untied (rho 0, K2, w_L 0.995), entry 60 gives kh_qumran 0.048 and Tell es-Sultan 0.050. Tied (rho 0.9, w_A 0) they are 0.045 and 0.026.
- INFERENCE: the tie lifts kh_qumran above the other proposals with the same label. Entry 19 sits next to entry 20 (Wadi Qumran), so the order already pulled entry 19 toward Qumran in v1 (0.043). W2B notes that Secacah = Qumran itself rests on the order, so this lift is partly circular.

**Other entries with TV(v1, v2) > 0.01** (21 entries in all, including 25, 60 and the Koḥlit group):

| Entry | Title | TV place only (B) | TV v2 (E) | Main change |
|---|---|---|---|---|
| 26 | The facing cave | 0.0114 | 0.0542 | kh_qumran −0.044 (follows entry 25) |
| 24 | The Kippa ravine | 0.0081 | 0.0305 | U_JERICHO +0.011 |
| 1 | Valley of Achor | 0.0294 | 0.0291 | ain_duk −0.021 |
| 17 | Achor's two features | 0.0250 | 0.0246 | ain_duk −0.018 |
| 27 | The queen's residence | 0.0127 | 0.0209 | jericho_area +0.007 |
| 28 | The high priest's ford | 0.0203 | 0.0208 | IV/17 +0.012 |
| 33, 41, 36, 30, 37, 2, 42, 16, 39 | (no or few candidates) | 0.010–0.017 | 0.010–0.017 | IV/17 +0.004 to +0.010 |

- Only entry 24 crosses 0.01 because of a candidate row rather than the place itself. Entries 25, 26, 24 and 27 change through the entry-25 row; 60 and the Koḥlit group through the entry-60 row. Every other listed change comes from the new place's prior mass.
- Mean TV over all 61 entries: 0.009 for the place alone, 0.014 for v2.

### R2–R4. Sensitivity

Label steps (primary: confidence one step; extra: status one step). P(new state) and TV against v2:

| Row | Label | P(new state) | TV of its entry | Largest TV elsewhere |
|---|---|---|---|---|
| 60 at kh_qumran | possible/unknown (row inert) | 0.0129 | 0.0236 | Koḥlit 0.021 |
| | **possible/weak** | **0.0325** | – | – |
| | possible/low | 0.0421 | 0.0096 | Koḥlit 0.005 |
| | weak/weak, preferred/weak | 0.0284, 0.0351 | 0.0041, 0.0026 | Koḥlit ≤ 0.002 |
| 25 at IV/17 | possible/weak | 0.0539 | 0.1263 | entry 26: 0.035 |
| | **possible/low** | **0.1802** | – | – |
| | possible/medium | 0.4349 | 0.2546 | entry 26: 0.070 |
| | weak/low, preferred/low | 0.0990, 0.2480 | 0.0812, 0.0678 | entry 26 ≤ 0.022 |

- Entry 60's label moves entry 60 by at most 0.024; the effect stays inside the Koḥlit group and entry 59.
- Entry 25's label decides most of its result. Neither label touches the other row's entry (TV ≤ 0.0002).
- Kernel grid (R4, 15 configurations): P(25 at IV/17) ranges 0.13–0.44. It is 0.23 with the order off, 0.13 under Sinkhorn or the 5-km grid, and 0.29–0.44 when order-derived rows (including entry 25's kh_qumran row) are excluded. P(60 at kh_qumran) ranges 0.008–0.056. Table: [kernel_sensitivity_v2.csv](../../agent_review_2026-10-07/wave2/W2B_model_v1/outputs_v2/kernel_sensitivity_v2.csv).

### R5. The search-effectiveness layer on v2

`run_analysis.analyse` was imported and run unchanged, with the frozen PLAN.md scenarios and reading sets.

| Look | v1 | v2 with looks.csv | v2 with looks_v2.csv |
|---|---|---|---|
| L42 (60, kh_qumran) | no candidate row: unused | **counted**: the candidate source cites de Vaux 1973 | **counted** |
| L43 (25, IV/17) | no candidate row: unused | still unused: looks.csv codes it at U_JERICHO | **counted**: the source cites Sion 2002 |
| L44 (25, deposit) | no candidate row | no candidate row | odds not lowered (placement_relevant no: never a factor) |

- EVIDENCE: no reported row adds a factor (all 24 have factor 1). The factors below 1 are the same as in v1 (L03 and L04, entry 4). So the layer counts nothing twice.
- EVIDENCE: the coded silences move the Koḥlit entries as before (entry 4, S0 against S4: 0.0315 in v1, 0.0318 in v2).
- EVIDENCE: probe P11 (a silent 2002 cave-survey or IAA record at Kh. Qumran for entry 60, supplied but unread) now has P 0.031 instead of 0.012. At pd 0.9 it would remove 0.028 instead of 0.011. The other probes shrink slightly (P05, Tell es-Sultan: −0.020 → −0.018).
- INFERENCE, three cautions on double counting:
  1. L42 and L43 now sit in the candidate odds. A later positive factor for either row would count the same record twice.
  2. The Koḥlit tie carries the entry-60 row to entries 4, 11, 15 and 19 (+0.009 to +0.015 at kh_qumran). No record is used twice. But chain.json excludes the mound link for Qumran (it is "not a tell"), and nothing in the model or the looks table opposes entry 4 at kh_qumran under Puech's "mound" reading.
  3. Twin Cave matches the same form as IV/17 but has no state; its mass sits in U_QUMRAN. The model cannot rank IV/17 against it.

## What stays unknown, and why

- Both identifications. The labels copy the existing candidates on purpose; no source ranks Qumran among the Koḥlit proposals or IV/17 against Twin Cave.
- Entry 25's probability: it follows the label (0.054–0.435) and the kernel (0.13–0.44).
- How much of any change is real. Adding a state to the per-place background prior already gives about 40–50% of the Koḥlit change and nearly all the change in 12 other entries.
- IV/17's mouth coordinates. The grid reference locates the cave group only.

## Run and test

From the repository root (Python 3 with numpy and pyproj, which W2B already needs; nothing else):

```sh
python3 -I research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/build_inputs_v2.py --check
python3 -I research/models/search_effectiveness/build_looks_v2.py --check
python3 -I -B research/models/search_effectiveness/run_v2.py --tables
python3 -I -B -m unittest discover -s research/models/search_effectiveness -t research/models/search_effectiveness -p 'test_v2.py'
```

The run takes about 40 s. It refuses to start if a frozen input changed, and stops if R0 fails. `-B` keeps bytecode caches out of the W2B folder. The 14 tests check: v2 = v1 bytes plus exactly the declared rows; the rows match PLAN_v2; a fresh build gives the same files; looks_v2 differs only in two place ids; the PLAN_v2 hash; how the loader treats each new field; reproduction of `outputs_fixed/` (to 10⁻¹²) and `results.json`; determinism and agreement with `results_v2.json`.

## Files

| File | What it is |
|---|---|
| `PLAN_v2.md` | Frozen choices, runs and input hashes |
| `build_looks_v2.py`, `looks_v2.csv` | looks.csv with L43 and L44 at the new place |
| `run_v2.py` | The runner: R0–R5; writes `results_v2.json` and the W2B `outputs_v2/` tables |
| `results_v2.json` | All outputs, rounded to 8 decimals |
| `tests/test_v2.py` | 14 unittest tests |
| `W2B_model_v1/inputs_v2/` | v2 inputs, generator and `additions_v2.json` |
| `W2B_model_v1/outputs_v2/` | `repro_v1/` (R0), `entry_tv_v2.csv`, `posteriors_v1_v2.csv`, `kernel_sensitivity_v2.csv` |

## Sources

All inputs were already in the repository: the W2B model, inputs and grid converter; the Koḥlit chain; the rarity result and its source-4 addendum; the entry 25 assessment and the ʿAtiqot 41 review; the IV/17 registration record. No web source and no image was opened, so no link failed.
