# Staged objectives (research/plan)

What it is: a ladder of six stages, each rated before work, and a map of all 32 live lanes to those stages, with costs and proposed stop rules.
Main result: S1 A, S2 B, S3 B, S4 C, S5 C, S6 D. 20 of 32 lanes serve S1–S3. 15 lanes are proposed to park now.
What stays unknown: whether any pending request will arrive, and what it will show. The ratings are judgements, not probabilities.

9 October 2026. Exploratory. This folder changes no registered result or counter and makes no identification claim. It plans no travel: the project owner declined trip planning on 8 October (status note outside the repository). Every stop rule is PROPOSED; the owner decides.

## Files

| File | What it holds |
|---|---|
| [STAGED_OBJECTIVES.md](STAGED_OBJECTIVES.md) | The plan: two lessons, the rating scale, the six stages with evidence, rules, and the lane tables |
| [stages.json](stages.json) | The same plan, machine-readable, plus the six closed tests with their reopen criteria |
| [rating_scale.json](rating_scale.json) | The four ratings, frozen before any stage was rated |
| [test_stages.py](test_stages.py) | 17 unittest tests |

## Freeze record

- The rating scale was written first. `rating_scale.json` SHA-256 `40ed58bef248e1bd71733e4785678854ede8c3795499c9c18b9e988f3d03014c`, recorded 2026-10-09T18:07:38Z. No stage had been rated then.
- The ratings are judgements with cited evidence. No statistical test was run, so no result was computed after the freeze.
- The recovery benchmark's continue threshold (no more than 2 wrong selections on the reserved run) is set here before that run. It is PROPOSED. Its key was not opened or looked for.

## Choices

- **Six stages, not five.** S1 (an observation in hand that passes its frozen gate) is the "find the friary" rung. Without it the plan has no reasonable expectation to steer by.
- **Two levels for the ground test.** S3 is a branch-level test at one candidate; AGENTS.md allows it before identification, and the ledger has precedents (two conditional exclusions at L103). S5 is the same kind of test at a discriminated landmark.
- **Phase before ground.** The brief's example put "instruction tested against measured ground" before "phase-to-instruction match". Here phase comes first, because the datum for the ground test is that phase's surface.
- **One stage per lane.** Each lane sits at the stage that its next observation would reach. The plan tool itself sits at S1, because the owner's decision on it comes before any arrival.
- **R07 and the active questions.** AQ1–AQ3 are the Koḥlit parts of R07. The R07 lane covers Achor and Sekakah only, so no question is counted twice.
- **Dates.** Stop dates are proposals: 31 Dec 2026 for replies to requests sent 5–8 October, 31 Jan 2027 for the XII 10 image, and 31 Mar 2027 for the L-656 file, which still needs its own request.

## Sources for the two lessons

- University of Leicester, "Where to dig", https://le.ac.uk/richard-iii/discovery/where-to-dig, read 9 October 2026 through a web reader. A direct download returned HTTP 403, so no SHA-256 of the page is recorded. It gives the five objectives with their ratings, about 17% of the precinct accessible and about 1% dug.
- Buckley et al. 2013, "The king in the car park", *Antiquity* 87: 519–538, doi:10.1017/S0003598X00049103, p. 521 (grave "improbable if not impossible") and p. 523 (trench plan). Open-access PDF SHA-256 `3d8c7e844c02c057d79da220d489f451aeede0a7cbb5d68bead2d10fc35e6cf8`.
- J. T. Wood 1877, *Discoveries at Ephesus*, Introduction pp. vii–viii and chapter VI summary p. 111. archive.org item `discoveriesateph00wood`; OCR text SHA-256 `4b29539ae858dba930453e36b103d9cd27e491fd76487ba0ed6919c3aab29f87`. The `download/` route returned HTTP 500 once; the `stream/` route worked.
- No source text or image is stored in the repository.

## Run and test

From the repository root:

```sh
python3 -I -m unittest discover -s research/plan -t research/plan
```

The tests check that:
- every R-number in OPEN_QUESTIONS.md and every active question in ACTIVE_TEST.md is a lane exactly once;
- all nine methods-round tools, the seven tools of this round and the Koḥlit rarity count are lanes;
- every rating is on the frozen scale, the scale's hash matches, and ratings never rise along the ladder;
- every stop rule and every new rule is marked PROPOSED, and money is "none" or needs the owner's approval;
- the six closed tests keep their reopen criteria and carry no stop rule;
- every cited file exists, the counter snapshot matches the outcome ledger, and the S4 and S6 flags follow the ledger;
- STAGED_OBJECTIVES.md has one table row per lane, with its stage and PROPOSED.

If ACTIVE_TEST gains a question, OPEN_QUESTIONS gains an R-number, or a ledger counter changes, a test fails on purpose. Then update stages.json and the page.
