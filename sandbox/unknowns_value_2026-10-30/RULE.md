# Run 25 rule: which missing records would settle the most sandbox verdicts?

Fixed 30 Oct 2026, before the run results are read for this purpose. Owner request, 30 Oct 2026 10:50 America/Los_Angeles: "#6, 7, 8 seem interesting". Exploratory. Sandbox rules in [../README.md](../README.md) apply.

## Question
Runs 1–22 mostly stop at **unknown** or **not discriminating** because a datum is missing. Which missing records, if obtained, would change the most verdicts, and which runs would stay undecided even with every record they name?

## Scope (fixed)
- All 22 runs listed in [../README.md](../README.md), with run 12 addendum A and run 19 addendum A1. Each run's RULE.md and RESULT.md as committed at dbfbf7f.
- Not in scope: main-project tests. The feature workbench's method 6 ("Decisions", `research/feature_workbench/decisions/`) already ranks record dependencies for those. This run reuses its record identifiers and access fields where a record is the same, and compares its own ranking with method 6's at the end.

## Units
- **Verdict unit:** one criterion or relation in one run whose committed result is unknown, not discriminating, fails only on a strict reading, or is called fragile. Each is listed with the run, the criterion id as written in the rule, and the result's wording.
- **Record:** a specific source (edition and pages, plan, map sheet, dataset, image, or person's data) named in a result as missing or decisive, or one the rule's criterion directly needs. A record is named exactly enough that one could tell later whether it was obtained.

## Linking rule (fixed)
A record **could change** a verdict unit only if:
1. the result names it for that unit, **or** the unit's criterion needs a measurement or fact of a kind the record is known (EVIDENCE: table of contents, abstract, catalogue entry, or another source citing it) to contain; and
2. the record is not already read for that unit.
Links resting only on a guess about the record's content are listed separately as INFERENCE links and counted apart.

## Per record
Verdict units it could change (EVIDENCE links; INFERENCE links); runs touched; access state, using the existing categories where they exist (read; on the owner's Mac, online-only; in Drive over the 10 MB connector limit; not in the library; held by a person, request pending); and effort (owner action needed, purchase, request).

## Ranking (fixed)
Primary: number of EVIDENCE-linked verdict units. Ties: more runs touched, then easier access. A second table ranks by EVIDENCE + INFERENCE links. Both are reported.

## Undecidable runs
A run is **structurally undecidable** if, even with every record linked to its units obtained, at least one of its criteria still could not be scored (for example it needs an observation no record holds, such as an unexcavated subsurface feature). These are listed with the reason.

## Comparison with method 6
For records that appear in both, report whether their order agrees, and any record method 6 ranks high that no sandbox run needs, or the reverse.

## Outputs
`out/units.csv`, `out/records.csv`, `out/links.csv`, the two rankings, the undecidable list and RESULT.md. No new hypotheses and no re-scoring of any run.

## Exposure
This run reads only committed sandbox results and method 6 outputs. No new evidence is gathered.
