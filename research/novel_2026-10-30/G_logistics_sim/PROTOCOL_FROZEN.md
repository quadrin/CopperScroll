# Direction G: logistics simulation of the concealment (frozen protocol)

Written 30 Oct 2026 by worker G, branch `claude/novel-2026-10-30-G`, before any run on the scroll's real amounts. Novel-direction session (Tier 1, direction G). Exploratory under AGENTS.md: it bears on the unit reading and on placement priors, not on any identification. It changes no rating, ledger, ACTIVE_TEST or atlas data.

## Claim tested

Carrying the weighed metal listed in 3Q15 from an origin to its hiding places, at night, with a crew small enough to keep the secret, inside a dated 66–70 CE window, is physically feasible under the karsh reading but not under the talent reading. The alternatives are that the reading changes nothing, or that feasibility turns on parameters no source constrains.

## Novelty gate

Searched `main` (7a3b3074) and `sb` (eb0ef639) for porter, donkey, mule, logistics, person-night, Sobol and Monte Carlo, plus `research/logs/`. No logistics or load model exists. The nearest precedents are:
- Run 21 (`sb:sandbox/amount_gravity_2026-10-27`). It correlated each entry's mass with its walking time from the Temple. Its result was underpowered with the sign reversed.
- Run 8 (`route_travel_time_2026-10-27`). It tested whether the entry order is a walking route.
- Method 10 / run 4. These matched sums against hoards by weight.
- T08 `unit_totals.csv`. It gives the total tonnage under each reading.

None of these converts mass into loads, trips, crew-nights or dated windows. None asks whether an operation is possible, and none runs a global sensitivity analysis. The walking-time engine (Tobler on GLO-30) is reused unchanged.

## Prior exposure (logged)

Before freezing I knew the following:
- T08's totals: about 80 t (talent reading) vs about 56 t (karsh reading) at 21.3 kg per talent. The whole-scroll talent/karsh mass ratio is therefore only 1.42, because the large ככרין sums (entries 3, 29, 47, 58) are talents under both readings. I computed this ratio from `scroll_sums.json`: kk 1,117.5 units, ככרין/ככר 2,637.3 talents.
- Run 21's walking times and verdict.
- The walking-time input built below (`inputs/walk_times_90m.json`). It is an input, not a result.

The smoke run replaced every sum with value 1, so it used no real amounts. It showed only that the code runs. Its outputs are in `/root/novel/data_G/smoke/` and are not in the repo.

## Inputs (sha256)

| Input | Path | sha256 |
|---|---|---|
| 45 weight sums (unit ככ 30, ככרין 14, ככר 1; status ok/uncertain; displayed values), from method 10 | `research/first_tests_2026-10-24/method10_hoards/scroll_sums.json` (main) | `6ebb98c0069b210c1d41a9b6a1666a3200f590c5f3e2670dd120423857144652` |
| Their parent amount table, T08 | `research/agent_review_2026-10-07/wave1/T08_real_or_legend/data/scroll_amounts.csv` | `f19960d49c4f8817a0ecf8c4f86bda6c32d6e5c76bddaf1ac5cae3d98ca73091` |
| Placement scenarios: W2B K2 model v3 posterior per entry and state. Used as scenarios, not as truth | `research/agent_review_2026-10-07/wave2/W2B_model_v1/outputs_v3/posteriors_v2_v3.csv` (column `P_v3`) | `832a3bea95db898652a4583122169eabcb7670f5384961d1dffc989a73ce1e4b` |
| Its gazetteer: 50 places, 11 regions, mixtures | `.../W2B_model_v1/inputs_v3/places_v3.csv` | `381894a6e383d8f763197048d751bc8c89a5506144b295b3b77d338cc9ad3b9c` |
| Copernicus GLO-30 DSM, 4 tiles N31–32 E034–035 (from `https://copernicus-dem-30m.s3.amazonaws.com/`) | `/root/novel/data_G/dl/` | listed in `inputs/dem_sha256.txt` |
| Walking times (Tobler, 90 m, 8-neighbour, run 8/21 edge construction, box 31.25–32.85 N, 34.90–35.85 E), out and back, from the Temple, Kh. Qumran and Tell es-Sultan to every place, mixture component and region centroid (the U_ states) | `inputs/walk_times_90m.json`, built by `scripts/walk_times.py` | `8c631251478eca7f580bc63a7aa3074e51abfd045ff1895669cf4e4313dc9907` |
| Josephus, *Jewish War*, Whiston translation, Project Gutenberg #2850 | `/root/novel/data_G/src/josephus_war_whiston_pg2850.txt` | `9a72663aefa6b22bb4398d5f878bb027c6b6de839e7cbe744a34240505fd8d20` |
| Mishnah Shekalim 5, Sefaria API (William Davidson edition) | `/root/novel/data_G/src/shekalim5.json` | `a1da6d744df46d68c8bf2adc2e195bc5a1b0ed1ff7811d530bfacd3eb094e03c` |
| Model code | `scripts/sim.py` | `e795c38f9790b658bad15c64975bdd5f887beebc019ca258aaa45237c779548e` |
| GLO-30 decoder (copied from `sb:sandbox/route_travel_time_2026-10-27/scripts/read_cop.py`) | `scripts/read_cop.py` | `2b523b4a6f5e2904eb8c9e2d6186b38ad788e7ac3f51c87ac8409a247db37972` |
| Walking-time builder | `scripts/walk_times.py` | `3ed194819f0bdf92dc2e04f605fb8eaec6204521a6df14708bc2169b0177eec2` |

Walking-time check against run 21 (30 m): Mar Saba out 2.88 h here vs 3.01 h; Beth-shean 19.5 h vs 19.9 h. The difference comes from the 90 m grid.

## Model

The model works at trip level, by Monte Carlo with common random numbers. Each draw takes one value of every parameter, one placement of every weighed entry (42 entries, 45 sums), one origin, one transport mode and one unit reading.

1. **Mass per entry** (kg) = Σ over the entry's sums of value × unit factor × talent_kg.
   - *talent* reading (Milik, Allegro): ככ = ככרין = ככר = 1 talent.
   - *karsh* reading (Lefkovits 2000; Puech 2006): ככ = 1/300 talent; ככרין and ככר = 1 talent.
   - *all_small*: every unit = 1/300 talent. This is a hypothetical lower bound with no source, reported only as a bracket.
2. **Loads** per entry = ceil(mass / L). L is the load per porter or per animal.
3. **Round trip** (h) = out_h / (f_night × f_load) + back_h / f_night + 0.5 h handling. Out and back are the asymmetric least-cost Tobler times from the origin.
4. **Carrier-nights per load**: if H ≥ round trip, 1/floor(H / round trip). Otherwise ceil(round trip / H), meaning several nights spent in hiding. H is the usable walking hours per night.
5. **Person-nights** P = Σ loads × carrier-nights per load, divided by k (animals per handler) for animal modes, plus overhead × (number of weighed entries).
6. **Crew required** N_req = P / (T_max × duty), where T_max is the window's length in nights.
7. **Corridor rule**: every entry's destination must be reachable in the window, or the draw fails.

## Scenarios (frozen)

- **Readings**: talent, karsh, all_small.
- **Origins**: Temple Mount (`jer_temple`); Kh. Qumran (`kh_qumran`); Jericho, Tell es-Sultan (`tell_es_sultan`).
- **Place spreads**:
  - *map*: each entry at its v3 MAP state. A mixture uses the mean of its members' times.
  - *posterior*: the state is sampled from v3 `P_v3`, renormalised over states ≥ 0.001, and a mixture member is sampled.
  - *uniform*: one of the 50 listed places, sampled uniformly.
  - *local*: every entry at the origin region's U_ centroid. This is a minimum-distance bracket.
- **Modes**: porter, donkey, mule. Animal modes carry k animals per handler.
- **Windows**, from Josephus, Whiston/Gutenberg (Julian equivalents are approximate, ±1 month):
  - **W1 open**, 575 nights: from 8 Dius 66 (Cestius routed; BJ II 19.9) to 3 Desius 68 (Vespasian reaches Jericho; BJ IV 8.1). All destinations are reachable from all origins.
  - **W2 encircled**, 665 nights: from 3 Desius 68 to 14 Xanthicus 70 (Titus encamps; BJ V 13.7). BJ IV 9.1 has Vespasian "erected citadels at Jericho and Adida" and Jerusalem's people "deprived of the liberty of going out of the city". Only the Temple origin is usable, and only JER-region destinations.
  - **W3 sealed**, 115 nights: from 14 Xanthicus 70 to 10 Lous 70 (the Temple burns; BJ VI 4.5). Titus' wall of 39 furlongs went up in three days (BJ V 12.2). Only the Temple origin is usable, and only JER-region destinations within 0.35 h walk of the Temple (an intramural proxy).
- **Crew sizes** N: 3, 10, 20, 50, 100, 300.
- **Secret-keepable crew**: N_SECRET = 10. Mishnah Shekalim 5:2: "no fewer than seven trustees [amarkolin] and three treasurers".

## Parameter priors (uniform; frozen)

| Parameter | Range | Source or class |
|---|---|---|
| talent_kg | 20.4–42.6 | Light talent 21.3 kg (Lefkovits 2000 p. 473, via the method 10 registration). Heavy talent 42.6 kg (3,000 × 14.2 g). The 58.9 kg "heavy common" talent in T08 is left out because it comes from Wikipedia only. *Sourced* |
| load_porter | 20–60 kg | Roman soldier 20–45 kg total kit; Marian legionary about 55 kg (Łuć 2018, via imperiumromanum.pl "Marius' mules"). Head-carrying porters can exceed body mass (Bastien et al. 2016, *J. Exp. Biol.* 219:3626); that extreme is left out. *Sourced* |
| load_donkey | 50–100 kg | Donkey 80–100 kg, 24–30 km/day (Cotterell & Kamminga 1990 p. 194, cited in Adams 2007 OXREP WP). Lower bound 50 kg as a welfare-limited load (assumption). *Sourced* |
| load_mule | 90–200 kg | US Army limit of 20 % of body mass, about 91 kg; Indian 1965 rules cap mules at 200 kg (Wikipedia "Pack animal"). *Sourced* |
| k_animals | 1–4 (integer) | Animals per handler. *Unconstrained* |
| f_load | 0.6–1.0 | Ratio of loaded to unloaded speed. Loaded porters walk 3–4 km/h (Bastien et al. 2016, EurekAlert release) vs Tobler's 5 km/h on the flat. *Sourced* |
| f_night | 0.5–0.9 | Night-speed factor. *Unconstrained* |
| hours | 6–10 h | Usable walking hours per night. Night lasts 9.8–13.9 h at 31.78 N (computed; solstices). *Sourced (bounded)* |
| duty | 0.5–1.0 | Fraction of nights worked. *Unconstrained* |
| overhead | 1–10 | Person-nights to dig, conceal and mark each weighed entry. *Unconstrained* |
| T_op (Sobol Y2 only) | 7–575 nights, log-uniform | Length of the operation. *Unconstrained* |

Fixed values: 0.5 h handling per round trip; 4,000 Monte Carlo draws per cell; seed 20261030.

## Feasibility criterion

A draw is **feasible** at crew N in window W when two conditions hold:
- every weighed entry's destination is reachable under W's corridor rule;
- N_req ≤ N.

F is the fraction of feasible draws.

A secondary check counts an entry as **single-trip feasible** when two conditions hold:
- its loads ≤ N carriers (or N × k animals);
- its round trip fits within one night's H.

## Outputs (named exactly)

- `out/feasibility_envelope.csv`: one row per reading × origin × spread × mode × window × N (3 × 3 × 4 × 3 × 3 × 6 = 1,944 rows). Columns: F, route fraction, person-night quantiles, N_req quantiles, median tonnes, single-trip fractions.
- `out/sensitivity_indices.csv`: Sobol first-order (S1) and total (ST) indices with confidence intervals, from SALib Saltelli sampling and Jansen/Saltelli estimators. Base N = 4,096, giving 69,632 evaluations per setting.
  - Factors: reading, talent_kg, mode, three loads, k, f_load, f_night, hours, overhead, origin, placement (index into 2,048 posterior placements per origin), duty, T_op.
  - Settings: A = {talent, karsh}; B = {talent, karsh, all_small}.
  - Outputs: Y1 = log10 person-nights; Y2 = log10 crew required = Y1 − log10(T_op × duty).
- `out/paired_ratio_talent_karsh.csv` and `out/summary.json`.

## Decision rule (frozen)

Main cells are origin (3) × spread {map, posterior} (2) × mode (3) = 18, each evaluated in window W1 at N = 10. In each cell:
- **excluded**: F_talent < 0.05 and F_karsh ≥ 0.50;
- **constrained**: otherwise, if F_karsh − F_talent ≥ 0.25;
- **unaffected**: if |F_karsh − F_talent| < 0.25;
- **other**: anything else.

Overall verdict on the talent reading:
- **excluded** if at least 12 of 18 cells are excluded;
- otherwise **constrained** if excluded + constrained ≥ 9;
- otherwise **unaffected** if unaffected ≥ 10;
- otherwise **mixed**.

W2 and W3 are reported in full but do not enter the verdict. Their corridor rules exclude non-Jerusalem spreads by construction.

## Failure conditions

- **F1 (no discrimination)**: the overall verdict is *unaffected*. Feasibility is then insensitive to the unit reading across the frozen ranges.
- **F2 (unconstrained parameters dominate)**: in Sobol setting A for Y1, either ST(reading) < 0.05, or ST(reading) < the largest ST among the unconstrained parameters k_animals, f_night and overhead. The result then depends mainly on parameters no source constrains.

## Outcome classes (AGENTS.md closing line)

- **Obtained**: both datasets are produced, the verdict is *excluded* or *constrained*, and neither F1 nor F2 fires.
- **Partly**: both datasets are produced, but the case is neither obtained nor not obtained. That covers exactly one of F1 or F2 firing, or a *mixed* verdict with no more than one of F1 or F2 firing. The envelope then still stands as a prior generator.
- **Not obtained**: both F1 and F2 fire, or the datasets cannot be produced.

Any change after seeing results is a new, labelled exploratory model.

## Run

```
python3 -I scripts/sim.py /root/CopperScroll inputs/walk_times_90m.json out
```
