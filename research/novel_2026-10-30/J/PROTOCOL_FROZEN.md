# Lane J frozen protocol: a landscape date for the Copper Scroll list

Frozen 31 October 2026 UTC (session of 30 October 2026), branch `claude/novel-2026-10-30-J`, base `7a3b307`. This file is not edited after its freeze commit.

## 1. Claim under test

"At the proposed places of the Copper Scroll (3Q15) entries, the installations of the kinds the entries name were in existence together at one period more than at any other registered period, beyond what the regional date mix of each installation class predicts."

The test asks which registered scenario date gives the largest number of entries with at least one eligible installation in existence, compared with a permutation null and with the other scenarios. It does not test any identification, any deposit, or places outside the proposed set.

## 2. Inputs (SHA-256)

| item | path | SHA-256 |
|---|---|---|
| HA-ESI merged inventory | research/regional/haesi_features/merged_2026-10-12/features_all.csv | 23a23214ed475b5c3a3a213f29d4094518acbdf1b187cffd7c78949a635eae38 |
| ASI near places | research/regional/asi_jerusalem/features.csv | 19d1841da638ff1a3982c197126d733e98c7a6c1158757e87b92bd10acfcb6c9 |
| Caves (entry 25 lane) | research/regional/caves_entry25/caves.csv | 16ab5e3437f317fcb01a36639f66beb05c956ad49d9250a1308cd72287528f2d |
| Columbaria | research/regional/columbaria/columbaria.csv | 8262b226860de8bc1e89aa0507c9fa2f9dfa520b7d646ed30c5ed58754afa7e3 |
| Entry features | research/agent_review_2026-10-07/wave1/T02_hoard_match/entry_features.csv | a13ba89abb7c30ca40e665d95fca0910998ef3279b0d51ec5cbd99af02d9da75 |
| Place coordinates | research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v2/places_v2.csv | 315474bd3be8cce3e1776e119417e2444edd99e3f028c7413185302fc7663683 |
| Period strings | research/novel_2026-10-30/J/period_coding/strings.csv | 0885a311eeb344f5bad80d70678bf41c914f2246d9d3c26d18b6087e386e0495 |
| Coded interval table (blind) | research/novel_2026-10-30/J/period_coding/coded_intervals.csv | b52b83db970db12e6df3a61bbf2d50d1afb01c0ad78e9972dd135cffcf0913d0 |
| Coder instructions | research/novel_2026-10-30/J/period_coding/CODER_INSTRUCTIONS.md | 0a6efabdb779517a63fbf2be89a3e4f546cd3251106fefba229c05d04bb6347b |
| Checker instructions | research/novel_2026-10-30/J/period_coding/CHECKER_INSTRUCTIONS.md | 8ed1223c679e3809d9c106a3cc0fb19af5d29fffb46d3cca83dfc118b5f621fb |
| Unified feature table | research/novel_2026-10-30/J/data/features_unified.csv | 9c87c6bc9d0ef0603c5c575837f67febcb3382278a90e2d92183ce08efd4302e |
| Entry × feature eligibility | research/novel_2026-10-30/J/data/eligibility.csv | 2426be55f6d95b0aa1c35110f98629182a1b9e3143e50705e1e914535261a0bf |
| Bias check | research/novel_2026-10-30/J/bias_check.md | 27cf6ad46167b1ec2fd14c0c18057ea7b6f35a05907d7bc8f77c7676419bce53 |
| Blind log | research/novel_2026-10-30/J/period_coding/BLIND_LOG.md | badb5b37caab3fdb4ab1968b0fbcd547f5221fee952ffe306ca29419f3403f49 |
| code: build_strings.py | research/novel_2026-10-30/J/code/build_strings.py | b40e51b10396f30c4857cd84a58f0725cc5ec0191eef66a9fc1c1b66d06ce111 |
| code: make_batches.py | research/novel_2026-10-30/J/code/make_batches.py | 3a01214d1c496225fb4f7a320d35eac842b487371d5be1f99a2469a848fd518b |
| code: run_blind_coder.sh | research/novel_2026-10-30/J/code/run_blind_coder.sh | 7f5a5e47f5ad5f05cf1a2101a394a670904b9e476ba40dce1ca82a168d861a12 |
| code: merge_coded.py | research/novel_2026-10-30/J/code/merge_coded.py | b4657b2a0b22912f2983d3ac5134bb44527357e03f1bb597e4901bce65bf2260 |
| code: build_features.py | research/novel_2026-10-30/J/code/build_features.py | 252127e816d6673907de84bf3b15b04cd3e3f9fd1be02b99a99fcdb5a0b306d0 |
| code: score.py (confirmatory) | research/novel_2026-10-30/J/code/score.py | 4ceb11c574b4f12a0d213442f3f491f7e906d5ae0f2d685ea3808877f2ae9263 |

Environment: Python 3.13, numpy 2.5.3, pandas 3.0.5. Left out (reasons in `bias_check.md`): tombs, water_systems (window-driven source lineages, duplicates), peraea (dropped rows outside the window), mandate_maps (no dates), raf_1940s (no features).

## 3. Units and eligibility (no date input)

- Feature = one row of the unified table (7,366 rows: HA-ESI 3,373 non-alternate rows of nine installation classes; ASI 3,099 feature mentions of mapped classes; caves 665; columbaria 229). Class mapping and zones: `build_features.py`. Stratum = class × zone (zones of the HA-ESI phase-2 plan, plus OUT and UNZONED); 55 strata.
- Eligibility: entry landmark word → class (bias_check.md); feature within 2.0 km of a candidate place point of the entry, or placed by that place's name. 42 entries, 7,255 pairs.
- `dated_in_window`, `period_in_window`, `date_code` and `candidate_entries` are never read.

## 4. Scenarios (finite, frozen) and boundary sources

Each scenario is evaluated at one year t (negative = BCE). The interval is documentation; existence is evaluated at t.

| id | scenario | interval | t | boundary source |
|---|---|---|---|---|
| HAS | Hasmonean | 140–37 BCE | −88 | Simon's independent rule (1 Macc 13:41–42; 14:27–49) to Herod's capture of Jerusalem (Josephus, Ant. 14.465–488); E. Schürer, G. Vermes, F. Millar, *The History of the Jewish People in the Age of Jesus Christ* I (1973), §§7–13. |
| HER | Herodian (reign of Herod) | 37–4 BCE | −20 | Schürer–Vermes–Millar I §15 (Herod 37–4 BCE); t = start of the Temple rebuilding, 20/19 BCE (Ant. 15.380). |
| ERP | Early Roman before the revolt | 6–65 CE | 36 | Judaea a Roman province from 6 CE (Ant. 17.355; 18.1–2) to the outbreak of the revolt (War 2.284); Schürer–Vermes–Millar I §17. t = midpoint. |
| REV1 | First Revolt | 66–70 CE | 68 | Josephus, War 2.284 (66 CE) to the fall of Jerusalem (War 6.250, 435, August 70 CE); t = 68 CE (Vespasian's spring campaign to Jericho, War 4.449–451; branch G constraint "before June 68"). |
| INT | Between the revolts | 71–131 CE | 101 | Schürer–Vermes–Millar I §§19–20; t = midpoint. |
| BK | Bar Kokhba revolt | 132–135 CE | 134 | Schürer–Vermes–Millar I §21 (132–135 CE); W. Eck, "The Bar Kokhba Revolt: The Roman Point of View", JRS 89 (1999) 76–89. |
| LR | Late Roman (legend) | 136–324 CE | 230 | Late Roman period limits as used in the coder table; E. Stern (ed.), NEAEHL (1993) vol. 4, chronological table. t = midpoint. |
| BYZ | Byzantine (legend) | 324–640 CE | 482 | NEAEHL (1993) vol. 4, chronological table (Byzantine 324–640). t = midpoint. |

Known limit (from the coder table, before any statistic): "Herodian" and "Early Roman" are coded −37 to 70 CE, so HER, ERP and REV1 differ only through features with finer dates or stated end events.

## 5. "In existence at t"

From the blind interval (start, end, start_event, end_event, kind). A row is **dated** if kind ∈ {feature, other} and start is present. Undated = everything else (kind undated, relative, site, finds, empty text, no start).

- **persist (primary)** — the task's definition "built before it, and not abandoned or destroyed before it, as the source states": dated row exists at t if start ≤ t and not (end_event = yes and t > end); otherwise it does not exist. A row with only an end year and end_event = yes does not exist at t > end.
- **attested (sensitivity)**: dated row exists at t if start ≤ t ≤ end.
- **persist_sitefinds (sensitivity)**: as persist, but kinds site and finds also count as dated.
- **Bounds**: best = every undated row exists at t; worst = no undated row exists at t.

## 6. Statistics and null

- **S1 (primary, the task's statistic)**: number of the 42 entries with ≥ 1 eligible feature in existence at t.
- **S2 (secondary)**: mean over the 42 entries of the share of the entry's eligible features in existence at t.
- **Null**: permute the full coded record (start, end, events, kind, i.e. the row's date) among all features of the same stratum (class × zone), including non-eligible features; 10,000 permutations; numpy `default_rng(20261030)`; one permutation set shared by all scenarios, rules and bounds. Recompute S1 and S2.
- Per scenario: z = (obs − null mean) / null sd; upper p = (1 + #{null ≥ obs}) / 10,001.
- Winner per (statistic, rule, bound): the scenario with the largest z. Scenario comparison: for each other scenario r, d = z_win − z_r, compared with the same difference over the permutations; p_diff = (1 + #{d_perm ≥ d_obs}) / 10,001.

## 7. Decision rule

For a statistic, under rule persist, the test **passes** if all hold:
1. the best-bound and worst-bound winners are the same scenario;
2. in both bounds the winner's p ≤ 0.05 / 8 = 0.00625 (Bonferroni over 8 scenarios);
3. in both bounds p_diff ≤ 0.05 against every other scenario.

- **Obtained**: S1 passes (name the winner).
- **Partly**: S1 fails and S2 passes (name the winner); or S1 passes under persist but the sensitivity rules give a different winner (reported).
- **Not obtained**: S1 and S2 both fail.
- **Failure condition**: no scenario separates from the null, or the bounds disagree (different winners, or one bound fails). Then the AGENTS.md closing result is **not identifiable from available evidence**. If S1 passes, the closing result is **supported relative to the registered alternatives** for the claim of §1, with the winning scenario; no identification or deposit claim follows. **Rejected** applies to a scenario when its z is ≤ 0 in both bounds while another scenario passes (it is then contradicted relative to the winner).
- Expected structural limit (seen on fake data in the self-test, not on real dates): with many undated features, S1 in the best bound saturates (all entries counted in every scenario), which makes the bounds disagree. This is a property of the record, and the rule is not changed for it.

## 8. Exposure before freeze

Seen before freeze: the inventories' columns and value counts; ~100 period strings (samples and those naming revolts or Bar Kokhba, to check content); the coded table's kind and confidence counts and its kind × inventory crosstab; the check-sample disagreements; counts of eligible pairs per entry and class. Not seen: any existence count at any scenario year, any null, any statistic on the real coded dates. Development runs used only fake intervals (`score.py --selftest`, `--planttest`; outputs in `data/devtests/`). The planted test (fake 60–70 CE dates for 30 % of eligible features) was detected by S2 in the worst bound (REV1 z = 5.2) but not by S1 or by the best bound, so the test has low power under the S1 statistic.

## 9. One confirmatory run

`python3 research/novel_2026-10-30/J/code/score.py` once, after the freeze commit. Outputs: `scenario_counts.csv`, `confirmatory_result.json`.
