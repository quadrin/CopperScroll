# Run 10 result: the cave entries against excavated caves

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit c420100. Entry constraints fixed before the inventory ([out/step1_entry_constraints.md](out/step1_entry_constraints.md), SHA-256 `cca5a0ea…c8c8b`, 2026-10-27T05:26:25Z). Exploratory.

## Verdict
**Not supported.** Real entry–cave pairs give leads no more often than landmark-swapped controls.

| Measure | Real | 10 swaps | p |
|---|---|---|---|
| Strict coding, literal lead rule (6 entries, 1,283 pairs) | 38 | 28–110 (median ~47) | 0.82 |
| Strict lead rule (≥2 entry-specific passes) | 8 | 7–35 | 0.55 |
| Lenient coding, primary lead rule | 141 | 28–110 | 0.091 (an artefact: 100 leads are entry 7 caves in Jerusalem ASI records listing "building" and "cave" together) |
| Landmark clause required to pass (exploratory) | 15 | 1–83 | 0.91 |

**Why:** the lead rule rewards clauses that do not depend on the landmark (e.g. entry 25's "two entrances" plus "northern entrance"), so entry 25 keeps its strict leads under every swap.

## Per entry (strict)
- **7** (416 caves): 0 leads; "building at the cave" and "third ledge" unknown everywhere.
- **22** (146): 3 leads — **7Q, 8Q, 10Q** (within 500 m, pottery and written material). "East of the reservoir" is unknown only because their placement is approximate; INFERENCE: standard maps put 7Q–9Q south and 10Q west of the site, which would make it a fail.
- **25** (410): 27 leads, 7 strict: **XII/53** passes everything at cave level (pillar W2, two openings, east, northern opening, jar and scroll wrappings — Gutfeld 2017 — and period); Twin Cave; IV/17, III/11, IV/1, IV/21, VIII/29. All already known to the entry-25 lane.
- **26** (146): 8 leads, 1 strict: XII/53 ("facing east", boulder blocking its southern part). Not proposed before in the repo.
- **30** (157): 0 leads; "next to the cool room" unknown (Jericho palaces point ±300 m).
- **38** (11, Milik's cave branch, added under the rule's "other editions" clause): 0 strict leads.

## Exploratory follow-ups
- A future rule should require the landmark clause to pass and merge likely duplicate cave records.
- Published plans of 7Q–10Q (de Vaux; Humbert & Chambon) would decide entry 22's "east of the reservoir" clause; a fail is likely.
- 1Q coded from DJD I could change entry 25.
- The crack east of Qumran L71 (run 1) remains the only fissure east of a reservoir in the data.

## Not accessible
DJD I pp. 8–17; DJD VI; DJD III pp. 26–31 (Internet Archive loan, sign-in); Raviv et al. 2021 (IEJ 71); Porat et al. 2019; Eshel & Porat refuge-cave volumes; ʿAtiqot 41 Part 2; Gutfeld 2020 (Drive folder empty). L-656 and IAA archive cave records not opened (protected).

## Files
[out/](out/) (constraints, inventory descriptors, pair tables, results, run logs); [scripts/](scripts/) (overrides.py holds the hand coding with sources).
