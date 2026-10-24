# Method 1 extraction test: coding schema (frozen before the blind run)

Fixed 2026-10-23. The feature types and the dated_in_window rule are copied unchanged from the repository's frozen HA-ESI search plan (haesi_features_search_plan_v1, SHA-256 eb6a1de4…e807e9). The same schema is used by the model and by the human coder.

## Unit of coding

One row per feature, or per group of features that the report itself describes together with the same values ("three cisterns, each c. 2 m deep" = one row, count 3). Features with different stated values get separate rows.

## Feature types (code exactly one)

| code | includes |
|---|---|
| cistern | cistern, bell-shaped pit, water pit |
| pool_reservoir | pool, reservoir, water basin, dam |
| channel_aqueduct | channel, conduit, aqueduct, pipe, water tunnel, drain |
| ritual_bath | ritual bath, miqveh |
| rockcut_installation | rock-cut installation, winepress, oil press, press, quarry, cupmark, columbarium, rock-cut basin or pit |
| tomb_burial_cave | tomb, burial cave, grave, kokhim, loculi, ossuary, cemetery, sarcophagus, cist grave |
| cave_with_finds | a cave that is not a tomb, with finds |
| wall_tower | city or fortification wall, enclosure wall, terrace or field wall, tower, fortress, fort. Walls inside an excavated building are NOT coded unless the report names the wall as a feature in its own right (fortification, enclosure, terrace, field, dam or boundary wall). |
| hoard_cache | hoard, cache, hidden vessels, hidden deposit |

Anything else (buildings, kilns, floors, pottery, etc.) is not coded.

## Fields

| field | what to write |
|---|---|
| report | the report number (file name) |
| feature_type | one code from the table |
| label | the report's own name for it, e.g. "Cistern L105", "Tomb 2" (blank if none) |
| count | how many features the row covers, as the report states |
| period_as_given | the report's own words for the feature's date (blank if the report does not date the feature itself) |
| dated_in_window | yes: the report dates the feature itself to the Hasmonean, Herodian, Early Roman, Late Hellenistic, Second Temple or Bar Kokhba period, the 1st c. BCE, the 1st c. CE, or up to 135 CE, or says it was in use then. no: dated only outside that window. unknown: undated, dated only by the site's general periods, or by a range that only partly overlaps (e.g. "Hellenistic", "Roman", "Hellenistic–Roman"). |
| size_as_given | the dimensions the text states for the feature, verbatim with units (e.g. "2.5 × 3.1 m"). Blank if the text states none. |
| depth_as_given | the depth or height the text states, verbatim with units. Blank if none. |
| location_as_given | the area, square, locus or map reference the text gives for the feature (blank if none) |
| quote | verbatim from the report, 12 words or fewer, that shows the feature exists |

## Rules

- Never write a value the text does not state. Do not read sizes off figures or estimate them; do not convert units; do not date a feature from the site's overall periods. A blank is a correct answer when the text is silent.
- Use only the report text. Figures, captions not in the text, and outside knowledge are not used.
