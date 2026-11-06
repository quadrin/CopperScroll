# Round-2 review note (6 Nov 2026)

Use `/home/claude/swarm/REVIEW_BRIEF.md` for method, verdict scale (SURVIVES / WEAKENED / KILLED / MERGE) and format, with these changes:
- AGENTS.md was removed by the owner (PR #93). Do not judge cards by its procedures (freezing, held areas, exposure, blind reading). Judge evidence, novelty and reasoning only.
- Round-2 cards may contain an "ARGUMENT" section about a scroll entry. Review the argument as well: say whether it follows from the evidence and whether it overstates.
- Each card has a "Round-1 link". Check it does not merely restate the round-1 card (`/home/claude/swarm/out/<LANE>/FINDS.md`, `review/R*.md`). A restatement is KILLED as "not new".
- Re-open the cited evidence yourself (store PDFs via `hexview.py`, Drive, repo, web) for at least the strongest claim of every card, and run any cheap kill test the worker left unrun.
- Write `/home/claude/swarm/review2/<YOU>.md`. Append rows to `/home/claude/swarm/review2/all_verdicts.csv` with header `reviewer,lane,card,short_title,original_tag,verdict,final_tag,confidence,cost` (create the header if the file is missing; use a file lock or write your rows in one append).
- Never print secrets; images stay private (crops to `/home/claude/swarm/private2/<YOU>/`).
- Final message: one line per card (lane-card, verdict, final tag) and key reasons, under 500 words.
