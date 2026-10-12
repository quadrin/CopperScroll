# What the present measurements can distinguish

Obtained: an entry-specific, reproducible resolution dataset from exposed plan records and the two measurement/recovery pilots. This is a derived exploratory analysis. It obtains no new pixels, field dimensions, ancient datum or reserved observation. The [pinned source manifest](source_manifest.json), [inputs](inputs.json), [runner](assessment.py) and [complete results](results.json) preserve the underlying choices and failures.

The present plan measurements can reproduce selected source geometry, and sometimes exclude a particular drawing model. They cannot yet decide the ancient cubit-scale comparisons. Missing physical endpoints, ancient surfaces and source error bounds prevent those conclusions even when a raster measurement looks precise.

## Resolution model

Use bounded intervals rather than estimated statistical errors: the record contains no calibrated distributions or field covariance. A chord with pixel length D, scale bar P pixels for S metres, radial chord-endpoint allowance r and bar-endpoint allowance e lies within `S × [max(0,D−2r)/(P+2e), (D+2r)/(P−2e)]`, provided `P>2e`. This reproduces PR31's picking-only sensitivity. It omits drafting, anisotropic distortion, physical endpoint equivalence, phase and field survey error.

Two scalar prediction windows with centres separated by G and equal half-width E are disjoint only when `2E<G`. Equality leaves them touching. The tabulated ceilings are requirements for disjoint conditional windows, rather than estimates that the present evidence meets them. Additional uncertainty in the datum shifts the predicted target; an unknown datum remains null and receives no invented interval.

For a same-plan pair, a shared translation cancels. A shared rigid rotation preserves scalar length but changes bearing and east/north components. Uniform scale survives: `|sR(q−p)|=s|q−p|`. An affine or locally distorted drawing needs a differential linear/source-error bound over that pair. Control RMS and one withheld check measure residuals at their selected locations; they cannot partition translation, rotation, scale or local distortion, establish their covariance, or calibrate a confidence interval. The bounded helper includes scale, radial endpoint, pair-local distortion and datum terms only when every required component is explicitly supplied. Unknown terms produce null.

## Entry-specific consequences

**Entry 25, IV/17.** The exposed repeat retains northern chord 0.859 m, southern remaining gap 1.164 m and midpoint separation 4.225 m. These are source-relative geometry. The northern facing proxy's 99.5°–140.8° endpoint sensitivity crosses the primary 135° sector boundary; its central 122.9° value has only 12.1° to that boundary before north-convention, distortion and phase questions. An outward chord-normal remains distinct from a passage axis and three-dimensional face. The southern ancient mouth and northern ancient threshold are unresolved. This audit does not score Plan 5 under the later frozen aspect rules, which explicitly exclude exposed records.

The three-cubit conditional depth is 1.20–1.80 m over the legacy 0.40–0.60 m/cubit continuum. Fixed illustrative units 0.445, 0.500 and 0.525 m predict 1.335, 1.500 and 1.575 m. Disjoint equal-width windows for the closest pair need half-width strictly below **0.0375 m**; the extreme pair needs below **0.120 m**. One-centimetre changes in cubit length would need below **0.015 m**. Neither the horizontal opening-width repeat nor its overlap supplies the missing vertical datum or that total accuracy.

**Entries 11 and 26.** The inherited four- and nine-cubit branches give 1.60–2.40 and 3.60–5.40 m. For fixed 0.500/0.525 m units, equal-window ceilings are **0.0500 m** and **0.1125 m**, respectively. Their ancient reference surfaces, axes and total errors remain unavailable. These are conditional acquisition requirements and do not select a local cubit or a textual variant.

**Entry 29, A(C)94.** The existing stress-envelope maximum for the drawn terminus is **9.241453 m**. Preserving its plan-level miss needs additional upper-distance uncertainty below **0.358547 m** against 24 cubits' 9.6 m minimum, or below **1.558547 m** against 27 cubits' 10.8 m minimum. Equivalent purely multiplicative sensitivities are below **3.8798%** and **16.8647%**, respectively. They supplement the existing picking envelope; they do not measure actual error. The report/drawn east-inner trace already differs by 0.481907 m (5.4762% of the reported 8.8 m length), with unestablished endpoint/elevation equivalence.

As illustrative sensitivities only, widening the terminus stress upper bound by that discrepancy magnitude reaches 9.747535 m; Dagesh's 8.79% documentary mismatch reaches 10.053770 m and Migdal's 7.87% reaches 9.968715 m. Each erases the 24-cubit envelope gap in that scenario. None estimates A(C)94's survey error, proves an actual perturbed fit, or licenses changing its scale. The 27-cubit gap survives these particular scenarios, while its archaeological exclusion remains unsupported because total source, aperture, wall-face, axis and phase errors are unknown. Preserve the existing numerical drawing failures and closed archaeological result.

The two free-unit numeral bands, 9.6–14.4 m and 10.8–16.2 m, overlap **10.8–14.4 m**. A length inside that overlap cannot distinguish 24 from 27 under these unit alternatives even with perfect geometry. Outside the overlap a sufficiently defined length can exclude a numeral branch, conditional on its other gates. Fixing the same locally demonstrated cubit would separate their predictions by three cubits, but no local unit calibration exists in these records. The broader finite-pipe shortest-distance branch and its constrained perpendicular/chainage alternatives retain their recorded different outcomes.

**Entry 29, Hyrcania.** The shortest reported side, 15 m, exceeds 24 cubits' upper bound by 2.40 m for 0.445–0.525 units, or by only **0.60 m** for the broader continuum. These preserve the reported-dimension side interpretation's arithmetic. Unreported physical endpoint/survey error prevents an independent field exclusion; an offset interpretation has different, unresolved origins. Historical pool-centre picking alone is about **2.797 m**, and the geographical check remains a failed **244.371 m**. The derivative Patrich–Eshel scale-bar disagreement, about 11.6%, provides source-dependence/distortion warning rather than an independent calibration or universal percentage allowance. Geographic and cubit-scale release remains unsupported.

**Entry 49, Siloam.** The inspected edition supplies an under-feature relation and no cubit distance or digging depth. Measuring L103's receiving-side height cannot define its unknown main-side underside, floor, basin membership or contemporary state. A numeric tolerance here would require an observed named contact and a distinct registered claim; no 17-cubit model is admissible from the treasure quantity.

**Entry 60, north of Tell es-Sultan.** The existing 49 m rejected map check exceeds the mouth-relation project's 2.5 m registration-proxy ceiling. At 150 m from the inherited 50 m-error anchor, a hypothetical feature with 10 m error needs a 34.21° margin from sector edges under the existing `2E` proxy, leaving about 10.79° either side of due north. Those inputs and margin rules are project proxies, not calibrated probabilities. A future good registration can locate a modern documented opening; its ancient date and grave-mouth coexistence remain separate requirements.

## Existing benchmark exposure

PR31's plan pilot retains **8.79%** and **7.87%** longer-chord mismatches and the unmeasurable **ʿEtri** case. Neither endpoints nor scale were adjusted. PR32's recovery pilot uses the same exposed Dagesh/Migdal/ʿEtri report families. Recovery agreement checks report facts, while independent field accuracy remains unscorable. Repeating picks checks operator reproducibility; source redaction and program-level answer separation cannot reverse prior exposure or create independently measured truth.

The audited reserved-batch template remains empty: coordinator, independent reviewers, actual freeze commit, pre-access chronology and cases are missing. No eligible unused geometry benchmark with verified independent physical endpoints is documented in these audited records. This finding is scoped to the named pilots, template and measurement packets; it is not a search of all future archive contents. L-656 and other protected arrivals remain unopened. The [finite next procedure](BENCHMARK_PROTOCOL.md) supplies a concrete preparation contract and retains those gates.

## Analytical correction applied

`registration.py::pair_error(..., same_document=True)` and registration-protocol §4 previously suppressed all shared-transform uncertainty and return picking-only `sqrt(2) × pick_error`. That is unjustified for unknown scale and affine/local distortion, and also insufficient for cardinal relations with uncertain rotation. Its existing same-document test encodes the same omission.

The [proposed correction](proposed_pair_error.py) requires a complete caller-justified `pair_local_error_m` for same-document relations and refuses the old picking-only shortcut. It leaves cross-document RSS as the historical project proxy, explicitly requiring covariance justification before any statistical interpretation. It neither adds an arbitrary global error to an internal distance nor invents a scale-error allowance. The integrator applied this correction to the shared helper, protocol and legacy test on 12 October. The companion proposal preserves the review artifact. No current registration or scientific verdict is rescored here.

## Reproduce and close

From the repository root:

```sh
python3 -I research/feature_workbench/measurement_resolution_2026-10-12/assessment.py --check
python3 -I -m unittest discover -s research/feature_workbench/measurement_resolution_2026-10-12 -p 'test*.py' -v
```

Fourteen tests pass. They check fixed numeric bounds, preserved documentary mismatches/abstention, free-unit overlap, unknown datums, an empty holdout template, rigid-motion length invariance, a counterexample for common scale, rotation's effect on cardinal order, and refusal to certify a picking-only same-document error. These mathematical fixtures validate the implementation; they supply no field observations.

The stated claim that existing measurements can discriminate the retained ancient feature/depth alternatives closes **not identifiable from available evidence**, with the explicit conditional drawing distinctions above preserved. Reopen for independently defined physical endpoints, an ancient datum and phase, a justified complete error model, a locally calibrated unit where needed, and an exposure-audited reserved reference; or a documented analytical correction. Obtained: the resolution dataset and the same-document error correction.
