# Active test: R11 Greek groups and personal initials

Updated 3 October 2026 UTC. User authorized parallel investigation after parking Jericho. Three threads audited the old calculation, sought an eligible name corpus and designed chance controls. **Stage: exploratory preparation; scoring blocked on corpus acquisition.** This is the sole current-session state. Follow [AGENTS.md](../AGENTS.md).

## Claim, result and limits

Do the seven Greek groups match exact beginnings of independently attested Greek-script personal names in a fixed dated local corpus? The historical claim that they mean personal initials is **not identifiable from available evidence**. No new corpus matches have been computed. Prefix compatibility alone cannot identify a person, entry author, engraving hand or inventory purpose.

The [Phase 4 audit and source review](phases/phase4_summary.md#r11-personal-initials-audit--3-october-2026) distinguishes historical reported counts from reproducible calculations. The previous 4,950-form/six-of-seven Josephus result lacks its committed input, extractor and baseline output. Josephus and all seven groups are already exposed; no verified holdout exists.

## Frozen design before corpus scoring

The [machine-readable protocol](../deep_analysis/greek_personal_initials_protocol.json) fixes the claim, source population, date/region filters, normalization, source exclusions, reading menu, controls and decision rule. It is blocked, not a completed dataset freeze. Source selection must not depend on prefix coverage. Freeze the complete source snapshot, metadata crosswalk, auditable inclusion/exclusion table, selected CSV and hashes in a new commit before any historical prefix scoring. Changing eligibility after scoring creates a new exploratory model.

Primary readings: ΚΕΝ / ΧΑΓ / ΗΝ / ΘΕ / ΔΙ / ΤΡ / ΣΚ. Sensitivities: ΘΕ→ΞΕ, ΤΡ→ΤΡΙ, ΣΚ→ΧΚ or ΞΚ. Their 12 combinations form a conservative sensitivity envelope, not 12 published editions. Proposed ΚΑΓειρας is not an artifact reading; Puech’s cancelled Ι remains inactive. These are existing edition-based readings, not a new manuscript inspection.

Primary population: independently dated Palestinian Jewish bearers localized in Judaea, Galilee or Peraea, with attestation date intervals wholly within 100 BCE–70 CE. Full Part I Palestine 330 BCE–200 CE is a separate sensitivity population. This operational window does not date the scroll. Unknown/doubtful/restored evidence and target-derived 3Q15 attestations are excluded and logged. Greek-script names from every origin section qualify; Greek-origin names alone do not define the corpus. Normalize/deduplicate attested forms, preserve name IDs, and never manufacture Greek spellings from transliteration.

Chance controls preserve each slot’s vowel/consonant pattern and give the union the same reading opportunities. A uniform 24-letter null is secondary. Exact probabilities, all reading results and misses must be disclosed. These are artificial letter controls, not a calibrated model of ancient name formation. No minimum-p selection or historical significance claim is allowed.

## Acquisition blocker and next action

Obtain **Tal Ilan, Lexicon of Jewish Names in Late Antiquity, Part I: Palestine 330 BCE–200 CE (2002)**: [publisher / ebook](https://www.mohrsiebeck.com/en/book/lexicon-of-jewish-names-in-late-antiquity-9783161587931/), DOI10.1628/978-3-16-158793-1, print ISBN9783161476464. Need the complete entry corpus and printed pp.32–54 for description, source exceptions and dating rules, especially p.50. The public preview supplies front matter and pp.1–25 only. Its bibliography includes 3Q15; audit source lineage before accepting names. LGPN supplies useful open infrastructure but no verified complete local dated export was recovered. Stop repeating the checked preview/search routes.

Then extract all eligible records without prefix queries, preserve exclusions and source/page references, commit the complete input freeze, and run the [test runner](../deep_analysis/initials_control.py). Until the input exists, no match rates, chance tails or name-based conclusion can be reported. Synthetic runner tests validate mechanics only.

## Parked Jericho work and accounting

The user parked entry29/Jericho. Preserve its terminal **not identifiable from available evidence** result and [original-report evidence](assessments/entry29_jericho_pools/README.md). Unfolded2001 Plans14/15/23, the A(B)101 wall tie and exact2002 comparison pages remain the acquisition triggers; do not resume their searches now. Archive/source changes remain in [draft PR6](https://github.com/quadrin/CopperScroll/pull/6).

R11 moves from Queued to In progress: 10 in progress, 2 queued. Archaeological source/check counters remain54/61, cartographic intakes5; this metadata/source-design audit and synthetic code verification supply no archaeological inspection, decisive test, identification, outcome-ledger or confidence increment. The Ilan preview is partial onomastic coverage, not a completed eligible name inventory or independent manuscript observation.
