# Amendment 2 (exploratory): the Akeldama tombs, and the coding of IAA Reports 7

Written 11 October 2026 UTC, after the frozen build (PLAN.md, commit cd394d7) and Amendment 1, and **before** any tomb description in either report was read. **Everything in Part B is exploratory.** It changes no rule in PLAN.md, and the frozen Region A headline stays as it is. Part A records the implementation choices for source HK, which the frozen plan lists but does not say how to code.

## What had been seen when this was written

- Both PDFs were hashed on the owner's computer and match the hashes the integrator gave: IAA Reports 7 `7c6e6208…a2efb7` (209 PDF pages), IAA Reports 1 `f23c881e…e1d5` (140 PDF pages).
- Both are page scans with no text layer, apart from the portal's cover page. They were run through OCR (tesseract 4.1.1, 300 dpi, English) on the owner's computer. The OCR text stays there and in the scratch folder, never in the repo.
- Read so far in IAA Reports 7: the title and imprint pages, the contents page, the foreword and the first page of ch. I (PDF pp. 2–8), and one figure caption ("Tombs on Hill D, plans", PDF p. 20). Printed page = PDF page − 7. No tomb description, inscription, nefesh or chronology text has been read.
- Read so far in IAA Reports 1: the portal cover page only.
- **Background knowledge before reading** (not from a source in this session; listed because it could steer choices):
  - Jericho: the cemetery lies on the hills west of the town. Tomb H is the "Goliath" family tomb, with Greek and Aramaic/Hebrew inscriptions, a wall painting and a forecourt. One ossuary there names Theodotos, a freedman of a queen (Agrippina). The loculi tombs held wooden coffins in an earlier phase and ossuaries later.
  - Akeldama: three burial caves in the lower Ben Hinnom valley, with carved entrances, ossuaries with inscriptions (one names an Ariston of Apamea), and later reuse.
- PLAN §1 already lists the Jericho cemetery as exposed. Akeldama lies in Region A near the Ben Hinnom tombs 102/481–484, which the ASI lane had coded.

## Part A. How source HK is coded (implementation of the frozen plan)

The frozen plan names HK as a source for B1 (PLAN §3). It is silent on the unit, the text that is coded and the position. These choices follow the Kenyon precedent (`data/kenyon_ii_units.csv`):

1. **Unit.** Each tomb that ch. II ("Description of the Tombs") describes under its own number is one unit, whether excavated or only surveyed, and whatever its date. A courtyard or mourning enclosure belongs to its tomb. A nefesh (ch. VI) is attached to the tomb that the report assigns it to; a nefesh with no tomb is its own unit.
2. **Coded text.** One row per unit in `data/hk_units.csv`, with a short English transcription of what the report states about that tomb. There is one plain sentence per feature, in the report's own feature words: the tomb type, chambers, loculi or kokhim, arcosolia, benches, pits, courtyard or forecourt, steps, entrance and its direction, columns or pillars, nefesh, coffins, ossuaries, inscriptions, painting, closing stones, setting (hill, wadi). The frozen word lists and the frozen `Coder` then code that text unchanged. No description text is copied. Names in inscriptions are given as the report reads them, in a sentence that says "inscription" and "name".
3. **Dating sentence.** Each row ends with one sentence that starts "The report dates the tomb" and gives the report's own period words for that tomb: from ch. II, or if ch. II gives none, from ch. VII (Chronology). The frozen strict and lenient rules then apply. A tomb the report leaves undated gets no dating sentence and stays unknown.
4. **Position.** The report's own grid reference for the tomb, if it gives one. Otherwise the reference of its hill or area. Otherwise the cemetery point of WBADB S2446 (the row for this cemetery). Old Israel Grid values are converted with pyproj from EPSG:28193, as for WBADB. The uncertainty is the cemetery's extent as the report states it, or 1.2 km (the Kenyon value) if it states none. A position read off a figure by eye is not used for scoring.
5. **Locators.** Each row records the printed page(s) and figure(s) of the tomb's description and plan, the inscription numbers (ch. IV) and the nefesh pages (ch. VI). Figures are cited, not copied (IAA copyright).
6. **Duplicates, manual check, exposure.** The frozen rules apply unchanged. HK is not a primary lineage, so an HK unit within 0.15 km of a primary unit is flagged `possible_duplicate_of`. Each lineage is also counted on its own (PLAN §3), so the HK tombs are reported by themselves too. Every `yes` for F1, F2, F2x, F3, F5, F6, F7w or a name is checked by hand in `data/manual_check.csv`. All HK units are exposed under PLAN §1 (the Jericho cemetery); their records were first read after the freeze.
7. **Unit ids.** The 1,055 earlier units keep their ids (T0001–T1055). New units are numbered after them, so no earlier id moves.
8. **Links to earlier rows.** If the report says that a tomb is one that Kenyon (or another earlier excavator) recorded, the HK row names that record in `linked_to`. This does not change the duplicate flag.

## Part B. The Akeldama tombs (exploratory)

IAA Reports 1 (Avni and Greenhut 1996) is not in the frozen source list. Reading it is an exploratory addition.

1. **Units.** Each burial cave the report numbers is one unit, coded with the Part A template (transcription, the same `Coder`, the same dating sentence rule, the same manual check).
2. **Position.** The report's grid reference for each cave or for the site; else the site reference it gives; else the nearest ASI record that the report or the ASI text identifies as the same tombs. The ASI uncertainty (0.05 km) applies to a report grid reference given to 10 m; a coarser reference takes its stated precision.
3. **Scoring.** The Region A branches (and A∪B) are scored with the frozen clause rules, by the same `clause_value` function. The duplicate rule is applied against the ASI units (0.15 km).
4. **Outputs.** `amendment2_akeldama_units.csv` (the coded caves) and `amendment2_scores_summary.csv` (Region A counts with and without the caves, all three date sets, plus the caves alone). Script: `scripts/amendment2.py`. These files never feed `tombs.csv`, `scores.csv` or `scores_summary.csv`.
5. **Reporting.** The README says whether any Region A count changes when the caves are added, and keeps the frozen Region A headline unchanged.
