# Phase 4, part E, reader r2: notes

Reader r2 read tier T2, order positions 61–135 of `../pdfs_needed.csv` (75 units), on 11 October 2026, under the frozen phase-4 plan (`../../PLAN.md`, commit b002e03) and the phase-2 plan and amendments. Everything here is exploratory. No identification claim is made.

## What was read

- All 75 units, in the frozen order. Page ranges are in `data/page_map.csv`; the text span hashed is PDF pages 2 to the end of each file.
- Reading depth: title block, introduction and map reference; then every line hit by a keyword search for the ten classes (English and Hebrew), read in context with the description and dating paragraphs of each hit. Discussion sections were read where they date a feature. Pottery and finds catalogues were scanned by keyword only.
- Hebrew articles (10): the Hebrew text was searched with Hebrew keywords and the relevant passages were read; the English summary in the same PDF was read in full. Hebrew quotes are given in logical word order; pdftotext gives them in visual order, so they were checked as word sets on the page (`data/mac_quote_pages.csv`).
- Arrival check: `python3 -I research/preregistration/arrivals/arrival.py check` returned `manifest: ok (29 files)` before reading.

## Deviations and choices (exploratory)

1. **Finds reports and find contexts.** A finds or specialist report gets a feature row when it names an eligible feature as the context of its finds (for example a drainage channel, a burial cave, a quarry, a hoard). The same feature is often also coded from the excavation report or from a sister finds report (for example Channel 515 in ATQ119-i12, ATQ119-i14, ATQ119-i16 and ATQ119-i17; Burial Cave 900 in ATQ88-017, -033, -071; the Tel Arza tomb in ATQ106-177 and -193). Rows are not deduplicated in this phase, as the phase-4 plan says.
2. **Authors' own site visit.** ATQ63-001s (Kh. ʿAddasa): the authors record burial caves, underground cavities, rock cuttings and cisterns seen on their own visit (25.7.07). These are coded as `inspected`, undated. Survey results of earlier surveys in the same article are not coded.
3. **Features found in the same excavation but published elsewhere.** ATQ49-i02 mentions an Ottoman reservoir and winepresses found in the same salvage excavation (published in HA-ESI 116). They are coded, dated `no`.
4. **Built basins and vats.** Plastered water basins that are built, not rock-cut, are coded `pool_reservoir` when the report connects them with water or calls them a plastered basin (Umm Leisun basins L405–L406; Djabsha vat L1005; the plastered basin under the Kathisma mosaic, function not stated). Slab-lined or plastered installations without a stated water function are not coded (ATQ104-193 L3012, L5030; ATQ47-i22 pit L9; ATQ47-i25 troughs; ATQ58-091 troughs and silo).
5. **Hedged and second-hand dates.** As amendment A4: a hedged date takes the period named. ATQ47-i25 channel W4: the only date given is the Crusader date of the same channel at Zahal Square (another excavation); coded `no`. ATQ66-137 channel L80 ("We suggest a Crusader date"): `no`.
6. **Same class, different dates.** Where one report gives features of one class with different dates, they get separate rows (as in phases 2 and 3).
7. **Map-reference readings.**
   - ATQ54-001s: the Hebrew text's OIG string extracts as `13472/17332`; read as E 17332 / N 13472 (halves swapped by right-to-left ordering; INFERENCE). The printed NIG string does not match the OIG reference and is treated as a misprint.
   - ATQ47-i25: printed `NIG 2213/1829` is impossible; the OIG `1713/1329` is used.
   - ATQ106-089: the reference is printed northing first; read as NIG E 221616 / N 630959.
   - ATQ42-i22, ATQ42-i19, ATQ43-i11: grid not labelled; OIG by size (INFERENCE).
   - ATQ88-017, ATQ83-145, ATQ90-127, ATQ90-001s, ATQ106-001, ATQ106-257, ATQ119-i12: grid not labelled; NIG by the northing (geo.py rule).
8. **Name-only placement.** 48 units have no map reference in the text read. All name a place in Jerusalem or its hills (Jerusalem, Herodium, Har Homa, Beit Safafa, Nahal Refaʾim, Kh. Kaʿkul, Kh. Umm Leisun, Mordot Arnona). They are placed in Z4 by name (plan §2) without distances.
9. **Kh. ʿAdasa and Kh. ʿAddasa.** ATQ58-091 (Kh. ʿAdasa, Pisgat Zeʾev, NIG 22273/63722) and ATQ63-001s (Kh. ʿAddasa near Bir Nabala, NIG 220650/638945) are different sites; each is located by its own reference.
10. **ATQ114-i02.** The Rogem Gannim winepress in this article re-analyses ATQ66-079 and is not coded again. ʿEmeq Lavan and Mordot Arnona winepresses are coded with `feature_site`.
11. **ATQ110-i02.** Its rows come from the site's stratigraphic table, which the finds article prints; the excavation report itself is not in this reader's range.
12. **Quotes changed during verification.** Four quotes were shortened or replaced so that they occur in the extracted text: three in ATQ43-i11 (OCR errors such as "ofthe", "LI 18") and one in ATQ72-001s (the printed sentence is interrupted by a figure caption in the text layer). One ATQ54-001s quote is found only with spaces ignored (the raw text lost its spaces) and one only in the layout text.
13. **Pages.** The `pages` column of `features.csv` gives the printed page of the quote, from the PDF page where the verifier found it and `data/page_map.csv`. For Hebrew articles the English summary pages carry their own numbers.

## Figures to archive later (not stored)

Printed page of the caption in the extracted text (the figure may sit on the facing page). Plans of features in the region, location maps and sections:

- `ATQ66-079` Rogem Gannim: Fig. 1 (p. 79); Figs. 2–3 (p. 80); Fig. 4 (p. 81); Fig. 13, Cave 1 section (p. 88); Plan 1 (fold-out at the end of the PDF).
- `ATQ119-i12` Western Wall Tunnels dam: Fig. 1 (p. 265); Figs. 2–3 (p. 267); Fig. 4 (p. 268); Plan 2 (p. 272); Plan 3 (p. 277); Plan 4 (p. 279); Plans 5–9 (pages not recorded).
- `ATQ90-001s` Armon Ha-Naẓiv tunnel: Plans 1–7 and Figs. 2–20 (Hebrew section; captions listed on p. 166–167; figure pages not recorded).
- `ATQ69-069s` Upper Aqueduct and Kathisma: Fig. 1 route map, Plans 1–4 (Hebrew section; captions listed on p. 162; figure pages not recorded).
- `ATQ106-089` Mount Zion: Fig. 1 (p. 90); Fig. 2 (p. 91); Plan 2 (p. 93); Plan 3 (p. 100); Plan 4, hewn Room F (p. 119).
- `ATQ116-i05` City of David rock-cut rooms: Fig. 1 (p. 78); Fig. 2 (p. 80); Fig. 3 (p. 83).
- `ATQ83-145` Umm Leisun monastery: Fig. 1 (p. 146); Plan 3, crypts (p. 150); Plan 4 (p. 160); Plan 1 (fold-out at the end of the PDF).
- `ATQ43-i11` Umm Leisun: Fig. 1 (p. 127); Plan 1 (p. 128); Plan 2, cave and miqveh (p. 132).
- `ATQ106-257` Har Homa monastery: Fig. 1 (p. 258); Fig. 2 (p. 261); Fig. 27, winepress (p. 278); Fig. 29 (p. 280).
- `ATQ114-i02` winepresses: Fig. 1 map (p. 2); Fig. 2 (p. 5); Fig. 3 (p. 7); Fig. 7 (p. 11); Fig. 11 (p. 16).
- `ATQ54-125` Mamillah: Fig. 1 (p. 125); Plan 1 (p. 127).
- `ATQ47-i25` Kikkar Safra: Fig. 1 (p. 169); Plan 1 (p. 171).
- `ATQ113-i02` Har Homa: Fig. 1 (p. 2); Fig. 2 site plan (p. 4).
- `ATQ110-i02` Mordot Arnona: Fig. 1 (p. 4); Fig. 2 plan by strata (p. 5).
- `ATQ65-i18` cairn field: Fig. 1 (p. 1*); Plan 1 (p. 3*); Plan 2 (p. 7*).
- `ATQ88-017` Burial Cave 900: Plans 2–3 (pp. 22–23).
- `ATQ106-001` Beit Safafa cave: Fig. 1 (p. 2); Fig. 2 (p. 3); Plan 1 (p. 4).
- `ATQ49-i02` Holyland shaft tombs: Fig. 1 (p. 1).
- `ATQ42-i19` Mount of Olives shrine: Plan 1 (p. 221); Plan 2 (p. 224).
- `ATQ66-137` Muristan: Fig. 1 (p. 138); Plan 1 (p. 140); Plan 4, Underground Chamber V (p. 148).
- `ATQ90-127` Djabsha Street: Fig. 1 (p. 127).
- `ATQ104-193` Ẓahal Square: Fig. 1 (p. 194); Plan 1 (p. 196); Plan 2 (p. 200); Plan 3 (p. 207).
- `ATQ42-i22` Armenian Patriarchate Road: Fig. 1 (p. 261); Plan 1 (p. 263).
- `ATQ106-195` Warren's Gate: Fig. 1 (p. 196); Plan 1 (p. 199); Plan 4 (p. 204); Plan 5 (p. 206).
- `ATQ119-i17` Great Causeway sampling: Fig. 1 (p. 386); Fig. 2 (p. 387).
- Hebrew articles with plans (pages not recorded; captions in the English summaries): `ATQ54-001s` Plans 1–3; `ATQ63-001s` Fig. 1, Plans 1–2; `ATQ54-015s` Plans 1–3; `ATQ54-087s` Fig. 1, Plan 1; `ATQ76-001s` Fig. 1, Plans 1–2; `ATQ80-067s` Fig. 1, Plans 1–3.

## Not read

None. Every assigned unit was read.

## Problems

- The raw text of some older volumes lost spaces between words (ATQ54-001s summary) or has OCR errors (ATQ43-i11). Quotes were checked against these texts; see choice 12.
- Running heads are missing from the text layer of ATQ49-i02; its pages were taken from the layout text.
- For Hebrew articles, figure pages could not be tied to the Hebrew pages from the caption lists.

## Proposed changes for the integrator

- Merge `reading_r2/` rows into part E's `reports.csv` and `features.csv`, and mark T2 positions 61–135 as read in part E's records.
- When the merged inventory is extended, deduplicate the same-feature rows listed in choice 1, and link ATQ119-i12/-i14/-i16/-i17 and ATQ88-017/-033/-071 to one feature each.
- Add the figures listed above to the rights-checked archiving queue.
