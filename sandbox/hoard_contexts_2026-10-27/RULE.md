# Run 15 rule: recovering the hiding places of the near-miss hoards

Fixed 27 Oct 2026 before any new source was read for this run. Exploratory. Follows run 4 (already_found_2026-10-27), whose rule and conditions C1–C4 are reused unchanged.

## Hypothesis
Run 4 found that 31 hoard–entry pairs failed only because the hoard's find context is unknown, and one near-lead (ʿEin Feshkha 1953) lacked its coin denominations. Original publications, museum registers or contemporary reports may give those contexts. If they do, some pairs may meet all four conditions.

## Targets (fixed now, from run 4's results)
1. St Stephen's Gate hoard (CHRE 7541).
2. Jerusalem (North) hoard (CHRE 7901).
3. Jericho 1874 hoard (CHRE 8082): ~100 shekels in a pot with a lead seal.
4. ʿEin Feshkha 1953 hoard (CHRE 7586): ≥277 silver coins "in a cave", denominations unknown.
5. Beth Likiah, Shahariyem, Bir Zeit 1940, Kh. Beit Kanun (the box-only hoards in run 4).

## Steps
For each target: find the earliest publication (CHRE bibliography, IGCH, Kadman, Meshorer, PEFQS for 1874, *Revue Biblique* / *RB* 1953–54 chronicles, de Vaux's Feshkha reports, Hendin, Ariel & Fontanille). Record the find context exactly as published (setting, placement, container, depth, landmark), the coin list (denominations, count, weight), and the source page. Then re-run run 4's code (sandbox/already_found_2026-10-27/scripts/run.py) with the recovered values, changing nothing else.

## Decision
- **Lead:** any pair now meeting C1–C4 under run 4's main reading (fine class, sure mass). Report it with its sources.
- Report every target: context recovered or not, and the pairs it now passes or fails.
- A recovered context that differs from the entry's class turns those pairs into fails; report those too.
