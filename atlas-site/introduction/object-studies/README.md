# Realistic object studies and references

The current introduction uses material-rich cutout renders for generic explanatory objects. Measurements, routes, highlights and source-plan annotations remain editable SVG geometry.

Two subjects deliberately use documentary references rather than generated substitutes:

- **Copper Scroll:** the existing original photograph of strip 13 by Osama Shukir Muhammed Amin (2020), CC BY-SA 4.0. The displayed viewport is a detail crop of that photograph, not an invented complete scroll or newly reconstructed inscription.
- **Second Temple:** Berthold Werner, *Jerusalem Modell BW 3.JPG*, public domain, photographed at the Israel Museum. This is a photograph of the Holyland Model's **modern reconstruction**, not the ancient building itself or proof of the inventory's ownership. The displayed viewport focuses on the Temple.

`app/atlas-intro-study-references.json` records these overrides. `prepare-atlas-object-studies.py` preserves them instead of regenerating these subjects. Their rejected generic render files are absent from this folder.

The remaining cave, jar, parchment, courtyard, soil, terrain and silver images are generated illustrations. They do not identify a particular excavated object, site, cave mouth, historical building or deposit. The courtyard is not a reconstruction of Qumran. Source photographs, radiographs and site plans elsewhere in the page remain separate evidence.

The generated sheet remains unchanged in the chat's generated-image workspace. The pipeline extracts its cells and encodes WebP files, clearing only sub-visible alpha fringe below 3/255. It does not trace or smooth away the material texture. `provenance.json` records its hash, references and framing. Standalone SVG symbols under `../icons/` belong to the earlier design and are not the current object treatment.
