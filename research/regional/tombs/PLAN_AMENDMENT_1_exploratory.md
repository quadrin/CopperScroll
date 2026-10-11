# Amendment 1 (exploratory, after the frozen build was inspected)

Written 11 October 2026 UTC, after the frozen build (PLAN.md, commit cd394d7) had been run and its manual checks read. **Everything here is exploratory.** It does not replace the frozen result; both are reported. It changes no rule in PLAN.md.

## Why

While doing the frozen manual checks, three gaps showed up in the frozen word lists:

1. **Direction abbreviations.** The ASI records write directions as single capitals: "W-facing entrance", "facing E", "Entrance faces N". The frozen F7 rule knows only full words (west, western, …), so it finds an entrance direction in only 2 of 1,055 units. Seen in ASI 102/221, 102/320 and 102/408.
2. **Pillars in an entrance.** Some records put a pillar or column *in* or *beside* a tomb's entrance, with no porch word in the sentence: "A rock-hewn pillar stands in the center of the wide entrance" (106/42). The frozen F2x rule needs a porch word. Seen in 105/95, 106/42 and 106/54, all of which the frozen F3 check rejected as not interior.
3. **WBADB "Rom1".** WBADB writes Early Roman as "Rom1" (and later Roman as "Rom2"). The frozen labels do not include "Rom1", so no WBADB tomb row can be dated strictly in the window. This affects 270 WBADB tomb rows. All but 6 of them in Region A are flagged duplicates of ASI records. INFERENCE: "Rom1" means Early Roman; the WBADB codebook was not read to confirm this.

## Rules (exploratory)

- **A1, F7a / F7wa.** Direction words are the frozen list plus the capitals N, S, E, W, NE, NW, SE, SW (case-sensitive, standing alone or before "-facing"). A direction counts only if it is within 4 word tokens of a frozen OPENING term in the same sentence. F7wa is `yes` if any counted direction is W, NW or SW. Otherwise it is `no` if a direction was counted.
- **A1b.** In a unit flagged `multi_tomb_record`, a `no` becomes `unknown`, because other tombs in the unit may face west.
- **A1c, manual check.** Every A1 `yes` and every A1 `no` is read. Each is confirmed, rejected (set to unknown) or set to `no`, with a reason, in `data/manual_check_amendment1.csv`. Rejections cover a direction that gives a position ("the W cave"), an inner opening ("an opening in the W wall leads to the second chamber"), or a non-tomb feature (a cistern, a kiln, monks' cells).
- **A2, F2xa.** `yes` if frozen F2x is yes, or if one sentence has an entrance-place word (entrance, forecourt, antechamber, vestibule, courtyard, porch, portico, façade) and pillar or column. Each new `yes` is checked by hand.
- **A3, date set "strict+Rom1".** The strict set, plus WBADB units whose period text contains "Rom1".

The re-scored branches are 51-S, 51-O, 51-J (F2x → F2xa), 52-M (F7w → F7wa), 56-P and 56-M (F7w → F7wa), and a 52-P proxy (F7wa + F14). Branch 52-P itself stays unscored, because its landmark is a scarp, not a tomb. The other clauses are the frozen ones.

## Outputs

- `amendment1_codes.csv`: per unit, F7a, F7wa (raw and checked) and F2xa (raw and checked).
- `amendment1_scores_summary.csv`: per branch, region and date set, using the union of lineages without duplicates. The row "ALL-TOMBS" gives N alone.
- Script: `scripts/amendment1.py`.
