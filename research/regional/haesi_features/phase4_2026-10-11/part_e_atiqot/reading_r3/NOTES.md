# Phase 4, part E, reader r3: notes

Reader r3 read ʿAtiqot units in tier T2, order positions 136–208 of `../pdfs_needed.csv` (73 units, all Z4 by the screen), on 11 October 2026. Everything here is exploratory. Nothing identifies a place for the scroll.

## What was read and how

- **Files.** The 73 PDFs in `~/Downloads/IAA portal volumes/phase4/` (owner's Mac), opened one by one by exact name. Nothing else in `~/Downloads` was listed or opened. Every PDF's SHA-256 matched `../../downloads_2026-10-11.csv` (73/73).
- **Text.** `pdftotext -raw` and `-layout`, into `$HOME/p4text/r3/` on the Mac (outside `mnt`), not copied to the repository. All 73 PDFs have a text layer; no OCR was needed.
- **Hebrew.** Twenty-one units are Hebrew articles. They were read in Hebrew (`pdftotext` reverses the word order within each line; quotes are given in reading order). Where the PDF carries the English summary, it was read too.
- **Spans.** `reports.csv` `text_lines` gives the line ranges of the `-raw` text read closely; `grep:all` marks keyword searches (English and Hebrew feature terms) over the whole text. `text_sha256` is over the listed ranges only, whitespace collapsed (`scripts/verify_spans.py`, run on the Mac; script SHA-256 `81c8a35901680d565153e4f380d91418dd4fd3b6335d064476883af8cd77dd2e`). "all" means the whole short article.
- **Quotes.** Every quote was checked against the source text by the same script (`data/spans_r3.jsonl`): exact substring, or (Hebrew) every word present.

## Deviations and choices (exploratory)

- **D1. Order.** Position 142 (ATQ87-081) was read before 141 (ATQ76-123). No coding depended on it.
- **D2. Text of other articles seen.** Three Hebrew PDFs end with the volume's English-summary pages, which also carry parts of neighbouring summaries: the start of the Horbat Gores burial-cave summary (ʿAtiqot 54, pp. 87*–94*; map ref. NIG 21851/62907) in ATQ54-061s and ATQ54-047s, and the end of the Ramat Sharet summary (captions only) in ATQ54-047s. A few lines were seen. Nothing was coded from them. The text is ordinary excavation text, not held material. If the Horbat Gores article is another reader's unit, that reader should still code it from its own PDF.
- **C1. Kiln and other non-water channels** (the rock-hewn air channel L1026 under the kiln in ATQ87-071s) are not coded as `channel_aqueduct`.
- **C2. Finds and specialist reports.** Where a finds, anthropology, epigraphy or lab report names the feature its material came from in the same excavation (a tomb, a burial cave, a pool, a quarry, channels), that feature is coded as the report's row, with a note naming the excavation report. These rows repeat features coded elsewhere (see the list below). A feature named only as a place near the find, or only as a findspot label in a catalogue, is not coded.
- **C3. Dam in ATQ106-239.** The 2018 probe was dug inside Tunnel 230, a vault built into the core of the Tyropoeon dam wall (exposed earlier by Onn). The dam is coded once, as the context of the reported work. The miqveh and pools in Room 21, known from Onn's excavation, are not coded.
- **C4. Winepress parts.** Ducts, gutters and channels inside a winepress belong to its `rockcut_installation` row and are not coded again as channels.
- **C5. Industrial vats** (the soap-factory vats in ATQ67-119, small plastered industrial installations elsewhere) are not coded as pools.
- **C6. Map references.** A printed range is converted at its first value, as in phases 2–3. ATQ59-021s: the English summary prints NIG 22280/61302, which as written falls about 17 km south of the place described; the Hebrew text's NIG 2228/6302 is used. ATQ76-011s: all three printed references (NIG 1777x/7669x-7719x) fit neither grid in Jerusalem and are not used; the unit is placed by name. ATQ54-095s: the Hebrew title says "north-western corner", the portal's English title "Northeastern"; the reference (NIG 221485/631715) is by the Knights Palace hotel, i.e. the north-western corner.
- **C7. Summaries of results published elsewhere** are cited work, not coded: ATQ113-i03 (a synthesis on the Siloam pools), ATQ120-i02 (Motza; "nearly 200 burials" and quarrying mentioned only as a summary), ATQ120-i08 (features at the Beit Shalom Garden).
- **C8. Dumps are not hoards.** The 1st-century cooking-pot dump in the cistern of ATQ112-i05 is not coded as `hoard_cache`: the report says it was dumped, not hidden. The cistern is coded.
- **C9. One feature, one class.** The Mount Scopus chalk quarry cave (ATQ113-i09, ATQ113-i11) is coded as `cave_with_finds` (an artificial underground cavity), not also as a quarry.
- **C10. New observation of standing features.** ATQ119-i02 describes the five gutter-like channels of the Temple Mount walls from earlier publications plus the authors' own "recent observation"; they are coded as `inspected`. The Second Temple date is the authors' argument.
- **Feature-level splits.** Where one report gives one class with different dates or different work (excavated and surveyed), the class is split into rows by `feature_site` (for example quarries of two periods; burial caves excavated and surveyed). `excavated_or_surveyed` is then set per row.
- **Hedged labels** follow amendment A4: the named period decides; the hedge stays in `period_as_given`. A range reaching beyond 135 CE but named "Early Roman" by the report (glass of the "Early Roman period (2nd half 1st–2nd c. CE)") is coded yes; 70–135 CE (ATQ63-045 Cave 1) is inside the window.

## Same feature in more than one row (not deduplicated, per the phase-4 plan)

- ʿEn Yaʿal burial cave (Area B): ATQ76-011s, ATQ76-015s, ATQ76-123.
- Sallah ed-Din Street Late Roman cemetery: ATQ80-045, ATQ80-073, ATQ80-133 (T2200).
- Ketef Hinnom (Avner and Zelinger): ATQ80-023s, ATQ80-055s (quarry and tombs).
- Kh. Umm Leisun crypt: ATQ83-185, ATQ83-205.
- Nahal Qidron monastery tombs: ATQ89-049, ATQ89-111.
- Siloam Road plastered pool: ATQ101-071s, ATQ101-079.
- Nahal Refaʾim (railway) Cave 500 and pits: ATQ116-i11, ATQ116-i12.
- Mount Scopus south slope (Re'em): ATQ63-027, ATQ63-045 (quarry, miqveh, a burial cave).
- Mount Scopus chalk quarry cave: ATQ113-i09, ATQ113-i11.
- Moza Crusader reservoir: ATQ58-135 and probably ATQ91-193.
- Rows whose excavation report is not among my units: Cave 900 (ATQ88-069), Har Homa hoard (ATQ106-297), Umm Leisun crypt, ʿEn Lavan cave (ATQ98-103), Tel Arza tomb (ATQ106-187), Wadi el-Halaf caves (ATQ48-i06), Qidron Valley burial caves (ATQ78-025), Musrara tombs (ATQ116-i09), Warren's Gate channels (ATQ106-211), Western Wall Plaza quarry (ATQ72-001).

## Protected and held

- No unit described a cave in a held area; all 73 units lie in Jerusalem and its hills (Z4). `held.csv` has its header only.
- No Tell es-Sultan north-strip text and no Kh. ʿAlmit text was met, so there is no `tier1_kh_almit_extraction.md`.
- The two flagged units (110.9, 116.8) are not in my range.

## Figures worth archiving later (not stored; rights to be checked)

Printed page given where seen in the text layer; otherwise the article's range.

- ATQ101-071s (Siloam Road): Plan 1 (plan and sections of dam and pool); Figs. 3–5 (plastered dam wall, pool, Channel 103) — Hebrew pp. 71*–86*, captions p. 138.
- ATQ106-239 (Western Wall Tunnels): Plan 1 (Great Causeway and Wilson's Arch), Plan 2 (Tunnel 230, dam, miqveh) — pp. 239–255 (Fig. 1 and Plan 1 near p. 240–241).
- ATQ108-i13 (Horbat Mazruq): Fig. 1 location map, Fig. 2 aerial view 1918 (pp. 250–251); Plan 1 general plan; Plan 4 reservoir F4 (p. 268); Plan 5 burial caves 1–3; Plan 6 hiding complex (p. 274); Figs. 15–29.
- ATQ113-i09 (Mount Scopus chalk quarry): Figs. 1–2 location; plans of the lower and upper caves; Plans 2–3 limestone quarry, winepress and water installations (pp. 251–253); Figs. 63–72 (pp. 253–263); Plan 4 burial cave T44 (p. 263); Plan 5 tunnel T45.
- ATQ63-027 (Mount Scopus south slope): Fig. 1 map of the burial caves; Plan 1 quarry Area A1; Plan 2 quarry and installations Area A2 (p. 30); Figs. 3–4 cistern and miqveh (p. 31); Figs. 5–6 burial caves.
- ATQ54-031s (Ramat Sharet): Fig. 1 site map with survey sites A–M; Plans 1–3 winepresses; Plan 4 winepress 1III in burial cave; Plan 5 miqveh 1I — pp. 31*–45*.
- ATQ54-047s (Mount of Olives caves): Plans 1–3 (Caves 3, 4, 2), Figs. 2–20 — pp. 47*–59*.
- ATQ49-i05 (Mount of Olives burial cave): Plan 1, Figs. 1–4 (pp. 33–36).
- ATQ65-093 (Diskin St.): Plan 1 burial cave (p. 93–94).
- ATQ59-021s (ʿEin el-Luza): Plans 1–3, Figs. 1–4 — pp. 21*–35*.
- ATQ80-045 (Sallah ed-Din St.): Fig. 1 location map, Plans 1–6, Figs. 7, 18–21 (quarries) — pp. 45–71.
- ATQ80-023s (Ketef Hinnom): Plans 1–9, Figs. 3–5, 10–11 — pp. 23*–53*.
- ATQ89-049 (Nahal Qidron monastery): Plan 1, Plan 2 (burial complex) — pp. 49–82.
- ATQ120-i13 (Byzantine Street, Area S2): Plans 1–5, Figs. 6–12 (channels, Cistern 240).
- ATQ44-i13 (Beit Safafa): Fig. 1 location map; Plans 1–4 (winepress reconstruction Plan 4); Figs. 2–15.
- ATQ58-135 (Moza reservoirs): Plans 1–2 — pp. 135–144.
- ATQ67-041 (Mount of Olives dwelling cave): Plans 1–4 — pp. 41–59.
- ATQ54-095s (Old City wall, NW corner): Fig. 1 location map, Plan 1 plan and sections — near p. 96*.
- ATQ117-i02 (Nebi Samwil): Figs. 1–4 (site plan of the six units; Cave 3).
- ATQ116-i11 (Nahal Refaʾim): Fig. 1, Plans 1–8 (Plan 8 shaft tomb Cave 500).
- ATQ119-i02 (Temple Mount channels): Figs. 1–2.
- ATQ51-049s ('Jordanian Garden'): Plan 1, Figs. 1–2 — pp. 49*–53*.
- ATQ43-i15 (Har Hozevim): Plan 1, Figs. 16–18 (quarries, cupmark, cave).

## Proposed changes for the integrator

- Merge `reports.csv` and `features.csv` into part E with the other readers' tables; the columns are the phase-2 columns in order.
- When the merge is extended, deduplicate the same-feature rows listed above by excavation, not by report.
- In-window rows of note for entry lanes (exploratory, INFERENCE only, no claim): the Siloam dam, plastered pool and connecting channel (ATQ101-071s); the Tyropoeon dam (ATQ106-239); the Horbat Mazruq cisterns, reservoirs, possible miqveh and First-Revolt hiding complex (ATQ108-i13); the Mount Scopus chalk quarry cave and Early Roman cistern (ATQ113-i09); the five Temple Mount wall channels (ATQ119-i02, authors' dating).
- ATQ59-021s and ATQ76-011s carry misprinted map references (C6); a later coordinate pass may want to check the plans.
