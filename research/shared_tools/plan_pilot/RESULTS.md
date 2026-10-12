# Published-dimension plan pilot result

9 October 2026 UTC / 8 October Los Angeles. Method: [frozen protocol](PROTOCOL.md); [selected coordinates and exposure log](SELECTION.md); [sealed predictions](predictions.json); [separate references](references.json); [machine-readable comparison](results.json). Source captions, links, original raster hashes and inspection scope are in the [paired figure manifest](../../assets/plans/published-dimension-pilot/figure_manifest.json).

The selected longer floor chords in both measurable plans exceed the frozen screening budget. The claim that every primary chord agrees within max(0.10 m, 5% of the prose dimension) is **rejected for these coordinate selections**. The third case remains unmeasurable under the rule requiring both spans. Field measurement accuracy is **not identifiable from available evidence**: physical endpoint equivalence and independent reference provenance remain unresolved.

| Plan and selected span | Scale-bar prediction | Report dimension | Absolute difference | Screening result |
| --- | ---: | ---: | ---: | --- |
| Dagesh L1, longer chord | 2.554 m | 2.8 m | 0.246 m (8.79%) | Outside 0.14 m budget |
| Dagesh L1, shorter chord | 2.353 m | 2.3 m | 0.053 m (2.29%) | Within 0.115 m budget |
| Migdal L32, longer chord | 4.315 m | c. 4 m | 0.315 m (7.87%) | Outside 0.20 m budget |
| Migdal L32, shorter chord | 3.569 m | c. 4 m | 0.431 m (10.78%) | Outside 0.20 m budget |
| 'Etri Z2 | Primary unmeasurable | c. 4.8 × 4.8 m | Not graded | Missing second endpoint |

The one available 'Etri chord is 5.074 m. It is retained in the prediction file and receives no primary screening flag because the longer full-floor span cannot be determined.

## Source and datum limits

[Haimi, Horbat Dagesh, HA-ESI 128 (2016), Figure 2](https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=25151): the winepress paragraph reports L1 floor dimensions. Closely spaced floor and cut-lip lines make their equivalence to the selected internal chords uncertain. No endpoint definition or rounding error accompanies the prose dimensions.

[Mokary, Migdal Ha-'Emeq (A), HA-ESI 135 (2023), Figure 3](https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=26364): Area A, Winepress 1 describes L32 as approximately square. The drawing separates some upper-cut and interior-floor edges, and the interior is irregular. Approximately square prose dimensions do not specify the mid-floor chords used here.

[Zissu, Ganor and Neugeborn, Horbat 'Etri, HA-ESI 122 (2010), Figure 8](https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=1572&mag_id=117): the Winepress Z2 paragraph gives approximately square dimensions and notes poor preservation. The plan lacks a reliably identifiable southern full-floor boundary for the perpendicular chord. The press-channel edge supplies no replacement endpoint.

These HTML reports have no assigned printed or PDF pages; paragraph and figure locators are preserved without inventing page numbers. Figure rasters remain local, with original download URLs and hashes in the manifest, because redistribution permission is unestablished.

## Interpretation

This pilot adds new measured documentary discrepancies. It does not estimate a universal percentage error. The sample is small and selected for access; all three plans depict rock-cut floors, and the approximate or irregular boundaries remain a substantial source of uncertainty. A 5% budget is a chosen screening threshold, not a result derived from these errors.

The 2-pixel endpoint sensitivity calculation bounds only the chosen raster points. It excludes source distortion, drafting accuracy, upper-edge versus floor-toe choices, damaged boundaries, prose rounding and field uncertainty. The disagreement in the longer chords exceeds that narrow sensitivity interval, but the remaining causes cannot be separated by this dataset.

Prediction inputs exclude the report dimensions. The analyst saw those dimensions before choosing points and made approximate visual estimates, so the experiment does not supply a blind analyst or independent holdout result. Point selections and predictions were committed before the separate reference file was loaded for grading; endpoints were not adjusted afterwards.

The next independent accuracy benchmark needs plans with explicitly documented survey spans and endpoints, plus an observer who has not seen the answers. Until then, preserve floor/cut-edge alternatives as separate observations and leave unsupported spans unknown. No global correction factor follows from this pilot.

## Reproduction and stopping rule

Use the commands in the [shared-tools README](../README.md). `benchmark` recalculates both the predictions and grading and verifies their input hashes. The source images can be reacquired from the manifest URLs and checked against the recorded original hashes.

This screening test is closed for these inputs. Reopen only for a documented coordinate/scale error, a newly legible boundary or independently established endpoint/reference information. A new observer or source plan defines a new benchmark and preserves this result.
