# Lane I protocol (frozen): medieval place names 1100–1600 against the Copper Scroll names

Frozen 2026-10-31 (session of 30 October 2026), before any scroll name was scored against any medieval record. Never edited after the freeze commit.

## Claim under test
C1 (primary). In place records written 1100–1600, read from the sources listed below, scroll name groups find **conjunctive matches** (name score ≥ 0.75 AND feature class allowed for that scroll name AND position inside that name's candidate area) more often than random Hebrew-like names do under the same conjunction.
C2 (secondary, survival). The same for the scroll names that have no biblical or ancient-literary form (a match for a biblical name in a Christian or Jewish source can be learned tradition).
T (tomb sub-test). The scroll's named tombs (ha-Melaḥ, Kippa, Absalom, Zadok, Bene ha-ʿAm/Obed) against the named-tomb records of the Jewish itineraries and tomb lists (Adler 1930; Carmoly 1847; Benjamin of Tudela, Adler 1907).

## Inputs (SHA-256)
| Input | Path | SHA-256 |
|---|---|---|
| Extracted records (blind; step 1) | data/medieval_records.csv | c4782809d1e85d12d6bf694aa5a3e7e94cdfe49541739c4881219086df10b7a8 |
| Placed records (step 2) | data/medieval_records_placed.csv | 145da2b3490d019a362eba41a4bbe63ef6f617b5908375e6bcd49e00f6d70013 |
| Anchor gazetteer (from repo SWP/Mandate/places/Peraea data) | data/anchors.csv | dbd1bf521c8963ee37776b49e4a96119a693046a130c8e98c25105c460819117 |
| Name constraints, controls, pass counts | data/name_constraints.json | d75b3522a0d1eb3683eea70a51d717ab7713bd8c87379257dcff3d8444ae01f2 |
| Passage selection manifest | data/selection_manifest.json | efc516f599855a56df55fc47855fda6753e47addc59ffc2535e1620c9092b054 |
| Record collector (layer rule) | scripts/collect_records.py | 3c28f8f0a52b073d23bb77f55eb5243345c9f3a00d9476129bcd13d34d592c32 |
| Placement script | scripts/place_records.py | a0194135322e45fa7effa7ee4acf6532868e63d3395d90698aabc577fd060a52 |
| Matcher (rules M1–M9, conjunction, chance) | scripts/medieval_match.py | e7f059c75c58283369b548be7ff5cc9429a070a5ee1f5828d6ec77f4ede0cc20 |
| T01 scorer | research/agent_review_2026-10-07/wave1/T01_place_names/scripts/toponym.py | dea86acb74a54f3a49fa96066a1044087d295f928b57c30a2ad89a7910399d77 |
| T01 sound rules | …/T01_place_names/data/sound_rules.csv | 629798de76b8ce91f70a0f394e6e28e5bb2a0624f881c6afc3ef30f5d8489911 |
| Scroll names | …/T01_place_names/data/scroll_names.json | bfaef21601de684ce7ae5443f600a961e72949f23029b8c3d01f7905146fcf6c |
| T01 positive controls (source of control cores) | …/T01_place_names/data/positive_controls.json | 35b126047d78e83114ac123c6821c11d0cf0497b8d974ec0f7e1a265cfd2f83b |
| SWP grid calibration | …/T01_place_names/data/grid_calibration.json | cee1d2265dc4032faa36b6c554bc790d892cd38bf2266a7c967e791b027254f1 |
| Candidate places | research/agent_review_2026-10-07/wave2/W2B_model_v1/inputs_v3/places_v3.csv | 381894a6e383d8f763197048d751bc8c89a5506144b295b3b77d338cc9ad3b9c |
| Entry → candidate map | …/inputs_v3/candidates_v3.csv | f8d70eb7fda81a8cbbc07bfaa22a8c48785dc423e73e0d989139c717cf51b2a5 |
| Mandate 1:20,000 features | research/regional/mandate_maps/features.csv | 1f63e2fc36a7a5e2a2c0db665c8d0bacc9abf420524121920ece405eb1019ccc |
| Peraea gazetteer | research/regional/peraea/gazetteer.csv | b7abb1e6e52d514c605fd3cf4ea2560b367e8a4b0f36897c0745bbbe54d537fe |
| Blind-extraction log | blind_extraction/ (instructions, runner, selector, input/output/source hashes, sources.csv) | see files |

Full OCR texts are not committed; blind_extraction/sources.csv gives archive.org identifiers, URLs and SHA-256.

## Layer rule
Primary layer = records with by_editor = false AND year of writing 1100–1600 (speaker date when the extractor gave one; else the segment date). Le Strange records count only with a speaker date. Anonymous Pilgrim I (translator: "part early, part 11th century", source lines 60–236) is excluded. 1,965 of 2,372 records are in the primary layer.

## Rule
1. Name score: T01 `toponym.score` (rules R1–R14, H1–H3, A3–A4 unchanged) between each Hebrew variant core of the scroll name (scroll_names.json) and each skeleton of the record's name_as_printed and other_names, produced by medieval rendering rules M1–M9 (docstring of scripts/medieval_match.py) and T01 `lat_tokens`. Threshold 0.75 (as T01).
2. Feature: the record's feature_type is in a class allowed for the scroll name (name_constraints.json `names.*.classes`).
3. Position: a placed record lies within (record radius + candidate-place sigma + 5 km) of at least one candidate place (candidates_v3/places_v3) of any entry that uses the name; an unplaced record's region code must be in the regions mapped from those candidates.
4. Statistic for a name group: number of distinct primary-layer records meeting 1–3 for any variant.
5. Chance: for each name group, NRAND = 200 random cores per variant with the T01 `chance.py` construction (pattern kept; strong consonants drawn 50/50 from the pooled scroll-name consonant frequency or uniformly), scored against the **same eligible record set** (same feature and position filter). Seed 20261030.
6. Pass mark: observed total of conjunctive records over the 26 test names (name_constraints.json `test_names`) exceeds the 99th percentile of the random totals. Same for C2 (non-biblical test names) and T (tomb groups). One-sided p = (1 + #random ≥ observed)/(NRAND + 1).
7. Per-name report: every group with observed > its own random p99 is listed with source and page; every conjunctive match is listed in results/conjunctive_matches.csv.
8. Known-survival names (asla, haqqos, doq, koziba, kidron, natof, horon, kerem, rahil, gerizim, bethsham, bezek, janoah, jericho) are scored and reported but are not in the C1/C2 totals.

## Positive controls (expected list stated before matching)
Known survivals or well-attested places that the medieval sources are expected to name: Jericho (ירחו), Siloam (שלוח), Bethlehem (לחם), Anathoth (ענתות), Tekoa (תקוע), Kidron (קדרון, Latin Cedron expected), Gerizim (גריזים), Beth-Hoglah (חגלה). Area = control point and sigma (name_constraints.json); feature class: any. Pass: at least 6 of 8 found (≥ 1 conjunctive record each). If fewer than 6 are found, the matcher is declared insensitive on this layer and C1/C2 close as "not identifiable from available evidence" whatever the counts.
Tomb controls (Jewish tomb lists, feature class TOMB): Zechariah (זכריה), Huldah (חלדה), Simeon the Just (שמעון). Pass: at least 2 of 3. Otherwise the tomb sub-test closes as not identifiable.

## Failure condition
C1 fails (rejected for the sources read) if the observed total does not exceed the random p99. A name-level result above its own p99 without a C1 pass is reported as exploratory only.

## Meaning of outcomes
- **Obtained**: C1 passes and the controls pass. The listed matches are medieval attestations in the right feature class and area beyond chance. For a biblical name this is evidence of a medieval tradition at that place, not of continuous local survival; only C2 speaks to survival.
- **Not obtained**: C1 fails with the controls passing. Medieval name survival is closed for the sources read (coverage table in the NOTE).
- **Partly**: C1 fails but one or more single names exceed their own p99, or C1 passes only through biblical names (C2 fails).

## Parameters
THRESH 0.75; SLACK_KM 5; NRAND 200; seed 20261030; position radii as in data/medieval_records_placed.csv (anchor sigma; + stated distance, or + 3 km when no distance).

## Exposure log (exploratory work before the freeze)
I selected passages with region keywords from which scroll-only names were removed (blind_extraction/select_passages.py). I read the source contents pages and segment boundaries. I looked at extracted records only for structure (field counts, feature-type, region and language distributions); I did not run any scroll name against them. Anchor patterns and name constraints were written from the repo candidate tables and the scroll's own text, not from the records.
