# Run 28 rule: do feature attributes locate a described feature?

**Status: frozen, 31 Oct 2026.** Owner decision, 19:57 America/Los_Angeles: option 2 of the draft (add the 1952 cave list, then run), with "u can open page and get that info" (the main session opens the Internet Archive loan). This file is frozen by the commit that adds `RULE.sha256`, **before** any concordance, describer page or benchmark item is read. Nothing below has been run. Exploratory: nothing here changes ratings, the ledger, ACTIVE_TEST or atlas data. No result of this run is an identification.

## Question

Runs 26 and 27 showed that class-level records ("a cave is recorded here") separate a true place from others by 0.99–1.4×. Run 27 named one condition that would reopen the question: an inventory with feature attributes, so that rarer conjunctions can be scored. The attribute inventory (`../attribute_inventory_2026-10-31/`) is that inventory for the 1993 cave survey.

Run 28 asks: **when a second, independent observer describes a feature by its class and attributes, do those attributes pick out the right feature of the inventory, and by how much more than the class alone?** The scroll is scored only if this gate passes.

## What changes from run 27, and why

| Item | Run 27 | Run 28 | Reason |
|---|---|---|---|
| Evidence | class present in a 1 km cell | class plus attributes of one feature | Run 27, reopening condition 1 |
| Hypotheses | 2,558 cells of 1 km | the inventory's features | Attributes belong to features, not cells |
| Benchmark | 1940s map marks (class only) | earlier surveys that describe the same caves | A map mark has no attributes |
| Location | likelihood ignored directions and distances | the clue's location is not used at all; it only fixes the truth | The test is about attributes alone |

## Inputs (frozen)

- **Inventory:** `../attribute_inventory_2026-10-31/out/atq41_consolidated_v2.csv` at commit b9f9f7d (SHA-256 starts `873970697d428710`). The candidates are its whole features (key without a `.` suffix), positioned or not.
- **Same-team check only:** `out/atq41_consolidated.csv` (text only, before plans; SHA-256 starts `35f04edbd891be61`).
- **Scroll clues (only if the gate passes):** `../landscape_map_2026-10-31/inputs/entry_features.csv` (SHA-256 starts `a13ba89abb7c30ca`), columns `landmarks` and `position_cues`.

## Attributes used

Only the attribute types the scroll entries use (attribute-inventory README, order of work, step 4):

| Attribute | Clue value | Match with an inventory value |
|---|---|---|
| Class group | from `feature_class` | same group (below) |
| `n_openings` | integer | equal |
| `opening_dirs` | 8-point directions, one per opening | the shorter list can be paired one-to-one into the longer, each pair equal or neighbouring (`/` values match either point) |
| Pillar | `n_pillars` ≥ 1 or = 0 | same presence |
| Steps | `n_steps` ≥ 1 or = 0 | same presence |

Sizes, plaster, construction and relations are not used. Values that are blank, `unknown`, `undecidable` or unresolved (`A|B`) count as unknown.

**Class groups.** cave = {cave, chamber, rock_shelter, columbarium, fissure}; water = {cistern, pool, reservoir, basin, ritual_bath, pit}; channel = {conduit, outlet, dam}; tomb = {tomb, burial}; spring = {spring}; built = {building, room, court, tower, wall, doorway, steps, terrace, road, cairn, pillar}; other = {other}.

## Model

For a clue d and candidate feature j, with a uniform prior over candidates:

P(j | d) ∝ ∏ over attributes a known on both sides of LR_a(j)

- If the values match: LR_a = α_a / q_a(d) + (1 − α_a).
- If they do not: LR_a = 1 − α_a.
- If either side is unknown: LR_a = 1.

Here q_a(d) is the share of candidates with a known value of a whose value matches d. α_a is the chance that an independent observer reports a value consistent with the true one; otherwise the report is unrelated to it.

**Fitting α_a, on the training fold only.** α_a has a grid of 0.00–0.99 (step 0.01) and a uniform prior. Each training item whose truth set has exactly one feature, and whose clue and true feature both know a, contributes α + (1 − α)q_i if they match and (1 − α)(1 − q_i) if not. The posterior mean is used.

**Class-only model:** the same, with the class group as the only attribute.

**Truth sets.** An item may name several inventory features as one place. Its posterior is the sum over its truth set, and its Bayes factor is that sum divided by the prior share of the set.

## Benchmark D: independent describers (the gate)

**Describers.** Surveys made by other teams, before 1993, of caves the 1993 survey also recorded:
- **Benjamin Part IV** (Goldfus & Golani, in Finkelstein & Magen 1993), above all the Makkukh cave list (Hebrew pp. 333–335) and the sites within 1 km of an inventory feature in the frozen location list (`claude/held_benjamin_parts4_5_locations_frozen_2026-10-30.csv`). Region II was written by Hirschfeld & Riklin, so the teams differ.
- **Bar-Adon 1972** (ASI 1, "The Judaean Desert and Plain of Jericho", 1968 fieldwork).
- **The 1952 survey:** the numbered list of 40 sites in DJD III Textes (pp. 6–12; Internet Archive loan `lespetitesgrotte0000unse`). Positions come from the repo's digitised 1952 map, `research/history/devaux1952_cave_points/devaux1952_cave_points.csv` (27 points, about 30 m 1σ), matched by site number.

**Steps.** Steps 1, 2 and the first pass of step 3 start together, because their scope does not depend on each other. The first pass keys the whole 1952 list, and for Benjamin the Makkukh cave list plus the 19 Part IV sites within 1 km of an inventory feature. Sites that the concordance cites beyond these are keyed in a second pass, after step 1 is committed. Each output is committed as it finishes.
1. **Concordance.** Two separate instances read the *ʿAtiqot* 41.2 region reports and list every statement that an *ʿAtiqot* feature is the same as a feature of a describer. Each row gives the *ʿAtiqot* key or keys, the describer, its site, cave or page number, the basis (explicit number, page, name), a quote of 15 words or fewer, and `copied = yes` when the sentence repeats the earlier survey's description. Agreed rows are kept; disagreements go to a third reading. Output: `keyed/concordance.csv`.
2. **Site headers (Bar-Adon only).** One instance lists the number, name and grid of every site from the entry headers only. A script then selects the sites that are cited in the concordance or lie within 1 km of an inventory feature.
3. **Describer keying.** For each describer, two instances (A, B) key the selected sites with the unchanged `SCHEMA.md` and `READER_INSTRUCTIONS.md`. They see only their describer's pages; never *ʿAtiqot* 41, the inventory, the concordance or each other's files. Agreement and third reading follow `scripts/agreement.py` and `scripts/consolidate.py`.
4. **Items.** One item is one whole feature of a describer:
   - its class group is cave, water, channel or tomb;
   - it knows at least one of `n_openings`, `opening_dirs`, pillar or steps;
   - it has a truth set from the concordance (primary), or, failing that, every inventory feature of the same class group within 150 m of its position: the printed grid (5-digit grids; 300 m for 4-digit grids), or for the 1952 list the digitised map point;
   - concordance rows marked `copied = yes` are excluded.
5. **Power floor.** If fewer than **30** items result, the run stops with "not identifiable from available evidence". The scroll is not scored.

**Folds.** Items are grouped by describer site. Groups are shuffled (seed 2828) and alternated into fold 1 and fold 2. Each fold is scored with α fitted on the other.

**Metrics.**
- Coverage of the 50 % and 90 % credible sets. Ties are taken in random order, so an item's coverage is its expected coverage.
- log10 Bayes factor of the truth set, under the attribute model and the class-only model.
- Gain = log10 BF (attributes) − log10 BF (class only).
- Rank of the truth; size of the 90 % set.

**Gate** (attribute model, all items pooled):
- **G1 calibration:** both coverages lie inside the central 95 % region of Binomial(N, 0.5)/N and Binomial(N, 0.9)/N.
- **G2 evidence:** mean log10 BF > 0, with the 95 % bootstrap interval above 0. The bootstrap resamples describer sites (4,000 draws, seed 2829).
- **G3 added value:** mean gain > 0, with the 95 % bootstrap interval above 0.

All three must pass. **No revision is allowed**; a changed model is a new run.

## Reported checks (not gates)

1. **Same team, other medium (an upper bound).** The 41.1 plan readings as clues, against the text-only inventory, with the same model and folds.
2. **Kh. Qumran (built features).** Magen & Peleg 2018 features that cite exactly one de Vaux locus present in IIIA are clues. The candidates are IIIA's whole features other than walls.
3. **Truth by location only,** for every item.
4. **Exposure sensitivity:** items from Benjamin sites the main session has already seen summarised (327, 332, 355, 363, 370, 372, 378, 386, 387, 390, 391, the Makkukh list) are left out.
5. **α_a posteriors** and the q_a distribution, per attribute.

## Scroll outputs (only if the gate passes)

1. **Coding.** Two separate coder instances read only the `landmarks` and `position_cues` of each entry and code its feature:
   - the class group;
   - "two openings" → `n_openings` 2;
   - "facing X" → one opening direction X;
   - "column" or "pillar" → pillar present;
   - steps or a stair of the feature → steps present;
   - anything else → blank.
   Where the two coders differ, the field is left blank. An entry is scored only if its class group is in the inventory and it has at least one attribute.
2. **Scoring.** α comes from all benchmark items. For each scored entry, report:
   - the posterior over the inventory, **conditional on the entry's place being one of its features**;
   - the top five features, with posterior and Bayes factor;
   - the number of features that match every coded attribute;
   - the sizes of the 50 % and 90 % sets.
3. **No unconditional claim.** The chance that a scroll place is in the inventory at all is not estimated in this run.

## Assumptions and limits, stated now

- **Independence.** The earlier surveys stand in for the scroll's author: they observed the same features without the 1993 survey's notes.
- **Selection.** A concordance made by the 1993 authors may favour pairs that look alike, which would raise α. Check 3 reports location-only truth.
- **Missingness.** Unknown values are treated as carrying no information. Many inventory caves lack an opening count (159 of 343 in the cave group) or a pillar count (314 of 343).
- **Power.** Expected N is small. Counts made for this draft (no sentence read): the region reports cite the Benjamin survey about 45 times and Bar-Adon about 30, mostly by page. Only about 10 cites carry an explicit site or cave number. Of the 106 gridded Part IV sites, 6 lie within 500 m of an inventory feature and 19 within 1 km. A gate at N ≈ 30–45 can show a large effect (several-fold), not a small one.
- **Ceiling.** In the inventory, 5 of the 343 cave-group features are recorded with two or more openings and a pillar, and 8 with exactly two openings, one of them facing E, NE or SE. So even a perfect observer would give at most a few tens-fold for such a clue, and only if the place is a surveyed cave.
- **Coverage of the land.** The inventory covers the cliff strip from Wadi el-Makkuk to Naḥal Kidron, nothing more.

## Exposure log (main session, while drafting)

- Read the run 27 RESULT and RULE, run 26 RULE lines on clue sources, and the header of `entry_features.csv`. No scroll entry text was read.
- Read the project note `claude/held_benjamin_parts4_5_2026-10-30.md` in full, including the summaries of not-held Part IV sites (see check 4), and the frozen location list.
- In the *ʿAtiqot* 41.2 texts: per-article counts of citations of earlier surveys, counts of distinct cited numbers, and the first lines (title, authors) of articles 2546 and 2553. No other sentence was displayed.
- From the inventory: the conjunction counts in "Ceiling" and the missingness counts.
- Bucket: page counts and text-layer checks for ASI 1 and the Benjamin survey (reversed Hebrew text layers; page numbers only).
- Keyed Qumran files: row counts, class counts, attribute fill rates, and how many rows cite a locus number.
- Earlier project notes seen in this session (search snippets): the 1952 list has 40 sites, 26 with Qumran pottery, and few depths (cave 1, cave 3, 3Q). No site description was read.

## Order of work

1. Owner approval (above); this file is frozen (commit and SHA-256).
2. The scripts (`scripts/bench28.py`, `scripts/score28.py`) are committed before any consolidated describer file exists.
3. Steps 1–5 of benchmark D, each committed as it finishes.
4. The gate; `RESULT.md`. Scroll coding and scoring only if the gate passes.
