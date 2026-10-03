# Entry 29: northern pool of the Hasmonean Pools Complex, Jericho

Assessment completed 2 October 2026 UTC. **Result: inconclusive.** The northern pool is a specific provisional feature candidate. This assessment supplies reproducible offsets, a southern-pool control and a construction-phase review. Its present evidence does not distinguish that pool as the scroll’s reservoir or locate a deposit.

## Hypothesis and source scope

Test entry 29, VII 3–7, against the northern of the two large pools marked palace phase 3 in the Hasmonean Pools Complex. In Trümper’s Fig. 18, printed p. 281, north points up and the candidate is the upper of the paired pools. In Figs. 20–22, printed pp. 284–286, north points right and it is the right-hand pool. No excavation locus number is assigned to this candidate without verification in the original report. A(C)94 is a different pool and its dimensions/elevations are excluded.

The tested geometry is perpendicular distance from either **inner long-wall face** to the central inter-pool route, confined to the short wall segments actually visible in each detailed figure. The southern pool receives the same test. The models are conditional on Puech’s side-reference reconstruction and our interpretation of “large” as long. Northern describes the reservoir; it supplies no measurement bearing. The original source defines neither a perpendicular axis nor a route-distance starting junction.

Puech’s actual edition images, printed pp. 62–65, were reinspected. Jericho is entirely restored; the starting-side relationship and parts of the numeral are also reconstructed. His preferred 24-cubit reading and the apparatus’s 27-cubit alternative are retained as separate branches. His note 259 says Netzer’s Jericho suggestion preceded his restoration. The specific northern pool and sampled channel are our hypothesis, rather than a pool identified on that page. [Detailed reading constraints](reading-note.md).

Trümper’s actual page images, printed pp. 280–286 and p. 296 illustration credits, were inspected. This is an authored archaeological reanalysis using Netzer-derived plans. It supplies accessible evidence from the same excavation lineage, rather than independent corroboration. [Phase and provenance review](phase-review.md).

## Measurement result

Use an exploratory cubit range of 0.40–0.60 m: 24 cubits = 9.6–14.4 m; 27 cubits = 10.8–16.2 m. These are sensitivity assumptions, not an established local cubit standard. Figs. 20–22 have legible 10 m scale bars. Complete pool lengths are cropped from those figures; the overview establishes orientation but was not used for metric calibration. The subsequent Kotar inspection supplies Netzer’s approximately 18 × 13 m published dimensions for both earlier pools and a complete p. 100 plan; see the follow-up below. The frozen offsets continue to use their original 2018 figures.

| Model | Northern pool | Southern control | Interpretation |
|---|---|---|---|
| Phase 3 / Fig. 20 | Near side 2.09 m; far side 15.65 m | Near side 3.48 m; far side 16.78 m | Neither nominal offset reaches the 24-cubit band. |
| Phase 5 / Fig. 21 | Near side 2.26 m; far side 15.65 m | Near side 3.30 m; far side 16.78 m | Same conditional result; repeated drawing geometry adds no independent evidence. |
| Phase 6 / Fig. 22 | Unclassified central line: near 1.02 m; far 14.24 m | Near 4.41 m; far 17.37 m | Line identity unresolved; excluded from qualifying channel matches. |

Decimal precision here supports recomputation; reporting archaeological accuracy at centimetre scale would be unjustified. Picks were made in full-page 2× fitz renders. A tighter assumed error envelope gives the phase-3/5 northern far distance 14.62–16.76 m; a wider stress envelope gives 14.05–17.43 m. **The nominal 24-cubit miss therefore cannot exclude this branch robustly.** Near-side offsets remain far too small in both envelopes.

The 27-cubit branch overlaps the northern far-side interval and the southern control’s far-side interval. This overlap fails to distinguish the northern pool geometrically. The southern pool is a geometry control; it does not satisfy the northern-reservoir designation as a whole candidate. Phase 6’s numerical overlap is an unclassified-line coincidence requiring feature identification before it can count as support. No all-channel search or hidden wall extension is represented as tested. [Full geometry note](assessment.md), [pixel inputs and results](measurements.json), [recomputation script](measure.py).

![Original offset schematic](schematic.svg)

The schematic shows a sampled cross-section near the visible western ends. It is an original simplified diagram with metres in source-plan space. It is neither a complete pool footprint nor a geographically registered candidate area. See the input JSON for finite sample segments. No WGS84 deposit coordinate is proposed.

## Phase and preservation

The overview assigns palace phase 3 to 103–76 BCE, phase 5 to 76–67 BCE, and phase 6 to 67–63 BCE. These labels do not precisely date every channel line. The account distinguishes successive supply arrangements; their prose numbering must not be equated with palace phase numbers.

Trümper printed p. 285 explicitly reports that Herodian alterations left the original pool inlets and inter-pool pipe unpreserved. A reconstructed line cannot provide an observed inlet datum. Earlier construction is period-compatible. Netzer’s newly inspected 1983 pp. 105–106 describe Herodian joining of these two pools into one basin, creating an explicit limit on a separate-northern-pool later-use model. The relevant channel’s continued accessibility and a dated concealment surface remain unresolved. [Exact pages and source lineage](phase-review.md).

## Confidence and next discriminating test

- Reading: edition-based and damaged; 24 and 27 cubit branches retained, side datum conditional.
- Site association: low; Jericho is restored and the cited archaeology identifies no unique pool for entry 29.
- Feature identity: low; northern pool remains possible, with no distinctive dimensional result over the southern control.
- Phase: broad Hasmonean compatibility; individual channel phase and later survival unresolved.
- Position: sampled source-plan offsets only; no geographic registration or ancient inlet point.

The original pass left the whole candidate open while documenting a nonunique geometry branch. Current work follows [ACTIVE_TEST.md](https://github.com/quadrin/CopperScroll/blob/main/research/ACTIVE_TEST.md) and the [preparation audit below](#comparison-design-and-exposure-audit--3-october-2026-utc). Protect observations reserved for confirmation while logged exploratory sourcing continues; resolve each test's relevant design and exposure dependencies before revealing its reserved evidence. Route-distance models require a physically justified starting junction.

## Access links and reproducibility

Accessible: Monika Trümper, “Swimming Pools and Water Management in the Eastern Mediterranean World of the 4th to 1st Century BC,” in Jonas Berking, ed., *Water Management in Ancient Civilizations*, Berlin Studies of the Ancient World 53 (2018), pp. 255–296. [Direct publisher PDF](https://edition-topoi.org/download_pdf/bsa_053_10.pdf). File SHA-256 `0d0cd8031e3e03181d67942851017f7a4ae9219f0bc405c97f954b094f7efab7`; 42 PDF pages; printed page = PDF page + 254. Render PDF pages 30–32 at fitz Matrix(2,2) to inspect recorded pixel picks. Run `python measure.py` to regenerate the JSON from the frozen picks. This recomputes manual measurements; it does not automatically reidentify the archaeology.

Historical access state at the first assessment; subsequent supplied-page inspections below supersede it to their stated scope:

- Ehud Netzer, *Hasmonean and Herodian Palaces at Jericho: Final Reports of the 1973–1987 Excavations*, Vol. I, *Stratigraphy and Architecture* (Israel Exploration Society, 2001): [publisher record](https://www.israelexplorationsociety.com/product-page/volume-i-stratigraphy-and-architecture-2001). Relevant text pp. 74–84 and plans 14, 17–21; rerouting pp. 92–100 and plans 17–22, as cited by Trümper. Those original pages were not recovered here.
- Ehud Netzer, *The Palaces of the Hasmoneans and Herod the Great* (English edition, 2001): [publisher record](https://www.israelexplorationsociety.com/product-page/the-palaces-of-the-hasmoneans-and-herod-the-great-1), [Google Books record without ebook/reader](https://books.google.com/books/about/The_Palaces_of_the_Hasmoneans_and_Herod.html?id=eGhoQgAACAAJ). Trümper’s credits point to p. 93 / plan 17, p. 96 / plan 19, and p. 7 / plan 20; the last is the surprising printed credit and remains uncorrected. Her bibliography’s edition metadata differs from the English publisher record; exact source edition/pagination needs checking.

New KPI contributions: one scoped Trümper source target and one bounded offset/control check. Puech reinspection adds no target. One conditional candidate assessment is completed with an inconclusive result; decisive tests and question closures remain zero. Current cumulative totals: 22 direct targets, 5 cartographic intakes, 22 bounded checks, 0 decisive tests, 0 closures.



## Kotar follow-up — 2 October 2026, Los Angeles

Netzer’s 1983 original chapter now supplies a complete plan (p. 100), approximately 18 × 13 m for each early pool (p. 101), and a later plan/text identifying Herod’s joining of the pair into one approximately 32 × 18 m basin (pp. 105–106, footnote). This adds a specific conflict with assuming survival of two separate reservoirs into a later-use model. A merged northern basin is a separate possible hypothesis and changes which sides are longer; the earlier offset calculations cannot transfer to it. Candidate confidence remains low and the assessment inconclusive. One new source target and one bounded survival check bring totals to 23 direct targets / 5 map intakes / 23 bounded checks / 0 decisive tests / 0 closures. [Image-checked observations, exact pages and remaining source limits](https://github.com/quadrin/CopperScroll/blob/main/research/assessments/entry29_jericho_pools/kotar-netzer1983.md).


## Original final report: first pass

The supplied 2001 final report now provides an image-checked channel distinction: late Hasmonean supply branches are identified, while the Herodian combined-pool supply remains explicitly unknown. Tentative southern-side walls W57/W43 offer a separate tracing target. Original plans and foldout completeness remain to be checked. [Scope and evidence](netzer2001-first-pass.md).


## Archived original plans

[Netzer final-report Plans 17–22](../../assets/plans/netzer2001/README.md) are now stored as source figure crops with provenance and hashes. The user’s 2 October 2026 archive instruction supersedes earlier delivery notes withholding these particular images. Their upload adds no independent evidence or completed test. Folded plans and illustrated-book extracts remain queued.


## Earlier measurement figures archived

[Trümper Figs. 18–22](../../assets/plans/trumper2018/README.md) now preserve the publication figures used for the earlier offsets. The archived images retain the article’s printed orientation; their crop coordinates differ from the frozen full-page raster inputs used by measure.py. Do not apply the old pixel picks directly to these crops without the recorded transformation. Source-lineage and research KPI counts remain unchanged.


## Joined-basin follow-up — 3 October 2026 UTC

The specific Herodian A(B)101 eastern-outlet branch has now been checked against original report pp. 87/100/131–133. Supply remains unknown and no outlet-wall tie is established. Approximately32×18m merged dimensions change the long-side reference; both 24/27-cubit counterfactuals fit an assumed 18 m width, without any observed channel point measured. This revises the existing assessment, leaving it inconclusive and low-confidence. [Assessment and numeric inputs](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle14/jericho_merged.md). [New source-page archive](../../assets/plans/netzer2001-cycle14/README.md). Specific folded Plans14/15/23 remain unlocated in the supplied PDF; the main text is available. Earlier access statements in this historical record are superseded to these stated inspection scopes.


## Hydraulic-direction follow-up — 3 October 2026 UTC

The defended original wording does not establish inflow direction. Puech’s proposed collection-installation continuation is conjectural; Milik1960 sourceentry31 preserves a damaged Qe-form and reservoir relation. A(B)171’s observed drainage survives the narrow direction test without a positive textual identification. The fuller collecting-installation branch needs that associated structure, and the outlet still lacks a pool-wall contact/datum. All earlier numeric bands remain counterfactual; no coordinate or confidence change follows. [Original-edition comparison](https://github.com/quadrin/CopperScroll/blob/main/research/measurements/cycle15/jericho_conduit.md).


## Comparison design and exposure audit — 3 October 2026 UTC

Three parallel threads audited the existing inventory, parameter records and source exposure at baseline `09acbd264af82c689c6259f3d16562f18b78f3e1`. They read repository notes, tables and archive metadata; they opened no new original pages, target plans, images or field measurements. **Regional comparison preparation remains incomplete; no confirmatory test is registered.** The identification remains **not identifiable from available evidence**. This audit adds no archaeological source target, bounded archaeological check, formal assessment, outcome-ledger count or question closure.

### Scope, selection and provisional inventory

The stated claim is conditional on restoring Jericho in entry 29, VII 3–7. Puech 2015 pp. 62–65 supplies partly preserved northern-reservoir/four-side constraints and discusses palace installations and Ain Doq; it selects no particular basin. Existing records also notice a reservoir at Tell es-Sultan/ʿAin es-Sultan. These named sectors justify an inventory search extending beyond the preferred palace pair. They establish no closed ancient-oasis polygon, survey footprint or complete basin census. Fix geographic limits from documented landscape/survey coverage before a regional comparison. Atlas markers, an arbitrary radius and the full extent of a historical map cannot supply those limits. [Reading constraints](constraints.json), [edition scope](reading-note.md), [Koḥlit screen](../../measurements/cycle7/kohlit_pool.md).

The selection policy retains every source-noticed water-retaining basin/tank and conduit association within the eventual boundary, without a size or swimming-function filter. Retain excavated, partly excavated, unexcavated, destroyed and status-unknown records. Missing shape, conduit, northern reference, date or datum stays unknown unless adequate coverage demonstrates absence. Separate successive states of one installation family; require contemporaneous surfaces and connections for a qualifying fit. Northern describes the reservoir and supplies no displacement bearing. Hyrcania and other restoration proposals remain outside this conditional Jericho claim; a Jericho-relative outcome would leave them unresolved.

The following **eight preparation rows form an incomplete roster**. They include related phases and an aggregate pair; their row count is not a count of independent eligible candidates. No fit is newly assessed here.

| ID | Installation/state | Existing source and comparison limit |
| --- | --- | --- |
| J01 | Early northern Pools Complex pool | Netzer 1983 pp. 100–101: approximately 18 × 13 m; Trümper Figs. 18/20–22: derivative phase plans. Original inlet/contact remains unresolved. |
| J02 | Early southern Pools Complex pool | Same pair and fieldwork as J01; historical 27-cubit geometry overlap. Retain as geometry control; the pair-relative northern designation does not make it a full-entry match. |
| J03 | Joined Herodian A(B)101 | Netzer 2001 pp. 74/85/100: approximately 32 × 18 m; drainage through A(B)171, pp. 87/131–133. Later state of J01/J02; wall junction, collector and face remain unestablished. Supply unknown, p. 84. |
| J04 | A(C)94 | Distinct Area AC pool; Trümper p. 284 records a channel segment and absent terminal connection. Complete phase/datum eligibility unresolved; no transfer of J01 offsets. |
| J05 | A(C)90 | Existing phase review notices another Area AC pool. Shape, date, conduit and datum remain unassessed in this roster. |
| J06 | Other pool pair west of central palace | Netzer 1983 p. 100 label 3, distinct from the selected label-4 pair. Aggregate notice requiring individual identities before enumeration. |
| J07 | Settling Tank A(B)99 | Netzer 2001 p. 84: two late Hasmonean branches supply J01/J02. Reservoir eligibility, shape, northern relation and datum remain unresolved. |
| J08 | ʿAin es-Sultan reservoir/channels | Existing table attributes a shallow dressed-stone reservoir and irrigation channels to SWP III pp. 222–223. Historical notice; ancient phase, footprint and entrance remain unknown. |

J01/J02/J06 derive from the [1983 inspection record](kotar-netzer1983.md); J04/J05 from the [phase review](phase-review.md); J03/J07 from the [first pass](netzer2001-first-pass.md) and [joined-basin record](../../measurements/cycle14/jericho_merged.md). J08 is an attributed record in [phase5_reports.csv](https://github.com/quadrin/CopperScroll/blob/main/tables/phase5_reports.csv), carried through the Koḥlit screen; this audit did not recheck SWP pages.

Coverage gaps remain explicit: other palace/estate pools and pipes noticed around Netzer 1983 pp. 99–101; the Ain Doq sector named by Puech p. 65; workshop installations in the [encyclopedia archive's stated Jericho scope](../../assets/plans/neaehl-vol5/README.md); and unidentified unexcavated, destroyed or obscured oasis alternatives. These are coverage notices, not invented basin identities. The [TIR intake](https://github.com/quadrin/CopperScroll/blob/main/research/sources/tir_umich_map_intake_2026-10-01.md) supplies selected map windows and no complete transcribed inventory. Regional denominator, completeness and detection rate remain unknown.

### Retained design choices and numerical limits

The [constraints](constraints.json) and [hydraulic comparison](../../measurements/cycle15/jericho_conduit.md) support a finite categorical design menu, pending named observations and source-grounded combinations:

- Retain 24/27-cubit readings; distinguish the defended partial conduit association, Puech's conjectural collecting-installation continuation, and Milik's damaged Qe-name branch. The collector requirement belongs to the fuller restoration; an unnamed drain cannot confirm the Qe-name. An outlet feeding a collector is a project interpretation. Keep Puech's restored from-side relation and the project's large-equals-longer interpretation explicit; do not invent a complete alternative preposition reading.
- Retain both physical longer sides and inner/outer faces where recoverable at a fixed surface/elevation. Early north/south long sides and merged west/east long sides are separate models. Taper, wall exceptions and imperfect alignment preclude a universal face correction or an assumed exact rectangle.
- Retain signed horizontal perpendicular offsets on finite observed wall segments, and route distance only from a physical junction with the chosen face along a phase-identified conduit. Register the direction/path convention. Arbitrary conduit stations, extended wall lines, a northern displacement and independent digging depth have no justification here. Slope-distance alternatives remain unresolved pending a profile and justified convention.
- Keep early Hasmonean arrangements separate from joined Herodian A(B)101/A(B)171. Trümper's palace phases 3/5/6 and Netzer's hydraulic stages need explicit mapping. Phase 6's unidentified central line supplies no qualifying conduit. A reconstructed old channel and later wall require their own contemporaneity evidence.

The existing 0.40–0.60 m/cubit continuum supplies exploratory sensitivity, with 24 = 9.6–14.4 m and 27 = 10.8–16.2 m. No finite calibrated local cubit set is established. A discrete grid or preferred unit chosen from a target fit would add an unsupported assumption. The original ±3/±5-pixel pick envelopes quantify assumed digitization sensitivity only; they exclude original plan accuracy and distortion and cannot transfer to new sheets or crops. Rounded published dimensions supply no survey error budget. These block confirmatory distance registration; a topology/contact test need not resolve cubit calibration. [Original geometry scope](assessment.md), [merged counterfactual](../../measurements/cycle14/jericho_merged.md).

Before confirmatory distance measurement, specify each permitted row's candidate, compatible textual bundle, numeral/unit hypothesis, phase, finite side/face/elevation, axis or anchored route, exact target and source-specific uncertainty. Apply the same menu to every eligible control and retain each control's best permitted fit. Keep one shared metrology hypothesis consistent across linked distances. For defensible uncertainty intervals, disjoint observed/predicted distance intervals contradict that branch; overlap establishes compatibility only. An essential unbounded uncertainty or missing datum yields unknown. Fix the comparison scope and discrimination criterion before results; a regional uniqueness claim requires adequate alternative coverage and contradictions across each alternative's retained branches. No rarity probability or advantage threshold is established here.

### Observation-level exposure audit

| Observation/source | Status before this audit | Consequence |
| --- | --- | --- |
| Early/merged outlines, dimensions and phase selection | Used from Netzer 1983 pp. 100–101/104–106; Netzer 2001 pp. 74/82/84–85; Trümper pp. 280–286 | Exposed model-selection evidence. |
| Herodian drainage through A(B)171 toward eastern fields | Used in cycle14 from Netzer 2001 pp. 87/100/131–133 | Recovering the same drainage observation repeats known evidence. |
| Collection-restoration requirement and wall/collector gap | Used in cycle15 from Puech pp. 62–65 and Milik 1960 p. 140/pp. 148–149 | Existing model requirements; the collector itself remains unestablished. |
| Exact A(B)101 east-wall contact/aperture, profile and connected collector | Unestablished in inspected records; no located Plan 14 sheet or identified field section | Potential dependency; source coverage and prior exposure unverified. |
| Detailed Plans 15/23 | Not located in the supplied scan; earlier western/Stage 7 control roles already known | Phase-control gaps; holdout eligibility unverified. |

**No verified holdout exists.** Failure to locate Plans 14/15/23 in the 408-page scan establishes an access gap, not an affirmative nonexposure record. Trümper derivatives and Netzer's publications share the excavation lineage. Original [Plans 17–22](../../assets/plans/netzer2001/README.md) are archived; the [cycle14 manifest](../../assets/plans/netzer2001-cycle14/figure_manifest.json) distinguishes inspected targets, additional text and retained contextual figures. Unanalyzed archived content may have been encountered. The two 2001 publications and Trümper's odd printed Plan-20 page credit also require exact bibliographic reconciliation. A newly obtained file or original sheet supplies no automatic independence or unseen observation.

### Next evidence trigger and stopping point

Develop the regional catalogue, geographic/coverage limits and individual feature identities before confirmatory regional comparison. Logged exploratory sourcing and analysis may proceed. For observations reserved for confirmation, obtain metadata-only sheet/section identity and coverage information and audit prior exposure by model selectors through originals, captions, OCR, derivatives and summaries before revealing the reserved content. The publisher volume link is a routing lead; no exact sheet accession, field-section ID or custodian is verified here. This pass sent no contact request.

Required target data are a phase-specific A(B)101 east-wall plan/section, a named face and ancient surface, aperture/physical channel contact, centerline/invert levels and continuity to A(B)171; the fuller collection branch additionally requires an identified collector and its contemporaneous connections. Record survey/height datum, scale, north convention, uncertainty, reconstruction status, remodeling/disturbance and excavation reach sufficient to interpret an absence. Obtain equivalent minimum evidence for comparison candidates. Missing remains or documentation cannot prove absence.

If a specific existing observation cannot be shown unused, classify it as exploratory. A genuinely new independently collected measurement after a design freeze could supply the missing test evidence. A narrower topology/contact test may proceed before the regional catalogue or cubit calibration is complete once its own claim, relevant parameters, exposure audit and failure rule are frozen. Its result concerns only that narrower relation; identification still needs a fixed regional comparison and unseen prediction. Commit an exact prediction, relevant finite justified parameters, tolerances and failure rule before revealing the reserved test observations. Prediction failure rejects its registered model; reject the whole stated identification only after adequate contradictions across every retained branch. Retain the present terminal identification result until its conditions are met; logged exploration and narrower frozen tests do not reopen it. No confidence, coordinate, source/activity counter or outcome-ledger change follows.


## Fresh contact and catalogue search — 3 October 2026 UTC

Three parallel exploratory threads checked original contact figures, exact pocket-sheet access routes and comparison sources after `4677550`. No confirmatory observation was reserved. The [original-page audit and access record](netzer2001-first-pass.md#contact-reinspection-and-source-recovery--3-october-2026-utc) preserve source identity, image scope and limitations. Netzer reports the Herodian A(B)171 outlet segment, but the checked originals still establish no pool-wall aperture/tie, drain profile or connected contemporaneous collector. Nearby sections and junctions belong to other systems. Plan 14 remains unrecovered; the exact Michigan/HathiTrust copy and its pocket-plan metadata now provide a concrete acquisition route.

### Original comparison evidence

Reinspected the [publisher Trümper PDF](https://edition-topoi.org/download_pdf/bsa_053_10.pdf), text pp. 280–285 and figure credits p. 296, original images pp. 280–283/Figs.18–19 (PDF pages = printed minus254); hash matches the previously archived source `0d0cd8031e3e03181d67942851017f7a4ae9219f0bc405c97f954b094f7efab7`. The article's eight large Hasmonean swimming pools span several phases. Footnote55 p. 283 excludes other reservoirs/distribution/ritual basins: that selected census cannot supply our basin denominator.

Fig. 19 p. 282 distinguishes A(C)90, A(C)94 and AC44. In that plan's north-arrow frame, A(C)90 lies north of94 and AC44 east of94. J06's older aggregate pair cannot be silently merged with these named pools. A(C)94 has distinct supply arrangements (pp. 283–284): a proposed roof supply lacks an identified inlet; a **terracotta pipe found in its northern wall near the northwest corner** was followed 3.3 m northwest; a later northeast distribution basin/open-channel fragment lacks its terminal connection. The found pipe most likely branched from the Wadi Qelt aqueduct and later cut when Na’aran supply was installed. Footnote57 routes to Netzer2001 p. 57/Plan13; its reported levels belong to this installation and cannot transfer to A(B)101. Numbered phase assignments for each connection remain unresolved. This establishes a published physical contact in a comparison pool, not a new Copper Scroll fit or independent field campaign.

### Roster updates and coverage notices

The earlier eight-row audit remains a dated record. This pass extends the preparation roster to **18 rows**, including successive states, aggregate notices and unresolved overlaps. They are not 18 independent eligible candidates. All missing dates, wall faces, channel ties and preservation/measurement coverage remain unknown. Later-period records are retained for a documented temporal screen, not accepted as first-century layouts.

| ID | Source-noticed installation/state | Newly checked evidence and limit |
| --- | --- | --- |
| J04, updated | A(C)94 | Found northern-wall pipe distinct from later missing channel terminal; Trümper pp. 283–284. Actual Netzer p. 57/Plan13 still needed. |
| J05, updated | A(C)90 | Separately labeled in Fig.19, north of94 in the source frame. Required dated conduit/contact/datum unresolved. |
| J07, updated | A(B)99 | Netzer pp. 83–84/Ill.117 supply tank with sections and two branches to the early pair; not a demonstrated eastern collector. |
| J08, updated | ʿAin es-Sultan historical reservoir | SWP III pp. 222–223 original reports 24 ×40 feet and irrigation channels. Construction date, wall face and inlet datum unestablished. ROSAPAT pp. 110–112 separately lists Roman nymphaeum, Ottoman pool and modern roofed pool; their identity with the SWP feature is unverified. |
| J09 | AC44 | Distinct pool in Trümper Fig.19; p. 281 n.50 cites Netzer p. 60 for drainage. Original drainage-wall tie not inspected. |
| J10 | Septic Tank A(B)215 | Netzer p. 94, southern Western Garden; bath drainage interpretation for earlier Buried Palace, separate from Herodian eastern outlet. |
| J11 | Abu el-ʿAlayiq North area pool, PADIS0153 | ROSAPAT pp. 101–102, catalogue no.4: Hellenistic pool, preserved; cites Netzer–Garbrecht2002 Fig.6. Identity/overlap with existing palace rows unresolved. |
| J12 | Birket Musa, PADIS0025 | ROSAPAT p. 120, no.38: Roman pool, partly preserved/under cultivation; published220 ×160 m and21.5 m depth need original-source reconciliation. No target contact/datum established. |
| J13 | Birket Gilgiuliyeh, PADIS0157 | ROSAPAT p. 120, no.37: Byzantine pool ruins near Khirbet en-Nitla. Shape/contact unknown; retain as temporal coverage notice. |
| J14 | Tell el-ʿAqaba/Cypros water-system aggregate, PADIS0145 | ROSAPAT p. 118, no.32: late Hellenistic cisterns; Roman/Herodian pools/cisterns; later aqueduct use; partly eroded. Individual basin identities unresolved. |
| J15 | Khirbet el-Mafjar water-system aggregate, PADIS0012 | ROSAPAT p. 126, no.50: early Islamic palace water channels/reservoir with later reuse. Individual contacts/footprints unassessed. |
| J16 | Tell el-Qos basin/cistern aggregate, PADIS0021 | ROSAPAT p. 139, no.74: Byzantine plastered basin/cisterns, ruins; no ancient estate identification follows. |
| J17 | Small stepped Pool A(B)63 | Netzer p. 131:1.8 ×1.4 m; assumed depth1.4 m, interpreted ritual bath, rim and surrounding floor eroded. Construction relation unresolved. No function/size filter removes this notice. |
| J18 | Cypros fortress/palace water-system aggregate, PADIS0010 | ROSAPAT p. 117, no.31: Hellenistic cistern/pool and Roman bathhouse/water system. Individual features and overlap with J14 unresolved; hilltop inclusion requires the boundary rule. |

No atlas marker or geographic coordinate was added. Catalogue site coordinates are site references, not pool-wall/deposit datums. The p. 87 apparent north–south outlet toward the Hasmonean Garden supplies an additional conduit notice for J01 with precise phase and physical wall tie unresolved; it is distinct from J03's eastern outlet.

### Inventory-source scope

The newly accessed *Archaeological Heritage in the Jericho Oasis* (Nigro, Sala and Taha, eds., 2011; ROSAPAT7) supplies a regional site catalogue. Its chapter3 is by Marta D’Andrea/Maura Sala. Methods pp. v–vi combine earlier literature with surveys/field checks and retain concealed, damaged or inaccessible recorded sites. Not all coordinates were GPS checked; some derive from satellite maps (p. vi n.3), and coordinate seconds are indicative (p. 99 n.2). The list pp. 95–99 describes visited/recorded/surveyed and sometimes excavated sites spanning Natufian–Ottoman dates in the oasis and surroundings. This is an explicit coverage source, not an assertion that every ancient basin was detected. The subsequent records preserve specific disturbances and unknown feature relationships. The introduction p. 1 reports103 sites, while the actual list reaches105, including cave aggregates; preserve these source scopes. Environmental setting p. 2 is not a ready-made eligibility polygon. A closed geographic inventory boundary, basin-level deduplication, detection limits and unrecorded alternatives remain unresolved. Ain Duq/Doq records remain water-system notices without resolved individual basin identities; their compressed accounts cannot exclude pools. The 2015 *Jericho Oasis Archaeological Park* report selects13 visitor sites from105 sites (p. 219/n.1 and p. 222); its tourism selection cannot replace the catalogue or a basin census.

Original acquisition, hashes and inspected page/figure scopes are recorded below. These sources mix survey observations and earlier bibliography; count no independent-observation total from publication count. Newly exposed content is exploratory. The copyrighted catalogue and2019 contextual chapter are linked, not republished. Existing Trümper figures remain in their original archive; metadata/access work adds no archive or outcome count.

### Accounting and next action

| Retrieved source | Exact original inspection scope | Acquisition and file identity |
| --- | --- | --- |
| Conder/Kitchener, SWP Memoirs III (1883) | Printed222/PDF248 and223/PDF251, visually checked; intervening foldouts make page offsets nonconstant | [Original scan](https://archive.org/download/surveyofwesternp03pale/surveyofwesternp03pale.pdf),510 PDF pages; SHA-256 `07c42f05488658faff9a12b01c3af37707192e72214a32f5242469c708cce18c`. Text-only target pages; underlying work public domain. |
| Nigro/Ripepi/Hamdan/Yasine, JOAP2015, *Vicino Oriente* XIX219–247 | Original219/PDF1,222/PDF4,232/PDF14 Figs.1–2,238/PDF20 Fig.12 | [Institutional author deposit](https://iris.uniroma1.it/bitstream/11573/862728/1/Nigro_Jericho_2015.pdf),34 PDF pages; SHA-256 `b4cf24e3f6b55a6427ff31203aeb42afb6af5fdd8e637ae80c8d1bca27ab3dea`. Rights reserved; visitor maps are not a basin census. |
| Nigro/Sala/Taha, eds., ROSAPAT7 (2011) | Original title/rights PDF3–4; v–vi/PDF9–10;1–2/PDF13–14;95–99/PDF107–111;101–102/PDF113–114;110–112/PDF122–124;117–118/PDF129–130;120/PDF132;126/PDF138;139/PDF151. Other catalogue text screening does not establish image inspection. PlateI regional map uninspected. | [Official expedition publications](https://sites.google.com/uniroma1.it/sapienzatojericho/publications), observed public embed “Nigro2011-ROSAPAT07.pdf”; [linked download](https://drive.google.com/uc?id=1RE_9cNN76qub2UGHE6ntJTO8PbMUBJXV&export=download). Old `lasapienzatojericho.it` direct PDF failed.336 PDF pages,79,335,139 bytes; SHA-256 `0c7fefdf676abb796c6cccf4f33dd6289c499d6a54249322e0b2ea672122af73`. No scan/figure redistribution permission. |

The2019 chapter's hash, original-page scope and public publisher route are in the linked contact/access note. All PDFs were visually checked to these stated scopes; text extraction supplied navigation. Publicly linked expedition/publisher downloads involved no private Drive or Library search. No catalogue coordinate was accepted as a geographic or vertical survey control.


Four new scoped source targets: SWP original reservoir pages, JOAP2015 selection/coverage, ROSAPAT2011 methodology plus scoped water-site records, and the2019 contextual chapter. Four bounded checks: SWP ancient-phase/contact coverage; JOAP selection-versus-census scope; ROSAPAT basin identity/coverage scope;2019 target-contact coverage. Repeated Netzer/Trümper evidence and bibliographic routing add no extra targets/checks. Cumulative activity becomes47 scoped targets /5 cartographic intakes /52 bounded checks. Identification/outcome counts, question states, grades and coordinates remain unchanged; this search completes no regional inventory or decisive test.

Next, obtain the exact folded Plans14/15/23 and pursue the recovered catalogue's original basin records. Resolve J06/J11 overlaps and individual Cypros/Mafjar/Doq installations before fixing the regional roster. A(C)94's p. 57/Plan13 wall contact supplies a concrete comparison-document target. Protect any future reserved observation only after its specific exposure audit and test freeze; these newly inspected sources cannot confirm a model independently. Missing source records still do not establish absent remains.
