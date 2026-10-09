# Investigation coverage

`evaluate.py` imports the reviewed Jericho source-sector inventory, its current Wadi original-report review and the IV/17 assessment/context chain. It returns a machine-readable module for the feature workbench. Rebuild from the repository root with:

```sh
python research/feature_workbench/coverage/evaluate.py
python -m unittest discover -s research/feature_workbench/coverage -p 'test_*.py'
```

The 28 J-records remain documentary notices: 13 physical-feature records, three phase-state records, ten aggregates and two unresolved identities. The twelve sectors define documentary scope. Their polygons, eligible-basin denominators and uniform detection coverage remain null. Twenty-one additional obligations retain later, concealed, unrecorded and crosswalk-unknown alternatives. The earlier separate J01/J02 basins and joined J03 state remain distinct records; unresolved aliases are never collapsed.

Published loss/reach observations are imported once per explicit source feature and observation lineage. The two destroyed numbered lower Cypros cisterns appear once each despite sharing J14/J18 parent notices. Netzer's preliminary/final accounts and Trümper's reanalysis share the recorded excavation lineage. A lineage group is not a newly verified discrete field campaign, and an unknown lineage stays unknown.

J23 uses the complete inspected ESI5 report, pp. 110–111 / PDF 118–119, as its current source state. Historical pending-source fields remain visible under `historical_record`. One miqva is explicitly described; the complete site bath count and field-locus crosswalk remain unknown. The separate western rectangle's dimensions do not become bath dimensions, and the site's period range does not date bath construction. Alluvium, flash floods and illegal excavation leave target coverage unknown.

IV/17 preserves the difference between excavation in chamber centres and a tested ancient northern threshold. Its target volume, ancient datum, reached levels, architectural phase, disturbance and detection limits remain unknown. Published basket/permit identifiers identify the next field-record dependency; they do not establish spatial coverage. Table 1's repeated coins add no independent chronological observation. The target-volume join below records this per branch. No A(C)94 geometry is rerun or parked source acquisition restarted.

`evaluate_target()` provides six gates for a future bounded negative-excavation assessment: ancient target volume, ancient datum, actual reach, phase alignment, disturbance/preservation and detection method/limits. Structured evidence and source provenance are required. Target/datum/reach reference frames and record identities must agree. Explicit phase identities must match, or a sourced equivalence record must name both exact states and their physical same-state contact. Period labels and broad date overlap remain unknown; explicit incompatible phases fail. A separate sourced negative observation is required before a negative claim is eligible. Bare period headings, depths, source silence, incomplete reach and unexplained-removal rescue cannot pass. The shipped evidence passes no negative-deposit gate and assigns no detection percentage or identification probability.

The datum gate requires an identified, source-backed ancient surface with a verified exact phase matching the accepted target/exposed state. A direct ancient datum must name that surface. A modern benchmark requires a separate measured join naming the benchmark, ancient surface, phase and reference frame, with a signed offset in metres, its convention, bounded uncertainty and source provenance. A concrete pad or modern surveyed height alone cannot supply the ancient surface; broad chronology or mismatched surface phases remain unknown.

Tests use clearly synthetic complete targets to verify every missing/failed gate, frame/datum mismatch, absent negative finding and disturbance failure. Imported-evidence regressions check source precedence, documentary counts/null denominators, shared-feature deduplication, distinct states, IV/17 threshold limits and resolved source/feature references. Running this module adds no inspection/activity/outcome increment.

## Target volumes and excavation footprints

An unsuccessful excavation means little unless we know where the target was, whether the dig reached it, and whether the dig could have detected it. This extension carries those facts together in one join. The brief calls this the AF447 lesson: a search area can look covered when the search could not have found the target.

Files:

- `volume_join.py` is the join library.
- `volume_inputs.json` holds the reviewed target, footprint and field-record entries.
- `test_volume_join.py` holds the tests.
- `evaluate.py` runs the joins. It adds two results and `data.volume_joins`.

Run from the repository root:

```sh
python3 -I research/feature_workbench/coverage/evaluate.py --repo-root .
python3 -I -m unittest discover -s research/feature_workbench/coverage -p 'test_*.py'
```

### Records

A target-volume record holds what a textual instruction defines. It names the entry and lines, the candidate assignment, the frame, the origin feature and point, and the ancient reference surface with its elevation, datum and phase. It also lists branch dimensions: the direction model, the direction sector, the distance band, the depth band and the cubit length. Every unknown value is an explicit null. A missing key is an error.

A footprint record holds what an excavation reached. It names the frame, the cuts (outline, top level and lowest level reached), the vertical datum and the phase reached. It also records disturbance, the recording method, detection limits, documented areas that were not searched, and sources.

A field-record entry names a document, who holds it, whether that holding is verified, and which open parameters it would resolve. A declaration entry names a parameter that no field record can supply. Such a parameter needs a declared model, or a new observation, before any test.

### The join

The join expands each target into branches. Each branch is joined to each footprint. It returns one of four statuses:

- covered: every point of the branch volume lies in a cut whose levels span it.
- partly covered: some of the branch volume lies in a cut, and some does not.
- not covered: every recorded cut lies outside the branch outline, or above or below its levels.
- undeterminable: a needed parameter is missing. The result lists the missing parameters.

The join refuses to compare a target and a footprint drawn in different frames. It also refuses different vertical datums. A refused join becomes undeterminable, with the registration or datum join as the missing parameter.

An unknown datum or reference elevation keeps the result undeterminable. A footprint with no recorded cuts is undeterminable, never not covered. A cut that lies wholly outside the target outline is not covered, even when the datum is unknown.

Every join also carries five components: target position, ancient accessibility, preservation, excavation reach and recording capability. A phase comparison is carried as well. These do not change the spatial status. They must all be established before an unsuccessful dig can be read as a test.

The join computes no detection probability. It never infers that a deposit is absent, whatever the status. A covered branch still needs the six negative-excavation gates above.

Geometry uses the standard library only. Polygons are split into convex pieces and clipped exactly. Overlapping cuts are combined by inclusion and exclusion. Levels are handled in slabs, so a cut that stops halfway gives partial coverage. A direction sector is drawn in 1° steps with an inner and an outer outline. When the two outlines disagree, the result is undeterminable.

### Entry 25 at IV/17

The target is the Entry 25 digging point at the northern opening of IV/17. The project treats IV/17 as an exploratory candidate only. The target has eight branches: two direction models (vertical below the ancient threshold, or horizontal from the opening) times four cubit branches (the 0.40–0.60 m range and samples of 0.40, 0.50 and 0.60 m).

The footprint is the L-656 excavation. Sion places it in the centres of both spaces, beneath animal-activity remains (p. 63, note 11). The footprint has two cuts, one per space. Their outlines and levels are null because no excavation plan, section or level is published. This work rechecked Plan 5 on the archived p. 63 image. It shows the cave outline, pillar, wall stones, two entrance arrows, north arrow and 0–3 m scale. It shows no excavation limits, section lines or levels.

All eight joins are undeterminable. So the chamber-centre excavation does not establish coverage of the northern-threshold target. The description supports neither covered nor not covered.

The vertical branches lack the threshold elevation, its datum and phase, the threshold-zone outline, and the cut outlines, levels and datum. The horizontal branches lack the same reference surface and cut data. They also lack an origin point, a direction sector and a depth band, which the text does not give. The three single-cubit horizontal branches also lack a distance tolerance.

Field records that would resolve these parameters are all in Michael Dadon's IV/17 excavation file, permit L-656. Sion p. 82 (starred editorial note) names the archive of the Archaeology Staff Officer for Judea and Samaria. Its present holding and accession are unverified. No specific request has been sent; the 7 October IAA request concerns the regional cave inventory.

- The original excavation plan, including the north mouth, gives the cut outlines and the threshold outline.
- The section and levels through the northern threshold give the threshold elevation, datum and phase, and bear on ancient access.
- A level register with its benchmark gives the excavation datum and cut levels. The publication does not name one.
- The basket register (656.17, 656.20 and others) may give levels and the deposits reached.
- The locus list gives the phase reached and the state of the deposits near the mouth.
- Method notes would give sieving and detection limits. The publication does not name them.

The origin point, direction sector, depth band, distance tolerance and threshold-zone extent are model choices. No field record can supply them. They must be declared before any test.

### Entry 60 at Tell es-Sultan

The repository has enough to build the records, so the same join runs as a second case. The target is the Entry 60 pit north of Koḥlit, under the exploratory branch Koḥlit = Tell es-Sultan (registry P60-T1). Readings RB-M, RB-P and RB-B share this target. RB-L places the pit at Janoaḥ and is excluded here. The target has two sector branches: the text's "north side" with no bounds, and the legacy 315°–45° sector, which the registry calls an operational choice.

There are two footprints. Kenyon's Trench II / Site O lies on the northern slope (III pp. 173–174). It is recorded in local square ordinates and local heights. Kenyon's 1955–1958 tomb search covered areas north and north-west of the tell (II Figs 14, 91). It skipped the ground just north of the tell (II p. 169). That strip is recorded as a documented non-search, not as an empty area.

All four joins are undeterminable. Entry 60 states no distance from Koḥlit, so the target has no outer limit. No field record can supply that band. The target is defined by a feature, the pit, rather than by a measured offset. Its coverage is therefore an inventory question: were all pits north of the tell recorded?

Records that would resolve the footprint side:

- The Kenyon III plate volume: Trench II plans and sections, the eastern section at local 37.50–38.00 m N / 8.17 m H, and Pl. 111b. The project has no copy.
- Kenyon's field and working records: grid survey, level datum and Trench II registers. III pp. 3–4 place them at the Museum of Archaeology and Anthropology, Cambridge, in 1981. Their current holding is unverified.
- Kenyon III Fig. 1 (p. xxv), a composite sketch plan, could give an approximate common frame for the tell and Trench II. It is link-only and untraced.
- Kenyon II Figs 14 and 91 and Pls XXXIV–XLI locate the tomb areas. They do not give cleared limits or depths.

The pending Garstang Museum, PEF and Nigro requests concern the ground north of the tell before the camp. They could show features there. They do not define the distance band or Kenyon's footprint. No new request is made.

### Limits

All inputs were already in the repository. The p. 63 recheck reinspects an already inspected page. This work adds no source inspection, outcome, identification, coordinate or outreach. It reopens no closed or parked test. It does not touch the reserved XII 10 observation. Puech 2006 and Lefkovits 2000 were not needed. `evaluate.py` fails if the threshold state, cubit range, chord endpoints or Entry 60 registry record drift from the values in `volume_inputs.json`.
