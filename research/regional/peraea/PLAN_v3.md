# PLAN v3: documented Peraea places for Goranson's Transjordan proposal (frozen before any v3 run)

Exploratory model variant, 9 October 2026 UTC. No identification claim. No model had been run on v3 inputs when this file was written. The frozen-input hashes are below; the runner refuses to start if any of them changed.

## Question

The W2B model represents Goranson's Transjordan reading of Koḥlit by one place, `transjordan`: two 15-km components at Machaerus and Amathus. What changes for entry 60 and the Koḥlit group (entries 4, 11, 15, 19, 60) when that proxy is replaced by the Second Temple sites of Peraea documented in the gazetteer?

## Rule (primary variant V3-P)

1. The place `transjordan` keeps its place_id, its region TRANSJ and all its candidate rows (entries 4, 11, 15, 19, 60; possible/weak; Koḥlit proposal; entry 60 conditional on XII 10 not read "Janoah").
2. Its `components` become an equal-weight mixture over every gazetteer row with status `documented`, peraea_proper `yes` and a coordinate (12 sites; gazetteer column w2b_place_id = transjordan). Each site is one component `lat:lon:sigma` with its gazetteer sigma.
3. Nothing else changes. Every other v3 input file is a byte copy of its v2 file; grid_conversions_v3 only appends the five Palestine Grid conversions used.
4. Why this rule: Goranson names a district, not a site. The documented sites are the places where the record shows Jewish, Hasmonean or Herodian presence in the window. Equal weight per site is the simplest rule that uses no information about the scroll. It keeps the state count and the per-place background prior unchanged, so only the spatial kernel changes.

Note (known before the run, from the code): the unlisted state `U_TRANSJ` is built from the components of the region's listed places, so it also moves from the two 15-km points to the 12 sites (with sigma_U = 2 km added).

## Runs

Model: `W2B_model_v1/scripts/joint_model_v1.py`, imported unchanged, `cfg_with()` defaults (transition `fixed` = K2, rho 0.9, w_A 0.4, w_L 0.995, XII 10 `milik_puech`, kohlit_scheme None).

- **R0 reproduction (stop rule).** (a) `build_inputs_v3.py` with the change switched off gives files byte-identical to inputs_v2. (b) The v3 runner on inputs_v2 reproduces `outputs_v2/posteriors_v1_v2.csv` column P_v2 for every stored (entry, state) within 1e-8 (the file is rounded to 8 decimals), and gives P(60 at kh_qumran) = 0.0325 and P(25 at iv17_abu_saraj) = 0.1802 to 4 decimals. If R0 fails, the run stops.
- **R1 primary.** V3-P against v2. For entries 4, 11, 15, 19 and 60: P(transjordan), P(region TRANSJ), P(U_TRANSJ), total variation (TV) against v2, top 8 states. The Koḥlit latent at transjordan. logml. Every entry with TV(v2, V3-P) > 0.01, with its largest change.
- **R2 sensitivity** (each against v2 and against V3-P; same report for entries 4-60):
  - S1 cluster-merge: single-linkage clusters of sites within 5 km; one component per cluster at the mean position, sigma = max(member sigma, largest member distance from the mean).
  - S2 broad: documented plus partial Peraea-proper sites that have a coordinate (19 sites).
  - S3 blur: primary sites with a sigma floor of 5 km.
  - S4 split: each documented site becomes its own place in region TRANSJ; the five transjordan candidate rows are replaced by one row per site and entry with the same labels and conditions, and prior_override = (0.1/0.9)/n so that the total Goranson odds per entry stay 0.1111; the `transjordan` place is kept with no candidate rows. This adds n states and their background prior mass.
  - S5 kernel grid: the 15 `check_order_kernel.py` configurations (transition sinkhorn/fixed, grid 0/5 km, five rho/w settings) on v2 and V3-P; report P(60 at transjordan), P(60 in TRANSJ) and P(60 at tell_es_sultan).
  - S6 Janoah reading: XII 10 read `janoah` on v2 and V3-P; report entries 4, 11, 15, 19 (entry 60 leaves the Koḥlit group under this reading).
- No input, rule or variant is changed after seeing a result. Anything added later is labelled a new exploratory variant.

## Reporting

Descriptive only. There is no decision threshold: the numbers are model outputs under stated assumptions, not probabilities that Koḥlit lay in Peraea. All runs are reported whatever they show. Outputs go to `W2B_model_v1/outputs_v3/`; numbers rounded to 8 decimals.

## Frozen inputs (SHA-256)

| File | SHA-256 |
|---|---|
| research/regional/peraea/plan.json | 010fa981cd2967b8443a1a30566547332758276c96ff596c820f09138393e707 |
| research/regional/peraea/gazetteer.csv | b7abb1e6e52d514c605fd3cf4ea2560b367e8a4b0f36897c0745bbbe54d537fe |
| research/regional/peraea/scripts/build_gazetteer.py | 908875245716d7bfe6690bbd8f37a76e08374dcf0d4fb2712c602f46cb11d01e |
| W2B_model_v1/inputs_v3/build_inputs_v3.py | 99bd3622f9c4f93d6cbb75775b3541c5c84293e2315d92e27aeee07464aa2e19 |
| W2B_model_v1/inputs_v3/additions_v3.json | e764fbee9abd86548751f7442358c76221b8e16e2ddde63a6732a20d6bd9d527 |
| W2B_model_v1/inputs_v3/places_v3.csv | 381894a6e383d8f763197048d751bc8c89a5506144b295b3b77d338cc9ad3b9c |
| W2B_model_v1/inputs_v3/candidates_v3.csv | f8d70eb7fda81a8cbbc07bfaa22a8c48785dc423e73e0d989139c717cf51b2a5 |
| W2B_model_v1/inputs_v3/entries_v3.csv | 7fa03e97ed46e6b4bcb550538be815bc99b7a5c2b08700c11551586d3b2c31b0 |
| W2B_model_v1/inputs_v3/name_groups_v3.csv | 82a7d44b299ee6f7ccf3b43a14aad6d4b429f7a264a11ce0e012831a02b2cc28 |
| W2B_model_v1/inputs_v3/kohlit_proposals_v3.csv | 21001790432bcca973bb7dd8464cb407a3647893e6db06c0db80ae9bab963feb |
| W2B_model_v1/inputs_v3/grid_conversions_v3.csv | cbcdb12fccf8c7617ff7a4618124b0364be1b06217dc709f655cafe1668cec7e |
| W2B_model_v1/scripts/joint_model_v1.py | 702e69c0e793c38002efa72230748435b6f02476f2f5da8a389a107d94d4c6b6 |
| W2B_model_v1/outputs_v2/posteriors_v1_v2.csv | 7cbc2e5816bc8b0a462df8466c11ca1459c4f2856f9ec2c2ee74c8a45803a322 |

```json
{"frozen_inputs_sha256": {
 "research/regional/peraea/plan.json": "010fa981cd2967b8443a1a30566547332758276c96ff596c820f09138393e707",
 "research/regional/peraea/gazetteer.csv": "b7abb1e6e52d514c605fd3cf4ea2560b367e8a4b0f36897c0745bbbe54d537fe",
 "research/regional/peraea/scripts/build_gazetteer.py": "908875245716d7bfe6690bbd8f37a76e08374dcf0d4fb2712c602f46cb11d01e",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/build_inputs_v3.py": "99bd3622f9c4f93d6cbb75775b3541c5c84293e2315d92e27aeee07464aa2e19",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/additions_v3.json": "e764fbee9abd86548751f7442358c76221b8e16e2ddde63a6732a20d6bd9d527",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/places_v3.csv": "381894a6e383d8f763197048d751bc8c89a5506144b295b3b77d338cc9ad3b9c",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/candidates_v3.csv": "f8d70eb7fda81a8cbbc07bfaa22a8c48785dc423e73e0d989139c717cf51b2a5",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/entries_v3.csv": "7fa03e97ed46e6b4bcb550538be815bc99b7a5c2b08700c11551586d3b2c31b0",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/name_groups_v3.csv": "82a7d44b299ee6f7ccf3b43a14aad6d4b429f7a264a11ce0e012831a02b2cc28",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/kohlit_proposals_v3.csv": "21001790432bcca973bb7dd8464cb407a3647893e6db06c0db80ae9bab963feb",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/grid_conversions_v3.csv": "cbcdb12fccf8c7617ff7a4618124b0364be1b06217dc709f655cafe1668cec7e",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/scripts/joint_model_v1.py": "702e69c0e793c38002efa72230748435b6f02476f2f5da8a389a107d94d4c6b6",
 "research/agent_review_2026-10-07/wave2/W2B_model_v1/outputs_v2/posteriors_v1_v2.csv": "7cbc2e5816bc8b0a462df8466c11ca1459c4f2856f9ec2c2ee74c8a45803a322"},
 "sensitivity": {"cluster_km": 5.0, "sigma_floor_km": 5.0, "split_total_odds": 0.1111111111111111},
 "r0_tolerance_abs": 1e-8}
```
