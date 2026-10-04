# USC Digital Library: Copper Scroll image index

`index.csv` lists every item in the **Copper Scroll** folder of the USC Digital Library (InscriptiFact collection, text 3Q15). There are 942 items. Each row has the catalog data, a link back to the item, and a detailed description of what the image shows.

**The images themselves are not in this repo.** Follow `usc_link` to see an item.

## What is in the folder

| Count | Item type | What it is |
|---|---|---|
| 612 | facsimile RTI capture | 2013 colour photos of the metal facsimile of the scroll. West Semitic Research shot each column (and Top/Bottom close-ups) many times for RTI, with the light at a different angle in each shot. `column`, `section` and `rti_shot` come from the title. |
| 294 | original cut segment | 1988 film photos of the real scroll's cut segments, taken by Bruce and Kenneth Zuckerman and drum-scanned. Each segment was shot recto and verso, under light from named directions, in colour or black-and-white negative. `cut`, `side`, `lighting_as_titled` and `film` come from the title. |
| 36 | RTI/PTM data file | Lighting-model files for the facsimile columns. Only a small preview is shown, and some catalog fields are empty. |

## Columns

- **Identity:** `order` (position in the folder listing), `usc_record_id`, `uc_identifier`, `title`, `item_type`, the fields parsed from the title, `usc_link`
- **Catalog:** `date_created`, `creator`, `format`, `place`, `catalog_description`, `rights`. Copied from each item's page.
- **Visual description**, written from the library's public preview of each item (about 1000 px; previews for the RTI files are smaller):
  - `preview_px`: size of the preview that was examined
  - `region_shown`: the part of the object that is in frame, and the framing
  - `text_visible`: line counts, letter size against the scale, legibility and damage. There is **no transcription**.
  - `light_direction_observed`: the direction the light appears to come from, and the evidence. For cut photos this is compared with the light named in the title.
  - `physical_features`: cracks, seams, cut edges, holes, corrosion and missing areas
  - `reference_objects`: scale bars, the red calibration sphere, grey and colour charts, and handwritten tags
  - `background_setup`: what the object rests on and what else is in frame
  - `photographic_qualities`: colour, exposure, contrast, sharpness and grain
  - `detailed_description`: 180–260 words of prose per item

## Method and caveats

- Each item was opened and described individually on 3–4 October 2026, from anonymous access to the library. The full-resolution TIFFs need a USC login and were not examined.
- Light direction is hard to judge on full-column facsimile shots that have no calibration sphere in frame. Those rows say "appears", "uncertain" or "unclear".
- On many 1988 cut photos the handwritten "light" tag sits somewhere other than the position named in the title. The rows flag these mismatches; they were not resolved.
- Descriptions are visual observations, not readings of the text. For readings, use the editions.

## Rights

The rights statements are in the `rights` column. West Semitic Research holds the rights to the digital images, and the Department of Antiquities, Jordan, holds the rights to the physical object. The catalog says the images are for educational use only and that requests to publish must go to West Semitic Research in writing. This index contains only catalog data and original descriptions, and no image content.
