# mp18, reader A (group Q2): keying log

- Source: Magen & Peleg 2018, *Back to Qumran: Final Report (1993–2004)*, JSP 18, chapter "Site Description" (JSTOR chapter PDF, 91 pages, printed pp. [11]–[100]; printed page = PDF page + 9).
- Text read: the whole bucket text extraction, PDF pp. 1–91 (`qum/src/mp18_site_description.txt`, 153,032 characters). NUL bytes in the JSTOR footer were stripped from a working copy; no other text was changed.
- Instructions followed: `SCHEMA.md`, `READER_INSTRUCTIONS.md`, `QUMRAN_NOTES.md`. No other repo file, keyed file, project document or web source was opened.
- Started: 2026-10-31 19:16 PT (02:16:45Z). Finished: 19:39 PT (02:39:18Z).
- Output: `keyed/mp18_A_g1.csv`, 312 rows, sha256 `6e3d39f1…7a96aae`. The generating script is a scratchpad copy: `key_mp18.py`, which writes the rows from data and checks them.

## Page renders viewed (render_bucket.py, PDF pages)

| PDF p. | Figure | Use |
|---|---|---|
| 3 | Fig. 9, general plan | Viewed only. Has a north arrow, but its scale bar is labelled "cm", so I scaled nothing from it. |
| 44 | Fig. 57, western building | 0–5 m bar and north arrow. **Scaled cistern L110:** inner rim c. 5.0 m (N–S) × 5.35 m (E–W), keyed as diameter `5-5.5` (`plan_scaled`). Pools L117/L118 were not scaled because their N and S limits merge with channels and steps. |
| 87 | Fig. 112, graves T1–T5 | 0–5 m bar; each plan has a north arrow. Scaled the shafts of T1 (1.5×0.5 m, depth 1.5), T2 (2.0×0.5, depth 2.0) and T3 (2.5×0.5, depth 2.0) to the nearest 0.5 m. For T4 and T5 the text gives depth 1.70 m, so only the text is keyed and the scaled plan sizes are in notes. |
| 89 | Fig. 114, grave T7 | 0–3 m bar and north arrow. T7 shaft scaled to 2.0×0.5 m. The second plan on the page is not captioned, so I did not use it. |

I scaled nothing else from plans. No opening direction comes from a plan alone: all directions are from the text. For the burial chambers, the text gives the side of the shaft the chamber is on, and I keyed the chamber mouth facing the opposite way. Those six rows are marked medium and explained in their notes.

## Conventions used

- `feature_id` is `mp18:<locus>` with the source's labels: L-numbers; combined loci as printed (`L12-L14`, `L48-L49`, `L86-L87-L89`); walls `W…`; channels 17 and 18; graves `T1`–`T9`. For sub-features I added a suffix: the wall label for an opening in a named wall (`L8.W525`), otherwise a short descriptive suffix (`.a`, `.niche`, `.stE`). Features with no source label got descriptive ids (`NW_tower`, `central_channel`, `aq.long_tunnel`, `eastern_dump`, and so on).
- `site_name` is "Qumran" throughout, including the aqueduct in Naḥal Qumran and the cemetery. No grid reference is printed, so `grid_printed` and `grid_system` are blank and `position_basis = text_only`.
- In a printed "a×b" for a niche, window or opening the order is not stated. I keyed width × height and said so in notes.
- `n_openings` counts all openings the text states, blocked ones included. `opening_dirs` holds only directions the text states, either directly ("in the eastern wall", "leads westward") or through a wall the text names as the room's N/S/E/W wall. Where the text gives only a corner position, or no direction, the count can exceed the directions given; the notes say so.
- Steps that belong to a doorway and descend into the next room: `n_steps` is on the doorway row with `steps_where = outside`, and also on the receiving room with `into_feature` (L4, L30, L77).
- `in_window`: phase A (Hasmonean) and phase B (1st c. CE) count as yes. De Vaux's period III items (garrison, dated 72–73 CE on p. 11) are also yes. Iron Age items are no, as is the plateau (not settled). Anything else undated is unknown.
- Walls named only as boundaries, plan labels without text, and test squares or soundings are not keyed as rows; they are mentioned in the notes of the features they belong to.

## Problems and inconsistencies in the source

1. **L67** has two sizes in the text: 1.80×1.75 m on p. 44 and 2.05×1.75 m, 1.43 m deep, on p. 86. The p. 86 values are keyed; p. 44 is in notes.
2. **L34 channel** is printed "15 m-wide", which is impossible in a 2.00 m-wide room (probably 15 cm). It is keyed as printed with confidence low.
3. **Long tunnel wall** is printed "preserved to a height of 0.16 cm", keyed as 0.0016 m with confidence low (probably 0.16 m).
4. **Pools L117/L118** have no dimensions in the text. The captions of Figs. 59, 95 and 96 call them "pools L17 and L18". Keyed with relations only.
5. **Small pool SE of L48–L49** has no locus number in the text; keyed as `L48-L49.SEpool`.
6. **Central channel** is "0.50 m wide" on p. 80 but "broad open central channel" on p. 94. The 0.50 m figure is keyed.
7. Several quotes had to be shortened where a page footer or caption interrupts a sentence in the extraction (e.g. L6–L40 platform, L98–L3064, L111 N entrance, L138). Every quote was checked against the source text by script.
8. Plan-only loci in the SE area (L44, L59–L61, L63, L64, L72, L80, L84 and others on Figs. 9, 41, 71, 104) are not described in the text and are not keyed.
9. Cemetery graves excavated by de Vaux, Steckoll and Eshel & Broshi are mentioned only by contents (bones, finds), with no physical attributes, so they are not keyed. T1–T9 (2002) are keyed, each with its mound and, where present, its chamber.
