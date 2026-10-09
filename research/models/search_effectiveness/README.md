# Search effectiveness in the joint placement model

**What it is.** A layer over the W2B joint placement model (K2) that turns "someone looked here and recorded nothing" into a likelihood factor, with a 46-row looks table, five failure-mode scenarios and a probe of the next records.\
**Main result.** Only 2 of 22 silent or absent looks in the repository have a detection probability that is not null, both editorial "no mound" claims (ʿAyn Feshkha, ʿAyn el-Ghuweir). So the coded looks barely move the model (largest change: entry 4, total variation 0.031), and 99.99% of the posterior mass, averaged over all entries, sits in states whose combined detection probability is below 0.2.\
**What stays unknown.** The detection probability is null or zero for 20 of 22 negative looks, including every look the project cites against Kh. Yanun, Kh. el-Marjama and the ground north of Tell es-Sultan. This identifies nothing.

Exploratory method work, 9 October 2026. No registered result, outcome count or identification changes. Labels: EVIDENCE (what a source says), INFERENCE (our reasoning), CLAIM (an author's assertion without a cited field record).

## The idea and the gap

After AF447 (2011), Metron gave each failed search its own probability of detection. It also built a map that assumed the beacons had failed. Probability flowed back into an area the acoustic search had "cleared", and the wreck was there. An unsuccessful look is evidence only as good as its detection model.

The W2B model places each entry over 49 places and 11 "unlisted site" states (one per region). It uses priors, name groups and entry order. It never used a look that found nothing. The methods round of 8 October measured such looks separately ([coverage](../../feature_workbench/coverage/README.md), [observation process](../../rarity/kohlit/observation_process/README.md)). This folder joins them to the model.

## How a look enters the model

- For a silent or explicit-absence row: pd = coverage × p_recognise × p_report × p_survive, and the factor is 1 − pd on that entry's place state.
- Any null number makes the factor 1. Unknown stays unknown.
- Rows from one field lineage count once (the largest pd). Different lineages multiply.
- A reported row adds no factor. Positive evidence belongs to the candidate odds in `candidates_v1.csv`. Each reported row is checked for double counting against them.
- If a reported row fully satisfies the requirement at a target (entry, place, relation), silences at that target add no factor.
- Factors multiply the W2B likelihood rows after name-group tempering, and are not tempered. Each row concerns a separate record and a separate required feature.
- The W2B code is imported by path and never changed. With every factor equal to 1, `search_model.run` reproduces the W2B K2 default exactly: posteriors bit for bit, log marginal likelihood equal, and the recorded `outputs_fixed/kernel_sensitivity.csv` row matched (tests).

## The looks table (`looks.csv`)

One row per (entry, place state, required feature, record). 46 rows: 24 reported, 20 silent, 2 explicit absences. They cover entries 4, 11, 15, 19 and 60 (Koḥlit), 25 and 29.

| Column | Meaning |
|---|---|
| look_id | L01–L46 |
| entry_id, place_id | W2B entry and state (a `places_v1` place or `U_<region>`) |
| relation_id | The required relation; for Koḥlit the ids of [chain.json](../../assessments/kohlit_chain/chain.json) |
| required_feature | What the entry needs at that place |
| reading_condition | Reading keys that switch the row on (`tel=mound`, `xii10=janoah`, `kohlit15=yes`, `e4cleft=immersion`) |
| placement_relevant | `no` for a look at a deposit target; such a row never enters the placement model |
| record, record_key, record_id | Citation with page; short author-year key; chain.json record id |
| lineage | Field campaign or observation lineage, for deduplication |
| looked_at | The area or volume the record covers, with its source |
| coverage, p_recognise, p_report, p_survive | Numbers in 0–1, or empty (null) |
| *_basis | EVIDENCE or INFERENCE with the reason, or UNKNOWN with the reason |
| result | reported / silent / explicit_absence |
| result_basis | EVIDENCE, CLAIM or INFERENCE |
| satisfies_requirement | For reported rows: yes / partly / unknown / no |
| counted_via | Where a proposer used this feature, so the candidate odds already count it |
| project_use | Where the project treats this record as a look |
| notes | Short notes |

`next_records.csv` lists 11 records that could become the next look at a target, with access tier and whether they can contradict (from the [Koḥlit chain](../../assessments/kohlit_chain/README.md)).

### Where the table is thin

- Every row comes from records already in the repository. No new source was read except Puech 2015 p. 14 n. 49, to check the two quotes.
- 54 of 61 entries have no row. Their factors are 1 by construction.
- Of 22 negative rows, only L03 and L04 have every number. Both are an editor's statement (CLAIM), not a field record. All four of their numbers are INFERENCE: coverage 1.0, recognition 0.9, reporting 1.0, survival 0.9 (pd 0.81).
- Three rows carry an evidenced zero: Zohar's spring-area record has zero coverage of the east sector (L15); Kenyon skipped the strip just north of the tell (L32, II p. 169); CORONA cannot resolve 1–2 m openings (L35).
- The remaining 17 negative rows have at least one null. Most have four.
- Kuḥlah, Carmel and Transjordan have no look at all. The other controls got unequal looks: Puech commented on Feshkha and Ghuweir, nobody on Mount Zion or Beit Kahil. Under search theory a looked-at state loses mass and an unlooked one gains it. That is correct only if the pd values are right.

## Scenarios (frozen)

[PLAN.md](PLAN.md) holds the values. The caps apply only where the coded value is higher.

| Scenario | Meaning | Change |
|---|---|---|
| S0 | as coded | none |
| S1 | features often destroyed before the look | p_survive ≤ 0.3 |
| S2 | features not recognised (a cistern or tomb mouth logged as a quarry or modern pit) | p_recognise ≤ 0.3 |
| S3 | seen but never published | p_report ≤ 0.3, silences only |
| S4 | every look uninformative | pd = 0 (the W2B K2 default) |

Reading sets: R-P (main; Puech's "mound", W2B default XII 10 reading, Koḥlit restored in entry 15), R-E (Eshel's "ruins"; the mound rows switch off), R-J (XII 10 read as Janoaḥ; the Kh. Yanun rows switch on).

## Results

### 1. Factors below 1

| Reading set | Scenario | Entry | Place | Factor | Row |
|---|---|---|---|---|---|
| R-P, R-J | S0, S3 | 4 | ein_feshkha | 0.190 | L03 |
| R-P, R-J | S0, S3 | 4 | ein_ghuweir | 0.190 | L04 |
| R-P, R-J | S1, S2 | 4 | ein_feshkha | 0.730 | L03 |
| R-P, R-J | S1, S2 | 4 | ein_ghuweir | 0.730 | L04 |

No other target has a factor below 1 in any scenario. Under R-E, S0–S3 equal S4 exactly. S3 equals S0 everywhere, because no silent row has a number.

### 2. Change against S4 (total-variation distance, R-P)

| Entry | Title | S0 | S1 | S2 | S3 |
|---|---|---|---|---|---|
| 4 | The mound of Kohlit | 0.0315 | 0.0103 | 0.0103 | 0.0315 |
| 19 | The Kohlit pit | 0.0157 | 0.0051 | 0.0051 | 0.0157 |
| 60 | The final Kohlit entry | 0.0144 | 0.0047 | 0.0047 | 0.0144 |
| 15 | Kohlit's great cistern | 0.0142 | 0.0046 | 0.0046 | 0.0142 |
| 11 | Kohlit's pool | 0.0128 | 0.0042 | 0.0042 | 0.0128 |
| 3 | The great courtyard | 0.0034 | 0.0011 | 0.0011 | 0.0034 |
| 5 | The winding stair | 0.0033 | 0.0011 | 0.0011 | 0.0033 |
| 59 | Bezek? | 0.0024 | 0.0008 | 0.0008 | 0.0024 |

21 more entries change by between 0.0001 and 0.002 (all in `results.json`). Under R-J the pattern is the same and slightly smaller (entry 4: 0.0264); entry 60 then leaves the Koḥlit group and does not change.

### 3. Where the mass goes (R-P, S0 minus S4)

| Entry | State | S4 | S0 | Change |
|---|---|---|---|---|
| 4 | ein_feshkha | 0.0261 | 0.0051 | −0.0210 |
| 4 | ein_ghuweir | 0.0131 | 0.0026 | −0.0106 |
| 4 | U_JER | 0.1856 | 0.1916 | +0.0061 |
| 4 | U_JERICHO | 0.0632 | 0.0653 | +0.0021 |
| 4 | tell_es_sultan | 0.0215 | 0.0222 | +0.0007 |
| 4 | ein_samiya | 0.0167 | 0.0173 | +0.0006 |
| 60 | ein_feshkha | 0.0280 | 0.0233 | −0.0047 |
| 60 | U_QUMRAN | 0.0461 | 0.0425 | −0.0036 |
| 60 | U_JER | 0.1915 | 0.1952 | +0.0037 |
| 3 | jer_temple | 0.3039 | 0.3063 | +0.0025 |

- EVIDENCE (model output): for entry 4, the QUMRAN region loses 0.029. Jerusalem gains 0.018 and Jericho 0.005.
- EVIDENCE (model output): entry 60 has no look at Feshkha, yet its Feshkha probability falls by 17%. The shared Koḥlit latent carries entry 4's look to entries 11, 15, 19 and 60. This is the joint modelling the AF447 lesson asks for.
- INFERENCE: the freed mass goes mostly to unlisted Jerusalem states and the Temple. The block-A itinerary prior decides that, not any look. W2B calls that pull circular.
- Under S1 or S2 (the "beacon failed" maps), about two thirds of the move disappears (entry 4: 0.0315 to 0.0103).

### 4. Unsearched mass (combined pd < 0.2; R-P, S0; mean over all 61 entries)

| Region | Mass | Unsearched | Searched |
|---|---|---|---|
| JER | 0.4839 | 0.4839 | 0 |
| JERICHO | 0.1889 | 0.1889 | 0 |
| QUMRAN | 0.1310 | 0.1308 | 0.0001 |
| SOUTH | 0.0561 | 0.0561 | 0 |
| NORTH | 0.0526 | 0.0526 | 0 |
| DESERT | 0.0503 | 0.0503 | 0 |
| HEBNEG | 0.0119 | 0.0119 | 0 |
| WEST | 0.0089 | 0.0089 | 0 |
| SAMDES | 0.0069 | 0.0069 | 0 |
| CARMEL | 0.0055 | 0.0055 | 0 |
| TRANSJ | 0.0040 | 0.0040 | 0 |

Searched mass in total: 0.0001. Only two states are "searched": entry 4 at Feshkha and at Ghuweir (0.0077 of entry 4's mass). For entries 11, 15, 19 and 60 the searched mass is 0. Per entry and region values are in `results.json`.

### 5. Phantom coverage

Places the project treats as looked at, where pd is null or below 0.2:

| Look | Entry | Place | Record | Why pd is low or null |
|---|---|---|---|---|
| L39 | 60 | kh_yanun | Highlands 1997 pp. 828–831 | all four null; no cistern or tomb field; isolated features went to unpublished lists (p. 12) |
| L40 | 60 | kh_yanun | SWP II p. 394 | all four null |
| L37 | 60 | ein_samiya | Mazar 1995 p. 97, Fig. 7 | summit excavation only; all null |
| L16 | 11 | ein_samiya | Zohar 1981, HA 76 p. 19 | squares by the spring, SW of the tell; all null |
| L15 | 11 | ein_samiya | Zohar 1980, IEJ 30 p. 219 | coverage of the east sector is 0 (same campaign as L16) |
| L17 | 11 | ein_samiya | Mazar 1995 pp. 85–87 | description scope not stated; all null |
| L20 | 11 | ein_samiya | SWP II p. 394 | all null |
| L32 | 60 | tell_es_sultan | Kenyon II p. 169 | coverage 0: the strip just north was never searched |
| L35 | 60 | tell_es_sultan | CORONA DF041 (1967) | p_recognise 0: openings below resolution; camp over the ground |
| L36 | 60 | tell_es_sultan | BS Pal. 1031 (1918) | frame not registered; resolution not recorded |
| L13 | 11 | tell_es_sultan | Warren 1876 pp. 162–197 | silent although a basin existed (calibration case) |
| L25 | 15 | tell_es_sultan | Nigro 2011; SWP III (W2C F5 "absent") | compiled catalogue; all null |
| L09 | 4 | tell_es_sultan | NEAEHL 5 p. 1799; Nigro 2011 p. 273 (W2C F3 "absent") | all null |
| L10 | 4 | ein_samiya | Zissu 2001; WBADB (W2C F3 "absent") | all null |
| L06 | 4 | beit_kahil | SWP III p. 303 (W2C F1 "absent") | coverage and p_report null |
| L23 | 11 | beit_kahil | SWP III p. 303 (W2C F4 "absent") | all null |
| L07 | 4 | mount_zion | Zissu 2001 p. 148; Goranson 2002 p. 228 | an argument about a word, not a ground look |
| L22 | 11 | muhalhil | Bar-Adon 1972 via Zissu p. 148 | Bar-Adon not read; all null |
| L24 | 11 | ein_ghuweir | WBADB and SWP screen (S4546) | WBADB cannot state an absence; all null |
| L44 | 25 | U_JERICHO | Sion 2002 p. 63 n. 11 (L-656) | deposit target, 8 of 8 joins undeterminable; outside the placement model |

- INFERENCE: the W2C feature matrix scores "ABSENT_IN_SOURCES" as 0, the same as "not covered". That treats silence as absence in six cells above.
- INFERENCE: the follow-up line "Kh. Yanun: nothing beyond the place-name" rests on L39 and L40. Both have unknown pd. KERNEL_CORRECTION.md already says so.

### 6. Double counting against `candidates_v1.csv`

No reported row adds a factor, so nothing is double counted here. The check says what a future positive factor would double count:

- 15 of 24 reported rows describe a feature the candidate odds already rest on. One is cited in the candidate source (Zissu 2001, L02). Nine are features the proposer used (Puech 2015 p. 13 n. 49 for Tell es-Sultan; Zissu 2001 pp. 150–151 for ʿEin Samiya). Five more describe the same feature class at the same target (for example Dorrell 1993 and Nigro cat. 21 on the spring basin Puech used).
- 7 rows have a candidate row that does not use them: Bar-Adon's small structure at Muhalhil (L05), the Jericho conduits (L08), Kenyon's Early Bronze cistern (L26), Beit Kahil's tombs (L30), the Yanun village burial caves (L41) and the entry-29 pools (L45, L46, whose candidates are order-derived).
- 2 rows are positive evidence the model cannot use, because no candidate row exists: Kh. Qumran's northern caves and cemetery for entry 60 (L42), and IV/17 for entry 25 (L43). INFERENCE: IV/17 lies about 2.8 km NW of Tell es-Sultan, in the unlisted Jericho state, while the model's entry-25 candidate is kh_qumran (order-derived).
- Absences are not reflected in the odds: all ten Koḥlit proposals carry the same odds (0.111) for each Koḥlit entry, including Feshkha, whose source column already notes Puech's rejection.

### 7. Probes: one more silent record at a target

Each probe adds one silent look with pd 0.5 or 0.9 on top of S0. P = probability of the entry at the place.

| Probe | Entry | Place | Record | Access | Can contradict | P now | Change at 0.5 | Change at 0.9 | Most moved other entry (0.9) |
|---|---|---|---|---|---|---|---|---|---|
| P11 | 60 | kh_qumran | 2002 cave-survey entries; IAA records | supplied, unread | under Milik's reading only | 0.0122 | −0.0061 | −0.0110 | 19 (TV 0.0049) |
| P05 | 60 | tell_es_sultan | Kenyon III plate volume (E section, Pl. 111b) | library | quarry branch only | 0.0219 | −0.0108 | −0.0197 | 15 (TV 0.0100) |
| P02 | 60 | ein_samiya | Kallai 1972 pp. 172–173 | library | only by explicit absence | 0.0183 | −0.0091 | −0.0164 | 19 (TV 0.0083) |
| P01 | 11 | ein_samiya | Kallai 1972 pp. 172–173 | library | yes | 0.0155 | −0.0077 | −0.0140 | 60 (TV 0.0073) |
| P03 | 4 | muhalhil | Bar-Adon 1972 p. 118 | library | only by explicit absence | 0.0134 | −0.0067 | −0.0121 | 19 (TV 0.0045) |
| P04 | 11 | muhalhil | Bar-Adon 1972 p. 118 | library | only by explicit absence | 0.0112 | −0.0056 | −0.0101 | 19 (TV 0.0038) |
| P06 | 60 | tell_es_sultan | Garstang, PEF, Nigro pre-camp records | requested | no (confirm only) | 0.0219 | −0.0108 | −0.0197 | 15 (TV 0.0100) |
| P07 | 60 | tell_es_sultan | Kenyon field records | archive order | N.S.1 branch only | 0.0219 | −0.0108 | −0.0197 | 15 (TV 0.0100) |
| P09 | 11 | ein_samiya | RAF verticals 1945 | archive order | dark square only | 0.0155 | −0.0077 | −0.0140 | 60 (TV 0.0073) |
| P10 | 60 | kh_yanun | field survey (R-J reading only) | fieldwork | only with a complete dated record | 0.5779 | −0.1715 | −0.4575 | 59 (TV 0.0667) |
| P08 | 11 | tell_es_sultan | sealed contexts under the basin rim | fieldwork | yes | 0.0181 | −0.0090 | −0.0163 | 15 (TV 0.0087) |

- EVIDENCE (model output): under the K2 default, no Koḥlit proposal holds more than about 4% for any Koḥlit entry (the largest is Mount Zion, pulled by the Jerusalem itinerary, or Feshkha for entry 19). A silent look can therefore move a proposal by at most a few hundredths. The biggest lever is Kh. Yanun under the Janoaḥ reading (P = 0.58), and it needs fieldwork.
- INFERENCE: the cheapest records that can deliver a high pd are Kallai 1972 pp. 172–173 (one scan, two targets: P01 and P02) and the Kenyon III plate volume (P05). The requested pre-camp records (P06) cannot deliver a high pd for a silent result: photographs can confirm an opening but not rule one out. Their probe numbers are reachable only by an excavation record.
- Each Koḥlit probe moves the most affected other Koḥlit entry by 0.37–0.53 of the change in its own entry, through the shared latent.

## What stays unknown, and why

- The detection probability of almost every look. Survey entries state no search area; gazetteers compile; excavation footprints are unpublished (coverage README); W2C's "absent" cells are silences.
- Whether the two Puech claims rest on a field look. They are editorial. Under Eshel's "ruins" reading they do not apply at all.
- Positive evidence. This layer handles only silences. Unused positive evidence (L42, L43) needs a candidate decision, not a factor.
- Where the freed mass should go. In this model the itinerary prior decides it.

## Run and test

From the repository root (Python 3 with numpy, which the W2B model needs; this layer adds no other dependency):

```sh
python3 -I research/models/search_effectiveness/run_analysis.py --tables
python3 -I -m unittest discover -s research/models/search_effectiveness -t research/models/search_effectiveness
```

The run takes about 6 s and refuses to start if `looks.csv` or `next_records.csv` differ from the hashes in PLAN.md. The 14 tests check: factor 1 reproduces W2B exactly (and the recorded K2 run); a pd of 0.9 on a one-place toy cuts that place's odds by exactly 10×; nulls are inert; lineage, dominance, reading gates and caps; table validity; the freeze hashes; determinism and agreement with `results.json`.

## Files

| File | What it is |
|---|---|
| `PLAN.md` | Frozen scenarios, readings, thresholds, probe values and input hashes |
| `looks.csv` | The looks table (46 rows) |
| `next_records.csv` | Records for the probe (11 rows) |
| `search_model.py` | The layer: loading, validation, pd, factors, W2B wrapper |
| `run_analysis.py` | The frozen analysis; writes `results.json`; `--tables` prints the tables above |
| `results.json` | All outputs, rounded to 8 decimals; posteriors stored for states at or above 0.001 |
| `tests/test_search_model.py` | 14 unittest tests |

## Freeze record

- PLAN.md SHA-256: `c2f044311ea676c7819b376a5f5e7d10ad3c1245b90b2beb4be9711a1d4db817`, recorded 2026-10-09T18:18:33Z, before any scenario was run.
- looks.csv SHA-256 `6a0420fcef8d08e00ac483810f39ac6ca442cbe6769c269a4f550ce1002af0da`; next_records.csv SHA-256 `62fa74497c59ae4470347e0e5fdd303d40ad718b2d732bc468c46902964e33ad` (both inside PLAN.md).
- Changes after the first run, none affecting any number: the validator now accepts an EVIDENCE note on a null number (L19 failed it; the table was not changed); the double-count check also flags rows on a target where the proposer used the same feature class (L12, L14, L19, L21, L34 changed status); absence rows use the odds of their own reading set (L39, L40); `results.json` stores posteriors at or above 0.001 and the S4 posterior for unchanged entries.

## Sources

All inputs were already in the repository: W2B model and inputs; the coverage and observation-process modules; the rarity sheets and stage-1 screens; follow-up reports A–D; W2A, W2C and W2G reports; the Koḥlit chain; the entry 25 and 29 assessments. Puech 2015 p. 14 n. 49 was read in the shared text extract to check two quotes. No web source was opened, so no link failed. No image of column XII was opened.
