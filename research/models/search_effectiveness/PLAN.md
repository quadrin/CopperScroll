# Search-effectiveness plan (frozen before any scenario was run)

Written 9 October 2026, about 18:20 UTC. No scenario, probe or unsearched-mass result had been computed when this file was frozen. The W2B baseline (S4) is the already published K2 default; it was not rerun before the freeze.

## What is being computed

This is exploratory. It tests no identification and has no decision rule. Every output below is reported whatever it shows.

1. The looks table (`looks.csv`) codes what the repository already holds. A silent or explicit-absence row gives a likelihood factor 1 − pd on its entry's place state, with pd = coverage × p_recognise × p_report × p_survive. Any null makes the factor 1.
2. Rows from one field lineage count once: the largest pd within a lineage. Different lineages multiply.
3. A target (entry, place, relation) with a reported row that fully satisfies the requirement (`satisfies_requirement = yes`) takes no silence factor. Reported rows add no factor.
4. Factors multiply the W2B likelihood rows after the name-group tempering. They are not tempered.
5. Scenarios S0–S4 and the reading sets are fixed below. S4 sets every pd to 0 and must equal the W2B K2 default.
6. Outputs: per-entry posteriors under S0–S4, the change against S4 (total-variation distance and the largest place changes), the rows that drive each change (leave one target out), the unsearched mass per region (states whose combined pd is below the threshold), a phantom-coverage list, a double-counting check against `candidates_v1.csv`, and a probe for each record in `next_records.csv`.
7. Probe: add one silent look with pd equal to each probe value to the probe's target, on top of S0, and report the change of P(entry at place), the total-variation change of that entry, and the three most moved other entries. Rank by access tier, then by the size of the change at the first probe value.

## Frozen parameters

```json
{
 "plan_id": "search-effectiveness-2026-10-09",
 "model": "research/agent_review_2026-10-07/wave2/W2B_model_v1/scripts/joint_model_v1.py, inputs v1, cfg_with() defaults (K2 'fixed', kohlit_scheme None, rho 0.9, w_A 0.4, w_L 0.995)",
 "reading_sets": {
  "R-P": {"tel": "mound", "xii10": "milik_puech", "kohlit15": "yes", "e4cleft": "immersion"},
  "R-E": {"tel": "ruins", "xii10": "milik_puech", "kohlit15": "yes", "e4cleft": "immersion"},
  "R-J": {"tel": "mound", "xii10": "janoah", "kohlit15": "yes", "e4cleft": "immersion"}
 },
 "main_reading_set": "R-P",
 "scenarios": {
  "S0": {"label": "as coded", "caps": {}},
  "S1": {"label": "features often destroyed before the look", "caps": {"p_survive": {"value": 0.3, "results": ["silent", "explicit_absence"]}}},
  "S2": {"label": "features not recognised (e.g. a cistern or tomb mouth logged as a quarry or modern pit)", "caps": {"p_recognise": {"value": 0.3, "results": ["silent", "explicit_absence"]}}},
  "S3": {"label": "seen but never published (silences only)", "caps": {"p_report": {"value": 0.3, "results": ["silent"]}}},
  "S4": {"label": "every look uninformative (= W2B K2 default)", "zero": true}
 },
 "combination": {"within_lineage": "max", "across_lineages": "product of (1 - pd)", "reported_dominates_if": "satisfies_requirement == yes"},
 "unsearched_pd_threshold": 0.2,
 "phantom_pd_threshold": 0.2,
 "probe_pd": [0.5, 0.9],
 "access_order": ["supplied_unread", "open_access_unread", "library", "requested_pending", "archive_order", "fieldwork"],
 "rounding_decimals": 8,
 "frozen_inputs_sha256": {
  "looks.csv": "6a0420fcef8d08e00ac483810f39ac6ca442cbe6769c269a4f550ce1002af0da",
  "next_records.csv": "62fa74497c59ae4470347e0e5fdd303d40ad718b2d732bc468c46902964e33ad"
 }
}
```

## Reading sets

- R-P (main): Puech's "mound" for btl, the W2B default reading of XII 10 (Milik/Puech), Koḥlit restored in entry 15, and Eshel's immersion cleft in entry 4. These keys only switch rows of the looks table on or off; XII 10 and entry 15 also set the W2B readings.
- R-E: Eshel's "ruins" for btl. The two mound-absence rows switch off.
- R-J: XII 10 read as Janoaḥ. Entry 60 leaves the Koḥlit group in W2B, and the Kh. Yanun rows switch on.

## Why the caps are 0.3

The value is a round scenario choice, not an estimate. It marks a failure mode as likely: at most three looks in ten would detect the feature. It applies only where the coded value is higher.

## What would count as a coding error

A wrong page, a wrong place state or a misread result in `looks.csv`. Any correction after the run is logged in the README with the new hash, and both runs are reported.
