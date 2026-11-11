# Atlas candidate additions — 5 November 2026

The selected question is which of the November Drive reviews can supply useful Atlas candidate records and documented features. The result of this bounded pass is three additional locality records, seven entry-to-locality comparisons and eleven feature descriptions. Existing preferred candidates, confidence ratings and research test outcomes are retained.

## Sources inspected

- [Feshkha / Fasael entry assessment, 4 November](https://drive.google.com/file/d/1ODhkHAgeJhnci0sjQJGnueftHHr5Xj11/view).
- [Fasael reservoir identity and plan retrieval, 5 November](https://drive.google.com/file/d/1g2RDUEbxAAtDy-sT6pD-PpBL8LovkZ1_/view).
- [Cypros surviving cistern review](https://drive.google.com/file/d/1wfbP62366xistjCCuT5Joc7I7eOMl1g5/view) and [numbering correction](https://drive.google.com/file/d/1pwAVEquJTgKMB1Alm6tGXJenUNkaLnkk/view).
- Hirschfeld 2004, IEJ 54, pp. 56–62; Fig. 20 p. 58 inspected as a complete page image. Its 0–5 m scale, section levels and three adjoining spaces are visible. The original image is restricted and is not copied to this repository.
- [Hizmi 2016](https://www.ariel.ac.il/wp/judea-and-samaria-research-studies/wp-content/uploads/sites/144/2019/02/Hizmi.pdf), pp. *151–*156, Figs. 10–16. Direct text checked for reservoir dimensions, residence pool pair, courtyard dimensions, steps, columns and outlet. Detailed courtyard plan not recovered.
- Earlier project extraction: [de Vaux / Hirschfeld source review, 24 October](../sources/readings_2026-10-24/feshkha_devaux1959_hirschfeld2004_2026-10-24.md).

## Candidate decisions

| Locality | Entries | Basis | Outstanding relation |
| --- | --- | --- | --- |
| Ein Feshkha | 16, 55 | Connected basins, drains, stepped cells and twin feed mouths | Edition-dependent wording, route origin/destination, intended pair and ancient entrance datum |
| Fasael / Phasaelis | 3, 55 | Colonnaded bath courtyard with pool; separate residence immersion/reserve pair | Detailed plan, required wall/opening relation, common phase and intended pair |
| Cypros | 1, 17, 29 | Numbered cistern pairs, reported dimensions and descending steps | Achor relation, east-facing access, original floor, pair midpoint, inlet and side relations |

These are project comparisons. They do not identify a listed deposit, establish that treasure existed, or change a registered test result. The amount of source material is not a confidence measure.

Feshkha's several installations remain distinct. A jar described in the field notes as free in a pit is not a sealed cache. The short conduit does not establish a walkable passage. Excavator phase divisions and functional interpretations are attributed separately.

Hizmi reports nine courtyard columns, three on each side, surviving as bases; the complete distribution is unresolved. The town reservoir, bath courtyard, residence pool pair and upstream Fusail/Samsam reservoir are kept separate. The earlier and later summaries disagree on depth, wall thickness and relative position; the dossier retains those limits.

At Cypros, the triangular description is a cross-section. It cannot supply a triangular ground plan. Identification of the surviving third cistern as number 3 is ordinal inference; individual archive-photo and entrance matches remain provisional.

## Coordinates

All three WGS84 coordinates are locality display anchors. No individual opening, pool corner, wall or deposit receives an archaeological point.

- Feshkha: 31.7144, 35.4533, from the [Ein Feshkha locality record](https://en.wikipedia.org/wiki/Ein_Feshkha); project display precision approximately 300 m. The installation is unregistered.
- Fasael: 32.0275145, 35.443361, [Pleiades 688003](https://pleiades.stoa.org/places/688003) coordinate reproduced in [LACRIMALit](https://ontologia.fr/OTB/LACRIMALit-Ontology.htm). Direct Pleiades retrieval was blocked by its browser challenge; project display precision approximately 500 m. The individual installations are unregistered.
- Cypros: [PADIS archaeological project](https://sites.google.com/uniroma1.it/sapienza-padis-project/archaeological-sites/aqaba-tell-el-cypros), 31°50′39.14″ N, 35°25′36.44″ E, converted arithmetically to decimal degrees. Project display precision approximately 300 m, deliberately coarser than the printed decimals. This is the fortress anchor, not a numbered cistern mouth.

## Model scope

Feshkha now has a source-based display model of basin L142 and cells L119/L127, with their separate small pools, steps and hydraulic connection. Hirschfeld Fig. 20 (p. 58; PDF page 23) and Fig. 24 (p. 62; PDF page 27) were inspected directly. Simplified wall faces were sampled at Fig. 20’s 5 m bar, with reported basin dimensions and depths retained separately. Relative orientation follows the source arrow; placement at the locality anchor remains schematic. Wall tops, drawing thicknesses, stair tread runs, estimated relative cell-floor levels and the full connecting drain run are display assumptions. The two reconstructed lower steps into L119’s pool are omitted.

Fasael can support a dimension-based courtyard schematic; a measured reconstruction needs the missing plan. Cypros cannot yet support a measured cistern footprint.

The model is `feshkha-installation` in `atlas/app/atlas-site-plans.json` and `atlas/app/atlas-model-geometry.ts`. Its local terrain uses a 65 × 65 Mapterhorn grid over 800 m around the existing anchor; modern terrain supplies no ancient datum or registration. The source tile and receipt are archived in the existing terrain directories and mirrors.

The Java Edition 26.3 build uses 0.125 m blocks and was saved and read back through `atlas/scripts/minecraft/build-world.mjs`: 112 × 40 × 112 blocks, 5,145 fill commands, 364,953 blocks placed, 501,760 block positions checked, zero mismatches and zero missing saved sky-light values. The Atlas mesh is `atlas/public/minecraft/feshkha-installation.bin.gz`; the separate [saved world](../models/minecraft/feshkha-installation-26.3.zip) opens in creative mode above this build. It extends neither the existing combined-world archive nor the archaeological claims.

The additive input `atlas/research/candidate_additions_2026-11-05.json` is applied by `build_atlas.py`, so rebuilding retains all three sites and seven associations. Map Sources now exposes the same dossier sources and exact locators used by the complete site record. Existing status/confidence fields, candidates and locality records are retained. The earlier corpus review date remains separate from this bounded update.

## Review coverage

The Atlas's inherited review date and snapshot identify its earlier corpus-wide review. This pass updates only the candidate associations and dossiers listed above. It does not assert a new review of the other Atlas entries.

No protected source pages, photographs, credentials or private PDFs are included.

## Implementation checks

TypeScript and source-model checks passed. The Minecraft validation checks all 75 saved builds and preserves the existing block files and world strips. Desktop and phone browser checks passed for the three pins, site search, seven entry/locality deep links, all eleven dossier features, direct source links, Feshkha’s loaded block mesh, selectable plan features and eye-level walking. Candidate records survive rebuilding the data; inherited status, confidence and place records match the previous main revision.

The static app passed the pinned GitHub Jekyll Pages builder and payload checks (126.4 MiB, unchanged app-file bytes, resolving entrypoints, no research/private archive payload). The owner-private hosted build retains its separate private image packet and access settings. No additional restricted source page or photograph is included.
