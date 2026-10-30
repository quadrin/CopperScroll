# Copper Scroll research

Use the accumulated evidence to improve our understanding of the Copper Scroll and its geography. Test particular landmarks and location instructions when the evidence can distinguish them. The user's current question determines the work.

## Choose the work before continuing it

Historical priorities expire. A previous agent's P1, "next", open checkbox, pending request, unfinished tool or proposed test supplies context; it does not authorize or prioritize another session. [ACTIVE_TEST.md](research/ACTIVE_TEST.md) records the current direction. Older plans and handoffs are reference material.

1. Check the branch, recent changes and relevant open PRs before claiming that work is missing. Read ACTIVE_TEST, then the existing result for the question at hand. Follow later corrections and distinguish merged findings from unmerged work.
2. For an explicit user task, do that task. For an open-ended "continue", briefly compare at most three materially different approaches, including synthesis of evidence already held. Choose by the importance of the conclusion that could change and the realistic chance of changing it with available evidence. Being unfinished or easy to execute gives a task no priority.
3. Before substantive research, state in at most four short sentences: the question; the consequential conclusion or decision that could change; the evidence available now and what has already been tried; and the bounded deliverable and stopping point. Put this in the working conversation or the existing note. Do not create a proposal file or scoring system for routine selection.
4. Work on one consequential question at a time. Existing-data analysis, synthesis, testing a competing explanation and correcting a consequential error are valid work. A new source is useful only when it serves that question. A subtask must explain its connection to the same conclusion.
5. Default budget: one bounded pass in the current session. When a needed observation is unavailable, record that dependency and stop that lane. Do not turn it into another catalogue sweep, source hunt, archive reconstruction or tool project. An extension requires a fresh reason why its expected result justifies the work; a newly found loose end is insufficient.
6. Finish with what we learned, the evidence and limits, and what decision changes or why the question should stop here. Update the existing result and ACTIVE_TEST only when they change. A routine session needs no new handoff, framework, checklist or duplicate state file.

## Prevent task multiplication

- Reassess inherited work against the project question before resuming it. Check earlier attempts once; do not repeatedly audit the same history.
- Pending correspondence, unavailable records and inaccessible images are waiting items. Their arrival triggers a relevance check, not automatic processing.
- A first pass that ends inconclusively can be complete. Preserve its result and its exact reopening condition; uncertainty does not create an obligation to keep working.
- Maintenance, source intake, data cleaning, software, visualizations and benchmarks need an explicit user request or a direct dependency of the chosen research question. A prepared benchmark has no automatic claim on the next session.
- Archive figures and build tools only to support the selected work or an explicit user deliverable. Encountering a potentially useful item does not create an archival or implementation task.
- Preserve evidence standards for claims. Exploratory synthesis may use inspected evidence with its limits stated; an independent confirmation claim still needs the controls and unused observation below.
- A justified decision to stop, narrow a claim, reject an approach or change strategy is a useful outcome. File counts, new sources and completed subtasks do not measure it.

## Status files

- ACTIVE_TEST is the single current direction; keep it under 60 lines. PROGRESS_METRICS stays under 40 lines and records formal outcomes from [outcome_ledger.json](research/progress/outcome_ledger.json).
- Report substantive changes in understanding in ordinary prose, with sources and limits. Formal identification/deposit counters retain their existing definitions. Do not inflate them to reward partial work.
- Preserve historical records and existing research/atlas mirrors. Keep waiting requests in their existing record instead of copying them into a work queue. Archive superseded current guidance verbatim when replacing it.
- Replace overlapping instructions rather than appending more workflow. Historical plans and their tests describe the state when written; they must not force current work back into an obsolete queue.

## Tests that can fail

- **Freeze before confirmatory evidence.** Derive constraints from the entry and edition variants before choosing features. In the active test, record a finite, source-justified set of readings, cubit lengths, origins/wall faces, axes, construction phases and numerical tolerances; also fix the decision rule and failure conditions. Commit the parameters relevant to the stated claim before inspecting evidence reserved for that test. Exploratory sourcing and analysis may continue with exposure and choices logged; protect reserved observations and never reuse exploratory evidence as independent confirmation. Report all retained branches and combinations, including misses. Choices learned from already inspected evidence are exploratory. Changing a choice after seeing a result creates a new exploratory model, never a rescue of the frozen test.
- **Give controls the same opportunities.** For a regional identification claim, fix the regional boundary, inventory sources, eligibility rules and candidate/control list before confirmatory scoring. Include excavated, unexcavated, destroyed and status-unknown alternatives, with detection/coverage gaps. Apply the same reading, unit, origin, phase and tolerance search to each control as to the preferred candidate. Record missing data as unknown. Judge discrimination against each control's best permitted fit; a hand-picked comparator or incomplete inventory cannot establish landscape-wide rarity.
- **Require an unseen prediction.** Register one specific predicted observation and its success/failure criterion before revealing a demonstrably unused observation reserved for that test. Audit prior exposure, including derivative plans and descriptions, and separate evidence used to select the model from evidence testing it. A newly downloaded copy of a known observation is not a holdout. If none is available, record that limit and make no confirmatory identification claim.
- **Close the stated test.** End with **supported relative to the registered alternatives**, **rejected**, or **not identifiable from available evidence**, naming the exact claim and surviving branches. Identification support requires discrimination plus the registered unseen prediction; rejection requires contradiction across the retained branches of the stated claim. Missing coverage or unresolved datums can make the result not identifiable. All three are terminal for that evidence/specification. Reopen only for a specified new observation or documented analytical error; preserve the previous result. Neither a broader question nor a new interpretation silently reopens it.
- **Separate claims.** Identify structures independently of whether the listed treasure existed or survives. A landmark match proves neither a deposit nor the whole scroll's historical account. A branch-level test may run before the regional inventory is complete once its own claim, relevant parameters, evidence and failure rule are frozen. Its result is limited to that relation; a conditional branch failure excludes only that branch. A negative excavation counts only with the ancient target volume, phase/datum, excavation reach, disturbance and detection limits established; unexplained earlier removal cannot rescue a failed deposit prediction.

## Evidence and reporting

Starting documents must state the current goal, relevant result, limit and decision directly. Give linked sources descriptive titles and dates; use them to verify those statements. Define abbreviations and entry identifiers on first use. Do not make current guidance depend on a previous conversation, a pending merge, unexplained codes or an unnamed proposal.

Cite exact edition pages and archaeological figures. Mark restorations and distinguish observed remains, published reconstruction, excavator function labels, textual meanings and new inference. Require a textual argument before imposing an archaeological function on the entry. Deduplicate corroboration by original observation/field campaign; source availability and the amount of work done add no identification confidence.

Record coordinates or bounded source-plan areas when justified, with CRS, reference point, direction/path convention, surface, phase and uncertainty. Keep reading, site association, feature identity and position confidence separate. Use [PROGRESS_METRICS.md](research/PROGRESS_METRICS.md) and its source-linked ledger for outcome/coverage definitions; unknown denominators remain null. Preserve conditional exclusions and negative/inconclusive results. Update candidate/map data only when the assessment changes.

## Text and publication

Use Puech, Lefkovits and Milik without requiring an openly licensed replacement edition. Ancient Hebrew is public domain; modern reconstructions, translations, apparatus, commentary and page images have their own rights. Write from the ancient text, cite readings and mark uncertainty. Call a reading edition-based unless the manuscript was checked.

Apply the specific attribution, noncommercial and share-alike terms of each source. Distinguish protected source material from original analysis, factual comparisons and project translations; public GitHub is not inherently incompatible with a noncommercial licence.

## Source continuity and archive

The owner's sources are routed through [drive_index.md](research/sources/drive_index.md), which links the current Drive inventory. The checked-in CSV is a historical snapshot; consult the live index or supplied folder before calling a later source missing. [Methods and Challenge status](research/experimental_approaches/README.md) links the proposals to recorded results and their source folders. Check the relevant existing evidence/access record before searching.

Retrieve the particular source or observation the selected question needs. Record what was inspected, with pages, figures, access limits and provenance. If access fails, report the source, the needed observation and the best stable retrieval route once, then stop that dependency or pursue an independent approach. Do not repeat failed searches without a changed access route.

Preserve the source material and derived figures actually used in an inference or requested deliverable, where reproduction is permitted. Keep captions, scales, north arrows, source URL, extraction details, attribution and reuse terms; use existing asset locations and manifests, including their atlas mirrors. If reproduction is restricted, keep the citation and access note. Bulk figure harvesting, index rebuilding and historical backfill require a reason tied to the selected work or an explicit user request.
