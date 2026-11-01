# Q4 reader A (g1) log: esh02, qum4a

- Reader: A, group Q4. Started 31 Oct 2026 19:16 PT; finished 19:33 PT.
- Read first: `SCHEMA.md`, `READER_INSTRUCTIONS.md`, `QUMRAN_NOTES.md`. I opened no other repo file, no project docs and no other keyed file. The CSVs were written with the Python `csv` module in SCHEMA header order. The generator script is in the scratchpad (`q_A_q4/key_q4.py`), and it is not part of the repo.
- Output: `esh02_A_g1.csv` (207 rows) and `qum4a_A_g1.csv` (41 rows).

## esh02: Eshel, Broshi, Freund & Schultz 2002, *DSD* 9.2: 135–165 (JSTOR text extraction only)

- Read: the whole text, printed pp. 135–165, including footnotes, Table I (p. 141), Table II (p. 143), Table III, and Appendices B and C.
- **Could not read**
  - Maps 1–3 (pp. 138–139) are garbled OCR. I keyed no positions from them, so `position_basis` is `text_only` throughout.
  - Plate III (plan of the building, with a 0–2 m scale bar) is not visible.
  - Appendix A, Table IV (pp. 156–160, per-tomb characteristics such as depth of tomb, depth of shaft, loculus, stone covering and headstone) and Table V (pp. 161–163) are rotated tables that came out as illegible OCR. **No per-tomb depth or construction could be keyed from them.** A page-image or PDF reading of pp. 156–163 is needed.
- **Rows**
  - 1 cemetery and 5 sections from Table II, with counts in `notes`.
  - The Northern and Southern Cemeteries, plus the "division path".
  - The building at the eastern end of the Middle Finger (de Vaux "Point B"), its W wall, N wall and entrance, and the wadi north of it.
  - Burial 1000 and tombs 977, 978 and 1001.
  - 37 de Vaux tombs from Table I. Each is keyed as `T<Reeder no.>`, or `dVT8` where there is no number; de Vaux's number is in `notes`. De Vaux's TA and TB, Steckoll's G2 (= T232), and Clermont-Ganneau's 1873 grave.
  - 48 further E-W tombs from the lists in nn. 13–16. Six of the 54 E-W tombs are de Vaux rows.
  - GPR-listed tombs: 34 in the NW corner (749 is the de Vaux T7 row), 6 in the South Finger, 22 on the North Hill, and 39 possible tombs near the ruins (all `low`).
- **Conventions**
  - List-only rows begin their notes with "List-only row".
  - Orientation is in `notes` as "long axis N-S/E-W".
  - The building's `opening_dirs` = N comes from "in the north wall".
  - Building to burial 1001 is 12 m (printed). I left the bearing blank because it is printed only as "east".
  - Section membership is keyed only where the text states it. The fit of de Vaux 32–37 to the South Finger, 11 to the Middle Finger and so on is not used, except where a tomb appears in a sectional list.
- **Skipped** (modern or not a feature): the visitors' center and paved road, Steckoll's G1 (it turned out not to be a tomb), the coffins (objects), and the pottery.

## qum4a: Humbert & Fidanzio 2019, IVA, PDF pp. 26–111 = printed pp. 1–86

- Read: the whole text extraction, PDF pp. 26–111.
- Page renders (150–500 dpi) viewed:
  - PDF p. 49 (Patrich plan, Fig. 12, p. 24).
  - PDF p. 75 (Humbert Fig. 6, p. 50: plan with letters a–x, 0–18 m scale bar, N arrow pointing to page right, sections C–B–A and D–E).
  - PDF p. 97 (App. B Fig. 1, p. 72: 3D-scan plan, 1 m grid, 0–3 m scale bar, N arrow about 36° clockwise from page top, blocks A and B, "arch", X, Y, upper chamber).
  - PDF p. 101 (App. B Fig. 6, section with a printed "1900cm"/"500cm"; Figs 7–8 DTM).
  - PDF p. 110 (Fig. 21, sketch of the upper chamber, no scale).
- Photo-only figures (Figs 2–5, 7–21 of ch. 1–2, and the geology photos) were not rendered. I keyed nothing from them.
- **Orientation check**: entrance a sits at the lower left of Fig. 6, which is SE with N to the right, and at the bottom of Fig. 1, which is SE. Both agree with the text: "s'ouvre au sud-est".
- **Rows**
  - The cave (grid as printed, `NIG`).
  - Humbert parts a, b, l, c, d, e, f, g, h, j, k, q, r (pillar), and the built elements u, v, w, x.
  - The blockage and the hearth.
  - The shaft crevice above h, and Patrich's three crevices.
  - From the geology appendix: fractures N150 and N30, the fracture to e, and two karst conduits (class `other`).
  - From App. B: the catchment basin, blocks A and B, the breach, the fallen slab, the "arch", wedge Y, the 1956 stone structures A/B/C (kept separate from u/v/w because the source does not equate them; likely matches are in `notes`), the upper chamber and its vertical passage.
- **Dimensions**
  - Text: doorway a, 1.60 × 1.35 m as cleared by de Vaux. Upper chamber, about 2 × 6 m, height 1.2–3.5 m. Passage, 2.5 m. Cave height, about 2 m.
  - Cave length: 19 m, from the dimension printed on the section (p. 76). Plan-scaled alternatives are in `notes`: about 21 m on Fig. 1 and about 18.5 m on Fig. 6, a mismatch between plans.
  - Plan-scaled, to the nearest 0.5 m: chambers and features on Fig. 6, and blocks A/B, the arch and wedge Y on Fig. 1. Boundaries on Fig. 6 are shaded zones, not lines, so those values are `low`/`medium` confidence.
- **Skipped**
  - Plan labels m, n, p, s and t (not described in the text).
  - Excavation trenches (Operation B, de Vaux's sounding), Patrich's dump terrace, the modern path and camp, and strata.
  - Tombs 32–37 named in the diary (no physical attributes in this source).
  - Other caves named only as distances (3Q, 1Q, Patrich's cave 24, caves A and B). Their distances are in the notes of the 11Q row.
  - All scroll and text matters.
