# Coding plan for the scenario columns (frozen before coding)

Written 9 October 2026 UTC, before any scenario value was entered in `catalogue.csv` or `searches.csv`. The README records this file's SHA-256 and time. Later changes to this file create a new exploratory coding, not a correction of this one.

## What is coded

Each catalogue row gets three columns, one per scenario:

- `s_removed`: the deposits were real and were removed in antiquity.
- `s_unrecovered`: the deposits were real and some remain unrecovered.
- `s_literary`: the list is literary or legendary (no deposits of this kind were made).

Each value is one of `supports`, `weakens` or `neutral`. A short `scenario_reason` gives the reason in one sentence.

## Coding rules

1. Code only what the account itself reports or presupposes. Do not code the modern reader's view of the account.
2. `supports` for `s_removed`: the account reports that hidden valuables of the period and region were found or handed over soon after the loss, by force, by informers, by custodians or by survivors.
3. `supports` for `s_unrecovered`: the account reports hidden valuables that were not found, or a search that failed, or knowledge of a hiding place that died with the hider. A tradition that something is "still hidden" supports this scenario only as a belief, so code it `supports` and say "belief" in the reason.
4. `supports` for `s_literary`: the account is itself a legend of hidden sacred objects with a famous hider, supernatural agency or an end-time frame. Such accounts show that lists of hidden Temple objects were a literary form.
5. `weakens` is used only when the account reports something that the scenario says should not happen. Example: an account of systematic recovery weakens `s_unrecovered` only if it claims that all hidden valuables were found. An account that some were found does not weaken it.
6. Otherwise `neutral`.
7. One account may support more than one scenario. The scenarios are not exclusive at the level of single deposits.

## What the counts mean

The summary script counts rows per scenario and value. These counts are descriptive only. Rows are not independent (see `dependency_group`), sources differ in reliability, and a count of accounts is not a weight of evidence. No decision rule is attached to the counts, and no scenario is declared supported or rejected by them.

## Search ledger

`searches.csv` has no scenario columns. Its `result` uses: `negative` (looked, nothing relevant to the scroll found), `other_finds` (finds, but no deposit of the kind the scroll lists), `claimed_find` (a find was claimed as scroll-related and is disputed or unverified), `unknown` (the result is not documented in the accessed sources). A `negative` result counts toward coverage only with the target volume, depth reach and detection limits established (AGENTS.md); this ledger records those fields where a source gives them and leaves them blank otherwise.
