# Run 10 rule: the cave entries match caves already excavated

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
Five entries hide things in caves or fissures (scroll_contexts.csv setting_P = cave: entries 7, 22, 25, 26, 30; check the other editions' codings and add any entry they code as cave). The Judean Desert caves near Qumran, Jericho and the Kidron were intensively excavated (1949–56, the 1993 "Operation Scroll", the 2002 cave survey, the 2017–21 IAA survey). Some scroll caves may already be in those reports: a cave whose position, entrance, and Second Temple-period finds (especially empty jars, pits, sealed niches, signs of removal) match an entry.

## Steps
1. **Entry constraints (fixed now from the text):** for each cave entry, list what the text says: landmark, direction, depth, item type and quantity, cave features (column, two entrances, "the fissure", etc.), with every edition's variants (text/readings.json). Write this to a file with its SHA-256 before step 2.
2. **Cave inventory:** every catalogued cave within 5 km of each entry's candidate places (ratings.csv, places.csv), plus the whole Qumran–Feshkha cliff band, from: DJD III cave list; Patrich (1994) and ʿAtiqot 41 (2002 survey; repo coding research/regional/caves_entry25); Bar-Adon; Eshel & Porat; IAA 2017–21 reports (ʿAtiqot, HA-ESI, press). Record for each: position, entrance(s), size, period of finds, and whether finds suggest a deposit (jars, coins, metal, empty pits, cut niches).
3. **Score** each entry–cave pair on each constraint (pass / unknown / fail, as in run 1), plus J7 (Second Temple finds in the cave).
4. **Control:** score the same caves against the five entries with their landmarks **swapped** at random (10 random swaps), to see how often a cave "fits" an arbitrary entry.

## Decision
- **Lead:** an entry–cave pair with no fail, at least two passes beyond the period test, and passes on a feature specific to the entry (not "is a cave").
- **Supported** (exploratory) if real pairs yield leads clearly more often than the swapped controls (report the counts and a permutation p).
- Note prior proposals for each lead (e.g. Cave of Letters for entry 25, already in the project).
