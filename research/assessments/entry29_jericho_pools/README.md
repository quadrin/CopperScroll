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

Next inspect a complete phase-specific original plan to identify the northern supply branch, its wall reference and vertical/construction contacts. Then repeat independent picks against that defined branch. Route-distance models need a justified starting junction; choosing one to obtain 24 cubits would invalidate the test. This pass leaves the whole candidate open while documenting a tested, nonunique geometry branch.

## Access links and reproducibility

Accessible: Monika Trümper, “Swimming Pools and Water Management in the Eastern Mediterranean World of the 4th to 1st Century BC,” in Jonas Berking, ed., *Water Management in Ancient Civilizations*, Berlin Studies of the Ancient World 53 (2018), pp. 255–296. [Direct publisher PDF](https://edition-topoi.org/download_pdf/bsa_053_10.pdf). File SHA-256 `0d0cd8031e3e03181d67942851017f7a4ae9219f0bc405c97f954b094f7efab7`; 42 PDF pages; printed page = PDF page + 254. Render PDF pages 30–32 at fitz Matrix(2,2) to inspect recorded pixel picks. Run `python measure.py` to regenerate the JSON from the frozen picks. This recomputes manual measurements; it does not automatically reidentify the archaeology.

Unread original books; the links expose publisher/catalogue information:

- Ehud Netzer, *Hasmonean and Herodian Palaces at Jericho: Final Reports of the 1973–1987 Excavations*, Vol. I, *Stratigraphy and Architecture* (Israel Exploration Society, 2001): [publisher record](https://www.israelexplorationsociety.com/product-page/volume-i-stratigraphy-and-architecture-2001). Relevant text pp. 74–84 and plans 14, 17–21; rerouting pp. 92–100 and plans 17–22, as cited by Trümper. Those original pages were not recovered here.
- Ehud Netzer, *The Palaces of the Hasmoneans and Herod the Great* (English edition, 2001): [publisher record](https://www.israelexplorationsociety.com/product-page/the-palaces-of-the-hasmoneans-and-herod-the-great-1), [Google Books record without ebook/reader](https://books.google.com/books/about/The_Palaces_of_the_Hasmoneans_and_Herod.html?id=eGhoQgAACAAJ). Trümper’s credits point to p. 93 / plan 17, p. 96 / plan 19, and p. 7 / plan 20; the last is the surprising printed credit and remains uncorrected. Her bibliography’s edition metadata differs from the English publisher record; exact source edition/pagination needs checking.

New KPI contributions: one scoped Trümper source target and one bounded offset/control check. Puech reinspection adds no target. One conditional candidate assessment is completed with an inconclusive result; decisive tests and question closures remain zero. Current cumulative totals: 22 direct targets, 5 cartographic intakes, 22 bounded checks, 0 decisive tests, 0 closures.



## Kotar follow-up — 2 October 2026, Los Angeles

Netzer’s 1983 original chapter now supplies a complete plan (p. 100), approximately 18 × 13 m for each early pool (p. 101), and a later plan/text identifying Herod’s joining of the pair into one approximately 32 × 18 m basin (pp. 105–106, footnote). This adds a specific conflict with assuming survival of two separate reservoirs into a later-use model. A merged northern basin is a separate possible hypothesis and changes which sides are longer; the earlier offset calculations cannot transfer to it. Candidate confidence remains low and the assessment inconclusive. One new source target and one bounded survival check bring totals to 23 direct targets / 5 map intakes / 23 bounded checks / 0 decisive tests / 0 closures. [Image-checked observations, exact pages and remaining source limits](https://github.com/quadrin/CopperScroll/blob/main/research/assessments/entry29_jericho_pools/kotar-netzer1983.md).
