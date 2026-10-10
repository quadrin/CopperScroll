# Past-search schematics

These sheets draw **past searches and survey records**, not scroll entries. They sit beside the [entry schematics](../README.md) and use the same drawing kit (`../lib/schematic.py`). Each sheet draws on the search ledger ([salvage_records](../../history/salvage_records/README.md)) and the source extractions in `research/history/`.

A sheet shows what a source says was looked at, dug or reached, and where. It does not say that any deposit is or is not at a place.

## How to read a sheet

- **Blue** = dug, cleared or reached, with who and when.
- **Red** = the scroll's own wording, or the depths it states.
- **Grey** = not recorded, or not dug.
- **Ochre dashed** (sheet 02 only) = looked at or measured, not dug.
- A sheet is drawn to scale only where it says so. Elsewhere it is a schematic arrangement, and the distances the sources give are written on the drawing.
- Each footer has four parts: the sources, how the sheet was drawn, what it shows and what it does not show.

## Index

| Sheet | What it shows | Ledger rows | Files |
|---|---|---|---|
| 01 | The March 1952 cliff survey around Cave 3. Survey points plotted to scale on the Palestine grid (from de Vaux's 1953 map, about ±30 m), with what DJD III records at each. | S01 | [svg](search_01_qumran_caves_1952.svg) · [png](png/search_01_qumran_caves_1952.png) |
| 02 | Kh. Mird (Hyrcania): what each campaign from 1952 to 2023 looked at or dug. Schematic plan, not to scale, with a timeline. | S03 (the 1962–63, 2000–04 and 2023 work is not yet in the ledger) | [svg](search_02_mird_hyrcania.svg) · [png](png/search_02_mird_hyrcania.png) |
| 03 | The "monument" SW of Kh. Mird, Allegro's candidate for his item 2: a plan to scale from the stated dimensions, and a schematic section showing what the April 1960 clearance examined. | S03 | [svg](search_03_mird_monument.svg) · [png](png/search_03_mird_monument.png) |
| 04 | Every "dig N cubits" in the project translation (26 entries) against the depths the ledger's searches reached. Depth axis to scale. | S01, S03, S07, S09, S11, S13 | [svg](search_04_depths.svg) · [png](png/search_04_depths.png) |

## Main points

- **Sheet 01.** Only Cave 3 is said to have been dug out completely in 1952. For the other points the record gives contents, not how deep anyone dug. Patrich and Arubas's Cave 13 cannot be placed: their figure and text differ by about 0.4 km.
- **Sheets 02–03.** At Kh. Mird, only the monument and the tunnels were cleared with the scroll in mind, and neither has a published depth. The east-side "steps" of entry 1 were only looked for. The monument was cleared round the base and through a section. No chamber or deposit was found, but the clearance depth is not stated. The ledger therefore does not treat S03 as a complete negative for the monument.
- **Sheet 04.** 25 of the 26 stated depths lie beyond the 0.46 m that the 1960 detectors reached. The median is 7 cubits (about 3.5 m). The deepest scroll-motivated digging with a figure is the Cave 13 pits (about 2.5 m, stopped as unsafe) and the Cypros shaft (about 6 m, not bottomed).

## Sources

- Sheet 01: [devaux1952_cave_points](../../history/devaux1952_cave_points/README.md) (RB 60 pl. XX, digitized), [djd3_text_cave_list_extracted.md](../../history/djd3_text_cave_list_extracted.md) and [devaux1953_cave_list_extracted.md](../../history/devaux1953_cave_list_extracted.md).
- Sheets 02 and 03:
  - [wright_milik1961_el_mird_extracted.md](../../history/wright_milik1961_el_mird_extracted.md)
  - [allegro1964_treasure_2nd_ed_extracted.md](../../history/allegro1964_treasure_2nd_ed_extracted.md)
  - [allegro1966_search_in_the_desert_extracted.md](../../history/allegro1966_search_in_the_desert_extracted.md)
  - [haber_gutfeld2024_hyrcania_extracted.md](../../history/haber_gutfeld2024_hyrcania_extracted.md)
  - SRC-GUTFELD-2006 (abstract only) in the ledger's `sources.csv`.
- Sheet 04: `text/translation_en.json`, `atlas/app/atlas-data.json` and the ledger's `searches.csv`.

No published plan, plate or photograph is copied. The 1952 points are coordinates measured from the map, and the plate image is not in the repository. The monument plan is redrawn from the dimensions given in the text. It is not a copy of Wright's Fig. 4.

## Rebuilding

- `python3 -I research/schematics/build.py` rebuilds these sheets with the entry schematics. To rebuild one sheet, run its script, for example `python3 -I research/schematics/searches/search_04_depths.py`.
- The builds are deterministic.
- Sheet 04 checks each "dig" phrase against the translation. It stops if the text changes, or if an entry with "dig" is not on the chart.
- To re-render the PNGs, run `node render_png.mjs` from this folder. It needs Playwright and Pillow, and uses the same settings as the entry schematics: 1.5×, reduced to 256 colours.

Drawn 10 October 2026. The sheets add no identification, outcome or confidence change.
