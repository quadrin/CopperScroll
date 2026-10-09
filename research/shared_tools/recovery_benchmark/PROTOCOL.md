# Feature recovery pilot

9 October 2026 UTC / 8 October Los Angeles. Repository base: `897733283606988581155a3c1df0cd235cb7bea9`.

## Stated claim

Evaluate whether a conservative matching procedure recovers named features from redacted descriptions in primary excavation reports and abstains when the retained descriptors leave multiple or incompletely observed alternatives. The independent archaeology establishes the features independently of the Copper Scroll. The benchmark's descriptions, candidate facts and documentary answer keys share those reports. Field accuracy and unseen archaeological confirmation remain unscorable.

The analyst read the reports and answers before selecting the convenience cases. No freeze occurred before that exposure. Preparing packets and hashes now supplies software separation and a reproducible exploratory baseline. Redaction supplies anonymous item/candidate codes; it cannot erase prior knowledge or source recognition. Six fit-excluded relationship expectations are already exposed source facts.

## Inputs and selection

Use the recorded factual selections from Haimi's Dagesh report, Mokary's Migdal Ha-'Emeq report, and Zissu, Ganor and Neugeborn's 'Etri report in [source_grounded_cases.json](source_grounded_cases.json). Each model retains report title, source URL, campaign, named paragraph and figure. HTML articles have no assigned printed/PDF pages. Source rasters and copyrighted article text are excluded; the data contains factual fields and project paraphrases.

Keep thirteen cases: six named source identities, two ambiguous descriptors, one deliberately crafted null, three unresolved ancient truths, and one missing competitor observation. The null descriptor is a test construction, explicitly absent from the six compared reported directions. It says nothing about regional absence. Candidate subsets are convenient alternatives, with no landscape inventory or rarity denominator.

The floor-length cases compare printed report values within chosen +/-0.05 m windows. These windows classify documentary numbers. They have no established relationship to drafting error, survey precision, physical floor boundaries or archaeological tolerances. They cannot validate the separate PR31 floor-chord measurements.

## Decision and failure rules

Check every retained predicate for every candidate. An accepted reported observation gives match or contradiction; missing values and excavator/reconstructed phase inferences give unknown when an observed condition is required. Exclude only a candidate with at least one recorded contradiction. Retain candidates with missing observations irrespective of how completely another candidate matches.

Return a unique documentary match only when one survivor matches every required predicate. Return no compatible candidate only when every candidate has an observed contradiction. Otherwise return insufficient evidence. Evaluate each phase model separately; combining one phase's screw depression with another's functioning settling pit is unavailable.

Report all surviving candidates and each missing/contradictory field. Do not rank survivors by a count of reported matches. Selected site/feature identity supplies no deposit claim, field accuracy or construction date.

## Separation and scoring

`prepare` writes `reviewer/packet.json` and a blank response form separately from `coordinator/answer_key.json` and a hash manifest. Give reviewers only the reviewer directory. Coordinator filenames, source identifiers, source labels, target IDs, reference answers and expected decisions cannot appear in a valid reviewer packet. Exact source facts can still make a familiar case recognizable; disclose that exposure rather than labelling the pilot blind.

Relationship expectations listed in `excluded_from_matching` are removed from matching facts for every candidate and remain available only as separate model forecasts. They cannot appear among selection predicates. Forecast agreement therefore checks a source expectation recovered after matching, with same-report dependence recorded. It supplies no unseen prediction.

`predict` reads only reviewer inputs. `grade` loads the key and verifies the coordinator manifest's hashes. It rejects missing/duplicate response cases, invalid candidate codes, an asserted unique decision without one selected survivor, and altered packet/key content. A documentary recovery requires a genuine unique match against the complete supplied candidate set. Incomplete or unscorable cases never become independent accuracy observations.

This pilot closes with documentary compatibility supported relative to its supplied alternatives. Independent empirical feature accuracy remains not identifiable from available evidence. Changing the model facts, predicates or source readings creates a new exploratory version and retains these outputs.

## Relation to PR31

[PR31](https://github.com/quadrin/CopperScroll/pull/31), pinned at `7504f1f42014a745e1df044abc86d2bba0b90e42`, tests agreement of selected plan chords with printed report dimensions. Its analyst saw the answers and its independent field-reference provenance is unresolved. The read-only [reproduction](outputs/pr31_reproduction.json) recalculates its existing selections without opening images, choosing new points, modifying its branch or changing results.

That pilot addresses measurement definitions. This pilot addresses selection, unknown observations and abstention. Their shared three source reports make them dependent exercises; combining the results supplies no additional independent archaeological evidence.
