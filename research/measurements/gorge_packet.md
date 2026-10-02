# Qumran gorge measurement packet

Prepared 2 October 2026 UTC for R01/R08. Repository baseline: `bb2fde4c76dbbe34b4c7345646acee049e875229`. This packet defines measurements and preserves prior recorded inputs. It adds zero primary-source targets, bounded checks, decisive tests or question closures.

## Readiness

Schulz 1960 Fig. 2 / p. 53 (capture p. 4) is a compass-oriented route sketch with approximate 100/100/500 m labels. The original image has no scale bar or survey control. A uniform pixel-to-metre transformation, measured route bearing or geographic registration would create unsupported precision.

Strobel 1972 Fig. 1 / p. 56 (capture p. 2) has a 0–20 m scale and north arrow. It covers the settlement, with a caption crediting de Vaux 1956. It supplies no upper-gorge control or common frame for A/B, the channel start, the boulder or Reeder's wall. Its settlement scale cannot calibrate the gorge photographs.

Existing original images and scalar observations support source-relative records. They currently prevent quantitative common-frame gorge tests. The missing inputs are measured control, identified endpoints and feature-specific chronology. Peleg's map and the pocket sheet remain parked; this packet initiates no retrieval for either.

Read-only visual audit repeated Schulz pp. 53–55 and Strobel Fig. 1 against extracted original capture images. These were previously counted inspections. Schulz p. 55 describes a curved tunnel, A opening south toward the side branch, and a total fall below 1 m over approximately 12 m. These details reinforce the need to record measurement path and vertical datum; they do not establish coordinates or a dated construction phase.

## Independent measurement jobs

**G01 — Long-tunnel traverse and endpoint audit.** Record west mouth, B exterior opening, B north-side floor gap, A exterior opening and east mouth as separate features. Define each point by a stable sill/floor/rock edge and photograph identifier. Measure horizontal coordinates, vertical levels and tunnel-centreline chainage on a shared local datum. Repeat critical endpoint picks and retain their observed spread. Deliver each distance as horizontal chord, horizontal centreline path and 3-D path; retain the distinction in every comparison. Published numbers provide an existing comparison: Schulz west→B ≈4.05 m, B→A ≈3 m, A→east 4.50 m; these yield ≈11.55 m only under a common path convention. Completion requires a documented traverse and a repeatable endpoint map. The source-relative result can remain inconclusive when old reference surfaces cannot be recovered.

**G02 — Individual-opening identity test.** Work independently from G01's numeric fit. Identify A and B using exterior/interior photographs, A's worked/plastered sill, B's natural fissure and bridging floor, and their order from the western mouth. Preserve the north-side floor gap as a separate observed opening. Compare the Magen–Peleg first/second break identifications after tracing their photographic or plan labels. The existing conditional offset comparison already records mixed agreement and a natural/artificial descriptive disagreement. Completion requires feature-specific correspondence with supporting and conflicting observations; similar chainage alone leaves identity unresolved. Schulz's original close-up plates remain unread in the supplied capture inventory.

**G03 — Channel-head to tunnel/boulder frame.** Identify the surviving upstream end in the northern side branch and specify whether it represents original intake, preserved channel limit, branch junction or later truncation. Keep these alternative anchors separate. Locate the small collecting basin, west tunnel mouth, A/B and any proposed boulder/wall on one local survey. Measure downstream channel-centreline distance from each head alternative to the west mouth and B; also preserve straight horizontal offsets. Schulz's approximately 31 m west-mouth-to-small-basin distance is a published route-relative comparison with an unspecified measurement convention. A/B-to-channel-start distances remain unmeasured. Completion requires a shared measured frame and endpoints; transferring a 100 m schematic segment supplies no such frame. Matching modern point 3 to the source's intake also needs independent feature identification.

**G04 — Reservoir-to-B directional test.** Identify each reservoir alternative independently: the approximately 1.10 × 1.00 m collecting basin, the large natural gorge basin and any other named-reservoir candidate. On a surveyed local frame, measure ΔE and ΔN from a defined reference boundary/point to B. Test a cardinal east-half-plane model (ΔE > 0) and any narrower east-sector interpretation separately; state the selected angular width and that it is a project assumption. Propagate the full endpoint uncertainty bounds. Report “direction unresolved” whenever the east-offset uncertainty spans zero or reservoir identity remains open. Complete the geometry subtest only after edition/readings and reservoir anchors are explicit. Geographic bearings need an independently tied north direction; a local arbitrary X axis cannot establish east.

**G05 — Hydraulic height and phase test.** Measure present basin floor, identifiable earlier floor/sediment contacts, channel bed, proposed dam/spillway crest and tunnel sill levels on one vertical datum. Preserve Strobel's reported 5–7 m channel-above-contemporary-floor difference as a dated observation of the surface he inspected. Compute gravity-supply feasibility for each explicitly reconstructed ponding scenario, including outlet and crest controls. Unknown ancient floor or crest levels remain unknown inputs. A proposed lifting installation needs its own physical evidence. Completion requires level differences plus phase-linked surfaces; modern levels alone answer only a modern geometric subquestion.

G01–G05 can proceed independently when their inputs become available. G02 may resolve identity without a full survey. G01/G03/G04 need a common measured local frame, and G05 adds vertical and phase controls. Each job must record whether it completed source extraction, a geometric subtest or a decisive candidate test.

## Calibration, uncertainty and reporting contract

Use source-native reported metres for scalar observations. Preserve terms such as “about” as qualitative uncertainty where the author gives no error bounds. Decimal typography supplies no survey accuracy. Do not turn an unknown standard error into zero or set an invented tolerance that makes the candidate pass.

For a measured plan, preserve the source file hash, exact image/page, crop rectangle and pixel dimensions. A metric scale supplies only the displayed plan conversion. Check at least two independently known directions or lengths before accepting isotropic calibration; scan stretch and camera perspective require their own controls. Record calibration residuals and leave geographic accuracy separate from relative plan accuracy. Current gorge illustrations fail this calibration gate.

For every distance record: source; exact endpoints; observation or reconstruction; source unit; horizontal chord / horizontal path / ground path / vertical depth; reference surface; north convention; phase; endpoint uncertainty; calibration uncertainty; and whether errors are correlated. For coordinates (E,N,Z), horizontal chord is sqrt(ΔE²+ΔN²); the 3-D chord is sqrt(ΔE²+ΔN²+ΔZ²). A curved path requires measured segment sums. Neither chord gives tunnel travel distance automatically.

The prior 0.95 m / 0.05 m / 0.85 m differences remain conditional arithmetic, with unknown path, endpoint and measurement errors. They supply no statistical agreement threshold. Report unknown uncertainty and preserve the descriptive conflict rather than declaring a numerical fit.

No first-century construction date follows from the modern survey. Keep reading, site association, individual feature identity, construction/use phase and geographic position as separate assessment fields. A decisive R01 result requires the relevant reading, identified features, geometry and phase; a successful survey may leave R01 open.

## Reusable record

`gorge_measurement_record.json` provides a minimal scalar-record template and current evidence inputs, with nullable calibration and uncertainty fields. It contains no executable pixel-measurement pipeline because the inspected gorge drawings have no valid metric image frame. Add source-space measurements only after their calibration gate passes.

## Sources and dependencies

- [Schulz 1960](https://www.jstor.org/stable/27930608), Fig. 2 / p. 53 and pp. 54–57. Supplied capture: `screencapture-jstor-org-stable-27930608-2026-10-01-18_59_28.pdf`; SHA-256 `113325858c68fb341d2942aca6fa136f89785626cf4567659160454301bdd773`. Original close-up plates remain unread.
- [Strobel 1972](https://www.jstor.org/stable/27930927), Fig. 1 / p. 56; gorge text pp. 65–68 and plates 7–10. Supplied capture: `screencapture-jstor-org-stable-27930927-2026-10-01-19_01_05.pdf`; SHA-256 `861c63c2ba96563c8644df8770b211dfc3be4cb1b10da04a92911d7b5f053ebb`. Repeated Schulz dimensions do not establish an independent survey.
- [Existing inspected-source review](https://github.com/quadrin/CopperScroll/blob/bb2fde4c76dbbe34b4c7345646acee049e875229/research/sources/qumran_supplied_originals_review_2026-10-01.md).
- [Existing machine-readable source observations](https://github.com/quadrin/CopperScroll/blob/bb2fde4c76dbbe34b4c7345646acee049e875229/registration/qumran_waterworks_originals_2026-10-01.json).

Ready output: measurement definitions and source-native scalar record. Pending output: new measured coordinates, calibrated gorge-image distances, individual-opening correspondence and construction-phase test. Counts stay unchanged.
