# Koḥlit witness audit — 9 October 2026 UTC / 8 October Los Angeles

**Obtained:** a reproducible witness and assignment dataset for the latest source-2 addendum at commit `897733283606988581155a3c1df0cd235cb7bea9`. This is exploratory analysis of already exposed evidence. It changes no frozen coding, matching rule or rarity result.

The audit covers every positive primary condition in either coder, the nine exposed candidate records, and every merged primary FAIL. It reconstructs the two addendum merges, reads coder A's exact hit IDs from the committed comparison, and recovers coder B's verbal/plan witnesses and grid witnesses whose points survive in `stage1a_units.csv`. Omitted packet-only geometry stays unknown. The inputs include 244 A sheets and 63 B sheets; input hashes are in [outputs/summary.json](outputs/summary.json).

The frozen result contains 120 positive conditions across 94 units, over the full pre-70 inventory. Of those conditions, 79 have only coder A. Three have a manually paired source-feature group in both coders: Sartaba's peristyle pool, Shiloh's two silos, and Tell es-Sultan's spring reservoir. Twenty have compatible citation/class keys but unresolved feature identity. Seventeen have a B MATCH whose exact witness cannot be recovered from committed geometry. One—Sartaba C2—uses different recovered source-feature groups. Citation/class compatibility never establishes feature identity, even when two coders cite the same page and feature class.

## Sartaba: condition agreement conceals assignment disagreement

Both coders select the **same documented peristyle pool** for C1: A `s2z_f3`, B `f16`, Zertal Vol. 4 pp. 471–472. Both use the excavation's eastern-side description and code its date D from the Herodian peristyle. These are two readings of one published excavation account; this audit establishes no independent archaeological confirmation.

Their C2 witnesses differ:

- A `f11`: cemented cave-cisterns, SWP *Mem II* p. 398. A transfers the supplying aqueduct's north-side description to the cisterns. B records the same group as `f20` with no direction.
- B `f14`: northern robbing pits, Zertal Vol. 4 p. 461. A records that group as `s2z_f4` with no unit-relative position. A treats “northern area” as a within-site location; B treats it as a north direction from the unit. Zertal's proposed nineteenth-century digging date is hedged, so both code U. U supplies no ancient date.

Each coder has one branch-B pool/pit assignment, and those assignments have no shared C2 feature. The frozen branch-B MATCH therefore records agreement on existential condition values. It does not establish agreement on a single pool/pit assignment. C3 survey and C3 text remain unknown; no pit-mouth/grave relation is recorded.

The SWP summit pits and Zertal robbing pits share an explicitly reported observation lineage in the B notes; the aqueduct-fed cave-cisterns form a separate group. [CURATION.json](CURATION.json) records these pairings, their provenance and limits. The direction ambiguity and the undated pit are separate gaps.

## Other checks

At **Tell es-Sultan**, A `f89` and B `f88` describe the same 24-by-40-foot spring reservoir, east of the site, with date U. The citations differ: A identifies the passage on *Mem III* p. 223, while B cites the entry start at p. 220. The original passage-page check remains outstanding. Neither recorded witness dates the reservoir's construction. The northern pit and the pit-mouth/grave relation remain unknown.

At **Shiloh**, A `s4_s4f3` and B `f19` pair the Area M silo 2009; A `s4_s4f5` and B `f21` pair Area K silo 1207. Their citation formatting differs, but their feature numbers/areas distinguish the groups. A shared page alone would not have supplied that pairing.

The **main Hel/Rom window has five** frozen primary branch-B positives: S1283, S6040, S2539, S2589 and S3137. The broader pre-70 window adds E357, bringing its total to six. Except Sartaba, at least one B component cannot be recovered without packet-only geometry. This limits the witness audit; it does not overturn their frozen condition values. No primary branch-A positive exists and no coder has a primary C3 text MATCH. Every assignment retains contemporaneity UNKNOWN: D admits any feature dated to 135 CE or earlier, and U leaves its date unresolved. The output summary separates all R1/R2 and main/pre-70 windows; [frozen primary unit records](outputs/frozen_primary_units.json) preserve all 499 units' MATCH/FAIL/UNKNOWN values, branch A survey/text distinction and branch B values.

The candidate records preserve all coded features and their source, direction, date and mouth fields. Yanun, Kh. Yanun and ʿEin el-Ghuweir stopped at Stage 1, so their audit records state that no feature sheet exists. No missing sheet becomes a negative observation.

The 31 FAIL unit-conditions comprise 30 source-2 C2 absences and the earlier S676 C3 survey absence. [outputs/absence_audit.json](outputs/absence_audit.json) preserves their documentary status and marks physical sector/target-volume coverage UNKNOWN. “Cisterns: none” describes the survey entry's site rather than an investigated northern kilometre sector. S241 and S1080 retain the addendum's entry-mapping flags. No survey label establishes excavation reach, detection capability, phase or a searched target volume.

## Files and reproduction

Run from any directory:

```sh
python3 -I /path/to/CopperScroll/research/rarity/kohlit/witness_audit/audit.py
python3 -I /path/to/CopperScroll/research/rarity/kohlit/witness_audit/test_audit.py
```

The output directory contains exact positive [witness records](outputs/witnesses.json), [condition audit](outputs/condition_audit.json) (also CSV), [per-coder assignments](outputs/assignments.json), [candidate features](outputs/candidate_features.json), [unresolved B witnesses](outputs/unresolved_B_matches.json), absence records and the input-hash summary. Outputs omit source quotations and uncommitted packet excerpts. Nine tests passed, including the actual Sartaba result, missing grid geometry, reference-point transfer, two distinct same-page pits, and selecting the grave attached to the same chosen pit. A second run reproduced all nine generated files byte for byte.

**Claim closed: not identifiable from available evidence**—a single shared physical feature assignment with a joint ancient phase and the text's pit-mouth/grave relation. Specific missing direction, phase and mouth evidence would be needed to test that claim further. The current audit supplies an explicit account of those gaps.
