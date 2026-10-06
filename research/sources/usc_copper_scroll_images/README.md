# USC Digital Library: Copper Scroll image index

`index.csv` lists every item in the **Copper Scroll** folder of the USC Digital Library (InscriptiFact collection, text 3Q15). There are 942 items. Each row has the catalog data, a link back to the item, and a detailed description of what the image shows.

The repository includes small JPEG thumbnails in `images/medium-res`, added at commit `16df396`. Despite that folder name, these are not medium-resolution previews. Native public item-page previews are now stored separately in `images/previews`. Follow `usc_link` to see the library's item page.

## Repository image coverage and larger-preview retrieval

On 4 October 2026, all 906 JPEGs in `images/medium-res` were decoded and matched by filename to `uc_identifier`: 612 facsimile photographs and 294 original-scroll photographs, with no missing photograph IDs or extra IDs. Every image is 192 pixels high; widths range from 93 to 288 pixels. The 36 RTI/PTM records are indexed but have no files in this JPEG set. The 50 files in `images/page-04` are byte-identical duplicates of files in `images/medium-res`.

`cuts_01_10_retrieval.csv` selects all 122 original-scroll photographs for candidate cuts 1–10: 100 recto and 22 verso images. It records the source item links, thumbnail paths, actual pixel dimensions and SHA-256 hashes. Cut numbers are candidate regions for the seven Greek-letter loci; this list does not establish precise line-to-cut registration.

All 122 selected public item-page previews were acquired on 4 October 2026: 100 recto and 22 verso. They are native JPEGs saved under `images/previews/cuts-01-10/` using each `uc_identifier` as the filename. Every image is 1000 pixels high; widths range from 482 to 799 pixels. No resampling, cropping or re-encoding was applied to the saved files. The set totals 8,275,644 bytes. No downloads remain failed.

`cuts_01_10_preview_manifest.csv` records every USC item URL, actual direct JPEG URL resolved from the displayed image, repository filename, decoded dimensions, byte size and SHA-256 hash. Direct preview URLs are signed CloudFront URLs and may expire; the USC item links are durable provenance. Each item was opened individually in Chrome, with requests spaced at least 20 seconds apart, and its title and unique identifier checked against the retrieval list. Files were decoded fully with Pillow, compared with the corresponding existing thumbnail, and reviewed visually in labelled contact sheets for cut and side consistency. Both dimensions exceed those of each corresponding thumbnail. Resizing was used only for validation copies: the largest mean absolute RGB difference from a thumbnail was 5.255 on the 0–255 scale.

The earlier acquisition reported six failures. Five were caused by dropping underscore suffixes from USC record IDs; the exact CSV URLs resolve those records correctly. The sixth succeeded in this spaced retry. One preview initially appeared after its page metadata; a delayed retry acquired it successfully. The earlier manifest's item links in the direct-image column have been replaced with actual image URLs for all 122 files. Full-resolution archival TIFFs were not acquired; the existing catalogue notes indicate that they require USC login. Public preview access does not grant publication permission.

### Remaining public previews — 5 October 2026

After [PR #9](https://github.com/quadrin/CopperScroll/pull/9) was merged, all 820 remaining indexed public previews were acquired: 784 photographs and 36 static RTI/PTM posters. The 172 additional original-scroll photographs cover cuts 11–23, with 144 recto and 28 verso images. Together with the earlier 122 files, every one of the 906 indexed photographs now has a native 1000-pixel-longest-side preview. All 36 RTI/PTM records have their smaller native JPEG poster; the interactive PTM data files were not acquired.

| New files | Coverage | Native width × height range (pixels) | Repository directory | Bytes |
|---|---|---|---|---|
| 612 | Facsimile photographs; columns 1–12 and indexed close-ups | 652–1000 × 667–1000; longest side 1000 | `images/previews/facsimile/` | 104,387,718 |
| 172 | Original-scroll photographs; cuts 11–23 | 509–1000 × 962–1000; longest side 1000 | `images/previews/original-scroll-remaining/` | 12,505,465 |
| 36 | Static RTI/PTM public posters | 334–512 × 321–512; longest side 512 | `images/previews/rti-public-previews/` | 1,256,265 |

The new files total 118,149,448 bytes. Filenames preserve each index `uc_identifier`. Saved JPEG bytes were copied from the browser exports without resampling, cropping or re-encoding. RTI posters retain the resolution already described in the index; no resolution upgrade is claimed for that group. The original 122 cut 1–10 previews were retained unchanged.

`remaining_preview_manifest.csv` contains all 820 records, including USC item URLs, exact signed direct image URLs, repository filenames, fully decoded dimensions, byte sizes, SHA-256 hashes and final acquisition status. It also records live catalog identifiers and titles. For all 36 RTI/PTM records, the JPEG preview-file identifier differs from the identifier displayed in the catalog metadata; some index titles abbreviate Top/Bottom. Both forms are recorded explicitly. The descriptive `index.csv`, including its original identifiers, observations and source credits, remains unchanged.

Each indexed item URL was opened individually in Chrome. USC navigations were spaced at least 20 seconds apart; later requests allowed 12 seconds of that interval for the viewer to load before export. Photograph titles and catalog identifiers were checked against the index. RTI titles were checked with their Top/Bottom abbreviations expanded, and exports were selected by the observed preview-file identifier. Every saved image decoded fully. Both dimensions of all 784 new photographs exceed the corresponding 192-pixel-high thumbnail. The largest mean absolute RGB difference after resizing a validation copy to its thumbnail was 6.382 on the 0–255 scale. All 820 previews were reviewed in 18 labelled contact sheets for catalog cut/side or column/section consistency. Contact sheets and comparison copies did not alter the saved files; existing catalog/tag caveats below remain applicable.

`remaining_preview_retry_log.csv` records observed loading/navigation interruptions and RTI identity discrepancies, with their resolutions. Sixteen photographs were initially missing after the main pass and were recovered with spaced retries. One required a further retry after another title-loading timeout. Final coverage is 820/820, with zero failed, missing or undecodable files.

Direct image URLs are expiring signed CloudFront links. The durable USC item URL and file hash identify the source and downloaded bytes after those links expire. Acquisition used the public item-page JPEGs; full-resolution archival TIFFs and PTM data files remain outside this acquisition. The existing catalog access notes indicate USC login is required for archival TIFFs. Public viewing and downloading leave the educational-use restriction and written publication-permission requirement in force.

This acquisition adds no engraving-order result, depth measurement, independent field observation, identification, confidence change or question closure. The original index descriptions and source credits are preserved; this task only acquires image assets.

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

The rights statements are in the `rights` column. West Semitic Research holds the rights to the digital images, and the Department of Antiquities, Jordan, holds the rights to the physical object. The catalog says the images are for educational use only and that requests to publish must go to West Semitic Research in writing. The index itself contains catalog data and original descriptions; the separately stored previews retain the source restrictions. Source credit: Photograph by Bruce and Kenneth Zuckerman, West Semitic Research, in collaboration with Princeton Theological Seminary. Courtesy the Department of Antiquities, Jordan.
