# Entry 25 aspect rule and IV/17 target declarations

**What it is:** two rules frozen before the L-656 field file or the IAA cave records arrive: how to score an Entry 25 mouth facing, and the model choices the eight IV/17 coverage branches need.
**Main result:** both rules are frozen and hashed (below). A mouth-facing FAIL at IV/17 would remove Entry 25 classes c02, c03 and c05; a PASS removes none. No real record was scored.
**What stays unknown:** what the L-656 file or the IAA records will show, and whether they will come. The sectors, tolerances and zone sizes are declared assumptions, not estimates.

9 October 2026 UTC. Worker: rule-freezer. Exploratory. No identification claim. No registered result changes. No closed or parked test is reopened.

## Freeze record

The two rule files were written first. Only a JSON syntax parse ran before hashing. No checker existed when the hashes were taken.

| File | SHA-256 | Bytes |
|---|---|---|
| `RULES.md` | `794a4e5ec0a93cb18acb7a6177339e5e6e7c1ac7ec093eb8b3fc3e2bbf3ec95f` | 24942 |
| `rules.json` | `24a1377d00f4448ebadb75fd3882e768a36dacf803a1e23c24ca8715f40d2445` | 35456 |

- Hashed at 2026-10-09T21:27:06Z.
- Repository base: main 6fee376, branch fixes-2026-10-09.
- `arrival.py check` printed `manifest: ok (29 files)` at 2026-10-09T21:22:00Z, before the rules were written, and again after the tests.
- Registration commit: _to be filled by the integrator with the commit that first adds these two files, and its push time._ A verdict counts as a test only if that push came before the record arrived.
- The checker and tests were written after the freeze. They found no inconsistency, so the frozen files were never edited.

## Files

| File | What it holds |
|---|---|
| [RULES.md](RULES.md) | The frozen rules in plain text: exposure, Part A (aspect rule), Part B (IV/17 declarations), Part C (neighbouring documents) |
| [rules.json](rules.json) | The same rules, machine-readable, with the SHA-256 of every neighbouring document at freeze time |
| `check_rules.py` | Schema and consistency checks, a dry run on synthetic intervals, and `instantiate` for later use |
| `test_check_rules.py` | 35 unit tests, synthetic geometry only |

## The rules in brief

**Aspect rule (Part A).**
- A mouth's facing is the outward normal of its rock-cut aperture chord, in true north. Masonry is excluded.
- The interval adds four terms: chord endpoint uncertainty (r = 0.10 m), north-arrow picking, drawing distortion (1°) and a north allowance (6° when the north convention is unstated).
- "East" (מזרח) is 45°–135°, the four-wind bin. Sensitivity sectors: 67.5°–112.5°, the solstice sunrise arc 62°–118°, and 22.5°–157.5°.
- PASS only if the whole interval lies inside the sector. FAIL only if it shares no arc with it. Otherwise inconclusive.
- Individual mouths: FAIL if any mouth fails, PASS if both pass. Cave level: the hull of the facade normal and the mean mouth facing.
- "The northern opening" is decided by relative position, not by facing.
- The same rule applies to IV/17, IV/11 and Twin Cave.

**Class effects (decisions module classes).**
- IV/17 mouths FAIL removes c02, c03 and c05 (the registered `not-both-east` row).
- If the record shows the aperture was recut after the ancient phase, a FAIL removes c03 only.
- An IV/17 cave-level FAIL would remove c04 and c06 and 24 members of c01. No decisions row exists for it yet.
- PASS, inconclusive, not measurable and silent remove nothing.

**IV/17 declarations (Part B).**
- Origin: midpoint of the northern mouth's threshold chord.
- Vertical zone: the chord plus 0.50 m each side, widened by r.
- Horizontal sector: inward normal ±(45° + chord term).
- Radial bands: 1.10–1.90 m (range), or three cubits ±0.30 m.
- Horizontal depth band: 0–1.80 m.
- Each value names its `volume_join.py` field. Each lists its sensitivity alternatives.

## Exposure

The rule-writer had seen the Plan 5 proxies (123° and 119°, ranges 99.5–140.8° and 104.0–132.4°) and the mouth offsets. The northern range already crosses the 135° sector edge. No verdict was computed on any real record. Plan 5, Sion's text, Bar-Adon and Feig can never test these rules. The L-656 file and the IAA records were not opened, requested or searched for.

## Run and test

From the repository root:

```sh
python3 -I -B research/preregistration/entry25_iv17_rules/check_rules.py           # prints "rules: ok"
python3 -I -B research/preregistration/entry25_iv17_rules/check_rules.py dry-run   # synthetic intervals
python3 -I -B -m unittest discover -s research/preregistration/entry25_iv17_rules -t research/preregistration/entry25_iv17_rules
```

- The check also cross-checks the coverage and decisions modules, read-only. `--no-modules` skips that.
- It reports whether any neighbouring document has changed since the freeze. On 9 October all 22 were unchanged.
- `check_rules.py instantiate GEOMETRY.json` turns plan geometry into `volume_join` field values. It has run only on synthetic geometry.
- `-B` keeps Python from writing `__pycache__`.

## Dry-run result (synthetic only)

- 125°±10° passes the primary sector. 130°±10° is inconclusive. 145°±10° fails (it touches 135° only).
- A full-circle interval is inconclusive.
- For IV/17 mouths, a FAIL removes c02, c03 and c05.

## Limits

- Every sector, tolerance and zone size is a declared assumption. Each has a reason and sensitivity alternatives.
- A PASS is compatibility, not identification. Coverage outcomes remove no class. The join never infers that a deposit is absent.
- Puech 2006 and Lefkovits 2000 were not needed and were not read. No web source was opened. No message was sent. Drive was not used.

## Proposed changes to shared files (for the integrator)

1. `research/ACTIVE_TEST.md`, pending requests, after the arrival-register line: "Before reading the L-656 file or the IAA cave records, apply the [frozen Entry 25 aspect rule and IV/17 target declarations](preregistration/entry25_iv17_rules/RULES.md) (9 October)."
2. `research/feature_workbench/decisions/plans.json`, task `decisions-iv17-l656`, `freeze`: set `spec_path` to `research/preregistration/entry25_iv17_rules/rules.json` and `commit` to the registration commit. Keep the detail that phase branches are not frozen.
3. Optional, `discrimination.json`: add the proposed cave-level aspect row for IV/17 and aspect rows for IV/11 and Twin Cave, with the effects in `rules.json`, then recompute the classes.
4. Optional, a new addendum beside the arrival register (not an edit of its frozen files). Written after the freeze; bookkeeping only. It maps IAA item `pred1` ids to these verdicts: `e25aspect:iv17:mouths:pass` → `pred1:confirm`; `…:fail` → `pred1:contradict`; `…:inconclusive` or `…:not-measurable` → `pred1:inconclusive`; `…:silent` → `pred1:silent`.
5. Fill the registration commit line above.
