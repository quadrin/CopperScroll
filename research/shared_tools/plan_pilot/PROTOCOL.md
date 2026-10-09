# Published-dimension plan pilot

Frozen before point selection on 9 October 2026 UTC / 8 October Los Angeles.

## Claim and sample

Test whether scale-bar measurements of three newly sourced excavation plans agree with the dimensions in their reports. This is a convenience sample and a documentary agreement test. Independent field accuracy remains untested: the reports do not establish that the prose dimensions were measured independently of the drawings.

The source search exposed the analyst to the prose dimensions before point selection. The measurement program receives scale length and pixel coordinates only; reference dimensions are stored separately and loaded only for grading. This is program-level answer separation, not a blind analyst experiment or an unused archaeological prediction.

Retain these three cases, including failures or unmeasurable targets. No substitutions after seeing errors:

- Yoram Haimi, *Horbat Dagesh*, HA-ESI 128 (2016), report 25151, Figure 2, treading floor L1.
- Abdallah Mokary, *Migdal Ha-'Emeq (A)*, HA-ESI 135 (2023), report 26364, Figure 3, treading floor L32.
- Boaz Zissu and Amir Ganor, *Horbat 'Etri*, HA-ESI 122 (2010), report 1572, Figure 8, winepress Z2 treading floor.

Report locators are figure numbers and named paragraphs; these HTML articles have no assigned printed or PDF pages. The last report's author metadata will be checked before final attribution.

## Measurement rule

Use the original downloaded figure raster without stretching or resampling. Pixel origin is its top-left corner; x increases rightward and y downward. Calibrate isotropically from the printed scale bar's outer ticks. Do not calibrate from any reported target dimension or fit a correction to the answers.

Pick two approximately perpendicular chords through the middle of the treading-floor outline, parallel to its two principal sides, ending at the drawn internal floor boundary. Ignore internal press bases or channels. Record ambiguity, preservation and whether the floor toe can be distinguished from the upper cut edge. Preserve those picks before calculating target lengths. The larger chord is the primary target; the smaller is a diagnostic. Compare to the larger and smaller prose dimensions respectively, since prose gives no axis convention. Do not retune endpoints after grading. If the boundary cannot be selected, retain the case as unmeasurable.

Prediction: pixel chord length multiplied by scale metres / scale pixel length. Also calculate a digitization-only sensitivity interval using a 2-pixel radius around each selected endpoint; each distance can change by at most 4 pixels. This interval excludes drafting error, source distortion, irregular geometry, datum mismatch, prose rounding and field uncertainty.

For a screening flag only, use an absolute error budget of max(0.10 m, 5% of the prose reference). This is a chosen pilot budget, not an established archaeological tolerance or a confidence interval. Retain every primary and diagnostic error. Unsupported physical equivalence remains a limitation even when a numerical flag passes.

## Exposure and reproducibility

Commit this protocol and the measurement program before picking coordinates. Commit the selected coordinates before generating predictions. Save predictions and their input hash before the grading program opens the separate reference file. Record source URL, original raster hash/dimensions, caption, scale, north-arrow convention, download date, inspection scope and reuse status in the paired figure manifest. Source rasters remain local because no redistribution permission has been established; the repository retains links and original project coordinate selections.

The result can support only agreement with the specified published dimensions under this protocol. It cannot establish site identity, ancient surfaces, survey precision, geographic registration, true bearings or letter-reading accuracy.
