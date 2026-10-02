# IV/17 independent manual repeat — 2026-10-02

The independently picked point measurements fall inside the pilot's declared width, outward-normal and separation envelopes. This supports the limited claim that the pilot's plan-relative raster measurements can be reproduced. Envelope overlap does not validate the ancient spatial interpretation or identify an exact location.

Source: Sion, *Atiqot* 41 part 1 (2002), Hebrew printed p. 63, Plan 5, Cave IV/17; PDF page 21. The inspected PDF SHA256 is `7b56f84d7f87d7ad16f5f707739fb6f91b9193dafb11756d860324d69a7ca718`. The reused source render is `tmp/parallel-measurements/iv17-work/plan5-crop.png` (626 × 541 px), SHA256 `59c490eb83e918b09be1d9bdcb8a4809a08401d54988f5c9fc6028d803deb044`. After the freeze, pilot metadata identifies PyMuPDF Matrix(3,3), page raster 1526 × 2438 px and crop [152,207,778,748]. Coordinates below refer to crop pixels, x right and y down. Source images remain outside Git. This is a repeated measurement of the existing primary-source plan, not a newly discovered primary source.

I inspected the original crop and an enlarged crop of the left entrance, selected coordinates manually and froze `iv17_repeat.json` before reading the pilot JSON or recomputed values. Raw file SHA256 is `15579fd41e2fcfebd2ea06cf1f5ffe138ec94909fed2110fda73e8700d1b5b5f`. Its filesystem modification time was 2026-10-02 05:40:28.472118 UTC; the first tool command that read the pilot ran at 05:40:33 UTC. The hand-entered `frozen_utc` value of 05:42:00 is erroneous and remains unchanged to preserve the frozen record. Tool ordering and file mtime support the before/after claim.

The raw feature keys mistakenly named the left opening “northern” and the right opening “southern.” The drawn north arrow makes the right opening geographically northern. I corrected this classification after comparison, while preserving every frozen coordinate. The blind independence applies to endpoint picks; the corrected geographic labels are an audited post-freeze interpretation. Exact AGENTS.md at commit `4a6c4434ff86f213aa2471351707ef2e8d7ab663` was read through the connector; the stale local repository was not edited.

| Physical feature | Frozen key | Correct interpretation | Frozen chord endpoints |
|---|---|---|---|
| Left, partly blocked by masonry | `northern_clear_mouth` | Southern remaining present gap | [258,398] to [319,375] |
| Right, clear opening | `southern_present_gap` | Northern present aperture | [548,386] to [502,400] |

The left chord runs from the far clear end of the block wall to the southwestern tip of the central hatched pillar. The right chord runs from the mid-thickness eastern cave wall end to the mid-thickness easternmost pillar tip. The outside is below each chord, on the entrance marker's tail side. Raw outward-side points [300,421] and [537,431] choose the normal's sign. The scale ends [402,472] and [570,472] represent 3 m, giving 0.017857 m/px. North-arrow tail [99,147] and tip [169,64] were selected independently.

| Measurement | Independent point result | Pilot unrounded result | Pilot envelope | Comparison |
|---|---:|---:|---:|---|
| Right / northern aperture chord | 0.859 m | 0.849 m | 0.6–1.1 m | Inside envelope |
| Right / northern outward chord-normal proxy | 122.9° | 125.6° | 101–151° | Inside envelope |
| Left / southern remaining gap chord | 1.164 m | 1.197 m | 0.9–1.5 m | Inside envelope |
| Left / southern outward chord-normal proxy | 119.2° | 122.9° | 103–143° | Inside envelope |
| Gap midpoint separation | 4.225 m | 4.227 m | 3.8–4.6 m | Inside envelope |
| Southern-to-northern midpoint bearing | 51.4° | 54.6° | No bearing envelope supplied | Difference −3.2° |

Relative to the drawn north arrow, the independently selected northern midpoint is 2.634 m north and 3.303 m east of the southern midpoint. Bearings are degrees clockwise from that arrow; true, grid or magnetic north is unspecified. Display decimals allow audit and do not imply equivalent archaeological precision.

The raw annotation assigned ±2 px to each scale and north-arrow endpoint, ±5 px to each coordinate of the ragged left opening and ±6 px to the right wall-end/pillar-tip definition. Corner perturbations produce non-statistical sensitivity ranges of 0.918–1.432 m and 104.0–132.4° for the left opening, and 0.594–1.163 m and 99.5–140.8° for the right opening. The latter range extends slightly outside the pilot width and lower-bearing bounds; the repeats agree at their point estimates and broadly overlapping sensitivities, without demonstrating that the pilot envelopes capture every reasonable endpoint convention. Scan distortion and north-reference systematics remain unquantified.

Completion: one independent raster endpoint-picking repeat and a reproducible computation are complete. Source phase, ancient northern threshold, pre-wall southern mouth, passage-axis orientation, deposit geometry and geographic registration remain unresolved. An outward chord normal is only a two-dimensional opening-facing proxy. The southern width measures the gap still visible beside the built wall, not an ancient full mouth. This repeated use of the same plan is not independent archaeological corroboration, does not close the site-identification question and supports no exact-location or new-primary-source claim.

Artifacts: unchanged raw picks `iv17_repeat.json`, computation `iv17_repeat_compute.py`, derived metrics and audit `iv17_repeat_results.json`, and this report. All are under `tmp/measurement-cycle2`; no repository edits or pushes, Library operations or outside communications were performed.
