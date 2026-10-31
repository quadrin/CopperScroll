# Run 27 fork log

Changes after the rule commit, in order, each logged before it is run.

No change was made after the rule commit (8fd634f).

- 17:20 UTC (f1aff49): scripts committed before any reading was used. Fake readings were used only to smoke-test the code, and their outputs were deleted.
- About 17:48 UTC: benchmark C run once on the first readings. G1 passes, G2 fails. Under the rule there is no revision; the run stops without scoring the scroll.
- After the gate: the reported checks (LOSO, benchmark A) and one exploratory breakdown, labelled as such in RESULT.md.
