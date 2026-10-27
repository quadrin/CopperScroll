# Run 20 rule: the Temple-area entries fit the Mishnah's map of the Temple Mount

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
About ten early entries are placed, at low confidence, on the Temple Mount (places.csv jer_temple: 3, 5, 7, 8, 12, 12a, 13, 14; jer_east_gate: 9, 10; plus 6, 13, 14 with ha-Melaḥ = Millo). The Temple Mount cannot be dug, but Mishnah tractate *Middot* (with *Tamid* and *Shekalim*) describes its gates, courts, chambers, cisterns and corners. If these entries describe the Temple precinct, their relations should fit Middot's layout jointly (Linear B, text against text).

## Steps
1. **Entry relations (fixed now from the text, written to a file with SHA-256 before step 2):** for each candidate entry, every landmark word and relation (e.g. entry 3 "great cistern in the court of the peristyle"; 12a "the other corner"; 9–10 the east gate area; 7 "the old house of tribute (?), the chain"), with all edition variants from text/readings.json.
2. **Middot gazetteer:** every named feature in Middot 1–5 (gates, chambers, the Lishkat ha-Golah with its well, the Wood Chamber, the Ḥel, the Soreg, the courts, the eastern gate, the "Bet ha-Moqed", corners and directions), with its stated position, from an open Hebrew text (Sefaria or similar) and a standard translation. Add Tamid and Shekalim features only if they give a position.
3. **Score** each entry against each Middot feature: pass (the feature type and every positional relation agree), unknown, fail.
4. **Joint fit:** an assignment of entries to distinct Middot features in which every entry passes and the entries' relative directions are consistent with Middot's layout.
5. **Control:** the same procedure with 10 entries from the scroll's Jericho/desert block (entries 20–30) in place of the Temple entries.

## Decision
- **Supported** (exploratory): a joint fit exists for at least 5 Temple-area entries with no fail, and the control entries achieve clearly fewer passes (report counts).
- Report every entry–feature score and every unresolved word.
