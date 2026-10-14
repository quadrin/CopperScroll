# New-resource sweep: evidence changes and actual reading coverage

14 October 2026. This pass checks the new intake against existing source records, traces claims to their original observation and keeps text reading, native visual inspection and publication completeness separate. The [inventory](inventory.csv) identifies the 39 received files by publication and source hash. Its 6,396 PDF viewer units include double-page scans and overlapping browser captures; they are not a count of printed pages read.

Each observation is compared with its existing source chain before integration:

| Relationship to earlier evidence | Treatment |
| --- | --- |
| Same original object, excavation campaign or cited passage | Add provenance or detail to that observation; do not count another corroboration. |
| Later excavation or new measurement | Record the new observation, phase and uncertainty; compare it with the earlier account. |
| Retraction, contradiction or copy error | Preserve both accounts and state exactly which inference changes. |
| New archive locator or interpretive possibility | Record a retrieval lead or exploratory question, with the required next observation. |

## What changes the evidence

**The original papers replace several secondhand attributions and expose an evolving interpretation.** Wolters's1990 vocabulary paper retracts his1988 portions reading and substitutes anointing oil; Mandel1993 disputes the oil, protocol and expanded-key interpretation. These papers cannot count as independent confirmation of a separate deciphering key. The [paper review](copper_changes.md) also separates Pixner's compulsory pre68 deposition model from Taylor's later criticism, records a copy-level east/west caption annotation, and identifies Clark's addition of vessel counts to talent quantities. The existing [source catalogue](https://github.com/quadrin/CopperScroll/blob/research/resource-sweep-2026-10-14/research/sources/sources.md) and [Greek-letter source-access record](https://github.com/quadrin/CopperScroll/blob/research/resource-sweep-2026-10-14/research/phases/phase4_summary.md#6-what-would-decide-the-open-points) now name the directly read originals.

**A later excavation revises the ʿAujah surface-survey model.** Ben-Shlomo2023's2019–2021 excavation report places the proposed barracks in later occupation and reports destruction deposits. The2009 survey's abandonment narrative and architectural dates cannot carry over unchanged. Printed coordinates also conflict between accounts and within the later chapter. The [regional review](regional_changes.md) retains those differences without silently importing a point or transferring a nearby date to a structure.

**The new hydraulic records distinguish observed connections from proposed continuities.** The now-read [MHCSV](zertal_v_changes.md) irrigation appendix reports observable end sections of the Auja–Archelais aqueduct but an unfound middle connection. The Phasaelis courtyard drain and Buqeiʿa tunnel/cistern plans add observed geometry with unresolved construction phases. The [Buqeiʿa chapter review](reference_changes.md#levy-festschrift-buqeiʿa-chapter) preserves remeasurements, partly lost fittings, modern graves beside older remains and a capacity/unit discrepancy. A shared site, name or adjacent potsherd cannot date a particular channel–wall–floor junction.

**Qumran object identities and dating require their own source chains.** The [cave-source review](qumran_changes.md) distinguishes renewed chemical measurements from inherited object provenances and places limits on negative cave surveys. The3Q lamp discussion traces back to one object and derivative drawings; a lamp-family production range does not directly date scroll deposition. A perforated-disc attribution needs the full dated cave inventory, not a bare cave-number match. The earlier11Q arrowhead correction already appears in the2016 volume, so later repetition adds no independent observation.

**Reference works add source controls and retrieval leads.** Sokoloff's [completed readable dictionary pass](lexicon_changes.md) specify a predominantly later Aramaic corpus and explicit exclusions. The [collected-volume review](reference_changes.md) separates firsthand observation from literary/historical reconstruction, identifies PEF Buqeiʿa drafts M/WS/137–138 and other archive locators, and corrects a mat/basket conflict in an out-of-period hoard control through an [erratum](https://github.com/quadrin/CopperScroll/blob/research/resource-sweep-2026-10-14/research/agent_review_2026-10-07/wave1/T02_hoard_match/REPORT.md#sourcecoding-erratum--14-october-2026). The SHA-frozen input remains preserved.

## Copy identity and overlap

- The two Mogilany uploads are complementary PartI and PartII, not duplicate copies. The1991 imprint of PartII and the later advertisement's March1992 publication statement remain separate metadata.
- The file labelled QumranIB contains QumranII2003. That correction was already recorded on28September; this intake adds remaining chapter coverage, not a newly identified volume or the missing1994 pages.
- Abel's file contains tomeII, third edition1967, rather than both volumes. The imprint does not make its inherited source observations new1967 fieldwork.
- Cypros's clipped capture was repaired from the HA54–55 issue already in the corpus. The original1975 note and later accounts of the same campaign add source detail without adding another excavation.
- The image-only Cave1 book is a double-page scan with missing preliminary leaves. Its available copy has now been read throughout. Abel's scan lacks printed pages 74–75 and duplicates 76–77.
- The combined Levy volumes have recoverable paragraph loss in ordinary extraction and several printed-folio jumps. The [recovery record](extraction_recovery.md) distinguishes extracted-text availability from completed reading and physical-copy completeness.

## Coverage and continuation

The Copper Scroll papers' text pass is complete through the supplied PDFs or the identified publisher text; visual reservations and redactions remain explicit in [copper coverage](copper_coverage.json). The regional short works, including Cypros's recovered original, are recorded in [regional coverage](regional_coverage.json). The complete supplied MHCSV text/figures are accounted in [its ledger](zertal_v_coverage.json). A missing full paper in MogilanyII is an editorial absence despite completion of its available text.

The remaining available readable text has now been completed across the long volumes: [Qumran sources](qumran_coverage.json), [Qumran II joined receipts](qumranII2003_union_coverage.json), [Cave 1](cave1_coverage.json), [reference volumes](reference_coverage.json), [Sokoloff](lexicon_coverage.json) and [both Levy volumes](levy2023_union_coverage.json). The Qumran II union distinguishes substantive prose completion from leaves without consumed-content receipts. Native inspection has its own receipts; extraction, contents mapping and keyword searches receive no reading credit.

Safe layout inventories supplement the detailed figure reads for [Mogilany I/II](reference_visual_56_coverage.json), [Jewish Studies I](reference_visual_15_coverage.json) and [Abel](reference_visual_33_coverage.json). The [Levy visual closure](levy_visual_closure_coverage.json) records additional layouts and an unnumbered table. These inventories do not certify full native inspection of every page.

The [supplement recovery](supplements_recovery.md) adds Stroth's full workbook and a publisher video transcode inspected throughout. Workbook context labels and count/weight cells conflict; quantitative reuse requires reconciliation. The original AVI and Gadot's promised map remain unverified or unavailable. The [cemetery plate recovery](plate9_recovery_notes.md) identifies the exact 1993 issue but obtains no plate content.

Whole-publication completion remains false where original leaves or maps are missing, strokes or figure labels are unreadable, or images are withheld. Named examples include Abel pp.74–75 and unlocated maps, Cave 1 preliminaries, Sokoloff pp.778–779, Qumran inventory photographs and dividers, and Levy viewer422 under SULTAN-1. Each ledger retains the exact exception; a completed available-text pass does not clear it.

## Exposure and source preservation

Two inventory facsimiles in *The Caves of Qumran* were viewed before their image scope was established. Their possible target-image exposure is unresolved: [exact record](visual_exposure.json). They and potentially overlapping derivatives cannot supply unseen evidence until the existing protocol's masked human-administrator audit establishes their scope. Further unclassified inventory images are withheld; safe text and other source reading continue. This exploratory pass supplies no confirmatory score.

Full encountered source pages preserve original captions, scales, north arrows and credits in private archives. The [asset register](../../assets/plans/new-batch-2026-10-14/README.md) supplies hashes and member routes without publishing source images or private access identifiers. Public files contain original notes, page locators and hashes. Archive/source availability does not establish reading completion, an independent observation or public redistribution rights. Reader-specific manifests retain exact inspection and source-copy limits.

**Partly obtained:** original-paper corrections, later excavation constraints, hydraulic/provenance observations and recoverable copy repairs; available readable text and safe visual work are integrated, with named copy, legibility and image-reservation gaps retained.
