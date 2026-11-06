# Side-quest swarm, round 2 (6 November 2026, afternoon Los Angeles)

The owner removed `AGENTS.md` from the repository on 6 Nov 2026 (PR #93, merged as bb612c3) because its procedures were slowing work down. He asked for all side-quest work to be done again without them. This file changes the brief for round 2. Where it conflicts with `brief_common.md` or `ACCESS_NOTES.md`, this file wins.

## What changes

1. **No AGENTS.md procedures.** No frozen protocols, no "held area" or "exposure" rules, no blind readers, no requirement for unseen predictions, and no AGENTS outcome labels. You may look at any data in the corpus, including the H1/H2 held areas of the 25 Oct rule.
2. **Bigger budget.** Up to about 150 tool calls. Go deep, not wide.
3. **Build on round 1; do not repeat it.** Read `/home/claude/swarm/SUMMARY.md` first, then every round-1 file of your lane family (listed in your prompt) and the reviews that judged them (`/home/claude/swarm/review/R*.md`; `review/all_verdicts.csv`). Then:
   - (a) finish what round 1 left open in your lane: kill tests that were not run, "needs new data" items that the corpus can in fact answer, dead ends that were dropped for budget, blocked inputs that have another route now;
   - (b) take the strongest surviving round-1 card of your lane further where the data allow (more cases, a second witness, the consequence);
   - (c) hunt new finds in parts of your inputs that round 1 did not reach.
   A card that only restates a round-1 card is not a find.
4. **Scroll consequences are allowed.** If a find bears on a Copper Scroll entry, you may argue what it means for the identification (which candidate it helps or hurts, by how much, and why). Label that part "ARGUMENT" and keep it separate from the evidence.

## What stays the same

- AI only: no emails, forms, purchases, archive requests or contact with people.
- Do not change the repository. The orchestrator commits your files.
- Image and copyright terms: USC/WSRP, Allegro DQCAAS and IAA images may be read, not published. No images or image products in public output. Quote at most short passages.
- **Site protection:** coordinates of unrecorded or unprotected features go in private files only.
- Never print, write or commit the bucket key (`~/.hexcog.env`, `~/.boto`), and do not put the owner's e-mail in any request.
- Blocked inputs: record the exact path and error, then continue.

## Where you write

- Public: `/home/claude/swarm/out2/<LANE>/FINDS.md` plus small CSV/JSON/MD data files (each under 2 MB).
- Private: `/home/claude/swarm/private2/<LANE>/`.
- `FINDS.md` format: the brief's §6 FIND CARD format, up to 4 cards. Add the line "Round-1 link:" to each card (the round-1 card it extends, or "new"). Then "Dead ends", then "Blocked inputs".

## Final message (under 600 words)

The path of your FINDS.md; for each card its title, tag, confidence, round-1 link and a one-line evidence pointer; dead ends; blocked inputs.
