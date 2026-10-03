# Copper Scroll research

Identify the ancient places and specific locations described in the Copper Scroll. Develop and test candidates at the level of individual caves, cisterns, pools, aqueduct segments, tunnel openings, fissures, tombs, walls and other landmarks.

## Evidence and spatial analysis

- Read the entry and its editorial variants before testing a location. Cite edition pages and archaeological figures; retain alternative readings that change the spatial model.
- Propose specific features and coordinates where the evidence permits. A provisional candidate may include an estimated point, a bounded area or a position relative to a source plan. Label its status and explain how it was located.
- Convert directions, distances and depths into explicit spatial hypotheses. State the reference point, direction convention, unit range, terrain surface, construction phase and uncertainty. Test alternative anchors and unit values when they affect the result.
- Distinguish observed remains, published reconstructions and new inferences. Track confidence in the reading, site association, individual feature and geographic position separately.
- Compare supporting and conflicting evidence for every candidate. Trace repeated claims to their original observations and identify independent corroboration.
- When evidence is incomplete, give the most specific defensible candidate, explain the unresolved assumption and identify the next discriminating source or measurement. Use new evidence to revise rankings and geometry.

## Text and publication

Use the available Puech, Lefkovits and Milik editions for research, comparison and citation. Do not make finding an openly licensed replacement transcription a prerequisite for continuing the research or writing the atlas.

Distinguish the ancient Hebrew text from modern editorial reconstructions, translations, apparatus, commentary and page images. The ancient text is public domain; that does not establish permission to reproduce every contribution or image in a modern edition. Prepare project wording from the ancient text, cite the readings used, and mark restorations and uncertainty. Describe an edition-based reading as such; do not call it a new manuscript transcription unless the manuscript was actually checked.

Notes saying a file was “not pushed”, “not committed” or delivered locally record earlier delivery decisions. They do not make all readings in those files private or prohibit publishing original analysis, site identifications, factual comparisons or project-authored translations of the ancient text. When a proposed output reproduces modern protected material, resolve that specific use and continue the unaffected work. Do not infer that a public GitHub repository is inherently incompatible with a noncommercial licence; apply the actual attribution, noncommercial and share-alike terms to the asset concerned.

## Research continuity

Check existing notes and source-access records before searching. Prioritize digital primary sources, original plans, surveys and historical photographs. Record exact pages, figure numbers and access status. Use the existing research files to distinguish a newly accessed source from independent new evidence.

Keep research copies under this directory and `atlas/research/` aligned where both exist. Update candidate evidence and map data when the underlying assessment changes. Geometry records should distinguish site anchors, observed feature footprints and modeled candidate areas, with the coordinate system, source and positional uncertainty.

## Open-question tracker

Use `research/OPEN_QUESTIONS.md` to select and track research work. After each research session, update the affected R question's dated progress, inspected evidence, contradictions, next test and access limits; recompute summary counts and add a change-history entry. Keep `atlas/research/open_questions_tracker.md` byte-identical. Preserve historical Q identifiers in `research/logs/open_questions.md`. Count completed source inspections and explicit tests separately from question closures; retain negative and inconclusive results. Close only the stated question or candidate to the scope supported by the evidence. Update underlying notes, logs and assessments when the evidence changes.

## Plan and map archive

Save every map, plan, layout, section, aerial image, and photograph of geography or ruins encountered during research to GitHub when reproduction is permitted, including material without an immediate candidate application, including relevant extracts from user-supplied files that the user authorizes for archiving. Store source images under `research/assets/plans/` with a matching `atlas/research/assets/plans/` mirror. Preserve captions, scale bars and north arrows where available. Record full source title, author, edition, printed page, PDF/viewer page, figure number, source URL or supplied-file provenance, original-file hash, extraction/crop details, asset hash, attribution and reuse status in an adjacent manifest. Link each asset from its research note. Distinguish source images from tracings and project reconstructions. Do not infer a reuse licence from online access. If uploading a discovered source is restricted, retain its exact link and access limit, and archive an explicitly labelled project tracing where useful. Keep a backfill queue for earlier relevant figures. Archiving alone adds no source-inspection or completed-test KPI.


## Candidate selection and outcome counters

- Derive entry constraints and retained textual alternatives before choosing archaeological candidates. Define the regional search scope and include unexcavated, destroyed and status-unknown alternatives. Source availability does not increase identification confidence.
- Keep observed archaeology, excavator function interpretations and ancient-text meanings separate. Require a textual argument before turning an archaeological label into a Copper Scroll requirement.
- Freeze measurement tolerances, unit ranges, feature origins and control-selection rules before assessing numerical fits. Record plausible alternative features and constraints satisfied by controls; generic resemblance and repeated reports of one observation supply no independent identification.
- Use research/PROGRESS_METRICS.md and research/progress/outcome_ledger.json for headline outcome/coverage counters. Source inspections, map intakes, bounded checks and prepared packets remain activity measures. Add a source-linked outcome row before recomputing a counter; preserve conditions and surviving branches.
- Count conditional model exclusions separately from whole-candidate/site exclusions. Do not treat a missing function argument as proof of absence or infer an overall identification probability from activity totals.
- Audit the ancient target geometry, phase/datum and excavation reach/detection limits before counting a negative excavation result. Do not assume previous removal to rescue a failed candidate. Unknown coverage and inventory denominators remain null, with the missing audit named.
- Deduplicate corroboration by original observation and field campaign. Preserve historical totals, but apply the outcome schema to future summaries and mirror all new metric/ledger records under atlas/research.
