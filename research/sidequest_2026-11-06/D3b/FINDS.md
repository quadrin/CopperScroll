# Side-quest D3b: figure and plate cross-references in published volumes (6 Nov 2026)

Lane D3b (brief §4 D3, second pass). Route: data first, then a hand check of every flag. I took the text layers of seven page-split PDFs from the store (`pdf/<slug>/pages.jsonl`). For each one I extracted every in-text reference (Fig., Figs., Figure, Pl., Plate, Plan, Table, "see p.") and every caption (a line that starts with the same labels). I separated out citations of other publications (author–year before the reference). Then I ran three checks:
(a) does the cited target exist;
(b) do the locus, wall, unit, room, area or SC tokens in the citing clause conflict with those in the caption;
(c) a hand read of samples, and of every flag.

Four volumes were done in full: Magen 2018 (Qumran), Stern 2025 *Maresha IV*, Leibner 2018 (Wadi Ḥamam) and Reich & Shukron 2021 (City of David). DJD III vol. I was a partial pass: Fig. 5 against the cave catalogue.

Data: `xref_checks.csv` (5,222 rows: doc, PDF page, reference as printed, target, found?, caption subject, match?, note). Scripts: `xref_scripts.md`. Page numbers are PDF pages of the store copy. *Maresha IV* printed page = PDF − 11.

**Excluded as already known.** The Magen 2018 captions of Figs. 59, 95 and 96 say "pools L17 and L18" where the text means L117/L118. This is already logged on `sandbox/methods` (`sandbox/attribute_inventory_2026-10-31/keyed/mp18_A_g1_log.md`, line 35). Earlier *Maresha IV* cards (A6-3 grid order; B3-1/B3-2 SC 57 → 126, CIIP 3738) do not touch figure references.

---

FIND CARD
Title (one line): *Maresha IV* (Stern 2025, IAA Reports 76) points 10 times to the wrong figure, or to figures that do not exist, mostly where other chapters cite the chapter 1–2 figures. Four of the chapter 1 pointers are exactly two numbers too low.
Lane: D3 (D3b)
What is odd (2–4 sentences): I checked by hand all 69 references in the volume to chapter 1–2 figures, the 47 figure cells of Tables 5.1–5.4 and the 22 rows of Table 6.1. In each of 10 cases, the cited figure shows a different complex or subject. Another figure in the same volume shows exactly what the citing sentence describes, except in one case where the cited numbers do not exist at all. Every wrong cross-reference comes from a different chapter or section (ch. 1 → ch. 2; ch. 2 → ch. 1 and ch. 6; Table 5.2 → ch. 2; ch. 7 → ch. 2). The references inside chapter 1, and the tables of chapters 5 and 6, are correct. Four chapter 1 targets are off by exactly +2 (1.5→1.7, 1.6:2→1.8:2, 1.8:1→1.10:1, 1.8:2→1.10:2), which looks like figures were renumbered after the cross-references were written.
Evidence (exact sources: file path / page / figure / frame / coordinates): bucket doc `Stern-2025-Maresha-IV-Subterranean-Complexes-IAA-Reports-76-db5921ab`, PDF pages (printed = PDF − 11):
1. PDF 28: "SC 89 has four pressing installations (in Room 75, Figs. 2.12.2, 2.12.3)". Fig 2.12 (PDF 134) is "Cistern with banister in Room A21" in SC 61. The Room 75 presses are Figs. 2.17–2.18 (PDF 167).
2. PDF 90, SC 30 "es-Shuk": "'Columbarium Shuk/Market' in English (see Chapter 1, Fig. 1.5)". Fig. 1.5 (PDF 24) is "Spiral staircase in a cistern in SC 61". The SC 30 columbarium is Fig. 1.7 (PDF 27).
3. PDF 133, SC 61: "(see Chapter 1 : Fig. 1.8:1 Chapter 7 : Fig. 7.7)". Fig. 1.8:1 (PDF 29) is "Olive press in SC 1". Fig. 1.10:1 (PDF 31) is "Olive press in SC 61". Fig. 7.7, in the same parenthesis, is correctly SC 61.
4. PDF 164, SC 89: "three olive presses (Rooms 1, 40, and 75; [see Chapter 1, Fig. 1.8:2])". Fig. 1.8:2 is "olive press in SC 90". Fig. 1.10:2 is "olive press in SC 89 (Rm 40)".
5. PDF 170, SC 90: "olive press in pristine condition … (see Chapter 1 : Fig. 1.6:2)". Fig. 1.6:2 (PDF 25) is "plastered cracks in cistern wall". The SC 90 press is Fig. 1.8:2.
6. PDF 228, SC 169 Room 9a: "reads 'Zabdada' (see Chapter 6, Fig. 6.17 …)". Fig. 6.17 (PDF 343) is "SC 144 inscription", the modern "Były Polacy" graffito. Chapter 6 itself and Table 6.1 (PDF 344–345) put Zabdada at Fig. 6.18.
7. PDF 300, Table 5.2, row "90 1 7 Olive Press 2.21". Fig. 2.21 (PDF 215) is "Dovecotes in Rooms B and C" (SC 147). Fig. 2.20 (PDF 170) is "Subterranean Complex 90. Vandalized altar in Room 7."
8. PDF 346 (ch. 7): seven tombs "within SCs 36, 71, 89, 92, 93, 149, and 154 … Chapter 2 : Fig. 2.12". Fig. 2.12 is the SC 61 cistern, and SC 61 is not on the list. The repurposed-tomb figures are 2.16 (SC 89) and 2.22 (SC 149).
9–10. PDF 358 (ch. 7): "cistern in SC 105 was repurposed into a columbarium (see Chapter 2 : Figs. 2.91–2.92)". Chapter 2's figures end at 2.22. Plans 2.91–2.92 show SC 91 and SC 92, and SC 105 is Plans 2.105.1–2 (PDF 181).
Captions of items 1, 7 and 8 were checked on page images (PDF 134, 170, 215); the rest are from the publisher text layer. Rows are marked "NO" in `xref_checks.csv`.
Why these are errors and not a convention: the volume's own convention is "Fig. chapter.number:panel", and it uses separate "Plan" numbers. In every case the caption names a different SC or a different kind of installation from the one the sentence describes. In nine cases a figure elsewhere in the same volume matches the sentence exactly; in the tenth (items 9–10), no figure with that number exists.
Literature check (queries run, result, tag): web search `Stern 2025 "Maresha IV" Subterranean Complexes IAA Reports 76 review OR errata` found only announcements (AWOL, 1 Sep 2025; the author's academia.edu page) and no review or corrigendum. Repo: main and `branch_only` contain nothing for "Zabdada", "Polacy", "es-Shuk" or "Fig. 2.12". B3's CIIP × *Maresha IV* concordance (`out/B3/`) checked readings and found them consistent; it did not check the figure pointers. **NEW TO THE LITERATURE.**
Why it might matter: *Maresha IV* is the new reference catalogue of the 170 complexes (open access, 2025). A reader who follows the pointers will see SC 1 or SC 90 instead of the SC 61 and SC 89 presses, and a Polish 1943 graffito instead of the Idumaean name Zabdada (CIIP 3737). Table 5.2 also sends the SC 90 altar to a dovecote. The +2 offset suggests the chapter-2/7 pointers into chapter 1 should all be re-checked for the IAA online edition.
How to confirm or kill it (with data in hand, or what is missing): open the 13 PDF pages listed (about 10 minutes). The card is killed only if the IAA's current online PDF differs from the store copy (a corrected re-issue). I did not compare the two editions.
Confidence: high
Touches the Copper Scroll? no (Maresha lies outside the scroll regions)

---

## Dead ends
- Magen 2018 (Qumran site description): all 107 internal references resolve (Figs. 9–115). Of the 7 locus flags, 4 are normal (multi-locus captions). Figs. 59/95/96 "L17/L18" for L117/L118 are already on `sandbox/methods`, so not carded.
- Leibner 2018: of 1,378 internal references, every chapter-numbered target exists. There are three label slips: "Fig. 12.5:13" for Pl. 12.5:13 (PDF 454); "Table 7.3", which is the legend of Plate 7.1 (PDF 287/293); and the Table 18.5 caption printed without "Table" (PDF 621). The 19 locus/unit flags were all dismissed by hand, and the chalkstone text agrees with the catalogue (Cat. 110–133). Trivial, not carded.
- Reich & Shukron 2021: of 1,941 internal references, every apparent gap (Figs. 2.18, 8.5, 8.16, 13.145–146, 46.4) is a "Figure." or line-wrap variant in the text layer. All 39 locus flags were dismissed. Ch. 31 lmlk no. 3 is "Area A, Permit 3230" in the catalogue and "Area J" in the caption (PDF 529–530). This is ambiguous, because Permit 3230 is also used for Area A finds in ch. 44, so it is not carded.
- DJD III vol. I: in the cave catalogue (PDF 27–32), all 19 citations of Fig. 5 agree with the "N° de fouille" column of the Fig. 5 legend (PDF 44, read from the page image). "cf. ci-dessous, p. 16" lands on the Iron II bowl and lamp, and the page ranges for 3Q and 6Q agree with the contents page. The OCR'd text layer garbles Roman plate numerals, so there was no automated plate check. The Copper Scroll plates were left alone (A1b/A1c covered them).
- "See p. N" internal page references hardly occur in these volumes (2 hits, both to other works). The route has nothing to check here.
- *Maresha IV* missing plan captions (Plans 2.8–2.9, 2.51.2) are gaps in the text layer: the Plan 2.9 caption is visible on the image of PDF 63. "Table 1" / "Table 4" for Tables 5.1/5.4 is a short form, not an error. "Fig. 6. 15.1–3" (ch. 6) is a typesetting slip. The SC 44/45 plans (Plan 2.44 = SC 44/45, Plan 2.45 = SC 44) are odd but match their captions. "SC 705" on PDF 357 was not checked.
- HCM 2016, JSP 8, ROSAPAT 07 and Humbert–Fidanzio 2019 cannot be checked by machine: their plate and figure captions are not in the text layer (HCM 2016: 163 of 164 internal Pl. references unresolved; JSP 8: 227 of 346). This would need page images; not attempted.
- Humbert–Gunneweg 2003: 75 internal references, and the 8 unresolved ones are de Vaux's plans and other volumes' plates (external). Nothing to card.

## Blocked inputs
- None hard-blocked. Limit: plates and captions with no text layer (HCM 2016 `Humbert-Chambon-Mynarczyk-eds-2016-…-31a119b3` from PDF p. 442; `01-JSP8-Mount-Gerizim-II-indexed-843e1fce`; `Nigro-Sala-Taha-eds-2011-…-9af25da3` Plates 227–267) leave those volumes unchecked by this method.
- I did not compare the IAA online PDF of IAA Reports 76 with the store copy.

## Seed / reproducibility
- Text layers: `hexview.pdf_pages_text(<slug>)` for the slugs above, saved to `scratch/D3b/txt/<KEY>.json`. Run `python3 -I xref.py KEY`, then `python3 -I subject.py KEY` (both in `xref_scripts.md`). Panel → SC maps for *Maresha IV* Figs. 5.x were read from the captions on PDF 301–316.
- Page images viewed (not kept in output): *Maresha IV* PDF 63, 64, 113, 114, 134, 170, 215; Leibner PDF 293, 620, 621; DJD III PDF 30, 32, 44.
