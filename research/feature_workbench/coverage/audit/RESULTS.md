# Negative-notice and registration audit

**Result: not identifiable from available evidence.** The tested claim is that the inspected records supply a target-specific archaeological exclusion likelihood or an independently validated registration of the ancient landscape. The new source-instrument dataset was obtained; a calibrated detection model, new field observation and independent geographic holdout were not.

## Source instrument matters

The [crosswalk](absence_witnesses.csv) and [full result](results.json) retain every source-2 absence field, including fields that did not cause a FAIL. The source-2 intake contains 78 units, 60 in the main set. Fifty units carry the standard “Cisterns: none” field; 33 of these are in the main set. Nineteen main-set units and thirty pre-70 units have frozen C2 FAILs. Those frozen classifications are preserved.

Each record names its exact English volume, survey site, printed pages, coder sheet and original entry-level observation. Two coder sheets of that entry are two interpretations of the same report. They do not add an independent field search. The six landmark-exclusion gates remain unknown for every standard-field record: target identity/boundary, instrument's feature types, actual search reach, exact phase, preservation/visibility and detection limits. The “full” survey class supplies none of those target-specific joins. The quoted field concerns the site's cistern inventory; C2 requires an eligible pit/cistern in the northern sector within the frozen distance and origin rules.

The retained counterexamples make that distinction concrete:

- **S845, Kh. es-Saleh:** source-2 Vol. IV Site 44 pp. 199–200 was not visited because of minefields, but still has the standard absence field. Its frozen C2 is MATCH from other sources. This field cannot prove that a search failed.
- **S1173, Rujm es-Siʿa:** Vol. IV Site 86 pp. 288–289 has the absence field and reports Guérin's southern cisterns. The frozen C2 FAIL remains the registered documentary result; the field does not establish an exhaustive physical search.
- **S503 and S1116:** Vol. II Site 108 p. 329 and Vol. IV Site 84 pp. 280–284 retain field/narrative conflicts. Their frozen C2 values are UNKNOWN. A standard field is not a sufficient absence classifier by itself.
- **S241 and S1080:** the source-entry/WBADB grid and naming problems remain explicit. No new geographic target boundary is fabricated to resolve them.

The old S676 C3 survey failure is retained separately with its SWP Mem. II p. 30 reference. Its tomb-report instrument cannot be silently joined to the cistern field. The complementary [witness audit](../../../rarity/kohlit/witness_audit/outputs/absence_audit.json) retains exact coder witnesses for the frozen failures.

## An excavation exposure is not a target-volume search

The audit imports all 28 Jericho documentary notices and the IV/17 northern-opening target through the existing [coverage evaluator](../README.md). All six deposit-target gates remain unknown for these 29 targets. No source-backed target-specific negative observation is supplied, and no negative excavation claim is allowed.

The six deduplicated physical reach/loss observations retain useful, limited facts: A(C)90's bottom was not reached in four soundings (Netzer 2001 p. 67); A(C)161's floor was reached in a small northeast area (pp. 63–64, Ill. 94); AC44's eastern half was destroyed (pp. 58–60, 67, Ills. 86–87); the two numbered lower Cypros cisterns were destroyed (Meshel–Amit 1989 p. 234); AC1's last metre of feeder was destroyed (Netzer 2001 pp. 53–55, Ills. 77–80). These observations are not whole-basin claims. Their relation to an ancient deposit-target volume is unknown.

IV/17 retains excavation in chamber centres, not a documented search through a dated northern-threshold target. Wadi Nuʿeima retains the inspected ESI 5 pp. 110–111 report and its described bath; alluvium, flood exposure and illegal excavation do not establish a bounded bath target, phase or search reach. The geographic denominator and detection probabilities remain null.

The AF447 method therefore transfers as an explicit evidence requirement: a nondetection can change a location hypothesis only after the instrument, exact searched region, relevant feature/material and detection failures are tied together. Current records cannot supply the needed likelihood. No numerical posterior is computed.

## Five plan records checked without refitting

- **Hyrcania regional map, Patrich 1989 p. 243 Fig. 1:** one manual summit anchor plus assumed scale/north. The old Guide check's 244.371 m residual remains an exposed diagnostic. Its dam identity and source-position error are unverified. Neither this old check nor a newly downloaded copy can provide a fresh holdout.
- **Hyrcania detailed plan, p. 256 Fig. 22:** source-image scale and picks remain useful; geographic origin, verified north and independently located corresponding features are missing.
- **Qumran aerial, Magen–Peleg 2007 Fig. 35:** the five RANSAC inliers cluster in a western strip. A low training error and post-selection leave-one-out errors do not establish named geographic control or independent validation.
- **Qumran upstream plans, Ilan–Amit 1989 p. 283 Fig. 1 / Reeder–Jol 2006 p. 229 Fig. 4:** the two approximate tunnel centres support a source-to-source transfer. The uncertain, exposed junction is not a geographic holdout; the analyst's pixel perturbation is not a calibrated error distribution.
- **IV/17, Sion 2002 Plan 5 p. 63 / Fig. 12 p. 61:** the native crop, scale and north annotations support source-local proxies. Geographic registration, systematic error and the threshold/wall phase remain unresolved.

None passes geographic-registration eligibility or the separate historical-landscape phase join. Existing rejected registrations remain rejected. No fitted transform is regenerated and no old observation is relabelled unseen. `results.json` records the exact next observation needed for each case. Ephesus-style reconstruction can proceed once stable corresponding landmarks, a bounded error model, the relevant landscape state and a genuinely reserved comparison exist.

## Reproduction

The CLI generated `results.json`, `absence_witnesses.csv` and the SHA-256 [input manifest](input_manifest.json). Registration readiness requires explicit finite control and holdout coordinates in matching frames/units, a frozen nondegenerate transform and residuals computed from those point pairs. Metadata assertions without coordinates and collinear affine controls fail. The tests also exercise missing provenance and gates, wrong target/instrument/frame joins, incomplete feature-taxonomy coverage, phase mismatch, partial reach, exposed or duplicated controls and unbounded error. Actual-evidence checks preserve frozen results, notice identities, conflicting fields and old exposed diagnostics. No closed archaeological test was reopened.
