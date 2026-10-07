# T06 — Placing all the entries together (joint placement model, v0)

Agent report, 6 October 2026, saved by the coordinator. v0, built on existing data only; results from tasks 1 and 5 should be added as rows in `inputs/*.csv` and the model re-run. It identifies no individual hiding place. Labels: EVIDENCE / INFERENCE.

## Model
Exact forward–backward over all 61 entries (Puech numbering incl. 12a).
- **States:** the 39 gazetteer places plus one "unlisted site" state for each of seven regions (JER, SOUTH, DESERT, QUMRAN, JERICHO, NORTH, WEST).
- **Prior:** odds by confidence (medium 0.6, low 0.3, weak 0.1) × status (preferred 1.5, possible 1, weak 0.5); remainder to "elsewhere". With no sequence or name term the posterior equals the prior (self-test).
- **Itinerary:** T(a,b) = (1−w)π(b) + w·π(b)·K̃(a,b), K a two-scale distance kernel (1 km and 10 km) using each place's stated precision; separate weights inside 1–19 (w_A) and elsewhere (w_L); w = 0 is the control.
- **Names:** a latent location per repeated-name group (Achor, Koḥlit, ha-Melaḥ, Secacah, Solomon, Shaveh, Zadok), members' evidence tempered so one shared identification counts once.
- Fits: λ unidentifiable (fixed at 2). Without names w = 0.995 (log ML +17.7 vs independence; +13.7 if w_A = 0). With names w_A = 0.4, w_L = 0.995 — the itinerary inside 1–19 adds little once names are tied.

## Findings
1. **The real order is far more geographically coherent than shuffled orders** under all three nulls (full shuffle, within block, within region; 20,000 shuffles each), and still after dropping documented and likely order-derived candidates (n = 35, p ≤ 0.002). The effect is real (high confidence); that it reflects geography rather than circularity is medium-low confidence.
2. **The order places districts, not sites.** With an anchor's own evidence hidden, the order recovers its region 2–12× better than background (15 of 18 anchors) but the specific site only ~2–3× (Doq, Choziba, Siloam: P ≈ 0.03 vs 0.013 background). High confidence.
3. **Shortlist:** entry 21 (Kh. Qumran) 0.69 → 0.90; 31 (Doq) 0.61 → 0.78; 32 (Choziba) 0.69 → 0.84; 49 (Siloam) 0.69 → 0.84. District-level support only. For 21, support comes from 20, 22, 23, which share the Secacah identification that "rests on the order" (atlas note e20).
4. **Koḥlit = Tell es-Sultan conflicts most with the order.** Entry 60 is pulled north: P(NORTH) 0.07 → 0.71, P(Tell es-Sultan) 0.30 → 0.10, for any w_A. With names tied and tempered, the Koḥlit group splits: Jericho 0.25, North 0.23, Qumran 0.17, Jerusalem 0.17. The atlas rejects Milik's Carmel, Goranson's Transjordan and Zissu's Samarian desert because they "break the order"; that rejection holds only if entries 1–19 are geographically ordered (which the repo's own name-adjacency test says they are not) or if Tell es-Sultan is counted once per Koḥlit entry. Low–medium confidence.
5. **Weak pulls:** entry 27 away from the Tombs of the Kings (0.23 → 0.04, toward the Jericho oasis 0.41); 34 away from Bir Ayyub (0.19 → 0.08); 29 away from Hyrcania (0.16 → 0.05); 41 south (0.55, circular). Low–medium.

## Sensitivity and tests
- Anchor leave-one-out: region recovered at rank 1 for 15 of 18 anchors (lift 1.6–9×); not recovered: 18 ʿAṣla, 38 Naṭuf, 35 Mar Saba. Identifications the order contradicts: 11, 60, 27, 24, 35, 19.
- Removing anchor 59 (Ibziq) shifts 57, 58, 60 by 0.2–0.3 and the Koḥlit entries through the name tie.
- Null tests (strict coordinates): all candidates n = 56, D = 1.630 vs null means 2.468 / 2.003 / 1.915, all p ≤ 1.5×10⁻⁴. Without documented or likely order-derived candidates (n = 35): log BF p < 1×10⁻⁴ (full), 3×10⁻⁴ (within block), 0.002 (within region).
- Circularity flags in `inputs/candidates_v0.csv`: 17 "documented" order-derived pairs (the atlas says so), 24 "likely" (agent's judgement). Dropping the documented ones collapses the joint fit (log ML 3.3).
- Stable across 26 variants: 21, 31, 32, 49, 27, 34. Unstable: Koḥlit entries, 36/37, 41/45, 24.

## Limits
Candidates and the numeric conversion of confidence labels are the project's and the agent's; direction words ignored; regions and coordinate proxies (tekoa_herodium midpoint; jordan_ford at Qasr al-Yahud; jer_shaveh mixture) are the agent's; λ and w weakly identified.

## Re-run
```
python3 -I scripts/build_inputs.py ../../shared inputs
python3 -I scripts/joint_model.py --inputs inputs --out outputs [--config inputs/config_example.json]
python3 -I scripts/extra_tables.py inputs outputs
python3 -I scripts/plot_regions.py outputs
```
To add evidence, append rows to `inputs/candidates_v0.csv` (optional `prior_override`), `places_v0.csv` or `name_groups_v0.csv`. Full run ~3 minutes.

## Best next step
Order-independent location evidence for Koḥlit and Secacah (from tasks 1 and 5), then re-run with `exclude_order_derived=documented`.
