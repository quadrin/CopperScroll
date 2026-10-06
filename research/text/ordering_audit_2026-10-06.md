# Ordering claims: exact arithmetic and counting definitions

6 October 2026 UTC / 5 October Los Angeles. This retrospective audit closes the specified calculation gaps in the [30 September report](deeper_analysis_2026-09-30.md), using existing repository sources at `5a0e9561135fddec6af6030e8c19e52a9dd7edae`. The report, delivered scripts and their outputs remain unchanged. [Runner](../../deep_analysis/ordering_audit.py), [machine-readable results](../../deep_analysis/ordering_audit_results.json), and [exhaustive verification](../../deep_analysis/test_ordering_audit.py) record the calculations and all retained branches.

The later block shows repeated-name clustering under both retained readings at entry23. The arithmetic does not establish geographic proximity. The offering-formula calculation tests entry cooccurrence; its previously reported interpretation as a token-adjacency probability lacks a specified null. The historical full-unit spelling counts remain unreconciled.

## Entry conventions and exposure

The 61 canonical Puech slots include12a. Entries1–19 therefore occupy20 slots;20–59 occupy40. The first16 canonical slots end at entry15, with45 slots remaining. Entry50 has zero-based position50 because12a shifts subsequent labels. The runner retains the I6 mid-line division correction documented in `features.py` (Puech2006 p.179). Every six-slot scan covers all56 windows, including the first and last.

The limited source-token excerpts come from ETCBC `dss` Text-Fabric2.0.1,3Q15: transcription/morphology by Martin G. Abegg Jr., James E. Bowley and Edward M. Cook; conversion by Jarod Jacobs, Martijn Naaijer and Dirk Roorda, licensed [CC BY-NC4.0](https://creativecommons.org/licenses/by-nc/4.0/). Existing display changes are documented in [the builder](../../tools/build_scroll_text.py). This audit joins displayed segments, groups tokens by the canonical concordance with the I6 correction, extracts bounded contexts/annotations and computes statistics. It edits no source text and supplies no new manuscript reading. The JSON carries the same attribution/licence/modification statement.

The existing hand-coded name list, blocks, formula locations and reported outcomes were already exposed. These are conditional, unadjusted arithmetic checks. They supply no confirmatory freeze, unused prediction, new edition adjudication or archaeological identification. The broader hypothesis-selection process and reading alternatives outside this stated audit remain outside its probability models.

## Shared-name adjacency

An adjacent entry pair contributes one when its historical label sets intersect, even if they share multiple labels. Each null gives every linear order of the same distinct entry identities equal weight.

- Entries20–59, Solomon at23:9 shared-name pairs;5 observed adjacent pairs; expected0.45. Exact upper tail=`41/11515140`=`0.00000356052987632`. This reproduces the report's rounded`3.6×10⁻⁶`.
- Entries20–59, Shallum at23:8 shared-name pairs;4 observed; expected0.40. Exact upper tail=`43/411255`=`0.000104557999295`. The report's approximate`9×10⁻⁵` differs from this exact value.
- Entries1–19, restored Koḥlit at15:10 shared-name pairs;1 observed; expected1. Exact upper/lower tails=`0.676202270382`/`0.739576883385`, consistent with the historical permutation estimates.
- Entries1–19, no identifiable name at15:7 shared-name pairs;1 observed; expected0.70. Exact upper/lower tails=`0.533578431373`/`0.855159958720`. Removing the restoration preserves the observed count and changes its null distribution.

The four combinations of these entry15/23 readings are retained. `text/readings.json` supplies the documented alternatives: `e15-kohlit` (Milik1962 DJD D60; Puech2006 restoration) and `e23-shallum` (Puech2006 p.189; Puech2015 p.58). An unidentified name at15 receives no invented shared label. All other labels remain conditional on the historical hand-coded list; this pass does not claim to cover every possible reading in the scroll.

For each shared-name graph, enumerate every subset of adjacency events:1024 early-block subsets or512 later-block subsets, fewer in the altered branches. A feasible subset consists of disjoint paths. Contracting its`k` edges gives`2^c (n−k)!` labeled orders, where`c` counts path components. Cycles and degree above two have zero orders. Expanding`Σ_F (z−1)^|F| count(F)` gives the exact count distribution. This handles dependence among Secacah's overlapping pairs.

Repeated labels cluster in the later block relative to this uniform-order model. The early-block tails leave that specific clustering test inconclusive; they do not establish random compilation or exclude organization by another variable. Entry labels alone give no site location, walking route or distance.

## Offering-formula definitions

The source text has five full formula loci: V7, XI1, XI4, XI11 and XI15, assigned to entries22,50,51,54,55 on the canonical division. II5/entry8 has the bare stem after wood. The JSON records all six local contexts. V6's vessel word is spelled differently (`כאלין`); source morphology supplies the vessel lemma. Some full formulae follow numerals. XI14 also includes an isolated mem marked removed by the modern editor; the context retains that annotation. Thus “immediately after” describes the offering clause after those intervening forms, rather than five identical adjacent token pairs.

With ten canonical entries containing`דמע`:

- All five full formulae cooccur with it. Uniformly choosing five of61 entry slots gives`C(10,5)/C(61,5)=84/1983049=0.0000423590138216`.
- Five of six stem-bearing entries cooccur with it. The hypergeometric upper tail is`933/3966098=0.000235243808902`, reproducing `T6_record.p_cooc`.

Both probabilities measure entry cooccurrence. Neither supplies a literal token-adjacency probability. Such a claim needs independently specified admissible token positions and an appropriate null that preserves relevant syntax and formula opportunities. The historical report's Holm table cannot transfer its “adjacency” interpretation to these entry probabilities. This audit revalidates neither the entire16-test family nor an adjusted significance claim.

The concordance records Milik's reassignment of each full formula to the following item. A descriptive crosswalk places them with canonical entries23,51,52,55,56:2/5 share`דמע`, or2/6 including entry8. This reproduces the report's division sensitivity. The complete Milik slot/null reconstruction remains absent, so no probability under that segmentation is supplied. The physical word order survives reassignment; canonical entry probabilities do not become division invariant. `g-ktbn` also retains`כתבן`/`בתכן` and several meanings. The positional calculation does not decide the consonant, attachment or “written record” interpretation.

## Exact six-slot scan

Both occurrence definitions have four loci in the window50–55. The maximum-over-all-windows null uniformly chooses occurrence slots among61 canonical slots:

- Five full formulae: exact upper tail=`30262/5949147=0.00508677966774`, reproducing the rounded report value`0.005`.
- Six stem occurrences: exact upper tail=`113591/7932196=0.0143202462471`, consistent with the delivered200,000-draw estimate`0.01422`.

A dynamic program counts binary slot assignments by selected count, the preceding five bits and the largest completed-window count. Overlapping windows remain dependent in the calculation. Scanning all positions is accounted for; trying other widths, occurrence definitions, blocks or hypotheses is outside that conditional null. A six-slot span under another segmentation needs its own specification.

## Full-unit spelling and stopping point

Joining source `h` segments exactly as `features.py` does reproduces entry presence6/8: early1,3,6,8,9,11; later29,32,38,46,47,56,58,59. Token counts are6/9 because entry56 has two occurrences. The JSON retains line/word IDs and segment annotations: entry38 includes a modern editorial correction, entry46 a damaged letter. `e38-bars` also records bars/pitchers alternatives that conflict with the displayed full-unit spelling. These flags describe the source representation, rather than newly authenticated manuscript letters.

Phase4T8's7/4 counts have no retained per-entry coding list or sufficient edition-level basis. The discrepancy is **not identifiable from available evidence**. Obtain that specific list/basis before substituting another feature vector or rerunning the Greek-gap claim. This audit changes neither historical Greek-gap output nor textual reading confidence.

Run `python3 deep_analysis/ordering_audit.py` and `python3 -m unittest discover -s deep_analysis -p test_ordering_audit.py -v`. Four checks passed: all64 graphs on four labeled vertices against direct permutations, an overlapping seven-vertex example, disjoint-pair closed-form counts, and every subset for sizes6/8/10 at several scan widths. The output is deterministic and records input SHA256 hashes. One bounded existing-data audit completed; no new primary-source scope, cartographic intake, decisive test, question closure, site/deposit identification or confidence change follows. Reopen the unresolved interpretive claims only for a justified token null, complete alternative segmentation or the missing T8 coding basis.
