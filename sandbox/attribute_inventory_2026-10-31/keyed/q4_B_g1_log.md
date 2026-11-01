# Group Q4, reader B (g1): keying log

- Started: 2026-10-31 19:16 PT. Finished: 2026-10-31 19:37 PT.
- Read first: `SCHEMA.md`, `READER_INSTRUCTIONS.md`, `QUMRAN_NOTES.md`. No other repo file, keyed file, Projects doc, Drive item or web page opened. The rendering script was only run, not read.
- Outputs: `keyed/esh02_B_g1.csv` (204 rows), `keyed/qum4a_B_g1.csv` (35 rows). Builder script and page renders are in the session scratchpad (`q_B_q4/`), outside the repo.

## esh02: Eshel, Broshi, Freund & Schultz 2002, *DSD* 9.2, pp. 135-165 (text only)

Read: the whole JSTOR text extraction, pp. 135-165 (sections I-IV, footnotes, Appendices A-C).

Could not read:
- **Table IV** (Appendix A, pp. 156-160: per-tomb characteristics of the excavated tombs, such as depths of shaft and loculus, orientation, loculus wall, stone or brick covering and headstone). It is printed rotated, and the OCR is reversed, upside-down text that cannot be aligned to tomb numbers. Only column headings can be made out. **No per-tomb sizes or depths for de Vaux's tombs could be keyed.** A page image of pp. 156-160 is needed.
- Table V (pp. 161-163, gender and age) is partly legible. It has no physical attributes, so it was not keyed (used only for the TA/TB labels).
- Maps 1-3 (Rosenberg & Myers; Reeder GPR map) and Plates I-VII exist only as OCR noise. No positions were taken from them, so position_basis is `text_only` throughout. Plate III (the plan of the mourning enclosure, with a 0-2 m scale) is also illegible.

Decisions:
- Ids. Tombs dug by de Vaux use **de Vaux's number**, as in the labels of Tables IV/V (`esh02:T26` is de Vaux 26). Reeder's map number goes in the notes, from Table I. All other tombs use the **Reeder map number** (`esh02:T978`). The two ranges do not collide: map nos. 23 and 37 belong to de Vaux tombs 12 and 6 and are not keyed separately. Map 661 is keyed as T4; maps 793, 812, 814, 794 and 808 as T32-T36; map 749 sits under T7 because the correlation is uncertain. Other ids: `PointB` (de Vaux's "Point B", the square building or "mourning enclosure"), `TA`, `TB`, `G2` (Steckoll).
- Rows: the cemetery, its 5 sections, the Northern and Southern Cemeteries, the building with its walls, entrance and burial 1000, and de Vaux T1-T37 (all of them, as the brief asks; 13 of them have only the Table I correlation, are marked `low`, and are noted as such). Also TA, TB, G2, tombs 977, 978 and 1001, the 48 E-W tombs listed by number in nn. 13-16, and 100 GPR-listed tombs (nn. 24-27, 29). The listed tombs carry only section membership and orientation or detection notes. Each row's notes say "listed in n. X", so they can be filtered out.
- Orientation goes in notes as "long axis N-S/E-W", per QUMRAN_NOTES. `opening_dirs` is used only for the building's entrance in its north wall (N).
- The building's size is printed as "4.50 x 5.05 m" and is kept in printed order (length 4.50 = west wall, width 5.05 = SW-SE). The depth of T978 (1.20 m) is the depth of the coffin bottom below the surface.
- "c. 12 m east" (the building from burial 1001) is keyed as a distance only. The bearing is left blank because it is printed as a word, not a number.
- in_window: `yes` for the N-S tombs with finds the source dates to the second temple period, and for the building. `no` for the E-W (Bedouin) tombs and the Southern Cemetery. `unknown` otherwise.

## qum4a: Humbert & Fidanzio (eds) 2019, IVA, PDF pp. 26-111 = printed pp. 1-86

Read: the full text extraction of PDF pp. 26-111 (introduction; ch. 1 archival sources: diary, field notes, preliminary report, other published texts, Patrich report, photo captions; ch. 2 Humbert; App. A Massonnat; App. B 2017 notes). Printed page = PDF page − 25.

Rendered and inspected (150/300 dpi): PDF 49 (Patrich plan and section, Fig. 12, p. 24), 75 (Humbert Fig. 6, plan and sections, p. 50), 97 (2017 plan, Fig. 1, p. 72), 101 (2017 section, Fig. 6, p. 76), 110 (Fig. 21 sketch, no scale).

Not inspected as images: the photo figures (ch. 1 Figs 13-49; ch. 2 Figs 2-5, 7-21; App. A-B photographs), the location maps (intro Fig. 1, ch. 2 Fig. 1), the DTMs (2017 Figs 7-8) and the inventory and diary facsimiles. Text and captions only.

Plan rules applied:
- **Humbert Fig. 6** has a scale bar of 0-18 m (77.7 px/m at 300 dpi) and a half-arrow north sign whose "N" sits at the tail and whose point faces page-right. I took north as page-right because that is the only reading consistent with the text: the entrance (a) is at lower left and "s'ouvre au sud-est" (pp. 46, 48). The reading is also consistent with the 2017 plan. Patrich's plan uses the same arrow style and was not measured.
- **2017 Fig. 1** has a scale bar of 0-3 m and a 1 m grid (71.7 px/m). Its north arrow points c. 37° clockwise from page-up. It was used for blocks A and B, the "arch" and wedge Y, and for comparison values in the notes.
- Chamber sizes for b, c and d are the extents of the light "station debout" zones, measured by flood-filling the plan image. Wall and block sizes come from the extents of their outlines. Every plan value is rounded to 0.5 m. Bounding extents overstate irregular rooms; the notes give the areas.
- Opening directions for chambers b, c, d and f come from Fig. 6. Each is the bearing from the chamber's centroid to the passage, converted to the 8-point compass, with the degrees in the notes. Several fall close to a compass boundary: b→d 290°, d→b 159°, b→a 115°. The opening of e (c. 247°) is left blank.
- Text over plan: the cave length is 19 m, from the "1900cm" dimension printed on the 2017 section. The cave height is 2 m (p. 46). The entrance is 1.60 x 1.35 m (de Vaux field notes; this is the opening after he widened it). The upper chamber is 2 x 6 m, height 1.2-3.5 m, and its passage is 2.5 m. Plan-scaled values for these appear in notes only.
- Ids follow QUMRAN_NOTES (`qum4a:11Q`, `qum4a:11Q.<part>`), using Humbert's letters a-x for the parts. The 2017 labels get distinct suffixes (`blockA/B`, `struct19A/B/C`, `arch`, `Y`, `upper`, `upper_passage`). The pillar is one row (`11Q.r`, which the 2017 plan labels X). The 2017 stone structures A-C are kept apart from Humbert's u/v/w because the source does not equate them, although they are probably the same masonry. Patrich's three crevices are separate low-confidence rows.
- Not keyed: plan labels m, s, n, t and p, which have no description in the text. Point h is described within c. Also not keyed: the hypothetical hearth, the 2017 Operation B squares and sounding (excavation units), and other caves (1Q, 3Q, A, B, Patrich 24). Their distances to 11Q are in the cave row's notes.
- Grid: "x: 243652.818; y: 629357.345; z: -282.992 (entrance point according to the Israeli Grid)", p. 1, keyed as ITM (the values are in the new-grid range).

## Problems for the third reading
1. esh02 Table IV is illegible. All size and depth data for the 37 de Vaux tombs is missing from this keying.
2. The north arrow on qum4a Fig. 6 is ambiguous on its own. All plan-derived chamber directions depend on reading north as page-right.
3. Plan-scaled chamber sizes depend on how "chamber" is bounded on Fig. 6 (standing zone versus low-vault margins). For example, c is 8.5 m including the low back h, and 4.8 m for the standing zone alone.
