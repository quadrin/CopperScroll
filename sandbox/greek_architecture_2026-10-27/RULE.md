# Run 9 rule: Greek architectural loanwords point to Herodian-style buildings

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
A few entries use Greek architectural loanwords: peristyle (פרסטלין, entry 3, I 6–7), exedra (אכסדרה, entry 51), and any others the project lexicon lists as Greek or Latin loans. A writer using these words was describing real Greek-style buildings. In the scroll's region such buildings are few: Herodian and Hasmonean palaces, the Temple porticoes, a few rich houses. If each loanword entry must sit at a building that has that feature **and** the entry's other relations, the candidate list becomes short and testable.

## Steps
1. **Loanwords (fixed by the lexicon).** List every entry with a Greek or Latin architectural loanword, from tables/landmark_lexicon_index.csv, text/readings.json and the editions' notes. Record the word, the entry, the other relations in the entry (orientation, depth, "in its floor", "southern corner", etc.). Write the list to a file and give its SHA-256 before step 2.
2. **Buildings.** For each loanword, list every excavated or surveyed building in the region (31.40–32.55 N, 35.00–35.60 E) with that feature, dated 100 BCE–135 CE: e.g. peristyle courts at the Jericho palaces, Herodium, Masada, Machaerus (outside the region; list but mark), Hyrcania, Kypros, Jerusalem's Upper City mansions, the Temple Mount; exedrae likewise. Sources: excavation reports and the repo's research files.
3. **Fit.** For each entry–building pair, score each of the entry's other relations pass / unknown / fail (as in run 1). Example for entry 3: a **great cistern** in the court of the peristyle, **in its floor**.
4. **Control.** The same buildings scored against two entries **without** loanwords that also name a cistern in a court (choose them from the text before scoring and list them in the step 1 file). If those control entries fit the same buildings as often, the loanword adds nothing.

## Decision
- Report every pair. A **lead** = an entry–building pair with all relations pass.
- The hypothesis is **useful** if at least one loanword entry has ≤ 3 buildings with no fail and the control entries do not have fewer.
- Note who first proposed each building for each entry (Milik, Puech, Lefkovits, others), so a lead's novelty is clear.
