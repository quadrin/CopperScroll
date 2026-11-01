# mp18, reader B (group Q2): keying log

- Source: Magen & Peleg 2018, *Back to Qumran: Final Report (1993-2004)*, JSP 18, chapter "Site Description" (JSTOR chapter copy, 91 PDF pages; printed pp. 11-100; printed page = PDF page + 9).
- Text read: `scratchpad/qum/src/mp18_site_description.txt`, all PDF pages 1-91 (every prose page; plan pages checked for prose: only labels and captions).
- Started 2026-10-31 19:16 PDT (02:16 UTC); finished 19:36 PDT (02:36 UTC).
- Files read: SCHEMA.md, READER_INSTRUCTIONS.md, QUMRAN_NOTES.md and the source text. No other repo files, keyed files, project docs or web.
- Output: `keyed/mp18_B_g1.csv`, 331 rows, written with Python `csv` in SCHEMA header order.

## Page images rendered (render_bucket.py, saved to scratchpad/q_B_q2/)
- PDF p. 27 (Fig. 38, eastern-wing plan): checked for a locus label for the small pool SE of L48-L49. It has none, so it is keyed as `L48-L49.SE_pool`.
- PDF p. 41 (top): checked the printed "15 m-wide channel" (L34). The misprint is in the original, so the width is not keyed.
- PDF p. 44 (Fig. 57, western building plan, 0-5 m bar, north arrow): scaled the inner diameter of cistern L110, about 5.4 m E-W and 5.0 m N-S, keyed `5-5.5`, `plan_scaled`. Pools L117 and L118 are oblique on the plan and were not scaled.
- PDF p. 87 (Fig. 112, graves T1-T5, 0-5 m bar): scaled shaft length, width and depth to the nearest 0.5 m on a 0.5 m grid overlay. Check: the scaled section depths of T4 and T5 (about 1.7 m) agree with the printed 1.70 m. For T4 and T5 the depth is keyed from the text.
- PDF p. 89 (Fig. 114, "Graves T-7"): not scaled, because two cuttings are drawn and which is T6 and which T7 is unclear.

## Conventions and judgement calls
- `feature_id`: the source's locus, wall or grave label (`mp18:L48-L49`, `mp18:W526`, `mp18:T3`). Combined loci keep the source's form (`L12-L14`, `L86-L87-L89`). Sub-features without a label get descriptive suffixes (`L8.W525_opening`, `L121.N_pool`). Unlabelled wholes get names: `main_building`, `northwestern_tower`, `small_tower`, `central_channel`, `aqueduct.*`, `cemetery`, `point_B`. De Vaux's tomb numbers are `dV.Tomb16` and so on, kept apart from the 2002 graves T1-T9.
- An unlabelled "A×B m" is keyed as length = A and width = B. For openings printed as A×B, the notes say that the width/height split is not stated.
- Preserved heights are keyed as `height_m` and noted as preserved. Approximate and estimated values are keyed as printed and flagged in the notes (hall 19×8 m, courtyard 16×16 m, crack "some 30 m").
- Doorways and windows with a printed width get their own rows (windows are class `other`). Rooms also carry `n_openings` and the directions the text states. Directions that are inferred or that only name a corner position are explained in the notes.
- Graves: one `tomb` row (shaft), one `cairn` row (fieldstone mound, with its long axis in the notes) and one `chamber` row where the text reports a burial chamber (side and blocking material in the notes).
- `in_window = yes` where the text assigns phase A or B (Hasmonean to 1st c. CE). `no` for Iron Age features and the unsettled plateau. Blank where no period is given.
- Text disagreements: L67 is 1.80×1.75 m on p. 44 but 2.05×1.75 m, 1.43 m deep on p. 86. The p. 86 values are keyed and the other is noted.
- Misprints not keyed: "15 m-wide" channel in L34 (p. 50); wall "preserved to a height of 0.16 cm" in the long tunnel (p. 79).
- Caption discrepancy: Figs. 59, 95 and 96 read "pools L17/L18", where the text has L117/L118. Noted.
- Wall relations: only walls that have their own rows are used in `relations`. Other wall numbers are in the notes.

## Not keyed (no attribute beyond class, or not an ancient feature)
- Excavation soundings and squares (L9/1, L10/1, L3047, L3050, L4/1 as a sounding, L3048, L3054, L3055, L30/1, L30/2, L3038, L3040, L3043, L3044, L3049, L3052, L4013, L4014, L4019, L5018, L9000-L9007, L401, the seven 1993 squares).
- Floors as such (L9122, L62's floor), except where they are part of a room row.
- Walled-in areas L130-L133 (named only). Steckoll's 10 graves and Eshel and Broshi's 2 graves (unlabelled; one of them is in the notes of `point_B`). Loci that appear only on plans (L64, L72, L84 and others).
