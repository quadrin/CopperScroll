# Recovery benchmark: reserved batch

This folder holds the independently reserved test batch for the recovery benchmark.
Each case follows the fixed schema in the shared brief (RECOVERY_SCHEMA.md).
The answers and the source citations are sealed outside the repository.

## Record

- Date: 2026-10-08.
- Prepared by: recovery-reserved (worker in the 8 October 2026 methods round).
- Number of cases: 11.
- Key file: `scratchpad/agents/sealed/recovery_reserved_key.json` (outside the repository).
- Key file SHA-256: `df1b27659fc8a32a31843513cd0932dbcaeef7ced866620bc3b63d87f2f3fc76`.
- Each case file holds `key_sha256`, the SHA-256 of the canonical JSON of its key entry:
  `json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":"))`, UTF-8.
- The script that wrote these files and the key is sealed with the key (`scratchpad/agents/sealed/recovery_reserved_build.py`).
- `scratchpad/agents/sealed/verify_reserved_key.py` checks the seal. It prints hashes only.

## Rule

The reserved batch is run once, after the harness is frozen.
The result is reported whatever it is.
Nobody tunes the harness on these cases, and nobody opens the key before that single run.
A second run, or a change made after seeing a result, is a new exploratory result and must be labelled so.

## Cases

| Case | SHA-256 of the case file |
|---|---|
| `res-001` | `3800019922218f0584637ccadd0a0190a5c50205e6e97d57fbb3db69b2913542` |
| `res-002` | `9940fe9ac4fb434519f5e6906680ab23e4d80afb2237d056a6609f7bf1c6340f` |
| `res-003` | `b8dd2576a108e07b448567b5faa34ff6a10fe864b97e72465072afee686d8db9` |
| `res-004` | `2e5a08a011a5cbaa71f11841188f241b24b32a3f41ddd7fcb6fac329544839e6` |
| `res-005` | `36fc7957013df18f3aeadbf14059de9ddd48f2be4ce903dc379020216bd5a067` |
| `res-006` | `c0d18eb77ed67bf5ed8d01b0abf36ef498385e82047cfbd9a48964e75154198e` |
| `res-007` | `83686653a6dd99f6cff9ad0aac77d8226157cf970c994034bc877a5db1455dad` |
| `res-008` | `a38459e1f84e8078aee4cb050dc0de83c2172cc0a92abbf501f04bf53b656f8b` |
| `res-009` | `f712482e11d5579341f611eb75ba85770330262e40e749fb30b50aa3b29db5cc` |
| `res-010` | `90685fc5f491fe5cd6a6a9d0880c1d3ad03e3e99c08e9fb8a8cc2bbc90199e3a` |
| `res-011` | `296c2bdafbea21a73313f90d9da23f1c53d35ecfe401ba92ec43798cd0a190e5` |

## How the cases were made

- Each case starts from one real feature in a published excavation or survey report.
- The candidates come from the same report. They are plausible alternatives, not invented ones.
- No case uses a place in tables/phase3_places.csv or the excluded regions (Jerusalem, Jericho, Qumran, the Dead Sea cliffs, the Samaria and Manasseh hills).
- Instructions name landmarks and relations in the style of a Copper Scroll entry. Distances are in cubits; the cubit length is not fixed.
- Candidate records keep what the report records. Unknown values stay null. Measurements are converted to metres.
- Date codes: D = target window or earlier, L = securely later, U = undated.
- `answer` may be a candidate, `none` (no candidate is the real feature) or `insufficient` (the redacted information cannot select one even in principle).

## Degradation labels

- `names_redacted`: place, person and site names were removed from the instruction, context and records.
- `direction_word_lost`: a compass word that the source gives was left out of the instruction.
- `distance_missing`: the records give no usable distances.
- `direction_unknown`: the records give no bearings for most candidates.
- `position_unrecorded`: the records give no position on the site.
- `date_unknown`: some or all candidates are undated.
- `reports_conflict`: the underlying reports disagree on size or place.
- `measurement_rounded_to_cubits`: a size in the instruction was rounded to whole cubits.
- `withheld_field_removed`: the property asked in the withheld question was removed from every record.
- `inventory_partial`: the candidate list is a subset of the features the report records.

## Check

Run `python3 -I -B -m unittest discover -s research/benchmarks/recovery/reserved -p 'test_*.py'` from the repository root.
The test checks the case files against the schema and this manifest. It does not read the key.
