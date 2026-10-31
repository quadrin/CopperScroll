# Run 26 rule: a calibrated landscape map for the scroll's landmark words

Written 31 Oct 2026 before any scroll entry is scored and before any test benchmark is drawn. Owner request, 31 Oct 2026 08:56 America/Los_Angeles ("Shall we begin?"), after agreeing to a loosened, quantitative sandbox (08:41). Exploratory: nothing here changes ratings, the ledger, ACTIVE_TEST or atlas data. No result of this run is an identification.

## Question

For each entry, where on the landscape does the evidence of its landmark words put the entry, with probabilities that have been shown to be calibrated? How much can this kind of evidence concentrate probability at all? Which single site check would change the map most?

## Novelty (checked 31 Oct, `main` 7a3b307, `sandbox/methods` eb0ef63)

- W2B / T06 (wave 2, 7–9 Oct) is a joint model over the project's 50-place list with an order (itinerary) term. Its hypotheses are the scholars' places, and it has no benchmark.
- Rarity (stage 2, k of 333) counts units that meet combined predicates. It gives no probabilities.
- Run 22 (reverse lookup) scored 8 documented sites against coded relations. Result: not above chance.
- Lane J (30 Oct) built the unified feature table used here, and scored dating scenarios, not places.
- New here: every 300 m cell of the landscape is a hypothesis, recorded or not; recording gaps enter the likelihood; the probabilities must pass a calibration gate on fake entries before any scroll entry is scored.

## Inputs (hashes in `inputs.sha256`)

- `features_unified.csv`: lane J's unified feature table (branch `claude/novel-2026-10-30-J`, 7b58cf0), 7,366 records from HA-ESI, ASI, the Judean Desert cave survey and the columbaria list, with classes rockcut, cave, tomb, cistern, channel_aqueduct, pool_reservoir, dovecote, steps_ritual_bath, fortress, dam. Date fields are not read.
- `entry_features.csv`: wave 1 T02 entry table (7 Oct). Its `landmarks` column is the only clue source. Its `candidate_places` column is used only by priors R1 and R2.
- `places_v2.csv`: W2B place coordinates, for R1, R2 and labels.
- `mandate_features.csv`: the 1940s 1:20,000 map features (`research/regional/mandate_maps/features.csv`), for benchmark B only. These are not in the scoring inventory.

## Model

**Cells.** 300 m square cells on a local equirectangular grid (x scale cos 31.8° × 111.32 km per degree of longitude, y 110.57 km per degree of latitude), origin 31.20 N, 35.10 E. Hypotheses are the cells whose centre lies in a zone box of lane J (Z1 Gerizim, Z2 Jordan Valley, Z3 Judean Desert, Z4 Jerusalem Hills), minus a crude Dead Sea mask: for latitude below 31.77, cells east of the line through (31.20, 35.40), (31.46, 35.40), (31.60, 35.43), (31.714, 35.462), (31.77, 35.50).

**Records.** Located records whose point is in a hypothesis cell. Records with no coordinates are left out of the primary run (sensitivity S1 puts them at their named place).

**Clues.** Each landmark word of an entry maps to unified classes by lane J's `LANDMARK_CLASS` table, unchanged. Words in the same entry whose class sets overlap are merged into one clue (union of classes). Other words (valley, threshold, court, corner, stone, spring and so on) carry no likelihood in this run. Direction and distance words carry none either: record positions are good to about 100 m, and most of the scroll's distances are tens of cubits. An entry with no mapped clue is not scored.

**Pattern.** For entry e with n clues, the pattern T(u) of cell u is the set of clues with at least one record of their classes in u.

**Stratum.** s(u) = zone × other-class richness bin, where other-class richness is the number of records in u whose class is in none of e's clues. Bins: 0, 1, 2–4, 5–15, 16+.

**Background.** P_bg(T | s) is the empirical share of cells in stratum s with pattern T. It is smoothed towards the zone (weight 5 cells), the zone towards the whole area (weight 5), and the whole area by 0.5 pseudo-count per pattern.

**Likelihood.** If u is the true place, each clue's real landmark is recorded in u with probability c, independently, on top of the background:
P(T | H_u) = Σ_{B ⊆ T} P_bg(B | s(u)) · c^{|T∖B|} · (1−c)^{n−|T|}.
If u is not the true place, P(T | not H_u) = P_bg(T | s(u)). The likelihood ratio of u against "no cell is the place" is LR_u = P(T(u) | H_u) / P_bg(T(u) | s(u)). c absorbs recording gaps, destruction, position error and wrong word meanings.

**Prior over cells.** A cell is a "site" if its other-class richness is at least 1. A share ρ of the prior goes uniformly to sites, 1 − ρ uniformly to other cells. Region variants:
- R0: none.
- R1: 0.8 of the mass to the zones of the entry's candidate places (each zone's share fixed by the site/other split above), 0.2 to the other zones.
- R2: 0.5 of the mass to cells within 2 km of the entry's candidate places, 0.5 as R0.

**Parameters.** c ∈ {0.1, 0.2, …, 0.9} and ρ ∈ {0.5, 0.7, 0.9}, uniform over the 27 pairs. The posterior over pairs uses each pair's marginal likelihood Σ_u prior(u) LR_u. The cell posterior is the mixture over pairs.

## Calibration gate (before any scroll entry is scored)

**Benchmark A: fake entries on thinned records.** Dev seeds 1–200 may be used freely. Test seeds 1001–2000 are drawn once.
- For each fake entry, c_true ~ U(0.2, 0.8). Every record in the inventory is kept independently with probability c_true, and the scorer sees only the kept records.
- The true zone is drawn with the shares of the scored entries' candidate places by zone. The true cell is drawn uniformly from cells of that zone that have at least one record before thinning.
- The clue count n is drawn from the scored scroll entries' clue counts after merging.
- For each clue, with probability 0.8 a class present at the true cell before thinning is chosen (uniformly among present classes not yet used), and a word is chosen uniformly among the words that map to it. Otherwise, or if no unused present class is left, a word is drawn from the scroll's mapped-word frequencies (a wrong meaning or an unrecorded kind). The clue is the word's class set, then the merge rule applies.
- The scorer is run under R0 and under R1, where R1 gives 0.8 to the true zone.

**Metrics.** The 50 % and 90 % highest-posterior sets (cells in posterior order until the mass is reached) and whether they contain the true cell; log10 of posterior over prior for the true cell (the Bayes factor); median posterior and rank of the true cell; top-1, top-10 and top-100 hit rates; median area of the 90 % set; all by zone too.

**Gate.**
- G1: under R0 and under R1, 90 % set coverage between 0.85 and 0.95, and 50 % set coverage between 0.42 and 0.58.
- G2: under R1, mean log10 Bayes factor of the true cell above 0, with a 95 % bootstrap interval above 0.

If the gate fails, the scroll is not scored. At most two revisions are allowed. Each is recorded in `FORK_LOG.md` with its reason before it is run, and each is judged on a fresh test block (seeds 2001–3000, then 3001–4000). Only a passing model scores the scroll.

**Benchmark B: an independent describer (reported, not a gate).** Each 1940s map feature of class cave, aqueduct, tomb, pool, cistern or well_or_cistern becomes a one-clue entry: cave → {cave}; aqueduct → {channel_aqueduct, dam}; tomb → {tomb}; pool → {pool_reservoir}; cistern and well_or_cistern → {cistern}. The true cell is the cell of its printed position. The scoring inventory is not thinned. R1 gives 0.8 to its zone. Same metrics. These map items lie in windows around candidate places, so B favours well-recorded places; that limit is reported. Label for the scroll map: if B's 90 % coverage is at least 0.80, "calibrated on fake entries and on an independent describer"; otherwise "calibrated on fake entries only".

## Scroll outputs (only after the gate passes)

For each scored entry, under R0, R1 and R2:
- the top 5 cells, with the nearest W2B place and distance;
- the posterior of the top cell, and the areas of the 50 % and 90 % sets;
- the posterior within 1 km of each candidate place, against its prior;
- the posterior over c;
- robustness: the share of the 27 parameter pairs under which the top cell is the same.

Sensitivities: S1, records without coordinates placed at their named place; S2, 500 m cells. They are reported, not chosen between.

**Value of information.** A perfect check of cell v shows, for each clue, whether its class exists there. If v is the place, each clue is present with probability 0.8, independently. If not, the pattern follows P_bg(· | s(v)). The expected information gain of the check is the prior entropy of the entry's posterior minus its expected entropy after the check. Report the 15 cells with the largest gain summed over entries under R1, and the gain at the cells of Kh. Qumran, Kh. es-Samra and the Jericho palaces, the places of the unread records named in run 25 (Humbert & Chambon 1994, Magen & Peleg 2018 pp. 58–66, Stager 1976, Netzer *Final Reports* I). At this resolution the model cannot predict feature-level details in those records (the crack line, stair bearings), so no record prediction is registered in this run.

## Not claimed

No identification, no deposit, no change to any record. A high posterior here means "where landmark-class evidence points, given these inventories and these assumptions", not "where the place is".

## Fork log

Every change after this rule is committed goes into `FORK_LOG.md`, with the time and the reason, before it is run. All versions are reported.
