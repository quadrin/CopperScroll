# M04/R08: Hyrcania source-space dimension provenance

Prepared 2 October 2026 UTC / 1 October 2026 Los Angeles. Baseline: `quadrin/CopperScroll` commit `4a6c4434ff86f213aa2471351707ef2e8d7ab663`.

This cycle checked the available source files and reproduced arithmetic from the recorded plan inputs. Patrich's detailed plan, printed p. 256 Fig. 22, historical scan `269.jpg`, is absent from the authorized workspace. The original aqueduct ZIP is absent. A scan of 336 available image headers found no image matching the recorded 900 × 1231-pixel original dimensions. Filename checks and the handoff's archive inventory also supplied no original aqueduct scans. The surviving `hyrcania_detail.jpg` is a TIR crop; its regional symbols supply no pool boundaries for this task. This cycle made zero new original-page inspections or pixel picks.

Original source to reopen: Joseph Patrich, “אמות המים להורקניה,” in *אמות המים הקדומות בארץ־ישראל* (1989), printed pp. 243–260, [Kotar volume 6765980](https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=6765980). The pool dimension passage is printed p. 255, historical scan `268.jpg`; the detailed plan is p. 256, `269.jpg`. The viewer was not retried during this cycle. Its link identifies the absent source; this note makes no new claim about current online access.

## Provenance of the inputs

The [registration record](https://github.com/quadrin/CopperScroll/blob/4a6c4434ff86f213aa2471351707ef2e8d7ab663/registration/hyrcania_plan_registration_2026-09-30.json) identifies Patrich p. 255 as the source of the northern pool's reported side lengths: south 19 m, west 15 m, north 18.2 m and east 16 m. Those are previously transcribed published measurements. Their 68.2-m sum is project arithmetic. Neither a drawn pool perimeter nor four independent source-space edge measurements survives in the record. Published measurement uncertainty remains unreported in that record.

The scale-bar endpoints `(622,796)` and `(765,796)` are historical project picks from Fig. 22. They produce 143 pixels for 50 m, or 0.3496503497 m/pixel. The two approximate double-pool centers and their 8-pixel uncertainties are project picks and assumed picking uncertainty. They provide no corner polygon, edge thickness, wall-face definition or repeated independent scale estimate. The label sector for passage 49 provides no surveyed entrance point.

The [earlier extraction](https://github.com/quadrin/CopperScroll/blob/4a6c4434ff86f213aa2471351707ef2e8d7ab663/registration/hyrcania_patrich1989_extracted.md) now begins with a 30 September update reporting direct inspection of the entire 1989 Hebrew chapter. It preserves older blocked-access and 2002 English snippet notes below that update. The [run-3 extraction](https://github.com/quadrin/CopperScroll/blob/4a6c4434ff86f213aa2471351707ef2e8d7ab663/registration/extractions_run3/hyrcania_patrich1989_extracted.md) retains the older 29 September snippet stage. These two extractions supply no independent second measurement of Fig. 22. Their old north/south aqueduct labels require the later direct-review distinction; snippet-stage introductory-table wording cannot overwrite the directly reviewed chapter's northern 1,950-m and southern 9-km routes.

The [30 September direct review](https://github.com/quadrin/CopperScroll/blob/4a6c4434ff86f213aa2471351707ef2e8d7ab663/research/sites/christmas_hyrcania_primary_followup_2026-09-30.md) reports rock separating the double-pool members by 4.8–5.4 m, northern depth about 5 m and southern maximum depth about 2.6 m. These remain reported dimensions from the previous inspection. Source-center separation cannot validate that rock-width measurement. The same-author 1996 synthesis remains dependent evidence.

## Reproducible arithmetic and its scope

Run `python hyrcania_dimensions_audit.py`; it writes `hyrcania_dimensions_audit.json`. The script uses recorded inputs and performs no network access or image analysis.

At the historical scale, the reported four side lengths would span south 54.34, west 42.90, north 52.052 and east 45.76 pixels. These are computed comparison targets for a future digitization. They are not measured pixel lengths.

Nominal pick uncertainties convert as follows: 8 pixels = 2.7972 m, 10 pixels = 3.4965 m and 12 pixels = 4.1958 m. Two metres corresponds to 5.72 pixels. The current pool-center uncertainty already exceeds the declared two-metre feature-release target before scale or registration error. Its nominal status supplies no calibrated 95% bound. The record therefore cannot certify that target.

For illustration only, allowing each recorded bar endpoint to move by at most two pixels gives a conservative bar-length interval of 139–147 pixels and scale interval 0.34014–0.35971 m/pixel. No repeated picks establish that two-pixel allowance. Preserve it as a sensitivity assumption until original-page measurements supply an error estimate.

The existing entry 29 record retains the damaged conduit name and competing reservoir qualifications; Hyrcania's identity remains provisional. Under a side-length interpretation, 24 cubits at 0.445–0.525 m produces 10.68–12.60 m. The shortest reported side exceeds the upper limit by 2.40 m. A broader 0.40–0.60-m sensitivity interval produces 9.60–14.40 m, leaving a 0.60-m numerical gap. A 15-m side requires a 0.625-m cubit. This repeats conditional arithmetic on recorded source dimensions. Unreported source measurement errors and the reading's relation to the four sides remain unresolved. An outward-offset interpretation still lacks its origin and boundary geometry.

## Exact inputs still required

1. Full-resolution `269.jpg` or an authorized original Fig. 22 export with stable image identity, unaltered dimensions and visible scale labels; p. 255 / `268.jpg` for the full dimension paragraph.
2. Two independently collected scale-endpoint pick sets, recorded before comparison with earlier picks.
3. Northern-pool corner/edge coordinates distinguishing water faces, masonry faces and reconstructed boundaries. Record any obscured side explicitly.
4. Source north convention, scan distortion/anisotropy information, and measured or published uncertainty. Four side lengths alone cannot determine a unique quadrilateral shape or bearing.
5. Six independently identified geographic fit controls and three withheld controls with surveyed coordinates, datum, accuracy and footprint coverage. TIR supplies regional context and cannot replace these controls.

No geographic fit, pool footprint, deposit coordinate, independent source corroboration or architectural-phase determination results from this cycle. Hyrcania remains possible/low for entries 16, 29 and 35. This provenance/arithmetic audit adds zero primary-source targets, zero decisive candidate tests and zero question closures. Preserve the failed station-44 withheld check and the original source-space picks unchanged. The next executable source-space measurement requires the original Fig. 22 image; the parent cycle separately handles grid/datum sensitivity.
