# Entry schematics

One schematic plan for each Copper Scroll entry the project has studied: 60 of the 61 entries. Entry 41 is too damaged to draw.

Each page shows **one arrangement the entry's text allows**. It is not a reconstruction of any real site. Candidate sites are named in the footer. Where a candidate setting is drawn, it sits in a small inset labelled "candidate setting (schematic)".

## How to read a page

- **Main panel:** follows the project's translation (`text/translation_en.json`). A badge says whose reading that is.
- **Direction:** north is up unless the page says otherwise. Each direction word in the text covers a 90° quarter. Where the text gives no direction, the page says that the orientation is arbitrary.
- **Deposits and measurements:** a red × marks each deposit, labelled with what is deposited and any digging depth. Measurements are in cubits, with a metre equivalent at about 0.5 m per cubit. Features are enlarged unless a scale bar says otherwise.
- **Side panels:** show only reading variants recorded in the repo (`text/readings.json`, the phase-5 assessments, research notes). Each names whose reading it is, and is badged as the project reading, an alternative, or not adopted. A panel headed "Readings that leave the plan unchanged" lists the variants that move only the name, the sum or the place.
- **Footer:**
  - the text quoted from the project translation;
  - the drawing choices;
  - the atlas placement;
  - what the archaeological records show (phase-5 assessments, feature constraints).
  Where the records are silent, it says "not recorded".

Assumptions the text does not fix are labelled on the drawing, for example where a distance is measured from or which corner is meant.

## Koḥlit, entries 11 and 60

These two entries share one sheet, drawn for the [approved rarity-count pre-registration](../preregistration/kohlit_rarity_2026-10-08.md):
- [entry_11_60_kohlit.svg](entry_11_60_kohlit.svg) ([png](png/entry_11_60_kohlit.png)) shows a site that meets the pre-registered conditions.
- [entry_11_60_kohlit_variants.svg](entry_11_60_kohlit_variants.svg) ([png](png/entry_11_60_kohlit_variants.png)) shows all 12 variants: the Milik and Puech openings, strict and loose graves, the pool outside or inside the site, the "buried" reading, the Janoaḥ reading, and Koḥlit as a district.

The other Koḥlit entries have their own pages: 4, 15, 16 and 19.

## Rebuilding

The scripts in `entries/` draw with the shared kit `lib/schematic.py`, which uses only the standard library. Run `python3 -I research/schematics/build.py` to rebuild every SVG. The build is deterministic. The one exception is `entry_11_60_kohlit.svg`, which was drawn by hand and has no script.

`png/` holds an image of every page. Each was rendered from its SVG with headless Chromium at 1.5× and reduced to 256 colours. After changing a script, run `node render_png.mjs` from this folder to re-render them; it needs Playwright and Pillow.

## Index

| Entry | Lines | Schematic | Files |
|---|---|---|---|
| 1 | I 1-4 | the ruin in the Valley of Achor | [entry_01.svg](entry_01.svg) · [png](png/entry_01.png) |
| 2 | I 5-6 | the funerary monument | [entry_02.svg](entry_02.svg) · [png](png/entry_02.png) |
| 3 | I 6-8 | the great cistern in the court of the peristyle | [entry_03.svg](entry_03.svg) · [png](png/entry_03.png) |
| 4 | I 9-12 | the mound of Koḥlit and the rock cleft of immersion | [entry_04.svg](entry_04.svg) · [png](png/entry_04.png) |
| 5 | I 13-15 | the pit of the foundry(?) of Manos | [entry_05.svg](entry_05.svg) · [png](png/entry_05.png) |
| 6 | II 1-2 | the cistern of ha-Melaḥ under the steps | [entry_06.svg](entry_06.svg) · [png](png/entry_06.png) |
| 7 | II 3-4 | the cave of the old House of Washing(?) | [entry_07.svg](entry_07.svg) · [png](png/entry_07.png) |
| 8 | II 5-6 | the underground chamber in the court of Mattiyah | [entry_08.svg](entry_08.svg) · [png](png/entry_08.png) |
| 9 | II 7-9 | the cistern opposite the East Gate | [entry_09.svg](entry_09.svg) · [png](png/entry_09.png) |
| 10 | II 10-12 | the cistern under the eastern wall | [entry_10.svg](entry_10.svg) · [png](png/entry_10.png) |
| 11 | II 13-15 | Koḥlit's pool (11) and the final pit (60): a qualifying site, plus all 12 variants | [entry_11_60_kohlit.svg](entry_11_60_kohlit.svg) · [png](png/entry_11_60_kohlit.png) |
| 12 | III 1-4 | the courtyard corner | [entry_12.svg](entry_12.svg) · [png](png/entry_12.png) |
| 12a | III 5-7 | the adjoining corner | [entry_12a.svg](entry_12a.svg) · [png](png/entry_12a.png) |
| 13 | III 8-10 | the Millo pit | [entry_13.svg](entry_13.svg) · [png](png/entry_13.png) |
| 14 | III 11-13 | the Millo tomb | [entry_14.svg](entry_14.svg) · [png](png/entry_14.png) |
| 15 | IV 1-2 | the great cistern in Koḥlit and its pillar | [entry_15.svg](entry_15.svg) · [png](png/entry_15.png) |
| 16 | IV 3-5 | the entering conduit | [entry_16.svg](entry_16.svg) · [png](png/entry_16.png) |
| 17 | IV 6-8 | the two domes(?) in the Valley of Achor | [entry_17.svg](entry_17.svg) · [png](png/entry_17.png) |
| 18 | IV 9-10 | the earth(?) pit at the edge of the ʿAṣla | [entry_18.svg](entry_18.svg) · [png](png/entry_18.png) |
| 19 | IV 11-12 | the eastern pit north of Koḥlit | [entry_19.svg](entry_19.svg) · [png](png/entry_19.png) |
| 20 | IV 13-14 | the cairn in the valley of Sekakah | [entry_20.svg](entry_20.svg) · [png](png/entry_20.png) |
| 21 | V 1-4 | the head of the water conduit of Sekakah | [entry_21.svg](entry_21.svg) · [png](png/entry_21.png) |
| 22 | V 5-7 | the fissure east of the Reservoir of Solomon | [entry_22.svg](entry_22.svg) · [png](png/entry_22.png) |
| 23 | V 8-11 | from the Trench of Solomon to the great heap | [entry_23.svg](entry_23.svg) · [png](png/entry_23.png) |
| 24 | V 12-14 | the tomb in the Wadi of the Vault | [entry_24.svg](entry_24.svg) · [png](png/entry_24.png) |
| 25 | VI 1-6 | the Cave of the Column | [entry_25.svg](entry_25.svg) · [png](png/entry_25.png) |
| 26 | VI 7-10 | the cave at the corner of the heap of stones | [entry_26.svg](entry_26.svg) · [png](png/entry_26.png) |
| 27 | VI 11-13 | the resting place of the Queen | [entry_27.svg](entry_27.svg) · [png](png/entry_27.png) |
| 28 | VI 14-VII 2 | the cairn at the ford of the High Priest | [entry_28.svg](entry_28.svg) · [png](png/entry_28.png) |
| 29 | VII 3-7 | the conduit and the great northern reservoir | [entry_29.svg](entry_29.svg) · [png](png/entry_29.png) |
| 30 | VII 8-10 | the cave next to the cool room of the House of Haqqoṣ | [entry_30.svg](entry_30.svg) · [png](png/entry_30.png) |
| 31 | VII 11-13 | under the eastern corner at Doq | [entry_31.svg](entry_31.svg) · [png](png/entry_31.png) |
| 32 | VII 14-16 | the mouth of the water outlet of Koziba | [entry_32.svg](entry_32.svg) · [png](png/entry_32.png) |
| 33 | VIII 1-3 | the conduit on the road east of the Treasury | [entry_33.svg](entry_33.svg) · [png](png/entry_33.png) |
| 34 | VIII 4-7 | the inscribed stone | [entry_34.svg](entry_34.svg) · [png](png/entry_34.png) |
| 35 | VIII 8-9 | Kidron: the cairn at the mouth of the gorge | [entry_35.svg](entry_35.svg) · [png](png/entry_35.png) |
| 36 | VIII 10-13 | Valley of Shaveh | [entry_36.svg](entry_36.svg) · [png](png/entry_36.png) |
| 37 | VIII 14-16 | Shaveh's irrigated land | [entry_37.svg](entry_37.svg) · [png](png/entry_37.png) |
| 38 | IX 1-3 | Netophah: the dovecote at the spring | [entry_38.svg](entry_38.svg) · [png](png/entry_38.png) |
| 39 | IX 4-6 | the chamber in the second terrace | [entry_39.svg](entry_39.svg) · [png](png/entry_39.png) |
| 40 | IX 7-9 | the chambers of Ḥoron, the chamber facing the Sea | [entry_40.svg](entry_40.svg) · [png](png/entry_40.png) |
| 41 | IX 10 | The damaged entry | not drawn: the entry's text is damaged |
| 42 | IX 11-13 | the waterfall near the bend of the conduit | [entry_42.svg](entry_42.svg) · [png](png/entry_42.png) |
| 43 | IX 14-16 | the pit north of the gorge of Beth Tamar | [entry_43.svg](entry_43.svg) · [png](png/entry_43.png) |
| 44 | IX 17 - X 2 | the dovecote in the fort's second upper storey | [entry_44.svg](entry_44.svg) · [png](png/entry_44.png) |
| 45 | X 3-4 | the ravine cistern | [entry_45.svg](entry_45.svg) · [png](png/entry_45.png) |
| 46 | X 5-7 | the reservoir in Beth ha-Kerem | [entry_46.svg](entry_46.svg) · [png](png/entry_46.png) |
| 47 | X 8-11 | the basin in the valley | [entry_47.svg](entry_47.svg) · [png](png/entry_47.png) |
| 48 | X 12-14 | Absalom's monument | [entry_48.svg](entry_48.svg) · [png](png/entry_48.png) |
| 49 | X 15-16 | the basin of the bathhouse (Siloam?) | [entry_49.svg](entry_49.svg) · [png](png/entry_49.png) |
| 50 | X 17 - XI 1 | the upper pool, at its four corners | [entry_50.svg](entry_50.svg) · [png](png/entry_50.png) |
| 51 | XI 2-4 | the tomb of Zadok, below the portico | [entry_51.svg](entry_51.svg) · [png](png/entry_51.png) |
| 52 | XI 5-7 | the rock opposite Zadok | [entry_52.svg](entry_52.svg) · [png](png/entry_52.png) |
| 53 | XI 8 | the gallery tomb | [entry_53.svg](entry_53.svg) · [png](png/entry_53.png) |
| 54 | XI 9-11 | the Jericho people's tomb | [entry_54.svg](entry_54.svg) · [png](png/entry_54.png) |
| 55 | XI 12-15 | the house of the two pools | [entry_55.svg](entry_55.svg) · [png](png/entry_55.png) |
| 56 | XI 16 - XII 3 | the burial chamber | [entry_56.svg](entry_56.svg) · [png](png/entry_56.png) |
| 57 | XII 4-5 | under the steps of the upper pit, Mount Gerizim | [entry_57.svg](entry_57.svg) · [png](png/entry_57.png) |
| 58 | XII 6-7 | at the mouth of the spring of Beth Sham | [entry_58.svg](entry_58.svg) · [png](png/entry_58.png) |
| 59 | XII 8-9 | the great drain of the cistern (Bezek?) | [entry_59.svg](entry_59.svg) · [png](png/entry_59.png) |
| 60 | XII 10-13 | Koḥlit's pool (11) and the final pit (60): a qualifying site, plus all 12 variants | [entry_11_60_kohlit.svg](entry_11_60_kohlit.svg) · [png](png/entry_11_60_kohlit.png) |

Drawn 8 October 2026. Eight parallel drafting agents worked from the repo's records using one brief and the shared kit. Every page was rendered and checked for layout. No new evidence was sought; the pages add no identification, outcome or confidence change.
