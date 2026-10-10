# Past-search schematics

These sheets draw **past searches and survey records**, not scroll entries. They sit beside the [entry schematics](../README.md) and use the same drawing kit (`../lib/schematic.py`). Each sheet draws on the search ledger ([salvage_records](../../history/salvage_records/README.md)) and the source extractions in `research/history/`.

A sheet shows what a source says was looked at, dug or reached, and where. It does not say that any deposit is or is not at a place.

## How to read a sheet

- **Blue** = dug, cleared or reached, with who and when.
- **Red** = the scroll's own wording, or the depths it states.
- **Grey** = not recorded, or not dug.
- **Ochre dashed** = looked at, measured or recorded, not dug.
- Sheet 10 is the exception: there, blue and grey mark the purpose of a search coded in the ledger, not whether a place was dug.
- A sheet is drawn to scale only where it says so. Elsewhere it is a schematic arrangement, and the distances the sources give are written on the drawing.
- Each footer has four parts: the sources, how the sheet was drawn, what it shows and what it does not show.

## Index

| Sheet | What it shows | Ledger rows | Files |
|---|---|---|---|
| 01 | The March 1952 cliff survey around Cave 3. Survey points plotted to scale on the Palestine grid (from de Vaux's 1953 map, about ±30 m), with what DJD III records at each. | S01 | [svg](search_01_qumran_caves_1952.svg) · [png](png/search_01_qumran_caves_1952.png) |
| 02 | Kh. Mird (Hyrcania): what each campaign from 1952 to 2023 looked at or dug. Schematic plan, not to scale, with a timeline. | S03 (the 1962–63, 2000–04 and 2023 work is not yet in the ledger) | [svg](search_02_mird_hyrcania.svg) · [png](png/search_02_mird_hyrcania.png) |
| 03 | The "monument" SW of Kh. Mird, Allegro's candidate for his item 2: a plan to scale from the stated dimensions, and a schematic section showing what the April 1960 clearance examined. | S03 | [svg](search_03_mird_monument.svg) · [png](png/search_03_mird_monument.png) |
| 04 | Every "dig N cubits" in the project translation (26 entries) against the depths the ledger's searches reached. Depth axis to scale. | S01, S03, S07, S09, S11, S13 | [svg](search_04_depths.svg) · [png](png/search_04_depths.png) |
| 05 | Where the ledger's searches were, against the atlas's 39 candidate places. Three maps to scale (whole area, Jericho–Qumran, central Jerusalem); counts computed from the atlas, the ledger and the looks table. | all rows with a place or point | [svg](search_05_coverage_map.svg) · [png](png/search_05_coverage_map.png) |
| 06 | Entry 25, "the cave of the pillar with the two entrances": the text's clues against four candidate caves (Twin Cave, Jones's "north entrance", Abu Saraj IV/11 and IV/17), and every dig at them with depth and result. A matrix, not a map. | S09, S10, S14, S15, S20 | [svg](search_06_entry25_column_cave.svg) · [png](png/search_06_entry25_column_cave.png) |
| 07 | Kh. Qumran: Allegro's four 1959–60 actions, de Vaux, Magen and Peleg, the 2009 probe, and the graves opened in 1874–1912, with Allegro's items 21–25 in his own numbering. Schematic plan, not to scale. | S02, S03, S17, S18 | [svg](search_07_qumran_searches.svg) · [png](png/search_07_qumran_searches.png) |
| 08 | Mount Gerizim: Bull's trenches at Tell er-Ras (to bedrock at about 7.6 m) and Magen's excavation of the main summit, with entry 57's wording as a label only. Schematic plan, not to scale. | S07, S08 | [svg](search_08_gerizim.svg) · [png](png/search_08_gerizim.png) |
| 09 | Cave 3 (3Q): where the copper rolls, the jars and the fragments lay, and what the 1952 and 1986 digs recorded. Schematic plan and section; the stated dimensions are to scale. | S01, S11 | [svg](search_09_cave3_find.svg) · [png](png/search_09_cave3_find.png) |
| 10 | All 27 ledger rows on one time axis, 1952–2017, by purpose and result, with counts checked against summary.json. | all | [svg](search_10_ledger_timeline.svg) · [png](png/search_10_ledger_timeline.png) |
| 11 | The Kidron monuments in Jerusalem: entries 48, 51, 52 and 54 as candidates, Allegro's dig at the Zechariah monument and the unfinished tomb, and his item numbers against the project's entries. Schematic, not to scale. | S03 | [svg](search_11_kidron_monuments.svg) · [png](png/search_11_kidron_monuments.png) |

## Main points

- **Sheet 01.** Only Cave 3 is said to have been dug out completely in 1952. For the other points the record gives contents, not how deep anyone dug. Patrich and Arubas's Cave 13 cannot be placed: their figure and text differ by about 0.4 km.
- **Sheets 02–03.** At Kh. Mird, only the monument and the tunnels were cleared with the scroll in mind, and neither has a published depth. The east-side "steps" of entry 1 (Allegro's item 1, the same lines) were only looked for. The monument was cleared round the base and through a section. No chamber or deposit was found, but the clearance depth is not stated. The ledger therefore does not treat S03 as a complete negative for the monument.
- **Sheet 04.** 25 of the 26 stated depths lie beyond the 0.46 m that the 1960 detectors reached. The median is 7 cubits (about 3.5 m). The deepest scroll-motivated digging with a figure is the Cave 13 pits (about 2.5 m, stopped as unsafe) and the Cypros shaft (about 6 m, not bottomed).
- **Sheet 05.** Of 39 candidate places, 4 have a ledger search, and 2 of those are "near" matches only. Only Kh. Qumran has a scroll-motivated search. 32 places have nothing in the ledger or the looks table, all 15 Jerusalem places among them. No look at any atlas place has a detection probability.
- **Sheet 06.** Twin Cave and Abu Saraj IV/17 each have a published pillar between two mouths; IV/11 has a pillar and one recorded opening. No dig at any candidate records a period northern threshold, so the text's three cubits has no starting point anywhere.
- **Sheet 07.** Allegro's party worked at four spots at Kh. Qumran in 1959–60. None has a depth, and two have no stated position. His three books report different work there (none in 1960, four actions in 1964, one trench in 1966).
- **Sheet 08.** Neither Gerizim campaign was a scroll search. No excavation is reported in the fosse south of Tell er-Ras, which Bull asked about as the scroll's "upper fosse" (1968 p. 59).
- **Sheet 09.** The documents in 3Q lay 0.30–0.40 m deep (ESI 6). DJD III and RB 60 disagree on where the jars lay and how many there were, and ESI 6 has the roof fall before the documents were placed, while de Vaux's account implies a block fell after the rolls were laid (inference).
- **Sheet 10.** 8 of 27 searches had a scroll-related purpose and 4 were aimed at a deposit. All 3 negative results are among them. 7 rows give a depth figure or say bedrock was reached.
- **Sheet 11.** The only recorded dig at the Kidron monuments is Allegro's, round the Zechariah monument and in the unfinished tomb south of it, with no depth or date. No source records a dig on the west side of Absalom's monument, where entry 48 says to dig.

## Sources

- Sheet 01: [devaux1952_cave_points](../../history/devaux1952_cave_points/README.md) (RB 60 pl. XX, digitized), [djd3_text_cave_list_extracted.md](../../history/djd3_text_cave_list_extracted.md) and [devaux1953_cave_list_extracted.md](../../history/devaux1953_cave_list_extracted.md).
- Sheets 02 and 03:
  - [wright_milik1961_el_mird_extracted.md](../../history/wright_milik1961_el_mird_extracted.md)
  - [allegro1964_treasure_2nd_ed_extracted.md](../../history/allegro1964_treasure_2nd_ed_extracted.md)
  - [allegro1966_search_in_the_desert_extracted.md](../../history/allegro1966_search_in_the_desert_extracted.md)
  - [haber_gutfeld2024_hyrcania_extracted.md](../../history/haber_gutfeld2024_hyrcania_extracted.md)
  - SRC-GUTFELD-2006 (abstract only) in the ledger's `sources.csv`.
- Sheet 04: `text/translation_en.json`, `atlas/app/atlas-data.json` and the ledger's `searches.csv`.
- Sheets 05–11: each script's docstring and footer list its sources with pages. The main ones are the ledger (`searches.csv`, `README.md`), `atlas/app/atlas-data.json`, `research/models/search_effectiveness/` (05), the entry-25 reviews, registrations and assessments (06), the Allegro extractions, Magen and Peleg and the PEF Quarterly Statement table (07), the NEAEHL extract and Bull via the ledger (08), DJD III, RB 60 and the ESI 6 review (09), and ASI Map 102 (11).

No published plan, plate or photograph is copied. The 1952 points are coordinates measured from the map, and the plate image is not in the repository. The monument plan is redrawn from the dimensions given in the text. It is not a copy of Wright's Fig. 4. Sheets 07, 08 and 09 used published plans in `research/assets/plans/` only for rough positions; nothing is traced.

## Rebuilding

- `python3 -I research/schematics/build.py` rebuilds these sheets with the entry schematics. To rebuild one sheet, run its script, for example `python3 -I research/schematics/searches/search_04_depths.py`.
- The builds are deterministic.
- Sheet 04 checks each "dig" phrase against the translation. It stops if the text changes, or if an entry with "dig" is not on the chart.
- Sheets 05–11 also read their data from the repo and stop on a mismatch: counts against `summary.json` (10), ledger fields and atlas candidates (05, 06, 08, 11), quoted phrases against the extractions (07, 08, 11).
- To re-render the PNGs, run `node render_png.mjs` from this folder. It needs Playwright and Pillow, and uses the same settings as the entry schematics: 1.5×, reduced to 256 colours.

Sheets 01–04 drawn 10 October 2026; sheets 05–11 drafted the same day by parallel agents from one brief and checked by render. The sheets add no identification, outcome or confidence change.
